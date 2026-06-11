# PointMass 气动力与旋转限幅模型 -- 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-pointmass-aero-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│          PointMassAeroModel                          │
│  （PointMass 气动力与旋转限幅/稳定频率模型）             │
├──────────────────────────────────────────────────────┤
│  + calculate(q_bar, Mach, α, β,                      │
│      speedbrake, flaps, spoilers, R,                 │
│      → lift, drag, side,                             │
│      → maxRollAccel, maxPitchAccel, maxYawAccel,     │
│      → alphaStabFreq, betaStabFreq, rollStabFreq)    │
│                                                      │
│  - CL_AlphaBetaMach(M,α,β) → CL      (基类3D表)      │
│  - Cd_AlphaBetaMach(M,α,β) → Cd      (基类3D表)      │
│  - CY_AlphaBetaMach(M,α,β) → CY      (基类3D表)      │
│  - SpeedbrakeDeltaCd_Mach(M) → ΔCd     (操纵面1D表)   │
│  - FlapsDeltaCL_Mach(M) → ΔCL                     │
│  - FlapsDeltaCd_Mach(M) → ΔCd                     │
│  - SpoilersDeltaCL_Mach(M) → ΔCL                  │
│  - SpoilersDeltaCd_Mach(M) → ΔCd                  │
│  - MaximumRollAcceleration_Mach(M) → ω̇_max_base   │
│  - MaximumPitchAcceleration_Mach(M) → ω̇_max_base  │
│  - MaximumYawAcceleration_Mach(M) → ω̇_max_base    │
│  - AlphaStabilizingFrequency_Mach(M) → f_α        │
│  - BetaStabilizingFrequency_Mach(M) → f_β         │
│  - RollStabilizingFrequency_Mach(M) → f_roll      │
│  （共11个查表函数）                                   │
└──────────┬───────────────────────────────────────────┘
           │ 输出供
           ▼
┌──────────────────────────────────────────────────────┐
│              积分器 / SAS 控制器                       │
│  - 有量纲气动力 → 积分器计算平动加速度                  │
│  - 旋转加速度限幅 → SAS 控制项限幅                      │
│  - 稳定化频率 → SAS 稳定增稳项基准                      │
└──────────────────────────────────────────────────────┘
```

**数据流向说明**：PointMass 气动模型服务于两个消费者：
1. **积分器**：使用有量纲升力/阻力/侧力计算平动加速度。
2. **SAS 控制器**：使用旋转加速度限幅（限制控制指令不超出飞行器能力）和稳定化频率（设定增稳回路的固有频率）。

与 RigidBody 气动模型不同，PointMass 模型**不计算力矩**、**不需要角速率和变化率输入**、**不需要简化频率**。它额外提供操纵面（减速板/襟翼/扰流板）的增量叠加。

## 2. 核心接口定义

### 2.1 AerodynamicForces（有量纲气动力）

```cpp
// 有量纲气动力输出 -- 所有力在气流坐标系（wind frame）下
struct AerodynamicForces {
    double lift_n       = 0.0;  // 升力（N），垂直于相对气流，向上为正
    double drag_n       = 0.0;  // 阻力（N），平行于相对气流，向后为正
    double side_force_n = 0.0;  // 侧力（N），垂直于升阻平面，向右为正
};
```

### 2.2 RotationAuthority（旋转操纵能力参数）

```cpp
// 旋转操纵能力参数 -- 供 SAS 控制器使用的限幅和频率基准
struct RotationAuthority {
    // --- 最大旋转加速度（操纵限幅） ---
    // 物理含义：该飞行器在当前位置各通道能产生的最大角加速度
    // SAS 使用此值对控制指令做硬限幅，防止指令超出飞行器能力
    double max_roll_accel_rps2  = 0.0;  // 最大滚转角加速度（rad/s^2）
    double max_pitch_accel_rps2 = 0.0;  // 最大俯仰角加速度（rad/s^2）
    double max_yaw_accel_rps2   = 0.0;  // 最大偏航角加速度（rad/s^2）

