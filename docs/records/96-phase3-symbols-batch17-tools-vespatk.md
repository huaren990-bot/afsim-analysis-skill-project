# Phase3 Batch17: tools/vespatk 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/tools/vespatk/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 243 |
| C++ 覆盖文件 | 74 |
| CMake 文件 | 4 |
| CodeGraph C++ 文件读取成功 | 74 |
| 新增 `symbol-index.jsonl` 条目 | 238 |
| 新增 `enum-index.jsonl` 条目 | 20 |
| 标记跳过 | 5 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个 C++ 文件只读取一次。解析范围覆盖 VESPA/VTK 工具的资源、显示、数据类型、结构体、typedef、using、namespace、class 和 enum。`cmake_function` 条目不是 C++ formal symbol，按 `skipped_invalid_phase2_symbol_batch17` 记录跳过。

## 跳过项

| 符号 | kind | 路径 | 原因 |
|---|---|---|---|
| `vtk_write_vcproj_user` | cmake_function | `afsim-2_9/swdev/src/tools/vespatk/cmake/config.cmake` | CMake function，不是 C++ formal symbol |
| `swdev_install_resources` | cmake_function | `afsim-2_9/swdev/src/tools/vespatk/cmake/install_resources.cmake` | CMake function，不是 C++ formal symbol |
| `install_maps` | cmake_function | `afsim-2_9/swdev/src/tools/vespatk/cmake/install_maps_models.cmake` | CMake function，不是 C++ formal symbol |
| `install_models` | cmake_function | `afsim-2_9/swdev/src/tools/vespatk/cmake/install_maps_models.cmake` | CMake function，不是 C++ formal symbol |
| `swdev_extract_resources` | cmake_function | `afsim-2_9/swdev/src/tools/vespatk/cmake/resources.cmake` | CMake function，不是 C++ formal symbol |

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 238 条 `phase3:batch17` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 20 条 `phase3:batch17` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 238 条标记为 `done_batch17`，5 条标记为 `skipped_invalid_phase2_symbol_batch17` |

