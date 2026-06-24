# 运动学积分器 — 伪代码参考

> **日期:** 2026-06-10
> **状态:** draft
> **对应算法卡:** flight-dynamics-pointmass-sas-card.md, flight-dynamics-p6dof-heun-integrator-card.md, flight-dynamics-aero-coefficient-model-card.md

## 1. Heun 修正欧拉积分（P6DOF / PointMass 共用框架）

```
Algorithm: heun_integrate(state0, t0, dt, force_sources)
    → IntegrationResult s1
    // Heun 修正欧拉法：二阶预测-校正，每帧执行一次

    // Step A — 在 t = t0 处评估力/力矩（用 ε·dt 避免除零）
    F0, M0 = evaluate_all_forces(force_sources, state0, t0, EPSILON, dt)

    // Step B — 预测步（半隐式欧拉推进到临时中间状态）
    s_pred = copy(state0)
    s_pred = apply_forces_and_moments(s_pred, F0, M0, dt)

    // Step C — 在预测状态处重新评估力/力矩
    F1, M1 = evaluate_all_forces(force_sources, s_pred, t0+dt, EPSILON, dt)

    // Step D — Heun 平均：取两端点力/力矩的算术平均（二阶精度）
    F_avg = (F0 + F1) / 2
    M_avg = (M0 + M1) / 2

    // Step E — 校正步：用平均力/力矩对 *原始* 状态推进（非预测态！）
    s1 = copy(state0)
    s1 = apply_forces_and_moments(s1, F_avg, M_avg, dt)
    s1 = copy_diagnostics_from(s_pred)   // 从预测态拷贝诊断值：升力、阻力、推力

    return s1
```

## 2. 力/力矩评估

```
Algorithm: evaluate_all_forces(sources, state, time, dt) → F_total, M_total
    // 汇总所有力源（气动/推进/起落架/重力），输出体轴系总力总力矩

    F_total_body = [0, 0, 0]   // 体轴系合力 (N)
    M_total_body = [0, 0, 0]   // 体轴系合力矩 (N·m)

    // 2a. 气动力/力矩 — 依赖攻角/侧滑角/马赫数/动压
    alpha, beta, mach, q_bar = compute_aero_state(state, atmosphere)
    F_aero, M_aero = aerodynamics.compute(q_bar, mach, alpha, beta,
                                          alpha_dot, beta_dot, omega_body)
    F_total_body += F_aero
    M_total_body += M_aero

    // 2b. 推进力/力矩 — 发动机推力 + 推力偏心/矢量产生的力矩
    F_prop_wcs, M_prop_body = propulsion.compute(time, dt, state)
    F_prop_body = dcm.wcs_to_body(F_prop_wcs)    // 从地心惯性系转到体轴系
    F_total_body += F_prop_body
    M_total_body += M_prop_body

    // 2c. 起落架力/力矩 — 仅当触地时生效
    if landing_gear is present:
        F_gear, M_gear = landing_gear.compute(state, F_total_body)
        F_total_body += F_gear
        M_total_body += M_gear

    // 2d. 重力 — 作用于质心，方向由 WGS84/球面地球模型确定
    g_direction = gravity.normalized_accel_vector(state.lat, state.lon, state.alt)
    F_grav_wcs = g_direction * state.mass                // 重力 = mg，方向指向地心
    F_grav_body = dcm.wcs_to_body(F_grav_wcs)            // 转到体轴系
    F_total_body += F_grav_body

    return F_total_body, M_total_body
```

## 3. 力和力矩应用（平动 + 转动推进）

