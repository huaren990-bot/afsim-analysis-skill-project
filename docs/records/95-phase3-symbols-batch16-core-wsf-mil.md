# Phase3 Batch16: core/wsf_mil 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/core/wsf_mil/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 250 |
| 覆盖文件 | 32 |
| CodeGraph 文件读取成功 | 32 |
| 新增 `symbol-index.jsonl` 条目 | 247 |
| 新增 `enum-index.jsonl` 条目 | 13 |
| 标记跳过 | 3 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个文件只读取一次。解析范围覆盖 MIL 接口、对象、任务、光学路径、track classifier 等 namespace、class、struct、using 和 enum。解析成功的 Phase2 粗符号标记为 `done_batch16`，测试文件名误分类候选标记为 `skipped_unresolved_phase2_symbol_batch16`。

## 跳过项

| 符号 | kind | 路径 | 原因 |
|---|---|---|---|
| `main` | class | `afsim-2_9/swdev/src/core/wsf_mil/test/main.cpp` | Phase2 将测试入口函数所在文件误归类为 class |
| `test_wsfopticalpath` | class | `afsim-2_9/swdev/src/core/wsf_mil/test/test_wsfopticalpath.cpp` | Phase2 将测试源文件名误归类为 class |
| `test_wsftrackclassifier` | class | `afsim-2_9/swdev/src/core/wsf_mil/test/test_wsftrackclassifier.cpp` | Phase2 将测试源文件名误归类为 class |

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 247 条 `phase3:batch16` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 13 条 `phase3:batch16` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 247 条标记为 `done_batch16`，3 条标记为 `skipped_unresolved_phase2_symbol_batch16` |