    // --- 稳定化固有频率 ---
    // 物理含义：飞行器在各通道的自然稳定频率（由气动设计决定）
    // SAS 使用此值设定二阶临界阻尼系统（俯仰/偏航）和
    // 一阶滞后系统（滚转）的固有频率
    double alpha_stab_freq_rps  = 0.0;  // 攻角稳定化频率（rad/s）
    double beta_stab_freq_rps   = 0.0;  // 侧滑角稳定化频率（rad/s）
    double roll_stab_freq_rps   = 0.0;  // 滚转稳定化频率（rad/s）
};
```

### 2.3 ControlSurfaceDeflections（操纵面偏度）

```cpp
// 操纵面偏度输入 -- 各杆位为 0~1 归一化值
// 物理含义：0.0 = 完全收起，1.0 = 完全伸出
struct ControlSurfaceDeflections {
    double speedbrake = 0.0;  // 减速板杆位（仅产生阻力增量）
    double flaps      = 0.0;  // 襟翼杆位（产生升力+阻力增量）
    double spoilers   = 0.0;  // 扰流板杆位（产生负升力+阻力增量）
};
```

### 2.4 PointMassAeroTables（PointMass 气动查表集合）

```cpp
// PointMass 气动数据源 -- 封装所有系数查表
// 所有表指针为 nullptr 表示该参数未配置，计算时贡献为 0
class PointMassAeroTables {
public:
    // ======== 基础气动 3D 表（α, β, Mach → 系数） ========
    // 这三个表是所有气动模型的必需输入
    using Table3D = std::function<double(double alpha_rad, double beta_rad, double mach)>;

    Table3D cl_table;   // CL(α, β, M) -- 升力系数
    Table3D cd_table;   // Cd(α, β, M) -- 阻力系数
    Table3D cy_table;   // CY(α, β, M) -- 侧力系数

    // ======== 操纵面增量 1D 表（仅 Mach → 满偏增量） ========
    // 每个增量 = 杆位(0~1) × 满偏查表值
    using Table1D = std::function<double(double mach)>;

    Table1D speedbrake_dcd_table;   // ΔCd_speedbrake(M) -- 减速板满偏阻力增量
    Table1D flaps_dcl_table;        // ΔCL_flaps(M)      -- 襟翼满偏升力增量
    Table1D flaps_dcd_table;        // ΔCd_flaps(M)      -- 襟翼满偏阻力增量
    Table1D spoilers_dcl_table;     // ΔCL_spoilers(M)   -- 扰流板满偏升力减量（负值）
    Table1D spoilers_dcd_table;     // ΔCd_spoilers(M)   -- 扰流板满偏阻力增量

    // ======== 旋转动力学 1D 表（仅 Mach → 基准值） ========
    // 注意：初始查表值单位为 deg/s^2 和 Hz，接口内部自动转换为 SI

    Table1D max_roll_accel_table;   // ω̇_max_roll_base(M)  -- 名义最大滚转角加速度基准（deg/s^2）
    Table1D max_pitch_accel_table;  // ω̇_max_pitch_base(M) -- 名义最大俯仰角加速度基准（deg/s^2）
    Table1D max_yaw_accel_table;    // ω̇_max_yaw_base(M)   -- 名义最大偏航角加速度基准（deg/s^2）

    Table1D alpha_stab_freq_table;  // f_α(M)   -- 攻角稳定化频率基准（Hz）
    Table1D beta_stab_freq_table;   // f_β(M)   -- 侧滑角稳定化频率基准（Hz）
    Table1D roll_stab_freq_table;   // f_roll(M) -- 滚转稳定化频率基准（Hz）

    // 查表安全方法 -- 表为nullptr时返回0.0
    double lookup_CL(double alpha, double beta, double mach) const;
    double lookup_Cd(double alpha, double beta, double mach) const;
    double lookup_CY(double alpha, double beta, double mach) const;
    // ... 其余8个各有对应的lookup方法
};
```

### 2.5 PointMassAeroModel（PointMass 气动模型主类）

```cpp
// PointMass 气动力与旋转限幅模型 -- 主计算类
// 负责：(1)计算有量纲气动力（含操纵面增量）
//       (2)输出旋转加速度限幅（供SAS控制限幅用）
//       (3)输出稳定化频率（供SAS增稳回路设计用）
class PointMassAeroModel {
public:
    // ======== 配置 ========
    struct Config {
        double ref_area_m2 = 0.0;     // 参考面积（m^2），有量纲力的缩放基准
        PointMassAeroTables tables;   // 气动系数查表集合
    };

