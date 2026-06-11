# 数值积分轨道传播器 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** space-integrating-propagator-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────┐
│              WsfIntegratingPropagator                     │
│  (数值积分轨道传播器)                                       │
├──────────────────────────────────────────────────────────┤
│  + Initialize(initialTime) → bool                        │
│  + InitializeDynamics(simulationPtr, initialTime) → bool │
│  + Propagate(currentTime)                                │
│  + SetOrbitalIntegrator(integratorPtr) → bool            │
│  + SetOrbitalDynamics(dynamicsPtr) → bool                │
│  + GetDynamicalMass() → double                           │
└──────────┬───────────────────────────────────────────────┘
           │ owns                  │ owns
           ▼                       ▼
┌──────────────────────┐  ┌────────────────────────────────┐
│  WsfOrbitalIntegrator│  │     WsfOrbitalDynamics          │
│  (积分器抽象接口)      │  │  (动力学模型聚合器)               │
├──────────────────────┤  ├────────────────────────────────┤
│  + AdvanceToTime(    │  │  + ComputeAcceleration(mass,    │
│      dynamics,       │  │      time, pos, vel) → UtVec3d │
│      finalTime,      │  │  + AddTerm(termPtr)            │
│      initialState)   │  │  + GetTerms<T>() → vector<T*>  │
│      → OrbitalState  │  │  + RemoveTerm(index)           │
└──────┬───────────────┘  └──────────┬─────────────────────┘
       │ 派生                       │ contains
       ▼                             ▼
┌──────────────────────────┐  ┌────────────────────────────┐
│PK78OrbitalIntegrator     │  │ WsfOrbitalDynamicsTerm × N  │
│(Prince-Dormand 8(7)13M)  │  │ (各项动力学加速度贡献)        │
│Butcher表: c, A, b, b̂    │  │ • EarthMonopoleTerm         │
│自适应步长: L₂/L∞ 误差    │  │ • EarthJ2Term               │
│FSAL 优化: 12次评估/步    │  │ • SunMonopoleTerm           │
└──────────────────────────┘  │ • MoonMonopoleTerm          │
                               │ • AtmosphericDragTerm       │
                               │ • ... (用户可自定义)         │
                               └────────────────────────────┘
```

## 2. 核心接口定义

### 2.1 WsfOrbitalIntegrator（积分器抽象接口）

```cpp
class WsfOrbitalIntegrator : public WsfObject {
public:
    // 从当前状态推进到目标时刻
    // aDynamics:  轨道动力学模型（提供加速度计算）
    // aFinalTime: 目标预报时刻
    // aInitialState: 初始轨道状态（ECI 位置 + 速度 + 加速度）
    // 返回: 目标时刻的轨道状态
    virtual ut::OrbitalState AdvanceToTime(
        const WsfOrbitalDynamics& aDynamics,
        const UtCalendar&         aFinalTime,
        const ut::OrbitalState&   aInitialState) = 0;

    // 获取积分器类型标识字符串
    virtual std::string GetIntegratorType() const = 0;

    // 设置所属的传播器（用于获取质量等信息）
    void SetPropagator(const WsfIntegratingPropagator* aPropagatorPtr);
};
```

### 2.2 WsfRungeKuttaOrbitalIntegrator（自适应 RK 基类模板）

```cpp
template<unsigned int Order, unsigned int StepCount, typename Integrator>
class WsfRungeKuttaOrbitalIntegrator : public WsfOrbitalIntegrator {
public:
    static constexpr unsigned int cORDER     = Order;    // 主格式阶数 (PD78 = 8)
    static constexpr unsigned int cSTEPCOUNT = StepCount; // 阶段数 (PD78 = 13)

    enum class ErrorCriterion {
        cL_INFINITY_NORM,  // L∞ 范数: max(|Δr|, |Δv|)
        cL_TWO_NORM        // L₂ 范数: max(|Δr|₂/|Δr_step|₂, |Δv|₂/|Δv_step|₂)
    };

