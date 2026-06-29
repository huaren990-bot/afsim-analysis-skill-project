# 需求缺口分析报告 — 3_REQ-002-requirement-gap-analysis.md

> **来源需求规范**：[`2_REQ-002-requirement-formation-move-along-path.md`](2_REQ-002-requirement-formation-move-along-path.md)
> **日期**：2026-06-27
> **需求编号**：REQ-002
> **说明**：本报告总结需求覆盖度情况，列出所有能力缺口，并按优先级排序，给出总体迁移建议。

## 1. 分析概览
- **需求总数**：3（含 9 个功能单元 FU）
- **完全满足**：0
- **部分满足**：0
- **缺失（AFSIM 有参考）**：9
- **缺失（AFSIM 无参考）**：0
- **无法判断**：0
- **参与校准人员**：AI + 待人工确认

## 2. 需求覆盖度详表
| 需求 ID | 需求描述 | 覆盖状态 | 优先级 | 缺口 FU ID | 迁移建议 |
|---------|----------|----------|--------|------------|----------|
| REQ-002-PATH-01 | 航路段映射（仅向前搜索） | ❌ | 高 | FU-001 | Clean-room（简化版） |
| REQ-002-PATH-01 | 航线推进（三维指令输出） | ❌ | 高 | FU-002 | Clean-room |
| REQ-002-PATH-01 | 剩余航线裁剪 | ❌ | 低 | FU-003 | Clean-room |
| REQ-002-KINEMATICS-02 | 推进系统（最简层级） | ❌ | 高 | FU-004 | Clean-room（简化版） |
| REQ-002-KINEMATICS-02 | 气动模型（仅气动力） | ❌ | 高 | FU-005 | Clean-room（简化版） |
| REQ-002-KINEMATICS-02 | 自动驾驶仪 PID（完整20PID四通道） | ❌ | 中 | FU-006 | Clean-room（完整版） |
| REQ-002-KINEMATICS-02 | SAS 姿态控制（控制-稳定解耦） | ❌ | 中 | FU-007 | Clean-room（完整版） |
| REQ-002-KINEMATICS-02 | 六自由度积分器（Heun+四元数+欧拉方程） | ❌ | 高 | FU-008 | Clean-room（完整版） |
| REQ-002-INTEGRATION-03 | 航线机动集成层 | ❌ | 中 | FU-009 | Clean-room（调度层） |

## 3. 能力缺口详细说明
### FU-001: 航路段映射（简化版）
- **关联需求**：REQ-002-PATH-01
- **功能描述**：
  - 确定飞机在航线中的位置——所在航路段序号和段内归一化进度。已简化为仅向前搜索（禁止回退），搜索范围 O(1)。输出航路段索引和段内进度供航线推进使用。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 期望航线 | path | vector\<Point\> | 航路点坐标数组 |
    | 2 | 仿真步长 | Δt | double | 时间推进步长 |
    | 3 | 飞机速度 | V | double | 当前速度 |
    | 4 | 当前位置 | cur_pos | Point | 飞机当前经纬度/高度 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 航路段索引 | current_leg_index | int | 当前所处的航路段序号 |
    | 2 | 段内进度 | leg_progress | double | 归一化进度 [0,1]，0=段起点，1=段终点 |

- **AFSIM 参考实现**：
  - 1. wsf_six_dof `maneuver/` 航路管理模块 — 机动动作库中的航路管理
  - 2. 编队三状态机动控制 FormUp 阶段航路跟踪逻辑

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统，无任何航路管理相关代码。

- **建议迁移方式**：Clean-room 重实现
  - 按简化版（仅向前搜索）实现。算法卡片参考：[station-keeping-card](../../algorithms/flight-dynamics-station-keeping-card.md) 已逐卡阅读。

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

