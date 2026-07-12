# Phase 2 batch27 增量验证报告

> **验证日期**：2026-07-10
> **验证对象**：P6DOF_Tuner、TaskList、CoverageOverlay、Astrolabe、PlatformPartBrowser、SatelliteTether
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 6 个目录已标记为 `done_batch27`。 |
| file-index 覆盖 | 通过 | 82 个 source/header 均写入批次、系统、子系统和中文说明。 |
| 粗符号索引 | 通过 | 30 条代表性符号均来自目录边界内源码。 |
| 同名模块消歧 | 通过 | Warlock `Astrolabe/source` 与 Wizard `SpaceTools/source/Astrolabe` 已按路径区分。 |
| Markdown 位置 | 通过 | 本批报告位于 `docs/` 下。 |

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `P6DOF_Tuner` | `Gui2SimData`、`WriteDataEvent` |
| `CoverageOverlay` | `CoverageDataReader`、`HeatmapOverlay` |
| `Astrolabe` | `VerifyMissionCommand`、`InjectMissionSequenceCommand`、`MissionVerifier` |
| `PlatformPartBrowser` | `ChangePartCommand` |
| `SatelliteTether` | `AddTrackCommand`、`PropagationManager` |

## 已知风险

`P6DOF_Tuner` 是 deprecated 旧调参插件，且 `WriteDataEvent` 属于绕过新 SimEvent/SimCommand 架构的兼容实现；后续业务分析应优先与 SixDOF 链路对照。

`CoverageOverlay` 和 `SatelliteTether` 主要是结果/轨迹消费侧入口，业务规则需要继续向 `wsf_coverage`、space mover 和 orbital event 生产方追踪。
