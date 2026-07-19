# Phase 2 batch39 增量验证报告

> **验证日期**：2026-07-13
> **验证对象**：wsf_nx 非公开扩展与 utilosg 可视化基础库
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 最小目录单元数量 | 通过 | 2 个目录已标记为 `done_batch39`。 |
| file-index 覆盖 | 通过 | 294 个 source/header 均写入批次、系统、子系统、analysis_unit 和中文说明。 |
| 粗符号索引 | 通过 | 10 条代表性符号均来自本批目录边界内源码。 |
| EXPORT 过滤 | 通过 | 新增符号未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为业务符号。 |
| 同名模块消歧 | 通过 | CodeGraph 跨目录命中已按完整路径过滤。 |
| Markdown 位置 | 通过 | 批次记录和验证报告均位于 `docs/` 下。 |

## 按目录验证

| 单元 | source/header | 代表性符号 | 判定 |
|------|------:|------|------|
| `core/wsf_nx/source` | 72 | `Register_wsf_nx`、`WsfNonExportableExtension::AddedToScenario`、`WsfChaffWeapon::DropChaffCloud`、`WsfEM_ALARM_Propagation`、`WsfCoherentSensorProcessor::ProcessResults` | 通过 |
| `tools/utilosg` | 222 | `UtoViewer`、`UtoWorld`、`UtoResourceDB`、`UtoShapeFactory`、`DtedTmsTileSource::createImage` | 通过 |

## CodeGraph 与源码交叉验证

本批先使用 CodeGraph 批量探索，再用目录内源码扫描确认符号归属。对 `Plugin`、`Event`、`Network`、`Coverage` 等通用名称，最终以 `analysis_unit` 路径前缀和源码行号为准。

## 已确认的业务入口

| 单元 | 入口 |
|------|------|
| `core/wsf_nx/source` | 扩展注册和业务链：`Register_wsf_nx` -> `WsfNonExportableExtension::AddedToScenario` 注册类型 -> `WSF_CHAFF_WEAPON/ejector` 或传感器处理器配置 -> `DropChaffCloud/EjectParcel` 或 `WsfCoherentSensorProcessor::ProcessResults`。 |
| `tools/utilosg` | 可视化入口链：应用创建 `UtoViewer` -> `UtoWorld`/window/overlay manager -> `UtoResourceDB` 解析资源定义 -> `UtoShapeFactory/UtoTerrainFactory` 创建对象 -> OSG scene graph 渲染；外部资源走 `ReaderWriter*.readNode` 和 `DtedTmsTileSource::createImage`。 |

## 已知风险

本批包含 UI 工具库、可视化基础设施和仿真业务扩展。Phase 2 已确认入口、边界和代表性符号；具体算法正确性、线程/资源生命周期、输入合法性和输出格式一致性需在后续函数级分析中验证。
