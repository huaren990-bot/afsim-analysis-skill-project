# Algorithm Card — P6DOF Heun 积分器

## Metadata

- **Algorithm name**: P6DOF Heun's Modified Euler Integrator（P6DOF Heun 修正欧拉积分器）
- **Domain**: Flight Dynamics / Numerical Integration — 飞行器六自由度运动方程数值积分
- **Date**: 2026-06-10
- **Analyst**: afsim-algorithm-extractor
- **Status**: draft

## Purpose

对飞行器/导弹在三维空间中的平移和旋转运动进行时间推进。采用 Heun 修正欧拉法（二阶 Runge-Kutta 预测-校正），以及四元数姿态积分，在 AFSIM 仿真主循环中每帧更新一次运动状态。

## Source Locations

| File | Symbol | Lines | Evidence level | 中文说明 |
|------|--------|-------|---------------|----------|
| [P6DofIntegrator.hpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofIntegrator.hpp) | `P6DofIntegrator::Update()` | 36-47 | source-cited | 积分器主入口声明 — 接收飞行器对象、仿真时间和步长 |
| [P6DofIntegrator.cpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofIntegrator.cpp) | `P6DofIntegrator::Update()` | 31-115 | source-cited | 积分器主循环实现 — Heun 预测-校正全流程（质量更新→预测→平均→校正→后处理） |
| [P6DofIntegrator.cpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofIntegrator.cpp) | `P6DofIntegrator::CalculateFM()` | 117-269 | source-cited | 力/力矩汇总 — 依次计算气动/推进/起落架/重力四项，输出参考点与质心的合力和合力矩 |
| [P6DofIntegrator.cpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofIntegrator.cpp) | `P6DofIntegrator::PropagateUsingFM()` | 281-396 | source-cited | 半隐式欧拉推进 — 将力/力矩转化为加速度，执行平动和转动运动学推进（含 1000G 限幅） |
| [P6DofIntegrator.cpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofIntegrator.cpp) | `P6DofIntegrator::PropagateRotation()` | 705-836 | source-cited | 转动传播 — 角速率推进 + 四元数姿态积分（已替代弃用的 DCM 连乘法） + 偏航阻尼器 |
| [P6DofIntegrator.cpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofIntegrator.cpp) | `P6DofIntegrator::PropagateTranslationSphericalEarth()` | 427-558 | source-cited | 球面地球平动 — 恒定半径球面地球模型下的位置/速度推进（含冻结标志处理） |
| [P6DofIntegrator.cpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofIntegrator.cpp) | `P6DofIntegrator::PropagateTranslationWGSEarth()` | 561-702 | source-cited | WGS84椭球地球平动 — WGS84 ECEF 坐标系下的位置/速度推进（高保真场景用） |

## Entry Point & Call Chain

```
// 每一帧的仿真主循环从 WsfSimulation 出发，途经 P6DOF Mover 进入积分器
WsfSimulation::Update()                                      // AFSIM 仿真引擎主循环，每帧调用
  → WsfP6DOF_Mover::Update()                                // P6DOF 运动器更新 — 平台生命周期中的运动学推进
    → P6DofIntegrator::Update(vehicle, simTime_ns, dt_sec)  // Heun 积分器入口 — 执行完整的预测-校正流程
      → CalculateFM()        // 第一步：计算当前力/力矩（气动+推进+起落架+重力）
      → PropagateUsingFM()   // 第二步：预测步 — 用 F₀ 推进到临时中间状态
      → CalculateFM()        // 第三步：在预测态重新计算力/力矩 F₁
      → average(F0, F1)      // 第四步：Heun 平均 — 取 F₀ 和 F₁ 的算术平均值
      → UpdateUsingFM()      // 第五步：校正步 — 用平均力/力矩对原始状态推进
        → UpdateFuelBurn()   // 燃油消耗更新
        → PropagateUsingFM() // 同上推进逻辑，使用平均力/力矩
      → calculate_rates()    // 后处理：更新 α_dot, β_dot 变化率
      → calculate_secondary_params() // 后处理：更新 LLA、Mach、动压、航向等导出量
```

## Inputs

| Name | Type | Meaning | Units | Source |
|------|------|--------|-------|--------|
| `aObject` | `P6DofVehicle*` | 飞行器对象（含质量属性/气动对象/推进系统/起落架） | — | mover |
| `aSimTime_nanosec` | `int64_t` | 当前仿真时间 | ns | simulation clock |
| `aDeltaT_sec` | `double` | 帧时间步长 | s | simulation framework |

## Outputs

