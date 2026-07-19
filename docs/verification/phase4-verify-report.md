# Phase 4 验证报告（基线与重建计划）

> 完成日期：2026-07-16  
> 当前结论：旧 Phase4 产物不通过；新版候选基线和批次计划通过预检查；`phase4-batch01` 已用增强头/源匹配规则重跑并通过批次级验证  
> 注意：本报告当前只覆盖 Phase4 重建基线，最终函数索引生成后需要重跑完整 Phase4 验证。

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|---|---|---|
| 旧 `function-index.jsonl` 可直接复用 | 不通过 | 旧文件存在 2,502 个重复 `qualified_name`，且 1,496 条 Method-level 签名不满足新版门禁 |
| 旧 `function-body-summary.jsonl` 可直接复用 | 不通过 | 旧文件存在 1,689 个重复 `qualified_name`，并包含 `POST_PROCESSOR_LIB_EXPORT::max` 等导出宏伪函数 |
| 新版候选完整唯一键 | 通过 | `qualified_name + signature + path` 重复数为 0 |
| 源码路径存在性 | 通过 | 53,064 条有效候选的源码路径均存在 |
| 导出宏过滤 | 通过 | 有效候选中 `_EXPORT/_IMPORT/_API/_LIB_EXPORT` 伪函数残留为 0 |
| 宏调用过滤 | 通过 | 有效候选中全大写宏调用残留为 0 |
| 控制语句/调用表达式过滤 | 通过 | `if/for/case` 等控制语句残留为 0 |
| 批次计划 | 通过 | 已生成 23 个批次，覆盖 53,064 条候选 |
| `phase4-batch01` JSONL 可解析性 | 通过 | Method-level、body summary、skips 三个 JSONL 均可解析 |
| `phase4-batch01` 唯一性 | 通过 | 2,212 条 Method-level `qualified_name` 无重复 |
| `phase4-batch01` 伪调用过滤 | 通过 | `if/for/else/case/block/get/move` 等关键词/包装调用未残留在 calls |
| `phase4-batch02` 至 `phase4-batch07` 批次验证 | 通过 | 6 个批次合计覆盖率 93.26%，无重复、无配对断裂、无导出宏污染 |
| `phase4-batch08` 至 `phase4-batch13` 批次验证 | 通过 | 6 个批次合计覆盖率 94.35%，无重复、无配对断裂、无导出宏污染 |

## 新版基线统计

| 指标 | 数量 |
|---|---:|
| 有效候选 | 53,064 |
| 已记录跳过项 | 56,419 |
| 批次数 | 23 |
| 候选源码路径缺失 | 0 |
| 完整唯一键重复 | 0 |

## 候选类型分布

| kind | 数量 |
|---|---:|
| `method` | 47,136 |
| `constructor` | 3,806 |
| `destructor` | 1,978 |
| `function` | 153 |

## 跳过原因分布

| 跳过原因 | 数量 | 说明 |
|---|---:|---|
| `parse_failed` | 50,191 | 无有效声明形态、控制语句、调用表达式或无法证明为函数 |
| `macro_generated_unexpanded` | 5,964 | 宏调用或宏生成函数，当前无法可靠展开 |
| `variable_not_function` | 255 | 变量、类型别名、回调容器或成员变量误识别 |

## 旧产物不通过原因

旧版 `function-index.jsonl` 与 `function-body-summary.jsonl` 不能作为 Phase5 输入，主要原因：

1. 导出宏伪函数进入函数体摘要，例如 `POST_PROCESSOR_LIB_EXPORT::max`。
2. `qualified_name` 未携带签名摘要，导致构造函数、重载函数和模板函数有静默覆盖风险。
3. `function-body-summary.jsonl` 存在重复配对和变量伪函数，例如成员变量被当成函数摘要。
4. 部分条目的签名字段缺失或从 `brief` 反推，不满足新版 skill 对 Method-level 可验证函数签名的要求。

