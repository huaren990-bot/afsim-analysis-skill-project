# `core/wsf_mil` ESA 相控阵第四批算法提取验证报告

> 日期：2026-07-24  
> 批次：`batch-004-core-wsf-mil-esa-pattern`  
> 结论：**通过**

## 1. 范围与输入

本报告只验收第四批 4 条候选记录对应的 3 个算法：

1. `ALG-SENSORS-ESA-TAYLOR-DISTRIBUTION-WEIGHTS`
2. `ALG-SENSORS-ESA-WEIGHTED-ARRAY-FACTOR`
3. `ALG-SENSORS-ESA-APERTURE-EFFICIENCY`

第四条候选 `a81cf65a6ded7076` 是前两个算法共用的向零截断量化依赖。

验证输入：

| 文件 | 行数 | SHA-256 |
| --- | ---: | --- |
| `workspace/source-index/function-index.jsonl` | 55,031 | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `workspace/source-index/function-body-summary.jsonl` | 49,561 | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `workspace/algorithm-extraction/algorithm-candidates.jsonl` | 8,138 | `fd5da95885bef98fd426e000186ee27f09a308cfca8ef20bd4a4faeb3dd38a14` |
| `workspace/algorithm-extraction/algorithm-coverage.jsonl` | 8,138 | `ab2f37cc6f5c752ca55c66730b66bd07324f913b1b6d41d984b6e3dfc0ddeed7` |
| `workspace/algorithm-extraction/batches/batch-004-core-wsf-mil-esa-pattern.jsonl` | 4 | `f49ea70336a7ebcbc4eb474f368dd02da0e4c75600c9e3da18aee1cd8657f1bd` |

真实源码根为 `source_root/afsim-2_9`。核心文件为
`afsim-2_9/swdev/src/core/wsf_mil/source/WsfESA_AntennaPattern.cpp`，
并补查同目录头文件和 `tools/util/source/UtMath.cpp`。

## 2. 候选状态与覆盖率

全局分母为 8,138 条候选：

| 状态 | 数量 |
| --- | ---: |
| extracted | 23 |
| rejected | 2 |
| deferred | 0 |
| selected | 0 |
| pending | 8,113 |

全局闭环率为 `25 / 8138 = 0.3072%`，不构成模块或 AFSIM 全量完成声明。

本批分母为 4 条候选：

| 算法/依赖 | 候选记录 | extracted | 说明 |
| --- | ---: | ---: | --- |
| Taylor 幅度加权 | 1 | 1 | 主函数 |
| 加权阵因子 | 1 | 1 | 主函数 |
| 孔径效率 | 1 | 1 | 主函数 |
| 向零量化 | 1 | 1 | Taylor 与阵因子共享，不单列算法 |
| 合计 | 4 | 4 | 3 个算法 |

本批闭环率 100%，没有 `pending`、`selected`、`rejected` 或 `deferred`。

## 3. 检查结果

| 检查项 | 结果 | 可复现证据 |
| --- | --- | --- |
| JSONL 解析与唯一性 | 通过 | candidates/coverage 各 8,138 条唯一 ID；batch-004 为 4 条唯一 ID |
| 全量账本一致性 | 通过 | candidates 与 coverage 的 ID 集合完全相同 |
| 批次状态闭环 | 通过 | 4 条均为 `extracted` 且 verification=`passed` |
| function/body 连接 | 通过 | 4 条均按 `candidate_id + qualified_name + path + line range` 精确匹配 |
| 真实源码位置 | 通过 | 源码文件存在，4 条行号均未越界 |
| 算法粒度 | 通过 | 三个主算法独立；随机失效、几何布局和增益组装未混入 |
| 共享依赖处理 | 通过 | 量化候选关联两个算法 ID，未虚增算法数 |
| 卡片完整性 | 通过 | 3 张卡均具备连续 1–10 节，无占位标记 |
| 接口完整性 | 通过 | 3 份规格均具备连续 1–11 节，并声明不代表已有实现 |
| 公式与变量 | 通过 | Taylor、相位、复数和、归一化与效率符号均映射到代码变量 |
| 单位与坐标 | 通过 | 频率 Hz、位置/间距 m、角 rad、线性功率比与幅度权重已区分 |
| 生命周期 | 通过 | 初始化顺序与运行期增益调用链均有源码证据 |
| 全量 extracted 产物 | 通过 | 23 条 extracted 候选均有算法 ID、存在的卡片/接口和 `passed` 状态 |
| rejected/deferred 理由 | 通过 | 2 条 rejected 均有具体理由；无 deferred |
| Compendium | 通过 | 三个新算法主条目各 1 次；传感器分类 11 项，总计 43 项 |
| Python 脚本语法 | 通过 | 两个算法账本脚本 `py_compile` 成功 |

