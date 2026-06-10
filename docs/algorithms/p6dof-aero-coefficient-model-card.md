# Algorithm Card — P6DOF 气动系数模型

## Metadata

- **Algorithm name**: P6DOF Stability-Derivative Aerodynamic Model（P6DOF 稳定性导数气动模型）
- **Domain**: Aerodynamics / Flight Dynamics — 线性/非线性气动力系数查表与插值
- **Date**: 2026-06-10
- **Analyst**: afsim-algorithm-extractor
- **Status**: draft

## Purpose

基于飞行状态（马赫数、攻角、侧滑角、角速率、攻角变化率、侧滑角变化率）通过高维查表和多维插值计算气动力系数（升力 CL、阻力 Cd、侧力 CY、俯仰力矩 Cm、偏航力矩 Cn、滚转力矩 Cl），再乘以动压和参考面积得到气动力和力矩。

## Source Locations

| File | Symbol | Lines | Evidence level | 中文说明 |
|------|--------|-------|---------------|----------|
| [P6DofAeroCoreObject.hpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofAeroCoreObject.hpp) | `P6DofAeroCoreObject::CalculateCoreAeroFM()` | 55-67 | source-cited | 气动力/力矩主计算函数 — 接收动压/马赫/速度/气动角/角速率，输出六分量 |
| [P6DofAeroCoreObject.hpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofAeroCoreObject.hpp) | 全类定义 + 20 个稳定性导数查表 | 31-218 | source-cited | 气动核心对象全量 — 包含所有查表成员变量和模态切换逻辑 |
| [P6DofAeroCoreObject.hpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofAeroCoreObject.hpp) | `CL_AlphaBetaMach`, `Cd_AlphaBetaMach`, `CY_AlphaBetaMach`, `Cm_AlphaBetaMach` 等 | 93-131 | source-cited | 六分量 3D 查表接口 — 升力/阻力/侧力/俯仰/偏航/滚转的静态系数查询 |
| [P6DofAeroCoreObject.hpp](source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/p6dof/source/P6DofAeroCoreObject.hpp) | `CLq_AlphaMach`, `Cmq_Mach`, `CL_AlphaDotAlphaMach` 等 | 93-131 | source-cited | 动态阻尼和非定常导数查表接口 — 角速率和变化率对系数的增量贡献 |

## Entry Point & Call Chain

```
// 从积分器进入 → 先算气动状态 → 再调气动模型计算力/力矩 → 内部分派到各查表
P6DofIntegrator::CalculateFM()                              // 力/力矩汇总函数 — 积分器调用以获取当前飞行条件下的总力
  → aState.UpdateAeroState()                                // 更新气动状态：α, β, Mach, q_bar, ρ, α̇, β̇
  → object.CalculateAeroBodyFM()                            // 计算气动力/力矩矢量（体轴系）
    → P6DofAeroCoreObject::CalculateCoreAeroFM(             // 气动系数模型主入口
        q_bar,    // 动压 (lb/ft²)
        Mach,     // 马赫数
        V,        // 真空速 (ft/s)
        α, β,     // 攻角/侧滑角 (rad)
        α̇, β̇,     // 攻角/侧滑角变化率 (rad/s)
        ω_vec,    // 体轴角速率 [roll, pitch, yaw] (rad/s)
        ...)
      → CL_AlphaBetaMach(Mach, α, β)   // 升力系数 3D 表 — 静态项
      → Cd_AlphaBetaMach(Mach, α, β)   // 阻力系数 3D 表
      → CY_AlphaBetaMach(Mach, α, β)   // 侧力系数 3D 表
      → Cm_AlphaBetaMach(Mach, α, β)   // 俯仰力矩系数 3D 表
      → Cn_AlphaBetaMach(Mach, α, β)   // 偏航力矩系数 3D 表
      → Cl_AlphaBetaMach(Mach, α, β)   // 滚转力矩系数 3D 表
      → CLq_AlphaMach(Mach, α)         // 升力对俯仰速率的导数 — 阻尼增量
      → Cmq_Mach(Mach)                 // 俯仰力矩对俯仰速率的阻尼导数
      → CL_AlphaDotAlphaMach(Mach, α)  // 升力对攻角变化率（非定常）的导数
      ... 等 20+ 条查表（完整见下方 Internal State 表格）
```

