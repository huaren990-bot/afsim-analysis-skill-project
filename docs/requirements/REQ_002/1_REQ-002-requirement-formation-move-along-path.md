# 延航线机动设计需求规范文档

> **模糊需求文档**：`docs/requirements/REQ_002/0_formation_move_along_path.md`
> **日期**：2026-06-26
> **需求编号**：REQ-002

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

## 非功能需求

> **说明**：以下非功能需求适用于本文档中的所有规范需求。人工需逐项确认，确认后作为下游设计和实现的约束条件。

### 1. 多线程支持

| 规范需求ID                 | 是否需要多线程支持 | 依据             | 备注                        |
| ---------------------- | --------- | -------------- | ------------------------- |
| REQ-002-PATH-01        | ✅         | 单机路径推进为串行逻辑    | 多机并行时各自持有独立航线副本           |
| REQ-002-KINEMATICS-02  | ✅         | 单机六自由度计算为串行逻辑  | 多机并行时每架飞机持有独立状态副本，数据并行无需锁 |
| REQ-002-INTEGRATION-03 | ✅         | 集成层为单机调度，无共享状态 | —                         |

- ✅ 需要多线程支持：算法复杂度高、或实时性要求严格、或目标系统为多线程架构，各实体需并行更新
- ❌ 不需要：算法简单、或单线程即可满足性能要求、或无共享状态无需考虑并发
- ⚠️ 不确定：需人工评估算法复杂度和性能需求后再定

> 多线程支持判定规则：
> 1. 若目标系统为多线程架构，且该需求对应的算法在各实体间独立执行（数据并行），标记为 ✅ 需要多线程支持，但实现难度较低——每个实体持有独立状态副本即可天然线程安全。
> 2. 若算法涉及跨实体的共享状态（如全局资源池、环境数据），标记为 ✅ 并额外标注"含共享状态，需加锁或原子操作"。
> 3. 若 AFSIM 原始实现为单线程，但目标系统为多线程，标记为 ⚠️ 并注明需评估线程安全改造的工作量。

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

| #   | 流程        | 上流程输入变量                                        | 输出至下流程变量                                      | 其他变量                    | 其他常量                                 | 功能                              | 是否需要简化 |
| --- | --------- | ---------------------------------------------- | --------------------------------------------- | ----------------------- | ------------------------------------ | ------------------------------- | ------ |
| ❌   | 1. 航路段映射  | path, Δt, V                                    | current_leg_index, leg_progress（航路段序号和当前段内进度） | 当前位置（cur_pos, Point）    | 航线点数组（path_array）、地球参数（Earth_Params） | 根据飞机当前位置，确定所处的航路段；若到达航路点则切换到下一段 | Y      |
| ❌   | 2. 航线推进   | current_leg_index, leg_progress, V, Δt, V_wind | ref_pos_next（下一时刻参考点位置）                       | 期望航向角（heading_cmd, deg） | 最大速度（V_max）                          | 沿当前航路段以设定速度推进参考点位置，考虑风速影响       | N      |
| ❌   | 3. 剩余航线裁剪 | path, ref_pos_next                             | remaining_path（剩余期望航线, vector\<Point\>）       | —                       | —                                    | 从原航线中裁剪已飞越的航路点，返回剩余未到达的航点序列     | N      |

- 输出变量：remaining_path（剩余的期望航线, vector\<Point\>）、ref_pos_next（飞机参考点下一时刻位置, Point）、heading_cmd（期望航向角, double）

（表中"是否需要简化"列应当留给人工确认）
（需要在表中把所有流程都列出来，严禁使用省略号）

#### 算法1：航路段映射

本算法旨在**确定飞机在航线中的位置（位于哪个航路段以及段内进度）**，通过**点到线段投影和累积弧长计算**，实现**航路段索引和段内归一化进度的确定**。

