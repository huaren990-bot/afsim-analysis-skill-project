# Phase 2 完成记录：batch27 P6DOF、任务列表、coverage、Astrolabe、平台部件与卫星 tether

> **完成日期**：2026-07-10
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 结论 |
|------|------:|------|
| `warlock/plugins/P6DOF_Tuner/source` | 13 | P6DOF 调参 UI、GUI/仿真数据交换和写回事件入口。 |
| `wizard/plugins/TaskList/source` | 13 | Wizard 解析任务/问题列表入口。 |
| `tools/wkf/plugins/CoverageOverlay/source` | 14 | coverage `.cvg` 文件读取和热力图叠加入口。 |
| `warlock/plugins/Astrolabe/source` | 14 | Warlock 轨道 mission sequence 验证、注入和创建入口。 |
| `warlock/plugins/PlatformPartBrowser/source` | 14 | 平台 part 列表、属性显示和变更入口。 |
| `warlock/plugins/SatelliteTether/source` | 14 | 卫星 tether 视图、传播器和轨迹事件入口。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 只读取证 | CodeGraph 命中 Wizard SpaceTools 同名 Astrolabe，最终以 Warlock 目录边界内源码为准。 |
| 目录内批量扫描 | 主 agent | 确认 class/struct/enum、注册宏和命令/事件处理入口。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块概览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `P6DOF_Tuner` | `Gui2SimData`、`WriteDataEvent` 和 auto-tune command 是飞行动力学调参入口。 |
| `TaskList` | 主要是 Wizard 编辑诊断入口，不等同于运行时任务业务。 |
| `CoverageOverlay` | `CoverageDataReader` 和 `HeatmapOverlay` 是 coverage 输出消费入口。 |
| `Astrolabe` | `VerifyMissionCommand`、`InjectMissionSequenceCommand`、`MissionVerifier` 是空间 mission sequence 入口。 |
| `PlatformPartBrowser` | `ChangePartCommand` 是平台部件属性修改入口。 |
| `SatelliteTether` | `AddTrackCommand`、`PropagationManager` 和 `SatelliteTetherEvent` 是卫星轨迹显示入口。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch27-verify-report.md` |

## 已知问题

1. `P6DOF_Tuner` 源码命名空间为 `WkTuner`，且插件描述标注 deprecated；后续优先与 SixDOF 调参链路对照。
2. `Astrolabe` 存在 Warlock 和 Wizard SpaceTools 同名路径，后续引用必须写完整路径。
3. `CoverageOverlay` 是消费侧工具，coverage 计算规则需要继续追 `wsf_plugins/wsf_coverage`。
4. `SatelliteTether` 与 Mystic/WKF tether 视图存在跨工具链消费关系，Phase 5/6 应补依赖链。

## 下游就绪

本批把 P6DOF 调参、空间 mission sequence、coverage 可视化、平台 part 变更和卫星 tether 轨迹纳入 Phase 2 入口索引，可支撑下一步业务逻辑分析。
