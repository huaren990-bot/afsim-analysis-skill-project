# Phase 2 完成记录：batch28 SixDOF、tracks、prompt、route、scenario analyzer 与 multiresolution

> **完成日期**：2026-07-11
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `warlock/plugins/SixDOF_Tuner/source` | 14 | `wkf::WkSixDOF_Tuner::CommandDialog`、`WkSixDOF_Tuner::Plugin`、`six_dof::WkSixDOF_Tuner::SimInterface`、`six_dof::WkSixDOF_Tuner::WriteDataEvent`、`wkf::WkSixDOF_Tuner::MainWidget` | Warlock SixDOF 调参 UI、仿真桥和控制事件入口。 |
| `warlock/plugins/Tracks/source` | 14 | `WkTracks::PlatformTracksRequestCommand`、`wkf::WkTracks::Plugin`、`WkTracks::SimInterface`、`WkTracks::AllTracksRequestCommand`、`WkTracks::TeamTracksRequestCommand` | Warlock tracks 显示、track state 更新和平台航迹消费入口。 |
| `warlock/plugins/WsfPrompt/source` | 14 | `WkWsfPrompt::Plugin`、`WkWsfPrompt::SimInterface`、`WkWsfPrompt::PromptDialog`、`WkWsfPrompt::PauseCommand`、`WkWsfPrompt::ResumeCommand` | Warlock WSF prompt/命令输入插件，提供运行时命令交互入口。 |
| `wizard/plugins/RouteBrowser/source` | 14 | `RouteBrowser::RouteBrowserCreateDialog`、`RouteBrowser::RouteBrowserEditDialog`、`wizard::RouteBrowser::RouteBrowserInterface`、`RouteBrowser::CreateGlobalRouteDialog`、`RouteBrowser::Plugin` | Wizard route browser，提供路线对象浏览、选择和编辑辅助。 |
| `wizard/plugins/ScenarioAnalyzer/source` | 14 | `ScenarioAnalyzer::ScenarioAnalyzerPlugin`、`ScenarioAnalyzer::Plugin`、`ScenarioAnalyzer::ScenarioAnalyzerPluginRegistration`、`ScenarioAnalyzer::ExpandingResultsGroupModel`、`ScenarioAnalyzer::ResultsTreeView` | Wizard scenario analyzer 插件，承接场景分析脚本、检查结果和 UI 展示。 |
| `wsf_plugins/wsf_multiresolution/source` | 14 | `WsfMultiresolutionWrapperMetaModel`、`WsfMultiresolutionPlatformComponent`、`wsf::multiresolution::WsfMultiresolutionMultirunTable`、`wsf::multiresolution::FidelityRange`、`WsfMultiresolutionTypes` | WSF multiresolution 插件源码，处理多分辨率模型扩展与注册。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 查询覆盖 SixDOF_Tuner、Tracks、WsfPrompt、RouteBrowser、ScenarioAnalyzer、wsf_multiresolution；`TracksPlugin.cpp::CreateTrack/SetTrackState` 命中路径内源码，ScenarioAnalyzer 同名命中含跨目录噪声，最终以目录边界内扫描为准。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `warlock/plugins/SixDOF_Tuner/source` | SixDOF 调参与运行时控制入口，后续应追 six_dof vehicle/controller 与调参命令。 |
| `warlock/plugins/Tracks/source` | 航迹显示消费侧入口，后续应与 track db 和 sensor/local track 消息生产链串联。 |
| `warlock/plugins/WsfPrompt/source` | 运行时命令侧入口，后续应追 prompt command 如何进入 sim/script 解释链。 |
| `wizard/plugins/RouteBrowser/source` | 场景 route 配置消费/编辑入口，后续应与 MapRoute、route parser 和 platform route 绑定逻辑串联。 |
| `wizard/plugins/ScenarioAnalyzer/source` | 场景静态分析入口，后续应追注册脚本类型和检查器输出。 |
| `wsf_plugins/wsf_multiresolution/source` | 模型分辨率/聚合行为入口，后续应追 extension 注册和 scenario 输入参数。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch28-verify-report.md` |

## 已知问题

1. 本批多处存在同名或相邻模块命中，CodeGraph 结果只作为候选证据，最终归属以完整路径前缀为准。
2. 批次内 UI/工具类目录多为消费侧或配置侧入口；真正业务规则仍需在下一步沿 sim command、event pipe、extension 注册和 ResultData 生产链继续追踪。
3. 大目录 `core/wsf_parser`、`wizard/plugins`、`core/wsf_space`、`wsf_plugins/wsf_coverage` 仍按实际展开数延期拆分，不在本批误标完成。

## 下游就绪

本批新增 6 个最小目录单元、84 个 source/header 和 30 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
