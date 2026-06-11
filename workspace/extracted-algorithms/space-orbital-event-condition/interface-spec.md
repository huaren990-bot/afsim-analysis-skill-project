# 轨道事件条件系统 -- 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** space-orbital-event-condition-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────┐
│              WsfOrbitalEvent（轨道事件执行器）              │
│  调度条件检查 → 执行事件 → 安排下一事件                     │
├──────────────────────────────────────────────────────────┤
│  + Execute(context) -- 当仿真时间到达预设时刻时执行         │
│    → mCondition->GetTimeToCondition(propagator, time)     │
└──────────────┬───────────────────────────────────────────┘
               │ 包含
               ▼
┌──────────────────────────────────────────────────────────┐
│        OrbitalPropagatorCondition（条件抽象基类）          │
│  所有条件的共同接口 + mOrbitNumber（跳过的轨道圈数）        │
├──────────────────────────────────────────────────────────┤
│  + GetTimeToCondition(propagator, time) → bool (纯虚)     │
│  + Accept(visitor) -- 访问者模式                          │
│  + GetOrbitNumber() / SetOrbitNumber(n)                   │
└──────────────┬───────────────────────────────────────────┘
               │ 继承
     ┌─────────┼──────────────────────────┐
     │ 直接求解（无搜索）                    │ 优化搜索求解
     ▼                                     ▼
┌──────────────────────┐    ┌──────────────────────────────────────┐
│ NoneCondition        │    │ OrbitalPropagatorOptimizingCondition   │
│ RelativeTimeCondition│    │ (模板方法基类)                          │
│ EclipseEntry/Exit    │    │ GetTimeToCondition() → 二分/增步搜索    │
└──────────────────────┘    ├──────────────────────────────────────┤
                            │ + Objective(prop, epoch, t) → bool    │
                            │ + InitialGuess(prop) → (bool, double) │
                            │ + HandleSpecialCases(prop, time)       │
                            └──────────────┬───────────────────────┘
                                           │ 派生 8 个条件子类
           ┌──────────┬──────────┬─────────┼──────────┬──────────┐
           ▼          ▼          ▼         ▼          ▼          ▼
    Periapsis  Apoapsis  AscNode  DescNode  AscRadius  DescRadius
    (近地点)   (远地点)   (升交点) (降交点)  (上升穿越) (下降穿越)
                              │
                              ▼
                    ┌──────────────────────┐
                    │ IntersectionCondition │
                    │ (轨道面交线条件基类)   │
                    ├──────────────────────┤
                    │ + OrbitNormal(RAAN,i) │
                    └──────────┬───────────┘
                          ┌────┴─────┐
                          ▼          ▼
                  NorthernInt  SouthernInt
                  (北交线)     (南交线)
```

## 2. 核心接口定义

### 2.1 ConditionType（条件类型枚举）

```cpp
// 12 种轨道事件条件子类的类型标识
// 每个子类都有一个对应的 cTYPE 字符串常量（如 "periapsis"、"ascending_node"），
// 场景文件中通过此字符串键配置条件类型
enum class OrbitalConditionType {
    NONE,                   // "none"              -- 无条件（立即执行）
    RELATIVE_TIME,          // "relative_time"     -- 相对时间偏移
    PERIAPSIS,              // "periapsis"         -- 近地点
    APOAPSIS,               // "apoapsis"          -- 远地点
    ASCENDING_NODE,         // "ascending_node"    -- 升交点（北向穿越赤道面）
    DESCENDING_NODE,        // "descending_node"   -- 降交点（南向穿越赤道面）
    ECLIPSE_ENTRY,         // "eclipse_entry"     -- 进入地影
    ECLIPSE_EXIT,          // "eclipse_exit"      -- 离开地影
    ASCENDING_RADIUS,      // "ascending_radius"  -- 上升穿越指定半径
    DESCENDING_RADIUS,     // "descending_radius" -- 下降穿越指定半径
    NORTHERN_INTERSECTION, // "northern_intersection" -- 北向轨道面交线
    SOUTHERN_INTERSECTION, // "southern_intersection" -- 南向轨道面交线
};
```

### 2.2 OrbitalPropagatorCondition（条件抽象基类）

```cpp
// 所有轨道事件条件的抽象基类
// 定义条件求解的统一接口，具体条件通过派生实现
class OrbitalPropagatorCondition {
public:
    virtual ~OrbitalPropagatorCondition() = default;

    // 深拷贝克隆
    virtual OrbitalPropagatorCondition* Clone() const = 0;

