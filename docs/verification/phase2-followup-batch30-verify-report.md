# Phase 2 batch30 增量验证报告

> **验证日期**：2026-07-11
> **验证对象**：VESPA Qt、PlatformMovement、DialogBuilder、ModelImport、wsf_util 与行为分析结果
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 6 个目录已标记为 `done_batch30`。 |
| file-index 覆盖 | 通过 | 115 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 30 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤，未写入不属于本批目录的符号。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `tools/vespatk/vespatk_qt/source` | 18 | `vespa::VaWidget`、`vespa::VaOverlayMapGrid`、`vespa::VaOverlayMapRings`、`vespa::VaDecoratorNode`、`vespa::AngleEntry` | 通过 |
| `warlock/plugins/PlatformMovement/source` | 18 | `WkPlatformMovement::Plugin`、`WkPlatformMovement::RouteBrowserInterface`、`WkPlatformMovement::SimInterface`、`vespa::WkPlatformMovement::RouteEvent`、`WkPlatformMovement::Command` | 通过 |
| `warlock/plugins/DialogBuilder/source` | 19 | `WkDialogBuilder::Plugin`、`WkDialogBuilder::DockWidget`、`WkDialogBuilder::MainDialog`、`WkDialogBuilder::DialogDef`、`WkDialogBuilder::ScriptCreator` | 通过 |
| `wizard/plugins/ModelImport/source` | 19 | `ModelImport::Plugin`、`ModelImport::DockWidget`、`ModelImport::DirectoryReaderThread`、`ModelImport::FileData`、`ParserLite::FileInput` | 通过 |
| `core/wsf_util/source` | 20 | `UtPackSchema`、`UtBuffer`、`UtPackSerializer`、`UtPackMessageStream`、`UtmlObject` | 通过 |
| `mystic/plugins/ResultBehaviorAnalysisTool/source` | 21 | `RvBAT::Plugin`、`rv::RvBAT::DockWindow`、`rv::RvBAT::Interface`、`RvBAT::ABTScene`、`RvBAT::FSMScene` | 通过 |

## CodeGraph 与源码交叉验证

CodeGraph 对 PlatformMovement 命中 `PlatformMovementSimEvents.hpp` 和 `PlatformMovementSimCommands.hpp`，确认 route/altitude/heading/location/speed/follow route 等运行时命令体系；子 agent 补充了 VESPA、DialogBuilder、ModelImport、wsf_util 和 BAT 的源码证据。

本批最终索引以目录边界内的源码声明为准；跨目录命中仅记录为噪声或后续追踪线索，不直接写入本批 symbol-index。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `tools/vespatk/vespatk_qt/source` | `vespa::VaWidget`、`vespa::VaOverlayMapGrid`、`vespa::VaOverlayMapRings`、`vespa::VaDecoratorNode`、`vespa::AngleEntry` |
| `warlock/plugins/PlatformMovement/source` | `WkPlatformMovement::Plugin`、`WkPlatformMovement::RouteBrowserInterface`、`WkPlatformMovement::SimInterface`、`vespa::WkPlatformMovement::RouteEvent`、`WkPlatformMovement::Command` |
| `warlock/plugins/DialogBuilder/source` | `WkDialogBuilder::Plugin`、`WkDialogBuilder::DockWidget`、`WkDialogBuilder::MainDialog`、`WkDialogBuilder::DialogDef`、`WkDialogBuilder::ScriptCreator` |
| `wizard/plugins/ModelImport/source` | `ModelImport::Plugin`、`ModelImport::DockWidget`、`ModelImport::DirectoryReaderThread`、`ModelImport::FileData`、`ParserLite::FileInput` |
| `core/wsf_util/source` | `UtPackSchema`、`UtBuffer`、`UtPackSerializer`、`UtPackMessageStream`、`UtmlObject` |
| `mystic/plugins/ResultBehaviorAnalysisTool/source` | `RvBAT::Plugin`、`rv::RvBAT::DockWindow`、`rv::RvBAT::Interface`、`RvBAT::ABTScene`、`RvBAT::FSMScene` |

## 已知风险

本批包含多个 UI/工具层目录，Phase 2 只确认入口、边界和代表性符号；业务规则解释需要在下一步沿命令处理、事件生产、extension 注册和结果数据生产端继续追踪。子 agent 已补充的具体风险点已折叠进职责/深挖点，后续业务逻辑分析应按这些入口继续验证。
