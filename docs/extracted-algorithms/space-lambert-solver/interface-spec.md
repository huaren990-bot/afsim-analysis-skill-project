# Lambert 求解器 + 轨道确定 — 接口规格

> **日期:** 2026-06-11 | **状态:** draft | **对应算法卡:** space-lambert-solver-card.md

## 1. 总体架构

```
WsfOrbitDeterminationFusion (轨道确定融合策略)
  ├─ AnglesOnlyInitialGuess()   — 仅角度初轨确定（圆轨道假设）
  ├─ AnglesOnlyKinematicSolution() — 运动学迭代求解
  ├─ ComputeLambertf_g()        — Lambert f/g 级数展开
  ├─ ComputeVelocities()        — 从位置计算速度
  ├─ ComputeCircularLocationsAndSpeeds() — 圆轨道几何解
  └─ CreateFilterOnTrack()      — 建立 Kalman 滤波器跟踪
```

## 2. 核心接口

```cpp
// Lambert f/g 函数计算 (math 标记)
void ComputeLambertf_g(const UtVec3d& aLocECI, const UtVec3d& aVelECI,
                       double aDeltaT, double& aF, double& aG);
// 从 ECI 位置/速度计算 Lagrange f/g 系数

// 速度求解 (math 标记)
void ComputeVelocities(const MeasurementList& aData,
                       const std::vector<UtVec3d>& aLocECI,
                       std::vector<UtVec3d>& aVelECI);
// 使用 Lambert 方法从位置+飞行时间求解速度

// 仅角度初始猜测
bool AnglesOnlyInitialGuess(const UtVec3d& aUnitTargetVecECI_1,
                            const UtVec3d& aSiteLocECI_1,
                            const UtVec3d& aUnitTargetVecECI_2,
                            const UtVec3d& aSiteLocECI_2,
                            double aDt, UtVec3d& aLocECI_1, UtVec3d& aLocECI_2);
```

## 3. 框架依赖解耦

| 原始依赖 | 替换方案 |
|----------|----------|
| `UtVec3d` | `Eigen::Vector3d` |
| `WsfMeasurement` / `WsfTrack` | 自定义测量/航迹结构体 |
| `WsfKalmanFilter` | 自定义 Kalman 滤波器 |