## Inputs

| Name | Type | Meaning | Units | Source |
|------|------|--------|-------|--------|
| `aDynPress_lbsqft` | `double` | 动压 $\bar{q} = \frac{1}{2}\rho V^2$ | lb/ft² | atmospheric + velocity |
| `aMach` | `double` | 马赫数 | — | velocity / speed of sound |
| `aSpeed_fps` | `double` | 真空速 | ft/s | kinematic state |
| `aAlpha_rad` | `double` | 攻角 | rad | kinematic state |
| `aBeta_rad` | `double` | 侧滑角 | rad | kinematic state |
| `aAlphaDot_rps` | `double` | 攻角变化率 $\dot{\alpha}$ | rad/s | kinematic state |
| `aBetaDot_rps` | `double` | 侧滑角变化率 $\dot{\beta}$ | rad/s | kinematic state |
| `aAngularRates_rps` | `UtVec3dX` | 体轴角速率 (p, q, r) | rad/s | kinematic state |
| `aRadiusSizeFactor` | `double` | 尺度因子（缩放气动面） | — | config |

## Outputs

| Name | Type | Meaning | Units | Source |
|------|------|--------|-------|--------|
| `aMoment_ftlbs` | `UtVec3dX&` | 气动力矩 [roll, pitch, yaw] | ft·lb | output arg |
| `aLift_lbs` | `double&` | 升力大小 | lb | output arg |
| `aDrag_lbs` | `double&` | 阻力大小 | lb | output arg |
| `aSideForce_lbs` | `double&` | 侧力大小 | lb | output arg |

## Internal State (Aero Tables via `UtTable::Table` / `UtTable::Curve`)

### 升力导数 (Lift)

| 查表变量名 | 数学符号 | 维度 | 说明 |
|-----------|----------|------|------|
| `mCL_AlphaBetaMachTablePtr` | $C_L(\alpha, \beta, M)$ | 3D | 升力系数 — 静态项，速度向量法向 |
| `mCLq_AlphaMachTablePtr` | $C_{L_q}(\alpha, M)$ | 2D | 俯仰阻尼升力导数 — 由俯仰速率 q 产生的升力增量 |
| `mCL_AlphaDotAlphaMachTablePtr` | $C_{L_{\dot{\alpha}}}(\alpha, M)$ | 2D | 攻角延迟导数 — 非定常流动滞后效应产生的升力增量 |

### 阻力导数 (Drag)

| 查表变量名 | 数学符号 | 维度 | 说明 |
|-----------|----------|------|------|
| `mCd_AlphaBetaMachTablePtr` | $C_d(\alpha, \beta, M)$ | 3D | 阻力系数 — 速度向量方向，含零升阻力 + 诱导阻力 |

### 侧力导数 (Side Force)

| 查表变量名 | 数学符号 | 维度 | 说明 |
|-----------|----------|------|------|
| `mCY_AlphaBetaMachTablePtr` | $C_Y(\alpha, \beta, M)$ | 3D | 侧力系数 — 体轴 y 方向 |
| `mCYr_BetaMachTablePtr` | $C_{Y_r}(\beta, M)$ | 2D | 偏航速率侧力 — 偏航速率 r 产生的侧力增量 |
| `mCY_BetaDotBetaMachTablePtr` | $C_{Y_{\dot{\beta}}}(\beta, M)$ | 2D | 侧滑延迟侧力 — 非定常侧滑变化产生的侧力增量 |

### 俯仰力矩导数 (Pitching Moment)

