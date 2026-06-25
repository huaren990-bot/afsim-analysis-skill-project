# 无人机六自由度机动设计需求规范文档

> **模糊需求文档**：`docs/requirements/external_requirements_doc/six_dof_UAV.md`
> **日期**：2026-06-16
> **需求编号**：REQ-001

本规范需求文档中的所有需求均源于 `six_dof_UAV.md` 模糊需求文档，原模糊需求文档共提出需求 **1 个**，在本文档规范表述为 **1 个**，对应关系如下：

| #   | 原需求     | 对应规范需求            |
| --- | ------- | ----------------- |
| 1   | REQ-001 | REQ-001-SIXDOF-01 |


## 1. REQ-001 → REQ-001-SIXDOF-01

本原需求旨在**为无人机/飞机提供六自由度运动学仿真能力**，要求**以仿真步长为推进单位，基于上一时刻的飞行状态（位置、速度、姿态角、角速度）和发动机燃油流量输入，通过推进系统、气动模型、运动学积分和姿态控制四个阶段的级联计算**，实现**本时刻飞行状态（经纬度、高度、速度、姿态角、角速度）及燃油消耗量的精确输出**。

### 需求实现流程
- 输入变量：仿真步长（Δt）、当前时间戳（t）、上一时刻经度（λₜ₋₁）、上一时刻纬度（φₜ₋₁）、上一时刻高度（hₜ₋₁）、上一时刻速度（Vₜ₋₁）、上一时刻翻滚角（φᵣₒₗₗ,ₜ₋₁）、上一时刻俯仰角（θₚᵢₜ꜀ₕ,ₜ₋₁）、上一时刻偏航角（ψᵧₐ𝆑,ₜ₋₁）、上一时刻翻滚角速度（pₜ₋₁）、上一时刻俯仰角速度（qₜ₋₁）、上一时刻偏航角速度（rₜ₋₁）、发动机燃油流量（ṁ𝒻𝓊ₑₗ）、上一时刻燃油量（m𝒻𝓊ₑₗ,ₜ₋₁）

| #   | 流程          | 上流程输入变量                                                                                                | 输出至下流程变量                                                                                                                                 | 其他变量                                               | 其他常量                                                          | 功能                                                             | 是否需要简化 |
| --- | ----------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------- | ------ |
| 1   | 推进系统与燃油管理   | Δt, ṁ𝒻𝓊ₑₗ, m𝒻𝓊ₑₗ,ₜ₋₁, Vₜ₋₁, hₜ₋₁                                                                   | Fₜₕᵣ𝓊ₛₜ（推力）, m𝒻𝓊ₑₗ,ₜ（本时刻燃油量）                                                                                                          | 油门位置（δₜₕᵣₒₜₜₗₑ）、发动机转速（Nₛₚₒₒₗ）                      | 发动机推力表（T_Table）、燃油消耗率表（TSFC_Table）、油箱容量（Fuel_Capacity）        | 根据油门和飞行状态查表计算发动机推力，并更新燃油消耗量                                    | Y/N    |
| 2   | 气动模型        | Vₜ₋₁, hₜ₋₁, φᵣₒₗₗ,ₜ₋₁, θₚᵢₜ꜀ₕ,ₜ₋₁, ψᵧₐ𝆑,ₜ₋₁, pₜ₋₁, qₜ₋₁, rₜ₋₁                                         | Fₐₑᵣₒ（气动合力矢量）, Mₐₑᵣₒ（气动合力矩矢量）                                                                                                            | 马赫数（Ma）、攻角（α）、侧滑角（β）、动压（q̄）                        | 参考面积（Sᵣₑ𝒻）、参考长度（lᵣₑ𝒻）、稳定性导数表（C_L/C_D/C_Y/C_l/C_m/C_n Table） | 根据飞行状态计算气动六分量（升力/阻力/侧力/滚转力矩/俯仰力矩/偏航力矩）                         | Y/N    |
| 3   | 六自由度积分器     | Fₜₕᵣ𝓊ₛₜ, Fₐₑᵣₒ, Mₐₑᵣₒ, λₜ₋₁, φₜ₋₁, hₜ₋₁, Vₜ₋₁, φᵣₒₗₗ,ₜ₋₁, θₚᵢₜ꜀ₕ,ₜ₋₁, ψᵧₐ𝆑,ₜ₋₁, pₜ₋₁, qₜ₋₁, rₜ₋₁, Δt | λₜ（本时刻经度）, φₜ（本时刻纬度）, hₜ（本时刻高度）, Vₜ（本时刻速度）, φᵣₒₗₗ,ₜ（本时刻翻滚角）, θₚᵢₜ꜀ₕ,ₜ（本时刻俯仰角）, ψᵧₐ𝆑,ₜ（本时刻偏航角）, pₜ（本时刻翻滚角速度）, qₜ（本时刻俯仰角速度）, rₜ（本时刻偏航角速度） | 四元数（q₀,q₁,q₂,q₃）、质量（m）、转动惯量（Iₓₓ, Iᵧᵧ, I𝆑𝆑, Iₓ𝆑） | 重力加速度（g）、质量（m）、转动惯量张量（I）                                      | 使用 Heun 预测-校正法进行六自由度时间推进：将合力和合力矩转化为线加速度和角加速度，积分得到速度、位置、角速度和姿态角 | Y/N    |
| 4   | 姿态控制系统（SAS） | pₜ₋₁, qₜ₋₁, rₜ₋₁, α, β, Vₜ₋₁, 控制指令（δₑₗₑᵥₐₜₒᵣ, δₐᵢₗₑᵣₒₙ, δᵣ𝓊𝒹𝒹ₑᵣ）                                    | p̈（翻滚角加速度）, q̈（俯仰角加速度）, r̈（偏航角加速度）                                                                                                       | 各通道限幅值（p̈ₘₐₓ, q̈ₘₐₓ, r̈ₘₐₓ）                        | 控制增益（Kₚ, Kᵢ, K𝒹）、时间常数（τᵣₒₗₗ, τₚᵢₜ꜀ₕ, τᵧₐ𝆑）                  | 控制-稳定解耦：将自动驾驶仪输出的控制指令转化为角加速度，含各通道独立限幅保护                        | Y/N    |

