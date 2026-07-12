# Phase 2 完成记录：batch33 wsf_mtt、air combat、CommVis、artificer、SPLAT 与 sensor plot lib

> **完成日期**：2026-07-11
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `core/wsf_mtt/source` | 30 | `MTT`、`WsfMTT_Interface`、`WsfMTT_Correlation`、`WsfMTT_Fusion`、`MTT_ActiveTrack` | WSF multi-target tracking 源码单元，处理多目标跟踪基础能力。 |
| `wsf_plugins/wsf_air_combat/source` | 31 | `WsfSA_Processor`、`WsfSA_Perceive`、`WsfSA_Assess`、`WsfSA_Predict`、`WsfAirCombatTypeManager` | WSF air combat 插件源码，承接空战模型扩展和注册。 |
| `wizard/plugins/CommVis/source` | 32 | `WizCommVis::Plugin`、`WizCommVis::CommVisDialog`、`WizCommVis::CommVisEditDialog`、`WizCommVis::CommVisAddCommDialog`、`WizCommVis::CommVisRouterNodeDialog` | Wizard CommVis 插件，提供通信可视化配置/编辑入口。 |
| `tools/artificer/source` | 34 | `artificer::V1Parser`、`artificer::V1PrototypeSummarizer`、`artificer::RunData`、`artificer::SimulationData`、`artificer::TextTable` | Artificer 工具源码，提供模型/场景工件生成或编辑支持。 |
| `wizard/plugins/SPLAT/source` | 40 | `SPLAT::Plugin`、`SPLAT::SensorAnalysisDialog`、`SPLAT::ProxyInterface`、`SPLAT::PlotOptionsDialog`、`SPLAT::PlotOptionsWidget` | Wizard SPLAT 插件，提供地形/传播/覆盖相关工具入口。 |
| `core/sensor_plot_lib/source` | 41 | `WsfSensorPlotExtension`、`Function`、`MapPlotFunction`、`MapPlotVariables`、`Sensor` | sensor_plot_lib 核心库，提供传感器图/覆盖绘制与计算支撑。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 命中 `WkCommVis::CommVisEvent` 与 `wkf::CommVisPacketGraphicsItem`，确认 CommVis 公共事件/packet 图元链；`WsfEventManager` 等核心 WSF 命中为跨目录噪声，不归入本批符号。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `core/wsf_mtt/source` | 高价值 tracking 业务入口，后续应追 track update/filter/fusion 调用链。 |
| `wsf_plugins/wsf_air_combat/source` | 高价值空战业务入口，后续应与 ResultDataAirCombat、Brawler 和 SA 生产链串联。 |
| `wizard/plugins/CommVis/source` | 通信可视化配置入口，后续与 WKF common、Warlock/Mystic CommVis 串联。 |
| `tools/artificer/source` | 工具生成入口，后续按输出类型追到场景或资源消费方。 |
| `wizard/plugins/SPLAT/source` | 传播/地形辅助入口，后续应与 sensor plot、coverage 或地形数据库调用链对齐。 |
| `core/sensor_plot_lib/source` | 高价值传感器可视化/覆盖入口，后续应追 sensor volumes、projector 和 coverage 生产链。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch33-verify-report.md` |

## 已知问题

1. 本批多处存在同名或相邻模块命中，CodeGraph 结果只作为候选证据，最终归属以完整路径前缀为准。
2. 批次内 UI/工具类目录多为消费侧或配置侧入口；真正业务规则仍需在下一步沿 sim command、event pipe、extension 注册和 ResultData 生产链继续追踪。
3. 大目录 `core/wsf_parser`、`wizard/plugins`、`core/wsf_space`、`wsf_plugins/wsf_coverage` 仍按实际展开数延期拆分，不在本批误标完成。

## 下游就绪

本批新增 6 个最小目录单元、208 个 source/header 和 30 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
