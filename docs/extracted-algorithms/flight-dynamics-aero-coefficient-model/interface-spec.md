# 稳定性导数气动系数模型 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-aero-coefficient-model-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────────┐
│                  P6DofAeroCoreObject                         │
│  (稳定性导数气动系数模型 — 高维查表 + 系数叠加)                 │
│  所有成员配置期加载、运行时只读（纯参数化函数）                   │
├──────────────────────────────────────────────────────────────┤
│  + CalculateCoreAeroFM(q, M, V, α, β, α̇, β̇, ω) → L,D,Y,M  │
│  + CalculateLiftAtSpecifiedAlpha_lbs(q, M, α)                │
│  + CalculateAeroCoefficientVectors(M, α, CL, Cd, Cm)         │
│  + SetModeName(name)          → 气动模态切换                  │
│  + GetAeroCenter_ft()         → 气动中心偏移                  │
│                                                                 │
│  25+ 查表函数（CL_AlphaBetaMach, Cd_AlphaBetaMach 等）:         │
│  - 6 个静态 3D 表 (Mach × Beta × Alpha)                      │
│  - 4 个动态导数 2D 表 (Mach × Alpha/Beta)                     │
│  - 11 个动态导数 1D 曲线 (Mach)                               │
│  - 4 个已弃用 Legacy 2D 表                                   │
│                                                                 │
│  几何参数:                                                      │
│  mWingChord_ft, mWingSpan_ft, mWingArea_sqft,               │
│  mRefArea_sqft, mRefLength_ft, mAeroCenter_ft                │
│                                                                 │
│  控制标志:                                                      │
│  mUseRefArea, mUseReducedFrequency, mUseLegacy                │
│                                                                 │
│  多模态支持:                                                    │
│  mSubModesList (气动构型切换，如挂弹/空载/襟翼)                  │
└──────────┬───────────────────────────────────────────────────┘
           │ 计算流程
           ▼
┌──────────────────────────────────────────────────────────────┐
│              CalculateCoreAeroFM 管道                         │
│                                                               │
│  输入 (参数)          处理                   输出 (引用返回)    │
│  ┌──────────┐    ┌──────────────┐        ┌────────────────┐  │
│  │ q_bar    │───→│ 角速率拆解    │        │ aLift_lbs      │  │
│  │ Mach     │    │ (p, q, r)    │        │   (升力 lbf)    │  │
│  │ V        │    ├──────────────┤        ├────────────────┤  │
│  │ α        │    │ 简化频率     │        │ aDrag_lbs      │  │
│  │ β        │    │ k = rate*L/2V│        │   (阻力 lbf)    │  │
│  │ α̇, β̇    │    ├──────────────┤        ├────────────────┤  │
│  │ ω_body   │    │ 静态3D表查值 │        │ aSideForce_lbs │  │
│  │ R_factor │    │ + 动态导数   │        │   (侧力 lbf)    │  │
│  └──────────┘    │    × 无量纲化 │        ├────────────────┤  │
│                  │   速率        │        │ aMoment_ftlbs  │  │
│                  ├──────────────┤        │   (力矩 ft-lbf) │  │
│                  │ 系数叠加     │        └────────────────┘  │
│                  ├──────────────┤                            │
│                  │ ×q_bar×S_ref │                            │
│                  │ ×L_ref       │                            │
│                  │ → 有量纲力/矩│                            │
│                  └──────────────┘                            │
└──────────────────────────────────────────────────────────────┘
```

**气动系数六分量结构：**

```
升力 (L)   = q̄·S_ref · [CL(α,β,M)                    → 静态3D表
                        + CLq(α,M) · k_q              → 俯仰阻尼
                        + CL_adot(α,M) · k_α̇          → 攻角延迟]  × R²

阻力 (D)   = q̄·S_ref · Cd(α,β,M)                     → 静态3D表（无动态项）× R²

侧力 (Y)   = q̄·S_ref · [CY(α,β,M)                    → 静态3D表
                        + CYr(β,M) · k_r              → 偏航速率侧力
                        + CY_bdot(β,M) · k_β̇          → 侧滑延迟侧力] × R²

