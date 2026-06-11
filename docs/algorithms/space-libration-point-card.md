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

### 内部状态

下表列出 `LibrationPoint` 类中跨帧持久化的成员变量。该类在构造时一次性计算 Gamma 系数（`mGamma1`、`mGamma2`、`mGamma3`），这些系数在整个生命周期内不变。`mutable` 标记的变量在每次查询不同历元时更新，用于缓存旋转参考系变换。

| 变量名 | 类型 | 初始值 | 物理含义 | 更新时机 |
|--------|------|--------|----------|----------|
| `mSystem` | System (enum) | 由构造函数参数决定 | 三体系统类型：`cSUN_EARTH`（日-地）、`cEARTH_MOON`（地-月）、`cSUN_JUPITER`（日-木）、`cUNKNOWN` | 构造时一次设定，不可更改 |
| `mPrimaryBody` | `ut::CloneablePtr<ut::CentralBody>` | 由 `GetPrimaryBody(mSystem)` 创建 | 主天体（如日-地系中的太阳、地-月系中的地球） | 构造时一次创建 |
| `mSecondaryBody` | `ut::CloneablePtr<ut::CentralBody>` | 由 `GetSecondaryBody(mSystem)` 创建 | 次天体（如日-地系中的地球、地-月系中的月球） | 构造时一次创建 |
| `mMuStar` | double | $\mu^* = \mu_2 / (\mu_1 + \mu_2)$ | 归一化质量比（无量纲），其中 $\mu_1$、$\mu_2$ 为两天体的引力参数 (m^3/s^2) | 构造时由两天体引力参数计算一次 |
| `mGamma1` | double | 由 Newton-Raphson 求解 | L1 点无量纲距离修正因子 $\gamma_1$，L1 距次天体 $\gamma_1 R$ | 构造时由 `ComputeGamma()` 一次性计算 |
| `mGamma2` | double | 由 Newton-Raphson 求解 | L2 点无量纲距离修正因子 $\gamma_2$，L2 距次天体 $\gamma_2 R$ | 构造时由 `ComputeGamma()` 一次性计算 |
| `mGamma3` | double | 由 Newton-Raphson 求解 | L3 点无量纲距离修正因子 $\gamma_3$，L3 距质心 $\gamma_3 R$ | 构造时由 `ComputeGamma()` 一次性计算 |
| `mPosDiff` | mutable UtVec3d | — | 次天体相对于主天体的位置矢量 $\mathbf{r}_s - \mathbf{r}_p$ (m) | 每次调用 `UpdateTransform()` 时若历元变更则更新 |
| `mVelDiff` | mutable UtVec3d | — | 次天体相对于主天体的速度矢量 $\mathbf{v}_s - \mathbf{v}_p$ (m/s) | 每次调用 `UpdateTransform()` 时若历元变更则更新 |
| `mPosOriginECI` | mutable UtVec3d | — | 旋转参考系原点（主天体）在 ECI 中的位置 (m) | 每次调用 `UpdateTransform()` 时若历元变更则更新 |
| `mVelOriginECI` | mutable UtVec3d | — | 旋转参考系原点（主天体）在 ECI 中的速度 (m/s) | 每次调用 `UpdateTransform()` 时若历元变更则更新 |
| `mTransform` | mutable UtMat3d | — | ECI → 旋转系 (RF) 的 3×3 旋转矩阵，列向量为旋转系基向量在 ECI 中的分量 | 每次调用 `UpdateTransform()` 时若历元变更则重新构建 |
| `mTransformDot` | mutable UtMat3d | — | 旋转矩阵的时间导数 $\dot{\mathbf{T}}$，用于将旋转系速度转换到 ECI | 每次调用 `UpdateTransform()` 时若历元变更则重新计算（z 轴导数假设为 0） |
| `mCurrentEpoch` | mutable UtCalendar | — | 最后一次变换计算的历元，用于缓存判断 | `UpdateTransform()` 时若输入历元不同于此值则重新计算所有 mutable 变量 |

