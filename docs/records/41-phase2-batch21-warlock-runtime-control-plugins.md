# Phase 2 batch21 完成记录：Warlock 运行时控制与显示插件

> **完成日期**：2026-07-08
> **阶段**：Phase 2 / 模块级粗粒度分析
> **状态**：已完成

## 分析范围

本批处理 6 个最小目录单元，覆盖 48 个 source/header 文件。`vx.json` 与 `CMakeLists.txt` 仅作为元数据/构建证据，不计入 source/header 统计。

| 最小目录单元 | source/header 数 | 中文说明 |
|--------------|------------------|----------|
| `warlock/plugins/BattleManagement/source` | 8 | 平台状态、damage/fuel、aux data 与 BM 规则刷新 |
| `warlock/plugins/Comment/source` | 8 | 仿真 comment 到地图 comment bubble/attachment |
| `warlock/plugins/CyberEngagementController/source` | 8 | cyber attack/scan 菜单与仿真命令 |
| `warlock/plugins/NetworkBrowser/source` | 8 | DIS/XIO 网络配置采集与 dock 展示 |
| `warlock/plugins/Orbit/source` | 8 | space mover 轨道、机动和月球轨道 UI 同步 |
| `warlock/plugins/Projector/source` | 8 | 传感器视场 terrain projector 自动增删与更新 |

## 执行方式

| 角色 | 数量 | 职责 |
|------|------|------|
| 主 agent | 1 | 在子 agent 失败后使用 CodeGraph 和窄范围源码证据完成分析、合并索引、写正式文档和验证 |
| 子 agent | 3 | 原计划每个 agent 处理 2 个目录；本批均因用量/连接限制失败，未写共享文件 |

本批最终证据均由主 agent 复核落地。CodeGraph 已用于定位关键类、事件、命令和调用链；源码窄范围扫描用于补充声明行和风险点。

## 产出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` | 更新 batch21 目录字段和中文 brief |
| 粗符号索引增量 | `workspace/source-index/symbol-index-phase2.jsonl` | 新增/替换 49 个 batch21 粗符号 |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 6 个目录标记为 `done_batch21` |
| 模块概览 | `docs/architecture/module-overview-v2-incremental.md` | 追加第 97-102 节 |
| 验证报告 | `docs/verification/phase2-followup-batch21-verify-report.md` | 记录覆盖、证据来源和风险项 |

## 业务逻辑承接价值

| 入口 | 价值 |
|------|------|
| `WkBM::SimInterface::SimulationClockRead` | 可追平台 damage/fuel、aux data 如何进入 Battle Management 状态和规则显示 |
| `WkComment::SimInterface::SimulationInitializing` | 可追 `WsfObserver::Comment` 如何映射到地图 comment bubble |
| `WkCyberEngagementController::CyberEngagementControllerCommand::Process` | 可追 UI 权限检查后如何调用 `CyberAttack` |
| `WkCyberEngagementController::CyberScanCommand::Process` | 可追 UI 权限检查后如何调用 `CyberScan` |
| `WkNetworkBrowser::SimInterface::SimulationStarting` | 可追 DIS/XIO 网络配置和 UDP target 如何被采集展示 |
| `WkOrbit::SimInterface::OnSpaceMoverUpdate` | 可追 space mover 轨道元素、机动状态和 orbit UI 的同步链 |
| `Projector::SimInterface::OnSensorUpdate` | 可追 sensor mode/beam/EM receiver/FOV 到 terrain projector 的显示链 |

## 已知问题与备注

1. `BattleManagement` 的 `RuleSetWeaponCount` 仍有 TODO 语义，后续分析 weapon count 规则时不能把当前显示当成完整业务规则。
2. `CyberEngagementController` 只暴露不需要额外输入的 attack type，并排除 `WSF_CYBER_ATTACK` 基类类型；后续需要追 `wsf::cyber::ScenarioExtension` 的 attack type 定义。
3. `NetworkBrowser` 是配置/运行状态审计入口，不直接改变仿真业务状态。
4. `ProjectorSimInterface` 多处用 `GetAzimuthFieldOfView` 填充 elevation 范围，疑似应调用 elevation FOV；后续若进入修复阶段应重点验证。

## 下游就绪

batch21 为后续 AFSIM 业务逻辑分析补齐了 Battle Management、Comment、Cyber、Network、Orbit、Projector 六类 Warlock 运行时入口，覆盖状态观察、用户命令、网络审计、轨道同步和传感器视场显示链。
