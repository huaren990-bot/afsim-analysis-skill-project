# 2026-07-24 `core/wsf_mil` ESA 相控阵第四批算法提取记录

## 1. 目标与范围

继续提取 3 个同属 `WsfESA_AntennaPattern` 的独立算法：

1. ESA Taylor 阵元幅度加权；
2. ESA 加权相控阵阵因子；
3. ESA 幅度权重孔径效率。

主范围为：

- `WsfESA_AntennaPattern.cpp:303-437`
- `WsfESA_AntennaPattern.cpp:440-498`
- `WsfESA_AntennaPattern.cpp:609-649`
- 共享量化依赖 `WsfESA_AntennaPattern.cpp:518-530`

为确认生命周期、配置、坐标和效率语义，补查同文件的构造、初始化、布局、失效、增益组装与输入解析，以及 `WsfESA_AntennaPattern.hpp` 和 `UtMath.cpp`。

本批没有把以下相邻机制混入三张卡：

- `ComputeFailedModulesWeights`：独立的随机失效选择算法；
- `AdjustElementLocations`：独立的矩形/三角晶格布局算法；
- `AdjustApertureElements`：初始化编排器；
- `ComputeGain`：阵元因子和阵因子的薄组装层。

这些候选保持原状态，供后续批次处理。本记录不声明 `core/wsf_mil` 或 AFSIM 全量完成。

## 2. 输入

| 输入 | SHA-256 / 状态 |
| --- | --- |
| `workspace/source-index/function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `workspace/source-index/function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `workspace/algorithm-extraction/algorithm-candidates.jsonl` | 8,138 条；`fd5da95885bef98fd426e000186ee27f09a308cfca8ef20bd4a4faeb3dd38a14` |
| AFSIM 源码 | `source_root/afsim-2_9` |
| 批次决策 | `batch-004-core-wsf-mil-esa-pattern.jsonl`，4 条；`f49ea70336a7ebcbc4eb474f368dd02da0e4c75600c9e3da18aee1cd8657f1bd` |

按仓库 `AGENTS.md` 约束，先通过 CodeGraph 读取三个主函数、共享量化函数、初始化/配置和调用路径，再以真实文件行号复核。

共享量化函数上游被标为 `control_flow`，不在原数学候选集合中。本批通过精确
`candidate_id=a81cf65a6ded7076` 纳入，候选总数由 8,137 增至 8,138；候选构建脚本保留了既有决策与产物关联。

## 3. 处理结果

| 指标 | 数量 |
| --- | ---: |
| 批次候选记录 | 4 |
| extracted | 4 |
| rejected/deferred | 0 |
| 提取的物理算法 | 3 |

候选多于算法的原因是 `ComputeQuantizationError` 同时服务 Taylor 幅度量化与阵因子相位量化。它作为两个主算法的共享依赖闭环，不单独扩成第四个算法。

## 4. 产物

- 算法卡：
  - `docs/algorithms/sensors-esa-taylor-distribution-weights-card.md`
  - `docs/algorithms/sensors-esa-weighted-array-factor-card.md`
  - `docs/algorithms/sensors-esa-aperture-efficiency-card.md`
- 对应的 3 份中性接口规格；
- `workspace/algorithm-extraction/batches/batch-004-core-wsf-mil-esa-pattern.jsonl`；
- 更新候选/覆盖账本；
- 更新 `docs/algorithms/CompendiumofAlgorithms.md`：
  - 当前候选流程验证算法由 8 项增至 11 项；
  - 加 32 项历史结果后汇编总数由 40 增至 43；
- 验证报告：
  `docs/verification/algorithm-extraction-core-wsf-mil-esa-pattern-batch-004-verify-report.md`。

## 5. 关键提取决策

### 5.1 Taylor 幅度加权

- 保留输入副瓣水平的线性功率比语义；30 dB 对应 `1000`。
- 精确记录二维元素权重先量化、X/Y 轴向量后量化的顺序，避免错误地用量化轴乘积重建元素权重。
- `n_bar` 缺少范围校验、Taylor 参数可不完整及大位数量化溢出均作为显式风险保留。

### 5.2 加权阵因子

- 按总阵元数平方归一化，不改成按权重和归一化；因此锥削和失效的效率进入阵因子。
- 保留频率不大于零时按阵元间距推导匹配波长的兼容分支。
- 基础阵列 `z=0`；对派生非平面阵列，转向与观察 Z 相位项分别使用 `cos(elevation)` 和 `sin(elevation)` 的差异标为阻塞性疑点。
- 相位量化对负值使用 C++ 向零截断，不替换为 `floor` 或最近级。

### 5.3 孔径效率

- X/Y 轴效率只使用轴权重，总效率使用已经过随机失效归零的二维权重。
- `failed_elements_ratio=1` 是合法配置，但会使总效率成为 `0/0` NaN；中性接口以 `all_zero_element_weights` 状态暴露。
- 未把随机失效选择本身并入效率卡，保持算法粒度可独立测试。

## 6. 覆盖状态

回写后全局状态：

| 状态 | 数量 |
| --- | ---: |
| extracted | 23 |
| rejected | 2 |
| pending | 8,113 |
| selected/deferred | 0 |

全局闭环率为 `25 / 8138 = 0.3072%`。本批 4/4 闭环。

## 7. 独立验证

| 算法/机制 | 输入 | Oracle |
| --- | --- | --- |
| Taylor | 5 单元、30 dB、`n_bar=3`、不量化 | `[0.3404043556738716, 0.7768161156469154, 1, 0.7768161156469154, 0.3404043556738716]` |
| Taylor 量化 | 同上、3 bit | `[0.25,0.75,1,0.75,0.25]` |
| 量化符号 | `±0.73`、3 bit、范围 1 | `±0.625`，确认向零截断 |
| 阵因子偏轴 | 两个半波长间距阵元、观察 30°、转向 0 | `0.5000000000000002` |
| 阵因子锥削 | 波束中心、权重 `[1,0.5]` | `0.5625` |
| 相位量化 | 观察/转向 30°、2 bit | `0.5000000000000002`；不量化为 1 |
| 孔径效率 | `[1,0.5]` | `0.9` |
| 全失效 | `[0,0]` | 源码 NaN；中性状态 `all_zero_element_weights` |

Oracle 使用独立 JavaScript 标量/复数和实现，不调用 AFSIM 函数。

## 8. 验证结论与未决问题

- candidates/coverage 各 8,138 条、JSONL 可解析且 ID 唯一。
- 4 条批次记录逐条回连 function index、body summary 与真实源码。
- 3 张卡具备 1–10 节，3 份接口具备 1–11 节，无占位内容。
- 累计 23 条 extracted 候选均有存在的卡片、接口、算法 ID 和 `passed` 状态。
- Compendium 三个新算法各一个主条目，传感器分类 11 项、总计 43 项。
- 两个账本脚本 `py_compile` 通过。

验收结论：通过。

仍需外部证据解决：

1. Taylor `n_bar` 的正式合法范围；
2. 二维先量化、轴后量化是否为刻意设计；
3. 非平面阵列 Z 相位公式差异；
4. 100% 阵元失效时业务上应返回零增益还是模式不可用。
