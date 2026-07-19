# AFSIM 业务逻辑分析承接文档

> **状态**：已完成
> **日期**：2026-07-16
> **分析范围**：Phase 1-6 已索引范围内的 AFSIM 仿真相关源码
> **上游产物**：Phase 1-6 索引与 Phase 7 架构文档
> **用途**：为下一步业务逻辑分析提供源码入口、候选流程、规则点和证据链

## 0. 文档说明

**承接目标**：把可继续深入的业务域、端到端流程、规则候选、输入输出和源码证据组织为可执行入口。

**不做的事**：不把候选业务含义写成最终业务规则；不脱离源码证据解释业务背景。

**证据级别**：

| evidence_level | 含义 | 使用条件 |
|----------------|------|----------|
| direct | 直接证据 | 源码函数、类、配置解析或事件处理直接体现该业务含义 |
| cross_checked | 交叉证据 | 至少两类证据互相支持，如生命周期和函数索引 |
| inferred | 推断证据 | 主要由命名、目录、弱调用关系推断，需要后续确认 |
| unknown | 未确认 | 当前产物不足以判断，需要人工或源码深挖 |

## 1. 业务域候选总览

| # | 业务域候选 | 中文说明 | 关联系统/模块 | 主要输入 | 主要输出 | 证据入口 | evidence_level | 下一步问题 |
|---|------------|----------|----------------|----------|----------|----------|----------------|------------|
| 1 | 仿真生命周期执行 | 从入口到关闭的阶段化运行流程 | `core/wsf`、运行入口 | 命令行、场景文件 | 运行状态、结果输出 | `docs/architecture/lifecycle.md`、`FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | cross_checked | 阶段切换条件和状态不变量是什么 |
| 2 | 场景配置与对象创建 | 配置解析后创建平台、组件和模型对象 | `core/wsf` | 场景文本、脚本配置 | `WsfScenario`、`WsfPlatform` | `function-index.jsonl`、`docs/architecture/dataflow.md` | cross_checked | 配置字段到对象属性的映射如何确认 |
| 3 | 平台、传感器与模型更新 | 平台和组件在循环中更新状态 | `core/wsf`、传感器模块 | 运行时状态、时间步 | 航迹、特征、平台状态 | `docs/architecture/dataflow.md`、`WsfAdvancedBehaviorTree::Initialize#43a4d4a5e4` | cross_checked | 哪些更新函数承载核心业务公式 |
| 4 | 事件调度与观察者 | 事件对象被调度并分发给订阅者 | `core/wsf` 事件系统 | 事件队列 | 状态变化、输出副作用 | `docs/architecture/lifecycle.md`、`FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | cross_checked | 事件优先级和过滤规则在哪里 |
| 5 | 通信与消息交换 | 消息对象在通信链路中发送、接收、处理 | `core/wsf_l16`、通信模块 | 消息、协议字段 | 接收状态、输出记录 | `dependency-index.jsonl`、`function-index.jsonl` | inferred | 协议字段业务含义需要逐条确认 |
| 6 | 扩展注册与插件接入 | 通过工厂、注册表、脚本入口接入能力 | 插件和扩展模块 | 注册调用、配置项 | 新对象类型、策略行为 | `docs/architecture/extension-points.md`、`FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | cross_checked | 注册顺序是否影响行为 |

## 2. 端到端业务流程入口