    // 从场景配置文件解析条件参数
    virtual bool ProcessInput(UtInput& input);

    // 获取/设置轨道圈数
    // mOrbitNumber = 0 表示当前圈即可触发条件
    // mOrbitNumber = N 表示跳过 N 圈完整轨道后才检测条件
    unsigned GetOrbitNumber() const;
    void SetOrbitNumber(unsigned orbit_number);

    // 参数验证（子类可覆写）
    // 返回 true 表示所有参数在合法范围内
    virtual bool ValidateParameterRanges() const;

    // 核心接口：计算到条件满足的时间
    // 参数:
    //   aPropagator: 轨道传播器引用（提供当前轨道状态）
    //   aTimeToCondition [out]: 从传播器当前时刻到条件满足的秒数
    // 返回: true=成功找到条件时间, false=无法确定（双曲线/未包围/未收敛）
    virtual bool GetTimeToCondition(
        const UtOrbitalPropagatorBase& propagator,
        double& time_to_condition_s    // [out] 单位：秒
    ) const = 0;

    // 接受访问器（访问者模式）
    virtual void Accept(OrbitalPropagatorConditionVisitor& visitor) = 0;

    // 返回条件的字符串标识
    virtual std::string GetConditionString() const = 0;

protected:
    unsigned mOrbitNumber = 0;  // 跳过的轨道圈数
};
```

### 2.3 OrbitalPropagatorOptimizingCondition（优化条件模板方法基类）

```cpp
// 利用二分/增步搜索求解的条件的模板方法基类
// 派生类只需覆写三个虚函数即可适配任意轨道传播器：
//   Objective()    -- 目标函数（返回布尔值指示在根之前/之后）
//   InitialGuess() -- 二体近似的初值猜测
//   HandleSpecialCases() -- 退化轨道处理（圆轨道、赤道轨道等）
// GetTimeToCondition() 为 final 实现，不可覆写
class OrbitalPropagatorOptimizingCondition : public OrbitalPropagatorCondition {
public:
    // ===================== 三个必须覆写的虚函数 =====================

    // 目标函数（Objective Function）
    // 将传播器推进到 aBaseEpoch + aOffsetTime 时刻
    // 返回的布尔值指示该时刻在根的"之前"还是"之后"
    // 具体含义由子类定义（如近地点条件：v·r̂ < 0 表示在近地点之前）
    // 参数:
    //   propagator: 可修改的传播器（会调用 Update 推进到评估时刻）
    //   base_epoch: 搜索起点（绝对日历时间）
    //   offset_time: 从 base_epoch 起算的偏移 (s)
    // 返回: true=在根之前, false=在根之后
    virtual bool Objective(
        UtOrbitalPropagatorBase& propagator,
        const UtCalendar& base_epoch,
        double offset_time_s
    ) const = 0;

    // 初值猜测
    // 利用传播器内置的二体机动传播器做解析预测
    // 返回: pair<bool, double>
    //   .first = true 表示猜测成功，.second 为猜测时间 (s)
    //   .first = false 表示无法猜测（如赤道轨道查交点无 RAAN 定义）
    virtual std::pair<bool, double> InitialGuess(
        const UtOrbitalPropagatorBase& propagator
    ) const = 0;

    // 退化轨道处理
    // 检测圆轨道（近/远地点无定义）、赤道轨道（升/降交点无定义）、
    // 反平行轨道面（处处是交线）等特殊情形
    // 参数:
    //   propagator: 传播器引用
    //   time_to_condition_s [out]: 若检测到特殊情形，直接设置为 mOrbitNumber * period
    // 返回: true=检测到特殊情形并已设置时间; false=无特殊情形，需要搜索
    virtual bool HandleSpecialCases(
        const UtOrbitalPropagatorBase& propagator,
        double& time_to_condition_s    // [out]
    ) const { return false; }  // 默认：无特殊情形

    // ===================== 模板方法（final 实现，不可覆写） =====================

    // 条件求解主流程：
    //   1. 前置检查：拒绝双曲线轨道
    //   2. HandleSpecialCases：检测退化轨道
    //   3. InitialGuess：二体近似初值
    //   4. 克隆传播器（避免污染原始状态）
    //   5. 偏移 mOrbitNumber * period 圈
    //   6. 试探 + 扩展区间包围根
    //   7. UtBinarySearch 二分迭代收敛
    //   8. 结果合成（偏移 + 圈数补偿）
    bool GetTimeToCondition(
        const UtOrbitalPropagatorBase& propagator,
        double& time_to_condition_s
    ) const final;  // final：子类不可覆写
};
```

### 2.4 直接求解条件接口（NoneCondition / RelativeTimeCondition）

```cpp
// 无条件：立即执行（返回 0.0 或 mOrbitNumber * period）
class NoneCondition : public OrbitalPropagatorCondition {
public:
    NoneCondition();
    NoneCondition* Clone() const override;

