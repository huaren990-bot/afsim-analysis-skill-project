# Phase 4 批次记录：phase4-batch08 至 phase4-batch13 函数/方法提取

> **完成日期**：2026-07-16  
> **阶段**：Phase 4 / 7  
> **状态**：已完成 6 个批次并通过批次级验证

## 分析范围

| 参数 | 值 |
|---|---|
| batch_id | `phase4-batch08` 至 `phase4-batch13` |
| 模块 | `wizard`、`core/wsf_mil`、`mover_creator` |
| 输入候选 | 14,517 |
| 执行规则 | 增强头/源匹配、注释感知函数体匹配、重复限定名兜底 |

## 执行方式

| 子阶段 | Agent 数 | 职责 |
|---|---:|---|
| 批量源码提取 | 1 | 使用增强脚本逐批提取 Method-level 和 body summary |
| 批次验证 | 1 | 检查 JSONL、配对、唯一性、导出宏、伪调用和路径存在性 |

执行命令：

```bash
for b in phase4-batch08 phase4-batch09 phase4-batch10 phase4-batch11 phase4-batch12 phase4-batch13; do
  python3 tools/indexers/phase4_extract_batch.py --batch-id "$b" --root .
done
```

## 产出文件

| 文件类型 | 路径模式 |
|---|---|
| Method-level 批次索引 | `workspace/source-index/phase4-batches/<batch_id>-function-index.jsonl` |
| 函数体摘要 | `workspace/source-index/phase4-batches/<batch_id>-function-body-summary.jsonl` |
| 批次跳过清单 | `workspace/source-index/phase4-batches/<batch_id>-skips.jsonl` |
| 批次摘要 | `workspace/source-index/phase4-batches/<batch_id>-summary.json` |

## 关键统计数据

| 批次 | 输入候选 | Method-level | 跳过 | 覆盖率 | 头/同名文件命中 |
|---|---:|---:|---:|---:|---:|
| phase4-batch08 | 2,587 | 2,358 | 229 | 91.15% | 730 |
| phase4-batch09 | 2,494 | 2,323 | 171 | 93.14% | 507 |
| phase4-batch10 | 2,456 | 2,325 | 131 | 94.67% | 691 |
| phase4-batch11 | 2,251 | 2,183 | 68 | 96.98% | 703 |
| phase4-batch12 | 2,388 | 2,312 | 76 | 96.82% | 1,222 |
| phase4-batch13 | 2,341 | 2,196 | 145 | 93.81% | 1,149 |
| 合计 | 14,517 | 13,697 | 820 | 94.35% | 5,002 |

## 验证结果

| # | 检查项 | 结果 | 详情 |
|---|---|---|---|
| 1 | JSONL 可解析性 | 通过 | 6 个批次的 Method-level、body summary、skips 均无解析错误 |
| 2 | Method/body 配对 | 通过 | 每个 Method-level 条目均有同 `candidate_id` 的 body summary |
| 3 | `qualified_name` 唯一性 | 通过 | `batch09` 修正 38 条、`batch10` 修正 4 条、`batch11` 修正 2 条重复短名 |
| 4 | 导出宏过滤 | 通过 | 未发现导出宏伪函数 |
| 5 | 伪调用过滤 | 通过 | 未发现 `if/for/else/case/block/get/move` 等残留在 calls |
| 6 | 路径存在性 | 通过 | Method-level 中的源码路径均存在 |
| 7 | 覆盖率 | 通过 | 6 个批次合计覆盖率 94.35%，每批均超过 90% |

## 已知问题与备注

- 跳过项全部为 `declaration_only`，主要对应纯虚接口、默认析构、无显式函数体或 Phase3 候选残留。
- 本轮覆盖 `wizard`、`core/wsf_mil` 与 `mover_creator`，头文件/inline 命中比例较高，说明增强头/源规则仍然必要。
- 后续批次应继续统一使用 `tools/indexers/phase4_extract_batch.py`。

## 下游就绪

`phase4-batch08` 至 `phase4-batch13` 可进入后续 Phase4 合并。当前 Phase4 已完成 `phase4-batch01` 至 `phase4-batch13`，下一个待处理批次为 `phase4-batch14`。
