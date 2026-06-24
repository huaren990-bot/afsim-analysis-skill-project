# 自动驾驶仪 PID 嵌套回路控制 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-autopilot-pid-card.md

## 1. 总体架构

```
┌───────────────────────────────────────────────────────────────┐
│                     CommonController                          │
│  (自动驾驶仪主控 — BTT/YTT 分发 + 嵌套回路调度)                │
│  包含 20 个 PID 实例 + 4 条嵌套回路                            │
├───────────────────────────────────────────────────────────────┤
│  + Update(controls, dT_ns)  [纯虚函数]                        │
│  + SetCurrentActivity(action*)                                │
│  # UpdateBankToTurn(controls, simTime)                        │
│  # UpdateYawToTurn(controls, simTime)                         │
│  # EnforceControlLimits()                                     │
│  # CalcGBiasData() / CalcAlphaBetaGLimits()                   │
│                                                                 │
│  PID实例 (20个)：                                               │
│  mAlphaPID, mVerticalSpeedPID, mPitchAnglePID, ...             │
│                                                                 │
│  嵌套回路调度：                                                  │
│  mLateralControlLoop (middle/outer loops)                     │
│  mVerticalControlLoop                                         │
│  mSpeedControlLoop                                            │
└──────────┬────────────────────────────────────────────────────┘
           │ 使用 20 个 PID 实例
           ▼
┌───────────────────────────────────────────────────────────────┐
│                          PID                                  │
│  (单回路 PID 控制器 — 增益调度 + 抗积分饱和 + 低通滤波)         │
├───────────────────────────────────────────────────────────────┤
│  + CalcOutputFromTarget(SP, PV, time)                         │
│  + CalcOutputFromTargetWithLimits(SP, PV, time, min, max)     │
│  + CalcOutputFromError(error, curVal, time)                   │
│  + CalcOutputFromErrorWithLimits(error, curVal, time, min,max)│
│  + SetControllingValue(value)    → 增益调度控制变量            │
│  + SetBias(bias)                 → 前馈偏置                    │
│  - GetOutputWithLimits(time, min, max, useLimits)             │
│  - CalcPidGainsData(tables, controllingValue, ...)            │
│                                                                 │
│  13个跨帧状态变量：                                              │
│  mOutput, mErrorAccum, mCurrentError, mCurrentDerivative, ... │
│  mGainTables (增益调度数据表)                                    │
└──────────┬────────────────────────────────────────────────────┘
           │ 数据结构
           ▼
┌───────────────────────────────────────────────────────────────┐
│                       PidGainData                             │
│  (PID 增益条目 — 增益调度表的单行)                              │
├───────────────────────────────────────────────────────────────┤
│  ControllingValue, KpGain, KiGain, KdGain,                    │
│  LowpassAlpha, MaxAccum, MaxErrorZero, MinErrorZero, Kt       │
└───────────────────────────────────────────────────────────────┘
```

**BTT（Bank-To-Turn）嵌套回路架构：**

```
                     ┌──────────────────────┐
  航向命令 ─────────→│  RollHeadingPID      │ 外侧回路：航向误差 → 转弯速率
  (heading_deg)      │  (航向→转弯速率)       │ 更新间隔：middle×outer 帧
                     └──────────┬───────────┘
                                │ cmdTurnRate_dps
                                ▼
                     ┌──────────────────────┐
                     │  BankAnglePID        │ 中间回路：转弯速率 → 坡角 → 滚转速率
                     │  (坡角→滚转速率)       │ 更新间隔：middle 帧
                     └──────────┬───────────┘
                                │ cmdRollRate_dps
                                ▼
                     ┌──────────────────────┐
                     │  RollRatePID         │ 内侧回路：滚转速率 → 副翼指令
                     │  (滚转速率→stickRight) │ 更新间隔：每帧
                     └──────────────────────┘
```

**垂直通道嵌套回路架构：**

```
                     ┌──────────────────────┐
  高度命令 ─────────→│  AltitudePID         │ 外侧回路：高度误差 → 垂直速率
  (alt_ft)           │  (高度→垂直速率)       │
                     └──────────┬───────────┘
                                │ cmdVertSpeed_fpm
                                ▼
                     ┌──────────────────────┐
                     │  VerticalSpeedPID    │ 中间回路：垂直速率 → 攻角
                     │  (垂直速度→攻角)       │ 前馈偏置：g-bias Alpha
                     └──────────┬───────────┘
                                │ cmdAlpha_deg
                                ▼
                     ┌──────────────────────┐
                     │  AlphaPID            │ 内侧回路：攻角 → 升降舵指令
                     │  (攻角→stickBack)     │
                     └──────────────────────┘
```

## 2. 核心接口定义

### 2.1 PidGainData（PID 增益调度表条目）