### 变量映射表

| 代码变量 | 数学符号 | 含义 |
|----------|----------|------|
| `mMuStar` | $\mu^*$ | 归一化质量比 $\mu^* = \mu_2 / (\mu_1 + \mu_2) = m_2 / (m_1 + m_2)$（无量纲） |
| `mGamma1` | $\gamma_1$ | L1 点无量纲距离修正因子 |
| `mGamma2` | $\gamma_2$ | L2 点无量纲距离修正因子 |
| `mGamma3` | $\gamma_3$ | L3 点无量纲距离修正因子 |
| `mPosDiff` | $\mathbf{r}_s - \mathbf{r}_p$ | 次天体相对主天体的位置矢量 (m) |
| `mVelDiff` | $\mathbf{v}_s - \mathbf{v}_p$ | 次天体相对主天体的速度矢量 (m/s) |
| `rsMag` | $R = \|\mathbf{r}_s - \mathbf{r}_p\|$ | 两天体间距离 (m) |
| `xHat` / `yHat` / `zHat` | $\hat{\mathbf{x}}, \hat{\mathbf{y}}, \hat{\mathbf{z}}$ | 旋转参考系的正交基向量：$\hat{\mathbf{x}}$ 从主指向次天体，$\hat{\mathbf{z}}$ 沿轨道角动量方向，$\hat{\mathbf{y}}$ 完成右手系 |
| `mTransform` | $\mathbf{T}$ | ECI → RF 旋转矩阵 |
| `mTransformDot` | $\dot{\mathbf{T}}$ | 旋转矩阵的时间导数 |
| `mPosOriginECI` | $\mathbf{r}_p$ | 主天体 ECI 位置 (m) |
| `mVelOriginECI` | $\mathbf{v}_p$ | 主天体 ECI 速度 (m/s) |
| `guess` | $\gamma_0$ | Newton 迭代初始猜测 $\gamma_0 = (\mu^* / [3(1-\mu^*)])^{1/3}$ |
| `cTOLERANCE` (1.0e-14) | $\epsilon$ | Newton 迭代收敛容差 |

### 边界条件

下表列出模型中影响数值稳定性、输入合法性、限幅和回退行为的关键边界条件。

| 条件 | 所在位置 | 处理方式 | 说明 |
|------|----------|----------|------|
| 无效系统枚举 | `GetSystemFromIdentifier()` | 不识别字符串时返回 `System::cUNKNOWN` | 调用方需检查返回值 |
| 无效点枚举 | `GetPointFromIdentifier()` | 不识别字符串时返回 `Point::cUNKNOWN` | 调用方需检查返回值 |
| `cUNKNOWN` 系统查询 | `GetPointLocation()` / `GetPrimaryBody()` / `GetSecondaryBody()` | 抛出 `std::runtime_error("Unknown Libration point selection.")` 或 `"Unknown Libration point system."` | 异常回退，提示错误原因 |
| `cUNKNOWN` 系统周期查询 | `GetSystemPeriod()` | 返回 31536000.0 s（约一年），等同于 `cSUN_EARTH` 的 fall-through 默认值 | 安全默认值，不会崩溃 |
| Newton 迭代收敛容差 | `ComputeGamma()` | 容差 `cTOLERANCE = 1.0e-14` | 高精度要求，由 `UtNewtonRaphson1D` 内部循环控制收敛 |
| Newton 迭代初始猜测 | `ComputeGamma()` | L1/L2 的初始猜测为 $\gamma_0 = (\mu^* / [3(1-\mu^*)])^{1/3}$；L3 的初始猜测为 1.0 | 基于 CRTBP 理论分析的近似解作为迭代起点，确保快速收敛 |
| 历元缓存检查 | `UpdateTransform()` | 若 `aEpoch == mCurrentEpoch`，直接返回不重算变换矩阵 | 避免对同一历元重复计算天体星历 |
| z 轴时间导数假设 | `UpdateTransform()` | `zHatDot = {0, 0, 0}`，假设次天体加速度垂直于位置矢量（即 $\mathbf{r}_s \times \mathbf{a}_s = 0$） | 该简化假设适用于近圆轨道，对于椭圆轨道可能引入微小误差 |
| 无效点有效校验 | `ValidLibrationPoint()` | 同时检查 `systemCheck && pointCheck`，任一无效返回 false | 调用方在查询位置/速度前应使用此函数校验 |

