# Phase 2 batch12 WKF and Warlock Tools

> 日期：2026-07-07
> 范围：6 个最小目录单元，24 个 source/header 文件
> 方法：3 个子 agent 并行采集证据；主 agent 统一合并 JSONL、模块概览和验证报告。

## 1. 批次范围

| # | 最小目录单元 | source/header | 定位 |
|---|--------------|---------------|------|
| 1 | `afsim-2_9/swdev/src/tools/wkf/plugins/ModelBrowser/source` | 4 | WKF 模型资源查看/编辑工具 |
| 2 | `afsim-2_9/swdev/src/tools/wkf/plugins/PositionConverterTool/source` | 4 | WKF LL/MGRS 坐标转换工具 |
| 3 | `afsim-2_9/swdev/src/tools/wkf/plugins/TerrainTools/source` | 4 | WKF terrain line-of-sight 查询工具 |
| 4 | `afsim-2_9/swdev/src/tools/wkf/plugins/UnitConverterTool/source` | 4 | WKF 通用单位换算工具 |
| 5 | `afsim-2_9/swdev/src/warlock/plugins/AdHocScriptBrowser/source` | 4 | Warlock ad hoc script 执行入口 |
| 6 | `afsim-2_9/swdev/src/warlock/plugins/Log/source` | 4 | Warlock 日志展示插件 |

## 2. 关键结论

batch12 的主体是工具层，不应直接并入 AFSIM 核心仿真业务逻辑。唯一需要作为业务入口关注的是 `AdHocScriptBrowser`，它能通过 `warlock::ScriptSimInterface::ExecuteScript()` 执行 global/platform ad hoc script。

| 单元 | 业务逻辑相关性 | 说明 |
|------|----------------|------|
| ModelBrowser | 间接相关 | 可修改模型资源定义，影响可视化模型数据库，不执行仿真逻辑。 |
| PositionConverterTool | 无 | 坐标格式转换 UI，不读写场景。 |
| TerrainTools | 间接相关 | 调用地形 LOS 资源能力做交互查询，不实现传感器/战术判定。 |
| UnitConverterTool | 无 | 通用单位换算 UI。 |
| AdHocScriptBrowser | 高 | 开发者脚本执行入口，可触发或改变仿真行为。 |
| Log | 低 | 观察/展示型日志插件，不改变状态。 |

## 3. 已更新产物

| 产物 | 更新 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 为 24 个 source/header 补入 batch12 精化职责、关键符号和函数。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 删除旧粗符号，新增 63 个经 CodeGraph/源码确认的符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 将 6 个目录标记为 `done_batch12`。 |
| `docs/architecture/module-overview-v2-incremental.md` | 新增第 47-52 节。 |
| `docs/verification/phase2-followup-batch12-verify-report.md` | 新增本批验证报告。 |

## 4. 保留复核项

| 单元 | 复核项 |
|------|--------|
| ModelBrowser | `models.txt` 整文件替换的原子性、目录创建和错误处理；临时定义预览异常路径。 |
| PositionConverterTool | 页切换是否应触发转换；用 `isVisible()` 判定转换方向的 UI 状态假设。 |
| TerrainTools | `mActiveRulerPtr` 未见赋值；剖面图投影零分母；LOS request/result 同步语义。 |
| UnitConverterTool | `mRepopulateMap[aString]()` 隐式插入风险；控件删除生命周期；空输入保留旧结果。 |
| AdHocScriptBrowser | 临时脚本权限边界、global context 权限、无平台时行为、`-lock_fileload` 覆盖范围。 |
| Log | 高日志量刷新成本；raw console 文本过滤/截断。 |
