# 轨道机动模型 — 接口规格

> **日期:** 2026-06-11 | **状态:** draft | **对应算法卡:** space-orbital-maneuvers-card.md

## 1. 总体架构

```
WsfDeltaVOrbitalManeuver (瞬时 Delta-V 机动 — 速度脉冲)
  ├─ SetDeltaV(v)           — 设置 ΔV 矢量 (m/s, 在指定坐标系)
  └─ Execute(state)         — 施加脉冲: v_post = v_pre + Δv

ChangeEccentricity  — 偏心率变更（远地点切向脉冲）
ChangeInclination   — 倾角变更（节点处面外脉冲）
ChangeRAAN          — RAAN 变更（利用 J2 进动差速）

WsfOrbitalManeuversTarget (交会/拦截瞄准)
  ├─ SetComputeForRendezvous()  — 调用 Lambert 求解器
  └─ ComputeOptimalManeuver()   — 最小化 Δv_total
```

## 2. 核心接口

```cpp
// 瞬时 Delta-V 机动
class WsfDeltaVOrbitalManeuver {
public:
    void SetDeltaV(const UtVec3d& aDV, ReferenceFrame aFrame);
    // aFrame: LVLH (V-bar/R-bar/H-bar), NTW, ECI

    void Execute(ut::OrbitalState& aState);
    // aState.velocity += Δv (经坐标系转换)
};

// 交会瞄准 — 使用 Lambert 求解器
class WsfOrbitalManeuversTarget {
public:
    void SetComputeForRendezvous(const ut::OrbitalState& aTargetState,
                                  double aTimeOfFlight);
    // 内部调用 Lambert 求解器确定 Δv1, Δv2
    UtVec3d GetDepartureDeltaV() const;
    UtVec3d GetArrivalDeltaV() const;
};
```

## 3. 框架依赖解耦

| 原始依赖 | 替换方案 |
|----------|----------|
| `ut::OrbitalState` | 自定义 OrbitalState (r, v, epoch) |
| `WsfOrbitalDynamicsTerm` | 移除 — 机动不是动力学项 |
| `UtOrbitalPropagatorBase` | 自定义 IPropagator 接口 |