| Name | Type | Meaning | Units | Source |
|------|------|--------|-------|--------|
| `kinematicState` (mutated) | `P6DofKinematicState&` | 更新后的完整运动状态：位置(WGS84/球坐标)、速度、姿态DCM、角速率、攻角/侧滑角、马赫数、动压... | SI/Imperial 混合 | state mutator |
| For debugging: `lift_lbs`, `drag_lbs`, `thrust_lbs`, `moment_ftlbs` | double, UtVec3dX | 气动/推力/力矩诊断值 | lb, ft·lb | state accessors |

## Internal State (via P6DofKinematicState)

| Variable | Meaning | Units | 中文说明 |
|----------|---------|-------|----------|
| `mWGS84_pos` / `mSpherical_pos` | 惯性位置 | m | WGS84 ECEF 或球面地心惯性系下的三维坐标 |
| `mWGS84_vel` / `mSpherical_vel` | 惯性速度 | m/s | 对应坐标系下的三维速度矢量 |
| `mDCM` | 体轴到 NED 方向余弦矩阵 | — | 3×3 旋转矩阵，将体轴系矢量旋转到北-东-地导航系 |
| `mOmega` | 体轴角速率 (roll/pitch/yaw) | rad/s | 绕体轴 x(滚)/y(俯)/z(偏) 的旋转角速率 |
| `mOmegaDot` | 体轴角加速度 | rad/s² | 体轴角速率的导数 — 由力矩/转动惯量得出 |
| `mInertialAccel` | 惯性加速度 | m/s² | WGS84/球面惯性系下的平动加速度矢量 |

## Dependencies

| Dependency | Type | Description | 中文说明 |
|------------|------|-------------|----------|
| `P6DofVehicle::CalculateCurrentMassProperties()` | method call | 计算当前质量/质心/转动惯量 | 燃油消耗后更新质量属性，影响后续所有力/力矩到加速度的换算 |
| `P6DofVehicle::CalculateAeroBodyFM()` | method call | 气动力和力矩（查表+稳定性导数） | 依赖攻角/侧滑角/马赫数，计算升力/阻力/侧力/力矩 |
| `P6DofVehicle::CalculatePropulsionFM()` | method call | 推进系统力和力矩 | 发动机推力 + 推力偏心/矢量力矩，输出在惯性系 |
| `P6DofVehicle::CalculateLandingGearFM()` | method call | 起落架地面接触力 | 仅当触地时生效，包含地面反力和摩擦力 |
| `P6DofVehicle::UpdateFuelBurn()` | method call | 燃油消耗更新 | 根据推力水平和发动机油耗特性更新剩余燃油 |
| `P6DofKinematicState::NormalizedGravitationalAccelVec()` | static method | 重力加速度方向（WGS84或球面地球） | 返回单位重力方向矢量，纬度越高越偏向地心 |
| `UtQuaternion` | external class | 四元数运算（姿态积分） | 四元数乘法、求速率、规范化 — 用于替代弃用的 DCM 连乘 |
| `P6DofFreezeFlags` | config dependency | 冻结标志（测试/调试用） | 可独立冻结位置/高度/速度/姿态的某个维度 |

## Mathematical Form

### Heun's Modified Euler Method（二阶预测-校正）

**Step 1 — 计算初始力/力矩 F₀**（在 `t = t_last` 处）：
计算气动、推进、起落架、重力四项的合力与合力矩。

**Step 2 — 预测步（PropagateUsingFM）**：
使用 **半隐式欧拉** 推进到临时中间状态：

$$\vec{v}_{p} = \vec{v}_0 + \vec{a}_0 \cdot \Delta t$$

$$\vec{x}_{p} = \vec{x}_0 + \vec{v}_0 \cdot \Delta t + \frac{1}{2} \vec{a}_0 \cdot \Delta t^2$$

$$\vec{\omega}_{p} = \vec{\omega}_0 + \vec{\alpha}_0 \cdot \Delta t$$

姿态四元数：
$$\Delta\vec{\theta} = \vec{\omega}_0 \cdot \Delta t + \frac{1}{2} \vec{\alpha}_0 \cdot \Delta t^2$$
$$q_p = \text{normalize}\left(q_0 + \dot{q}(\vec{\omega}_0) \cdot \Delta t\right)$$

**Step 3 — 计算预测态力/力矩 F₁**（在 `t = t_now` 处）。

**Step 4 — 平均**：
$$\vec{F}_{avg} = \frac{\vec{F}_0 + \vec{F}_1}{2}, \quad \vec{M}_{avg} = \frac{\vec{M}_0 + \vec{M}_1}{2}$$

**Step 5 — 校正步（UpdateUsingFM）**：用平均力/力矩对**原始状态**（不是预测态！）做半隐式欧拉推进。

### 平动方程

惯性加速度（英制→公制转换）：
$$\vec{a}_{inertial} = g_0 \cdot \frac{\vec{F}_{total\_inertial}}{m}$$

