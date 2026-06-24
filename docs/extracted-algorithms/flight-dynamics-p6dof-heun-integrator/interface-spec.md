# P6DOF Heun 修正欧拉积分器 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-p6dof-heun-integrator-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│                 P6DofIntegrator                      │
│  (Heun 预测-校正法 + 四元数姿态积分)                     │
│  所有方法均为 static — 无类实例状态                     │
├──────────────────────────────────────────────────────┤
│  + Update(vehicle, simTime_ns, dt_sec)  [static]    │
│  - CalculateFM(vehicle, state, time, dt, FM_RP,FM_CM)│
│  - PropagateUsingFM(vehicle, state, mass, dt, ...)   │
│  - UpdateUsingFM(vehicle, state, mass, time, dt, ...)│
│  - PropagateTranslation(vehicle, state, a, dt)       │
│    ├ PropagateTranslationSphericalEarth(...)          │
│    └ PropagateTranslationWGSEarth(...)                │
│  - PropagateRotation(vehicle, state, α_dot, dt)      │
│  - UpdateFuelBurn(vehicle, state, time, dt)          │
└──────────┬───────────────────────────────────────────┘
           │ operates on
           ▼
┌──────────────────────────────────────────────────────┐
│              P6DofVehicle (飞行器模型)                │
│  - 提供质量特性、气动模型、推进模型、起落架状态          │
│  - 提供 P6DofKinematicState 运动学状态读写            │
│  - 提供地球模型选择（球面 / WGS84）                    │
└──────────┬───────────────────────────────────────────┘
           │ uses
           ▼
┌──────────────────────────────────────────────────────┐
│         P6DofForceAndMomentsObject                   │
│  (力/力矩容器 — 参考点管理 + 叠加 + 限幅 + 平均)       │
├──────────────────────────────────────────────────────┤
│  mForceVec_lbs:   体轴合力 (lbf)                      │
│  mMomentVec_ftlbs: 体轴合力矩 (ft-lbf)               │
│  mRefPoint_ft:     内部参考点坐标 (ft)                 │
│  + operator+=    → 自动参考点转换叠加                 │
│  + CalcAverageWith → 两帧F&M算术平均                  │
│  + LimitMaxForceMagnitude_lbs  → 力矢量限幅          │
│  + LimitMomentMagnitude_ftlbs → 力矩矢量限幅          │
└──────────────────────────────────────────────────────┘
```

**架构说明：**
- `P6DofIntegrator` 所有方法都是 **static**（静态函数），自身不维护跨帧持久化状态。
- 帧间状态的持久化完全由 `P6DofKinematicState`（飞行器运动学状态容器）承担。
- 积分器每次调用都是无状态的纯函数变换。
- 平动推进支持两种地球模型：球面地球（恒定半径 R=6366707m）和 WGS84 椭球地球。
- 与 wsf_six_dof 版 `RigidBodyIntegrator` 的核心 Heun 框架一致，但实现更底层（直接操作 P6DofKinematicState）。

## 2. 核心接口定义

### 2.1 P6DofIntegrator（P6DOF Heun 积分器主类）

```cpp
// P6DOF Heun 修正欧拉积分器：对飞行器在三维空间中的平移和旋转运动进行时间推进。
// 采用 Heun 修正欧拉法（二阶预测-校正），逐帧计算气动/推进/起落架/重力四项力与力矩的综合作用。
// 所有方法均为 static，无类实例状态。帧间状态由 P6DofKinematicState 跨帧保持。
class P6DofIntegrator {
public:
    // 克隆：深拷贝构造新积分器（由于所有方法为static，拷贝仅保留类型信息）
    P6DofIntegrator* Clone() const;

    // ---------- 主积分入口 [static] ----------

