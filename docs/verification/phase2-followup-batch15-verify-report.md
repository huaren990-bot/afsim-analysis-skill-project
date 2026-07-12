# Phase 2 batch15 增量验证报告

> 日期：2026-07-07
> 范围：`Performance`、`AcesDisplay`、`AirCombatVisualization`、`Annotation`、`ApplicationLauncher`、`CommVis`

## 1. 检查结果汇总

| 检查项 | 结果 | 证据 |
|--------|------|------|
| 批次目录覆盖 | 通过 | 6 个最小目录单元均已写入 `phase2-analysis-unit-worklist.jsonl`，状态为 `done_batch15`。 |
| source/header 覆盖 | 通过 | 每个目录 6 个 source/header，共 36 个文件均在 `file-index.jsonl` 中保留并补充 `analysis_unit`。 |
| 符号去噪 | 通过 | `symbol-index-phase2.jsonl` 仅追加真实 class 符号，未把 `WKF_PLUGIN_DEFINE_SYMBOLS` 或 `*_EXPORT` 宏作为业务符号。 |
| 证据链 | 通过 | 每个目录均记录插件入口、仿真接口、事件类或 UI 类的源码行号证据。 |
| Markdown 位置 | 通过 | 新增 Markdown 产物均位于 `docs/records` 或 `docs/verification`，未向 `workspace` 写入 Markdown。 |

## 2. 按目录验证

| 单元 | 文件数 | 精化符号数 | 业务入口判断 | 风险 |
|------|--------|------------|--------------|------|
| Performance | 6 | 3 | 否，开发者诊断 UI | 无阻塞项 |
| AcesDisplay | 6 | 3 | 部分，是 ACES/SA 观察入口 | 上游业务语义需继续追 |
| AirCombatVisualization | 6 | 7 | 部分，是空战显示观察入口 | `try_lock` 跳过、target/菜单路径需复核 |
| Annotation | 6 | 3 | 否，是 annotation 显示桥 | 非空假设需复核 |
| ApplicationLauncher | 6 | 3 | 否，是工具启动入口 | 无阻塞项 |
| CommVis | 6 | 6 | 部分，是通信行为观察入口 | 通信事件来源需继续追 |

## 3. 结论

batch15 通过 Phase 2 增量验证。该批主要补齐 Warlock 运行时显示/工具插件，其中 `AcesDisplay`、`AirCombatVisualization`、`CommVis` 可作为下一步 AFSIM 业务逻辑分析的观察侧入口，但核心业务规则仍应向上追运行时模型、SA、weapon engagement、communication 生产方。
