# 需求缺口分析报告 — REQ-002-requirement-gap-analysis.md

> **来源需求规范**：[`2_REQ-002-requirement-formation-move-along-path.md`](../../requirements/REQ_002/2_REQ-002-requirement-formation-move-along-path.md)
> **日期**：2026-06-26
> **需求编号**：REQ-002
> **说明**：本报告总结需求覆盖度情况，列出所有能力缺口，并按优先级排序，给出总体迁移建议。

## 1. 分析概览
- **需求总数**：3（含 8 个功能单元 FU）
- **完全满足**：0
- **部分满足**：0
- **缺失（AFSIM 有参考）**：8
- **缺失（AFSIM 无参考）**：0
- **无法判断**：0
- **参与校准人员**：AI + 待人工确认

## 2. 需求覆盖度详表
| 需求 ID | 需求描述 | 覆盖状态 | 优先级 | 缺口 FU ID | 迁移建议 |
|---------|----------|----------|--------|------------|----------|
| REQ-002-PATH-01 | 航路段映射（仅向前搜索） | ❌ | 高 | FU-001 | Clean-room |
| REQ-002-PATH-01 | 航线推进（风速修正） | ❌ | 高 | FU-002 | Clean-room |
| REQ-002-PATH-01 | 剩余航线裁剪 | ❌ | 低 | FU-003 | Clean-room |
| REQ-002-KINEMATICS-02 | 推进系统（线性推力+恒定燃油率+单油箱） | ❌ | 高 | FU-004 | Clean-room（按简化版） |
| REQ-002-KINEMATICS-02 | 气动模型（仅气动力） | ❌ | 高 | FU-005 | Clean-room（按简化版） |
| REQ-002-KINEMATICS-02 | 六自由度积分器（Heun+四元数+欧拉方程） | ❌ | 高 | FU-006 | Clean-room（完整版） |
| REQ-002-KINEMATICS-02 | SAS 姿态控制（三通道） | ❌ | 中 | FU-007 | Clean-room（完整版） |
| REQ-002-INTEGRATION-03 | 航线机动集成层 | ❌ | 中 | FU-008 | Clean-room（调度层） |

## 3. 能力缺口详细说明
### FU-001: 航路段映射（简化版）
- **关联需求**：REQ-002-PATH-01
- **功能描述**：
  - 确定飞机在航线中的位置——所在航路段序号和段内归一化进度。已简化为仅向前搜索（禁止回退），搜索范围 O(1)。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 期望航线 | path | vector\<Point\> | 航路点坐标数组 |
    | 2 | 飞机当前位置 | cur_pos | Point | 当前飞机经纬度/高度 |
    | 3 | 当前航路段索引 | current_leg | int | 上一帧所处航路段 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 更新后航路段索引 | current_leg_index | int | 当前帧所处航路段 |
    | 2 | 段内归一化进度 | leg_progress | double | [0,1]，0=段起点，1=段终点 |

- **AFSIM 参考实现**：
  - 1. wsf_six_dof/wsf_p6dof `maneuver/` 航路管理模块
  - 2. 编队三状态机动控制 FormUp 阶段航路跟踪逻辑

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统，无任何航路管理相关代码。

- **建议迁移方式**：Clean-room 重实现
  - 按简化版（仅向前搜索）实现，算法卡片参考：[flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md)

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：无
  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | sqrt、min/max 等基本运算 |
    | 2 | `Eigen` | 向量点积、线段投影 |

  - 3. 其它模块：无

- **风险等级**：低

- **备注**：已简化为仅向前搜索（O(1)），算法简单，无外部数据依赖。

### FU-002: 航线推进（风速修正）
- **关联需求**：REQ-002-PATH-01
- **功能描述**：
  - 沿当前航路段以设定速度推进参考点位置，考虑风速矢量叠加影响，输出期望航向角。使用 ECS（地球中心驻留）坐标系下的位移计算。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 当前航路段索引 | current_leg_index | int | 所处航路段 |
    | 2 | 段内进度 | leg_progress | double | [0,1] |
    | 3 | 飞机速度 | V | double | 编队/飞机设定速度 |
    | 4 | 仿真步长 | Δt | double | 时间推进步长 |
    | 5 | 风速 | V_wind | double（含方向） | 环境风速矢量 |
    | 6 | 期望航线 | path | vector\<Point\> | 航路点数组 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 下一时刻参考点位置 | ref_pos_next | Point | 飞机参考点经纬度/高度 |
    | 2 | 期望航向角 | heading_cmd | double | 指向下一航路点的航向角（度） |