    // Heun 预测-校正积分器的完整流程（每帧调用一次）：
    //   1) vehicle.CalculateCurrentMassProperties() → 更新质量/质心/转动惯量
    //   2) 深拷贝当前 kinematicState → tempState（保存原始状态供校正步使用）
    //   3) 在 t=t_last 用 EPSILON (1e-12 s) 计算初始力/力矩 F0：
    //      CalculateFM(vehicle, tempState, t_last, EPSILON, F0_RP, F0_CM)
    //      用 EPSILON 代替 0 避免气动状态求取时 di=0 导致除零崩溃
    //   4) 预测推进：PropagateUsingFM(vehicle, tempState, ..., F0_RP, F0_CM)
    //   5) 在预测态重新计算力/力矩 F1：
    //      CalculateFM(vehicle, tempState, simTime, EPSILON, F1_RP, F1_CM)
    //   6) Heun 平均：F_avg = (F0 + F1) / 2   → 二阶精度
    //   7) 从 tempState 拷贝诊断值到 kinematicState（升力/阻力/推力/重量/力矩）
    //   8) 校正步：UpdateUsingFM(vehicle, kinematicState, ..., F_avg_RP, F_avg_CM)
    //      → 燃油消耗 + 用平均F&M对原始状态推进
    //   9) 后处理：
    //      - RemoveAlphaForTesting()    → 测试模式攻角归零
    //      - CalculateRates()           → 更新 alpha_dot, beta_dot
    //      - CalculateSecondaryParameters() → 更新 LLA/Mach/动压/航向
    static void Update(
        P6DofVehicle* aObject,           // 飞行器对象指针（提供全部子系统接口）
        int64_t       aSimTime_nanosec,   // 当前帧结束时刻仿真时间 (ns)
        double        aDeltaT_sec         // 帧时间步长 (s)
    );

protected:
    // ---------- 受保护的静态方法 ----------

    // 力/力矩汇总计算：依次计算气动力/力矩、推进力/力矩、起落架力/力矩、重力。
    // 气动+推进+起落架力叠加到 aForcesMomentsAtRP（参考点处），重力叠加到 aForcesMomentsAtCM（质心处）。
    // P6DofForceAndMomentsObject 的 operator+= 自动执行参考点转换（力臂产生附加力矩）。
    static void CalculateFM(
        P6DofVehicle*               aObject,            // 飞行器对象
        P6DofKinematicState&        aState,             // 运动学状态（读取 α/β/Mach/位置）
        int64_t                     aSimTime_nanosec,    // 评估时间 (ns)
        double                      aDeltaT_sec,          // 评估步长 (s)
        P6DofForceAndMomentsObject& aForcesMomentsAtRP,  // [输出] 参考点处合力/合力矩
        P6DofForceAndMomentsObject& aForcesMomentsAtCM   // [输出] 质心处合力（重力）
    );

    // 燃油消耗更新：根据当前推力和时间步长，扣除已消耗的燃油质量。
    static void UpdateFuelBurn(
        P6DofVehicle*        aObject,           // 飞行器对象
        P6DofKinematicState& aState,            // 运动学状态（将被修改：燃油质量）
        int64_t              aSimTime_nanosec,   // 当前仿真时间 (ns)
        double               aDeltaT_sec         // 时间步长 (s)
    );

    // 平动推进分派器：根据飞行器的地球模型配置分发到球面或WGS84推进函数。
    static void PropagateTranslation(
        P6DofVehicle*        aObject,            // 飞行器对象（查询地球模型）
        P6DofKinematicState& aState,             // 运动学状态（将被修改：位置、速度）
        const UtVec3dX&      aInertialAccel_mps2, // 惯性系加速度 (m/s²)
        double               aDeltaT_sec           // 时间步长 (s)
    );

    // 球面地球平动推进：使用恒定半径球面坐标系推进位置和速度。
    // 适用于简单弹道导弹/火箭场景。
    static void PropagateTranslationSphericalEarth(
        P6DofVehicle*        aObject,
        P6DofKinematicState& aState,
        UtVec3dX             aInertialAccel_mps2,  // 惯性系加速度 (m/s²)
        double               aDeltaT_sec            // 时间步长 (s)
    );

    // WGS84 椭球地球平动推进：使用标准 WGS84 ECEF 坐标系推进位置和速度。
    // 适用于高保真场景。
    static void PropagateTranslationWGSEarth(
        P6DofVehicle*        aObject,
        P6DofKinematicState& aState,
        UtVec3dX             aInertialAccel_mps2,  // 惯性系加速度 (m/s²)
        double               aDeltaT_sec            // 时间步长 (s)
    );

