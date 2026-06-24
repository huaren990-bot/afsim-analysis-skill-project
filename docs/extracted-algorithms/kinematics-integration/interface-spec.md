# 运动学积分器 — 接口规格

> **日期:** 2026-06-10
> **状态:** draft
> **对应算法卡:** flight-dynamics-p6dof-heun-integrator-card.md, flight-dynamics-pointmass-sas-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────┐
│              Integrator                  │
│  (Heun Modified Euler + Quaternion)      │
├──────────────────────────────────────────┤
│  + update(vehicle, simTime, dt)         │
│  - calculateFM(state, time, dt) → F,M   │
│  - propagateUsingFM(state, dt, F, M)     │
│  - updateUsingFM(state, time, dt, F, M)  │
│  - propagateTranslation(state, a, dt)    │
│  - propagateRotation(state, α, dt)       │
└──────────┬───────────────────────────────┘
           │ uses
           ▼
┌──────────────────────────────────────────┐
│          Kinematic State                 │
│  (Position, Velocity, Attitude, Rates)   │
├──────────────────────────────────────────┤
│  Position:  WGS84 / Spherical Earth      │
│  Velocity:  WCS inertial / NED           │
│  Attitude:  DCM (Direction Cosine Matrix)│
│  Rotation:  body ω, body ω_dot           │
│  Aero:      α, β, α_dot, β_dot, Mach, q̄ │
└──────────────────────────────────────────┘
           │ computed by
           ▼
┌──────────────────────────────────────────┐
│        Force & Moment Sources            │
│  - Aerodynamics (stability derivatives)  │
│  - Propulsion   (thrust + moment)        │
│  - Landing Gear (ground reaction)        │
│  - Gravity      (WGS84 or spherical)     │
└──────────────────────────────────────────┘
```

## 2. 核心接口定义

### 2.1 IntegrationResult（集成结果）

```cpp
struct IntegrationResult {
    // Position (m, WGS84 ECEF or spherical)
    double pos_ecef[3];

    // Velocity (m/s, WCS inertial)
    double vel_wcs[3];

    // Attitude as DCM (body-to-NED)
    double dcm[3][3];

    // Body angular rates (rad/s)
    double omega_body[3];  // [roll, pitch, yaw]

    // Aerodynamic state
    double alpha_rad;       // angle of attack
    double beta_rad;        // sideslip angle
    double mach;            // Mach number
    double dynamic_pressure_pa;  // q_bar (Pa)

    // Derived navigation state
    double latitude_deg;
    double longitude_deg;
    double altitude_m;

    double heading_deg;     // local heading
    double flight_path_angle_rad;

    // Body g-loads (minus gravity component)
    double nx_g, ny_g, nz_g;

    // Diagnostics
    double lift_n, drag_n, side_force_n;
    double thrust_n;
    double moment_nm[3];   // [roll, pitch, yaw]
    double mass_kg;
};
```

### 2.2 FrameConversion（坐标系转换工具）

```cpp
// Direction cosine matrix: body frame → NED frame
// Implements 3-2-1 Euler rotation (yaw → pitch → roll)
struct DCM {
    double m[3][3];

    // Rotate vector from body to NED
    Vec3 body_to_ned(const Vec3& v_body) const;

    // Rotate vector from NED to body
    Vec3 ned_to_body(const Vec3& v_ned) const;

    // Convert to quaternion
    Quaternion to_quaternion() const;

    // Create from quaternion
    static DCM from_quaternion(const Quaternion& q);

    // Create from Euler angles (rad, yaw-pitch-roll)
    static DCM from_euler(double yaw, double pitch, double roll);
};
```

### 2.3 Quaternion（四元数）

```cpp
struct Quaternion {
    double w, x, y, z;  // scalar-first convention

    // Quaternion multiplication (Hamilton product)
    Quaternion operator*(const Quaternion& q) const;

    // Rate quaternion: q_dot = 0.5 * q ⊗ [0, ω]
    static Quaternion rate(const Quaternion& q, const Vec3& omega_body);

    // Normalize (critical for numerical stability)
    void normalize();

    // Convert to DCM
    DCM to_dcm() const;
};
```

### 2.4 ForceMomentSource（力/力矩源接口）

```cpp
struct ForceMoment6DOF {
    Vec3 force_body_n;      // force in body coordinates (N)
    Vec3 moment_body_nm;    // moment in body coordinates (N·m)
    Vec3 application_point_m; // force application point relative to RP (m)
};

