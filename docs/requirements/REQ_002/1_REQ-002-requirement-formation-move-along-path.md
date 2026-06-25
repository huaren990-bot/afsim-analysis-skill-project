# 编队沿航线机动设计需求规范文档

> **模糊需求文档**：`docs/requirements/REQ_002/0_formation_move_along_path.md`
> **日期**：2026-06-25
> **需求编号**：REQ-002

本规范需求文档中的所有需求均源于 `0_formation_move_along_path.md` 模糊需求文档，原模糊需求文档共提出 **2 组（5 个子需求）**，在本文档规范表述为 **5 个规范需求**（含 1 个集成需求），对应关系如下：

| #   | 原需求              | 对应规范需求                    |
| --- | ---------------- | ------------------------- |
| 1   | REQ-002（编队沿航线机动） | REQ-002-FORMATION-01      |
| 2   | REQ-002（编队沿航线机动） | REQ-002-FORMATION-02      |
| 3   | REQ-002（编队沿航线机动） | REQ-002-FORMATION-03      |
| 4   | REQ-002（编队沿航线机动） | REQ-002-FORMATION-04      |
| 5   | REQ-002（编队沿航线机动） | REQ-002-FORMATION-05（集成层） |

自有系统中未有的需求对应关系如下：

| #   | 原需求     | 对应规范需求               | 自有系统覆盖度 |
| --- | ------- | -------------------- | ------- |
| 1   | REQ-002 | REQ-002-FORMATION-01 | ❌       |
| 2   | REQ-002 | REQ-002-FORMATION-02 | ❌       |
| 3   | REQ-002 | REQ-002-FORMATION-03 | ❌       |
| 4   | REQ-002 | REQ-002-FORMATION-04 | ❌       |
| 5   | REQ-002 | REQ-002-FORMATION-05 | ❌       |

- ✅ 完全满足（功能完全匹配，接口兼容）
- ⚠️ 部分满足（有类似功能但需要修改接口或补充参数）
- ❌ 缺失（无相关实现，但 AFSIM 有参考实现）
- 🆕 缺失（AFSIM无参考）（无相关实现，且 AFSIM 中也无对应功能，需全新设计）
- ❓ 无法判断（索引或描述不足，需人工补充）


---

## 非功能需求

> **说明**：以下非功能需求适用于本文档中的所有规范需求。人工需逐项确认，确认后作为下游设计和实现的约束条件。

### 1. 多线程支持

| 规范需求ID | 是否需要多线程支持 | 依据 | 备注 |
|-----------|------------------|------|------|
| REQ-002-FORMATION-01 | ❌ | 单编队内路径推进为串行逻辑 | 多编队时分派到不同线程 |
| REQ-002-FORMATION-02 | ✅ | 多架飞机独立进行六自由度机动计算 | 每架飞机独立状态，数据并行，天然线程安全 |
| REQ-002-FORMATION-03 | ✅ | 多架飞机独立姿态计算 | 同 REQ-002-FORMATION-02 |
| REQ-002-FORMATION-04 | ✅ | 多架飞机独立燃油计算 | 同 REQ-002-FORMATION-02 |
| REQ-002-FORMATION-05 | ✅ | 集成层负责数据分发与收集 | 含共享输入/输出缓冲区，需最小化锁粒度 |

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
| REQ-002-FORMATION-02 | < 200 μs/架 | < 10 KB/架 | 每仿真步长调用 1 次 | 随编队规模线性扩展 |
| REQ-002-FORMATION-05 | < 100 μs（N架汇总） | < 50 KB（N架缓存） | 每仿真步长调用 1 次 | 汇总步长自适应 |

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


## 1. REQ-002 → REQ-002-FORMATION-01：编队航线推进

本原需求旨在**为飞机编队提供沿期望航线（坐标点数组）前进的航路管理能力**，要求**根据当前编队位置和期望航线，通过航线跟踪和航路段切换逻辑，推进编队沿航线运动**，实现**编队参考点随时间的航线轨迹更新，并输出剩余未到达的期望航点**。

> **AFSIM 参考**：wsf_p6dof 和 wsf_six_dof 均含 `maneuver/` 子目录（机动动作库）和 `formation/` 子目录（编队动作库）；编队汇合/位置保持/追击三状态机动控制算法（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.编队汇合/位置保持/追击三状态机动控制），对应卡片 [flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md)

### 需求实现流程
- 输入变量：期望航线（path, vector\<Point\>）、当前仿真步长（Δt, double）、编队速度（V_formation, double）、最大速度（V_max, double）、风速（V_wind, double）、当前时间戳（t, double）