- **AFSIM 参考实现**：
  - 1. 编队三状态机动控制 KeepStation 阶段——ECS 坐标系 P+D+DD 偏差精细控制
  - 2. wsf_six_dof/wsf_p6dof `formation/` 编队动作库

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。

- **建议迁移方式**：Clean-room 重实现
  - 无简化，完整实现。算法卡片参考：[flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md)

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 最大速度 | V_max | double | 硬编码（全局常量） | 速度上限限幅 |
    | 2 | 地球参数 | Earth_Params | struct | 硬编码（全局常量） | 经纬度↔距离转换 |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | sin/cos/sqrt 等三角函数和基本运算 |
    | 2 | `Eigen` | 矢量加法/点积、坐标系旋转变换 |

  - 3. 其它模块：无

- **风险等级**：中

- **备注**：地理坐标系下位移计算需正确处理经纬度→距离转换，风速矢量叠加需考虑风向坐标系变换。

### FU-003: 剩余航线裁剪
- **关联需求**：REQ-002-PATH-01
- **功能描述**：
  - 从原始航线数组中移除已飞越的航路点，返回剩余未到达的航点序列。基本数组遍历操作。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 原始航线 | path | vector\<Point\> | 完整期望航线 |
    | 2 | 参考点下一时刻位置 | ref_pos_next | Point | 判断飞越状态 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 剩余航线 | remaining_path | vector\<Point\> | 未到达的航点序列 |

- **AFSIM 参考实现**：
  - 1. 无——基本数组操作，AFSIM 中无独立算法对应

- **目标系统当前状态**：❌（缺失）

- **建议迁移方式**：Clean-room 重实现

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：无
  - 2. 数学库：无
  - 3. 其它模块：无

- **风险等级**：低

- **备注**：无算法复杂度，标准 C++ 数组操作。

### FU-004: 推进系统（线性推力+恒定燃油率+单油箱）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 简化版推进系统：推力使用线性推力-油门关系（T=δ×Tmax(h)）；燃油消耗使用恒定燃油消耗率（m_fuel=ṁ_const×Δt）；油箱管理简化为单油箱直接消耗模型。跳过 AFSIM 完整模型的三层查表+spool dynamics+多油箱传输协调。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 仿真步长 | Δt | double | 时间推进步长 |
    | 2 | 油门位置 | δ_throttle | double | 0~1 |
    | 3 | 上一时刻燃油量 | prev_fuel | double | 当前燃油质量 |
    | 4 | 当前高度 | altitude | double | 用于 T_max(h) 查值 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 推力 | F_thrust | double | 当前帧推力 |
    | 2 | 更新后燃油量 | updated_fuel | double | 消耗后的燃油质量 |

- **AFSIM 参考实现**：
  - 1. `JetEngine::CalculateThrust` (`WsfSixDOF_JetEngine.cpp:428-864`)——完整三层查表+spool dynamics 推力计算
  - 2. `PropulsionSystem::Update` (`WsfSixDOF_PropulsionSystem.cpp:78-249`)——多油箱燃油传输协调
  - 3. `FuelTank::UpdateFuelBurn` (`WsfSixDOF_FuelTank.cpp:390-431`)——燃油燃烧状态更新

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。当前需求参数（fuel_flow_rate、prev_fuel、fuel_consumption_rate）不足以支持完整模型，本 FU 采用最简层级简化组合。

- **建议迁移方式**：Clean-room 重实现（简化版）
  - 简1（线性推力 T=δ×Tmax(h)）+ 简2（恒定燃油率 ṁ=const）+ 简3（单油箱模型）。算法卡片参考：[jet-engine-card](../../algorithms/flight-dynamics-jet-engine-card.md) + [propulsion-fuel-card](../../algorithms/flight-dynamics-propulsion-fuel-card.md)

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 最大推力曲线 | T_max(h) | double[] 或 double | 硬编码（全局常量） | 线性推力公式 T=δ×T_max(h) |
    | 2 | 恒定燃油流量 | ṁ_const | double | 硬编码（全局常量） | 恒定燃油消耗率 |
    | 3 | 油箱最大容量 | Max_Fuel_Capacity | double | 硬编码（全局常量） | 油箱满度限制 |
    | 4 | 初始油量 | Initial_Fuel | double | 硬编码（全局常量） | 仿真起始燃油量 |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | min/max 限幅操作 |
    | 2 | `<algorithm>` | std::clamp |

  - 3. 其它模块：无

