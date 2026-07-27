# 算法提取输出契约

## 候选清单

`workspace/algorithm-extraction/algorithm-candidates.jsonl` 每行一个函数候选。自动字段由候选脚本生成，人工字段在重跑时保留。

必需字段：

- 定位：`candidate_id`、`qualified_name`、`function_name`、`module`、`path`、`line_start`、`line_end`
- 排序：`algorithm_hint`、`algorithm_pattern`、`computation_density`、`priority_score`、`selection_reasons`
- 闭环：`status`、`algorithm_ids`、`decision_reason`

## 覆盖账本

`workspace/algorithm-extraction/algorithm-coverage.jsonl` 每行对应一个候选，并至少包含：

```json
{
  "candidate_id": "stable-id",
  "qualified_name": "Namespace::Class::Method#digest",
  "source": {"path": "relative/path.cpp", "line_start": 10, "line_end": 40},
  "status": "extracted",
  "algorithm_ids": ["ALG-FLIGHT-DYNAMICS-RK4"],
  "decision_reason": "核心积分更新",
  "artifacts": {
    "card": "docs/algorithms/flight-dynamics-rk4-card.md",
    "interface_spec": "docs/extracted-algorithms/rk4/flight-dynamics-rk4-interface-spec.md"
  },
  "verification": "passed"
}
```

`status` 只允许 `pending`、`selected`、`extracted`、`rejected`、`deferred`。完成批次中不得保留 `pending` 或 `selected`。

## 算法卡片

除模板章节外，每张卡片必须能回答：

1. 这是什么算法，边界在哪里，为什么不是相邻的另一个算法。
2. 入口、核心函数、调用链和生命周期位置是什么。
3. 输入、输出、参数、状态、副作用、单位和坐标系是什么。
4. 源码离散步骤如何对应数学表达式。
5. 经验常量、假设、边界与数值风险是什么。
6. 如何脱离 AFSIM 验证该算法。

Method 必须使用当前 `function-index.jsonl` 中存在的 `qualified_name`。源码位置必须使用索引中的 `path:line_start-line_end`，并在生成时核对真实源码。

## 接口规格

接口规格描述可移植契约，不得伪装成已实现代码。至少包含：

- 输入输出类型、单位、坐标系、有效范围和所有权。
- 配置、内部状态、初始化、逐步更新、重置和错误处理。
- AFSIM 类型到中性类型的映射。
- 框架依赖、替代方案和不可移植部分。
- 至少一个最小调用示例和验证 oracle。

## Compendium

每个已通过算法恰好有一条主条目，包含算法 ID、名称、领域、模块、卡片链接、接口规格链接、核心源码证据和验证状态。统计数字必须由实际条目计算，不手填推测值。