## 待完成验证项

以下验证项需要等 23 个批次生成 Method-level 和 body summary 后执行：

| 验证项 | 当前状态 |
|---|---|
| 四层条目完整性 | 通过 |
| 层级追溯完整性 | 通过 |
| Method-level 参数抽样 | 通过基础 schema 校验；深度语义抽样留待业务逻辑分析阶段 |
| `function-body-summary` 配对率 | 通过 |
| lifecycle_role 分布 | 通过；`unknown` 比例 0.00% |
| algorithm_hint 与 computation_density 交叉验证 | 通过基础枚举/配对校验；深度语义抽样留待业务逻辑分析阶段 |
| functions_to_extract 覆盖率 | 通过；有效覆盖率 93.61% |

## 批次 01 验证

| 指标 | 数量 |
|---|---:|
| 输入候选 | 2,329 |
| 读取源码文件 | 94 |
| Method-level 条目 | 2,212 |
| body summary 条目 | 2,212 |
| 跳过项 | 117 |
| 批次覆盖率 | 94.98% |
| 命中原始 path 之外的头/同名文件 | 754 |
| 头文件/inline Method-level 条目 | 800 |

跳过原因全部为 `declaration_only`。增强后脚本会同时搜索 `definition_path`、`path`、`declaration_path`、同名头文件和 inline 文件，已把大量头文件 inline 函数从误跳过转为 Method-level 条目。

`phase4-batch01` 的生命周期分类分布：

| lifecycle_role | 数量 |
|---|---:|
| `configuration` | 905 |
| `simulation_loop` | 333 |
| `utility` | 296 |
| `object_create` | 229 |
| `model_update` | 113 |
| `event_handling` | 111 |
| `scenario_load` | 103 |
| `shutdown` | 95 |
| `output` | 27 |

## 批次 02-07 验证

| 批次 | 输入候选 | Method-level | 跳过 | 覆盖率 | 头/同名文件命中 | 唯一性/配对 |
|---|---:|---:|---:|---:|---:|---|
| phase4-batch02 | 1,903 | 1,823 | 80 | 95.80% | 580 | 通过 |
| phase4-batch03 | 1,862 | 1,693 | 169 | 90.92% | 451 | 通过 |
| phase4-batch04 | 2,203 | 2,132 | 71 | 96.78% | 539 | 通过 |
| phase4-batch05 | 1,872 | 1,732 | 140 | 92.52% | 525 | 通过 |
| phase4-batch06 | 2,595 | 2,383 | 212 | 91.83% | 1,172 | 通过 |
| phase4-batch07 | 2,565 | 2,361 | 204 | 92.05% | 1,002 | 通过 |

合计：

| 指标 | 数量 |
|---|---:|
| 输入候选 | 13,000 |
| Method-level 条目 | 12,124 |
| body summary 条目 | 12,124 |
| 跳过项 | 876 |
| 合计覆盖率 | 93.26% |
| 命中原始 path 之外的头/同名文件 | 4,269 |
| 头文件/inline Method-level 条目 | 2,990 |
| 重复限定名兜底修正 | 30 |

验证结果：

| 检查项 | 结果 | 说明 |
|---|---|---|
| JSONL 可解析性 | 通过 | 6 个批次的 Method-level、body summary、skips 均可解析 |
| Method/body 配对 | 通过 | `candidate_id` 集合一致，无配对断裂 |
| `qualified_name` 唯一性 | 通过 | 重复短限定名已追加 `candidate_id` 短后缀 |
| 导出宏过滤 | 通过 | 未发现 `_EXPORT/_IMPORT/_API/_LIB_EXPORT` 伪函数 |
| 伪调用过滤 | 通过 | 未发现 `if/for/else/case/block/get/move` 等残留在 calls |
| 路径存在性 | 通过 | Method-level 记录中的源码路径均存在 |

## 批次 08-13 验证

