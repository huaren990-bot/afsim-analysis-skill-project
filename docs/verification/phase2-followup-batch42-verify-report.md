# Phase 2 增量验证报告：batch42

> **验证日期**：2026-07-14
> **范围**：`afsim-2_9/swdev/src/tools/vespatk/source`, `afsim-2_9/swdev/src/core/wsf_l16/source`
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 说明 |
|------|------|------|
| source/header 计数 | 通过 | 本批 240 个 source/header，逐目录与 `rg --files` 结果一致。 |
| file-index 更新 | 通过 | 本批目录均写入 `analysis_unit`、`system`、`subsystem`、`batch`、中文 `brief` 和 `key_symbols`。 |
| 符号索引过滤 | 通过 | 代表符号均为真实 class/function/method，未写入 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 宏。 |
| `vx.json` 排除 | 通过 | `vx.json` 不计入本批 source/header，也未作为代表符号来源。 |
| 文档位置 | 通过 | Markdown 产物均位于 `docs/records` 与 `docs/verification`。 |

## 按目录验证

| 最小目录单元 | source/header 数 | 代表符号数 | 证据来源 | 结果 |
|------|------:|------:|------|------|
| `afsim-2_9/swdev/src/tools/vespatk/source` | 135 | 5 | CodeGraph + 目录内源码扫描 + 子 agent 摘要 | 通过 |
| `afsim-2_9/swdev/src/core/wsf_l16/source` | 105 | 5 | CodeGraph + 目录内源码扫描 + 子 agent 摘要 | 通过 |

## 风险项

- `afsim-2_9/swdev/src/tools/vespatk/source`：工厂扩展依赖字符串 if/else 与 `UserCreate*` 虚扩展点；事件管理使用裸指针和手动 delete，重入与生命周期需后续验证。
- `afsim-2_9/swdev/src/core/wsf_l16/source`：静态全局消息/accessor 状态需要 `ResetState` 防止多场景串状态；DIS/JTIDS/WSF 输出路径交织，J-message 位级解析对 header/字节序/长度敏感。

## 结论

batch42 可接受。该批次已按最小目录单元独立记录职责、核心符号、关键入口链、输入输出和待确认项。
