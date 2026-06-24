# 舵机执行机构 — 接口规格

> **日期:** 2026-06-24
> **状态:** draft
> **对应算法卡:** flight-dynamics-rate-limited-actuator-card.md, flight-dynamics-first-order-lag-actuator-card.md

## 1. 总体架构

AFSIM 中执行机构（Actuator）分为两类数学实现，分别对应不同的飞行器建模精度：

```
┌──────────────────────────────────────────────────────┐
│              执行机构 (Actuator)                       │
├──────────────────────────┬───────────────────────────┤
│  角速率限制舵机            │  一阶滞后滤波执行机构        │
│  (Rate-Limited Actuator) │  (First-Order Lag)        │
│                          │                           │
│  适用: 刚体六自由度舵面     │  适用: 点质模型连续控制通道  │
│  P6DofControlActuator    │  PointMassControlActuator │
│  RigidBodyControlActuator│                           │
│                          │                           │
│  核心: 最大角速率钳制       │  核心: 隐式欧拉一阶微分方程   │
│  输出: 角度 (deg)          │  输出: 归一化设定值 [0,1]     │
└──────────┬───────────────┴───────────┬───────────────┘
           │                           │
           ▼                           ▼
┌──────────────────────────────────────────────────────┐
│            飞行控制系统 (FlightControlSystem)           │
│  PID 嵌套回路 → 指令角度/指令设定值 → Actuator.Update()  │
└──────────────────────────────────────────────────────┘
```

## 2. 核心接口定义

### 2.1 角速率限制舵机

```cpp
// ==========================================
// 角速率限制执行机构（P6DOF / 刚体六自由度通用）
// 以有限角速率驱动舵面，受机械止动约束
// ==========================================
class RateLimitedActuator {
public:
    // ----- 配置参数 -----
    struct Config {
        double max_positive_rate_dps = 0.0;   // 正向最大角速率 (deg/s)
        double max_negative_rate_dps = 0.0;   // 负向最大角速率 (deg/s)
        double max_angle_deg         = 0.0;   // 机械止动最大角度 (deg) —— 必需
        double min_angle_deg         = 0.0;   // 机械止动最小角度 (deg) —— 必需
    };

    // ----- 构造函数 -----
    // 传入父飞控系统指针（用于访问测试模式标志）
    RateLimitedActuator(FlightControlSystem* parent);

    // ----- 主更新方法 -----
    // sim_time_ns: 当前仿真时间 (纳秒)
    // cmd_angle_deg: 飞控系统输出的指令舵面角度 (度)
    // 副作用: 更新内部 mCurrentAngle_deg
    void Update(int64_t sim_time_ns, double cmd_angle_deg);

    // ----- 更新并返回当前角度 -----
    // 等同于 Update() + GetCurrentAngle()
    // 返回值: 经过速率限制和限幅后的实际角度 (度)
    double UpdateAndGetCurrentAngle(int64_t sim_time_ns, double cmd_angle_deg);

    // ----- 查询当前角度 -----
    // 返回值: 当前舵面实际角度 (度)
    double GetCurrentAngle() const;

    // ----- 强制设置角度（瞬时，绕过速率限制） -----
    // 用于初始化或重置场景
    void SetCurrentAngle(double angle_deg);
};
```

### 2.2 一阶滞后滤波执行机构

```cpp
// ==========================================
// 一阶滞后滤波执行机构（点质模型专用）
// 用隐式欧拉法平滑跟踪归一化指令设定值
// ==========================================
class FirstOrderLagActuator {
public:
    // ----- 配置参数 -----
    struct Config {
        double lag_time_constant_sec = 0.0;  // 一阶滞后时间常数 (s)
                                              // 0.0 = 瞬时响应
    };

    // ----- 构造函数 -----
    FirstOrderLagActuator(FlightControlSystem* parent);

    // ----- 主更新方法 -----
    // sim_time_ns: 当前仿真时间 (纳秒)
    // cmd_setting: 飞控系统输出的指令设定值 (归一化, 期望范围[0,1])
    // 副作用: 更新内部 mCurrentSetting
    void Update(int64_t sim_time_ns, double cmd_setting);

    // ----- 更新并返回当前设定值 -----
    double UpdateAndGetCurrentSetting(int64_t sim_time_ns, double cmd_setting);

    // ----- 查询当前设定值 -----
    double GetCurrentSetting() const;

    // ----- 强制设置设定值（瞬时） -----
    void SetCurrentSetting(double setting);
};
```

