# NORAD SGP4/SDP4 轨道传播器 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** space-norad-orbital-propagator-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│            WsfNORAD_OrbitalPropagator                 │
│  (SGP4/SDP4 解析轨道传播器)                            │
├──────────────────────────────────────────────────────┤
│  + Initialize(initialTime) → bool                    │
│  + Propagate(currentTime)                            │
│  + PostPropagate()                                   │
│  + UpdateOrbitalState()                              │
│  - SelectEphemeris() → int                           │
│  - SGP4_init() / SGP4(tsince)                       │
│  - SDP4_init() / SDP4(tsince)                       │
│  - SGP8_init() / SGP8(tsince)                       │
│  - SDP8_init() / SDP8(tsince)                       │
└──────────┬───────────────────────────────────────────┘
           │ 包含
           ▼
┌──────────────────────────────────────────────────────┐
│                tle_t (TLE 数据结构)                    │
│  epoch, xno, eo, xincl, xnodeo, omegao, xmo, bstar  │
│  xndt2o, xndd6o                                      │
├──────────────────────────────────────────────────────┤
│  来源: UtTwoLineElement                               │
└──────────┬───────────────────────────────────────────┘
           │ 驱动
           ▼
┌──────────────────────────────────────────────────────┐
│            WsfNORAD_Util (核心数学库)                  │
│  + sxpx_common_init(params, tle, init, deep_arg)     │
│  + sxpx_posn_vel(node, a, e, params, ..., pos, vel)  │
│  + Deep_dpinit(tle, deep_arg)                        │
│  + Deep_dpsec(tle, deep_arg)                         │
│  + Deep_dpper(deep_arg)                              │
│  + FMod2p(x) → double                                │
│  + ThetaG(jd) → double (static)                      │
└──────────────────────────────────────────────────────┘
```

## 2. 核心接口定义

### 2.1 tle_t（TLE 双行轨道根数）

```cpp
// 从 NORAD 双行轨道根数 (TLE) 中提取的 9 个经典轨道要素
// 全部采用 rad 和 rad/min 单位制
struct tle_t {
    double epoch;   // TLE 历元时刻 (Julian Date, 儒略日)
                    // 参考 UTC，表示自公元前 4713 年 1 月 1 日 12:00:00 起的天数
    double xndt2o;  // 平运动一阶时间导数 (rad/min²)
                    // 即 ṅ₀ / 2，常用于计算大气阻力引起的轨道衰减
    double xndd6o;  // 平运动二阶时间导数 / 6 (rad/min³)
                    // 即 n̈₀ / 6
    double bstar;   // B* 阻力项 (1/地球半径)
                    // 弹道系数的修正参数，驱动力大气阻力模型
    double xincl;   // 轨道倾角 (rad)
                    // 轨道面与赤道面的夹角，0=赤道轨道，π/2=极轨道
    double xnodeo;  // 升交点赤经 RAAN (rad)
                    // 春分点方向到升交点方向的角距
    double eo;      // 偏心率 (无量纲)
                    // 0=圆轨道，0<e<1=椭圆轨道
    double omegao;  // 近地点幅角 (rad)
                    // 升交点到近地点的角距
    double xmo;     // 历元平近点角 (rad)
                    // 卫星在历元时刻的平均角位置
    double xno;     // 平运动 (rad/min)
                    // 卫星的平均角速度，输入时已乘以 60（从 rad/sec 转换为 rad/min）
};
```

### 2.2 deep_arg_t（深空摄动参数集）

```cpp
// SDP4/SDP8 深空传播所需的日月引力摄动参数
// 包含 80+ 个中间计算量和周期项系数
struct deep_arg_t {
    // === 公共参数（SGP4 和 SDP4 共用）===
    double aodp;         // 恢复的原始半长轴 (地球半径)
    double cosio, sinio; // cos(i₀), sin(i₀)
    double omgdot;       // 近地点幅角长期变化率 ω̇ (rad/min)
    double xmdot;        // 平近点角长期变化率 Ṁ (rad/min)
    double xnodot;       // 升交点赤经长期变化率 Ω̇ (rad/min)
    double xnodp;        // 恢复的原始平运动 n₀'' (rad/min)
    double betao, betao2;// β₀ = √(1-e₀²), β₀²
    double eosq;         // e₀²
    double theta2;       // cos²(i₀)

