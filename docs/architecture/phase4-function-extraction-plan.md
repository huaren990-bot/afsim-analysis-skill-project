# Phase 4 函数/方法级提取计划

> 完成日期：2026-07-16  
> 当前状态：重建基线已完成，头/源匹配规则已增强，`phase4-batch01` 至 `phase4-batch13` 已完成  
> 适用 skill：`cpp-project-analyzer` / `cpp-proj-functions`

## 目标

Phase 4 基于 Phase 3 的最终符号索引，重建函数/方法级产物：

- `workspace/source-index/function-index.jsonl`
- `workspace/source-index/function-body-summary.jsonl`

旧版 Phase4 产物存在导出宏伪函数、调用表达式误入函数、`qualified_name` 重复和函数体摘要误配等问题，不能继续作为 Phase5-Phase7 的可信输入。本轮从 `functions_to_extract` 基线重新闭环。

## 输入边界

| 项目 | 值 |
|---|---|
| 源码根目录 | `/Users/hjt/afsim/afsim-analysis-skill-project/source_root` |
| 分析根目录 | `afsim-2_9` |
| 默认排除 | `afsim-2_9/demos`、`afsim-2_9/documentation`、`afsim-2_9/training`、`afsim-2_9/resources`、隐藏目录、`vx.json` |
| CodeGraph | 已存在：`source_root/afsim-2_9/.codegraph` |
| 编译数据库 | 未发现 `compile_commands.json`，函数解析采用 CodeGraph + 源码文本批量证据 |

## 候选基线

| 指标 | 数量 |
|---|---:|
| Phase4 有效候选函数/方法 | 53,064 |
| 已记录跳过项 | 56,419 |
| 完整唯一键重复 | 0 |
| 缺失源码路径 | 0 |
| 导出宏伪函数残留 | 0 |
| 宏调用残留候选 | 0 |

候选唯一键：

```text
qualified_name + signature + path
```

跳过原因只用于闭环统计，不进入 Method-level：

| 跳过原因 | 含义 |
|---|---|
| `macro_generated_unexpanded` | 宏调用或宏生成函数，当前无法可靠展开 |
| `parse_failed` | 无有效签名、控制语句、调用表达式或无法证明为函数声明 |
| `variable_not_function` | 变量、类型别名、回调容器或成员变量被旧索引误识别为函数 |

## 批次策略

执行时按“父目录最小单元”分组；超大父目录按文件范围拆分；每批尽量合并多个目录单元，但保持候选数约 2,000 到 2,500，便于子 agent 并行处理并降低遗漏风险。

批次计划机器文件：

```text
workspace/source-index/phase4-function-batch-plan.jsonl
```