| # | 流程/用例候选 | 触发入口 | 配置/事件输入 | 关键处理链 | 主要状态对象 | 输出/副作用 | 源码证据 | evidence_level | 下一步分析问题 |
|---|---------------|----------|----------------|------------|--------------|------------|----------|----------------|----------------|
| 1 | 场景加载到对象创建 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | 场景输入文件 | 解析入口到 `WsfScenario` 再到平台和组件 | `WsfScenario`、`WsfPlatform` | 运行对象集合 | `lifecycle.md`、`function-index.jsonl` | cross_checked | 逐个配置字段的目标对象属性是什么 |
| 2 | 仿真循环到模型更新 | `WsfAdvancedBehaviorTree::Initialize#43a4d4a5e4` | 时间步、运行时状态 | 循环入口到模型更新函数 | Platform、Track、Signature | 状态变化、结果记录 | `dataflow.md`、`function-index.jsonl` | cross_checked | 模型更新顺序如何影响结果 |
| 3 | 事件触发到输出 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | Event 队列 | 事件执行到订阅者和输出模块 | Event、Platform | 输出文件、可视化更新 | `lifecycle.md`、`dependency-index.jsonl` | cross_checked | 哪些事件改变核心状态 |
| 4 | 扩展注册到能力接入 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | 插件、工厂、脚本注册 | 注册入口到工厂表再到对象创建 | 工厂表、注册表 | 新组件或新消息类型 | `extension-points.md`、`dependency-index.jsonl` | cross_checked | 注册冲突和加载顺序如何处理 |

## 3. 业务规则/决策点候选

| # | 规则/决策点候选 | 条件/阈值/分支 | 所在函数/类 | 影响对象/输出 | 证据 | evidence_level | 待确认问题 |
|---|-----------------|----------------|-------------|----------------|------|----------------|------------|
| 1 | 场景字段驱动对象类型选择 | 配置字段和工厂匹配条件 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` 及工厂注册入口 | 平台、组件、模型对象 | `function-index.jsonl`、`extension-points.md` | inferred | 配置关键字和工厂键的精确映射是什么 |
| 2 | 时间步推进和模型更新分发 | 时间、状态、启停条件 | `WsfAdvancedBehaviorTree::Initialize#43a4d4a5e4` | 平台状态、航迹、输出 | `lifecycle.md`、`dataflow.md` | inferred | 更新函数的排序和跳过条件是什么 |
| 3 | 事件分发和订阅过滤 | 事件类型、订阅条件 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | 订阅者状态、输出副作用 | `dependency-index.jsonl` registration 关系 | inferred | 事件优先级和取消机制是否存在 |
| 4 | 消息类型选择和协议处理 | 消息类型、协议字段 | `core/wsf_l16` 相关方法 | Message、通信状态 | `dependency-index.jsonl`、`function-index.jsonl` | inferred | 协议字段业务含义如何验证 |

## 4. 数据与配置映射

| # | 配置/输入/事件对象 | 来源 | 解析/接收函数 | 运行时状态对象 | 消费者 | 输出影响 | 证据位置 | evidence_level |
|---|-------------------|------|----------------|----------------|--------|----------|----------|----------------|
| 1 | 场景文件 | 文件输入 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | `WsfScenario` | 对象创建链 | 运行对象集合 | `docs/architecture/lifecycle.md` | cross_checked |
| 2 | 平台定义 | 场景配置 | `CompleteLoad` 候选 | `WsfPlatform` | 模型更新和事件 | 平台状态 | `docs/architecture/dataflow.md` | inferred |
| 3 | Event 事件 | 调度器 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | Event 队列 | 订阅者 | 状态变化、输出 | `docs/architecture/lifecycle.md` | cross_checked |
| 4 | Message 消息 | 通信模块 | 发送和接收方法候选 | Message 队列 | 接收方 | 通信副作用 | `workspace/source-index/dependency-index.jsonl` | inferred |
| 5 | Signature 特征 | 平台和传感器配置 | 传感器更新候选 | Signature 状态 | 传感器模型 | 探测和输出 | `docs/architecture/dataflow.md` | inferred |

## 5. 扩展点与业务能力接入