```cpp
// PID 增益调度表的一行数据。
// 每个 PidGainData 记录在指定控制变量值下的全套 PID 参数。
// 增益表按 ControllingValue 单调递增排序，运行时线性插值获取中间值。
struct PidGainData {
    float KpGain = 0.0f;           // 比例增益 Kp，放大当前误差
    float KiGain = 0.0f;           // 积分增益 Ki，放大误差累积量（消除稳态误差）
    float KdGain = 0.0f;           // 微分增益 Kd，放大误差变化率（抑制超调）

    float LowpassAlpha = 1.0f;     // 导数低通滤波系数（0~1）
                                   //   0 = 最强滤波（纯积分模式，完全平滑）
                                   //   1 = 不滤波（直接使用采样导数）

    float MaxAccum = FLT_MAX;      // 积分累积值绝对值上限
                                   //   防止积分饱和（windup）

    float MaxErrorZero = FLT_MAX;  // 大误差抗积分饱和阈值
                                   //   |error| > MaxErrorZero → 停止积分累积
                                   //   防止执行器饱和时积分器持续累加

    float MinErrorZero = FLT_MIN;  // 小误差死区阈值
                                   //   |error| < MinErrorZero → 停止积分累积
                                   //   防止稳态零误差附近因噪声导致的积分抖振

    float KtAntiWindup = 0.0f;     // 抗积分饱和反馈增益 Kt
                                   //   有效积分增益 = Ki + Kt*(u_limited - u_prelimited)
                                   //   当输出被限幅时，Kt 反馈修正积分通道

    float ControllingValue = 0.0f; // 增益调度控制变量（如动压 q_bar，用于查表插值）
                                   //   表中各行按此值单调递增排序
};
```

### 2.2 PID（单回路 PID 控制器）

```cpp
// PID 控制器：实现带增益调度的比例-积分-微分控制算法。
// 每个 PID 实例维护 13 个跨帧状态变量，独立追踪误差累积、导数滤波和输出。
// 支持：增益调度（动压/Mach 查表线性插值）、导数低通滤波、
//       抗积分饱和（Kt 反算 + 误差阈值死区）、前馈偏置（feed-forward bias）。
class PID {
public:
    // ---------- 初始化 ----------

    // 从配置输入块读取 PID 参数和增益表
    void ProcessInput(UtInputBlock& aInputBlock);

    // 克隆：深拷贝一个新的 PID 实例
    PID* Clone() const;

    // ---------- 四种求值接口 ----------

    // 按设定点和当前值计算误差后求 PID 输出（无输出限幅）。
    // aSetPoint:   设定点 SP（目标值）
    // aCurValue:   过程变量 PV（当前测量值）
    // aSimTime_sec: 当前仿真时间（秒 s），用于计算实际帧间隔 dT
    // 返回: PID 输出 u(t)
    double CalcOutputFromTarget(
        double aSetPoint,    // 设定点（目标值）
        double aCurValue,    // 过程变量（当前测量值）
        double aSimTime_sec  // 仿真时间 (s)
    );

    // 按设定点和当前值计算误差后求 PID 输出（带输出限幅）。
    // aMinOutput: 输出下限（小于此值则钳位）
    // aMaxOutput: 输出上限（大于此值则钳位）
    double CalcOutputFromTargetWithLimits(
        double aSetPoint, double aCurValue, double aSimTime_sec,
        double aMinOutput, double aMaxOutput  // 输出限幅范围
    );

    // 按外部预计算误差求 PID 输出（无输出限幅）。
    // 适用于角度归一化等场景（误差需在 [-180, +180] 区间内预先归一化）。
    // aError:  预计算误差 e = SP - PV（已归一化）
    // aCurValue: 当前过程变量 PV（用于导数计算）
    double CalcOutputFromError(
        double aError,       // 预计算误差
        double aCurValue,    // 当前过程变量
        double aSimTime_sec  // 仿真时间 (s)
    );

    // 按外部预计算误差求 PID 输出（带输出限幅）。
    double CalcOutputFromErrorWithLimits(
        double aError, double aCurValue, double aSimTime_sec,
        double aMinOutput, double aMaxOutput
    );

    // ---------- 运行时设置 ----------

    // 设置过程变量当前值（在不求值的情况下更新 PV 记录）
    void SetCurrentValue(double aCurrentValue);

    // 设置设定点目标值
    void SetTargetValue(double aTargetValue);

    // 设置增益调度控制变量（如动压 q_bar 或马赫数 Mach）。
    // 每次求值前需调用，GetOutputWithLimits() 通过它查增益表插值。
    void SetControllingValue(double aControllingValue);

    // 设置前馈偏置（feed-forward bias），直接加到 P 通道输出。
    // 用于引入上级回路输出的先验信息（如 g-bias 攻角、阻力前馈）。
    // 偏置在清零前持续有效。
    void SetBias(double aBias);
    void SetFeedForward(double aFeedForward);  // 别名，同 SetBias

    // 查询前馈偏置是否激活及当前值
    bool GetFeedForward(double& aFeedForward);

    // ---------- 增益表管理 ----------

    // 获取增益调度数据表（用于外部查看/修改）
    std::vector<PidGainData>* GetPidGainTableData();

    // 设置增益调度数据表
    void SetPidGainTableData(const std::vector<PidGainData>& aDataTables);

    // 向增益表预分配空间（在逐条添加前调用，避免空表错误）
    void AddElementsToGainTable(size_t aTotalElementsInTable);

    // ---------- 更新间隔 ----------

    // 获取 PID 最小更新间隔 (s)
    double GetUpdateInterval_sec();

    // 尝试设置更新间隔，但保留已有的更小值
    // 嵌套回路的外侧/中间层通过此机制实现降频运行
    bool TrySetUpdateInterval_sec(double aInterval_sec);

    // ---------- 状态管理 ----------

    // 获取 PID 的当前运行值（SetPoint/Kp/Ki/Kd/Output/AccumError 等）
    void GetPidValueData(SinglePidValueData& aData) const;

    // 清零所有计算状态（误差累积、导数、时间戳等）
    // 用于父运动器状态重置时的 PID 重置
    void ResetPidState();

    // 仅清零仿真时间相关数据（时间戳），保留增益表配置
    // 用于"洗入"（wash-in）后恢复
    void ResetPidTiming();

private:
    // ---------- PID 核心求值（私有） ----------

    // 每帧 PID 求值核心流水线（143 行）：
    //   1) 更新间隔检查：dT < updateInterval → 返回上一帧输出
    //   2) 增益调度线性插值：CalcPidGainsData() → 获取 Kp/Ki/Kd/Alpha/MaxAccum/...
    //   3) 导数低通滤波：adjustedAlpha = dT/(intendedTau + dT)
    //      currentDerivative = adjustedAlpha * (-dPV/dT) + (1-adjustedAlpha) * lastDerivative
    //   4) 误差累积条件判断：
    //      - |error| > MaxErrorZero → 停止累积（大误差抗积分饱和）
    //      - |error| < MinErrorZero → 停止累积（小误差死区）
    //   5) Kt 抗积分饱和：effectiveKi = Ki + Kt*(u_limited - u_prelimited)
    //   6) 积分累积：errorAccum += error * dT
    //   7) 积分限幅：clamp(errorAccum, -MaxAccum, +MaxAccum)
    //   8) 三通道输出叠加：
    //      u = Kp*error + effectiveKi*accum + Kd*derivative + bias
    //   9) 输出限幅（可选）：clamp(u, minOutput, maxOutput)
    //  10) 保存状态：lastValue/Error/Derivative/SimTime
    double GetOutputWithLimits(
        double aSimTime_sec,  // 当前仿真时间 (s)
        double aMinOutput,    // 输出下限
        double aMaxOutput,    // 输出上限
        bool   aUseLimits     // 是否执行输出限幅
    );

    // 增益调度线性插值：按当前 controllingValue 查增益表，
    // 插值得到 Kp/Ki/Kd/LowpassAlpha/MaxAccum/MaxErrorZero/MinErrorZero/KtAntiWindup。
    // 边界处理：
    //   - 空表：全部增益 = 0
    //   - 单元素表：直接使用
    //   - 控制值 <= 首条目：使用首条目
    //   - 控制值 >= 末条目：使用末条目
    //   - 中间值：线性插值
    void CalcPidGainsData(
        std::vector<PidGainData>& aTables,         // 增益表
        double                    aControllingValue, // 当前控制变量值
        double& aKpGain,           // [输出] 比例增益
        double& aKiGain,           // [输出] 积分增益
        double& aKdGain,           // [输出] 微分增益
        double& aLowpassAlpha,     // [输出] 低通滤波系数
        double& aMaxAccum,         // [输出] 积分累积上限
        double& aMaxErrorZero,     // [输出] 大误差抗积分饱和阈值
        double& aMinErrorZero,     // [输出] 小误差死区阈值
        double& aKtAntiWindup      // [输出] 抗积分饱和反馈增益
    );

    // ---------- 跨帧状态变量（13 个） ----------

    double mLastSimTime_sec = 0.0;              // 上次求值的时间戳 (s)
    ut::optional<double> mUpdateInterval_sec;   // 最小更新间隔 (s)，嵌套外层/中间层使用

    double mSetPoint          = 0.0;  // PID 设定点 SP（目标值）
    double mCurrentValue      = 0.0;  // 当前过程变量 PV（测量值）
    double mCurrentError      = 0.0;  // 当前误差 e = SP - PV
    double mCurrentDerivative = 0.0;  // 当前低通滤波后的过程变量变化率 dPV/dt

    double mLastValue      = 0.0;      // 上一帧过程变量 PV(t-1)，用于采样导数
    double mLastError      = 0.0;      // 上一帧误差 e(t-1)
    double mLastDerivative = 0.0;      // 上一帧滤波后导数

    double mErrorAccum       = 0.0;    // 积分误差累积量 ∫e(τ)dτ，受 MaxAccum 限幅
    double mPrelimitedOutput = 0.0;    // 限幅前输出值 u_prelimited，用于 Kt 反算
    double mOutput           = 0.0;    // 当前最终输出值 u(t)（可能经限幅）

    std::vector<PidGainData> mGainTables;  // 增益调度数据表

    double mControllingValue        = 0.0;    // 当前增益调度控制变量值（如动压）
    bool   mProportionalBiasActive  = false;  // 前馈偏置激活标志
    double mProportionalBiasValue   = 0.0;    // 前馈偏置值，直接加到 P 通道
};
```