    // 不需要搜索：直接返回 0.0 + mOrbitNumber * period
    bool GetTimeToCondition(
        const UtOrbitalPropagatorBase& propagator,
        double& time_to_condition_s
    ) const override;

    static constexpr const char* cTYPE = "none";
};

// 相对时间条件：在指定时间偏移后触发
class RelativeTimeCondition : public OrbitalPropagatorCondition {
public:
    RelativeTimeCondition();
    RelativeTimeCondition* Clone() const override;

    bool ProcessInput(UtInput& input) override;

    // 获取/设置偏移时间 (s)
    UtTimeValue GetOffsetTime() const;
    void SetOffsetTime(const UtTimeValue& offset_time);

    // 参数验证：mOffsetTime >= 0
    bool ValidateParameterRanges() const override;

    // 不需要搜索：直接返回 mOffsetTime + mOrbitNumber * period
    bool GetTimeToCondition(
        const UtOrbitalPropagatorBase& propagator,
        double& time_to_condition_s
    ) const override;

    static constexpr const char* cTYPE = "relative_time";

private:
    UtTimeValue mOffsetTime{};  // 偏移时间 (s)
};
```

### 2.5 各几何条件子类接口

```cpp
// ===================== 近地点条件 =====================
class PeriapsisCondition : public OrbitalPropagatorOptimizingCondition {
    // Objective: v·r̂ < 0 → 在近地点之前（径向速度向内）
    //   f(t) = vel · r̂
    //   条件：寻找 f(t) 从负穿越零变为正的时刻
    // HandleSpecialCases: 圆轨道（OrbitIsCircular）→ 返回 mOrbitNumber * period
    // InitialGuess: 二体传播器的 GetTimeToPeriapsisPassage(mOrbitNumber)
    static constexpr const char* cTYPE = "periapsis";
};

// ===================== 远地点条件 =====================
class ApoapsisCondition : public OrbitalPropagatorOptimizingCondition {
    // Objective: v·r̂ > 0 → 在远地点之前（径向速度向外）
    //   f(t) = vel · r̂
    //   条件：寻找 f(t) 从正穿越零变为负的时刻
    // HandleSpecialCases: 圆轨道 → 返回 mOrbitNumber * period
    static constexpr const char* cTYPE = "apoapsis";
};

// ===================== 升交点条件 =====================
class AscendingNodeCondition : public OrbitalPropagatorOptimizingCondition {
    // Objective: z_TOD < 0 → 在升交点之前（赤道面以下/南半球）
    //   f(t) = z_TOD(t)  -- ECI TOD 坐标系的 Z 分量
    //   条件：寻找 z 从负穿越零变为正的时刻（且 ż > 0）
    // HandleSpecialCases: 赤道轨道（OrbitIsEquatorial）→ 返回 mOrbitNumber * period
    static constexpr const char* cTYPE = "ascending_node";
};

// ===================== 降交点条件 =====================
class DescendingNodeCondition : public OrbitalPropagatorOptimizingCondition {
    // Objective: z_TOD > 0 → 在降交点之前（赤道面以上/北半球）
    //   f(t) = z_TOD(t)
    //   条件：寻找 z 从正穿越零变为负的时刻（且 ż < 0）
    // HandleSpecialCases: 赤道轨道 → 返回 mOrbitNumber * period
    static constexpr const char* cTYPE = "descending_node";
};

// ===================== 地影进入/离开条件（非优化类）=====================
class EclipseEntryCondition : public OrbitalPropagatorCondition {
    // 直接委托传播器: propagator.GetEclipseTimes() → 取 entry time
    static constexpr const char* cTYPE = "eclipse_entry";
};

class EclipseExitCondition : public OrbitalPropagatorCondition {
    // 直接委托传播器: propagator.GetEclipseTimes() → 取 exit time
    static constexpr const char* cTYPE = "eclipse_exit";
};