- 输出变量：λₜ（本时刻经度）、φₜ（本时刻纬度）、hₜ（本时刻高度）、Vₜ（本时刻速度）、φᵣₒₗₗ,ₜ（本时刻翻滚角）、θₚᵢₜ꜀ₕ,ₜ（本时刻俯仰角）、ψᵧₐ𝆑,ₜ（本时刻偏航角）、pₜ（本时刻翻滚角速度）、qₜ（本时刻俯仰角速度）、rₜ（本时刻偏航角速度）、m𝒻𝓊ₑₗ,ₜ（本时刻燃油量）

（表中"是否需要简化"列应当留给人工确认）
（需要在表中把所有流程都列出来，严禁使用省略号）

#### 算法1：推进系统与燃油管理

本算法旨在**根据发动机燃油流量输入和当前飞行状态计算发动机推力并更新燃油量**，通过**燃油消耗率限制、燃油质量更新和推力查表**，实现**推力输出和燃油状态的时间推进**。

> **AFSIM 参考**：推进系统与燃油管理模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.推进系统与燃油管理模型），对应卡片 [flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md)；喷气发动机推力模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.喷气发动机推力模型），对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)

1. 简化方案1：将**喷气发动机三层查表推力模型（Idle/Mil/AB）简化为线性推力-油门关系**。算法复杂度从 O(查表×3 表×4 spin rate) 降至 O(1)。
   1. 用公式表示为，将 $$F_{\text{thrust}} = f_{\text{table}}(N_{\text{spool}}, \text{Ma}, h)$$ 简化为 $$F_{\text{thrust}} = \delta_{\text{throttle}} \times F_{\text{max}}(h)$$，其中 $\delta_{\text{throttle}}$ 表示油门位置（0~1），$F_{\text{max}}(h)$ 表示当前高度的最大推力。
   2. 简化后涉及变量：油门位置（δₜₕᵣₒₜₜₗₑ）、最大推力曲线（Fₘₐₓ(h)）
   3. 简化后涉及常量：最大推力（Fₘₐₓ,ₛₑₐₗₑᵥₑₗ）
   4. 是否选择此方案：Y/N  （只有在表格中为该算法选择Y，这里才需要进行简化方案的选择）

2. 简化方案2：将**燃油消耗计算简化为恒定燃油消耗率**。算法复杂度从 O(TSFC 多维查表 + spool dynamics) 降至 O(1)。
   1. 用公式表示为，将 $$\dot{m}_{\text{fuel}} = f_{\text{TSFC}}(F_{\text{thrust}}, \text{Ma}, h)$$ 简化为 $$\dot{m}_{\text{fuel}} = \text{const}$$，其中 $\dot{m}_{\text{fuel}}$ 表示燃油质量流量，const 表示用户配置的恒定燃油消耗率。
   2. 简化后涉及变量：恒定燃油流量（ṁ𝒻𝓊ₑₗ,𝒸ₒₙₛₜ）
   3. 简化后涉及常量：恒定燃油消耗率（Fuel_Const_Rate）
   4. 是否选择此方案：Y/N

