# Phase 2 batch33 增量验证报告

> **验证日期**：2026-07-11
> **验证对象**：wsf_mtt、air combat、CommVis、artificer、SPLAT 与 sensor plot lib
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 6 个目录已标记为 `done_batch33`。 |
| file-index 覆盖 | 通过 | 208 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 30 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤，未写入不属于本批目录的符号。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `core/wsf_mtt/source` | 30 | `MTT`、`WsfMTT_Interface`、`WsfMTT_Correlation`、`WsfMTT_Fusion`、`MTT_ActiveTrack` | 通过 |
| `wsf_plugins/wsf_air_combat/source` | 31 | `WsfSA_Processor`、`WsfSA_Perceive`、`WsfSA_Assess`、`WsfSA_Predict`、`WsfAirCombatTypeManager` | 通过 |
| `wizard/plugins/CommVis/source` | 32 | `WizCommVis::Plugin`、`WizCommVis::CommVisDialog`、`WizCommVis::CommVisEditDialog`、`WizCommVis::CommVisAddCommDialog`、`WizCommVis::CommVisRouterNodeDialog` | 通过 |
| `tools/artificer/source` | 34 | `artificer::V1Parser`、`artificer::V1PrototypeSummarizer`、`artificer::RunData`、`artificer::SimulationData`、`artificer::TextTable` | 通过 |
| `wizard/plugins/SPLAT/source` | 40 | `SPLAT::Plugin`、`SPLAT::SensorAnalysisDialog`、`SPLAT::ProxyInterface`、`SPLAT::PlotOptionsDialog`、`SPLAT::PlotOptionsWidget` | 通过 |
| `core/sensor_plot_lib/source` | 41 | `WsfSensorPlotExtension`、`Function`、`MapPlotFunction`、`MapPlotVariables`、`Sensor` | 通过 |

## CodeGraph 与源码交叉验证

CodeGraph 命中 `WkCommVis::CommVisEvent` 与 `wkf::CommVisPacketGraphicsItem`，确认 CommVis 公共事件/packet 图元链；`WsfEventManager` 等核心 WSF 命中为跨目录噪声，不归入本批符号。

本批最终索引以目录边界内的源码声明为准；跨目录命中仅记录为噪声或后续追踪线索，不直接写入本批 symbol-index。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `core/wsf_mtt/source` | `MTT_ActiveTrack`、`MTT_CandidateTrack`、`MTT_EmbryonicTrack`、`MTT_NonlocalTrack`、`MTT_Track` |
| `wsf_plugins/wsf_air_combat/source` | `wsf::six_dof::SA_TrackManagerData`、`wsf::AirCombat::EventPipe`、`WsfAirCombatTypeManager`、`WsfSA_GroupManager`、`TrackDelayData` |
| `wizard/plugins/CommVis/source` | `WizCommVis::CommVisViewLinksDialog`、`WizCommVis::CommVisAddRouterDialog`、`WizCommVis::Plugin`、`WizCommVis::CommVisRouterNodeDialog`、`WizCommVis::CommVisAddCommDialog` |
| `tools/artificer/source` | `artificer::RunData`、`artificer::SimulationData`、`artificer::TextTable`、`artificer::AfperfParserInterface`、`artificer::AfperfSummarizerInterface` |
| `wizard/plugins/SPLAT/source` | `SPLAT::PlatformOptionsWidget`、`SPLAT::Plugin`、`SPLAT::TargetPlatformTypeDialog`、`SPLAT::AnalysisMapOptionsDialog`、`SPLAT::HorizontalCoverageOptionsDialog` |
| `core/sensor_plot_lib/source` | `ClutterTableFunction`、`FlightPathAnalysisFunction`、`RadarLookupTableFunction`、`AntennaPlotFunction`、`ContourFilter2D` |

## 已知风险

本批包含多个 UI/工具层目录，Phase 2 只确认入口、边界和代表性符号；业务规则解释需要在下一步沿命令处理、事件生产、extension 注册和结果数据生产端继续追踪。子 agent 已补充的具体风险点已折叠进职责/深挖点，后续业务逻辑分析应按这些入口继续验证。
