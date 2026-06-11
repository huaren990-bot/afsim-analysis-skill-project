# 刚体六自由度积分器 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-rigid-body-integrator-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│                  RigidBodyIntegrator                 │
│  (Heun 预测-校正法 + 四元数姿态积分)                     │
│  继承自 Integrator（抽象基类）                         │
├──────────────────────────────────────────────────────┤
│  + Update(simTime_ns, dt_sec)                       │
│  + SetParentVehicle(mover*)                         │
│  - CalculateFM(state, time, dt, FM_RP, FM_CM)       │
│  - PropagateUsingFM(state, mass, dt, FM_RP, FM_CM)  │
│  - UpdateUsingFM(state, mass, time, dt, FM_RP,FM_CM)│
│  - PropagateRotation(state, α_dot, dt)              │
│  (继承) PropagateTranslation(state, a_body, dt)     │
│  (继承) UpdateFuelBurn(state, time, dt)             │
└──────────┬───────────────────────────────────────────┘
           │ 持有指针
           ▼
┌──────────────────────────────────────────────────────┐
│               RigidBodyMover (父运动器)              │
│  - 提供质量特性、气动模型、推进模型、起落架状态          │
│  - 提供 KinematicState 运动学状态读写                 │
└──────────┬───────────────────────────────────────────┘
           │ 使用
           ▼
┌──────────────────────────────────────────────────────┐
│              ForceAndMomentsObject                   │
│  (力/力矩容器 — 参考点管理 + 叠加 + 限幅 + 平均)       │
├──────────────────────────────────────────────────────┤
│  mForceVec_lbs:  体轴合力 (lbf)                      │
│  mMomentVec_ftlbs: 体轴合力矩 (ft-lbf)               │
│  mRefPoint_ft:   内部参考点坐标 (ft)                  │
│  + operator+=    → 自动参考点转换叠加                 │
│  + CalcAverageWith → 两帧F&M算术平均                  │
│  + LimitMaxForceMagnitude_lbs  → 力矢量限幅          │
│  + LimitMomentMagnitude_ftlbs → 力矩矢量限幅          │
└──────────────────────────────────────────────────────┘
```

**架构说明：**
- `RigidBodyIntegrator` 继承自 `Integrator` 抽象基类，实现刚体六自由度的 Heun 预测-校正积分。
- 它通过 `RigidBodyMover*` 指针访问飞行器各子系统（质量特性、气动力/力矩、推进力/力矩、起落架力/力矩）。
- `ForceAndMomentsObject` 是力/力矩的容器类，提供参考点管理、自动参考点转换（operator+=）、矢量限幅和算术平均功能。
- 基类 `Integrator::PropagateTranslation` 处理平动推进（体轴加速度→惯性系加速度→位置/速度更新，可选旋转地球效应）。
- 基类 `Integrator::PropagateRotation` 处理转动推进（角速率更新 + 四元数姿态积分 + 冻结标志处理）。

## 2. 核心接口定义

### 2.1 Integrator（抽象基类 — 积分器基类接口）

```cpp
// 积分器抽象基类：定义所有积分器的公共接口。
// 所有方法均可被子类覆写，基类提供平动/转动/燃油消耗的默认实现。
class Integrator {
public:
    // ---------- 公共接口 ----------

    // 主积分入口：每帧由运动器调用，推进运动学状态一个时间步。
    // aSimTime_nanosec: 当前帧结束时刻的仿真时间（纳秒 ns）
    // aDeltaT_sec:     本帧的时间步长（秒 s）
    virtual void Update(int64_t aSimTime_nanosec, double aDeltaT_sec) const = 0;

protected:
    // ---------- 受保护的推进方法（子类可覆写） ----------

    // 获取父运动器指针（纯虚函数，子类必须实现）
    virtual Mover* GetParentVehicle() const = 0;

