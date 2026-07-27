# AFSIM 算法提取记录：core/wsf_mil SAR performance batch 005

## 1. 输入版本

| 输入 | SHA-256 |
| --- | --- |
| `workspace/source-index/function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `workspace/source-index/function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `workspace/algorithm-extraction/algorithm-candidates.jsonl` | `105b3c563bc5ff8e87ba6e9f421e4865fe6d692a6bbabbff60b7107126f192af` |
| `workspace/algorithm-extraction/algorithm-coverage.jsonl` | `7a21036da2f7b9b82e853ace51ea0204e87e50ee482651d49ce445a0ea1ce5df` |
| `workspace/algorithm-extraction/batches/batch-005-core-wsf-mil-sar-performance.jsonl` | `7573e11985f810b0e0b7e2196edbce5fd87852c33931550c3c7d4a73a1bd452c` |

备注：function-body-summary 哈希沿用本轮实际校验输出；本记录不表示索引已重新生成。

## 2. 范围

本批处理 `core/wsf_mil` 中 `WsfSAR_Sensor.cpp` 的三个 SAR 性能/几何候选：

| candidate_id | Method | 源码范围 | 决策 |
| --- | --- | --- | --- |
| `700e32cae89966e0` | `WsfSAR_Sensor::ComputeAzimuthResolution#091f833369` | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2192-2232` | extracted |
| `0b890e242f61ebe9` | `WsfSAR_Sensor::ComputeCNR#1c885b981d` | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2063-2129` | extracted |
| `8a395a5e539e9ed8` | `WsfSAR_Sensor::ComputeFOV#e0203ca715` | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2628-2688` | extracted |

选择理由：三个候选同属 SAR 成像性能链，与已提取 `ALG-SENSORS-SAR-DWELL-TIME` 同域，但算法边界独立，可分别验证和迁移。

## 3. 输出产物

| 算法 ID | 卡片 | 接口规格 |
| --- | --- | --- |
| `ALG-SENSORS-SAR-AZIMUTH-RESOLUTION` | `docs/algorithms/sensors-sar-azimuth-resolution-card.md` | `docs/extracted-algorithms/sar-azimuth-resolution/sensors-sar-azimuth-resolution-interface-spec.md` |
| `ALG-SENSORS-SAR-CLUTTER-TO-NOISE-RATIO` | `docs/algorithms/sensors-sar-clutter-to-noise-ratio-card.md` | `docs/extracted-algorithms/sar-clutter-to-noise-ratio/sensors-sar-clutter-to-noise-ratio-interface-spec.md` |
| `ALG-SENSORS-SAR-IMAGE-FIELD-OF-VIEW` | `docs/algorithms/sensors-sar-image-field-of-view-card.md` | `docs/extracted-algorithms/sar-image-field-of-view/sensors-sar-image-field-of-view-interface-spec.md` |

同步更新：

- `docs/algorithms/CompendiumofAlgorithms.md`
- `workspace/algorithm-extraction/algorithm-candidates.jsonl`
- `workspace/algorithm-extraction/algorithm-coverage.jsonl`
- `workspace/algorithm-extraction/batches/batch-005-core-wsf-mil-sar-performance.jsonl`

## 4. 候选统计

运行 `apply_algorithm_decisions.py` 后：

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected |
| --- | ---: | ---: | ---: | ---: | ---: |
| 全局候选账本 | 8138 | 26 | 2 | 0 | 8110 |
| batch 005 | 3 | 3 | 0 | 0 | 0 |

## 5. 关键源码结论

- `ComputeAzimuthResolution` 使用 `lambda * Ka * R / (2 * V * dwell * |sin(squint)| * cos(grazing))`，但 `mAngularResolution > 0` 时优先走旧路径；背面或退化几何返回 1000 m。
- `ComputeCNR` 先计算 ground patch RCS，再经 AFSIM `ComputeRF_TwoWayPower`、脉冲压缩、`int(dwell*PRF)` 脉冲积分、积分增益和调整因子，最后除噪声功率；扫描角 `>=90 deg` 返回 `1e-37`。
- `ComputeFOV` 在存在 cue 且图像宽高均为正时，根据 terrain-aware 图像中心、斜距、NED down 分量和 positive-down depression angle 反算天线 FOV。

## 6. 验证摘要

执行的检查：

- CodeGraph-first 检查目标函数、调用者和源码。
- 解析候选/覆盖 JSONL，确认 8138 行、ID 集合一致、状态统计一致。
- 核对本批 3 个 candidate_id 与 function-index、body-summary、真实源码路径和行号一致。
- 确认本批卡片 1-10 节、接口规格 1-11 节存在，无模板占位内容。
- 确认 Compendium 中 3 个新增算法 ID 各 1 个主条目，当前 `ALG-SENSORS-*` 主条目为 14。
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile` 通过两个算法提取脚本。
- `git diff --check` 通过本批相关文件。

结论：本批通过。

## 7. 未决问题

- `ComputeCNR` 的默认 backscatter 经验式源码内标有 TODO，迁移实现需要外部模型资料或黄金场景确认适用范围。
- `ComputeFOV` 调用的 `ComputeImageCenter` 具有地形遮挡递归逻辑，本批作为辅助依赖记录，后续可独立审查是否扩展成算法卡。
- `ComputeAzimuthResolution` 对 `scan_angle == pi/2` 的处理与 dwell-time 算法不同；当前按源码兼容记录。
