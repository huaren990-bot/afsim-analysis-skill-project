# Phase 2 完成记录：batch36 Mystic 公共库与 Wizard SpaceTools

> **完成日期**：2026-07-13
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `mystic/lib/source` | 52 | `rv::PluginT`、`rv::RunManager`、`rv::EventThread`、`rv::TrackDb`、`rv::ResultMessageArray` | Mystic 公共库，提供 result viewer 插件基类、run manager、event thread、track db、plotting/startup/preference 等基础设施。 |
| `wizard/plugins/SpaceTools/source` | 52 | `SpaceTools::Plugin`、`SpaceTools::Astrolabe`、`SpaceTools::ConstellationMaker`、`SpaceTools::SatelliteInserterDialog`、`SpaceTools::SatelliteInserterModel` | Wizard SpaceTools 插件，提供 Astrolabe、constellation maker、satellite inserter、TLE 和轨道尺寸/起始时间 UI。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | CodeGraph 对 `mystic lib SpaceTools` 查询主要命中 Mystic result 插件基类相关源码，存在 Result* 插件噪声；SpaceTools 由本地目录扫描确认 `Plugin`、`Astrolabe`、`ConstellationMaker` 和 satellite inserter 入口。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/struct/enum/function，过滤导出宏伪符号和跨目录同名命中。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `mystic/lib/source` | 结果查看基础设施入口，后续应追 `Factory::UserOpenFile` → `rv::Environment::OpenEventRecording` → `RvWsfPipe::FileStreamer` → `ResultDb::ProcessOneTimeMessage` → `rv::PluginT` 插件事件分发和 `ResultPlatform/TrackDb/InteractionDb` 查询链。 |
| `wizard/plugins/SpaceTools/source` | 空间场景编辑入口，后续应追 `SpaceTools::Plugin` 菜单/上下文注册 → `Astrolabe` mission sequence 读写 → `InputReader/InputWriter` → `OrbitalSequenceToInput`，以及 `ConstellationMaker`、`SatelliteInserterHandler`、TLE 更新写回链。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch36-verify-report.md` |

## 已知问题

1. CodeGraph 对通用 `Plugin`、`Event`、`Command` 等名称存在跨目录噪声，正式归属以完整路径前缀为准。
2. Mystic lib 的手动 `Ref/Unref`、后台 `EventThread/FileStreamerThread` 与 UI 定时器协作需要函数级验证生命周期和并发边界。
3. SpaceTools 大量写回依赖文本查找 `mission_sequence/end_mover/end_platform/orbit` 等片段，后续业务分析必须把 comment masking、source cache 和 editor replace 路径纳入证据。
4. 本批只修 Phase 2 粗索引；函数级调用链、参数和分支语义留给 Phase 3/4 或业务逻辑深挖。

## 下游就绪

本批新增 2 个最小目录单元、104 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