    // === 配置参数 ===
    void SetTolerance(double aTolerance);          // 截断误差容差 (默认 1e-10)
    void SetMaxStepSize(double aMaxStepSize);      // 最大步长 (s)
    void SetMinStepSize(double aMinStepSize);      // 最小步长 (s)
    void SetMaxAdjustmentAttempts(unsigned int);    // 单步最大重试次数 (默认 50)
    void SetErrorCriterion(ErrorCriterion);         // 误差范数选择
    void SetInitialStepSize(double);                // 初始步长 (s, 默认 0.1)

    // === 主积分循环 ===
    ut::OrbitalState AdvanceToTime(
        const WsfOrbitalDynamics& aDynamics,
        const UtCalendar&         aFinalTime,
        const ut::OrbitalState&   aInitialState) override;

private:
    // === 内部步骤 ===
    void TakeStep(const WsfOrbitalDynamics&, const ut::OrbitalState&);
    // 执行一个 13 阶段 RK 步: 计算各阶段 RHS → 加权合成 8 阶/7 阶解

    double ComputeError(const ut::OrbitalStateVector&) const;
    // 用 8 阶与 7 阶解的差值估计局部截断误差

    void AdjustTimeStep(double aError);
    // 根据误差自适应调整步长: h *= 0.9*(tol/err)^{1/p}

