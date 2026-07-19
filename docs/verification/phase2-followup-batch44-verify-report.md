# Phase 2 batch44 增量验证报告

> **验证日期**：2026-07-15
> **验证对象**：Phase 2 最小目录单元增量产物
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 目录边界 | 通过 | 本批 4 个最小目录单元均按独立 `analysis_unit` 写入工作清单和 file-index。 |
| source/header 计数 | 通过 | 本批合计 72 个 source/header；验证脚本按 file-index 路径前缀复算。 |
| 代表性符号 | 通过 | 本批新增 20 条代表性符号，均写入 `workspace/source-index/symbol-index-phase2.jsonl`。 |
| 导出宏过滤 | 通过 | 本批未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为符号写入。 |
| Markdown 产物位置 | 通过 | 批次记录与验证报告均位于 `docs/` 下。 |

## 单元复核

| 最小目录单元 | 计数 | 状态 | 主要风险 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/core/wsf_util` | 21 | 通过 | UtPack optional/union/conversion 分支复杂；`UtBuffer` 涉及手工内存、字节序和边界检查；schema 输入异常路径需在业务逻辑阶段复核。 |
| `afsim-2_9/swdev/src/post_processor/lib` | 20 | 通过 | 命令行参数存在 `++argIndex` 缺参风险；未知配置多为 warning；`TrajectoryReport` 存在 TODO/空实现，字段 schema 对字符串较敏感。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8` | 14 | 通过 | `missile_type`、`guidance_update_interval` 与外部动态库路径约束严格；目标、track、sensor 缺失分支会影响交战结果。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_multiresolution` | 17 | 通过 | 模板封装较深；fidelity 区间重叠、默认值、loop-after-table-end 与 component name specialization 需要业务阶段复核。 |

## 结论

batch44 已完成。该批可以作为下一步 AFSIM 业务逻辑分析的证据入口，但复杂算法、线程/GUI 生命周期和生成消息 schema 仍应在后续阶段按函数级证据继续追踪。
