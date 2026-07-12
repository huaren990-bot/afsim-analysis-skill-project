# Phase 2 最小目录单元分析计划

> **日期**：2026-06-24
> **最近更新**：2026-07-11，batch28-batch33 完成 SixDOF、Tracks、Prompt、Route、ScenarioAnalyzer、multiresolution、Result/Brawler/Joystick/Engage/PostProcessor、PlatformMovement、SimController、fires/RIPR/weapon tools/CommVis、MTT/air combat/SPLAT/sensor plot 等 36 个最小目录单元；继续由子 agent 只读取证，主 agent 统一合并 JSONL 与文档。
> **依据**：`workspace/project-boundary/project-boundary.json` 的 `analysis_boundaries` 与 `module_hierarchy`
> **目标**：面对大型 AFSIM C++ 源码，按目录树中的最小可验证源码单元逐步补强 Phase 2，而不是一次性重写全部模块。

## 1. 分析策略

Phase 2 后续分析按“系统 -> 子系统 -> 最小目录单元”推进：

| 层级 | 含义 | 示例 |
|------|------|------|
| 系统 | Phase 1 定义的主分析域 | `core_framework`、`plugin_modules`、`applications`、`developer_tools` |
| 子系统 | `swdev/src` 下的一级或二级职责目录 | `core/wsf_weapon_server`、`wsf_plugins/wsf_six_dof` |
| 最小目录单元 | 通常是含 `source/` 的最小源码目录；没有 `source/` 时使用可独立归属的最小源码目录 | `afsim-2_9/swdev/src/core/wsf_weapon_server/source` |

默认排除 `afsim-2_9/demos`、`afsim-2_9/documentation`、`afsim-2_9/training`、`afsim-2_9/resources` 的架构级模块分析。它们可作为场景、文档、训练或资源证据，但不进入 Phase 2 默认模块概览。

## 2. 工作清单

机器可读工作清单已生成：

`workspace/source-index/phase2-analysis-unit-worklist.jsonl`

当前统计：

| 指标 | 值 |
|------|-----|
| 最小目录单元数 | 237 |
| 默认范围内 source/header 数 | 17,179 |
| 已完成单元 | 174 |
| 当前完成单元 | batch33：`core/wsf_mtt/source`、`wsf_plugins/wsf_air_combat/source`、`wizard/plugins/CommVis/source`、`tools/artificer/source`、`wizard/plugins/SPLAT/source`、`core/sensor_plot_lib/source` |

## 3. 批次规则

最小目录单元仍是 Phase 2 的原子分析粒度；后续批次可以在保证证据完整和结果可验证的前提下，同时处理多个最小目录单元。批次规模按正确性优先控制：

| 规则 | 要求 |
|------|------|
| 原子粒度 | 每个最小目录单元必须独立列出边界、文件、关键符号、职责、未确认项；不得把多个目录粗略合并成一个无法追溯的模块结论。 |
| 批次合并 | 同一批次优先合并文件数少、边界清晰、职责相近或互不耦合的多个最小目录单元。复杂目录、跨模块调用密集目录或证据不足目录应单独成批。 |
| 批次容量 | 建议每批处理 2-6 个小目录；在每个目录都能独立取证、独立验证且主 agent 能完成复核时，可超过约 20 个 source/header 文件。若 CodeGraph 证据、调用链或源码语义较复杂，应主动缩小批次。 |
| 正确性门槛 | 每个目录都必须完成 CodeGraph/源码交叉确认、file-index 更新、symbol-index 粗符号修正和人工可读说明；任一目录存疑时可拆出为后续批次，不影响同批其他已确认目录落地。 |

每个批次完成后必须更新：

