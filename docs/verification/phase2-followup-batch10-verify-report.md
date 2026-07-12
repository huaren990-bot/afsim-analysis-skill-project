# Phase 2 follow-up batch10 验证报告

> **日期**：2026-07-05
> **批次范围**：6 个 Mystic result data extension 最小目录单元
> **执行方式**：3 个子 agent 并行采集证据，主 agent 复核 CodeGraph/source 并统一合并 JSONL 与文档。

## 1. 批次范围

| # | 最小目录单元 | source/header 数 | 子系统 |
|---|--------------|------------------|--------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataAnnotation/source` | 4 | `mystic/plugins` |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataCyber/source` | 4 | `mystic/plugins` |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataP6Dof/source` | 4 | `mystic/plugins` |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataSixDOF/source` | 4 | `mystic/plugins` |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataSpace/source` | 4 | `mystic/plugins` |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataWk/source` | 4 | `mystic/plugins` |

## 2. 验证摘要

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Phase1/File-index 覆盖闭环 | 通过 | `file-index.jsonl` 保持 43,586 行。 |
| batch10 工作清单状态 | 通过 | 6 个目标单元均标记为 `done_batch10`，总完成单元数为 40/237。 |
| batch10 文件索引 | 通过 | 24 个 source/header 条目均补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions` 和中文 `brief`。 |
| batch10 粗符号索引 | 通过 | 本批目标路径下共有 115 条粗符号。 |
| 导出宏伪符号 | 通过 | 本批目标路径中 `*_EXPORT` 作为 `symbol_name` 的条目为 0；`WKF_PLUGIN_DEFINE_SYMBOLS` 仅作为插件注册宏调用记录。 |
| JSONL 可解析 | 通过 | `file-index.jsonl`、`symbol-index-phase2.jsonl`、`phase2-analysis-unit-worklist.jsonl` 均可逐行解析。 |
| 文档产物位置 | 通过 | 新增/更新 Markdown 均位于 `docs/`；`workspace` 下 Markdown 数为 0。 |

## 3. 按目录验证

| 最小目录单元 | 文件条目 | 粗符号条目 | 关键修正 |
|--------------|----------|------------|----------|
| `ResultDataAnnotation/source` | 4 | 16 | 补入 annotation serializer/schema、one-time 非 event 分流、`rvEnv.AddAnnotationMessage` 和 decoration/POI/range-ring 字段。 |
| `ResultDataCyber/source` | 4 | 24 | 补入 11 类 Cyber 消息、InteractionDb paired/unpaired 写入/移除、state card 和 interaction metadata。 |
| `ResultDataP6Dof/source` | 4 | 21 | 补入 P6DOF telemetry 8 类消息、ResultPlatform 模板写入和已 deprecated 迁移关系。 |
| `ResultDataSixDOF/source` | 4 | 21 | 补入 SixDOF telemetry 8 类消息、ResultPlatform 模板写入和当前主路径。 |
| `ResultDataSpace/source` | 4 | 17 | 补入 `MsgOrbitalElements` one-time/event 双重身份、平台缓存和 `OrbitEventHandler`。 |
| `ResultDataWk/source` | 4 | 16 | 补入 UserAction/HUD_Data/ChatMessage 分流，HUD_DATA 平台缓存和事件表展示字段。 |

## 4. 子 agent 交叉确认

| 子 agent 范围 | 结论 |
|---------------|------|
| `ResultDataAnnotation/source`、`ResultDataCyber/source` | 与主 agent CodeGraph 证据一致；补充 annotation one-time 路径和 Cyber add/remove 对称性复核点。 |
| `ResultDataP6Dof/source`、`ResultDataSixDOF/source` | 与主 agent CodeGraph 证据一致；补充 P6DOF deprecated、SixDOF 优先和 ControlSurfaces 展示缺口。 |
| `ResultDataSpace/source`、`ResultDataWk/source` | 与主 agent CodeGraph 证据一致；补充 orbit event handler、HUD_DATA 平台缓存和 UserAction/Chat 二级索引缺口。 |

## 5. 保留风险

| 风险 | 处理 |
|------|------|
| `ResultDataAnnotation` 的 RangeRing `lat/lon` 未展示，`alignPlatform` 反向显示为 align north。 | 记录为 needs_review。 |
| `ResultDataCyber` 的 `CyberImmune` add/remove 条件不一致，镜像写入与删除对称性需确认。 | 记录为 needs_review，是 Cyber 交互线分析重点。 |
| P6DOF 已 deprecated，但仍保留数据扩展；后续业务分析优先跟 SixDOF。 | 记录为迁移/兼容关系。 |
| P6DOF/SixDOF 的 ControlSurfaces 消息可入库但无 generic event list handler。 | 记录为 needs_review；专用 UI 可能另行读取变长字段。 |
| Space `MsgOrbitalElements` 的 `resultOfManeuver` 未在事件表展示，缺实体状态时事件位置退化为 `(0,0,0)`。 | 记录为 needs_review。 |
| WK 的 HUD mode 不在事件表展示，UserAction/ChatMessage 无二级索引。 | 记录为 needs_review。 |

## 6. 结论

batch10 通过。该批次补强了 Mystic result data extension 的核心数据入口，明确了 annotation、cyber、P6DOF/SixDOF、space、Warlock/WK 消息从 event pipe 进入 `rvEnv`、`ResultPlatform` 或 `InteractionDb` 的分流方式。产物可支撑后续从结果数据入口反查 AFSIM 业务逻辑生产端。
