# Phase 2 batch35 增量验证报告

> **验证日期**：2026-07-13
> **验证对象**：engage 核心与 SOSM 传感器模型
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 2 个目录已标记为 `done_batch35`。 |
| file-index 覆盖 | 通过 | 90 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 10 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤，未写入不属于本批目录的符号。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `engage/source` | 45 | `engage::Simulation`、`engage::TaskManager`、`engage::Events`、`engage::EventItem`、`engage::Task` | 通过 |
| `wsf_plugins/wsf_sosm/sosm/source` | 45 | `SOSM_Manager`、`SOSM_Sensor`、`SOSM_SensorTarget`、`SOSM_Atmosphere`、`SOSM_Interaction` | 通过 |

## CodeGraph 与源码交叉验证

CodeGraph 对 `engage source wsf_sosm sosm` 批量探索命中 `engage/source/Events.hpp`，确认 sensor/weapon/simulation 事件体系；WSF 通用事件和消息表命中为跨目录噪声，正式索引只采纳本批目录内符号。

本批最终索引以目录边界内的源码声明或真实函数定义为准；跨目录命中仅记录为噪声或后续追踪线索，不直接写入本批 symbol-index。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `engage/source` | `main`、`TaskManager::Execute`、`Task::Execute`、`RunConfig::CreatePlatforms`、`SimulationExtension::AddedToSimulation`、`TaskOutput` |
| `wsf_plugins/wsf_sosm/sosm/source` | `SOSM_Manager::ProcessInput/Load*Type`、`SOSM_SensorTarget::Initialize/ComputeTargetIrradiance`、`SOSM_Sensor::ComputeProbabilityOfDetection`、`SOSM_BinaryIO` |

## 已知风险

本批包含业务核心和工具基础库混合目录。Phase 2 只确认入口、边界和代表性符号；具体规则解释需要在下一步沿命令处理、事件生产、配置输入、运行时状态和输出数据继续追踪。
