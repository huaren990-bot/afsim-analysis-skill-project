# 轨道交会与拦截瞄准 -- 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** space-rendezvous-targeting-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────┐
│              Rendezvous / Intercept（编排层）              │
│  MissionSequence 组合模式：Target + MatchVelocity         │
│  (Rendezvous) 或 Target + CompleteInterceptEvent         │
│  (Intercept)                                              │
├──────────────────────────────────────────────────────────┤
│  + Initialize(epoch, context) → bool                     │
│  + AdvanceMissionEvent(epoch, context) → Event*          │
│  + GetMaximumDeltaT() / GetMaximumDeltaV()               │
│  + SetOptimizeOption(option) / SetMaximumDeltaV(v)       │
└──────────┬───────────────────────────────────────────────┘
           │ 内部组合
           ▼
┌──────────────────────────────────────────────────────────┐
│              Target（核心瞄准类）                           │
│  Lambert 求解 + TOF-ΔV 代价函数优化                        │
├──────────────────────────────────────────────────────────┤
│  + Initialize(epoch, context) → bool                     │
│  + ComputeDeltaV(currentTime, evalTime, prop, out dV)    │
│  + GetInterceptTime() → UtCalendar                      │
│  + GetFinalDeltaV() → UtVec3d (交会模式用)               │
│  + SetComputeForRendezvous(bool) -- 控制终端速度差计算     │
│  + GetMaximumDeltaT() / GetMaximumDeltaV()               │
│  + GetOptimizeOption() / GetTolerance()                  │
│  - OptimizeSolution(propagator) → bool                    │
│  - OptimizeNone(propagator) → bool                       │
│  - FixedDtSolve(evalTime, prop, out dV) → Result         │
└──────────┬───────────────────────────────────────────────┘
           │ 调用
           ▼
┌──────────────────────────────────────────────────────────┐
│           WsfOrbitalTargeting（瞄准求解引擎）               │
│  Lambert Universal + TOF 搜索 + 代价最小化                 │
├──────────────────────────────────────────────────────────┤
│  + MinimizeDeltaV(dtMax, dvMax, rendezvous, tol, dt, dv)  │
│  + MinimizeDeltaT(dtMax, dvMax, rendezvous, tol, dt, dv)  │
│  + MinimizeCost(cost, dtMax, dvMax, rendezvous, tol, ...)  │
│  + Solve(dt, rendezvous, out dV) → Result                │
│  + Solve(dt, out dV_intercept, out dV_rendezvous)         │
│  + SetTolerance(tol) -- Lambert 收敛容差                   │
└──────────┬───────────────────────────────────────────────┘
           │ 调用
           ▼
┌──────────────────────────────────────────────────────────┐
│           UtLambertProblem::Universal（Lambert 求解器）     │
│  给定 (r1, r2, TOF, μ) → (v1_transfer, v2_transfer)      │
└──────────────────────────────────────────────────────────┘
           │ 使用
           ▼
┌──────────────────────────────────────────────────────────┐
│         OrbitalTargetPoint（目标点抽象层）                  │
│  目标轨道传播器 + 位置/速度/时间偏移 + 平动点               │
├──────────────────────────────────────────────────────────┤
│  + GetPosition(time) / GetVelocity(time)                 │
│  + GetPropagator() → UtOrbitalPropagatorBase&            │
└──────────────────────────────────────────────────────────┘
```

## 2. 核心接口定义

### 2.1 OptimizeOption（优化策略枚举）

```cpp
// 交会/拦截瞄准的优化策略
// 控制 Lambert 求解如何选择最优飞行时间 TOF
enum class OptimizeOption {
    NONE     = 0,  // 不优化：使用固定飞行时间 mDeltaTime 直接求解
    TIME     = 1,  // 最小化飞行时间：在 ΔV 约束下寻找最早交会时刻
    DELTA_V  = 3,  // 最小化 ΔV：在给定时间窗口 [0, mMaxTime] 内寻找最小 ΔV
    COST     = 4,  // 最小化自定义代价函数：J(TOF, ΔV) = w1*|Δv1| + w2*|Δv2| + wt*TOF
};
```

### 2.2 TargetConfig（瞄准配置参数）

```cpp
// Target 瞄准机动类的配置参数
struct TargetConfig {
    // === 优化策略 ===
    OptimizeOption optimize_option;  // 优化模式（NONE/TIME/DELTA_V/COST）

