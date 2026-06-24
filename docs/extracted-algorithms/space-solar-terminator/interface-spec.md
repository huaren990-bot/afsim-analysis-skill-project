# 太阳终结线与地影分析 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** space-solar-terminator-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│            WsfSolarTerminator (命名空间)              │
│  (太阳终结线——无状态纯函数集合)                        │
├──────────────────────────────────────────────────────┤
│  + GetPhaseOfDay(lat, lon, time, limit) → PhaseOfDay  │
│  + MaskedByHorizon(observerWCS, targetWCS) → bool     │
│  + GetPlatformSolarIllumination(platform) → Enum      │
└──────────┬───────────────────────────────────────────┘
           │ 辅助函数（匿名命名空间，翻译单元内部）
           ▼
┌──────────────────────────────────────────────────────┐
│  匿名命名空间（.cpp 内部）                             │
│  - EllipsoidalInnerProduct(a, b) → double            │
│  - EllipsoidalFunction(location) → double             │
│  - GetDisplacementToSolarLimbs(loc, time, up, low)    │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│          WsfEclipseEventManager                       │
│  (地影事件管理器——有状态调度器)                        │
├──────────────────────────────────────────────────────┤
│  + Initialize() → bool                                │
│  + Enable(simTime)                                    │
│  + Disable()                                          │
│  - InitiateEclipseEvent(simTime, id, mover)           │
│  - InitiateMonitoring(simTime, platform)              │
│  - UpdateMonitoring(simTime, mover, maneuver)         │
│  └─── EclipseEvent (内部类)                           │
│       ├─ Execute() → EventDisposition                 │
│       └─ 状态机: cENTRY ↔ cEXIT, cEVALUATE            │
└──────────┬───────────────────────────────────────────┘
           │ 依赖
           ▼
┌──────────────────────────────────────────────────────┐
│  外部依赖                                            │
│  - UtSun (太阳位置、NED方向、太阳半径)                 │
│  - UtEarth (地球椭球赤道半径 cA、极半径 cB)           │
│  - UtVec3d (三维矢量运算)                              │
│  - UtOrbitalPropagatorBase::GetEclipseTimes()         │
│  - WsfEvent / WsfObserver (仿真事件调度框架)           │
└──────────────────────────────────────────────────────┘
```

整体分为两部分：(1) `WsfSolarTerminator` 命名空间提供无状态的太阳照明判断函数；(2) `WsfEclipseEventManager` 提供有状态的地影事件调度，通过仿真事件队列周期性预测并触发入影/出影事件。

## 2. 核心接口定义

### 2.1 PhaseOfDay（天光阶段枚举——GetPhaseOfDay 输出）

```cpp
// 地面观测点的光照阶段分类
enum class PhaseOfDay {
    cDAY      = 1,   // 白天：太阳在地平线下不到 50 角分（即太阳几乎在地平线以上）
    cTWILIGHT = 2,   // 黄昏：介于白天阈值与自定义黄昏限角之间
    cNIGHT    = 3    // 黑夜：太阳天顶角超过限值，充分在地平线以下
};
```

### 2.2 PlatformSolarIllumination（航天器光照状态枚举——GetPlatformSolarIllumination 输出）

```cpp
// 航天器相对于地球阴影的光照状态
enum class PlatformSolarIllumination {
    cINVALID_PLATFORM = 0,  // 无效平台：未关联仿真，无法计算
    cILLUMINATED      = 1,  // 光照区：太阳上下边缘均可见
    cEARTH_PENUMBRA   = 2,  // 半影：仅太阳下边缘被地球遮挡（上边缘可见）
    cEARTH_UMBRA      = 3   // 全影：太阳上下边缘均被地球遮挡
};
```

### 2.3 黄昏阈值常量（WsfSolarTerminator 命名空间中的 constexpr）

```cpp
// 三种标准黄昏定义，取自 Fundamentals of Astrodynamics and Applications, 4th Ed., p.281
// 均为太阳天顶角（即太阳在地平线下的角度）
constexpr double cTWILIGHT_CIVIL        = 96.0;   // 民用黄昏（太阳在地平线下 6°）
constexpr double cTWILIGHT_NAUTICAL     = 102.0;  // 航海黄昏（太阳在地平线下 12°）
constexpr double cTWILIGHT_ASTRONOMICAL = 108.0;  // 天文黄昏（太阳在地平线下 18°）
```

### 2.4 GetPhaseOfDay（天光阶段判别——无状态函数）

```cpp
// 根据地面观测点的经纬度和时间，判断该位置的白天/黄昏/黑夜阶段
// 参数：
//   aLatDegrees  - 地面观测点的地理纬度，单位：度
//   aLonDegrees  - 地面观测点的地理经度，单位：度
//   aTime        - 需要判断天光阶段的世界协调时
//   aLimitDegrees - 黄昏结束角度（太阳天顶角），默认为 cTWILIGHT_CIVIL = 96.0，单位：度
// 返回：PhaseOfDay 枚举值（cDAY / cTWILIGHT / cNIGHT）
//
// 判据（cosTheta = -太阳方向_NED_z，即太阳天顶角的余弦值）：
//   cosTheta > cos(90°50')        → 白天
//   cosTheta > cos(aLimitDegrees) → 黄昏
//   否则                           → 黑夜
PhaseOfDay GetPhaseOfDay(double aLatDegrees, double aLonDegrees,
                         const UtCalendar& aTime,
                         double aLimitDegrees = cTWILIGHT_CIVIL);
