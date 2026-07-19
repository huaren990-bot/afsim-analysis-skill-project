# 扩展点识别

## 0. 用途说明

扩展点分析用于识别插件、工厂、注册表、事件订阅、策略/Policy 等扩展边界，帮助判断外部能力如何接入系统、哪些接口可稳定复用、哪些注册路径会改变运行时行为。

## 1. 扩展机制总览

| 扩展机制 | 关键接口/基类 | 注册位置 | 使用示例 | 用途说明 |
|---|---|---|---|---|
| `RegisterExtension` | `WsfApplication::RegisterExtension()`, `wsf::comm::router::medium::WsfScenario::RegisterExtension()`, `wsf::comm::WsfSimulation::RegisterExtension()` | `afsim-2_9/swdev/src/core/sensor_plot_lib/source/WsfSensorPlot.cpp:75` | `aScenario.RegisterExtension(GetExtensionName(), ut::make_unique<WsfSensorPlotExtension>(this));` | 应用或场景扩展注册机制，用于把外部能力挂接到 WsfApplication/WsfScenario 生命周期。 |
| `AddMessage` | `wsf::console::SubscriberBase::AddMessageP()`, `WsfL16::Messages::Factory::AddMessage()`, `rv::PartMap::AddMessage()` | `afsim-2_9/swdev/src/core/wsf_l16/source/MessagesFactory.cpp:33` | `AddMessage(new J2_0::Initial());` | 消息工厂注册机制，用于把消息类型加入消息表。 |
| `EventPipe` | `WsfEventPipeExtension::AddCallback()`, `WsfEventPipeExtension::AddSchema()`, `WsfEventPipeExtension::Find()` | `afsim-2_9/swdev/src/core/wsf/source/xio_sim/WsfXIO_EventPipe.cpp:30` | `void wsf::xio::EventPipe::RegisterEvents(WsfEventPipeExtension& aEventPipeExtension)` | 事件管道订阅/记录机制，用于把仿真事件输出给 Warlock/Mystic 等工具。 |
| `AddComponent` | `WsfComponentList::AddComponentP()`, `wsf::comm::router::Router::AddComponent()`, `ToggleEffect::AddComponent()` | `afsim-2_9/swdev/src/core/sensor_plot_lib/source/MapPlotVariables.cpp:275` | `// after ownership has been transferred to the platform (via AddComponent)` | 平台组件挂接机制，用于给 WsfPlatform 增加传感器、武器、通信等运行时能力。 |
| `Subscribe` | `wsf::console::ConsoleSubscriber::ConsoleSubscriber()`, `wsf::console::ConsoleSubscriber::FlushStream()`, `wsf::console::ConsoleSubscriber::GetStream()` | `afsim-2_9/swdev/src/core/wsf/source/dis/WsfDisInterface.cpp:144` | `// Subscribe to callbacks; these are applicable for both threaded and non-threaded` | 事件订阅机制，用于让观察者接收运行时事件。 |
| `AddExtension` | `WsfExtensionList::AddExtension()` | `afsim-2_9/swdev/src/core/wsf/source/WsfApplication.cpp:176` | `mExtensionListPtr->AddExtension(aName, std::move(aExtensionPtr));` | 扩展列表机制，用于维护扩展对象和扩展间依赖顺序。 |
| `ComponentFactory` | `WsfCommandChain::RegisterComponentFactory()`, `WsfComponentFactory::PreInitialize()`, `WsfComponentFactory::PreInput()` | `afsim-2_9/swdev/src/core/wsf_cyber/source/WsfCyberConstraintTypes.cpp:27` | `class ComponentFactory : public WsfComponentFactory<WsfPlatform>` | 组件工厂机制，用于根据输入类型创建运行时组件。 |
| `AddFactory` | `AddFactory` | `afsim-2_9/swdev/src/core/wsf/source/comm/WsfCommMediumFactory.hpp:108` | `void AddFactory(std::unique_ptr<Factory<MEDIUM_TYPE>> aFactory)` | 工厂注册机制，用于把类型工厂加入 FactoryManager。 |
| `RegisterComponent` | `WsfCommandChain::RegisterComponentFactory()`, `WsfExclusionSensorComponent::RegisterComponentFactory()`, `WsfGeoPoint::RegisterComponentFactory()` | `afsim-2_9/swdev/src/wsf_plugins/wsf_oms_uci/source/WsfUCI_Component.cpp:100` | `interfacePtr->RegisterComponent(*this);` | 组件注册机制，用于声明可创建或可识别的组件类型。 |
| `RegisterScriptClasses` | `WsfL16::Messages::Factory::RegisterScriptClasses()` | `afsim-2_9/swdev/src/core/wsf_l16/source/MessagesFactory.cpp:73` | `RegisterScriptClasses(*aScriptTypes);` | 脚本类注册机制，用于把 C++ 类型暴露给脚本系统。 |

## 2. 机制详情

### `RegisterExtension`