| 查表变量名 | 数学符号 | 维度 | 说明 |
|-----------|----------|------|------|
| `mCm_AlphaBetaMachTablePtr` | $C_m(\alpha, \beta, M)$ | 3D | 俯仰力矩系数 — 绕体轴 y，抬头为正 |
| `mCmq_MachCurvePtr` | $C_{m_q}(M)$ | 1D | 俯仰阻尼导数 — 俯仰速率 q 产生的阻尼力矩 |
| `mCmp_MachCurvePtr` | $C_{m_p}(M)$ | 1D | 滚转-俯仰交叉导数 — 滚转速率 p 对俯仰力矩的影响 |
| `mCm_AlphaDotMachCurvePtr` | $C_{m_{\dot{\alpha}}}(M)$ | 1D | 攻角延迟俯仰力矩 — 非定常 α̇ 产生的俯仰力矩 |

### 偏航力矩导数 (Yawing Moment)

| 查表变量名 | 数学符号 | 维度 | 说明 |
|-----------|----------|------|------|
| `mCn_AlphaBetaMachTablePtr` | $C_n(\alpha, \beta, M)$ | 3D | 偏航力矩系数 — 绕体轴 z，机头右偏为正 |
| `mCn_BetaDotMachCurvePtr` | $C_{n_{\dot{\beta}}}(M)$ | 1D | 侧滑延迟偏航力矩 — 非定常 β̇ 产生的偏航力矩 |
| `mCnr_MachCurvePtr` | $C_{n_r}(M)$ | 1D | 偏航阻尼导数 — 偏航速率 r 产生的阻尼力矩 |
| `mCnp_MachCurvePtr` | $C_{n_p}(M)$ | 1D | 滚转-偏航交叉导数 — 滚转速率 p 对偏航力矩的影响 |

### 滚转力矩导数 (Rolling Moment)

| 查表变量名 | 数学符号 | 维度 | 说明 |
|-----------|----------|------|------|
| `mCl_AlphaBetaMachTablePtr` | $C_l(\alpha, \beta, M)$ | 3D | 滚转力矩系数 — 绕体轴 x，右翼下沉为正 |
| `mClp_MachCurvePtr` | $C_{l_p}(M)$ | 1D | 滚转阻尼导数 — 滚转速率 p 产生的阻尼力矩 |
| `mClr_MachCurvePtr` | $C_{l_r}(M)$ | 1D | 偏航-滚转交叉导数 — 偏航 r 对滚转的影响 |
| `mClq_MachCurvePtr` | $C_{l_q}(M)$ | 1D | 俯仰-滚转交叉导数 — 俯仰 q 对滚转的影响 |
| `mCl_AlphaDotMachCurvePtr` | $C_{l_{\dot{\alpha}}}(M)$ | 1D | 攻角延迟滚转 — 非定常 α̇ 对滚转的影响 |
| `mCl_BetaDotMachCurvePtr` | $C_{l_{\dot{\beta}}}(M)$ | 1D | 侧滑延迟滚转 — 非定常 β̇ 对滚转的影响 |

## Mathematical Form

### 气动系数模型架构

总气动力/力矩 = 静态项 + 动态阻尼项 + 非定常延迟项 + 操纵面增量。

#### 升力

$$C_L = C_L(\alpha, \beta, M) \quad (\text{3D 查表 — 静态项})$$

$$C_{L\_total} = C_L + C_{L_q} \cdot \frac{q \cdot c_{ref}}{2V} + C_{L_{\dot{\alpha}}} \cdot \frac{\dot{\alpha} \cdot c_{ref}}{2V}$$

升力（有量纲）：
$$L = \bar{q} \cdot S_{ref} \cdot C_{L\_total}$$

#### 阻力

$$C_d = C_d(\alpha, \beta, M) \quad (\text{3D 查表，通常无动态项})$$

$$D = \bar{q} \cdot S_{ref} \cdot C_d$$

#### 侧力

$$C_Y = C_Y(\alpha, \beta, M) + C_{Y_r} \cdot \frac{r \cdot b}{2V} + C_{Y_{\dot{\beta}}} \cdot \frac{\dot{\beta} \cdot b}{2V}$$

$$Y = \bar{q} \cdot S_{ref} \cdot C_Y$$

#### 俯仰力矩

$$C_m = C_m(\alpha, \beta, M) + C_{m_q} \cdot \frac{q \cdot c_{ref}}{2V} + C_{m_p} \cdot \frac{p \cdot b}{2V} + C_{m_{\dot{\alpha}}} \cdot \frac{\dot{\alpha} \cdot c_{ref}}{2V}$$

