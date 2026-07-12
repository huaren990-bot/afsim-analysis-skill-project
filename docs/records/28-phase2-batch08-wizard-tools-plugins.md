# Phase 2 batch08 Wizard/WKF 小插件处理记录

> **日期**：2026-07-04
> **目标**：继续按最小目录单元推进 Phase2，采用 3 个子 agent 并行采集证据，主 agent 统一合并索引和文档。

## 1. 本批范围

| # | 最小目录单元 | 系统 | 子系统 | source/header 数 |
|---|--------------|------|--------|------------------|
| 1 | `afsim-2_9/swdev/src/tools/wkf/plugins/Visibility/source` | `developer_tools` | `tools/wkf` | 2 |
| 2 | `afsim-2_9/swdev/src/wizard/main/source` | `applications` | `wizard/main` | 2 |
| 3 | `afsim-2_9/swdev/src/wizard/plugins/MapAnnotation/source` | `applications` | `wizard/plugins` | 2 |
| 4 | `afsim-2_9/swdev/src/wizard/plugins/MysticLauncher/source` | `applications` | `wizard/plugins` | 2 |
| 5 | `afsim-2_9/swdev/src/wizard/plugins/SIMDIS/source` | `applications` | `wizard/plugins` | 2 |
| 6 | `afsim-2_9/swdev/src/wizard/plugins/UnitConversion/source` | `applications` | `wizard/plugins` | 2 |

## 2. 执行方式

| 角色 | 工作 |
|------|------|
| 子 agent 1 | 只读分析 `Visibility/source`、`wizard/main/source`，输出平台可见性过滤、启动包装和风险项。 |
| 子 agent 2 | 只读分析 `MapAnnotation/source`，输出 proxy/annotation/text editor 双向同步和风险项。 |
| 子 agent 3 | 只读分析 `MysticLauncher/source`、`SIMDIS/source`、`UnitConversion/source`，输出外部工具启动、文件动作、单位转换和风险项。 |
| 主 agent | 使用 CodeGraph 复核 12 个 source/header 文件，串行合并 `file-index.jsonl`、`symbol-index-phase2.jsonl`、工作清单、模块概览、计划和验证报告。 |

## 3. 修改产物

| 产物 | 处理 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 精修 12 个 source/header 条目，补充最小目录单元、系统、子系统、关键符号、函数和中文职责。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 替换本批目标目录旧 auto-extracted 粗符号，新增 101 条可追溯粗符号；插件注册宏仅保留为 metadata。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 6 个目标单元标记为 `done_batch08`，总完成数达到 28/237。 |
| `docs/architecture/module-overview-v2-incremental.md` | 追加第 23-28 节，并修正顶部总览表。 |
| `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` | 更新完成数、当前完成批次、batch09 候选和 batch08 注意事项。 |
| `docs/verification/phase2-followup-batch08-verify-report.md` | 新增本批验证报告。 |

## 4. 关键发现

| 目录 | 发现 |
|------|------|
| `Visibility/source` | 提供 WKF 用户层平台可见性过滤，依赖 `RegisterPlatformVisibilityFilter` 和 `PlatformVisibilityChanged`。 |
| `wizard/main/source` | 只是 Wizard 启动包装层；真实业务入口在 `wizard_main` / `wizard_core`。 |
| `MapAnnotation/source` | 连接 WSF proxy tree、WKF annotation display 和 Wizard editor，是场景文本与地图 annotation 双向同步的核心入口。 |
| `MysticLauncher/source` | 注册 `WSF_PIPE` 文件检测器，为 `wsf_pipe` 文件添加 “Open with Mystic” 并启动 Mystic。 |
| `SIMDIS/source` | 配置 SIMDIS exe 和模型目录，为 `.asi` 启动、模型替换、beam color 替换提供 Wizard 集成。 |
| `UnitConversion/source` | 基于 WSF parse value 和 `UtUnits` 生成编辑器右键单位换算菜单。 |

## 5. 验证结果

| 指标 | 值 |
|------|-----|
| file-index 行数 | 43,586 |
| symbol-index-phase2 行数 | 14,286 |
| batch08 文件条目 | 12 |
| batch08 粗符号条目 | 101 |
| batch08 导出宏伪符号 | 0 |
| 已完成最小目录单元 | 28 / 237 |
| `workspace` 下 Markdown | 0 |

## 6. 后续建议

batch09 应跳过实际展开较大的 `core/sensor_plot_lib`、`core/wsf_cyber`、`core/wsf_mil`、`post_processor/lib`、`wsf_plugins/wsf_air_combat` 等目录，优先处理实际展开为 3-4 个 source/header 的小入口和 Mystic data/display 插件，例如 `sensor_plot/source`、`warlock/warlock_exec/source`、`wsf_plugins/wsf_argo8/source`、`ResultBattleManagement/source`、`ResultCommVis/source`、`ResultDataAirCombat/source`。