| #   | 流程        | 上流程输入变量                                                  | 输出至下流程变量                                      | 其他变量                  | 其他常量                                 | 功能                                 | 是否需要简化 |
| --- | --------- | -------------------------------------------------------- | --------------------------------------------- | --------------------- | ------------------------------------ | ---------------------------------- | ------ |
| ❌   | 1. 航路段映射  | path, Δt, V_formation                                    | current_leg_index, leg_progress（航路段序号和当前段内进度） | 参考点位置（ref_pos, Point） | 航线点数组（path_array）、地球参数（Earth_Params） | 根据当前参考点位置，确定编队所处的航路段；若到达航路点则切换到下一段 | Y      |
| ❌   | 2. 航线推进   | current_leg_index, leg_progress, V_formation, Δt, V_wind | ref_pos_next（下一时刻参考点位置）                       | 航向角（heading, deg）     | 最大速度（V_max）                          | 沿当前航路段以编队速度推进参考点位置，考虑风速影响          | N      |
| ❌   | 3. 剩余航线裁剪 | path, ref_pos_next                                       | remaining_path（剩余期望航线, vector\<Point\>）       | —                     | —                                    | 从原航线中裁剪已飞越的航路点，返回剩余未到达的航点序列        | N      |

- 输出变量：remaining_path（剩余的期望航线, vector\<Point\>）、ref_pos_next（编队参考点下一时刻位置, Point）

（表中"是否需要简化"列应当留给人工确认）
（需要在表中把所有流程都列出来，严禁使用省略号）

#### 算法1：航路段映射

本算法旨在**确定编队参考点在航线中的位置（位于哪个航路段以及段内进度）**，通过**点到线段投影和累积弧长计算**，实现**航路段索引和段内归一化进度的确定**。

> **AFSIM 参考**：wsf_p6dof 和 wsf_six_dof 的 `maneuver/` 子目录中航路管理模块；编队三状态机动控制的 FormUp 阶段（远距离飞向目标）含航路跟踪逻辑

1. 简化方案1：将**点到线段精确投影简化为最近航路点匹配**。算法复杂度从 O(N×投影) 降至 O(N×距离)。
   1. 用公式表示为，将 $$d = \min_{i} \text{dist\_to\_segment}(\mathbf{p}_{\text{ref}}, \mathbf{p}_i, \mathbf{p}_{i+1})$$ 简化为 $$d = \min_{i} \|\mathbf{p}_{\text{ref}} - \mathbf{p}_i\|$$，其中 $\mathbf{p}_{\text{ref}}$ 表示编队参考点，$\mathbf{p}_i$ 表示第 i 个航路点，$\text{dist\_to\_segment}$ 表示点到线段的垂直距离。
   2. 简化后涉及变量：最近航路点索引（i_nearest）
   3. 简化后涉及常量：无
- [ ] 选择此方案

5. 简化方案2：将**逐段搜索简化为仅向前搜索（禁止回退）**。算法复杂度从 O(N) 降至 O(1)（仅检查当前段+下一段）。
   6. 用公式表示为，搜索范围从 $\forall i \in [1, N-1]$ 缩减为 $i \in [\text{current\_leg}, \text{current\_leg}+1]$，已知航线单调前进方向。
   7. 简化后涉及变量：当前段索引（current_leg）
   8. 简化后涉及常量：无
- [x] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法2：航线推进

本算法旨在**沿当前航路段以编队速度推进参考点**，通过**航向矢量计算和风速修正**，实现**编队参考点沿航线的增量位移**。

> **AFSIM 参考**：编队三状态机动控制的 KeepStation 阶段——ECS 坐标系 P+D+DD 偏差精细控制

1. 简化方案1：将**风速修正简化为矢量线性叠加**（忽略阵风和湍流）。算法复杂度保持 O(1)。
   1. 用公式表示为，将 $$\mathbf{v}_{\text{ground}} = \mathbf{v}_{\text{formation}} + \mathbf{v}_{\text{wind}}(t, h)$$ 简化为 $$\mathbf{v}_{\text{ground}} = \mathbf{v}_{\text{formation}} + \mathbf{v}_{\text{wind\_const}}$$，其中 $\mathbf{v}_{\text{wind\_const}}$ 表示恒定风速矢量。
   2. 简化后涉及变量：恒定风速（V_wind_const, double + direction）
   3. 简化后涉及常量：恒定风速矢量（Wind_Vector_Const）
- [ ] 选择此方案

2. 简化方案2：将**弧线航线推进简化为直线航段间折线推进**（不进行弧线拟合）。航线曲率处产生位置跳变。
   1. 用公式表示为，航路段连接处不进行平滑过渡，参考点直接从段 i 的终点跳至段 i+1 的起点。
   2. 简化后涉及变量：航路段端点（p_i, p_{i+1}）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法3：剩余航线裁剪

