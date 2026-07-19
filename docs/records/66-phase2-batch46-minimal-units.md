# Phase 2 完成记录：batch46 WKF 空战可视化公共库与 PatternVisualization

> **完成日期**：2026-07-15
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/tools/wkf/air_combat/wkf_air_combat_common/source` | 94 | `wkf::DataContainer`、`wkf::AirCombatDataEngagementSummary`、`wkf::AirCombatDisplayInterface`、`wkf::SA_Display::PluginBase`、`wkf::AcesDisplay::PluginBase` | WKF 空战可视化公共库，提供 SA、ACES、HUD、HDD 与 overlay 绘制的数据容器、显示接口和 Qt/OSG 插件基类。 |
| `afsim-2_9/swdev/src/wizard/plugins/PatternVisualization/source` | 95 | `PatternVisualizer::Plugin`、`PatternVisualizer::Session`、`PatternVisualizer::Pattern`、`PatternVisualizer::PatternData`、`PatternVisualizer::Canvas` | Wizard 天线 pattern 与雷达/光学/红外/声学 signature 可视化插件，生成临时 SigView 输入，构建会话并用 Qt/OpenGL 渲染 2D/3D pattern。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先按批次执行 CodeGraph 探索；对大范围噪声结果，按目录路径回落到源码扫描确认。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描注册入口、class/function、ProcessInput/Initialize/Update 和输出链，排除 `vx.json` 与导出宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览、批次记录和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `afsim-2_9/swdev/src/tools/wkf/air_combat/wkf_air_combat_common/source` | `AirCombatDisplayInterface::Update` 消费 `DataContainer` 中的 engagement、fuel、weapons、track、SA 等字段更新 decorators/interactions/overlays；SA/ACES 插件通过 context menu 接入平台显示。 |
| `afsim-2_9/swdev/src/wizard/plugins/PatternVisualization/source` | `Plugin::RunPatternVisualization -> DockWidget::ReadPatternFile -> Session::LoadPatterns -> Session::RequestPatternUpdate -> PatternUpdateManager -> Canvas::AddOrUpdatePattern/paintGL` 是从 Wizard 节点到 pattern 渲染的主链。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch46-verify-report.md` |

## 已知问题

| 单元 | 风险与待确认项 |
|------|------|
| `afsim-2_9/swdev/src/tools/wkf/air_combat/wkf_air_combat_common/source` | 数据填充主要来自外部插件/结果消息；`HasSituationAwarenessProcessor` 默认 true；Qt/OSG 生命周期、raw pointer 与 callback 混合使用需关注。 |
| `afsim-2_9/swdev/src/wizard/plugins/PatternVisualization/source` | `PatternData` 固定 720x360 网格有 CPU/内存成本；`PatternUpdateManager::mPendingUpdates` 跨 GUI/worker 线程需复核同步；存在 `accoustic_signature` 拼写兼容风险。 |

## 下游就绪

本批新增 2 个最小目录单元、189 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