### FU-002: 航线推进（三维指令输出）
- **关联需求**：REQ-002-PATH-01
- **功能描述**：
  - 沿当前航路段以设定速度推进参考点位置。考虑风速矢量叠加影响，输出 heading_cmd（航向方位角）、altitude_cmd（沿航路段两端高度线性插值的目标高度）、speed_cmd（speed_profile 中对应航路段的期望速度值）。使用 ECS 坐标系下的位移计算。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 航路段索引 | current_leg_index | int | 当前所处航路段 |
    | 2 | 段内进度 | leg_progress | double | [0,1] |
    | 3 | 飞机速度 | V | double | 飞机设定速度 |
    | 4 | 仿真步长 | Δt | double | 时间推进步长 |
    | 5 | 风速 | V_wind | double | 环境风速（含方向） |
    | 6 | 期望航线 | path | vector\<Point\> | 航路点数组（Point 含 _lon/_lat/_alt） |
    | 7 | 速度规划 | speed_profile | vector\<double\> | 每个航路点的期望巡航速度 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 下一时刻参考点位置 | ref_pos_next | Point | 飞机参考点经纬度/高度 |
    | 2 | 期望航向角 | heading_cmd | double | 指向下一航路点的方位角（度） |
    | 3 | 期望高度 | altitude_cmd | double | 航路段两端高度线性插值的目标高度 |
    | 4 | 期望速度 | speed_cmd | vector\<double\> | speed_profile 对应段的期望速度 |

- **AFSIM 参考实现**：
  - 1. 编队三状态机动控制 KeepStation 阶段 ECS 坐标系 P+D+DD 偏差精细控制
  - 2. wsf_six_dof `formation/` 编队动作库

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。altitude_cmd 和 speed_cmd 由人工在 Autopilot PID 确认阶段补充为 PATH-01 输出。

- **建议迁移方式**：Clean-room 重实现
  - 无简化，完整实现。算法卡片参考：[station-keeping-card](../../algorithms/flight-dynamics-station-keeping-card.md) 已逐卡阅读。

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 最大速度 | V_max | double | 硬编码（全局常量） | 速度上限限幅 |
    | 2 | 地球参数 | Earth_Params | struct | 硬编码（全局常量） | 经纬度↔距离转换 |
    | 3 | 速度规划 | speed_profile | vector\<double\> | 配置文件/输入参数 | 每航路点期望速度 |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | sin/cos/sqrt 三角函数和基本运算 |
    | 2 | `Eigen` | 矢量加法/点积、坐标系旋转变换 |

  - 3. 其它模块：无

- **风险等级**：中
- **备注**：地理坐标系下位移计算需正确处理经纬度→距离转换，风速矢量叠加需考虑风向坐标系变换。altitude_cmd 和 speed_cmd 由人工在确认阶段补充。

### FU-003: 剩余航线裁剪
- **关联需求**：REQ-002-PATH-01
- **功能描述**：
  - 从原始航线数组中移除已飞越的航路点，返回剩余未到达的航点序列。基本数组遍历操作，无算法复杂度。
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
  - 1. 无——基本数组操作，function-index.jsonl 中无独立对应函数

- **目标系统当前状态**：❌（缺失）

- **建议迁移方式**：Clean-room 重实现

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：无
  - 2. 数学库：无
  - 3. 其它模块：无

- **风险等级**：低
- **备注**：无算法复杂度，标准 C++ 数组操作。

### FU-004: 推进系统（最简层级）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 简化版推进系统——推力使用线性推力-油门关系（T=δ×Tmax(h)）；燃油消耗使用恒定燃油消耗率（m_fuel=ṁ_const×Δt）；油箱管理简化为单油箱直接消耗模型（CG 固定在油箱中心）。跳过 AFSIM 完整模型的三层查表+spool dynamics+多油箱传输协调。
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
  - 2. `PropulsionSystem::Update` (`WsfSixDOF_PropulsionSystem.cpp:78-249`)——多油箱传输协调

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。当前需求参数不足以支持完整模型，本 FU 采用最简层级简化组合（简1+简2+简3）。

- **建议迁移方式**：Clean-room 重实现（简化版）
  - 简1（线性推力 T=δ×Tmax(h)）+ 简2（恒定燃油率 ṁ=const）+ 简3（单油箱模型）。算法卡片：[jet-engine-card](../../algorithms/flight-dynamics-jet-engine-card.md) + [propulsion-fuel-card](../../algorithms/flight-dynamics-propulsion-fuel-card.md) 已逐卡阅读。

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 最大推力曲线 | T_max(h) | double[] 或 double | 配置文件（AFSIM 默认值） | 线性推力公式 T=δ×T_max(h) |
    | 2 | 恒定燃油流量 | ṁ_const | double | 数据库 | 恒定燃油消耗率 |
    | 3 | 油箱最大容量 | Max_Fuel_Capacity | double | 数据库 | 油箱满度限制 |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | min/max 限幅操作 |
    | 2 | `<algorithm>` | std::clamp |

  - 3. 其它模块：无

