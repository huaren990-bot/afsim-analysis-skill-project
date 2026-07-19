# Phase 4 批次记录：phase4-batch02 至 phase4-batch07 函数/方法提取

> **完成日期**：2026-07-16  
> **阶段**：Phase 4 / 7  
> **状态**：已完成 6 个批次并通过批次级验证

## 分析范围

| 参数 | 值 |
|---|---|
| batch_id | `phase4-batch02` 至 `phase4-batch07` |
| 模块 | `core/wsf`、`wizard` |
| 输入候选 | 13,000 |
| 执行规则 | 增强头/源匹配、注释感知函数体匹配、重复限定名兜底 |

## 执行方式

| 子阶段 | Agent 数 | 职责 |
|---|---:|---|
| 批量源码提取 | 1 | 使用增强脚本逐批提取 Method-level 和 body summary |
| 批次验证 | 1 | 检查 JSONL、配对、唯一性、导出宏、伪调用和路径存在性 |

执行命令：

```bash
for b in phase4-batch02 phase4-batch03 phase4-batch04 phase4-batch05 phase4-batch06 phase4-batch07; do
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
| phase4-batch02 | 1,903 | 1,823 | 80 | 95.80% | 580 |
| phase4-batch03 | 1,862 | 1,693 | 169 | 90.92% | 451 |
| phase4-batch04 | 2,203 | 2,132 | 71 | 96.78% | 539 |
| phase4-batch05 | 1,872 | 1,732 | 140 | 92.52% | 525 |
| phase4-batch06 | 2,595 | 2,383 | 212 | 91.83% | 1,172 |
| phase4-batch07 | 2,565 | 2,361 | 204 | 92.05% | 1,002 |
| 合计 | 13,000 | 12,124 | 876 | 93.26% | 4,269 |

## 验证结果

| # | 检查项 | 结果 | 详情 |
|---|---|---|---|
| 1 | JSONL 可解析性 | 通过 | 6 个批次的 Method-level、body summary、skips 均无解析错误 |
| 2 | Method/body 配对 | 通过 | 每个 Method-level 条目均有同 `candidate_id` 的 body summary |
| 3 | `qualified_name` 唯一性 | 通过 | `batch04` 修正 22 条重复短名，`batch05` 修正 8 条重复短名 |
| 4 | 导出宏过滤 | 通过 | 未发现导出宏伪函数 |
| 5 | 伪调用过滤 | 通过 | 未发现 `if/for/else/case/block/get/move` 等残留在 calls |
| 6 | 路径存在性 | 通过 | Method-level 中的源码路径均存在 |
| 7 | 覆盖率 | 通过 | 6 个批次合计覆盖率 93.26%，每批均超过 90% |

## 已知问题与备注

- 跳过项全部为 `declaration_only`，主要对应纯虚接口、默认析构、无显式函数体或 Phase3 候选残留。
- 本轮额外增强了注释感知匹配：跳过字符串、行注释、块注释，以及参数列表后的行尾注释，例如 `) // = 0`。
- 后续批次应继续统一使用 `tools/indexers/phase4_extract_batch.py`。

## 下游就绪

`phase4-batch02` 至 `phase4-batch07` 可进入后续 Phase4 合并。当前 Phase4 已完成 `phase4-batch01` 至 `phase4-batch07`，下一个待处理批次为 `phase4-batch08`。