俯仰力矩 = q̄·S_ref·c_ref · [Cm(α,β,M)                → 静态3D表
                             + Cmq(M)·k_q             → 俯仰阻尼
                             + Cmp(M)·k_p             → 滚转交叉
                             + Cm_adot(M)·k_α̇]        → 攻角延迟

偏航力矩 = q̄·S_ref·b · [Cn(α,β,M)                     → 静态3D表
                         + Cnr(M)·k_r                 → 偏航阻尼
                         + Cnp(M)·k_p                 → 滚转交叉
                         + Cn_bdot(M)·k_β̇]            → 侧滑延迟

滚转力矩 = q̄·S_ref·b · [Cl(α,β,M)                     → 静态3D表
                         + Clp(M)·k_p                 → 滚转阻尼
                         + Clr(M)·k_r                 → 偏航交叉
                         + Clq(M)·k_q                 → 俯仰交叉
                         + Cl_adot(M)·k_α̇             → 攻角延迟
                         + Cl_bdot(M)·k_β̇]            → 侧滑延迟
```

## 2. 核心接口定义

### 2.1 P6DofAeroCoreObject（稳定性导数气动模型）

```cpp
// 稳定性导数气动系数模型：基于飞行状态（α, β, Mach, 角速率, 变化率），
// 通过高维查表和多维插值计算六分量气动力/力矩。
//
// 核心计算方法论：
//   总系数 = 静态项(3D表) + Σ 动态导数 × 无量纲速率
//   有量纲力/力矩 = 总系数 × 动压 × 参考面积 × 参考长度
//
// 运行时只读：所有成员变量在配置期加载后不再修改（构型切换除外）。
// CalculateCoreAeroFM() 是纯函数，无副作用，不修改成员变量。
class P6DofAeroCoreObject {
public:
    // ---------- 初始化和模态管理 ----------

    // 从配置输入流读取全部气动参数（翼面几何 + 25+ 张气动数据表）
    bool ProcessInput(UtInput& aInput);

    // 初始化：将顶层控制设置（mUseLegacy, mUseReducedFrequency 等）传播到所有子模态
    bool Initialize();

    // 克隆：深拷贝整个气动模型（含所有数据表和子模态）
    P6DofAeroCoreObject* Clone() const;

    // ---------- 主气动力/力矩计算接口 ----------

    // 稳定性导数气动模型的完整计算入口（280 行）。
    // 给定飞行状态参数，通过查表和系数叠加计算六分量气动力/力矩。
    // 无副作用，不修改成员变量。
    void CalculateCoreAeroFM(
        double          aDynPress_lbsqft,   // [输入] 动压 q_bar = 0.5*ρ*V² (lb/ft²)
        double          aMach,              // [输入] 飞行马赫数 M（无量纲，用于查表）
        double          aSpeed_fps,         // [输入] 真空速 V (ft/s)，注意下限保护为 max(V, 1.0)
        double          aAlpha_rad,         // [输入] 攻角 α (rad)，体轴x与相对气流夹角
        double          aBeta_rad,          // [输入] 侧滑角 β (rad)，体轴y与相对气流夹角
        double          aAlphaDot_rps,      // [输入] 攻角变化率 α̇ (rad/s)
        double          aBetaDot_rps,       // [输入] 侧滑角变化率 β̇ (rad/s)
        const UtVec3dX& aAngularRates_rps,  // [输入] 体轴角速率 [p, q, r] (rad/s)
        UtVec3dX&       aMoment_ftlbs,      // [输出] 气动力矩 [Mx, My, Mz] = [滚转,俯仰,偏航] (ft-lbf)
        double&         aLift_lbs,          // [输出] 升力 (lbf)，垂直于相对气流方向
        double&         aDrag_lbs,          // [输出] 阻力 (lbf)，平行于相对气流方向
        double&         aSideForce_lbs,     // [输出] 侧力 (lbf)，垂直于升阻平面
        double          aRadiusSizeFactor = 1.0  // [输入] 几何尺度因子（默认1.0，用于降落伞/气球面积缩放）
    );

    // ---------- 单分量计算接口 ----------