    // ======== 构造函数 ========
    explicit PointMassAeroModel(const Config& config);

    // ======== 主计算入口 ========
    // 每帧调用一次，同时计算出力和旋转动力学参数
    // 此函数是纯函数，不修改任何成员变量
    //
    // @param q_bar_pa          自由流动压 0.5*rho*V^2（Pa）
    // @param mach              飞行马赫数（无量纲）
    // @param alpha_rad         攻角（rad）
    // @param beta_rad          侧滑角（rad）
    // @param controls          操纵面杆位（0~1 归一化）
    // @param radius_scale_factor 几何尺度因子（无量纲，力按R^2缩放，默认1.0）
    // @param forces       [out] 有量纲气动力（N）
    // @param authority    [out] 旋转操纵能力参数
    void calculate(
        double q_bar_pa,
        double mach,
        double alpha_rad,
        double beta_rad,
        const ControlSurfaceDeflections& controls,
        double radius_scale_factor,
        AerodynamicForces&  forces,
        RotationAuthority&  authority
    ) const;

private:
    Config config_;
};
```

## 3. 典型调用模式

```cpp
// ======== 1. 初始化阶段：加载气动数据 ========
PointMassAeroModel::Config config;

// 设置参考面积
config.ref_area_m2 = 1.5;  // 参考面积 1.5 m^2

// 加载基础气动 3D 表
config.tables.cl_table = [](double a, double b, double m) {
    return my_3d_interp("CL", a, b, m);
};
config.tables.cd_table = [](double a, double b, double m) {
    return my_3d_interp("Cd", a, b, m);
};
config.tables.cy_table = [](double a, double b, double m) {
    return my_3d_interp("CY", a, b, m);
};

// 加载操纵面增量 1D 表（可选）
config.tables.speedbrake_dcd_table = [](double m) {
    return my_1d_interp("SpeedbrakeDeltaCd", m);  // 满偏阻力增量
};
config.tables.flaps_dcl_table = [](double m) {
    return my_1d_interp("FlapsDeltaCL", m);       // 满偏升力增量
};
config.tables.flaps_dcd_table = [](double m) {
    return my_1d_interp("FlapsDeltaCd", m);       // 满偏阻力增量
};
config.tables.spoilers_dcl_table = [](double m) {
    return my_1d_interp("SpoilersDeltaCL", m);    // 满偏升力减量（负值）
};
config.tables.spoilers_dcd_table = [](double m) {
    return my_1d_interp("SpoilersDeltaCd", m);    // 满偏阻力增量
};

// 加载旋转动力学 1D 表
// 注意：原始数据单位为 deg/s^2，接口内部自动转换为 rad/s^2
config.tables.max_roll_accel_table  = [](double m) { return my_1d_interp("MaxRollAccel", m); };
config.tables.max_pitch_accel_table = [](double m) { return my_1d_interp("MaxPitchAccel", m); };
config.tables.max_yaw_accel_table   = [](double m) { return my_1d_interp("MaxYawAccel", m); };

// 注意：原始数据单位为 Hz，接口内部自动转换为 rad/s
config.tables.alpha_stab_freq_table = [](double m) { return my_1d_interp("AlphaStabFreq", m); };
config.tables.beta_stab_freq_table  = [](double m) { return my_1d_interp("BetaStabFreq", m); };
config.tables.roll_stab_freq_table  = [](double m) { return my_1d_interp("RollStabFreq", m); };

// 创建气动模型实例
PointMassAeroModel aero_model(config);

// ======== 2. 仿真循环：每帧计算 ========
double q_bar   = 5000.0;     // 动压（Pa）
double mach    = 0.8;        // 马赫数
double alpha   = 0.05;       // 攻角 0.05 rad（约 2.9 度）
double beta    = 0.0;        // 侧滑角 0
double R       = 1.0;        // 尺度因子

// 操纵面杆位 -- 正常巡航：全收起
ControlSurfaceDeflections controls;
controls.speedbrake = 0.0;   // 减速板收起
controls.flaps      = 0.0;   // 襟翼收起
controls.spoilers   = 0.0;   // 扰流板收起

AerodynamicForces  forces;
RotationAuthority  authority;

// 调用主计算
aero_model.calculate(q_bar, mach, alpha, beta, controls, R, forces, authority);

