# Phase 2 batch11 Mystic Result Consumers

> 日期：2026-07-05
> 范围：6 个最小目录单元，24 个 source/header 文件
> 方法：主 agent 选批与合并，3 个子 agent 并行采集证据；所有目录先使用 CodeGraph，再按需读取源码行号。

## 1. 批次范围

| # | 最小目录单元 | source/header | 定位 |
|---|--------------|---------------|------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultDetectionReport/source` | 4 | `MsgDetectAttempt` 探测质量报表消费端 |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultQuantumTaskerData/source` | 4 | Quantum Tasker 全局矩阵 UI 消费端 |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultSensorVolumes/source` | 4 | sensor/jammer volume 和 boresight 可视化消费端 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultVaScenarioManager/source` | 4 | ResultPlatform 到 `VaScenario` 的场景同步前置 |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultWsfDraw/source` | 4 | `MsgDrawCommand` 到 WKF overlay 的消费端 |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultZones/source` | 4 | zone one-time 消息到 WKF ZoneBrowser 的消费端 |

## 2. 关键结论

batch11 与 batch10 的性质不同：batch10 主要是 data extension 写入/分流，batch11 主要是结果消费和 UI 场景还原。

| 单元 | 业务链路价值 | 核心消费链 |
|------|--------------|------------|
| DetectionReport | 传感器探测判定质量分析入口 | `WsfEventPipeInterface::SensorDetectionAttempt -> MsgDetectAttempt -> ResultPlatform::mDetectionAttemptMap -> SensorDetectionModel::data()` |
| QuantumTaskerData | 任务分配/资源选择矩阵查看入口 | `WsfQuantumTaskerProcessor -> WsfMilEventPipe::QuantumTaskerUpdate -> MsgQuantumTaskerUpdate -> ResultDb::Push -> Dialog::UpdateTable()` |
| SensorVolumes | 传感器/干扰机体积显示入口 | `ResultPlatform parts/modes/articulation -> PlatformVolumes::UpdateAndUnmark -> wkf::AttachmentSensorVolume` |
| VaScenarioManager | 多数 Mystic 可视化插件的场景基础 | `ResultPlatform status/entity/visual parts -> Interface::GuiUpdate -> wkf::Platform/subobject` |
| WsfDraw | draw 命令落地图层入口 | `MsgDrawCommand -> rvEnv.DrawCommandRead -> Interface::DrawViewerCommand -> wkf::OverlayWsfDraw` |
| Zones | zone 定义落图入口 | `Msg*Zone/MsgZoneSet -> rvEnv.ZoneRead -> wkf::ZoneSetData -> ZoneBrowserDockWidget` |

## 3. 已更新产物

| 产物 | 更新 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 为 24 个 source/header 补入 `analysis_unit`、`system`、`subsystem`、职责说明、关键符号和关键函数。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 删除本批旧粗符号，新增 109 个经源码/CodeGraph 确认的符号；过滤 `*_EXPORT`，插件宏只作为元数据说明。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 将 6 个目录标记为 `done_batch11`。 |
| `docs/architecture/module-overview-v2-incremental.md` | 新增第 41-46 节。 |
| `docs/verification/phase2-followup-batch11-verify-report.md` | 新增本批验证报告。 |
| `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` | 已完成数更新为 46/237，并给出 batch12 候选。 |

## 4. 保留复核项

| 单元 | 复核项 |
|------|--------|
| DetectionReport | `BuildEntityContextMenu()` 未显式 `addAction`；`SetCacheRange()` 空数据时直接解引用 `mArray`。 |
| QuantumTaskerData | `MsgQuantumTaskerUpdate` 未见 Pop 清理；首个矩阵时间为 `0.0` 可能首次不刷新；Tools 菜单空 action 列表需确认。 |
| SensorVolumes | `statusMsg->on()` 缺空指针保护；赤道 FOV 路径可能解引用空 articulation；依赖 Scenario Manager 先建平台实体。 |
| VaScenarioManager | `FindPlatform` 空结果后续可能被解引用；`ClearScenario()` 未显式加锁；visual part 同时刻变更可能被 dirty/read-time 逻辑吞掉。 |
| WsfDraw | deferred command try_lock/lock 时序需验证；相对平台 placeholder 生命周期需确认；non-standard viewer layer 默认不可见。 |
| Zones | `ClearScenario()` 未清 `mPlatformZoneData`；`ZoneRead()` 依赖 message id 与实际类型一致；reference platform delayed redraw 需结合回退验证。 |

## 5. 下一步建议

batch12 可处理 6 个实际展开为 4 个 source/header 的 WKF/Warlock 工具插件目录：`ModelBrowser`、`PositionConverterTool`、`TerrainTools`、`UnitConverterTool`、`AdHocScriptBrowser`、`Log`。该批应重点区分“开发/编辑工具入口”和“仿真业务逻辑入口”，避免把纯 UI 工具误归入仿真业务核心。