> **AFSIM 参考**：wsf_p6dof 和 wsf_six_dof 的 `maneuver/` 子目录中航路管理模块；编队三状态机动控制的 FormUp 阶段含航路跟踪逻辑

1. 简化方案1：将**点到线段精确投影简化为最近航路点匹配**。算法复杂度从 O(N×投影) 降至 O(N×距离)。
   1. 用公式表示为，将 $$d = \min_{i} \text{dist\_to\_segment}(\mathbf{p}, \mathbf{p}_i, \mathbf{p}_{i+1})$$ 简化为 $$d = \min_{i} \|\mathbf{p} - \mathbf{p}_i\|$$，其中 $\mathbf{p}$ 表示飞机位置，$\mathbf{p}_i$ 表示第 i 个航路点。
   2. 简化后涉及变量：最近航路点索引（i_nearest）
   3. 简化后涉及常量：无
- [ ] 选择此方案

1. 简化方案2：将**逐段搜索简化为仅向前搜索（禁止回退）**。算法复杂度从 O(N) 降至 O(1)（仅检查当前段+下一段）。
   1. 用公式表示为，搜索范围从 $\forall i \in [1, N-1]$ 缩减为 $i \in [\text{current\_leg}, \text{current\_leg}+1]$，已知航线单调前进方向。
   2. 简化后涉及变量：当前段索引（current_leg）
   3. 简化后涉及常量：无
- [x] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法2：航线推进

本算法旨在**沿当前航路段以设定速度推进参考点**，通过**航向矢量计算和风速修正**，实现**参考点沿航线的增量位移，并输出期望航向角**。

> **AFSIM 参考**：编队三状态机动控制的 KeepStation 阶段——ECS 坐标系 P+D+DD 偏差精细控制

1. 简化方案1：将**风速修正简化为矢量线性叠加**（忽略阵风和湍流）。算法复杂度保持 O(1)。
   1. 用公式表示为，将 $$\mathbf{v}_{\text{ground}} = \mathbf{v}_{\text{air}} + \mathbf{v}_{\text{wind}}(t, h)$$ 简化为 $$\mathbf{v}_{\text{ground}} = \mathbf{v}_{\text{air}} + \mathbf{v}_{\text{wind\_const}}$$，其中 $\mathbf{v}_{\text{wind\_const}}$ 表示恒定风速矢量。
   2. 简化后涉及变量：恒定风速（V_wind_const, double + direction）
   3. 简化后涉及常量：恒定风速矢量（Wind_Vector_Const）
- [ ] 选择此方案

1. 简化方案2：将**弧线航线推进简化为直线航段间折线推进**（不进行弧线拟合）。航线曲率处产生位置跳变。
   1. 用公式表示为，航路段连接处不进行平滑过渡，参考点直接从段 i 的终点跳至段 i+1 的起点。
   2. 简化后涉及变量：航路段端点（p_i, p_{i+1}）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法3：剩余航线裁剪

本算法旨在**从原始航线中移除已飞越的航路点**，通过**航点遍历和进度判断**，实现**返回未完成航线供下游使用**。

1. 简化方案1：无需简化。此算法为基本数组操作。
- [ ] 选择此方案

1. 简化方案2：无需简化。
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  


## 2. REQ-002 → REQ-002-KINEMATICS-02：六自由度运动学计算

本原需求旨在**使用六自由度模型计算飞机的姿态、位置和剩余油量**，要求**以仿真步长为推进单位，基于上一时刻的飞行状态（位置、速度、姿态角、角速度）和发动机燃油流量、期望航向角等输入，通过推进系统→气动模型→运动学积分→姿态控制的四步管线**，实现**本时刻飞行状态（位置、速度、姿态角、角速度）及燃油剩余量的精确输出**。

