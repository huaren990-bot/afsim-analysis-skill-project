# 编队汇合/位置保持/追击三状态机动控制 — 接口规格

> **日期:** 2026-06-24
> **状态:** draft
> **对应算法卡:** flight-dynamics-station-keeping-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────┐
│           WsfFormUpKeepStationManeuver                    │
│         (编队汇合/位置保持机动容器)                         │
├──────────────────────────────────────────────────────────┤
│  + Evaluate() → 分发给当前活跃状态对象                      │
│  + GetG_LoadMax() : double                                │
│  + GetSpeedMpsMin() : double                              │
│  + GetSpeedMpsMax() : double                              │
│  + LimitG_Load(g) : double                                │
│  + LimitSpeed(v) : double                                 │
│  + IsSpeedInsideAllowedRange(v) : bool                    │
└──────────┬───────────────────────────────────────────────┘
           │ owns and dispatches to
           ▼
┌──────────────────────────────────────────────────────────┐
│          RelativeManeuverState (抽象基类)                  │
├──────────────────────────────────────────────────────────┤
│  + Evaluate() → unique_ptr<RelativeManeuverState>         │
│  + GetEvaluationInterval() : double                       │
└──┬──────────────────────┬──────────────────────┬─────────┘
   │                      │                      │
   ▼                      ▼                      ▼
┌──────────────┐ ┌────────────────┐ ┌──────────────────────┐
│ FormUpState  │ │KeepStationState│ │ PursueState          │
│ (汇合状态)    │ │ (位置保持状态)   │ │ (追击状态)            │
├──────────────┤ ├────────────────┤ ├──────────────────────┤
│ 评估间隔:1.0s │ │ 评估间隔:0.1s   │ │ 评估间隔:1.0s         │
│              │ │                │ │                      │
│ 输出:        │ │ 输出:          │ │ 输出:                │
│  roll        │ │  roll          │ │  roll                │
│  altitude    │ │  g-load        │ │  g-load              │
│  speed       │ │  speed         │ │  speed               │
└──────────────┘ └────────────────┘ └──────────────────────┘
```

## 2. 状态转移规则

```
        距离 < 200m
  FormUp ───────────────► KeepStation
     ▲                       │
     │         距离 > 500m    │
     └───────────────────────┘
                             │
                             │ 目标速度越界 3次
                             ▼
                         Pursue
                             │
                             │ 目标速度回界 3次
                             ▼
                        KeepStation
```

## 3. 核心接口定义

### 3.1 机动容器接口

```cpp
// ==========================================
// 编队汇合/位置保持机动 — 容器接口
// 管理追击者到目标点的运动，维护三状态状态机
// ==========================================
struct FormUpKeepStationManeuver {
    // ----- 机体性能限制接口 -----
    // 返回机动允许的最大 G载荷 (g 倍数)
    double GetG_LoadMax() const;

    // 返回机动允许的最小/最大空速 (m/s)
    double GetSpeedMpsMin() const;
    double GetSpeedMpsMax() const;

    // 判断速度是否在允许范围内
    bool IsSpeedInsideAllowedRange(double speed_mps) const;

    // 将 G载荷钳制到允许范围
    double LimitG_Load(double g) const;

    // 将速度钳制到允许范围
    double LimitSpeed(double v_mps) const;
};
```

### 3.2 共享数据结构

```cpp
// ==========================================
// 机动共享数据 — 追击者和目标运动状态
// 所有状态对象共享此只读引用
// ==========================================
struct ManeuverData {
    // 追击者信息
    Platform*    chaser_platform_ptr;    // 追击者平台指针（查询位置/速度/加速度）
    Vec3d        chaser_loc_wcs;         // 追击者 WCS 位置 (m)

    // 目标站位的运动学状态
    Kinematics   kinematics;             // 目标站位的完整运动学
    // kinematics.mLocWCS   : WCS 位置 (m)
    // kinematics.mVelWCS   : WCS 速度 (m/s)
    // kinematics.mAccWCS   : WCS 加速度 (m/s²)
    // kinematics.mAnglesNED: NED 欧拉角 [yaw, pitch, roll] (rad)
    // kinematics.mG_Load   : 当前 G载荷 (g 倍数)

    // 追击者到目标的 WCS 分离矢量 (m)
    Vec3d        separation_wcs;         // = chaser_loc - target_loc
};
```

### 3.3 控制输出接口

```cpp
// ==========================================
// 自动驾驶仪指令输出接口
// 各状态共同输出到自动驾驶仪
// ==========================================
struct AutopilotCommands {
    double roll_angle_deg = 0.0;    // 指令滚转角 (deg) — 所有状态共用
    double pitch_g_load   = 1.0;    // 指令纵向 G载荷 (g) — KeepStation + Pursue
    double speed_ktas     = 0.0;    // 指令空速 (KTAS) — 所有状态共用
    double altitude_ft    = 0.0;    // 指令高度 (ft) — 仅 FormUp 状态
};
```

## 4. 典型调用模式

```cpp
// ==========================================
// 编队保持机动 — 典型仿真循环
// ==========================================

