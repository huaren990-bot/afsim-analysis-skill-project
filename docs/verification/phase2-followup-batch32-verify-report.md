# Phase 2 batch32 增量验证报告

> **验证日期**：2026-07-11
> **验证对象**：wsf_fires、wsf_ripr、EventOutput、P6DOF_Controller、weapon_tools 与 comm vis common
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 6 个目录已标记为 `done_batch32`。 |
| file-index 覆盖 | 通过 | 151 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 30 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤，未写入不属于本批目录的符号。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `wsf_plugins/wsf_fires/source` | 22 | `Fires::FiresTables`、`Fires::FiresTableLoader`、`Fires::BallisticPath`、`Fires::FiresLaunchComputer`、`Fires::FiresMover` | 通过 |
| `core/wsf_ripr/source` | 24 | `WsfRIPRManager`、`wsf::comm::WsfRIPRProcessor`、`WsfRIPRJobBoard`、`wsf::comm::WsfRIPRJob`、`SafeRIPRProc` | 通过 |
| `wizard/plugins/EventOutput/source` | 24 | `wizard::EventOutput::Plugin`、`wizard::EventOutput::Dialog`、`wizard::EventOutput::editor::Editor`、`wizard::EventOutput::tokenizer::Tokenizer`、`wizard::EventOutput::event::Widget` | 通过 |
| `warlock/plugins/P6DOF_Controller/source` | 26 | `WkP6DOF_Controller::Plugin`、`WkP6DOF_Controller::PluginObject`、`WkP6DOF_Controller::SimInterface`、`WkP6DOF_Controller::P6DOF_ControllerDataContainer`、`WkP6DOF_Controller::HUD` | 通过 |
| `weapon_tools/source` | 26 | `ToolManager`、`Tool`、`WeaponToolsExtension`、`WeaponObserver`、`TargetMover` | 通过 |
| `tools/wkf/comm_vis/wkf_comm_vis_common/source` | 29 | `wkf::CommVisDialog`、`wkf::DataContainer`、`wkf::CommEvent`、`wkf::CommVisPacketGraphicsItem`、`wkf::CommVisLink` | 通过 |

## CodeGraph 与源码交叉验证

CodeGraph 命中 `weapon_tools.cpp::weapon_tools` 和 CommVis 公共图元；子 agent 补充了 fires、RIPR、EventOutput、P6DOF_Controller、weapon_tools、wkf_comm_vis_common 的具体业务入口和风险点。

本批最终索引以目录边界内的源码声明为准；跨目录命中仅记录为噪声或后续追踪线索，不直接写入本批 symbol-index。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `wsf_plugins/wsf_fires/source` | `Fires::FiresTables`、`Fires::FiresTableLoader`、`Fires::BallisticPath`、`Fires::FiresLaunchComputer`、`Fires::FiresMover` |
| `core/wsf_ripr/source` | `WsfRIPRManager`、`wsf::comm::WsfRIPRProcessor`、`WsfRIPRJobBoard`、`wsf::comm::WsfRIPRJob`、`SafeRIPRProc` |
| `wizard/plugins/EventOutput/source` | `wizard::EventOutput::Plugin`、`ValueWidget::event::Dialog`、`EventOutput::event::Widget`、`editor::tokenizer::Editor`、`editor::tokenizer::Tokenizer` |
| `warlock/plugins/P6DOF_Controller/source` | `WkP6DOF_Controller::P6DOF_ControllerDataContainer`、`WkP6DOF_Controller::Plugin`、`sdl::WkP6DOF_Controller::PluginObject`、`WkP6DOF_Controller::SimInterface`、`WkP6DOF_Controller::HUD` |
| `weapon_tools/source` | `ToolManager`、`Tool`、`WeaponToolsExtension`、`WeaponObserver`、`TargetMover` |
| `tools/wkf/comm_vis/wkf_comm_vis_common/source` | `wkf::CommVisDialog`、`wkf::DataContainer`、`wkf::CommEvent`、`wkf::CommVisPacketGraphicsItem`、`wkf::CommVisLink` |

## 已知风险

本批包含多个 UI/工具层目录，Phase 2 只确认入口、边界和代表性符号；业务规则解释需要在下一步沿命令处理、事件生产、extension 注册和结果数据生产端继续追踪。子 agent 已补充的具体风险点已折叠进职责/深挖点，后续业务逻辑分析应按这些入口继续验证。
