# ESA 加权相控阵阵因子算法（ESA Weighted Phased-Array Factor）

> **算法 ID**：ALG-SENSORS-ESA-WEIGHTED-ARRAY-FACTOR  
> **状态**：verified  
> **版本/日期**：1.0 / 2026-07-24  
> **领域**：传感器 / 相控阵天线  
> **AFSIM 模块**：`core/wsf_mil`  
> **覆盖候选**：`7582a7774d4872f1`、`a81cf65a6ded7076`（共享量化依赖）  
> **接口规格**：`docs/extracted-algorithms/esa-weighted-array-factor/sensors-esa-weighted-array-factor-interface-spec.md`

## 1. 算法边界

- **目的**：对带幅度权重的任意三维阵元位置求复数远场和，加入电子波束指向相位量化，返回按阵元总数归一化的线性功率阵因子。
- **入口条件**：阵元几何、幅度权重和阵列维数已在初始化阶段确定。
- **完成条件**：返回非 dB 的无量纲阵因子。
- **包含**：频率到波长转换、零/负频率的匹配间距回退、转向/观察相位、相位量化和复数和。
- **不包含**：阵元方向图、孔径直射增益、扫描损失、背瓣门禁、增益调整、权重生成和失效选择。
- **生命周期位置**：运行期 `GetGain -> ComputeGain -> ComputeArrayFactor`。

## 2. 数据契约

### 2.1 输入

| 中文名称 | 代码标识 | 符号 | 类型 | 单位 | 约束/来源 | Method |
| --- | --- | --- | --- | --- | --- | --- |
| 频率 | `aFrequency` | $f$ | `double` | Hz | `>0` 使用 $c/f$；否则进入匹配间距回退 | `WsfESA_AntennaPattern::ComputeArrayFactor#0e651783ae` |
| 电子转向方位/俯仰 | `aEBS_Az/El` | $\alpha_s,\epsilon_s$ | `double` | rad | ESA 本地角 | 同上 |
| 观察方位/俯仰 | `aAzAngle/aElAngle` | $\alpha,\epsilon$ | `double` | rad | 已包含调用者施加的 EBS 偏移 | 同上 |
| 阵元数 | `mNX,mNY` | $N_x,N_y$ | `int` | 1 | 正常初始化后 `>0` | 同上 |
| 阵元间距 | `mdX,mdY` | $d_x,d_y$ | `double` | m | 仅频率 `<=0` 回退使用 | 同上 |
| 阵元位置 | `mLocation` | $\mathbf r_i=(x_i,y_i,z_i)$ | `UtVec3d` | m | ESA 局部 XYZ | 同上 |
| 阵元权重 | `mWeight` | $w_i$ | `double` | 1 | 包含 Taylor 量化与失效归零 | 同上 |
| 相位位数 | `mPhaseNumBits` | $b_\phi$ | `int` | bit | 0 表示不量化 | 同上 |

### 2.2 输出

| 中文名称 | 代码标识 | 符号 | 类型 | 单位 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 阵因子 | return | $AF$ | `double` | 线性功率比 | 不含阵元因子和外围增益调整 |

核心函数无状态写入和外部副作用。

## 3. 数学模型

波长分支：

$$
\lambda=
\begin{cases}
c/f,&f>0\\
d_x+d_y,&f\le0,\ N_x\ne1,\ N_y\ne1\\
2d_x,&f\le0,\ N_x\ne1,\ N_y=1\\
2d_y,&f\le0,\ N_x=1,\ N_y\ne1\\
2,&f\le0,\ N_x=N_y=1
\end{cases},
\quad k=\frac{2\pi}{\lambda}
$$

对阵元 $\mathbf r_i=(x_i,y_i,z_i)$，源码的转向相位为：

$$
\psi_i^s=k[x_i\sin\alpha_s\cos\epsilon_s+
y_i\sin\epsilon_s+
z_i\cos\alpha_s\cos\epsilon_s]
$$

仅转向相位经过 $2\pi$ 范围量化：

$$
\hat\psi_i^s=Q_{b_\phi,2\pi}(\psi_i^s)
$$

观察相位为：

$$
\psi_i=k[x_i\sin\alpha\cos\epsilon+
y_i\sin\epsilon+
z_i\cos\alpha\sin\epsilon]
$$

注意源码的 Z 项在转向式使用 $\cos\epsilon_s$，在观察式使用 $\sin\epsilon$。基础布局令 $z_i=0$，因此该差异通常被隐藏；派生非平面阵列可能受影响。

$$
P_R=\sum_iw_i\cos(\psi_i-\hat\psi_i^s),\qquad
P_I=\sum_iw_i\sin(\psi_i-\hat\psi_i^s)
$$

$$
\boxed{AF=\frac{P_R^2+P_I^2}{(N_xN_y)^2}}
$$

分母使用总阵元数而不是 $\sum_iw_i$，因此幅度锥削和失效会降低波束中心阵因子；该效率不能在外围重复补偿。

## 4. 伪代码