    // 在指定攻角下计算升力（不含动态项）。
    // 常用于自动驾驶仪的攻角→升力换算。
    double CalculateLiftAtSpecifiedAlpha_lbs(
        double aDynPress_lbsqft,  // 动压 (lb/ft²)
        double aMach,             // 马赫数
        double aAlpha_deg,        // 攻角 (deg)
        double aRadiusSizeFactor = 1.0
    );

    // 计算升力/阻力/俯仰力矩系数（含参考面积效应，不含动压）。
    // 用于自动驾驶仪的配平攻角计算。
    void CalculateAeroCoefficientVectors(
        double  aMach,             // 马赫数
        double  aAlpha_rad,        // 攻角 (rad)
        double& aCLArea,           // [输出] CL × 参考面积（含半径因子）
        double& aCdArea,           // [输出] Cd × 参考面积
        double& aCmArea,           // [输出] Cm × 参考面积
        double  aRadiusSizeFactor = 1.0
    );

    // ---------- 升力系数查表（25+ 查表函数） ----------

    // 静态3D表：Mach × Beta × Alpha
    double CL_AlphaBetaMach(double aMach, double aAlpha_rad, double aBeta_rad);
        // 升力系数静态项（主要项），3D表 (Mach × Beta × Alpha)
    double Cd_AlphaBetaMach(double aMach, double aAlpha_rad, double aBeta_rad);
        // 阻力系数静态项（唯一项，无动态阻尼），3D表
    double CY_AlphaBetaMach(double aMach, double aAlpha_rad, double aBeta_rad);
        // 侧力系数静态项，3D表
    double Cm_AlphaBetaMach(double aMach, double aAlpha_rad, double aBeta_rad);
        // 俯仰力矩系数静态项，3D表
    double Cn_AlphaBetaMach(double aMach, double aAlpha_rad, double aBeta_rad);
        // 偏航力矩系数静态项，3D表
    double Cl_AlphaBetaMach(double aMach, double aAlpha_rad, double aBeta_rad);
        // 滚转力矩系数静态项，3D表

    // 升力动态导数 2D表：Mach × Alpha
    double CLq_AlphaMach(double aMach, double aAlpha_rad);
        // 俯仰阻尼升力导数 CLq，乘以 k_q 得升力增量
    double CL_AlphaDotAlphaMach(double aMach, double aAlpha_rad);
        // 攻角延迟升力导数 CL_adot，乘以 k_α̇ 得升力增量

    // 侧力动态导数 2D表：Mach × Beta
    double CYr_BetaMach(double aMach, double aBeta_rad);
        // 偏航速率侧力导数 CYr，乘以 k_r 得侧力增量
    double CY_BetaDotBetaMach(double aMach, double aBeta_rad);
        // 侧滑延迟侧力导数 CY_bdot，乘以 k_β̇ 得侧力增量

    // 俯仰力矩动态导数 1D曲线：仅 Mach
    double Cmq_Mach(double aMach);
        // 俯仰阻尼导数，乘以 k_q 得俯仰力矩增量
    double Cmp_Mach(double aMach);
        // 滚转-俯仰交叉导数，乘以 k_p 得俯仰力矩增量
    double CmAlphaDotMach(double aMach);
        // 攻角延迟俯仰力矩导数，乘以 k_α̇ 得俯仰力矩增量

    // 偏航力矩动态导数 1D曲线：仅 Mach
    double Cnr_Mach(double aMach);
        // 偏航阻尼导数，乘以 k_r 得偏航力矩增量
    double Cnp_Mach(double aMach);
        // 滚转-偏航交叉导数，乘以 k_p 得偏航力矩增量
    double CnBetaDotMach(double aMach);
        // 侧滑延迟偏航力矩导数，乘以 k_β̇ 得偏航力矩增量

    // 滚转力矩动态导数 1D曲线：仅 Mach
    double Clp_Mach(double aMach);
        // 滚转阻尼导数，乘以 k_p 得滚转力矩增量
    double Clr_Mach(double aMach);
        // 偏航-滚转交叉导数，乘以 k_r 得滚转力矩增量
    double Clq_Mach(double aMach);
        // 俯仰-滚转交叉导数，乘以 k_q 得滚转力矩增量
    double Cl_AlphaDotMach(double aMach);
        // 攻角延迟滚转力矩导数，乘以 k_α̇ 得滚转力矩增量
    double Cl_BetaDotMach(double aMach);
        // 侧滑延迟滚转力矩导数，乘以 k_β̇ 得滚转力矩增量

