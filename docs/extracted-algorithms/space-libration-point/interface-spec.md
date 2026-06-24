# 拉格朗日点计算 — 接口规格

> **日期:** 2026-06-11 | **状态:** draft | **对应算法卡:** space-libration-point-card.md

## 1. 总体架构

```
WsfLibrationPoint
  ├─ ComputeGamma()        — Gamma 系数 (math: 五次方程 Newton 求解)
  ├─ GetL1_Position()      — L1 点位置
  ├─ GetL2_Position()      — L2 点位置
  ├─ GetL3_Position()      — L3 点位置
  ├─ GetL4_Position()      — L4 三角点 (领先 60°)
  ├─ GetL5_Position()      — L5 三角点 (落后 60°)
  └─ ComputeHaloOrbit()    — Halo/Lissajous 轨道计算
```

## 2. 核心接口

```cpp
class WsfLibrationPoint {
public:
    // 构造: primary=主天体(地球), secondary=次天体(月球或太阳)
    WsfLibrationPoint(const CentralBody& aPrimary, const CentralBody& aSecondary);

    // Gamma 系数计算 (math 标记)
    double ComputeGamma(int aPointIndex) const;
    // aPointIndex: 1=L1, 2=L2, 3=L3
    // 使用 Newton 迭代法求解五次方程

    // 拉格朗日点位置 (ECI, m)
    UtVec3d GetL1_Position(const UtCalendar& aTime) const;
    UtVec3d GetL2_Position(const UtCalendar& aTime) const;
    UtVec3d GetL3_Position(const UtCalendar& aTime) const;
    UtVec3d GetL4_Position(const UtCalendar& aTime) const;
    UtVec3d GetL5_Position(const UtCalendar& aTime) const;

    // 质量比
    double GetMu() const { return mMassRatio; }

private:
    double mMassRatio;  // μ = m2 / (m1 + m2)
};
```

## 3. 框架依赖解耦

| 原始依赖 | 替换方案 |
|----------|----------|
| `CentralBody` / `UtCalendar` | 天体星历数据 (JPL DE 系列或解析公式) |
| `UtVec3d` | `Eigen::Vector3d` |
| Newton 迭代 | 标准 C++ `<cmath>` + 自定义收敛循环 |
