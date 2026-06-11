# 刚体稳定性导数气动系数模型 -- 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-rigidbody-aero-coefficient-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│            RigidBodyAeroCoreObject                   │
│  （刚体稳定性导数气动系数模型）                          │
├──────────────────────────────────────────────────────┤
│  + CalculateCoreAeroFM(q_bar, Mach, V, α, β,         │
│      α̇, β̇, ω_body, R, → lift, drag, side, moment)   │
│  - CL_AlphaBetaMach(Mach, α, β) → CL     (基类3D表)  │
│  - Cd_AlphaBetaMach(Mach, α, β) → Cd     (基类3D表)  │
│  - CY_AlphaBetaMach(Mach, α, β) → CY     (基类3D表)  │
│  - CLq_AlphaMach(Mach, α) → CLq          (子类2D表)  │
│  - CL_AlphaDotAlphaMach(Mach, α) → CL_adot           │
│  - CYr_BetaMach(Mach, β) → CYr                      │
│  - CY_BetaDotBetaMach(Mach, β) → CY_bdot             │
│  - Cm_AlphaBetaMach / Cmq_Mach / Cmp_Mach / ...      │
│  - Cn_AlphaBetaMach / Cnr_Mach / Cnp_Mach / ...      │
│  - Cl_AlphaBetaMach / Clp_Mach / Clr_Mach / ...      │
│  （共14个导数查表函数）                                 │
└──────────┬───────────────────────────────────────────┘
           │ 调用
           ▼
┌──────────────────────────────────────────────────────┐
│              AeroCoreObject（基类）                    │
│  仅管理CL/Cd/CY三张静态3D表 + 参考面积/模态             │
├──────────────────────────────────────────────────────┤
│  mCL_AlphaBetaMachTablePtr    (α,β,M → CL)           │
│  mCd_AlphaBetaMachTablePtr    (α,β,M → Cd)           │
│  mCY_AlphaBetaMachTablePtr    (α,β,M → CY)           │
│  mRefArea_sqft    (显式参考面积)                       │
│  mModeName        (当前气动模态名称)                    │
│  mSubModesList    (多构型子模态列表)                    │
└──────────────────────────────────────────────────────┘
           │ 输入来源
           ▼
┌──────────────────────────────────────────────────────┐
│              飞行状态参数（来自积分器）                   │
│  - 动压 q_bar (Pa)                                    │
│  - 马赫数 Mach                                        │
│  - 真空速 V (m/s)                                     │
│  - 攻角 α / 侧滑角 β (rad)                           │
│  - 攻角变化率 α̇ / 侧滑角变化率 β̇ (rad/s)             │
│  - 体轴角速率 ω_body = [p, q, r] (rad/s)              │
│  - 几何尺度因子 R                                     │
└──────────────────────────────────────────────────────┘
```

**数据流向说明**：积分器每帧调用 `CalculateCoreAeroFM()`，传入飞行状态参数。该函数先计算简化频率（Reduced Frequency）将角速率无量纲化，然后通过基类 3D 表查取静态系数、通过子类 2D 表/1D 曲线查取动态导数，线性叠加总系数后乘以动压、参考面积和参考长度，输出有量纲的六分量气动力和气动力矩。

## 2. 核心接口定义

### 2.1 AeroGeometry（气动几何参数）

```cpp
// 气动几何参数 -- 用于简化频率计算和力矩有量纲化
// 支持两种模式：翼面模式（默认）和显式参考面积模式
struct AeroGeometry {
    // --- 翼面模式参数 ---
    double wing_chord_m = 0.0;    // 平均气动弦长 MAC（m），缩放俯仰相关简化频率
    double wing_span_m  = 0.0;    // 翼展（m），缩放滚转/偏航相关简化频率
    double wing_area_m2 = 0.0;    // 机翼参考面积（m^2），用于力/力矩有量纲化

    // --- 显式参考面积模式参数 ---
    bool   use_ref_area   = false;  // 是否启用显式参考面积（替代翼面参数）
    double ref_area_m2    = 0.0;    // 显式参考面积（m^2），启用后用于所有力/力矩计算
    double ref_length_m   = 0.0;    // 显式参考长度 sqrt(ref_area_m2)（m），启用后替代弦长/翼展