    // ---------- 已弃用的 Legacy 查表（alpha-only 2D，向后兼容） ----------

    // @deprecated 以下 Legacy 函数仅由 mUseLegacy=true 时激活，
    // 使用 deg/s 为单位的导数表（乘以 DEG_PER_RAD 转换）
    double CL_AlphaMach(double aMach, double aAlpha_rad);       // 旧版升力 2D (alpha-only)
    double Cd_AlphaMach(double aMach, double aAlpha_rad);       // 旧版阻力 2D (alpha-only)
    double Cd_BetaMach(double aMach, double aBeta_rad);         // 旧版阻力 2D (beta-only)
    double CY_BetaMach(double aMach, double aBeta_rad);         // 旧版侧力 2D (beta-only)
    double Cm_AlphaMach(double aMach, double aAlpha_rad);       // 旧版俯仰力矩 2D (alpha-only)
    double Cn_BetaMach(double aMach, double aBeta_rad);         // 旧版偏航力矩 2D (beta-only)
    double Cl_BetaMach(double aMach, double aBeta_rad);         // 旧版滚转力矩 2D (beta-only)

    // ---------- 模态管理 ----------

    // 切换气动构型模态（如挂弹→空载、襟翼收起→放下）
    void SetModeName(const std::string& aName);
    std::string GetModeName() const;

    // 按名称查找子模态
    P6DofAeroCoreObject* GetSubModeByName(const std::string& aName) const;

    // ---------- 几何参数查询 ----------

    UtVec3dX GetAeroCenter_ft() const;  // 气动中心相对参考点的偏移 (ft)
    double GetWingChord_ft() const;     // 机翼平均气动弦长 MAC (ft)
    double GetWingSpan_ft() const;      // 翼展 (ft)
    double GetWingArea_sqft() const;    // 机翼参考面积 (ft²)
    double GetRefArea_sqft() const;     // 显式参考面积 (ft²)，mUseRefArea=true 时替代机翼面积

    // ---------- 控制标志查询 ----------

    bool UsesRefArea() const;           // 是否使用显式参考面积
    bool UseLegacyAero() const;         // 是否使用 Legacy 旧版导数（已弃用）

protected:
    // ---------- 配置解析 ----------

    // 解析通用气动命令（25+ 种命令：翼面几何 + 导数表加载 + 模态定义）
    static bool ProcessCommonInput(UtInput& aInput, const std::string& aCommand,
                                   P6DofAeroCoreObject* aObject);

    // ---------- 几何参数 ----------

    double mWingChord_ft  = 0.0;   // 机翼平均气动弦长 (ft)，俯仰力矩无量纲化的参考长度
    double mWingSpan_ft   = 0.0;   // 翼展 (ft)，滚转/偏航力矩无量纲化的参考长度
    double mWingArea_sqft = 0.0;   // 机翼参考面积 (ft²)，所有力/力矩有量纲化的参考面积
    double mRefArea_sqft  = 0.0;   // 显式参考面积 (ft²)，mUseRefArea=true 时生效
    double mRefLength_ft  = 0.0;   // sqrt(mRefArea_sqft)，替代弦长/翼展用于无量纲化

    UtVec3dX mAeroCenter_ft;        // 气动中心相对参考点偏移 (ft)，影响力/力矩参考点位置

    // ---------- 控制标志 ----------

    bool mUseRefArea = false;           // true: 使用 mRefArea/mRefLength（非翼面气动体）
                                        // false: 使用翼面参数（标准飞行器）
    bool mUseLegacy = false;            // true: 使用已弃用的 alpha-only / beta-only 导数表
    bool mUseLegacySet = false;         // 是否显式设置过 legacy 标志
    bool mUseReducedFrequency = true;   // true: 角速率无量纲化（默认）
                                        // false: 直接用有量纲角速率（已弃用）
    bool mUseReducedFrequencySet = false;

    // ---------- 模态管理 ----------

