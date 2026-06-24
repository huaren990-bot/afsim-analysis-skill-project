# 轨道交会判别 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** space-conjunction-assessment-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│          WsfOrbitalConjunctionAssessment             │
│  (轨道交会判别器——核心评估类)                          │
├──────────────────────────────────────────────────────┤
│  + FindNext() → Status                               │
│  + CurrentConjunction() → ConjunctionRecord          │
│  - FastFilter() → bool                               │
│  - PredictNextState()                                │
│  - FindMinimum() → double                            │
│  - ComputeNextTime() → double                        │
└──────────┬───────────────────────────────────────────┘
           │ 包含
           ▼
┌──────────────────────────────────────────────────────┐
│  Object (目标封装)     Encounter (相遇计算)            │
│  ├─ Propagate(t)       ├─ Compute(...)               │
│  ├─ Periapsis()        ├─ ComputeProbability()        │
│  ├─ Apoapsis()         ├─ ComputeEncounterTimes()     │
│  ├─ Size()             ├─ RecomputeMinTime()          │
│  ├─ Covariance(t)      ├─ ContractTowardRoot()        │
│  └─ EstimateTimeStep() └─ HasCloseEncounter()         │
└──────────────────────────────────────────────────────┘
           │ 使用
           ▼
┌──────────────────────────────────────────────────────┐
│  外部依赖                                            │
│  - UtOrbitalPropagatorBase (轨道外推器)               │
│  - UtQuinticSpline / UtCubicSpline (样条插值)         │
│  - UtGoldenSectionSearch (黄金分割搜索)               │
│  - UtCovariance (协方差矩阵)                           │
│  - WsfLocalTrack (航迹数据)                           │
└──────────────────────────────────────────────────────┘
```

算法核心结构：`WsfOrbitalConjunctionAssessment` 包含两个 `Object`（主目标和次目标），每个 `Object` 拥有独立的轨道外推器。`FindNext()` 循环中依次执行 `PredictNextState()`（步进预测）和 `FindMinimum()`（最近点搜索），找到极小值点后由 `Encounter::Compute()` 计算碰撞概率和相遇时刻。

## 2. 核心接口定义

### 2.1 WsfOrbitalConjunctionRecord（交会记录——输出结果）

```cpp
// 描述一次预测到的交会事件的完整数据
struct WsfOrbitalConjunctionRecord {
    std::string mPrimary;          // 主目标名称字符串
    std::string mSecondary;        // 次目标名称字符串
    double mMinTime;               // 最近点时刻（两目标距离最近的仿真时间），单位：s
    double mStartTime;             // 相遇开始时间（进入协方差椭球危险区的时间），单位：s
    double mEndTime;               // 相遇结束时间（离开协方差椭球危险区的时间），单位：s
    double mMaxProbability;        // 最大碰撞概率（最坏情况下的碰撞概率估计，0~1），无量纲
    double mMissDistance;          // 脱靶量（最近点处的相对距离），单位：m
    double mRelativeVelocity;      // 最近点处的相对速度大小，单位：m/s
};
```

### 2.2 Options（评估选项——配置参数结构体）

```cpp
// 控制交会判别算法的配置参数，在构造函数中一次性传入，搜索过程中不变
struct Options {
    double mCutRadius;             // 快速过滤距离阈值（用于近/远地点快速截断），单位：m
    double mStepRadians;           // 搜索步长角（平近点角增量，默认 PI/60 即 3 度），单位：rad
    double mExclusionFactor;       // 协方差椭球缩放因子（默认 8.0），无量纲
    double mInitialSearchTime;     // 搜索起始仿真时间，单位：s
    double mFinalSearchTime;       // 搜索终止仿真时间，单位：s
    double mDefaultObjectRadius;   // 默认目标半径（当目标尺寸未知时使用，默认 1.0），单位：m
    double mDefaultVariance;       // 默认位置方差（无航迹滤波器时用于构造协方差，默认 10.0），单位：m
};
```

### 2.3 Kinematics（运动学数据——单个目标在某一时刻的运动状态）

```cpp
// 封装一个空间目标在特定时刻的位置、速度和加速度（惯性系）
struct Kinematics {
    UtVec3d mPosition;      // 惯性系（ECI）位置矢量，单位：m
    UtVec3d mVelocity;      // 惯性系（ECI）速度矢量，单位：m/s
    UtVec3d mAcceleration;  // 惯性系（ECI）加速度矢量，单位：m/s^2
};
```

### 2.4 State（两目标在某一时刻的相对状态）

```cpp
// 封装两目标在某一时刻的运动状态，并计算相对运动的距离函数及其导数
struct State {
    double DistanceFunction() const;              // 平方距离函数 D(t) = |r_rel|^2，单位：m^2
    double DistanceFunctionPrime() const;         // D(t) 的一阶导数 D'(t) = 2·v_rel·r_rel，单位：m^2/s
    double DistanceFunctionPrimePrime() const;    // D(t) 的二阶导数 D''(t) = 2|v_rel|^2 + 2·a_rel·r_rel，单位：m^2/s^2
    UtVec3d RelativePosition() const;             // 相对位置 r_rel = r_secondary - r_primary，单位：m
    UtVec3d RelativeVelocity() const;             // 相对速度 v_rel = v_secondary - v_primary，单位：m/s
    UtVec3d RelativeAcceleration() const;         // 相对加速度 a_rel = a_secondary - a_primary，单位：m/s^2

