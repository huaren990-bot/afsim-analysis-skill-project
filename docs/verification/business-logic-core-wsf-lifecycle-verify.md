# 业务逻辑分析验证报告：core/wsf 主生命周期

> **日期**：2026-07-15  
> **验证对象**：`docs/architecture/business-logic-readiness.md`、`workspace/business-logic/core-wsf-lifecycle-flows.jsonl`、`docs/architecture/lifecycle.md`

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|---|---|---|
| 1 | Markdown 产物位置 | 通过 | 新增 Markdown 均位于 `docs/` 下 |
| 2 | 机器可读产物位置 | 通过 | JSONL 位于 `workspace/business-logic/` |
| 3 | CodeGraph 优先 | 通过 | 先使用 `codegraph explore` 和 `codegraph node` 获取源码证据 |
| 4 | 源码证据可追溯 | 通过 | 每个流程均包含源码路径和行号范围 |
| 5 | 业务结论边界 | 通过 | 文档标注为候选入口，没有把候选写成最终业务规则 |
| 6 | evidence_level | 通过 | 业务域、流程、规则、映射均包含 `direct` 或 `cross_checked` |
| 7 | 边界外排除 | 通过 | demo/training/documentation/resources 未作为核心结论证据 |
| 8 | 可处理未知项 | 通过 | 未知项包含影响、当前证据、建议确认对象和严重度 |

## 核心证据抽查

| 证据 | 验证结论 |
|---|---|
| `WsfStandardApplication.cpp:279-289` | 可支持场景文件加载入口 |
| `WsfScenario.cpp:671-743` | 可支持场景完成加载和 extension/type/input platform 收尾 |
| `WsfSimulation.cpp:537-648` | 可支持仿真初始化生命周期 |
| `WsfSimulation.cpp:1157-1321` | 可支持 input platform 注入和初始化流程 |
| `WsfFrameStepSimulation.cpp:111-252` | 可支持固定帧更新、事件执行和实时超时处理 |

## 结论

本批通过验证。下一步可以沿 `WsfPlatform::Update`、`WsfProcessor::Update`、`WsfSensor::Update`、`WsfEvent` 子类和 `WsfSimulationExtension` 注册点继续展开业务逻辑。
