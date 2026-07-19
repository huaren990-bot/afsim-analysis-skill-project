# Phase3 Batch13: tools/util 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/tools/util/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 309 |
| 覆盖文件 | 90 |
| CodeGraph 文件读取成功 | 90 |
| 新增 `symbol-index.jsonl` 条目 | 303 |
| 新增 `enum-index.jsonl` 条目 | 6 |
| 标记跳过 | 6 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个文件只读取一次。解析范围覆盖 util 基础类型、cloneable pointer、反射 visitor、attribute、string id、string util、logging stream 等 namespace、using、typedef、class、struct 和 enum。解析成功的 Phase2 粗符号标记为 `done_batch13`，无法对应真实 C++ class 声明的误分类候选标记为 `skipped_unresolved_phase2_symbol_batch13`。

## 跳过项

| 符号 | kind | 路径 | 原因 |
|---|---|---|---|
| `main` | class | `afsim-2_9/swdev/src/tools/util/test/main.cpp` | Phase2 将测试入口函数所在文件误归类为 class |
| `test_tbllookup` | class | `afsim-2_9/swdev/src/tools/util/test/test_tbllookup.cpp` | Phase2 将测试源文件名误归类为 class |
| `test_utalgorithm` | class | `afsim-2_9/swdev/src/tools/util/test/test_utalgorithm.cpp` | Phase2 将测试源文件名误归类为 class |
| `UtLogStream` | class | `afsim-2_9/swdev/src/tools/util/source/UtLogStream.cpp` | Phase2 将实现文件名误归类为 class；真实类为 `ut::log::MessageStream` |
| `UtStringUtil` | class | `afsim-2_9/swdev/src/tools/util/source/UtStringUtil.cpp` | Phase2 将 namespace 误归类为 class |
| `Parse` | class | `afsim-2_9/swdev/src/tools/util/source/UtStringUtil.hpp` | Phase2 将 free function 误归类为 class |

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 303 条 `phase3:batch13` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 6 条 `phase3:batch13` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 303 条标记为 `done_batch13`，6 条标记为 `skipped_unresolved_phase2_symbol_batch13` |