- **风险等级**：中

- **备注**：三个简化方案均选中（简1+简2+简3），形成"最简"层级。需人工补充 T_max(h)、ṁ_const、Max_Fuel_Capacity、Initial_Fuel 四个参数。完整模型参数缺口见本报告 §5。

### FU-005: 气动模型（仅气动力）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 仅计算气动力的三个分量（升力、阻力、侧力），不计算气动力矩（三个力矩分量全为零）。力矩全部由 SAS 系统提供。使用参考面积、参考长度和动压进行缩放。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 当前速度 | V | double | 速度标量 |
    | 2 | 当前高度 | h | double | 海拔高度 |
    | 3 | 当前姿态 | posture | Posture | yaw/pitch/roll 角 |
    | 4 | 滚转角速率 | p | double | 绕体轴 x 角速率 |
    | 5 | 俯仰角速率 | q | double | 绕体轴 y 角速率 |
    | 6 | 偏航角速率 | r | double | 绕体轴 z 角速率 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 气动力矢量 | F_aero | Vector3 | [F_x, F_y, F_z]（升力/阻力/侧力） |

- **AFSIM 参考实现**：
  - 1. `RigidBodyAeroCoreObject::calculateAero` (`WsfRigidBodySixDOF_AeroCoreObject.hpp`)——完整 6 分量气动计算
  - 2. PointMass 气动力与旋转限幅模型——简化气动替代

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。

- **建议迁移方式**：Clean-room 重实现（简化版）
  - 仅保留气动力三向分量。算法卡片参考：[rigidbody-aero-coefficient-card](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md) + [pointmass-aero-card](../../algorithms/flight-dynamics-pointmass-aero-card.md)

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 参考面积 | S_ref | double | 硬编码（全局常量） | 动压缩放 |
    | 2 | 参考长度 | l_ref | double | 硬编码（全局常量） | 力矩系数缩放（本FU不计算力矩但仍需保留以备扩展） |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | sin/cos 攻角侧滑角分解 |
    | 2 | `Eigen` | Vector3 运算 |

  - 3. 其它模块：如下表所示

    | # | 模块名 | 用途 |
    |---|------|------|
    | 1 | FU-007（SAS） | 提供全部力矩控制 |

- **风险等级**：中

- **备注**：已选简2（仅保留气动力），力矩全部由 SAS 提供。需人工补充 S_ref、l_ref 参数。

### FU-006: 六自由度积分器（Heun+四元数+欧拉转动方程）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 使用 Heun 预测-校正法（二阶 Runge-Kutta）对飞机进行六自由度时间推进。将合力和合力矩转化为线加速度和角加速度，通过四元数姿态积分和欧拉转动方程（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz）更新飞行状态（位置、速度、姿态四元数、角速度）。根据补充约束，质量（m）和转动惯量（I）在飞行全程为常量（仅燃油质量随时间衰减）。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 当前位置 | position | Point | 经纬度/高度 |
    | 2 | 当前速度 | velocity | double | 速度标量 |
    | 3 | 当前姿态四元数 | quaternion | Quaternion | 姿态表示 |
    | 4 | 当前角速度 | angular_velocity | Vector3 | p/q/r |
    | 5 | 合外力 | total_force | Vector3 | 推力+气动力+重力 |
    | 6 | 合外力矩 | total_moment | Vector3 | 气动力矩（来自SAS） |
    | 7 | 飞行器质量 | mass | double | m（常量） |
    | 8 | 转动惯量张量 | inertia_tensor | Matrix3 | I（常量，含 I_xz 非对角项） |
    | 9 | 仿真步长 | Δt | double | 时间推进步长 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 更新后位置 | new_position | Point | 下一时刻经纬度/高度 |
    | 2 | 更新后速度 | new_velocity | double | 下一时刻速度 |
    | 3 | 更新后姿态四元数 | new_quaternion | Quaternion | 下一时刻姿态 |
    | 4 | 更新后角速度 | new_angular_velocity | Vector3 | 下一时刻 p/q/r |

- **AFSIM 参考实现**：
  - 1. `RigidBodySixDOF_Mover::integrate` (`WsfRigidBodySixDOF_Mover.hpp`)——刚体六自由度 Heun 积分器
  - 2. PointMass 六自由度 Heun 积分器 (`WsfPointMassSixDOF_Mover.hpp`)——点质替代方案

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。

