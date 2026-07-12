# Phase 2 batch13 Wizard Importers and Annotation Plugin

> 日期：2026-07-07
> 范围：4 个最小目录单元，18 个 source/header 文件
> 说明：工作清单 order 68 `tools/geodata` 实际展开 98 个 source/header，已按计划跳过，不并入小批次。

## 1. 批次范围

| # | 最小目录单元 | source/header | 定位 |
|---|--------------|---------------|------|
| 1 | `afsim-2_9/swdev/src/wizard/plugins/ACOImporter/source` | 4 | ACO/ATO 导入转换工具 |
| 2 | `afsim-2_9/swdev/src/wizard/plugins/ErrorList/source` | 4 | Wizard parse error 展示 dock |
| 3 | `afsim-2_9/swdev/src/wizard/plugins/ScenarioImporter/source` | 5 | Wizard 文本/CSV 场景导入生成工具 |
| 4 | `afsim-2_9/swdev/src/wsf_plugins/wsf_annotation/source` | 5 | AFSIM annotation 场景输入与 event pipe 插件 |

## 2. 关键结论

| 单元 | 业务逻辑相关性 | 说明 |
|------|----------------|------|
| ACOImporter | 工具侧入口 | 导入 ACO/ATO 文本并生成 AFSIM 兼容输出，不参与 runtime。 |
| ErrorList | 无 | 只展示 Wizard parse errors 并跳转文本位置。 |
| ScenarioImporter | 工具侧入口 | 通过预处理/过滤/解析/模板生成输出文件，不直接注册 WSF 命令。 |
| wsf_annotation | 可视化业务入口 | 解析 `visual_elements` 并输出 annotation event pipe 消息，是 annotation 生产端。 |

## 3. 已更新产物

| 产物 | 更新 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 为 18 个 source/header 补入 batch13 精化职责、关键符号和函数。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 删除旧粗符号，新增 batch13 精化符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 将 4 个目录标记为 `done_batch13`。 |
| `docs/architecture/module-overview-v2-incremental.md` | 新增第 53-56 节。 |
| `docs/verification/phase2-followup-batch13-verify-report.md` | 新增本批验证报告。 |

## 4. 保留复核项

| 单元 | 复核项 |
|------|--------|
| ACOImporter | `UnregisterAcoRequirements()` 疑似注册/注销错误；多选删除只删首项；目录导入小写化路径。 |
| ErrorList | `mModelPtr` 裸指针释放责任；项目关闭时信号连接生命周期。 |
| ScenarioImporter | 模板条件比较、搜索边界、不可达进度分支、析构中 `QCoreApplication::quit()`。 |
| wsf_annotation | `range_ring` 名称去重时机；边界校验文案；event pipe 输出文件名前置条件。 |