- **风险等级**：中
- **备注**：三个简化方案均选中（简1+简2+简3），形成"最简"层级。所有参数已确认来源：T_max(h) 来自配置文件、ṁ_const/Max_Fuel_Capacity 来自数据库。Initial_Fuel 已移除——prev_fuel 每次调用传入，首帧由外部初始化。

### FU-005: 气动模型（仅气动力）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 仅计算气动力的三个分量（升力、阻力、侧力），不计算气动力矩（三个力矩分量全为零）。力矩全部由 SAS 系统（FU-007）提供。使用参考面积、参考长度和动压进行缩放。
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
  - 仅保留气动力三向分量（简2）。算法卡片：[rigidbody-aero-coefficient-card](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md) + [pointmass-aero-card](../../algorithms/flight-dynamics-pointmass-aero-card.md) 已逐卡阅读。

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 参考面积 | S_ref | double | 数据库 | 动压缩放 |
    | 2 | 参考长度 | l_ref | double | 数据库 | 力矩系数缩放 |

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

### FU-006: 自动驾驶仪 PID（完整 20 PID 四通道）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 完整 20 PID 三通道嵌套回路（外侧→中间→内侧），四通道全部激活。横向 BTT：heading_cmd→RollHeadingPID→BankAnglePID→RollRatePID→δ_aileron；YTT 协调：→YawRatePID→BetaPID→δ_rudder；垂直：altitude_cmd→AltitudePID→VertSpeedPID→AlphaPID→δ_elevator；速度：speed_cmd→Speed PID→throttle_cmd。含增益调度（以动压查 PID 增益表）、抗积分饱和（back-calculation anti-windup）、低通滤波导数和前馈偏置。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 期望航向角 | heading_cmd | double | 来自 PATH-01（FU-002） |
    | 2 | 期望高度 | altitude_cmd | double | 来自 PATH-01（FU-002） |
    | 3 | 期望速度 | speed_cmd | vector\<double\> | 来自 PATH-01（FU-002） |
    | 4 | 当前姿态 | prev_posture | Posture | yaw/pitch/roll 角 |
    | 5 | 滚转角速率 | p | double | 绕体轴 x 角速率 |
    | 6 | 俯仰角速率 | q | double | 绕体轴 y 角速率 |
    | 7 | 偏航角速率 | r | double | 绕体轴 z 角速率 |
    | 8 | 当前速度 | prev_velocity | double | 速度标量 |
    | 9 | 攻角 | α | double | 气动参考 |
    | 10 | 侧滑角 | β | double | 气动参考 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 升降舵偏转指令 | δ_elevator | double | [-1,1]，SAS 输入 |
    | 2 | 副翼偏转指令 | δ_aileron | double | [-1,1]，SAS 输入 |
    | 3 | 方向舵偏转指令 | δ_rudder | double | [-1,1]，SAS 输入 |
    | 4 | 油门指令 | throttle_cmd | double | 推进系统输入 |

- **AFSIM 参考实现**：
  - 1. `CommonController::Update` (`wsf_six_dof/source/`)——20 PID 嵌套回路主入口，Bank-To-Turn/Yaw-To-Turn 双模式
  - 2. 各嵌套 PID 实例：RollHeadingPID、BankAnglePID、RollRatePID、YawHeadingPID、YawRatePID、BetaPID、AltitudePID、VertSpeedPID、AlphaPID、SpeedPID 等

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。altitude_cmd 和 speed_cmd 由人工在确认阶段补充为 PATH-01 输出，使 Autopilot PID 四通道现已全部获得上游指令。

