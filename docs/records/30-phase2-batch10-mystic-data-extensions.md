# Phase 2 batch10 Mystic 数据扩展处理记录

> **日期**：2026-07-05
> **目标**：继续按最小目录单元推进 Phase2，集中补强 Mystic result data extension 链路。

## 1. 本批范围

| # | 最小目录单元 | 系统 | 子系统 | source/header 数 |
|---|--------------|------|--------|------------------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataAnnotation/source` | `applications` | `mystic/plugins` | 4 |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataCyber/source` | `applications` | `mystic/plugins` | 4 |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataP6Dof/source` | `applications` | `mystic/plugins` | 4 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataSixDOF/source` | `applications` | `mystic/plugins` | 4 |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataSpace/source` | `applications` | `mystic/plugins` | 4 |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataWk/source` | `applications` | `mystic/plugins` | 4 |

## 2. 执行方式

| 角色 | 工作 |
|------|------|
| 子 agent 1 | 只读分析 `ResultDataAnnotation/source`、`ResultDataCyber/source`，输出 one-time annotation 分流和 Cyber InteractionDb 链路。 |
| 子 agent 2 | 只读分析 `ResultDataP6Dof/source`、`ResultDataSixDOF/source`，输出 P6DOF/SixDOF telemetry 差异和迁移关系。 |
| 子 agent 3 | 只读分析 `ResultDataSpace/source`、`ResultDataWk/source`，输出 orbit event handler、HUD/UserAction/Chat 分流。 |
| 主 agent | 使用 CodeGraph 复核 24 个 source/header 文件，串行合并 JSONL、模块概览、计划和验证报告。 |

## 3. 修改产物

| 产物 | 处理 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 精修 24 个 source/header 条目，补充最小目录单元、系统、子系统、关键符号、函数和中文职责。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 替换本批目标目录旧 auto-extracted 粗符号，新增 115 条可追溯粗符号；插件注册宏仅保留为 metadata。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 6 个目标单元标记为 `done_batch10`，总完成数达到 40/237。 |
| `docs/architecture/module-overview-v2-incremental.md` | 追加第 35-40 节，并修正顶部总览表。 |
| `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` | 更新完成数、当前完成批次、batch11 候选和 batch10 注意事项。 |
| `docs/verification/phase2-followup-batch10-verify-report.md` | 新增本批验证报告。 |

## 4. 关键发现

| 目录 | 发现 |
|------|------|
| `ResultDataAnnotation/source` | Annotation 消息是 one-time、非 event；不进入平台缓存，而是经 `rvEnv.AddAnnotationMessage` 发 `AnnotationRead`。 |
| `ResultDataCyber/source` | Cyber attack/scan 生命周期写入 `InteractionDb`，并提供 Cyber state card 与 interaction metadata。 |
| `ResultDataP6Dof/source` | P6DOF telemetry 已被 SixDOF 替代，仍保留兼容数据入口。 |
| `ResultDataSixDOF/source` | 当前 SixDOF telemetry 主入口，将 8 类飞行动力学消息写入 `ResultPlatform`。 |
| `ResultDataSpace/source` | `MsgOrbitalElements` 同时是 one-time 与 event message，挂平台缓存并提供 orbit event handler。 |
| `ResultDataWk/source` | 仅 HUD_DATA 进入平台缓存；UserAction/ChatMessage 主要走事件表展示。 |

## 5. 验证结果

| 指标 | 值 |
|------|-----|
| batch10 source/header 文件条目 | 24 |
| batch10 粗符号条目 | 115 |
| batch10 导出宏伪符号 | 0 |
| 已完成最小目录单元 | 40 / 237 |
| 剩余 pending 单元 | 197 |
| `workspace` 下 Markdown | 0 |

## 6. 后续建议

batch11 建议继续处理实际展开为 4 个 source/header 的剩余小型 Mystic/WKF 目录，优先 `ResultDetectionReport/source`、`ResultQuantumTaskerData/source`、`ResultSensorVolumes/source`、`ResultVaScenarioManager/source`、`ResultWsfDraw/source`、`ResultZones/source`。这些目录与 batch10 的 data extension 链路相邻，可继续补强“结果数据如何被显示/消费”的业务逻辑入口。
