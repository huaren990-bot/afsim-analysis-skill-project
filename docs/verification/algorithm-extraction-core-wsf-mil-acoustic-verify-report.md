# `core/wsf_mil` 被动声学算法提取验证报告

> 日期：2026-07-23  
> 范围：`WsfAcousticSensor.cpp` 首批与第二批算法提取  
> 结论：**通过**

## 1. 范围与输入

验证对象：

- `workspace/algorithm-extraction/algorithm-candidates.jsonl`
- `workspace/algorithm-extraction/algorithm-coverage.jsonl`
- `workspace/algorithm-extraction/batches/batch-001-core-wsf-mil-acoustic.jsonl`
- `workspace/algorithm-extraction/batches/batch-002-core-wsf-mil-acoustic.jsonl`
- 5 张算法卡、5 份接口规格和 `docs/algorithms/CompendiumofAlgorithms.md`
- `workspace/source-index/function-index.jsonl`
- `workspace/source-index/function-body-summary.jsonl`
- `source_root/afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfAcousticSensor.cpp`

输入摘要：

| 文件 | SHA-256 |
| --- | --- |
| `function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `algorithm-candidates.jsonl` | `d4ce8b555698c62cd29fd50f7dca3614f820c792c5cb2376bfd586c2acb71c82` |
| `algorithm-coverage.jsonl` | `b377df8ed75d777afe69eeb4b79e8c86dc7c493a86568ca2de1207a61977ba9e` |

## 2. 候选状态与覆盖率

全局分母为 8,137 条候选：

| 状态 | 数量 |
| --- | ---: |
| extracted | 12 |
| rejected | 2 |
| deferred | 0 |
| selected | 0 |
| pending | 8,123 |

全局候选闭环率为 `14 / 8137 = 0.1721%`。这不构成 AFSIM 全量完成声明。

本次范围分母为两个批次的 14 条候选记录：

| 批次 | 候选 | extracted | rejected | pending/selected | 物理算法 |
| --- | ---: | ---: | ---: | ---: | ---: |
| batch-001 | 6 | 4 | 2 | 0 | 2 |
| batch-002 | 8 | 8 | 0 | 0 | 3 |
| 合计 | 14 | 12 | 2 | 0 | 5 |

本次范围闭环率为 100%。多个候选记录是同一物理函数的索引别名，因此候选数不等于算法数。

## 3. 检查结果

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| JSONL 解析 | 通过 | 候选、覆盖和两个批次逐行解析成功 |
| 候选/覆盖唯一性 | 通过 | 两份账本各 8,137 个唯一 `candidate_id` |
| 批次闭环 | 通过 | 14 条均为 `extracted` 或 `rejected` |
| 源码定位 | 通过 | 14 条逐条核对真实路径和行号范围 |
| function/body 连接 | 通过 | 按 `candidate_id + qualified_name + path + line range` 精确匹配 |
| Method 契约 | 通过 | 卡片中的主 Method 均存在于当前 `function-index.jsonl` |
| 卡片完整性 | 通过 | 5 张卡均包含模板 10 节，无占位内容 |
| 接口完整性 | 通过 | 5 份规格均包含模板 11 节，并声明“规格，不代表实现” |
| 算法粒度 | 通过 | 传播吸收、概率、Doppler、地面效应和听觉加权独立成卡；编排器被拒绝 |
| Compendium | 通过 | 5 个算法 ID 各出现一次，链接存在，总数更新为 37 |
| 覆盖账本产物 | 通过 | 12 条 extracted 均关联存在的卡片、接口和 `passed` |
| 拒绝理由 | 通过 | 2 条 `AttemptToDetect` 别名均有具体编排器拒绝理由 |
| 可续跑性 | 通过 | 默认重跑仍保留 4 条显式纳入的误分类候选，总数保持 8,137 |

## 4. 数值复验

| 算法 | 独立输入 | 结果 | 容差 |
| --- | --- | ---: | ---: |
| 大气声吸收 | 288.15 K、RH 0.5、压力比 1、1000 Hz | `0.29636178637145016` dB/100 m | `1e-12` |
| 探测概率 | $\beta=1,0,-1$ | `0.8413513380564247`、`0.5`、`0.1586486619435753` | `1e-12` |
| Doppler 系数 | $c=340,v_r=10,v_s=20$ m/s | `1.09375` | `1e-12` |
| 听觉加权 | band 5、常数谱 1 | `1.5309599999999999` | `1e-12` |
| 地面效应 | 卡片第 8 节完整复数样例 | `1.6262959722255055` | `1e-12` |

数值 oracle 由独立标量/复数实现计算，不调用 AFSIM 代码。

## 5. 缺陷清单

本批产物未发现阻断、严重、一般或轻微缺陷。

以下是已在卡片和接口中显式保留的上游/模型风险，不属于本次文档缺陷：

1. `function-index.jsonl` 全局存在 5,469 条超出唯一 ID 集合的重复 ID 记录；验证已使用完整复合定位消歧。
2. `GroundEffectAttenuation` 的线性式返回值被调用者直接当作 dB 相加，单位尚未闭合。
3. `ComputeIncidenceAngle` 的注释与变换实参需要场景黄金数据复核；`aLoc` 注释称 WCS，但实际写入 LLA。
4. `ApplyFilterWeighting` 在 band 1、2 不访问低频邻居，且线性声级正式物理单位待确认。
5. Doppler 函数注释称返回“除数”，但当前调用者实际把它乘到频率上；兼容规格采用真实调用行为。

这些风险会阻塞相应迁移决策，但不阻塞“源码行为已被准确提取并标明未知”的验收结论。

## 6. 结论

两个批次的 5 个声学算法均满足源码可追溯、公式/变量映射、接口契约、边界风险和三类验证要求；批次范围通过。全局仍有 8,123 条候选待处理。