本算法旨在**从原始航线中移除已飞越的航路点**，通过**航点遍历和进度判断**，实现**返回未完成航线供下游使用**。

1. 简化方案1：无需简化。此算法为基本数组操作。

2. 简化方案2：无需简化。

**修改要求**（若有）：  
______________________________________________  


## 2. REQ-002 → REQ-002-FORMATION-02：编队内各机六自由度机动计算

本原需求旨在**用单架飞机模型替代整个编队进行机动计算**，要求**遍历编队中的每架飞机，以编队参考点位置为基准结合各机在编队中的相对位置偏移，使用六自由度模型（推进系统→气动模型→运动学积分→姿态控制）独立计算每架飞机的姿态、位置和剩余油量**，实现**编队内所有飞机的飞行状态更新**。

> **AFSIM 参考**：wsf_six_dof 模块（849 源文件），含 PointMass（点质）和 RigidBody（刚体）双重模型。核心类：RigidBodySixDOF_Mover、PointMassMover、PointMassPropulsionSystem、RigidBodyAeroCoreObject、PointMassFlightControlSystem。架构文档：docs/architecture/wsf_plugins/afsim-architecture.md §2.1.2；算法卡片：docs/algorithms/CompendiumofAlgorithms.md §一（飞行动力学）

### 需求实现流程

编队中各机六自由度机动计算分两阶段：(A) 编队级——将编队参考点分解为各机目标位置；(B) 单机级——每架飞机独立执行推进→气动→积分→姿态控制的四步管线。

#### 阶段 A：编队目标位置

- 输入变量：ref_pos（编队参考点位置, Point）、formation_offset_i（各机编队偏移量, vector\<Point\>）、编队航向角（ψ_formation, double）

| #   | 流程         | 上流程输入变量                                  | 输出至下流程变量                              | 其他变量 | 其他常量                    | 功能                            | 是否需要简化 |
| --- | ---------- | ---------------------------------------- | ------------------------------------- | ---- | ----------------------- | ----------------------------- | ------ |
| ❌   | A1. 目标位置计算 | ref_pos, formation_offset_i, ψ_formation | target_pos_i（各机目标位置, vector\<Point\>） | —    | 编队队形参数（Formation_Shape） | 根据编队参考点位置和各机编队偏移量，计算每架飞机的目标位置 | Y      |

#### 阶段 B：单机六自由度（逐机执行）

- 输入变量（每架飞机）：target_pos_i（目标位置, Point）、prev_position_i（上一时刻位置, Point）、prev_posture_i（上一时刻姿态, Posture）、prev_velocity_i（上一时刻速度, double）、prev_fuel_i（上一时刻油量, double）、Δt（仿真步长, double）、fuel_flow_rate（发动机燃油流量, double）、V_wind（风速, double）

| #   | 流程             | 上流程输入变量                                                                                                                  | 输出至下流程变量                                                              | 其他变量                                               | 其他常量                                                          | 功能                                                             | 是否需要简化 |
| --- | -------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------- | ------ |
| ❌   | B1. 推进系统与燃油管理  | Δt, fuel_flow_rate, prev_fuel_i, prev_velocity_i, prev_position_i.alt                                                    | F_thrust_i（推力）, updated_fuel_i（本时刻燃油量）                                | 油门位置（δ_throttle）、发动机转速（N_spool）                    | 发动机推力表（T_Table）、燃油消耗率表（TSFC_Table）、油箱容量（Fuel_Capacity）        | 根据油门和飞行状态查表计算发动机推力，并更新燃油消耗量                                    | N      |
| ❌   | B2. 气动模型       | prev_velocity_i, prev_position_i.alt, prev_posture_i（roll/pitch/yaw）, p_i, q_i, r_i                                      | F_aero_i（气动合力矢量）, M_aero_i（气动合力矩矢量）                                   | 马赫数（Ma）、攻角（α）、侧滑角（β）、动压（q̄）                        | 参考面积（S_ref）、参考长度（l_ref）、稳定性导数表（C_L/C_D/C_Y/C_l/C_m/C_n Table） | 根据飞行状态计算气动六分量（升力/阻力/侧力/滚转力矩/俯仰力矩/偏航力矩）                         | Y/N    |
| ❌   | B3. 六自由度积分器    | F_thrust_i, F_aero_i, M_aero_i, prev_position_i, prev_posture_i, prev_velocity_i, Δt                                     | new_position_i, new_posture_i, new_velocity_i, new_angular_velocity_i | 四元数（q₀,q₁,q₂,q₃）、质量（m_i）、转动惯量（I_xx/I_yy/I_zz/I_xz） | 重力加速度（g=9.80665）、质量（m）、转动惯量张量（I）                              | 使用 Heun 预测-校正法进行六自由度时间推进：将合力和合力矩转化为线加速度和角加速度，积分得到速度、位置、角速度和姿态角 | Y/N    |
| ❌   | B4. 姿态控制系统 SAS | prev_angular_velocity_i, prev_posture_i（角度）, control_command_i（δ_elevator/δ_aileron/δ_rudder）, prev_velocity_i, α_i, β_i | angular_accel_i（角加速度 p̈/q̈/r̈，含限幅保护）                                  | 各通道限幅值（p̈_max/q̈_max/r̈_max）                       | 控制增益（K_p/K_i/K_d）、时间常数（τ_roll/τ_pitch/τ_yaw）                  | 控制-稳定解耦：将控制指令转化为角加速度，含各通道独立限幅保护                                | Y/N    |

