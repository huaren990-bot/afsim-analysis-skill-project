# 需求缺口分析报告 — requirement-gap-analysis.md

> **日期**：2026-06-16
> **来源需求规范**：`docs/requirements/structured_requirement_confirm/REQ-001-requirement-six-dof-UAV.md`
> **说明**：本报告总结需求覆盖度情况，列出所有能力缺口，并按优先级排序，给出总体迁移建议。

## 1. 分析概览
- **需求总数**：1
- **完全满足**：0
- **部分满足**：0
- **缺失**：1（拆分为 4 个功能单元 FU）
- **无法判断**：0
- **本次分析日期**：2026-06-16
- **参与校准人员**：由 requirement-spec-generator 自动生成，待人工复核

## 2. 需求覆盖度详表
| 需求 ID | 需求描述 | 覆盖状态 | 优先级 | 缺口 FU ID | 迁移建议 |
|---------|----------|----------|--------|------------|----------|
| REQ-001 | 使用六自由度模型计算无人机姿态和轨迹（含推进、气动、积分、SAS 四个子流程） | ❌ | 高 | FU-001, FU-002, FU-003, FU-004 | Clean-room 重实现（目标系统为空，无现有代码可适配） |

## 3. 能力缺口详细说明

### FU-001: 推进系统与燃油管理
- **关联需求**：REQ-001
- **功能描述**：根据发动机燃油流量输入和当前飞行状态（速度、高度）计算发动机推力，并更新燃油消耗量。需实现喷气发动机推力模型（含 Idle/Mil/AB 三层查表 + spool dynamics 转速加减速动特性）和燃油管理系统（含燃油消耗率限制、多油箱燃油传输比例协调、CG 位置线性插值）。
- **期望接口**：
  - 输入：仿真步长（Δt, double）、燃油流量（fuel_flow_rate, double）、当前燃油量（current_fuel_mass, double）、当前速度（velocity, double）、当前高度（altitude, double）
  - 输出：推力（thrust, double）、更新后燃油量（updated_fuel_mass, double）
