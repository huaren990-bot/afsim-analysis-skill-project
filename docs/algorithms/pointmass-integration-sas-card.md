# Algorithm Card — PointMass Six-DOF 积分器与稳定增稳系统 (SAS)

## Metadata

- **Algorithm name**: PointMass Six-DOF Integrator with Stability Augmentation（点质六自由度积分器 / 二阶稳定增稳控制）
- **Domain**: Flight Dynamics / Control Systems — 点质飞行器动力学积分与控制稳定性增稳
- **Date**: 2026-06-10
- **Analyst**: afsim-algorithm-extractor
- **Status**: draft

## Purpose

对"点质量"（PointMass）这一简化六自由度模型进行时间推进。其核心创新在于将**旋转动力学与控制指令解耦**——控制指令（来自飞行员/自动驾驶仪的期望角速率）与物理稳定性（自然恢复力矩 + 阻尼）合并为一个"增稳"旋转加速度系统。这使得模型既能反映基本飞行稳定性，又能避免刚体六自由度模型的完整力矩耦合。

## Source Locations

| File | Symbol | Lines | Evidence level | 中文说明 |
|------|--------|-------|---------------|----------|
| [WsfPointMassSixDOF_Integrator.cpp:46-151](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfPointMassSixDOF_Integrator.cpp) | `PointMassIntegrator::Update()` | 46-151 | source-cited | 积分器主循环 — Heun 预测-校正全流程（质量更新→加速度计算→预测→平均→校正→后处理） |
| [WsfPointMassSixDOF_Integrator.cpp:153-343](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfPointMassSixDOF_Integrator.cpp) | `PointMassIntegrator::CalculateAcceleration()` | 153-343 | source-cited | 加速度计算 — 气动+推进+重力三项力汇总 + 旋转加速度分解为控制+稳定 |
| [WsfPointMassSixDOF_Integrator.cpp:346-394](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfPointMassSixDOF_Integrator.cpp) | `PointMassIntegrator::PropagateUsingAcceleration()` | 346-394 | source-cited | 用加速度推进状态 — 平动加速度→位置/速度更新 + 旋转加速度→角速率/姿态更新 |
| [WsfPointMassSixDOF_FlightControlSystem.hpp:75-108](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfPointMassSixDOF_FlightControlSystem.hpp) | `PointMassFlightControlSystem::GetBodyRateCommands_dps()` | 105-108 | source-cited | 飞控系统输出体轴角速率指令 — 从操纵曲线将杆位移映射为期望角速率 |

## Entry Point & Call Chain

```
// 每一帧从 WsfSimulation 出发 → PointMass Mover → 积分器 → 加速度计算 → 飞控指令
WsfSimulation::Update()                                              // AFSIM 仿真引擎主循环
  → WsfPointMassSixDOF_Mover::Update()                              // PointMass 运动器更新
    → PointMassIntegrator::Update(simTime_ns, dt_sec)              // 积分器入口 — Heun 预测-校正
      → CalculateAcceleration(state, t_last, dt)                   // Heun Step 1: 在 t0 处计算加速度
        → CalculateAeroBodyForceAndRotation()                       //   气动力 + 旋转增稳参数（α_limit_base, ω_stab_base）
        → CalculatePropulsionFM()                                   //   推进力 + 推进旋转加速度
        → NormalizedGravitationalAccelVec()                         //   重力方向矢量
        → FlightControlSystem::GetBodyRateCommands_dps()           //   飞控系统输出期望体轴角速率 (deg/s)
      → PropagateUsingAcceleration(state, dt, g0, a0, α0)          // Heun Step 2: 预测步 — 用 a₀ 推进到临时状态
      → CalculateAcceleration(temp_state, simTime, dt)             // Heun Step 3: 在预测态计算 a₁
      → average(a0, a1)                                             // Heun Step 4: 平均 — 取两端的算术平均值
      → UpdateUsingAcceleration(state, dt, g_avg, a_avg, α_avg)    // Heun Step 5: 校正步 — 用平均加速度对原始状态推进
        → UpdateFuelBurn()                                          //   燃油消耗更新
        → PropagateUsingAcceleration()                              //   推进逻辑同上，使用平均加速度
      → UpdateAeroState()                                           // 后处理：更新 α, β 及变化率
      → CalculateSecondaryParameters()                              // 后处理：更新 LLA、Mach、航向等导出量
```

## Inputs

