# Phase 2 完成记录：batch44 core util、post processor 与小型 WSF 插件

> **完成日期**：2026-07-15
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/core/wsf_util` | 21 | `UtBuffer`、`UtCsv::Parser`、`UtPackSerializer`、`UtPackReflector`、`UtmlParser` | WSF 底层工具库，提供 byte buffer、CSV、UTML、tar、SHA 与 UtPack 反射/schema/二进制消息序列化能力。 |
| `afsim-2_9/swdev/src/post_processor/lib` | 20 | `Configuration`、`Configuration::Execute`、`Report`、`DetectionReport`、`DSV_Output` | 仿真后处理报表库，读取命令行、配置文件和输出 CSV，生成通信、探测、交战、eclipse、轨迹与 DSV 报表。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8` | 14 | `Register_wsf_argo8`、`WsfARGO8_Extension::AddedToScenario`、`WsfARGO8_Mover`、`Argo8Missile`、`standard_Argo8Model` | ARGO8 导弹/飞行模型插件，把外部或标准 ARGO8 模型包装进 WSF mover 生命周期。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_multiresolution` | 17 | `WsfMultiresolutionMultirunTable`、`WsfMultiresolutionTypesRegistration::AddedToScenario`、`WsfMultiresolutionPlatformComponent`、`WsfMultiresolutionWrapperMetaModel`、`wsf::multiresolution::ComponentName` | 多分辨率组件插件，为 mover、sensor、processor、fuel、comm 和 signature 等组件按 fidelity 选择具体模型实现。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先按批次执行 CodeGraph 探索；对大范围噪声结果，按目录路径回落到源码扫描确认。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描注册入口、class/function、ProcessInput/Initialize/Update 和输出链，排除 `vx.json` 与导出宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览、批次记录和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `afsim-2_9/swdev/src/core/wsf_util` | `UtPackSchema::Read -> Resolve -> UtPackSerializer::Initialize/RegisterMessage` 串起 schema 装载、类型注册和消息序列化；`UtCsv::Parser::ReadRow` 与 `UtmlParser` 可承接文本输入解析分析。 |
| `afsim-2_9/swdev/src/post_processor/lib` | `Configuration::Execute -> ProcessConfigurationFile -> CreateReport -> InitReport -> Report::PrintReport` 是后处理业务主链；派生 report 的 `ProcessHeaders/ProcessData/PrintReport` 是报表字段语义入口。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8` | `Register_wsf_argo8 -> WsfARGO8_Extension::AddedToScenario -> WsfARGO8_Mover` 建立 mover 类型；运行时沿 `WsfARGO8_Mover::Update -> Argo8Missile::Update -> Argo8Model::Update` 进入飞行/制导逻辑。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_multiresolution` | `Register_wsf_multiresolution -> WsfMultiresolutionTypesRegistration::AddedToScenario -> AddMultiresolutionType` 注册 wrapper；运行时 `PreInitialize -> GetFidelity -> ModelIndexForFidelity -> Clone` 选择 fidelity 对应模型。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch44-verify-report.md` |

## 已知问题

| 单元 | 风险与待确认项 |
|------|------|
| `afsim-2_9/swdev/src/core/wsf_util` | UtPack optional/union/conversion 分支复杂；`UtBuffer` 涉及手工内存、字节序和边界检查；schema 输入异常路径需在业务逻辑阶段复核。 |
| `afsim-2_9/swdev/src/post_processor/lib` | 命令行参数存在 `++argIndex` 缺参风险；未知配置多为 warning；`TrajectoryReport` 存在 TODO/空实现，字段 schema 对字符串较敏感。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8` | `missile_type`、`guidance_update_interval` 与外部动态库路径约束严格；目标、track、sensor 缺失分支会影响交战结果。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_multiresolution` | 模板封装较深；fidelity 区间重叠、默认值、loop-after-table-end 与 component name specialization 需要业务阶段复核。 |

## 下游就绪

本批新增 4 个最小目录单元、72 个 source/header 和 20 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