- 输出变量（每架飞机）：new_position_i（下一时刻位置, Point）、new_posture_i（下一时刻姿态, Posture）、new_velocity_i（下一时刻速度, double）、new_fuel_i（下一时刻油量, double）

---

### 阶段 A 详细算法

#### 算法 A1：目标位置计算

本算法旨在**将编队参考点位置根据各机编队偏移量分解为各机目标位置**，通过**ECS（编队坐标系）偏移量变换**，实现**每架飞机在地理坐标系中的绝对目标位置计算**。

> **AFSIM 参考**：编队三状态机动控制的 KeepStation 阶段——在 ECS（Earth-Centered, Station-keeping）坐标系中定义各机期望相对位置，含独立的三轴（纵向/横向/垂直）偏差控制。算法卡片：[flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md)

1. 简化方案1：将**ECS 坐标系偏移变换简化为航向角旋转+平移**（忽略地球曲率）。算法复杂度从 O(地理坐标转换) 降至 O(1)。
   1. 用公式表示为，将 ECS 坐标系中的编队偏移映射到地理坐标系：$$\mathbf{p}_{\text{target}}^{(i)} = \mathbf{p}_{\text{ref}} + R(\psi) \cdot \Delta\mathbf{p}_{\text{formation}}^{(i)}$$，其中 $R(\psi)$ 表示航向角旋转矩阵，$\Delta\mathbf{p}_{\text{formation}}^{(i)}$ 表示第 i 架飞机的编队偏移量。
   2. 简化后涉及变量：编队参考点位置（ref_pos）、航向角（ψ）、编队偏移量（formation_offset_i）
   3. 简化后涉及常量：编队队形参数（Formation_Shape）
- [ ] 选择此方案

2. 简化方案2：将**编队队形简化为固定队形（不随航向旋转）**。编队偏移量在世界坐标系中固定。
   1. 用公式表示为，固定偏移量：$$\mathbf{p}_{\text{target}}^{(i)} = \mathbf{p}_{\text{ref}} + \Delta\mathbf{p}_{\text{fixed}}^{(i)}$$，不乘旋转矩阵。
   2. 简化后涉及变量：编队参考点位置（ref_pos）、固定偏移量（fixed_offset_i）
   3. 简化后涉及常量：固定编队偏移量数组
- [x] 选择此方案

**修改要求**（若有）：  
______________________________________________  

---

### 阶段 B 详细算法

#### 算法 B1：推进系统与燃油管理

本算法旨在**根据发动机燃油流量输入和当前飞行状态（速度、高度）计算发动机推力并更新燃油量**，通过**燃油消耗率限制、燃油质量更新和推力查表（Idle/Mil/AB 三层查表 + spool dynamics 转速加减速动特性）**，实现**推力输出和燃油状态的时间推进**。

> **AFSIM 参考**：推进系统与燃油管理模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.推进系统与燃油管理模型），对应卡片 [flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md)；喷气发动机推力模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.喷气发动机推力模型），对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)

1. 简化方案1：将**喷气发动机三层查表推力模型（Idle/Mil/AB）简化为线性推力-油门关系**。算法复杂度从 O(查表×3 表×4 spin rate) 降至 O(1)。
   1. 用公式表示为，将 $$F_{\text{thrust}} = f_{\text{table}}(N_{\text{spool}}, \text{Ma}, h)$$ 简化为 $$F_{\text{thrust}} = \delta_{\text{throttle}} \times F_{\text{max}}(h)$$，其中 $\delta_{\text{throttle}}$ 表示油门位置（0~1），$F_{\text{max}}(h)$ 表示当前高度的最大推力。
   2. 简化后涉及变量：油门位置（δ_throttle）、最大推力曲线（F_max(h)）
   3. 简化后涉及常量：最大推力（F_max_sea_level）