    double mTime;           // 该状态对应的仿真时间，单位：s
    Kinematics mPrimary;    // 主目标在该时刻的运动学数据
    Kinematics mSecondary;  // 次目标在该时刻的运动学数据
};
```

### 2.5 Object（目标对象——封装单个空间目标的轨道信息）

```cpp
// 封装单个空间目标的航迹引用、轨道外推器和尺寸信息
class Object {
public:
    // 构造函数：传入航迹引用、目标尺寸和轨道外推器原型（会被 Clone() 复制）
    Object(WsfLocalTrack& aTrack, double aSize, const UtOrbitalPropagatorBase* aPropPtr);

    // 估算推进给定弧度所需的时间步长
    // 基于瞬时平近点角变化率：Δt ≈ r^2 · Δθ / (n · a^2 · √(1-e^2))
    double EstimateTimeStep(double aTime, double aRadians);

    double Periapsis() const;       // 轨道近地点半径，单位：m
    double Apoapsis() const;        // 轨道远地点半径，单位：m
    double Size() const;            // 目标等效半径（<= 0 时回退为 DefaultObjectRadius），单位：m

    // 获取目标在指定时刻的位置协方差（6x6 矩阵，速度分量会被后续投影掉）
    UtCovariance Covariance(double aTime) const;

    // 外推目标到指定时刻，返回该时刻的位置/速度/加速度（惯性系）
    Kinematics Propagate(double aTime);

    std::string GetName() const;    // 获取目标名称字符串
};
```

### 2.6 Encounter（相遇计算——内嵌类）

```cpp
// 封装相遇事件的完整计算流程：精确定位最小距离点、计算碰撞概率、确定进入/离开危险区时刻
class Encounter {
public:
    Encounter();    // 将 mRecord 初始化为哨兵值（-1.0）
    void Reset();    // 重置 mRecord 所有数值字段为 -1.0

    // 主入口：从当前区间 [aCurr, aNext] 的路径计算完整交会数据
    // aCombinedRadius = R_p + R_s（组合目标半径，单位：m）
    // aCombinedCovariance = 主目标协方差 + 次目标协方差（组合协方差矩阵，单位：m^2）
    // aScaleFactor = mExclusionFactor（协方差缩放因子）
    void Compute(const State& aCurr, const State& aNext,
                 double aCombinedRadius,
                 const UtCovariance& aCombinedCovariance,
                 double aScaleFactor);

    // 判断是否存在有效交会（mStartTime < mEndTime 即为有效）
    bool HasCloseEncounter() const;

