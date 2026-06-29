# 延航线机动设计需求规范文档

> **模糊需求文档**：[`0_formation_move_along_path.md`](0_formation_move_along_path.md)
> **日期**：2026-06-27
> **需求编号**：REQ-002
> **状态**：已确认

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

- ✅ 完全满足 / ⚠️ 部分满足 / ❌ 缺失（AFSIM有参考） / 🆕 缺失（AFSIM无参考） / ❓ 无法判断


---

## 非功能需求（已确认）

### 1. 多线程支持

| 规范需求ID | 是否需要多线程支持 | 依据 | 备注 |
|-----------|------------------|------|------|
| REQ-002-PATH-01 | ❌ | 单机路径推进为串行逻辑，单次调用 O(1~N) | 多机并行时各自持有独立航线副本即可 |
| REQ-002-KINEMATICS-02 | ✅ | 多架飞机独立进行六自由度机动计算，每架飞机状态独立 | 数据并行，天然线程安全，每实体独立状态副本 |
| REQ-002-INTEGRATION-03 | ✅ | 集成层负责数据分发与收集，含步长自适应输出 | 输出缓冲区需线程安全容器或最小锁粒度 |

### 2. 性能要求

| 规范需求ID | 单次调用耗时上限 | 内存占用上限 | 其他性能约束 | 备注 |
|-----------|----------------|-------------|-------------|------|
| REQ-002-KINEMATICS-02 | < 200 μs/架 | < 10 KB/架 | 每仿真步长调用 1 次 | 管线内 5 个算法子流程串联 |
| REQ-002-INTEGRATION-03 | < 300 μs（含路径+六自由度+步长自适应） | < 20 KB | 每仿真步长调用 1 次 | 汇总步长自适应 |

### 3. 平台与可移植性

| 项目 | 要求 |
|------|------|
| 目标 OS | 跨平台（Windows + Linux） |
| C++ 标准 | C++17 |
| 编译器 | MSVC / GCC / Clang |
| 第三方库限制 | 允许 Eigen |

### 4. 其他约束

编码规范 Google Style，单元测试覆盖率 > 80% 核心路径，中文注释 + 英文标识符。


---


## 1. REQ-002 → REQ-002-PATH-01：航线管理与航路跟踪

本原需求旨在**为无人机/飞机提供沿预设期望航线（坐标点数组）自主飞行的航路管理能力**。根据最终确认，航线管理不仅输出期望航向角（heading_cmd），还输出期望高度（altitude_cmd）和期望速度（speed_cmd），为下游 Autopilot PID 的完整四通道控制提供全部指令输入。

> **AFSIM 参考**：编队汇合/位置保持/追击三状态机动控制算法，完整卡片 [flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md) 已逐卡阅读。

### 需求实现流程
- 输入变量：期望航线（path, vector\<Point\>）、当前仿真步长（Δt, double）、飞机速度（V, double）、最大速度（V_max, double）、风速（V_wind, double）、当前时间戳（t, double）、各航路点期望速度（speed_profile, vector\<double\>）

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 其他变量 | 其他常量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|---------|---------|------|-------------|
| ❌ | 1. 航路段映射 | path, Δt, V | current_leg_index, leg_progress | cur_pos（Point） | 航线点数组、地球参数 | 确定飞机所处航路段和段内进度 | Y |
| ❌ | 2. 航线推进 | current_leg_index, leg_progress, V, Δt, V_wind | ref_pos_next, heading_cmd, altitude_cmd, speed_cmd | — | V_max | 推进参考点，输出航向/高度（沿航路段两端高度线性插值）/速度指令 | N |
| ❌ | 3. 剩余航线裁剪 | path, ref_pos_next | remaining_path | — | — | 移除已飞越航点 | N |

- 输出变量：remaining_path（vector\<Point\>）、ref_pos_next（Point）、heading_cmd（double）、altitude_cmd（double）、speed_cmd（vector\<double\>）

> **说明**：航线点 Point 含 `_lon/_lat/_alt`，因此 altitude_cmd 由航路段两端高度线性插值得出。speed_cmd 来自新增输入 `speed_profile`，为各航路点的期望巡航速度。以上两个输出是 Autopilot PID 垂直通道和速度通道的上游指令来源，由人工在确认阶段补充。

#### 算法1：航路段映射（已简化）

✅ 已选择——简化方案2：仅向前搜索（禁止回退），O(1)。搜索范围从 $\forall i \in [1, N-1]$ 缩减为 $i \in [\text{current\_leg}, \text{current\_leg}+1]$。

#### 算法2：航线推进（无需简化）

沿航路段推进参考点，含风速矢量修正，输出 heading_cmd（航向方位角）、altitude_cmd（两端高度线性插值）、speed_cmd（speed_profile 对应段期望速度）。使用完整的风速修正和航线推进逻辑。

> AFSIM 参考：KeepStation 阶段 ECS 坐标系 P+D+DD 偏差精细控制。

