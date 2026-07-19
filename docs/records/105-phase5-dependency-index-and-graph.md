# Phase5 依赖关系索引与图谱生成记录

## 范围

本记录覆盖 Phase5 跨模块依赖关系分析，输入为 Phase1-4 的最新产物：

```text
workspace/project-boundary/project-boundary.json
workspace/source-index/file-index.jsonl
workspace/source-index/symbol-index.jsonl
workspace/source-index/function-index.jsonl
workspace/source-index/function-body-summary.jsonl
```

## 执行

先使用 CodeGraph 对核心注册/工厂/事件订阅路径做批量探索，确认 `WsfExtensionList`、`WsfEventManager`、`FactoryManager`、L16 `Messages::Factory` 等注册与工厂路径存在源码证据。

随后执行可复跑脚本：

```bash
python3 tools/indexers/phase5_build_dependencies.py --root .
```

## 输出

| 产物 | 说明 |
|---|---|
| `workspace/source-index/dependency-index.jsonl` | 全量依赖清单 |
| `workspace/source-index/phase5-dependency-summary.json` | Phase5 统计摘要 |
| `docs/architecture/dependency-graph.md` | Mermaid 摘要图与追溯矩阵 |
| `docs/architecture/module-dependency.md` | 模块依赖明细摘要 |
| `docs/verification/phase5-verify-report.md` | Phase5 验证报告 |

## 统计

| relation | 条目数 |
|---|---:|
| `build` | 280 |
| `call` | 179,465 |
| `composition` | 13,083 |
| `include` | 74,737 |
| `inheritance` | 5,102 |
| `registration` | 683 |
| **合计** | **273,350** |

## 边界处理

按 Phase1 边界排除以下路径进入核心依赖索引：

| 路径 | 处理 |
|---|---|
| `afsim-2_9/demos` | 排除 |
| `afsim-2_9/documentation` | 排除 |
| `afsim-2_9/training` | 排除 |
| `afsim-2_9/resources` | 排除 |

验证结果显示 `source`、`target`、`path` 字段无边界污染。

## 验证摘要

| 检查项 | 结果 |
|---|---|
| JSONL 解析 | 通过 |
| relation 六类覆盖 | 通过 |
| 每类 relation ≥ 5 | 通过 |
| strength 字段覆盖 | 通过 |
| Mermaid 边追溯 | 通过 |
| inheritance 与 symbol-index 交叉验证 | 通过 |
| 分析边界污染 | 通过 |

## 已知限制

1. `call` 关系来自 Phase4 函数级 `calls`/`dependencies` 数组，部分目标保留为 `external-call:<name>`。
2. `composition` 从 Phase3 `member_variables` 启发式抽取，复杂模板类型保留原始类型文本。
3. Mermaid 图是跨模块摘要图，完整依赖以 `workspace/source-index/dependency-index.jsonl` 为准。