    // === 深空专用：dpsec 和 dpper 的中间变量 ===
    double xll, omgadf, xnode, em, xinc, xn, t;
    // xll: 平经度, omgadf: 近地点幅角(含长期项)
    // xnode: 升交点经度, em: 偏心率(含长期项), xinc: 倾角(含长期项)
    // xn: 平运动(含长期项), t: 距历元时间

    // === 共振轨道系数（12小时 e>0.5 或 地球同步）===
    double d2201, d2211, d3210, d3222, d4410, d4422,
           d5220, d5232, d5421, d5433;
    // 格式 d(l)(m)(p)(q): 对共振项的傅里叶系数

    // === 日月摄动周期项系数 ===
    double sse, ssi, ssl, ssg, ssh;  // 太阳长期项
    double se2, si2, sl2, sgh2, sh2; // 太阳周期项 2 阶
    double se3, si3, sl3, sgh3, sh3; // 太阳周期项 3 阶
    double sl4, sgh4;                // 太阳周期项 4 阶
    double ee2, e3, xi2, xi3, xl2, xl3, xl4; // 月球周期项
    double xgh2, xgh3, xgh4, xh2, xh3;        // 月球周期项

    // === 积分状态 ===
    double atime;    // 上次积分时刻
    double xli;      // 当前平经度
    double xni;      // 当前平运动
    double xfact;    // xni - xnq + 长期项

    // === 深空常数 ===
    double xnq;      // 初始平运动快照
    double xqncl;    // 初始倾角快照
    double omegaq;   // 初始近地点幅角快照
    double thgr;     // 历元时刻的 Greenwich 时角
    double preep;    // 上次日月项计算的天数
    double savtsn;   // 上次周期摄动计算的时间

    int resonance_flag;    // 共振轨道标志
    int synchronous_flag;  // 同步轨道标志

    // ... 以及更多中间变量（共 87 个 double + 2 个 int）
};
```

### 2.3 WsfNORAD_OrbitalPropagator（主传播器类）

```cpp
class WsfNORAD_OrbitalPropagator : public WsfNonClassicalOrbitalPropagator {
public:
    // === 星历类型枚举 ===
    enum EphemerisType {
        cSGP  = 0,  // 简化通用摄动 (Simplified General Perturbations)
        cSGP4 = 1,  // SGP4 — 近地轨道标准模型
        cSGP8 = 2,  // SGP8 — 近地轨道扩展模型
        cSDP4 = 3,  // SDP4 — 深空轨道标准模型（含日月引力）
        cSDP8 = 4   // SDP8 — 深空轨道扩展模型（含日月引力）
    };

    // === 构造/析构 ===
    WsfNORAD_OrbitalPropagator();
    // 默认构造：初始化轨道状态为 TEME 坐标系、WGS84 地球模型

    WsfNORAD_OrbitalPropagator(const WsfNORAD_OrbitalPropagator& aSrc);
    // 拷贝构造：深拷贝所有 params、位置、速度和星历类型

    // === 初始化 ===
    bool Initialize(const UtCalendar& aInitialTime) override;
    // 输入: aInitialTime — 仿真起始时间
    // 流程: TLE 解析 → 星历选择(SGPx vs SDPx) → 对应初始化函数 → 基类初始化
    // 返回: true=成功, false=TLE 数据不完整

    // === 轨道状态设置 ===
    bool SetInitialOrbitalState(const ut::OrbitalState& aState) override;
    // 输入: aState — 轨道状态（可为 Cartesian 或 Keplerian）
    // 若状态不含有效的平均轨道要素，则调用 WsfNORAD_PropagatorInverter 反演 TLE

    // === 传播 ===
    void Propagate(const UtCalendar& aTime) override;
    // 输入: aTime — 目标预报时刻
    // 计算 tsince = (aTime - epoch) / 60 (分钟)
    // 根据星历类型分派到 SGP/SGP4/SGP8/SDP4/SDP8

    void UpdateOrbitalState() override;
    // 将 mPropagatedOrbitalState 写入基类的轨道状态

    void PostPropagate() override;
    // 传播后的后处理:
    //   1. 位置: km → m (乘以 1000)
    //   2. 速度: km/min → m/s (乘以 1000/60)
    //   3. 写入 mPropagatedOrbitalState

    // === 查询 ===
    int GetEphemerisType() const;
    // 返回当前使用的星历类型 (0-4)