#### 算法3：剩余航线裁剪（无需简化）

基本数组遍历操作，从航线中移除已飞越航点。


## 2. REQ-002 → REQ-002-KINEMATICS-02：六自由度运动学计算

本原需求旨在**使用六自由度模型计算飞机的姿态、位置和剩余油量**，通过**推进系统→气动模型→自动驾驶仪 PID→姿态控制系统 SAS→运动学积分**的五步管线实现。Autopilot PID 的完整四通道（横向 BTT/垂直/速度/YTT 协调）由 PATH-01 输出的 heading_cmd + altitude_cmd + speed_cmd 驱动。

> **AFSIM 参考**（全部逐卡阅读）：jet-engine-card、propulsion-fuel-card、rigidbody-aero-coefficient-card、pointmass-aero-card、autopilot-pid-card、pointmass-sas-card、rigid-body-integrator-card。
> 
> **补充约束（已确认）**：m 和 I 为飞行全程常量，仅 m_fuel 随时间衰减。

### 需求实现流程
- 输入变量：Δt、t、prev_position、prev_posture、prev_velocity、p/q/r、fuel_flow_rate、prev_fuel、heading_cmd（来自 PATH-01）、altitude_cmd（来自 PATH-01）、speed_cmd（来自 PATH-01）

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 其他变量 | 其他常量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|---------|---------|------|-------------|
| ❌ | 1. 推进系统与燃油管理 | Δt, fuel_flow_rate, prev_fuel, prev_velocity, prev_position.alt | F_thrust, updated_fuel | δ_throttle, N_spool | T_Table(Idle/Mil/AB), TSFC(3段) | 查表计算推力，TSFC 公式计算燃油消耗 | Y |
| ❌ | 2. 气动模型 | prev_velocity, prev_position.alt, prev_posture, p, q, r | F_aero, M_aero | Ma, α, β, q̄ | S_ref, l_ref, 稳定性导数表 | 计算气动六分量 | Y |
| ❌ | 3. 自动驾驶仪 PID | heading_cmd, altitude_cmd, speed_cmd, prev_posture, p, q, r, prev_velocity, α, β | δ_elevator/δ_aileron/δ_rudder, throttle_cmd | cmd_bank, turn_rate, cmd_vert_spd | PID 增益表(K_p/K_i/K_d, 动压调度)、限幅值 | 四通道 PID 嵌套回路：横向 BTT→aileron，垂直 Altitude→elevator，速度 Speed→throttle，YTT→rudder 协调 | N |
| ❌ | 4. 姿态控制系统 SAS | δ_commands, prev_angular_velocity, prev_posture, prev_velocity, α, β | angular_accel（p̈/q̈/r̈, 含限幅） | 限幅值, massFraction | ω_n_base, τ_roll/τ_pitch/τ_yaw | 控制-稳定解耦：一阶指令跟踪 + 二阶临界阻尼稳定项，各通道独立限幅 | N |
| ❌ | 5. 六自由度积分器 | F_thrust, F_aero, M_aero, angular_accel, prev_position, prev_posture, prev_velocity, p, q, r, Δt | new_position, new_posture, new_velocity, new_angular_velocity | 四元数, m(常量), I(常量) | g=9.80665, m, I | Heun 二阶 RK + 四元数姿态积分 + 欧拉转动方程 ω×Iω | N |

- 输出变量：new_position（Point）、new_posture（Posture）、new_velocity（double）、new_angular_velocity（Vector3）、updated_fuel（double）

#### 算法1：推进系统与燃油管理（已简化）

✅ 已选择——简化方案1（线性推力）：T = δ_throttle × T_max(h)。需补充 T_max(h) 和 δ_throttle 参数。
✅ 已选择——简化方案2（恒定燃油率）：m_fuel = ṁ_const × Δt。需补充 ṁ_const 参数。
✅ 已选择——简化方案3（单油箱）：m_fuel(t+Δt) = m_fuel(t) - m_burn，CG 固定在油箱中心。需补充 Max_Fuel_Capacity、Initial_Fuel。

> 三个简化方案组合为"最简"层级。AFSIM 参考：jet-engine-card（CalculateThrust, WsfSixDOF_JetEngine.cpp:428-864）+ propulsion-fuel-card（PropulsionSystem::Update, WsfSixDOF_PropulsionSystem.cpp:78-249）。

#### 算法2：气动模型（已简化）

✅ 已选择——简化方案2：仅保留气动力（不计算力矩），力矩全部由 SAS 提供。输出 [F_x, F_y, F_z]，M 全零。

> AFSIM 参考：rigidbody-aero-coefficient-card + pointmass-aero-card。

#### 算法3：自动驾驶仪 PID（无需简化，完整 20 PID 四通道）