其中 $g_0 = 9.80665 \text{ m/s}^2$（将英制 lb 力转换为公制 m/s² 加速度的关键常数）。

### 转动方程

欧拉方程（分别绕三轴，假设惯量积为零）：
$$\alpha_x = \frac{M_x}{I_{xx}}, \quad \alpha_y = \frac{M_y}{I_{yy}}, \quad \alpha_z = \frac{M_z}{I_{zz}}$$

### 四元数姿态积分（替代已弃用的 DCM 连乘）

体轴角速率 $\vec{\omega}_{body}$ → 四元数速率：
$$\dot{q} = \frac{1}{2} q \otimes [0, \vec{\omega}_{body}]$$
$$q(t+\Delta t) = \text{normalize}\left(q(t) + \dot{q} \cdot \Delta t\right)$$

> 每步规范化是**必须的** — 不规范化会导致四元数范数漂移，姿态逐渐失真。

### 力/力矩限幅（防止数值尖峰）

- **最大过载限制**：$|\vec{F}| \leq m \cdot G_{max}$，其中 $G_{max} = 1000$ — 防止碰撞/爆炸产生天文数字的力
- **最大角加速度限制**：$|M_i| \leq I_{ii} \cdot \dot{\omega}_{max}$，其中 $\dot{\omega}_{max} = 100 \text{ rev/s}^2$

### 地球模型

两种地球模型，通过 `P6DofKinematicState::UseSphericalEarth()` 选择：
- **球面地球**（简单弹道导弹）：恒定半径 $R = 6366707.0 \text{ m}$
- **WGS84 椭球地球**（高保真）：`UtEntity` 标准 WGS84 坐标变换

## Pseudocode

```text
algorithm P6DOF_Heun_Integrate(object, simTime, dt):
    // Heun 修正欧拉法：二阶预测-校正，每帧执行一次

    // 1. 准备：获取飞行器当前质量属性和运动状态
    mass_props = object.calculate_mass_properties()   // 含燃油消耗后的质量/质心/转动惯量
    state = object.kinematic_state                    // 当前帧的运动状态（位置/速度/姿态/角速率）
    atmosphere = object.atmosphere                    // 大气模型（密度/声速/风场）

    // 2. 在 t=t0 处计算初始力/力矩 F₀
    //    用 ε·dt ≈ 1e-12 代替 0 以避免求取气动状态时的除零
    F0_RP, F0_CM = calculate_FM(object, state, t_last, EPSILON)

    // 3. 预测步：用 F₀ 推进到临时中间状态（半隐式欧拉）
    temp_state = copy(state)
    propagate_using_FM(object, temp_state, mass_props, dt, F0_RP, F0_CM)
        // 平动：惯性加速度 a = g₀ × (F_total / m)
        a_inertial = g0 * (F_total_inertial / mass)    // m/s²
        v_p = v0 + a_inertial * dt                     // 速度预测值
        x_p = x0 + v0*dt + 0.5*a_inertial*dt^2         // 位置预测值（半隐式欧拉）
        // 转动：欧拉方程 α_i = M_i / I_ii
        α = M / I_moment                                // rad/s²
        ω_p = ω0 + α * dt                               // 角速率预测值
        // 姿态：四元数积分（已替代弃用的 DCM 连乘法）
        Δθ = ω0*dt + 0.5*α*dt^2                         // 角增量 (rad)
        ω_new = ω0 + α*dt                               // 新的体轴角速率
        q_new = normalize(q0 + q_rate(ω0) * dt)         // 四元数推进 + 规范化

    // 4. 在预测态 (t=t1) 重新计算力/力矩 F₁
    F1_RP, F1_CM = calculate_FM(object, temp_state, simTime, EPSILON)

    // 5. Heun 平均：取两个端点力/力矩的算术平均 → 达到二阶精度
    F_avg_RP = average(F0_RP, F1_RP)
    F_avg_CM = average(F0_CM, F1_CM)

    // 6. 校正步：用平均力/力矩对 *原始状态* 推进（不用预测态！）
    state.set_lift_drag(...) = temp_state values  // 从预测态拷贝诊断值
    update_using_FM(object, state, mass_props, simTime, dt, F_avg_RP, F_avg_CM)
        // 包含：燃油消耗 → 平动+转动推进（同步骤3，但用平均力/力矩）

    // 7. 后处理：计算导出量和变化率
    if freeze_flags.no_alpha: state.remove_alpha()  // 测试模式：去除攻角效应
    state.calculate_rates()                          // 更新 α_dot, β_dot
    state.calculate_secondary_params()               // 更新 LLA, Mach, 动压, 航向等
```

## Variable Mapping

