# Phase 2 follow-up batch07 验证报告

> **日期**：2026-07-03
> **批次范围**：6 个 Mystic 结果显示插件最小目录单元
> **执行方式**：3 个子 agent 并行采集证据，主 agent 复核 CodeGraph/source 并统一合并 JSONL 与文档。

## 1. 批次范围

| # | 最小目录单元 | source/header 数 | 子系统 |
|---|--------------|------------------|--------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultInteractionLines/source` | 2 | `mystic/plugins` |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultOrbit/source` | 2 | `mystic/plugins` |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultProjector/source` | 2 | `mystic/plugins` |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultRoute/source` | 2 | `mystic/plugins` |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultSituationAwarenessDisplay/source` | 2 | `mystic/plugins` |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultVisualEffects/source` | 2 | `mystic/plugins` |

## 2. 验证摘要

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Phase1/File-index 覆盖闭环 | 通过 | `file-index.jsonl` 保持 43,586 行。 |
| batch07 工作清单状态 | 通过 | 6 个目标单元均标记为 `done_batch07`，总完成单元数为 22/237。 |
| batch07 文件索引 | 通过 | 12 个 source/header 条目均补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions` 和中文 `brief`。 |
| batch07 粗符号索引 | 通过 | `symbol-index-phase2.jsonl` 共 14,199 行；本批目标路径下共有 84 条粗符号，覆盖 namespace、class、struct/using、macro invocation、function、method。 |
| 导出宏伪符号 | 通过 | 本批目标路径中 `*_EXPORT` 作为 `symbol_name` 的条目为 0；`WKF_PLUGIN_DEFINE_SYMBOLS` 仅作为插件注册宏调用记录。 |
| JSONL 可解析 | 通过 | `file-index.jsonl`、`symbol-index-phase2.jsonl`、`phase2-analysis-unit-worklist.jsonl` 均可逐行解析。 |
| 文档产物位置 | 通过 | 新增/更新 Markdown 均位于 `docs/`；`workspace` 下 Markdown 数为 0。 |

## 3. 按目录验证

| 最小目录单元 | 文件条目 | 粗符号条目 | 关键修正 |
|--------------|----------|------------|----------|
| `ResultInteractionLines/source` | 2 | 17 | 补入 InteractionDb、时间前进/回退、unpaired timeout、AttachmentInteraction 和 extension 类型注册链路。 |
| `ResultOrbit/source` | 2 | 10 | 补入 MsgOrbitalElements、AttachmentOrbit、message index 缓存、颜色模式和 epoch/moon orbit 关系。 |
| `ResultProjector/source` | 2 | 9 | 补入右键菜单筛选、sensor FOV/mode/articulation、terrain projector 生命周期和矩阵更新。 |
| `ResultRoute/source` | 2 | 19 | 补入 route option、MsgRouteChanged、relative waypoint 转换、AttachmentRoute 和 RouteDialog 联动。 |
| `ResultSituationAwarenessDisplay/source` | 2 | 13 | 补入 SA 飞行/导航/燃油/武器/航迹/感知/威胁/编组/truth 数据容器转换链路。 |
| `ResultVisualEffects/source` | 2 | 16 | 补入 appearance/weapon/status 事件输入、烟火/尾迹/爆炸效果映射、anchor entity 和时间回退逻辑。 |

## 4. 子 agent 交叉确认

| 子 agent 范围 | 结论 |
|---------------|------|
| `ResultInteractionLines/source`、`ResultOrbit/source` | 与主 agent CodeGraph 证据一致；补充 InteractionDb 字段、OrbitPluginBase 基类能力和空指针复核点。 |
| `ResultProjector/source`、`ResultRoute/source` | 与主 agent CodeGraph 证据一致；补充 terrain projector、route dialog、FOV 点数和 route map 语义复核点。 |
| `ResultSituationAwarenessDisplay/source`、`ResultVisualEffects/source` | 与主 agent CodeGraph 证据一致；补充 SA Display 基类分发、VisualEffectsDisplayInterface 生命周期和业务入口价值。 |

## 5. 保留风险

| 风险 | 处理 |
|------|------|
| 多个插件依赖 generated event-pipe headers 或 ResultData data-extension 插件，消息 schema 未在本批源码中完整展开。 | 本批记录显示/聚合入口和使用到的消息族；字段 schema 留给 Phase 3/4 或后续业务逻辑分析。 |
| `ResultProjector`、`ResultOrbit`、`ResultVisualEffects` 多处 `FindPlatform` / `FindPlatformByIndex` 返回值未显式判空。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| `ResultSituationAwarenessDisplay` 和 batch06 的 HUD/HDD 插件均出现 pitch/roll 单位转换疑点。 | 记录为跨插件复核项，后续业务逻辑分析或代码审查时集中确认。 |
| `ResultVisualEffects` smoke=3 移除分支、appearance 历史时间戳和武器爆炸位置查找存在边界语义。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| batch08 候选前方存在工作清单小计数但实际展开很大的 `tools/*` 目录。 | 已在计划中标注，需先细化边界再分析。 |

## 6. 结论

batch07 通过。该批次继续按最小目录单元处理 6 个 Mystic 结果显示插件目录，产物可支撑下一步从“结果显示消费侧”倒推 AFSIM 业务逻辑：SA Display、InteractionDb、Route、Orbit、Projector 和 VisualEffects 分别对应态势感知、平台交互、航路、轨道、传感器视场和交战/外观事件。