#### 算法2：气动模型

本算法旨在**根据无人机当前飞行状态（速度、高度、姿态角、角速度）计算气动力和力矩**，通过**稳定性导数查表或简化解析公式**，实现**气动六分量（升力/阻力/侧力/滚转力矩/俯仰力矩/偏航力矩）的计算**。

> **AFSIM 参考**：RigidBody 稳定性导数气动系数模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.RigidBody 稳定性导数气动系数模型），对应卡片 [flight-dynamics-rigidbody-aero-coefficient-card.md](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md)；PointMass 气动力与旋转限幅模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 气动力与旋转限幅模型），对应卡片 [flight-dynamics-pointmass-aero-card.md](../../algorithms/flight-dynamics-pointmass-aero-card.md)

1. 简化方案1：将**RigidBody 稳定性导数高维查表模型简化为固定气动系数模型**。算法复杂度从 O(稳定性导数查表×6分量×(Ma×α×β×p×q×r 6维插值)) 降至 O(1)。
   1. 用公式表示为，将 $$C_i = C_i(\text{Ma}, \alpha, \beta, p, q, r)$$ 简化为 $$C_i = \text{const}$$，其中 $C_i$ 表示各气动系数（C_L, C_D, C_Y, C_l, C_m, C_n），各自简化为固定常数值。
   2. 简化后涉及变量：固定升力系数（C_L,𝒸ₒₙₛₜ）、固定阻力系数（C_D,𝒸ₒₙₛₜ）、固定侧力系数（C_Y,𝒸ₒₙₛₜ）、固定滚转力矩系数（C_l,𝒸ₒₙₛₜ）、固定俯仰力矩系数（C_m,𝒸ₒₙₛₜ）、固定偏航力矩系数（C_n,𝒸ₒₙₛₜ）
   3. 简化后涉及常量：各组固定气动系数常量值
   4. 是否选择此方案：Y/N

2. 简化方案2：将**气动力矩计算简化为仅保留气动力（不计算力矩），依赖 SAS 控制角加速度**。算法复杂度从 O(6分量×6维插值) 降至 O(3分量×1维插值)。
   1. 用公式表示为，将完整气动六分量 $$[F_x, F_y, F_z, M_x, M_y, M_z]^T$$ 简化为仅气动力 $$[F_x, F_y, F_z]^T$$，力矩全部由 SAS 系统提供。
   2. 简化后涉及变量：气动力矢量（Fₐₑᵣₒ）
   3. 简化后涉及常量：无
   4. 是否选择此方案：Y/N

#### 算法3：六自由度积分器

本算法旨在**对无人机进行六自由度时间推进**，通过**Heun 预测-校正法（二阶 Runge-Kutta）+ 四元数姿态积分 + 欧拉转动方程**，实现**从合力和合力矩到下一时刻飞行状态（位置、速度、姿态角、角速度）的数值积分**。

> **AFSIM 参考**：刚体六自由度 Heun 预测-校正积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.刚体六自由度积分器），对应卡片 [flight-dynamics-rigid-body-integrator-card.md](../../algorithms/flight-dynamics-rigid-body-integrator-card.md)；PointMass 六自由度 Heun 积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 六自由度 Heun 积分器），对应卡片 [flight-dynamics-pointmass-integrator-card.md](../../algorithms/flight-dynamics-pointmass-integrator-card.md)

1. 简化方案1：将**刚体六自由度积分器（含完整转动惯量张量 Iₓₓ, Iᵧᵧ, I𝆑𝆑, Iₓ𝆑 和欧拉转动方程）简化为 PointMass 点质积分器（忽略转动惯量耦合，使用半隐式欧拉法旋转积分）**。算法复杂度从 O(转动惯量矩阵求逆 + 交叉耦合项) 降至 O(对角项独立积分)。
   1. 用公式表示为，将刚体转动方程 $$I\dot{\boldsymbol{\omega}} + \boldsymbol{\omega} \times (I\boldsymbol{\omega}) = \mathbf{M}_{\text{total}}$$ 简化为点质旋转方程 $$\dot{p} = M_x, \dot{q} = M_y, \dot{r} = M_z$$（单位转动惯量），其中 $\boldsymbol{\omega} = [p, q, r]^T$ 表示角速度矢量，$I$ 表示转动惯量张量，$\mathbf{M}_{\text{total}}$ 表示合外力矩。
   2. 简化后涉及变量：角速度（p, q, r）、合外力矩（Mₓ, Mᵧ, M𝆑）
   3. 简化后涉及常量：无需转动惯量矩阵
   4. 是否选择此方案：Y/N

