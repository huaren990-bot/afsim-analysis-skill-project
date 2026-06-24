# PointMass 六自由度 Heun 积分器 -- 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-pointmass-integrator-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────┐
│                PointMassIntegrator                       │
│           （点质 Heun 预测-校正积分器）                      │
├──────────────────────────────────────────────────────────┤
│  + step(state, sim_time_s, dt_s) → new_state            │
│                                                          │
│  - calculateAcceleration(state, t, dt)                   │
│      → translational_accel_mps2 (平动加速度, m/s^2)       │
│      → rotational_accel_rps2   (旋转角加速度, rad/s^2)    │
│      → gravitational_accel_g   (重力加速度, 以g为单位)     │
│                                                          │
│  - propagateUsingAccel(state, dt, g, a, α)              │
│      → 1000G平动限幅 → 体轴过载设定                       │
│      → propagateTranslation(state, a, dt)               │
│      → propagateRotation(state, α, dt)                  │
│                                                          │
│  - updateUsingAccel(state, t, dt, g, a, α)              │
│      → UpdateFuelBurn() → propagateUsingAccel()          │
└──────────┬───────────────────────────────────────────────┘
           │ 读写
           ▼
┌──────────────────────────────────────────────────────────┐
│                  VehicleState                            │
│              （飞行器运动状态容器）                          │
├──────────────────────────────────────────────────────────┤
│  位置: ECEF (m)    速度: WCS惯性 (m/s)                    │
│  姿态: DCM (体→NED) 角速率: 体轴 [p,q,r] (rad/s)          │
│  攻角α / 侧滑角β / α̇ / β̇ / Mach / 动压                   │
│  导出量: LLA / 航向 / 飞行路径角 / 体轴过载                │
└──────────────────────────────────────────────────────────┘
           │ 计算加速度时调用
           ▼
┌──────────────────────────────────────────────────────────┐
│              加速度来源（外部子系统）                        │
│  - 气动模型  → 气动力(升/阻/侧)                            │
│  - 推进模型  → 推力 + 推力矢量                             │
│  - 重力模型  → 重力加速度方向                               │
│  - SAS 控制器 → 旋转角加速度（控制+稳定）                    │
└──────────────────────────────────────────────────────────┘
```

**核心流程**：积分器每帧执行 Heun 预测-校正法（二阶 Runge-Kutta）：
1. 在 t_n 时刻计算加速度 a0
2. 用 a0 预测推进到中间状态（预测步）
3. 在预测态重新计算加速度 a1
4. 取 a_avg = (a0+a1)/2（Heun 平均实现二阶精度）
5. 用 a_avg 从原始状态出发做校正推进（校正步）
6. 更新导出量（气动角、LLA、马赫数、过载等）

## 2. 核心接口定义

### 2.1 VehicleState（飞行器运动状态）

```cpp
// 飞行器运动状态 -- 积分器每帧读写的完整运动状态
// 所有跨帧持久化的状态都存储在此结构体中
struct VehicleState {
    // ======== 平动状态 ========
    double pos_ecef_m[3] = {0, 0, 0};    // ECEF 地心地固位置（m）
    double vel_wcs_mps[3] = {0, 0, 0};   // WCS 惯性系速度（m/s）

    // ======== 转动状态 ========
    double dcm[3][3] = {                  // 方向余弦矩阵 DCM（体轴→NED 坐标转换）
        {1, 0, 0},
        {0, 1, 0},
        {0, 0, 1}
    };
    double omega_body_rps[3] = {0, 0, 0}; // 体轴角速率 [roll, pitch, yaw]（rad/s）

    // ======== 气动状态（每帧由 UpdateAeroState() 更新） ========
    double alpha_rad        = 0.0;  // 攻角（rad）
    double beta_rad         = 0.0;  // 侧滑角（rad）
    double alpha_dot_rps    = 0.0;  // 攻角变化率（rad/s）
    double beta_dot_rps     = 0.0;  // 侧滑角变化率（rad/s）
    double mach             = 0.0;  // 马赫数（无量纲）
    double dynamic_pressure_pa = 0.0; // 动压 q_bar（Pa）

    // ======== 导航导出量（每帧由 CalculateSecondaryParameters() 更新） ========
    double latitude_rad     = 0.0;  // 纬度（rad）
    double longitude_rad    = 0.0;  // 经度（rad）
    double altitude_m       = 0.0;  // 海拔高度（m）
    double heading_rad      = 0.0;  // 航向角（rad，北偏东为正）
    double flight_path_angle_rad = 0.0; // 飞行路径角（rad）

