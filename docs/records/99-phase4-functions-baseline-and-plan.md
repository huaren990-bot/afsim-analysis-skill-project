# Phase 4 完成记录：函数候选基线与批次计划

> **完成日期**：2026-07-16  
> **阶段**：Phase 4 / 7  
> **状态**：进行中，候选基线与批次计划已完成

## 分析范围

| 参数 | 值 |
|---|---|
| source_root | `/Users/hjt/afsim/afsim-analysis-skill-project/source_root` |
| extract_roots | `afsim-2_9` |
| exclude_paths | `afsim-2_9/demos`、`afsim-2_9/documentation`、`afsim-2_9/training`、`afsim-2_9/resources`、隐藏目录、`vx.json` |
| analysis_depth | `full` |

## 执行方式

| 子阶段 | Agent 数 | 职责 |
|---|---:|---|
| Phase 4A：候选基线生成 | 1 | 从 Phase3 精细符号索引和 file-index 补充候选，过滤伪函数 |
| Phase 4B：旧产物审计 | 1 | 检查旧 `function-index` 和 `function-body-summary` 是否满足新版门禁 |
| Phase 4C：批次计划生成 | 1 | 按父目录最小单元和文件范围拆分 23 个批次 |

**总耗时**：约 1 小时  
**总 Agent 数**：1  
**总工具调用**：多次本地 JSONL 统计与文件校验

## 产出文件

| 文件 | 路径 | 用途 |
|---|---|---|
| Phase4 函数候选基线 | `workspace/source-index/functions-to-extract-phase4.jsonl` | 后续 Method-level 提取输入 |
| Phase4 跳过清单 | `workspace/source-index/functions-to-extract-phase4-skips.jsonl` | 覆盖闭环和 known-issue 依据 |
| Phase4 基线摘要 | `workspace/source-index/functions-to-extract-phase4-summary.json` | 候选、跳过、模块分布统计 |
| Phase4 批次计划 | `workspace/source-index/phase4-function-batch-plan.jsonl` | 23 个批次的机器可读计划 |
| Phase4 重建计划 | `docs/architecture/phase4-function-extraction-plan.md` | 人读执行计划 |
| Phase4 基线验证报告 | `docs/verification/phase4-verify-report.md` | 当前基线验证与旧产物不通过说明 |

## 关键统计数据

| 指标 | 数量 |
|---|---:|
| 有效候选函数/方法 | 53,064 |
| 已记录跳过项 | 56,419 |
| 批次数 | 23 |
| 完整唯一键重复 | 0 |
| 源码路径缺失 | 0 |
| 导出宏伪函数残留 | 0 |

## 验证结果

| # | 检查项 | 结果 | 详情 |
|---|---|---|---|
| 1 | 旧 Phase4 产物质量 | 不通过 | 旧产物存在导出宏伪函数、重复 `qualified_name` 和签名缺失 |
| 2 | 新候选唯一键 | 通过 | `qualified_name + signature + path` 无重复 |
| 3 | 路径存在性 | 通过 | 有效候选源码路径均存在 |
| 4 | 宏/控制语句过滤 | 通过 | 宏调用和 `if/for/case` 等伪候选未进入有效候选 |
| 5 | 批次覆盖 | 通过 | 23 个批次覆盖全部 53,064 条有效候选 |

## 已知问题与备注

- 未发现 `compile_commands.json`，Phase4 后续不能依赖完整 AST，只能采用 CodeGraph + 源码文本批量证据。
- `macro_generated_unexpanded` 项不会生成虚假 Method-level 条目，需要在最终覆盖率中作为有原因跳过项处理。
- 当前 `docs/verification/phase4-verify-report.md` 是基线验证报告，最终合并后必须重跑完整 Phase4 验证。

## 下游就绪

后续从 `phase4-batch01` 开始执行 Method-level 提取。每批输出到 `workspace/source-index/phase4-batches/`，批次全部完成后再合并为最终 `function-index.jsonl` 和 `function-body-summary.jsonl`。
