# Phase 2 follow-up batch09 验证报告

> **日期**：2026-07-04
> **批次范围**：6 个小入口与 Mystic 结果数据/展示最小目录单元
> **执行方式**：3 个子 agent 并行采集证据，主 agent 复核 CodeGraph/source 并统一合并 JSONL 与文档。

## 1. 批次范围

| # | 最小目录单元 | source/header 数 | 子系统 |
|---|--------------|------------------|--------|
| 1 | `afsim-2_9/swdev/src/sensor_plot/source` | 3 | `sensor_plot/source` |
| 2 | `afsim-2_9/swdev/src/warlock/warlock_exec/source` | 3 | `warlock/warlock_exec` |
| 3 | `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8/source` | 3 | `wsf_plugins/wsf_argo8` |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultBattleManagement/source` | 4 | `mystic/plugins` |
| 5 | `afsim-2_9/swdev/src/mystic/plugins/ResultCommVis/source` | 4 | `mystic/plugins` |
| 6 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataAirCombat/source` | 4 | `mystic/plugins` |

## 2. 验证摘要

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Phase1/File-index 覆盖闭环 | 通过 | `file-index.jsonl` 保持 43,586 行。 |
| batch09 工作清单状态 | 通过 | 6 个目标单元均标记为 `done_batch09`，总完成单元数为 34/237。 |
| batch09 文件索引 | 通过 | 21 个 source/header 条目均补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions` 和中文 `brief`。 |
| batch09 粗符号索引 | 通过 | 本批目标路径下共有 104 条粗符号。 |
| 导出宏伪符号 | 通过 | 本批目标路径中 `*_EXPORT` 作为 `symbol_name` 的条目为 0；`WKF_PLUGIN_DEFINE_SYMBOLS` 和 plugin setup 仅作为注册元数据。 |
| JSONL 可解析 | 通过 | `file-index.jsonl`、`symbol-index-phase2.jsonl`、`phase2-analysis-unit-worklist.jsonl` 均可逐行解析。 |
| 文档产物位置 | 通过 | 新增/更新 Markdown 均位于 `docs/`；`workspace` 下 Markdown 数为 0。 |

## 3. 按目录验证

| 最小目录单元 | 文件条目 | 粗符号条目 | 关键修正 |
|--------------|----------|------------|----------|
| `sensor_plot/source` | 3 | 8 | 补入 Sensor Plot 应用启动、stub_interface 注册、dummy WSF 类型和 ignore 输入容错。 |
| `warlock/warlock_exec/source` | 3 | 11 | 补入 Qt/WKF/VTK/Warlock 环境创建、RunManager、权限锁定、event pipe 和 simulation observer。 |
| `wsf_argo8/source` | 3 | 21 | 补入 ARGO8 插件注册、mover type 注入、导弹 flyout、truth/track guidance 和 weapon engagement 回写。 |
| `ResultBattleManagement/source` | 4 | 30 | 补入 ResultDb 平台/武器/状态消费、damage/fuel/aux data rule set 和 WKF BM 展示关系。 |
| `ResultCommVis/source` | 4 | 11 | 补入 Tools 菜单动作、network/comm/link 到 WKF CommVis event 的转换和未完成 router/time 占位。 |
| `ResultDataAirCombat/source` | 4 | 23 | 补入 Air Combat serializer/schema、11 类 `MsgSA_*`、ResultPlatform 增删和 engagement summary 展示字段。 |

## 4. 子 agent 交叉确认

| 子 agent 范围 | 结论 |
|---------------|------|
| `sensor_plot/source`、`warlock/warlock_exec/source` | 与主 agent CodeGraph 证据一致；补充 dummy object 语义、RunManager 和环境 lifecycle 复核点。 |
| `wsf_argo8/source`、`ResultBattleManagement/source` | 与主 agent CodeGraph 证据一致；补充 ARGO8 guidance/seeker/termination 风险和 Battle Management TODO 项。 |
| `ResultCommVis/source`、`ResultDataAirCombat/source` | 与主 agent CodeGraph 证据一致；补充 CommVis 未完成项和 AirCombat `HandleMessage` 返回值疑点。 |

## 5. 保留风险

| 风险 | 处理 |
|------|------|
| `sensor_plot` 的 dummy 类型和 ignore 输入会降低场景语义真实性。 | 记录为 needs_review；后续分析 plot 算法时需转向 `core/sensor_plot_lib`。 |
| `warlock_exec` 聚合多个 environment 生命周期，且部分命令行文件不可读处理不一致。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| `WsfARGO8_Mover` 多处依赖 engagement/platform/track 生命周期保证，且存在路径判断、浮点比较和 dead-target 数据初始化疑点。 | 记录为 needs_review，是后续武器交战业务分析重点。 |
| `ResultBattleManagement` 的 `RuleSetWeaponCount` 未完成，AuxData 取值语义需要结合 ResultDb 排序确认。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| `ResultCommVis` 的 router/time 动态可视化尚未实现，本地 dialog 子类未见实际使用。 | 记录为 needs_review，不能把它视为完整通信业务逻辑。 |
| `ResultDataAirCombat::HandleMessage` 未返回 handler 结果，且多数 SA handler 仅映射 owner/platform。 | 记录为 needs_review，这是空战结果展示链的重要疑点。 |

## 6. 结论

batch09 通过。该批次补强了三个重要方向：应用入口链（Sensor Plot、Warlock）、武器交战模型适配（ARGO8）和 Mystic 结果数据/展示消费链（Battle Management、CommVis、Air Combat data extension）。产物可支撑后续从 event pipe、ResultDb 和 weapon engagement 继续追踪 AFSIM 业务逻辑。
