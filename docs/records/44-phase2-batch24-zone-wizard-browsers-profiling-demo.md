# Phase 2 batch24 完成记录：Zone/Wizard 浏览器、Profiling 与 DemoMode

> **完成日期**：2026-07-08
> **阶段**：Phase 2 / 模块级粗粒度分析
> **状态**：已完成

## 分析范围

本批处理 6 个最小目录单元，覆盖 69 个 source/header 文件。`tools/profiling` 在工作清单中原计数偏小，实际 file-index 展开为 18 个 source/header。

| 最小目录单元 | source/header 数 | 中文说明 |
|--------------|------------------|----------|
| `warlock/plugins/ZoneBrowser/source` | 10 | zone 数据复制、显示和颜色修改 |
| `wizard/plugins/OSMConverter/source` | 10 | OSM XML 到 AFSIM 场景片段转换 |
| `wizard/plugins/PlatformBrowser/source` | 10 | Wizard 平台树、组件和定义位置浏览 |
| `wizard/plugins/TypeBrowser/source` | 10 | Wizard 类型树、使用状态和定义位置浏览 |
| `tools/profiling` | 18 | profiling hooks 动态库加载和 region/section API |
| `warlock/plugins/DemoMode/source` | 11 | 演示模式运行速度控制 |

## 业务逻辑承接价值

| 入口 | 价值 |
|------|------|
| `WkZoneBrowser::SimInterface::InterpretZoneSet` | 可追 WsfZoneDefinition/ZoneSet 到 UI 数据结构 |
| `OSMConverterDataContainer::ParseFile` | 可追 OSM XML 到 AFSIM 输出片段转换 |
| `PlatformBrowser::DockWidget::OnProxyUpdated` | 可追 parse/proxy 平台树到编辑器浏览 |
| `TypeBrowser::Model::ScanForTypes` | 可追 proxy type map 和类型定义/使用状态 |
| `profiling::ProfilingSystem` | 可追性能采样 hooks 动态加载和生命周期 |
| `WkDemoMode::RunSpeedCommand::Process` | 可追演示模式运行速度控制命令 |

## 已知问题与备注

1. `ZoneBrowser` 的颜色修改命令依赖 zone 名和平台名定位，重名 zone/path 语义需后续验证。
2. `OSMConverter` 的输出规则依赖过滤配置，需结合示例输入确认道路/要素字段映射；data container 的手工 `new` 生命周期和部分错误信息中的 id 值输出也需复核。
3. `PlatformBrowser` 与 `TypeBrowser` 均依赖 Wizard parse/proxy 状态，空项目、parse 未完成和 stale view 路径需 UI 验证；二者都有搜索结果选择未完整实现的迹象。
4. `ProfilingSystem` 明确要求只允许一个 profiling system 实例活跃；global hooks、region stack 和输出文件均为全局状态，误用会影响全局 hooks。
5. `DemoMode` 快捷键切换、最近场景重启顺序和自动选平台精确匹配需要运行验证。

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| 粗符号索引增量 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块概览 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch24-verify-report.md` |