### 提取策略

该算法的信息从以下源文件按以下方式提取：

| 源文件 | 提取方式 | 提取内容 |
|--------|----------|----------|
| `WsfLibrationPoint.hpp` | 阅读头文件 | 类定义、枚举类型（`System` 和 `Point`）、所有成员变量的类型和初始值分配。`mutable` 标记揭示了哪些变量是缓存变量。`private` 方法签名显示了 ComputeGamma 的隐式调用点。 |
| `WsfLibrationPoint.cpp` | 逐函数分析 | `ComputeGamma()` 中 Newton-Raphson 求解五次方程的完整实现，包括初始猜测 $\gamma_0$ 公式、收敛容差 1.0e-14。`UpdateTransform()` 中的旋转矩阵构建逻辑（ECI → RF 变换），包括 `zHatDot = 0` 的简化假设。`GetPointLocation()` 中 L1-L5 无量纲位置的定义。 |
| `WsfLibrationTargetPoint.cpp/.hpp` | 阅读脚本绑定 | LibrationPoint 的脚本接口暴露方式和使用模式。 |
| `UtNewtonRaphson.hpp` | 阅读框架工具 | Newton-Raphson 1D 迭代求解器的接口签名和收敛行为说明。 |
| `function-index.jsonl` | JSON 行检索 | 通过 `grep` 搜索 `LibrationPoint` 确认关键函数：`ComputeGamma` 标记为 `math`，`F_Gamma1`/`F_Gamma2`/`F_Gamma3` 及其导数函数均出现在索引中。 |

**提取流程**：
1. 从头文件的 private 成员变量中提取"内部状态"，区分不变变量（`mSystem`、`mMuStar`、`mGamma1-3`）和可变缓存变量（`mutable` 标记的 `mPosDiff`、`mTransform` 等）。
2. 从 `ComputeGamma()` 函数提取 Newton 迭代的参数（容差、初始猜测）作为边界条件。
3. 从 `GetPointLocation()` 函数直接读取 L1-L5 的无量纲坐标定义，与 `UpdateTransform()` 中的非量纲化逻辑结合理解位置变换。
4. 从 `UpdateTransform()` 函数提取旋转矩阵构建方法和 `zHatDot = 0` 的简化假设作为边界条件。
5. 从 `GetPrimaryBody()` / `GetSecondaryBody()` 确认每个系统使用的 `UtCentralBody` 子类（`UtSun`、`UtEarthEGM96`、`UtMoon`、`UtJupiter`），作为提取过程中确定天体数据来源的路径。

### 源码位置

| File | Symbol | 中文说明 |
|------|--------|----------|
| [WsfLibrationPoint.hpp](source_root/src/core/wsf_space/source/WsfLibrationPoint.hpp) | `WsfLibrationPoint` | 平动点类声明 |
| [WsfLibrationPoint.cpp](source_root/src/core/wsf_space/source/WsfLibrationPoint.cpp) | `ComputeGamma()` | Gamma 系数计算 — 五次方程 Newton 求解 |
| 同上 | — | L1-L5 位置计算 |

### 可移植性评分

**可移植性**：高 — 限制性三体问题公式为标准天体力学内容，Gamma 系数 Newton 迭代为通用数值方法，可直接用公式重实现。