| 批次 | 输入候选 | Method-level | 跳过 | 覆盖率 | 头/同名文件命中 | 唯一性/配对 |
|---|---:|---:|---:|---:|---:|---|
| phase4-batch08 | 2,587 | 2,358 | 229 | 91.15% | 730 | 通过 |
| phase4-batch09 | 2,494 | 2,323 | 171 | 93.14% | 507 | 通过 |
| phase4-batch10 | 2,456 | 2,325 | 131 | 94.67% | 691 | 通过 |
| phase4-batch11 | 2,251 | 2,183 | 68 | 96.98% | 703 | 通过 |
| phase4-batch12 | 2,388 | 2,312 | 76 | 96.82% | 1,222 | 通过 |
| phase4-batch13 | 2,341 | 2,196 | 145 | 93.81% | 1,149 | 通过 |

合计：

| 指标 | 数量 |
|---|---:|
| 输入候选 | 14,517 |
| Method-level 条目 | 13,697 |
| body summary 条目 | 13,697 |
| 跳过项 | 820 |
| 合计覆盖率 | 94.35% |
| 命中原始 path 之外的头/同名文件 | 5,002 |
| 头文件/inline Method-level 条目 | 2,998 |
| 重复限定名兜底修正 | 44 |

验证结果：

| 检查项 | 结果 | 说明 |
|---|---|---|
| JSONL 可解析性 | 通过 | 6 个批次的 Method-level、body summary、skips 均可解析 |
| Method/body 配对 | 通过 | `candidate_id` 集合一致，无配对断裂 |
| `qualified_name` 唯一性 | 通过 | 重复短限定名已追加 `candidate_id` 短后缀 |
| 导出宏过滤 | 通过 | 未发现 `_EXPORT/_IMPORT/_API/_LIB_EXPORT` 伪函数 |
| 伪调用过滤 | 通过 | 未发现 `if/for/else/case/block/get/move` 等残留在 calls |
| 路径存在性 | 通过 | Method-level 记录中的源码路径均存在 |

## 批次 14-23 验证

| 批次 | 输入候选 | 有效候选 | Method-level | 跳过 | 变量误报 | 原始覆盖率 | 有效覆盖率 | 头/同名/类名文件命中 | 唯一性/配对 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| phase4-batch14 | 2,419 | 2,417 | 2,278 | 141 | 2 | 94.17% | 94.25% | 682 | 通过 |
| phase4-batch15 | 2,424 | 2,418 | 2,276 | 148 | 6 | 93.89% | 94.13% | 449 | 通过 |
| phase4-batch16 | 2,439 | 2,434 | 2,302 | 137 | 5 | 94.38% | 94.58% | 738 | 通过 |
| phase4-batch17 | 2,510 | 2,500 | 2,326 | 184 | 10 | 92.67% | 93.04% | 981 | 通过 |
| phase4-batch18 | 2,466 | 2,399 | 2,184 | 282 | 67 | 88.56% | 91.04% | 428 | 通过 |
| phase4-batch19 | 2,575 | 2,567 | 2,385 | 190 | 8 | 92.62% | 92.91% | 851 | 通过 |
| phase4-batch20 | 2,422 | 2,421 | 2,308 | 114 | 1 | 95.29% | 95.33% | 1,045 | 通过 |
| phase4-batch21 | 2,658 | 2,642 | 2,399 | 259 | 16 | 90.26% | 90.80% | 950 | 通过 |
| phase4-batch22 | 2,447 | 2,444 | 2,296 | 151 | 3 | 93.83% | 93.94% | 888 | 通过 |
| phase4-batch23 | 858 | 858 | 774 | 84 | 0 | 90.21% | 90.21% | 308 | 通过 |

合计：

