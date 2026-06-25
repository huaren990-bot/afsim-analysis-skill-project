# Phase 2 后续修正验证报告：batch02

> **日期**：2026-06-25
> **批次**：batch02
> **最小目录单元**：`afsim-2_9/swdev/src/core/wsf_grammar_check/source`
> **验证对象**：`workspace/source-index/file-index.jsonl`、`workspace/source-index/symbol-index-phase2.jsonl`、`workspace/source-index/phase2-analysis-unit-worklist.jsonl`、`docs/architecture/module-overview-v2-incremental.md`

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | Phase 1/Phase 2 行数一致 | 通过 | `file-index.jsonl` 为 43,586 行，与 Phase 1 `file-classification.jsonl` 一致。 |
| 2 | 顶层 `src/*` 遗留清理 | 通过 | `file-index.jsonl` 中顶层 `src/*` 记录为 0。 |
| 3 | 最小目录工作清单 | 通过 | 工作清单共 237 个最小目录单元，已完成 2 个。 |
| 4 | batch02 文件索引 | 通过 | `WsfGrammarCheck.hpp` 与 `WsfGrammarCheck.cpp` 均标记 `analysis_status=phase2_v2_batch02_refined`。 |
| 5 | batch02 符号修正 | 通过 | 旧索引仅有 `ParseSourceProvider`；现补入 `WsfGrammarCheckExtension`、`ParseSourceProvider`、`Register_wsf_grammar_check`、`(anonymous namespace)::GetLineNumber`。 |
| 6 | 导出宏过滤 | 通过 | `WSF_GRAMMAR_CHECK_EXPORT` 只保留在 `signature` 中，未作为 `symbol_name/qualified_name`。 |
| 7 | Markdown 产物位置 | 通过 | `workspace/` 下 `.md` 文件数为 0；本批报告写入 `docs/verification/`。 |
| 8 | 证据可追溯 | 通过 | 使用 CodeGraph node 读取 `WsfGrammarCheck.hpp/.cpp`，关键结论均带源码行号。 |

## 关键统计

| 指标 | 值 |
|------|-----|
| `file-index.jsonl` 行数 | 43,586 |
| `file-index.jsonl` source/header 数 | 17,342 |
| `symbol-index-phase2.jsonl` 行数 | 13,941 |
| `phase2-analysis-unit-worklist.jsonl` 单元数 | 237 |
| 已完成单元数 | 2 |
| batch02 文件数 | 2 |
| batch02 粗符号数 | 4 |
| batch02 导出宏伪符号数 | 0 |

## batch02 修正细节

| 类型 | 修正 |
|------|------|
| 文件索引 | 为 `WsfGrammarCheck.hpp`、`WsfGrammarCheck.cpp` 补充 `system`、`subsystem`、`analysis_unit`、`analysis_status`、更准确的 `key_symbols`、`functions` 和中文 `brief`。 |
| 粗符号索引 | 将旧的单条 `ParseSourceProvider` 粗符号替换为 2 个类和 2 个函数候选。 |
| 模块概览 | 在 `module-overview-v2-incremental.md` 新增 `core/wsf_grammar_check/source` 的职责、文件、核心符号、关键关系和修正记录。 |
| 计划清单 | 将 `phase2-analysis-unit-worklist.jsonl` 中该单元标记为 `done_batch02`，并将下一批候选顺延。 |

## 未覆盖项

本报告只验证 batch02，不声称 Phase 2 全量完成。剩余 235 个最小目录单元仍需逐步处理。

另：旧 Phase 3 精细索引中曾出现 `WsfGrammarCheckExtension` 成员被错误归属到 `ParseSourceProvider` 的问题；本批仅修 Phase 2 粗索引，Phase 3 后续应按本批证据增量修正。

## 结论

batch02 通过。当前按最小目录单元推进的方式能够发现并修正旧索引中的漏记、误归属和导出宏风险，适合继续用于后续 Phase 2 补强。