    // ======== 体轴过载（以g为单位，已减去重力分量） ========
    double nx_g = 0.0;  // 纵向过载（体轴X方向，前为正）
    double ny_g = 0.0;  // 横向过载（体轴Y方向，右为正）
    double nz_g = 0.0;  // 法向过载（体轴Z方向，下为正）

    // ======== 诊断值 ========
    double lift_n         = 0.0;  // 升力（N）
    double drag_n        = 0.0;  // 阻力（N）
    double side_force_n  = 0.0;  // 侧力（N）
    double thrust_n      = 0.0;  // 推力（N）
};

// 运动状态的后处理接口（由积分器每帧调用）
// 这些函数的具体实现依赖于坐标系转换和地球模型
class StatePostProcessor {
public:
    // 更新气动状态：根据当前速度和姿态计算 α, β, α̇, β̇, Mach, 动压
    virtual void updateAeroState(VehicleState& state, int64_t sim_time_ns) = 0;

    // 计算导出导航参数：从位置/速度/DCM 导出 LLA / 航向 / 飞行路径角 / 体轴过载
    virtual void calculateSecondaryParameters(VehicleState& state) = 0;
};
```

### 2.2 MassProperties（质量属性）

```cpp
// 质量属性 -- 每帧开始时由飞行器模型更新（含燃油消耗）
struct MassProperties {
    double mass_kg       = 0.0;  // 当前总质量（kg），含剩余燃油
    double base_mass_kg  = 0.0;  // 基准质量（kg），通常为最大起飞质量，用于计算质量比率
    double center_of_mass_m[3] = {0, 0, 0}; // 质心位置（m），体轴系下相对参考点

    // 转动惯量矩阵（kg·m^2），体轴系
    double Ixx = 0.0;  // 绕X轴（滚转）转动惯量
    double Iyy = 0.0;  // 绕Y轴（俯仰）转动惯量
    double Izz = 0.0;  // 绕Z轴（偏航）转动惯量
    double Ixy = 0.0, Ixz = 0.0, Iyz = 0.0;  // 惯性积

    // 质量比率：m / m_base，燃油消耗后减小，飞行器变得更敏捷
    double mass_fraction() const {
        return (base_mass_kg > 0.0) ? (mass_kg / base_mass_kg) : 1.0;
    }
};
```

### 2.3 AccelerationSources（加速度来源接口）

```cpp
// 加速度来源 -- 积分器不关心具体实现，只通过此接口获取加速度
// 具体实现包括：气动模型、推进模型、重力模型、SAS 控制器
class IAccelerationSource {
public:
    virtual ~IAccelerationSource() = default;

    // 计算一个时间点上的全部加速度
    // @param state        当前运动状态（只读）
    // @param mass         当前质量属性（只读）
    // @param sim_time_s   仿真时间（s）
    // @param dt_s         积分步长（s）
    // @param trans_accel  [out] 体轴系平动加速度（m/s^2）
    // @param rot_accel    [out] 体轴系旋转角加速度（rad/s^2）
    // @param grav_accel   [out] 体轴系重力加速度（以 g=9.80665 为单位）
    // @param lift/drag/thrust [out] 诊断用气动力/推力（N）
    virtual void compute(
        const VehicleState& state,
        const MassProperties& mass,
        double sim_time_s,
        double dt_s,
        double trans_accel_mps2[3],
        double rot_accel_rps2[3],
        double grav_accel_g[3],
        double& lift_n,
        double& drag_n,
        double& thrust_n
    ) = 0;
};
```

### 2.4 PointMassIntegrator（积分器主类）

```cpp
// PointMass Heun 积分器 -- 主类
// 使用 Heun 预测-校正法（二阶 Runge-Kutta）推进点质量飞行器的六自由度运动
// 积分器本身不持有跨帧状态（m_vehicle 除外），所有状态存储在 VehicleState 中
class PointMassIntegrator {
public:
    // ======== 配置 ========
    struct Config {
        double max_translational_accel_g = 1000.0; // 平动加速度硬限幅（g），防止碰撞尖峰
        // 标准重力加速度用于将英制 lbf 转换为公制 m/s^2
        double reference_gravity_mps2 = 9.80665;   // g0
    };

    // ======== 构造 ========
    // @param config           积分器配置
    // @param accel_source     加速度来源（气动+推进+重力+SAS 的统一接口）
    // @param post_processor   状态后处理器（气动状态更新 + 导出量计算）
    PointMassIntegrator(
        const Config& config,
        std::unique_ptr<IAccelerationSource> accel_source,
        std::unique_ptr<StatePostProcessor> post_processor
    );