```
Algorithm: apply_forces_and_moments(state, F_body, M_body, dt) → new_state
    // 将合力和合力矩转化为平动/转动加速度，并推进运动状态

    mass = state.mass                              // 当前质量 (kg)
    Ixx, Iyy, Izz = state.moment_of_inertia        // 主转动惯量 (kg·m²)

    // 3a. 加速度计算

    // 平动：a = F / m（体轴系），再转到惯性系
    a_body = F_body / mass
    a_wcs = dcm.body_to_wcs(a_body)

    // 过载限幅：防止碰撞/爆炸产生数值尖峰（P6DOF 限制 1000G）
    if |a_body| > MAX_G * g0:
        a_body = a_body * (MAX_G * g0 / |a_body|)

    // 转动：欧拉方程 α_i = M_i / I_ii（三轴解耦，假设惯量积为零）
    alpha_body = [M_body.x / Ixx, M_body.y / Iyy, M_body.z / Izz]

    // 3b. 平动运动学推进
    if spherical_earth:
        // 球面地球：v(t+dt) = v(t) + a·dt，x(t+dt) = x(t) + v(t)·dt + ½a·dt²
        vel_wcs = state.vel_spherical + a_wcs * dt
        pos_spherical = state.pos_spherical + state.vel_spherical * dt
                      + 0.5 * a_wcs * dt^2
    else (WGS84):
        // WGS84 椭球地球：坐标系为 ECEF 地心地固
        vel_wcs = state.vel_wgs + a_wcs * dt
        pos_wgs = state.pos_wgs + state.vel_wgs * dt + 0.5 * a_wcs * dt^2

    // 3c. 转动速率推进
    omega_new = state.omega_body + alpha_body * dt
    // 角增量（用于姿态积分）：Δθ = ω·dt + ½α·dt²
    delta_angle = state.omega_body * dt + 0.5 * alpha_body * dt^2

    // 3d. 姿态积分 — 四元数法（已替代旧的 DCM 连乘）
    q = quaternion_from_dcm(state.dcm)
    q_dot = quaternion_rate(q, omega_new)           // 四元数变化率
    q_new = normalize(q + q_dot * dt)               // 前向欧拉 + 规范化（关键！）
    dcm_new = q_new.to_dcm()

    // 3e. 体轴过载（驾驶员感受到的加速度，扣除重力分量）
    body_accel_g = a_body / g0
    grav_body_g = F_grav_body / mass / g0
    nx = body_accel_g.x - grav_body_g.x   // 前向过载
    ny = body_accel_g.y - grav_body_g.y   // 侧向过载
    nz = body_accel_g.z - grav_body_g.z   // 法向过载（负值 = "拉杆"）

    // 3f. 打包结果
    new_state.pos = pos, new_state.vel = vel_wcs
    new_state.dcm = dcm_new
    new_state.omega_body = omega_new
    new_state.alpha_body = alpha_body
    new_state.nx = nx, new_state.ny = ny, new_state.nz = nz
    return new_state
```

## 4. 四元数姿态积分

```
Algorithm: quaternion_rate(q, omega_body) → q_dot
    // 计算四元数变化率 ᑭ = ½ q ⊗ [0, ω_body]
    // 输入：q — 当前姿态四元数 [w, x, y, z]，标量在前
    //       ω_body — 体轴角速率 [p, q, r] (rad/s)，p=滚转, q=俯仰, r=偏航
    // 输出：q_dot — 四元数时间导数

    // 四元数乘法展开：½ * [w, x, y, z] ⊗ [0, ωx, ωy, ωz]
    q_dot.w = 0.5 * ( -q.x*omega.x - q.y*omega.y - q.z*omega.z )
    q_dot.x = 0.5 * (  q.w*omega.x + q.y*omega.z - q.z*omega.y )
    q_dot.y = 0.5 * (  q.w*omega.y + q.z*omega.x - q.x*omega.z )
    q_dot.z = 0.5 * (  q.w*omega.z + q.x*omega.y - q.y*omega.x )
    return q_dot

Algorithm: quaternion_integrate(q, omega, dt) → q_new
    // 用体轴角速率推进四元数一个时间步长
    // q(t+dt) = normalize(q(t) + q̇(t) · dt)

    q_dot = quaternion_rate(q, omega)
    q_new_raw = q + q_dot * dt          // 前向欧拉迭代
    q_new = normalize(q_new_raw)         // 规范化防止数值漂移（非常重要）
    return q_new
```

## 5. 气动状态计算

```
Algorithm: compute_aero_state(state, atmosphere, wind) → α, β, Mach, q̄, ρ
    // 从运动状态和大气/风场计算气动计算所需的状态量

    // 相对气流速度（体轴系），扣除风的影响
    v_body = state.dcm.wcs_to_body(state.vel_wcs)         // 惯性速 → 体轴系
    wind_body = wind.velocity_at(state.lat, state.lon, state.alt, state.time)
    v_air_body = v_body - wind_body                        // 真空速（体轴系）

    // 气动角计算
    V = |v_air_body|                                        // 真空速标量 (m/s)
    if V > 0:
        α = atan2(v_air_body.z, v_air_body.x)              // 攻角：体轴 z/x 比值的反正切
        β = asin(v_air_body.y / V)                           // 侧滑角：体轴 y 分量与总速的反正弦
    else:
        α = 0, β = 0                                        // 零速时定义为零

    // 大气属性
    ρ = atmosphere.density(state.alt)                       // 空气密度 (kg/m³)
    a_sound = atmosphere.speed_of_sound(state.alt)           // 当地声速 (m/s)
    Mach = V / a_sound                                       // 马赫数
    q̄ = 0.5 * ρ * V²                                         // 动压 (Pa)

    // 气动角变化率（时间差分近似）
    α̇ = (α - state.last_alpha) / dt
    β̇ = (β - state.last_beta) / dt

    return α, β, α̇, β̇, Mach, q̄, ρ
```

