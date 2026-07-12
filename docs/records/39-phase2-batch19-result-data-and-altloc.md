# Phase 2 batch19 完成记录：alternate locations 与 Mystic 结果数据插件

> **完成日期**：2026-07-08
> **阶段**：Phase 2 / 模块级粗粒度分析
> **状态**：已完成

## 分析范围

本批按最小目录单元处理 6 个目录，覆盖 47 个 source/header 文件。`vx.json` 和 `CMakeLists.txt` 仅作为元数据/构建证据，不计入 source/header 覆盖数。

| 最小目录单元 | source/header 数 | 中文说明 |
|--------------|------------------|----------|
| `wsf_plugins/wsf_alternate_locations/source` | 7 | WSF 平台替代位置初始化插件 |
| `mystic/plugins/ResultMerger/source` | 8 | Mystic recording 合并工具 |
| `mystic/plugins/ResultOrbitalData/source` | 8 | Mystic 空间平台轨道根数显示/绘图插件 |
| `mystic/plugins/ResultP6DOFData/source` | 8 | Mystic deprecated P6DOF 结果数据插件 |
| `mystic/plugins/ResultPlatformBrowser/source` | 8 | Mystic 平台浏览 dock 适配插件 |
| `mystic/plugins/ResultPlatformData/source` | 8 | Mystic 平台状态、部件、类别、data ring 与绘图插件 |

## 执行方式

| 角色 | 数量 | 职责 |
|------|------|------|
| 主 agent | 1 | 选定 batch19 范围、合并 JSONL、写入正式文档并执行验证 |
| 子 agent | 3 | 每个 agent 分析 2 个最小目录单元，只读采集 CodeGraph/源码证据 |

## 产出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` | 更新 batch19 目录的 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions`、中文 `brief` |
| 粗符号索引增量 | `workspace/source-index/symbol-index-phase2.jsonl` | 替换 batch19 目录符号，新增 45 个真实粗符号 |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 6 个目录标记为 `done_batch19` |
| 模块概览 | `docs/architecture/module-overview-v2-incremental.md` | 追加第 85-90 节 |
| 验证报告 | `docs/verification/phase2-followup-batch19-verify-report.md` | 记录覆盖、符号过滤、文档位置和风险项 |

## 关键统计数据

| 指标 | 值 |
|------|-----|
| 本批目录数 | 6 |
| 本批 source/header 文件数 | 47 |
| 新增/替换粗符号数 | 45 |
| 子 agent 数 | 3 |
| CodeGraph 使用策略 | 子 agent 优先使用 `.codegraph`，仅对文件清单、构建元数据和宏行号做窄范围文本补充 |

## 业务逻辑承接价值

| 入口 | 价值 |
|------|------|
| `WsfAltLoc::Component::PreInitialize` | 高价值运行时行为入口，能追踪平台初始位置如何由配置、随机 draw、引用平台和地形修正共同决定 |
| `RvMerger::MergerThread::run` | 高价值结果处理入口，能追踪多个 recording 的平台身份、时间偏移、schema 和消息过滤规则 |
| `RvOrbitalData::Interface::GenerateOrbitalData` | 高价值空间业务入口，能追踪平台状态消息到轨道根数的转换 |
| `RvP6DOFData::Interface::AdvanceTimeRead` | P6DOF 结果消息消费入口，适合后续核对飞行、燃油、自动驾驶和力矩字段 |
| `RvPlatformData::Interface::AdvanceTimeRead` | 平台状态/部件/类别消费入口，是 Mystic 平台业务字段追踪的核心起点 |

## 已知问题与备注

1. `ResultPlatformBrowser` 是薄适配层，平台枚举与过滤核心逻辑在 `wkf::PlatformBrowserInterface` 和 `WkfPlatformBrowserDockWidget` 中。
2. `ResultP6DOFData` 插件源码声明 P6DOF 已 deprecated，后续业务分析应同时对照 SixDOF 数据插件。
3. 多个 Result 插件使用 `mIndex > 0` 判断平台有效性，平台索引是否 0-based/1-based 需要在 `ResultData/ResultDb` 中统一确认。
4. `ResultMerger` 的跨 recording 时间排序和 `simIndex()==0` 过滤策略需要 Phase 3/4 继续用函数级证据验证。

## 下游就绪

本批已形成可供 Phase 3/4 深挖的入口：平台初始位置修改、recording 合并、空间轨道根数、P6DOF/SixDOF 对照、平台状态字段、ResultDb 平台索引语义。
