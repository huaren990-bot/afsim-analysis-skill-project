# Phase 2 batch14 Mystic Result Views

> 日期：2026-07-07
> 范围：4 个最小目录单元，24 个 source/header 文件

## 1. 批次范围

| # | 最小目录单元 | source/header | 定位 |
|---|--------------|---------------|------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultAuxData/source` | 6 | AuxData 平台数据树与绘图消费端 |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultInteractionPlots/source` | 6 | InteractionDb waterfall plot 消费端 |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultSatelliteTether/source` | 6 | 空间平台 satellite tether 可视化 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultTracks/source` | 6 | TrackDb 航迹结果可视化与追踪解释 |

## 2. 关键结论

| 单元 | 后续业务分析价值 | 说明 |
|------|------------------|------|
| ResultAuxData | 低 | 只展示 `MsgAuxData`，业务语义在生产方。 |
| ResultInteractionPlots | 中低 | 揭示 Mystic 关注的交互类型，但业务链路应追 `InteractionDb::AddMessage`。 |
| ResultSatelliteTether | 低到中 | 连接 `ResultDataSpace`、轨道元素和相对轨迹可视化。 |
| ResultTracks | 高 | `TraceTrackId`、`TrackDb`、local/sensor track 链路是后续航迹业务分析重点。 |

## 3. 已更新产物

| 产物 | 更新 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 为 24 个 source/header 补入 batch14 精化职责、关键符号和函数。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 删除旧粗符号，新增 batch14 精化符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 将 4 个目录标记为 `done_batch14`。 |
| `docs/architecture/module-overview-v2-incremental.md` | 新增第 57-60 节。 |
| `docs/verification/phase2-followup-batch14-verify-report.md` | 新增本批验证报告。 |

## 4. 保留复核项

| 单元 | 复核项 |
|------|--------|
| ResultAuxData | UI 旧节点删除逻辑被注释，可能产生 stale data。 |
| ResultInteractionPlots | 手工锁/解锁 `InteractionDb`；未闭合区间拼接展示正确性。 |
| ResultSatelliteTether | 空平台直接解引用；`rvEnv.GetData()` 判空顺序；`mWidgetNamer` 初始化。 |
| ResultTracks | `PlotUpdater::CollectContributorData()` 可能未释放 `TraceTrackId` 返回指针；TrackDb 手工锁早退安全。 |
