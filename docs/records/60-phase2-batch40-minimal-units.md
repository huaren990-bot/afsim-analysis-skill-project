# Phase 2 完成记录：batch40 wsf_coverage 覆盖分析与 wsf_cyber 网络攻防模型

> **完成日期**：2026-07-13
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `wsf_plugins/wsf_coverage/source` | 81 | `Register_wsf_coverage`、`wsf::coverage::ScenarioExtension`、`wsf::coverage::SimulationExtension`、`wsf::coverage::Coverage`、`wsf::coverage::Measure` | WSF coverage 插件核心，提供 coverage/grid/measure/output 类型体系，计算传感器或资产访问区间、覆盖时间、revisit/gap/access 指标并输出文本/CSV/overlay/raw data。 |
| `core/wsf_cyber/source` | 85 | `Register_wsf_cyber`、`wsf::cyber::ScenarioExtension`、`wsf::cyber::SimulationExtension`、`wsf::cyber::EngagementManager`、`wsf::cyber::Event::Execute` | WSF cyber 核心模型，提供 cyber attack/scan/protect/constraint/effect/trigger/engagement/event pipe/script extension，并把结果写入 event output 与 observer。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先执行批量 CodeGraph 查询；对通用 `Plugin/Event/Network` 等跨目录噪声，按完整路径回落到目录内源码扫描确认。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/function/registration/ProcessInput/输出入口，排除 `vx.json` 和导出宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览、批次记录和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `wsf_plugins/wsf_coverage/source` | 覆盖分析入口链：`WsfPluginSetup` -> `Register_wsf_coverage` -> `ScenarioExtension::AddedToScenario` 注册 grid/coverage/measure/output 类型 -> `SimulationExtension::ProcessInput(grid/coverage)` -> `SimulationExtension::Initialize` -> `Coverage::Initialize`/`Grid::Initialize` -> `Coverage::PendingStart` -> `SensorCoverage::OnSensorDetectionChanged` -> `Coverage::AddIntervalStart/EndToData` -> `Measure::CollectionCompleting` -> raw/MOE CSV/overlay/grid data 输出。 |
| `core/wsf_cyber/source` | Cyber 业务入口链：`Register_wsf_cyber` -> `ScenarioExtension::AddedToScenario` 注册 attack/effect/protect/trigger/constraint 类型和组件 -> `SimulationExtension::AddedToSimulation/Initialize` 注册 observer/event output/script observer/event_pipe -> trigger 或脚本 `CyberAttack/CyberScan` -> `EngagementManager` -> `EventManager/Event::Execute` 延迟阶段 -> `CyberAttackEffect`/具体 effect -> `CyberResult/EventPipe` 输出。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch40-verify-report.md` |

## 已知问题

1. CodeGraph 对通用名称存在跨目录噪声，本批正式索引只采纳完整路径落在本批目录内的源码证据。
2. 本批只修 Phase 2 粗索引；函数参数、重载、调用链和边界分支留给 Phase 3/4 或业务逻辑深挖。
3. `vx.json` 只作为存在事实，不进入本批 source/header 文件索引。
4. coverage overlay 只适用于 structured grid；配置 overlay 但无 MOE、非结构网格或输出路径冲突需要后续函数级确认。
5. cyber MITM、track manager、detonate 等 effect 会动态修改通信层、track manager 或武器状态；延迟事件、平台删除和重复攻击的边界需要业务级验证。

## 下游就绪

本批新增 2 个最小目录单元、166 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
