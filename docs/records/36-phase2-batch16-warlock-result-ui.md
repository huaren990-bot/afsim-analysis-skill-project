# Phase 2 batch16 Warlock Result/UI Runtime Bridges

> 日期：2026-07-07
> 范围：6 个最小目录单元，36 个 source/header 文件

## 1. 批次范围

| # | 最小目录单元 | source/header | 定位 |
|---|--------------|---------------|------|
| 1 | `afsim-2_9/swdev/src/warlock/plugins/EventMarker/source` | 6 | 平台/武器事件标记显示 |
| 2 | `afsim-2_9/swdev/src/warlock/plugins/HeadDownView/source` | 6 | HDD 玻璃座舱显示 |
| 3 | `afsim-2_9/swdev/src/warlock/plugins/HeadUpView/source` | 6 | HUD 抬头显示 |
| 4 | `afsim-2_9/swdev/src/warlock/plugins/Interactions/source` | 6 | 跨域 interaction 可视化 |
| 5 | `afsim-2_9/swdev/src/warlock/plugins/PlatformHistory/source` | 6 | 平台历史 trace/ribbon 显示 |
| 6 | `afsim-2_9/swdev/src/warlock/plugins/SituationAwarenessDisplay/source` | 6 | SA Processor 输出显示 |

## 2. 关键结论

| 单元 | 后续业务分析价值 | 说明 |
|------|------------------|------|
| EventMarker | 中 | 识别平台损坏/删除、武器终止等事件如何被 Warlock 可视化。 |
| HeadDownView | 高 | 集中消费 SA processor 的飞行、导航、燃油、武器、航迹、感知资产数据。 |
| HeadUpView | 中 | 消费 flight/control/nav/fuel/weapon 摘要，适合追显示字段来源。 |
| Interactions | 高 | 跨域业务事件 taxonomy 的集中消费点，覆盖 jamming、track、message、task、detection、weapon、kill、cyber。 |
| PlatformHistory | 中 | 可观察 detection/track/attack 生命周期，但不实现规则。 |
| SituationAwarenessDisplay | 高 | SA processor、Perceive、Assess 输出到 UI 的集中映射层。 |

## 3. 已更新产物

| 产物 | 更新 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 为 36 个 source/header 补入 batch16 精化职责、关键符号和函数。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 删除旧粗符号，新增 37 个 batch16 精化符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 将 6 个目录标记为 `done_batch16`。 |
| `docs/architecture/module-overview-v2-incremental.md` | 新增第 67-72 节。 |
| `docs/verification/phase2-followup-batch16-verify-report.md` | 新增本批验证报告。 |

## 4. 保留复核项

| 单元 | 复核项 |
|------|--------|
| EventMarker | summary 字符串是否进入 marker、仿真完成删除 markers 是否符合复盘预期。 |
| HeadDownView | `sender->data()` 空指针、菜单 action 挂载、`Update()` 参数未使用、禁用状态跨仿真清理。 |
| HeadUpView | `sender` 空指针、重复 signal 连接、平台数据复用、`ReleasePlatform()` QPointer/key 防御。 |
| Interactions | `mMessageHopTracker` 跨仿真清理、`mTimeout` 并发读写、one-shot 事件取消、attachment 去重。 |
| PlatformHistory | wing ribbon 更新时间、缺省模型几何、未知 state value release 下静默 0。 |
| SituationAwarenessDisplay | `try_lock` 失败覆盖容器、disabled 初始化不清空集合、平台指针直接解引用。 |
