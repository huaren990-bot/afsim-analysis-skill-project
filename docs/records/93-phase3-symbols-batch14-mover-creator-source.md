# Phase3 Batch14: mover_creator/source 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/mover_creator/source/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 303 |
| 覆盖文件 | 114 |
| CodeGraph 文件读取成功 | 114 |
| 新增 `symbol-index.jsonl` 条目 | 303 |
| 新增 `enum-index.jsonl` 条目 | 9 |
| 标记跳过 | 0 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个文件只读取一次。解析范围覆盖 mover creator 的 GUI widget、几何对象、气动表、推进数据、设置对话框、应用入口支撑类，以及 `Designer`、`Ui` 相关 namespace、class、struct、using 和 enum。所有 Phase2 粗符号均成功追溯并标记为 `done_batch14`。

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 303 条 `phase3:batch14` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 9 条 `phase3:batch14` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 303 条标记为 `done_batch14` |

