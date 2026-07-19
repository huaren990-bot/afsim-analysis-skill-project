# Phase 2 batch45 增量验证报告

> **验证日期**：2026-07-15
> **验证对象**：Phase 2 最小目录单元增量产物
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 目录边界 | 通过 | 本批 2 个最小目录单元均按独立 `analysis_unit` 写入工作清单和 file-index。 |
| source/header 计数 | 通过 | 本批合计 78 个 source/header；验证脚本按 file-index 路径前缀复算。 |
| 代表性符号 | 通过 | 本批新增 10 条代表性符号，均写入 `workspace/source-index/symbol-index-phase2.jsonl`。 |
| 导出宏过滤 | 通过 | 本批未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为符号写入。 |
| Markdown 产物位置 | 通过 | 批次记录与验证报告均位于 `docs/` 下。 |

## 单元复核

| 最小目录单元 | 计数 | 状态 | 主要风险 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/core/sensor_plot_lib` | 44 | 通过 | 目录计数包含测试文件；部分函数算法未在本批深入；`RunFunction()` 在非 sensor_plot 模式可能直接 `exit(1)`。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_air_combat` | 34 | 通过 | `WsfSA_Processor.cpp` 单文件职责很重；事件 schema 来自 utpack 生成链，尚未细化字段；processor/track/component 类型假设需在业务阶段验证。 |

## 结论

batch45 已完成。该批可以作为下一步 AFSIM 业务逻辑分析的证据入口，但复杂算法、线程/GUI 生命周期和生成消息 schema 仍应在后续阶段按函数级证据继续追踪。