    // 更新燃油消耗：根据当前推力和时间步长，扣除已消耗的燃油质量。
    // 基类实现委托给 Mover::UpdateFuelBurn()。
    virtual void UpdateFuelBurn(
        KinematicState& aState,       // 运动学状态（将被修改：更新燃油质量）
        int64_t         aSimTime_nanosec, // 当前仿真时间 (ns)
        double          aDeltaT_sec       // 时间步长 (s)
    ) const;

    // 平动推进：将体轴加速度转换为惯性系加速度，更新位置和速度。
    // 体轴加速度 aBodyAccel = F_total_body / mass * g0（g0=9.80665 用于单位换算）。
    // 使用匀加速运动方程：r_new = r + v*dt + 0.5*a*dt², v_new = v + a*dt。
    // 可选叠加旋转地球的离心加速度和科里奥利加速度。
    virtual void PropagateTranslation(
        KinematicState& aState,          // 运动学状态（将被修改：位置、速度）
        const UtVec3dX& aBodyAccel_mps2, // 体轴加速度 (m/s²)
        double          aDeltaT_sec      // 时间步长 (s)
    ) const;

    // 转动推进：用角加速度更新角速率，再用四元数积分更新姿态。
    // omega_new = omega + alpha_dot * dt
    // 从当前DCM提取四元数 q_att → 计算速率四元数 q_rate = 0.5*q⊗[0,ω] →
    //   q_new = q + q_rate*dt → normalize(q_new) → newDCM = q_new.Get()
    // 冻结标志（freezeRoll/Pitch/Yaw）在推进前清零对应轴的角加速度和角速率。
    virtual void PropagateRotation(
        KinematicState& aState,             // 运动学状态（将被修改：角速率、姿态DCM）
        UtVec3dX        aRotationalAccel_rps2, // 体轴角加速度 [p_dot, q_dot, r_dot] (rad/s²)
        double          aDeltaT_sec             // 时间步长 (s)
    ) const;
};
```

### 2.2 RigidBodyIntegrator（刚体 Heun 积分器）

```cpp
// 刚体六自由度积分器：使用 Heun 预测-校正法（二阶精度）积分飞行器运动状态。
// 每帧执行：T0时刻力/力矩 → 预测推进 → T1时刻力/力矩 → 平均F&M → 校正推进。
// 继承自 Integrator，覆写 PropagateRotation 以添加简单偏航阻尼器支持。
class RigidBodyIntegrator : public Integrator {
public:
    // 构造函数：绑定父运动器（不可为空）
    explicit RigidBodyIntegrator(RigidBodyMover& mover);

    // 克隆：深拷贝一个新的积分器实例（拷贝 mVehicle 指针）
    RigidBodyIntegrator* Clone() const;

    // 设置/更换父运动器指针。
    // 通常在积分器构造后一次性调用，也可在运行时切换运动器。
    void SetParentVehicle(RigidBodyMover* aVehicle);

    // ---------- 主积分入口（覆写基类纯虚函数） ----------

    // Heun 预测-校正积分器的完整流程：
    //   1) 计算当前质量特性（含燃油消耗后的质心变化）
    //   2) 保存初始运动学状态快照 initialState
    //   3) T0 时刻力/力矩计算：CalculateFM(tempState, t_last, dt, FM_RP_T0, FM_CM_T0)
    //   4) 预测推进：PropagateUsingFM(tempState, ..., FM_RP_T0, FM_CM_T0)
    //   5) T1 时刻力/力矩计算：CalculateFM(tempState, t_current, dt, FM_RP_T1, FM_CM_T1)
    //   6) 再次推进：PropagateUsingFM(tempState, ..., FM_RP_T1, FM_CM_T1)
    //   7) 平均力/力矩：FM_avg = (FM_T0 + FM_T1) / 2
    //   8) 起落架摩擦保持静止检查 → 若静止则跳过后续更新
    //   9) 校正步：UpdateUsingFM(kinematicState, ..., FM_RP_avg, FM_CM_avg)
    //  10) 测试模式下移除攻角（可选）
    //  11) 更新气动状态导数（alpha_dot, beta_dot）
    //  12) 计算辅助输出参数（LLA, Mach, 动压, 航向等）
    void Update(int64_t aSimTime_nanosec,   // 当前仿真时间 (ns)
                double  aDeltaT_sec)          // 时间步长 (s)
                const override;

protected:
    // ---------- 受保护的方法（Heun 法各步骤） ----------

