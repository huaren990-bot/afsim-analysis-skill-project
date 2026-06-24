# PointMass 稳定增稳系统 (SAS) -- 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-pointmass-sas-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────┐
│                PointMassSAS                              │
│          （点质稳定增稳系统控制器）                           │
├──────────────────────────────────────────────────────────┤
│  + computeRotationalAccel(state, mass, dt,               │
│      rot_limit, stab_freq, cmd_rates) → α_total         │
│                                                          │
│  输出：总旋转角加速度 α_total = α_controls + α_stability   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │  控制项（α_controls）                             │    │
│  │  一阶指令跟踪：α_ctrl = (ω_cmd - ω_curr) / dt    │    │
│  │  各轴独立限幅：clamp(α_ctrl, ±α_limit)            │    │
│  └─────────────────────────────────────────────────┘    │
│                         +                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │  稳定增稳项（α_stability）                         │    │
│  │  俯仰：α_pitch = -α·ω_n² - 2ω_n·α̇（二阶临界阻尼） │    │
│  │  偏航：α_yaw   = -β·ω_n² - 2ω_n·β̇（二阶临界阻尼） │    │
│  │  滚转：一阶滞后 low-pass filter → 驱 p→0          │    │
│  │  各通道数值限幅（防止大步长发散）                    │    │
│  └─────────────────────────────────────────────────┘    │
└──────────┬───────────────────────────────────────────────┘
           │ 依赖
           ▼
┌──────────────────────────────────────────────────────────┐
│              输入来源（外部子系统）                          │
│  - 运动状态 → α, β, p, q, r, α̇, β̇                     │
│  - 质量属性 → massFraction = m / m_base                  │
│  - 气动模型 → 旋转加速度限幅基准 + 稳定化频率基准          │
│  - 飞控系统 → 期望体轴角速率指令 ω_cmd (deg/s)            │
└──────────────────────────────────────────────────────────┘
```

**核心设计理念**：PointMass SAS 将飞行器的旋转动力学与操控指令解耦，总旋转角加速度 = 控制项 + 稳定增稳项。

- **控制项**：一阶 P 控制器，将飞行员/自动驾驶仪的期望角速率转换为角加速度。
- **稳定增稳项**：模拟真实飞行器的固有静稳定性和气动阻尼。
  - 俯仰/偏航通道：二阶临界阻尼系统 (zeta=1)，将攻角/侧滑角驱回零。
  - 滚转通道：一阶滞后低通滤波，将滚转速率平滑衰减至零。

质量比率 (m/m_base) 影响飞行器敏捷性：燃油消耗后质量减小，限幅和稳定化频率均增大，飞行器变得更敏捷。

## 2. 核心接口定义

### 2.1 SASInput（SAS 输入参数）

```cpp
// SAS 输入参数 -- 集成来自运动状态、气动模型和飞控系统的全部输入
struct SASInput {
    // ======== 来自运动状态 ========
    double alpha_rad     = 0.0;  // 攻角（rad）
    double beta_rad      = 0.0;  // 侧滑角（rad）
    double alpha_dot_rps = 0.0;  // 攻角变化率（rad/s）
    double beta_dot_rps  = 0.0;  // 侧滑角变化率（rad/s）
    double omega_body_rps[3] = {0, 0, 0}; // 当前体轴角速率 [roll, pitch, yaw]（rad/s）

    // ======== 来自质量属性 ========
    double mass_kg       = 0.0;  // 当前总质量（kg）
    double base_mass_kg  = 0.0;  // 基准质量（kg）

    // ======== 来自气动模型（PointMassAeroModel 输出） ========
    double max_roll_accel_rps2  = 0.0;  // 滚转角加速度限幅基准（rad/s^2）
    double max_pitch_accel_rps2 = 0.0;  // 俯仰角加速度限幅基准（rad/s^2）
    double max_yaw_accel_rps2   = 0.0;  // 偏航角加速度限幅基准（rad/s^2）

