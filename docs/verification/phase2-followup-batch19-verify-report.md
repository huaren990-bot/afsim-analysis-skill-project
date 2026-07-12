# Phase 2 batch19 增量验证报告

> **验证日期**：2026-07-08
> **验证对象**：batch19 的 6 个最小目录单元
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|--------|------|------|
| 工作清单状态 | 通过 | 6 个目录已标记为 `done_batch19` |
| file-index 覆盖 | 通过 | batch19 目录均已补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions`、中文 `brief` |
| 粗符号索引 | 通过 | `symbol-index-phase2.jsonl` 新增/替换 45 个 batch19 符号，均含路径与行号 |
| 导出宏过滤 | 通过 | 未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为正式符号写入 |
| Markdown 位置 | 通过 | 新增报告写入 `docs/records/` 与 `docs/verification/`，未在 `workspace/` 写入 Markdown |
| 业务逻辑承接 | 通过 | 已标出 alternate location、recording merge、orbital、P6DOF、platform data 的 Phase3/4 深挖入口 |

## 按目录验证

| 目录 | source/header 数 | 粗符号数 | 主要证据 | 风险项 |
|------|------------------|----------|----------|--------|
| `wsf_plugins/wsf_alternate_locations/source` | 7 | 10 | `Component::ProcessInput`、`Component::PreInitialize`、`ComponentInitialized` | 引用平台 availability、`offset_lla` 单位/越界语义需深挖 |
| `mystic/plugins/ResultMerger/source` | 8 | 7 | `MergerThread::run`、`InitializeSerializer`、`PlatformDatabase` | 时间排序、`simIndex()==0` 过滤策略需验证 |
| `mystic/plugins/ResultOrbitalData/source` | 8 | 7 | `Interface::GenerateOrbitalData`、`PlotUpdater::GetSeries` | 平台 index 0 语义、采样性能需确认 |
| `mystic/plugins/ResultP6DOFData/source` | 8 | 9 | `Interface::AdvanceTimeRead`、`PlotUpdater::GetMessageType` | deprecated 插件、KTAS/KCAS 字段疑点、plot X 轴取值疑点 |
| `mystic/plugins/ResultPlatformBrowser/source` | 8 | 5 | `Plugin::GuiUpdate`、`Interface::ShowInactiveChanged` | 仅为薄适配层，核心平台浏览逻辑在外部 WKF 组件 |
| `mystic/plugins/ResultPlatformData/source` | 8 | 7 | `Interface::AdvanceTimeRead`、`PlotUpdater::GetData`、data ring 菜单 | `infoPtr` 空指针路径、平台 index 语义、`FuelUpdater` 注册疑点 |

## 结论

batch19 产物满足 Phase 2 增量要求。该批对 AFSIM 业务逻辑分析的价值集中在：平台初始位置配置规则、recording 合并规则、空间轨道数据转换、平台结果字段消费和 P6DOF/SixDOF 对照。