## 6. PointMass 旋转增稳算法

```
Algorithm: pointmass_rotation_acceleration(state, flight_controls, aero, dt) → α_total
    // PointMass 的旋转加速度 = 控制项（跟踪指令）+ 稳定项（自然恢复）
    // 这是 PointMass 区别于 P6DOF 刚体模型的核心设计

    // 6a. 控制项 — 跟踪飞行员/自动驾驶仪下达的体轴角速率指令
    ω_cmd_rps = flight_controls.get_commanded_body_rates()  // 从操纵曲线映射得到 (rad/s)
    ω_cur_rps = state.omega_body                            // 当前体轴角速率 (rad/s)

    α_control = (ω_cmd_rps - ω_cur_rps) / dt                // 一阶指令跟踪

    // 按气动能力限幅（随质量减轻而放宽 — 越轻越灵活）
    mass_ratio = state.mass / state.base_mass
    α_limit = aero.max_angular_acceleration / mass_ratio
    for axis in {roll, pitch, yaw}:
        α_control[axis] = clamp(α_control[axis], ±α_limit[axis])

    // 6b. 稳定项 — 模拟飞行器固有的气动静稳定性
    ω_stab = aero.stabilizing_frequencies / sqrt(mass_ratio)

    // 俯仰通道：二阶弹簧-阻尼系统，驱α→0，阻尼比=1（临界阻尼）
    α_pitch_stab = -state.α * ω_stab.pitch² - 2 * ω_stab.pitch * state.α̇

    // 偏航通道：二阶弹簧-阻尼系统，驱β→0，阻尼比=1
    α_yaw_stab   = -state.β * ω_stab.yaw² - 2 * ω_stab.yaw * state.β̇

    // 滚转通道：一阶滞后趋于零（滚转阻尼机制较简单）
    weight = ω_stab.roll * dt / (1 + ω_stab.roll * dt)
    expected_roll = (1 - weight) * state.roll_rate
    α_roll_stab = (expected_roll - state.roll_rate) / dt

    // 6c. 稳定性数值限幅 — 防止大时间步长下数值发散
    α_roll_stab  = clamp(α_roll_stab,  ±|state.roll_rate  / dt|)
    α_pitch_stab = clamp(α_pitch_stab, ±|2/dt² * (-state.α  - state.α̇*dt)|)
    α_yaw_stab   = clamp(α_yaw_stab,   ±|2/dt² * (-state.β  - state.β̇*dt)|)

    // 6d. 总旋转加速度 = 控制 + 稳定（注意偏航通道符号翻转）
    α_total = α_control + [α_roll_stab, α_pitch_stab, -α_yaw_stab]
    return α_total
```

## 7. 气动稳定性导数模型（简化版）

