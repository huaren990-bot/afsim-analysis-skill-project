# AFSIM 算法提取验证报告：core/wsf_mil LADAR radiometry/detection batch 007

## 1. 范围与输入摘要

验证范围：`workspace/algorithm-extraction/batches/batch-007-core-wsf-mil-ladar-radiometry-detection.jsonl` 的 5 个候选、5 张卡片、5 份接口规格和 Compendium 更新。源码根为 `source_root/afsim-2_9`。

## 2. 候选状态和覆盖率统计

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected | 结论 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 全局候选账本 | 8141 | 35 | 6 | 0 | 8100 | 持续提取中 |
| batch 007 | 5 | 5 | 0 | 0 | 0 | 通过 |

`algorithm-candidates.jsonl` 和 `algorithm-coverage.jsonl` 均为 8141 条有效 JSON，`candidate_id` 唯一且 ID 集合相同；本批全部为 `extracted` 和 `verification=passed`。

## 3. 源码可追溯性

| candidate_id | Method | 源码位置 | 检查 | 结论 |
| --- | --- | --- | --- | --- |
| `8489be3451662000` | `WsfLADAR_Sensor::SpectralRadiantEmittance#e62bac53c9` | `WsfLADAR_Sensor.cpp:205-232` | 文件、行号、索引 Method 一致 | 通过 |
| `e6e202761aa4beb3` | `WsfLADAR_Sensor::ComputeBackgroundRadiance#5c2a42d009` | `WsfLADAR_Sensor.cpp:234-244` | 文件、行号、索引 Method 一致 | 通过 |
| `4f57213d1ccef7ab` | `WsfLADAR_Sensor::ComputeTargetSolarIrradiance#ad32e21a39` | `WsfLADAR_Sensor.cpp:259-281` | 文件、行号、索引 Method 一致 | 通过 |
| `9a33250f14021782` | `WsfLADAR_Sensor::ComputeGaussianDetectionProbability#a63ba7cb81` | `WsfLADAR_Sensor.cpp:638-681` | 文件、行号、索引 Method 一致 | 通过 |
| `89f195e0973179a5` | `WsfLADAR_Sensor::ComputeProbabilityOfDetection#04d3a9fa19` | `WsfLADAR_Sensor.cpp:601-627` | 文件、行号、索引 Method 一致；精确纳入理由存在 | 通过 |

## 4. 卡片完整性

五张卡片均含 1–10 节，含算法边界、离散公式、变量映射、伪代码、调用链、边界和正常/边界/退化验证计划；无 `TBD` 或模板尖括号占位。每个公式符号均映射到源码变量、常数或明确中间量。

## 5. 公式与变量

| 算法 ID | 已核对公式/分支 | 结论 |
| --- | --- | --- |
| `ALG-SENSORS-LADAR-PLANCK-SPECTRAL-RADIANT-EMITTANCE` | $c_1/[\lambda^5\operatorname{expm1}(c_2/(\lambda T))]$ | 通过 |
| `ALG-SENSORS-LADAR-BACKGROUND-RADIANCE` | 正温度门限与两次 $10^6$ 单位步骤 | 通过 |
| `ALG-SENSORS-LADAR-TARGET-SOLAR-IRRADIANCE` | $SA\rho T/R^2$ | 通过 |
| `ALG-SENSORS-LADAR-GAUSSIAN-DETECTION-PROBABILITY` | 三段 Gaussian CDF 多项式 | 通过 |
| `ALG-SENSORS-LADAR-DETECTION-PROBABILITY-SELECTION` | $S/N$、$Nhc/(\lambda\tau)$、查表优先 | 通过 |

## 6. 接口规格

五份接口规格均含 1–11 节，明确输入输出单位/范围、状态、错误处理、AFSIM 映射、依赖替换、最小示例和三类 oracle。背景初始化规格将面积单位不确定性标为未决而非断言。

## 7. Compendium 与覆盖账本

- 5 个新算法 ID 在 Compendium 主条目中均恰好出现一次，卡片和接口链接存在。
- `ALG-SENSORS-*` 主条目为 23，统计表为传感器/声学 23、合计 55。
- 5 个 extracted 覆盖行均关联一个存在的算法 ID、卡片和接口规格。

## 8. 缺陷清单

无阻断、严重或一般缺陷。

残余风险：背景谱量的面积单位转换位置及 Pd 查表内部语义均超出当前函数边界，已在对应卡片和接口规格中列为未决。

## 9. 结论

结论：通过。

本批 5 个候选已完成真实源码追溯、卡片、接口规格、Compendium、覆盖账本和验证闭环。
