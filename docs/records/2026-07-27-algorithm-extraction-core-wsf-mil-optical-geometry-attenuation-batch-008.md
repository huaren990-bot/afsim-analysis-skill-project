# AFSIM 算法提取记录：core/wsf_mil optical geometry/attenuation batch 008

## 1. 输入版本

| 输入 | SHA-256 |
| --- | --- |
| `function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `algorithm-candidates.jsonl` | `ff60c1c8eebec350bec6778328192fecaf9b27f020d009aa23fcfeed49a2cc22` |
| `algorithm-coverage.jsonl` | `6a5d204613bdce652b8864bb80746dc39ff734d6de3b20e4d925ed9912a1aea4` |
| `batch-008-core-wsf-mil-optical-geometry-attenuation.jsonl` | `5d0727b5f2c4c89d3b46b86aa84833dce80a216ad5dffcc552f5d7d057529407` |

## 2. 范围

本批闭环 5 个高优先级光学数学候选，形成 3 个算法：球形地球路径高度（3 个上游别名共享同一源码实现）、默认长方体投影面积、分层简单大气透过率。

## 3. 输出产物

| 算法 ID | 卡片 | 接口规格 |
| --- | --- | --- |
| `ALG-SENSORS-OPTICAL-CURVED-EARTH-PATH-HEIGHT` | `docs/algorithms/sensors-optical-curved-earth-path-height-card.md` | `docs/extracted-algorithms/optical-curved-earth-path-height/sensors-optical-curved-earth-path-height-interface-spec.md` |
| `ALG-SENSORS-OPTICAL-BOX-PROJECTED-AREA` | `docs/algorithms/sensors-optical-box-projected-area-card.md` | `docs/extracted-algorithms/optical-box-projected-area/sensors-optical-box-projected-area-interface-spec.md` |
| `ALG-SENSORS-OPTICAL-LAYERED-SIMPLE-ATTENUATION` | `docs/algorithms/sensors-optical-layered-simple-attenuation-card.md` | `docs/extracted-algorithms/optical-layered-simple-attenuation/sensors-optical-layered-simple-attenuation-interface-spec.md` |

## 4. 候选统计

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected |
| --- | ---: | ---: | ---: | ---: | ---: |
| 全局候选账本 | 8141 | 40 | 6 | 0 | 8095 |
| batch 008 | 5 | 5 | 0 | 0 | 0 |

Compendium 当前流程新增传感器算法为 26 个，文档总算法数为 58。

## 5. 验证摘要

已以 CodeGraph-first 核对实现和调用链；检查 5 个候选源码范围、3 张卡片和 3 份接口规格、算法 ID/Compendium/账本一致性、JSONL 闭环、脚本编译及 `git diff --check`。结论：通过。

## 6. 未决问题

- 长方体投影公式的方位/俯仰与平台体轴精确定义需由平台坐标文档确认。
- 简单衰减模型的 1000 m 分层厚度及密度回调的绝对单位属于迁移配置问题。
