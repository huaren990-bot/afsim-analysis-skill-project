# NASA 碎片解体模型 — 接口规格

> **日期:** 2026-06-11 | **状态:** draft | **对应算法卡:** space-nasa-breakup-model-card.md

## 1. 总体架构

```
WsfSatelliteBreakupModel (基类)
  └─ WsfNASA_BreakupModel (NASA 标准模型)
       ├─ ExplosiveBreakup()      — 爆炸解体
       ├─ CollisionalBreakup()    — 碰撞解体
       ├─ ExplosionN()            — 爆炸碎片数幂律 (math)
       ├─ CollisionN()            — 碰撞碎片数幂律 (math)
       ├─ ComputeCollisionMass()  — 碰撞质量计算 (math)
       ├─ AoverM_Spacecraft()     — 航天器面质比
       ├─ AoverM_RocketBody()     — 火箭体面质比
       ├─ DeltaV_Explosion()      — 爆炸 ΔV 分布
       ├─ DeltaV_Collision()      — 碰撞 ΔV 分布
       └─ EnsureMomentumConservation() — 动量守恒修正

Fragment: {position, velocity, mass, areaToMassRatio, characteristicLength}
```

## 2. 核心接口

```cpp
struct Fragment {
    UtVec3d mLocation;   // ECI 位置 (m)
    UtVec3d mVelocity;   // ECI 速度 (m/s)
    double  mMass;       // 质量 (kg)
    double  mAoverM;     // 面质比 (m²/kg)
    double  mLc;         // 特征长度 (m)
};

class WsfNASA_BreakupModel {
public:
    // 爆炸解体: 输入母体平台+参数, 生成碎片云
    bool ExplosiveBreakup(double simTime, const string& platformName,
                          const vector<double>& params);

    // 碰撞解体: 输入两母体+参数
    bool CollisionalBreakup(double simTime,
                            const string& target, const vector<double>& targetParams,
                            const string& impactor, const vector<double>& impactorParams);

    size_t   GetFragmentCount() const;     // 碎片总数
    Fragment GetFragment(size_t i) const;   // 获取第 i 个碎片

    // NASA 模型参数
    void SetExplosionS_Factor(double s);    // 爆炸缩放因子 [0.1, 1.0]
    void SetLargeFragmentMassFraction(double f); // 大碎片质量占比 [0, 1]
    void SetMinFragmentSize(double s);      // 最小碎片尺寸 (m)
    void SetModeledAsSpacecraft(bool b);    // 航天器 vs 火箭体
};
```

## 3. 典型调用

```cpp
WsfNASA_BreakupModel model(simulation);
model.SetModeledAsSpacecraft(true);
model.SetMinFragmentSize(0.1);  // 10 cm 最小碎片
model.ExplosiveBreakup(simTime, "target_sat", params);
for (size_t i = 0; i < model.GetFragmentCount(); i++) {
    Fragment frag = model.GetFragment(i);
    // 将碎片添加到仿真中
}
```

## 4. 框架依赖解耦

| 原始依赖 | 替换方案 |
|----------|----------|
| `WsfPlatform` / `WsfSimulation` | 自定义 `Satellite` / `Simulation` 对象 |
| `UtVec3d` | `Eigen::Vector3d` |
| `WsfObject` / `WsfScenario` | 移除，用构造函数参数替代 |
