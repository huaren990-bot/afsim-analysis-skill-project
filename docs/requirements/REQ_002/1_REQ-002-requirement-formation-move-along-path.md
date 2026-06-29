# 延航线机动设计需求规范文档

> **模糊需求文档**：[`0_formation_move_along_path.md`](0_formation_move_along_path.md)
> **日期**：2026-06-27
> **需求编号**：REQ-002

本规范需求文档中的所有需求均源于 [`0_formation_move_along_path.md`](0_formation_move_along_path.md) 模糊需求文档，原模糊需求文档共提出需求 **2 个（共 3 个细化需求）**，在本文档规范表述为 **3 个规范需求**（含 1 个集成需求），对应关系如下：

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

| 规范需求ID                 | 是否需要多线程支持 | 依据                        | 备注                    |
| ---------------------- | --------- | ------------------------- | --------------------- |
| REQ-002-PATH-01        | ❌         | 单机路径推进为串行逻辑，单次调用 O(1~N)   | 多机并行时各自持有独立航线副本即可     |
| REQ-002-KINEMATICS-02  | ✅         | 多架飞机独立进行六自由度机动计算，每架飞机状态独立 | 数据并行，天然线程安全，每实体独立状态副本 |
| REQ-002-INTEGRATION-03 | ✅         | 集成层负责数据分发与收集，含步长自适应输出     | 输出缓冲区需线程安全容器或最小锁粒度    |

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
| REQ-002-KINEMATICS-02 | < 200 μs/架 | < 10 KB/架 | 每仿真步长调用 1 次 | 管线内 5 个算法子流程串联 |
| REQ-002-INTEGRATION-03 | < 300 μs（含路径+六自由度+步长自适应） | < 20 KB | 每仿真步长调用 1 次 | 汇总步长自适应 |

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

本原需求旨在**为无人机/飞机提供沿预设期望航线（坐标点数组）自主飞行的航路管理能力**，要求**根据飞机的当前位置和期望航线，通过航路段映射、航线推进（含风速修正）和剩余航线裁剪三步，驱动飞机沿航线运动**，实现**飞机参考点随时间的航线轨迹更新，输出剩余未到达的期望航点和期望航向角**。

> **AFSIM 参考**：编队汇合/位置保持/追击三状态机动控制算法（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.编队汇合/位置保持/追击三状态机动控制），完整卡片 [flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md) 已逐卡阅读。该卡片实现编队飞行中追击者相对于目标点的三状态运动控制——FormUp（从远距离飞向目标位置，使用方位角或 ECS 坐标偏差的 PD 控制律输出滚转角/速度指令）、KeepStation（ECS 坐标系三维位置/速度/加速度 P+D+DD 偏差精细控制）、Pursue（圆形航迹模型追击）。本规范需求为单机航线跟随场景，主要参考 FormUp 阶段的"飞向目标航点"逻辑提取点到线段映射和航线推进。wsf_p6dof 和 wsf_six_dof 均含 `maneuver/` 子目录（机动动作库）和 `formation/` 子目录（编队动作库）。

### 需求实现流程
- 输入变量：期望航线（path, vector\<Point\>）、当前仿真步长（Δt, double）、飞机速度（V, double）、最大速度（V_max, double）、风速（V_wind, double）、当前时间戳（t, double）

| #   | 流程        | 上流程输入变量                                        | 输出至下流程变量                                      | 其他变量                    | 其他常量                                 | 功能                                                    | 是否需要简化 |
| --- | --------- | ---------------------------------------------- | --------------------------------------------- | ----------------------- | ------------------------------------ | ----------------------------------------------------- | ------ |
| ❌   | 1. 航路段映射  | path, Δt, V                                    | current_leg_index, leg_progress（航路段序号和当前段内进度） | 当前位置（cur_pos, Point）    | 航线点数组（path_array）、地球参数（Earth_Params） | 根据飞机当前位置，确定所处的航路段；若到达航路点则切换到下一段                       | Y      |
| ❌   | 2. 航线推进   | current_leg_index, leg_progress, V, Δt, V_wind | ref_pos_next（下一时刻参考点位置）                       | 期望航向角（heading_cmd, deg） | 最大速度（V_max）                          | 沿当前航路段以设定速度推进参考点位置，考虑风速影响，输出期望航向角供下游 Autopilot PID 使用 | N      |
| ❌   | 3. 剩余航线裁剪 | path, ref_pos_next                             | remaining_path（剩余期望航线, vector\<Point\>）       | —                       | —                                    | 从原航线中裁剪已飞越的航路点，返回剩余未到达的航点序列                           | N      |

- 输出变量：remaining_path（剩余的期望航线, vector\<Point\>）、ref_pos_next（飞机参考点下一时刻位置, Point）、heading_cmd（期望航向角, double）、altitude_cmd（期望高度, double）、speed_cmd（期望速度, vector\<double\>）

> **注意**：航线点 Point 结构含 `_lon/_lat/_alt` 三维坐标和 `_alt` 高度信息，因此航线推进除输出 heading_cmd 外，还应输出 altitude_cmd（当前航路段两端高度线性插值）和 speed_cmd（各航路点期望速度），供 Autopilot PID 的垂直通道和速度通道使用。这些输出尚未在原模糊需求中显式定义，由人工在 Autopilot PID 的修改要求中提出补充。



