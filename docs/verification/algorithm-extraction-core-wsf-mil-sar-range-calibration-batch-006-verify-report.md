# AFSIM 算法提取验证报告：core/wsf_mil SAR range/calibration batch 006

## 1. 范围与输入摘要

验证范围：`workspace/algorithm-extraction/batches/batch-006-core-wsf-mil-sar-range-calibration.jsonl` 中 8 个候选及其产物。

输入：

- `workspace/algorithm-extraction/algorithm-candidates.jsonl`
- `workspace/algorithm-extraction/algorithm-coverage.jsonl`
- `workspace/source-index/function-index.jsonl`
- `workspace/source-index/function-body-summary.jsonl`
- AFSIM 源码根：`source_root/afsim-2_9`
- 本批 4 张算法卡、4 份接口规格和 Compendium

## 2. 候选状态和覆盖率统计

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected | 结论 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 全局候选账本 | 8140 | 30 | 6 | 0 | 8104 | 持续提取中 |
| batch 006 | 8 | 4 | 4 | 0 | 0 | 通过 |

JSONL 检查：

- `algorithm-candidates.jsonl`：8140 行，`candidate_id` 唯一。
- `algorithm-coverage.jsonl`：8140 行，与候选账本 ID 集合一致。
- `batch-006-core-wsf-mil-sar-range-calibration.jsonl`：8 行，均为 `extracted` 或 `rejected` 且 `verification=passed`。

## 3. 源码可追溯性

| candidate_id | Method | 源码位置 | 真实源码检查 | 结论 |
| --- | --- | --- | --- | --- |
| `bb30e1d34a7c26d7` | `WsfSAR_Sensor::ComputeGroundRangeResolution#ac1540f0b7` | `WsfSAR_Sensor.cpp:2235-2261` | 文件存在，行号有效 | 通过 |
| `42515149407bd8ce` | `WsfSAR_Sensor::ComputeSlantRange#bb0631eb2b` | `WsfSAR_Sensor.cpp:2273-2338` | 文件存在，行号有效 | 通过 |
| `e4ca613fd7961a9d` | `WsfSAR_Sensor::ComputePRF#3eaf3fdd9f` | `WsfSAR_Sensor.cpp:2165-2189` | 文件存在，行号有效 | 通过 |
| `c0e8cb95e06388ba` | `WsfSAR_Sensor::Calibrate#7f7c2eeadf` | `WsfSAR_Sensor.cpp:2704-2843` | 文件存在，行号有效 | 通过 |
| `b162c5a8b0ee7e90` | `WsfSAR_Sensor::ComputeSquintAngle#3ab342d87b` | `WsfSAR_Sensor.cpp:2342-2354` | 文件存在，行号有效 | 通过 |
| `2a34ca464df0add9` | `SAR_ErrorModel::GetErrorCovarianceMatrix#bcb14116e7` | `WsfSAR_Sensor.hpp:215-215` | 文件存在，行号有效 | 通过 |
| `8b5a8cbfc67c8712` | `WsfSAR_Sensor::GetErrorCovarianceMatrix#bcb14116e7` | `WsfSAR_Sensor.hpp:215-215` | 文件存在，行号有效 | 通过 |
| `00da6c51df212c02` | `WsfSAR_Sensor::SetIntegrationGain#ba2ae667f2` | `WsfSAR_Sensor.hpp:273-273` | 文件存在，行号有效 | 通过 |

## 4. 卡片完整性

| 算法 ID | 卡片 | 章节 1-10 | 源码证据 | 验证计划 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `ALG-SENSORS-SAR-GROUND-RANGE-RESOLUTION` | `docs/algorithms/sensors-sar-ground-range-resolution-card.md` | 完整 | source-cited | 完整 | 通过 |
| `ALG-SENSORS-SAR-SLANT-RANGE-GRAZING` | `docs/algorithms/sensors-sar-slant-range-grazing-card.md` | 完整 | source-cited | 完整 | 通过 |
| `ALG-SENSORS-SAR-PRF-UNAMBIGUOUS-RANGE` | `docs/algorithms/sensors-sar-prf-unambiguous-range-card.md` | 完整 | source-cited | 完整 | 通过 |
| `ALG-SENSORS-SAR-ONE-M2-CALIBRATION` | `docs/algorithms/sensors-sar-one-m2-calibration-card.md` | 完整 | source-cited | 完整 | 通过 |

占位符检查未发现 `TBD`、模板尖括号占位或省略调用链。

## 5. 公式与变量

| 算法 ID | 公式检查 | 变量映射 | 结论 |
| --- | --- | --- | --- |
| `ALG-SENSORS-SAR-GROUND-RANGE-RESOLUTION` | 脉宽/带宽、脉冲压缩、擦地角投影均映射源码 | 完整 | 通过 |
| `ALG-SENSORS-SAR-SLANT-RANGE-GRAZING` | 球面三角、地平线夹取和早退分支均映射源码 | 完整 | 通过 |
| `ALG-SENSORS-SAR-PRF-UNAMBIGUOUS-RANGE` | 普通和 constraint plotting 分支均映射源码 | 完整 | 通过 |
| `ALG-SENSORS-SAR-ONE-M2-CALIBRATION` | 噪声反算和检测距离四次根公式均映射源码 | 完整 | 通过 |

未发现把源码离散分支误写为连续模型的问题。

## 6. 接口规格

| 算法 ID | 接口规格 | 章节 1-11 | AFSIM 映射 | 示例和 oracle | 结论 |
| --- | --- | --- | --- | --- | --- |
| `ALG-SENSORS-SAR-GROUND-RANGE-RESOLUTION` | `docs/extracted-algorithms/sar-ground-range-resolution/sensors-sar-ground-range-resolution-interface-spec.md` | 完整 | 明确 | 明确 | 通过 |
| `ALG-SENSORS-SAR-SLANT-RANGE-GRAZING` | `docs/extracted-algorithms/sar-slant-range-grazing/sensors-sar-slant-range-grazing-interface-spec.md` | 完整 | 明确 | 明确 | 通过 |
| `ALG-SENSORS-SAR-PRF-UNAMBIGUOUS-RANGE` | `docs/extracted-algorithms/sar-prf-unambiguous-range/sensors-sar-prf-unambiguous-range-interface-spec.md` | 完整 | 明确 | 明确 | 通过 |
| `ALG-SENSORS-SAR-ONE-M2-CALIBRATION` | `docs/extracted-algorithms/sar-one-m2-calibration/sensors-sar-one-m2-calibration-interface-spec.md` | 完整 | 明确 | 明确 | 通过 |

## 7. Compendium 与覆盖账本

- Compendium 中新增 4 个算法主条目，均恰好出现一次。
- 当前 `ALG-SENSORS-*` 主条目数为 18。
- 统计表已更新为传感器/声学 18、合计 50。
- 覆盖账本中 4 个 extracted 候选均有关联算法 ID 和存在的 artifact 路径。
- 4 个 rejected 候选均有具体 `decision_reason`。

## 8. 缺陷清单

无阻断、严重或一般缺陷。

残余风险：

- `ComputePRF` 的 `+1.0` 分母保护缺少意图说明。
- `Calibrate` 的 `GetPower()` 与 `GetAveragePower()` 命名差异需在迁移时澄清。

## 9. 结论

结论：通过。

本批 8 个候选已完成源码追溯、算法卡、接口规格、Compendium 和覆盖账本闭环。