| Name | Type | Meaning | Units | Source |
|------|------|--------|-------|--------|
| Vehicle state (via `mVehicle`) | `PointMassMover*` | 飞行器全状态，含运动学/质量/气动/推进/飞控 | — | platform |
| `aSimTime_nanosec` | `int64_t` | 当前仿真时间 | ns | simulation clock |
| `aDeltaT_sec` | `double` | 帧时间步长 | s | simulation framework |

## Outputs

| Name | Type | Meaning | Units | Source |
|------|------|--------|-------|--------|
| `kinematicState` (mutated) | `KinematicState&` | 更新后的完整运动状态 | SI/Imperial 混合 | state mutator |
| `lift_lbs, drag_lbs, thrust_lbs` (via state) | double | 气动力/推力诊断值 | lb | state accessors |

## Dependencies

| Dependency | Type | Description | 中文说明 |
|------------|------|-------------|----------|
| `PointMassMover::CalculateCurrentMassProperties()` | method call | 质量/质心/惯量更新 | 燃油消耗后的质量变化影响后续所有加速度计算 |
| `PointMassMover::CalculateAeroBodyForceAndRotation()` | method call | 气动力和旋转增稳参数 | 返回 α_limit_base（气动限幅）和 ω_stab_base（稳定化频率） |
| `PointMassMover::CalculatePropulsionFM()` | method call | 推进系统力和力矩 | 发动机推力及推力矢量产生的旋转加速度 |
| `PointMassFlightControlSystem::GetBodyRateCommands_dps()` | method call | 飞行员/自动驾驶仪角速率指令 | 从操纵杆位移曲线映射得到三轴期望角速率 |
| `KinematicState::NormalizedGravitationalAccelVec()` | method | 重力方向 | 给定纬度/经度/高度，返回归一化重力方向矢量 |
| `cREFERENCE_GRAV_ACCEL_MPS2` (9.80665) | constant | 标准重力加速度 | 将英制 lb 力转换为公制加速度的转换因子 |
| `UtMath::Limit()` | utility | 数值限幅 | `clamp(value, ±limit)` — 防止数值发散 |

## Mathematical Form

### Heun's Modified Euler (与 P6DOF 相同框架)

**Step 1** — 在 `t = t_last` 计算初始加速度 $\vec{a}_0, \vec{\alpha}_0, \vec{g}_0$

**Step 2** — 预测步：用 $\vec{a}_0, \vec{\alpha}_0, \vec{g}_0$ 推进到临时状态

**Step 3** — 在临时状态计算 $\vec{a}_1, \vec{\alpha}_1, \vec{g}_1$

**Step 4** — 平均并校正：
$$\vec{a}_{avg} = \frac{\vec{a}_0 + \vec{a}_1}{2}, \quad \vec{\alpha}_{avg} = \frac{\vec{\alpha}_0 + \vec{\alpha}_1}{2}, \quad \vec{g}_{avg} = \frac{\vec{g}_0 + \vec{g}_1}{2}$$

### 旋转加速度模型（核心创新）

旋转加速度由**两项叠加**：

#### 1. 控制项 (Controls) — 一阶指令跟踪

飞行控制系统给出期望角速率 $\vec{\omega}_{cmd}$ (deg/s → rad/s)，积分器将其转化为指令角加速度：

$$\vec{\alpha}_{controls} = \frac{\vec{\omega}_{cmd} - \vec{\omega}_{current}}{dt_{mover}}$$

然后各轴独立限幅：
$$\alpha_i = \text{clamp}\left(\alpha_i, \pm |\alpha_{limit,i}|\right)$$

其中限幅值来自气动计算：$\vec{\alpha}_{limit} = \frac{\vec{\alpha}_{limit,base}}{m_{fraction}}$（质量减小 → 限幅增大 — 越轻越敏捷）。

#### 2. 稳定项 (Stability/Plant) — 自然恢复 + 阻尼

##### 俯仰/偏航通道：二阶系统（带阻尼的弹簧-质量模型）

$$a_{pitch,stab} = -\alpha \cdot \omega_n^2 - 2 \cdot \omega_n \cdot \dot{\alpha}$$

$$a_{yaw,stab} = -\beta \cdot \omega_n^2 - 2 \cdot \omega_n \cdot \dot{\beta}$$

