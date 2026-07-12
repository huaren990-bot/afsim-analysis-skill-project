# Phase 2 batch20 增量验证报告

> **验证日期**：2026-07-08
> **验证对象**：batch20 的 6 个最小目录单元
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|--------|------|------|
| 工作清单状态 | 通过 | 6 个目录已标记为 `done_batch20` |
| file-index 覆盖 | 通过 | batch20 目录均已补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions`、中文 `brief` |
| 粗符号索引 | 通过 | `symbol-index-phase2.jsonl` 新增/替换 42 个 batch20 符号 |
| 导出宏过滤 | 通过 | 插件注册宏保留为 notes 证据，未把导出宏作为正式符号 |
| Markdown 位置 | 通过 | 新增报告位于 `docs/records/` 与 `docs/verification/` |
| 子 agent 异常处理 | 通过 | 失败范围由主 agent 本地 CodeGraph/源码扫描补齐，失败 agent 未写入共享文件 |

## 按目录验证

| 目录 | source/header 数 | 粗符号数 | 主要证据 | 风险项 |
|------|------------------|----------|----------|--------|
| `mystic/plugins/ResultRelativeGeometry/source` | 8 | 8 | `BuildEntityContextMenu`、`DualPlatformUpdaterT::TimerRead`、`PlotUpdater::GetSeries` | 平台名空格协议、空序列边界 |
| `mystic/plugins/ResultScriptDataFeed/source` | 8 | 7 | `MsgScriptData` keyed map、`Interface::AdvanceTimeRead`、`PlotUpdater::GetSeries` | `MenuPlot()` 仅声明、锁内引用返回、平台 index 0 |
| `mystic/plugins/ResultSixDOF_Data/source` | 8 | 8 | `Interface::AdvanceTimeRead`、`PlotUpdater::GetSeries`、大量 `MsgSixDOF_*` | X 轴分支使用 `aYAxis`、构造函数空指针路径、平台 index 0 |
| `mystic/plugins/ResultStatistics/source` | 8 | 7 | `ShowStats`、`ShowEventList`、`EventTableModel::data` | 事件表巨大 switch 可维护性、扩展消息依赖 `rvEnv.GetExtensions()` |
| `tools/wkf/plugins/MapHoverInfo/source` | 8 | 7 | `HoverManager::HandleHoverEvent`、`GetPlatformString`、`GetNonPlatformString` | updater 缓存生命周期、tooltip 仅处理首个 hit |
| `tools/wkf/plugins/TetherView/source` | 8 | 5 | `BuildEntityContextMenu`、`ConnectToPlatform`、`LookAt`、`SaveSettings` | 多窗口对象名/生命周期、启动恢复只保存平台 tether |

## 结论

batch20 满足 Phase 2 增量要求。虽然两个子 agent 失败，但主 agent 已按相同证据规则补齐，最终索引、文档和验证结果一致。
