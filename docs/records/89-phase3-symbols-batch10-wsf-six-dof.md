# Phase3 Batch10: WSF SixDOF 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 430 |
| 覆盖文件 | 171 |
| CodeGraph 文件读取成功 | 171 |
| 新增 `symbol-index.jsonl` 条目 | 427 |
| 新增 `enum-index.jsonl` 条目 | 6 |
| 标记跳过 | 3 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个文件只读取一次。解析范围覆盖 SixDOF 插件的 engine、propulsion、point-mass、rigid-body、控制接口和测试支撑符号。解析成功的 Phase2 粗符号标记为 `done_batch10`，无法在源码中定位真实 C++ 声明的候选标记为 `skipped_unresolved_phase2_symbol_batch10`。

## 跳过项

| 符号 | kind | 路径 | 原因 |
|---|---|---|---|
| `test_six_dof_utils` | class | `afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/test/test_six_dof_utils.cpp` | Phase2 将测试文件名误归类为 class，源码无对应 class 声明 |
| `WsfPointMassSixDOF_PropulsionSystem` | class | `afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfPointMassSixDOF_PropulsionSystem.cpp` | 实现文件中无同名 class 声明 |
| `WsfRigidBodySixDOF_PropulsionSystem` | class | `afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfRigidBodySixDOF_PropulsionSystem.cpp` | 实现文件中无同名 class 声明 |

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 427 条 `phase3:batch10` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 6 条 `phase3:batch10` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 427 条标记为 `done_batch10`，3 条标记为 `skipped_unresolved_phase2_symbol_batch10` |