    WsfOrbitalConjunctionRecord GetRecord() const;   // 获取当前相遇记录

private:
    // 基于 Vallado 解析公式 (11-56) 计算最大碰撞概率
    void ComputeProbability(const UtInterpolatingPolynomial<UtVec3d, 5>& aPath,
                            double aCombinedRadius);

    // 用协方差椭球函数 F(t) 的三次样条插值求根，确定进入/离开危险区的时间
    void ComputeEncounterTimes(const UtInterpolatingPolynomial<UtVec3d, 5>& aPath,
                                double aCurrTime, double aNextTime,
                                double aMinTime, UtCovariance& aCombinedCovariance);

    // 黄金分割搜索法精确定位距离极小值点（收敛容差 1.0e-6 m）
    static double RecomputeMinTime(const UtInterpolatingPolynomial<UtVec3d, 5>& aFunction,
                                    double aLowRange, double aHighRange);

    // 根收缩算法：向固定点方向二分收缩搜索区间边界
    template<typename Callable>
    static double ContractTowardRoot(Callable aFunction, double aFixed, double aLimit);

    WsfOrbitalConjunctionRecord mRecord;   // 相遇记录（含最小距离时间、碰撞概率等）
};
```

### 2.7 WsfOrbitalConjunctionAssessment（主类）

```cpp
// 轨道交会判别主类：对两个空间目标进行五级逐层筛选，逐一发现交会事件
class WsfOrbitalConjunctionAssessment {
public:
    enum class Status {
        cNO_CONJUNCTION = 0,      // 继续搜索中（尚未找到交会）
        cCONJUNCTION_FOUND,       // 已找到交会事件
        cREACHED_FINAL_TIME       // 已到达搜索终止时间
    };

    // 构造函数：初始化两目标对象，执行 FastFilter 快速过滤器
    WsfOrbitalConjunctionAssessment(WsfLocalTrack& aPrimary, double aPrimarySize,
                                     WsfLocalTrack& aSecondary, double aSecondarySize,
                                     const Options& aOptions,
                                     const UtOrbitalPropagatorBase* aPropPtr);

    // 查找下一个交会事件（循环调用以逐次发现所有交会）
    // 返回 cCONJUNCTION_FOUND 表示找到交会；返回 cREACHED_FINAL_TIME 表示搜索完成
    Status FindNext();

    bool ReachedFinalTime() const;                   // 是否已到达终止时间
    WsfOrbitalConjunctionRecord CurrentConjunction() const;  // 获取当前交会记录
    double DefaultVariance() const;                  // 获取默认位置方差
    double DefaultObjectRadius() const;              // 获取默认目标半径

private:
    bool FastFilter();           // 近/远地点快速过滤（一级筛选）
    void PredictNextState();     // 按轨道角步长推进预测下一状态（二级筛选）
    double FindMinimum();        // 五次样条插值搜索距离函数极小值（三级筛选）
    double ComputeNextTime();    // 基于轨道运动学估计下一步时间

    Object mPrimary;             // 主目标对象
    Object mSecondary;           // 次目标对象
    Options mOptions;            // 评估选项参数
    State mCurrent;              // 当前步进区间的起始状态
    State mNext;                 // 当前步进区间的终止状态
    Status mStatus;              // 当前搜索状态
    Encounter mEncounter;        // 当前相遇计算对象
};
```

## 3. 典型调用模式

```cpp
// ============================================================
// 1. 构造 Options（评估选项）—— 配置搜索参数
// ============================================================
WsfOrbitalConjunctionAssessment::Options options;
options.mCutRadius          = 100000.0;   // 快速过滤距离阈值 100 km
options.mStepRadians        = M_PI / 60.0; // 步长角 3 度
options.mExclusionFactor    = 8.0;        // 椭球缩放因子
options.mInitialSearchTime  = 0.0;        // 从仿真开始时刻起搜索（单位：s）
options.mFinalSearchTime    = 86400.0;    // 搜索到 1 天后（单位：s）
options.mDefaultObjectRadius = 1.0;       // 默认目标半径 1 m
options.mDefaultVariance     = 10.0;      // 默认位置方差 10 m