    void AdvanceState(ut::OrbitalState&);
    // 接受当前步: 更新 epoch, pos, vel, acceleration (FSAL)
};
```

### 2.3 WsfPrinceDormand78OrbitalIntegrator（PD 8(7) 系数定义）

Butcher 表系数矩阵：

| $c_i$ | $a_{i,0}$ | $a_{i,1}$ | $a_{i,2}$ | $a_{i,3}$ | $a_{i,4}$ | $a_{i,5}$ | $a_{i,6}$ | $a_{i,7}$ | $a_{i,8}$ | $a_{i,9}$ | $a_{i,10}$ | $a_{i,11}$ | $b_i$ (8阶) | $\hat{b}_i$ (7阶) |
|-------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|------------|------------|------------|-------------------|
| $0$ | — | — | — | — | — | — | — | — | — | — | — | — | $\frac{14005451}{335480064}$ | $-\frac{13451932}{455176623}$ |
| $\frac{1}{18}$ | $\frac{1}{18}$ | — | — | — | — | — | — | — | — | — | — | — | 0 | 0 |
| $\frac{1}{12}$ | $\frac{1}{48}$ | $\frac{1}{16}$ | — | — | — | — | — | — | — | — | — | — | 0 | 0 |
| $\frac{1}{8}$ | $\frac{1}{32}$ | 0 | $\frac{3}{32}$ | — | — | — | — | — | — | — | — | — | 0 | 0 |
| $\frac{5}{16}$ | $\frac{5}{16}$ | 0 | $-\frac{75}{64}$ | $\frac{75}{64}$ | — | — | — | — | — | — | — | — | 0 | 0 |
| $\frac{3}{8}$ | $\frac{3}{80}$ | 0 | 0 | $\frac{3}{16}$ | $\frac{3}{20}$ | — | — | — | — | — | — | — | $-\frac{59238493}{1068277825}$ | $+\frac{808719846}{976000145}$ |
| $\frac{59}{400}$ | $\frac{29443841}{614563906}$ | 0 | 0 | $\frac{77736538}{692538347}$ | $-\frac{28693883}{1125000000}$ | $\frac{23124283}{1800000000}$ | — | — | — | — | — | — | $\frac{181606767}{758867731}$ | $-\frac{1757004468}{5645159321}$ |
| $\frac{93}{200}$ | $\frac{16016141}{946692911}$ | 0 | 0 | $\frac{61564180}{158732637}$ | $\frac{22789713}{633445777}$ | $\frac{545815736}{2771057229}$ | $-\frac{180193667}{1043307555}$ | — | — | — | — | — | $\frac{561292985}{797845732}$ | $-\frac{656045339}{265891186}$ |
| $\frac{5490023248}{9719169821}$ | $\frac{39632708}{573591083}$ | 0 | 0 | $-\frac{433636366}{683701615}$ | $-\frac{421739975}{2616292301}$ | $\frac{100302831}{723423059}$ | $\frac{790204164}{839813087}$ | $\frac{800635310}{3783071287}$ | — | — | — | — | $-\frac{1041891430}{1371343529}$ | $+\frac{3867574721}{1518517206}$ |
| $\frac{13}{20}$ | $\frac{246121993}{1340847787}$ | 0 | 0 | $-\frac{37695042795}{15268766246}$ | $-\frac{309121744}{1061227803}$ | $-\frac{12992083}{490766935}$ | $\frac{6005943493}{2108947869}$ | $\frac{393006217}{1396673457}$ | $\frac{123872331}{1001029789}$ | — | — | — | $\frac{760417239}{1151165299}$ | $-\frac{465885868}{322736535}$ |
| $\frac{1201146811}{1299019798}$ | $-\frac{1028468189}{846180014}$ | 0 | 0 | $\frac{8478235783}{508512852}$ | $\frac{1311729495}{1432422823}$ | $-\frac{10304129995}{1701304382}$ | $-\frac{48777925059}{3047939560}$ | $\frac{15336726248}{1032824649}$ | $-\frac{45442868181}{3398467696}$ | $\frac{3065993473}{597172653}$ | — | — | $\frac{118820643}{751138087}$ | $-\frac{53011238}{667516719}$ |
| $1$ | $\frac{185892177}{718116043}$ | 0 | 0 | $-\frac{3185094517}{667107341}$ | $-\frac{477755414}{1098053517}$ | $-\frac{703635378}{230739211}$ | $\frac{5731566787}{1027545527}$ | $\frac{5232866602}{850066563}$ | $-\frac{4093664535}{808688257}$ | $\frac{3962137247}{1805957418}$ | $\frac{65686358}{487910083}$ | — | $-\frac{528747749}{2220607170}$ | $-\frac{2}{45}$ |
| $1$ (FSAL) | $\frac{403863854}{491063109}$ | 0 | 0 | $-\frac{5068492393}{434740067}$ | $-\frac{411421997}{543043805}$ | $\frac{652783627}{914296604}$ | $\frac{11173962825}{925320556}$ | $-\frac{13158990841}{6184727034}$ | $\frac{3936647629}{1978049680}$ | $-\frac{160528059}{685178525}$ | $\frac{248638103}{1413531060}$ | 0 | $\frac{1}{4}$ | 0 |

### 2.4 WsfOrbitalDynamicsTerm（动力学项抽象接口）

```cpp
class WsfOrbitalDynamicsTerm : public WsfObject {
public:
    // 计算该动力学项在 ECI 坐标系中的加速度
    // aMass:     航天器质量 (kg) — 用于加速度 = 力/质量
    // aTime:     计算时刻
    // aPosition: ECI 位置 (m)
    // aVelocity: ECI 速度 (m/s)
    // 返回:      ECI 加速度 (m/s²)
    virtual UtVec3d ComputeAcceleration(
        double            aMass,
        const UtCalendar& aTime,
        const UtVec3d&    aPosition,
        const UtVec3d&    aVelocity) const = 0;

    virtual std::string GetTermType() const = 0;
    virtual bool Initialize(const WsfOrbitalDynamics& aDynamics);
};
```

## 3. 典型调用模式

```cpp
// === 1. 构建传播器 ===
WsfScenario scenario;
WsfIntegratingPropagator propagator(scenario);

