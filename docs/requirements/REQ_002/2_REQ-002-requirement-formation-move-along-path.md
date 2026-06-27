# 延航线机动设计需求规范文档

> **模糊需求文档**：`docs/requirements/REQ_002/0_formation_move_along_path.md`
> **日期**：2026-06-26
> **需求编号**：REQ-002
> **状态**：已确认

本规范需求文档中的所有需求均源于 `0_formation_move_along_path.md` 模糊需求文档，原模糊需求文档共提出需求 **2 个（3 个子需求）**，在本文档规范表述为 **3 个规范需求**（含 1 个集成需求），对应关系如下：

| # | 原需求 | 对应规范需求 |
|---|-------|--------------|
| 1 | REQ-002（延航线机动） | REQ-002-PATH-01 |
| 2 | REQ-002（延航线机动） | REQ-002-KINEMATICS-02 |
| 3 | REQ-002（延航线机动） | REQ-002-INTEGRATION-03（集成层） |

自有系统中未有的需求对应关系如下：

| # | 原需求 | 对应规范需求 | 自有系统覆盖度 |
|---|-------|--------------|--------------|
| 1 | REQ-002 | REQ-002-PATH-01 | ❌ |
| 2 | REQ-002 | REQ-002-KINEMATICS-02 | ❌ |
| 3 | REQ-002 | REQ-002-INTEGRATION-03 | ❌ |

- ✅ 完全满足（功能完全匹配，接口兼容）
- ⚠️ 部分满足（有类似功能但需要修改接口或补充参数）
- ❌ 缺失（无相关实现，但 AFSIM 有参考实现）
- 🆕 缺失（AFSIM无参考）（无相关实现，且 AFSIM 中也无对应功能，需全新设计）
- ❓ 无法判断（索引或描述不足，需人工补充）


---

## 非功能需求（已确认）

> 以下非功能需求已经人工确认，适用于本文档中的所有规范需求。

### 1. 多线程支持

| 规范需求ID | 是否需要多线程支持 | 依据 | 备注 |
|-----------|------------------|------|------|
| REQ-002-PATH-01 | ✅ | 单机路径推进为串行逻辑 | 多机并行时各自持有独立航线副本 |
| REQ-002-KINEMATICS-02 | ✅ | 单机六自由度计算为串行逻辑 | 多机并行时每架飞机持有独立状态副本，数据并行无需锁 |
| REQ-002-INTEGRATION-03 | ✅ | 集成层为单机调度，无共享状态 | — |

### 2. 性能要求

| 规范需求ID | 单次调用耗时上限 | 内存占用上限 | 其他性能约束 | 备注 |
|-----------|----------------|-------------|-------------|------|
| REQ-002-KINEMATICS-02 | < 200 μs | < 10 KB | 每仿真步长调用 1 次 | — |
| REQ-002-INTEGRATION-03 | < 300 μs（含路径+六自由度） | < 20 KB | 每仿真步长调用 1 次 | — |

### 3. 平台与可移植性

| 项目 | 要求 | 备注 |
|------|------|------|
| 目标 OS | 跨平台 | Windows + Linux |
| C++ 标准 | C++17 | — |
| 编译器 | MSVC / GCC / Clang | — |
| 第三方库限制 | 允许 Eigen | 向量/矩阵计算 |

### 4. 其他约束

| 项目 | 要求 | 备注 |
|------|------|------|
| 编码规范 | Google Style | — |
| 单元测试覆盖率 | > 80% 核心路径 | — |
| 文档语言 | 中文注释 + 英文标识符 | 统一要求 |


---


## 1. REQ-002 → REQ-002-PATH-01：航线管理与航路跟踪

本原需求旨在**为无人机/飞机提供沿预设期望航线（坐标点数组）自主飞行的航路管理能力**，要求**根据飞机的当前位置和期望航线，通过航线跟踪、航路段切换和航向引导计算，驱动飞机沿航线运动**，实现**飞机参考轨迹随时间的航线推进，并输出剩余未到达的期望航点**。

> **AFSIM 参考**：wsf_p6dof 和 wsf_six_dof 的 `maneuver/` 子目录（机动动作库），含航路管理、制导计算机（GuidanceComputer）等模块。编队汇合/位置保持/追击三状态机动控制算法（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.编队汇合/位置保持/追击三状态机动控制）的 FormUp（远距离飞向目标）和 KeepStation（ECS 坐标系 P+D+DD 精细控制）阶段为航路跟踪提供了参考逻辑。对应卡片 [flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md)