#### 算法1：航路段映射

本算法旨在**确定飞机在航线中的位置（位于哪个航路段以及段内进度）**，通过**点到线段投影和累积弧长计算**，实现**航路段索引和段内归一化进度的确定**。

> **AFSIM 参考**：编队三状态机动控制的 FormUp 阶段使用方位角（bearing angle）或 ECS 坐标偏差驱动飞向目标航点，含航路跟踪逻辑。卡片 [flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md) 已逐卡阅读。

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

本算法旨在**沿当前航路段以设定速度推进参考点**，通过**航向矢量计算和风速修正**，实现**参考点沿航线的增量位移，并输出期望航向角 heading_cmd 供下游自动驾驶仪 PID 使用**。

> **AFSIM 参考**：编队三状态机动控制的 KeepStation 阶段——ECS 坐标系 P+D+DD 偏差精细控制，计算三维位置/速度/加速度偏差。卡片 [flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md) 已逐卡阅读。

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

本原需求旨在**使用六自由度模型计算飞机的姿态、位置和剩余油量**，要求**以仿真步长为推进单位，基于上一时刻的飞行状态（位置、速度、姿态角、角速度）和发动机燃油流量、期望航向角等输入，通过推进系统→气动模型→自动驾驶仪 PID→姿态控制系统 SAS→运动学积分的五步管线**，实现**本时刻飞行状态（位置、速度、姿态角、角速度）及燃油剩余量的精确输出**。

> **AFSIM 参考**：wsf_six_dof 模块（849 源文件），含 PointMass（点质）和 RigidBody（刚体）双重模型。以下为逐卡阅读确认的各算法分工：
> - `flight-dynamics-jet-engine-card.md`：喷气发动机推力模型——三层查表（Idle/Mil/AB）+ spool dynamics 转速动特性，输出推力 T 和燃油消耗率（lb/s）。已逐卡阅读。
> - `flight-dynamics-propulsion-fuel-card.md`：推进系统与燃油管理模型——多油箱燃油分配（传输协调/比例因子）、CG 位置线性插值、总质量属性汇总。已逐卡阅读。
> - `flight-dynamics-rigidbody-aero-coefficient-card.md`：RigidBody 稳定性导数气动系数模型——高维查表（Ma×α×β×p×q×r 6维插值）、静态 3D 表项与动态阻尼增量叠加、动压缩放，输出气动六分量。已逐卡阅读。
> - `flight-dynamics-pointmass-aero-card.md`：PointMass 气动力与旋转限幅模型——在标准气动力上叠加非配平操纵面效果，输出旋转加速度限幅基准和稳定化频率基准供 SAS 使用。已逐卡阅读。
> - `flight-dynamics-autopilot-pid-card.md`：自动驾驶仪 PID 嵌套回路控制——Bank-To-Turn/Yaw-To-Turn 双模式，20 个 PID 三通道嵌套回路（外侧→中间→内侧），含增益调度、抗积分饱和、前馈偏置。**注意：此卡为 PID 控制的核心——负责航向→舵面指令的制导决策（"往哪飞"）**。已逐卡阅读。
> - `flight-dynamics-pointmass-sas-card.md`：PointMass 稳定增稳系统 SAS——**核心算法为控制-稳定解耦架构（一阶指令跟踪 + 二阶临界阻尼稳定项），非 PID 控制。负责舵面指令→角加速度的底层执行与自稳保护（"怎么安全地转向"）**。已逐卡阅读。
> - `flight-dynamics-rigid-body-integrator-card.md`：刚体六自由度 Heun 预测-校正积分器——Heun 二阶 RK + 四元数姿态积分 + 欧拉转动方程（含完整转动惯量张量）。已逐卡阅读。
> 
> **补充约束**：根据模糊需求的补充要求，默认从起飞到降落期间，飞机的物理属性（大小、材质、外观、非燃油质量、转动惯量等）保持不变，六自由度计算中的质量参数（m）和转动惯量张量（I）为常量，仅燃油质量（m_fuel）随时间衰减。

### 需求实现流程
- 输入变量：仿真步长（Δt, double）、当前时间戳（t, double）、飞机上一时刻位置（prev_position, Point）、上一时刻姿态（prev_posture, Posture）、上一时刻速度（prev_velocity, double）、上一时刻角速度（p/q/r, Vector3）、发动机燃油流量（fuel_flow_rate, double）、上一时刻燃油量（prev_fuel, double）、期望航向角（heading_cmd, double，来自 PATH-01）、期望高度（altitude_cmd, double，来自 PATH-01）、期望速度（speed_cmd, vector\<double\>，来自 PATH-01）

