# Phase 2 batch23 完成记录：Warlock 数据插件与 Wizard 表格工具

> **完成日期**：2026-07-08
> **阶段**：Phase 2 / 模块级粗粒度分析
> **状态**：已完成

## 分析范围

本批处理 6 个最小目录单元，覆盖 59 个 source/header 文件。

| 最小目录单元 | source/header 数 | 中文说明 |
|--------------|------------------|----------|
| `wizard/plugins/TablePlotter/source` | 9 | AFSIM table/curve 与 CSV 绘图工具 |
| `warlock/plugins/CreatePlatform/source` | 10 | 运行时创建平台 UI 和仿真命令 |
| `warlock/plugins/OrbitalData/source` | 10 | 空间平台轨道六要素显示和绘图 |
| `warlock/plugins/P6DOF_Data/source` | 10 | P6DOF mover 飞行状态显示和绘图 |
| `warlock/plugins/PlatformData/source` | 10 | 平台通用状态、DIS/XIO、aux data 显示 |
| `warlock/plugins/SixDOF_Data/source` | 10 | SixDOF mover 飞行状态显示和绘图 |

## 业务逻辑承接价值

| 入口 | 价值 |
|------|------|
| `AFSIM_Parser::InterpretInput` | 可追 AFSIM table/curve 配置如何被解释成曲线 |
| `WkCreatePlatform::CreatePlatformCommand::Process` | 可追 UI runtime mutation 到 `WsfSimulation::AddPlatform` |
| `WkOrbitalData::SimInterface::WallClockRead` | 可追 space mover/DIS space platform 到轨道数据展示 |
| `WkP6DOF_Data::SimInterface::WallClockRead` | 可追 P6DOF mover 飞行/燃油/控制字段 |
| `WkPlatformData::SimInterface::WallClockRead` | 可追平台通用状态、DIS/XIO locality 和 aux data |
| `WkSixDOF_Data::SimInterface::WallClockRead` | 可追 SixDOF mover 飞行/燃油/控制字段 |

## 已知问题与备注

1. `CreatePlatformDockWidget::CreatePlatform()` 中纬度校验重复调用 latitude，longitude 校验疑似遗漏。
2. `CreatePlatformCommand::Process()` 对 `Clone(mType)` 返回空的路径缺少防护，创建平台后释放所有权给 simulation，后续失败/异常路径需结合 `AddPlatform` 语义验证。
3. `TablePlotter` 的 CSV 判断使用 `contains(".csv")`，大小写和复合后缀不严谨；右键命令动作创建 dialog 的生命周期也需确认。
4. `P6DOF_Data` 与 `SixDOF_Data` 类结构高度相似，后续应对照 mover 字段差异和 plot X/Y 轴逻辑。
5. `PlatformData` 对 aux data container 类型只记录 `"unknown_type"`，嵌套属性语义可能丢失。

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| 粗符号索引增量 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块概览 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch23-verify-report.md` |