### 需求实现流程
- 输入变量：期望航线（path, vector\<Point\>）、当前仿真步长（Δt, double）、飞机速度（V, double）、最大速度（V_max, double）、风速（V_wind, double）、当前时间戳（t, double）

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 其他变量 | 其他常量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|---------|---------|------|-------------|
| ❌ | 1. 航路段映射 | path, Δt, V | current_leg_index, leg_progress（航路段序号和当前段内进度） | 当前位置（cur_pos, Point） | 航线点数组（path_array）、地球参数（Earth_Params） | 根据飞机当前位置，确定所处的航路段；若到达航路点则切换到下一段 | Y |
| ❌ | 2. 航线推进 | current_leg_index, leg_progress, V, Δt, V_wind | ref_pos_next（下一时刻参考点位置） | 期望航向角（heading_cmd, deg） | 最大速度（V_max） | 沿当前航路段以设定速度推进参考点位置，考虑风速影响 | N |
| ❌ | 3. 剩余航线裁剪 | path, ref_pos_next | remaining_path（剩余期望航线, vector\<Point\>） | — | — | 从原航线中裁剪已飞越的航路点，返回剩余未到达的航点序列 | N |

- 输出变量：remaining_path（剩余的期望航线, vector\<Point\>）、ref_pos_next（飞机参考点下一时刻位置, Point）、heading_cmd（期望航向角, double）

#### 算法1：航路段映射（已简化）

本算法旨在**确定飞机在航线中的位置（位于哪个航路段以及段内进度）**，通过**点到线段投影和累积弧长计算**，实现**航路段索引和段内归一化进度的确定**。

> **AFSIM 参考**：wsf_p6dof 和 wsf_six_dof 的 `maneuver/` 子目录中航路管理模块；编队三状态机动控制的 FormUp 阶段含航路跟踪逻辑

✅ 已选择——简化方案2：将**逐段搜索简化为仅向前搜索（禁止回退）**。算法复杂度从 O(N) 降至 O(1)（仅检查当前段+下一段）。
   1. 用公式表示为，搜索范围从 $\forall i \in [1, N-1]$ 缩减为 $i \in [\text{current\_leg}, \text{current\_leg}+1]$，已知航线单调前进方向。
   2. 简化后涉及变量：当前段索引（current_leg）
   3. 简化后涉及常量：无

#### 算法2：航线推进（无需简化）

本算法旨在**沿当前航路段以设定速度推进参考点**，通过**航向矢量计算和风速修正**，实现**参考点沿航线的增量位移，并输出期望航向角**。

> **AFSIM 参考**：编队三状态机动控制的 KeepStation 阶段——ECS 坐标系 P+D+DD 偏差精细控制

不简化。使用完整的风速修正和航线推进逻辑。

#### 算法3：剩余航线裁剪（无需简化）

本算法旨在**从原始航线中移除已飞越的航路点**，通过**航点遍历和进度判断**，实现**返回未完成航线供下游使用**。为基本数组操作，无需简化。


## 2. REQ-002 → REQ-002-KINEMATICS-02：六自由度运动学计算

本原需求旨在**使用六自由度模型计算飞机的姿态、位置和剩余油量**，要求**以仿真步长为推进单位，基于上一时刻的飞行状态（位置、速度、姿态角、角速度）和发动机燃油流量、期望航向角等输入，通过推进系统→气动模型→运动学积分→姿态控制的四步管线**，实现**本时刻飞行状态（位置、速度、姿态角、角速度）及燃油剩余量的精确输出**。

> **AFSIM 参考**：wsf_six_dof 模块（849 源文件），含 PointMass（点质）和 RigidBody（刚体）双重模型。核心类包括 RigidBodySixDOF_Mover、PointMassMover、PointMassPropulsionSystem、RigidBodyAeroCoreObject、PointMassFlightControlSystem。架构文档：docs/architecture/wsf_plugins/afsim-architecture.md §2.1.2；算法卡片：docs/algorithms/CompendiumofAlgorithms.md §一（飞行动力学，8 个算法）。
> 
> **补充约束（已确认）**：根据模糊需求的补充要求，默认从起飞到降落期间，飞机的物理属性（大小、材质、外观、非燃油质量、转动惯量等）保持不变，六自由度计算中的质量参数（m）和转动惯量张量（I）为常量，仅燃油质量（m_fuel）随时间衰减。

