# Phase 2 batch17 增量验证报告

> 日期：2026-07-07
> 范围：`VisualEffects`、`ColorUtils`、`DemoBrowser`、`LogServer`、`MapRoute`、`PlatformData`

## 1. 检查结果汇总

| 检查项 | 结果 | 证据 |
|--------|------|------|
| 批次目录覆盖 | 通过 | 6 个最小目录单元均已写入 `phase2-analysis-unit-worklist.jsonl`，状态为 `done_batch17`。 |
| source/header 覆盖 | 通过 | 每个目录 6 个 source/header，共 36 个文件均在 `file-index.jsonl` 中补充 `analysis_unit`。 |
| 符号去噪 | 通过 | 仅追加真实 class/struct/enum 符号；插件注册宏和导出宏未作为业务符号。 |
| 证据来源 | 通过 | `VisualEffects`、`DemoBrowser` 主插件、`LogServer` 主插件使用 CodeGraph；CodeGraph 未覆盖的 Qt 辅助文件已回退文本证据并在 notes 标记。 |
| Markdown 位置 | 通过 | 新增 Markdown 产物均位于 `docs/` 下。 |

## 2. 按目录验证

| 单元 | 文件数 | 精化符号数 | 业务入口判断 | 风险 |
|------|--------|------------|--------------|------|
| VisualEffects | 6 | 7 | 中价值显示消费侧 | fallthrough 和 effect 生命周期需复核 |
| ColorUtils | 6 | 2 | 否，编辑器颜色工具 | editor/tip 生命周期需复核 |
| DemoBrowser | 6 | 4 | 否，demo 浏览工具 | rst/search/UI 生命周期需复核 |
| LogServer | 6 | 3 | 中价值日志入口 | thread/连接清理需复核 |
| MapRoute | 6 | 4 | 高价值 route 语义入口 | altitude/reference/watcher 需复核 |
| PlatformData | 6 | 13 | 中价值平台字段入口 | 默认值和状态清理需复核 |

## 3. 结论

batch17 通过 Phase 2 增量验证。该批中 `MapRoute` 是最重要的业务逻辑承接入口，可继续追 `WsfPM_Mover`、`WsfPM_Route`、`WsfPathComputer` 和 route/orbit 编辑写回链路；`PlatformData` 与 `LogServer` 可作为平台字段和运行日志辅助入口；`ColorUtils`、`DemoBrowser` 主要是 Wizard 工具能力。