    // --- 通用参数 ---
    double aero_center_m[3] = {0,0,0};  // 气动中心位置（m），力/力矩的作用点参考
};
```

### 2.2 AerodynamicForces（有量纲气动力）

```cpp
// 有量纲气动力输出 -- 三个力分量均在气流坐标系（wind frame）下
struct AerodynamicForces {
    double lift_n      = 0.0;  // 升力（N），垂直于相对气流方向，向上为正
    double drag_n      = 0.0;  // 阻力（N），平行于相对气流方向，向后为正
    double side_force_n = 0.0; // 侧力（N），垂直于升阻平面，向右为正
};
```

### 2.3 AerodynamicMoments（有量纲气动力矩）

```cpp
// 有量纲气动力矩输出 -- 三轴力矩在体轴系（body frame）下
// 力矩矢量: [roll_moment, pitch_moment, yaw_moment] 对应体轴 X(前)、Y(右)、Z(下)
struct AerodynamicMoments {
    double roll_moment_nm  = 0.0;  // 滚转力矩（N·m），绕体轴X
    double pitch_moment_nm = 0.0;  // 俯仰力矩（N·m），绕体轴Y
    double yaw_moment_nm   = 0.0;  // 偏航力矩（N·m），绕体轴Z
};
```

### 2.4 StabilityDerivativeTables（稳定性导数查表集合）

```cpp
// 稳定性导数数据源 -- 封装所有气动系数查表
// 所有表指针为 nullptr 表示该导数未配置，计算时贡献为 0
class StabilityDerivativeTables {
public:
    // ======== 基类静态 3D 表（α, β, Mach → 系数） ========
    // 这三个表是所有气动模型的必需输入
    using Table3D = std::function<double(double alpha_rad, double beta_rad, double mach)>;

    Table3D cl_table;   // CL(α, β, M) -- 升力系数
    Table3D cd_table;   // Cd(α, β, M) -- 阻力系数
    Table3D cy_table;   // CY(α, β, M) -- 侧力系数

    // ======== 力导数 2D 表（α 或 β, Mach → 导数） ========
    using Table2D = std::function<double(double angle_rad, double mach)>;

    Table2D clq_table;     // CLq(α, M)       -- 俯仰阻尼升力导数
    Table2D cl_adot_table; // CL_adot(α, M)   -- 攻角延迟升力导数
    Table2D cyr_table;     // CYr(β, M)       -- 偏航速率侧力导数
    Table2D cy_bdot_table; // CY_betadot(β, M)-- 侧滑延迟侧力导数

    // ======== 力矩静态 3D 表（α, β, Mach → 系数） ========
    Table3D cm_table;   // Cm(α, β, M) -- 俯仰力矩系数
    Table3D cn_table;   // Cn(α, β, M) -- 偏航力矩系数
    Table3D cl_moment_table;   // Cl(α, β, M) -- 滚转力矩系数

    // ======== 力矩导数 1D 曲线（仅 Mach → 导数） ========
    using Table1D = std::function<double(double mach)>;

    Table1D cmq_curve;      // Cmq(M)  -- 俯仰阻尼导数
    Table1D cmp_curve;      // Cmp(M)  -- 滚转-俯仰交叉导数
    Table1D cm_adot_curve;  // Cm_adot(M) -- 攻角延迟俯仰力矩导数

    Table1D cnr_curve;      // Cnr(M)  -- 偏航阻尼导数
    Table1D cnp_curve;      // Cnp(M)  -- 滚转-偏航交叉导数
    Table1D cn_bdot_curve;  // Cn_betadot(M) -- 侧滑延迟偏航力矩导数

    Table1D clp_curve;      // Clp(M)  -- 滚转阻尼导数
    Table1D clr_curve;      // Clr(M)  -- 偏航-滚转交叉导数
    Table1D clq_curve;      // Clq(M)  -- 俯仰-滚转交叉导数
    Table1D cl_adot_curve;  // Cl_adot(M) -- 攻角延迟滚转力矩导数
    Table1D cl_bdot_curve;  // Cl_betadot(M) -- 侧滑延迟滚转力矩导数