### 2.3 CommonController（自动驾驶仪主控）

```cpp
// 自动驾驶仪主控类：实现 BTT/YTT 两种控制模式，管理 20 个 PID 控制器。
// 通过三级嵌套反馈回路（外侧→中间→内侧）将航路导航命令转换为操纵面指令。
// 包含增益调度、攻角/侧滑角限幅、g-bias 补偿、速度阻力前馈等辅助逻辑。
class CommonController {
public:
    // ---------- 自动驾驶仪输出结构 ----------

    // 每帧由自动驾驶仪填充的控制面输出指令
    struct sAutopilotControls {
        double stickBack           = 0.0;  // 升降舵指令（-1 全推 ~ +1 全拉）
        double stickRight          = 0.0;  // 副翼指令（-1 全左 ~ +1 全右）
        double rudderRight         = 0.0;  // 方向舵指令（-1 全左 ~ +1 全右）
        double throttleMilitary    = 0.0;  // 军推油门（0 慢车 ~ 1 全推）
        double throttleAfterburner = 0.0;  // 加力油门（0 关 ~ 1 全开）
        double thrustVectorYaw     = 0.0;  // 推力矢量偏航
        double thrustVectorPitch   = 0.0;  // 推力矢量俯仰
        double thrustVectorRoll    = 0.0;  // 推力矢量滚转
        double speedBrake          = 0.0;  // 减速板（0 关 ~ 1 全开）
        double noseWheelSteering   = 0.0;  // 前轮转向（NWS 方式1）
        double nwsSteering         = 0.0;  // 前轮转向（NWS 方式2）
        double wheelBrakeLeft      = 0.0;  // 左轮刹车
        double wheelBrakeRight     = 0.0;  // 右轮刹车
    };

    // ---------- 嵌套回路时序管理 ----------

    struct NestedFeedbackLoop {
        // 中间回路倍率：内侧回路每执行 middleLoopFactor 次，中间回路执行 1 次
        ut::optional<int> middleLoopFactor;
        // 外侧回路倍率：中间回路每执行 outerLoopFactor 次，外侧回路执行 1 次
        ut::optional<int> outerLoopFactor;

        // 计算中间回路更新间隔 = middleLoopFactor * cDT_RIGID_BODY_SEC
        double GetMiddleLoopInterval_sec();
        // 计算外侧回路更新间隔 = middleLoopFactor * outerLoopFactor * cDT_RIGID_BODY_SEC
        double GetOuterLoopInterval_sec();
    };

    // ---------- 纯虚函数（子类必须实现） ----------

    // 设置父运动器指针
    virtual void SetParentVehicle(Mover* aVehicle) = 0;

    // 主更新入口：每帧由飞行控制系统调用。
    // 内部分发到 BTT 或 YTT 控制模式，依次处理横向/垂直/速度通道。
    virtual void Update(
        sAutopilotControls& aControls,  // [输出] 操纵面指令
        int64_t             aDT_nanosec // 本帧时间步长 (ns)
    ) = 0;

    // 按 PID 类型获取 PID 实例指针（子类实现寄存器查找）
    virtual PID* GetPID_ByType(Pid::Type aTableType) = 0;

protected:
    // ---------- BTT/YTT 分发 ----------

    // Bank-To-Turn 控制更新
    void UpdateBankToTurn(sAutopilotControls& aControls, double aSimTime);
    // Yaw-To-Turn 控制更新
    void UpdateYawToTurn(sAutopilotControls& aControls, double aSimTime);

    // ---------- 横向通道（纯虚，子类实现具体模式分发） ----------

    virtual void ProcessLaternalNavChannelsBankToTurn(double aSimTime) = 0;
    virtual void ProcessLaternalNavChannelsYawToTurn(double aSimTime) = 0;

    // 标准横向模式（基类提供默认实现）
    virtual void ProcessStandardLateralNavMode_RollHeading(
        double aHeading_deg, double aSimTime);
    virtual void ProcessStandardLateralNavMode_Bank(
        double aBankAngle_deg, double aSimTime);
    virtual void ProcessStandardLateralNavMode_RollRate(
        double aCommandedRollRate_dps, double aSimTime);
    virtual void ProcessStandardLateralNavMode_YawHeading(
        double aHeading_deg, double aSimTime);
    virtual void ProcessStandardLateralNavMode_YawRate(
        double aCommandedYawRate_dps, double aSimTime);
    virtual void ProcessStandardLateralNavMode_Beta(
        double aCommandedBeta_deg, double aSimTime);

    // ---------- 垂直通道 ----------

    virtual void ProcessVerticalNavChannelBankToTurn(double aSimTime) = 0;
    virtual void ProcessVerticalNavChannelYawToTurn(double aSimTime) = 0;

    // 标准垂直模式（基类提供默认实现）
    virtual void ProcessStandardVerticalNavMode_Altitude(
        double aAltitude_ft, double aSimTime);
    virtual void ProcessStandardVerticalNavMode_VertSpeed(
        double aCommandedVertSpeed_fpm, double aSimTime);
    virtual void ProcessStandardVerticalNavMode_Alpha(
        double aCommandedAlpha_deg, double aSimTime);

    // ---------- 速度通道 ----------

    virtual void ProcessSpeedChannelBankToTurn(double aSimTime) = 0;
    virtual void ProcessSpeedChannelYawToTurn(double aSimTime) = 0;

    // 标准速度模式：速度误差 → SpeedPID → 油门指令。
    // 包含阻力前馈偏置：biasThrottle = (drag - minThrust) / (maxThrust - minThrust)
    virtual double ProcessStandardSpeedMode_FPS(
        double aSpeed_fps, double aSimTime);

    // ---------- 辅助计算 ----------

    // 计算 alpha/beta 限幅：同时考虑 g-load 限制和直接配置限制，取交集
    void CalcAlphaBetaGLimits();

    // 计算 g-bias 补偿：nz_bias = (1/cos(roll)) * cos(pitch)
    // 输出 g-bias 值和对应的攻角偏置（用于垂直速度 PID 前馈）
    void CalcGBiasData(double& aGBias_g, double& aGBiasAlpha_deg);

    // ---------- 操控面限幅 ----------

    // 所有操纵面指令强制限幅至 [-1, 1] 或 [0, 1]
    void EnforceControlLimits();

    // ---------- 活动管理 ----------

    // 获取/设置当前自动驾驶活动（外部管理生命周期）
    AutopilotAction* GetCurrentActivity() const;
    void SetCurrentActivity(AutopilotAction* aAPActivity);

    // ---------- 限幅与设置管理 ----------

    const AutopilotLimitsAndSettings& GetCurrentLimitsAndSettings() const;
    void SetCurrentLimitsAndSettings(const AutopilotLimitsAndSettings& aData);
    void RevertLimitsAndSettingsToDefaults();

    // ---------- 20 个 PID 实例 ----------

    PID mAlphaPID;               // 攻角 → 升降舵（垂直通道内侧回路）
    PID mVerticalSpeedPID;       // 垂直速率 → 攻角（垂直通道中间回路）
    PID mPitchAnglePID;          // 俯仰角 → 攻角
    PID mPitchRatePID;           // 俯仰速率 → 攻角
    PID mFlightPathAnglePID;     // 飞行路径角 → 攻角
    PID mDeltaPitchPID;          // 增量俯仰 → 攻角
    PID mAltitudePID;            // 高度 → 垂直速率（垂直通道外侧回路）
    PID mBetaPID;                // 侧滑角 → 方向舵（YTT 内侧回路）
    PID mYawRatePID;             // 偏航速率 → 侧滑角（YTT 中间回路）
    PID mYawHeadingPID;          // 偏航角 → 偏航速率（YTT 外侧回路）
    PID mTaxiHeadingPID;         // 滑行航向 → 偏航速率
    PID mRollRatePID;            // 滚转速率 → 副翼（BTT 内侧回路）
    PID mDeltaRollPID;           // 增量滚转 → 副翼
    PID mBankAnglePID;           // 坡角 → 滚转速率（BTT 中间回路）
    PID mRollHeadingPID;         // 航向 → 转弯速率（BTT 外侧回路）
    PID mForwardAccelPID;        // 前向加速度 → 油门
    PID mSpeedPID;               // 速度 → 油门
    PID mTaxiForwardAccelPID;    // 滑行前向加速度 → 油门
    PID mTaxiSpeedPID;           // 滑行速度 → 油门
    PID mTaxiYawRatePID;         // 滑行偏航速率 → 方向舵

    // ---------- 嵌套回路时序调度 ----------

    NestedFeedbackLoop mVerticalControlLoop;  // 垂直通道嵌套（middle/outer factor）
    NestedFeedbackLoop mLateralControlLoop;   // 横向通道嵌套
    NestedFeedbackLoop mSpeedControlLoop;     // 速度通道嵌套

    // ---------- 内部状态 ----------

    sAutopilotControls mControlOutputs;                // 当前帧输出
    AutopilotLimitsAndSettings mDefaultLimitsAndSettings;
    AutopilotLimitsAndSettings mCurrentLimitsAndSettings;
    AutopilotAction* mCurrentActivityPtr = nullptr;    // 外部管理的自动驾驶命令
    Control::Method mControlMethod = Control::Undefined; // 控制方法（BTT/YTT）

    double mCurrentGBias_g        = 1.0;   // 当前 g-bias 值（考虑滚转/俯仰修正）
    double mCurrentGBiasAlpha_deg = 0.0;   // g-bias 对应的攻角偏置 (deg)
    double mLimitedMinAlpha_deg   = 0.0;   // 有效攻角下限 (deg)
    double mLimitedMaxAlpha_deg   = 0.0;   // 有效攻角上限 (deg)
    double mLimitedBeta_deg       = 0.0;   // 有效侧滑角最大绝对值 (deg)
};
```