    bool HyperbolicPropagationAllowed() const override { return false; }
    // NORAD 传播器不支持双曲线轨道

private:
    static const int N_SAT_PARAMS = 98; // 11 + 87 (DEEP_ARG_T_PARAMS)
    ut::OrbitalState mPropagatedOrbitalState; // 传播后的轨道状态
    std::unique_ptr<WsfNORAD_Util::tle_t> tle; // TLE 数据
    bool mSimpleFlag; // 简化模式标志（近地点 < 220 km 时启用）
    int mEphem;       // 星历类型 (0-4)
    double params[N_SAT_PARAMS]; // 传播器参数数组（供各 SXP 函数共用）
    double mPos[3];   // ECI 位置 (km)
    double mVel[3];   // ECI 速度 (km/min)
};
```

### 2.4 WsfNORAD_Util（核心数学函数库）

```cpp
namespace WsfNORAD_Util {

// === 角度归一化 ===
double FMod2p(double x);
// 将角度 x 归一化到 [0, 2π) 范围
// 输入: x — 任意角度 (rad)
// 返回: fmod(x, 2π)，若结果 < 0 则加 2π

// === 通用 SXP 初始化 ===
void sxpx_common_init(double* params, const tle_t* tle,
                      init_t* init, deep_arg_t* deep_arg);
// 对 SGP4/SDP4/SGP8/SDP8 通用的初始化逻辑
// 计算内容:
//   1. 恢复原始平运动 n₀'' 和半长轴 a₀''
//   2. 计算长期摄动系数 (Ṁ, ω̇, Ω̇)
//   3. 计算大气阻力系数 (C₁, C₄)
//   4. 计算短周期项系数 (x3thm1, x1mth2, x7thm1, ...)
//   5. 计算 J3 周期项系数 (xlcof, aycof)
// 输出: params[0..8] 填入了 x3thm1, x1mth2, c1, c4, xnodcf, t2cof, xlcof, aycof, x7thm1
//       deep_arg 填入了 aodp, cosio, sinio, omgdot, xmdot, xnodot, xnodp 等

// === 位置/速度计算 ===
void sxpx_posn_vel(double xnode, double a, double e,
                   const double* params,
                   double cosio, double sinio, double xincl,
                   double omega, double xl,
                   double* pos, double* vel);
// 从修正后的轨道要素计算 TEME 坐标系的位置和速度
// 输入:
//   xnode — 升交点经度(含长期+短周期修正)
//   a     — 半长轴(含大气阻力修正)
//   e     — 偏心率(含大气阻力修正)
//   params — 初始化系数数组
//   cosio, sinio — cos(i₀), sin(i₀)
//   xincl — 轨道倾角
//   omega — 近地点幅角(含长期修正)
//   xl    — 平经度 = M + ω + Ω
// 输出:
//   pos[3] — TEME 位置 (km)
//   vel[3] — TEME 速度 (km/min)
// 内部步骤:
//   1. Kepler 方程 Newton 迭代 → 偏近点角
//   2. 偏近点角 → 真近点角 → 纬度幅角
//   3. 短周期摄动修正 (rk, uk, xnodek, xinck)
//   4. 方向余弦矩阵 (TEME 坐标系)
//   5. 位置 = rk * U, 速度 = ṙk * U + rk*ḟk * V

// === 深空日月引力初始化 ===
void Deep_dpinit(const tle_t* tle, deep_arg_t* deep_arg);
// 初始化日月引力摄动计算的初值
// 计算格林威治时角、日月长期/周期项系数
// 对 12 小时共振轨道 (e > 0.5) 和地球同步轨道进行特殊初始化

// === 深空日月引力长期摄动 ===
void Deep_dpsec(const tle_t* tle, deep_arg_t* deep_arg);
// 使用半步法 (最大步长 720 分钟) 积分日月引力的长期影响
// 更新: xll, omgadf, xnode, em, xinc, xn

// === 深空日月引力周期摄动 ===
void Deep_dpper(deep_arg_t* deep_arg);
// 计算日月引力的周期摄动修正量
// 仅当时间变化 ≥ 30 分钟时重新计算
// 倾角 ≥ 0.2 rad: 直接施加周期项
// 倾角 < 0.2 rad: 使用 Lyddane 修正避免奇点

} // namespace WsfNORAD_Util
```

## 3. 典型调用模式

```cpp
// === 1. 构建传播器 ===
auto propagator = WsfNORAD_OrbitalPropagator();
// 默认构造使用 TEME 坐标系和 WGS84 地球模型