    std::string mModeName = "DEFAULT";  // 当前激活的模态名称
    std::list<UtCloneablePtr<P6DofAeroCoreObject>> mSubModesList;
        // 多构型子模态列表：每个子模态有独立的全套气动参数表
        // 构型切换时，气动力计算委托给对应子模态完成

    // ---------- 25+ 张气动数据表指针 ----------

    // == 升力 (Lift) ==
    UtCloneablePtr<UtTable::Table> mCL_AlphaBetaMachTablePtr{nullptr};
        // CL 静态 3D表 (Mach × Beta × Alpha) — 升力系数主要来源
    UtCloneablePtr<UtTable::Table> mCLq_AlphaMachTablePtr{nullptr};
        // CLq 俯仰阻尼升力导数 2D表 (Mach × Alpha)
    UtCloneablePtr<UtTable::Table> mCL_AlphaDotAlphaMachTablePtr{nullptr};
        // CL_adot 攻角延迟升力导数 2D表 (Mach × Alpha)

    // == 阻力 (Drag) ==
    UtCloneablePtr<UtTable::Table> mCd_AlphaBetaMachTablePtr{nullptr};
        // Cd 静态 3D表 (Mach × Beta × Alpha) — 阻力系数唯一来源（无动态项）

    // == 侧力 (Side Force) ==
    UtCloneablePtr<UtTable::Table> mCY_AlphaBetaMachTablePtr{nullptr};
        // CY 静态 3D表 (Mach × Beta × Alpha)
    UtCloneablePtr<UtTable::Table> mCYr_BetaMachTablePtr{nullptr};
        // CYr 偏航速率侧力导数 2D表 (Mach × Beta)
    UtCloneablePtr<UtTable::Table> mCY_BetaDotBetaMachTablePtr{nullptr};
        // CY_bdot 侧滑延迟侧力导数 2D表 (Mach × Beta)

    // == 俯仰力矩 (Pitching Moment) ==
    UtCloneablePtr<UtTable::Table> mCm_AlphaBetaMachTablePtr{nullptr};
        // Cm 静态 3D表 (Mach × Beta × Alpha)
    UtCloneablePtr<UtTable::Curve> mCmq_MachCurvePtr{nullptr};
        // Cmq 俯仰阻尼导数 1D曲线 (Mach)
    UtCloneablePtr<UtTable::Curve> mCmp_MachCurvePtr{nullptr};
        // Cmp 滚转-俯仰交叉导数 1D曲线 (Mach)
    UtCloneablePtr<UtTable::Curve> mCm_AlphaDotMachCurvePtr{nullptr};
        // Cm_adot 攻角延迟俯仰力矩导数 1D曲线 (Mach)

    // == 偏航力矩 (Yawing Moment) ==
    UtCloneablePtr<UtTable::Table> mCn_AlphaBetaMachTablePtr{nullptr};
        // Cn 静态 3D表 (Mach × Beta × Alpha)
    UtCloneablePtr<UtTable::Curve> mCnr_MachCurvePtr{nullptr};
        // Cnr 偏航阻尼导数 1D曲线 (Mach)
    UtCloneablePtr<UtTable::Curve> mCnp_MachCurvePtr{nullptr};
        // Cnp 滚转-偏航交叉导数 1D曲线 (Mach)
    UtCloneablePtr<UtTable::Curve> mCn_BetaDotMachCurvePtr{nullptr};
        // Cn_bdot 侧滑延迟偏航力矩导数 1D曲线 (Mach)

    // == 滚转力矩 (Rolling Moment) ==
    UtCloneablePtr<UtTable::Table> mCl_AlphaBetaMachTablePtr{nullptr};
        // Cl 静态 3D表 (Mach × Beta × Alpha)
    UtCloneablePtr<UtTable::Curve> mClp_MachCurvePtr{nullptr};
        // Clp 滚转阻尼导数 1D曲线 (Mach)
    UtCloneablePtr<UtTable::Curve> mClr_MachCurvePtr{nullptr};
        // Clr 偏航-滚转交叉导数 1D曲线 (Mach)
    UtCloneablePtr<UtTable::Curve> mClq_MachCurvePtr{nullptr};
        // Clq 俯仰-滚转交叉导数 1D曲线 (Mach)
    UtCloneablePtr<UtTable::Curve> mCl_AlphaDotMachCurvePtr{nullptr};
        // Cl_adot 攻角延迟滚转力矩导数 1D曲线 (Mach)
    UtCloneablePtr<UtTable::Curve> mCl_BetaDotMachCurvePtr{nullptr};
        // Cl_bdot 侧滑延迟滚转力矩导数 1D曲线 (Mach)