$$M_y = \bar{q} \cdot S_{ref} \cdot c_{ref} \cdot C_m$$

#### 偏航力矩

$$C_n = C_n(\alpha, \beta, M) + C_{n_r} \cdot \frac{r \cdot b}{2V} + C_{n_p} \cdot \frac{p \cdot b}{2V} + C_{n_{\dot{\beta}}} \cdot \frac{\dot{\beta} \cdot b}{2V}$$

$$M_z = \bar{q} \cdot S_{ref} \cdot b \cdot C_n$$

#### 滚转力矩

$$C_l = C_l(\alpha, \beta, M) + C_{l_p} \cdot \frac{p \cdot b}{2V} + C_{l_r} \cdot \frac{r \cdot b}{2V} + C_{l_q} \cdot \frac{q \cdot c_{ref}}{2V} + C_{l_{\dot{\alpha}}} \cdot \frac{\dot{\alpha} \cdot c_{ref}}{2V} + C_{l_{\dot{\beta}}} \cdot \frac{\dot{\beta} \cdot b}{2V}$$

$$M_x = \bar{q} \cdot S_{ref} \cdot b \cdot C_l$$

其中：
- $\bar{q} = \frac{1}{2}\rho V^2$ — 动压 (lb/ft²)
- $S_{ref}$ — 参考面积（机翼面积 `mWingArea_sqft` 或显式 `mRefArea_sqft`）
- $b$ — 翼展 (`mWingSpan_ft`)
- $c_{ref}$ — 参考弦长 (`mWingChord_ft` 或 `mRefLength_ft`)
- $p, q, r$ — 体轴角速率 (roll, pitch, yaw, rad/s)
- $V$ — 真空速 (ft/s)

### 气动模态（Aero Modes）

通过 `mSubModesList` 支持多种构型（如内部挂载/自由飞行/不同襟翼设置），每种模态有自己的整套气动参数表。在 `SetModeName()` 时切换。这允许同一飞行器在不同状态下（挂弹/空载）使用不同的气动参数。

### 简化频率（Reduced Frequency）

当 `mUseReducedFrequency = true`（默认值）时，角速率项用简化频率而非直接的 $p, q, r$ 计算，以消除飞行器尺寸和速度的量纲影响：
$$\text{reduced freq} = \frac{\omega \cdot c_{ref}}{2V}$$

## Pseudocode