    // 转动推进：用角加速度更新角速率，再用四元数积分更新姿态。
    // 内部流程：
    //   1) 冻结标志处理：freezeRoll/Pitch/Yaw → 对应轴角加速度和角速率清零
    //   2) 角增量计算：delAng = omega*dt + 0.5*alpha*dt²
    //   3) 角速率更新：omega_new = omega + alpha*dt
    //   4) 起落架静摩擦处理：FrictionHoldingStill → 滚转/偏航速率清零
    //   5) 简单偏航阻尼器：离地时 yawRate = beta / dt
    //   6) 四元数姿态积分：
    //      q_att = Quaternion(dcm)
    //      q_rate.SetRate(q_att, omega)
    //      q_new = q_att + q_rate * dt
    //      q_new.Normalize()          → 关键归一化，防止范数漂移
    //      newDCM = q_new.ToDCM()
    static void PropagateRotation(
        P6DofVehicle*        aObject,             // 飞行器对象（查询冻结标志/偏航阻尼器）
        P6DofKinematicState& aState,              // 运动学状态（将被修改：角速率、姿态DCM）
        UtVec3dX             aRotationalAccel_rps2, // 体轴角加速度 [p_dot, q_dot, r_dot] (rad/s²)
        double               aDeltaT_sec             // 时间步长 (s)
    );

    // 用 F&M 推进状态（中间步）：执行力/力矩限幅 → 计算加速度 → 平动推进 → 转动推进。
    // 内部包含力限幅（1000g 上限）和力矩限幅（100 rev/s² 上限）。
    static void PropagateUsingFM(
        P6DofVehicle*               aObject,           // 飞行器对象
        P6DofKinematicState&        aState,            // 运动学状态（将被推进）
        const P6DofMassProperties&  aMassProperties,   // 当前质量特性
        double                      aDeltaT_sec,        // 时间步长 (s)
        P6DofForceAndMomentsObject& aForcesMomentsAtRP, // 参考点处力/力矩
        P6DofForceAndMomentsObject& aForcesMomentsAtCM  // 质心处力/力矩
    );

    // 完整更新状态（校正步）：先更新燃油消耗，再用平均 F&M 对原始状态推进。
    static void UpdateUsingFM(
        P6DofVehicle*               aObject,           // 飞行器对象
        P6DofKinematicState&        aState,            // 运动学状态（将被最终更新）
        const P6DofMassProperties&  aMassProperties,   // 质量特性
        int64_t                     aSimTime_nanosec,   // 当前仿真时间 (ns)
        double                      aDeltaT_sec,        // 时间步长 (s)
        P6DofForceAndMomentsObject& aForcesMomentsAtRP, // 参考点平均力/力矩
        P6DofForceAndMomentsObject& aForcesMomentsAtCM  // 质心平均力/力矩
    );
};
```

### 2.2 P6DofForceAndMomentsObject（力/力矩容器 — 概念接口）

```cpp
// 力/力矩容器：维护在指定参考点处的体轴合力和合力矩。
// 核心功能与 wsf_six_dof 的 ForceAndMomentsObject 等价：
//   参考点管理、力/力矩叠加（含自动参考点转换）、矢量限幅、算术平均。
class P6DofForceAndMomentsObject {
public:
    // 清空所有力/力矩
    void ClearForcesAndMoments();

    // 设置内部参考点坐标 (ft)
    void MoveRefPoint_ft(const UtVec3dX& aRefPoint_ft);

    // 在当前参考点处追加力 (lbf)
    void AddForceAtReferencePoint(const UtVec3dX& aForce_lbs);

    // 在当前参考点处追加力和力矩 (lbf, ft-lbf)
    void AddForceAndMomentAtReferencePoint(
        const UtVec3dX& aForce_lbs,
        const UtVec3dX& aMoment_ftlbs
    );

    // 获取当前参考点处的力/力矩
    void GetForceAndMomentAtCurrentRefPoint(
        UtVec3dX& aForce_lbs,       // [输出] 体轴合力 (lbf)
        UtVec3dX& aMoment_ftlbs     // [输出] 体轴合力矩 (ft-lbf)
    ) const;