> **AFSIM 参考**：wsf_six_dof 模块（849 源文件），含 PointMass（点质）和 RigidBody（刚体）双重模型。核心类包括 RigidBodySixDOF_Mover、PointMassMover、PointMassPropulsionSystem、RigidBodyAeroCoreObject、PointMassFlightControlSystem。架构文档：docs/architecture/wsf_plugins/afsim-architecture.md §2.1.2；算法卡片：docs/algorithms/CompendiumofAlgorithms.md §一（飞行动力学，8 个算法）。
> 
> **补充约束**：根据模糊需求的补充要求，默认从起飞到降落期间，飞机的物理属性（大小、材质、外观、非燃油质量、转动惯量等）保持不变，六自由度计算中的质量参数（m）和转动惯量张量（I）为常量，仅燃油质量（m_fuel）随时间衰减。

### 需求实现流程
- 输入变量：仿真步长（Δt, double）、当前时间戳（t, double）、飞机上一时刻位置（prev_position, Point）、上一时刻姿态（prev_posture, Posture）、上一时刻速度（prev_velocity, double）、上一时刻角速度（p/q/r, Vector3）、发动机燃油流量（fuel_flow_rate, double）、上一时刻燃油量（prev_fuel, double）、期望航向角（heading_cmd, double，来自 REQ-002-PATH-01）

| #   | 流程            | 上流程输入变量                                                                                                  | 输出至下流程变量                                                                                   | 其他变量                                                     | 其他常量                                                          | 功能                                                             | 是否需要简化 |
| --- | ------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------- | ------ |
| ❌   | 1. 推进系统与燃油管理  | Δt, fuel_flow_rate, prev_fuel, prev_velocity, prev_position.alt                                          | F_thrust（推力）, updated_fuel（本时刻燃油量）                                                         | 油门位置（δ_throttle）、发动机转速（N_spool）                          | 发动机推力表（T_Table）、燃油消耗率表（TSFC_Table）、油箱容量（Fuel_Capacity）        | 根据油门和飞行状态查表计算发动机推力，并更新燃油消耗量                                    | Y      |
| ❌   | 2. 气动模型       | prev_velocity, prev_position.alt, prev_posture, p, q, r                                                  | F_aero（气动合力矢量）, M_aero（气动合力矩矢量）                                                            | 马赫数（Ma）、攻角（α）、侧滑角（β）、动压（q̄）                              | 参考面积（S_ref）、参考长度（l_ref）、稳定性导数表（C_L/C_D/C_Y/C_l/C_m/C_n Table） | 根据飞行状态计算气动六分量（升力/阻力/侧力/滚转力矩/俯仰力矩/偏航力矩）                         | Y      |
| ❌   | 3. 六自由度积分器    | F_thrust, F_aero, M_aero, prev_position, prev_posture, prev_velocity, p, q, r, Δt                        | new_position（本时刻位置）, new_posture（本时刻姿态）, new_velocity（本时刻速度）, new_angular_velocity（本时刻角速度） | 四元数（q₀,q₁,q₂,q₃）、质量（m, 常量）、转动惯量（I_xx/I_yy/I_zz/I_xz, 常量） | 重力加速度（g=9.80665）、质量（m）、转动惯量张量（I）                              | 使用 Heun 预测-校正法进行六自由度时间推进：将合力和合力矩转化为线加速度和角加速度，积分得到速度、位置、角速度和姿态角 | N      |
| ❌   | 4. 姿态控制系统 SAS | prev_angular_velocity, prev_posture, control_command（δ_elevator/δ_aileron/δ_rudder）, prev_velocity, α, β | angular_accel（角加速度 p̈/q̈/r̈，含限幅保护）                                                         | 各通道限幅值（p̈_max/q̈_max/r̈_max）                             | 控制增益（K_p/K_i/K_d）、时间常数（τ_roll/τ_pitch/τ_yaw）                  | 控制-稳定解耦：将控制指令（含期望航向角）转化为角加速度，含各通道独立限幅保护                        | N      |