- [ ] 选择此方案

2. 简化方案2：将**燃油消耗计算简化为恒定燃油消耗率**。算法复杂度从 O(TSFC 多维查表 + spool dynamics) 降至 O(1)。
   1. 用公式表示为，将 $$\dot{m}_{\text{fuel}} = f_{\text{TSFC}}(F_{\text{thrust}}, \text{Ma}, h)$$ 简化为 $$\dot{m}_{\text{fuel}} = \text{const}$$，其中 $\dot{m}_{\text{fuel}}$ 表示燃油质量流量，const 表示用户配置的恒定燃油消耗率。
   2. 简化后涉及变量：恒定燃油流量（ṁ_fuel_const）
   3. 简化后涉及常量：恒定燃油消耗率（Fuel_Const_Rate）
- [ ] 选择此方案

**修改要求**（若有）： 喷气发动机三层查表推力模型（Idle/Mil/AB）算法参考的是喷气发动机推力模型对应的算法卡片吗？TSFC多维查表对应的是推进系统与燃油管理模型对应的算法卡片吗？
______________________________________________  

#### 算法 B2：气动模型

本算法旨在**根据无人机当前飞行状态（马赫数、攻角、侧滑角、角速率）计算气动六分量（升力、阻力、侧力、滚转力矩、俯仰力矩、偏航力矩）**，通过**RigidBody 稳定性导数气动系数模型——高维查表（Ma×α×β×p×q×r 6维插值）、静态 3D 表项与动态阻尼增量线性叠加、动压×参考面积×参考长度缩放**，实现**有量纲六分量气动力和气动力矩的计算**。

> **AFSIM 参考**：RigidBody 稳定性导数气动系数模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.RigidBody 稳定性导数气动系数模型），对应卡片 [flight-dynamics-rigidbody-aero-coefficient-card.md](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md)；PointMass 气动力与旋转限幅模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 气动力与旋转限幅模型），对应卡片 [flight-dynamics-pointmass-aero-card.md](../../algorithms/flight-dynamics-pointmass-aero-card.md)

1. 简化方案1：将**RigidBody 稳定性导数高维查表模型简化为固定气动系数模型**。算法复杂度从 O(稳定性导数查表×6分量×(Ma×α×β×p×q×r 6维插值)) 降至 O(1)。
   2. 用公式表示为，将 $$C_i = C_i(\text{Ma}, \alpha, \beta, p, q, r)$$ 简化为 $$C_i = \text{const}$$，其中 $C_i$ 表示各气动系数$（C_L, C_D, C_Y, C_l, C_m, C_n）$，各自简化为固定常数值。
   3. 简化后涉及变量：固定升力系数（C_L_const）、固定阻力系数（C_D_const）、固定侧力系数（C_Y_const）、固定滚转力矩系数（C_l_const）、固定俯仰力矩系数（C_m_const）、固定偏航力矩系数（C_n_const）
   4. 简化后涉及常量：各组固定气动系数常量值
- [ ] 选择此方案

2. 简化方案2：将**气动力矩计算简化为仅保留气动力（不计算力矩），依赖 SAS 控制角加速度**。算法复杂度从 O(6分量×6维插值) 降至 O(3分量×1维插值)。
   1. 用公式表示为，将完整气动六分量 $$[F_x, F_y, F_z, M_x, M_y, M_z]^T$$ 简化为仅气动力 $$[F_x, F_y, F_z]^T$$，力矩全部由 SAS 系统提供。
   2. 简化后涉及变量：气动力矢量（$F_aero$）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法 B3：六自由度积分器

本算法旨在**对无人机进行六自由度时间推进**，通过**Heun 预测-校正法（二阶 Runge-Kutta）+ 四元数姿态积分 + 欧拉转动方程（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz）**，实现**从合力和合力矩到下一时刻飞行状态（位置、速度、姿态四元数、角速度）的数值积分**。

> **AFSIM 参考**：刚体六自由度 Heun 预测-校正积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.刚体六自由度积分器），对应卡片 [flight-dynamics-rigid-body-integrator-card.md](../../algorithms/flight-dynamics-rigid-body-integrator-card.md)；PointMass 六自由度 Heun 积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 六自由度 Heun 积分器），对应卡片 [flight-dynamics-pointmass-integrator-card.md](../../algorithms/flight-dynamics-pointmass-integrator-card.md)