    // 获取父运动器（覆写基类纯虚函数）
    Mover* GetParentVehicle() const override;

    // 力/力矩汇总计算：依次计算气动力/力矩、推进力/力矩、起落架力/力矩、重力。
    // 气动+推进+起落架力叠加到 FM_at_RP（参考点处），重力叠加到 FM_at_CM（质心处）。
    // FM_at_CM 的参考点通过 operator+= 自动转换到质心，实现力臂附加力矩。
    void CalculateFM(
        KinematicState&        aState,            // 当前运动学状态（读取 α/β/Mach/位置）
        int64_t                aSimTime_nanosec,   // 评估时间 (ns)
        double                 aDeltaT_sec,         // 评估步长 (s)
        ForceAndMomentsObject& aForcesMomentsAtRP, // [输出] 参考点处合力/合力矩
        ForceAndMomentsObject& aForcesMomentsAtCM  // [输出] 质心处合力/重力
    ) const;

    // 用 F&M 推进状态（中间步）：执行力/力矩限幅 → 计算加速度 → 平动推进 → 转动推进。
    // 此为"预测推进"或"中间推进"，仅修改 tempState，不影响最终 kinematicState。
    void PropagateUsingFM(
        KinematicState&       aState,              // 运动学状态（将被推进）
        const MassProperties& aMassProperties,      // 当前质量特性（质量/质心/转动惯量）
        double                aDeltaT_sec,           // 时间步长 (s)
        ForceAndMomentsObject aForcesMomentsAtRP,   // 参考点处力/力矩
        ForceAndMomentsObject aForcesMomentsAtCM    // 质心处力/力矩
    ) const;

    // 完整更新状态（校正步）：先更新燃油消耗，再用平均 F&M 推进到最终状态。
    void UpdateUsingFM(
        KinematicState&              aState,           // 运动学状态（将被最终更新）
        const MassProperties&        aMassProperties,  // 质量特性
        int64_t                      aSimTime_nanosec, // 当前仿真时间 (ns)
        double                       aDeltaT_sec,       // 时间步长 (s)
        const ForceAndMomentsObject& aForcesMomentsAtRP, // 参考点平均力/力矩
        const ForceAndMomentsObject& aForcesMomentsAtCM  // 质心平均力/力矩
    ) const;

    // 转动推进（覆写基类）：在基类转动推进前添加简单偏航阻尼器逻辑。
    // 简单偏航阻尼器：离地时（无轮载）将偏航角速率强制设为 beta/dt，
    // 以消除侧滑角。仅在 dt > epsilon 时计算，防止除零。
    void PropagateRotation(
        KinematicState& aState,              // 运动学状态（将被修改）
        UtVec3dX        aRotationalAccel_rps2, // 体轴角加速度 [p_dot, q_dot, r_dot] (rad/s²)
        double          aDeltaT_sec              // 时间步长 (s)
    ) const override;

private:
    RigidBodyMover* mVehicle = nullptr;  // 父运动器指针（不可为空时才能积分）
};
```

### 2.3 ForceAndMomentsObject（力/力矩容器）

```cpp
// 力/力矩容器：维护在指定参考点处的体轴合力和合力矩。
// 核心功能：参考点管理、力/力矩叠加（含自动参考点转换）、矢量限幅、算术平均。
class ForceAndMomentsObject {
public:
    // 构造函数：力/力矩清零，参考点设为零
    ForceAndMomentsObject();

    // 拷贝构造：深拷贝力矢量、力矩矢量和参考点
    ForceAndMomentsObject(const ForceAndMomentsObject& other);

    // 清空所有力/力矩（置为零矢量）
    void ClearForcesAndMoments();