| #   | 流程            | 上流程输入变量                                                                                          | 输出至下流程变量                                                      | 其他变量                                                     | 其他常量                                                        | 功能                                                                                                                                                                                                    | 是否需要简化 |
| --- | ------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| ❌   | 1. 推进系统与燃油管理  | Δt, fuel_flow_rate, prev_fuel, prev_velocity, prev_position.alt                                  | F_thrust（推力）, updated_fuel（本时刻燃油量）                            | 油门位置（δ_throttle）、发动机转速（N_spool）                          | 发动机推力表（T_Table, Idle/Mil/AB 三层）、燃油比油耗（TSFC, Idle/Mil/AB 三段） | 根据油门和飞行状态查表计算发动机推力，按 TSFC 公式计算燃油消耗量并更新油量。卡片：[jet-engine-card](../../algorithms/flight-dynamics-jet-engine-card.md) + [propulsion-fuel-card](../../algorithms/flight-dynamics-propulsion-fuel-card.md) | Y      |
| ❌   | 2. 气动模型       | prev_velocity, prev_position.alt, prev_posture, p, q, r                                          | F_aero（气动合力矢量）, M_aero（气动合力矩矢量）                               | 马赫数（Ma）、攻角（α）、侧滑角（β）、动压（q̄ = 0.5·ρ·V²）                   | 参考面积（S_ref）、参考长度（l_ref）、稳定性导数表（C_L/C_D/C_Y/C_l/C_m/C_n）     | 根据飞行状态计算气动六分量（升力/阻力/侧力/滚转力矩/俯仰力矩/偏航力矩）。卡片：[rigidbody-aero-coefficient-card](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md)                                                      | Y      |
| ❌   | 3. 自动驾驶仪 PID  | heading_cmd（期望航向角）, altitude_cmd（期望高度）, speed_cmd（期望速度）, prev_posture, p, q, r, prev_velocity, α, β | control_command（δ_elevator/δ_aileron/δ_rudder）, throttle_cmd（油门指令） | 目标滚转角（cmd_bank）、转弯速率（turn_rate_dps）、目标垂直速率（cmd_vert_spd） | PID 增益表（K_p/K_i/K_d, 以动压为调度变量）、限幅值（max_bank/max_turn_rate） | 将 PATH-01 输出的 heading_cmd/altitude_cmd/speed_cmd 通过 PID 嵌套回路转化为三通道舵面指令 + 油门指令。横向 BTT→aileron，垂直 Altitude→elevator，速度 Speed→throttle | N      |
| ❌   | 4. 姿态控制系统 SAS | control_command（δ）, prev_angular_velocity, prev_posture, prev_velocity, α, β                     | angular_accel（角加速度 p̈/q̈/r̈，含限幅保护）                            | 各通道限幅值（p̈_max/q̈_max/r̈_max）、质量比率（massFraction）          | 基准稳定化频率（ω_n_base）、时间常数（τ_roll/τ_pitch/τ_yaw）                | 控制-稳定解耦：控制项（一阶指令跟踪 ω_cmd→α_controls）+ 稳定项（俯仰/偏航二阶临界阻尼 -α·ω_n²-2·ω_n·α̇，滚转一阶滞后），各通道独立限幅后叠加。卡片：[pointmass-sas-card](../../algorithms/flight-dynamics-pointmass-sas-card.md)                             | N      |
| ❌   | 5. 六自由度积分器    | F_thrust, F_aero, M_aero, angular_accel, prev_position, prev_posture, prev_velocity, p, q, r, Δt | new_position, new_posture, new_velocity, new_angular_velocity | 四元数（q₀,q₁,q₂,q₃）、质量（m, 常量）、转动惯量（I_xx/I_yy/I_zz/I_xz, 常量） | 重力加速度（g=9.80665）、质量（m）、转动惯量张量（I）                            | 使用 Heun 预测-校正法（二阶 RK）+ 四元数姿态积分 + 欧拉转动方程 ω×Iω，从合力/合力矩积分得到下一时刻飞行状态。卡片：[rigid-body-integrator-card](../../algorithms/flight-dynamics-rigid-body-integrator-card.md)                                      | N      |

- 输出变量：new_position（本时刻位置, Point）、new_posture（本时刻姿态, Posture）、new_velocity（本时刻速度, double）、new_angular_velocity（本时刻角速度, Vector3）、updated_fuel（本时刻燃油量, double）



#### 算法1：推进系统与燃油管理

本算法旨在**根据发动机燃油流量输入和当前飞行状态（速度、高度）计算发动机推力并更新燃油量**，通过**燃油消耗率限制、燃油质量更新和推力查表**，实现**推力输出和燃油状态的时间推进**。根据补充约束，飞机的非燃油质量在飞行全程保持恒定。

> **AFSIM 参考**（已逐卡阅读）：
> - **推力计算**：[flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)——CalculateThrust 函数（WsfSixDOF_JetEngine.cpp:428-864，436 行）。三层查表（Idle/Mil/AB）+ spool dynamics 油门转速动特性 + TSFC 燃油消耗率计算 + 熄火保护。核心公式：$T = T_{idle} + \delta_{mil} \cdot (T_{mil} - T_{idle}) + \delta_{ab} \cdot (T_{ab} - T_{mil})$，燃油消耗 $m_{fuel} = (T_{idle} \cdot SFC_{idle} + \delta_{mil} \cdot \Delta T_{mil} \cdot SFC_{mil}^{eff} + \delta_{ab} \cdot \Delta T_{ab} \cdot SFC_{ab}^{eff}) \cdot \Delta t / 3600$。
> - **燃油管理**：[flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md)——PropulsionSystem::Update（WsfSixDOF_PropulsionSystem.cpp:78-249，170 行）。多油箱燃油传输协调（比例因子算法）、CG 位置线性插值（emptyCg + fraction × (fullCg - emptyCg)）、总质量属性汇总。核心公式：$f = \min(1, |m_{max\_receive}| / |\sum m_{provided}|)$，等比压缩；CG 插值 $\mathbf{r}_{cg} = \mathbf{r}_{empty} + \frac{m_{current}}{m_{max}} \cdot (\mathbf{r}_{full} - \mathbf{r}_{empty})$。