    // === 时间参数 ===
    double max_time_s;     // 最大飞行时间上限 (s)，优化模式下的搜索窗口上界
    double delta_time_s;   // 固定飞行时间 (s)，仅在 cOPTIMIZE_NONE 模式下有效

    // === ΔV 约束 ===
    double max_delta_v_ms; // 单次脉冲 ΔV 上限 (m/s)，超过此值的解被排除
                           // 若为 0 且特征时间有效，自动填充为平台可用 ΔV

    // === 求解精度 ===
    double tolerance;      // Lambert 瞄准求解的数值容差，默认 1e-9

    // === 交会标志 ===
    bool compute_for_rendezvous; // 是否作为交会（Rendezvous）一部分计算
                                 // true: 额外输出终端速度差 mFinalDeltaV（供 MatchVelocity 机动使用）
                                 // false: 仅输出出发脉冲 ΔV（拦截模式）

    // === 代价函数（仅在 cOPTIMIZE_COST 模式下有效）===
    OrbitalTargetingCost* cost_ptr; // 自定义代价函数指针
                                    // 提供 IsValid() / IsLeastTime() 接口
                                    // J(TOF, ΔV) 的内部逻辑由子类实现
};
```

### 2.3 LambertResult（Lambert 求解结果）

```cpp
// UtLambertProblem::Result 的移植等价结构
// 封装 Lambert 求解的成功/失败状态
struct LambertResult {
    // 是否有有效解
    bool has_solution;

    // 是否为双曲线转移轨道
    bool is_hyperbolic;

    // 转移轨道是否与中心天体表面相交
    bool hits_central_body;

    // 出发转移速度 (m/s, ECI 坐标系)
    Vec3 v_transfer_departure;

    // 到达转移速度 (m/s, ECI 坐标系)
    Vec3 v_transfer_arrival;

    // 综合评估解的有效性
    // 检查: has_solution && !hits_central_body &&
    //       (!is_hyperbolic || hyperbolic_allowed)
    bool Assess(bool hyperbolic_allowed) const;
};
```

### 2.4 OrbitalTargetingCost（代价函数抽象基类）

```cpp
// 自定义代价函数抽象基类
// 用于 cOPTIMIZE_COST 优化模式下的 J(TOF, ΔV) 最小化
class OrbitalTargetingCost {
public:
    virtual ~OrbitalTargetingCost() = default;

    // 是否趋向最短时间：若为 true，时间容差用较粗的 1e-2 s
    // 若为 false，时间容差用较精细的 1e-4 s
    virtual bool IsLeastTime() const = 0;

    // 代价函数是否有效（已正确配置）
    virtual bool IsValid() const = 0;

    // 计算代价函数值
    // TOF: 飞行时间 (s)
    // dv1: 出发脉冲 ΔV 标量 (m/s)
    // dv2: 到达脉冲 ΔV 标量 (m/s)，拦截模式下 dv2 = 0
    // 返回: J = w1*|Δv1| + w2*|Δv2| + wt*TOF
    virtual double Compute(double TOF, double dv1, double dv2) const = 0;
};

// 基本 ΔV 代价（最小化总 ΔV）
class DeltaVCost : public OrbitalTargetingCost {
public:
    DeltaVCost(double w1 = 1.0, double w2 = 1.0, double wt = 0.0);
    bool IsLeastTime() const override { return false; }
    double Compute(double TOF, double dv1, double dv2) const override;

private:
    double w1_, w2_, wt_;
};
```

### 2.5 Target（核心瞄准类接口）

```cpp
// 轨道交会/拦截瞄准的核心机动类
// 以 Lambert 求解器为引擎，在 [0, mMaxTime] 飞行时间范围内搜索最优转移轨道
// 支持 4 种优化策略，提供固定时间和优化两种求解路径
class Target {
public:
    // ===================== 构造 =====================

