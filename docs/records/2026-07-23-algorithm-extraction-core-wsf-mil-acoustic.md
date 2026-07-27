# 2026-07-23 `core/wsf_mil` 被动声学算法提取记录

## 1. 目标与范围

在 `cpp-project-analyzer` 已完成的索引基础上启动正式算法提取，首轮限定：

- 模块：`core/wsf_mil`
- 源文件：`WsfAcousticSensor.cpp`
- 批次：
  - `batch-001-core-wsf-mil-acoustic`
  - `batch-002-core-wsf-mil-acoustic`

本记录不声明 `core/wsf_mil` 模块或 AFSIM 全量完成。

## 2. 输入

| 输入 | SHA-256 / 状态 |
| --- | --- |
| `workspace/source-index/function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `workspace/source-index/function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| AFSIM 源码 | `source_root/afsim-2_9` |
| 候选账本 | 8,137 条，源码全部可解析 |

## 3. 处理结果

| 指标 | 数量 |
| --- | ---: |
| 批次候选记录 | 14 |
| extracted | 12 |
| rejected | 2 |
| deferred | 0 |
| 提取的物理算法 | 5 |

提取算法：

1. `ALG-SENSORS-ACOUSTIC-ATMOSPHERIC-ABSORPTION`
2. `ALG-SENSORS-ACOUSTIC-DETECTION-PROBABILITY`
3. `ALG-SENSORS-ACOUSTIC-DOPPLER-COEFFICIENT`
4. `ALG-SENSORS-ACOUSTIC-GROUND-EFFECT`
5. `ALG-SENSORS-ACOUSTIC-AUDITORY-FILTER-WEIGHTING`

拒绝项：

- `AttemptToDetect` 的 2 条候选别名。该函数编排遮蔽、传播、Doppler、滤波、地面效应、门限、组件和脚本回调，不是一个可独立验证的算法。

## 4. 产物

- 5 张算法卡：`docs/algorithms/sensors-acoustic-*-card.md`
- 5 份中性接口规格：`docs/extracted-algorithms/acoustic-*/*-interface-spec.md`
- 更新 `docs/algorithms/CompendiumofAlgorithms.md`，汇总数由 32 项历史结果加本轮 5 项变为 37
- `workspace/algorithm-extraction/algorithm-candidates.jsonl`
- `workspace/algorithm-extraction/algorithm-coverage.jsonl`
- 两份批次决策 JSONL
- `docs/verification/algorithm-extraction-core-wsf-mil-acoustic-verify-report.md`

## 5. Skill 与流水线改进

执行过程中修正了两个可续跑问题：

1. `build_algorithm_candidates.py` 新增可重复的 `--include-candidate-id`，用于精确纳入被上游误标为 `none/control_flow`、但真实源码证明是算法的函数。
2. 已人工闭环的显式候选在以后默认重跑时保留，避免候选分母回退。
3. `apply_algorithm_decisions.py` 重建覆盖账本时保留旧批次的 `artifacts` 与 `verification`，避免后续批次抹除历史证据。

默认重跑验证结果：候选总数仍为 8,137，4 条显式候选均保留为 `extracted`。

## 6. 验证

- 14 条批次候选全部回连 function/body 索引和真实源码。
- 5 张卡、5 份接口、Compendium 与覆盖账本的算法 ID 和路径一致。
- 5 个算法均完成正常、边界和退化/异常验证设计。
- 5 组独立数值 oracle 通过，详见验证报告。
- `git diff --check` 通过。

结论：本轮范围通过。

## 7. 未决问题

| ID | 问题 | 影响 | 下一步 |
| --- | --- | --- | --- |
| ACOUSTIC-001 | 地面效应返回值的线性/dB 单位不闭合 | 阻塞直接迁移 | 用 Ref 1 与黄金场景确认 |
| ACOUSTIC-002 | 反射点 NED 变换实参与注释不一致；`aLoc` 注释称 WCS、实际写 LLA | 阻塞反射几何迁移 | 建立已知平地几何单测 |
| ACOUSTIC-003 | 听觉加权低频邻域和线性声级单位 | 影响跨系统接口 | 核对 Ref 3 与签名输入文档 |
| ACOUSTIC-004 | Doppler 注释与实际乘法调用矛盾 | 影响 API 命名 | 以黄金频移输出确认兼容行为 |
| ACOUSTIC-005 | ESDU/MDC/A&S 外部文献未逐项核验 | 影响理论来源追溯 | 在许可证允许条件下补充文献证据 |