1. `workspace/source-index/file-index.jsonl`：补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions`、中文 `brief`。
2. `workspace/source-index/symbol-index-phase2.jsonl`：修正该单元粗符号，过滤导出宏伪符号，保留真实 class/struct/enum/typedef。
3. `docs/architecture/module-overview-v2-incremental.md`：追加该单元的人类可读说明。
4. `docs/verification/phase2-followup-batchNN-verify-report.md`：验证该批次；若批次包含多个目录，报告必须覆盖全部目录，并提供按目录拆分的文件数、符号数、证据来源和风险项。
5. `docs/records/NN-phase2-...md`：记录批次处理结果。

## 4. 子 agent 并行规则

为提升大型 C++ 项目的 Phase 2 分析效率，后续批次可采用子 agent 并行，但主 agent 必须保留最终合并和一致性校验职责：

| 角色 | 职责 |
|------|------|
| 主 agent | 选定批次目录、分配互不冲突的目录范围、统一 schema、合并 `file-index.jsonl`/`symbol-index-phase2.jsonl`/文档、执行最终验证。 |
| 子 agent | 针对分配到的最小目录单元读取 CodeGraph 和源码，输出目录边界、文件清单、关键符号、调用/注册证据、未确认项和建议索引补丁。 |

并行执行时遵守以下约束：

1. 子 agent 的分析范围必须是一个或多个明确的最小目录单元，避免多个 agent 同时判断同一目录。
2. 默认由主 agent 写入共享 JSONL 和正式 `docs/` 报告；子 agent 只产出结构化分析摘要或临时补丁建议，除非已分配互不重叠的输出文件。
3. 主 agent 合并时必须逐目录复核子 agent 的证据链，尤其是导出宏伪符号、匿名命名空间符号、注册入口和跨目录调用归属。
4. 批次报告必须囊括该批所有目录，采用“批次总览 + 每目录小节 + 统一验证结果”的结构，不能只记录其中一个目录。
5. 若子 agent 之间结论冲突，先保留可证实部分；冲突目录降级为 `needs_review` 或拆入下一批，不用不确定结论污染已确认索引。

## 5. 下一批候选

batch15-batch33 已完成 114 个 WKF/Warlock/Wizard/WSF/Mystic/Core/Tools 小目录。batch05-batch33 已按实际源码展开数修正执行范围：`core/wsf_util`、`wsf_p6dof`、`wsf_six_dof`、`tools/util_script`、`tools/utilqt`、`tools/wkf`、`core/sensor_plot_lib`、`core/wsf_cyber`、`core/wsf_mil`、`post_processor/lib`、`wsf_plugins/wsf_air_combat`、`wsf_plugins/wsf_argo8`、`wsf_plugins/wsf_multiresolution`、`tools/geodata`、`tools/artificer`、`tools/vespatk`、`core/wsf` 等虽在工作清单中显示为小计数，但按路径前缀可能覆盖较多 source/header，因此不得直接并入小批次。后续候选必须同时检查工作清单计数和实际 file-index 路径展开数。

按“文件少、边界清晰、优先核心源码”排序，下一批建议可继续作为一个多目录批次处理；实际执行时根据 CodeGraph 证据复杂度动态拆分：

| 优先级 | 最小目录单元 | source/header 数 | 说明 |
|--------|--------------|------------------|------|
| 1 | `afsim-2_9/swdev/src/wizard/plugins/PartManager/source` | 43 | Wizard part manager；执行前复核实际展开。 |
| 2 | `afsim-2_9/swdev/src/engage/source` | 45 | Engage 核心源码；交战业务高价值入口，建议单独或小批处理。 |
| 3 | `afsim-2_9/swdev/src/wsf_plugins/wsf_sosm/sosm/source` | 45 | SOSM 传感器/探测模型源码；业务价值高，执行前用 CodeGraph 深挖。 |
| 4 | `afsim-2_9/swdev/src/tools/packetio/source` | 48 | packet IO 工具；边界清晰。 |
| 5 | `afsim-2_9/swdev/src/mystic/lib/source` | 待复核 | Mystic 公共库；执行前必须计算实际展开。 |
| 6 | `afsim-2_9/swdev/src/tools/utilosg` | 待复核 | OSG 工具库；执行前必须按最小目录拆分。 |

建议 batch34 从上述候选中选择 3-6 个目录，但 `engage/source`、`wsf_sosm/sosm/source` 属高价值业务目录，若 CodeGraph 调用链复杂应主动缩小批次。`afsim-2_9/swdev/src/core/wsf` 已确认实际展开 1125 个 source/header，不能作为一个小批次目录处理，应另建拆分计划。

## 6. 已知注意事项

1. `workspace/source-index/symbol-index.jsonl` 是 Phase 3 精细索引，当前只修 Phase 2 粗索引 `symbol-index-phase2.jsonl`。Phase 3 后续应按新的 Phase 2 单元结果重跑或增量修正。
2. `compile_commands.json` 仍未生成，因此本阶段以 CodeGraph + 源码文本证据为主，AST/include path 精确性仍受限。
3. 旧 `module-overview.md` 中的 107 同层模块清单属于历史 Phase 2 视图，不再作为新的架构模块组织依据。
4. batch02 发现旧 Phase 3 精细索引中存在 `WsfGrammarCheckExtension` 成员被错误挂到 `ParseSourceProvider` 下的问题；本轮只修 Phase 2 粗索引，Phase 3 后续应按最小单元重新精修。
5. batch03 的 `MissionVersion.hpp` 只有版本/产品宏，无 class/struct；本轮将版本宏作为 Phase 3 macro-index 候选，而不是伪造类符号。
6. batch04 首次按“多个最小目录单元 + 子 agent 并行 + 主 agent 合并”执行；对共享 JSONL 仍由主 agent 串行写入，子 agent 只提供目录级证据摘要。
7. batch05 发现工作清单中部分 `analysis_unit` 与实际 file-index 路径展开不一致；后续批次选择必须先计算实际展开的 source/header 数，避免把大目录误当成小单元。
8. batch06 发现多个 Mystic 插件依赖 generated event-pipe headers 或 ResultData 插件；Phase 2 只记录显示/聚合入口，消息字段精确定义留给后续业务逻辑或 Phase 3/4 深挖。
9. batch07 进一步确认 Mystic 结果显示插件可作为后续 AFSIM 业务逻辑分析的消费侧入口：`ResultSituationAwarenessDisplay` 聚合 SA 飞行/导航/燃油/武器/航迹/感知/威胁/编组数据，`ResultInteractionLines` 消费 InteractionDb，`ResultRoute`/`ResultOrbit`/`ResultProjector`/`ResultVisualEffects` 分别消费航路、轨道、传感器视场和交战/外观事件。
10. batch08 进一步确认 Wizard 工具链中的编辑器/地图同步入口：`MapAnnotation` 连接 WSF proxy tree、WKF annotation display 和文本编辑器，是后续分析“场景文本如何驱动地图对象、地图编辑如何反写场景文本”的高价值入口；`SIMDIS`、`MysticLauncher`、`UnitConversion` 分别覆盖外部工具启动、文件类型动作和编辑器单位转换。
11. batch09 进一步确认三个后续业务逻辑入口：`WsfARGO8_Mover` 是武器交战 flyout 和 `WsfWeaponEngagement` 结果回写入口；`ResultDataAirCombat` 列出 11 类空战 `MsgSA_*` 结果消息；`ResultBattleManagement` 和 `ResultCommVis` 分别体现平台状态/aux data 与通信拓扑在 Mystic 中的消费方式。
12. batch10 进一步确认 Mystic data extension 的分流模式：annotation one-time 消息走 `rvEnv.AddAnnotationMessage`；cyber 生命周期写入 `InteractionDb`；P6DOF/SixDOF telemetry 写入 `ResultPlatform::mMessageMap`；space orbital elements 同时是 one-time/event；WK 仅 HUD_DATA 进入平台缓存，UserAction/ChatMessage 主要走事件表展示。
13. batch11 进一步确认 Mystic result consumer 的消费侧骨架：`ResultVaScenarioManager` 是 ResultDb/ResultPlatform 到 `VaScenario`/`wkf::Platform` 的场景同步前置；`ResultSensorVolumes`、`ResultWsfDraw`、`ResultZones` 分别消费平台 part/mode、`MsgDrawCommand`、zone one-time 消息并挂到 viewer/附件/UI；`ResultDetectionReport` 消费 `MsgDetectAttempt` 形成探测质量报表；`ResultQuantumTaskerData` 消费 ResultDb 全局 Quantum Tasker 矩阵。这些产物可作为下一步 AFSIM 业务逻辑分析中“结果消息最终如何被 UI 使用”的定位索引。
14. batch12 进一步区分 WKF/Warlock 工具层：`AdHocScriptBrowser` 是可触发仿真行为的开发者脚本入口；`ModelBrowser`、`TerrainTools` 是资源/地形能力的工具入口；`PositionConverterTool`、`UnitConverterTool`、`Log` 不应作为核心业务逻辑入口。
15. batch13 建立 annotation 生产链起点：`wsf_annotation` 解析 `visual_elements` 并输出 annotation event pipe 消息，可与 batch10 的 `ResultDataAnnotation` 和 batch11 的 `ResultZones` 串联；`ACOImporter`、`ScenarioImporter` 是 Wizard 侧导入生成工具，`ErrorList` 是诊断 UI。
16. batch14 补齐 Mystic result view：`ResultTracks` 是后续航迹业务语义分析的高价值入口，应沿 `TraceTrackId`、`TrackDb` ingestion 和 `MsgLocalTrack*`/`MsgSensorTrack*` 生产路径继续追；`ResultAuxData`、`ResultInteractionPlots`、`ResultSatelliteTether` 主要是消费侧展示入口。
17. batch15 补齐 Warlock 运行时显示/工具插件：`AcesDisplay`、`AirCombatVisualization`、`CommVis` 是空战、SA 和通信行为的显示观察入口；核心业务规则仍应向上追 `WsfSA_Processor`、weapon engagement、communication 生产方。
18. batch16 补齐 Warlock 事件/HUD/HDD/SA/interaction 桥接：`HeadDownView`、`Interactions`、`SituationAwarenessDisplay` 是高价值消费侧入口，可为下一步业务逻辑分析提供 SA、跨域事件和座舱显示字段的追踪起点。
19. batch17 补齐 Warlock visual effects 与 Wizard route/platform/log/demo 工具插件：`MapRoute` 是高价值 route/orbit 业务语义入口；`PlatformData` 与 `LogServer` 是平台字段和运行日志辅助入口；`ColorUtils`、`DemoBrowser` 主要是编辑器/示例工具。
20. batch18 补齐 runtime editing/scripting 相关入口：`wsf_sosm` 是高价值传感器探测业务入口；`PlatformBrowser` 是高价值平台删除 mutation 入口；`ScriptBrowser` 是高价值 Warlock 脚本执行入口；`ZoneEditor` 和 `wsf_mil_parser` 是配置/proxy 追踪入口；`profiling` 是性能基础设施。
21. batch19-batch21 补齐 Mystic 结果数据、WKF 工具和 Warlock runtime control/display 入口：`ResultStatistics::EventTableModel::data`、`CyberEngagementControllerCommand::Process`、`Projector::SimInterface::OnSensorUpdate`、`WkOrbit::SimInterface::OnSpaceMoverUpdate`、`WkBM::SimInterface::SimulationClockRead` 均是后续 AFSIM 业务逻辑分析的高价值入口。
22. batch22-batch24 补齐相对几何、draw overlay、CRD/OSM 导入、ARGO8、场景检查、Scoreboard、CreatePlatform、Orbital/P6DOF/SixDOF/PlatformData、ZoneBrowser、Wizard Platform/TypeBrowser、profiling 和 DemoMode。高价值入口包括 `Argo8Missile::Update`、`ScenarioAnalyzerRegisterScriptTypes`、`WkCreatePlatform::CreatePlatformCommand::Process`、`WkPlatformData::SimInterface::WallClockRead`、`WkZoneBrowser::SimInterface::InterpretZoneSet`。
23. batch25-batch27 补齐 NetworkLog、WeaponBrowser、CommandChainBrowser、tracking_filters、SensorController、SensorVolumes、TaskAssigner、TaskStatus、TrackDetailsDisplay、ProjectBrowser、Brawler、CyberEngagementBrowser、P6DOF_Tuner、TaskList、CoverageOverlay、Astrolabe、PlatformPartBrowser 和 SatelliteTether。高价值入口包括 `WkWeaponBrowser::FireCommand`、`WkSensorController::SlewToTrackCommand`、`WkSensorVolumes::VolumeUpdateEvent`、`WkTaskAssigner::AssignTaskCommand`、`BrawlerMover`、`WkTuner::WriteDataEvent`、`WkAstrolabe::VerifyMissionCommand`、`WkPlatformPartBrowser::ChangePartCommand`、`SatelliteTether::AddTrackCommand`。
24. `afsim-2_9/swdev/src/core/wsf` 已复核为 1125 个 source/header，必须按 `source/` 下业务域或文件组拆分，不能按工作清单中 12 的小计数直接标记完成。
25. batch28-batch33 补齐 SixDOF/Tracks/Prompt/Route/ScenarioAnalyzer/multiresolution、Result/Brawler/Joystick/Engage/PostProcessor、PlatformMovement、SimController、fires/RIPR/weapon_tools/CommVis、MTT/air combat/artificer/SPLAT/sensor_plot_lib 等 36 个目录。高价值入口包括 `WkTracks::Plugin::SetTrackState`、`PlatformMovementSimCommands`、`WkSimController::SimControllerEvent`、`weapon_tools`、`wkf::CommVisPacketGraphicsItem`、`WkCommVis::CommVisEvent`、`wsf_mtt`、`wsf_air_combat` 和 `sensor_plot_lib`。
26. 已复核并延期拆分的大目录包括 `core/wsf_parser`（158 个 source/header）、`wizard/plugins`（555）、`core/wsf_space`（329）和 `wsf_plugins/wsf_coverage`（118）；这些目录不得被小批次整体标记完成。
