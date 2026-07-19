# Phase 2 完成记录：batch52 WKF core Qt/VESPA 基础库

> **完成日期**：2026-07-15
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/tools/wkf/core/source` | 165 | `wkf::Environment`、`wkf::PluginManager`、`wkf::Plugin`、`wkf::VtkEnvironment`、`wkf::MainWindow` | WKF Qt/VESPA 基础库，覆盖 Environment 单例、MainWindow、Plugin/PluginManager、VtkEnvironment、Scenario/Viewer/Platform、Observer、配置/权限/资源/单位。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先用 CodeGraph 批量探索批次范围；对 residual/资源/测试/grammar 等 CodeGraph 弱项，回落到目录内 `rg` 与文件清单。 |
| 子 agent 分片 | 6 个 explorer | batch47-batch52 分别读取互不重叠目录，只输出证据摘要，不写共享文件。 |
| 主 agent 合并 | 主 agent | 更新 JSONL、模块总览、批次记录和验证报告；父级 residual 不覆盖已完成子目录归属。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `afsim-2_9/swdev/src/tools/wkf/core/source` | `Environment::Create -> Environment ctor -> MainWindow::InitializeDialogs -> Environment::StartUp -> PluginManager::Initialize/LoadPluginInitialize -> QTimer TimerHandler/UpdateFrame`。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch52-verify-report.md` |

## 已知问题

| 单元 | 风险与待确认项 |
|------|------|
| `afsim-2_9/swdev/src/tools/wkf/core/source` | core 中无正式 WkfDocument；sim interface 是显示侧；插件 unload 直接 delete 有生命周期风险；插件 ABI 依赖版本/符号/tag。 |

## 下游就绪

本批新增/闭环 1 个最小目录单元、165 个 source/header 和 5 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