// 使用结果：
// forces.lift_n         -- 升力（N），供积分器计算平动加速度
// forces.drag_n        -- 阻力（N）
// forces.side_force_n  -- 侧力（N）

// SAS 控制器使用以下参数：
// authority.max_roll_accel_rps2   -- 滚转通道控制指令限幅
// authority.max_pitch_accel_rps2  -- 俯仰通道控制指令限幅
// authority.max_yaw_accel_rps2    -- 偏航通道控制指令限幅
// authority.alpha_stab_freq_rps   -- 攻角稳定化频率（二阶临界阻尼ω_n）
// authority.beta_stab_freq_rps    -- 侧滑角稳定化频率（二阶临界阻尼ω_n）
// authority.roll_stab_freq_rps    -- 滚转稳定化频率（一阶滞后时间常数 1/ω_n）


// ======== 3. 操纵面使用示例：着陆构型 ========
controls.flaps    = 1.0;   // 襟翼全开 -- 增升增阻
controls.spoilers = 0.0;   // 扰流板收起
controls.speedbrake = 0.3; // 减速板部分伸出 -- 增阻减速

aero_model.calculate(q_bar, mach, alpha, beta, controls, R, forces, authority);
// 此时 forces.drag_n 会显著增加（襟翼+减速板增阻）
// forces.lift_n 会增加（襟翼增升）


