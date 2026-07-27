# AFSIM 算法提取验证报告：core/wsf_mil SAR performance batch 005

## 1. 范围与输入摘要

验证范围：`workspace/algorithm-extraction/batches/batch-005-core-wsf-mil-sar-performance.jsonl` 中 3 个候选及其产物。

输入：

- `workspace/algorithm-extraction/algorithm-candidates.jsonl`
- `workspace/algorithm-extraction/algorithm-coverage.jsonl`
- `workspace/source-index/function-index.jsonl`
- `workspace/source-index/function-body-summary.jsonl`
- AFSIM 源码根：`source_root/afsim-2_9`
- 本批 3 张算法卡、3 份接口规格和 Compendium

## 2. 候选状态和覆盖率统计

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected | 结论 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 全局候选账本 | 8138 | 26 | 2 | 0 | 8110 | 持续提取中 |
| batch 005 | 3 | 3 | 0 | 0 | 0 | 通过 |

JSONL 检查：

- `algorithm-candidates.jsonl`：8138 行，`candidate_id` 唯一。
- `algorithm-coverage.jsonl`：8138 行，与候选账本 ID 集合一致。
- `batch-005-core-wsf-mil-sar-performance.jsonl`：3 行，均为 `extracted` 且 `verification=passed`。

## 3. 源码可追溯性

| candidate_id | Method | 索引源码位置 | 真实源码检查 | body-summary | 结论 |
| --- | --- | --- | --- | --- | --- |
| `700e32cae89966e0` | `WsfSAR_Sensor::ComputeAzimuthResolution#091f833369` | `WsfSAR_Sensor.cpp:2192-2232` | 文件存在，行号在 3203 行范围内 | 匹配 | 通过 |
| `0b890e242f61ebe9` | `WsfSAR_Sensor::ComputeCNR#1c885b981d` | `WsfSAR_Sensor.cpp:2063-2129` | 文件存在，行号在 3203 行范围内 | 匹配 | 通过 |
| `8a395a5e539e9ed8` | `WsfSAR_Sensor::ComputeFOV#e0203ca715` | `WsfSAR_Sensor.cpp:2628-2688` | 文件存在，行号在 3203 行范围内 | 匹配 | 通过 |

CodeGraph-first 检查确认：

- `ComputeAzimuthResolution` 被 `AttemptToDetect`、`SpotModeBegin`、`SpotModeEnd`、`PredictPerformance` 调用。
- `ComputeCNR` 被 `SpotModeEnd` 和 `PredictPerformance` 调用。
- `ComputeFOV` 被 `ComputeGeometry` 调用。
- 这三个符号无直接测试覆盖，验证采用源码核对和独立数值 oracle。

## 4. 卡片完整性

| 算法 ID | 卡片 | 章节 1-10 | 源码证据 | 正常/边界/退化验证 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `ALG-SENSORS-SAR-AZIMUTH-RESOLUTION` | `docs/algorithms/sensors-sar-azimuth-resolution-card.md` | 完整 | source-cited | 完整 | 通过 |
| `ALG-SENSORS-SAR-CLUTTER-TO-NOISE-RATIO` | `docs/algorithms/sensors-sar-clutter-to-noise-ratio-card.md` | 完整 | source-cited | 完整 | 通过 |
| `ALG-SENSORS-SAR-IMAGE-FIELD-OF-VIEW` | `docs/algorithms/sensors-sar-image-field-of-view-card.md` | 完整 | source-cited | 完整 | 通过 |

占位符检查未发现 `TBD`、模板尖括号占位或省略调用链。`<cmath>` 等真实 C++ 标识未按占位符处理。

## 5. 公式与变量

| 算法 ID | 公式检查 | 变量映射 | 风险记录 |
| --- | --- | --- | --- |
| `ALG-SENSORS-SAR-AZIMUTH-RESOLUTION` | 正常公式、旧角分辨率路径和 1000 m 哨兵均映射源码 | `frequency`、`mKa`、`Geometry`、`aDwellTime`、`mAngularResolution` 均已映射 | `scan > pi/2` 与 dwell-time 的 `>=` 差异已记录 |
| `ALG-SENSORS-SAR-CLUTTER-TO-NOISE-RATIO` | backscatter 默认式、RCS、脉冲积分和 CNR 后处理链均映射源码 | `mBackscatterCoefficient`、`aResolution`、`aPRF`、`aDwellTime`、`mIntegrationGain`、`mAdjustmentFactor` 均已映射 | RF 功率模型强框架耦合已记录 |
| `ALG-SENSORS-SAR-IMAGE-FIELD-OF-VIEW` | 方位半角、俯仰上下半角和限幅均映射源码 | cue、WCS/NED、图像宽高、depression angle 和天线 FOV 均已映射 | `ComputeImageCenter` 作为辅助依赖记录 |

未发现把离散源码分支误写为连续模型的问题。

## 6. 接口规格

| 算法 ID | 接口规格 | 章节 1-11 | AFSIM 映射 | 示例和 oracle | 结论 |
| --- | --- | --- | --- | --- | --- |
| `ALG-SENSORS-SAR-AZIMUTH-RESOLUTION` | `docs/extracted-algorithms/sar-azimuth-resolution/sensors-sar-azimuth-resolution-interface-spec.md` | 完整 | 明确 | 明确 | 通过 |
| `ALG-SENSORS-SAR-CLUTTER-TO-NOISE-RATIO` | `docs/extracted-algorithms/sar-clutter-to-noise-ratio/sensors-sar-clutter-to-noise-ratio-interface-spec.md` | 完整 | 明确 | 明确 | 通过 |
| `ALG-SENSORS-SAR-IMAGE-FIELD-OF-VIEW` | `docs/extracted-algorithms/sar-image-field-of-view/sensors-sar-image-field-of-view-interface-spec.md` | 完整 | 明确 | 明确 | 通过 |

## 7. Compendium 与覆盖账本

- Compendium 中新增 3 个算法主条目，均恰好出现一次。
- 当前 `ALG-SENSORS-*` 主条目数为 14。
- 统计表已更新为传感器/声学 14、合计 46。
- 覆盖账本中 3 个候选均为 `extracted`，artifact 路径存在，算法 ID 与卡片/接口一致。

## 8. 缺陷清单

无阻断或严重缺陷。

一般风险：

- `ALG-SENSORS-SAR-CLUTTER-TO-NOISE-RATIO`：默认 backscatter 经验式来源需外部资料复核。
- `ALG-SENSORS-SAR-IMAGE-FIELD-OF-VIEW`：`ComputeImageCenter` 未在本批独立展开。

## 9. 结论

结论：通过。

本批 3 个 SAR 算法已完成源码追溯、卡片、接口规格、Compendium 和覆盖账本闭环。