```text
algorithm Calculate_Aero_FM(q_bar, Mach, V, α, β, α_dot, β_dot, ω_body, radius_factor, aero_mode):
    // 气动系数模型：稳定性导数法 — 系数 = 静态查表 + 动态阻尼 + 非定常增量

    // 选择当前气动模态（不同构型有不同的气动参数表）
    mode = aero_mode or default_mode

    // 1. 静态项 — 从 3D 表 (α × β × Mach) 查取基础系数
    CL_static  = mode.lookup_CL(α, β, Mach)    // 升力系数静态项
    Cd_static  = mode.lookup_Cd(α, β, Mach)    // 阻力系数静态项
    CY_static  = mode.lookup_CY(α, β, Mach)    // 侧力系数静态项
    Cm_static  = mode.lookup_Cm(α, β, Mach)    // 俯仰力矩系数静态项
    Cn_static  = mode.lookup_Cn(α, β, Mach)    // 偏航力矩系数静态项
    Cl_static  = mode.lookup_Cl(α, β, Mach)    // 滚转力矩系数静态项

    // 2. 动态阻尼项 + 非定常增量 — 无量纲化角速率后乘以对应导数
    if mode.use_reduced_frequency:
        // 简化频率法：用无量纲速率消除飞行器尺寸和速度的量纲影响
        p_hat = p * b / (2*V)   // 无量纲滚转速率
        q_hat = q * c / (2*V)   // 无量纲俯仰速率
        r_hat = r * b / (2*V)   // 无量纲偏航速率
        α_dot_hat = α_dot * c / (2*V)    // 无量纲攻角变化率
        β_dot_hat = β_dot * b / (2*V)    // 无量纲侧滑角变化率
    else:
        use raw angular rates    // 罕见：直接用有量纲角速率（旧模式，已弃用）

    // 各分量增量 = 对应导数 × 对应无量纲速率
    ΔCL = CLq(α,Mach) * q_hat  +  CL_α_dot(α,Mach) * α_dot_hat
    ΔCY = CYr(β,Mach) * r_hat  +  CY_β_dot(β,Mach) * β_dot_hat
    ΔCm = Cmq(Mach)  * q_hat  +  Cmp(Mach) * p_hat  +  Cm_α_dot(Mach) * α_dot_hat
    ΔCn = Cnr(Mach)  * r_hat  +  Cnp(Mach) * p_hat  +  Cn_β_dot(Mach) * β_dot_hat
    ΔCl = Clp(Mach)  * p_hat  +  Clr(Mach) * r_hat   +  Clq(Mach) * q_hat
          + Cl_α_dot(Mach) * α_dot_hat  +  Cl_β_dot(Mach) * β_dot_hat

    // 3. 总系数 = 静态项 + 增量
    CL_total = CL_static + ΔCL
    Cd_total = Cd_static      // 阻力通常不包含动态增量
    CY_total = CY_static + ΔCY
    Cm_total = Cm_static + ΔCm
    Cn_total = Cn_static + ΔCn
    Cl_total = Cl_static + ΔCl

    // 4. 乘以动压 × 参考面积（及参考长度）得到有量纲力/力矩
    factor       = q_bar * S_ref * radius_factor       // 动压 × 参考面积 × 尺度因子
    lift         = factor * CL_total                    // 升力 (lb) — 垂直于相对气流
    drag         = factor * Cd_total                    // 阻力 (lb) — 平行于相对气流
    side_force   = factor * CY_total                    // 侧力 (lb) — 垂直于升力-阻力平面
    roll_moment  = factor * b * Cl_total                // 滚转力矩 (ft·lb) — 绕体轴 x
    pitch_moment = factor * c * Cm_total                // 俯仰力矩 (ft·lb) — 绕体轴 y
    yaw_moment   = factor * b * Cn_total                // 偏航力矩 (ft·lb) — 绕体轴 z

    return lift, drag, side_force, [roll, pitch, yaw]_moment
```

## Variable Mapping