- **建议迁移方式**：Clean-room 重实现（完整版）
  - 无简化。算法卡片参考：[rigid-body-integrator-card](../../algorithms/flight-dynamics-rigid-body-integrator-card.md) + [pointmass-integrator-card](../../algorithms/flight-dynamics-pointmass-integrator-card.md)

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 重力加速度 | g | double | 硬编码（全局常量） | 9.80665 m/s² |
    | 2 | 飞行器质量 | m | double | 硬编码（全局常量） | 平动方程 |
    | 3 | 转动惯量张量 | I | Matrix3 | 硬编码（全局常量） | 欧拉转动方程 |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | sin/cos/sqrt 等基本运算 |
    | 2 | `Eigen` | Vector3/Matrix3/Quaternion 全量运算 |

  - 3. 其它模块：无

- **风险等级**：中

- **备注**：欧拉转动方程交叉耦合项（ω×Iω）需正确处理；转动惯量张量非对角项 I_xz 的处理需验证。m 和 I 在飞行全程为常量（补充约束），仅燃油质量在 FU-004 中单独衰减。

### FU-007: SAS 姿态控制（三通道控制-稳定解耦）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 三通道（滚转/俯仰/偏航）控制-稳定解耦架构。控制项：一阶指令跟踪；稳定项：俯仰/偏航二阶临界阻尼 + 一阶滚转滞后；各通道独立限幅保护。将控制指令（含期望航向角）转化为受保护的角加速度输出。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 当前角速度 | angular_velocity | Vector3 | p/q/r |
    | 2 | 当前姿态角 | attitude | Vector3 | roll/pitch/yaw |
    | 3 | 控制指令 | control_command | Vector3 | δ_elevator/δ_aileron/δ_rudder |
    | 4 | 当前速度 | velocity | double | 动压参考 |
    | 5 | 攻角 | α | double | 气动参考 |
    | 6 | 侧滑角 | β | double | 气动参考 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 角加速度 | angular_accel | Vector3 | p̈/q̈/r̈（含限幅保护） |

- **AFSIM 参考实现**：
  - 1. `PointMassFlightControlSystem::computeAngularAcceleration` (`WsfPointMassSixDOF_FlightControlSystem.hpp`)——完整 SAS 系统

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。

- **建议迁移方式**：Clean-room 重实现（完整版）
  - 无简化。算法卡片参考：[pointmass-sas-card](../../algorithms/flight-dynamics-pointmass-sas-card.md)

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 滚转通道 P/I/D 增益 | K_p_roll/K_i_roll/K_d_roll | double/ double/ double | 硬编码（全局常量） | 滚转 PID 控制 |
    | 2 | 俯仰通道 P/I/D 增益 | K_p_pitch/K_i_pitch/K_d_pitch | double/ double/ double | 硬编码（全局常量） | 俯仰 PID 控制 |
    | 3 | 偏航通道 P/I/D 增益 | K_p_yaw/K_i_yaw/K_d_yaw | double/ double/ double | 硬编码（全局常量） | 偏航 PID 控制 |
    | 4 | 滚转时间常数 | τ_roll | double | 硬编码（全局常量） | 一阶滚转滞后 |
    | 5 | 俯仰时间常数 | τ_pitch | double | 硬编码（全局常量） | 二阶临界阻尼 |
    | 6 | 偏航时间常数 | τ_yaw | double | 硬编码（全局常量） | 二阶临界阻尼 |
    | 7 | 各通道角加速度限幅 | p̈_max/q̈_max/r̈_max | double/ double/ double | 硬编码（全局常量） | 限幅保护 |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | sin/cos/clip |
    | 2 | `Eigen` | Vector3 运算 |

  - 3. 其它模块：无

- **风险等级**：低

- **备注**：SAS 核心算法为标准 PID 控制，控制-稳定解耦架构为公开设计模式。需人工补充 12 个 PID 和限幅参数。