将 PATH-01 输出的 heading_cmd / altitude_cmd / speed_cmd 通过完整 20 PID 三通道嵌套回路转化为三通道舵面指令和油门指令。**由于 altitude_cmd 和 speed_cmd 的引入，Autopilot PID 的四条通道现已全部获得上游指令**：

| 通道 | 嵌套回路 | 输入 | 输出 |
|------|---------|------|------|
| 横向 BTT | RollHeading→BankAngle→RollRate | heading_cmd | δ_aileron |
| 横向 YTT | YawHeading→YawRate→Beta | heading_cmd（协调） | δ_rudder |
| 垂直 | Altitude→VertSpeed→Alpha | altitude_cmd | δ_elevator |
| 速度 | Speed PID | speed_cmd | throttle_cmd |

> AFSIM 参考：autopilot-pid-card（CommonController::Update，20 PID 三通道嵌套，含增益调度/anti-windup/前馈偏置）。需补充参数：60+ PID 增益（建议首轮使用 AFSIM 默认增益表）。

> **关键明确——SAS 与 Autopilot PID 的分工**：Autopilot PID 负责高层制导决策——将导航指令（heading/altitude/speed）映射为执行指令（δ + throttle），回答"往哪飞、飞多高、飞多快"；SAS 负责底层执行保护——将 δ 转化为受限角加速度，回答"怎么安全地转向"。

#### 算法4：姿态控制系统 SAS（无需简化）

控制-稳定解耦架构：控制项 α_controls = (ω_cmd - ω_current) / Δt（一阶指令跟踪）；稳定项俯仰/偏航二阶临界阻尼 α = -α·ω_n² - 2·ω_n·α̇，滚转一阶滞后。各轴独立限幅后叠加。

> **注意**：SAS 核心算法为控制-稳定解耦架构，**非 PID 控制**。PID 嵌套回路属于上游 Autopilot PID（算法3）。AFSIM 参考：pointmass-sas-card（CalculateStabilityAugmentation）。

#### 算法5：六自由度积分器（无需简化）

Heun 预测-校正法（二阶 RK）+ 四元数姿态积分 + 欧拉转动方程 Iω̇ + ω×(Iω) = M_total。m 和 I 为飞行全程常量（补充约束），仅 m_fuel 在 FU-004 中单独衰减。

> AFSIM 参考：rigid-body-integrator-card（RigidBodySixDOF_Mover::integrate）。


## 3. REQ-002 → REQ-002-INTEGRATION-03：航线机动集成层

将 PATH-01（航线管理 + 三维指令输出）和 KINEMATICS-02（六自由度五步管线）集成为完整的单机航线机动仿真步长更新，实现**飞机沿航线机动的端到端仿真更新（含三维位置 + 航向 + 高度 + 速度跟踪）**。

### 需求实现流程
- 输入变量：path（vector\<Point\>）、speed_profile（vector\<double\>）、prev_path、prev_posture、prev_velocity、prev_fuel、Δt、t、fuel_consumption_rate、V_wind、V、V_max、Earth_Params

| # | 流程 | 上流程输入变量 | 输出至下流程变量 | 功能 | 是否需要简化 |
|---|------|--------------|------------------|------|-------------|
| ❌ | 1. 航线推进 | path, speed_profile, V, Δt, V_wind, t | ref_pos_next, remaining_path, heading_cmd, altitude_cmd, speed_cmd | 调用 PATH-01 | N |
| ❌ | 2. 六自由度计算 | ref_pos_next, heading_cmd, altitude_cmd, speed_cmd, prev_state, Δt, fuel_consumption_rate | new_path, new_posture, new_velocity, new_fuel, throttle_cmd | 调用 KINEMATICS-02（推进→气动→PID→SAS→积分） | N |
| ❌ | 3. 输出组装 | new_state, Δt | output_path, output_posture, output_velocity, output_fuel | 步长自适应：>1s 序列，≤1s 单帧 | N |

- 输出变量：remaining_path、output_path、output_posture、output_velocity、output_fuel

#### 算法1：集成调度（无需简化）

顺序调用航线推进→六自由度计算→输出组装，纯调度逻辑。


## 参考文献：
[1]: docs/algorithms/CompendiumofAlgorithms.md
[2]: docs/algorithms/flight-dynamics-station-keeping-card.md
[3]: docs/algorithms/flight-dynamics-jet-engine-card.md
[4]: docs/algorithms/flight-dynamics-propulsion-fuel-card.md
[5]: docs/algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md
[6]: docs/algorithms/flight-dynamics-pointmass-aero-card.md
[7]: docs/algorithms/flight-dynamics-autopilot-pid-card.md
[8]: docs/algorithms/flight-dynamics-pointmass-sas-card.md
[9]: docs/algorithms/flight-dynamics-rigid-body-integrator-card.md
[10]: docs/algorithms/flight-dynamics-pointmass-integrator-card.md
[11]: docs/architecture/core/afsim-architecture.md
[12]: docs/architecture/wsf_plugins/afsim-architecture.md