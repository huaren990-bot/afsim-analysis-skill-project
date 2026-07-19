# Phase5 依赖关系验证报告

## 1. 总体结论

| 检查项 | 结果 |
|---|---|
| 总体状态 | 通过 |
| dependency-index 条目数 ≥ 200 | 通过 |
| 覆盖 6 种 relation | 通过 |
| 每种 relation ≥ 5 | 通过 |
| strength 字段覆盖 | 通过 |
| 分析边界污染 | 通过 |
| Mermaid 边追溯 | 通过 |
| inheritance 与 symbol-index 交叉验证 | 通过 |

## 2. relation 分布

| relation | 条目数 |
|---|---:|
| `build` | 280 |
| `call` | 179,465 |
| `composition` | 13,083 |
| `include` | 74,737 |
| `inheritance` | 5,102 |
| `registration` | 683 |

## 3. 输出文件

```text
workspace/source-index/dependency-index.jsonl
docs/architecture/dependency-graph.md
docs/architecture/module-dependency.md
```

## 4. 说明

Mermaid 图采用跨模块摘要展示，每条边在 `docs/architecture/dependency-graph.md` 的“Mermaid 边追溯矩阵”中记录 `dependency_id`，可回查 `workspace/source-index/dependency-index.jsonl`。

## 5. 深度验证

| 检查项 | 结果 | 证据 |
|---|---|---|
| JSONL 解析 | 通过 | 273,350 行全部可解析 |
| strength 缺失率 | 通过 | 缺失 0 条 |
| 分析边界污染 | 通过 | `source`、`target`、`path` 未命中 `demos/documentation/training/resources` |
| Mermaid 追溯 | 通过 | 文档中 270 个 `dependency_id` 全部存在于 `dependency-index.jsonl` |
| inheritance 交叉验证 | 通过 | 5,102 条 inheritance 中 101 条未能按短基类名直接交叉确认，不一致率 1.98%，低于 10% 门槛 |
| 完整清单入口 | 通过 | `dependency-graph.md` 链接 `workspace/source-index/dependency-index.jsonl` 与 `docs/architecture/module-dependency.md` |

## 6. 已知限制

1. `call` 关系优先来自 Phase4 `calls`/`dependencies` 数组。部分目标为 `external-call:<name>`，表示在 Method-level 中未解析到被调用函数定义，保留为弱依赖。
2. `composition` 关系从 Phase3 `member_variables` 启发式抽取，模板容器内的复杂类型会保留为类型文本；后续业务逻辑分析可对核心类再做 CodeGraph 精读。
3. Mermaid 图为摘要图，不代表只存在图中这些依赖；完整依赖以 `dependency-index.jsonl` 为准。