- 输出变量：new_position（本时刻位置, Point）、new_posture（本时刻姿态, Posture）、new_velocity（本时刻速度, double）、new_angular_velocity（本时刻角速度, Vector3）、updated_fuel（本时刻燃油量, double）

（表中"是否需要简化"列应当留给人工确认）
（需要在表中把所有流程都列出来，严禁使用省略号）

#### 算法1：推进系统与燃油管理

本算法旨在**根据发动机燃油流量输入和当前飞行状态（速度、高度）计算发动机推力并更新燃油量**，通过**燃油消耗率限制、燃油质量更新和推力查表（Idle/Mil/AB 三层查表 + spool dynamics 转速加减速动特性）**，实现**推力输出和燃油状态的时间推进**。根据补充约束，飞机的非燃油质量在飞行全程保持恒定。

> **AFSIM 参考**：
> - **推力计算**：喷气发动机推力模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.喷气发动机推力模型），对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md) — 负责三层查表（Idle/Mil/AB）推力计算、spool dynamics 转速动特性、TSFC 燃油消耗率计算、熄火保护。
> - **燃油管理**：推进系统与燃油管理模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.推进系统与燃油管理模型），对应卡片 [flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md) — 负责多油箱燃油分配、油箱间传输协调、CG 位置线性插值、总质量属性汇总。

1. 简化方案1：将**喷气发动机三层查表推力模型（Idle/Mil/AB）+ spool dynamics 简化为线性推力-油门关系**。对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)。
   1. 用公式表示为，将 $$T = T_{idle} + \delta_{mil} \cdot (T_{mil} - T_{idle}) + \delta_{ab} \cdot (T_{ab} - T_{mil})$$ 简化为 $$T = \delta_{throttle} \times T_{max}(h)$$，其中 $\delta_{throttle}$ 表示油门位置（0~1），$T_{max}(h)$ 表示当前高度的最大推力。
   2. 简化后涉及变量：油门位置（δ_throttle）、最大推力曲线（T_max(h)）
   3. 简化后涉及常量：最大推力（T_max_sea_level）
   4. 需要补充的参数：T_max(h) 曲线（或标量值：海平面最大推力）
- [x] 选择此方案

1. 简化方案2：将**TSFC 三段增量式燃油消耗计算简化为恒定燃油消耗率**。对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)（燃油公式部分）。
   1. 用公式表示为，将 $$m_{fuel} = (T_{idle} \cdot SFC_{idle} + \delta_{mil} \cdot \Delta T_{mil} \cdot SFC_{mil}^{eff} + \delta_{ab} \cdot \Delta T_{ab} \cdot SFC_{ab}^{eff}) \cdot \Delta t$$ 简化为 $$m_{fuel} = \dot{m}_{const} \cdot \Delta t$$，其中 $\dot{m}_{const}$ 表示用户配置的恒定燃油质量流量。
   2. 简化后涉及变量：恒定燃油流量（fuel_flow_rate_const, double）
   3. 简化后涉及常量：恒定燃油消耗率（Fuel_Const_Rate）
   4. 需要补充的参数：恒定燃油流量标量值
- [x] 选择此方案

1. 简化方案3：将**多油箱燃油管理（油箱传输协调 + CG 插值 + 质量汇总）简化为单油箱模型**。对应卡片 [flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md)。
   1. 用公式表示为，跳过 `PropulsionSystem::Update()` 中的传输分组/比例协调逻辑，燃油直接从唯一油箱消耗：$$m_{fuel}(t+\Delta t) = m_{fuel}(t) - m_{burn}$$，CG 固定在油箱中心。
   2. 简化后涉及变量：单油箱当前油量（current_fuel, double）
   3. 简化后涉及常量：油箱最大容量（Max_Fuel_Capacity）、初始油量（Initial_Fuel）
   4. 需要补充的参数：油箱最大容量、初始油量
- [x] 选择此方案

**修改要求**（人工提问与解答）：  

> **Q1**：三层查表推力模型对应的是 propulsion-fuel-card 吗？还是线性推力-油门关系对应的是该卡片？

