# AFSIM 算法提取记录：core/wsf_mil SAR range/calibration batch 006

## 1. 输入版本

| 输入 | SHA-256 |
| --- | --- |
| `workspace/source-index/function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `workspace/source-index/function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `workspace/algorithm-extraction/algorithm-candidates.jsonl` | `dd228ec887c8ba3a6a0f2c6f33e7fab7e866ef22a6f62a4acc1394980ddd8c2e` |
| `workspace/algorithm-extraction/algorithm-coverage.jsonl` | `854e106ec160bd1b471bbf399fa631bb19cdd073433151431e6417e66dc7c8e6` |
| `workspace/algorithm-extraction/batches/batch-006-core-wsf-mil-sar-range-calibration.jsonl` | `209039ea0cca95a8839c59c0b277cbf77a43edf00496d6ae18a8923e18a9b53b` |

## 2. 范围

本批闭环 8 个 SAR range/calibration 相关候选，其中 2 个是按源码证据精确纳入的上游误分类候选：

| candidate_id | Method | 源码范围 | 决策 |
| --- | --- | --- | --- |
| `bb30e1d34a7c26d7` | `WsfSAR_Sensor::ComputeGroundRangeResolution#ac1540f0b7` | `WsfSAR_Sensor.cpp:2235-2261` | extracted |
| `42515149407bd8ce` | `WsfSAR_Sensor::ComputeSlantRange#bb0631eb2b` | `WsfSAR_Sensor.cpp:2273-2338` | extracted |
| `e4ca613fd7961a9d` | `WsfSAR_Sensor::ComputePRF#3eaf3fdd9f` | `WsfSAR_Sensor.cpp:2165-2189` | extracted |
| `c0e8cb95e06388ba` | `WsfSAR_Sensor::Calibrate#7f7c2eeadf` | `WsfSAR_Sensor.cpp:2704-2843` | extracted |
| `b162c5a8b0ee7e90` | `WsfSAR_Sensor::ComputeSquintAngle#3ab342d87b` | `WsfSAR_Sensor.cpp:2342-2354` | rejected |
| `2a34ca464df0add9` | `SAR_ErrorModel::GetErrorCovarianceMatrix#bcb14116e7` | `WsfSAR_Sensor.hpp:215-215` | rejected |
| `8b5a8cbfc67c8712` | `WsfSAR_Sensor::GetErrorCovarianceMatrix#bcb14116e7` | `WsfSAR_Sensor.hpp:215-215` | rejected |
| `00da6c51df212c02` | `WsfSAR_Sensor::SetIntegrationGain#ba2ae667f2` | `WsfSAR_Sensor.hpp:273-273` | rejected |

## 3. 输出产物

| 算法 ID | 卡片 | 接口规格 |
| --- | --- | --- |
| `ALG-SENSORS-SAR-GROUND-RANGE-RESOLUTION` | `docs/algorithms/sensors-sar-ground-range-resolution-card.md` | `docs/extracted-algorithms/sar-ground-range-resolution/sensors-sar-ground-range-resolution-interface-spec.md` |
| `ALG-SENSORS-SAR-SLANT-RANGE-GRAZING` | `docs/algorithms/sensors-sar-slant-range-grazing-card.md` | `docs/extracted-algorithms/sar-slant-range-grazing/sensors-sar-slant-range-grazing-interface-spec.md` |
| `ALG-SENSORS-SAR-PRF-UNAMBIGUOUS-RANGE` | `docs/algorithms/sensors-sar-prf-unambiguous-range-card.md` | `docs/extracted-algorithms/sar-prf-unambiguous-range/sensors-sar-prf-unambiguous-range-interface-spec.md` |
| `ALG-SENSORS-SAR-ONE-M2-CALIBRATION` | `docs/algorithms/sensors-sar-one-m2-calibration-card.md` | `docs/extracted-algorithms/sar-one-m2-calibration/sensors-sar-one-m2-calibration-interface-spec.md` |

同步更新：

- `docs/algorithms/CompendiumofAlgorithms.md`
- `workspace/algorithm-extraction/algorithm-candidates.jsonl`
- `workspace/algorithm-extraction/algorithm-coverage.jsonl`
- `workspace/algorithm-extraction/batches/batch-006-core-wsf-mil-sar-range-calibration.jsonl`

## 4. 候选统计

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected |
| --- | ---: | ---: | ---: | ---: | ---: |
| 全局候选账本 | 8140 | 30 | 6 | 0 | 8104 |
| batch 006 | 8 | 4 | 4 | 0 | 0 |

本批执行后，Compendium 当前流程新增传感器算法为 18 个，文档总算法数为 50。

## 5. 关键源码结论

- `ComputeGroundRangeResolution` 支持旧角分辨率路径；否则用脉宽或 `1/bandwidth` 计算斜距分辨率，再按最多 45 deg 的擦地角投影成地距分辨率。
- `ComputeSlantRange` 用球形地球三角几何处理负高度、正下方、地平线夹取和低于地平线的斜距/擦地角。
- `ComputePRF` 当前编译路径是 `c/(2R+1)`，普通路径额外乘 0.9。
- `Calibrate` 中的核心算法是 1 m² 自由空间双程雷达方程；若配置检测距离大于 0，会写回接收机噪声功率。
- `ComputeSquintAngle` 只是框架坐标包装，两个 covariance getter 和 integration gain setter 不是独立算法。

## 6. 验证摘要

已执行：

- CodeGraph-first 读取 8 个目标符号及调用链。
- 精确纳入 `ComputePRF` 与 `ComputeSlantRange` 两个上游误分类候选。
- 解析候选/覆盖 JSONL，确认 8140 行、ID 集合一致、状态统计一致。
- 核对 batch 006 所有候选源码路径和行号存在。
- 检查 4 张卡片 1-10 节、4 份接口规格 1-11 节，无模板占位。
- 确认 Compendium 新增 4 个算法 ID 各出现一次，统计为传感器/声学 18、总数 50。
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile` 通过两个算法提取脚本。
- `git diff --check` 通过本批相关文件。

结论：通过。

## 7. 未决问题

- `ComputeSlantRange` 的有效地球半径倍数默认值需在发射机配置链中进一步确认。
- `Calibrate` 核心公式使用 `xmtr.GetPower()`，日志显示 `GetAveragePower()`；迁移时需明确参数命名。
- `ComputePRF` 的 `+1.0` 分母保护缺少源码注释解释，当前按源码兼容记录。