    // 基础构造（需要后续配置目标点）
    explicit Target(const WsfScenario& scenario);

    // 指定目标航迹的构造
    Target(const WsfScenario& scenario,
           const WsfTrackId&  local_track_id,     // 目标航迹 ID
           OptimizeOption      optimize_option,
           const UtTimeValue&  max_time,           // 最大飞行时间 (s)
           const UtSpeedValue& max_delta_v = -1.0);// 最大允许 ΔV (m/s)

    // 指定目标点选项的构造
    Target(const WsfScenario& scenario,
           const TargetPointOptions& options,      // 目标点完整配置
           OptimizeOption            optimize_option,
           const UtTimeValue&        max_time,
           const UtSpeedValue&       max_delta_v = -1.0);

    // 指定代价函数的构造
    Target(const WsfScenario&          scenario,
           const TargetPointOptions&   options,
           const OrbitalTargetingCost& optimize_cost,  // 自定义代价函数
           const UtTimeValue&          max_time,
           const UtSpeedValue&         max_delta_v = -1.0);

    Target* Clone() const;

    // ===================== 生命周期 =====================

    // 从场景文件解析配置
    bool ProcessInput(UtInput& input);

    // 初始化：验证参数 + 创建目标点对象 + 自动填充默认值
    // 失败条件：
    //   - mMaxTime==0 && mMaxDeltaV==0 && mDeltaTime==0（三项全零，必须至少指定一项）
    //   - mMaxDeltaV > 可用 ΔV
    //   - cOPTIMIZE_COST 模式但 cost 为空或无效
    //   - 目标点初始化失败（目标平台/航迹不存在）
    bool Initialize(const UtCalendar& epoch, const OrbitalMissionContext& context);

    // 参数验证：mMaxTime >= 0, mDeltaTime >= 0, mMaxDeltaV >= 0
    bool ValidateParameterRanges(const std::string& platform_name) const;

    // ===================== 核心机动计算 =====================

    // 计算本机动在当前时刻的 ΔV
    // 内部流程：
    //   1. 调用 OptimizeSolution(propagator) 或 OptimizeNone(propagator) 求解最优 TOF
    //   2. 调用 FixedDtSolve(evaluationTime, propagator, deltaV) 用最优 TOF 计算具体 ΔV
    // 参数:
    //   current_time: 当前仿真绝对时间
    //   evaluation_time: 机动评估时间
    //   propagator: 拦截方当前轨道传播器
    //   out deltaV [out]: 出发机动脉冲矢量 (m/s, ECI 坐标系)
    void ComputeDeltaV(
        const UtCalendar& current_time,
        const UtCalendar& evaluation_time,
        const UtOrbitalPropagatorBase& propagator,
        Vec3& deltaV  // [out] 单位: m/s
    ) const;

    // ===================== 结果查询 =====================

    // 获取计算出的交会/拦截绝对时间
    const UtCalendar& GetInterceptTime() const;

    // 获取终端速度差（仅在 mComputeForRendezvous=true 时有意义）
    // 交会时刻追击方与目标的速度差，传递给 MatchVelocity 机动执行速度匹配
    const Vec3& GetFinalDeltaV() const;

    // ===================== 参数设置/获取 =====================

    // 最大飞行时间 (s)
    UtTimeValue  GetMaximumDeltaT() const;
    void SetMaximumDeltaT(const UtTimeValue& max_delta_t);

    // 最大允许 ΔV (m/s)
    UtSpeedValue GetMaximumDeltaV() const;
    void SetMaximumDeltaV(const UtSpeedValue& max_delta_v);

    // 固定飞行时间 (s)，仅在 cOPTIMIZE_NONE 下有效
    UtTimeValue  GetDeltaTime() const;
    void SetDeltaTime(const UtTimeValue& delta_time);

    // 优化策略
    OptimizeOption GetOptimizeOption() const;
    void SetOptimizeOption(OptimizeOption option);

    // Lambert 求解精度容差
    double GetTolerance() const;
    void SetTolerance(double tolerance);