- 关键接口/基类：`WsfApplication::RegisterExtension()`, `wsf::comm::router::medium::WsfScenario::RegisterExtension()`, `wsf::comm::WsfSimulation::RegisterExtension()`
- 注册位置：`afsim-2_9/swdev/src/core/sensor_plot_lib/source/WsfSensorPlot.cpp:75`
- 使用示例：`aScenario.RegisterExtension(GetExtensionName(), ut::make_unique<WsfSensorPlotExtension>(this));`
- 用途说明：应用或场景扩展注册机制，用于把外部能力挂接到 WsfApplication/WsfScenario 生命周期。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 168 条记录。

### `AddMessage`

- 关键接口/基类：`wsf::console::SubscriberBase::AddMessageP()`, `WsfL16::Messages::Factory::AddMessage()`, `rv::PartMap::AddMessage()`
- 注册位置：`afsim-2_9/swdev/src/core/wsf_l16/source/MessagesFactory.cpp:33`
- 使用示例：`AddMessage(new J2_0::Initial());`
- 用途说明：消息工厂注册机制，用于把消息类型加入消息表。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 165 条记录。

### `EventPipe`

- 关键接口/基类：`WsfEventPipeExtension::AddCallback()`, `WsfEventPipeExtension::AddSchema()`, `WsfEventPipeExtension::Find()`
- 注册位置：`afsim-2_9/swdev/src/core/wsf/source/xio_sim/WsfXIO_EventPipe.cpp:30`
- 使用示例：`void wsf::xio::EventPipe::RegisterEvents(WsfEventPipeExtension& aEventPipeExtension)`
- 用途说明：事件管道订阅/记录机制，用于把仿真事件输出给 Warlock/Mystic 等工具。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 164 条记录。

### `AddComponent`

- 关键接口/基类：`WsfComponentList::AddComponentP()`, `wsf::comm::router::Router::AddComponent()`, `ToggleEffect::AddComponent()`
- 注册位置：`afsim-2_9/swdev/src/core/sensor_plot_lib/source/MapPlotVariables.cpp:275`
- 使用示例：`// after ownership has been transferred to the platform (via AddComponent)`
- 用途说明：平台组件挂接机制，用于给 WsfPlatform 增加传感器、武器、通信等运行时能力。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 107 条记录。

### `Subscribe`

- 关键接口/基类：`wsf::console::ConsoleSubscriber::ConsoleSubscriber()`, `wsf::console::ConsoleSubscriber::FlushStream()`, `wsf::console::ConsoleSubscriber::GetStream()`
- 注册位置：`afsim-2_9/swdev/src/core/wsf/source/dis/WsfDisInterface.cpp:144`
- 使用示例：`// Subscribe to callbacks; these are applicable for both threaded and non-threaded`
- 用途说明：事件订阅机制，用于让观察者接收运行时事件。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 58 条记录。

### `AddExtension`

- 关键接口/基类：`WsfExtensionList::AddExtension()`
- 注册位置：`afsim-2_9/swdev/src/core/wsf/source/WsfApplication.cpp:176`
- 使用示例：`mExtensionListPtr->AddExtension(aName, std::move(aExtensionPtr));`
- 用途说明：扩展列表机制，用于维护扩展对象和扩展间依赖顺序。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 7 条记录。

### `ComponentFactory`

- 关键接口/基类：`WsfCommandChain::RegisterComponentFactory()`, `WsfComponentFactory::PreInitialize()`, `WsfComponentFactory::PreInput()`
- 注册位置：`afsim-2_9/swdev/src/core/wsf_cyber/source/WsfCyberConstraintTypes.cpp:27`
- 使用示例：`class ComponentFactory : public WsfComponentFactory<WsfPlatform>`
- 用途说明：组件工厂机制，用于根据输入类型创建运行时组件。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 5 条记录。

### `AddFactory`

- 关键接口/基类：`AddFactory`
- 注册位置：`afsim-2_9/swdev/src/core/wsf/source/comm/WsfCommMediumFactory.hpp:108`
- 使用示例：`void AddFactory(std::unique_ptr<Factory<MEDIUM_TYPE>> aFactory)`
- 用途说明：工厂注册机制，用于把类型工厂加入 FactoryManager。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 3 条记录。

### `RegisterComponent`

- 关键接口/基类：`WsfCommandChain::RegisterComponentFactory()`, `WsfExclusionSensorComponent::RegisterComponentFactory()`, `WsfGeoPoint::RegisterComponentFactory()`
- 注册位置：`afsim-2_9/swdev/src/wsf_plugins/wsf_oms_uci/source/WsfUCI_Component.cpp:100`
- 使用示例：`interfacePtr->RegisterComponent(*this);`
- 用途说明：组件注册机制，用于声明可创建或可识别的组件类型。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 3 条记录。

### `RegisterScriptClasses`

- 关键接口/基类：`WsfL16::Messages::Factory::RegisterScriptClasses()`
- 注册位置：`afsim-2_9/swdev/src/core/wsf_l16/source/MessagesFactory.cpp:73`
- 使用示例：`RegisterScriptClasses(*aScriptTypes);`
- 用途说明：脚本类注册机制，用于把 C++ 类型暴露给脚本系统。
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 3 条记录。