    double alpha_stab_freq_rps = 0.0;  // 攻角稳定化频率基准（rad/s）
    double beta_stab_freq_rps  = 0.0;  // 侧滑角稳定化频率基准（rad/s）
    double roll_stab_freq_rps  = 0.0;  // 滚转稳定化频率基准（rad/s）

    // ======== 来自飞控系统 ========
    // 飞控系统从操纵杆位移映射到的期望体轴角速率
    double commanded_omega_dps[3] = {0, 0, 0}; // [roll, pitch, yaw] 期望角速率（deg/s）
    // 注：若飞控系统未挂载（nullptr），此项保持为零向量，仅稳定项生效

    // ======== 仿真参数 ========
    double dt_s = 0.0;  // 积分步长（s），用于控制项一阶差分和稳定项数值限幅
};
```

### 2.2 SASOutput（SAS 输出）

```cpp
// SAS 输出 -- 各通道加速度的详细分解，便于诊断
struct SASOutput {
    // ======== 总旋转角加速度 = 控制项 + 稳定增稳项 ========
    double total_rot_accel_rps2[3] = {0, 0, 0}; // [roll, pitch, yaw]（rad/s^2）

    // ======== 控制项分解 ========
    double control_accel_rps2[3] = {0, 0, 0}; // 控制项角加速度 [roll, pitch, yaw]

    // ======== 稳定增稳项分解 ========
    double stability_accel_rps2[3] = {0, 0, 0}; // 稳定项角加速度 [roll, pitch, yaw]

    // ======== 诊断信息 ========
    double mass_fraction         = 1.0;  // 质量比率 m/m_base
    double effective_stab_freq[3] = {0, 0, 0}; // 质量缩放后的有效稳定化频率 [roll, pitch, yaw]（rad/s）
    double effective_max_accel[3] = {0, 0, 0}; // 质量缩放后的有效限幅 [roll, pitch, yaw]（rad/s^2）
};
```

### 2.3 PointMassSAS（SAS 主类）

```cpp
// PointMass 稳定增稳系统 -- 主计算类
// 提供旋转角加速度计算，输出 = 控制项 + 稳定增稳项
// 这是一个纯函数式计算器，不持有任何跨帧状态
class PointMassSAS {
public:
    // ======== 主计算入口 ========
    // 给定全部输入参数，计算总旋转角加速度
    //
    // @param input  SAS 全部输入参数（运动状态 + 质量 + 气动限幅 + 飞控指令 + 步长）
    // @param output [out] SAS 计算结果（含详细分解）
    //
    // 若 input.mass_kg <= 0，output 全部为零向量，安全返回。
    void compute(const SASInput& input, SASOutput& output) const;

private:
    // ======== 内部辅助方法 ========

    // 计算控制项：一阶指令跟踪
    // α_controls = (ω_cmd - ω_curr) / dt，然后各轴独立限幅
    void computeControlTerm(const SASInput& in, SASOutput& out) const;

    // 计算俯仰通道稳定项（二阶临界阻尼）
    // α_pitch_stab = -α * ω_n^2 - 2 * ω_n * α̇
    double computePitchStability(const SASInput& in, double wn_pitch) const;

    // 计算偏航通道稳定项（二阶临界阻尼）
    // α_yaw_stab = -β * ω_n^2 - 2 * ω_n * β̇
    double computeYawStability(const SASInput& in, double wn_yaw) const;

    // 计算滚转通道稳定项（一阶滞后）
    // weight = wn*dt / (1+wn*dt), expectedP = (1-weight)*p, α = (expectedP-p)/dt
    double computeRollStability(const SASInput& in, double wn_roll) const;
};
```

## 3. 典型调用模式

```cpp
// ======== 1. 初始化阶段 ========
PointMassSAS sas;  // SAS 是无状态计算器，只需一个实例

// ======== 2. 仿真循环：每帧计算旋转加速度 ========
// 在积分器的 CalculateAcceleration() 中调用

