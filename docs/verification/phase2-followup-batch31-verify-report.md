# Phase 2 batch31 增量验证报告

> **验证日期**：2026-07-11
> **验证对象**：scene_gen、Chat、MapDisplay、SimController、MapUtils 与 SimulationManager
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 6 个目录已标记为 `done_batch31`。 |
| file-index 覆盖 | 通过 | 130 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 30 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤，未写入不属于本批目录的符号。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `tools/scene_gen/source` | 21 | `sceneGen::SceneGenPlatformTeam`、`sceneGen::SceneGenPlatformGroup`、`sceneGen::SceneGenInputFileReader`、`sceneGen::SceneGenInputData`、`sceneGen::SceneGenGeoPathGen` | 通过 |
| `warlock/plugins/Chat/source` | 21 | `Chat::Plugin`、`Chat::SimInterface`、`Chat::DockWidget`、`Chat::ChatCommand`、`Chat::Network` | 通过 |
| `tools/wkf/plugins/MapDisplay/source` | 22 | `wkf::Map::Plugin`、`wkf::Map::DockWidget`、`Map::OverlayScale`、`vespa::Map::CameraMotion`、`wkf::Map::ToolBar` | 通过 |
| `warlock/plugins/SimController/source` | 22 | `WkSimController::Plugin`、`WkSimController::SimControllerEvent`、`WkSimController::SimInterface`、`WkSimController::PauseCommand`、`wkf::WkSimController::Toolbar` | 通过 |
| `wizard/plugins/MapUtils/source` | 22 | `RotateScenario::TranslateScenario::Plugin`、`MapUtils::Message`、`MapUtils::ScenarioTransformation::DialogMenuAndButtonsWidget`、`MapUtils::PluginUtil::LineEditSliderManager`、`ScenarioTransformation::RotateScenario::Dialog` | 通过 |
| `wizard/plugins/SimulationManager/source` | 22 | `wizard::SimulationManager::Plugin`、`SimulationManager::Toolbar`、`wizard::SimulationManager::WsfScriptDebugger`、`wizard::SimulationManager::OutputDock`、`SimulationManager::ScriptBreakpointControl` | 通过 |

## CodeGraph 与源码交叉验证

CodeGraph 命中 `SimControllerSimEvents.hpp`，确认 pause/resume/complete/clock rate/start/state 事件体系；子 agent 补充了 scene_gen、Chat、MapDisplay、MapUtils、SimulationManager 的入口和风险点。

本批最终索引以目录边界内的源码声明为准；跨目录命中仅记录为噪声或后续追踪线索，不直接写入本批 symbol-index。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `tools/scene_gen/source` | `sceneGen::SceneGenPlatformTeam`、`sceneGen::SceneGenPlatformGroup`、`sceneGen::SceneGenInputFileReader`、`sceneGen::SceneGenInputData`、`sceneGen::SceneGenGeoPathGen` |
| `warlock/plugins/Chat/source` | `Chat::Plugin`、`Chat::SimInterface`、`Chat::DockWidget`、`Chat::ChatCommand`、`Chat::Network` |
| `tools/wkf/plugins/MapDisplay/source` | `wkf::Map::Plugin`、`wkf::Map::DockWidget`、`Map::OverlayScale`、`vespa::Map::CameraMotion`、`wkf::Map::ToolBar` |
| `warlock/plugins/SimController/source` | `WkSimController::Plugin`、`WkSimController::SimControllerEvent`、`WkSimController::SimInterface`、`WkSimController::PauseCommand`、`wkf::WkSimController::Toolbar` |
| `wizard/plugins/MapUtils/source` | `RotateScenario::TranslateScenario::Plugin`、`MapUtils::Message`、`MapUtils::ScenarioTransformation::DialogMenuAndButtonsWidget`、`MapUtils::PluginUtil::LineEditSliderManager`、`ScenarioTransformation::RotateScenario::Dialog` |
| `wizard/plugins/SimulationManager/source` | `wizard::SimulationManager::Plugin`、`SimulationManager::Toolbar`、`wizard::SimulationManager::WsfScriptDebugger`、`wizard::SimulationManager::OutputDock`、`SimulationManager::ScriptBreakpointControl` |

## 已知风险

本批包含多个 UI/工具层目录，Phase 2 只确认入口、边界和代表性符号；业务规则解释需要在下一步沿命令处理、事件生产、extension 注册和结果数据生产端继续追踪。子 agent 已补充的具体风险点已折叠进职责/深挖点，后续业务逻辑分析应按这些入口继续验证。
