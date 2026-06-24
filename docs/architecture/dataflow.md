# AFSIM 数据流分析

> 生成日期：2026-06-22
> 阶段：Phase 6

## 关键数据对象

| 数据对象                     | 依赖引用数 | 生产者（写入方）                                                               | 消费者（读取方）                                                                                                             | 关联生命周期       |
| ------------------------ | ----- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------ |
| Clone                    | 1042  | N/A                                                                    | WsfGeoPoint::GetLat, WsfGeoPoint::GetLocationLLA                                                                     | model_update |
| ProcessInput             | 621   | N/A                                                                    | WsfMessageTable::DefaultProp, WsfCorrelationStrategyTypes::ProcessInput                                              | model_update |
| WsfStringId              | 595   | WsfXIO_RawTrackPkt, WsfStandardInherentContrast                        | XWsfSeaTraffic::ProcessDepartureTraffic, XWsfSeaTraffic::ProcessLocalTraffic                                         | model_update |
| Initialize               | 553   | N/A                                                                    | WsfMessageTable::DefaultProp, WsfEventStepSimulation::~WsfEventStepSimulation                                        | output       |
| QString                  | 502   | ModelImport::detail::Json::ItemData, rv::RvStatistics::EventTableModel | N/A                                                                                                                  | model_update |
| BehaviorTreeNodeChildren | 462   | N/A                                                                    | wsf::comm::router::event::MessageTransmitEnded::GetSimulation, wsf::comm::router::event::MessageFailedRouting::Print | model_update |
| BehaviorTreeNodeExec     | 462   | N/A                                                                    | wsf::comm::router::event::MessageTransmitEnded::GetSimulation, wsf::comm::router::event::MessageFailedRouting::Print | model_update |
| CommAddedToLocal         | 462   | N/A                                                                    | wsf::comm::router::event::MessageTransmitEnded::GetSimulation, wsf::comm::router::event::MessageFailedRouting::Print | model_update |
| CommAddedToManager       | 462   | N/A                                                                    | wsf::comm::router::event::MessageTransmitEnded::GetSimulation, wsf::comm::router::event::MessageFailedRouting::Print | model_update |
| CommBroken               | 462   | N/A                                                                    | wsf::comm::router::event::MessageTransmitEnded::GetSimulation, wsf::comm::router::event::MessageFailedRouting::Print | model_update |

## 数据流路径

### 数据流 1: 仿真场景数据流
```mermaid
flowchart LR
    A[场景文件] -->|解析| B[Scenario Parser]
    B -->|创建| C[Scenario Objects]
    C -->|注册| D[Platform Registry]
    D -->|初始化| E[Simulation Engine]
    E -->|时间步进| F[Platform Update Loop]
    F -->|状态变更| G[Event Publisher]
    G -->|分发| H[Event Handlers]
    H -->|响应| F
    F -->|输出| I[Results Writer]
```

**描述**：场景文件 → 解析器(WsfParser/WsfParseGrammar) → 对象工厂(WsfComponentFactory) → 平台注册 → 仿真引擎(WsfSimulation) → 主循环更新 → 事件发布 → 事件处理 → 结果输出

### 数据流 2: 平台轨迹数据流
```mermaid
flowchart LR
    A[Mover Input] -->|动力学| B[Mover Model]
    B -->|位置/姿态| C[Platform State]
    C -->|发布| D[Track Update Event]
    D -->|融合| E[Track Fusion]
    E -->|输出| F[Track Output]
    F -->|渲染| G[Visualization]
```

### 数据流 3: 传感器检测数据流
```mermaid
flowchart LR
    A[Environment] -->|传播| B[Sensor Model]
    B -->|检测| C[Detection Event]
    C -->|处理| D[Signal Processor]
    D -->|跟踪| E[Track Manager]
    E -->|更新| F[Track State]
```

### 数据流 4: 通信消息数据流
```mermaid
flowchart LR
    A[Message Source] -->|编码| B[Message Encoder]
    B -->|发送| C[Comm Network]
    C -->|接收| D[Message Decoder]
    D -->|解析| E[Message Handler]
    E -->|触发| F[Behavior Response]
```

### 数据流 5: 配置参数流
```mermaid
flowchart LR
    A[XML/JSON Config] -->|加载| B[Config Parser]
    B -->|验证| C[Schema Validator]
    C -->|实例化| D[Component Factory]
    D -->|参数注入| E[Runtime Object]
    E -->|运行时修改| F[Dynamic Config]
```