// ===================== 半径穿越条件 =====================
class AscendingRadiusCondition : public RadiusCondition {
    // Objective: r < r_target → 在目标半径之下
    //   f(t) = r(t) - r_target
    //   条件：寻找 r(t) 从下往上穿越 r_target 的时刻
    // 配置参数: mRadius > 0 (m)
    static constexpr const char* cTYPE = "ascending_radius";
};

class DescendingRadiusCondition : public RadiusCondition {
    // Objective: r > r_target → 在目标半径之上
    //   f(t) = r(t) - r_target
    //   条件：寻找 r(t) 从上往下穿越 r_target 的时刻
    static constexpr const char* cTYPE = "descending_radius";
};

// ===================== 轨道面交线条件 =====================
class NorthernIntersectionCondition : public IntersectionCondition {
    // Objective: r̂_TOD · n̂_2 > 0 → 在交线之前（北交点正侧）
    //   n̂_2 = OrbitNormal(RAAN_target, i_target)
    //   f(t) = r̂_TOD(t) · n̂_2
    //   条件：寻找 f(t) 穿越零的时刻
    // HandleSpecialCases: n̂_1 · n̂_2 ≈ -1（反平行，处处为交点）
    static constexpr const char* cTYPE = "northern_intersection";
};

class SouthernIntersectionCondition : public IntersectionCondition {
    // 同上，但方向相反
    static constexpr const char* cTYPE = "southern_intersection";
};
```

### 2.6 BinarySearch（二分搜索工具类简化接口）

```cpp
// 二分/增步搜索器（为移植而简化的接口，不含 AFSIM 专属依赖）
// AFSIM 原始代码中使用 UtBinarySearch 类
class BinarySearchSolver {
public:
    // 搜索配置
    struct Config {
        size_t max_iterations = 60;       // 最大迭代次数
        double tolerance      = 1e-8;     // 收敛容差 (s)，bestSuccess - bestFailure < tolerance 时收敛
        double increment_ratio = 1.5;     // 增步比率（未包围时按此比率扩展区间）
    };

    // 初始化搜索器
    // find_max: true=查找目标函数返回 true 的最大值; false=查找最小值
    void Initialize(bool find_max, const Config& config);

    // 注册试探点，更新搜索状态
    // trial_value: 试探点的自变量值（时间偏移，单位 s）
    // trial_result: 试探点的目标函数布尔值
    // [out] converged: 搜索是否收敛
    // [out] bracketed: 搜索区间是否已包围根
    // [out] next_trial: 下一个试探点建议值
    void Update(
        double trial_value,
        bool trial_result,
        bool& converged,   // [out]
        bool& bracketed,   // [out]
        double& next_trial // [out]
    );

    // 当前最优值对
    double best_success;  // 最近一次返回 true 的最优试探点
    double best_failure;  // 最近一次返回 false 的最优试探点
};
```

## 3. 典型调用模式

```cpp
// ============================================================
// 1. 配置条件（从场景文件解析）
// ============================================================

// 创建近地点条件
auto condition = std::make_unique<PeriapsisCondition>();
condition->ProcessInput(input);   // 读取 "periapsis" 配置块
condition->SetOrbitNumber(0);     // 当前圈即可触发

// 创建升交点条件（第 3 圈完整轨道之后）
auto condition2 = std::make_unique<AscendingNodeCondition>();
condition2->SetOrbitNumber(3);

// 创建指定半径穿越条件（穿越 7000 km 半径）
auto condition3 = std::make_unique<AscendingRadiusCondition>();
condition3->SetRadius(UtLengthValue(7000000.0, "m"));  // 7000 km
condition3->ValidateParameterRanges();  // 验证半径 > 0

// ============================================================
// 2. 事件执行：计算到条件的时间
// ============================================================
// 在 WsfOrbitalEvent::Execute(context) 中调用：

double time_to_condition_s;
bool found = condition->GetTimeToCondition(propagator, time_to_condition_s);

if (found) {
    // 条件成功找到！
    // 在 (当前时间 + time_to_condition_s) 秒后触发事件
    double next_event_time = current_time + time_to_condition_s;
    scheduleEvent(next_event_time, my_event_handler);
} else {
    // 条件无法确定：双曲线轨道 / 搜索未收敛 / 无解
    // time_to_condition_s = -1.0
    handleConditionFailure();
}
// ============================================================
// 3. 完整场景：近地点事件调度
// ============================================================

// 为椭圆轨道创建近地点事件
PeriapsisCondition periapsis_cond;
periapsis_cond.SetOrbitNumber(0);