    // == 已弃用 Legacy 表 ==
    UtCloneablePtr<UtTable::Table> mCL_AlphaMachTablePtr{nullptr};  // @deprecated
    UtCloneablePtr<UtTable::Table> mCd_AlphaMachTablePtr{nullptr};  // @deprecated
    UtCloneablePtr<UtTable::Table> mCd_BetaMachTablePtr{nullptr};   // @deprecated
    UtCloneablePtr<UtTable::Table> mCY_BetaMachTablePtr{nullptr};   // @deprecated
    UtCloneablePtr<UtTable::Table> mCm_AlphaMachTablePtr{nullptr};  // @deprecated
    UtCloneablePtr<UtTable::Table> mCn_BetaMachTablePtr{nullptr};   // @deprecated
    UtCloneablePtr<UtTable::Table> mCl_BetaMachTablePtr{nullptr};   // @deprecated
};
```

### 2.2 简化频率（Reduced Frequency）计算说明

```cpp
// ===== 简化频率（无量纲化角速率）的计算 =====
// 这是稳定性导数法中最重要的预处理步骤：
// 将有量纲角速率和变化率消除飞行器尺寸和飞行速度的量纲影响。

// 基础无量纲化（除以 2V，V 下限保护为 1 ft/s）：
double speedSafe = max(aSpeed_fps, 1.0);  // 防止 V=0 时除零
double kq_raw = pitchRate_rps / (2.0 * speedSafe);   // 俯仰无量纲速率
double kr_raw = yawRate_rps   / (2.0 * speedSafe);   // 偏航无量纲速率
double kp_raw = rollRate_rps  / (2.0 * speedSafe);   // 滚转无量纲速率
double ka_raw = alphaDot_rps  / (2.0 * speedSafe);   // 攻角变化率无量纲速率
double kb_raw = betaDot_rps   / (2.0 * speedSafe);   // 侧滑角变化率无量纲速率

// 乘以参考长度（简化频率模式）：
if (mUseReducedFrequency) {
    if (mUseRefArea) {
        // 使用显式参考长度
        // 俯仰相关用量纲化速率 × refLength
        // 滚转/偏航相关用量纲化速率 × refLength
    } else {
        // 使用翼面参数
        // 俯仰相关：k × wingChord（弦长）
        // 滚转/偏航相关：k × wingSpan（翼展）
    }
} else {
    // 直接使用有量纲角速率（已弃用模式）
}
```

## 3. 典型调用模式

```cpp
// ========== 1. 配置加载 ==========

// 从 JSON/XML 配置文件加载气动数据：
P6DofAeroCoreObject aeroModel;

// 加载翼面几何参数：
//   wing_chord_ft  = 12.0    → 机翼弦长 12 ft
//   wing_span_ft   = 40.0    → 翼展 40 ft
//   wing_area_sqft = 400.0   → 机翼面积 400 ft²
//   aero_center_x/y/z = (0, 0, 0) → 气动中心与参考点重合

// 加载 25+ 张气动数据表（风洞试验或 CFD 数据）：
//   cL_alpha_beta_mach_table    → CL 3D表 (Mach×Beta×Alpha)
//   cd_alpha_beta_mach_table    → Cd 3D表
//   cY_alpha_beta_mach_table    → CY 3D表
//   cLq_alpha_mach_table        → CLq 2D表 (Mach×Alpha)
//   cL_alpha_dot_alpha_mach_table → CL_adot 2D表
//   cm_alpha_beta_mach_table    → Cm 3D表
//   cmq_mach_curve              → Cmq 1D曲线 (Mach)
//   ... 等 19 张其他导数表/曲线
//   aero_mode (子模态)          → 多构型数据（可选）

aeroModel.ProcessInput(configInput);
aeroModel.Initialize();  // 传播控制设置到所有子模态

// ========== 2. 每帧气动力/力矩计算 ==========

