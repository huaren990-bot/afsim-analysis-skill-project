# Phase4 batch14-batch23 Method-level 提取记录

## 范围

本记录覆盖 Phase4 剩余批次 `phase4-batch14` 到 `phase4-batch23`。执行顺序为串行逐批处理，每个批次完成后再进入下一个批次。

执行命令：

```bash
python3 tools/indexers/phase4_extract_batch.py --batch-id <batch_id> --root .
```

## 规则补充

本轮在原有头文件声明到 `.cpp` 定义匹配规则上补充：

1. 从 `owner` / `qualified_name` 提取类名，搜索类名同 stem 的 `.cpp/.hpp/.h/.hh/.hxx/.cc/.cxx/.C/.inl/.ipp/.tpp` 文件。
2. 覆盖 `Bounds.hpp` 声明 `TimeBounds`、`TimeBounds.cpp` 存放实现这类声明头文件与实现文件不同名的情况。
3. 对未匹配候选区分 `declaration_only` 和 `variable_not_function`。
4. summary 同时保留 `raw_coverage` 和有效候选口径 `coverage`。

## 批次结果

| 批次 | 输入候选 | 有效候选 | 读取文件 | Method-level | body summary | 跳过 | 变量误报 | 原始覆盖率 | 有效覆盖率 | 跨原始 path 命中 | 重复名兜底 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| phase4-batch14 | 2,419 | 2,417 | 313 | 2,278 | 2,278 | 141 | 2 | 94.17% | 94.25% | 682 | 592 |
| phase4-batch15 | 2,424 | 2,418 | 356 | 2,276 | 2,276 | 148 | 6 | 93.89% | 94.13% | 449 | 0 |
| phase4-batch16 | 2,439 | 2,434 | 336 | 2,302 | 2,302 | 137 | 5 | 94.38% | 94.58% | 738 | 6 |
| phase4-batch17 | 2,510 | 2,500 | 236 | 2,326 | 2,326 | 184 | 10 | 92.67% | 93.04% | 981 | 0 |
| phase4-batch18 | 2,466 | 2,399 | 345 | 2,184 | 2,184 | 282 | 67 | 88.56% | 91.04% | 428 | 20 |
| phase4-batch19 | 2,575 | 2,567 | 288 | 2,385 | 2,385 | 190 | 8 | 92.62% | 92.91% | 851 | 20 |
| phase4-batch20 | 2,422 | 2,421 | 259 | 2,308 | 2,308 | 114 | 1 | 95.29% | 95.33% | 1,045 | 30 |
| phase4-batch21 | 2,658 | 2,642 | 232 | 2,399 | 2,399 | 259 | 16 | 90.26% | 90.80% | 950 | 234 |
| phase4-batch22 | 2,447 | 2,444 | 336 | 2,296 | 2,296 | 151 | 3 | 93.83% | 93.94% | 888 | 0 |
| phase4-batch23 | 858 | 858 | 181 | 774 | 774 | 84 | 0 | 90.21% | 90.21% | 308 | 9 |

## 合计

| 指标 | 数量 |
|---|---:|
| 输入候选 | 23,218 |
| 有效候选 | 23,100 |
| Method-level 条目 | 21,528 |
| body summary 条目 | 21,528 |
| 跳过项 | 1,690 |
| `variable_not_function` | 118 |
| 原始覆盖率 | 92.72% |
| 有效覆盖率 | 93.19% |
| 跨原始 path 命中 | 7,320 |
| 重复限定名兜底修正 | 911 |

## 验证

已对 `phase4-batch14` 到 `phase4-batch23` 执行统一验证：

| 检查项 | 结果 |
|---|---|
| JSONL 可解析性 | 通过 |
| Method/body `candidate_id` 配对 | 通过 |
| `qualified_name` 批内唯一性 | 通过 |
| Method-level 路径存在性 | 通过 |
| 导出宏伪函数过滤 | 通过 |
| 常见伪调用过滤 | 通过 |

## 输出

批次输出位于：

```text
workspace/source-index/phase4-batches/
```

本轮同时更新：

```text
docs/architecture/phase4-function-extraction-plan.md
docs/verification/phase4-verify-report.md
```