| 指标 | 数量 |
|---|---:|
| 输入候选 | 23,218 |
| 有效候选 | 23,100 |
| Method-level 条目 | 21,528 |
| body summary 条目 | 21,528 |
| 跳过项 | 1,690 |
| 变量/表达式误报候选 | 118 |
| 原始覆盖率 | 92.72% |
| 有效覆盖率 | 93.19% |
| 命中原始 path 之外的头/同名/类名文件 | 7,320 |
| 重复限定名兜底修正 | 911 |

batch18 原始覆盖率低于 90% 的主要原因是旧索引把局部变量直接初始化、throw 表达式、return 表达式、typeid/流输出片段误识别为 Method 候选。新版脚本把这些条目标为 `variable_not_function`，仅从有效候选分母中剔除，不生成 Method-level 条目。

验证结果：

| 检查项 | 结果 | 说明 |
|---|---|---|
| JSONL 可解析性 | 通过 | 10 个批次的 Method-level、body summary、skips 均可解析 |
| Method/body 配对 | 通过 | `candidate_id` 集合一致，无配对断裂 |
| `qualified_name` 唯一性 | 通过 | 重复短限定名已追加 `candidate_id` 短后缀 |
| 导出宏过滤 | 通过 | 未发现 `_EXPORT/_IMPORT/_API/_LIB_EXPORT` 伪函数 |
| 伪调用过滤 | 通过 | 未发现 `if/for/else/case/block/get/move` 等残留在 calls |
| 路径存在性 | 通过 | Method-level 记录中的源码路径均存在 |

## 全量批次闭环

| 指标 | 数量 |
|---|---:|
| 批次数 | 23 |
| 输入候选 | 53,064 |
| 有效候选 | 52,946 |
| Method-level 条目 | 49,561 |
| body summary 条目 | 49,561 |
| 跳过项 | 3,503 |
| 变量/表达式误报候选 | 118 |
| 原始覆盖率 | 93.40% |
| 有效覆盖率 | 93.61% |

## 最终四层合并验证

最终输出：

```text
workspace/source-index/function-index.jsonl
workspace/source-index/function-body-summary.jsonl
workspace/source-index/phase4-function-skips.jsonl
workspace/source-index/phase4-merge-summary.json
```

| 层级 | 条目数 |
|---|---:|
| System-level | 1 |
| Module-level | 54 |
| Class-level | 5,415 |
| Method-level | 49,561 |
| function-index 总条目 | 55,031 |

配套产物：

| 产物 | 条目数 |
|---|---:|
| function-body-summary | 49,561 |
| phase4-function-skips | 3,503 |

验证结果：

| 检查项 | 结果 | 说明 |
|---|---|---|
| System → Module 追溯 | 通过 | `sub_functions` 全部可在 Module-level 找到 |
| Module → Class 追溯 | 通过 | `sub_functions` 全部可在 Class-level 找到 |
| Class → Method 追溯 | 通过 | `sub_functions` 全部可在 Method-level 找到 |
| `qualified_name` 全局唯一 | 通过 | 跨批次重复限定名已修正 248 条 |
| Method/body 配对 | 通过 | 49,561 个 Method-level 与 body summary 按 `candidate_id` 一一配对 |
| Method 与 skip 互斥 | 通过 | 无候选同时出现在 Method-level 与 skip 清单 |
| Method-level 路径存在性 | 通过 | 所有 Method-level `path` 均存在 |
| 导出宏过滤 | 通过 | 未发现 `_EXPORT/_IMPORT/_API/_LIB_EXPORT` 伪函数 |
| 伪调用过滤 | 通过 | 未发现 `if/for/else/case/block/get/move` 等残留在 calls |
| lifecycle_role `unknown` 比例 | 通过 | 0.00% |

## 结论

Phase4 的 23 个 Method-level 批次已经按新版 `functions-to-extract-phase4.jsonl` 和 `phase4-function-batch-plan.jsonl` 完成闭环，并已合并生成最终四层 `function-index.jsonl` 与全量 `function-body-summary.jsonl`。该产物可以进入下一步业务逻辑分析。