    // ======== 主积分步 ========
    // 用 Heun 预测-校正法推进一个时间步
    // @param state         当前运动状态（被原地修改为下一步状态）
    // @param sim_time_s    当前仿真时间（s）
    // @param dt_s          积分步长（s）
    void step(VehicleState& state, double sim_time_s, double dt_s);

private:
    Config config_;
    std::unique_ptr<IAccelerationSource> accel_source_;
    std::unique_ptr<StatePostProcessor> post_processor_;

    // ======== 内部辅助方法 ========

    // 使用给定加速度推进临时状态
    // 包含 1000G 限幅 + 平动推进 + 转动推进（半隐式欧拉）
    void propagateUsingAccel(
        VehicleState& state, double dt_s,
        const double grav_accel_g[3],
        const double trans_accel_mps2[3],
        const double rot_accel_rps2[3]
    );

    // 平动推进：v += a*dt, r += v*dt
    void propagateTranslation(VehicleState& state, double dt_s,
                              const double accel_mps2[3]);

    // 转动推进（半隐式欧拉）：ω += α*dt, 然后用新ω更新四元数姿态
    void propagateRotation(VehicleState& state, double dt_s,
                           const double alpha_rps2[3]);
};
```

## 3. 典型调用模式

```cpp
// ======== 1. 初始化阶段：组装积分器 ========

// 创建加速度来源（组合气动、推进、重力、SAS 的综合实现）
auto accel_source = std::make_unique<MyAccelerationSource>(
    aero_model,       // 气动模型实例
    propulsion_model, // 推进模型实例
    gravity_model,    // 重力模型实例
    sas_controller    // SAS 控制器实例
);

// 创建状态后处理器
auto post_processor = std::make_unique<MyStatePostProcessor>(earth_model);

// 创建积分器
PointMassIntegrator::Config config;
config.max_translational_accel_g = 1000.0;  // 1000g 限幅
config.reference_gravity_mps2    = 9.80665; // 标准重力加速度

PointMassIntegrator integrator(config,
    std::move(accel_source), std::move(post_processor));

// ======== 2. 初始化运动状态 ========
VehicleState state;
// 设置初始位置（ECEF，米）
state.pos_ecef_m[0] = 6378137.0;   // 赤道半径附近
state.pos_ecef_m[1] = 0.0;
state.pos_ecef_m[2] = 0.0;
// 设置初始速度
state.vel_wcs_mps[0] = 0.0;
state.vel_wcs_mps[1] = 0.0;
state.vel_wcs_mps[2] = 0.0;
// DCM 默认为单位矩阵（体轴与 NED 对齐：机头朝北、水平）

// ======== 3. 仿真主循环 ========
double sim_time = 0.0;
double dt       = 1.0 / 60.0;  // 60 Hz 物理帧率（约 16.67 ms）