// ============================================================
// 2. 构造评估器 —— 创建两目标对象并执行快速过滤
// ============================================================
WsfOrbitalConjunctionAssessment assessment(
    primaryTrack,    // 主目标航迹（WsfLocalTrack&）
    5.0,             // 主目标尺寸 5 m
    secondaryTrack,  // 次目标航迹（WsfLocalTrack&）
    3.0,             // 次目标尺寸 3 m
    options,         // 评估选项
    propPtr           // 轨道外推器原型指针
);

// ============================================================
// 3. 循环查找所有交会事件 —— 每次 FindNext() 前进到下一个交会
// ============================================================
while (!assessment.ReachedFinalTime()) {
    auto status = assessment.FindNext();

    if (status == WsfOrbitalConjunctionAssessment::Status::cCONJUNCTION_FOUND) {
        // 获取当前交会记录
        WsfOrbitalConjunctionRecord record = assessment.CurrentConjunction();

        // 输出/记录交会数据
        // record.mPrimary —— 主目标名称
        // record.mSecondary —— 次目标名称
        // record.mMinTime —— 最近点时间 (s)
        // record.mMissDistance —— 脱靶距离 (m)
        // record.mMaxProbability —— 碰撞概率 (0~1)
        // record.mStartTime —— 进入危险区时间 (s)
        // record.mEndTime —— 离开危险区时间 (s)
        // record.mRelativeVelocity —— 最近点相对速度 (m/s)
        log_conjunction(record);
    }
}
```

## 4. 坐标系与单位约定

| 坐标系 | 说明 |
|--------|------|
| **ECI (Earth-Centered Inertial)** | 地心惯性系，用于存储和传播目标的位置/速度/加速度 |
| **WCS (WCS/ECEF)** | 地心地固坐标系，用于航迹的位置/速度输入和协方差计算 |

**单位约定（SI 制）**：

| 物理量 | 单位 |
|--------|------|
| 位置/距离 | m |
| 速度 | m/s |
| 加速度 | m/s^2 |
| 时间 | s |
| 角度 | rad |
| 协方差 | m^2 (位置方差) |

## 5. 框架依赖解耦

| AFSIM 原始依赖 | 职责 | 替换方案 |
|---------------|------|----------|
| `WsfLocalTrack` | 航迹数据（提供位置、速度、滤波器） | 自定义 `TrackData` 结构体（含位置、速度、协方差） |
| `UtOrbitalPropagatorBase` | 轨道外推器（Kepler / NORAD 模型） | 自定义 `OrbitalPropagator` 接口（支持 Propagate 和 GetOrbitalElements） |
| `UtQuinticSpline` | 五次样条插值（用于距离函数和路径构造） | 自定义 `QuinticSpline` 类（TwoPoint 构造 + Derivative + Zeros） |
| `UtCubicSpline` | 三次样条插值（用于椭球函数求交） | 自定义 `CubicSpline` 类（FourPoint 构造 + Derivative + Zeros） |
| `UtGoldenSectionSearch` | 一维黄金分割极小值搜索 | 自定义 `GoldenSectionSearch` 函数模板 |
| `UtCovariance` | 协方差矩阵（含加、乘、求逆） | 自定义 `CovarianceMatrix` 类（支持基本线性代数运算） |
| `UtCalendar` | 日历时间（儒略日、相对时间转换） | 可简化为 `double` 类型的相对仿真时间（若不需要绝对历元） |
| `UtVec3d` | 三维矢量（加减、点积、叉积、归一化、模长） | 自定义 `Vec3` 类或使用 Eigen 库 |
| `UtMath::ErrorFunction` | 误差函数 erf(x)（用于 Vallado 碰撞概率公式） | 使用 `std::erf`（C++11 起标准库提供） |
| `WsfFilter` | 航迹滤波器（提供协方差矩阵） | 自定义 `FilterInterface` 抽象类 |
| `std::unique_ptr` | 轨道外推器的所有权管理 | 直接使用，C++ 标准库 |