// 在积分器的 CalculateFM() 中调用：
void Integrator::calculateAeroForces(KinematicState& state) {
    // 从运动学状态获取当前飞行条件
    double q_bar   = state.GetDynamicPressure_lbsqft();   // 动压 (lb/ft²)
    double mach    = state.GetMach();                     // 马赫数
    double speed   = state.GetTrueAirspeed_fps();          // 真空速 (ft/s)
    double alpha   = state.GetAlpha_rad();                 // 攻角 (rad)
    double beta    = state.GetBeta_rad();                  // 侧滑角 (rad)
    double alpha_d = state.GetAlphaDot_rps();              // 攻角变化率 (rad/s)
    double beta_d  = state.GetBetaDot_rps();               // 侧滑角变化率 (rad/s)
    UtVec3dX omega = state.GetOmegaBody();                 // 体轴角速率 [p,q,r] (rad/s)

    double lift_lbs, drag_lbs, sideForce_lbs;
    UtVec3dX moment_ftlbs;

    // 一键计算全部六分量气动力/力矩：
    //   内部流程：
    //   1) 角速率拆分：p, q, r
    //   2) 简化频率：k_q = q*c/(2V), k_r = r*b/(2V), k_p = p*b/(2V),
    //               k_α̇ = α̇*c/(2V), k_β̇ = β̇*b/(2V)
    //   3) 静态3D表查值：CL/Cd/CY/Cm/Cn/Cl
    //   4) 动态导数 × 简化频率 → 各分量增量
    //   5) 系数叠加：总系数 = 静态项 + Σ(导数 × 无量纲速率)
    //   6) 有量纲化：力 = q̄ × S_ref × 总系数  (力矩 × 对应参考长度)
    //   7) 几何尺度因子：力 × R², 力矩按对应面积和长度缩放
    aeroModel.CalculateCoreAeroFM(
        q_bar, mach, speed,           // 飞行条件
        alpha, beta,                  // 气动角
        alpha_d, beta_d,              // 气动角变化率
        omega,                        // 体轴角速率 (rad/s)
        moment_ftlbs,                 // [输出] 气动力矩 [Mx,My,Mz] (ft-lbf)
        lift_lbs, drag_lbs, sideForce_lbs,  // [输出] 升力/阻力/侧力 (lbf)
        1.0                           // 几何尺度因子 = 1.0 (标准飞行器)
    );

    // 后续：结合气动参考点偏移（mAeroCenter_ft），
    // 将气动力/力矩叠加到总 ForceAndMomentsObject
}

// ========== 3. 多模态构型切换 ==========

// 场景：导弹从内部挂载释放后切换为自由飞行模式
aeroModel.SetModeName("INTERNAL_CARRIAGE");  // 挂载模式（零气动）
// ... 在挂架内时，气动力/力矩全为零 ...

aeroModel.SetModeName("FREE_FLIGHT");        // 切换到自由飞行模式
// ... 释放后，正常计算气动力/力矩 ...

// ========== 4. 自动驾驶仪用升力查询 ==========

// 自动驾驶仪需要查询指定攻角下的升力（用于 g-load→攻角转换）
double alpha_deg = 5.0;  // 配平攻角 5°
double lift_at_5deg = aeroModel.CalculateLiftAtSpecifiedAlpha_lbs(
    q_bar,           // 当前动压
    mach,            // 当前马赫数
    alpha_deg,       // 指定攻角 (deg)
    1.0              // 标准几何尺度因子
);
// 升力 = q̄ × S_ref × CL(α=5°, Mach) × R²  → 直接返回有量纲力 (lbf)

// ========== 5. 配平攻角计算 ==========