1. 简化方案1：将**刚体六自由度积分器（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz 和欧拉转动方程）简化为 PointMass 点质积分器（忽略转动惯量耦合，使用半隐式欧拉法旋转积分）**。算法复杂度从 O(转动惯量矩阵求逆 + 交叉耦合项) 降至 O(对角项独立积分)。
   1. 用公式表示为，将刚体转动方程 $$I\dot{\boldsymbol{\omega}} + \boldsymbol{\omega} \times (I\boldsymbol{\omega}) = \mathbf{M}_{\text{total}}$$ 简化为点质旋转方程 $$\dot{p} = M_x, \dot{q} = M_y, \dot{r} = M_z$$（单位转动惯量），其中 $\boldsymbol{\omega} = [p, q, r]^T$ 表示角速度矢量，$I$ 表示转动惯量张量，$\mathbf{M}_{\text{total}}$ 表示合外力矩。
   2. 简化后涉及变量：角速度（p, q, r）、合外力矩（M_x, M_y, M_z）
   3. 简化后涉及常量：无需转动惯量矩阵
- [ ] 选择此方案

2. 简化方案2：将**Heun 预测-校正法（二阶 RK）简化为显式欧拉法（一阶）**。算法复杂度从 O(2次函数评估/步) 降至 O(1次函数评估/步)，但精度从 O(Δt²) 降至 O(Δt)。
   1. 用公式表示为，将 Heun 法 $$\begin{cases} \mathbf{y}^* = \mathbf{y}_n + \Delta t \cdot f(t_n, \mathbf{y}_n) \\ \mathbf{y}_{n+1} = \mathbf{y}_n + \frac{\Delta t}{2}[f(t_n, \mathbf{y}_n) + f(t_{n+1}, \mathbf{y}^*)] \end{cases}$$ 简化为显式欧拉法 $$\mathbf{y}_{n+1} = \mathbf{y}_n + \Delta t \cdot f(t_n, \mathbf{y}_n)$$，其中 $\mathbf{y}$ 表示状态矢量（位置、速度、姿态四元数、角速度）。
   2. 简化后涉及变量：状态矢量（y）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法 B4：姿态控制系统 SAS

本算法旨在**为无人机提供旋转角加速度控制**，通过**控制-稳定解耦架构（一阶指令跟踪 + 二阶临界阻尼稳定项 + 独立通道限幅）**，实现**从控制指令（升降舵/副翼/方向舵偏转）到角加速度的安全转化，防止大迎角操纵效能丧失**。

> **AFSIM 参考**：PointMass 稳定增稳系统 SAS（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 稳定增稳系统），对应卡片 [flight-dynamics-pointmass-sas-card.md](../../algorithms/flight-dynamics-pointmass-sas-card.md)

1. 简化方案1：将**完整三通道控制-稳定解耦 SAS 简化为仅角加速度限幅**。算法复杂度从 O(3通道×(P控制+I积分+D微分+限幅)) 降至 O(3通道×限幅)。
   1. 用公式表示为，将完整 SAS 控制律 $$\ddot{\theta}_{cmd} = K_p(\theta_{cmd} - \theta) + K_i\int(\theta_{cmd} - \theta)dt + K_d(\dot{\theta}_{cmd} - \dot{\theta})$$ 简化为 $$\ddot{\theta} = \text{clip}(\ddot{\theta}_{cmd}, -\ddot{\theta}_{max}, \ddot{\theta}_{max})$$，其中 $\theta$ 表示姿态角（滚转/俯仰/偏航），$\ddot{\theta}_{cmd}$ 表示控制指令角加速度，$\ddot{\theta}_{max}$ 表示角加速度限幅。
   2. 简化后涉及变量：控制指令角加速度（p̈_cmd, q̈_cmd, r̈_cmd）、角加速度限幅值（p̈_max, q̈_max, r̈_max）
   3. 简化后涉及常量：各通道角加速度最大限幅值
- [ ] 选择此方案

2. 简化方案2：将**完整 SAS 完全跳过，直接将控制指令角加速度输出给积分器**。算法复杂度从 O(3通道×3项PID) 降至 O(0)（跳过此流程）。
   1. 用公式表示为，将 SAS 环节完全省略，即 $$\ddot{\theta} = \ddot{\theta}_{cmd}$$，不做任何滤波、限幅或稳定化处理。
   2. 简化后涉及变量：控制指令角加速度（p̈_cmd, q̈_cmd, r̈_cmd）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  

### 编队特有简化方案

1. 简化方案1：将**编队内所有飞机使用同一套飞行参数**（质量、惯量、气动系数均相同）。不同飞机的差异仅体现在编队偏移量上。
   1. 用公式表示为，编队内 $\forall i: m_i = m_{\text{common}}, I_i = I_{\text{common}}, C_{L,i} = C_{L,\text{common}}$。
   2. 简化后涉及变量：统一质量（m_common）、统一惯量（I_common）、统一气动系数（C_common）
   3. 简化后涉及常量：无