| Code variable | Math symbol | Meaning | 中文说明 |
|--------------|-------------|---------|----------|
| `aDeltaT_sec` | $\Delta t$ | 积分步长 (s) | 通常 = 1/60 s（仿真帧率的倒数） |
| `cGravitationAccel_mps2` (9.80665) | $g_0$ | 标准重力加速度 (m/s²) | 将英制 lb 力转换为公制加速度的转换因子 |
| `currentMass_lbs` / `currentMass_lbm` | $m$ | 质量 (lb = slug) | 注意：lb 与 slug 共享变量名，实际是 slug 单位 |
| `aForcesMomentsAtRP` | $\vec{F}_{RP}, \vec{M}_{RP}$ | 参考点处的合力和合力矩 | RP = Reference Point，通常为机体几何参考点 |
| `aForcesMomentsAtCM` | $\vec{F}_{CM}, \vec{M}_{CM}$ | 质心处的合力和合力矩 | CM = Center of Mass，重力作用于此而非 RP |
| `Ixx_slugft2, Iyy_slugft2, Izz_slugft2` | $I_{xx}, I_{yy}, I_{zz}$ | 主转动惯量 (slug·ft²) | 仅用对角线元素，假设惯量积为零 |
| `inertialAccel_mps2` | $\vec{a}_{inertial}$ | 惯性加速度 (m/s²) | 地心惯性系下的平动加速度 |
| `rotationalAccel_rps2` | $\vec{\alpha}$ | 角加速度 (rad/s²) | 绕体轴的角加速度 — 由力矩 / 转动惯量得出 |
| `mOmega` | $\vec{\omega}$ | 体轴角速率 (rad/s) | [roll_rate, pitch_rate, yaw_rate] |
| `mOmegaDot` | $\dot{\vec{\omega}}$ | 体轴角加速度 (rad/s²) | 角速率的导数 |
| `mDCM` | $\mathbf{C}_{b/n}$ | 体轴到 NED 的方向余弦矩阵 | 3×3 正交矩阵，行列式 = 1 |
| `delAng` | $\Delta\vec{\theta}$ | 角增量 (rad) | 本帧内的角度旋转量 |
| `attitudeQuaternion` | $q$ | 姿态四元数 | [w, x, y, z] 标量在前约定 |
| `cMaxG` (1000.0) | $G_{max}$ | 最大过载限制 | 硬限幅：防止碰撞/爆炸产生尖峰力 |
| `cMaxOmegaDot_rps` | $\dot{\omega}_{max}$ | 最大角加速度限制 | 100 rev/s² ≈ 3600 rad/s² |

## Edge Cases

1. **零质量**：`CalculateFM` 中调用 `GetMass_lbs()`；若质量为 0，力/力矩会被除零——由上层保证质量 > 0
2. **零时间步长**：用 `cEPSILON_SIMTIME_SEC` (≈1e-12) 代替 0 计算初始 F&M，避免零除
3. **冻结标志**：测试模式下可单独冻结位置/高度/速度/姿态，对应跳过平动/转动更新
4. **起落架静止摩擦**：`PropagateRotation` 中若起落架摩擦保持静止，角速率 x/z 分量清零
5. **简单偏航阻尼器**：`UseSimpleYawDamper` 时用侧滑角直接计算偏航率（β → yaw_rate = β/dt），忽略转动动力学
6. **力/力矩限幅**：1000G 过载上限、100 rev/s² 角加速度上限防止数值尖峰

## Portability Assessment

- **Score**: Medium
- **Reason**: 核心算法（Heun 预测-校正 + 四元数积分）是标准数值方法，可直接迁移。但代码与 P6DofVehicle/P6DofKinematicState/P6DofForceAndMomentsObject 等 AFSIM 特有类强耦合，且单位混用（Imperial: lb/ft/slug + SI: m/mps）。
- **What can be extracted directly**: Heun 积分流程、四元数姿态积分、力/力矩限幅逻辑
- **What should be rewritten**: 
  - 用 SI 单位统一替换 Imperial/SI 混用
  - 用自有运动状态容器替换 `P6DofKinematicState`
  - 用自有力/力矩容器替换 `P6DofForceAndMomentsObject`
  - 冻结标志逻辑在非测试场景下可移除

## Validation Plan

1. **单位阶跃响应**：给定常值力和力矩，验证平动/转动速率线性增长
2. **无外力漂移**：零力零力矩条件下，位置/姿态应保持不变（能量守恒）
3. **纯重力抛体**：仅施加重力，与解析抛物轨迹对比（误差 < 0.01% per step @ 60Hz）
4. **姿态积分验证**：给定常值角速率（如 roll=1 rad/s），验证一个周期后 DCM 行列式 = 1.0 且四元数范数 = 1.0
5. **与 P6DOF 原始输出重现**：在相同输入条件下比较 P6DOF 原生输出与重实现结果，确保 < 1e-9 差异
6. **边界测试**：零质量/零惯量/极端步长（0.001s~1.0s）下的稳定性