    // 自定义代价函数
    const OrbitalTargetingCost* GetOptimizationCost() const;
    void SetOptimizationCost(std::unique_ptr<OrbitalTargetingCost> cost);

    // 交会/拦截模式切换
    void SetComputeForRendezvous(bool compute_for_rendezvous);

    // ===================== 目标点管理（通过 TargetingCapableManeuver 基类）=====================

    const WsfTrackId& GetLocalTrackId() const;
    WsfStringId       GetPlatformName() const;

    // 位置偏移（目标点的空间偏移）
    bool   HasOffset() const;
    Vec3   GetOffset() const;           // m
    String GetOffsetUnit() const;

    // 速度偏移
    bool   HasVelocityOffset() const;
    Vec3   GetVelocityOffset() const;   // m/s

    // 时间偏移/滞后
    UtTimeValue GetTargetOffsetTime() const;
    UtTimeValue GetTargetLagTime() const;

    // 原始目标点选项
    const TargetPointOptions& GetTargetPointOptions() const;

private:
    // ===================== 内部优化求解 =====================

    // 优化求解（3 种模式分支）：
    //   cOPTIMIZE_TIME    → tgt.MinimizeDeltaT(mMaxTime, mMaxDeltaV, ...)
    //   cOPTIMIZE_DELTA_V → tgt.MinimizeDeltaV(mMaxTime, mMaxDeltaV, ...)
    //   cOPTIMIZE_COST    → tgt.MinimizeCost(*mCostPtr, mMaxTime, mMaxDeltaV, ...)
    // 所有优化在传播器克隆上进行（不污染原始传播器状态）
    bool OptimizeSolution(const UtOrbitalPropagatorBase& propagator);

    // 固定时间求解（cOPTIMIZE_NONE）
    bool OptimizeNone(const UtOrbitalPropagatorBase& propagator);

    // 固定飞行时间的 Lambert 求解
    // 1. mInterceptTime = mStartTime + dT
    // 2. dt = mInterceptTime - evaluationTime
    // 3. tgt.Solve(dt, aDeltaV, mFinalDeltaV)
    // 4. 返回 LambertResult（含 Assess 状态）
    LambertResult FixedDtSolve(
        const UtCalendar& evaluation_time,
        const UtOrbitalPropagatorBase& propagator,
        Vec3& deltaV  // [out]
    ) const;
};
```

### 2.6 WsfOrbitalTargeting（瞄准求解引擎接口）

```cpp
// Lambert 瞄准求解引擎
// 封装拦截方传播器 + 目标点，提供 3 种优化搜索模式
class WsfOrbitalTargeting {
public:
    // 构造：绑定拦截时间、拦截方传播器、目标点
    WsfOrbitalTargeting(
        const UtCalendar& start_time,
        UtOrbitalPropagatorBase& interceptor_propagator,
        const OrbitalTargetPoint& target
    );

    // 带约束的构造（是否允许双曲线解 / 与地表相交的解）
    WsfOrbitalTargeting(
        const UtCalendar& start_time,
        UtOrbitalPropagatorBase& interceptor_propagator,
        const OrbitalTargetPoint& target,
        bool allow_hyperbolic,
        bool allow_earth_hit
    );

    // ===================== 三种优化模式 =====================

    // 最小化 ΔV
    // 参数:
    //   dt_max: 最大飞行时间 (s)
    //   dv_max: 最大允许 ΔV (m/s)
    //   rendezvous: true=交会模式（需要计算终端速度差）, false=拦截模式
    //   time_tolerance: 时间容差 (s)，通常 1e-4
    //   out dt_opt: 最优飞行时间 (s)
    //   out dv_opt: 最优 ΔV 标量 (m/s)
    // 返回: Lambert 求解结果
    LambertResult MinimizeDeltaV(
        double dt_max, double dv_max, bool rendezvous,
        double time_tolerance, double& dt_opt, double& dv_opt
    ) const;

    // 最小化飞行时间
    // time_tolerance: 通常 1e-2 s（比 MinimizeDeltaV 更粗的容差，更快收敛）
    LambertResult MinimizeDeltaT(
        double dt_max, double dv_max, bool rendezvous,
        double time_tolerance, double& dt_opt, double& dv_opt
    ) const;

