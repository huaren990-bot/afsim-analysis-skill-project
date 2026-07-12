# Phase 2 batch28 增量验证报告

> **验证日期**：2026-07-11
> **验证对象**：SixDOF、tracks、prompt、route、scenario analyzer 与 multiresolution
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 6 个目录已标记为 `done_batch28`。 |
| file-index 覆盖 | 通过 | 84 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 30 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤，未写入不属于本批目录的符号。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `warlock/plugins/SixDOF_Tuner/source` | 14 | `wkf::WkSixDOF_Tuner::CommandDialog`、`WkSixDOF_Tuner::Plugin`、`six_dof::WkSixDOF_Tuner::SimInterface`、`six_dof::WkSixDOF_Tuner::WriteDataEvent`、`wkf::WkSixDOF_Tuner::MainWidget` | 通过 |
| `warlock/plugins/Tracks/source` | 14 | `WkTracks::PlatformTracksRequestCommand`、`wkf::WkTracks::Plugin`、`WkTracks::SimInterface`、`WkTracks::AllTracksRequestCommand`、`WkTracks::TeamTracksRequestCommand` | 通过 |
| `warlock/plugins/WsfPrompt/source` | 14 | `WkWsfPrompt::Plugin`、`WkWsfPrompt::SimInterface`、`WkWsfPrompt::PromptDialog`、`WkWsfPrompt::PauseCommand`、`WkWsfPrompt::ResumeCommand` | 通过 |
| `wizard/plugins/RouteBrowser/source` | 14 | `RouteBrowser::RouteBrowserCreateDialog`、`RouteBrowser::RouteBrowserEditDialog`、`wizard::RouteBrowser::RouteBrowserInterface`、`RouteBrowser::CreateGlobalRouteDialog`、`RouteBrowser::Plugin` | 通过 |
| `wizard/plugins/ScenarioAnalyzer/source` | 14 | `ScenarioAnalyzer::ScenarioAnalyzerPlugin`、`ScenarioAnalyzer::Plugin`、`ScenarioAnalyzer::ScenarioAnalyzerPluginRegistration`、`ScenarioAnalyzer::ExpandingResultsGroupModel`、`ScenarioAnalyzer::ResultsTreeView` | 通过 |
| `wsf_plugins/wsf_multiresolution/source` | 14 | `WsfMultiresolutionWrapperMetaModel`、`WsfMultiresolutionPlatformComponent`、`wsf::multiresolution::WsfMultiresolutionMultirunTable`、`wsf::multiresolution::FidelityRange`、`WsfMultiresolutionTypes` | 通过 |

## CodeGraph 与源码交叉验证

CodeGraph 查询覆盖 SixDOF_Tuner、Tracks、WsfPrompt、RouteBrowser、ScenarioAnalyzer、wsf_multiresolution；`TracksPlugin.cpp::CreateTrack/SetTrackState` 命中路径内源码，ScenarioAnalyzer 同名命中含跨目录噪声，最终以目录边界内扫描为准。

本批最终索引以目录边界内的源码声明为准；跨目录命中仅记录为噪声或后续追踪线索，不直接写入本批 symbol-index。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `warlock/plugins/SixDOF_Tuner/source` | `wkf::WkSixDOF_Tuner::CommandDialog`、`WkSixDOF_Tuner::Plugin`、`six_dof::WkSixDOF_Tuner::SimInterface`、`six_dof::WkSixDOF_Tuner::WriteDataEvent`、`wkf::WkSixDOF_Tuner::MainWidget` |
| `warlock/plugins/Tracks/source` | `WkTracks::PlatformTracksRequestCommand`、`wkf::WkTracks::Plugin`、`WkTracks::SimInterface`、`WkTracks::AllTracksRequestCommand`、`WkTracks::TeamTracksRequestCommand` |
| `warlock/plugins/WsfPrompt/source` | `WkWsfPrompt::Plugin`、`WkWsfPrompt::SimInterface`、`WkWsfPrompt::PromptDialog`、`WkWsfPrompt::PauseCommand`、`WkWsfPrompt::ResumeCommand` |
| `wizard/plugins/RouteBrowser/source` | `RouteBrowser::RouteBrowserCreateDialog`、`RouteBrowser::RouteBrowserEditDialog`、`wizard::RouteBrowser::RouteBrowserInterface`、`RouteBrowser::CreateGlobalRouteDialog`、`RouteBrowser::Plugin` |
| `wizard/plugins/ScenarioAnalyzer/source` | `ScenarioAnalyzer::ScenarioAnalyzerPlugin`、`ScenarioAnalyzer::Plugin`、`ScenarioAnalyzer::ScenarioAnalyzerPluginRegistration`、`ScenarioAnalyzer::ExpandingResultsGroupModel`、`ScenarioAnalyzer::ResultsTreeView` |
| `wsf_plugins/wsf_multiresolution/source` | `WsfMultiresolutionWrapperMetaModel`、`WsfMultiresolutionPlatformComponent`、`wsf::multiresolution::WsfMultiresolutionMultirunTable`、`wsf::multiresolution::FidelityRange`、`WsfMultiresolutionTypes` |

## 已知风险

本批包含多个 UI/工具层目录，Phase 2 只确认入口、边界和代表性符号；业务规则解释需要在下一步沿命令处理、事件生产、extension 注册和结果数据生产端继续追踪。子 agent 已补充的具体风险点已折叠进职责/深挖点，后续业务逻辑分析应按这些入口继续验证。
