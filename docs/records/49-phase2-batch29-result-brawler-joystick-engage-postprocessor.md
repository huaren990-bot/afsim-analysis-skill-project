# Phase 2 完成记录：batch29 ResultPlatformHistory、Brawler、Joystick、Engage、post_processor 与时间控制

> **完成日期**：2026-07-11
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `mystic/plugins/ResultPlatformHistory/source` | 15 | `RvPlatformHistory::Plugin`、`RvPlatformHistory::StateData`、`RvPlatformHistory::TracelineData`、`RvPlatformHistory::WingRibbonData`、`RvPlatformHistory::BehaviorStateData` | Mystic 平台历史结果视图，消费平台历史轨迹/状态。 |
| `wsf_plugins/wsf_brawler/source` | 15 | `WsfBrawler`、`WsfBrawlerProcessor`、`WsfBrawlerMover`、`WsfBrawlerFuel`、`WsfBrawlerConsicousnessEvent` | WSF Brawler 插件适配层，承接 Brawler 模型注册和仿真集成。 |
| `warlock/plugins/Joystick/source` | 16 | `Joystick::Plugin`、`Joystick::SimInterface`、`Joystick::ActivatePilotCommand`、`Joystick::ControlCommand`、`Joystick::JoystickDataContainer` | Warlock joystick 插件，提供外部操纵输入到仿真控制的桥接。 |
| `wizard/plugins/Engage/source` | 16 | `Engage::Plugin`、`Engage::Dialog`、`Engage::TableWidget`、`Engage::TableRow`、`Engage::OutputItem` | Wizard Engage 插件，提供交战相关场景配置/展示入口。 |
| `post_processor/lib/source` | 17 | `Configuration`、`Options`、`Report`、`CommunicationReport`、`DetectionReport` | post_processor 公共库，提供结果后处理、报表和数据处理支撑。 |
| `mystic/plugins/ResultTimeController/source` | 18 | `RvTimeController::Plugin`、`RvTimeController::Interface`、`RvTimeController::Toolbar`、`RvTimeController::StatusWidget`、`RvTimeController::BookmarkBrowser` | Mystic 结果时间控制插件，驱动结果播放时间、速率和 UI 同步。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 查询覆盖 ResultPlatformHistory、wsf_brawler、Joystick、Engage、post_processor、ResultTimeController；命中 Engage 事件头和若干跨模块 WSF 符号，正式归属只采纳本批目录内源码。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `mystic/plugins/ResultPlatformHistory/source` | 结果平台历史消费入口，后续应追 ResultPlatform 时间序列字段来源。 |
| `wsf_plugins/wsf_brawler/source` | 空战 Brawler 模型入口，后续应与 brawler/source 的 mover/MIND/评估逻辑串联。 |
| `warlock/plugins/Joystick/source` | 人为操纵/控制输入入口，后续应追 joystick command/event 对 platform/mover 的影响。 |
| `wizard/plugins/Engage/source` | 交战配置侧入口，后续应与 engage/source 和 weapon engagement 事件生产链对齐。 |
| `post_processor/lib/source` | 后处理基础库入口，后续按调用者追具体业务指标。 |
| `mystic/plugins/ResultTimeController/source` | 结果回放控制入口，后续应与 ResultDb 时钟、平台插值和播放状态串联。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch29-verify-report.md` |

## 已知问题

1. 本批多处存在同名或相邻模块命中，CodeGraph 结果只作为候选证据，最终归属以完整路径前缀为准。
2. 批次内 UI/工具类目录多为消费侧或配置侧入口；真正业务规则仍需在下一步沿 sim command、event pipe、extension 注册和 ResultData 生产链继续追踪。
3. 大目录 `core/wsf_parser`、`wizard/plugins`、`core/wsf_space`、`wsf_plugins/wsf_coverage` 仍按实际展开数延期拆分，不在本批误标完成。

## 下游就绪

本批新增 6 个最小目录单元、97 个 source/header 和 30 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
