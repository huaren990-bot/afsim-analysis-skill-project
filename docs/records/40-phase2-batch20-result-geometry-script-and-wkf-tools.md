# Phase 2 batch20 完成记录：结果几何/脚本/SixDOF/统计与 WKF 工具插件

> **完成日期**：2026-07-08
> **阶段**：Phase 2 / 模块级粗粒度分析
> **状态**：已完成

## 分析范围

本批处理 6 个最小目录单元，覆盖 48 个 source/header 文件。`vx.json` 与 `CMakeLists.txt` 仅作为元数据/构建证据，不计入 source/header 统计。

| 最小目录单元 | source/header 数 | 中文说明 |
|--------------|------------------|----------|
| `mystic/plugins/ResultRelativeGeometry/source` | 8 | 双平台相对几何显示、updater 与绘图 |
| `mystic/plugins/ResultScriptDataFeed/source` | 8 | `MsgScriptData` 脚本数据消费、显示与绘图 |
| `mystic/plugins/ResultSixDOF_Data/source` | 8 | SixDOF 飞行/控制/力矩结果数据消费 |
| `mystic/plugins/ResultStatistics/source` | 8 | 结果消息统计、事件表过滤和执行元数据 |
| `tools/wkf/plugins/MapHoverInfo/source` | 8 | 地图悬停 tooltip 信息插件 |
| `tools/wkf/plugins/TetherView/source` | 8 | tether/look-at 二级视窗插件 |

## 执行方式

| 角色 | 数量 | 职责 |
|------|------|------|
| 主 agent | 1 | 合并索引、补齐失败 agent 范围、写正式文档和验证 |
| 子 agent | 3 | 原计划每个 agent 处理 2 个目录；其中 1 个完成，2 个因连接中断失败 |

失败的子 agent 未写入共享文件。主 agent 对失败范围使用 CodeGraph 优先、本地窄范围源码扫描补齐证据。

## 产出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` | 更新 batch20 目录字段和中文 brief |
| 粗符号索引增量 | `workspace/source-index/symbol-index-phase2.jsonl` | 新增/替换 42 个 batch20 粗符号 |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 6 个目录标记为 `done_batch20` |
| 模块概览 | `docs/architecture/module-overview-v2-incremental.md` | 追加第 91-96 节 |
| 验证报告 | `docs/verification/phase2-followup-batch20-verify-report.md` | 记录覆盖、证据来源和风险项 |

## 业务逻辑承接价值

| 入口 | 价值 |
|------|------|
| `RelativeGeometry::PlotUpdater::GetSeries` | 可追双平台时间对齐和相对几何计算 |
| `RvScriptDataFeed::Interface::AdvanceTimeRead` | 可追脚本数据如何从 event pipe keyed map 进入 UI |
| `RvSixDOF_Data::Interface::AdvanceTimeRead` | 可追 SixDOF 飞行、燃油、自动驾驶、操纵和力矩字段 |
| `RvStatistics::EventTableModel::data` | 可追 Mystic 原始消息表如何解释大量结果消息 |
| `MapHoverInfo::HoverManager::HandleHoverEvent` | 可追地图 hover 如何把实体、updater 和 NamedInfo 合成显示文本 |
| `TetherView::Plugin::ConnectToPlatform` | 可追二级视窗如何跟随平台并恢复启动状态 |

## 已知问题与备注

1. `ResultSixDOF_Data` 与 batch19 的 `ResultP6DOFData` 结构相近，后续建议对照字段映射和绘图 X/Y 轴逻辑。
2. `ResultScriptDataFeed` 的 `MenuPlot()` 只见声明未见实现，可能是遗留接口。
3. 多个 Result 插件仍有 `mIndex > 0` 的平台 index 语义疑点。
4. `MapHoverInfo` 的 updater 缓存在实体释放/场景清理时依赖 hover 重访和偏好变更清空，后续可验证生命周期。

## 下游就绪

batch20 为后续业务逻辑分析补齐了相对几何、脚本自定义数据、SixDOF、原始结果消息统计、地图交互和二级跟随视窗六类入口。