    // 设置内部参考点坐标
    // aRefPoint_ft: 参考点位置，相对于飞行器参考点(RP) (ft)
    void MoveRefPoint_ft(const UtVec3dX& aRefPoint_ft);

    // 在当前参考点处追加力
    // aForce_lbs: 体轴系力矢量 (lbf)
    void AddForceAtReferencePoint(const UtVec3dX& aForce_lbs);

    // 在当前参考点处追加力和力矩
    // aForce_lbs:  体轴系力矢量 (lbf)
    // aMoment_ftlbs: 体轴系力矩矢量 (ft-lbf)
    void AddForceAndMomentAtReferencePoint(
        const UtVec3dX& aForce_lbs,
        const UtVec3dX& aMoment_ftlbs
    );

    // 获取当前参考点处的力/力矩
    void GetForceAndMomentAtCurrentRefPoint(
        UtVec3dX& aForce_lbs,     // [输出] 体轴合力 (lbf)
        UtVec3dX& aMoment_ftlbs   // [输出] 体轴合力矩 (ft-lbf)
    ) const;

    // 获取当前参考点处的力矩（不输出力）
    UtVec3dX GetMomentAtRefPoint_ftlbs() const;

    // ---------- 叠加运算符（自动参考点转换） ----------

    // 将另一个 F&M 对象叠加到当前对象。
    // 若两者参考点不同，力矩通过力臂自动转换：M_附加 = (r_other - r_this) × F_other。
    // 这确保最终合力矩是作用于当前参考点的等效力矩。
    ForceAndMomentsObject& operator+=(const ForceAndMomentsObject& aOther);

    // ---------- 力/力矩限幅 ----------

    // 力矢量限幅：若合力幅值超过 aMaxForceMagnitude_lbs，则等比缩放至上限。
    // 防止碰撞/爆炸瞬间的天文数字级力尖峰导致状态 NaN。
    void LimitMaxForceMagnitude_lbs(double aMaxForceMagnitude_lbs);

    // 力矩矢量限幅：若合力矩幅值超过 aMaxMomentMagnitude_ftlbs，则等比缩放至上限。
    void LimitMomentMagnitude_ftlbs(double aMaxMomentMagnitude_ftlbs);

    // ---------- Heun 平均 ----------

    // 取当前 F&M 和 aOther F&M 的算术平均，结果存入当前对象。
    // 用于 Heun 法：FM_avg = (FM_T0 + FM_T1) / 2。
    // 注意：只平均力矢量和力矩矢量，不修改当前对象的参考点。
    void CalcAverageWith(const ForceAndMomentsObject& aOther);

private:
    UtVec3dX mForceVec_lbs;      // 体轴合力矢量，维护于内部参考点处 (lbf)
    UtVec3dX mMomentVec_ftlbs;   // 体轴合力矩矢量，维护于内部参考点处 (ft-lbf)
    UtVec3dX mRefPoint_ft;       // 内部参考点坐标 (ft)
};
```

### 2.4 MassProperties（质量特性容器 — 概念接口）

```cpp
// 质量特性容器：飞行器当前的质量属性，含燃油消耗后的实时值。
// 注意：此类属于 AFSIM 框架，此处给出概念接口用于移植。
struct MassProperties {
    // 获取当前质量 (lbm)
    double GetMass_lbs() const;

    // 获取质心相对参考点的偏移 (ft)
    // 用于将参考点处的力/力矩转换到质心
    UtVec3dX GetCmPosRelToRef_ft() const;

    // 绕体轴三轴的转动惯量 (slug-ft²)
    double GetIxx_slugft2() const;  // 滚转轴转动惯量
    double GetIyy_slugft2() const;  // 俯仰轴转动惯量
    double GetIzz_slugft2() const;  // 偏航轴转动惯量
};
```

### 2.5 KinematicState（运动学状态 — 概念接口）

```cpp
// 运动学状态：存储飞行器仿真的完整瞬态运动学状态。
// 注意：此类属于 AFSIM 框架，此处给出概念接口用于移植。
class KinematicState {
public:
    // ---------- 位置/速度 ----------
    // 获取/设置 ECEF 位置 (m)
    void SetPositionEcef_m(const UtVec3dX& pos);
    UtVec3dX GetPositionEcef_m() const;