```

### 2.5 MaskedByHorizon（地球遮挡判定——无状态函数）

```cpp
// 判断从观测者位置看向目标，目标是否被地球椭球遮挡（不考虑地形）
// 核心方法：视线（从观测者到目标）与地球 WGS-84 椭球的直线-椭球求交（二次方程求根）
//
// 参数：
//   aObserverWCS[3] - 观测者的 WCS/ECEF 位置，单位：m
//   aTargetWCS[3]   - 目标物的 WCS/ECEF 位置（如太阳边缘点），单位：m
// 返回：true = 目标被地球遮挡，false = 目标可见
//
// 算法步骤：
//   1. 计算视线向量 T-O，归一化并获取目标距离 lambdaTarget
//   2. 计算二次方程系数：
//        a = <T-O, T-O>_E （椭球内积，恒正）
//        b = 2·<O, T-O>_E
//        c = <O, O>_E - 1 = F(O) （观测者的椭球函数值）
//   3. 判别式 Δ = b^2 - 4ac
//   4. 若 Δ >= 0，求两根 λ1 >= λ2（因为 a > 0）
//   5. 遮挡判定：λ1 > 0.05m（容差）且 λ2 + 0.05m < lambdaTarget
//      （即视线在到达目标前穿过了地球表面）
bool MaskedByHorizon(const double aObserverWCS[3], const double aTargetWCS[3]);
```

### 2.6 GetPlatformSolarIllumination（航天器光照判别——无状态函数）

```cpp
// 判断指定航天器当前处于全影、半影还是光照区
// 将太阳视为具有有限半径的圆盘，取上下边缘两个点分别判断是否被地球遮挡
//
// 参数：
//   aPlatformPtr - 需要判断地影状态的航天器平台指针
// 返回：PlatformSolarIllumination 枚举值
//
// 算法步骤：
//   1. 若平台未关联仿真 → 返回 cINVALID_PLATFORM
//   2. 获取航天器 WCS 位置和当前仿真时间
//   3. 计算太阳上下边缘的 WCS 位置（GetDisplacementToSolarLimbs）
//   4. 分别对上下边缘调用 MaskedByHorizon
//   5. 根据遮挡组合判定：
//       - 上下均遮挡 → cEARTH_UMBRA（全影）
//       - 仅下边缘遮挡 → cEARTH_PENUMBRA（半影）
//       - 仅上边缘遮挡 → 物理不可能，触发断言
//       - 上下均可见 → cILLUMINATED（光照区）
PlatformSolarIllumination GetPlatformSolarIllumination(WsfPlatform* aPlatformPtr);
```

### 2.7 EclipseEvent（地影事件——WsfEclipseEventManager 内部类）

```cpp
// 仿真事件对象，在地影进入/离开时刻触发，通过状态机在 cENTRY/cEXIT 之间切换
class EclipseEvent : public WsfEvent {
public:
    enum Type {
        cENTRY,     // 入影事件：等待航天器进入地影
        cEXIT,      // 出影事件：等待航天器离开地影
        cEVALUATE   // 重新评估：当前轨道周期内无地影，等待 1/4 轨道周期后重新检查
    };

    // 构造函数
    // aType            - 事件类型（cENTRY / cEXIT / cEVALUATE）
    // aId              - 唯一事件 ID，用于判断事件是否过期
    // aEclipseManager  - 所属的 EclipseEventManager 引用
    // aSpaceMoverPtr   - 关联的航天器运动体指针
    EclipseEvent(Type aType, size_t aId, WsfEclipseEventManager& aEclipseManager,
                 WsfSpaceMoverBase* aSpaceMoverPtr);

