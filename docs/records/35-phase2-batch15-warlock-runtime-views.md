# Phase 2 batch15 WKF/Warlock Runtime Views

> 日期：2026-07-07
> 范围：6 个最小目录单元，36 个 source/header 文件

## 1. 批次范围

| # | 最小目录单元 | source/header | 定位 |
|---|--------------|---------------|------|
| 1 | `afsim-2_9/swdev/src/tools/wkf/plugins/Performance/source` | 6 | WKF Performance 开发者诊断插件 |
| 2 | `afsim-2_9/swdev/src/warlock/plugins/AcesDisplay/source` | 6 | Warlock ACES 空战/SA 显示适配 |
| 3 | `afsim-2_9/swdev/src/warlock/plugins/AirCombatVisualization/source` | 6 | Warlock 空战可视化 overlay |
| 4 | `afsim-2_9/swdev/src/warlock/plugins/Annotation/source` | 6 | Warlock annotation 场景标注显示桥 |
| 5 | `afsim-2_9/swdev/src/warlock/plugins/ApplicationLauncher/source` | 6 | Warlock Wizard/Mystic 应用启动工具 |
| 6 | `afsim-2_9/swdev/src/warlock/plugins/CommVis/source` | 6 | Warlock 通信事件可视化桥 |

## 2. 关键结论

| 单元 | 后续业务分析价值 | 说明 |
|------|------------------|------|
| Performance | 低 | 只读取当前进程内存并绘制诊断曲线。 |
| AcesDisplay | 中高 | 是 ACES/SA/engagement 语义的显示观察入口，应继续追 `WsfSA_Processor`、`WsfSA_Assess` 和 track manager。 |
| AirCombatVisualization | 中高 | 是空战态势 overlay 消费入口，应继续追 SA processor 与 weapon engagement 上游。 |
| Annotation | 中 | 与 `wsf_annotation` 生产链可串联，主要显示 POI、bullseye、decoration、range ring。 |
| ApplicationLauncher | 低 | 工具流程入口，不承载 AFSIM 业务规则。 |
| CommVis | 中高 | 通信行为观察入口，应继续追通信核心类和 message transmitted/hop 事件来源。 |

## 3. 已更新产物

| 产物 | 更新 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 为 36 个 source/header 补入 batch15 精化职责、关键符号和函数。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 删除旧粗符号，新增 25 个 batch15 精化符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 将 6 个目录标记为 `done_batch15`。 |
| `docs/architecture/module-overview-v2-incremental.md` | 新增第 61-66 节。 |
| `docs/verification/phase2-followup-batch15-verify-report.md` | 新增本批验证报告。 |

## 4. 保留复核项

| 单元 | 复核项 |
|------|--------|
| AcesDisplay | 上游 SA/Assess/Perceive/engagement 业务语义不在本目录内，需在 core/wsf 与 wsf_air_combat 继续确认。 |
| AirCombatVisualization | `try_lock` 跳过、target 去重、viewer 菜单对象空指针路径需后续验证。 |
| Annotation | display interface 非空假设和 range ring property 构造重复可在后续 UI 稳定性检查中验证。 |
| CommVis | `AddComms` 内部空指针假设和通信事件来源需继续追核心通信类。 |