// === 2. 设置 TLE 轨道根数 ===
UtTwoLineElement tle_data;
tle_data.SetEpochDate(cal);             // 历元时刻
tle_data.SetMeanMotion(0.001);          // 平运动 (rad/s)
tle_data.SetEccentricity(0.001);        // 偏心率
tle_data.SetInclination(1.0);           // 倾角 (rad) ≈ 57.3°
tle_data.SetRAAN(2.0);                  // 升交点赤经 (rad)
tle_data.SetArgumentOfPeriapsis(3.0);   // 近地点幅角 (rad)
tle_data.SetMeanAnomaly(4.0);           // 平近点角 (rad)
tle_data.SetBstarDrag(0.0001);          // B* 阻力项

ut::OrbitalState init_state(earth_model, csEQUATORIAL, rfTEME);
init_state.Set(tle_data);
propagator.SetInitialOrbitalState(init_state);

// === 3. 初始化传播器 ===
UtCalendar sim_start(2026, 6, 11, 0, 0, 0.0); // 2026-06-11 00:00:00 UTC
bool ok = propagator.Initialize(sim_start);
// 内部自动选择 SGP4(近地) 或 SDP4(深空)

// === 4. 仿真循环 ===
UtCalendar sim_time = sim_start;
double step_sec = 60.0;  // 60 秒步长

for (int step = 0; step < 1440; step++) { // 模拟 1 天
    sim_time.AddSeconds(step_sec);
    propagator.Propagate(sim_time);        // 预报到目标时刻
    propagator.UpdateOrbitalState();       // 更新轨道状态

    // 获取预报结果 (SI 单位: m, m/s)
    const auto& state = propagator.GetOrbitalState();
    UtVec3d pos = state.GetVector().GetPosition();  // ECI 位置 (m)
    UtVec3d vel = state.GetVector().GetVelocity();  // ECI 速度 (m/s)

    // 日志输出
    log_state(sim_time, pos, vel);
}
```

## 4. 坐标系约定

| 坐标系 | 缩写 | 轴定义 | 用途 |
|--------|------|--------|------|
| **TEME** | True Equator Mean Equinox | X=平春分点, Z=真赤道北极 | NORAD 传播器内部坐标系 |
| **ECI** | Earth-Centered Inertial | TEME 的近似等价 | 外部接口输出 |
| **ECEF** | Earth-Centered Earth-Fixed | X=格林威治子午线, Z=北极 | 地面站可见性计算 |
| **Orbital Plane** | 轨道面坐标系 | X=近地点方向, Z=轨道面法向 | 轨道要素定义 |

## 5. 单位约定

NORAD 传播器在**内部计算**和**外部接口**使用不同的单位体系：

| 物理量 | 内部计算单位 | 外部接口单位 | 转换关系 |
|--------|-------------|-------------|----------|
| 距离/位置 | km（地球半径倍数） | m | ×1000 |
| 速度 | km/min | m/s | ×1000/60 |
| 角度 | rad | rad | 一致 |
| 角速度/平运动 | rad/min | — | — |
| 时间差 (tsince) | min | — | — |
| B* 阻力项 | 1/地球半径 | 1/地球半径 | 一致 |

## 6. 框架依赖解耦

| AFSIM 原始依赖 | 替换方案 |
|---------------|----------|
| `UtOrbitalPropagatorBase` | 自定义 `OrbitalPropagator` 抽象基类 |
| `WsfNonClassicalOrbitalPropagator` | 合并到自定义基类 |
| `UtTwoLineElement` | 自定义 `TLE` 结构体（9 字段） |
| `UtCalendar` | `double` (JD) 或 C++ `std::chrono::system_clock` |
| `UtOrbitalState` | 自定义 `OrbitalState` (ECI pos + vel + time) |
| `UtVec3d` | `Eigen::Vector3d` 或 `std::array<double,3>` |
| `UtMath::cTWO_PI / cPI` | `2.0 * M_PI / M_PI` |
| `WsfScenario` (工厂注册) | 移除，直接实例化传播器 |
| `ut::log::error()` | `std::cerr` 或 `spdlog::error()` |
| `WsfNORAD_PropagatorInverter` | 可选 — 仅非 TLE 初始状态需要，可独立实现 |