1. 简化方案1：将**喷气发动机三层查表推力模型（Idle/Mil/AB）+ spool dynamics 简化为线性推力-油门关系**。对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)。
   1. 用公式表示为，将完整的 spool dynamics 限速渐进 + 三层查表公式简化为 $$T = \delta_{throttle} \times T_{max}(h)$$，其中 $\delta_{throttle}$ 表示油门位置（0~1），$T_{max}(h)$ 表示当前高度的最大推力。
   2. 简化后涉及变量：油门位置（δ_throttle）、最大推力曲线（T_max(h)）
   3. 简化后涉及常量：最大推力（T_max_sea_level）
   4. 需要补充的参数：T_max(h) 曲线（或海平面最大推力标量值）；油门位置 δ_throttle 需加入输入变量列表
- [x] 选择此方案

1. 简化方案2：将**TSFC 三段增量式燃油消耗计算简化为恒定燃油消耗率**。对应卡片 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md)（燃油公式部分）。
   1. 用公式表示为，将三段增量式 TSFC 公式简化为 $$m_{fuel} = \dot{m}_{const} \cdot \Delta t$$，其中 $\dot{m}_{const}$ 表示用户配置的恒定燃油质量流量。
   2. 简化后涉及变量：恒定燃油流量（fuel_flow_rate_const, double）
   3. 简化后涉及常量：恒定燃油消耗率（Fuel_Const_Rate）
   4. 需要补充的参数：恒定燃油流量标量值
- [x] 选择此方案

1. 简化方案3：将**多油箱燃油管理（传输协调+CG 插值+质量汇总）简化为单油箱模型**。对应卡片 [flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md)。
   1. 用公式表示为，跳过 PropulsionSystem::Update() 的传输分组/比例协调逻辑，燃油直接从唯一油箱消耗：$$m_{fuel}(t+\Delta t) = m_{fuel}(t) - m_{burn}$$，CG 固定在油箱中心。
   2. 简化后涉及变量：单油箱当前油量（current_fuel, double）
   3. 简化后涉及常量：油箱最大容量（Max_Fuel_Capacity）、初始油量（Initial_Fuel）
   4. 需要补充的参数：油箱最大容量、初始油量
- [x] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法2：气动模型

本算法旨在**根据飞机当前飞行状态（马赫数、攻角、侧滑角、角速率）计算气动六分量（升力、阻力、侧力、滚转力矩、俯仰力矩、偏航力矩）**，通过**稳定性导数高维查表（Ma×α×β×p×q×r 6维）+ 静态 3D 表项与动态阻尼增量叠加 + 动压×参考面积×参考长度缩放**，实现**有量纲六分量气动力和气动力矩的计算**。

> **AFSIM 参考**（已逐卡阅读）：
> - [flight-dynamics-rigidbody-aero-coefficient-card.md](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md)——RigidBodyAeroCoreObject::calculateAero，高维查表获取稳定性导数，静态 3D 表项与动态阻尼增量线性叠加后乘以动压/参考面积/参考长度得到有量纲六分量。
> - [flight-dynamics-pointmass-aero-card.md](../../algorithms/flight-dynamics-pointmass-aero-card.md)——PointMassAeroCoreObject::CalculateCoreAeroFM，在标准气动力上叠加非配平操纵面效果（减速板/襟翼/扰流板的 Delta CL/Cd），并输出旋转加速度限幅基准（随总迎角 cos α_total 衰减）和稳定化频率基准供 SAS 使用。

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

#### 算法3：自动驾驶仪 PID（航向→舵面指令转换）

本算法旨在**将 PATH-01 输出的期望航向角（heading_cmd）转化为 SAS 所需的三通道控制面指令（δ_elevator/δ_aileron/δ_rudder）**，通过**PID 嵌套回路控制**，实现**从导航级航向指令到执行级舵面偏转指令的转换**，填补 PATH-01 与 SAS 之间的管线缺口——heading_cmd 无人转化为 δ_commands。

> **AFSIM 参考**（已逐卡阅读）：
> [flight-dynamics-autopilot-pid-card.md](../../algorithms/flight-dynamics-autopilot-pid-card.md)——自动驾驶仪 PID 嵌套回路控制，Bank-To-Turn（BTT）和 Yaw-To-Turn（YTT）双模式，20 个 PID 控制器组成三通道嵌套反馈回路。BTT 横向通道：RollHeadingPID → BankAnglePID → RollRatePID → 副翼指令；YTT 横向通道：YawHeadingPID → YawRatePID → BetaPID → 方向舵指令；垂直通道：AltitudePID → VertSpeedPID → AlphaPID → 升降舵指令。支持增益调度（以动压查 PID 增益表）、抗积分饱和（back-calculation anti-windup + 误差阈值死区）、低通滤波导数和前馈偏置。
> 
> **与 SAS 的分工**：Autopilot PID 负责高层制导决策——将导航指令（heading_cmd）映射为执行指令（δ_commands），回答"往哪飞"；SAS 负责底层执行保护——将 δ_commands 转化为受限的角加速度，回答"怎么安全地转向"。