// Abstract interface for any force/moment source
class IForceSource {
public:
    virtual ~IForceSource() = default;

    // Compute forces and moments at a given state and time
    virtual ForceMoment6DOF compute(
        const IntegrationResult& state,
        double sim_time_s,
        double dt_s
    ) = 0;
};

// Concrete implementations:
//   AerodynamicsFM   — stability-derivative lookup tables
//   PropulsionFM     — engine thrust + moment
//   LandingGearFM    — ground reaction + friction
//   GravityFM        — WGS84 or spherical gravity
```

### 2.5 Integrator（积分器主接口）

```cpp
class HeunIntegrator {
public:
    // Configuration
    struct Config {
        double max_acceleration_g = 1000.0;   // g-force limit
        double max_angular_acceleration_rps2 = 3600.0; // rad/s² limit
        bool use_spherical_earth = false;     // spherical vs WGS84
        bool use_rotating_earth = false;      // Coriolis effects
        double spherical_earth_radius_m = 6366707.0;
    };

    HeunIntegrator(const Config& config,
                   std::vector<std::unique_ptr<IForceSource>> sources);

    // Main integration step
    IntegrationResult step(
        const IntegrationResult& state,
        double sim_time_s,
        double dt_s
    );

private:
    Config config_;
    std::vector<std::unique_ptr<IForceSource>> force_sources_;

    // Internal Heun method
    void heun_step(const IntegrationResult& s0, double t0, double dt,
                   IntegrationResult& s1,
                   Vec3& total_force, Vec3& total_moment);
};
```

## 3. 典型调用模式

```cpp
// 1. Setup integrator with force sources
auto sources = std::vector<std::unique_ptr<IForceSource>>{};
sources.push_back(std::make_unique<AerodynamicsFM>(aero_config, aero_tables));
sources.push_back(std::make_unique<PropulsionFM>(engine_config));
sources.push_back(std::make_unique<GravityFM>(earth_model));

HeunIntegrator::Config config;
config.use_spherical_earth = false;
HeunIntegrator integrator(config, std::move(sources));

// 2. Initialize state
IntegrationResult state;
state.pos_ecef = {1000000, -5000000, 3000000}; // WGS84 ECEF (m)
state.vel_wcs  = {0, 0, 0};                     // initial velocity
state.dcm      = DCM::from_euler(0, 0, 0);      // facing north, level

// 3. Simulation loop
double sim_time = 0.0;
double dt = 1.0 / 60.0;  // 60 Hz physics

for (int frame = 0; frame < 36000; frame++) {  // 10 minutes
    state = integrator.step(state, sim_time, dt);
    sim_time += dt;

    // output state for logging / visualization
    log_state(sim_time, state);
}
```

## 4. 坐标系约定

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **Body** | X=前, Y=右, Z=下 | 气动力/力矩、推力 |
| **NED** | X=北, Y=东, Z=下 | 导航输出 |
| **WCS** (ECEF) | 地心地固 | WGS84 位置/速度 |
| **Spherical** | 球面地心惯性 | 简化的球面地球模型 |

## 5. 单位约定

所有新实现统一使用 **SI 单位制**：
- 位置: m
- 速度: m/s
- 加速度: m/s²
- 角度: rad
- 角速率: rad/s
- 质量: kg
- 力: N
- 力矩: N·m
- 转动惯量: kg·m²
- 压力: Pa
- 密度: kg/m³

（AFSIM 原始代码大量使用了 Imperial 单位：ft, lb, slug, psf。）

## 6. 框架依赖解耦

| AFSIM 原始依赖 | 替换方案 |
|---------------|----------|
| `P6DofVehicle` | 自定义 `VehicleModel` 聚合体 |
| `P6DofKinematicState` | `IntegrationResult` struct (上) |
| `P6DofForceAndMomentsObject` | `ForceMoment6DOF` struct (上) |
| `UtDCM` / `UtQuaternion` | 自定义 `DCM` / `Quaternion` (上) |
| `UtTable::Table` | 自定义 `MultivariateLookupTable` |
| `P6DofFreezeFlags` | 移除（测试模式下另行处理） |
| `UtMath` | `std::clamp` 或自定义 `clamp` |
