# ESA 幅度权重孔径效率算法（ESA Amplitude-Weight Aperture Efficiency）

> **算法 ID**：ALG-SENSORS-ESA-APERTURE-EFFICIENCY  
> **状态**：verified  
> **版本/日期**：1.0 / 2026-07-24  
> **领域**：传感器 / 相控阵天线  
> **AFSIM 模块**：`core/wsf_mil`  
> **覆盖候选**：`848fed793112bbd6`  
> **接口规格**：`docs/extracted-algorithms/esa-aperture-efficiency/sensors-esa-aperture-efficiency-interface-spec.md`

## 1. 算法边界

- **目的**：由 X/Y 轴权重和最终二维阵元权重分别计算归一化孔径效率。
- **入口条件**：Taylor/均匀权重已生成，随机失效阵元已归零。
- **完成条件**：写入 X、Y 和总孔径效率并返回总效率。
- **包含**：绝对幅度和、平方和及阵元数归一化。
- **不包含**：权重生成、量化、随机失效选择、直射增益和阵因子。
- **生命周期位置**：初始化阶段 `AdjustApertureElements` 的最后一步；结果供波束宽度和增益组装使用。

## 2. 数据契约

### 2.1 输入

| 中文名称 | 代码标识 | 符号 | 类型 | 单位 | 约束/来源 | Method |
| --- | --- | --- | --- | --- | --- | --- |
| 阵元数 | `mNX,mNY` | $N_x,N_y$ | `int` | 1 | 正常初始化 `>0` | `WsfESA_AntennaPattern::ComputeApertureEfficiency#5c73ecce1d` |
| X/Y 轴权重 | `mWeightVecX/Y` | $w_{x,n},w_{y,m}$ | `vector<double>` | 1 | Taylor 量化后或均匀全 1 | 同上 |
| 最终阵元权重 | `mElements[].mWeight` | $w_{ij}$ | `double` | 1 | 已包含分布、幅度量化和失效归零 | 同上 |

### 2.2 输出

| 中文名称 | 代码标识 | 符号 | 类型 | 单位 | 说明 |
| --- | --- | --- | --- | --- | --- |
| X 轴效率 | `mApertureEffX` | $\eta_x$ | `double` | 1 | 用于方位波束宽度 |
| Y 轴效率 | `mApertureEffY` | $\eta_y$ | `double` | 1 | 用于俯仰波束宽度 |
| 总效率 | `mApertureEff` / return | $\eta$ | `double` | 1 | 用于直射增益和效率去重 |

函数写入三个对象成员；无随机性。X/Y 轴向量不会被随机失效逻辑归零，因此 $\eta_x,\eta_y$ 只反映分布/量化，总效率 $\eta$ 还反映失效。

## 3. 数学模型

对任一长度为 $N$ 的非零权重向量 $\mathbf w$：

$$
\eta(\mathbf w)=
\frac{\left(\sum_{i=1}^{N}|w_i|\right)^2}
{N\sum_{i=1}^{N}w_i^2}
$$

源码以 `sqrt(w*w)` 实现绝对值。三项输出为：

$$
\eta_x=\eta(\mathbf w_x),\qquad
\eta_y=\eta(\mathbf w_y)
$$

$$
\boxed{
\eta=
\frac{\left(\sum_{j=0}^{N_y-1}\sum_{i=0}^{N_x-1}|w_{ij}|\right)^2}
{N_xN_y\sum_{j=0}^{N_y-1}\sum_{i=0}^{N_x-1}w_{ij}^2}
}
$$

若向量非零，由 Cauchy–Schwarz 不等式可知 $1/N\le\eta\le1$。全零向量的分子、分母同时为零，源码产生 NaN。

## 4. 伪代码

```text
function efficiency(weights):
    amplitude_sum = sum(sqrt(w*w) for w in weights)
    square_sum = sum(w*w for w in weights)
    return amplitude_sum^2 / (len(weights) * square_sum)

function esa_aperture_efficiency(Nx, Ny, wx, wy, elements):
    eta_x = efficiency(wx)
    eta_y = efficiency(wy)
    eta_total = efficiency(elements)
    store eta_x, eta_y, eta_total
    return eta_total
```