### 2.4 辅助数据结构

```cpp
// ---------- SinglePidValueData（单回路 PID 运行状态快照）----------

// 用于外部查看一个 PID 实例的当前运行值（调试/监控用）
struct SinglePidValueData {
    float SetPoint      = 0.0f;  // PID 目标值 SP
    float CurrentValue  = 0.0f;  // 过程变量 PV
    float KpValue       = 0.0f;  // 当前比例增益 Kp
    float KiValue       = 0.0f;  // 当前积分增益 Ki
    float KdValue       = 0.0f;  // 当前微分增益 Kd
    float FFValue       = 0.0f;  // 当前前馈偏置值
    float OutputBase    = 0.0f;  // 限幅前输出 u_prelimited
    float OutputLimited = 0.0f;  // 限幅后输出 u
    float AccumError    = 0.0f;  // 积分累积量
    bool  FFValueValid  = false; // 前馈偏置是否激活
};

// ---------- AutopilotLimitsAndSettings（自动驾驶仪限幅与设置）----------

struct AutopilotLimitsAndSettings {
    // 控制开关
    bool  enableAfterburnerAutoControl = false;  // 加力自动控制开关
    bool  enableSpeedBrakeAutoControl  = false;  // 减速板自动控制开关

    // 阈值
    float afterburnerThreshold         = 1.0f;   // 加力触发阈值（油门 > 1.0 时开启加力）
    float speedBrakeThreshold          = 0.0f;   // 减速板触发阈值

    // 转弯控制
    float turnRollInMultiplier         = 1.0f;   // 转弯滚入倍率
    float routeAllowableAngleError_rad = 1.0f;   // 航路允许角度误差 (rad)

    // ---------- 限幅 ----------
    float pitchGLoad_Min   = 0.0f;     // 俯仰最小 g-load
    float pitchGLoad_Max   = 1.5f;     // 俯仰最大 g-load
    float alpha_Min        = 0.0f;     // 攻角下限 (deg)
    float alpha_Max        = 10.0f;    // 攻角上限 (deg)
    float pitchRate_Min    = -5.0f;    // 俯仰速率下限 (deg/s)
    float pitchRate_Max    = 10.0f;    // 俯仰速率上限 (deg/s)
    float vertSpd_Min      = -3000.0f; // 垂直速率下限 (ft/min)
    float vertSpd_Max      = 3000.0f;  // 垂直速率上限 (ft/min)
    float yawGLoad_Max     = 0.4f;     // 最大侧向 g-load
    float beta_Max         = 10.0f;    // 侧滑角最大绝对值 (deg)
    float yawRate_Max      = 5.0f;     // 偏航速率上限 (deg/s)
    float rollRate_Max     = 50.0f;    // 滚转速率上限 (deg/s)
    float bankAngle_Max    = 45.0f;    // 最大坡角 (deg)
    float forwardAccel_Min = -1.0f;    // 前向加速度下限 (g)
    float forwardAccel_Max = 2.0f;     // 前向加速度上限 (g)
    float taxiSpeed_Max    = 10.0f;    // 最大滑行速度 (ft/s)
    float taxiYawRate_Max  = 5.0f;     // 最大滑行偏航速率 (deg/s)
};

// ---------- Pid::Type（PID 类型枚举）----------

// 枚举所有 20 种 PID 类型，用于通过类型标识查找对应的 PID 实例
namespace Pid {
    enum Type {
        Unknown, Alpha, VerticalSpeed, PitchAngle, PitchRate,
        FlightPathAngle, DeltaPitch, Altitude, Beta, YawRate,
        YawHeading, TaxiHeading, RollRate, DeltaRoll, BankAngle,
        RollHeading, ForwardAccel, Speed, TaxiForwardAccel,
        TaxiSpeed, TaxiYawRate, LastPidType
    };
}
```