for (int frame = 0; frame < 36000; ++frame) {  // 仿真 10 分钟
    // 每帧调用一次积分步 -- state 被原地更新
    integrator.step(state, sim_time, dt);
    sim_time += dt;

    // 使用更新后的状态做日志/可视化/数据链输出
    // state.alpha_rad       -- 当前攻角
    // state.mach           -- 当前马赫数
    // state.latitude_rad   -- 当前纬度
    // state.altitude_m     -- 当前高度
    // state.nx_g / ny_g / nz_g -- 体轴过载
    log_frame(sim_time, state);
}
```

### Heun 预测-校正法内部流程示意

```cpp
void PointMassIntegrator::step(VehicleState& state, double t, double dt) {
    // 1. 更新质量属性（含本帧燃油消耗）
    MassProperties mass = get_current_mass_properties();

    // 2. 保存原始状态（校正步从原始状态出发，而非预测态）
    VehicleState state_original = state;

    // 3. Heun Step 1: 在 t_n 时刻计算加速度 a0
    double a0[3], alpha0[3], g0[3];
    double lift0, drag0, thrust0;
    accel_source_->compute(state, mass, t, dt, a0, alpha0, g0,
                           lift0, drag0, thrust0);

    // 4. Heun Step 2: 预测步 -- 用 a0 推进到临时中间状态
    VehicleState state_predictor = state;
    propagateUsingAccel(state_predictor, dt, g0, a0, alpha0);

    // 5. Heun Step 3: 在预测态 (t_{n+1}) 重新计算加速度 a1
    double a1[3], alpha1[3], g1[3];
    double lift1, drag1, thrust1;
    accel_source_->compute(state_predictor, mass, t + dt, dt,
                           a1, alpha1, g1, lift1, drag1, thrust1);

    // 6. Heun 平均 -- 梯形法则取两端点算术平均，实现二阶精度
    double a_avg[3], alpha_avg[3], g_avg[3];
    for (int i = 0; i < 3; ++i) {
        a_avg[i]     = (a0[i] + a1[i]) * 0.5;          // 平均平动加速度 (m/s^2)
        alpha_avg[i] = (alpha0[i] + alpha1[i]) * 0.5;   // 平均旋转加速度 (rad/s^2)
        g_avg[i]     = (g0[i] + g1[i]) * 0.5;           // 平均重力加速度 (g)
    }

    // 7. 从预测态拷贝诊断值（升力/阻力/侧力/推力/重量取自预测态）
    state.lift_n   = lift1;
    state.drag_n  = drag1;
    state.thrust_n = thrust1;

    // 8. Heun Step 4: 校正步 -- 用平均加速度对 *原始状态* 做完整推进
    //    从原始状态出发（而非预测态），确保不引入预测态的单步误差
    state = state_original;
    updateUsingAccel(state, t, dt, g_avg, a_avg, alpha_avg);

    // 9. 后处理：更新气动角和导出量
    post_processor_->updateAeroState(state, static_cast<int64_t>(t * 1e9));
    post_processor_->calculateSecondaryParameters(state);
}
```

## 4. 坐标系/单位约定

### 4.1 坐标系

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **Body（体轴系）** | X=前, Y=右, Z=下 | 加速度输入/输出、角速率、过载 |
| **NED（北东地）** | X=北, Y=东, Z=下 | 姿态 DCM 参考系、导航输出 |
| **WCS / ECEF** | 地心地固 | 位置和速度的绝对参考系 |
| **Wind（气流系）** | X=相对气流方向 | 攻角α/侧滑角β的定义参考 |

### 4.2 单位约定（SI）

所有接口统一使用 **SI 单位制**：

| 物理量 | 单位 | 说明 |
|--------|------|------|
| 位置 | m | ECEF 坐标 |
| 速度 | m/s | WCS 惯性系 |
| 加速度（平动） | m/s^2 | 体轴系 |
| 角加速度（旋转） | rad/s^2 | 体轴系 |
| 角速率 | rad/s | 体轴 [p, q, r] |
| 角度（α, β, 姿态等） | rad | |
| 时间 | s | |
| 质量 | kg | |
| 力（升力/阻力/推力） | N | |
| 转动惯量 | kg·m^2 | |
| 重力加速度 | 以 g (9.80665 m/s^2) 为单位 | 用于 Heun 平均 |
| 过载 | g（9.80665 m/s^2） | 体轴分量 |
| 动压 | Pa | |
| 仿真时间戳 | s（接口层），内部可用 ns | |

注意：AFSIM 原始代码混合使用 Imperial（lb, ft, slug）和 SI 单位。本接口规格已将全部单位统一为 SI。

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|----------|----------|
| `PointMassIntegrator` (wsf框架类) | 积分器主类 | `PointMassIntegrator` class（本章定义） |
| `PointMassMover` | 飞行器容器（持有状态+各子系统） | 拆分为独立接口：`VehicleState` + `IAccelerationSource` + `StatePostProcessor` |
| `KinematicState` | 运动状态容器（框架类） | `VehicleState` struct（本章定义） |
| `MassProperties` (框架类) | 质量属性容器 | `MassProperties` struct（本章定义） |
| `P6DofForceAndMomentsObject` | 力/力矩容器 | 不纳入接口；加速度直接以 `double[3]` 传递 |
| `UtVec3dX` | 三维矢量 | `double[3]` 原生数组 |
| `UtDCM` / `UtQuaternion` | 姿态表示 | `double[3][3]` DCM 矩阵 |
| `UtMath::Limit()` | 数值限幅 | `std::clamp()` |
| `P6DofFreezeFlags` | 测试冻结标志 | 移除；测试模式由外部另行处理 |
| `UtMath::cREFERENCE_GRAV_ACCEL_MPS2` | 数学常量 | 配置项 `reference_gravity_mps2`（默认 9.80665） |
| 燃油消耗逻辑（`UpdateFuelBurn`） | 质量更新 | 纳入 `IAccelerationSource` 或由外部在调用 `step()` 前执行 |