**A1**：两者对应不同的卡片。三层查表推力模型（Idle/Mil/AB）来自 `flight-dynamics-jet-engine-card.md`（喷气发动机推力模型），该卡片定义了推力计算公式和 spool dynamics。`flight-dynamics-propulsion-fuel-card.md`（推进系统与燃油管理模型）负责的是油箱层面的燃油分配管理（多油箱传输、CG 插值、质量汇总），不定义推力本身。原简化方案描述已按此修正，现在每个简化方案明确标注了对应的算法卡片。

> **Q2**：燃油消耗计算对应的是哪张卡片？卡片里使用的是恒定燃油消耗率吗？

**A2**：燃油消耗计算（TSFC 公式）来自 `flight-dynamics-jet-engine-card.md`。卡片中使用的是**三段增量式燃油消耗率**，即 Idle / Mil / AB 三种工况各有独立的 TSFC 值（lb/lb/hr），最终燃油消耗 = Idle推力×SFC_idle + Mil增量×有效SFC_mil + AB增量×有效SFC_AB。**不是恒定燃油消耗率**。恒定燃油消耗率是本规范中的简化方案 2。

> **Q3**：目前提供的参数能支持不简化的推进系统与燃油管理运行吗？

**A3**：**不能**。当前需求文档提供的参数（燃油流量 fuel_flow_rate、上一时刻燃油量 prev_fuel、耗油量 fuel_consumption_rate）不足以支持完整模型运行。

> **Q4**：如果不能支持，那还差哪些参数？

**A4**：缺少以下参数（按卡片分类）：

| 缺失参数                                  | 所属卡片                 | 用途                   |
| ------------------------------------- | -------------------- | -------------------- |
| Idle/Mil/AB 推力表（T_Table，3~9 张曲线/2D表）  | jet-engine-card      | 三层查表推力计算             |
| TSFC 值（Idle/Mil/AB 三个 lb/lb/hr 值）     | jet-engine-card      | 燃油消耗率计算              |
| 额定推力值（Rated Idle/Mil/AB，3 个 lb 值）     | jet-engine-card      | 有效 TSFC 标定           |
| Spin-up/down 速率（Mil+AB 共 4 个 /s 值或曲线） | jet-engine-card      | Spool dynamics 转速动特性 |
| 油门位置（δ_throttle）                      | 需求输入                 | 当前不在输入变量列表中          |
| 油箱最大容量（Max_Fuel_Capacity, lb）         | propulsion-fuel-card | 油箱满度限制               |
| 油箱供给速率上限（MaxFlowRate_pps, lb/s）       | propulsion-fuel-card | 供油速率限制               |
| 空/满 CG 位置（EmptyCg/FULLCg, ft 矢量）      | propulsion-fuel-card | 燃油质心线性插值             |

> **Q5**：在缺少这些参数的情况下，有哪些简化方案呢？

**A5**：已新增**简化方案 3**（单油箱模型），与方案 1（线性推力）+ 方案 2（恒定燃油率）组合，形成三个层级的简化路径：

| 层级  | 推力计算                | 燃油消耗     | 油箱管理   | 需补充参数最少                             |
| --- | ------------------- | -------- | ------ | ----------------------------------- |
| 最简  | 简1：线性推力-油门          | 简2：恒定燃油率 | 简3：单油箱 | 仅需 T_max、恒定流量、最大容量                  |
| 中等  | 简1：线性推力-油门          | 简2：恒定燃油率 | 完整多油箱  | 需完整油箱参数                             |
| 完整  | 三层查表+spool dynamics | 三段 TSFC  | 完整多油箱  | 需全部 jet-engine + fuel-tank 参数（见 Q4） |

> **Q6**：如果参数支持，不需要简化。