// ======== 4. 大迎角操纵效能衰减验证 ========
// 当 alpha = 90 deg (1.57 rad) 时，
// cosAlphaTotal = cos(α_limited)*cos(β_limited) = cos(π/2)*1 = 0
// 导致所有 maxAccel 输出为 0（操纵失效）
alpha = 1.5708;            // 攻角约 90 度
beta  = 0.0;
aero_model.calculate(q_bar, mach, alpha, beta, controls, R, forces, authority);
// authority.max_pitch_accel_rps2  ≈ 0  （俯仰操纵失效）
// authority.max_roll_accel_rps2  ≈ 0  （总迎角超90度，滚转也失效）
```

### 内部计算流程示意

```cpp
// 以下为 calculate() 内部的核心逻辑，中文注释说明每一步
void PointMassAeroModel::calculate(
    double q_bar, double mach, double alpha, double beta,
    const ControlSurfaceDeflections& ctrl, double R,
    AerodynamicForces& f, RotationAuthority& auth
) const {
    // 1. 基础气动系数查表（3D表：α, β, Mach）
    double CL = config_.tables.lookup_CL(alpha, beta, mach);   // 静态升力
    double Cd = config_.tables.lookup_Cd(alpha, beta, mach);   // 静态阻力
    double CY = config_.tables.lookup_CY(alpha, beta, mach);   // 静态侧力

    // 2. 叠加操纵面增量：增量 = 杆位 × 满偏查表值
    //    减速板仅增阻，襟翼增升+增阻，扰流板减升+增阻
    CL += ctrl.spoilers * config_.tables.lookup_SpoilersDeltaCL(mach)  // 扰流板减升（负值）
        + ctrl.flaps    * config_.tables.lookup_FlapsDeltaCL(mach);     // 襟翼增升

    Cd += ctrl.speedbrake * config_.tables.lookup_SpeedbrakeDeltaCd(mach)  // 减速板增阻
        + ctrl.spoilers   * config_.tables.lookup_SpoilersDeltaCd(mach)    // 扰流板增阻
        + ctrl.flaps      * config_.tables.lookup_FlapsDeltaCd(mach);      // 襟翼增阻

    // CY 无侧力操纵面增量，保持不变

    // 3. 有量纲力：动压 × 系数 × 参考面积 × 尺度因子²
    double area_factor = R * R;  // 面积随半径平方缩放
    f.lift_n       = q_bar * CL * config_.ref_area_m2 * area_factor;
    f.drag_n      = q_bar * Cd * config_.ref_area_m2 * area_factor;
    f.side_force_n = q_bar * CY * config_.ref_area_m2 * area_factor;

    // 4. 总迎角余弦 -- 操纵效能衰减因子
    //    先将攻角和侧滑角限幅在 ±90 度，防止 cos() 超出定义域
    double alpha_lim = std::clamp(alpha, -M_PI_2, M_PI_2);  // ±90度
    double beta_lim  = std::clamp(beta,  -M_PI_2, M_PI_2);
    double cos_alpha_total = std::cos(alpha_lim) * std::cos(beta_lim);

    // 5. 查表获取名义最大旋转加速度（初始单位 deg/s^2）
    double nom_roll  = config_.tables.lookup_MaxRollAccel(mach);   // deg/s^2
    double nom_pitch = config_.tables.lookup_MaxPitchAccel(mach);  // deg/s^2
    double nom_yaw   = config_.tables.lookup_MaxYawAccel(mach);     // deg/s^2

    // 6. 有效最大加速度 = 名义 × cosAlphaTotal × DEG_TO_RAD（deg/s^2 → rad/s^2）
    constexpr double DEG_TO_RAD = 0.01745329252;
    auth.max_roll_accel_rps2  = std::max(0.0, nom_roll  * cos_alpha_total * DEG_TO_RAD);
    auth.max_pitch_accel_rps2 = std::max(0.0, nom_pitch * cos_alpha_total * DEG_TO_RAD);
    auth.max_yaw_accel_rps2   = std::max(0.0, nom_yaw   * cos_alpha_total * DEG_TO_RAD);
    // 负值截断为0 -- 无操纵能力时不输出负限幅

    // 7. 查表获取稳定化频率（初始单位 Hz），转为 rad/s
    constexpr double TWO_PI = 6.28318530718;
    auth.alpha_stab_freq_rps = config_.tables.lookup_AlphaStabFreq(mach) * TWO_PI;
    auth.beta_stab_freq_rps  = config_.tables.lookup_BetaStabFreq(mach)  * TWO_PI;
    auth.roll_stab_freq_rps  = config_.tables.lookup_RollStabFreq(mach)  * TWO_PI;
}
```

## 4. 坐标系/单位约定

### 4.1 坐标系

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **Body（体轴系）** | X=前, Y=右, Z=下 | 体轴角速率、旋转加速度的参考系 |
| **Wind（气流系）** | X=相对气流方向 | 气动力输出（升力、阻力、侧力） |

### 4.2 单位约定（SI）

所有接口统一使用 **SI 单位制**：

| 物理量 | 单位 | 说明 |
|--------|------|------|
| 力（升力/阻力/侧力） | N | 有量纲气动力输出 |
| 动压 | Pa | q_bar = 0.5*rho*V^2 |
| 角度（攻角/侧滑角） | rad | 输入α和β |
| 面积（参考面积） | m^2 | 力缩放基准 |
| 马赫数 | 无量纲 | 查表参数 |
| 操纵面杆位 | 无量纲 | 0.0~1.0 归一化 |
| 几何尺度因子 | 无量纲 | 力按R^2缩放 |
| 旋转角加速度 | rad/s^2 | 最大加速度限幅输出 |
| 稳定化频率 | rad/s | 固有频率输出，2*pi*f |
| 查表基准角加速度 | deg/s^2 | 气动表原始数据单位，接口内部转为 rad/s^2 |
| 查表基准频率 | Hz | 气动表原始数据单位，接口内部转为 rad/s |

注意：AFSIM 原始代码使用 Imperial 单位（lb, ft, ft^2, deg/s^2, Hz）。本接口规格已将全部输出单位转换为 SI，查表原始数据的单位转换在接口内部完成。

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|----------|----------|
| `PointMassAeroCoreObject` | 气动模型主类 | `PointMassAeroModel` class（本章定义） |
| `AeroCoreObject` (基类) | 类继承 | 合并到 `PointMassAeroModel::Config` 中 |
| `UtTable::Table` | 高维查表引擎 | `std::function<double(...)>` 可调用对象 |
| `UtInput` / `UtInputBlock` | 配置文件解析 | 不纳入接口；用户自行解析后填入 Config |
| `UtVec3dX` | 三维矢量 | `double[3]` 原生数组（仅在内部使用） |
| `UtCloneablePtr` | 智能指针 | 不纳入接口 |
| `UtMath::cPI_OVER_2 / cRAD_PER_DEG / cTWO_PI` | 数学常量 | 直接硬编码 |
| `UtMath::Limit()` | 数值限幅 | `std::clamp()` |
| `ForceAndRotationObject` | 力+旋转参数容器 | 拆分为 `AerodynamicForces` + `RotationAuthority` 两个独立结构体 |
