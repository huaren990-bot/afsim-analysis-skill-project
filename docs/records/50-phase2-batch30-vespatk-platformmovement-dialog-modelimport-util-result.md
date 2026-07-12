# Phase 2 完成记录：batch30 VESPA Qt、PlatformMovement、DialogBuilder、ModelImport、wsf_util 与行为分析结果

> **完成日期**：2026-07-11
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `tools/vespatk/vespatk_qt/source` | 18 | `vespa::VaWidget`、`vespa::VaOverlayMapGrid`、`vespa::VaOverlayMapRings`、`vespa::VaDecoratorNode`、`vespa::AngleEntry` | VESPA Qt 工具层，提供 Qt/OpenGL 嵌入 OSG/VESPA viewer、地图网格/测距环 overlay、decorator 和 scenegraph 浏览器。 |
| `warlock/plugins/PlatformMovement/source` | 18 | `WkPlatformMovement::Plugin`、`WkPlatformMovement::RouteBrowserInterface`、`WkPlatformMovement::SimInterface`、`vespa::WkPlatformMovement::RouteEvent`、`WkPlatformMovement::Command` | Warlock 平台移动插件，提供路线浏览/编辑以及 altitude/location/speed/heading/route 等仿真命令。 |
| `warlock/plugins/DialogBuilder/source` | 19 | `WkDialogBuilder::Plugin`、`WkDialogBuilder::DockWidget`、`WkDialogBuilder::MainDialog`、`WkDialogBuilder::DialogDef`、`WkDialogBuilder::ScriptCreator` | Warlock 动态对话框构建插件，支持自定义脚本按钮、参数、过滤器、快捷键和返回值展示。 |
| `wizard/plugins/ModelImport/source` | 19 | `ModelImport::Plugin`、`ModelImport::DockWidget`、`ModelImport::DirectoryReaderThread`、`ModelImport::FileData`、`ParserLite::FileInput` | Wizard 模型导入器，扫描模型目录、生成/读取 JSON 元数据、递归导入文件及依赖。 |
| `core/wsf_util/source` | 20 | `UtPackSchema`、`UtBuffer`、`UtPackSerializer`、`UtPackMessageStream`、`UtmlObject` | WSF utility 小源码单元，提供 UtPack、UTML、字节缓冲、CSV、tar 打包和 SHA digest 等基础工具。 |
| `mystic/plugins/ResultBehaviorAnalysisTool/source` | 21 | `RvBAT::Plugin`、`rv::RvBAT::DockWindow`、`rv::RvBAT::Interface`、`RvBAT::ABTScene`、`RvBAT::FSMScene` | Mystic 行为分析结果工具，读取 ABT/FSM 消息并构建 QGraphicsScene 展示节点、状态、转换和 blackboard。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 对 PlatformMovement 命中 `PlatformMovementSimEvents.hpp` 和 `PlatformMovementSimCommands.hpp`，确认 route/altitude/heading/location/speed/follow route 等运行时命令体系；子 agent 补充了 VESPA、DialogBuilder、ModelImport、wsf_util 和 BAT 的源码证据。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `tools/vespatk/vespatk_qt/source` | VESPA 工具 UI 入口，后续重点检查 observer 生命周期、相机更新几何和跨日期线/单位切换。 |
| `warlock/plugins/PlatformMovement/source` | 高价值运行时 mutation 入口，后续应追 PlatformMovementSimCommands 对平台 mover/route 的具体修改。 |
| `warlock/plugins/DialogBuilder/source` | 脚本执行 UI 入口，后续应追 HandleScriptExecution、BuildScriptInstance、ExecuteScriptInstance 的权限和参数链。 |
| `wizard/plugins/ModelImport/source` | 资源导入入口，后续应复核 ImportRecursionHelper 拷贝条件和后台解析线程数据所有权。 |
| `core/wsf_util/source` | 通用工具入口，后续重点看 UtPack schema/layout 同步和 UtBuffer 边界调用责任。 |
| `mystic/plugins/ResultBehaviorAnalysisTool/source` | 行为分析消费侧入口，后续应追 ABT/FSM 消息生产端和大图布局性能。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch30-verify-report.md` |

## 已知问题

1. 本批多处存在同名或相邻模块命中，CodeGraph 结果只作为候选证据，最终归属以完整路径前缀为准。
2. 批次内 UI/工具类目录多为消费侧或配置侧入口；真正业务规则仍需在下一步沿 sim command、event pipe、extension 注册和 ResultData 生产链继续追踪。
3. 大目录 `core/wsf_parser`、`wizard/plugins`、`core/wsf_space`、`wsf_plugins/wsf_coverage` 仍按实际展开数延期拆分，不在本批误标完成。

## 下游就绪

本批新增 6 个最小目录单元、115 个 source/header 和 30 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
