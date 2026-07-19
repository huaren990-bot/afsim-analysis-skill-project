# Phase3 Batch18: tools/utilosg 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/tools/utilosg/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 233 |
| 覆盖文件 | 48 |
| CodeGraph 文件读取成功 | 48 |
| 新增 `symbol-index.jsonl` 条目 | 232 |
| 新增 `enum-index.jsonl` 条目 | 7 |
| 标记跳过 | 1 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个文件只读取一次。解析范围覆盖 utilosg 的 UTO 类型、terrain、viewer、map projection、OSG 支撑 class、struct、typedef、namespace、using、function 和 enum。函数指针 typedef 候选额外核对源码，`MakeProjectionFn`、`ColorTransFuncPtr`、`FARPROC` 已从 Phase2 片段归一为真实 typedef 条目。

## 跳过项

| 符号 | kind | 路径 | 原因 |
|---|---|---|---|
| `buf)` | typedef | `afsim-2_9/swdev/src/tools/utilosg/source/include/UtoTerrainImp.hpp` | Phase2 从 `ReadAttrFnPtr` 函数指针 typedef 的参数名中截出非法 typedef 片段 |

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 232 条 `phase3:batch18` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 7 条 `phase3:batch18` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 232 条标记为 `done_batch18`，1 条标记为 `skipped_unresolved_phase2_symbol_batch18` |

