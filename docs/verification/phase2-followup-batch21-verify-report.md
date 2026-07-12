# Phase 2 batch21 增量验证报告

> **验证日期**：2026-07-08
> **验证对象**：batch21 的 6 个最小目录单元
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|--------|------|------|
| 工作清单状态 | 通过 | 6 个目录已标记为 `done_batch21` |
| file-index 覆盖 | 通过 | batch21 目录均已补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions`、中文 `brief` |
| 粗符号索引 | 通过 | `symbol-index-phase2.jsonl` 新增/替换 49 个 batch21 符号 |
| 导出宏过滤 | 通过 | 插件注册宏保留为 notes 证据，未把导出宏作为正式符号 |
| Markdown 位置 | 通过 | 新增报告位于 `docs/records/` 与 `docs/verification/` |
| 子 agent 异常处理 | 通过 | 子 agent 因用量/连接限制失败；共享文件仅由主 agent 写入并复核 |

## 按目录验证

| 目录 | source/header 数 | 粗符号数 | 主要证据 | 风险项 |
|------|------------------|----------|----------|--------|
| `warlock/plugins/BattleManagement/source` | 8 | 10 | `Plugin::GuiUpdate`、`SimInterface::PlatformAdded`、`SimulationClockRead`、BM rule sets | weapon count TODO、aux data key 语义需向生产方追踪 |
| `warlock/plugins/Comment/source` | 8 | 7 | `WsfObserver::Comment`、`AddEvent::Process`、`DataContainer`、cleanup 超时逻辑 | `SimIntializedEvent` 拼写沿用源码；comment 生命周期依赖偏好和容器清理 |
| `warlock/plugins/CyberEngagementController/source` | 8 | 7 | `BuildEntityContextMenu`、权限检查、`CyberAttack`、`CyberScan` | 只覆盖无需额外输入 attack type；attack type 语义需追 cyber extension |
| `warlock/plugins/NetworkBrowser/source` | 8 | 8 | `SimulationStarting` 采集 DIS/XIO、`InitialEvent`、`DockWidget::RebuildDisplay` | 只在启动时采集，动态网络变化未见刷新链 |
| `warlock/plugins/Orbit/source` | 8 | 9 | `PlatformInitialized`、`OnSpaceMoverUpdate`、`OrbitUpdateEvent::Execute`、maneuver observer | 周期 1s/500s 更新策略需结合性能和 UI 刷新需求验证 |
| `warlock/plugins/Projector/source` | 8 | 8 | `BuildEntityContextMenu`、install/uninstall updater、`OnSensorUpdate`、`CheckProjectability` | elevation 范围疑似错误复用 azimuth FOV；mode/beam 空指针路径需验证 |

## 结论

batch21 满足 Phase 2 增量要求。虽然子 agent 未能产出有效结果，主 agent 已按 CodeGraph 优先和源码交叉确认规则完成全部 6 个最小目录单元，索引、文档和验证结果一致。