- [ ] 选择此方案

2. 简化方案2：将**尾流干扰效应忽略**（各机气动计算独立，不考虑前方飞机尾流对后机的影响）。
   1. 用公式表示为，前排飞机的诱导速度场不对后排飞机的气动计算产生影响：$\mathbf{F}_{\text{aero}}^{(i)} = \mathbf{F}_{\text{aero}}(\text{state}^{(i)})$，不涉及编队相对位置的诱导修正。
   2. 简化后涉及变量：无新增
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  


## 3. REQ-002 → REQ-002-FORMATION-03：编队姿态合成

本原需求旨在**汇总编队中各机的姿态信息**，要求**将逐机计算得到的每架飞机姿态（航向角/俯仰角/翻滚角）按编队顺序打包**，实现**编队整体姿态数组的输出**。

> **AFSIM 参考**：本需求为数据汇总操作，无独立 AFSIM 算法对应。AFSIM 中编队姿态由各平台 Mover 在每帧 Update 时独立更新，汇总由观察者（Observer）或事件管道（EventPipe）完成。

### 需求实现流程
- 输入变量：new_posture_i（各机姿态, vector\<Posture\>）、Δt（仿真步长, double）

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 其他变量 | 其他常量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|---------|---------|------|-------------|
| ❌ | 1. 姿态汇总 | new_posture_i | formation_posture（编队姿态数组） | — | — | 将逐机姿态按编队顺序打包为数组 | Y/N |
| ❌ | 2. 步长自适应输出 | formation_posture, Δt | output_posture（最终输出姿态） | — | 步长阈值（1 s） | 步长 > 1s：输出每秒姿态序列；步长 ≤ 1s：输出下一帧姿态 | Y/N |

- 输出变量：formation_posture（编队姿态数组, vector\<Posture\>），当 Δt > 1s 时数组包含每秒姿态序列，当 Δt ≤ 1s 时数组仅含下一帧姿态。

（表中"是否需要简化"列应当留给人工确认）
（需要在表中把所有流程都列出来，严禁使用省略号）

#### 算法1：姿态汇总

本算法旨在**收集编队内所有飞机的姿态数据并打包输出**，通过**数组遍历和字段复制**，实现**编队姿态向量的生成**。无显著算法复杂度，为基本数据搬运操作。无需简化。

**修改要求**（若有）：  
______________________________________________  

#### 算法2：步长自适应输出

本算法旨在**根据仿真步长自适应调整输出粒度**，通过**步长阈值判断和内部插值**，实现**大步长下的中频姿态序列输出和小步长下的单帧输出**。

1. 简化方案1：**仅输出下一帧姿态，不输出中间序列**（无论步长大小）。算法复杂度保持 O(1)。
   1. 用公式表示为，始终输出单帧：`output = new_posture`，丢弃步长 > 1s 时的中间帧序列。
   2. 简化后涉及变量：下一帧姿态（new_posture_i）
   3. 简化后涉及常量：无
- [ ] 选择此方案

2. 简化方案2：**步长 > 1s 时输出线性插值姿态序列**（非物理仿真中间帧）。使用首尾姿态线性插值。
   1. 用公式表示为，中间帧姿态 $$\mathbf{q}(t_k) = \text{slerp}(\mathbf{q}_{\text{prev}}, \mathbf{q}_{\text{new}}, t_k / \Delta t)$$，其中 $\text{slerp}$ 表示四元数球面线性插值。
   2. 简化后涉及变量：上一帧四元数（q_prev）、下一帧四元数（q_new）、中间时刻（t_k）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  


## 4. REQ-002 → REQ-002-FORMATION-04：编队速度与油量汇总

本原需求旨在**汇总编队中各机的速度和油量信息**，要求**将逐机计算得到的速度和油量按编队顺序打包**，实现**编队整体速度和油量数组的输出**。

> **AFSIM 参考**：本需求为数据汇总操作，与 REQ-002-FORMATION-03 同理。AFSIM 中速度和燃油由各平台 Mover 和 Fuel 组件独立维护。

### 需求实现流程
- 输入变量：new_velocity_i（各机速度, vector\<double\>）、new_fuel_i（各机油量, vector\<double\>）、Δt（仿真步长, double）

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 其他变量 | 其他常量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|---------|---------|------|-------------|
| ❌ | 1. 速度汇总 | new_velocity_i | formation_velocity（编队速度数组） | — | — | 将逐机速度按编队顺序打包 | Y/N |
| ❌ | 2. 油量汇总 | new_fuel_i | formation_fuel（编队油量数组） | — | — | 将逐机油量按编队顺序打包 | Y/N |
| ❌ | 3. 步长自适应输出 | formation_velocity, formation_fuel, Δt | output_velocity, output_fuel | — | 步长阈值（1 s） | 步长自适应：>1s 插值序列，≤1s 单帧 | Y/N |

