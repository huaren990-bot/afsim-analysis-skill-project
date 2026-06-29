# Phase 2 follow-up batch06 验证报告

> **日期**：2026-06-29
> **批次范围**：6 个 Mystic 小插件最小目录单元
> **执行方式**：3 个子 agent 并行采集证据，主 agent 复核 CodeGraph/source 并统一合并 JSONL 与文档。

## 1. 批次范围

| # | 最小目录单元 | source/header 数 | 子系统 |
|---|--------------|------------------|--------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultAnnotation/source` | 2 | `mystic/plugins` |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultComment/source` | 2 | `mystic/plugins` |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultEngagementAnalysis/source` | 2 | `mystic/plugins` |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultEventMarker/source` | 2 | `mystic/plugins` |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultHeadDownView/source` | 2 | `mystic/plugins` |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultHeadUpView/source` | 2 | `mystic/plugins` |

## 2. 验证摘要

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Phase1/File-index 覆盖闭环 | 通过 | `file-index.jsonl` 保持 43,586 行；source/header 条目数保持 17,342。 |
| batch06 工作清单状态 | 通过 | 6 个目标单元均标记为 `done_batch06`，总完成单元数为 16/237。 |
| batch06 文件索引 | 通过 | 12 个 source/header 条目均补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions` 和中文 `brief`。 |
| batch06 粗符号索引 | 通过 | 本批目标路径下共有 85 条粗符号，覆盖 namespace、class、struct/using、macro invocation、constructor、method、function。 |
| 导出宏伪符号 | 通过 | 本批目标路径中 `*_EXPORT` 作为 `symbol_name` 的条目为 0；`WKF_PLUGIN_DEFINE_SYMBOLS` 仅作为插件注册宏调用记录。 |
| JSONL 可解析 | 通过 | `file-index.jsonl`、`symbol-index-phase2.jsonl`、`phase2-analysis-unit-worklist.jsonl` 均可逐行解析。 |
| 文档产物位置 | 通过 | 新增/更新 Markdown 均位于 `docs/`；`workspace` 下 Markdown 数为 0。 |

## 3. 按目录验证

| 最小目录单元 | 文件条目 | 粗符号条目 | 关键修正 |
|--------------|----------|------------|----------|
| `ResultAnnotation/source` | 2 | 9 | 补入 `RvAnnotation::Plugin`、annotation message 回调、deferred decoration/range-ring 处理和颜色/range-ring helper。 |
| `ResultComment/source` | 2 | 14 | 补入 `CommentData`、`FindCommentByIndex`、comment 读取、缓存、重绘、偏好变化和格式化逻辑。 |
| `ResultEngagementAnalysis/source` | 2 | 16 | 补入 weapon fired/terminated 聚合、统计窗口、filter replay、row context menu、trace event 和排序逻辑。 |
| `ResultEventMarker/source` | 2 | 9 | 补入内置/custom event marker 处理、时间窗口逻辑、位置推算和 extension event 注册。 |
| `ResultHeadDownView/source` | 2 | 17 | 补入 HDD 右键入口、窗口生命周期、ResultData 到 HDD 数据转换、GUI 推送和 SA 数据检测。 |
| `ResultHeadUpView/source` | 2 | 20 | 补入 HUD 右键入口、窗口生命周期、ResultData 到 HUD 数据转换、GUI 推送、初始化处理和 SA 数据检测。 |

## 4. 子 agent 交叉确认

| 子 agent 范围 | 结论 |
|---------------|------|
| `ResultAnnotation/source`、`ResultComment/source` | 与主 agent CodeGraph 证据一致；补充 generated event-pipe header 未在普通源码树展开、comment 替换边界等复核点。 |
| `ResultEngagementAnalysis/source`、`ResultEventMarker/source` | 与主 agent CodeGraph 证据一致；补充 target platform 空指针、trace 指针所有权、marker 原点回退等复核点。 |
| `ResultHeadDownView/source`、`ResultHeadUpView/source` | 与主 agent CodeGraph 证据一致；补充 build 依赖、sender 空指针顺序、单位转换和数据残留复核点。 |

## 5. 保留风险

| 风险 | 处理 |
|------|------|
| 多个插件依赖 generated event-pipe headers 或 ResultData data-extension 插件，消息字段定义未在本批源码中完整展开。 | 本批只记录显示/聚合入口和使用到的字段；消息 schema 留给 Phase 3/4 或后续业务逻辑分析。 |
| `RvPluginEngagement.cpp` 中 `tplat` 查询后检查变量疑似写成 `aplat`。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| `RvPluginEngagement.cpp::TraceEvent` 对 eventList 指针执行 `delete`，所有权需确认。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| `RvEventMarkerPlugin.cpp` DAMAGED/REMOVED 分支缺少显式平台空指针检查，`GetPositionAtTime` 找不到数据时返回原点。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| HeadDown/HeadUp 插件中 sender 使用顺序、未使用常量、单位转换或跨平台临时数据残留存在可复核点。 | 记录为 needs_review，不在 Phase2 修改源码。 |

## 6. 结论

batch06 通过。该批次按最小目录单元一次处理 6 个 Mystic 小插件目录，所有共享 JSONL 由主 agent 串行合并，子 agent 只提供只读证据摘要。批次产物可继续支撑 Phase 3/4 对 Mystic 结果显示插件的符号细化、函数级分析和后续业务逻辑梳理。