**A6**：当前参数不支持完整模型。**建议**：若人工能提供 Q4 所列的全部参数，可将流程表中的"是否需要简化"改为 N（不简化）；否则建议选择 Q5 中的"最简"或"中等"层级组合。

______________________________________________  

#### 算法2：气动模型

本算法旨在**根据飞机当前飞行状态（马赫数、攻角、侧滑角、角速率）计算气动六分量（升力、阻力、侧力、滚转力矩、俯仰力矩、偏航力矩）**，通过**RigidBody 稳定性导数气动系数模型——高维查表（Ma×α×β×p×q×r 6维插值）、静态 3D 表项与动态阻尼增量线性叠加、动压×参考面积×参考长度缩放**，实现**有量纲六分量气动力和气动力矩的计算**。

> **AFSIM 参考**：RigidBody 稳定性导数气动系数模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.RigidBody 稳定性导数气动系数模型），对应卡片 [flight-dynamics-rigidbody-aero-coefficient-card.md](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md)；PointMass 气动力与旋转限幅模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 气动力与旋转限幅模型），对应卡片 [flight-dynamics-pointmass-aero-card.md](../../algorithms/flight-dynamics-pointmass-aero-card.md)

1. 简化方案1：将**RigidBody 稳定性导数高维查表模型简化为固定气动系数模型**。算法复杂度从 O(稳定性导数查表×6分量×(Ma×α×β×p×q×r 6维插值)) 降至 O(1)。
   1. 用公式表示为，将 $$C_i = C_i(\text{Ma}, \alpha, \beta, p, q, r)$$ 简化为 $$C_i = \text{const}$$，其中 $C_i$ 表示各气动系数（C_L, C_D, C_Y, C_l, C_m, C_n）。
   2. 简化后涉及变量：固定升力系数（C_L_const）、固定阻力系数（C_D_const）等 6 个固定系数
   3. 简化后涉及常量：各组固定气动系数常量值
- [ ] 选择此方案

1. 简化方案2：将**气动力矩计算简化为仅保留气动力（不计算力矩），依赖 SAS 控制角加速度**。算法复杂度从 O(6分量×6维插值) 降至 O(3分量×1维插值)。
   1. 用公式表示为，将完整气动六分量 $$[F_x, F_y, F_z, M_x, M_y, M_z]^T$$ 简化为仅气动力 $$[F_x, F_y, F_z]^T$$，力矩全部由 SAS 系统提供。
   2. 简化后涉及变量：气动力矢量（F_aero）
   3. 简化后涉及常量：无
- [x] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法3：六自由度积分器

本算法旨在**对飞机进行六自由度时间推进**，通过**Heun 预测-校正法（二阶 Runge-Kutta）+ 四元数姿态积分 + 欧拉转动方程（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz）**，实现**从合力和合力矩到下一时刻飞行状态（位置、速度、姿态四元数、角速度）的数值积分**。根据补充约束，质量（m）和转动惯量张量（I）在飞行全程为常量（仅燃油质量随时间衰减）。

> **AFSIM 参考**：刚体六自由度 Heun 预测-校正积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.刚体六自由度积分器），对应卡片 [flight-dynamics-rigid-body-integrator-card.md](../../algorithms/flight-dynamics-rigid-body-integrator-card.md)；PointMass 六自由度 Heun 积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 六自由度 Heun 积分器），对应卡片 [flight-dynamics-pointmass-integrator-card.md](../../algorithms/flight-dynamics-pointmass-integrator-card.md)

1. 简化方案1：将**刚体六自由度积分器（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz 和欧拉转动方程）简化为 PointMass 点质积分器（忽略转动惯量耦合，使用半隐式欧拉法旋转积分）**。算法复杂度从 O(转动惯量矩阵求逆 + 交叉耦合项) 降至 O(对角项独立积分)。
   1. 用公式表示为，将刚体转动方程 $$I\dot{\boldsymbol{\omega}} + \boldsymbol{\omega} \times (I\boldsymbol{\omega}) = \mathbf{M}_{\text{total}}$$ 简化为点质旋转方程 $$\dot{p} = M_x, \dot{q} = M_y, \dot{r} = M_z$$（单位转动惯量），其中 $\boldsymbol{\omega} = [p, q, r]^T$ 表示角速度矢量。
   2. 简化后涉及变量：角速度（p, q, r）、合外力矩（M_x, M_y, M_z）
   3. 简化后涉及常量：无需转动惯量矩阵