- 输出变量：formation_velocity（编队速度数组, vector\<double\>）、formation_fuel（编队油量数组, vector\<double\>）

（表中"是否需要简化"列应当留给人工确认）
（需要在表中把所有流程都列出来，严禁使用省略号）

#### 算法1-3：速度汇总 / 油量汇总 / 步长自适应

速度汇总和油量汇总为基本数组遍历操作，无算法复杂度。步长自适应输出逻辑与 REQ-002-FORMATION-03 算法2 相同，简化方案同前。

**修改要求**（若有）：  
______________________________________________  


## 5. REQ-002 → REQ-002-FORMATION-05：编队机动集成层

本原需求旨在**将编队航线推进、逐机六自由度机动计算、姿态合成、速度和油量汇总集成为一个完整的编队机动仿真步长更新**，要求**以仿真步长为推进单位，按顺序调用 REQ-002-FORMATION-01 到 04，组织输入数据的分发和输出数据的收集**，实现**编队沿航线机动的端到端仿真更新**。

> **AFSIM 参考**：AFSIM 中编队由 WsfPlatform 的 Update 循环驱动，Mover 基类负责位置/速度/姿态更新。编队中各平台通过事件系统（WsfEventManager）和观察者（Observer）进行协调。wsf_p6dof 和 wsf_six_dof 的 `maneuver/` 子目录实现机动编排，`formation/` 子目录实现编队动作编排。架构文档：docs/architecture/wsf_plugins/afsim-architecture.md §2.1 运动学系统。

### 需求实现流程
- 输入变量：path（期望航线, vector\<Point\>）、prev_path（上个步长编队路径, vector\<Point\>）、prev_posture（上个步长编队姿态, vector\<Posture\>）、prev_velocity（上个步长编队速度, vector\<double\>）、prev_fuel（上个步长编队油量, vector\<double\>）、Δt（仿真步长, double）、t（当前时间戳, double）、fuel_consumption_rate（耗油量, double）、V_wind（风速, double）、V_formation（编队速度, double）、V_max（最大速度, double）、formation_offset（编队偏移量数组, vector\<Point\>）、地球参数（Earth_Params）

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 其他变量 | 其他常量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|---------|---------|------|-------------|
| ❌ | 1. 航线推进 | path, V_formation, Δt, V_wind, t, Earth_Params | ref_pos_next, remaining_path | 编队参考点 | V_max | 调用 REQ-002-FORMATION-01：航路段映射→航线推进→剩余航线裁剪 | Y/N |
| ❌ | 2. 编队分解 + 六自由度 | ref_pos_next, formation_offset, prev_path, prev_posture, prev_velocity, prev_fuel, Δt, fuel_consumption_rate | new_path, new_posture, new_velocity, new_fuel | — | 气动 / 推力 / 惯量常量 | 调用 REQ-002-FORMATION-02：编队分解→逐机推进系统→气动模型→积分器→SAS | Y/N |
| ❌ | 3. 输出合成 | new_posture, new_velocity, new_fuel, Δt | output_posture, output_velocity, output_fuel | — | 步长阈值（1 s） | 调用 REQ-002-FORMATION-03 + 04：汇总姿态/速度/油量，步长自适应输出 | Y/N |

- 输出变量：remaining_path（剩余航线, vector\<Point\>）、output_path（编队路径, vector\<Point\>）、output_posture（编队姿态, vector\<Posture\>）、output_velocity（编队速度, vector\<double\>）、output_fuel（编队油量, vector\<double\>）

（表中"是否需要简化"列应当留给人工确认）
（需要在表中把所有流程都列出来，严禁使用省略号）

#### 算法1：编队集成调度

本算法旨在**编排编队机动仿真的完整更新周期**，通过**顺序调用航线推进→编队分解→单机计算→输出合成**，实现**端到端的编队机动仿真步长更新**。为纯调度逻辑，无独立算法复杂度。

1. 简化方案1：将**顺序调用简化为单线程串行**（不启用多线程并行）。单线程中顺序执行：`for i in 1..N: six_dof_update(plane[i])`，而非 `parallel_for i in 1..N: six_dof_update(plane[i])`。
   1. 简化后涉及变量：无新增
   2. 简化后涉及常量：无
- [ ] 选择此方案

2. 简化方案2：**跳过编队协调一致性检查**（不验证各机位置是否符合编队队形约束）。
   1. 用公式表示为，不对输出的各机相对位置进行队形检验，忽略编队位置协调。
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