# LADAR 普朗克谱辐射出射度（LADAR Planck Spectral Radiant Emittance）

> **算法 ID**：ALG-SENSORS-LADAR-PLANCK-SPECTRAL-RADIANT-EMITTANCE  
> **状态**：verified  
> **版本/日期**：1.0 / 2026-07-27  
> **领域**：传感器 / 激光雷达  
> **AFSIM 模块**：`core/wsf_mil`  
> **覆盖候选**：`8489be3451662000`  
> **接口规格**：`docs/extracted-algorithms/ladar-planck-spectral-radiant-emittance/sensors-ladar-planck-spectral-radiant-emittance-interface-spec.md`

## 1. 算法边界

- **目的**：按源码采用的普朗克黑体公式，计算给定温度和波长的谱辐射出射度。
- **入口条件**：温度与波长为正的有限标量；源码未自行校验。
- **完成条件**：返回每波长单位的双精度辐射出射度。
- **包含**：常数 `cC1/cC2`、五次波长幂和 `expm1` 数值稳定分母。
- **不包含**：背景辐照度状态写入、接收机光谱响应、波段积分和大气传输。
- **生命周期位置**：`initialize` 时由 `ComputeBackgroundRadiance` 调用，也可作为无状态工具函数。

## 2. 流程

```mermaid
flowchart LR
    A["温度 T、波长 λ(µm)"] --> B["λ⁵ = λ·λ²·λ²"]
    B --> C["x = c₂/(λT)"]
    C --> D["Mλ = c₁/(λ⁵·expm1(x))"]
    D --> E["谱辐射出射度"]
```

`expm1(x)` 保留源码实现；它避免在 $x$ 很小时由 `exp(x)-1` 引起的有效位损失。

## 3. 数据契约

### 3.1 输入

| 名称 | 代码标识 | 符号 | 类型 | 单位 | Method |
| --- | --- | --- | --- | --- | --- |
| 黑体温度 | `aTemperature` | $T$ | `double` | K（注释写 deg-K） | `WsfLADAR_Sensor::SpectralRadiantEmittance#e62bac53c9` |
| 波长 | `aWavelength` | $\lambda$ | `double` | µm | 同上 |

### 3.2 输出

| 名称 | 代码标识 | 符号 | 类型 | 单位 | Method |
| --- | --- | --- | --- | --- | --- |
| 谱辐射出射度 | `return` | $M_\lambda$ | `double` | W/(cm²·µm)，按源码注释 | 同上 |

### 3.3 参数与常量

| 名称 | 代码标识 | 符号 | 值 | 单位/来源 |
| --- | --- | --- | --- | --- |
| 第一辐射常数 | `cC1` | $c_1$ | `3.74177153E+4` | W/cm²，源码注释 NIST-2010 CODATA |
| 第二辐射常数 | `cC2` | $c_2$ | `1.4387770E+4` | µm·K，源码注释 NIST-2010 CODATA |

### 3.4 内部状态

无持久状态；局部量 `lambda_2`、`t1`、`t2` 只服务本次计算。

## 4. 数学模型

源码直接实现：

$$M_\lambda=\frac{c_1}{\lambda^5\,[\exp(c_2/(\lambda T))-1]}$$

其中 $\lambda^5$ 由 `lambda * lambda_2 * lambda_2` 得到，分母以 `expm1` 计算。这是离散无状态闭式实现，不包含积分或近似截断。

## 5. 伪代码

```text
function planck_spectral_emittance(temperature_k, wavelength_um):
    # 中文：中性接口拒绝非正或非有限输入；原函数未显式保护。
    validate_positive_finite(temperature_k, wavelength_um)
    lambda2 = wavelength_um * wavelength_um
    numerator = c1 / (wavelength_um * lambda2 * lambda2)
    # 中文：保持源码的 expm1，改善小指数时的数值精度。
    return numerator / expm1(c2 / (wavelength_um * temperature_k))
```

## 6. 源码证据

### 6.1 入口和调用链

```text
WsfLADAR_Sensor::LADAR_Mode::Initialize  // 初始化背景模型
  -> WsfLADAR_Sensor::ComputeBackgroundRadiance#5c2a42d009
  -> WsfLADAR_Sensor::SpectralRadiantEmittance#e62bac53c9
```

### 6.2 源码位置

| candidate_id | qualified_name | 模块 | 源码位置 | 角色 | 证据等级 |
| --- | --- | --- | --- | --- | --- |
| `8489be3451662000` | `WsfLADAR_Sensor::SpectralRadiantEmittance#e62bac53c9` | `core/wsf_mil` | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfLADAR_Sensor.cpp:205-232` | 核心 | source-cited |

### 6.3 框架与依赖

| 依赖 | 分类 | 用途 | 中性替代 |
| --- | --- | --- | --- |
| `<cmath>::expm1` | 标准库 | 指数差 | 等价数学库 |

## 7. 边界、风险与未知

| 条件 | 源码行为 | 影响 | 建议 |
| --- | --- | --- | --- |
| $T\le0$ 或 $\lambda\le0$ | 无检查 | 除零、溢出或非有限输出 | 中性接口拒绝 |
| $c_2/(\lambda T)$ 很大 | `expm1` 仍可能溢出 | 返回趋近 0 或非有限中间值 | 将极限 $M_\lambda\to0$ 单测化 |

- **已确认假设**：输入波长是 µm，而不是 m。
- **待人工复核**：源码注释的面积单位与下游背景量的面积换算未在此函数中处理。

## 8. 验证计划

| 类型 | 输入 | Oracle | 容差/不变量 |
| --- | --- | --- | --- |
| 正常 | $T=300$ K，$\lambda=10$ µm | `0.003117725468277123` | `1e-15` |
| 边界 | $T=300$ K，$\lambda=1$ µm | 有限且远小于 10 µm 值 | 单调比较 |
| 退化 | $T=0$ 或 $\lambda=0$ | 中性接口 `invalid_input` | 不调用公式 |

## 9. 可移植性

- **等级**：高。
- **可移植核心**：两常数和闭式普朗克公式。
- **AFSIM 耦合**：仅调用点及下游单位约定。
- **类型/单位适配**：必须显式指定 µm、K 和输出面积单位。
- **许可证/clean-room 注意**：以本卡公式和契约独立重实现。

## 10. 覆盖账本回写

| candidate_id | 状态 | algorithm_id | 决策理由 | 验证 |
| --- | --- | --- | --- | --- |
| `8489be3451662000` | extracted | ALG-SENSORS-LADAR-PLANCK-SPECTRAL-RADIANT-EMITTANCE | 独立、无状态的黑体谱辐射闭式计算 | passed |