- [ ] 选择此方案

1. 简化方案2：将**Heun 预测-校正法（二阶 RK）简化为显式欧拉法（一阶）**。算法复杂度从 O(2次函数评估/步) 降至 O(1次函数评估/步)，但精度从 O(Δt²) 降至 O(Δt)。
   1. 用公式表示为，将 Heun 法 $$\begin{cases} \mathbf{y}^* = \mathbf{y}_n + \Delta t \cdot f(t_n, \mathbf{y}_n) \\ \mathbf{y}_{n+1} = \mathbf{y}_n + \frac{\Delta t}{2}[f(t_n, \mathbf{y}_n) + f(t_{n+1}, \mathbf{y}^*)] \end{cases}$$ 简化为显式欧拉法 $$\mathbf{y}_{n+1} = \mathbf{y}_n + \Delta t \cdot f(t_n, \mathbf{y}_n)$$。
   2. 简化后涉及变量：状态矢量（y）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法4：姿态控制系统 SAS

本算法旨在**为飞机提供旋转角加速度控制**，通过**控制-稳定解耦架构（一阶指令跟踪 + 二阶临界阻尼稳定项 + 独立通道限幅）**，实现**从控制指令（升降舵/副翼/方向舵偏转，含期望航向角）到角加速度的安全转化，防止大迎角操纵效能丧失**。

> **AFSIM 参考**：PointMass 稳定增稳系统 SAS（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 稳定增稳系统），对应卡片 [flight-dynamics-pointmass-sas-card.md](../../algorithms/flight-dynamics-pointmass-sas-card.md)

1. 简化方案1：将**完整三通道控制-稳定解耦 SAS 简化为仅角加速度限幅**。算法复杂度从 O(3通道×(P控制+I积分+D微分+限幅)) 降至 O(3通道×限幅)。
   1. 用公式表示为，将完整 SAS 控制律 $$\ddot{\theta}_{cmd} = K_p(\theta_{cmd} - \theta) + K_i\int(\theta_{cmd} - \theta)dt + K_d(\dot{\theta}_{cmd} - \dot{\theta})$$ 简化为 $$\ddot{\theta} = \text{clip}(\ddot{\theta}_{cmd}, -\ddot{\theta}_{max}, \ddot{\theta}_{max})$$，其中 $\theta$ 表示姿态角（滚转/俯仰/偏航）。
   2. 简化后涉及变量：控制指令角加速度（p̈_cmd, q̈_cmd, r̈_cmd）、角加速度限幅值（p̈_max, q̈_max, r̈_max）
   3. 简化后涉及常量：各通道角加速度最大限幅值
- [ ] 选择此方案

1. 简化方案2：将**完整 SAS 完全跳过，直接将控制指令角加速度输出给积分器**。算法复杂度从 O(3通道×3项PID) 降至 O(0)（跳过此流程）。
   1. 用公式表示为，将 SAS 环节完全省略，即 $$\ddot{\theta} = \ddot{\theta}_{cmd}$$。
   2. 简化后涉及变量：控制指令角加速度（p̈_cmd, q̈_cmd, r̈_cmd）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  


## 3. REQ-002 → REQ-002-INTEGRATION-03：航线机动集成层

本原需求旨在**将航线管理（REQ-002-PATH-01）和六自由度运动学计算（REQ-002-KINEMATICS-02）集成为一个完整的单机航线机动仿真步长更新**，要求**以仿真步长为推进单位，按顺序调用航路段映射→航线推进→剩余航线裁剪→推进系统→气动模型→积分器→SAS，组织输入数据的分发和输出数据的收集**，实现**飞机沿航线机动的端到端仿真更新**。