    // 查表安全方法 -- 所有方法在表为nullptr时返回0.0
    double lookup_CL(double alpha, double beta, double mach) const;
    double lookup_Cd(double alpha, double beta, double mach) const;
    double lookup_CY(double alpha, double beta, double mach) const;
    // ... 其余14个导数各有对应的lookup方法
};
```

### 2.5 RigidBodyAeroCoefficient（刚体气动系数模型主类）

```cpp
// 刚体稳定性导数气动系数模型 -- 主计算类
// 负责将飞行状态通过高维查表转换为六分量气动力/力矩
class RigidBodyAeroCoefficient {
public:
    // ======== 配置 ========
    struct Config {
        AeroGeometry geometry;               // 气动几何参数
        StabilityDerivativeTables tables;    // 稳定性导数查表集合
        bool use_reduced_frequency = true;   // 默认启用简化频率无量纲化
    };

    // ======== 构造函数 ========
    // 传入气动几何参数和所有导数表；表可为空（未配置的导数为0）
    explicit RigidBodyAeroCoefficient(const Config& config);

    // ======== 主计算入口 ========
    // 每帧调用一次，根据飞行状态计算六分量气动力/力矩
    // 此函数是纯函数：不修改任何成员变量，仅读取表数据
    //
    // @param q_bar_pa           自由流动压 0.5*rho*V^2（Pa）
    // @param mach               飞行马赫数（无量纲）
    // @param true_airspeed_mps  真空速（m/s）
    // @param alpha_rad          攻角（rad）
    // @param beta_rad           侧滑角（rad）
    // @param alpha_dot_rps      攻角变化率（rad/s）
    // @param beta_dot_rps       侧滑角变化率（rad/s）
    // @param omega_body_rps[3]  体轴角速率 [roll, pitch, yaw]（rad/s）
    // @param radius_scale_factor 几何尺度因子（无量纲，力按R^2缩放，默认1.0）
    // @param forces   [out] 有量纲气动力（N）
    // @param moments  [out] 有量纲气动力矩（N·m）
    void calculate(
        double q_bar_pa,
        double mach,
        double true_airspeed_mps,
        double alpha_rad,
        double beta_rad,
        double alpha_dot_rps,
        double beta_dot_rps,
        const double omega_body_rps[3],
        double radius_scale_factor,
        AerodynamicForces&  forces,
        AerodynamicMoments& moments
    ) const;

    // ======== 气动模态切换 ========
    // 切换当前使用的子模态（多构型支持，如挂弹/空载/襟翼位置）
    void set_mode(const std::string& mode_name);

private:
    Config config_;

    // ======== 内部辅助方法 ========

    // 计算简化频率（Reduced Frequency）
    // 将角速率和变化率无量纲化: k = rate / (2*V_safe)
    // V_safe = max(V, 1.0) 防止除零
    struct ReducedFrequencies {
        double kq, kr, kp;    // 角速率简化频率
        double ka, kb;        // 变化率简化频率
    };
    ReducedFrequencies compute_reduced_frequencies(
        double true_airspeed_mps,
        double pitch_rate_rps, double yaw_rate_rps, double roll_rate_rps,
        double alpha_dot_rps, double beta_dot_rps
    ) const;

    // 按参考长度缩放简化频率 -- 俯仰相关用弦长，偏航/滚转相关用翼展
    // 若 use_ref_area = true 则统一用 ref_length
    void scale_reduced_frequencies(ReducedFrequencies& rf) const;
};
```

## 3. 典型调用模式

```cpp
// ======== 1. 初始化阶段：加载气动数据 ========
RigidBodyAeroCoefficient::Config config;

// 配置翼面几何参数（翼面模式）
config.geometry.wing_chord_m  = 1.5;    // 平均气动弦长 1.5 m
config.geometry.wing_span_m   = 10.0;   // 翼展 10 m
config.geometry.wing_area_m2  = 15.0;   // 机翼面积 15 m^2
config.geometry.use_ref_area  = false;  // 使用翼面参数而非显式参考面积
config.use_reduced_frequency  = true;   // 启用简化频率无量纲化