其中 $\omega_n$（stabilizing frequency，稳定化固有频率）由气动分析提供，等效于**上升静稳定性 + 气动阻尼**。阻尼系数恒为 2·ωₙ（临界阻尼）— 这意味着系统以最快速度回到零且不产生过冲。

除以质量比率：
$$\omega_n = \frac{\omega_{n,base}}{\sqrt{m_{fraction}}}$$

##### 滚转通道：一阶滞后（加权平滑）

$$\text{weight} = \frac{\omega_n \cdot dt}{1 + \omega_n \cdot dt}$$

$$\dot{p}_{expected} = (1 - \text{weight}) \cdot p$$

$$\alpha_{roll,stab} = \frac{\dot{p}_{expected} - p}{dt}$$

滚转力学的物理机制比俯仰/偏航简单（主要是翼展方向的速度分布变化），因此用一阶滞后即可近似。

#### 3. 稳定性限幅（防止数值发散）

大时间步长下稳定加速度可能过大导致发散，故对每个通道设置限幅：

$$\alpha_{roll,max} = \frac{|p|}{dt}$$

$$\alpha_{pitch,max} = \frac{2}{dt^2}|-\alpha - \dot{\alpha}\cdot dt|$$

$$\alpha_{yaw,max} = \frac{2}{dt^2}|-\beta - \dot{\beta}\cdot dt|$$

物理意义：限幅 = 一步内将速度归零所需加速度的 2 倍（安全裕量）。

#### 4. 总旋转加速度

$$\vec{\alpha}_{total} = \vec{\alpha}_{controls} + \vec{\alpha}_{stability}$$

### 体轴过载计算

平动加速度减去重力分量得到驾驶员感受到的体轴过载：

$$N_{i,g} = \frac{a_{translational,i}}{g_0} - g_{body,i}$$

其中 $i = x, y, z$（前、右、下）。

### 平动加速度限幅

$$|\vec{a}_{translational}| \leq 1000 \cdot g_0$$

## Pseudocode