## 3. 典型调用模式

```cpp
// ==========================================
// 1. 角速率限制执行机构 — 典型用法
// ==========================================

// 1a. 创建并配置舵机
RateLimitedActuator::Config elevator_config;
elevator_config.max_positive_rate_dps = 60.0;   // 最大上偏速率 60°/s
elevator_config.max_negative_rate_dps = 40.0;   // 最大下偏速率 40°/s
elevator_config.max_angle_deg         = 25.0;   // 最大机械角度 +25° (上偏限)
elevator_config.min_angle_deg         = -15.0;  // 最小机械角度 -15° (下偏限)

RateLimitedActuator elevator(&flight_control_system);
elevator.SetCurrentAngle(0.0);  // 初始位置: 中立

// 1b. 仿真循环（每帧调用）
double sim_time_s = 0.0;
double dt_s = 1.0 / 60.0;  // 60 Hz

for (int frame = 0; frame < 3600; frame++) {
    // PID 控制器计算出的指令舵面角度
    double cmd_elevator_deg = pid_controller.Compute(altitude_error, dt_s);

    // 通过执行机构进行速率限制
    elevator.Update(
        static_cast<int64_t>(sim_time_s * 1e9),  // 秒 -> 纳秒
        cmd_elevator_deg
    );

    // 获取实际角度用于气动力计算
    double actual_elevator_deg = elevator.GetCurrentAngle();

    // ... 使用 actual_elevator_deg 计算气动力矩 ...

    sim_time_s += dt_s;
}

// ==========================================
// 2. 一阶滞后执行机构 — 典型用法
// ==========================================

// 2a. 创建并配置
FirstOrderLagActuator::Config throttle_config;
throttle_config.lag_time_constant_sec = 0.3;  // 发动机推力响应时间常数 0.3s

FirstOrderLagActuator throttle(&flight_control_system);

// 2b. 仿真循环
double cmd_throttle = 0.8;  // PID 输出的油门指令 (80%)
throttle.Update(sim_time_ns, cmd_throttle);

double actual_throttle = throttle.GetCurrentSetting();
// actual_throttle 会在 ~0.3s 后达到 cmd_throttle 的 63.2%
```

## 4. 坐标系与单位约定

角速率限制执行机构仅涉及角度量，不涉及空间坐标系：

| 量 | 内部单位 | 输入/输出单位 |
|----|---------|------------|
| 角度 | 度 (°) | 度 (°) |
| 角速率 | 度/秒 (°/s) | 度/秒 (°/s) |
| 时间 | 纳秒 (ns) 内部、秒 (s) 计算 | 纳秒 (ns) |
| 设定值 | 无量纲 [0, 1] | 无量纲 [0, 1] |

## 5. 框架依赖解耦

| AFSIM 原始依赖 | 替换方案 |
|---------------|----------|
| `P6DofFlightControlSystem` / `RigidBodyFlightControlSystem` / `PointMassFlightControlSystem` | 父指针改为泛型 `void* context` 或去除（将测试标志作为构造参数传入） |
| `P6DofFreezeFlags::GetMasterNoLagTesting()` / `testingNoLag` | 构造函数中添加 `bool no_lag_mode = false` 参数 |
| `P6DofUtils::TimeToTime()` / `utils::TimeToTime()` | `std::chrono::duration<double>(nanoseconds).count()` |
| `UtMath::cDEG_PER_RAD` | `180.0 / M_PI` |
| `UtMath::cNMPH_PER_MPS` | `1.94384449` |
| `UtInput` / `UtInputBlock` | JSON / YAML 配置解析 |