| 批次 | 候选数 | 文件数 | 目录单元数 | 主要模块 |
|---|---:|---:|---:|---|
| phase4-batch01 | 2329 | 94 | 2 | core/wsf(2)，已完成：Method-level 2,212，跳过 117，覆盖率 94.98% |
| phase4-batch02 | 1903 | 87 | 2 | core/wsf(2)，已完成：Method-level 1,823，跳过 80，覆盖率 95.80% |
| phase4-batch03 | 1862 | 129 | 4 | core/wsf(4)，已完成：Method-level 1,693，跳过 169，覆盖率 90.92% |
| phase4-batch04 | 2203 | 123 | 5 | core/wsf(5)，已完成：Method-level 2,132，跳过 71，覆盖率 96.78% |
| phase4-batch05 | 1872 | 96 | 7 | core/wsf(5), wizard(2)，已完成：Method-level 1,732，跳过 140，覆盖率 92.52% |
| phase4-batch06 | 2595 | 103 | 3 | wizard(3)，已完成：Method-level 2,383，跳过 212，覆盖率 91.83% |
| phase4-batch07 | 2565 | 200 | 16 | wizard(16)，已完成：Method-level 2,361，跳过 204，覆盖率 92.05% |
| phase4-batch08 | 2587 | 195 | 17 | wizard(17)，已完成：Method-level 2,358，跳过 229，覆盖率 91.15% |
| phase4-batch09 | 2494 | 147 | 13 | wizard(11), core/wsf_mil(2)，已完成：Method-level 2,323，跳过 171，覆盖率 93.14% |
| phase4-batch10 | 2456 | 95 | 5 | core/wsf_mil(5)，已完成：Method-level 2,325，跳过 131，覆盖率 94.67% |
| phase4-batch11 | 2251 | 83 | 5 | core/wsf_mil(5)，已完成：Method-level 2,183，跳过 68，覆盖率 96.98% |
| phase4-batch12 | 2388 | 108 | 2 | mover_creator(2)，已完成：Method-level 2,312，跳过 76，覆盖率 96.82% |
| phase4-batch13 | 2341 | 85 | 2 | mover_creator(2)，已完成：Method-level 2,196，跳过 145，覆盖率 93.81% |
| phase4-batch14 | 2419 | 161 | 27 | mover_creator(1), warlock(26)，已完成：有效候选 2,417，Method-level 2,278，跳过 141，覆盖率 94.25% |
| phase4-batch15 | 2424 | 170 | 28 | warlock(28)，已完成：有效候选 2,418，Method-level 2,276，跳过 148，覆盖率 94.13% |
| phase4-batch16 | 2439 | 185 | 45 | warlock(2), mystic(43)，已完成：有效候选 2,434，Method-level 2,302，跳过 137，覆盖率 94.58% |
| phase4-batch17 | 2510 | 131 | 28 | mystic(4), tools/utilosg(9), tools/wkf(15)，已完成：有效候选 2,500，Method-level 2,326，跳过 184，覆盖率 93.04% |
| phase4-batch18 | 2466 | 190 | 20 | tools/wkf(16), tools/util(2), wsf_plugins/wsf_iads_c2_lib(2)，已完成：有效候选 2,399，Method-level 2,184，跳过 282，覆盖率 91.04%，原始覆盖率 88.56% |
| phase4-batch19 | 2575 | 180 | 6 | wsf_plugins/wsf_iads_c2_lib(2), core/wsf_space(3), tools/util_script(1)，已完成：有效候选 2,567，Method-level 2,385，跳过 190，覆盖率 92.91% |
| phase4-batch20 | 2422 | 204 | 13 | tools/util_script(1), wsf_plugins/wsf_p6dof(4), post_processor(3), tools/vespatk(2), core/wsf_cyber(3)，已完成：有效候选 2,421，Method-level 2,308，跳过 114，覆盖率 95.33% |
| phase4-batch21 | 2658 | 145 | 11 | wsf_plugins/wsf_oms_uci(1), core/wsf_nx(4), core/wsf_parser(3), core/wsf_l16(1), tools/dis(1), wsf_plugins/wsf_brawler(1)，已完成：有效候选 2,642，Method-level 2,399，跳过 259，覆盖率 90.80% |
| phase4-batch22 | 2447 | 186 | 20 | wsf_plugins/wsf_brawler(1), engage(1), core/wsf_ripr(2), wsf_plugins/wsf_coverage(2), wsf_plugins/wsf_sosm(2), wsf_plugins/wsf_air_combat(1), core/wsf_util(1), tools/utilqt(2), wsf_plugins/wsf_six_dof(3), core/sensor_plot_lib(1), tools/genio(1), tools/tracking_filters(1), wsf_plugins/wsf_argo8(2)，已完成：有效候选 2,444，Method-level 2,296，跳过 151，覆盖率 93.94% |
| phase4-batch23 | 858 | 103 | 25 | wsf_plugins/wsf_argo8(1), core/wsf_mtt(1), wsf_plugins/wsf_fires(1), weapon_tools(1), wsf_plugins/wsf_scenario_analyzer_iads_c2(1), wsf_plugins/wsf_multiresolution(1), tools/geodata(2), wsf_plugins/wsf_alternate_locations(1), core/wsf_weapon_server(1), tools/artificer(2), wsf_plugins/wsf_simdis(1), tools/packetio(1), tools/scene_gen(1), wsf_plugins/wsf_scenario_analyzer(1), evt_reader(1), tools/profiling(3), core/wsf_mil_parser(1), wsf_plugins/wsf_annotation(1), sensor_plot(1), core/wsf_grammar_check(1), mission(1)，已完成：有效候选 858，Method-level 774，跳过 84，覆盖率 90.21% |

## 执行要求

每个批次必须：

1. 读取批次对应源码文件，每个文件最多读取一次。
2. 生成批次级 Method-level 条目，输出到 `workspace/source-index/phase4-batches/`。
3. 对无法定位函数体的候选写入跳过/降级原因。
4. 保留 `candidate_id`，后续合并时按候选闭环。
5. 批次完成后写入 `docs/records/`，并更新覆盖统计。

批次执行使用增强脚本：

```bash
python3 tools/indexers/phase4_extract_batch.py --batch-id <batch_id> --root .
```

该脚本会同时搜索 `definition_path`、`path`、`declaration_path`、同名头文件和 inline 文件，并从 `owner`/`qualified_name` 提取类名搜索类名同 stem 的源/头/inline 文件。命中头文件 inline 函数或不同名实现文件时，Method-level 的 `path` 写入真实命中文件。

## 下游合并规则

批次全部完成后已通过合并脚本生成最终产物：

```bash
python3 tools/indexers/phase4_merge_outputs.py --root .
```

1. `function-index.jsonl` 必须包含 System-level、Module-level、Class-level、Method-level 四层。
2. Method-level 以 `candidate_id` 和 `qualified_name + signature + path` 去重。
3. `function-body-summary.jsonl` 必须与 Method-level 使用同一唯一键配对。
4. 覆盖率计算口径：

```text
coverage = Method-level 已完成候选 / functions-to-extract-phase4 有效候选
```

5. 覆盖率低于 90% 时，Phase4 不得标记为通过。

当前最终合并结果：

| 指标 | 数量 |
|---|---:|
| System-level | 1 |
| Module-level | 54 |
| Class-level | 5,415 |
| Method-level | 49,561 |
| function-index 总条目 | 55,031 |
| function-body-summary 条目 | 49,561 |
| 有效覆盖率 | 93.61% |