// 组装 SAS 输入
SASInput input;
input.alpha_rad     = 0.05;       // 攻角 0.05 rad（约 2.9 度）
input.beta_rad      = 0.0;        // 侧滑角 0
input.alpha_dot_rps = 0.01;       // 攻角变化率
input.beta_dot_rps  = -0.005;     // 侧滑角变化率
input.omega_body_rps[0] = 0.0;    // 滚转角速率
input.omega_body_rps[1] = 0.1;    // 俯仰角速率
input.omega_body_rps[2] = 0.0;    // 偏航角速率

input.mass_kg      = 5000.0;     // 当前质量 5000 kg
input.base_mass_kg = 10000.0;    // 基准质量（最大起飞重量）10000 kg
// massFraction = 5000/10000 = 0.5 → 燃油消耗一半，飞行器更敏捷

// 气动模型输出的限幅和频率（来自 PointMassAeroModel::calculate()）
input.max_roll_accel_rps2  = 15.0;    // 滚转角加速度限幅
input.max_pitch_accel_rps2 = 20.0;    // 俯仰角加速度限幅
input.max_yaw_accel_rps2   = 8.0;     // 偏航角加速度限幅

input.alpha_stab_freq_rps = 6.28;     // 攻角稳定化频率 1 Hz → 6.28 rad/s
input.beta_stab_freq_rps  = 4.19;     // 侧滑稳定化频率 0.67 Hz → 4.19 rad/s
input.roll_stab_freq_rps  = 3.14;     // 滚转稳定化频率 0.5 Hz → 3.14 rad/s

// 飞控系统输出的期望角速率指令（来自操纵杆位移映射）
input.commanded_omega_dps[0] = 0.0;    // 期望滚转角速率 0 deg/s（无滚转指令）
input.commanded_omega_dps[1] = 5.0;    // 期望俯仰角速率 5 deg/s（拉杆抬头）
input.commanded_omega_dps[2] = 0.0;    // 期望偏航角速率 0 deg/s

input.dt_s = 1.0 / 60.0;              // 步长 60 Hz

// 调用 SAS
SASOutput output;
sas.compute(input, output);

// 使用结果：
// output.total_rot_accel_rps2[0]  -- 滚转总角加速度，供积分器推进滚转角速率
// output.total_rot_accel_rps2[1]  -- 俯仰总角加速度，供积分器推进俯仰角速率
// output.total_rot_accel_rps2[2]  -- 偏航总角加速度，供积分器推进偏航角速率

// 诊断信息：
// output.mass_fraction            -- 0.5（燃油消耗一半）
// output.effective_stab_freq[1]   -- 12.56 rad/s（俯仰稳定频率 = 6.28/0.5 = 质量缩放后加倍）
// output.effective_max_accel[1]   -- 40.0 rad/s^2（限幅 = 20.0/0.5 = 加倍）
// output.control_accel_rps2[1]    -- 控制项俯仰加速度
// output.stability_accel_rps2[1]  -- 稳定项俯仰加速度


