# Phase3 Batch15: wizard/plugins 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/wizard/plugins/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 295 |
| C++ 覆盖文件 | 124 |
| CMake 插件清单文件 | 3 |
| CodeGraph C++ 文件读取成功 | 124 |
| 新增 `symbol-index.jsonl` 条目 | 292 |
| 新增 `enum-index.jsonl` 条目 | 4 |
| 标记跳过 | 3 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个 C++ 文件只读取一次。解析范围覆盖 CRDImporter、MapUtils、DemoBrowser、ScenarioAnalyzer 等 Wizard 插件中的 class、struct、namespace、function、method、constructor、macro invocation、using 和 enum。`wizard_plugin.cmake` 中的 `cmake_plugin` 条目不是 C++ formal symbol，按 `skipped_invalid_phase2_symbol_batch15` 记录跳过。

`CRDImporter_main` 已归一到源码中的 `int main(int argc, char* argv[])`，并作为 `done_batch15` 写入精细符号索引。

## 跳过项

| 符号 | kind | 路径 | 原因 |
|---|---|---|---|
| `WizDemoBrowser_plugin` | cmake_plugin | `afsim-2_9/swdev/src/wizard/plugins/DemoBrowser/wizard_plugin.cmake` | CMake 插件清单，不是 C++ formal symbol |
| `WizCRDImporter_plugin` | cmake_plugin | `afsim-2_9/swdev/src/wizard/plugins/CRDImporter/wizard_plugin.cmake` | CMake 插件清单，不是 C++ formal symbol |
| `WizScenarioAnalyzer_plugin` | cmake_plugin | `afsim-2_9/swdev/src/wizard/plugins/ScenarioAnalyzer/wizard_plugin.cmake` | CMake 插件清单，不是 C++ formal symbol |

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 292 条 `phase3:batch15` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 4 条 `phase3:batch15` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 292 条标记为 `done_batch15`，3 条标记为 `skipped_invalid_phase2_symbol_batch15` |

