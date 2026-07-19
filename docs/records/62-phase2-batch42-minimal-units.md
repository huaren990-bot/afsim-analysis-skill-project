# Phase 2 完成记录：batch42 vespatk 可视化工具包与 wsf_l16 Link-16 扩展

> **完成日期**：2026-07-14
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/tools/vespatk/source` | 135 | `vespa::VaEnvironment`, `vespa::VaScenario`, `vespa::VaViewer`, `vespa::VaFactory::CreateAttachment`, `vespa::VaEventManager` | vespatk 可视化工具包核心：管理 viewer/camera、场景实体、attachment/overlay、模型数据库、选择交互和时间事件调度。 |
| `afsim-2_9/swdev/src/core/wsf_l16/source` | 105 | `Register_wsf_l16`, `WsfL16::InterfaceSetup::ProcessInput`, `WsfL16::Interface`, `WsfL16::Messages::Factory`, `WsfL16::ComputerProcessor` | wsf_l16 Link-16 扩展：注册 Link-16 feature/extension，解析 link16_interface，处理 DIS Signal PDU、J-series 消息、脚本访问器和 Link16 computer parts。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先执行批量 CodeGraph 查询；对通用符号噪声，按完整路径回落到目录内源码扫描确认。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/function/registration/ProcessInput/输出入口，排除 `vx.json` 和导出宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览、批次记录和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `afsim-2_9/swdev/src/tools/vespatk/source` | 可视化链：`VaEnvironment::Initialize` -> scenarios/viewers/model database/event managers -> `VaScenario::Initialize/Load/UpdateFrame` -> `VaFactory::CreateEntity/CreateAttachment/CreateOverlay` -> `VaViewer` 交互与 overlay 绘制。 |
| `afsim-2_9/swdev/src/core/wsf_l16/source` | 注册/收发链：`Register_wsf_l16` -> `ApplicationExtension::AddedToApplication` -> `Messages::Factory::Initialize`/`ComputerProcessor::RegisterType` -> `WsfL16_Extension::SimulationCreated` -> `Interface::Initialize` -> `Factory::ReadMessage`/`Interface::SendJMessage`。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch42-verify-report.md` |

## 已知问题

| 单元 | 风险与待确认项 |
|------|------|
| `afsim-2_9/swdev/src/tools/vespatk/source` | 工厂扩展依赖字符串 if/else 与 `UserCreate*` 虚扩展点；事件管理使用裸指针和手动 delete，重入与生命周期需后续验证。 |
| `afsim-2_9/swdev/src/core/wsf_l16/source` | 静态全局消息/accessor 状态需要 `ResetState` 防止多场景串状态；DIS/JTIDS/WSF 输出路径交织，J-message 位级解析对 header/字节序/长度敏感。 |

## 下游就绪

本批新增 2 个最小目录单元、240 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