- **AFSIM 参考实现**：`PointMassPropulsionSystem::updateThrust` (`wsf_six_dof/source/WsfPointMassSixDOF_PropulsionSystem.hpp`)；`JetEngineThrustModel::calculateThrust` （喷气发动机推力模型，[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.喷气发动机推力模型）
- **目标系统当前状态**：缺失 — 目标系统为空系统，无任何推进或燃油管理代码
- **建议迁移方式**：Clean-room 重实现 — 参考 AFSIM 算法卡片 [flight-dynamics-propulsion-fuel-card.md](../../algorithms/flight-dynamics-propulsion-fuel-card.md) 和 [flight-dynamics-jet-engine-card.md](../../algorithms/flight-dynamics-jet-engine-card.md) 的算法描述，从零构建推进和燃油管理系统
- **依赖项**：数学库（插值计算）、发动机推力数据表（T_Table）、燃油消耗率表（TSFC_Table）、油箱容量配置
- **风险等级**：中 — 核心算法（查表 + 线性插值）为标准技术，推力数据表和燃油消耗率表采用 AFSIM 默认数据，风险可控
- **备注**：人工已确认不简化，需完整实现三层查表推力模型和燃油管理；发动机数据表采用 AFSIM 默认数据

### FU-002: 气动模型
- **关联需求**：REQ-001
- **功能描述**：根据无人机当前飞行状态（马赫数、攻角、侧滑角、角速率）计算气动六分量（升力、阻力、侧力、滚转力矩、俯仰力矩、偏航力矩）。需实现 RigidBody 稳定性导数气动系数模型，支持高维查表（Ma×α×β×p×q×r 6 维插值）、静态 3D 表项与动态阻尼增量线性叠加、动压×参考面积×参考长度缩放。
- **期望接口**：
  - 输入：马赫数（mach, double）、攻角（alpha, double）、侧滑角（beta, double）、滚转角速率（p, double）、俯仰角速率（q, double）、偏航角速率（r, double）、动压（dynamic_pressure, double）
  - 输出：气动力矢量（aero_force, Vector3）、气动力矩矢量（aero_moment, Vector3）
- **AFSIM 参考实现**：`RigidBodyAeroCoreObject::calculateAero` (`wsf_six_dof/source/WsfRigidBodySixDOF_AeroCoreObject.hpp`)；RigidBody 稳定性导数气动系数模型（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.RigidBody 稳定性导数气动系数模型）
- **目标系统当前状态**：缺失 — 目标系统为空系统，无任何气动模型代码
- **建议迁移方式**：Clean-room 重实现 — 参考 AFSIM 算法卡片 [flight-dynamics-rigidbody-aero-coefficient-card.md](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md) 的算法描述，实现稳定性导数查表和气动六分量计算
- **依赖项**：多维插值库、稳定性导数数据表（C_L/C_D/C_Y/C_l/C_m/C_n，含 Ma×α×β×p×q×r 维度）、参考面积（S_ref）、参考长度（l_ref）
- **风险等级**：中 — 稳定性导数数据表为各飞行器特有，但人工已确认采用 AFSIM 默认数据表，风险可控
- **备注**：人工已确认不简化，需完整实现高维查表气动模型；气动数据表采用 AFSIM 默认数据

### FU-003: 六自由度积分器
- **关联需求**：REQ-001
- **功能描述**：使用 Heun 预测-校正法（二阶 Runge-Kutta）对无人机进行六自由度时间推进。将合外力（推力+气动力+重力）和合外力矩转化为线加速度和角加速度，通过四元数姿态积分和欧拉转动方程（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz）更新飞行状态（位置、速度、姿态四元数、角速度）。
- **期望接口**：
  - 输入：当前状态（position, velocity, quaternion, angular_velocity）、合外力（total_force, Vector3）、合外力矩（total_moment, Vector3）、质量（mass, double）、转动惯量张量（inertia_tensor, Matrix3）、仿真步长（dt, double）
  - 输出：更新后状态（new_position, new_velocity, new_quaternion, new_angular_velocity）
- **AFSIM 参考实现**：刚体六自由度 Heun 预测-校正积分器（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.刚体六自由度积分器），对应卡片 [flight-dynamics-rigid-body-integrator-card.md](../../algorithms/flight-dynamics-rigid-body-integrator-card.md)
- **目标系统当前状态**：缺失 — 目标系统为空系统，无任何运动学积分代码
- **建议迁移方式**：Clean-room 重实现 — 参考 AFSIM 算法卡片中的 Heun 预测-校正法 + 四元数姿态积分 + 欧拉转动方程描述，从零构建六自由度积分器
- **依赖项**：数学库（向量/矩阵运算、四元数代数）、重力加速度常量（g = 9.80665）、刚体质量（m）、转动惯量张量（I_xx/I_yy/I_zz/I_xz）
- **风险等级**：中 — Heun 方法和四元数积分为标准数值方法，转动惯量张量采用 AFSIM 默认参数；欧拉转动方程中的交叉耦合项（ω × Iω）需正确处理
- **备注**：人工已确认不简化，使用完整刚体六自由度 Heun 积分器；转动惯量参数采用 AFSIM 默认值

### FU-004: 姿态控制系统 SAS
- **关联需求**：REQ-001
- **功能描述**：实现三通道（滚转/俯仰/偏航）控制-稳定解耦姿态控制系统。将自动驾驶仪输出的控制指令（升降舵/副翼/方向舵偏转）转化为角加速度输出，含控制项（一阶指令跟踪）、稳定项（俯仰/偏航二阶临界阻尼 + 一阶滚转滞后）和各通道独立限幅保护。
- **期望接口**：
  - 输入：当前角速度（p, q, r, Vector3）、当前姿态角（roll, pitch, yaw）、控制指令（elevator, aileron, rudder）、当前速度（velocity, double）、攻角（alpha, double）、侧滑角（beta, double）
  - 输出：角加速度（angular_acceleration, Vector3），含限幅保护
- **AFSIM 参考实现**：PointMass 稳定增稳系统 SAS（[CompendiumofAlgorithms.md](../../algorithms/CompendiumofAlgorithms.md) §一.PointMass 稳定增稳系统），对应卡片 [flight-dynamics-pointmass-sas-card.md](../../algorithms/flight-dynamics-pointmass-sas-card.md)
- **目标系统当前状态**：缺失 — 目标系统为空系统，无任何飞行控制系统代码
- **建议迁移方式**：Clean-room 重实现 — 参考 AFSIM 算法卡片中的控制-稳定解耦架构描述，从零构建 SAS 系统
- **依赖项**：PID 控制库、各通道控制增益（K_p/K_i/K_d）、时间常数（τ_roll/τ_pitch/τ_yaw）、角加速度限幅值（p̈_max/q̈_max/r̈_max）
- **风险等级**：低 — SAS 核心算法为标准 PID 控制，控制-稳定解耦架构为公开设计模式；增益参数需针对具体无人机型号调参
- **备注**：人工已确认不简化，需完整实现三通道控制-稳定解耦 SAS；各通道 PID 增益和时间常数需通过飞行试验或系统辨识获取

## 4. 优先级排序与阶段建议
- **高优先级（立即实施）**：FU-003（六自由度积分器）— 是运动学仿真的核心，其他模块（推进、气动、SAS）的输出均依赖积分器进行时间推进；可先以简化力模型（常力/零力）验证积分器正确性
- **中优先级（后续迭代）**：FU-001（推进系统与燃油管理）、FU-002（气动模型）— 两者为积分器提供力和力矩输入，需并行开发；气动模型（FU-002）依赖外部数据表，风险较高，建议尽早启动数据获取
- **低优先级（可延后）**：FU-004（姿态控制系统 SAS）— 在无自动驾驶仪/控制指令输入的初期测试中，SAS 可用直接角加速度输入替代；待积分器和气动模型验证通过后再集成

## 5. 遗留问题与待澄清项
- ~~**FU-003 简化状态**~~：已确认不简化，使用完整刚体六自由度 Heun 积分器
- ~~**气动数据表来源**~~：已确认采用 AFSIM 默认数据表
- ~~**转动惯量参数**~~：已确认采用 AFSIM 默认参数
- ~~**发动机数据表**~~：已确认采用 AFSIM 默认数据表

> **状态**：所有遗留问题已解决 ✅

## 6. 附录
- 引用文档：
  - 需求规范确认文档：`docs/requirements/structured_requirement_confirm/REQ-001-requirement-six-dof-UAV.md`
  - 功能映射矩阵：`docs/requirements/confirmed_requirement_doc/function-mapping-matrix.md`
  - 需求追溯矩阵：`docs/requirements/confirmed_requirement_doc/requirement-to-afsim-trace.md`
  - AFSIM 算法汇总：`docs/algorithms/CompendiumofAlgorithms.md`