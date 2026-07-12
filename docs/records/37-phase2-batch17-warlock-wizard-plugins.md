# Phase 2 batch17 Warlock/Wizard Plugins

> 日期：2026-07-07
> 范围：6 个最小目录单元，36 个 source/header 文件

## 1. 批次范围

| # | 最小目录单元 | source/header | 定位 |
|---|--------------|---------------|------|
| 1 | `afsim-2_9/swdev/src/warlock/plugins/VisualEffects/source` | 6 | Warlock visual effects 显示桥 |
| 2 | `afsim-2_9/swdev/src/wizard/plugins/ColorUtils/source` | 6 | Wizard editor 颜色辅助工具 |
| 3 | `afsim-2_9/swdev/src/wizard/plugins/DemoBrowser/source` | 6 | Wizard demo/scenario/training 浏览工具 |
| 4 | `afsim-2_9/swdev/src/wizard/plugins/LogServer/source` | 6 | Wizard 仿真日志 TCP 聚合入口 |
| 5 | `afsim-2_9/swdev/src/wizard/plugins/MapRoute/source` | 6 | Wizard route/orbit 可视化与编辑桥 |
| 6 | `afsim-2_9/swdev/src/wizard/plugins/PlatformData/source` | 6 | Wizard 平台初始状态数据面板 |

## 2. 关键结论

| 单元 | 后续业务分析价值 | 说明 |
|------|------------------|------|
| VisualEffects | 中 | 消费 appearance 和 weapon termination，显示 smoke/fire/afterburner/explosion effects。 |
| ColorUtils | 低到中 | 编辑器颜色构造/提示工具，不承载仿真业务规则。 |
| DemoBrowser | 低 | 训练/demo/scenario 浏览和启动入口，属于默认排除范围的辅助索引。 |
| LogServer | 中 | 仿真日志聚合入口，可用于追运行输出，但不实现业务逻辑。 |
| MapRoute | 高 | 包含 route mover/path/orbit 可视化和编辑写回，是 route 业务语义高价值入口。 |
| PlatformData | 中 | 展示平台初始状态、单位、AGL/MSL、Mach 等字段，适合作为平台字段索引。 |

## 3. 已更新产物

| 产物 | 更新 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 为 36 个 source/header 补入 batch17 精化职责、关键符号和函数。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 删除旧粗符号，新增 33 个 batch17 精化符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 将 6 个目录标记为 `done_batch17`。 |
| `docs/architecture/module-overview-v2-incremental.md` | 新增第 73-78 节。 |
| `docs/verification/phase2-followup-batch17-verify-report.md` | 新增本批验证报告。 |

## 4. 保留复核项

| 单元 | 复核项 |
|------|--------|
| VisualEffects | `switch` 缺少 `break` 的 fallthrough 是否符合意图；effect entity 生命周期需追 `VisualEffectsDisplayInterface`。 |
| ColorUtils | `ColorConstruct()` 行内下标、`mColorTipsPtr` 旧对象生命周期、`UpdateScenario()` 重复连接。 |
| DemoBrowser | rst 文件打开失败未校验，搜索只扫描 `*.txt`，UI 重建的 layout 生命周期需确认。 |
| LogServer | TCP thread 忙轮询、端口偏好重启竞态、连接/packet 所有权清理。 |
| MapRoute | `OnProxyModified()` 空实现、altitude reference 疑似反向、首 waypoint altitude 缺省、global route watcher。 |
| PlatformData | primitive 字段未默认初始化、平台缺失时不清空 state、`mIndex` 遗留、`SpeedUpdater` 未使用。 |
