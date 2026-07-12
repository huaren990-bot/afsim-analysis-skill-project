# Phase 2 完成记录：batch26 任务、航迹、项目浏览、Brawler 与 cyber 浏览

> **完成日期**：2026-07-10
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 结论 |
|------|------:|------|
| `warlock/plugins/TaskAssigner/source` | 12 | Warlock 任务分派操作入口。 |
| `warlock/plugins/TaskStatus/source` | 12 | Warlock 任务状态显示和取消入口。 |
| `warlock/plugins/TrackDetailsDisplay/source` | 12 | Warlock 平台/本地航迹详情显示入口。 |
| `wizard/plugins/ProjectBrowser/source` | 12 | Wizard 项目文件树、外部文件和打开/新建动作入口。 |
| `wsf_plugins/wsf_brawler/brawler/source` | 12 | Brawler 空战 mover、平台、决策和评估核心源码片段。 |
| `warlock/plugins/CyberEngagementBrowser/source` | 13 | Warlock cyber engagement 事件浏览入口。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 只读取证 | CodeGraph 命中部分 UCI 生成代码噪声，最终以目录边界内源码为准。 |
| 目录内批量扫描 | 主 agent | 抽取真实 class/struct/enum 行号，并过滤 `*_EXPORT` 宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块概览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `TaskAssigner` | `AssignTaskCommand`、`MilAssignJammerTaskCommand`、`MilAssignWeaponTaskCommand` 是任务分派入口。 |
| `TaskStatus` | `TaskUpdateEvent` 与 `CancelTaskCommand` 是任务状态观察和取消入口。 |
| `TrackDetailsDisplay` | `TrackDataExtractor` 是本地航迹、平台航迹和 sensor track 消费入口。 |
| `ProjectBrowser` | 支撑场景项目文件定位，不作为运行时业务规则入口。 |
| `brawler/source` | `BrawlerMover`、`BrawlerMIND`、`BrawlerEvaluation` 是空战机动/决策分析入口。 |
| `CyberEngagementBrowser` | `CyberEngagementEvent` 是 cyber 交战结果消费入口。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch26-verify-report.md` |

## 已知问题

1. `TaskStatus` 名称会被 CodeGraph 搜到 UCI generated `TaskStatus*` 类型，本批已按目录边界过滤。
2. `TrackDetailsDisplay` 中 raw/local track 类型判断存在可疑条件，后续应在 Phase 3/4 复核 `TrackDetailsSimInterface.cpp` 的 sensor track 分支。
3. `brawler/source` 是核心业务代码，Phase 2 只定位入口；机动算法和 MIND 决策需 Phase 3/4 深挖。

## 下游就绪

本批把任务分派/状态、航迹显示、Brawler 空战和 cyber 结果消费纳入 Phase 2 可追溯索引，可作为后续业务流追踪入口。