1. 简化方案1：将**完整 20 PID 三通道嵌套回路简化为 2 个简化 PID 控制器**——航向 PID（输出 δ_aileron）+ 俯仰保持 PID（输出 δ_elevator），方向舵取偏航阻尼比例项。算法复杂度从 O(20 PID × 多级嵌套) 降至 O(2 PID × 单层)。
   1. 用公式表示为：
      - **δ_aileron**（航向→副翼）：$$\delta_{ail} = \text{PID}_{hdg}(e_{hdg})$$，$e_{hdg} = \text{heading\_cmd} - \text{heading\_current}$，归一化到 [-180°, 180°]，限幅 [-1, 1]
      - **δ_rudder**（方向舵简化）：$$\delta_{rud} = K_{yaw} \cdot r$$，$r$ 为偏航角速率（简易偏航阻尼器），限幅 [-1, 1]
      - **δ_elevator**（俯仰保持）：$$\delta_{ele} = \text{PID}_{pitch}(e_{pitch})$$，$e_{pitch} = \theta_{cruise} - \theta_{current}$，保持巡航俯仰角，限幅 [-1, 1]
   2. 简化后涉及变量：航向误差（e_hdg, deg）、偏航角速率（r, deg/s）、俯仰误差（e_pitch, deg）、副翼偏转指令（δ_aileron）、方向舵偏转指令（δ_rudder）、升降舵偏转指令（δ_elevator）
   3. 简化后涉及常量：航向 PID 增益（K_p_hdg, K_i_hdg, K_d_hdg）、俯仰 PID 增益（K_p_pitch, K_i_pitch, K_d_pitch）、偏航阻尼增益（K_yaw）、最大转弯速率（max_turn_rate_dps）、最大滚转角（max_bank_deg）、巡航俯仰角（θ_cruise）
   4. 需要补充的参数：航向 PID 增益（3 个）、俯仰 PID 增益（3 个）、偏航阻尼增益（1 个）、转弯速率/滚转角限幅值（2 个）、巡航俯仰角（1 个）
- [ ] 选择此方案

1. 简化方案2：将**自动驾驶仪完全跳过，PATH-01 的 heading_cmd 直接驱动 SAS**（在 SAS 入口处从航向误差直接推算目标角速率，不使用 PID 和舵面指令中间层）。算法复杂度从 O(1~2 PID) 降至 O(0)（跳过此流程）。
   1. 用公式表示为，不再生成 δ 指令，改为 SAS 直接从 heading_cmd 和当前姿态角计算目标角速率：$$\omega_{cmd} = \text{clamp}(k \cdot e_{hdg}, \pm \omega_{max})$$，然后进入 SAS 控制项的一阶指令跟踪。
   2. 简化后涉及变量：航向误差（e_hdg）、目标角速率（ω_cmd, rad/s）
   3. 简化后涉及常量：比例增益系数（k）、最大角速率限幅（ω_max）
- [ ] 选择此方案

**修改要求**（人工提问与解答）：  

> **Q1**：方案1什么意思，什么是"本需求仅需航向跟踪，无需高度/速度通道"？为什么只有 δ_aileron 的计算公式？其他两个控制面指令呢？

**A1**：Autopilot PID 卡片定义了 4 条通道，每条输出一个控制面指令：

| 通道     | 嵌套回路                           | 最终输出                |
| ------ | ------------------------------ | ------------------- |
| 横向 BTT | RollHeading→BankAngle→RollRate | **δ_aileron（副翼）**   |
| 横向 YTT | YawHeading→YawRate→Beta        | **δ_rudder（方向舵）**   |
| 垂直     | Altitude→VertSpeed→Alpha       | **δ_elevator（升降舵）** |
| 速度/油门  | Speed PID                      | throttle            |

REQ-002 的 PATH-01 仅输出 heading_cmd（期望航向角），**没有**输出期望高度和期望速度指令。因此 BTT 的横向通道是**直接可用的**（heading→aileron），垂直通道和速度通道在当前模糊需求中尚无上游指令输入。

**人工追问**：
1.为什么PATH-01仅输出航向角？航线点Point是包括了高度的，理应需要考虑高度的变化，为什么会缺少期望高度？
2.对于期望速度，输入参数增加“期望在每个航向点的速度`vector<double>`”。

---

但原简化方案 1 的公式描述**不完整**——只给出了 δ_aileron，遗漏了 δ_rudder 和 δ_elevator。完整的简化方案 1 应该输出全部 3 个控制面指令，其中：
- **δ_aileron**：航向 PID 输出（BTT 简化）
- **δ_rudder**：在 BTT 模式下可取 0 或来自一个简易偏航阻尼器（proportional to r）
- **δ_elevator**：取固定配平值或来自一个简易俯仰保持 PID（target pitch = 0 或巡航俯仰角）

已在下方更正简化方案 1 的描述，补齐三个控制面指令的计算公式。

> **Q2**：采用简化方案1后有什么影响？

**A2**：简化方案 1 将嵌套三级 PID 压缩为单层后：