## 3. 典型调用模式

```cpp
// ========== 1. PID 配置（从数据文件加载） ==========
// 为每个 PID 实例加载增益调度表
PID alphaPID;
// ... 从 XML/JSON 读取 alphaPID 增益表数据 ...
// alphaPID 增益表可能类似：
//   ControllingValue=0(Kp=1,Ki=0.1,Kd=0.01)  → 低速高增益
//   ControllingValue=100(Kp=0.5,Ki=0.05,Kd=0.005) → 高速低增益

PID altitudePID;
// altitudePID 的嵌套层级最深，需要设置更新间隔：
//   TrySetUpdateInterval_sec(0.5)  → 外侧回路每 0.5s 执行一次

// ========== 2. 自动驾驶仪主循环（每帧一次） ==========
// 在飞行控制系统每帧调用中：

void FlightControlSystem::Update(int64_t simTime_ns, double dt_sec) {
    sAutopilotControls controls;

    // 自动驾驶仪执行完整控制回路计算：
    //   1) CalcAlphaBetaGLimits() → 计算攻角/侧滑角限幅
    //   2) CalcGBiasData()        → 计算 g-bias 补偿
    //   3) UpdateBankToTurn() 或 UpdateYawToTurn()
    //      └── BTT 横向: RollHeadingPID → BankAnglePID → RollRatePID → stickRight
    //      └── BTT 垂直: AltitudePID → VerticalSpeedPID → AlphaPID → stickBack
    //      └── 速度: SpeedPID → throttle
    //   4) EnforceControlLimits() → 所有输出限幅至 [-1,1] 或 [0,1]
    mAutopilot.Update(controls, simTime_ns);

    // 将操纵面指令传给飞行控制执行器
    applyControls(controls);  // stickBack → 升降舵偏角, throttle → 发动机推力, 等
}

// ========== 3. BTT 横向嵌套回路完整调用链 ==========
// 以下展示航向→转弯速率→坡角→滚转速率→副翼的完整信号链：

// --- 外侧回路：航向误差 → 指令转弯速率 ---
void ProcessStandardLateralNavMode_RollHeading(double heading_deg, double simTime) {
    double curHeading_deg = mVehicle->getLocalHeading_deg();  // 当前航向 (deg)
    double hdgError_deg = NormalizeAngle180(heading_deg - curHeading_deg);  // 归一化到 [-180, +180]

    // 计算最大转弯速率（基于最大坡角和当前速度的物理限制）
    double speed_fps = mVehicle->getSpeed_fps();  // 当前速度 (ft/s)
    double lateral_g = tan(maxBank_rad);          // 水平升力分量 (g)
    double radius_ft = speed_fps*speed_fps / (32.174 * lateral_g);  // 转弯半径 (ft)
    double circumference_ft = 2*PI * radius_ft;
    double timeToCircle_sec = circumference_ft / speed_fps;
    double maxTurnRate_dps = 360.0 / timeToCircle_sec;  // 最大转弯速率 (deg/s)

    // RollHeadingPID 求值 → 指令转弯速率
    // 入: hdgError_deg (航向误差, deg) → 出: cmdTurnRate_dps (转弯速率, deg/s)
    // 限幅: ±maxTurnRate_dps（受物理转弯能力约束）
    mRollHeadingPID.SetControllingValue(mVehicle->getDynamicPressure()); // 动压 → 增益调度
    double cmdTurnRate_dps = mRollHeadingPID.CalcOutputFromErrorWithLimits(
        hdgError_deg, curHeading_deg, simTime, -maxTurnRate_dps, maxTurnRate_dps);

    // --- 转弯速率 → 坡角反算 ---
    double radius_ft = speed_fps / (2*PI * abs(cmdTurnRate_dps) / 360.0);
    double lateral_g = speed_fps*speed_fps / (radius_ft * 32.174);
    double pitchFactor = 1.0 / cos(pitchAngle_rad);  // 俯仰角修正
    double bank_rad = atan2(lateral_g, pitchFactor);
    double cmdBank_deg = bank_rad * RAD_PER_DEG * sign(cmdTurnRate_dps);
    cmdBank_deg = clamp(cmdBank_deg, -bankAngle_Max, bankAngle_Max);

    // --- 中间回路：坡角误差 → 指令滚转速率 ---
    double curBank_deg = mVehicle->getLocalRoll_deg();
    double bankError_deg = NormalizeAngle180(cmdBank_deg - curBank_deg);
    mBankAnglePID.SetControllingValue(mVehicle->getDynamicPressure());
    double cmdRollRate_dps = mBankAnglePID.CalcOutputFromErrorWithLimits(
        bankError_deg, curBank_deg, simTime, -rollRate_Max, rollRate_Max);

    // --- 内侧回路：滚转速率误差 → 副翼指令 ---
    double curRollRate_dps = mVehicle->getRollRate_dps();
    cmdRollRate_dps = clamp(cmdRollRate_dps, -rollRate_Max, rollRate_Max);
    mRollRatePID.SetControllingValue(mVehicle->getDynamicPressure());
    mControlOutputs.stickRight = mRollRatePID.CalcOutputFromTarget(
        cmdRollRate_dps, curRollRate_dps, simTime);  // 输出: -1 ~ +1
}

// ========== 4. 垂直嵌套回路调用链 ==========

void ProcessStandardVerticalNavMode_Altitude(double cmdAlt_ft, double simTime) {
    double curAlt_ft = mVehicle->getAlt_ft();  // 当前高度 (ft)

    // 外侧回路：AltPID → 指令垂直速率
    mAltitudePID.SetControllingValue(mVehicle->getDynamicPressure());
    double cmdVertSpeed_fpm = mAltitudePID.CalcOutputFromTargetWithLimits(
        cmdAlt_ft, curAlt_ft, simTime, vertSpd_Min, vertSpd_Max);
        // 输出限幅：-3000 ~ +3000 ft/min

    // 中间回路：VertSpeedPID → 指令攻角（含 g-bias 前馈）
    double curVertSpeed_fpm = mVehicle->getVerticalSpeed_fpm();
    cmdVertSpeed_fpm = clamp(cmdVertSpeed_fpm, vertSpd_Min, vertSpd_Max);

    mVerticalSpeedPID.SetBias(mCurrentGBiasAlpha_deg);  // g-bias 攻角 → 前馈偏置
    mVerticalSpeedPID.SetControllingValue(mVehicle->getDynamicPressure());
    double cmdAlpha_deg = mVerticalSpeedPID.CalcOutputFromTargetWithLimits(
        cmdVertSpeed_fpm, curVertSpeed_fpm, simTime,
        mLimitedMinAlpha_deg, mLimitedMaxAlpha_deg);

    // 内侧回路：AlphaPID → 升降舵指令
    double curAlpha_deg = mVehicle->getAlpha_deg();
    cmdAlpha_deg = clamp(cmdAlpha_deg, mLimitedMinAlpha_deg, mLimitedMaxAlpha_deg);
    mAlphaPID.SetControllingValue(mVehicle->getDynamicPressure());
    mControlOutputs.stickBack = mAlphaPID.CalcOutputFromTarget(
        cmdAlpha_deg, curAlpha_deg, simTime);  // 输出: -1 ~ +1
}

// ========== 5. 速度通道（单回路 PID + 阻力前馈） ==========

double ProcessStandardSpeedMode_FPS(double cmdSpeed_fps, double simTime) {
    double curSpeed_fps = mVehicle->getSpeed_fps();  // 当前速度 (ft/s)

    // 计算前馈偏置：基于当前阻力与可用推力的线性插值
    double drag_lbs    = mVehicle->getDrag_lbs();     // 当前阻力 (lbf)
    double alpha_rad   = mVehicle->getAlpha_rad();
    double cosAlpha    = cos(alpha_rad);
    double maxThrust   = mVehicle->getMaxPotentialThrust_lbs() * cosAlpha;  // 最大推力投影
    double minThrust   = mVehicle->getMinPotentialThrust_lbs() * cosAlpha;  // 最小推力投影
    double deltaThrust = maxThrust - minThrust;

    double biasThrottle = 0.0;
    if (drag_lbs > maxThrust) {
        biasThrottle = 1.0;   // 阻力 > 最大推力 → 全推
    } else if (drag_lbs < minThrust) {
        biasThrottle = -1.0;  // 阻力 < 最小推力 → 减速
    } else if (deltaThrust != 0) {
        biasThrottle = (drag_lbs - minThrust) / deltaThrust;  // 线性插值
    }

    mSpeedPID.SetBias(biasThrottle);  // 阻力前馈偏置
    mSpeedPID.SetControllingValue(mVehicle->getDynamicPressure());

    // SpeedPID → 油门指令（限幅 -1 ~ 2，其中 1~2 用于分拆军推+加力）
    double cmdThrottle = mSpeedPID.CalcOutputFromTargetWithLimits(
        cmdSpeed_fps, curSpeed_fps, simTime, -1.0, 2.0);
    return cmdThrottle;
}

// ========== 6. PID 内部：增益调度线性插值 ==========
// 当 PID.GetOutputWithLimits() 调用 CalcPidGainsData() 时：
//   假设 mGainTables 有两条记录：
//     [0] ControllingValue=0,   KpGain=1.0
//     [1] ControllingValue=100, KpGain=0.5
//   当 mControllingValue=50（当前动压为中间值）时：
//     fraction = (50-0) / (100-0) = 0.5
//     Kp = 1.0 + 0.5 * (0.5-1.0) = 0.75  → 线性插值结果
//   同理插值得到 Ki, Kd, LowpassAlpha, MaxAccum, MaxErrorZero, MinErrorZero, Kt
```