- **建议迁移方式**：Clean-room 重实现（完整版）
  - 无简化。算法卡片：[autopilot-pid-card](../../algorithms/flight-dynamics-autopilot-pid-card.md) 已逐卡阅读。

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 各通道 PID 增益 | K_p/K_i/K_d 等 | double[60+] | 配置文件（AFSIM 默认值） | 20 个 PID 各含 K_p/K_i/K_d 等 8 参数，含增益调度表 |
    | 2 | 增益调度控制变量 | ControllingValue | double | 配置文件（AFSIM 默认值） | 以动压（q̄）为主控变量线性插值增益 |
    | 3 | 各通道限幅值 | max_bank 等 | double[10+] | 配置文件（AFSIM 默认值） | 嵌套回路各层输出限幅 |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | sin/cos、atan2、clip |
    | 2 | `Eigen` | Vector3 运算 |

  - 3. 其它模块：如下表所示

    | # | 模块名 | 用途 |
    |---|------|------|
    | 1 | FU-002 | 提供 heading_cmd / altitude_cmd / speed_cmd |
    | 2 | FU-007（SAS） | 消费 δ_commands 输出 |

- **风险等级**：高
- **备注**：⚠️ 与 SAS 明确分工——PID=制导决策（"往哪飞、飞多高、飞多快"），SAS=执行保护（"怎么安全转向"）。两卡已逐卡阅读确认非同一算法。完整 20 PID 参数数量巨大（60+），是最大风险点；建议首轮实现使用 AFSIM 默认增益表。

### FU-007: SAS 姿态控制（控制-稳定解耦）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 三通道（滚转/俯仰/偏航）控制-稳定解耦架构。控制项：从 Autopilot PID 输出的目标角速率指令经一阶跟踪转换为角加速度（α_controls = (ω_cmd - ω_current) / Δt）；稳定项：俯仰/偏航通道使用二阶临界阻尼将攻角/侧滑角驱回零（α_pitch = -α·ω_n² - 2·ω_n·α̇），滚转通道使用一阶滞后平滑；各通道独立限幅后叠加得总旋转加速度。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 当前角速度 | angular_velocity | Vector3 | p/q/r（rad/s） |
    | 2 | 当前姿态角 | attitude | Vector3 | roll/pitch/yaw（deg） |
    | 3 | 控制面指令 | control_command | Vector3 | δ_elevator/δ_aileron/δ_rudder（来自 FU-006） |
    | 4 | 当前速度 | velocity | double | 动压参考 |
    | 5 | 攻角 | α | double | 气动参考 |
    | 6 | 侧滑角 | β | double | 气动参考 |

  - 输出：如下表所示

    | # | 返回值名称 | 返回值符号 | 返回值类型 | 返回值用途 |
    |---|----------|---------|----------|---------|
    | 1 | 角加速度 | angular_accel | Vector3 | p̈/q̈/r̈（rad/s²）, 含限幅保护 |

- **AFSIM 参考实现**：
  - 1. `PointMassFlightControlSystem::CalculateStabilityAugmentation` (`WsfPointMassSixDOF_FlightControlSystem.hpp`)——完整控制-稳定解耦 SAS
  - 2. 控制项：一阶指令跟踪；稳定项：俯仰/偏航二阶临界阻尼 + 滚转一阶滞后

- **目标系统当前状态**：❌（缺失）
  - 目标系统为空系统。

- **建议迁移方式**：Clean-room 重实现（完整版）
  - 无简化。算法卡片：[pointmass-sas-card](../../algorithms/flight-dynamics-pointmass-sas-card.md) 已逐卡阅读。