| 维度        | 完整版（20 PID）                 | 简化方案 1（1~2 PID）       |
| --------- | --------------------------- | --------------------- |
| **航向跟踪**  | ✅ 三级嵌套 + 增益调度 + anti-windup | ✅ 可跟踪，但无增益调度，大机动时可能超调 |
| **协调转弯**  | ✅ YTT 模式有方向舵协调              | ⚠️ 无协调，可能产生侧滑         |
| **高度保持**  | ✅ Altitude PID 嵌套           | ❌ 丢失——转弯时可能掉高度        |
| **速度保持**  | ✅ Speed PID                 | ❌ 丢失——油门需外部给定         |
| **滚转角限制** | ✅ BankAngle PID 限幅          | ❌ 丢失——大航向误差时可能过滚      |
| **参数数量**  | 60+ (20 PID × 3 增益)         | 3~6 (1~2 PID × 3 增益)  |
| **调参难度**  | 极高（级联耦合）                    | 低（单回路）                |
| **适用场景**  | 高保真全任务仿真                    | 基本航点跟随                |

**总结**：简化方案 1 适用于仅需航向跟踪的基本航点跟随场景，可接受转弯不够协调、高度可能波动的情况。若需求包含高度/速度精确保持，则不适合。

> **Q3**：采用 heading_cmd 直接驱动 SAS 是不是相当于自己写了个自动驾驶逻辑，直接推算目标角速率？

**A3**：是的。简化方案 2 的本质是**把 Autopilot PID 的航向→角速率映射逻辑嵌入到 SAS 的上游**。流程变为：

```
完整版：heading_cmd → [Autopilot PID: PID级联] → δ_commands → [SAS: 一阶跟踪+稳定项] → angular_accel
方案2： heading_cmd → [简易映射: ω_cmd = clamp(k·e_hdg, ±ω_max)] → [SAS: 一阶跟踪+稳定项] → angular_accel
```

SAS 本身算法不变（仍然是一阶指令跟踪 + 二阶临界阻尼稳定项），变的只是它的**输入来源**——从"经过完整 PID 级联加工的 δ_commands"变为"从航向误差直接按比例推算的 ω_cmd"。这等效于在 SAS 前面串联了一个**单增益比例控制器**。这确实是自己写了一段简化版的自动驾驶逻辑，跳过了 PID 的积分项、微分项、增益调度、anti-windup 等所有高级特性。

> **Q4**：采用简化方案2后有什么影响？

**A4**：

| 维度 | 简化方案 1（单层 PID→δ→SAS） | 简化方案 2（heading→ω_cmd→SAS） |
|------|---------------------------|-------------------------------|
| **控制品质** | 有 PID（P+I+D），可消除稳态误差 | 仅有比例增益 k，**存在稳态航向误差**（无积分项消除） |
| **舵面指令** | 输出标准 δ_commands（-1~1） | 跳过 δ 层，直接输出 ω_cmd |
| **与 AFSIM 差距** | 保留了 PID 结构，仅简化嵌套层级 | **完全改变了控制架构**，AFSIM 的 SAS 输入从 δ 变为 ω |
| **实现量** | 需实现 1~2 个 PID + 限幅 | 仅需 1 行公式：ω_cmd = clamp(k·e_hdg, ±ω_max) |
| **可扩展性** | 可后续加入 I/D 项和限幅 | 需重构架构才能加回 PID |
| **适用场景** | 基本航点跟随，有 PID 基本控制品质 | **极简原型验证**，不推荐作为最终方案 |

**建议**：若目标系统需要基本可用的航向跟踪，选择简化方案 1（含修正后的三通道输出）；若仅为验证管线连通性（"跑通数据流"），可选择简化方案 2 作为临时占位。

---

**人工追问**：

> **追问1**：为什么 PATH-01 仅输出航向角？航线点 Point 是包括了高度的，理应需要考虑高度的变化，为什么会缺少期望高度？

**A1**：正确。Point 结构含 `_lon/_lat/_alt`，`_alt` 是高度分量。PATH-01 的航线推进算法沿两个航路点之间的线段推进时，不仅应当输出 heading_cmd（从当前点到下一个航路点的水平方位角），还应当输出 **altitude_cmd**——沿航路段两端高度进行线性插值或按爬升/下滑角计算的目标高度。已修正：PATH-01 的输出变量列表和航线推进算法描述已增加 `altitude_cmd`，Autopilot PID 的输入增加了 `altitude_cmd`，使其垂直通道（AltitudePID→VertSpeedPID→AlphaPID→升降舵）获得上游指令输入。

> **追问2**：对于期望速度，输入参数增加"期望在每个航向点的速度 `vector<double>`"。

**A2**：已在模糊需求文档的"其他参数"中隐含有 `速度 double` 和 `最大速度 double`，但确实缺少"每个航路点的期望速度"这一结构化输入。采纳建议：**新增输入参数 `speed_cmd: vector<double>`**，长度与 path 的航路点数一致，每个元素表示飞机在到达该航路点之前应维持的巡航速度（m/s）。已修正：PATH-01 的航线推进算法在该航路段输出对应的 speed_cmd 期望速度值，Autopilot PID 的输入增加 `speed_cmd`，使其速度通道（Speed PID→throttle）获得上游指令输入。

