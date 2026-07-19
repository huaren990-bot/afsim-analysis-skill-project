# Phase 2 完成记录：batch37 IADS C2 iadsLib 与 Warlock core

> **完成日期**：2026-07-13
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `wsf_plugins/wsf_iads_c2_lib/iadsLib/source` | 54 | `VclInterceptCalculator::CanIntercept`、`assetRecord::calculateAssignmentDelays`、`unclassifiedBattleManager::run`、`unclassifiedBattleManager::PerformWeaponPairings`、`weaponsManagerAI::Clone` | IADS C2 库实现层，包含 asset/track/weapon/zone/message 记录、weapon pairing、battle manager 和 intercept 计算。 |
| `warlock/warlock_core/source` | 61 | `warlock::CoreSimInterface`、`warlock::CoreSimEvent`、`warlock::RunManager`、`wk::EventPipe`、`warlock::ScriptSimInterface` | Warlock core 公共库，提供插件基类、sim interface、core sim events、event pipe、run manager、script sim interface 和平台数据 UI。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 对 `iadsLib warlock_core` 查询命中大量 Warlock/WSF 通用事件噪声；本批最终以 `iadsLib/source` 的 `.cpp` 实现函数和 `warlock_core/source` 的核心 class 声明为准。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum/function，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `wsf_plugins/wsf_iads_c2_lib/iadsLib/source` | 防空 C2/武器分配高价值入口，后续应追 `AssetManagerInterface::processMessage` → `PrepareTracksForEvaluation` → `unclassifiedBattleManager::run` → `PerformWeaponPairings/AssignWeapons` → `DisseminateC2Interface::updateOutgoingMessages` 的 assignment/cue/status 消息链。 |
| `warlock/warlock_core/source` | Warlock 运行时插件基础设施入口，后续应追 `RunManager::StartLoading/LoadThread::run/SimThread::run`、`SimEnvironment::InitializeCallbacks`、`CoreSimInterface` → `CoreSimEvents::*::Process`、`SimInterfaceBase::AddSimCommand/ProcessCommands` 和 `EventPipe::RegisterEvents`。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch37-verify-report.md` |

## 已知问题

1. CodeGraph 对通用 `Plugin`、`Event`、`Command` 等名称存在跨目录噪声，正式归属以完整路径前缀为准。
2. `iadsLib/source` 主要是 `.cpp` 实现文件，代表符号以真实函数/方法定义为主，不伪造 header class 条目。
3. IADS 的武器配对、dynamic route、latent message 和 terrain/intercept 依赖可能直接影响 assignment 结果；后续需要按消息生命周期深挖。
4. Warlock core 的仿真线程、GUI 线程、网络包注册和 EventPipe extension 获取存在边界假设；Phase 2 只登记入口，线程/空指针风险需在函数级确认。

## 下游就绪

本批新增 2 个最小目录单元、115 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