```
Algorithm: stability_derivative_aero(q̄, Mach, α, β, α̇, β̇, ω, aero_tables) → F, M
    // 基于稳定性导数的高维查表气动模型
    // 气动系数 = 静态项（α,β,Mach 3D 查表）+ 动态阻尼项 + 非定常延迟项

    // 参考几何参数
    S = aero_tables.ref_area       // 参考面积 (m²)
    b = aero_tables.span           // 翼展 (m)
    c = aero_tables.chord          // 平均气动弦长 (m)

    // 无量纲化角速率（简化频率法 — 消除速度和尺寸量纲）
    V = sqrt(2 * q̄ / ρ)                           // 真空速 (m/s)
    p_hat = ω.roll  * b / (2*V)                    // 无量纲滚转速率
    q_hat = ω.pitch * c / (2*V)                    // 无量纲俯仰速率
    r_hat = ω.yaw   * b / (2*V)                    // 无量纲偏航速率
    α̇_hat = α̇ * c / (2*V)                           // 无量纲攻角变化率
    β̇_hat = β̇ * b / (2*V)                           // 无量纲侧滑角变化率

    // --- 升力系数 CL ---
    CL = table_lookup(aero_tables.CL, Mach, α, β)                 // 静态升力系数 (3D 表)
       + table_lookup(aero_tables.CL_q, Mach, α) * q_hat          // 俯仰阻尼增量
       + table_lookup(aero_tables.CL_α̇, Mach, α) * α̇_hat         // 攻角延迟（非定常）增量

    // --- 阻力系数 Cd ---
    Cd = table_lookup(aero_tables.Cd, Mach, α, β)                  // 静态阻力系数 (3D 表)

    // --- 侧力系数 CY ---
    CY = table_lookup(aero_tables.CY, Mach, α, β)                 // 静态侧力系数 (3D 表)
       + table_lookup(aero_tables.CY_r, Mach, β) * r_hat          // 偏航阻尼侧力增量
       + table_lookup(aero_tables.CY_β̇, Mach, β) * β̇_hat         // 侧滑延迟（非定常）增量

    // --- 滚转力矩系数 Cl ---
    Cl = table_lookup(aero_tables.Cl, Mach, α, β)                 // 静态滚转力矩系数 (3D 表)
       + table_lookup(aero_tables.Cl_p, Mach) * p_hat             // 滚转阻尼
       + table_lookup(aero_tables.Cl_r, Mach) * r_hat             // 偏航-滚转交叉导数
       + table_lookup(aero_tables.Cl_α̇, Mach) * α̇_hat             // 攻角延迟滚转效应
       + table_lookup(aero_tables.Cl_β̇, Mach) * β̇_hat             // 侧滑延迟滚转效应

    // --- 俯仰力矩系数 Cm ---
    Cm = table_lookup(aero_tables.Cm, Mach, α, β)                 // 静态俯仰力矩系数 (3D 表)
       + table_lookup(aero_tables.Cm_q, Mach) * q_hat             // 俯仰阻尼
       + table_lookup(aero_tables.Cm_α̇, Mach) * α̇_hat             // 攻角延迟俯仰力矩

    // --- 偏航力矩系数 Cn ---
    Cn = table_lookup(aero_tables.Cn, Mach, α, β)                 // 静态偏航力矩系数 (3D 表)
       + table_lookup(aero_tables.Cn_r, Mach) * r_hat             // 偏航阻尼
       + table_lookup(aero_tables.Cn_β̇, Mach) * β̇_hat             // 侧滑延迟偏航力矩

    // --- 气动力（体轴系）---
    // 乘以动压和参考面积得到有量纲力
    F_lift   = q̄ * S * CL    // 升力 (N)，垂直于相对气流方向
    F_drag   = q̄ * S * Cd    // 阻力 (N)，平行于相对气流方向
    F_side   = q̄ * S * CY    // 侧力 (N)

    // （此处需用 α、β 将升力/阻力从风轴系旋转到体轴系）

    // --- 气动力矩 ---
    // 乘以动压、参考面积和参考长度得到有量纲力矩
    M_roll   = q̄ * S * b * Cl    // 滚转力矩 (N·m)，绕体轴 x
    M_pitch  = q̄ * S * c * Cm    // 俯仰力矩 (N·m)，绕体轴 y
    M_yaw    = q̄ * S * b * Cn    // 偏航力矩 (N·m)，绕体轴 z

    return [F_lift, F_drag, F_side], [M_roll, M_pitch, M_yaw]
```

## 8. 必须的数值保护

每条算法实现应包含以下数值保护：

| 保护 | 原因 | 中文说明 |
|------|------|----------|
| `if mass ≤ 0: return zero_accel` | 零质量除零 | 零质量导致加速度计算除零，直接返回零向量 |
| `if V ≤ EPSILON: no aero forces` | 零速度除零 | 零速时无量纲化会除零，跳过气动力计算 |
| `clamp(aero_coeff, ±LIMIT)` | 查表超出范围 | 气动系数查表边界外插可能产生非物理值 |
| `clamp(\|F\|, mass * MAX_G * g0)` | 碰炸尖峰 (P6DOF: 1000G) | 碰撞/爆炸产生的大加速度尖峰需硬限幅 |
| `clamp(\|α_axis\|, angular_limit)` | 角加速度发散 | 大时间步长下软/硬发散需限幅遏制 |
| `normalize(quaternion) after every step` | 四元数漂移 | 每步规范化防止四元数范数偏离 1.0 |
| `if dt ≤ EPSILON: return state unchanged` | 零步长 | 零步长时不做任何更新，直接返回当前状态 |