// 1. 创建机动对象（从编队定义初始化）
FormUpKeepStationManeuver maneuver;
// ... 从输入脚本加载 maneuver 配置 ...

// 2. 初始状态为 FormUp（从远距离开始汇合）
auto current_state = std::make_unique<FormUpState>(data, maneuver);

// 3. 仿真循环
double sim_time_s = 0.0;
double next_eval_time_s = 0.0;

while (sim_time_s < scenario_end_time_s) {
    // 仅在规定的评估间隔到达时才评估状态
    if (sim_time_s >= next_eval_time_s) {
        // 更新共享数据（目标位置、追击者位置等）
        UpdateManeuverData(data);

        // 评估当前状态 → 可能返回新状态（状态转移）
        auto new_state = current_state->Evaluate();

        if (new_state != nullptr) {
            // 发生了状态转移
            current_state = std::move(new_state);
        }

        // 获取下次评估的时间
        next_eval_time_s = sim_time_s + current_state->GetEvaluationInterval();
    }

    // 积分器每步仍在运行（1/60s 物理步长）
    sim_time_s += dt_physics_s;
}

// ==========================================
// 输出示例（KeepStation 状态）
// ==========================================
// 在 KeepStationState::Evaluate() 内部：
//
//   ComputeCoordinates(deltaLoc, deltaVel, deltaAcc);
//   // deltaLoc  = ECS转换后的位置偏差 (m)
//   // deltaVel  = ECS转换后的速度偏差 (m/s)
//   // deltaAcc  = ECS转换后的加速度偏差 (m/s²)
//
//   double roll = ComputeRollAngleDeg(deltaLoc, deltaVel, deltaAcc);
//   // = target_roll_deg - 0.7*loc_Y - 3.0*vel_Y - 6.0*acc_Y
//
//   double g = ComputeG_Load(deltaLoc, deltaVel);
//   // = target_g + 0.05*loc_Z + 0.1*vel_Z
//
//   double speed = ComputeSpeedKTAS(deltaLoc, deltaVel, deltaAcc);
//   // = target_speed - 0.5*loc_X - 1.0*vel_X - 5.0*acc_X
//
//   chaser->SetAutopilotRollAngle(roll);
//   chaser->SetPitchGLoad(g);
//   chaser->SetAutopilotSpeedKTAS(speed);
```

## 5. 坐标系约定

| 坐标系 | 用途 |
|--------|------|
| **WCS** (ECEF) | 追击者和目标的绝对位置、速度、加速度计算 |
| **ECS** (实体坐标系) | 位置/速度/加速度偏差的控制律计算（X=前向, Y=右侧, Z=下方） |
| **NED** | 目标姿态角度（`mAnglesNED`: yaw/pitch/roll） |

## 6. 框架依赖解耦

| AFSIM 原始依赖 | 替换方案 |
|---------------|----------|
| `WsfFormUpKeepStationManeuver` | 简单的 `ManeuverConfig` 结构体（含 G/speed 限制） |
| `WsfRelativeManeuver::Data` | `ManeuverData` 结构体（上） |
| `UtEntity::ConvertWCSToECS()` / `ConvertWCSVectorToECS()` | 基于目标 DCM 的四元数旋转矩阵乘法 |
| `TurnCircle` (圆形航迹) | 自定义 `CirclePath::LocationAtPhase(phase)` |
| `WsfPlatform` (平台指针) | 自定义 `Entity` 接口（`GetVelocityWCS()`, `GetAccelerationWCS()`, `GetLocationWCS()`） |
| `UtMath::cDEG_PER_RAD`, `UtMath::cNMPH_PER_MPS` | `180/M_PI`, `1.94384449` |

## 7. 增益常量表（移植参考）

所有控制增益均为经验值，移植后需重新调参：

| 常量 | 值 | 用途 |
|------|----|------|
| `cKEEP_STATION_ROLL_ALPHA` | 0.7 °/m | 位置保持滚转角 P 增益 |
| `cKEEP_STATION_ROLL_BETA` | 3.0 °·s/m | 位置保持滚转角 D 增益 |
| `cKEEP_STATION_ROLL_GAMMA` | 6.0 °·s²/m | 位置保持滚转角 DD 增益 |
| `cKEEP_STATION_GLOAD_ALPHA` | 0.05 m⁻¹ | 位置保持 G载荷 P 增益 |
| `cKEEP_STATION_GLOAD_BETA` | 0.1 s/m | 位置保持 G载荷 D 增益 |
| `cKEEP_STATION_SPEED_ALPHA` | 0.5 s⁻¹ | 位置保持速度 P 增益 |
| `cKEEP_STATION_SPEED_BETA` | 1.0 | 位置保持速度 D 增益 |
| `cKEEP_STATION_SPEED_GAMMA` | 5.0 s | 位置保持速度 DD 增益 |
| `cFORM_UP_CLOSING_ALPHA_FACTOR` | 1.0e-3 | FormUp 缩放因子 |
| `cFORM_UP_CLOSING_BETA_FACTOR` | 5.0e-3 | FormUp 缩放因子 |
