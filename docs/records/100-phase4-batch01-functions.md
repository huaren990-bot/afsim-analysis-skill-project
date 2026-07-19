# Phase 4 批次记录：phase4-batch01 函数/方法提取

> **完成日期**：2026-07-16  
> **阶段**：Phase 4 / 7  
> **状态**：已完成批次级提取，增强头/源匹配后通过批次级验证

## 分析范围

| 参数 | 值 |
|---|---|
| batch_id | `phase4-batch01` |
| 目录单元 | `afsim-2_9/swdev/src/core/wsf/source#part01`、`afsim-2_9/swdev/src/core/wsf/source#part02` |
| 模块 | `core/wsf` |
| 输入候选 | 2,329 |
| 源码文件 | 94 |

## 执行方式

| 子阶段 | Agent 数 | 职责 |
|---|---:|---|
| CodeGraph 抽查 | 1 | 使用 CodeGraph 读取代表文件 `WsfSimulation.cpp`，确认索引可用 |
| 批量源码提取 | 1 | 每个源码文件读取一次，定位函数体并生成 Method-level/body summary |
| 批次验证 | 1 | 检查 JSONL 可解析性、唯一性、伪调用残留和分类分布 |

执行脚本：

```bash
python3 tools/indexers/phase4_extract_batch.py --batch-id phase4-batch01 --root .
```

## 产出文件

| 文件 | 路径 |
|---|---|
| Method-level 批次索引 | `workspace/source-index/phase4-batches/phase4-batch01-function-index.jsonl` |
| 函数体摘要 | `workspace/source-index/phase4-batches/phase4-batch01-function-body-summary.jsonl` |
| 批次跳过清单 | `workspace/source-index/phase4-batches/phase4-batch01-skips.jsonl` |
| 批次摘要 | `workspace/source-index/phase4-batches/phase4-batch01-summary.json` |

## 关键统计数据

| 指标 | 数量 |
|---|---:|
| Method-level 条目 | 2,212 |
| body summary 条目 | 2,212 |
| 跳过项 | 117 |
| 批次覆盖率 | 94.98% |
| `qualified_name` 重复 | 0 |
| 命中原始 path 之外的头/同名文件 | 754 |
| 头文件/inline Method-level 条目 | 800 |

## 验证结果

| # | 检查项 | 结果 | 详情 |
|---|---|---|---|
| 1 | JSONL 可解析性 | 通过 | 三个批次 JSONL 文件均无解析错误 |
| 2 | Method-level 唯一性 | 通过 | `qualified_name` 已追加 `signature_digest`，无重复 |
| 3 | body summary 配对 | 通过 | 2,212 条 Method-level 均有同数 body summary |
| 4 | 伪调用过滤 | 通过 | `if/for/else/case/block/get/move` 等未残留在 calls |
| 5 | 覆盖率 | 通过 | 增强头/源匹配后批次覆盖率达到 94.98% |

## 已知问题与备注

- 剩余 117 条 `declaration_only` 多为默认/纯虚析构、纯虚接口或 Phase3 误分类残留，后续全局合并时继续作为有原因跳过项处理。
- 增强脚本已经固化到 `tools/indexers/phase4_extract_batch.py`，后续批次应统一使用该脚本。

## 下游就绪

`phase4-batch01` 可作为首批 Method-level 输入，但最终合并前需要结合全局覆盖率判断是否回补 `declaration_only` 项。
