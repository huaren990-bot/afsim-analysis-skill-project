# Phase 2 最小目录单元分析计划

> **日期**：2026-06-24
> **依据**：`workspace/project-boundary/project-boundary.json` 的 `analysis_boundaries` 与 `module_hierarchy`
> **目标**：面对大型 AFSIM C++ 源码，按目录树中的最小可验证源码单元逐步补强 Phase 2，而不是一次性重写全部模块。

## 1. 分析策略

Phase 2 后续分析按“系统 -> 子系统 -> 最小目录单元”推进：

| 层级 | 含义 | 示例 |
|------|------|------|
| 系统 | Phase 1 定义的主分析域 | `core_framework`、`plugin_modules`、`applications`、`developer_tools` |
| 子系统 | `swdev/src` 下的一级或二级职责目录 | `core/wsf_weapon_server`、`wsf_plugins/wsf_six_dof` |
| 最小目录单元 | 通常是含 `source/` 的最小源码目录；没有 `source/` 时使用可独立归属的最小源码目录 | `afsim-2_9/swdev/src/core/wsf_weapon_server/source` |

默认排除 `afsim-2_9/demos`、`afsim-2_9/documentation`、`afsim-2_9/training`、`afsim-2_9/resources` 的架构级模块分析。它们可作为场景、文档、训练或资源证据，但不进入 Phase 2 默认模块概览。

## 2. 工作清单

机器可读工作清单已生成：

`workspace/source-index/phase2-analysis-unit-worklist.jsonl`

当前统计：

| 指标 | 值 |
|------|-----|
| 最小目录单元数 | 237 |
| 默认范围内 source/header 数 | 17,179 |
| 已完成单元 | 2 |
| 当前完成单元 | `afsim-2_9/swdev/src/core/wsf_grammar_check/source` |

## 3. 批次规则

每个批次只处理少量最小目录单元，完成后必须更新：

1. `workspace/source-index/file-index.jsonl`：补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions`、中文 `brief`。
2. `workspace/source-index/symbol-index-phase2.jsonl`：修正该单元粗符号，过滤导出宏伪符号，保留真实 class/struct/enum/typedef。
3. `docs/architecture/module-overview-v2-incremental.md`：追加该单元的人类可读说明。
4. `docs/verification/phase2-followup-batchNN-verify-report.md`：验证该批次。
5. `docs/records/NN-phase2-...md`：记录批次处理结果。

## 4. 下一批候选

按“文件少、边界清晰、优先核心源码”排序，下一批建议：

| 优先级 | 最小目录单元 | source/header 数 | 说明 |
|--------|--------------|------------------|------|
| 1 | `afsim-2_9/swdev/src/mission/source` | 2 | 应用层任务入口，边界小。 |
| 2 | `afsim-2_9/swdev/src/wsf_plugins/wsf_simdis/source` | 2 | 插件层 SIMDIS 接口，边界小。 |
| 3 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer_iads_c2/source` | 2 | 插件层 IADS C2 场景分析接口。 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultAcesDisplay/source` | 2 | Mystic 结果显示插件，1 个 `.cpp` + 1 个 `.hpp`。 |

## 5. 已知注意事项

1. `workspace/source-index/symbol-index.jsonl` 是 Phase 3 精细索引，当前只修 Phase 2 粗索引 `symbol-index-phase2.jsonl`。Phase 3 后续应按新的 Phase 2 单元结果重跑或增量修正。
2. `compile_commands.json` 仍未生成，因此本阶段以 CodeGraph + 源码文本证据为主，AST/include path 精确性仍受限。
3. 旧 `module-overview.md` 中的 107 同层模块清单属于历史 Phase 2 视图，不再作为新的架构模块组织依据。
4. batch02 发现旧 Phase 3 精细索引中存在 `WsfGrammarCheckExtension` 成员被错误挂到 `ParseSourceProvider` 下的问题；本轮只修 Phase 2 粗索引，Phase 3 后续应按最小单元重新精修。
