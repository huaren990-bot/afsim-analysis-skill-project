# Phase 2 batch06 Mystic 小插件目录处理记录

> **日期**：2026-06-29
> **目标**：继续按 `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` 推进 Phase2，以最小目录单元为原子粒度，并采用子 agent 并行提升证据采集效率。

## 1. 本批范围

| # | 最小目录单元 | 系统 | 子系统 | source/header 数 |
|---|--------------|------|--------|------------------|
| 1 | `afsim-2_9/swdev/src/mystic/plugins/ResultAnnotation/source` | `applications` | `mystic/plugins` | 2 |
| 2 | `afsim-2_9/swdev/src/mystic/plugins/ResultComment/source` | `applications` | `mystic/plugins` | 2 |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultEngagementAnalysis/source` | `applications` | `mystic/plugins` | 2 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultEventMarker/source` | `applications` | `mystic/plugins` | 2 |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultHeadDownView/source` | `applications` | `mystic/plugins` | 2 |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultHeadUpView/source` | `applications` | `mystic/plugins` | 2 |

## 2. 执行方式

| 角色 | 工作 |
|------|------|
| 子 agent 1 | 只读分析 `ResultAnnotation/source`、`ResultComment/source`，输出文件职责、关键符号、插件运行关系、数据线索和风险项。 |
| 子 agent 2 | 只读分析 `ResultEngagementAnalysis/source`、`ResultEventMarker/source`，输出交战统计、事件 marker 和 ResultDb 关系证据。 |
| 子 agent 3 | 只读分析 `ResultHeadDownView/source`、`ResultHeadUpView/source`，输出 HDD/HUD 数据流、窗口生命周期和 SA 检测证据。 |
| 主 agent | 复核 CodeGraph/source 行号，串行合并 `file-index.jsonl`、`symbol-index-phase2.jsonl`、模块概览、计划和验证报告。 |

## 3. 修改产物

| 产物 | 处理 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 精修 12 个 source/header 条目，补充 `analysis_unit`、`system`、`subsystem`、关键符号、函数和中文职责。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 替换 6 个目标目录旧 auto-extracted 粗符号，新增 85 条可追溯粗符号；并修正 1 个旧 batch04 构造函数 duplicate-key 风险。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 6 个目标单元标记为 `done_batch06`，总完成数达到 16/237。 |
| `docs/architecture/module-overview-v2-incremental.md` | 追加第 11-16 节，分别描述 6 个最小目录单元。 |
| `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` | 更新完成数、当前完成批次、batch07 候选和 batch06 注意事项。 |
| `docs/verification/phase2-followup-batch06-verify-report.md` | 新增本批验证报告。 |

## 4. 关键发现

| 目录 | 发现 |
|------|------|
| `ResultAnnotation/source` | 消费 annotation event-pipe 消息，创建 POI、bullseye、decoration 和 range ring；平台相关 annotation 支持 deferred 补挂。 |
| `ResultComment/source` | 读取 `MsgComment`，同时驱动 comment dock log 和平台地图气泡；偏好控制 enabled、timeout 和时间戳展示。 |
| `ResultEngagementAnalysis/source` | 聚合 weapon fired/terminated 事件生成交战统计，并可 trace weapon/track 相关事件时间线。 |
| `ResultEventMarker/source` | 按时间窗口读取平台状态、武器终止和自定义 data-extension 事件，创建 viewer event marker。 |
| `ResultHeadDownView/source` | 将 ResultData 中平台、飞控、导航、燃油、武器、航迹、资产消息转换为 HDD 数据并推送给 Head Down View。 |
| `ResultHeadUpView/source` | 将平台状态、HUD、姿态插值、飞行、飞控、导航、燃油、武器消息转换为 HUD 数据并推送给 Head Up View。 |

## 5. 验证结果

| 指标 | 值 |
|------|-----|
| file-index 行数 | 43,586 |
| source/header 覆盖数 | 17,342 |
| symbol-index-phase2 行数 | 14,134 |
| batch06 文件条目 | 12 |
| batch06 粗符号条目 | 85 |
| batch06 导出宏伪符号 | 0 |
| 已完成最小目录单元 | 16 / 237 |
| `workspace` 下 Markdown | 0 |

## 6. 后续建议

batch07 可继续处理下一组 2 文件 Mystic 小插件目录：`ResultInteractionLines/source`、`ResultOrbit/source`、`ResultProjector/source`、`ResultRoute/source`、`ResultSituationAwarenessDisplay/source`、`ResultVisualEffects/source`。开始前仍需复核每个候选的实际路径展开数，并按插件复杂度决定是否拆分。
