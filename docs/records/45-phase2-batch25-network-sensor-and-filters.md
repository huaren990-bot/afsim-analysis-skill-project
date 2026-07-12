# Phase 2 完成记录：batch25 网络日志、武器/命令链、滤波与传感器插件

> **完成日期**：2026-07-10
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 结论 |
|------|------:|------|
| `warlock/plugins/NetworkLog/source` | 11 | Warlock 网络包日志、过滤和包字段查看入口。 |
| `warlock/plugins/WeaponBrowser/source` | 11 | Warlock 武器库存查看和 `FireCommand` 开火操作入口。 |
| `wizard/plugins/CommandChainBrowser/source` | 11 | Wizard 命令链树浏览、编辑和 proxy 定位入口。 |
| `tools/tracking_filters/source` | 12 | 通用航迹滤波算法库。 |
| `warlock/plugins/SensorController/source` | 12 | Warlock 传感器开关、slew 和 track 指向控制入口。 |
| `warlock/plugins/SensorVolumes/source` | 12 | 传感器/武器视场体显示、网络同步和 active list 查询入口。 |

`afsim-2_9/swdev/src/core/wsf` 在执行前复核时实际展开为 1125 个 source/header，已从本批移出并保留为待拆分单元。

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 只读取证 | 先用 CodeGraph 获取模块关系，再用源码扫描确认目录内真实符号。 |
| JSONL 合并 | 主 agent | 更新 `file-index.jsonl`、`symbol-index-phase2.jsonl`、`phase2-analysis-unit-worklist.jsonl`。 |
| 文档记录 | 主 agent | 追加模块概览与批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `NetworkLog` | 可用于追踪 Warlock 网络同步、Ping/Ack 和 packet schema 观察链路。 |
| `WeaponBrowser` | `WkWeaponBrowser::FireCommand` 是武器人工发射操作的入口。 |
| `CommandChainBrowser` | 可承接“场景文本 command_chain 如何映射到 Wizard 结构化编辑”的分析。 |
| `tracking_filters` | `TrackingFilters::KalmanFilter` 与 `OrbitDeterminationKalmanFilter` 是测量到航迹估计的算法入口。 |
| `SensorController` | `TurnOnCommand`、`SlewToAzElCommand`、`SlewToTrackCommand` 是传感器控制入口。 |
| `SensorVolumes` | `VolumeUpdateEvent` 与 `SensorVolumePacket` 是传感器视场可视化和网络同步入口。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch25-verify-report.md` |

## 已知问题

1. `core/wsf` 不能按工作清单的 12 个文件计数处理，后续必须按 `source/` 子目录或业务域拆分。
2. 本批只做 Phase 2 模块级粗粒度分析，`FireCommand::Process`、滤波数学细节和传感器 slew 执行语义留给 Phase 3/4。

## 下游就绪

本批新增的符号和目录职责可直接支撑后续武器控制、传感器控制、传感器视场、命令链配置和航迹滤波业务逻辑分析。