    // 获取当前参考点处的力矩
    UtVec3dX GetMomentAtRefPoint_ftlbs() const;

    // 叠加运算符：自动参考点转换
    P6DofForceAndMomentsObject& operator+=(
        const P6DofForceAndMomentsObject& aOther
    );

    // 力矢量限幅（按幅值等比缩放）
    void LimitMaxForceMagnitude_lbs(double aMaxForceMagnitude_lbs);

    // 力矩矢量限幅（按幅值等比缩放）
    void LimitMomentMagnitude_ftlbs(double aMaxMomentMagnitude_ftlbs);

    // Heun 算术平均：(当前 + aOther) / 2
    void CalcAverageWith(const P6DofForceAndMomentsObject& aOther);
};
```

### 2.3 P6DofKinematicState（运动学状态 — 概念接口）

```cpp
// P6DOF 运动学状态：存储飞行器仿真的完整瞬态运动学状态。
// 注意：此类属于 AFSIM 框架，此处给出概念接口用于移植。
class P6DofKinematicState {
public:
    // ---------- 位置/速度 ----------
    // 获取/设置位置 (WGS84 ECEF 或球面坐标)
    void SetPosition(const UtVec3dX& pos);
    UtVec3dX GetPosition() const;

    // 获取/设置速度
    void SetVelocity(const UtVec3dX& vel);
    UtVec3dX GetVelocity() const;

    // ---------- 姿态 ----------
    // 获取/设置方向余弦矩阵（体轴 → 世界坐标系）
    void SetDCM(const UtDCM& dcm);
    UtDCM GetDCM() const;

    // ---------- 角速率 ----------
    // 获取/设置体轴角速率 (rad/s)，[p, q, r] = [滚转, 俯仰, 偏航]
    void SetOmegaBody(const UtVec3dX& omega);
    UtVec3dX GetOmegaBody() const;

    // 设置体轴角加速度 (rad/s²)
    void SetOmegaBodyDot(const UtVec3dX& omega_dot);

    // ---------- 气动状态 ----------
    double GetAlpha_rad() const;    // 攻角 (rad)
    double GetBeta_rad() const;     // 侧滑角 (rad)
    double GetMach() const;         // 马赫数（无量纲）
    double GetDynamicPressure_lbsqft() const;  // 动压 (lb/ft²)

    // 更新气动状态（重新计算 alpha, beta, Mach, 动压等）
    void UpdateAeroState(int64_t aSimTime_nanosec, double aDeltaT_sec);

    // 更新气动状态变化率（alpha_dot, beta_dot）
    void CalculateRates(int64_t aSimTime_nanosec);

    // 计算辅助输出参数（LLA, 航向, 飞行路径角, Mach, 动压等）
    void CalculateSecondaryParameters();

    // ---------- 坐标系转换 ----------
    // 体轴矢量 → 惯性系矢量
    UtVec3dX CalcInertialVecFromBodyVec(const UtVec3dX& bodyVec) const;
    // 惯性系矢量 → 体轴矢量
    UtVec3dX CalcBodyVecFromInertialVec(const UtVec3dX& inertialVec) const;

    // ---------- 重力 ----------
    // 获取归一化重力加速度方向（惯性系单位矢量）
    UtVec3dX NormalizedGravitationalAccelVec() const;

    // ---------- 诊断/监控 ----------
    // 设置体轴过载（以 g 为单位，不含重力分量）
    void SetBodyAccel(double nx_g, double ny_g, double nz_g);

    // 设置升力/阻力/侧力/推力/重量监控值 (lbf)
    void SetLiftDragSideForceThrustWeight(
        double lift_lbs, double drag_lbs, double sideForce_lbs,
        double thrust_lbs, double wgt_lbs
    );

    // 设置质心处的总力矩 (ft-lbf)
    void SetMomentAtCG(const UtVec3dX& moment_ftlbs);

    // ---------- 起落架 ----------
    bool GetWeightOnWheels() const;

