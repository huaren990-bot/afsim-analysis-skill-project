# 大气密度模型 — 接口规格

> **日期:** 2026-06-11 | **状态:** draft | **对应算法卡:** space-atmosphere-model-card.md

## 1. 总体架构

```
Atmosphere (抽象基类)
  ├─ PiecewiseExponentialAtmosphere  — 分段指数大气
  └─ JacchiaRobertsAtmosphere        — Jacchia-Roberts 大气
       ↓ 作为 WsfOrbitalDynamicsTerm
  AtmosphericDragTerm::ComputeAcceleration(mass, t, r, v) → Vec3d
```

## 2. 核心接口

```cpp
class Atmosphere {
public:
    virtual double GetDensity(double aAltitude_m, const UtCalendar& aTime) const = 0;
    // 返回指定高度和时刻的大气密度 (kg/m³)
};

// 分段指数大气
class PiecewiseExponentialAtmosphere : public Atmosphere {
    // 按高度分多段，每段: ρ(h) = ρ_ref * exp(-(h - h_ref) / H)
};

// Jacchia-Roberts 大气
class JacchiaRobertsAtmosphere : public Atmosphere {
    // 输入: F10.7 太阳辐射通量, Kp 地磁指数
    // 输出: 修正后的高层大气密度
};

// 大气阻力动力学项
class AtmosphericDragTerm : public WsfOrbitalDynamicsTerm {
    // a_drag = -0.5 * (Cd * A / m) * ρ * |v_rel| * v_rel
};
```

## 3. 框架依赖解耦

| 原始依赖 | 替换方案 |
|----------|----------|
| `Atmosphere` 基类 | 自定义 `IAtmosphere::GetDensity(h, t)` |
| `WsfOrbitalDynamicsTerm` | 自定义 `IForceModel` 接口 |
| `UtCalendar` | `double` (从 epoch 起的秒数) |