double time_to_periapsis;
bool found = periapsis_cond.GetTimeToCondition(sat_propagator, time_to_periapsis);

if (found && time_to_periapsis > 0.0) {
    // 在近地点时刻安排相机拍照
    scheduleTargetingEvent(current_time + time_to_periapsis);
} else if (found && time_to_periapsis == 0.0) {
    // 已经在近地点！立即执行
    executeImmediately();
} else {
    // 圆轨道或搜索失败
    log("近地点无定义或搜索失败");
}
// ============================================================
// 4. 自定义条件子类（模板方法模式）
// ============================================================

// 只需覆写三个虚函数即可创建自定义条件
class MyCustomCondition : public OrbitalPropagatorOptimizingCondition {
public:
    // 目标函数：比较当前高度与目标高度
    bool Objective(UtOrbitalPropagatorBase& prop,
                   const UtCalendar& base_epoch,
                   double offset_time) const override {
        // 推进传播器到评估时刻
        UtCalendar eval_time = base_epoch;
        eval_time.AdvanceTimeBy(offset_time);
        prop.Update(eval_time);

        double r = prop.GetOrbitalState().Position().Magnitude();
        double h = r - EARTH_RADIUS;  // 轨道高度

        // 返回：h < target_altitude 时在条件之前
        return h < mTargetAltitude;
    }

    // 二体初值猜测
    std::pair<bool, double> InitialGuess(
        const UtOrbitalPropagatorBase& prop) const override {
        // 用半圈周期作为初值
        double period = prop.GetOrbitalElements().GetPeriod();
        return {true, 0.5 * period};
    }

    double mTargetAltitude;  // 目标高度
};
```

## 4. 坐标系/单位约定

| 量 | 单位 | 说明 |
|----|------|------|
| 时间偏移 (offset_time) | 秒 (s) | 从基准历元起算的相对时间 |
| 时间收敛容差 (tolerance) | 秒 (s) | ε = 1e-8 (约 10 ns) |
| 最大迭代次数 | 次 (无量纲) | N_max = 60 |
| 轨道周期 (period) | 秒 (s) | GetOrbitalElements().GetPeriod() |
| 位置矢量 | 米 (m) | ECI / TOD 坐标系 |
| 速度矢量 | 米/秒 (m/s) | ECI 坐标系 |
| 地心距 (r) | 米 (m) | r = sqrt(x² + y² + z²) |
| 目标半径 (mRadius) | 米 (m) | 配置参数，必须 > 0 |
| 轨道倾角 (mInclination) | 弧度 (rad) | 0 = 赤道轨道 |
| 升交点赤经 (mRAAN) | 弧度 (rad) | 0 ~ 2π |
| 点积/叉积 | 无量纲 | 矢量运算 |
| 日历时间 (base_epoch) | UTC 日历 | UtCalendar 表示绝对时间 |

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|---------|----------|
| `UtOrbitalPropagatorBase` | 轨道传播器抽象基类 | 自定义 OrbitPropagator 接口（提供 GetOrbitalState, Update, GetManeuveringPropagator 等方法） |
| `UtBinarySearch` | 二分/增步搜索器 | 自定义 BinarySearchSolver（如 2.6 节所定义） |
| `UtVec3d` | 3D 向量 | Eigen::Vector3d 或自定义 Vec3 |
| `UtCalendar` | 日历/时间系统 | 自定义 Time 类（支持 absolute time + offset 运算） |
| `UtUnitTypes` (UtTimeValue, UtLengthValue, UtSpeedValue) | 带单位的量纲类型 | 自定义 UnitValue 类或直接用 double + 硬编码单位转换 |
| `WsfObject` | AFSIM 对象基类（类型注册、克隆） | 自定义 Object 基类或直接剥离 |
| `ut::clone()` | 深拷贝工具函数 | C++ 拷贝构造函数或工厂方法 |
| `OrbitalPropagatorConditionVisitor` | 访问者模式 | 此模式仅用于 AFSIM 内部事件调度，可省略（直接使用 dynamic_cast 或虚函数 dispatch） |
| `UtInput` / `UtInputBlock` | 配置解析 | JSON/YAML/TOML 解析器 |
| `WsfOrbitalEvent` / `WsfObjectTypeList` | 事件系统 / 类型注册 | 自定义事件调度系统 |
| `OrbitalTargetPoint` (仅在 Intersection 中) | 目标轨道面定义 | 自定义 TargetOrbitPlane 结构体（RAAN + Inclination + OrbitNormal 辅助函数） |