> **补充修正**：由于 altitude_cmd 和 speed_cmd 的引入，Autopilot PID 的 4 条通道现在均可获得上游指令——横向 BTT（heading_cmd→aileron）、垂直（altitude_cmd→elevator）、速度（speed_cmd→throttle）、YTT 协调（可由偏航阻尼器简化）。此前"垂直通道和速度通道尚无上游指令，可暂以配平值替代"的限制已消除。Autopilot PID 选择 N（不简化，使用完整 20 PID）的决策现在具有完整的上游指令支撑。

______________________________________________  

#### 算法4：姿态控制系统 SAS

本算法旨在**为飞机提供旋转角加速度控制**，通过**控制-稳定解耦架构（一阶指令跟踪 + 二阶临界阻尼稳定项 + 独立通道限幅）**，实现**从控制指令（升降舵/副翼/方向舵偏转）到角加速度的安全转化，防止大迎角操纵效能丧失**。

> **AFSIM 参考**（已逐卡阅读）：
> [flight-dynamics-pointmass-sas-card.md](../../algorithms/flight-dynamics-pointmass-sas-card.md)——PointMassFlightControlSystem::CalculateStabilityAugmentation，核心创新为旋转动力学与控制指令解耦：控制项从目标角速率指令经一阶跟踪转换为角加速度 $\alpha_{controls} = (\omega_{cmd} - \omega_{current}) / \Delta t$；稳定项俯仰/偏航通道使用二阶临界阻尼 $\alpha_{pitch} = -\alpha \cdot \omega_n^2 - 2 \cdot \omega_n \cdot \dot{\alpha}$ 将攻角/侧滑角驱回零，滚转通道使用一阶滞后。各项各轴独立限幅后叠加得总旋转加速度。
> 
> **⚠️ 注意**：SAS 核心算法为**控制-稳定解耦架构**，非 PID 控制。PID 嵌套回路属于上游 Autopilot PID（算法3）。两卡的分工已在逐卡阅读中确认。

1. 简化方案1：将**完整三通道控制-稳定解耦 SAS 简化为仅角加速度限幅**。算法复杂度从 O(3通道×(一阶跟踪 + 二阶临界阻尼 + 限幅)) 降至 O(3通道×限幅)。
   1. 用公式表示为，将控制项+稳定项叠加的完整 SAS 简化为仅对上游输出的参考角加速度做裁剪：$$\ddot{\theta} = \text{clip}(\ddot{\theta}_{ref}, -\ddot{\theta}_{max}, \ddot{\theta}_{max})$$
   2. 简化后涉及变量：参考角加速度（p̈_ref, q̈_ref, r̈_ref）、角加速度限幅值（p̈_max, q̈_max, r̈_max）
   3. 简化后涉及常量：各通道角加速度最大限幅值
- [ ] 选择此方案

1. 简化方案2：将**完整 SAS 完全跳过，直接将上游角加速度输出给积分器**。算法复杂度降至 O(0)（跳过此流程）。
   1. 用公式表示为，将 SAS 环节完全省略，即 $$\ddot{\theta} = \ddot{\theta}_{ref}$$，不做任何滤波、限幅或稳定化处理。
   2. 简化后涉及变量：参考角加速度（p̈_ref, q̈_ref, r̈_ref）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  

#### 算法5：六自由度积分器

本算法旨在**对飞机进行六自由度时间推进**，通过**Heun 预测-校正法（二阶 Runge-Kutta）+ 四元数姿态积分 + 欧拉转动方程（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz）**，实现**从合力和合力矩到下一时刻飞行状态（位置、速度、姿态四元数、角速度）的数值积分**。根据补充约束，质量（m）和转动惯量张量（I）在飞行全程为常量（仅燃油质量随时间衰减）。

> **AFSIM 参考**（已逐卡阅读）：
> [flight-dynamics-rigid-body-integrator-card.md](../../algorithms/flight-dynamics-rigid-body-integrator-card.md)——RigidBodySixDOF_Mover::integrate，Heun 预测-校正法（二阶 RK）推进状态矢量，四元数姿态积分 + 欧拉转动方程 $I\dot{\boldsymbol{\omega}} + \boldsymbol{\omega} \times (I\boldsymbol{\omega}) = \mathbf{M}_{\text{total}}$。

1. 简化方案1：将**刚体六自由度积分器（含完整转动惯量张量 I 和欧拉转动方程交叉耦合项 ω×Iω）简化为 PointMass 点质积分器（忽略转动惯量耦合，使用半隐式欧拉法旋转积分）**。算法复杂度从 O(矩阵求逆+交叉耦合) 降至 O(对角项独立积分)。
   1. 用公式表示为，将刚体转动方程 $$I\dot{\boldsymbol{\omega}} + \boldsymbol{\omega} \times (I\boldsymbol{\omega}) = \mathbf{M}_{\text{total}}$$ 简化为点质旋转方程 $$\dot{p} = M_x, \dot{q} = M_y, \dot{r} = M_z$$（单位转动惯量），其中 $\boldsymbol{\omega} = [p, q, r]^T$ 表示角速度矢量。
   2. 简化后涉及变量：角速度（p, q, r）、合外力矩（M_x, M_y, M_z）
   3. 简化后涉及常量：无需转动惯量矩阵
- [ ] 选择此方案

