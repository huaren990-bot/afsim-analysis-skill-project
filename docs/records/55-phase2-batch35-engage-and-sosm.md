# Phase 2 完成记录：batch35 engage 核心与 SOSM 传感器模型

> **完成日期**：2026-07-13
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `engage/source` | 45 | `engage::Simulation`、`engage::TaskManager`、`engage::Events`、`engage::EventItem`、`engage::Task` | Engage 核心源码，提供 frame-step simulation、任务管理、事件采集、输出和传感器/武器交战事件模型。 |
| `wsf_plugins/wsf_sosm/sosm/source` | 45 | `SOSM_Manager`、`SOSM_Sensor`、`SOSM_SensorTarget`、`SOSM_Atmosphere`、`SOSM_Interaction` | SOSM 传感器/目标/大气/光谱交互模型源码，支撑 WSF SOSM 探测仿真。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 对 `engage source wsf_sosm sosm` 批量探索命中 `engage/source/Events.hpp`，确认 sensor/weapon/simulation 事件体系；WSF 通用事件和消息表命中为跨目录噪声，正式索引只采纳本批目录内符号。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum/function，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `engage/source` | 交战批运行高价值入口，后续应追 `main` → `TaskManager::Execute` → `Task::Execute` → `RunConfig::CreatePlatforms` → `Simulation::AdvanceTime/SimulationExtension` observer callbacks → `TaskOutput` 的事件、summary、Pk 输出链。 |
| `wsf_plugins/wsf_sosm/sosm/source` | 传感器探测业务高价值入口，后续应追 `SOSM_Manager::ProcessInput/Load*Type` → `SOSM_SensorTarget::Initialize` → `ComputeTargetIrradiance` → `SOSM_Sensor::ComputeProbabilityOfDetection`，并关联 atmosphere/target/interaction 表缓存。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch35-verify-report.md` |

## 已知问题

1. CodeGraph 对通用 `Plugin`、`Event`、`Command` 等名称存在跨目录噪声，正式归属以完整路径前缀为准。
2. Engage 的 `SimulationExtension::AddedToSimulation` 存在重复连接同类 sensor request 信号的迹象，后续需要验证是否导致事件重复输出。
3. SOSM 的 binary cache、共享表缓存和 simple atmosphere TODO 属于后续函数级风险点；Phase 2 只登记业务入口。
4. 本批只修 Phase 2 粗索引；函数级调用链、参数和分支语义留给 Phase 3/4 或业务逻辑深挖。

## 下游就绪

本批新增 2 个最小目录单元、90 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