// 加载气动导数表 -- 所有查表函数由配置文件/数据文件提供
// 未加载的表指针为nullptr，计算时该导数的贡献为0
config.tables.cl_table   = [](double a, double b, double m) { return my_3d_table("CL", a, b, m); };
config.tables.cd_table   = [](double a, double b, double m) { return my_3d_table("Cd", a, b, m); };
config.tables.cy_table   = [](double a, double b, double m) { return my_3d_table("CY", a, b, m); };
config.tables.cm_table   = [](double a, double b, double m) { return my_3d_table("Cm", a, b, m); };
config.tables.cn_table   = [](double a, double b, double m) { return my_3d_table("Cn", a, b, m); };
config.tables.cl_moment_table = [](double a, double b, double m) { return my_3d_table("Cl", a, b, m); };

// 加载动态导数 2D 表（可选，未加载时导数为0）
config.tables.clq_table     = [](double a, double m) { return my_2d_table("CLq", a, m); };
config.tables.cl_adot_table = [](double a, double m) { return my_2d_table("CL_adot", a, m); };
config.tables.cyr_table     = [](double b, double m) { return my_2d_table("CYr", b, m); };
config.tables.cy_bdot_table = [](double b, double m) { return my_2d_table("CY_bdot", b, m); };

// 加载动态导数 1D 曲线（可选）
config.tables.cmq_curve      = [](double m) { return my_1d_curve("Cmq", m); };
config.tables.cmp_curve      = [](double m) { return my_1d_curve("Cmp", m); };
config.tables.cnr_curve      = [](double m) { return my_1d_curve("Cnr", m); };
// ... 其余1D曲线同理

// 创建气动系数模型实例
RigidBodyAeroCoefficient aero_model(config);

// ======== 2. 仿真循环：每帧计算气动力/力矩 ========
double q_bar   = 5000.0;     // 动压 q_bar = 0.5*rho*V^2（Pa）
double mach    = 0.8;           // 马赫数
double V       = 272.0;         // 真空速（m/s）
double alpha   = 0.05;          // 攻角 0.05 rad（约 2.9 度）
double beta    = 0.0;           // 侧滑角 0
double alpha_dot = 0.01;        // 攻角变化率（rad/s）
double beta_dot  = 0.0;         // 侧滑角变化率
double omega[3]  = {0.0, 0.1, 0.0};  // 体轴角速率 [p, q, r]
double R         = 1.0;         // 几何尺度因子（默认1.0）

AerodynamicForces  forces;
AerodynamicMoments moments;

// 调用主计算函数 -- 纯函数，不修改模型内部状态
aero_model.calculate(
    q_bar, mach, V, alpha, beta, alpha_dot, beta_dot, omega, R,
    forces, moments
);