    void SetType(Type aType);          // 设置事件类型
    EventDisposition Execute() override; // 事件到期执行

private:
    Type mType;                        // 当前事件类型
    size_t mId;                        // 事件唯一 ID（用于过期验证）
    WsfEclipseEventManager& mEclipseManager;  // 所属管理器引用
    WsfSpaceMoverBase* mSpaceMoverPtr; // 关联的运动体指针
    size_t mPlatformIndex;             // 航天器平台在仿真中的索引
};
```

### 2.8 WsfEclipseEventManager（地影事件管理器——主调度类）

```cpp
// 优化地影事件生成（ECLIPSE_ENTRY 和 ECLIPSE_EXIT）
// 仅在有事件订阅者或 Enable() 被调用时才执行检查
// 事件在入影/出影时刻触发，每次触发时重新评估（考虑地球绕太阳公转导致阴影锥旋转）
// 若当前轨道无地影穿越，则每 1/4 轨道周期重新评估
class WsfEclipseEventManager : public WsfSimulationExtension {
public:
    WsfEclipseEventManager();

    bool Initialize() override;     // 检查是否有地影事件订阅者，有则自动 Enable
    bool IsEnabled() const;         // 是否已启用地影监测

    void Enable(double aSimTime);   // 启用地影监测，注册平台生命周期回调
    void Disable();                 // 禁用地影监测，清空所有事件

private:
    // 为指定航天器启动地影事件预测（调用 GetEclipseTimes 获取入影/出影相对时间）
    void InitiateEclipseEvent(double aSimTime, size_t aId,
                              WsfSpaceMoverBase& aSpaceMover);

    // 平台初始化时回调：若为空间平台则启动监测
    void InitiateMonitoring(double aSimTime, WsfPlatform* aPlatformPtr);

    // 轨道机动后回调：重新计算地影事件
    void UpdateMonitoring(double aSimTime, WsfSpaceMoverBase* aSpaceMoverPtr,
                          const WsfOrbitalEvent& aManeuver);

    void CeaseMonitoring(double aSimTime, WsfPlatform* aPlatformPtr);  // 平台删除时停用

    bool mIsEnabled;                                   // 地影监测是否已启用
    UtCallbackHolder mCallbacks;                       // 持有平台生命周期回调句柄
    std::map<WsfStringId, size_t> mPlatformToCurrentEventIdMap; // 平台名称 → 最新事件 ID（防止过期事件误触发）
};
```

## 3. 典型调用模式

### 3.1 天光阶段判别（简单查询）

```cpp
// 判断北纬 40°、东经 116° 在当前时间的天光阶段，使用航海黄昏阈值
double lat = 40.0;     // 纬度（度）
double lon = 116.0;    // 经度（度）
UtCalendar now;        // 当前时间

// 使用默认民用黄昏（96°）：
auto phase = WsfSolarTerminator::GetPhaseOfDay(lat, lon, now);
// phase == cDAY / cTWILIGHT / cNIGHT

// 使用航海黄昏（102°）：
auto phase2 = WsfSolarTerminator::GetPhaseOfDay(lat, lon, now,
    WsfSolarTerminator::cTWILIGHT_NAUTICAL);
```

### 3.2 航天器地影判别（即时查询）

```cpp
// 查询航天器当前处于全影/半影/光照区
auto illum = WsfSolarTerminator::GetPlatformSolarIllumination(platformPtr);
switch (illum) {
    case PlatformSolarIllumination::cILLUMINATED:
        // 航天器在光照区 —— 太阳能帆板可发电
        break;
    case PlatformSolarIllumination::cEARTH_PENUMBRA:
        // 航天器在半影区 —— 部分光照
        break;
    case PlatformSolarIllumination::cEARTH_UMBRA:
        // 航天器在全影区 —— 无太阳光照
        break;
    case PlatformSolarIllumination::cINVALID_PLATFORM:
        // 平台无效
        break;
}
```

### 3.3 地影事件调度（自动监测）

```cpp
// EclipseEventManager 的典型使用不需要用户手动编码
// 它在仿真初始化时自动启动（若有 ECLIPSE_ENTRY/EXIT 订阅者）
// 用户只需要在仿真场景中订阅地影事件：