    // ---------- 测试辅助 ----------
    void RemoveAlphaForTesting();
};
```

### 2.4 P6DofMassProperties（质量特性 — 概念接口）

```cpp
// P6DOF 质量特性容器：飞行器当前的质量属性。
struct P6DofMassProperties {
    double GetMass_lbs() const;              // 当前质量 (lbm)
    UtVec3dX GetCmPosRelToRef_ft() const;    // 质心相对参考点的偏移 (ft)
    double GetIxx_slugft2() const;           // 滚转轴转动惯量 (slug-ft²)
    double GetIyy_slugft2() const;           // 俯仰轴转动惯量 (slug-ft²)
    double GetIzz_slugft2() const;           // 偏航轴转动惯量 (slug-ft²)
};
```

## 3. 典型调用模式

```cpp
// ========== 1. 积分器初始化（纯静态类，不需要实例化） ==========
// P6DofIntegrator 的所有方法都是 static，不需要创建实例。
// Clone() 仅用于框架的多态积分器管理。

// ========== 2. 仿真主循环（每帧一次） ==========
int64_t simTime_ns = 0;          // 仿真时间戳（纳秒）
double  dt_sec     = 1.0 / 60.0; // 60Hz 物理步长（秒）

// 飞行器对象已在框架中创建和配置（含质量特性、气动模型、推进模型、起落架）
P6DofVehicle* vehicle = ...;  // 由框架管理

for (int frame = 0; frame < 36000; frame++) {  // 仿真 10 分钟
    // 一步 Heun 积分推进飞行器的所有运动学状态：
    //   1) vehicle.CalculateCurrentMassProperties()  → 更新质量/质心/转动惯量
    //   2) tempState = copy(kinematicState)          → 保存原始快照
    //   3) F0 = CalculateFM(vehicle, tempState, t_last, EPSILON)
    //      → 气动+推进+起落架+重力
    //   4) PropagateUsingFM(vehicle, tempState, ..., F0)
    //      → 力限幅→加速度→平动推进→转动推进
    //   5) F1 = CalculateFM(vehicle, tempState, t_current, EPSILON)
    //      → 在预测态重新计算
    //   6) F_avg = (F0 + F1) / 2                    → Heun 平均
    //   7) 诊断值拷贝：tempState → kinematicState
    //   8) UpdateUsingFM(vehicle, kinematicState, ..., F_avg)
    //      → 燃油消耗 + 平均F&M校正推进
    //   9) 后处理：CalculateRates + CalculateSecondaryParameters
    P6DofIntegrator::Update(
        vehicle,
        simTime_ns,     // 当前仿真时间 (ns)
        dt_sec           // 时间步长 (s)
    );

    simTime_ns += static_cast<int64_t>(dt_sec * 1e9);

    // 读取更新后的状态用于日志/可视化
    auto& state = vehicle->GetKinematicState();
    logPosition(simTime_ns, state.GetPosition());           // 位置
    logAttitude(simTime_ns, state.GetDCM());                // 姿态 DCM
    logAeroAngles(simTime_ns, state.GetAlpha_rad(), state.GetBeta_rad());
}

// ========== 3. 力/力矩计算的典型调用链 ==========
// 在 CalculateFM() 内部依次计算四项力/力矩：

// --- 准备 ---
auto& massProps = aObject->GetMassProperties();
P6DofForceAndMomentsObject FM_RP, FM_CM;
FM_CM.MoveRefPoint_ft(massProps.GetCmPosRelToRef_ft());  // CM参考点=质心

// --- 气动力/力矩 ---
aState.UpdateAeroState(atmosphere, wind, aSimTime_nanosec, aDeltaT_sec);
// 计算升力/阻力/侧力/力矩
aObject->CalculateAeroBodyFM(aeroLift, aeroDrag, aeroSide, aeroMoment, refPt);
aeroTotal = aeroLift + aeroDrag + aeroSide;  // 体轴总气动力 (lbf)
P6DofForceAndMomentsObject AeroFM;
AeroFM.MoveRefPoint_ft(refPt + aeroCenter_ft);
AeroFM.AddForceAndMomentAtReferencePoint(aeroTotal, aeroMoment);
FM_RP += AeroFM;  // 叠加到参考点F&M，自动参考点转换

