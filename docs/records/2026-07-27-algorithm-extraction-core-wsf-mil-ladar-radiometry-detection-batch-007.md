# AFSIM 算法提取记录：core/wsf_mil LADAR radiometry/detection batch 007

## 1. 输入版本

| 输入 | SHA-256 |
| --- | --- |
| `workspace/source-index/function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `workspace/source-index/function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `workspace/algorithm-extraction/algorithm-candidates.jsonl` | `2928c519dc7b17d3ba4943ccb55c763f64fa43a31fea236be5fad80e31c6fc86` |
| `workspace/algorithm-extraction/algorithm-coverage.jsonl` | `cfdb17b9efc241b1399008dbc55e84c43694c6ab5a81cb00fb5c517c20e0384d` |
| `workspace/algorithm-extraction/batches/batch-007-core-wsf-mil-ladar-radiometry-detection.jsonl` | `ccfaee15506599e3a52dceecd5725dcf31a291c75ba56deb20fdc62c3ae0e990` |

## 2. 范围

本批闭环 5 个 LADAR 辐射、太阳噪声和探测概率相关候选，均为 `extracted`。其中 `ComputeProbabilityOfDetection` 原标记为 `control_flow`，因源码直接输出 S/N、噪声功率和可选择的概率模型而精确纳入。

| candidate_id | Method | 源码范围 | 决策 |
| --- | --- | --- | --- |
| `8489be3451662000` | `WsfLADAR_Sensor::SpectralRadiantEmittance#e62bac53c9` | `WsfLADAR_Sensor.cpp:205-232` | extracted |
| `e6e202761aa4beb3` | `WsfLADAR_Sensor::ComputeBackgroundRadiance#5c2a42d009` | `WsfLADAR_Sensor.cpp:234-244` | extracted |
| `4f57213d1ccef7ab` | `WsfLADAR_Sensor::ComputeTargetSolarIrradiance#ad32e21a39` | `WsfLADAR_Sensor.cpp:259-281` | extracted |
| `9a33250f14021782` | `WsfLADAR_Sensor::ComputeGaussianDetectionProbability#a63ba7cb81` | `WsfLADAR_Sensor.cpp:638-681` | extracted |
| `89f195e0973179a5` | `WsfLADAR_Sensor::ComputeProbabilityOfDetection#04d3a9fa19` | `WsfLADAR_Sensor.cpp:601-627` | extracted |

## 3. 输出产物

| 算法 ID | 卡片 | 接口规格 |
| --- | --- | --- |
| `ALG-SENSORS-LADAR-PLANCK-SPECTRAL-RADIANT-EMITTANCE` | `docs/algorithms/sensors-ladar-planck-spectral-radiant-emittance-card.md` | `docs/extracted-algorithms/ladar-planck-spectral-radiant-emittance/sensors-ladar-planck-spectral-radiant-emittance-interface-spec.md` |
| `ALG-SENSORS-LADAR-BACKGROUND-RADIANCE` | `docs/algorithms/sensors-ladar-background-radiance-card.md` | `docs/extracted-algorithms/ladar-background-radiance/sensors-ladar-background-radiance-interface-spec.md` |
| `ALG-SENSORS-LADAR-TARGET-SOLAR-IRRADIANCE` | `docs/algorithms/sensors-ladar-target-solar-irradiance-card.md` | `docs/extracted-algorithms/ladar-target-solar-irradiance/sensors-ladar-target-solar-irradiance-interface-spec.md` |
| `ALG-SENSORS-LADAR-GAUSSIAN-DETECTION-PROBABILITY` | `docs/algorithms/sensors-ladar-gaussian-detection-probability-card.md` | `docs/extracted-algorithms/ladar-gaussian-detection-probability/sensors-ladar-gaussian-detection-probability-interface-spec.md` |
| `ALG-SENSORS-LADAR-DETECTION-PROBABILITY-SELECTION` | `docs/algorithms/sensors-ladar-detection-probability-selection-card.md` | `docs/extracted-algorithms/ladar-detection-probability-selection/sensors-ladar-detection-probability-selection-interface-spec.md` |

同步更新候选清单、覆盖账本、批次决策和 `docs/algorithms/CompendiumofAlgorithms.md`。

## 4. 候选统计

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected |
| --- | ---: | ---: | ---: | ---: | ---: |
| 全局候选账本 | 8141 | 35 | 6 | 0 | 8100 |
| batch 007 | 5 | 5 | 0 | 0 | 0 |

本批执行后，Compendium 当前流程新增传感器算法为 23 个，文档总算法数为 55。

## 5. 关键源码结论

- `SpectralRadiantEmittance` 实现每 µm 的普朗克谱出射度，并使用 `expm1`。
- `ComputeBackgroundRadiance` 仅在正背景温度时更新状态，显示 m↔µm 谱密度的 $10^6$ 换算；面积单位转换不在函数内。
- `ComputeTargetSolarIrradiance` 的核心公式为 $SA\rho T_a/R^2$。
- Gaussian 探测器对 $\beta=S/N-\theta$ 使用分段正态 CDF 多项式近似，信号非正时为 0。
- `ComputeProbabilityOfDetection` 将光子数换算为 $P_N=Nhc/(\lambda\tau)$，Pd 查表存在时优先于 Gaussian 分支。

## 6. 验证摘要

已执行 CodeGraph-first 源码/调用链核验、候选/覆盖 JSONL 一致性检查、5 张卡片第 1–10 节和 5 份接口规格第 1–11 节检查、Compendium 唯一条目与统计检查、源码路径/行号检查、脚本编译和 `git diff --check`。详细结果见验证报告。

结论：通过。

## 7. 未决问题

- 黑体函数注释的 W/(cm²·µm) 与背景变量下游注释 W/(m²·m) 的面积换算位置需由配置或接收机资料确认。
- Pd 查表 `Lookup` 的插值、外推和范围外夹取语义不在 `ComputeProbabilityOfDetection` 内。