    // 获取/设置惯性系速度 (m/s)
    void SetVelocityInertial_mps(const UtVec3dX& vel);
    UtVec3dX GetVelocityInertial_mps() const;

    // ---------- 姿态 ----------
    // 获取/设置方向余弦矩阵（体轴 → 世界坐标系）
    void SetDCM(const UtDCM& dcm);
    UtDCM GetDCM() const;

    // ---------- 角速率 ----------
    // 获取/设置体轴角速率 (rad/s)，[p, q, r] = [滚转, 俯仰, 偏航]
    void SetOmegaBody(const UtVec3dX& omega);
    UtVec3dX GetOmegaBody() const;

    // 获取/设置体轴角加速度 (rad/s²)
    void SetOmegaBodyDot(const UtVec3dX& omega_dot);

    // ---------- 气动状态 ----------
    double GetAlpha_rad() const;    // 攻角 (rad)
    double GetBeta_rad() const;     // 侧滑角 (rad)
    double GetMach() const;         // 马赫数（无量纲）
    double GetDynamicPressure_lbsqft() const;  // 动压 (lb/ft²)

    // 更新气动状态（重新计算 alpha, beta, Mach, 动压）
    void UpdateAeroState(int64_t aSimTime_nanosec);

    // 更新气动状态变化率（alpha_dot, beta_dot）
    void CalculateRates(int64_t aSimTime_nanosec);

    // 计算辅助输出参数（LLA, 航向, 飞行路径角等）
    void CalculateSecondaryParameters();

    // ---------- 坐标系转换 ----------
    // 体轴矢量 → 世界坐标系矢量
    UtVec3dX CalcWCSVecFromBodyVec(const UtVec3dX& bodyVec) const;
    // 世界坐标系矢量 → 体轴矢量
    UtVec3dX CalcBodyVecFromWCSVec(const UtVec3dX& wcsVec) const;

    // ---------- 重力 ----------
    // 获取归一化重力加速度方向（惯性系单位矢量）
    UtVec3dX NormalizedGravitationalAccelVec() const;

    // ---------- 诊断/监控 ----------
    // 设置体轴过载（以 g 为单位），不含重力分量
    void SetBodyAccel(double nx_g, double ny_g, double nz_g);

    // 设置升力/阻力/侧力/推力/重量监控值 (lbf)
    void SetLiftDragSideForceThrustWeight(
        double lift_lbs, double drag_lbs, double sideForce_lbs,
        double thrust_lbs, double wgt_lbs
    );

    // 设置质心处的总力矩 (ft-lbf)
    void SetMomentAtCG(const UtVec3dX& moment_ftlbs);

    // ---------- 起落架 ----------
    // 获取/设置轮载状态（是否在地面）
    bool GetWeightOnWheels() const;

    // ---------- 测试辅助 ----------
    // 测试模式下将攻角强制归零
    void RemoveAlphaForTesting();
};
```

## 3. 典型调用模式

```cpp
// ========== 1. 初始化积分器 ==========
// 创建刚体运动器，通过它创建并绑定积分器
RigidBodyMover mover(vehicleConfig);
RigidBodyIntegrator integrator(mover);
// 积分器的 mVehicle 指向 mover，积分过程中通过 mover 访问所有子系统

// ========== 2. 仿真主循环（每帧一次） ==========
double simTime_ns = 0;          // 仿真时间戳（纳秒）
double dt_sec     = 1.0 / 60.0; // 60Hz 物理步长（秒）