当前源码索引和仓库中未发现三个私有主函数的直接覆盖测试，因此数值行为由独立 Oracle 复验。

## 4. 数值与边界复验

| 算法 | 独立输入 | 结果 | 判据 |
| --- | --- | --- | --- |
| Taylor | $N=5,S=1000,\bar n=3,b=0$ | `[0.3404043556738716,0.7768161156469154,1,0.7768161156469154,0.3404043556738716]` | 每项误差 `<=1e-12` |
| Taylor 量化 | 同上，3 bit | `[0.25,0.75,1,0.75,0.25]` | 精确 |
| 二维量化顺序 | X/Y 均为上述 Taylor，3 bit，角阵元 | 兼容元素权重 0；量化轴乘积 0.0625 | 精确证明不可交换 |
| 有符号量化 | `±0.73`、3 bit、范围 1 | `±0.625` | 精确 |
| 阵因子波束中心 | $\lambda=0.1$ m、$x=\pm0.025$ m、权重 `[1,1]` | 1 | 误差 `<=1e-15` |
| 阵因子偏轴 | 同上，观察 30°、转向 0 | `0.5000000000000002` | 误差 `<=1e-14` |
| 阵因子锥削 | 波束中心、权重 `[1,0.5]` | 0.5625 | 精确 |
| 相位量化 | 观察/转向 30°，2 bit | `0.5000000000000002`；不量化为 1 | 误差 `<=1e-14` |
| 孔径效率 | `[1,0.5]` | 0.9 | 误差 `<=1e-15` |
| Taylor 效率 | 未量化 5 项 Taylor 权重 | `0.8579882159275146` | 误差 `<=1e-12` |
| 全失效 | `[0,0]` | 源码 `0/0` 为 NaN；安全状态 `all_zero_element_weights` | 精确分支 |

数值 Oracle 使用独立 JavaScript 标量与复数和实现，不调用 AFSIM 函数。

## 5. 缺陷清单

本批文档、账本、链接和统计未发现阻断、严重、一般或轻微缺陷。

以下为准确保留的上游模型风险，不属于本批产物缺陷：

1. Taylor `n_bar` 没有输入范围门禁，参数块也不强制提供完整副瓣水平。
2. 幅度/相位量化位数没有上限，`pow(2,bits)` 转 `int` 可能溢出。
3. 二维元素权重先量化，轴向量后量化，导致两套离散权重不完全一致。
4. 相位量化对负值向零截断，存在有符号偏差。
5. 非平面阵列的转向与观察 Z 相位使用不同俯仰三角函数。
6. `failed_elements_ratio=1` 可使总孔径效率为 NaN，并污染后续除法与增益。
7. 轴效率不含随机失效信息，部分失效对波束宽度的影响不会由这两项体现。

这些风险会阻塞不加适配的直接迁移，但不阻塞“源码行为、边界和未知已准确提取”的验收。

## 6. 结论

第四批 4 条候选已全部闭环为 3 个独立算法及 1 个共享依赖。算法卡、接口规格、覆盖账本、真实源码、索引、Compendium 和独立数值验证一致，批次验收通过。全局仍有 8,113 条候选待处理。