```text
algorithm PointMass_Integrate(object, simTime, dt):
    // PointMass 积分器主循环 — Heun 修正欧拉法

    // 1. 准备：获取质量属性和当前运动状态
    mass_props = object.calculate_mass_properties()   // 含燃油消耗后的质量/质心/转动惯量
    initial_state = copy(object.kinematic_state)      // 保存原始状态（校正步需要用到）
    temp_state = copy(initial_state)                  // 临时状态用于预测步

    // 2. Heun Step 1: 在 t = t0 处计算力/力矩 → 加速度
    g0, a0, α0 = calculate_acceleration(temp_state, t_last, dt)

    // 3. Heun Step 2: 预测步 — 用加速度推进到临时中间状态
    temp_state = propagate(temp_state, dt, g0, a0, α0)

    // 4. Heun Step 3: 在预测态 (t = t1) 重新计算加速度
    g1, a1, α1 = calculate_acceleration(temp_state, simTime, dt)

    // 5. Heun 平均：取两个端点加速度的算术平均值 → 二阶精度
    g_avg = (g0 + g1) * 0.5     // 平均重力加速度
    a_avg = (a0 + a1) * 0.5     // 平均平动加速度
    α_avg = (α0 + α1) * 0.5     // 平均旋转加速度

    // 6. Heun Step 4: 校正步 — 用平均加速度对 *原始状态* 推进（不用预测态！）
    state = object.kinematic_state                     // 取回原始状态
    state.copy_diagnostics_from(temp_state)            // 从预测态拷贝诊断值（升力/阻力/推力）
    state = update_using_accel(state, simTime, dt, g_avg, a_avg, α_avg)
        // 包含：燃油消耗 → 平动+转动推进（同步骤3逻辑，但输入为平均加速度）

    // 7. 后处理
    if freeze.testing_no_alpha: state.remove_alpha()   // 测试模式：去除攻角效应
    state.update_aero_state()                           // 更新 α, β, α̇, β̇（用于下一帧）
    state.calculate_secondary_params()                  // 更新 LLA、Mach、动压、航向、过载等导出量

algorithm calculate_acceleration(state, simTime, dt) → (g_vec, a_trans, α_rot):
    // 汇总所有力源并计算平动+旋转加速度
    mass = mass_properties.mass                         // 当前质量 (slug)

    // --- 气动力及旋转参数 ---
    aero_lift, aero_drag, aero_side, α_limit_base, ω_stab_base = object.calc_aero()
    total_force_body = aero_lift + aero_drag + aero_side  // 体轴系总气动力

    // --- 推进力 ---
    inertial_thrust, thrust_rot_accel = object.calc_propulsion(simTime, dt, state)
    thrust_body = state.body_from_wcs(inertial_thrust)     // 从地心惯性系转到体轴系
    total_force_body += thrust_body
    α_limit_base += thrust_rot_accel                        // 推力矢量增加旋转限幅

    // --- 重力 ---
    gravity_wcs = state.normalized_gravity_vec() * mass    // 重力 = mg，方向指向地心
    gravity_body = state.body_from_wcs(gravity_wcs)         // 转到体轴系
    total_force_body += gravity_body
    g_accel_body = gravity_body / mass                      // 重力加速度（体轴系，g 为单位）

    // --- 平动加速度 ---
    a_trans = total_force_body / mass * G0                  // 体轴加速度 (m/s²)

    // === 旋转加速度模型 = 控制项 + 稳定项 ===

    // 质量比率影响：越轻越敏捷（限幅增大，稳定化频率升高）
    mass_fraction = mass / base_mass                        // 质量比率（当前质量 ÷ 基准质量）
    α_limit = α_limit_base / mass_fraction                  // 旋转限幅随质量减小而增大
    ω_stab = ω_stab_base / sqrt(mass_fraction)              // 稳定化频率随质量减小而升高

    // --- 控制项：跟踪飞行员/自动驾驶仪的角速率指令 ---
    ω_cmd_rps = flight_controls.get_body_rate_commands_dps() * DEG_TO_RAD
    α_controls = (ω_cmd_rps - current_ω) / mover_dt         // 一阶指令跟踪
    for i in {0,1,2}: α_controls[i] = clamp(α_controls[i], ±α_limit[i])

    // --- 稳定项：模拟飞行器固有的静稳定性和气动阻尼 ---
    // 俯仰通道：二阶系统（阻尼比=1，临界阻尼），驱 α→0
    α_pitch_stab = -α * ω_stab_pitch² - 2 * ω_stab_pitch * α_dot
    // 偏航通道：二阶系统（阻尼比=1，临界阻尼），驱 β→0
    α_yaw_stab   = -β * ω_stab_yaw²  - 2 * ω_stab_yaw  * β_dot
    // 滚转通道：一阶滞后平滑趋于零（滚转力学较简单）
    weight = ω_stab_roll * dt / (1 + ω_stab_roll * dt)      // 滤波权重
    expected_p = (1 - weight) * current_p                     // 期望滚转速率（向零平滑过渡）
    α_roll_stab = (expected_p - current_p) / dt               // 一阶滞后转化为等效加速度

    // --- 稳定性数值限幅：防止大时间步长下发散 ---
    α_roll_stab  = clamp(α_roll_stab,  ±|current_p / dt|)
    α_pitch_stab = clamp(α_pitch_stab, ±|2/dt² * (-α - α_dot*dt)|)
    α_yaw_stab   = clamp(α_yaw_stab,   ±|2/dt² * (-β - β_dot*dt)|)

    // --- 总旋转加速度 = 控制 + 稳定（偏航通道符号翻转）---
    α_rot = α_controls + [α_roll_stab, α_pitch_stab, -α_yaw_stab]

    return g_accel_body, a_trans, α_rot
```

## Variable Mapping

