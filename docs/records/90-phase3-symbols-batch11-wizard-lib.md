# Phase3 Batch11: Wizard Lib 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/wizard/lib/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 424 |
| 覆盖文件 | 124 |
| CodeGraph 文件读取成功 | 124 |
| 新增 `symbol-index.jsonl` 条目 | 422 |
| 新增 `enum-index.jsonl` 条目 | 22 |
| 标记跳过 | 2 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个文件只读取一次。解析范围覆盖 `Us` 脚本上下文、核心解析数据结构、编辑器支撑类、UI 支撑类以及相关 namespace、using、typedef、class、struct 和 enum。解析成功的 Phase2 粗符号标记为 `done_batch11`，无法在源码中定位真实 C++ 声明的候选标记为 `skipped_unresolved_phase2_symbol_batch11`。

## 跳过项

| 符号 | kind | 路径 | 原因 |
|---|---|---|---|
| `WsfEditor` | class | `afsim-2_9/swdev/src/wizard/lib/source/editor/WsfEditor.cpp` | Phase2 将实现文件名误归类为 class，源码中无同名 class 声明 |
| `ParseResults` | class | `afsim-2_9/swdev/src/wizard/lib/source/core/ParseResults.cpp` | Phase2 将实现文件名误归类为 class，源码中无同名 class 声明 |

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 422 条 `phase3:batch11` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 22 条 `phase3:batch11` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 422 条标记为 `done_batch11`，2 条标记为 `skipped_unresolved_phase2_symbol_batch11` |

