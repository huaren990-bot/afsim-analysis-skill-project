# Phase 2 batch25 增量验证报告

> **验证日期**：2026-07-10
> **验证对象**：NetworkLog、WeaponBrowser、CommandChainBrowser、tracking_filters、SensorController、SensorVolumes
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 6 个目录均来自 `phase2-analysis-unit-worklist.jsonl`，`core/wsf` 未被误标完成。 |
| file-index 覆盖 | 通过 | 69 个 source/header 均写入 `analysis_unit`、`batch`、`system`、`subsystem` 和中文 `brief`。 |
| 粗符号索引 | 通过 | 每目录 5 个代表性真实符号，共 30 条，均有 `declaration_path` 和中文说明。 |
| 导出宏过滤 | 通过 | 未把 `TRACKING_FILTERS_EXPORT` 等导出宏作为符号写入。 |
| Markdown 位置 | 通过 | 本批 Markdown 均位于 `docs/records` 或 `docs/verification`。 |

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `WeaponBrowser` | `WkWeaponBrowser::FireCommand` |
| `SensorController` | `WkSensorController::TurnOnCommand`、`SlewToAzElCommand`、`SlewToTrackCommand` |
| `SensorVolumes` | `WkSensorVolumes::VolumeUpdateEvent`、`SensorVolumePacket` |
| `tracking_filters` | `TrackingFilters::KalmanFilter`、`OrbitDeterminationKalmanFilter` |

## 已知风险

`core/wsf` 实际展开为 1125 个 source/header，已作为待拆分项保留；若后续强行按当前工作清单计数合并，会造成覆盖率虚高。