| # | 扩展机制 | 业务影响候选 | 注册/发现入口 | 调用/分发路径 | 受影响模块 | 证据位置 | evidence_level | 待确认问题 |
|---|----------|--------------|----------------|--------------|------------|----------|----------------|------------|
| 1 | 工厂注册 | 新对象类型或消息类型接入 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | 工厂表到对象创建 | `core/wsf`、通信模块 | `extension-points.md` | cross_checked | 工厂键命名和冲突策略是什么 |
| 2 | 事件订阅 | 新事件消费者接入 | `Subscribe` 候选 | EventPipe 到订阅者 | 事件系统、输出模块 | `dependency-index.jsonl` | inferred | 订阅者是否可改变核心状态 |
| 3 | 脚本类注册 | 脚本可控制对象和行为 | `RegisterScriptClasses` 候选 | 脚本入口到 C++ 类 | 脚本相关模块 | `extension-points.md` | inferred | 脚本权限和生命周期边界是什么 |
| 4 | 插件加载 | 外部模块接入运行时 | `AddExtension` 候选 | 插件注册到能力表 | wizard、warlock、mystic | `dependency-index.jsonl` | inferred | 插件加载顺序是否影响业务结果 |

## 6. 下一步分析优先级

| 优先级 | 主题 | 推荐原因 | 已有证据 | 缺口 | 建议读取源码入口 |
|--------|------|----------|----------|------|------------------|
| P1 | 场景配置到对象创建 | 影响所有仿真对象起始状态 | 生命周期、数据流、函数索引 | 配置字段精确映射 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26`、`core/wsf` 场景解析源文件 |
| P2 | 仿真循环和模型更新 | 直接影响运行结果 | 生命周期、方法索引 | 更新顺序和状态不变量 | `WsfAdvancedBehaviorTree::Initialize#43a4d4a5e4` |
| P3 | 事件调度与订阅 | 影响异步状态变化和输出 | 事件链路、依赖索引 | 优先级和过滤条件 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` |
| P4 | 通信和消息处理 | 影响协议级业务行为 | 依赖索引、模块索引 | 协议字段语义 | `core/wsf_l16` 相关函数 |
| P5 | 扩展注册和插件接入 | 影响可插拔能力边界 | 扩展点文档、registration 依赖 | 加载顺序和冲突处理 | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` |

## 7. 边界外或暂不纳入项

| # | 项目/目录/功能 | 排除原因 | 是否可能影响业务逻辑 | 后续条件 |
|---|----------------|----------|----------------------|----------|
| 1 | training | 训练材料，不作为核心源码证据 | 低 | 用户要求纳入培训流程时再分析 |
| 2 | demos | 示例场景，不作为框架业务规则证据 | 中 | 需要验证具体场景时再纳入 |
| 3 | documentation | 文档说明，不替代源码证据 | 中 | 作为术语解释可辅助引用 |
| 4 | test | 测试代码，不作为核心业务逻辑入口 | 中 | 需要验证行为预期时作为辅助证据 |
| 5 | `vx.json` | 用户明确排除 | 低 | 不纳入本项目分析 |

## 8. 未知项和人工确认问题

| # | 问题描述 | 影响 | 当前证据 | 建议人工确认的问题 | 建议确认对象/文件 | 严重度 |
|---|----------|------|----------|----------------------|--------------------|--------|
| 1 | 配置字段到运行时对象属性的完整映射未展开 | 影响业务规则准确抽取 | 生命周期和数据流已定位入口 | 哪些字段直接改变平台、传感器、通信行为 | `core/wsf` 场景解析源文件 | 高 |
| 2 | 模型更新顺序和跳过条件未逐条确认 | 影响结果解释和规则抽取 | Phase6 给出阶段链路 | 更新顺序是否固定，是否受配置控制 | `function-index.jsonl` 中 model_update 方法 | 高 |
| 3 | 事件优先级、取消和过滤机制未确认 | 影响事件业务规则 | 事件执行和 registration 依赖已定位 | 事件队列如何排序和过滤 | 事件系统源文件 | 中 |
| 4 | 插件和工厂注册冲突策略未确认 | 影响扩展能力接入 | `extension-points.md` 和依赖索引 | 同名注册如何处理，加载顺序是否稳定 | 扩展注册源文件 | 中 |
