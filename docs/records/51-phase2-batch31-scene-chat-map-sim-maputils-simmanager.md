# Phase 2 完成记录：batch31 scene_gen、Chat、MapDisplay、SimController、MapUtils 与 SimulationManager

> **完成日期**：2026-07-11
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `tools/scene_gen/source` | 21 | `sceneGen::SceneGenPlatformTeam`、`sceneGen::SceneGenPlatformGroup`、`sceneGen::SceneGenInputFileReader`、`sceneGen::SceneGenInputData`、`sceneGen::SceneGenGeoPathGen` | scene_gen 命令行工具，从输入场景描述读取平台组并生成平台布局脚本和 startup 脚本。 |
| `warlock/plugins/Chat/source` | 21 | `Chat::Plugin`、`Chat::SimInterface`、`Chat::DockWidget`、`Chat::ChatCommand`、`Chat::Network` | Warlock chat 插件，管理聊天 UI、频道/分组、网络包收发，并映射到仿真 command/event pipe。 |
| `tools/wkf/plugins/MapDisplay/source` | 22 | `wkf::Map::Plugin`、`wkf::Map::DockWidget`、`Map::OverlayScale`、`vespa::Map::CameraMotion`、`wkf::Map::ToolBar` | WKF map display 插件，提供通用 3D 地图、viewer、toolbar、cursor status、测距尺和实体菜单。 |
| `warlock/plugins/SimController/source` | 22 | `WkSimController::Plugin`、`WkSimController::SimControllerEvent`、`WkSimController::SimInterface`、`WkSimController::PauseCommand`、`wkf::WkSimController::Toolbar` | Warlock 仿真控制插件，处理加载场景、暂停/继续/终止/重启、时钟速率和落后状态。 |
| `wizard/plugins/MapUtils/source` | 22 | `RotateScenario::TranslateScenario::Plugin`、`MapUtils::Message`、`MapUtils::ScenarioTransformation::DialogMenuAndButtonsWidget`、`MapUtils::PluginUtil::LineEditSliderManager`、`ScenarioTransformation::RotateScenario::Dialog` | Wizard 地图辅助工具，支持创建/克隆/删除平台、场景/实体旋转平移和 ghost 预览。 |
| `wizard/plugins/SimulationManager/source` | 22 | `wizard::SimulationManager::Plugin`、`SimulationManager::Toolbar`、`wizard::SimulationManager::WsfScriptDebugger`、`wizard::SimulationManager::OutputDock`、`SimulationManager::ScriptBreakpointControl` | Wizard 仿真执行与调试插件，管理 WSF executable、运行/调试/停止/重启、输出面板、断点/调用栈/watch。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 命中 `SimControllerSimEvents.hpp`，确认 pause/resume/complete/clock rate/start/state 事件体系；子 agent 补充了 scene_gen、Chat、MapDisplay、MapUtils、SimulationManager 的入口和风险点。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `tools/scene_gen/source` | 场景生成工具入口，后续应追输出脚本格式、路径拼接和命令行缺参边界。 |
| `warlock/plugins/Chat/source` | 用户消息入口，后续应复核 roll call/channel 字段、网络来源信任和链接解析。 |
| `tools/wkf/plugins/MapDisplay/source` | 地图显示基础入口，后续应沿 viewer/overlay、选择删除和拖放打开文件路径继续追。 |
| `warlock/plugins/SimController/source` | 高价值仿真生命周期入口，后续应追 SimControllerSimCommands/Events 与 DIS/XIO 联机控制。 |
| `wizard/plugins/MapUtils/source` | 场景编辑 mutation 入口，后续应复核 Apply*Change 类型判断、route waypoint size 和撤销路径。 |
| `wizard/plugins/SimulationManager/source` | 仿真启动配置入口，后续应复核 NewExecution 参数 quoting、输出链接打开和 XIO debug 生命周期。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch31-verify-report.md` |

## 已知问题

1. 本批多处存在同名或相邻模块命中，CodeGraph 结果只作为候选证据，最终归属以完整路径前缀为准。
2. 批次内 UI/工具类目录多为消费侧或配置侧入口；真正业务规则仍需在下一步沿 sim command、event pipe、extension 注册和 ResultData 生产链继续追踪。
3. 大目录 `core/wsf_parser`、`wizard/plugins`、`core/wsf_space`、`wsf_plugins/wsf_coverage` 仍按实际展开数延期拆分，不在本批误标完成。

## 下游就绪

本批新增 6 个最小目录单元、130 个 source/header 和 30 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
