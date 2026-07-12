# Phase 2 完成记录：batch32 wsf_fires、wsf_ripr、EventOutput、P6DOF_Controller、weapon_tools 与 comm vis common

> **完成日期**：2026-07-11
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `wsf_plugins/wsf_fires/source` | 22 | `Fires::FiresTables`、`Fires::FiresTableLoader`、`Fires::BallisticPath`、`Fires::FiresLaunchComputer`、`Fires::FiresMover` | WSF fires 插件源码，注册火力扩展、弹道表、launch computer、fires mover 和 DIS observer。 |
| `core/wsf_ripr/source` | 24 | `WsfRIPRManager`、`wsf::comm::WsfRIPRProcessor`、`WsfRIPRJobBoard`、`wsf::comm::WsfRIPRJob`、`SafeRIPRProc` | WSF RIPR 协作任务框架，管理 processor、任务板、投标/分配/进度、脚本 API 和 XIO 同步。 |
| `wizard/plugins/EventOutput/source` | 24 | `wizard::EventOutput::Plugin`、`wizard::EventOutput::Dialog`、`wizard::EventOutput::editor::Editor`、`wizard::EventOutput::tokenizer::Tokenizer`、`wizard::EventOutput::event::Widget` | Wizard event output 插件，用图形化方式编辑 csv_event_output/event_output block 并写回文本。 |
| `warlock/plugins/P6DOF_Controller/source` | 26 | `WkP6DOF_Controller::Plugin`、`WkP6DOF_Controller::PluginObject`、`WkP6DOF_Controller::SimInterface`、`WkP6DOF_Controller::P6DOF_ControllerDataContainer`、`WkP6DOF_Controller::HUD` | Warlock deprecated P6DOF 飞行控制插件，连接 P6DOF 平台、SDL 输入、HUD/音频和 sim bridge。 |
| `weapon_tools/source` | 26 | `ToolManager`、`Tool`、`WeaponToolsExtension`、`WeaponObserver`、`TargetMover` | weapon_tools 应用入口，加载扩展、处理输入、驱动 WsfEventStepSimulation，并批量生成武器工具输出。 |
| `tools/wkf/comm_vis/wkf_comm_vis_common/source` | 29 | `wkf::CommVisDialog`、`wkf::DataContainer`、`wkf::CommEvent`、`wkf::CommVisPacketGraphicsItem`、`wkf::CommVisLink` | WKF 通信可视化公共组件，缓存通信事件，构建节点/链路并动画显示 packet/hop。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 命中 `weapon_tools.cpp::weapon_tools` 和 CommVis 公共图元；子 agent 补充了 fires、RIPR、EventOutput、P6DOF_Controller、weapon_tools、wkf_comm_vis_common 的具体业务入口和风险点。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `wsf_plugins/wsf_fires/source` | 火力业务入口，后续应追 FiresMover/FiresPath/FiresLaunchComputer 的发射与弹道计算链。 |
| `core/wsf_ripr/source` | 外部协作/任务分配入口，后续重点复核 JobBoard 所有权、processor 判空和 XIO 同步边界。 |
| `wizard/plugins/EventOutput/source` | 事件输出配置入口，后续应复核 tokenizer/editor 写回、右键 connect 和空 current file。 |
| `warlock/plugins/P6DOF_Controller/source` | 旧 P6DOF 控制入口，后续与 Joystick/HeadUpView/SixDOF_Tuner 对照。 |
| `weapon_tools/source` | 武器工具高价值入口，后续应追 ToolManager、Tool、LaunchComputer generator 和主循环结束条件。 |
| `tools/wkf/comm_vis/wkf_comm_vis_common/source` | 通信拓扑/packet 可视化公共入口，后续可与 Warlock/Mystic/Wizard CommVis 生产消费链合并。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch32-verify-report.md` |

## 已知问题

1. 本批多处存在同名或相邻模块命中，CodeGraph 结果只作为候选证据，最终归属以完整路径前缀为准。
2. 批次内 UI/工具类目录多为消费侧或配置侧入口；真正业务规则仍需在下一步沿 sim command、event pipe、extension 注册和 ResultData 生产链继续追踪。
3. 大目录 `core/wsf_parser`、`wizard/plugins`、`core/wsf_space`、`wsf_plugins/wsf_coverage` 仍按实际展开数延期拆分，不在本批误标完成。

## 下游就绪

本批新增 6 个最小目录单元、151 个 source/header 和 30 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