    // 最小化自定义代价函数 J(TOF, ΔV)
    // cost: 代价函数对象
    LambertResult MinimizeCost(
        const OrbitalTargetingCost& cost,
        double dt_max, double dv_max, bool rendezvous,
        double time_tolerance, double& dt_opt, double& dv_opt
    ) const;

    // ===================== 固定时间求解 =====================

    // 给定飞行时间直接求解（不优化）
    // 参数:
    //   dt: 飞行时间 (s)
    //   rendezvous: true=交会模式
    //   out deltaV: 出发 ΔV 标量 (m/s)
    LambertResult Solve(double dt, bool rendezvous, double& deltaV) const;

    // 给定飞行时间直接求解（返回完整矢量信息）
    // 参数:
    //   dt: 飞行时间 (s)
    //   out deltaV_intercept: 出发脉冲 ΔV (m/s, ECI)
    //   out deltaV_rendezvous: 终端速度差 (m/s, ECI)，仅 rendezvous 模式有意义
    LambertResult Solve(
        double dt,
        Vec3& deltaV_intercept,   // [out]
        Vec3& deltaV_rendezvous   // [out]
    ) const;

    // ===================== 辅助方法 =====================

    // 判断是否应该走短弧（short way）
    // 基于拦截方位置+速度与目标位置的几何关系自动判定
    static bool GoShortWay(
        const Vec3& location_interceptor,
        const Vec3& velocity_interceptor,
        const Vec3& location_target
    );

    double GetTolerance() const;
    void SetTolerance(double tolerance);  // Lambert 求解收敛容差，默认 1e-9

private:
    // 内部采样结构
    struct Sample {
        double dt;
        double dv;
        double cost;
        bool   has_solution;
    };

    // 在时间窗口中按一定步长采样并寻找包含代价极值的子区间
    std::vector<std::pair<double, double>> FindAllRangesCost(
        const OrbitalTargetingCost& cost,
        double dt_zero, double dt_max, double dv_max, bool rendezvous
    ) const;

    // 在给定搜索区间内二分查找代价最小值
    LambertResult SearchCost(
        const OrbitalTargetingCost& cost,
        double dt_low, double dt_high, bool rendezvous,
        double dv_max, double time_tolerance, double& deltaV
    ) const;
};
```

### 2.7 Rendezvous / Intercept（编排层接口）

```cpp
// 交会机动：Target（瞄准） + MatchVelocity（速度匹配）
// 继承自 WsfOrbitalMissionSequence，内部组合 Target 和 MatchVelocity 两个子机动
class Rendezvous {
public:
    // 构造参数与 Target 一致
    Rendezvous(const WsfScenario& scenario);
    Rendezvous(const WsfScenario& scenario, const WsfTrackId& track_id,
               OptimizeOption option, const UtTimeValue& max_time,
               const UtSpeedValue& max_delta_v = 0.0);

    bool Initialize(const UtCalendar& epoch, const OrbitalMissionContext& context);
    bool ValidateParameterRanges(const std::string& platform_name) const;

    // 执行编排：AdvanceMissionEvent
    //   Target 完成 → MatchVelocity 使用 GetInterceptTime() 设置相对时间条件
    WsfOrbitalEvent* AdvanceMissionEvent(
        const UtCalendar& epoch, const OrbitalMissionContext& context
    );

    // 以下所有 Set/Get 方法代理至内部 Target 机动
    UtTimeValue  GetMaximumDeltaT() const;
    UtSpeedValue GetMaximumDeltaV() const;
    OptimizeOption GetOptimizeOption() const;
    // ... 其他参数存取器 ...
};

// 拦截机动：Target（瞄准） + CompleteInterceptEvent（完成标记）
// 与 Rendezvous 共享相同的核心瞄准逻辑（Target）
// CompleteInterceptEvent 为空操作事件（ExecuteEvent 直接返回 true）
class Intercept {
public:
    Intercept(const WsfScenario& scenario);
    Intercept(const WsfScenario& scenario, const WsfTrackId& track_id,
              OptimizeOption option, const UtTimeValue& max_time,
              const UtSpeedValue& max_delta_v = 0.0);

