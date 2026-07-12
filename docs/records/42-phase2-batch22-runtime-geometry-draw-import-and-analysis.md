# Phase 2 batch22 完成记录：运行时几何、绘制、导入与场景检查

> **完成日期**：2026-07-08
> **阶段**：Phase 2 / 模块级粗粒度分析
> **状态**：已完成

## 分析范围

本批处理 6 个最小目录单元，覆盖 49 个 source/header 文件。`vx.json` 与 `CMakeLists.txt` 仅作为元数据/构建证据，不计入 source/header 统计。

| 最小目录单元 | source/header 数 | 中文说明 |
|--------------|------------------|----------|
| `warlock/plugins/RelativeGeometry/source` | 8 | 双平台相对几何查看与绘图 |
| `warlock/plugins/WsfDraw/source` | 8 | WSF draw 命令到 Warlock viewer overlay |
| `wizard/plugins/CRDImporter/source` | 8 | CRD 文件导入和转换 UI |
| `wsf_plugins/wsf_argo8/argo8/source` | 8 | ARGO8 外部导弹模型适配层 |
| `wsf_plugins/wsf_scenario_analyzer/source` | 8 | 场景质量/配置规则检查脚本插件 |
| `warlock/plugins/Scoreboard/source` | 9 | 武器发射/命中/击杀/未命中统计面板 |

## 执行方式

| 角色 | 数量 | 职责 |
|------|------|------|
| 主 agent | 1 | 使用 CodeGraph/源码扫描复核，合并 JSONL、正式报告和验证 |
| 子 agent | 1 | 只读分析 batch22 6 个目录，未写共享文件 |

## 业务逻辑承接价值

| 入口 | 价值 |
|------|------|
| `RelativeGeometry::DualPlatformUpdaterT` | 可追双平台相对几何计算和 plot 数据来源 |
| `WkWsfDraw::SimInterface::HandleDrawPkt` | 可追 XIO/network draw 包如何映射为 viewer overlay |
| `CrdImporter::Dialog::ImportPushButtonClicked` | 可追 CRD 文件到 AFSIM 输入片段的转换入口 |
| `Argo8Missile::Update` | 可追 ARGO8 导弹飞行、引信和终止状态 |
| `ScenarioAnalyzerRegisterScriptTypes` | 可追场景检查规则如何暴露给脚本 |
| `WkScoreboard::SimInterface::SimulationInitializing` | 可追 weapon fired/terminated observer 到战果统计 |

## 已知问题与备注

1. `RelativeGeometryPlugin.cpp` 使用空格拆分复合平台名，平台名含空格时可能脆弱。
2. `WsfDrawSimInterface::HandleDrawPkt()` 明确映射前两个顶点的平台索引，多顶点网络绘制需继续验证。
3. `CRDImporter` 的局部 `ImportWorker` 与 thread 生命周期需要结合 `CrdFileImporter` 进一步确认。
4. `Argo8Missile` 对未知模型类型和空 `mArgoModel` 的路径需要后续缺陷验证。
5. `Scoreboard` 在仿真完成事件中清空数据，是否符合“结束后查看最终统计”的使用预期需确认。

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| 粗符号索引增量 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块概览 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch22-verify-report.md` |