// 使用 CalculateAeroCoefficientVectors 获取系数面积积
double clArea, cdArea, cmArea;
aeroModel.CalculateAeroCoefficientVectors(
    mach, 0.1,            // Mach, Alpha (rad)
    clArea, cdArea, cmArea
);
// clArea = CL × S_ref × R²  → 可直接乘以动压得到升力
```

## 4. 坐标系/单位约定

### 坐标系

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **Body（体轴系）** | X=前, Y=右, Z=下 | 角速率 [p,q,r] 和气动力/力矩的表达坐标系 |
| **Wind（气流系）** | X=迎流方向 | 升力（⊥气流）和阻力（∥气流）定义在气流系中 |

### 攻角/侧滑角的定义

- **攻角 α**：体轴 X（前）与相对气流方向的夹角，从体轴 Z 向 Y 旋转为正
- **侧滑角 β**：体轴 Y（右）与相对气流方向的夹角

### 简化频率（Reduced Frequency）物理含义

简化频率将角速率无量纲化，消除飞行器尺寸和飞行速度的影响：
- **k_q** = q·c_ref / (2V)：俯仰角速率的无量纲度量，c_ref 为弦长
- **k_r** = r·b / (2V)：偏航角速率的无量纲度量，b 为翼展
- **k_p** = p·b / (2V)：滚转角速率的无量纲度量

无量纲化使得不同尺寸、不同速度下的气动数据可直接比较和共用。

### 单位约定（AFSIM 原始代码 Imperial 单位）

| 物理量 | AFSIM 原始单位 | 说明 |
|--------|---------------|------|
| 长度（弦长、翼展、参考长度） | ft | 1 ft = 0.3048 m |
| 面积（机翼面积、参考面积） | ft² | 1 ft² = 0.0929 m² |
| 速度 | ft/s | 1 ft/s = 0.3048 m/s |
| 角速率 | rad/s | 统一 |
| 动压 q_bar | lb/ft² (psf) | 1 psf = 47.88 Pa |
| 力（升力/阻力/侧力） | lbf | 1 lbf = 4.448 N |
| 力矩 | ft-lbf | 1 ft-lbf = 1.356 N·m |
| 攻角/侧滑角 | rad | 统一 |
| 马赫数 | 无量纲 | 统一 |
| 气动系数 (CL/Cd/CY/Cm/Cn/Cl) | 无量纲 | 统一 |

### 为统一移植建议使用的 SI 单位制

所有新实现建议统一使用 SI：
- 长度 m, 面积 m², 速度 m/s, 角速率 rad/s
- 动压 Pa, 力 N, 力矩 N·m
- 气动系数保持无量纲

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|----------|----------|
| `P6DofAeroCoreObject` | 气动模型主体 | 自定义 `AeroCoefficientModel` 类（数据表 + 简化频率 + 系数叠加 + 有量纲化） |
| `UtTable::Table` | 多维查表引擎（3D/2D） | 自定义多维线性插值表（支持 2D 和 3D） |
| `UtTable::Curve` | 1D 曲线 | 自定义 1D 线性/Akima/Cubic Spline 插值 |
| `UtInput` / `UtInputBlock` | 配置解析 | JSON/YAML/TOML 解析器 |
| `UtVec3dX` | 三维矢量 | `Eigen::Vector3d` |
| `UtCloneablePtr` | 智能深拷贝指针 | `std::unique_ptr`（加 Clone 方法）或 `std::shared_ptr` |
| `UtMath::cPI / cDEG_PER_RAD / cRAD_PER_DEG / cFT_PER_M` | 数学和单位换算常数 | 直接硬编码 `M_PI`, `57.29578`, `0.0174533`, `0.3048` |

**核心需要重新实现的组件：**
1. **多维插值表** (MultivariateLookupTable)：替代 `UtTable::Table`，支持 2D（Mach×Alpha, Mach×Beta）和 3D（Mach×Beta×Alpha）线性插值，边界外 clamp-to-edge 行为
2. **1D 插值曲线** (InterpolationCurve)：替代 `UtTable::Curve`，支持线性插值，边界外 clamp-to-edge
3. **气动数据加载器**：从用户提供的 JSON/YAML 配置文件加载全部 25+ 张数据表，填充到上述表格对象中

**移植简化建议：**
1. Legacy 模式（alpha-only 导数表）和 non-ReducedFrequency 模式（有量纲角速率）均为已弃用功能，移植时可**完全移除**
2. 多模态支持（mSubModesList）可简化为单模态（大多数飞行器只有一个气动构型）
3. mUseRefArea 可简化为始终使用翼面参数（标准飞行器）或始终使用显式参考面积
4. 建议将 20+ 张导数表的名称统一为一个结构体 `StabilityDerivatives`，清晰组织