for (int frame = 0; frame < 36000; frame++) {  // 仿真 10 分钟
    // 更新运动器内部状态（如航路导航、自动驾驶命令）
    mover.Update(simTime_ns, dt_sec);

    // 积分器执行 Heun 预测-校正法推进运动学状态：
    // 内部流程：
    //   1) mover.CalculateCurrentMassProperties()   → 更新质心位置
    //   2) 保存 initialState = kinematicState 快照
    //   3) CalculateFM(tempState, lastTime, dt, FM_RP_T0, FM_CM_T0)
    //      → 气动+推进+起落架+重力
    //   4) PropagateUsingFM(tempState, ..., FM_RP_T0, FM_CM_T0)
    //      → 力限幅 → 加速度 → 平动推进 → 转动推进
    //   5) CalculateFM(tempState, curTime, dt, FM_RP_T1, FM_CM_T1)
    //      → 在预测态重新计算力/力矩
    //   6) PropagateUsingFM(tempState, ..., FM_RP_T1, FM_CM_T1)
    //      → 再次推进
    //   7) FM_avg = (FM_T0 + FM_T1) / 2  → Heun 算术平均
    //   8) 起落架摩擦检查 → 静止则跳过后续
    //   9) UpdateUsingFM(kinematicState, ..., FM_avg)
    //      → 燃油消耗 + 用平均F&M最终推进
    //  10) RemoveAlphaForTesting()  → 测试模式攻角归零
    //  11) UpdateAeroState()        → 更新 alpha_dot, beta_dot
    //  12) CalculateSecondaryParameters() → 更新导航输出参数
    integrator.Update(
        static_cast<int64_t>(simTime_ns),  // 当前仿真时间 (ns)
        dt_sec                              // 时间步长 (s)
    );

    simTime_ns += static_cast<int64_t>(dt_sec * 1e9);

    // 从运动器获取更新后的状态用于日志/可视化
    auto& state = mover.GetKinematicState();
    logPosition(simTime_ns, state.GetPositionEcef_m());     // ECEF位置 (m)
    logAttitude(simTime_ns, state.GetDCM());                // 姿态 DCM
    logAeroAngles(simTime_ns, state.GetAlpha_rad(), state.GetBeta_rad()); // 气动角
}

// ========== 3. 内部：力/力矩计算的典型调用链 ==========
// 在 CalculateFM() 内部：
void RigidBodyIntegrator::CalculateFM(
    KinematicState& state, int64_t simTime, double dt,
    ForceAndMomentsObject& FM_RP, ForceAndMomentsObject& FM_CM) const
{
    // --- 准备：获取质量特性，设置 CM 参考点 ---
    auto& massProps = mVehicle->GetMassProperties();
    FM_CM.MoveRefPoint_ft(massProps.GetCmPosRelToRef_ft()); // CM F&M参考点=质心

    // --- 1. 气动力/力矩 ---
    state.UpdateAeroState(simTime);  // 计算当前 alpha, beta, Mach, 动压
    UtVec3dX aeroLift, aeroDrag, aeroSide, aeroMoment, refPt;
    mVehicle->CalculateAeroBodyForceAndMoments(
        aeroLift, aeroDrag, aeroSide, aeroMoment, refPt);
    aeroTotal = aeroLift + aeroDrag + aeroSide;  // 体轴总气动力 (lbf)
    ForceAndMomentsObject aeroFM;
    aeroFM.MoveRefPoint_ft(refPt + aeroCenter);  // 气动参考点
    aeroFM.AddForceAndMomentAtReferencePoint(aeroTotal, aeroMoment);
    FM_RP += aeroFM;  // 叠加到 RP，自动参考点转换

    // --- 2. 推进力/力矩 ---
    UtVec3dX propInertialForce, propMoment;
    mVehicle->CalculatePropulsionFM(simTime, dt, state,
                                     propInertialForce, propMoment);
    propBodyForce = state.CalcBodyVecFromWCSVec(propInertialForce); // 惯性系→体轴
    FM_RP.AddForceAndMomentAtReferencePoint(propBodyForce, propMoment);

    // --- 3. 起落架力/力矩 ---
    UtVec3dX gearInertialForce, gearMoment;
    mVehicle->CalculateLandingGearFM(simTime, nonGearForce,
                                      gearInertialForce, gearMoment);
    gearBodyForce = state.CalcBodyVecFromWCSVec(gearInertialForce);
    FM_RP.AddForceAndMomentAtReferencePoint(gearBodyForce, gearMoment);

    // --- 4. 重力（仅作用于质心） ---
    gravityDir = state.NormalizedGravitationalAccelVec();  // 重力单位方向
    gravityInertialForce = gravityDir * currentMass_lbm;    // 重力 = 方向 × 质量 (lbf)
    gravityBodyForce = state.CalcBodyVecFromWCSVec(gravityInertialForce);
    FM_CM.AddForceAtReferencePoint(gravityBodyForce);       // 加到 CM F&M
}

