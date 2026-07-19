# Phase4 最终四层函数索引合并记录

## 范围

本记录覆盖 Phase4 批次产物到最终产物的合并：

```text
workspace/source-index/function-index.jsonl
workspace/source-index/function-body-summary.jsonl
workspace/source-index/phase4-function-skips.jsonl
workspace/source-index/phase4-merge-summary.json
```

执行命令：

```bash
python3 tools/indexers/phase4_merge_outputs.py --root .
```

## 合并策略

1. Method-level 从 `workspace/source-index/phase4-batches/phase4-batch??-function-index.jsonl` 合并。
2. 用 `candidate_id` 回填 `module`、`owner`、`kind`、`signature`、`phase4_sequence` 等候选元数据。
3. 全局检查 `qualified_name` 唯一性；跨批次重复时追加 `candidate_id` 短后缀，并同步 body summary。
4. Class-level 按 `module + owner` 聚合 Method-level。
5. Module-level 按 `module` 聚合 Class-level。
6. System-level 生成单一入口 `AFSIM::System::FunctionInventory`，聚合全部 Module-level。

## 输出统计

| 指标 | 数量 |
|---|---:|
| 批次数 | 23 |
| 输入候选 | 53,064 |
| 有效候选 | 52,946 |
| Method-level | 49,561 |
| Class-level | 5,415 |
| Module-level | 54 |
| System-level | 1 |
| function-index 总条目 | 55,031 |
| function-body-summary 条目 | 49,561 |
| skip 条目 | 3,503 |
| `variable_not_function` | 118 |
| 原始覆盖率 | 93.40% |
| 有效覆盖率 | 93.61% |
| 全局重复限定名修正 | 248 |

## 验证结果

| 检查项 | 结果 |
|---|---|
| 四层条目完整性 | 通过 |
| System → Module 追溯 | 通过 |
| Module → Class 追溯 | 通过 |
| Class → Method 追溯 | 通过 |
| `qualified_name` 全局唯一 | 通过 |
| Method/body `candidate_id` 配对 | 通过 |
| Method 与 skip 候选互斥 | 通过 |
| Method-level 路径存在性 | 通过 |
| 导出宏伪函数过滤 | 通过 |
| 常见伪调用过滤 | 通过 |
| lifecycle_role `unknown` 比例 | 0.00% |

## 结论

Phase4 已完成最终四层函数索引和全量 body summary 合并。该产物可以作为下一步 AFSIM 业务逻辑分析的函数级输入。
