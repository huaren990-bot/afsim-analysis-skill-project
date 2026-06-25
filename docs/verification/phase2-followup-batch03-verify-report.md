# Phase 2 后续修正验证报告：batch03

> **日期**：2026-06-25
> **批次**：batch03
> **最小目录单元**：`afsim-2_9/swdev/src/mission/source`
> **验证对象**：`workspace/source-index/file-index.jsonl`、`workspace/source-index/symbol-index-phase2.jsonl`、`workspace/source-index/phase2-analysis-unit-worklist.jsonl`、`docs/architecture/module-overview-v2-incremental.md`

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | Phase 1/Phase 2 行数一致 | 通过 | `file-index.jsonl` 为 43,586 行，与 Phase 1 `file-classification.jsonl` 一致。 |
| 2 | 顶层 `src/*` 遗留清理 | 通过 | `file-index.jsonl` 中顶层 `src/*` 记录为 0。 |
| 3 | 最小目录工作清单 | 通过 | 工作清单共 237 个最小目录单元，已完成 3 个。 |
| 4 | batch03 文件索引 | 通过 | `mission.cpp` 与 `MissionVersion.hpp` 均标记 `analysis_status=phase2_v2_batch03_refined`。 |
| 5 | batch03 符号补充 | 通过 | 新增 `main(int,char**)` 和 6 个 Mission 版本/产品宏候选。 |
| 6 | 导出宏过滤 | 通过 | batch03 未引入 `_EXPORT`、`_IMPORT`、`_API`、`_LIB_EXPORT` 伪符号。 |
| 7 | Markdown 产物位置 | 通过 | 本批报告写入 `docs/verification/`，记录写入 `docs/records/`，未在 `workspace/` 下新增 `.md`。 |
| 8 | 证据可追溯 | 通过 | 使用 CodeGraph node 读取 `mission.cpp` 与 `MissionVersion.hpp`，关键结论均带源码行号。 |

## 关键统计

| 指标 | 值 |
|------|-----|
| `file-index.jsonl` 行数 | 43,586 |
| `file-index.jsonl` source/header 数 | 17,342 |
| `symbol-index-phase2.jsonl` 行数 | 13,948 |
| `phase2-analysis-unit-worklist.jsonl` 单元数 | 237 |
| 已完成单元数 | 3 |
| batch03 文件数 | 2 |
| batch03 粗符号数 | 7 |
| batch03 导出宏伪符号数 | 0 |

## batch03 修正细节

| 类型 | 修正 |
|------|------|
| 文件索引 | 为 `mission.cpp`、`MissionVersion.hpp` 补充 `system`、`subsystem`、`analysis_unit`、`analysis_status`、更准确的 `key_symbols`、`functions` 和中文 `brief`。 |
| 粗符号索引 | 新增 `main(int,char**)`，以及 `MISSION_VERSION_MAJOR`、`MISSION_VERSION_MINOR`、`MISSION_VERSION_PATCH`、`VER_FILEVERSION_STR`、`VER_PRODUCTVERSION_STR`、`VER_PRODUCTNAME_STR`。 |
| 模块概览 | 在 `module-overview-v2-incremental.md` 新增 `mission/source` 的职责、文件、核心符号、关键关系和修正记录。 |
| 计划清单 | 将 `phase2-analysis-unit-worklist.jsonl` 中该单元标记为 `done_batch03`，并将下一批候选顺延。 |

## 未覆盖项

本报告只验证 batch03，不声称 Phase 2 全量完成。剩余 234 个最小目录单元仍需逐步处理。

`MissionVersion.hpp` 只有版本/产品宏，没有 class/struct/function 定义；本批不伪造类符号，相关宏作为 Phase 3 macro-index 候选处理。

## 结论

batch03 通过。该批次补强了应用层入口目录的 Phase 2 粗索引，使 `mission` 从笼统文件名记录变为可追溯的应用启动流程和版本宏候选。