### 需求实现流程
- 输入变量：仿真步长（Δt, double）、当前时间戳（t, double）、飞机上一时刻位置（prev_position, Point）、上一时刻姿态（prev_posture, Posture）、上一时刻速度（prev_velocity, double）、上一时刻角速度（p/q/r, Vector3）、发动机燃油流量（fuel_flow_rate, double）、上一时刻燃油量（prev_fuel, double）、期望航向角（heading_cmd, double，来自 REQ-002-PATH-01）

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 其他变量 | 其他常量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|---------|---------|------|-------------|
| ❌ | 1. 推进系统与燃油管理 | Δt, fuel_flow_rate, prev_fuel, prev_velocity, prev_position.alt | F_thrust（推力）, updated_fuel（本时刻燃油量） | 油门位置（δ_throttle）、发动机转速（N_spool） | 发动机推力表（T_Table）、燃油消耗率表（TSFC_Table）、油箱容量（Fuel_Capacity） | 根据油门和飞行状态查表计算发动机推力，并更新燃油消耗量 | Y |
| ❌ | 2. 气动模型 | prev_velocity, prev_position.alt, prev_posture, p, q, r | F_aero（气动合力矢量）, M_aero（气动合力矩矢量） | 马赫数（Ma）、攻角（α）、侧滑角（β）、动压（q̄） | 参考面积（S_ref）、参考长度（l_ref）、稳定性导数表（C_L/C_D/C_Y/C_l/C_m/C_n Table） | 根据飞行状态计算气动六分量（升力/阻力/侧力/滚转力矩/俯仰力矩/偏航力矩） | Y |
| ❌ | 3. 六自由度积分器 | F_thrust, F_aero, M_aero, prev_position, prev_posture, prev_velocity, p, q, r, Δt | new_position（本时刻位置）, new_posture（本时刻姿态）, new_velocity（本时刻速度）, new_angular_velocity（本时刻角速度） | 四元数（q₀,q₁,q₂,q₃）、质量（m, 常量）、转动惯量（I_xx/I_yy/I_zz/I_xz, 常量） | 重力加速度（g=9.80665）、质量（m）、转动惯量张量（I） | 使用 Heun 预测-校正法进行六自由度时间推进：将合力和合力矩转化为线加速度和角加速度，积分得到速度、位置、角速度和姿态角 | N |
| ❌ | 4. 姿态控制系统 SAS | prev_angular_velocity, prev_posture, control_command（δ_elevator/δ_aileron/δ_rudder）, prev_velocity, α, β | angular_accel（角加速度 p̈/q̈/r̈，含限幅保护） | 各通道限幅值（p̈_max/q̈_max/r̈_max） | 控制增益（K_p/K_i/K_d）、时间常数（τ_roll/τ_pitch/τ_yaw） | 控制-稳定解耦：将控制指令（含期望航向角）转化为角加速度，含各通道独立限幅保护 | N |

- 输出变量：new_position（本时刻位置, Point）、new_posture（本时刻姿态, Posture）、new_velocity（本时刻速度, double）、new_angular_velocity（本时刻角速度, Vector3）、updated_fuel（本时刻燃油量, double）

#### 算法1：推进系统与燃油管理（已简化）

本算法旨在**根据发动机燃油流量输入和当前飞行状态（速度、高度）计算发动机推力并更新燃油量**，通过**燃油消耗率限制、燃油质量更新和推力查表**，实现**推力输出和燃油状态的时间推进**。根据补充约束，非燃油质量在飞行全程保持恒定。

> **AFSIM 参考**：
> - **推力计算**：喷气发动机推力模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.喷气发动机推力模型），对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)
> - **燃油管理**：推进系统与燃油管理模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.推进系统与燃油管理模型），对应卡片 [flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md)

> **参数说明**：当前需求参数（fuel_flow_rate、prev_fuel、fuel_consumption_rate）不足以支持完整模型运行（完整模型需 9 类额外参数：推力表/TSFC/额定推力/spin速率/油门位置/油箱容量/供油速率/CG位置）。以下三个简化方案采用"最简"层级组合，仅需补充：T_max(h) 曲线、恒定燃油流量标量值、油箱最大容量和初始油量。

✅ 已选择——简化方案1（推力）：将**喷气发动机三层查表推力模型（Idle/Mil/AB）+ spool dynamics 简化为线性推力-油门关系**。对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)。
   1. 用公式表示为，将 $$T = T_{idle} + \delta_{mil} \cdot (T_{mil} - T_{idle}) + \delta_{ab} \cdot (T_{ab} - T_{mil})$$ 简化为 $$T = \delta_{throttle} \times T_{max}(h)$$
   2. 简化后涉及变量：油门位置（δ_throttle）、最大推力曲线（T_max(h)）
   3. 简化后涉及常量：最大推力（T_max_sea_level）
   4. 需补充参数：T_max(h) 曲线（或海平面最大推力标量值）