    bool Initialize(const UtCalendar& epoch, const OrbitalMissionContext& context);

    // 与 Rendezvous 完全相同的接口（共享 Target 核心逻辑）
    UtTimeValue  GetMaximumDeltaT() const;
    UtSpeedValue GetMaximumDeltaV() const;
    // ... 其他参数存取器 ...
};
```

## 3. 典型调用模式

```cpp
// ============================================================
// 1. 初始化：配置交会机动
// ============================================================

// 创建交会机动：目标为指定航迹的卫星
Rendezvous rendezvous(
    scenario,
    target_satellite_track_id,
    OptimizeOption::DELTA_V,          // 最小化 ΔV
    UtTimeValue(3600.0),              // 最大飞行时间 1 小时
    UtSpeedValue(500.0)               // 最大允许 ΔV 500 m/s
);

// 初始化：创建目标点 + 验证参数 + 填充默认值
bool ok = rendezvous.Initialize(current_epoch, mission_context);
if (!ok) {
    // 初始化失败：目标不存在 / ΔV 超出预算 / 参数无效
    return;
}
// ============================================================
// 2. 仿真循环：每帧评估机动
// ============================================================

// 在机动评估时刻（ComputeDeltaV 被调用时）
// 内部执行优化求解流程:
// 1. OptimizeSolution(propagator):
//    - 克隆传播器（不污染原始状态）
//    - 创建 WsfOrbitalTargeting 对象
//    - 根据 OptimizeOption 调用:
//      MinimizeDeltaV: 在 [0, 3600s] 内搜索最小 ΔV 的 TOF
//      MinimizeDeltaT: 在 [0, 3600s] 内搜索满足 ΔV 约束的最短 TOF
//      MinimizeCost:    在 [0, 3600s] 内搜索最小代价 J(TOF, ΔV) 的 TOF
// 2. 得到最优 TOF (dt_opt) 和 ΔV 标量 (dv_opt)
// 3. FixedDtSolve(evaluation_time, propagator, deltaV):
//    - mInterceptTime = mStartTime + dt_opt
//    - dt = mInterceptTime - evaluationTime
//    - tgt.Solve(dt, aDeltaV, mFinalDeltaV)
//      → 调用 UtLambertProblem::Universal(r1, r2, dt, mu)
//      → 计算出发脉冲: Δv1 = v1_transfer - v_current
//      → 计算终端速度差: mFinalDeltaV = v_target - v2_transfer (仅 rendezvous 模式)
// 4. 返回 Δv1 作为本机动执行的脉冲

Vec3 deltaV;  // 出发脉冲 (m/s, ECI)
rendezvous.GetTargetManeuver().ComputeDeltaV(
    current_time, evaluation_time, my_propagator, deltaV);

// 执行脉冲机动
my_propagator.ApplyImpulsiveDeltaV(deltaV);
// ============================================================
// 3. 拦截模式（Intercept）
// ============================================================

// 创建拦截机动
Intercept intercept(
    scenario,
    target_track_id,
    OptimizeOption::TIME,              // 最小化飞行时间（尽快拦截）
    UtTimeValue(7200.0),               // 最大飞行时间 2 小时
    UtSpeedValue(1000.0)               // 最大 ΔV 1000 m/s
);

intercept.Initialize(current_epoch, mission_context);

// 拦截模式与交会模式的区别：
//   - Intercept: mComputeForRendezvous = false
//     Target 仅计算出发脉冲 Δv1，不计算终端速度差
//     到达目标位置即完成任务
//   - Rendezvous: mComputeForRendezvous = true
//     Target 额外计算终端速度差 mFinalDeltaV
//     MatchVelocity 机动随后执行 ΔV = mFinalDeltaV 完成速度匹配
// ============================================================
// 4. 目标点偏移（定点交会）
// ============================================================

// 设置位置偏移：目标点前 1000 m（目标轨道前方 1 km）
rendezvous.SetOffset(
    Vec3(1000.0, 0.0, 0.0),           // 偏移量 (m)
    OrbitalReferenceFrame::VNC        // VNC 坐标系（沿航迹方向）
);

