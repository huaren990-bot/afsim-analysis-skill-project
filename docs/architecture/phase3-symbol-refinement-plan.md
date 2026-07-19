# Phase3 符号级细粒度分析闭环计划

> **日期**：2026-07-16  
> **状态**：已闭环  
> **输入**：`workspace/source-index/symbol-index-phase2.jsonl`  
> **工作清单**：`workspace/source-index/symbols-to-refine-phase3.jsonl`

## 当前基线

| 指标 | 值 |
|---|---:|
| Phase2 粗符号分母 | 12,108 |
| 当前精细符号条目 | 90,524 |
| 宏定义 | 9,371 |
| 枚举 | 1,159 |
| 已完成/已有匹配 | 11,971 |
| 已记录跳过 | 137 |
| 待精细化 | 0 |
| 闭环覆盖率 | 100.00% |
| 导出宏伪符号污染 | 0 |
| 违规宏 | 0 |
| 空 values 枚举 | 2 |

## 执行规则回顾

| 规则 | 执行结果 |
|---|---|
| CodeGraph 优先 | 所有批次均按文件分组调用 `codegraph node <file>` |
| 不重复读取 | 同一批同一文件只读取一次 |
| 粗符号闭环 | 每个 Phase2 符号均为已完成、已有匹配或明确跳过 |
| 导出宏过滤 | `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 未进入正式符号索引 |
| 文档位置 | Markdown 在 `docs/`，JSONL 在 `workspace/` |

## 批次结果

| 批次 | 范围 | 输入 | 补齐 | 跳过 |
|---|---|---:|---:|---:|
| batch01-batch18 | 已记录的核心/插件/工具批次 | 10,168 | 10,080 | 88 |
| batch19 | `tools/dis` | 218 | 218 | 0 |
| batch20 | `core/wsf_space` | 189 | 184 | 5 |
| batch21 | `wsf_plugins/wsf_iads_c2_lib` | 183 | 177 | 6 |
| batch22 | `core/wsf_cyber` | 169 | 164 | 5 |
| batch23 | `tools/util_script` | 151 | 148 | 3 |
| batch24 | `wizard/usmtf` | 138 | 134 | 4 |
| batch25 | `wsf_plugins/wsf_oms_uci` | 128 | 125 | 3 |
| batch26 | `post_processor/WizPostProcessor` | 113 | 113 | 0 |
| batch27 | `wsf_plugins/wsf_coverage` | 112 | 107 | 5 |
| batch28 | `core/wsf_parser` | 94 | 90 | 4 |
| batch29 | residual scopes | 445 | 431 | 14 |

## 跳过口径

| 类型 | 说明 |
|---|---|
| Phase2 误分类 | 测试文件名、实现文件名、注释词、参数片段被粗索引识别为 class/typedef/function |
| 非 C++ formal symbol | CMake project/call/function/extension、grammar_rule、test_case 不写入 `symbol-index.jsonl` |
| 宏条目 | 宏由 `macro-index.jsonl` 跟踪，不作为 `symbol-index.jsonl` formal symbol |
| 错误路径引用 | Phase2 将函数归到不含声明/定义的文件，已在 worklist notes 中记录 |

## 后续建议

Phase3 本轮已完成。下一步可进入业务逻辑分析；若需要进一步提高符号索引质量，可单独开展 Phase3.1：

| 建议项 | 目的 |
|---|---|
| exact-key 对齐 | 将 711 条 `refined_by_qualified_name` 尽量提升为路径/kind 精确匹配 |
| 旧空枚举补齐 | 处理 `engage::Phase`、`UtStringEnumId` 两个旧有空 values 枚举 |
| 成员级增强 | 对关键业务类补充更准确的访问修饰符、条件编译和模板约束信息 |