// --- 推进力/力矩 ---
aObject->CalculatePropulsionFM(aSimTime_nanosec, aDeltaT_sec, aState,
                                inertialPropForce, propMoment);
propBodyForce = aState.CalcBodyVecFromInertialVec(inertialPropForce);
FM_RP.AddForceAndMomentAtReferencePoint(propBodyForce, propMoment);

// --- 起落架力/力矩 ---
aObject->CalculateLandingGearFM(aSimTime_nanosec, ...);
FM_RP.AddForceAndMomentAtReferencePoint(gearBodyForce, gearMoment);

// --- 重力（仅作用于质心，不含力矩） ---
gravityVec = aState.NormalizedGravitationalAccelVec();
gravityInertialForce = gravityVec * currentMass_lbm;  // 重力 = 方向×质量 (lbf)
gravityBodyForce = aState.CalcBodyVecFromInertialVec(gravityInertialForce);
FM_CM.AddForceAtReferencePoint(gravityBodyForce);

// 总质心力矩 = CM力矩 + RP力矩（operator+= 自动参考点转换）
P6DofForceAndMomentsObject totalCM = FM_CM;
totalCM += FM_RP;   // 参考点偏移产生的附加力矩自动计算

// ========== 4. PropagateUsingFM 的力→加速度转换 ==========
// 在 PropagateUsingFM() 内部：
double mass_lbs = aMassProperties.GetMass_lbs();

// 力矢量限幅（1000g 上限）
double maxForce_lbs = mass_lbs * 1000.0;
FM_RP.LimitMaxForceMagnitude_lbs(maxForce_lbs);

// 设置体轴过载
FM_RP.GetForceAndMomentAtCurrentRefPoint(nonGravityForce, ...);
aState.SetBodyAccel(nonGravityForce.X() / mass_lbs,  // Nx (g)
                    nonGravityForce.Y() / mass_lbs,  // Ny (g)
                    nonGravityForce.Z() / mass_lbs); // Nz (g)

// 合并 RP 和 CM 的 F&M 到 CM
P6DofForceAndMomentsObject totalFM_CM = FM_CM;
totalFM_CM += FM_RP;

// 力矩限幅（100 rev/s² 上限）
double I_max = max(Ixx, Iyy, Izz);
double maxMoment = I_max * (100.0 * 360.0 * DEG_PER_RAD);
totalFM_CM.LimitMomentMagnitude_ftlbs(maxMoment);

// 提取总力/力矩 → 惯性系加速度
totalFM_CM.GetForceAndMomentAtCurrentRefPoint(totalBodyForce, totalMoment);
totalInertialForce = aState.CalcInertialVecFromBodyVec(totalBodyForce);
inertialAccel = totalInertialForce * 9.80665 / mass_lbs;  // F/m*g0 (m/s²)

// 平动推进（分派到球面或WGS84地球模型）
PropagateTranslation(aObject, aState, inertialAccel, aDeltaT_sec);

// 角加速度 = 力矩 / 转动惯量（各轴独立）
rotationalAccel[0] = totalMoment.X() / Ixx_slugft2;  // p_dot (rad/s²)
rotationalAccel[1] = totalMoment.Y() / Iyy_slugft2;  // q_dot (rad/s²)
rotationalAccel[2] = totalMoment.Z() / Izz_slugft2;  // r_dot (rad/s²)