✅ 已选择——简化方案2（燃油消耗）：将**TSFC 三段增量式燃油消耗计算简化为恒定燃油消耗率**。对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)。
   1. 用公式表示为，将三段增量式 TSFC 公式简化为 $$m_{fuel} = \dot{m}_{const} \cdot \Delta t$$
   2. 简化后涉及变量：恒定燃油流量（fuel_flow_rate_const, double）
   3. 简化后涉及常量：恒定燃油消耗率（Fuel_Const_Rate）
   4. 需补充参数：恒定燃油流量标量值

✅ 已选择——简化方案3（油箱管理）：将**多油箱燃油管理（油箱传输协调 + CG 插值 + 质量汇总）简化为单油箱模型**。对应卡片 [flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md)。
   1. 用公式表示为，跳过传输分组/比例协调逻辑，燃油直接从唯一油箱消耗：$$m_{fuel}(t+\Delta t) = m_{fuel}(t) - m_{burn}$$，CG 固定在油箱中心。
   2. 简化后涉及变量：单油箱当前油量（current_fuel, double）
   3. 简化后涉及常量：油箱最大容量（Max_Fuel_Capacity）、初始油量（Initial_Fuel）
   4. 需补充参数：油箱最大容量、初始油量

#### 算法2：气动模型（已简化）

本算法旨在**根据飞机当前飞行状态（马赫数、攻角、侧滑角、角速率）计算气动六分量（升力、阻力、侧力、滚转力矩、俯仰力矩、偏航力矩）**。

> **AFSIM 参考**：RigidBody 稳定性导数气动系数模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.RigidBody 稳定性导数气动系数模型），对应卡片 [flight-dynamics-rigidbody-aero-coefficient-card.md](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md)；PointMass 气动力与旋转限幅模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 气动力与旋转限幅模型），对应卡片 [flight-dynamics-pointmass-aero-card.md](../../algorithms/flight-dynamics-pointmass-aero-card.md)

✅ 已选择——简化方案2：将**气动力矩计算简化为仅保留气动力（不计算力矩），依赖 SAS 控制角加速度**。算法复杂度从 O(6分量×6维插值) 降至 O(3分量×1维插值)。
   1. 用公式表示为，将完整气动六分量 $$[F_x, F_y, F_z, M_x, M_y, M_z]^T$$ 简化为仅气动力 $$[F_x, F_y, F_z]^T$$，力矩全部由 SAS 系统提供。
   2. 简化后涉及变量：气动力矢量（F_aero）
   3. 简化后涉及常量：无

#### 算法3：六自由度积分器（无需简化）

本算法旨在**对飞机进行六自由度时间推进**，通过**Heun 预测-校正法（二阶 Runge-Kutta）+ 四元数姿态积分 + 欧拉转动方程（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz）**，实现**从合力和合力矩到下一时刻飞行状态（位置、速度、姿态四元数、角速度）的数值积分**。根据补充约束，质量（m）和转动惯量张量（I）在飞行全程为常量（仅燃油质量随时间衰减）。

> **AFSIM 参考**：刚体六自由度 Heun 预测-校正积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.刚体六自由度积分器），对应卡片 [flight-dynamics-rigid-body-integrator-card.md](../../algorithms/flight-dynamics-rigid-body-integrator-card.md)；PointMass 六自由度 Heun 积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 六自由度 Heun 积分器），对应卡片 [flight-dynamics-pointmass-integrator-card.md](../../algorithms/flight-dynamics-pointmass-integrator-card.md)

#### 算法4：姿态控制系统 SAS（无需简化）

本算法旨在**为飞机提供旋转角加速度控制**，通过**控制-稳定解耦架构（一阶指令跟踪 + 二阶临界阻尼稳定项 + 独立通道限幅）**，实现**从控制指令（升降舵/副翼/方向舵偏转，含期望航向角）到角加速度的安全转化，防止大迎角操纵效能丧失**。

> **AFSIM 参考**：PointMass 稳定增稳系统 SAS（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 稳定增稳系统），对应卡片 [flight-dynamics-pointmass-sas-card.md](../../algorithms/flight-dynamics-pointmass-sas-card.md)


