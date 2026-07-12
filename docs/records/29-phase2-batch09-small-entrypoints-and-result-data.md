# Phase 2 batch09 小入口与结果数据插件处理记录

> **日期**：2026-07-04
> **目标**：继续按最小目录单元推进 Phase2，采用 3 个子 agent 并行采集证据，主 agent 统一合并索引和文档。

## 1. 本批范围

| # | 最小目录单元 | 系统 | 子系统 | source/header 数 |
|---|--------------|------|--------|------------------|
| 1 | `afsim-2_9/swdev/src/sensor_plot/source` | `applications` | `sensor_plot/source` | 3 |
| 2 | `afsim-2_9/swdev/src/warlock/warlock_exec/source` | `applications` | `warlock/warlock_exec` | 3 |
| 3 | `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8/source` | `plugin_modules` | `wsf_plugins/wsf_argo8` | 3 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultBattleManagement/source` | `applications` | `mystic/plugins` | 4 |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultCommVis/source` | `applications` | `mystic/plugins` | 4 |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataAirCombat/source` | `applications` | `mystic/plugins` | 4 |

## 2. 执行方式

| 角色 | 工作 |
|------|------|
| 子 agent 1 | 只读分析 `sensor_plot/source`、`warlock/warlock_exec/source`，输出应用启动链、注册链路和风险项。 |
| 子 agent 2 | 只读分析 `wsf_argo8/source`、`ResultBattleManagement/source`，输出 ARGO8 weapon engagement 适配和 Mystic BM 结果消费链。 |
| 子 agent 3 | 只读分析 `ResultCommVis/source`、`ResultDataAirCombat/source`，输出通信拓扑展示和 Air Combat data extension 数据链。 |
| 主 agent | 使用 CodeGraph 复核 21 个 source/header 文件，串行合并 `file-index.jsonl`、`symbol-index-phase2.jsonl`、工作清单、模块概览、计划和验证报告。 |

## 3. 修改产物

| 产物 | 处理 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 精修 21 个 source/header 条目，补充最小目录单元、系统、子系统、关键符号、函数和中文职责。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 替换本批目标目录旧 auto-extracted 粗符号，新增 104 条可追溯粗符号；插件注册宏仅保留为 metadata。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 6 个目标单元标记为 `done_batch09`，总完成数达到 34/237。 |
| `docs/architecture/module-overview-v2-incremental.md` | 追加第 29-34 节，并修正顶部总览表。 |
| `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` | 更新完成数、当前完成批次、batch10 候选和 batch09 注意事项。 |
| `docs/verification/phase2-followup-batch09-verify-report.md` | 新增本批验证报告。 |

## 4. 关键发现

| 目录 | 发现 |
|------|------|
| `sensor_plot/source` | Sensor Plot 是场景读取到传感器/天线绘图的轻量入口；`StubInterface` 为非完整依赖场景提供 dummy 类型和 ignore 输入容错。 |
| `warlock/warlock_exec/source` | Warlock executable 串联 Qt、WKF/VTK、Warlock environment、权限系统、RunManager、场景加载和 event loop。 |
| `wsf_argo8/source` | ARGO8 mover 将 WSF 平台、航迹、seeker 和 weapon engagement 转换给 `Argo8Missile`，并回写 miss distance 和终止结果。 |
| `ResultBattleManagement/source` | Mystic BM 插件消费 ResultDb 平台/武器/状态消息，将 damage、fuel、aux data 映射为 WKF battle management 展示规则。 |
| `ResultCommVis/source` | CommVis 插件把 network/comm/link 结果消息转成 WKF CommVis events；router 和时间推进显示仍是占位。 |
| `ResultDataAirCombat/source` | Air Combat data extension 注册 11 类 `MsgSA_*` 消息，是追踪空战业务逻辑到 Mystic 结果展示的高价值入口。 |

## 5. 验证结果

| 指标 | 值 |
|------|-----|
| batch09 source/header 文件条目 | 21 |
| batch09 粗符号条目 | 104 |
| batch09 导出宏伪符号 | 0 |
| 已完成最小目录单元 | 34 / 237 |
| 剩余 pending 单元 | 203 |
| `workspace` 下 Markdown | 0 |

## 6. 后续建议

batch10 建议继续处理实际展开为 4 个 source/header 的 Mystic data 插件：`ResultDataAnnotation/source`、`ResultDataCyber/source`、`ResultDataP6Dof/source`、`ResultDataSixDOF/source`、`ResultDataSpace/source`、`ResultDataWk/source`。这些目录都属于结果数据扩展链，可连续补强下一步业务逻辑分析所需的 event pipe -> ResultDb 数据入口。
