# Phase 2 batch07 Mystic 结果显示插件处理记录

> **日期**：2026-07-03
> **目标**：继续按最小目录单元推进 Phase2，采用 3 个子 agent 并行采集证据，主 agent 统一合并索引和文档。

## 1. 本批范围

| # | 最小目录单元 | 系统 | 子系统 | source/header 数 |
|---|--------------|------|--------|------------------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultInteractionLines/source` | `applications` | `mystic/plugins` | 2 |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultOrbit/source` | `applications` | `mystic/plugins` | 2 |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultProjector/source` | `applications` | `mystic/plugins` | 2 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultRoute/source` | `applications` | `mystic/plugins` | 2 |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultSituationAwarenessDisplay/source` | `applications` | `mystic/plugins` | 2 |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultVisualEffects/source` | `applications` | `mystic/plugins` | 2 |

## 2. 执行方式

| 角色 | 工作 |
|------|------|
| 子 agent 1 | 只读分析 `ResultInteractionLines/source`、`ResultOrbit/source`，输出 InteractionDb、OrbitalElements、插件基类关系和风险项。 |
| 子 agent 2 | 只读分析 `ResultProjector/source`、`ResultRoute/source`，输出 projector matrix、route waypoint、UI 菜单和风险项。 |
| 子 agent 3 | 只读分析 `ResultSituationAwarenessDisplay/source`、`ResultVisualEffects/source`，输出 SA 数据容器、visual effects 事件链和风险项。 |
| 主 agent | 使用 CodeGraph 复核 12 个 source/header 文件，串行合并 `file-index.jsonl`、`symbol-index-phase2.jsonl`、工作清单、模块概览、计划和验证报告。 |

## 3. 修改产物

| 产物 | 处理 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 精修 12 个 source/header 条目，补充最小目录单元、系统、子系统、关键符号、函数和中文职责。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 替换本批目标目录旧 auto-extracted 粗符号，新增 84 条可追溯粗符号；保留 `WKF_PLUGIN_DEFINE_SYMBOLS` 为插件注册宏调用。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 6 个目标单元标记为 `done_batch07`，总完成数达到 22/237。 |
| `docs/architecture/module-overview-v2-incremental.md` | 追加第 17-22 节，并修正顶部总览表。 |
| `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` | 更新完成数、当前完成批次、batch08 候选和 batch07 注意事项。 |
| `docs/verification/phase2-followup-batch07-verify-report.md` | 新增本批验证报告。 |

## 4. 关键发现

| 目录 | 发现 |
|------|------|
| `ResultInteractionLines/source` | 消费 `rv::InteractionDb`，把 paired、one-time、unpaired interaction 映射为平台 incoming/outgoing 交互线或卡片。 |
| `ResultOrbit/source` | 消费 `rv::MsgOrbitalElements`，把轨道根数、颜色和机动结果写入 `wkf::AttachmentOrbit`。 |
| `ResultProjector/source` | 消费传感器状态、模式、FOV、articulation 和平台姿态，在 `UtoCmeTerrain` 上维护传感器地形投影矩阵。 |
| `ResultRoute/source` | 消费 `rv::MsgRouteChanged`，构建 route attachment，并用 `RouteDialog` 展示 waypoint 信息。 |
| `ResultSituationAwarenessDisplay/source` | 聚合 SA 飞行、导航、燃油、武器、航迹、感知、威胁、目标、编组和 truth 数据，是后续业务逻辑分析的高价值入口。 |
| `ResultVisualEffects/source` | 消费平台外观变化、武器终止和平台移除事件，创建/删除烟火、尾迹、爆炸、碎片等视觉特效。 |

## 5. 验证结果

| 指标 | 值 |
|------|-----|
| file-index 行数 | 43,586 |
| symbol-index-phase2 行数 | 14,199 |
| batch07 文件条目 | 12 |
| batch07 粗符号条目 | 84 |
| batch07 导出宏伪符号 | 0 |
| 已完成最小目录单元 | 22 / 237 |
| `workspace` 下 Markdown | 0 |

## 6. 后续建议

batch08 应跳过实际展开过大的 `tools/util_script`、`tools/utilqt`、`tools/wkf`，优先处理实际展开为 2 个 source/header 的 `tools/wkf/plugins/Visibility/source` 和 wizard 小插件组。若要处理 `tools/*` 大目录，应先重建更细的最小目录边界。