## 3. REQ-002 → REQ-002-INTEGRATION-03：航线机动集成层

本原需求旨在**将航线管理（REQ-002-PATH-01）和六自由度运动学计算（REQ-002-KINEMATICS-02）集成为一个完整的单机航线机动仿真步长更新**，要求**以仿真步长为推进单位，按顺序调用航路段映射→航线推进→剩余航线裁剪→推进系统→气动模型→积分器→SAS，组织输入数据的分发和输出数据的收集**，实现**飞机沿航线机动的端到端仿真更新**。

> **AFSIM 参考**：AFSIM 中飞机运动由 WsfPlatform 的 Update 循环驱动，Mover 基类负责位置/速度/姿态更新。wsf_six_dof 的 `maneuver/` 子目录实现机动编排。架构文档：docs/architecture/wsf_plugins/afsim-architecture.md §2.1 运动学系统，docs/architecture/core/afsim-architecture.md §6 仿真生命周期。

### 需求实现流程
- 输入变量：path（期望航线, vector\<Point\>）、prev_path（上个步长内路径, vector\<Point\>）、prev_posture（上个步长内姿态, vector\<Posture\>）、prev_velocity（上个步长内速度, vector\<double\>）、prev_fuel（上个步长内油量, vector\<double\>）、Δt（仿真步长, double）、t（当前时间戳, double）、fuel_consumption_rate（耗油量, double）、V_wind（风速, double）、V（飞机速度, double）、V_max（最大速度, double）、地球参数（Earth_Params）

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 其他变量 | 其他常量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|---------|---------|------|-------------|
| ❌ | 1. 航线推进 | path, V, Δt, V_wind, t, Earth_Params | ref_pos_next, remaining_path, heading_cmd | — | V_max | 调用 REQ-002-PATH-01：航路段映射→航线推进→剩余航线裁剪 | N |
| ❌ | 2. 六自由度计算 | ref_pos_next, heading_cmd, prev_path, prev_posture, prev_velocity, prev_fuel, Δt, fuel_consumption_rate | new_path, new_posture, new_velocity, new_fuel | — | 气动/推力/惯量常量（全部为飞行全程常量） | 调用 REQ-002-KINEMATICS-02：推进系统→气动模型→积分器→SAS | N |
| ❌ | 3. 输出组装 | new_path, new_posture, new_velocity, new_fuel, Δt | output_path, output_posture, output_velocity, output_fuel | — | 步长阈值（1 s） | 步长自适应输出：>1s 时输出每秒状态序列；≤1s 时仅输出下一帧状态 | N |

- 输出变量：remaining_path（剩余航线, vector\<Point\>）、output_path（输出路径, vector\<Point\>）、output_posture（输出姿态, vector\<Posture\>）、output_velocity（输出速度, vector\<double\>）、output_fuel（输出油量, vector\<double\>）

#### 算法1：集成调度（无需简化）

本算法旨在**编排航线机动仿真的完整更新周期**，通过**顺序调用航线推进→六自由度计算→输出组装**，实现**端到端的单机航线机动仿真步长更新**。为纯调度逻辑，无独立算法复杂度。


## 参考文献：
[1]: docs/algorithms/CompendiumofAlgorithms.md "AFSIM 算法汇总文档"
[2]: docs/algorithms/flight-dynamics-station-keeping-card.md "编队汇合/位置保持/追击三状态机动控制算法卡片"
[3]: docs/algorithms/flight-dynamics-rigid-body-integrator-card.md "刚体六自由度积分器算法卡片"
[4]: docs/algorithms/flight-dynamics-pointmass-integrator-card.md "PointMass 六自由度积分器算法卡片"
[5]: docs/algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md "RigidBody 稳定性导数气动系数模型算法卡片"
[6]: docs/algorithms/flight-dynamics-pointmass-aero-card.md "PointMass 气动力与旋转限幅模型算法卡片"
[7]: docs/algorithms/flight-dynamics-propulsion-fuel-card.md "推进系统与燃油管理模型算法卡片"
[8]: docs/algorithms/flight-dynamics-jet-engine-card.md "喷气发动机推力模型算法卡片"
[9]: docs/algorithms/flight-dynamics-pointmass-sas-card.md "PointMass 稳定增稳系统算法卡片"
[10]: docs/architecture/core/afsim-architecture.md "AFSIM 核心架构报告"
[11]: docs/architecture/wsf_plugins/afsim-architecture.md "AFSIM 插件架构报告（含 wsf_six_dof 子系统）"