// 使用结果
// forces.lift_n       -- 升力（N）
// forces.drag_n      -- 阻力（N）
// forces.side_force_n -- 侧力（N）
// moments.roll_moment_nm   -- 滚转力矩（N·m）
// moments.pitch_moment_nm  -- 俯仰力矩（N·m）
// moments.yaw_moment_nm    -- 偏航力矩（N·m）
```

### 内部计算流程示意

```cpp
// 以下为 calculate() 内部的核心逻辑片段，中文注释说明每一步
void RigidBodyAeroCoefficient::calculate(
    double q_bar, double mach, double V, double alpha, double beta,
    double alpha_dot, double beta_dot, const double omega[3], double R,
    AerodynamicForces& forces, AerodynamicMoments& moments
) const {
    // 1. 拆分角速率到三轴分量
    double p = omega[0];  // 滚转角速率 (rad/s)
    double q = omega[1];  // 俯仰角速率 (rad/s)
    double r = omega[2];  // 偏航角速率 (rad/s)

    // 2. 基础无量纲化：各角速率 / (2*V)，V 下限保护为 1.0 m/s 防止除零
    double V_safe = std::max(V, 1.0);                       // 保护下限 1.0 m/s
    double kq = q / (2.0 * V_safe);                          // 基础俯仰无量纲速率
    double kr = r / (2.0 * V_safe);                          // 基础偏航无量纲速率
    double kp = p / (2.0 * V_safe);                          // 基础滚转无量纲速率
    double ka = alpha_dot / (2.0 * V_safe);                  // 基础攻角变化率无量纲速率
    double kb = beta_dot  / (2.0 * V_safe);                  // 基础侧滑角变化率无量纲速率

    // 3. 按参考长度缩放各分量的简化频率
    // 俯仰相关（力：kLq/kLa，力矩：kmq/kma/kmp）用弦长（或 ref_length）
    // 偏航/滚转相关用力分量kYr/kYb和力矩分量knr/klp等用翼展（或 ref_length）
    double chord = config_.geometry.wing_chord_m;            // 弦长（俯仰参考长度）
    double span  = config_.geometry.wing_span_m;             // 翼展（滚转/偏航参考长度）
    if (config_.geometry.use_ref_area) {
        chord = span = config_.geometry.ref_length_m;        // 统一用 ref_length
    }

    // 力分量简化频率
    double kLq = kq * chord, kLa = ka * chord;               // 俯仰相关力分量（用弦长）
    double kYr = kr * span,  kYb = kb * span;                // 偏航相关力分量（用翼展）

    // 力矩分量简化频率（各通道独立缩放）
    double kmq = kq * chord, kma = ka * chord, kmp = kp * chord;  // 俯仰力矩
    double klq = kq * span, kla = ka * span, klr = kr * span,    // 滚转力矩
           klb = kb * span, klp = kp * span;
    double knr = kr * span, knb = kb * span, knp = kp * span;    // 偏航力矩

    // 若不使用简化频率（已弃用模式），直接用有量纲速率替代
    if (!config_.use_reduced_frequency) {
        kLq = q; kLa = alpha_dot; kYr = r; kYb = beta_dot;
        kmq = q; kma = alpha_dot; kmp = p;
        klq = q; kla = alpha_dot; klr = r; klb = beta_dot; klp = p;
        knr = r; knb = beta_dot; knp = p;
    }

    // 4. 升力/阻力/侧力系数查表并叠加
    double CL = config_.tables.lookup_CL(alpha, beta, mach);    // 静态升力
    double CLq_val   = config_.tables.lookup_CLq(alpha, mach) * kLq;   // 俯仰阻尼升力增量
    double CL_adot_val = config_.tables.lookup_CL_adot(alpha, mach) * kLa; // 攻角延迟升力增量
    double CL_total  = CL + CLq_val + CL_adot_val;

    double Cd       = config_.tables.lookup_Cd(alpha, beta, mach);  // 阻力（仅静态，无动态项）
    double CY       = config_.tables.lookup_CY(alpha, beta, mach);  // 静态侧力
    double CYr_val  = config_.tables.lookup_CYr(beta, mach) * kYr;  // 偏航速率侧力增量
    double CY_bdot_val = config_.tables.lookup_CY_bdot(beta, mach) * kYb; // 侧滑延迟侧力增量
    double CY_total = CY + CYr_val + CY_bdot_val;

    // 5. 有量纲力 = 动压 × 总系数 × 参考面积 × 尺度因子²
    double area = config_.geometry.use_ref_area
        ? config_.geometry.ref_area_m2 : config_.geometry.wing_area_m2;
    double area_factor = R * R;  // 面积随半径的平方缩放
    forces.lift_n       = q_bar * CL_total * area * area_factor;
    forces.drag_n      = q_bar * Cd       * area * area_factor;
    forces.side_force_n = q_bar * CY_total * area * area_factor;

    // 6. 有量纲力矩 = 动压 × 总系数 × 面积 × 参考长度
    // 俯仰力矩用弦长（或 ref_length），滚转/偏航力矩用翼展（或 ref_length）
    double pitch_ref = chord;  // 俯仰力矩参考长度
    double lat_ref   = span;   // 滚转/偏航力矩参考长度
    if (config_.geometry.use_ref_area) {
        pitch_ref = lat_ref = config_.geometry.ref_length_m;
    }

    double Cm = config_.tables.lookup_Cm(alpha, beta, mach);
    double Cmq = config_.tables.lookup_Cmq(mach) * kmq;
    double Cmp = config_.tables.lookup_Cmp(mach) * kmp;
    double Cm_adot = config_.tables.lookup_Cm_adot(mach) * kma;
    double Cm_total = Cm + Cmq + Cmp + Cm_adot;
    moments.pitch_moment_nm = q_bar * Cm_total * area * pitch_ref;

    double Cn = config_.tables.lookup_Cn(alpha, beta, mach);
    double Cnr = config_.tables.lookup_Cnr(mach) * knr;
    double Cnp = config_.tables.lookup_Cnp(mach) * knp;
    double Cn_bdot = config_.tables.lookup_Cn_bdot(mach) * knb;
    double Cn_total = Cn + Cnr + Cnp + Cn_bdot;
    moments.yaw_moment_nm = q_bar * Cn_total * area * lat_ref;

    double Cl = config_.tables.lookup_Cl(alpha, beta, mach);
    double Clp = config_.tables.lookup_Clp(mach) * klp;
    double Clr = config_.tables.lookup_Clr(mach) * klr;
    double Clq = config_.tables.lookup_Clq(mach) * klq;
    double Cl_adot = config_.tables.lookup_Cl_adot(mach) * kla;
    double Cl_bdot = config_.tables.lookup_Cl_bdot(mach) * klb;
    double Cl_total = Cl + Clp + Clr + Clq + Cl_adot + Cl_bdot;
    moments.roll_moment_nm = q_bar * Cl_total * area * lat_ref;
}
```

## 4. 坐标系/单位约定

### 4.1 坐标系

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **Body（体轴系）** | X=前, Y=右, Z=下 | 角速率输入 [p,q,r]、力矩输出 [Mx,My,Mz] |
| **Wind（气流系）** | X=相对气流方向 | 气动力输出（升力、阻力、侧力） |
| **Stability（稳定性系）** | X=速度在对称面投影 | 攻角α、侧滑角β的定义参考 |

### 4.2 单位约定（SI）

所有接口统一使用 **SI 单位制**：

| 物理量 | 单位 | 符号 |
|--------|------|------|
| 力（升力/阻力/侧力） | N | L, D, Y |
| 力矩（滚转/俯仰/偏航） | N·m | Mx, My, Mz |
| 动压 | Pa | q_bar |
| 真空速 | m/s | V |
| 角度（攻角/侧滑角） | rad | α, β |
| 角速率 | rad/s | p, q, r |
| 角速率变化率 | rad/s^2 | α_dot, β_dot |
| 长度（弦长/翼展/参考长度） | m | c, b, l_ref |
| 面积（机翼面积/参考面积） | m^2 | S, S_ref |
| 马赫数 | 无量纲 | M |
| 几何尺度因子 | 无量纲 | R |

注意：AFSIM 原始代码使用 Imperial 单位（lb, ft, ft^2, ft-lb, psf 等）。本接口规格已将全部单位转换为 SI。

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|----------|----------|
| `RigidBodyAeroCoreObject` | 气动系数模型主类 | `RigidBodyAeroCoefficient` class（本章定义） |
| `AeroCoreObject` (基类) | 类继承（CL/Cd/CY 3D表 + 参考面积 + 模态管理） | 合并到 `RigidBodyAeroCoefficient::Config` 中 |
| `UtTable::Table` | 高维查表引擎（2D/3D表） | `std::function<double(...)>` 可调用对象，用户自行提供插值实现 |
| `UtTable::Curve` | 1D 曲线查表 | 同上，`std::function<double(double)>` |
| `UtInput` / `UtInputBlock` | 配置文件解析 | 不纳入接口；用户自行解析配置文件后填入 `Config` 结构体 |
| `UtVec3dX` | 三维矢量 | `double[3]` 原生数组 |
| `UtCloneablePtr` | 智能指针（深拷贝） | 不纳入接口；多模态切换由用户管理 |
| `UtMath::cRAD_PER_DEG` 等 | 数学常量 | 直接硬编码（`PI = 3.1415926535`, `DEG_PER_RAD = 57.2957795`） |
| `mSubModesList` | 多构型子模态列表 | 不纳入接口；若需多构型，创建多个 `RigidBodyAeroCoefficient` 实例并手动切换 |
