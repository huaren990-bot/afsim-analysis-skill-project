# Phase6 生命周期、数据流与扩展点生成记录

## 范围

本记录覆盖 Phase6 动态行为视图生成，输入为 Phase1-5 最新产物：

```text
workspace/project-boundary/project-boundary.json
workspace/source-index/file-index.jsonl
workspace/source-index/symbol-index.jsonl
workspace/source-index/function-index.jsonl
workspace/source-index/function-body-summary.jsonl
workspace/source-index/dependency-index.jsonl
```

## 执行

按 Phase6 规则：

1. `function-index.jsonl` 中没有 `lifecycle_role=entry` 的 Method-level 条目，因此使用一次 CodeGraph 批量查询补充入口点证据。
2. 使用一次配置入口批量 grep，覆盖 `ProcessInput`、`LoadConfig`、`ParseScenario`、`ReadXML`、`UtInput`、`json::parse`、`tinyxml`。
3. 使用一次扩展点批量 grep，覆盖 `ComponentFactory`、`ObjectFactory`、`PluginManager`、`Extension`、`Observer`、`EventPipe`、`Subscribe` 等模式。
4. 执行可复跑脚本：

```bash
python3 tools/indexers/phase6_build_lifecycle.py --root .
```

## 输出

| 产物 | 说明 |
|---|---|
| `docs/architecture/lifecycle.md` | 生命周期阶段、关键函数和可验证调用链 |
| `docs/architecture/dataflow.md` | 关键数据对象与配置流 |
| `docs/architecture/extension-points.md` | 扩展机制、注册位置和运行时影响 |
| `docs/verification/phase6-verify-report.md` | Phase6 验证报告 |
| `workspace/source-index/phase6-lifecycle-summary.json` | Phase6 统计摘要 |

## 统计

| 指标 | 数量 |
|---|---:|
| 生命周期阶段 | 8 |
| 生命周期调用链 | 24 |
| 关键数据对象 | 5 |
| 扩展机制 | 10 |
| Mermaid 图块 | 7 |

## 阶段覆盖

| lifecycle_role | 关键函数数 |
|---|---:|
| `entry` | 5 |
| `scenario_load` | 8 |
| `object_create` | 8 |
| `simulation_loop` | 8 |
| `model_update` | 8 |
| `event_handling` | 8 |
| `output` | 8 |
| `shutdown` | 8 |

## 验证摘要

| 检查项 | 结果 |
|---|---|
| 8 个生命周期阶段覆盖 | 通过 |
| 生命周期调用链追溯 | 通过 |
| 数据对象数量 ≥ 5 | 通过 |
| 扩展机制数量 ≥ 3 | 通过 |
| Mermaid 代码块闭合 | 通过 |
| 配置流用途说明 | 通过 |
| 扩展点用途说明 | 通过 |

## 已知限制

1. Phase4 未单独标记 `entry`，入口阶段由 `main/WinMain` 函数和 CodeGraph 查询补充。
2. 数据流文档按 5 类核心对象聚合，不展开每一个派生类；完整对象证据仍在 `symbol-index.jsonl` 与 `dependency-index.jsonl`。
3. 扩展点按注册模式聚合，具体实例以 `dependency-index.jsonl` 中 `relation=registration` 为完整清单。
