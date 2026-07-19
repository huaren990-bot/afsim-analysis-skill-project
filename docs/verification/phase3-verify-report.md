# Phase 3 符号级细粒度分析验证报告

> **日期**：2026-07-16  
> **阶段**：Phase 3 / 7  
> **状态**：通过；Phase2 粗符号追溯闭环覆盖率已达到 100%

## 验证对象

| 产物 | 路径 | 当前条目数 | 说明 |
|---|---|---:|---|
| Phase2 粗符号快照 | `workspace/source-index/symbol-index-phase2.jsonl` | 12,108 | Phase3 追溯分母 |
| Phase3 精细符号索引 | `workspace/source-index/symbol-index.jsonl` | 90,524 | 已清理导出宏伪符号并补入 batch01-batch29 |
| 宏索引 | `workspace/source-index/macro-index.jsonl` | 9,371 | 已过滤导出/API/import 宏、include guard、边界外 training 宏 |
| 枚举索引 | `workspace/source-index/enum-index.jsonl` | 1,159 | DIS xenum include 已补齐；仍有 2 个旧有空枚举 |
| Phase3 工作清单 | `workspace/source-index/symbols-to-refine-phase3.jsonl` | 12,108 | `pending=0` |

## 检查结果汇总

| # | 检查项 | 结果 | 当前证据 |
|---|---|---|---|
| 1 | JSONL 可解析 | 通过 | 5 个 JSONL 文件均可逐行解析 |
| 2 | 导出宏伪符号过滤 | 通过 | `symbol-index.jsonl` 中匹配 `*_EXPORT/*_IMPORT/*_API/*_LIB_EXPORT` 的伪符号为 0 |
| 3 | macro-index 过滤 | 通过 | 违规宏为 0 |
| 4 | enum-index values 完整性 | 警告 | 1,159 个枚举中仍有 2 个旧有空枚举：`engage::Phase`、`UtStringEnumId` |
| 5 | Phase2 到 Phase3 追溯 | 通过 | 12,108 个 Phase2 粗符号均已转为已完成或有明确跳过原因 |
| 6 | 粗版快照保留 | 通过 | `symbol-index-phase2.jsonl` 存在且可解析 |

## 闭环统计

| 指标 | 数量 |
|---|---:|
| Phase2 粗符号分母 | 12,108 |
| 已完成/已有匹配 | 11,971 |
| 已记录跳过 | 137 |
| 未解释缺失 | 0 |
| pending | 0 |
| 闭环覆盖率 | 100.00% |

## batch19-batch29 收尾

| 批次 | 范围 | 输入 | 补齐 | 跳过 | 说明 |
|---|---|---:|---:|---:|---|
| batch19 | `tools/dis` | 218 | 218 | 0 | DIS 协议枚举、结构、namespace；xenum include values 已补齐 |
| batch20 | `core/wsf_space` | 189 | 184 | 5 | 空间模型；跳过项为测试宏/测试文件名/实现文件名误分类 |
| batch21 | `wsf_plugins/wsf_iads_c2_lib` | 183 | 177 | 6 | IADS C2 库；跳过项为注释词 typedef 和错误路径函数引用 |
| batch22 | `core/wsf_cyber` | 169 | 164 | 5 | Cyber C++ 符号；CMake/grammar 条目按非 C++ formal symbol 跳过 |
| batch23 | `tools/util_script` | 151 | 148 | 3 | 脚本工具 C++ 符号；test/cmake 条目跳过 |
| batch24 | `wizard/usmtf` | 138 | 134 | 4 | USMTF C++ 符号；测试文件名误分类跳过 |
| batch25 | `wsf_plugins/wsf_oms_uci` | 128 | 125 | 3 | OMS/UCI C++ 符号；实现文件名误分类跳过 |
| batch26 | `post_processor/WizPostProcessor` | 113 | 113 | 0 | 后处理插件符号全闭环 |
| batch27 | `wsf_plugins/wsf_coverage` | 112 | 107 | 5 | Coverage C++ 符号；CMake/grammar 条目跳过 |
| batch28 | `core/wsf_parser` | 94 | 90 | 4 | Parser C++ 符号；错误路径函数引用跳过 |
| batch29 | residual scopes | 445 | 431 | 14 | 小目录收尾；宏/test_case 等非 symbol 条目跳过，7 条真实模板/嵌套类型已补正 |

## 剩余警告

| 问题 | 当前状态 | 建议 |
|---|---|---|
| 2 个旧有枚举 `values` 为空 | 不影响 Phase2 → Phase3 追溯闭环 | 后续可单独定位 `engage::Phase`、`UtStringEnumId` 的真实定义来源 |
| `refined_by_qualified_name` 仍有 711 条 | 属于早期同名追溯口径，不是 pending 缺失 | 后续若需要更强一致性，可做 Phase3.1 exact-key 对齐 |

## 结论

Phase3 已达到本轮目标：`symbols-to-refine-phase3.jsonl` 中无 `pending`，Phase2 粗符号追溯闭环覆盖率为 100%。当前产物可作为下一步 AFSIM 业务逻辑分析的符号级基础输入。