## 4. 坐标系/单位约定

### PID 各回路物理量及单位

| 回路名称 | 设定点 SP（物理量） | 过程变量 PV（物理量） | SP/PV 单位 | 输出 u(t) | 输出单位 |
|----------|-------------------|---------------------|-----------|-----------|----------|
| AlphaPID | 指令攻角 | 当前攻角 | deg | stickBack | 无量纲 [-1, +1] |
| VerticalSpeedPID | 指令垂直速率 | 当前垂直速率 | ft/min | 指令攻角 | deg |
| AltitudePID | 指令高度 | 当前高度 | ft | 指令垂直速率 | ft/min |
| PitchAnglePID | 指令俯仰角 | 当前俯仰角 | deg | 指令攻角 | deg |
| PitchRatePID | 指令俯仰速率 | 当前俯仰速率 | deg/s | 指令攻角 | deg |
| FlightPathAnglePID | 指令飞行路径角 | 当前飞径角 | deg | 指令攻角 | deg |
| DeltaPitchPID | 增量俯仰角 | 累计增量角 | deg | 指令攻角 | deg |
| BetaPID | 指令侧滑角 | 当前侧滑角 | deg | rudderRight | 无量纲 [-1, +1] |
| YawRatePID | 指令偏航速率 | 当前偏航速率 | deg/s | 指令侧滑角 | deg |
| YawHeadingPID | 指令航向角 | 当前航向角 | deg | 指令偏航速率 | deg/s |
| RollRatePID | 指令滚转速率 | 当前滚转速率 | deg/s | stickRight | 无量纲 [-1, +1] |
| BankAnglePID | 指令坡角 | 当前坡角 | deg | 指令滚转速率 | deg/s |
| RollHeadingPID | 指令航向角 | 当前航向角 | deg | 指令转弯速率 | deg/s |
| SpeedPID | 指令速度 | 当前速度 | ft/s | 油门 | 无量纲 [-1, 2] |
| ForwardAccelPID | 指令前向加速 | 当前前向加速 | g | 油门 | 无量纲 [-1, 2] |