// ========== 4. 内部：PropagateUsingFM 的力/力矩→加速度转换 ==========
void RigidBodyIntegrator::PropagateUsingFM(...) const
{
    double mass_lbm = aMassProperties.GetMass_lbs();

    // 力矢量限幅（防止加速度尖峰）
    double maxForce_lbs = mass_lbm * 1000.0;  // 1000g 上限
    FM_RP.LimitMaxForceMagnitude_lbs(maxForce_lbs);
    FM_CM.LimitMaxForceMagnitude_lbs(maxForce_lbs);

    // 设置体轴过载 (不含重力)
    FM_RP.GetForceAndMomentAtCurrentRefPoint(nonGF, nonGM);
    aState.SetBodyAccel(nonGF.X() / mass_lbm,   // Nx (g)
                        nonGF.Y() / mass_lbm,   // Ny (g)
                        nonGF.Z() / mass_lbm);  // Nz (g)

    // 合并 RP 和 CM 的 F&M 到 CM（operator+= 自动参考点转换）
    FM_CM += FM_RP;

    // 力矩限幅（防止角加速度尖峰）
    double I_max = max(Ixx, Iyy, Izz);                         // slug-ft²
    double maxMoment = I_max * (100.0 * 360.0 * PI / 180.0);   // 100 rev/s²
    FM_CM.LimitMomentMagnitude_ftlbs(maxMoment);

    // 提取总力/力矩（含重力）
    FM_CM.GetForceAndMomentAtCurrentRefPoint(totalBodyForce, totalMoment);

    // 体轴加速度 → 平动推进
    bodyAccel = totalBodyForce * 9.80665 / mass_lbm;  // F/m * g0 (m/s²)
    PropagateTranslation(aState, bodyAccel, dt);

    // 角加速度 → 转动推进
    omegaDot[0] = totalMoment.X() / Ixx;  // p_dot = M_x / Ixx (rad/s²)
    omegaDot[1] = totalMoment.Y() / Iyy;  // q_dot = M_y / Iyy (rad/s²)
    omegaDot[2] = totalMoment.Z() / Izz;  // r_dot = M_z / Izz (rad/s²)
    PropagateRotation(aState, omegaDot, dt);
}
```

## 4. 坐标系/单位约定

### 坐标系

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **Body（体轴系）** | X=前, Y=右, Z=下 | 气动力/力矩、推力、过载表达 |
| **WCS / ECEF（地心地固）** | 地心地固直角坐标 | 位置/速度存储，平动推进的中间坐标系 |
| **NED（北东地）** | X=北, Y=东, Z=下 | 导航输出（经纬度/高度/航向） |
| **Spherical Earth（球面地球）** | 球面地心 | 简化地球模型（可选开启） |

### 单位约定（AFSIM 原始代码混合单位制）

由于 AFSIM 原始代码同时使用 Imperial（英制）和 SI（公制）单位，理解单位换算关系至关重要。

| 物理量 | AFSIM 原始单位 | SI 等效 | 换算关系 |
|--------|---------------|---------|----------|
| 位置 | ft | m | 1 ft = 0.3048 m |
| 速度 | ft/s | m/s | 1 ft/s = 0.3048 m/s |
| 加速度 | m/s² | m/s² | 统一（基类输出SI） |
| 角度 | rad | rad | 统一 |
| 角速率 | rad/s | rad/s | 统一 |
| 角加速度 | rad/s² | rad/s² | 统一 |
| 质量 | lbm (slug) | kg | 1 slug = 32.174 lbm ≈ 14.594 kg |
| 力 | lbf | N | 1 lbf / 1 lbm = 9.80665 m/s² = 32.174 ft/s² |
| 力矩 | ft-lbf | N·m | 1 ft-lbf ≈ 1.3558 N·m |
| 转动惯量 | slug-ft² | kg·m² | 1 slug-ft² ≈ 1.3558 kg·m² |
| 动压 | lb/ft² (psf) | Pa | 1 psf ≈ 47.88 Pa |

**关键换算公式**（贯穿代码始终，移植时务必保留）：
- 体轴力 → 惯性加速度：`a_inertial_mps2 = F_body_lbf * 9.80665 / mass_lbm`
- 其中 `9.80665 m/s²` = `32.174 ft/s²`，既是标准重力加速度，也是 lbf→lbm 换算因子（1 lbf = 1 lbm * g₀）

### 为统一移植建议使用的 SI 单位制

所有新实现建议统一使用 **SI 单位制**：
- 位置: m
- 速度: m/s
- 加速度: m/s²
- 角度: rad
- 角速率: rad/s
- 角加速度: rad/s²
- 质量: kg
- 力: N
- 力矩: N·m
- 转动惯量: kg·m²
- 动压: Pa
- 密度: kg/m³

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|----------|----------|
| `wsf::six_dof::Integrator` | 抽象基类 | 自定义 `RigidBodyIntegratorBase`（含 Update / PropagateTranslation / PropagateRotation 纯虚接口） |
| `wsf::six_dof::KinematicState` | 运动学状态容器 | 自定义 `RigidBodyState` 结构体（位置/速度/DCM/角速率/四元数/气动状态/冻结标志） |
| `wsf::six_dof::MassProperties` | 质量特性容器 | 自定义 `MassProperties` 结构体（质量/质心偏移/转动惯量Ixx,Iyy,Izz） |
| `wsf::six_dof::ForceAndMomentsObject` | F&M 容器 | 自定义 `ForceMoments` 类（参考点管理 + 叠加含自动转换 + 矢量限幅 + 算术平均） |
| `wsf::six_dof::Mover` / `RigidBodyMover` | 运动器抽象基类 | 自定义 `Vehicle` 接口（质量特性、气动/推进/起落架 F&M 计算、起落架状态查询） |
| `wsf::six_dof::RigidBodyLandingGear` | 起落架组件 | 自定义 `LandingGear` 类（摩擦保持静止查询） |
| `wsf::six_dof::RigidBodyAeroCoreObject` | 气动核心对象 | 自定义 `AeroModel` 类（气动中心偏移） |
| `wsf::six_dof::FreezeFlags` | 冻结标志 | 自定义 `FreezeFlags` 位掩码结构体 |
| `UtVec3dX` | 三维矢量 | `Eigen::Vector3d` 或自定义 Vec3 |
| `UtQuaternion` | 四元数 | `Eigen::Quaterniond` 或自定义 Quaternion |
| `UtDCM` | 方向余弦矩阵 | `Eigen::Matrix3d` 或自定义 3x3 矩阵 |
| `UtMath::cDEG_PER_RAD` | 数学常数 | `M_PI / 180.0` |
| `ut::log::error()` / `UtLog` | 日志 | `std::cerr` 或 spdlog |
| `utils::TimeToTime()` / `utils::cEPSILON_SIMTIME_SEC` | 时间工具 | `static_cast<double>(ns)/1e9`、自定义 epsilon |

**核心需要重新实现的类**：
1. `ForceMoments`：实现参考点管理、operator+=（含力臂转换）、矢量限幅、算术平均
2. `RigidBodyState`：位置/速度/DCM/角速率/气动角的统一存储
3. `Quaternion`：实现 SetRate / Update / Normalize / Get (to DCM) 四个关键接口