```text
function weighted_array_factor(input):
    lambda = resolve_wavelength(input.frequency, input.Nx, input.Ny,
                                input.dx, input.dy)
    k = 2*pi / lambda
    real = 0
    imag = 0

    for element in row_major_elements:
        steering = steering_phase(element.position, ebs_az, ebs_el, k)
        steering = truncating_quantize(steering, phase_bits, 2*pi)
        look = source_compatible_look_phase(element.position, az, el, k)
        delta = look - steering
        real += element.weight * cos(delta)
        imag += element.weight * sin(delta)

    return (real*real + imag*imag) / (Nx*Ny)^2
```

## 5. 源码证据

| candidate_id | qualified_name | 模块 | 源码位置 | 证据等级 |
| --- | --- | --- | --- | --- |
| `7582a7774d4872f1` | `WsfESA_AntennaPattern::ComputeArrayFactor#0e651783ae` | `core/wsf_mil` | `afsim-2_9/swdev/src/core/wsf_mil/source/WsfESA_AntennaPattern.cpp:440-498` | source-cited |
| `a81cf65a6ded7076` | `WsfESA_AntennaPattern::ComputeQuantizationError#85239a09d9` | `core/wsf_mil` | 同文件 `518-530` | source-cited |

### 5.1 调用与语义证据

| 证据 | 位置 | 结论 |
| --- | --- | --- |
| 公共入口和单位 | `.cpp:92-120` | Hz、rad，返回线性增益倍率 |
| 增益组装 | `.cpp:123-136` | 总增益为阵元因子乘阵因子 |
| 效率去重 | `.cpp:551-569` | 阵因子已含权重效率，阵元因子除掉重复效率 |
| 位置生成 | `.cpp:280-300` | 基础矩形/三角晶格为平面 $z=0$ |
| 峰值调用 | `.cpp:190-200` | 零角度调用用于峰值增益 |

未发现覆盖这些私有函数的直接单元测试。

## 6. 依赖与可替换性

| 依赖 | 用途 | 核心必需 | 中性替代 |
| --- | --- | --- | --- |
| `ElementVec` / `UtVec3d` | 位置与权重 | no | SI 三元组数组 |
| `ESA_Data` | 间距和位数 | no | 显式输入 |
| `UtMath` | 光速和 $2\pi$ | no | 精确常量 |
| `<cmath>` | 三角函数和平方 | yes | 等价数学库 |

## 7. 边界、风险与未知

| 条件 | 源码行为 | 风险/建议 |
| --- | --- | --- |
| $f\le0$ | 从间距推导匹配波长 | 二维非等间距时用 $d_x+d_y$；这是兼容约定而非一般物理波长 |
| $N_xN_y=0$ | 分母为零 | 标准初始化阻止；中性接口必须显式校验 |
| `elements.size()!=Nx*Ny` | 固定索引读取 | 越界；中性接口必须拒绝 |
| 负转向相位量化 | 向零而非向下截断 | 引入有符号量化偏差 |
| 权重全零 | 返回 0 | 与孔径效率算法的 `0/0` 行为不同 |
| 非平面 $z\ne0$ | 转向/观察 Z 项的俯仰三角函数不同 | 疑似坐标公式不一致；兼容与修正模式需分开 |
| 极小/零回退间距 | $\lambda=0$ | 非有限相位；输入门禁必须检查 |

## 8. 验证计划与结果

统一使用 $\lambda=0.1$ m、$f=2\,997\,924\,580$ Hz、位置 $x=\pm0.025$ m、$y=z=0$：

| 类型 | 输入 | Oracle | 判据 |
| --- | --- | --- | --- |
| 波束中心 | 权重 `[1,1]`，观察/转向均 0 | $AF=1$ | 绝对误差 $\le10^{-15}$ |
| 偏轴 | 观察 30°、转向 0、权重 `[1,1]` | $AF=0.5000000000000002$ | 绝对误差 $\le10^{-14}$ |
| 幅度锥削 | 波束中心、权重 `[1,0.5]` | $AF=0.5625$ | 精确 |
| 转向匹配 | 观察/转向均 30°、不量化 | $AF=1$ | 绝对误差 $\le10^{-15}$ |
| 相位量化 | 同上、2 bit | $AF=0.5000000000000002$ | 绝对误差 $\le10^{-14}$ |
| 异常 | 数量不匹配、零间距回退、NaN | 中性接口拒绝 | 不计算 |

数值 Oracle 使用独立 JavaScript 复数和实现，不调用 AFSIM 函数。

## 9. 可移植性

- **等级**：高（平面阵列）/ 中（非平面阵列和调用语义）。
- 复数阵列求和本身高度可移植；必须保留“按总阵元数归一化”和向零相位量化。
- 建议接口显式区分 `source_compatible` 与 `geometric_consistent` Z 相位策略，默认兼容模式。
- 重实现前需审查 AFSIM 随附许可证。

## 10. 覆盖账本回写

| candidate_id | 状态 | algorithm_id | 决策理由 | 验证 |
| --- | --- | --- | --- | --- |
| `7582a7774d4872f1` | extracted | ALG-SENSORS-ESA-WEIGHTED-ARRAY-FACTOR | 独立、可测试的相控阵复数和与归一化算法 | passed |
| `a81cf65a6ded7076` | extracted | 本算法；ALG-SENSORS-ESA-TAYLOR-DISTRIBUTION-WEIGHTS | 共享量化依赖 | passed |