### 角度归一化

对于航向角（heading）和坡角（bank angle）等圆形量，误差必须在 [-180°, +180°] 范围内归一化后传入 PID：

```
hdgError = NormalizeAngle180(cmdHeading - curHeading)
// 例如：cmdHeading=359°, curHeading=1° → 误差 = -2°（不是 358°）
```

### 增益调度控制变量

通常使用 **动压 q_bar** (lb/ft²) 作为控制变量，也可使用 **马赫数 Mach**。随着动压/Mach 变化，PID 增益通过线性插值平滑调整：
- 低动压（低速高空）：高增益 → 灵敏感应
- 高动压（高速低空）：低增益 → 避免过控

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|----------|----------|
| `wsf::six_dof::CommonController` | 自动驾驶仪主控基类 | 自定义 `AutopilotController` 类，含 BTT/YTT 分发 + 嵌套回路调度 |
| `wsf::six_dof::PID` | PID 控制器 | 自定义 `PIDController` 类（增益调度 + 抗积分饱和 + 低通滤波 + 前馈偏置） |
| `PidGainData` | 增益条目结构体 | 直接复制结构体定义（9 个 float 成员） |
| `SinglePidValueData` | 运行状态快照 | 直接复制结构体定义 |
| `AutopilotLimitsAndSettings` | 限幅配置结构体 | 自定义 `AutopilotLimits` 结构体 |
| `sAutopilotControls` | 操纵面输出结构体 | 自定义 `ControlOutputs` 结构体（12 个 double 成员） |
| `NestedFeedbackLoop` | 嵌套回路时序管理 | 自定义 `LoopScheduler` 类（middleFactor/outerFactor） |
| `AutopilotAction` | 自动驾驶命令 | 自定义 `FlightCommand` 类 |
| `Mover` / `KinematicState` | 飞行状态查询 | 自定义 `VehicleState` 接口 |
| `UtTable::Curve` | 1D 曲线（CL/Mach, Alpha/Mach 等） | 自定义 1D 线性/Akima 插值 |
| `UtTable::Table` | 2D 表（Alpha vs Mach vs CL） | 自定义 2D 线性插值 |
| `UtInput` / `UtInputBlock` | 配置解析 | JSON/YAML/TOML 解析器 |
| `UtVec3dX` | 三维矢量 | `Eigen::Vector3d` |
| `UtLLAPos` | 经纬高位置 | 自定义 GeoPoint 类 |
| `UtMath` (NormalizeAngle180, NearlyZero, PI) | 数学工具 | `M_PI`, 自定义 NormalizeAngle180 |

**核心需要重新实现的类**：
1. `PIDController`：13 个状态变量 + 增益调度线性插值 + 导数低通滤波（时间常数归一化）+ 抗积分饱和（Kt 反算 + 误差阈值死区）+ 前馈偏置
2. `AutopilotController`：20 个 PID 实例组网 + BTT/YTT 嵌套回路时序调度 + g-bias 补偿 + alpha/beta 限幅
3. `LoopScheduler`：middleFactor/outerFactor 倍率 → 更新间隔映射

**移植关键点**：
- PID 导数低通滤波的时间常数归一化技术（`adjustedAlpha = dT/(intendedTau + dT)`）是 AFSIM 特有的处理，移植时需仔细复现
- 增益调度的 8 参数同时线性插值（Kp/Ki/Kd/Alpha/MaxAccum/MaxErrorZero/MinErrorZero/Kt）需要在 `CalcPidGainsData()` 等效实现中完整保留
- 嵌套回路的降频运行机制通过 `mUpdateInterval_sec` 实现，外侧/中间回路只在 dT >= updateInterval 时执行求值
