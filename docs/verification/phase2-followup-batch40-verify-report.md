# Phase 2 batch40 增量验证报告

> **验证日期**：2026-07-13
> **验证对象**：wsf_coverage 覆盖分析与 wsf_cyber 网络攻防模型
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 2 个目录已标记为 `done_batch40`。 |
| file-index 覆盖 | 通过 | 166 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 10 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `wsf_plugins/wsf_coverage/source` | 81 | `Register_wsf_coverage`、`wsf::coverage::ScenarioExtension`、`wsf::coverage::SimulationExtension`、`wsf::coverage::Coverage`、`wsf::coverage::Measure` | 通过 |
| `core/wsf_cyber/source` | 85 | `Register_wsf_cyber`、`wsf::cyber::ScenarioExtension`、`wsf::cyber::SimulationExtension`、`wsf::cyber::EngagementManager`、`wsf::cyber::Event::Execute` | 通过 |

## CodeGraph 与源码交叉验证

本批先使用 CodeGraph 批量探索，再用目录内源码扫描确认符号归属。对 `Plugin`、`Event`、`Network`、`Coverage` 等通用名称，最终以 `analysis_unit` 路径前缀和源码行号为准。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `wsf_plugins/wsf_coverage/source` | 覆盖分析入口链：`WsfPluginSetup` -> `Register_wsf_coverage` -> `ScenarioExtension::AddedToScenario` 注册 grid/coverage/measure/output 类型 -> `SimulationExtension::ProcessInput(grid/coverage)` -> `SimulationExtension::Initialize` -> `Coverage::Initialize`/`Grid::Initialize` -> `Coverage::PendingStart` -> `SensorCoverage::OnSensorDetectionChanged` -> `Coverage::AddIntervalStart/EndToData` -> `Measure::CollectionCompleting` -> raw/MOE CSV/overlay/grid data 输出。 |
| `core/wsf_cyber/source` | Cyber 业务入口链：`Register_wsf_cyber` -> `ScenarioExtension::AddedToScenario` 注册 attack/effect/protect/trigger/constraint 类型和组件 -> `SimulationExtension::AddedToSimulation/Initialize` 注册 observer/event output/script observer/event_pipe -> trigger 或脚本 `CyberAttack/CyberScan` -> `EngagementManager` -> `EventManager/Event::Execute` 延迟阶段 -> `CyberAttackEffect`/具体 effect -> `CyberResult/EventPipe` 输出。 |

## 已知风险

本批包含 coverage 和 cyber 两类高价值仿真业务扩展。Phase 2 已确认入口、边界和代表性符号；coverage 的 structured grid/overlay/MOE 输出边界，以及 cyber 的延迟事件、MITM/track manager/detonate effect 和平台删除边界，需在后续函数级分析中验证。