// 转动推进（四元数姿态积分）
PropagateRotation(aObject, aState, rotationalAccel, aDeltaT_sec);
```

## 4. 坐标系/单位约定

### 坐标系

| 坐标系 | 轴定义 | 用途 |
|--------|--------|------|
| **Body（体轴系）** | X=前, Y=右, Z=下 | 气动力/力矩、推力、过载表达 |
| **Inertial（惯性系）** | WCS ECEF 或球面地心惯性 | 推进力和重力在惯性系下的表达 |
| **WGS84 ECEF** | 地心地固直角坐标 | 椭圆地球模型下的位置/速度推进 |
| **Spherical Earth** | 球面地心坐标 | 简化地球模型下的位置/速度推进（半径 6366707 m） |

### 地球模型选择

- `aObject->UseSphericalEarth() == true` → 球面地球（恒定半径，简单弹道导弹用）
- `aObject->UseSphericalEarth() == false` → WGS84 椭球地球（高保真场景用）

### 单位约定（AFSIM 原始代码混合单位制）

| 物理量 | AFSIM 原始单位 | SI 等效 | 换算关系 |
|--------|---------------|---------|----------|
| 位置 | ft | m | 1 ft = 0.3048 m |
| 速度 | ft/s | m/s | 1 ft/s = 0.3048 m/s |
| 加速度 | m/s² | m/s² | 统一 |
| 角度 | rad | rad | 统一 |
| 角速率 | rad/s | rad/s | 统一 |
| 角加速度 | rad/s² | rad/s² | 统一 |
| 质量 | lbm (slug) | kg | 1 slug = 32.174 lbm |
| 力 | lbf | N | 1 lbf = 4.448 N |
| 力矩 | ft-lbf | N·m | 1 ft-lbf = 1.356 N·m |
| 转动惯量 | slug-ft² | kg·m² | 1 slug-ft² = 1.356 kg·m² |
| 动压 | lb/ft² (psf) | Pa | 1 psf = 47.88 Pa |

**关键换算公式**：
- 英制力 → 公制加速度：`a_mps2 = F_lbf * 9.80665 / mass_lbm`
- 其中 `9.80665 m/s²` 既是标准重力加速度，也是 lbf → N 的换算式中的隐含因子

### 为统一移植建议使用的 SI 单位制

所有新实现建议统一使用 SI 单位制：位置 m、速度 m/s、加速度 m/s²、质量 kg、力 N、力矩 N·m、转动惯量 kg·m²、动压 Pa。

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|----------|----------|
| `P6DofVehicle` | 飞行器模型 | 自定义 `Vehicle` 接口（质量/气动/推进/起落架子系统 + 地球模型选择） |
| `P6DofKinematicState` | 运动学状态容器 | 自定义 `KinematicState` 结构体（位置/速度/DCM/角速率/气动角） |
| `P6DofForceAndMomentsObject` | 力/力矩容器 | 自定义 `ForceMoments` 类（参考点管理 + 叠加含自动转换 + 矢量限幅 + 算术平均） |
| `P6DofMassProperties` | 质量特性容器 | 自定义 `MassProperties` 结构体（mass/cm/inertia） |
| `P6DofFreezeFlags` | 冻结标志 | 可移除或自定义冻结标志位掩码 |
| `P6DofScenario` / `P6DofAtmosphere` | 场景/大气配置 | 自定义 `Environment` 上下文 |
| `P6DofLandingGear` | 起落架模型 | 自定义起落架子系统（纯空中飞行器可省略） |
| `UtQuaternion` | 四元数运算 | `Eigen::Quaterniond` 或自定义四元数类（需 SetRate/Update/Normalize/ToDCM） |
| `UtDCM` | 方向余弦矩阵 | `Eigen::Matrix3d` 或自定义 DCM 类 |
| `UtVec3dX` | 三维矢量 | `Eigen::Vector3d` |
| `UtMath::cFT_PER_M / cDEG_PER_RAD / cRAD_PER_DEG` | 单位换算常数 | 直接硬编码 `0.3048`, `57.29578`, `0.0174533` |
| `cEPSILON_SIMTIME_SEC` (~1e-12) | 极小时间步长 | 自定义常数 `1e-12` |

**与 wsf_six_dof 版积分器的主要差异**：
1. P6DofIntegrator 所有方法为 **static**，wsf_six_dof 版有实例状态（mVehicle 指针）
2. P6DofIntegrator 用 `EPSILON (1e-12 s)` 代替零时间步长传给 CalculateFM，避免除零
3. P6DofIntegrator 支持双地球模型（球面/WGS84），wsf_six_dof 版在基类 PropagateTranslation 中处理
4. P6DofIntegrator 不包含 `operator+=` 隐式参考点转换中的附加力矩自动计算（需要显式处理）