// ======== 3. 纯稳定模式（无飞行员输入） ========
input.commanded_omega_dps[0] = 0.0;
input.commanded_omega_dps[1] = 0.0;
input.commanded_omega_dps[2] = 0.0;
// 此时 output.control_accel_rps2 为零向量
// output.stability_accel_rps2 中的俯仰项 ≈ -α*ω_n² - 2*ω_n*α̇
//   将攻角以临界阻尼方式驱回零
//   偏航项将侧滑角驱回零
//   滚转项将滚转速率平滑衰减至零
```

### 内部计算流程示意

```cpp
void PointMassSAS::compute(const SASInput& in, SASOutput& out) const {
    // 零质量保护：质量无效时输出全零
    if (in.mass_kg <= 0.0 || in.base_mass_kg <= 0.0) {
        out = SASOutput{};  // 全部归零
        return;
    }

    // 1. 计算质量比率
    out.mass_fraction = in.mass_kg / in.base_mass_kg;
    double mf = out.mass_fraction;

    // 2. 质量比率缩放的稳定化频率和限幅
    //    质量越小 → mf越小 → 频率越高、限幅越大 → 飞行器越敏捷
    out.effective_stab_freq[0] = in.roll_stab_freq_rps  / mf;  // 滚转
    out.effective_stab_freq[1] = in.alpha_stab_freq_rps / mf;  // 俯仰
    out.effective_stab_freq[2] = in.beta_stab_freq_rps  / mf;  // 偏航

    out.effective_max_accel[0] = in.max_roll_accel_rps2  / mf;
    out.effective_max_accel[1] = in.max_pitch_accel_rps2 / mf;
    out.effective_max_accel[2] = in.max_yaw_accel_rps2   / mf;

    double dt = in.dt_s;

    // ======== 控制项：一阶指令跟踪 ========
    constexpr double DEG_TO_RAD = 0.01745329252;

    // 将期望角速率 deg/s → rad/s，然后计算一阶差分角加速度
    double omega_cmd_rps[3];
    omega_cmd_rps[0] = in.commanded_omega_dps[0] * DEG_TO_RAD;
    omega_cmd_rps[1] = in.commanded_omega_dps[1] * DEG_TO_RAD;
    omega_cmd_rps[2] = in.commanded_omega_dps[2] * DEG_TO_RAD;

    for (int i = 0; i < 3; ++i) {
        // α_controls = (ω_cmd - ω_curr) / dt
        out.control_accel_rps2[i] = (omega_cmd_rps[i] - in.omega_body_rps[i]) / dt;

        // 各轴独立限幅：clamp(α_i, ±α_limit_i)
        double limit = std::abs(out.effective_max_accel[i]);
        out.control_accel_rps2[i] = std::clamp(out.control_accel_rps2[i], -limit, limit);
    }

    // ======== 稳定增稳项 ========

    // 滚转通道：一阶滞后低通滤波
    double wn_roll = out.effective_stab_freq[0];
    double weight = wn_roll * dt / (1.0 + wn_roll * dt);  // 一阶滞后权重
    double expected_p = (1.0 - weight) * in.omega_body_rps[0]; // 向零平滑过渡
    double roll_stab = (expected_p - in.omega_body_rps[0]) / dt;

    // 俯仰通道：二阶临界阻尼系统 (ζ=1) → 驱 α→0
    double wn_pitch = out.effective_stab_freq[1];
    double pitch_stab = -in.alpha_rad * wn_pitch * wn_pitch    // 恢复项（静稳定性）
                       - 2.0 * wn_pitch * in.alpha_dot_rps;    // 阻尼项

    // 偏航通道：二阶临界阻尼系统 (ζ=1) → 驱 β→0
    double wn_yaw = out.effective_stab_freq[2];
    double yaw_stab = -in.beta_rad * wn_yaw * wn_yaw             // 恢复项
                      - 2.0 * wn_yaw * in.beta_dot_rps;          // 阻尼项

    // ======== 稳定性数值限幅（防止大时间步长发散） ========
    // 限幅值 = 一步内将气动角/角速率归零所需加速度的 2 倍（安全裕量）
    double max_roll  = std::abs(in.omega_body_rps[0] / dt);
    double max_pitch = std::abs((-in.alpha_rad - in.alpha_dot_rps * dt) * 2.0 / (dt * dt));
    double max_yaw   = std::abs((-in.beta_rad  - in.beta_dot_rps  * dt) * 2.0 / (dt * dt));

    roll_stab  = std::clamp(roll_stab,  -max_roll,  max_roll);
    pitch_stab = std::clamp(pitch_stab, -max_pitch, max_pitch);
    yaw_stab   = std::clamp(yaw_stab,   -max_yaw,   max_yaw);

    out.stability_accel_rps2[0] = roll_stab;          // 滚转
    out.stability_accel_rps2[1] = pitch_stab;          // 俯仰
    out.stability_accel_rps2[2] = -yaw_stab;           // 偏航（符号翻转）

    // ======== 总旋转角加速度 = 控制项 + 稳定增稳项 ========
    for (int i = 0; i < 3; ++i) {
        out.total_rot_accel_rps2[i] = out.control_accel_rps2[i]
                                    + out.stability_accel_rps2[i];
    }
}
```

## 4. 坐标系/单位约定

### 4.1 坐标系

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **Body（体轴系）** | X=前, Y=右, Z=下 | 角速率输入、角加速度输出 |

所有 SAS 输入和输出均在**体轴系**下：
- `omega_body_rps[0]` = 滚转角速率 p（绕体轴 X，rad/s）
- `omega_body_rps[1]` = 俯仰角速率 q（绕体轴 Y，rad/s）
- `omega_body_rps[2]` = 偏航角速率 r（绕体轴 Z，rad/s）
- 输出 `total_rot_accel_rps2` 同样遵循 `[roll, pitch, yaw]` 顺序

攻角 α 和侧滑角 β 的定义遵循标准气动约定（气流系 → 体轴系的分解）。

### 4.2 单位约定（SI）

所有接口统一使用 **SI 单位制**：

| 物理量 | 单位 | 说明 |
|--------|------|------|
| 角度（α, β） | rad | 攻角和侧滑角 |
| 角速率变化率（α̇, β̇） | rad/s | 攻角和侧滑角变化率 |
| 角速率（p, q, r） | rad/s | 体轴角速率 |
| 角加速度（α_controls, α_stability, α_total） | rad/s^2 | 旋转角加速度 |
| 稳定化固有频率（ω_n） | rad/s | 质量缩放后的有效频率 |
| 飞控指令角速率 | deg/s | SAS 内部转为 rad/s 后再计算 |
| 质量 | kg | 当前质量和基准质量 |
| 时间（步长 dt） | s | 用于一阶差分和数值限幅 |
| 质量比率 | 无量纲 | m / m_base |

注意：AFSIM 原始代码在控制项中使用 deg/s 和 rad/s 混合单位。本接口规格在 SAS 内部统一转为 rad/s 后再计算，对外接口中的飞控指令保持 deg/s 输入（与飞控系统约定一致）。

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|----------|----------|
| SAS 代码内联在 `PointMassIntegrator::CalculateAcceleration()` | 内联代码段 | 独立 `PointMassSAS` class（本章定义） |
| `KinematicState` (框架类) | 运动状态容器 | `SASInput` struct 中的独立字段 |
| `MassProperties` (框架类) | 质量属性容器 | `SASInput` 中的 `mass_kg` / `base_mass_kg` |
| `ForceAndRotationObject` | 旋转参数容器 | `SASInput` 中的 `max_*_accel_rps2` + `*_stab_freq_rps` |
| `PointMassFlightControlSystem` | 飞控系统接口 | `SASInput` 中的 `commanded_omega_dps[3]` 数组 |
| `GetBodyRateCommands_dps()` | 飞控输出方法 | 由外部飞控模块计算后填入 `SASInput` |
| `UtVec3dX` | 三维矢量 | `double[3]` 原生数组 |
| `UtMath::Limit()` | 数值限幅 | `std::clamp()` |
| `UtMath::cDEG_PER_RAD / cRAD_PER_DEG` | 单位换算常量 | 直接硬编码 `DEG_TO_RAD = 0.0174533` |
| 操纵杆位移 → 角速率映射曲线 (`UtTable::Curve`) | 飞控查表 | 不纳入 SAS 接口；由外部飞控模块完成映射后将 `commanded_omega_dps` 传入 |
| `GetStepSize_sec()` | 步长获取（来自Mover） | `SASInput` 中的 `dt_s`，由调用者提供 |