- **依赖项**：
  - 1. 配置参数（含全局常量与外部配置）：如下表所示

    | # | 名称 | 符号 | 类型 | 来源 | 用途 |
    |---|------|------|------|------|------|
    | 1 | 基准稳定化频率 | ω_n_base | double | 配置文件（AFSIM 默认值） | 二阶临界阻尼频率基准 |
    | 2 | 滚转时间常数 | τ_roll | double | 配置文件（AFSIM 默认值） | 一阶滚转滞后 |
    | 3 | 俯仰时间常数 | τ_pitch | double | 配置文件（AFSIM 默认值） | 二阶临界阻尼 |
    | 4 | 偏航时间常数 | τ_yaw | double | 配置文件（AFSIM 默认值） | 二阶临界阻尼 |
    | 5 | 滚转角加速度限幅 | p̈_max | double | 配置文件（AFSIM 默认值） | 滚转限幅保护 |
    | 6 | 俯仰角加速度限幅 | q̈_max | double | 配置文件（AFSIM 默认值） | 俯仰限幅保护 |
    | 7 | 偏航角加速度限幅 | r̈_max | double | 配置文件（AFSIM 默认值） | 偏航限幅保护 |

  - 2. 数学库：如下表所示

    | # | 库 | 用途 |
    |---|------|------|
    | 1 | `<cmath>` | sin/cos/clip |
    | 2 | `Eigen` | Vector3 运算 |

  - 3. 其它模块：如下表所示

    | # | 模块名 | 用途 |
    |---|------|------|
    | 1 | FU-006（Autopilot PID） | 提供 δ_commands 输入 |

- **风险等级**：低
- **备注**：⚠️ 核心算法为控制-稳定解耦架构，**非 PID 控制**。PID 嵌套回路属于上游 FU-006（Autopilot PID）。两卡分工已在逐卡阅读中确认，不可混淆。

### FU-008: 六自由度积分器（Heun+四元数+欧拉方程）
- **关联需求**：REQ-002-KINEMATICS-02
- **功能描述**：
  - 使用 Heun 预测-校正法（二阶 Runge-Kutta）对飞机进行六自由度时间推进。将合外力（推力+气动力+重力）和合外力矩（气动力矩+SAS角加速度）转化为线加速度和角加速度，通过四元数姿态积分和欧拉转动方程（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz）更新飞行状态。根据补充约束，质量（m）和转动惯量（I）在飞行全程为常量（仅燃油质量随时间衰减）。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 当前位置 | position | Point | 经纬度/高度 |
    | 2 | 当前速度 | velocity | double | 速度标量 |
    | 3 | 当前姿态四元数 | quaternion | Quaternion | 姿态表示（q₀,q₁,q₂,q₃） |
    | 4 | 当前角速度 | angular_velocity | Vector3 | p/q/r（rad/s） |
    | 5 | 合外力 | total_force | Vector3 | F_thrust + F_aero + F_gravity |
    | 6 | 合外力矩 | total_moment | Vector3 | M_aero（来自气动模型和SAS） |
    | 7 | 飞行器质量 | mass | double | m（常量，仅燃油在 FU-004 中衰减） |
    | 8 | 转动惯量张量 | inertia_tensor | Matrix3 | I（常量，含 I_xx/I_yy/I_zz/I_xz） |
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
  - 无简化。算法卡片：[rigid-body-integrator-card](../../algorithms/flight-dynamics-rigid-body-integrator-card.md) + [pointmass-integrator-card](../../algorithms/flight-dynamics-pointmass-integrator-card.md) 已逐卡阅读。

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
    | 2 | `Eigen` | Vector3 / Matrix3 / Quaternion 全量运算 |

  - 3. 其它模块：如下表所示

    | # | 模块名 | 用途 |
    |---|------|------|
    | 1 | FU-004 | 提供 F_thrust |
    | 2 | FU-005 | 提供 F_aero |
    | 3 | FU-007 | 提供 angular_accel |

- **风险等级**：中
- **备注**：欧拉转动方程交叉耦合项（ω×Iω）需正确处理；转动惯量张量非对角项 I_xz 的处理需验证。m 和 I 为飞行全程常量（补充约束），仅燃油质量在 FU-004 中单独衰减。

### FU-009: 航线机动集成层
- **关联需求**：REQ-002-INTEGRATION-03
- **功能描述**：
  - 按顺序调度 PATH-01（航路段映射→航线推进→剩余航线裁剪）→ KINEMATICS-02（推进系统→气动模型→自动驾驶仪 PID→SAS→积分器）→ 输出组装。步长自适应输出：>1s 时输出每秒状态序列，≤1s 时仅输出下一帧状态。纯调度逻辑，无独立算法复杂度。
