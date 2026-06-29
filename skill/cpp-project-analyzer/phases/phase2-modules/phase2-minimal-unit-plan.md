# Phase 2 最小目录单元分析计划

> **日期**：2026-06-24
> **最近更新**：2026-06-29，batch06 采用 3 个子 agent 并行分析 6 个 Mystic 小插件目录，并由主 agent 统一合并 JSONL 与文档。
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
| 已完成单元 | 16 |
| 当前完成单元 | batch06：`ResultAnnotation/source`、`ResultComment/source`、`ResultEngagementAnalysis/source`、`ResultEventMarker/source`、`ResultHeadDownView/source`、`ResultHeadUpView/source` |

## 3. 批次规则

最小目录单元仍是 Phase 2 的原子分析粒度；后续批次可以在保证证据完整和结果可验证的前提下，同时处理多个最小目录单元。批次规模按正确性优先控制：

| 规则 | 要求 |
|------|------|
| 原子粒度 | 每个最小目录单元必须独立列出边界、文件、关键符号、职责、未确认项；不得把多个目录粗略合并成一个无法追溯的模块结论。 |
| 批次合并 | 同一批次优先合并文件数少、边界清晰、职责相近或互不耦合的多个最小目录单元。复杂目录、跨模块调用密集目录或证据不足目录应单独成批。 |
| 批次容量 | 建议每批处理 2-6 个小目录，或控制在约 20 个 source/header 文件以内；若 CodeGraph 证据、调用链或源码语义较复杂，应主动缩小批次。 |
| 正确性门槛 | 每个目录都必须完成 CodeGraph/源码交叉确认、file-index 更新、symbol-index 粗符号修正和人工可读说明；任一目录存疑时可拆出为后续批次，不影响同批其他已确认目录落地。 |

每个批次完成后必须更新：

1. `workspace/source-index/file-index.jsonl`：补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions`、中文 `brief`。
2. `workspace/source-index/symbol-index-phase2.jsonl`：修正该单元粗符号，过滤导出宏伪符号，保留真实 class/struct/enum/typedef。
3. `docs/architecture/module-overview-v2-incremental.md`：追加该单元的人类可读说明。
4. `docs/verification/phase2-followup-batchNN-verify-report.md`：验证该批次；若批次包含多个目录，报告必须覆盖全部目录，并提供按目录拆分的文件数、符号数、证据来源和风险项。
5. `docs/records/NN-phase2-...md`：记录批次处理结果。

## 4. 子 agent 并行规则

为提升大型 C++ 项目的 Phase 2 分析效率，后续批次可采用子 agent 并行，但主 agent 必须保留最终合并和一致性校验职责：

| 角色 | 职责 |
|------|------|
| 主 agent | 选定批次目录、分配互不冲突的目录范围、统一 schema、合并 `file-index.jsonl`/`symbol-index-phase2.jsonl`/文档、执行最终验证。 |
| 子 agent | 针对分配到的最小目录单元读取 CodeGraph 和源码，输出目录边界、文件清单、关键符号、调用/注册证据、未确认项和建议索引补丁。 |

并行执行时遵守以下约束：

1. 子 agent 的分析范围必须是一个或多个明确的最小目录单元，避免多个 agent 同时判断同一目录。
2. 默认由主 agent 写入共享 JSONL 和正式 `docs/` 报告；子 agent 只产出结构化分析摘要或临时补丁建议，除非已分配互不重叠的输出文件。
3. 主 agent 合并时必须逐目录复核子 agent 的证据链，尤其是导出宏伪符号、匿名命名空间符号、注册入口和跨目录调用归属。
4. 批次报告必须囊括该批所有目录，采用“批次总览 + 每目录小节 + 统一验证结果”的结构，不能只记录其中一个目录。
5. 若子 agent 之间结论冲突，先保留可证实部分；冲突目录降级为 `needs_review` 或拆入下一批，不用不确定结论污染已确认索引。

## 5. 下一批候选

batch06 已完成 6 个 Mystic 小插件目录。batch05 已按实际源码展开数修正执行范围：`core/wsf_util`、`wsf_p6dof`、`wsf_six_dof` 虽在工作清单中显示为小计数，但按路径前缀会覆盖大量 source/header，因此未并入 batch05。后续候选必须同时检查工作清单计数和实际 file-index 路径展开数。

按“文件少、边界清晰、优先核心源码”排序，下一批建议可继续作为一个多目录批次处理；实际执行时根据 CodeGraph 证据复杂度动态拆分：

| 优先级 | 最小目录单元 | source/header 数 | 说明 |
|--------|--------------|------------------|------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultInteractionLines/source` | 2 | Mystic interaction lines 显示插件，小目录。 |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultOrbit/source` | 2 | Mystic orbit 显示插件，小目录。 |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultProjector/source` | 2 | Mystic projector 显示插件，小目录。 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultRoute/source` | 2 | Mystic route 显示插件，小目录。 |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultSituationAwarenessDisplay/source` | 2 | Mystic situation awareness display 插件，小目录。 |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultVisualEffects/source` | 2 | Mystic visual effects 插件，小目录。 |

建议 batch07 继续按 3-6 个 Mystic 小插件目录并行分析：由主 agent 统一批次范围和验证标准，子 agent 分别负责单目录证据采集；如果某插件存在复杂 UI/数据链路，则缩小到 2-3 个目录。

## 6. 已知注意事项

1. `workspace/source-index/symbol-index.jsonl` 是 Phase 3 精细索引，当前只修 Phase 2 粗索引 `symbol-index-phase2.jsonl`。Phase 3 后续应按新的 Phase 2 单元结果重跑或增量修正。
2. `compile_commands.json` 仍未生成，因此本阶段以 CodeGraph + 源码文本证据为主，AST/include path 精确性仍受限。
3. 旧 `module-overview.md` 中的 107 同层模块清单属于历史 Phase 2 视图，不再作为新的架构模块组织依据。
4. batch02 发现旧 Phase 3 精细索引中存在 `WsfGrammarCheckExtension` 成员被错误挂到 `ParseSourceProvider` 下的问题；本轮只修 Phase 2 粗索引，Phase 3 后续应按最小单元重新精修。
5. batch03 的 `MissionVersion.hpp` 只有版本/产品宏，无 class/struct；本轮将版本宏作为 Phase 3 macro-index 候选，而不是伪造类符号。
6. batch04 首次按“多个最小目录单元 + 子 agent 并行 + 主 agent 合并”执行；对共享 JSONL 仍由主 agent 串行写入，子 agent 只提供目录级证据摘要。
7. batch05 发现工作清单中部分 `analysis_unit` 与实际 file-index 路径展开不一致；后续批次选择必须先计算实际展开的 source/header 数，避免把大目录误当成小单元。
8. batch06 发现多个 Mystic 插件依赖 generated event-pipe headers 或 ResultData 插件；Phase 2 只记录显示/聚合入口，消息字段精确定义留给后续业务逻辑或 Phase 3/4 深挖。
