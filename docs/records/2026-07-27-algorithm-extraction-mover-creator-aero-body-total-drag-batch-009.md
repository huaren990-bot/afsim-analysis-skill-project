# AFSIM 算法提取记录：mover_creator aero body total drag batch 009

## 1. 输入版本

| 输入 | SHA-256 |
| --- | --- |
| `function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `algorithm-candidates.jsonl` | `96acb2c9e4946a2b13172a7d67c0afcbfde1d04e113eaf1343108f207b0e07d5` |
| `algorithm-coverage.jsonl` | `6c2a8236fd548dde1f370faad963e415c6c07b1e068011a15f62ff2553b6cbd1` |
| `batch-009-mover-creator-aero-body-total-drag.jsonl` | `3bcb92ff198f8af12fea3e3b0946f4ff49a937426e37a2822ef98afe4246f0ce` |

## 2. 范围与结果

本批闭环 `AeroBody::CalcDragCoefficient#afedea7029` 及其 `Designer` 索引别名，提取一个总阻力系数算法。它将姿态、诱导、摩擦和外形阻力项相加并乘以总阻力倍率。

| 候选数 | extracted | rejected | deferred | pending/selected |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 2 | 0 | 0 | 0 |

全局账本更新为 8141 候选、42 extracted、6 rejected、8093 pending。

## 3. 产物与验证

- 卡片：`docs/algorithms/aerodynamics-body-total-drag-coefficient-card.md`
- 接口规格：`docs/extracted-algorithms/aero-body-total-drag-coefficient/aerodynamics-body-total-drag-coefficient-interface-spec.md`
- 已更新 Compendium、候选和覆盖账本。
- CodeGraph-first 源码追溯、两候选行号/别名、章节、算法 ID、oracle、JSONL 一致性、`py_compile` 与 `git diff --check` 均通过。

## 4. 未决问题

`cDragMultiplier` 的配置来源和各子系数模型的内部标定不在该函数边界内。
