# Phase 2 完成记录：batch38 wsf_spaceg 轨道任务编辑与 WizPostProcessor 报表插件

> **完成日期**：2026-07-13
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `tools/wkf/wsfg/wsf_spaceg/source` | 62 | `AstrolabeDockWidgetBase`、`AstrolabeConfig`、`ConfigWidgetFactory`、`OrbitalMissionModel`、`MissionVerifierBase::Verify` | WKF/WSFG 的 Astrolabe 轨道任务编辑核心库，负责 JSON 配置控件、mission sequence 模型、验证、模型/序列转换和轨道预览。 |
| `post_processor/WizPostProcessor/source` | 80 | `PostProcessor::Plugin`、`PostProcessor::ReportDialog`、`PostProcessor::ProxyInterface`、`PostProcessor::GeneralOutput`、`PostProcessor::ReportDialog::GenerateClickedHandler` | Wizard Post Processor 报表生成插件，提供 Communication、Detection、DSV、Eclipse、Engagement、Trajectory 等报表 UI，并把选择写成 post_processor 配置执行。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先执行批量 CodeGraph 查询；对通用 `Plugin/Event/Network` 等跨目录噪声，按完整路径回落到目录内源码扫描确认。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/function/registration/ProcessInput/输出入口，排除 `vx.json` 和导出宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览、批次记录和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `tools/wkf/wsfg/wsf_spaceg/source` | Astrolabe 业务入口链：`AstrolabeDockWidgetBase::OnVerify/OnApply` -> `MissionVerifierBase::Verify` -> `OrbitalModelToSequence::Transform` -> `OrbitalMissionVerificationContext::VerifyMission` -> `OrbitPreviewManager` 预览更新。 |
| `post_processor/WizPostProcessor/source` | 报表生成入口链：`PostProcessor::Plugin` 菜单 action -> `Show*Dialog` -> `ProxyInterface::Update` -> widget 候选项刷新 -> `ReportDialog::GenerateClickedHandler` -> `ReportWidget::WriteData` -> `Configuration::Execute`。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch38-verify-report.md` |

## 已知问题

1. CodeGraph 对通用名称存在跨目录噪声，本批正式索引只采纳完整路径落在本批目录内的源码证据。
2. 本批只修 Phase 2 粗索引；函数参数、重载、调用链和边界分支留给 Phase 3/4 或业务逻辑深挖。
3. `vx.json` 只作为存在事实，不进入本批 source/header 文件索引。

## 下游就绪

本批新增 2 个最小目录单元、142 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
