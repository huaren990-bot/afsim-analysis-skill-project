# AFSIM 扩展点分析

> 生成日期：2026-06-22
> 阶段：Phase 6

## 扩展机制总览

| # | 扩展机制 | 关键接口 | 基类 | 识别来源 |
|---|---------|---------|------|---------|
| 1 | 组件工厂 (Component Factory) | WsfComponentFactory / WsfObjectTypeList<T> | WsfObject | symbol-index.jsonl 中的 using TypeList 声明 |
| 2 | 插件系统 (Plugin System) | WsfPlugin / Plugin base class | Plugin | dependency-index.jsonl 中的 Plugin 继承关系 |
| 3 | 事件总线 (Event Bus) | WsfEvent / Subscribe / Publish / EventPipe | WsfEvent | function-index.jsonl 中的 event_handling l |
| 4 | 脚本扩展 (Script Extension) | UtScriptClass / UtScriptAccessible | UtScriptAccessible | inheritance: UtScriptAccessible (348 des |
| 5 | 仿真扩展点 (Simulation Extension) | WsfSimulationExtension | WsfSimulationExtension | dependency-index.jsonl 中的 registration 条 |
| 6 | 策略模式 (Strategy Pattern) | WsfFusionStrategy / WsfTrackExtrapolationStrategy | WsfFusionStrategy | inheritance graph 中的 Strategy 基类 |

## 组件工厂 (Component Factory)

| 属性 | 值 |
|------|-----|
| 关键接口/基类 | `WsfComponentFactory / WsfObjectTypeList<T>` |
| 扩展机制 | 通过 DECLARE_COMPONENT_ROLE_TYPE / REGISTER_TYPE 宏注册新组件类型到全局工厂 |
| 识别来源 | symbol-index.jsonl 中的 using TypeList 声明 |

**使用示例**：
- `WsfFusionStrategyTypes`
- `WsfSensorTypes`
- `WsfMoverTypes`

---

## 插件系统 (Plugin System)

| 属性 | 值 |
|------|-----|
| 关键接口/基类 | `WsfPlugin / Plugin base class` |
| 扩展机制 | 动态库加载 (LoadLibrary/dlopen) + PluginManager::Load 接口 |
| 识别来源 | dependency-index.jsonl 中的 Plugin 继承关系 |

**使用示例**：
- `wsf_space`
- `wsf_cyber`
- `wsf_six_dof`
- `wsf_p6dof`

---

## 事件总线 (Event Bus)

| 属性 | 值 |
|------|-----|
| 关键接口/基类 | `WsfEvent / Subscribe / Publish / EventPipe` |
| 扩展机制 | 发布-订阅模式，通过 WsfEventPublisher 分发事件到已注册的观察者 |
| 识别来源 | function-index.jsonl 中的 event_handling lifecycle_role 函数 |

**使用示例**：
- `SimEvent`
- `TrackUpdateEvent`
- `SensorDetectionEvent`

---

## 脚本扩展 (Script Extension)

| 属性 | 值 |
|------|-----|
| 关键接口/基类 | `UtScriptClass / UtScriptAccessible` |
| 扩展机制 | C++ 类通过 UT_SCRIPT_* 宏暴露方法到 Lua/Python 脚本层 |
| 识别来源 | inheritance: UtScriptAccessible (348 descendants) |

**使用示例**：
- `WsfScriptPlatformClass`
- `WsfScriptTrackClass`
- `WsfScriptSimulationClass`

---

## 仿真扩展点 (Simulation Extension)

| 属性 | 值 |
|------|-----|
| 关键接口/基类 | `WsfSimulationExtension` |
| 扩展机制 | 通过 AddExtension/RegisterExtension 在仿真生命周期的特定阶段注入自定义逻辑 |
| 识别来源 | dependency-index.jsonl 中的 registration 条目 |

**使用示例**：
- `WsfBallisticMissileLaunchComputerSharedData`
- `WsfStandardOpticalSignature`

---

## 策略模式 (Strategy Pattern)

| 属性 | 值 |
|------|-----|
| 关键接口/基类 | `WsfFusionStrategy / WsfTrackExtrapolationStrategy` |
| 扩展机制 | 运行时通过多态切换算法策略（如轨道预报器、融合策略） |
| 识别来源 | inheritance graph 中的 Strategy 基类 |

**使用示例**：
- `WsfFusionStrategy`
- `WsfTrackExtrapolationStrategy`

---

## 注册依赖统计

dependency-index.jsonl 中共 1557 条 registration 依赖。

| 注册目标 | 出现次数 |
|---------|--------|
| WsfObjectTypeList | 244 |
| COMPONENT_ROLE_TYPE | 88 |
| PACKET | 77 |
| TypeList | 74 |
| RegisterComponentFactory | 68 |
| AddComponent | 62 |
| WsfComponentFactory | 52 |
| GetTypeList | 44 |
| CreateTypeList | 42 |
| AddTypeList | 41 |