## 5. 源码证据

| candidate_id | qualified_name | 模块 | 源码位置 | 证据等级 |
| --- | --- | --- | --- | --- |
| `848fed793112bbd6` | `WsfESA_AntennaPattern::ComputeApertureEfficiency#5c73ecce1d` | `core/wsf_mil` | `afsim-2_9/swdev/src/core/wsf_mil/source/WsfESA_AntennaPattern.cpp:609-649` | source-cited |

### 5.1 调用与语义证据

| 证据 | 位置 | 结论 |
| --- | --- | --- |
| 初始化顺序 | `.cpp:255-277` | 先分布、再失效、最后效率 |
| 失效归零 | `.cpp:501-515` | 只修改二维 `mElements` 权重 |
| 直射增益 | `.cpp:575-606` | 总效率乘入 directivity |
| 效率去重 | `.cpp:551-569` | 与阵因子组合时再除去一次，避免双计 |
| 允许全失效配置 | `.cpp:749-753` | `failed_elements_ratio` 闭区间包含 1 |
| 初始效率 | `.cpp:30-45` | 三项初值均为 1 |

未发现覆盖该私有函数的直接单元测试。

## 6. 依赖与可替换性

| 依赖 | 用途 | 核心必需 | 中性替代 |
| --- | --- | --- | --- |
| `ElementVec` | 二维权重 | no | 连续标量数组 |
| 对象成员 | 缓存三项效率 | no | 纯函数返回结构 |
| `<cmath>` | `sqrt`、平方 | no | `abs` 与乘法 |

## 7. 边界、风险与未知

| 条件 | 源码行为 | 风险/建议 |
| --- | --- | --- |
| 均匀非零权重 | 效率 1 | 正常上界 |
| 仅一个非零权重 | 效率 $1/N$ | 正常下界 |
| 全部权重为 0 | `0/0 -> NaN` | 配置允许 100% 失效；中性接口应返回明确状态 |
| `N<=0` 或长度不匹配 | 除零或越界 | 正常初始化阻止；接口必须校验 |
| 负权重 | 按绝对幅度计分子 | 公式仍有限，但正常 Taylor 链不应生成负最终幅度 |
| 部分失效 | 只影响总效率，不影响 $\eta_x,\eta_y$ | 波束宽度不反映随机失效方向分布 |
| 总效率 NaN/0 | 下游 `ComputeElementFactor` 用它作除数 | 可能污染最终增益 |

## 8. 验证计划与结果

| 类型 | 输入权重 | Oracle | 判据 |
| --- | --- | --- | --- |
| 均匀 | `[1,1,1,1]` | $\eta=1$ | 精确 |
| 锥削 | `[1,0.5]` | $\eta=0.9$ | 精确 |
| 半失效 | `[1,0,1,0]` | $\eta=0.5$ | 精确 |
| Taylor | 5 单元、30 dB、$\bar n=3$ 的未量化权重 | $\eta=0.8579882159275146$ | 绝对误差 $\le10^{-12}$ |
| Taylor 3 bit | `[0.25,0.75,1,0.75,0.25]` | $\eta=0.8$ | 精确 |
| 全失效 | `[0,0]` | 源码为 NaN；安全接口状态 `all_zero_weights` | 精确分支 |

数值 Oracle 使用独立 JavaScript 标量实现，不调用 AFSIM 函数。

## 9. 可移植性

- **等级**：极高。
- 公式是无状态的归一化标量归约；迁移重点是全零状态以及轴效率不含随机失效的调用语义。
- 建议使用缩放求和或更高精度累加，降低极大/极小权重的平方溢出与下溢。
- 重实现前需审查 AFSIM 随附许可证。

## 10. 覆盖账本回写

| candidate_id | 状态 | algorithm_id | 决策理由 | 验证 |
| --- | --- | --- | --- | --- |
| `848fed793112bbd6` | extracted | ALG-SENSORS-ESA-APERTURE-EFFICIENCY | 独立、可测试的幅度权重孔径效率公式 | passed |
