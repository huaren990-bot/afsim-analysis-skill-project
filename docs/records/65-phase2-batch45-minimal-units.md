# Phase 2 完成记录：batch45 sensor plot 与 air combat 插件

> **完成日期**：2026-07-15
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/core/sensor_plot_lib` | 44 | `WsfSensorPlotExtension`、`Register_sensor_plot_lib`、`WsfSensorPlotExtension::AddedToScenario`、`Function`、`MapPlotFunction` | AFSIM 传感器绘图/分析函数库，注册 antenna plot、map plot、lookup table、vertical coverage 等分析函数，并在临时仿真中采样输出。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_air_combat` | 34 | `Register_wsf_air_combat`、`WsfAirCombatTypeManager::AddedToScenario`、`WsfSA_Processor`、`WsfSA_Processor::ProcessInput`、`wsf::AirCombat::EventPipe` | 空战态势感知插件，注册 `WSF_SA_PROCESSOR`，提供感知、评估、预测与空战事件管道。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先按批次执行 CodeGraph 探索；对大范围噪声结果，按目录路径回落到源码扫描确认。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描注册入口、class/function、ProcessInput/Initialize/Update 和输出链，排除 `vx.json` 与导出宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览、批次记录和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `afsim-2_9/swdev/src/core/sensor_plot_lib` | `Register_sensor_plot_lib -> WsfSensorPlotExtension::AddedToScenario -> ProcessInput -> ExecutePlots -> RunFunction -> Function::Execute` 是 plot 执行链；`MapPlotFunction` 等派生类承接具体采样语义。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_air_combat` | `Register_wsf_air_combat -> WsfAirCombatTypeManager::AddedToScenario -> WSF_SA_PROCESSOR` 建立处理器；运行时 `WsfSA_Processor::ProcessInput/Update` 串起 perceive、assess、predict 和 event pipe 输出。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch45-verify-report.md` |

## 已知问题

| 单元 | 风险与待确认项 |
|------|------|
| `afsim-2_9/swdev/src/core/sensor_plot_lib` | 目录计数包含测试文件；部分函数算法未在本批深入；`RunFunction()` 在非 sensor_plot 模式可能直接 `exit(1)`。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_air_combat` | `WsfSA_Processor.cpp` 单文件职责很重；事件 schema 来自 utpack 生成链，尚未细化字段；processor/track/component 类型假设需在业务阶段验证。 |

## 下游就绪

本批新增 2 个最小目录单元、78 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