| Code variable | Math symbol | Meaning | 中文说明 |
|--------------|-------------|---------|----------|
| `moverTimestep_sec` / `aDeltaT_sec` | $dt$ | 积分步长 (s) | 通常 = 1/60 s（仿真帧率倒数） |
| `commandedRotationRates_rps` | $\vec{\omega}_{cmd}$ | 期望体轴角速率 (rad/s) | 来自飞行员/自动驾驶仪 — 飞控系统将杆位移映射为角速率 |
| `currentRotationRates_rps` | $\vec{\omega}_{current}$ | 当前体轴角速率 (rad/s) | 当前帧的实测体轴角速率 |
| `rotationalAccelControls_rps2` | $\vec{\alpha}_{controls}$ | 控制命令角加速度 (rad/s²) | 一阶指令跟踪的产物 — 驱动当前角速率趋近期望角速率 |
| `massFraction` | $m_{frac} = m/m_0$ | 质量比率 | 越小的质量比率 → 越敏捷（限幅增大、稳定化频率升高） |
| `stabilizingFrequency_rps` | $\omega_n$ | 气动稳定化固有频率 (rad/s) | 由飞行器气动设计决定 — 决定了稳定性的"弹性系数" |
| `alpha_rad` / `beta_rad` | $\alpha, \beta$ | 攻角/侧滑角 (rad) | 气动角 — 稳定项的目标是将其驱回零 |
| `alphaDot_rps` / `betaDot_rps` | $\dot{\alpha}, \dot{\beta}$ | 攻角/侧滑角变化率 (rad/s) | 稳定项的"阻尼"分量依赖于此 |
| `rollRate_rps` | $p$ | 体轴滚转角速率 (rad/s) | 滚转通道用一阶滞后而非二阶振子 |
| `rotationalAccelStability_rps2` | $\vec{\alpha}_{stability}$ | 稳定增稳角加速度 (rad/s²) | 俯仰/偏航为二阶弹簧阻尼，滚转为一阶滞后 |
| `cREFERENCE_GRAV_ACCEL_MPS2` (9.80665) | $g_0$ | 标准重力加速度 (m/s²) | 英制 lb 力 → 公制加速度的转换因子 |
| `mStickBack` / `mStickRight` / `mRudderRight` | — | 操纵杆位置 (归一化) | 飞行员输入 — 通过操纵曲线映射为期望角速率 |
| `mStickBackCurvePtr` | — | 杆位移 → 俯仰角速率 (deg/s) 映射曲线 | Lookup table：将杆位置映射为期望俯仰速率 |
| `mThrottleMil` / `mThrottleAb` | — | 军用推力/加力推力油门位置 | 发动机油门输入 — 控制推力输出大小 |

## Edge Cases

1. **零质量**：`CalculateAcceleration` 中 mass ≤ 0 时直接返回零向量，不更新 — 防御性编程
2. **零车辆指针**：所有函数入口检查 `mVehicle == nullptr`，提前返回 — 防止空指针崩溃
3. **空飞控系统**：`flightControls == nullptr` 时跳过控制项，仅执行稳定项 — 此时飞行器无外部操纵输入
4. **零时间步长**：稳定项的数值限幅公式保证 $dt \to 0$ 时不发散（因为限幅分母中有 dt）
5. **极端角速率**：起落架摩擦状态 (`FrictionHoldingStill`) 时角速率强制归零 — 地面静止保护
6. **1000G 限幅**：平动加速度上限为 $1000 \cdot g_0$，防止碰撞/爆炸尖峰
7. **控制角加速度限幅**：由空气动力学计算的 `maximumAngularAcceleration` 决定上限 — 保证指令不超过物理能力

## Portability Assessment

- **Score**: Medium-High
- **Reason**: 旋转加速度分解为"控制 + 稳定"的设计是 PointMass 的核心，可用标准公式重实现。控制项是标准一阶跟踪（P 控制），稳定项是标准二阶阻尼振子 + 一阶滚转滞后。不依赖气动系数查表（稳定化频率和气动限幅由外部提供即可）。
- **What can be extracted directly**: 旋转加速度模型（控制+稳定项拆分）、稳定性数值限幅策略、Heun 积分框架
- **What should be rewritten**:
  - 与 `PointMassMover` / `KinematicState` / `ForceAndRotationObject` 的解耦
  - 稳定化频率 $\omega_n$ 需由外部气动分析或用户指定
  - `CalculateAeroBodyForceAndRotation` 的实际查表逻辑需替换
  - 操纵曲线 (`UtTable::Curve`) 需替换为自有多维插值

## Validation Plan

1. **纯控制模式** (stab=0)：给定常值 $\vec{\omega}_{cmd}$，验证角速率在一步后收敛到指令值
2. **纯稳定模式** (controls=0, 初始 α=5°)：验证攻角以二阶振子方式衰减到 0°，阻尼比为 1（临界阻尼）
3. **滚转一阶滞后** (controls=0, 初始 p=10°/s)：验证滚转速率按一阶指数衰减，时间常数 $\tau = 1/\omega_{n,roll}$
4. **质量减少 → 敏捷性增加**：半质量时稳定化频率应为 2×，限幅应为 2×
5. **单位脉冲响应**：给定 $\omega_{cmd}=[1,0,0]$ 持续一帧，验证峰值角速率不超过限幅
6. **与 PointMass 原生输出重现**：相同输入条件下比较原生与重实现结果
