# Phase 2 batch23 增量验证报告

> **验证日期**：2026-07-08
> **验证对象**：batch23 的 6 个最小目录单元
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|--------|------|------|
| 工作清单状态 | 通过 | 6 个目录已标记为 `done_batch23` |
| file-index 覆盖 | 通过 | 59 个 source/header 均补充目录字段、关键符号、函数和中文 brief |
| 粗符号索引 | 通过 | 新增/替换 41 个 batch23 粗符号 |
| 导出宏过滤 | 通过 | 导出宏未作为正式符号进入索引 |
| Markdown 位置 | 通过 | 新增报告均位于 `docs/` |

## 按目录验证

| 目录 | source/header 数 | 粗符号数 | 风险项 |
|------|------------------|----------|--------|
| `wizard/plugins/TablePlotter/source` | 9 | 7 | AFSIM table 语法分支多、CSV 后缀判断不严谨、dialog 生命周期 |
| `warlock/plugins/CreatePlatform/source` | 10 | 6 | longitude 校验疑似遗漏、`Clone(mType)` 空指针、AddPlatform 所有权路径 |
| `warlock/plugins/OrbitalData/source` | 10 | 7 | space mover 与 DIS space platform 双路径需一致性验证 |
| `warlock/plugins/P6DOF_Data/source` | 10 | 7 | deprecated 兼容层、speedbrake handle/name 约定、需对照 mover 差异 |
| `warlock/plugins/PlatformData/source` | 10 | 7 | aux data 嵌套属性语义可能丢失 |
| `warlock/plugins/SixDOF_Data/source` | 10 | 7 | 与 P6DOF 字段同构、speedbrake 位置语义、需对照 plot/updater 分支 |

## 结论

batch23 满足 Phase 2 增量要求，补齐了 runtime 创建平台、轨道/P6DOF/SixDOF/平台通用数据和 Wizard 表格绘图工具入口。