// 设置时间偏移：提前 60 秒到达目标位置
rendezvous.SetTargetOffsetTime(UtTimeValue(-60.0));

// 绑定到指定平台名称（非航迹 ID 方式）
rendezvous.SetPlatformName(WsfStringId("ISS"));
// ============================================================
// 5. 代价函数自定义
// ============================================================

// 创建加权代价函数：燃料权重 0.8，时间权重 0.2
auto cost = std::make_unique<DeltaVCost>(1.0, 1.0, 0.001);
// J = 1.0 * |Δv1| + 1.0 * |Δv2| + 0.001 * TOF

// 使用代价优化模式
Rendezvous rendezvous_cost(
    scenario,
    target_options,
    *cost,
    UtTimeValue(3600.0),
    UtSpeedValue(500.0)
);
```

## 4. 坐标系/单位约定

| 量 | 单位 | 说明 |
|----|------|------|
| 引力参数 μ | km³/s² | 地球 μ = 398600.44 km³/s² |
| 位置矢量 | m | ECI 坐标系 |
| 速度矢量 | m/s | ECI 坐标系 |
| ΔV (脉冲) | m/s | 出发脉冲和到达脉冲均为 ECI 系矢量 |
| 飞行时间 TOF | s | 从出发到达到交会点的飞行时间 |
| 最大飞行时间 | s | mMaxTime，搜索窗口上界 |
| 最大 ΔV | m/s | mMaxDeltaV，超出此值的解被排除 |
| 时间容差 | s | 1e-2 (最小化时间) 或 1e-4 (最小化 ΔV/代价) |
| Lambert 容差 | 无量纲 | mTolerance = 1e-9（Lambert Universal 求解器容差） |
| 角度 | rad | RAAN、倾角 |

> 注：AFSIM 使用 SI 单位制（m, m/s, s）用于轨道力学部分，与飞行器动力学部分（Imperial）不同。

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|---------|----------|
| `UtLambertProblem::Universal` | Lambert 求解器 | 自定义 Lambert Universal 求解器（见 Lambert 卡片） |
| `UtOrbitalPropagatorBase` | 轨道传播器 | 自定义 OrbitPropagator 接口（Propagate + GetPosition + GetVelocity） |
| `WsfOrbitalTargeting` | 瞄准求解引擎 | 自定义 TargetingSolver（封装 TOF 搜索 + Lambert 调用） |
| `OrbitalTargetPoint` | 目标点抽象 | 自定义 TargetState 结构体（封装目标轨道查询 + 位置/速度/时间偏移） |
| `TargetPointOptions` | 目标点配置 | 自定义 TargetOptions 结构体 |
| `UtVec3d` | 3D 向量 | Eigen::Vector3d |
| `UtCalendar` | 日历/时间 | 自定义 Time 类 |
| `UtUnitTypes` (UtTimeValue, UtSpeedValue, UtLengthValue) | 带单位的量纲 | 自定义 UnitValue 或直接用 double + 硬编码单位 |
| `UtCloneablePtr<T>` | 深拷贝智能指针 | `std::unique_ptr<T>` + Clone 工厂 |
| `WsfOrbitalMissionSequence` | 机动序列编排基类 | 自定义 MissionSequence 类 |
| `WsfOrbitalManeuver` | 机动基类 | 自定义 Maneuver 接口 |
| `WsfScenario` | 场景对象 | 替换为自定义 SimulationContext |
| `WsfTrackId` / `WsfStringId` | 航迹/平台标识 | 字符串 ID 或 UUID |
| `WsfOrbitalEvent` | 事件系统 | 自定义事件调度系统 |
| `WsfObject` | 对象基类 | 自定义 Object 接口或直接剥离 |
| `UtInput` / `UtInputBlock` | 配置解析 | JSON/YAML/TOML 解析器 |
| `MatchVelocity` 机动 | 速度匹配机动 | 自定义 MatchVelocity 机动（读取 Target.GetFinalDeltaV() → 执行匹配脉冲） |
| `CompleteInterceptEvent` | 拦截完成标记 | 自定义空操作事件 |
