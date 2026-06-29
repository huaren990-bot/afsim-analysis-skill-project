# Phase 2 follow-up batch05 验证报告

> **日期**：2026-06-28
> **批次范围**：3 个最小目录单元
> **执行方式**：子 agent 逐目录采集证据，主 agent 复核 CodeGraph/source 并统一合并 JSONL 与文档。

## 1. 批次范围

| # | 最小目录单元 | source/header 数 | 子系统 |
|---|--------------|------------------|--------|
| 1 | `afsim-2_9/swdev/src/core/wsf_parser/legacy_test/source` | 1 | `core/wsf_parser` |
| 2 | `afsim-2_9/swdev/src/mystic/exec/source` | 1 | `mystic/exec` |
| 3 | `afsim-2_9/swdev/src/post_processor/exec/source` | 1 | `post_processor/exec` |

## 2. 验证摘要

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Phase1/File-index 覆盖闭环 | 通过 | Phase1 `file-classification.jsonl` 43,586 行；`file-index.jsonl` 43,586 行；source/header 均为 17,342。 |
| batch05 工作清单状态 | 通过 | 3 个目标单元均标记为 `done_batch05`，总完成单元数为 10/237。 |
| batch05 文件索引 | 通过 | 3 个 source 条目均补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions` 和中文 `brief`。 |
| batch05 粗符号索引 | 通过 | 本批目标路径下共有 12 条粗符号，覆盖 class、method、function。 |
| 导出宏伪符号 | 通过 | 本批目标路径中 `*_EXPORT` 作为 `symbol_name` 的条目为 0。 |
| 文档产物位置 | 通过 | 新增/更新 Markdown 均位于 `docs/`；`workspace` 下 Markdown 数为 0。 |

## 3. 按目录验证

| 最小目录单元 | 文件条目 | 粗符号条目 | 关键修正 |
|--------------|----------|------------|----------|
| `core/wsf_parser/legacy_test/source` | 1 | 6 | 补入 `ParseSourceProvider`、`FindSource`、`GetLineNumber`、`CheckFile`、`PrintInclude` 和测试入口 `main`。 |
| `mystic/exec/source` | 1 | 5 | 补入 `main`、`rvExecute` 和匿名命名空间 helper，记录 Mystic GUI 环境创建和 event recording 打开流程。 |
| `post_processor/exec/source` | 1 | 1 | 补入 CLI 入口 `main`，记录 `Configuration::Execute` 报表生成调用链起点。 |

## 4. 候选修正说明

batch05 原计划候选中 `core/wsf_util`、`wsf_p6dof`、`wsf_six_dof` 在工作清单中显示为小计数，但按 `file-index.jsonl` 路径前缀实际会展开为大量 source/header 文件。为保证正确性，本批未处理这些目录，并已在 plan 中要求后续批次选择前同时检查工作清单计数和实际路径展开数。

## 5. 保留风险

| 风险 | 处理 |
|------|------|
| `wsf_core_parse_test.cpp` 使用 `std::vector`、`std::string` 但未直接 include 对应标准头。 | 记录为 include hygiene 复核项，不在 Phase2 修改源码。 |
| `mystic.cpp` 中 Windows helper `associateFileTypes` 未发现调用。 | 记录为行为复核项，不影响入口索引。 |
| `mystic_version_defines.hpp`、`post_processor_version_defines.hpp` 未在源码树中找到。 | 按构建生成头处理，不把版本宏写入本批粗符号索引。 |

## 6. 结论

batch05 通过。该批次处理 3 个真实小目录，并修正了后续批次选择规则：不能只看工作清单计数，必须复核实际路径展开的 source/header 数。