> **AFSIM 参考**：AFSIM 中飞机运动由 WsfPlatform 的 Update 循环驱动，Mover 基类负责位置/速度/姿态更新。wsf_six_dof 的 `maneuver/` 子目录实现机动编排。架构文档：docs/architecture/wsf_plugins/afsim-architecture.md §2.1 运动学系统，docs/architecture/core/afsim-architecture.md §6 仿真生命周期。

### 需求实现流程
- 输入变量：path（期望航线, vector\<Point\>）、prev_path（上个步长内路径, vector\<Point\>）、prev_posture（上个步长内姿态, vector\<Posture\>）、prev_velocity（上个步长内速度, vector\<double\>）、prev_fuel（上个步长内油量, vector\<double\>）、Δt（仿真步长, double）、t（当前时间戳, double）、fuel_consumption_rate（耗油量, double）、V_wind（风速, double）、V（飞机速度, double）、V_max（最大速度, double）、地球参数（Earth_Params）

| #   | 流程        | 上流程输入变量                                                                                                 | 输出至下流程变量                                                  | 其他变量 | 其他常量                  | 功能                                               | 是否需要简化 |
| --- | --------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---- | --------------------- | ------------------------------------------------ | ------ |
| ❌   | 1. 航线推进   | path, V, Δt, V_wind, t, Earth_Params                                                                    | ref_pos_next, remaining_path, heading_cmd                 | —    | V_max                 | 调用 REQ-002-PATH-01：航路段映射→航线推进→剩余航线裁剪，获取参考位置和期望航向 | N      |
| ❌   | 2. 六自由度计算 | ref_pos_next, heading_cmd, prev_path, prev_posture, prev_velocity, prev_fuel, Δt, fuel_consumption_rate | new_path, new_posture, new_velocity, new_fuel             | —    | 气动/推力/惯量常量（全部为飞行全程常量） | 调用 REQ-002-KINEMATICS-02：推进系统→气动模型→积分器→SAS，计算新状态 | N      |
| ❌   | 3. 输出组装   | new_path, new_posture, new_velocity, new_fuel, Δt                                                       | output_path, output_posture, output_velocity, output_fuel | —    | 步长阈值（1 s）             | 步长自适应输出：>1s 时输出每秒状态序列；≤1s 时仅输出下一帧状态              | N      |

- 输出变量：remaining_path（剩余航线, vector\<Point\>）、output_path（输出路径, vector\<Point\>）、output_posture（输出姿态, vector\<Posture\>）、output_velocity（输出速度, vector\<double\>）、output_fuel（输出油量, vector\<double\>）

#### 算法1：集成调度

本算法旨在**编排航线机动仿真的完整更新周期**，通过**顺序调用航线推进→六自由度计算→输出组装**，实现**端到端的单机航线机动仿真步长更新**。为纯调度逻辑，无独立算法复杂度。

1. 简化方案1：将**输出组装简化为仅输出下一帧状态**（不进行步长自适应插值）。无论步长大小，始终输出单帧结果。
   1. 用公式表示为，始终输出单帧：`output = new_state`，丢弃步长 > 1s 时的中间帧序列。
   2. 简化后涉及变量：下一帧状态（new_state）
   3. 简化后涉及常量：无
- [ ] 选择此方案

1. 简化方案2：**跳过航线完整性检查**（不验证飞机是否偏离航线超过容忍阈值）。
   1. 不进行航线偏离检测和越界判断，假定飞机始终在航线容忍范围内飞行。
   2. 简化后涉及变量：无新增
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  


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
[11]: docs/architecture/wsf_plugins/afsim-architecture.md "AFSIM 插件架构报告（含 wsf_six_dof 编队/机动子系统）"