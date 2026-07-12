# Phase 2 batch29 增量验证报告

> **验证日期**：2026-07-11
> **验证对象**：ResultPlatformHistory、Brawler、Joystick、Engage、post_processor 与时间控制
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 6 个目录已标记为 `done_batch29`。 |
| file-index 覆盖 | 通过 | 97 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 30 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤，未写入不属于本批目录的符号。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `mystic/plugins/ResultPlatformHistory/source` | 15 | `RvPlatformHistory::Plugin`、`RvPlatformHistory::StateData`、`RvPlatformHistory::TracelineData`、`RvPlatformHistory::WingRibbonData`、`RvPlatformHistory::BehaviorStateData` | 通过 |
| `wsf_plugins/wsf_brawler/source` | 15 | `WsfBrawler`、`WsfBrawlerProcessor`、`WsfBrawlerMover`、`WsfBrawlerFuel`、`WsfBrawlerConsicousnessEvent` | 通过 |
| `warlock/plugins/Joystick/source` | 16 | `Joystick::Plugin`、`Joystick::SimInterface`、`Joystick::ActivatePilotCommand`、`Joystick::ControlCommand`、`Joystick::JoystickDataContainer` | 通过 |
| `wizard/plugins/Engage/source` | 16 | `Engage::Plugin`、`Engage::Dialog`、`Engage::TableWidget`、`Engage::TableRow`、`Engage::OutputItem` | 通过 |
| `post_processor/lib/source` | 17 | `Configuration`、`Options`、`Report`、`CommunicationReport`、`DetectionReport` | 通过 |
| `mystic/plugins/ResultTimeController/source` | 18 | `RvTimeController::Plugin`、`RvTimeController::Interface`、`RvTimeController::Toolbar`、`RvTimeController::StatusWidget`、`RvTimeController::BookmarkBrowser` | 通过 |

## CodeGraph 与源码交叉验证

CodeGraph 查询覆盖 ResultPlatformHistory、wsf_brawler、Joystick、Engage、post_processor、ResultTimeController；命中 Engage 事件头和若干跨模块 WSF 符号，正式归属只采纳本批目录内源码。

本批最终索引以目录边界内的源码声明为准；跨目录命中仅记录为噪声或后续追踪线索，不直接写入本批 symbol-index。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `mystic/plugins/ResultPlatformHistory/source` | `RvPlatformHistory::PlatformHistoryBehaviorColorWidget`、`RvPlatformHistory::PlatformStateData`、`RvPlatformHistory::Plugin`、`rv::RvPlatformHistory::BehaviorStateData`、`RvPlatformHistory::MonoStateData` |
| `wsf_plugins/wsf_brawler/source` | `WsfBrawlerConsicousnessEvent`、`ConsicousnessEventType`、`WsfBrawler`、`WsfBrawlerFuel`、`WsfBrawlerMover` |
| `warlock/plugins/Joystick/source` | `sdl::Joystick::Plugin`、`Joystick::SimInterface`、`Joystick::HUD_DataCommand`、`Joystick::PlatformAddedEvent`、`Joystick::PlatformDeletedEvent` |
| `wizard/plugins/Engage/source` | `Engage::Plugin`、`Engage::TableWidget`、`Engage::Dialog`、`Engage::OutputRateDialog`、`Engage::RunOutputDialog` |
| `post_processor/lib/source` | `EventData`、`ChangedEvent`、`EclipseEvent`、`CommunicationReport`、`Configuration` |
| `mystic/plugins/ResultTimeController/source` | `RvTimeController::BookmarkBrowser`、`RvTimeController::PrefWidget`、`RvTimeController::StatusWidget`、`RvTimeController::Plugin`、`RvTimeController::Toolbar` |

## 已知风险

本批包含多个 UI/工具层目录，Phase 2 只确认入口、边界和代表性符号；业务规则解释需要在下一步沿命令处理、事件生产、extension 注册和结果数据生产端继续追踪。子 agent 已补充的具体风险点已折叠进职责/深挖点，后续业务逻辑分析应按这些入口继续验证。
