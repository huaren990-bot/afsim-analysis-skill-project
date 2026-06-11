# 算法卡片 — 拉格朗日点计算

> **状态**：draft
> **日期**：2026-06-11
> **索引证据**：function-index.jsonl (ComputeGamma 为 math 标记)
> **关联文档**：space-integrating-propagator-card.md

### 基础资料

- **算法名称**：Libration Point Computation — Circular Restricted Three-Body Problem（拉格朗日点计算 — 圆型限制性三体问题）
- **算法所属模块**：wsf_space（空间/轨道力学模块）
- **算法功能**：计算地-月系或日-地系的 5 个拉格朗日点（L1-L5）位置，以及相关的平动点轨道特性。用于分析平动点任务（如 James Webb 望远镜所在的日-地 L2 点）。

### 算法变量和常量

#### 输入变量

| 变量名 | 类型 | 中文说明 | 所属函数 (Method) |
|--------|------|----------|-------------------|
| `mu` | double | 三体系统质量比 μ = m₂/(m₁+m₂) | ComputeGamma |
| `r1` | UtVector3 | 主天体 m₁ 位置矢量 (m) | ComputeGamma |
| `r2` | UtVector3 | 次天体 m₂ 位置矢量 (m) | ComputeGamma |
| `R` | double | 两天体间距离 (m) | ComputeGamma |
| `x1` | double | 主天体质心坐标 x 分量 (m) | ComputeGamma |
| `x2` | double | 次天体质心坐标 x 分量 (m) | ComputeGamma |

#### 输出变量

| 变量名 | 类型 | 中文说明 | 所属函数 (Method) |
|--------|------|----------|-------------------|
| `gamma1` | double | L1 点距离修正因子 | ComputeGamma |
| `gamma2` | double | L2 点距离修正因子 | ComputeGamma |
| `gamma3` | double | L3 点距离修正因子 | ComputeGamma |
| `L1_position` | UtVector3 | L1 拉格朗日点位置 (m) | ComputeGamma |
| `L2_position` | UtVector3 | L2 拉格朗日点位置 (m) | ComputeGamma |
| `L3_position` | UtVector3 | L3 拉格朗日点位置 (m) | ComputeGamma |
| `L4_position` | UtVector3 | L4 拉格朗日点位置 (m) | ComputeGamma |
| `L5_position` | UtVector3 | L5 拉格朗日点位置 (m) | ComputeGamma |

#### 常量

| 常量名 | 类型 | 值 | 中文说明 | 所属函数 (Method) |
|--------|------|-----|----------|-------------------|
| — | — | — | 无特定常量，所有参数由输入变量提供 | — |

### 关键数学公式

1. **限制性三体问题质量比**：

   $\mu = \frac{m_2}{m_1 + m_2}$

   其中 $m_1$ 为主天体（如地球），$m_2$ 为次天体（如月球）。

2. **Gamma 系数 (ComputeGamma)**：用于计算共线拉格朗日点 L1、L2、L3 的距离修正因子：

   对 L1 点：$\gamma_1^5 - (3 - \mu)\gamma_1^4 + (3 - 2\mu)\gamma_1^3 - \mu\gamma_1^2 + 2\mu\gamma_1 - \mu = 0$

   对 L2 点：$\gamma_2^5 + (3 - \mu)\gamma_2^4 + (3 - 2\mu)\gamma_2^3 - \mu\gamma_2^2 - 2\mu\gamma_2 - \mu = 0$

   对 L3 点：$\gamma_3^5 - \mu\gamma_3^4 + (3 - 2\mu)\gamma_3^3 - (3 - \mu)\gamma_3^2 - 2\mu\gamma_3 - \mu = 0$

   使用 Newton 迭代法求解上述五次方程。

3. **共线拉格朗日点位置**（L1、L2、L3）：

   $x_{L1} = x_2 - \gamma_1 \cdot R$ （$m_1$ 和 $m_2$ 之间）

   $x_{L2} = x_2 + \gamma_2 \cdot R$ （$m_2$ 外侧）

   $x_{L3} = -x_1 - \gamma_3 \cdot R$ （$m_1$ 远处外侧）

   其中 $R$ 为两天体间距，$x_1, x_2$ 为两天体质心坐标。

4. **三角拉格朗日点位置**（L4、L5）：

   $x_{L4,L5} = \frac{x_1 + x_2}{2} = R \cdot \left(\frac{1}{2} - \mu\right)$

   $y_{L4} = +\frac{\sqrt{3}}{2} \cdot R$ （L4，领先 $m_2$ 60°）

   $y_{L5} = -\frac{\sqrt{3}}{2} \cdot R$ （L5，落后 $m_2$ 60°）

5. **平动点轨道（Halo/Lissajous）**：L1/L2 附近的线性化运动方程：

   $\ddot{x} - 2n\dot{y} - (n^2 + 2c_2)x = 0$

   $\ddot{y} + 2n\dot{x} + (c_2 - n^2)y = 0$

   $\ddot{z} + c_2 z = 0$

   其中 $n$ 为系统平运动，$c_2 = \frac{\mu}{|x_e - 1 + \mu|^3} + \frac{1-\mu}{|x_e + \mu|^3}$。

### 源码位置

| File | Symbol | 中文说明 |
|------|--------|----------|
| [WsfLibrationPoint.hpp](source_root/src/core/wsf_space/source/WsfLibrationPoint.hpp) | `WsfLibrationPoint` | 平动点类声明 |
| [WsfLibrationPoint.cpp](source_root/src/core/wsf_space/source/WsfLibrationPoint.cpp) | `ComputeGamma()` | Gamma 系数计算 — 五次方程 Newton 求解 |
| 同上 | — | L1-L5 位置计算 |

### 可移植性评分

**可移植性**：高 — 限制性三体问题公式为标准天体力学内容，Gamma 系数 Newton 迭代为通用数值方法，可直接用公式重实现。
