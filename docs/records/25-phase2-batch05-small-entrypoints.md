# Phase 2 batch05 小入口目录处理记录

> **日期**：2026-06-28
> **目标**：继续按 `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` 推进 Phase2，并在执行前复核候选目录的实际源码展开数。

## 1. 本批范围

| # | 最小目录单元 | 系统 | 子系统 | 文件数 |
|---|--------------|------|--------|--------|
| 1 | `afsim-2_9/swdev/src/core/wsf_parser/legacy_test/source` | `core_framework` | `core/wsf_parser` | 1 |
| 2 | `afsim-2_9/swdev/src/mystic/exec/source` | `applications` | `mystic/exec` | 1 |
| 3 | `afsim-2_9/swdev/src/post_processor/exec/source` | `applications` | `post_processor/exec` | 1 |

## 2. 执行方式

| 角色 | 工作 |
|------|------|
| 子 agent | 分别负责一个最小目录单元，只读取 CodeGraph/source，输出文件职责、关键符号、入口流程、跨模块证据和风险项。 |
| 主 agent | 复核源码行号和生成头风险，串行合并 `file-index.jsonl`、`symbol-index-phase2.jsonl`、模块概览、计划和验证报告。 |

## 3. 候选调整

本批未纳入 `core/wsf_util`、`wsf_p6dof`、`wsf_six_dof`。原因是这些 `analysis_unit` 在工作清单中显示为小计数，但按 `file-index.jsonl` 路径前缀实际展开后会覆盖大量 source/header 文件，不符合 batch05 的“小目录多并行”前提。

后续批次选择必须先计算实际路径展开数，再决定是否并行合批。

## 4. 修改产物

| 产物 | 处理 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 精修 3 个 source 条目，补充 `analysis_unit`、`system`、`subsystem`、关键符号、函数和中文职责。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 新增本批 12 条可追溯符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 3 个目标单元标记为 `done_batch05`，总完成数达到 10。 |
| `docs/architecture/module-overview-v2-incremental.md` | 追加第 8-10 节，分别描述 3 个最小目录单元。 |
| `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` | 更新完成数、当前完成批次、batch06 候选和候选选择注意事项。 |
| `docs/verification/phase2-followup-batch05-verify-report.md` | 新增本批验证报告。 |

## 5. 关键发现

| 目录 | 发现 |
|------|------|
| `core/wsf_parser/legacy_test/source` | 旧索引无粗符号；本批补入 parser 测试本地 provider、错误行号计算、文件检查、include tracing 和测试入口。 |
| `mystic/exec/source` | 旧索引只有泛化 `mystic`；本批补入 `main`、`rvExecute` 和匿名 helper，记录 WKF/VTK/RV 环境创建流程。 |
| `post_processor/exec/source` | 旧索引只有泛化 `post_processor`；本批补入 CLI 入口 `main` 和 `Configuration::Execute` 调用链起点。 |

## 6. 验证结果

| 指标 | 值 |
|------|-----|
| Phase1 文件行数 | 43,586 |
| file-index 行数 | 43,586 |
| source/header 覆盖一致 | 是，均为 17,342 |
| symbol-index-phase2 行数 | 14,067 |
| batch05 文件条目 | 3 |
| batch05 粗符号条目 | 12 |
| batch05 导出宏伪符号 | 0 |
| 已完成最小目录单元 | 10 / 237 |
| `workspace` 下 Markdown | 0 |

## 7. 后续建议

batch06 可优先处理 Mystic 下多个 2 文件小插件目录，例如 `ResultAnnotation/source`、`ResultComment/source`、`ResultEngagementAnalysis/source`、`ResultEventMarker/source`、`ResultHeadDownView/source`、`ResultHeadUpView/source`。开始前仍需复核每个候选的实际路径展开数。