- **期望接口**：
  - 输入：如下表所示

    | # | 参数名称 | 参数符号 | 参数类型 | 参数用途 |
    |---|----------|---------|----------|---------|
    | 1 | 期望航线 | path | vector\<Point\> | 航路点数组 |
    | 2 | 速度规划 | speed_profile | vector\<double\> | 每航路点期望速度 |
    | 3 | 上一时刻路径 | prev_path | vector\<Point\> | 上一帧位置 |
    | 4 | 上一时刻姿态 | prev_posture | vector\<Posture\> | 上一帧姿态 |
    | 5 | 上一时刻速度 | prev_velocity | vector\<double\> | 上一帧速度 |
    | 6 | 上一时刻油量 | prev_fuel | vector\<double\> | 上一帧燃油 |
    | 7 | 仿真步长 | Δt | double | 时间推进步长 |
    | 8 | 当前时间戳 | t | double | 仿真时间 |
    | 9 | 耗油量 | fuel_consumption_rate | double | 燃油消耗率 |
    | 10 | 风速 | V_wind | double | 环境风速 |
    | 11 | 飞机速度 | V | double | 设定速度 |
    | 12 | 最大速度 | V_max | double | 速度上限 |
    | 13 | 地球参数 | Earth_Params | struct | 坐标转换 |

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
  - 依赖 FU-001~FU-008 全部完成后集成。

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
    | 6 | FU-006 | 自动驾驶仪 PID |
    | 7 | FU-007 | SAS 姿态控制 |
    | 8 | FU-008 | 六自由度积分器 |

- **风险等级**：中
- **备注**：纯调度逻辑，依赖所有子 FU。需在所有子 FU 完成后进行端到端集成测试。

## 4. 优先级排序与阶段建议
- **高优先级（立即实施）**：
  - 1. FU-008（六自由度积分器）——运动学仿真核心，其它模块（推进、气动、SAS）的输出均依赖积分器；可先以简化力模型（常力/零力）验证积分器正确性。
  - 2. FU-001 + FU-002（航线推进）——路径管理核心，与积分器并行的管线入口模块。FU-002 输出三维指令（heading+altitude+speed）为下游 Autopilot PID 提供全部输入。
  - 3. FU-004（推进系统）+ FU-005（气动模型）——为积分器提供力和力矩输入，在积分器验证通过后接入。
  
- **中优先级（后续迭代）**：
  - 1. FU-006（Autopilot PID）——依赖 PATH-01 的 heading/altitude/speed 指令和积分器的飞行状态反馈，参数数量巨大（60+），建议在核心管线稳定后用 AFSIM 默认增益表启动。
  - 2. FU-007（SAS 姿态控制）——依赖 Autopilot PID 输出 δ_commands，与 FU-006 可并行开发后串联。
  - 3. FU-009（集成层）——依赖全部子 FU，需在所有子 FU 完成后进行端到端集成。
  
- **低优先级（可延后）**：
  - 1. FU-003（剩余航线裁剪）——基本数组操作，可在航线推进实现后随时添加。

## 5. 遗留问题与待澄清项

### 已确认（全部解决 ✅）
| # | 项目 | 确认方案 | 影响 FU |
|---|------|---------|---------|
| 1 | 60+ PID 增益参数和各通道限幅值 | 配置文件（AFSIM 默认值） | FU-006 |
| 2 | ω_n_base、τ_roll/pitch/yaw、p̈_max/q̈_max/r̈_max | 配置文件（AFSIM 默认值） | FU-007 |
| 3 | T_max(h) | 配置文件（AFSIM 默认值） | FU-004 |
| 4 | ṁ_const、Max_Fuel_Capacity | 数据库 | FU-004 |
| 5 | S_ref、l_ref | 数据库 | FU-005 |
| — | Initial_Fuel | 已移除——prev_fuel 每次调用传入 | FU-004 |

> **状态**：所有参数缺口已解决。无遗留待澄清项。

## 6. 附录
- 引用文档：
  - 需求规范确认文档：`docs/requirements/REQ_002/2_REQ-002-requirement-formation-move-along-path.md`
  - 功能映射矩阵：`docs/requirements/REQ_002/3_REQ-002-function-mapping-matrix.md`
  - 需求追溯矩阵：`docs/requirements/REQ_002/3_REQ-002-requirement-to-afsim-trace.md`