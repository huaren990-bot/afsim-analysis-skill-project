# 05 — 架构推导决策

**日期**：2026-06-08
**状态**：草稿期

---

## 1. 子系统划分依据

### 决策：按功能域划分 14 个子系统

**依据**：
1. 文件命名规律：Wsf 前缀后的第一个词通常标识子系统（WsfEM_* → EM 子系统，WsfTrack* → 跟踪子系统）
2. 目录组织：wsf/source/ 下的子目录（sensor/, mover/, comm/ 等）直接对应子系统
3. 类继承关系：WsfObject → WsfPlatform → 子系统组件这一继承线定义了清晰的层次

### 子系统间关系推导

```
应用层 (Application) → 场景层 (Scenario) → 仿真层 (Simulation)
                                                      ↓
                                                 实体层 (Platform)
                                                      ↓
                         感知层 (Sensor/Comm/Processor) ←→ 环境层 (Terrain/Environment/EM)
```

### 不确定处

- WsfMover 和 WsfFuel 是否应当从 Platform 子系统独立出来列为独立子系统？当前将其作为 Platform 的强依赖组件
- EM 系统和 Sensor 系统的边界在何处？当前将 EM_Types/EM_Manager/天线/传播等列为 EM 子系统，传感器特定逻辑列为 Sensor 子系统

## 2. 数据流推导过程

### 仿真主循环

通过阅读 WsfSimulation 头文件和 WsfEventManager 实现推导：
1. WsfSimulation 维护 WsfEventManager（事件队列）+ WsfEM_Manager（收发机）
2. 事件队列按时间排序分派 → Platform::Update → 各组件更新
3. 组件初始化顺序由 cWSF_INITIALIZE_ORDER_* 控制（Mover 在 Sensor 之前）

### 传感器→跟踪 数据流

从 WsfTrackManager、WsfCorrelationStrategy、WsfFusionStrategy 的接口推导：
1. 传感器生成 Raw WsfTrack → 送入 TrackManager
2. TrackManager 调用 CorrelationStrategy 进行关联配对
3. 配对结果送入 FusionStrategy → 生成 WsfLocalTrack

## 3. 关键全局参数作用分析

### 组件初始化顺序

cWSF_INITIALIZE_ORDER_* 常量（负值，从 -100M 到 -1000M）的意义：
- 这些不是"初始化所需时间"，而是"初始化顺序优先级"
- Mover（-800M）在 Sensor（-500M）之前，确保位置定义在感知之前
- 大间隔（100M）允许在中间插入新组件的初始化

### 仿真状态机

7 个状态严格顺序转换，不允许跳跃：
- cPENDING_INITIALIZE → cINITIALIZING：调用 Initialize 时
- cINITIALIZING → cPENDING_START：初始化完成
- cPENDING_START → cSTARTING：调用 Start 时
- cSTARTING → cACTIVE：开始成功
- cACTIVE → cPENDING_COMPLETE：仿真逻辑完成
- cPENDING_COMPLETE → cCOMPLETE：调用 Complete 时

这一设计保证了仿真生命周期的可预测性。

### 组件角色的编号策略

cWSF_COMPONENT_* 编号反映了系统架构演进：
- 1-18：平台核心组件（PLATFORM→THERMAL_SYSTEM）
- 61-72：通信组件（后续扩展）
- 98-99：EM 收发机
- 100-108：非平台核心组件（后续扩展）

编号不连续说明框架在逐步演进中，不同时期添加了不同组件类型。

## 4. 实现模式总结

### 多继承组件模式

WsfPlatform 是多继承的典型：
```
WsfObject (name+type)
+ WsfPlatformComponent (组件接口, = WsfComponentT<WsfPlatform>)
+ WsfPlatformComponentList (子组件容器)
+ WsfUniqueId (唯一 ID)
+ UtEntity (实体)
+ WsfAuxDataEnabled (辅助数据)
```

### 策略模式

多处使用策略模式实现可插拔行为：
- WsfCorrelationStrategy / WsfFusionStrategy → TrackManager
- WsfEM_Propagation / WsfEM_Attenuation → EM 交互
- WsfTrackExtrapolationStrategy / WsfTrackReportingStrategy → Track

### 观察者模式

WsfSimulation 维护 30+ 种观察者列表：
- WsfPlatformObserver, WsfSensorObserver, WsfTrackObserver
- WsfCommObserver, WsfMoverObserver, WsfProcessorObserver
- WsfDisObserver, WsfExchangeObserver, WsfZoneObserver
- 等等

### 变量绑定模式

WsfVariable<T> 提供固定值和脚本引用之间的透明切换：
```
WsfVariable<double> mHeight = 0.0;  // 可以是固定值
// 或通过输入文件绑定到脚本变量：height = $script_var_name
```