1. 简化方案2：将**Heun 预测-校正法（二阶 RK）简化为显式欧拉法（一阶）**。算法复杂度从 O(2次函数评估/步) 降至 O(1次函数评估/步)，精度从 O(Δt²) 降至 O(Δt)。
   1. 用公式表示为，将 Heun 法 $$\begin{cases} \mathbf{y}^* = \mathbf{y}_n + \Delta t \cdot f(t_n, \mathbf{y}_n) \\ \mathbf{y}_{n+1} = \mathbf{y}_n + \frac{\Delta t}{2}[f(t_n, \mathbf{y}_n) + f(t_{n+1}, \mathbf{y}^*)] \end{cases}$$ 简化为显式欧拉法 $$\mathbf{y}_{n+1} = \mathbf{y}_n + \Delta t \cdot f(t_n, \mathbf{y}_n)$$
   2. 简化后涉及变量：状态矢量（y）
   3. 简化后涉及常量：无
- [ ] 选择此方案

**修改要求**（若有）：  
______________________________________________  


## 3. REQ-002 → REQ-002-INTEGRATION-03：航线机动集成层

本原需求旨在**将航线管理（REQ-002-PATH-01）和六自由度运动学计算（REQ-002-KINEMATICS-02）集成为一个完整的单机航线机动仿真步长更新**，要求**以仿真步长为推进单位，按顺序调用航路段映射→航线推进→剩余航线裁剪→推进系统→气动模型→自动驾驶仪 PID→SAS→积分器，组织输入数据的分发和输出数据的收集**，实现**飞机沿航线机动的端到端仿真更新（含三维位置 + 航向 + 高度 + 速度跟踪）**。

> **AFSIM 参考**：AFSIM 中飞机运动由 WsfPlatform::Update 循环驱动，Mover 基类负责位置/速度/姿态更新。wsf_six_dof 的 `maneuver/` 子目录实现机动编排。架构文档：docs/architecture/wsf_plugins/afsim-architecture.md §2.1 运动学系统，docs/architecture/core/afsim-architecture.md §6 仿真生命周期。

### 需求实现流程
- 输入变量：path（期望航线, vector\<Point\>）、prev_path（上个步长内路径, vector\<Point\>）、prev_posture（上个步长内姿态, vector\<Posture\>）、prev_velocity（上个步长内速度, vector\<double\>）、prev_fuel（上个步长内油量, vector\<double\>）、Δt（仿真步长, double）、t（当前时间戳, double）、fuel_consumption_rate（耗油量, double）、V_wind（风速, double）、V（飞机速度, double）、V_max（最大速度, double）、地球参数（Earth_Params）

| #   | 流程        | 上流程输入变量                                                                                                 | 输出至下流程变量                                                  | 其他变量 | 其他常量                  | 功能                                                   | 是否需要简化 |
| --- | --------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---- | --------------------- | ---------------------------------------------------- | ------ |
| ❌   | 1. 航线推进   | path, V, Δt, V_wind, t, Earth_Params                                                                    | ref_pos_next, remaining_path, heading_cmd, altitude_cmd, speed_cmd | —    | V_max                 | 调用 REQ-002-PATH-01：航路段映射→航线推进→剩余航线裁剪，输出航向/高度/速度指令 | N      |
| ❌   | 2. 六自由度计算 | ref_pos_next, heading_cmd, altitude_cmd, speed_cmd, prev_path, prev_posture, prev_velocity, prev_fuel, Δt, fuel_consumption_rate | new_path, new_posture, new_velocity, new_fuel, throttle_cmd | —    | 气动/推力/惯量常量（全部为飞行全程常量） | 调用 REQ-002-KINEMATICS-02：推进→气动→PID（含高度/速度通道）→SAS→积分 | N      |
| ❌   | 3. 输出组装   | new_path, new_posture, new_velocity, new_fuel, Δt                                                       | output_path, output_posture, output_velocity, output_fuel | —    | 步长阈值（1 s）             | 步长自适应输出：>1s 时输出每秒状态序列；≤1s 时仅输出下一帧状态                  | N      |

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
[3]: docs/algorithms/flight-dynamics-jet-engine-card.md "喷气发动机推力模型算法卡片"
[4]: docs/algorithms/flight-dynamics-propulsion-fuel-card.md "推进系统与燃油管理模型算法卡片"
[5]: docs/algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md "RigidBody 稳定性导数气动系数模型算法卡片"
[6]: docs/algorithms/flight-dynamics-pointmass-aero-card.md "PointMass 气动力与旋转限幅模型算法卡片"
[7]: docs/algorithms/flight-dynamics-autopilot-pid-card.md "自动驾驶仪 PID 嵌套回路控制算法卡片"
[8]: docs/algorithms/flight-dynamics-pointmass-sas-card.md "PointMass 稳定增稳系统算法卡片"
[9]: docs/algorithms/flight-dynamics-rigid-body-integrator-card.md "刚体六自由度积分器算法卡片"
[10]: docs/algorithms/flight-dynamics-pointmass-integrator-card.md "PointMass 六自由度积分器算法卡片"
[11]: docs/architecture/core/afsim-architecture.md "AFSIM 核心架构报告"
[12]: docs/architecture/wsf_plugins/afsim-architecture.md "AFSIM 插件架构报告（含 wsf_six_dof 子系统）"