2. 简化方案2：将**Heun 预测-校正法（二阶 RK）简化为显式欧拉法（一阶）**。算法复杂度从 O(2次函数评估/步) 降至 O(1次函数评估/步)，但精度从 O(Δt²) 降至 O(Δt)。
   1. 用公式表示为，将 Heun 法 $$\begin{cases} \mathbf{y}^* = \mathbf{y}_n + \Delta t \cdot f(t_n, \mathbf{y}_n) \\ \mathbf{y}_{n+1} = \mathbf{y}_n + \frac{\Delta t}{2}[f(t_n, \mathbf{y}_n) + f(t_{n+1}, \mathbf{y}^*)] \end{cases}$$ 简化为显式欧拉法 $$\mathbf{y}_{n+1} = \mathbf{y}_n + \Delta t \cdot f(t_n, \mathbf{y}_n)$$，其中 $\mathbf{y}$ 表示状态矢量（位置、速度、姿态四元数、角速度）。
   2. 简化后涉及变量：状态矢量（y）
   3. 简化后涉及常量：无
   4. 是否选择此方案：Y/N

#### 算法4：姿态控制系统（SAS）

本算法旨在**为无人机提供旋转角加速度控制**，通过**控制-稳定解耦架构（一阶指令跟踪 + 二阶临界阻尼稳定项 + 独立通道限幅）**，实现**从自动驾驶仪控制指令到角加速度的安全转化，防止大迎角操纵效能丧失**。

> **AFSIM 参考**：PointMass 稳定增稳系统（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 稳定增稳系统），对应卡片 [flight-dynamics-pointmass-sas-card.md](../../algorithms/flight-dynamics-pointmass-sas-card.md)

1. 简化方案1：将**完整三通道控制-稳定解耦 SAS 简化为仅角加速度限幅**。算法复杂度从 O(3通道×(P控制+I积分+D微分+限幅)) 降至 O(3通道×限幅)。
   1. 用公式表示为，将完整 SAS 控制律 $$\ddot{\theta}_{cmd} = K_p(\theta_{cmd} - \theta) + K_i\int(\theta_{cmd} - \theta)dt + K_d(\dot{\theta}_{cmd} - \dot{\theta})$$ 简化为 $$\ddot{\theta} = \text{clip}(\ddot{\theta}_{cmd}, -\ddot{\theta}_{max}, \ddot{\theta}_{max})$$，其中 $\theta$ 表示姿态角（滚转/俯仰/偏航），$\ddot{\theta}_{cmd}$ 表示控制指令角加速度，$\ddot{\theta}_{max}$ 表示角加速度限幅。
   2. 简化后涉及变量：控制指令角加速度（p̈𝒸ₘ𝒹, q̈𝒸ₘ𝒹, r̈𝒸ₘ𝒹）、角加速度限幅值（p̈ₘₐₓ, q̈ₘₐₓ, r̈ₘₐₓ）
   3. 简化后涉及常量：各通道角加速度最大限幅值
   4. 是否选择此方案：Y/N

2. 简化方案2：将**完整 SAS 完全跳過，直接将控制指令角加速度输出给积分器**。算法复杂度从 O(3通道×3项PID) 降至 O(0)（跳过此流程）。
   1. 用公式表示为，将 SAS 环节完全省略，即 $$\ddot{\theta} = \ddot{\theta}_{cmd}$$，不做任何滤波、限幅或稳定化处理。
   2. 简化后涉及变量：控制指令角加速度（p̈𝒸ₘ𝒹, q̈𝒸ₘ𝒹, r̈𝒸ₘ𝒹）
   3. 简化后涉及常量：无
   4. 是否选择此方案：Y/N

## 参考文献：
[1]: docs/algorithms/CompendiumofAlgorithms.md "AFSIM 算法汇总文档"
[2]: docs/algorithms/flight-dynamics-propulsion-fuel-card.md "推进系统与燃油管理模型算法卡片"
[3]: docs/algorithms/flight-dynamics-jet-engine-card.md "喷气发动机推力模型算法卡片"
[4]: docs/algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md "RigidBody 稳定性导数气动系数模型算法卡片"
[5]: docs/algorithms/flight-dynamics-pointmass-aero-card.md "PointMass 气动力与旋转限幅模型算法卡片"
[6]: docs/algorithms/flight-dynamics-rigid-body-integrator-card.md "刚体六自由度积分器算法卡片"
[7]: docs/algorithms/flight-dynamics-pointmass-integrator-card.md "PointMass 六自由度积分器算法卡片"
[8]: docs/algorithms/flight-dynamics-pointmass-sas-card.md "PointMass 稳定增稳系统算法卡片"