### FU-008: 航线机动集成层
- **关联需求**：REQ-002-INTEGRATION-03
- **功能描述**：
  - 按顺序调度 PATH-01（航路段映射→航线推进→剩余航线裁剪）→ KINEMATICS-02（推进系统→气动模型→积分器→SAS）→ 输出组装。步长自适应输出：>1s 时输出每秒状态序列，≤1s 时仅输出下一帧状态。纯调度逻辑，无独立算法复杂度。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 期望航线 | path | vector\<Point\> | 航路点数组 |
    | 2 | 上一时刻路径 | prev_path | vector\<Point\> | 上一帧位置 |
    | 3 | 上一时刻姿态 | prev_posture | vector\<Posture\> | 上一帧姿态 |
    | 4 | 上一时刻速度 | prev_velocity | vector\<double\> | 上一帧速度 |
    | 5 | 上一时刻油量 | prev_fuel | vector\<double\> | 上一帧燃油 |
    | 6 | 仿真步长 | Δt | double | 时间推进步长 |
    | 7 | 当前时间戳 | t | double | 仿真时间 |
    | 8 | 耗油量 | fuel_consumption_rate | double | 燃油消耗率 |
    | 9 | 风速 | V_wind | double | 环境风速 |
    | 10 | 飞机速度 | V | double | 设定速度 |
    | 11 | 最大速度 | V_max | double | 速度上限 |
    | 12 | 地球参数 | Earth_Params | struct | 坐标转换 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 剩余航线 | remaining_path | vector\<Point\> | 未到达航点 |
    | 2 | 输出路径 | output_path | vector\<Point\> | 步长自适应 |
    | 3 | 输出姿态 | output_posture | vector\<Posture\> | 步长自适应 |
    | 4 | 输出速度 | output_velocity | vector\<double\> | 步长自适应 |
    | 5 | 输出油量 | output_fuel | vector\<double\> | 步长自适应 |

- **AFSIM 参考实现**：
  - 1. `WsfPlatform::Update` → `WsfMover::Update` (`WsfPlatform.hpp`, `WsfMover.hpp`)——AFSIM 仿真驱动框架
  - 2. docs/architecture/core/afsim-architecture.md §6 仿真生命周期

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。

- **建议迁移方式**：Clean-room 重实现（调度层）
  - 依赖 FU-001~FU-007 全部完成后集成

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 步长阈值 | STEP_THRESHOLD | double | 硬编码（全局常量） | 1.0s，控制输出粒度 |

  - 2. 数学库：无
  - 3. 其它模块：如下表所示

    | # | 模块名 | 用途 |
    |---|------|------|
    | 1 | FU-001 | 航路段映射 |
    | 2 | FU-002 | 航线推进 |
    | 3 | FU-003 | 剩余航线裁剪 |
    | 4 | FU-004 | 推进系统 |
    | 5 | FU-005 | 气动模型 |
    | 6 | FU-006 | 六自由度积分器 |
    | 7 | FU-007 | SAS 姿态控制 |

- **风险等级**：中

- **备注**：纯调度逻辑，依赖所有子 FU。需在所有子 FU 完成后进行端到端集成测试。

## 4. 优先级排序与阶段建议
- **高优先级（立即实施）**：
  - 1. FU-006（六自由度积分器）——运动学仿真核心，其它模块（推进、气动、SAS）的输出均依赖积分器；可先以简化力模型（常力/零力）验证积分器正确性。
  - 2. FU-001 + FU-002（航线推进）——路径管理核心，与积分器并行的管线入口模块。
  - 3. FU-004（推进系统）+ FU-005（气动模型）——为积分器提供力和力矩输入，在积分器验证通过后接入。
  
- **中优先级（后续迭代）**：
  - 1. FU-007（SAS 姿态控制）——依赖积分器和气动模型，在核心管线稳定后接入控制回路。
  - 2. FU-008（集成层）——依赖全部子 FU，需在所有子 FU 完成后集成。
  
- **低优先级（可延后）**：
  - 1. FU-003（剩余航线裁剪）——基本数组操作，可在航线推进实现后随时添加。

## 5. 遗留问题与待澄清项
- FU-004 参数缺口：T_max(h) 曲线（或标量值）、ṁ_const、油箱容量/初始油量，共 3~5 个参数待人工提供。
- FU-005 参数缺口：S_ref（参考面积）、l_ref（参考长度），共 2 个参数待人工提供。
- FU-007 参数缺口：PID 增益（9 个 K_p/K_i/K_d）+ 时间常数（3 个 τ）+ 限幅值（3 个），共 15 个参数待人工提供或采用 AFSIM 默认值。

## 6. 附录
- 引用文档：
  - 需求规范确认文档：`docs/requirements/REQ_002/2_REQ-002-requirement-formation-move-along-path.md`
  - 功能映射矩阵：`docs/requirements/confirmed_requirement_doc/REQ-002-function-mapping-matrix.md`
  - 需求追溯矩阵：`docs/requirements/confirmed_requirement_doc/REQ-002-requirement-to-afsim-trace.md`