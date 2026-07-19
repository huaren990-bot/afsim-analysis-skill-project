# Phase 2 完成记录：batch39 wsf_nx 非公开扩展与 utilosg 可视化基础库

> **完成日期**：2026-07-13
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `core/wsf_nx/source` | 72 | `Register_wsf_nx`、`WsfNonExportableExtension::AddedToScenario`、`WsfChaffWeapon::DropChaffCloud`、`WsfEM_ALARM_Propagation`、`WsfCoherentSensorProcessor::ProcessResults` | WSF NX 非公开扩展能力包，注入高级雷达/电磁传播、天线模型、相干传感器融合、TRIMSIM、chaff 云/箔条武器与 EW 效果。 |
| `tools/utilosg` | 222 | `UtoViewer`、`UtoWorld`、`UtoResourceDB`、`UtoShapeFactory`、`DtedTmsTileSource::createImage` | AFSIM 工具侧 OSG 可视化基础库，提供 viewer/window/world/overlay/entity/resource/shape/terrain 抽象和 OSG/osgEarth 资源插件。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先执行批量 CodeGraph 查询；对通用 `Plugin/Event/Network` 等跨目录噪声，按完整路径回落到目录内源码扫描确认。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/function/registration/ProcessInput/输出入口，排除 `vx.json` 和导出宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览、批次记录和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `core/wsf_nx/source` | 扩展注册和业务链：`Register_wsf_nx` -> `WsfNonExportableExtension::AddedToScenario` 注册类型 -> `WSF_CHAFF_WEAPON/ejector` 或传感器处理器配置 -> `DropChaffCloud/EjectParcel` 或 `WsfCoherentSensorProcessor::ProcessResults`。 |
| `tools/utilosg` | 可视化入口链：应用创建 `UtoViewer` -> `UtoWorld`/window/overlay manager -> `UtoResourceDB` 解析资源定义 -> `UtoShapeFactory/UtoTerrainFactory` 创建对象 -> OSG scene graph 渲染；外部资源走 `ReaderWriter*.readNode` 和 `DtedTmsTileSource::createImage`。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch39-verify-report.md` |

## 已知问题

1. CodeGraph 对通用名称存在跨目录噪声，本批正式索引只采纳完整路径落在本批目录内的源码证据。
2. 本批只修 Phase 2 粗索引；函数参数、重载、调用链和边界分支留给 Phase 3/4 或业务逻辑深挖。
3. `vx.json` 只作为存在事实，不进入本批 source/header 文件索引。

## 下游就绪

本批新增 2 个最小目录单元、294 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