| Code variable | Math symbol | Meaning | 中文说明 |
|--------------|-------------|---------|----------|
| `aDynPress_lbsqft` | $\bar{q}$ | 动压 (lb/ft²) | ½ρV² — 将气动系数转换为有量纲力的关键因子 |
| `aMach` | $M$ | 马赫数 | 压缩性效应的支配参数 |
| `aSpeed_fps` | $V$ | 真空速 (ft/s) | 用于无量纲化角速率 |
| `aAlpha_rad` | $\alpha$ | 攻角 (rad) | 体轴 x 与相对气流方向夹角 — 升力的主要决定因素 |
| `aBeta_rad` | $\beta$ | 侧滑角 (rad) | 体轴 y 与相对气流夹角 — 侧力的主要决定因素 |
| `aAlphaDot_rps` | $\dot{\alpha}$ | 攻角变化率 (rad/s) | 非定常流动延迟效应的输入 |
| `aBetaDot_rps` | $\dot{\beta}$ | 侧滑角变化率 (rad/s) | 非定常侧力/偏航力矩的输入 |
| `aAngularRates_rps[0,1,2]` | $p, q, r$ | 体轴角速率 (roll/pitch/yaw, rad/s) | 阻尼力矩的输入 |
| `mWingArea_sqft` / `mRefArea_sqft` | $S_{ref}$ | 参考面积 (ft²) | 机翼面积或显式指定参考面积 |
| `mWingSpan_ft` | $b$ | 翼展 (ft) | 用于滚转/偏航力矩的无量纲化 |
| `mWingChord_ft` / `mRefLength_ft` | $c_{ref}$ | 参考弦长 (ft) | 用于俯仰力矩的无量纲化 |
| `mCL_AlphaBetaMachTablePtr` | $C_L(\alpha,\beta,M)$ | 升力系数 3D 表 | 核心静态数据 — 飞行器 wind tunnel 试验结果 |
| `mCLq_AlphaMachTablePtr` | $C_{L_q}(\alpha,M)$ | 俯仰阻尼升力导数 | 由于俯仰速率引起的升力变化 |
| `mCL_AlphaDotAlphaMachTablePtr` | $C_{L_{\dot{\alpha}}}(\alpha,M)$ | 攻角延迟升力导数 | 非定常流动：α 变化时气动力不能瞬间响应 |
| `mCd_AlphaBetaMachTablePtr` | $C_d(\alpha,\beta,M)$ | 阻力系数 3D 表 | 含零升阻力（型阻） + 诱导阻力 |
| `mCY_AlphaBetaMachTablePtr` | $C_Y(\alpha,\beta,M)$ | 侧力系数 3D 表 | 主要由侧滑角 β 驱动 |
| `mCm_AlphaBetaMachTablePtr` | $C_m(\alpha,\beta,M)$ | 俯仰力矩系数 3D 表 | 抬头为正 — 纵向静稳定性的核心判定依据 |
| `mCn_AlphaBetaMachTablePtr` | $C_n(\alpha,\beta,M)$ | 偏航力矩系数 3D 表 | 机头右偏为正 — 航向静稳定性的核心判定依据 |
| `mCl_AlphaBetaMachTablePtr` | $C_l(\alpha,\beta,M)$ | 滚转力矩系数 3D 表 | 右翼下沉为正 — 横侧静稳定性的核心判定依据 |
| `aRadiusSizeFactor` | $k_{scale}$ | 几何尺度因子 | 允许缩放气动面而不改变系数表 |

## Edge Cases

1. **跨声速/超声速**：马赫数 0.8–1.2 区域系数跳变剧烈，依赖表格数据密度；插值在稀疏点处可能产生非物理结果
2. **大攻角失速**：$\alpha > 30°$ 时线性稳定性导数失效，需依赖 3D 表覆盖失速后区域
3. **零速度**：$V = 0$ 时简化频率项出现除零——此时可跳过所有非定常项
4. **空模式**：`GetActiveAeroObject()` 返回 null 时不计算气动力（仅重力作用，如弹道导弹在真空中）
5. **Legacy 导数 (deprecated)**：`mUseLegacy = true` 时使用单变量 (α-only) 导数，与多变量导数 (α-β) 互斥 — 这是已弃用的旧模式
6. **参考面 vs 翼面积**：`mUseRefArea = true` 时用 `mRefArea_sqft` 替代 `mWingArea_sqft`/`mWingSpan_ft`/`mWingChord_ft`
7. **亚音速 vs 超声速标准化**：无因次化用不同的参考长度/速度组合

## Portability Assessment

- **Score**: High (核心数学) / Low (数据依赖)
- **Reason**: 稳定性导数模型是航空航天工程的标准方法，数学公式完全可移植。但实际精度取决于气动数据表——这些表格是飞行器特有的机密数据，不能直接搬运。代码与 `UtTable::Table` 高维查表引擎耦合。
- **What can be extracted directly**: 稳定性导数公式、系数叠加逻辑、简化频率计算
- **What should be rewritten**: 
  - 替换 `UtTable::Table` 为自有多维插值引擎
  - 气动数据表需用户提供（wind tunnel 或 CFD 数据）
  - 单位统一为 SI
  - 删除 deprecated legacy 导数支持

## Validation Plan

1. **零攻角零侧滑角**：仅对称阻力非零，升力 = 侧力 = 力矩 = 0（对称飞行器假设）
2. **小扰动线性性**：小 α/β 下 CL ∝ α（线性段），验证斜率匹配表格
3. **表格边界外推**：超表范围的 α/β/M 值应有合理边界处理
4. **与 DATCOM 结果对比**：对简单构型，气动系数应接近 DATCOM 估算值
5. **已知飞行器回放**：用公开气动数据（如 F-16 或 X-31）验证六自由度飞行包线