// 仿真初始化阶段（自动）：
//   WsfEclipseEventManager::Initialize()
//     → 检测到 ECLIPSE_ENTRY/EXIT 订阅者
//     → 调用 Enable(0.0)
//     → 对每个空间平台调用 InitiateEclipseEvent()

// 运行阶段（自动）：
//   当 EclipseEvent::Execute() 触发时：
//     若 mType == cENTRY：
//       → 调用 WsfObserver::EclipseEntry() 通知所有观察者
//       → mType 切换为 cEXIT，安排在 timeToExit 秒后触发
//     若 mType == cEXIT：
//       → 调用 WsfObserver::EclipseExit() 通知所有观察者
//       → mType 切换为 cENTRY，安排在 timeToEntry 秒后触发

// 用户通过 WsfObserver 接收回调：
//   WsfObserver::EclipseEntry(&sim).Connect([](double time, WsfSpaceMoverBase* mover) {
//       // 航天器进入地影，处理相关逻辑
//   });
```

## 4. 坐标系与单位约定

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **WCS** (ECEF) | 地心地固 | 观测者/目标/太阳边缘的位置矢量；EllipsoidalInnerProduct 的输入坐标 |
| **NED** | X=北, Y=东, Z=地心方向(下) | 天光阶段判别中太阳方向矢量的坐标系 |
| **椭球归一化空间** | 通过赤道半径 A 和极半径 B 缩放 | 直线-椭球求交的内部计算空间 |

**单位约定（SI 制）**：

| 物理量 | 单位 |
|--------|------|
| 位置/距离 | m |
| 角度（输入） | 度 |
| 角度（内部计算） | rad |
| 时间 | s |
| 容差 (cMASKED_BY_EARTH_TOLERANCE) | 0.05 m |
| 地球赤道半径 (UtEarth::cA) | ~6378137 m |
| 地球极半径 (UtEarth::cB) | ~6356752 m |
| 太阳平均半径 (UtSun::cMEAN_RADIUS) | ~6.963420e8 m |

## 5. 框架依赖解耦

| AFSIM 原始依赖 | 职责 | 替换方案 |
|---------------|------|----------|
| `UtSun` | 太阳位置 WCS 计算 (`GetSunLocationWCS`)、太阳 NED 方向 (`GetSunVecNED`)、太阳半径 (`cMEAN_RADIUS`)、太阳赤纬/赤经、太阳黄经 | 自定义 `SunModel` 类（实现太阳星历算法，如 Meeus 或 Vallado 方法） |
| `UtEarth` | 地球椭球参数：赤道半径 `cA`、极半径 `cB` | 直接硬编码 WGS-84 椭球常量（6378137.0 m, 6356752.0 m） |
| `UtVec3d` | 三维矢量运算（加减、点积、叉积、归一化、模长） | 自定义 `Vec3` 类或使用 Eigen/GLM 库 |
| `UtCalendar` | 日历时间（用于太阳位置计算） | 自定义 `DateTime` 类或直接使用儒略日 `double` |
| `UtMath` | 角度转换常量 `cRAD_PER_DEG`、`cTWO_PI`、`cPI` | 直接使用 `M_PI` 宏或自定义转换函数 |
| `WsfPlatform` | 仿真平台（提供 WCS 位置、更新时间、仿真引用） | 自定义 `Platform` 聚合体（含位置矢量和时间信息） |
| `WsfSimulation` | 仿真框架（提供时间、事件队列、平台遍历） | 自定义 `Simulation` 类（含时间管理和平台列表） |
| `UtOrbitalPropagatorBase::GetEclipseTimes()` | 轨道传播器的地影时间预测（EclipseEventManager 核心依赖） | 自定义轨道传播器接口，实现独立的入影/出影时间估计算法 |
| `WsfEvent` / `WsfObserver` | 仿真事件调度和观察者模式 | 自定义 `EventScheduler` + `Signal/Slot` 机制 |
| `WsfSpaceMoverBase` | 空间运动体（含轨道传播器引用和平台引用） | 自定义 `SpaceMover` 聚合体 |
| `WsfOrbitalEvent` | 轨道机动事件（用于触发地影时间重算） | 自定义 `OrbitalManeuverEvent` 结构体 |
| `WsfDateTime` | 仿真日期时间管理 | 自定义 `DateTimeProvider` |
| `std::exp`、`std::cos`、`std::sqrt` | 标准数学函数 | 直接使用，C++ 标准库 |
