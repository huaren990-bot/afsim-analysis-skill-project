# Phase 2 batch18 Runtime Editing and Scripting

> 日期：2026-07-08
> 范围：6 个最小目录单元，40 个 source/header 文件；另记录 1 个 profiling 头模板 `ProfilingMacros.hpp.in`

## 1. 批次范围

| # | 最小目录单元 | source/header | 定位 |
|---|--------------|---------------|------|
| 1 | `afsim-2_9/swdev/src/wizard/plugins/ZoneEditor/source` | 6 | Wizard zone 编辑和可视化 |
| 2 | `afsim-2_9/swdev/src/wsf_plugins/wsf_sosm/source` | 6 | SOSM 传感器运行时插件 |
| 3 | `afsim-2_9/swdev/src/core/wsf_mil_parser/source` | 7 | MIL proxy typed accessor |
| 4 | `afsim-2_9/swdev/src/tools/profiling/source` | 7 | profiling 基础设施 |
| 5 | `afsim-2_9/swdev/src/warlock/plugins/PlatformBrowser/source` | 7 | Warlock 平台浏览和删除入口 |
| 6 | `afsim-2_9/swdev/src/warlock/plugins/ScriptBrowser/source` | 7 | Warlock 脚本浏览和执行入口 |

## 2. 关键结论

| 单元 | 后续业务分析价值 | 说明 |
|------|------------------|------|
| ZoneEditor | 中 | 连接 `WsfPM_Zone` proxy、zone 显示变量和 WSF 文本写回。 |
| wsf_sosm | 高 | 注册 `WSF_SOSM_SENSOR`，`AttemptToDetect()` 写入 `WsfSensorResult`，是运行时传感器业务入口。 |
| wsf_mil_parser | 中 | MIL proxy 访问层，可帮助追踪 weapon、platform、RF jammer 配置字段。 |
| profiling | 低 | 性能基础设施，不承载业务规则。 |
| PlatformBrowser | 高 | Warlock UI 到 `WsfSimulation::DeletePlatform` 的平台删除 mutation 入口。 |
| ScriptBrowser | 高 | Warlock UI 到 `WARLOCK_` global/platform script 执行环境的入口。 |

## 3. 已更新产物

| 产物 | 更新 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 为本批目录补入 batch18 精化职责、关键符号和函数。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 删除旧粗符号，新增 38 个 batch18 精化符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 将 6 个目录标记为 `done_batch18`。 |
| `docs/architecture/module-overview-v2-incremental.md` | 新增第 79-84 节。 |
| `docs/verification/phase2-followup-batch18-verify-report.md` | 新增本批验证报告。 |

## 4. 保留复核项

| 单元 | 复核项 |
|------|--------|
| ZoneEditor | 手写 WSF 文本拼接、UI 空指针、重复 `RemoveZone()`、point list 越界。 |
| wsf_sosm | `mManagerPtr` 生命周期、extension 空值、频率除零、sensor-target pair 空值、throttle TODO。 |
| wsf_mil_parser | 注册函数体注释、`platforms()` 返回类型表达式、RF jammer transmitter accessor。 |
| profiling | 单实例全局状态、动态符号 ABI、section key 0、空 label。 |
| PlatformBrowser | 菜单 action 挂载、XIO host connection 空值、GUI/仿真平台身份一致性。 |
| ScriptBrowser | 全局脚本权限、global tree item 重复添加、参数转换缺少校验。 |