// === 2. 配置积分器 (Prince-Dormand 8(7)) ===
auto integrator = std::make_unique<WsfPrinceDormand78OrbitalIntegrator>();
integrator->SetTolerance(1e-12);                  // 高精度要求
integrator->SetMaxStepSize(3600.0);               // 最大步长 1 小时
integrator->SetMinStepSize(1e-6);                 // 最小步长 1 μs
integrator->SetErrorCriterion(L_TWO_NORM);        // 使用相对 L₂ 误差
integrator->SetInitialStepSize(10.0);             // 初始步长 10 s
propagator.SetOrbitalIntegrator(std::move(integrator));

// === 3. 配置动力学模型 ===
auto dynamics = std::make_unique<WsfOrbitalDynamics>(scenario);
dynamics->AddTerm(std::make_unique<EarthMonopoleTerm>());     // 地球中心引力
dynamics->AddTerm(std::make_unique<EarthJ2Term>());           // J2 摄动
dynamics->AddTerm(std::make_unique<SunMonopoleTerm>());       // 太阳引力
dynamics->AddTerm(std::make_unique<MoonMonopoleTerm>());      // 月球引力
propagator.SetOrbitalDynamics(std::move(dynamics));

// === 4. 设置初始状态 ===
UtCalendar epoch(2026, 6, 11, 0, 0, 0.0);
UtVec3d init_pos = {7000e3, 0.0, 0.0};    // ECI 位置 (m), 约 7000 km
UtVec3d init_vel = {0.0, 7500.0, 0.0};    // ECI 速度 (m/s), LEO 轨道
ut::OrbitalState init_state(earth, cEQUATORIAL, rfTRUE_OF_DATE);
init_state.Set(epoch, {init_pos, init_vel});
propagator.SetInitialOrbitalState(init_state);

// === 5. 初始化 ===
propagator.Initialize(epoch);

// === 6. 传播到目标时间 ===
UtCalendar target_time = epoch;
target_time.AddSeconds(86400.0);           // 预报 1 天
propagator.Propagate(target_time);

const auto& result = propagator.GetOrbitalState();
UtVec3d final_pos = result.GetVector().GetPosition();
UtVec3d final_vel = result.GetVector().GetVelocity();
```

## 4. 坐标系约定

| 坐标系 | 缩写 | 轴定义 | 用途 |
|--------|------|--------|------|
| **ECI (True of Date)** | TOD | X=真春分点, Z=真北极 (历元时刻) | 内部积分坐标系 |
| **ECI (J2000)** | J2K | X=J2000.0 平春分点, Z=J2000.0 平北极 | 输入选项 |
| **ECEF** | WCS | X=格林威治子午线, Z=北极 | 地面站相关计算 |

## 5. 单位约定

| 物理量 | 外部接口单位 | 内部计算单位 |
|--------|-------------|-------------|
| 位置 | m | m |
| 速度 | m/s | m/s |
| 加速度 | m/s² | m/s² |
| 质量 | kg | kg |
| 时间 | s (double) | s (double) |
| 步长 | s | s |
| 误差容差 | m 或 m/s (绝对) 或 无量纲 (相对) | — |

## 6. 框架依赖解耦

| AFSIM 原始依赖 | 替换方案 |
|---------------|----------|
| `WsfOrbitalIntegrator` | 自定义 `IIntegrator` 抽象接口 |
| `WsfRungeKuttaOrbitalIntegrator<O,S,I>` | 模板可直接移植，Butcher 表用常量 |
| `WsfOrbitalDynamics` | 自定义 `DynamicsModel` (vector<IForceModel>) |
| `WsfOrbitalDynamicsTerm` | 自定义 `IForceModel::GetAcceleration(t, r, v)` |
| `UtCalendar` | `double` (从 epoch 起的秒数) |
| `UtOrbitalState` | 自定义 `OrbitalState{t, r, v, a}` |
| `UtVec3d` | `Eigen::Vector3d` |
| `WsfIntegratingPropagator` | 自定义 `IntegratingPropagator` (组合积分器+动力学) |
| `WsfObject` / 脚本系统 | 移除，用构造函数/setter 配置 |
| `UtInput` (配置解析) | YAML/JSON 配置文件或代码内配置 |
