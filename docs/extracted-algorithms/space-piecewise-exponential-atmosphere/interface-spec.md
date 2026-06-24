# 分段指数大气密度模型 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** space-piecewise-exponential-atmosphere-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│       PiecewiseExponentialAtmosphere                 │
│  (分段指数大气密度模型——完全无状态)                     │
├──────────────────────────────────────────────────────┤
│  + GetDensity(epoch, lla) → double (kg/m³)          │
│  - mTable: static const array<Row, 28> (分段数据表)  │
└──────────┬───────────────────────────────────────────┘
           │ 继承自
           ▼
┌──────────────────────────────────────────────────────┐
│              Atmosphere (抽象基类)                    │
│  + GetDensity(epoch, lla) → double = 0 (纯虚)       │
│  + ProcessInput(input) → bool                        │
│  - mCentralBodyPtr (中心天体指针，默认 EarthEGM96)     │
└──────────────────────────────────────────────────────┘
           │ 被调用者
           ▼
┌──────────────────────────────────────────────────────┐
│        WsfAtmosphericDragTerm                         │
│  (大气阻力项——密度消费者)                              │
│  ├─ ComputeAcceleration()                            │
│  └─ 使用 GetDensity() 获取 ρ，代入阻力公式            │
└──────────────────────────────────────────────────────┘
```

架构极其简单：`PiecewiseExponentialAtmosphere` 继承自 `Atmosphere` 抽象基类，重写 `GetDensity()` 方法。模型完全无状态（stateless），每次调用仅依赖输入的几何高度和编译期静态常量分段表，时间复杂度 O(log 28) = 常数级。

## 2. 核心接口定义

### 2.1 Row（分段表单行数据——内部数据结构）

```cpp
// 分段大气表中单行的三个参数，对应 Vallado Table 8-4 的一行
struct Row {
    Row(double aBaseHeight, double aScaleHeight, double aBaseDensity);

    double mBaseHeight;   // 该段的底边界高度（基准高度），单位：km
    double mScaleHeight;  // 该段的标高（scale height），密度衰减到 1/e 所需的高度差，单位：km
    double mBaseDensity;  // 该段底边界处的大气密度（基准密度），单位：kg/m³
};
```

### 2.2 分段表（mTable——28 段静态常量数组）

```cpp
// 28 段分段大气数据表，来源于 Vallado Table 8-4 (p.567)
// 所有实例共享同一份编译期常量数据
// 按 mBaseHeight 升序排列
static const std::array<Row, 28> mTable;
```

**28 段完整数据**：

| 段序号 | 基准高度 (km) | 标高 (km) | 基准密度 (kg/m³) |
|--------|--------------|----------|-------------------|
| 0 | 0.0 | 7.249 | 1.225 |
| 1 | 25.0 | 6.349 | 3.899e-2 |
| 2 | 30.0 | 6.682 | 1.774e-2 |
| 3 | 40.0 | 7.554 | 3.972e-3 |
| 4 | 50.0 | 8.382 | 1.057e-3 |
| 5 | 60.0 | 7.714 | 3.206e-4 |
| 6 | 70.0 | 6.549 | 8.770e-5 |
| 7 | 80.0 | 5.799 | 1.905e-5 |
| 8 | 90.0 | 5.382 | 3.396e-6 |
| 9 | 100.0 | 5.877 | 5.297e-7 |
| 10 | 110.0 | 7.263 | 9.661e-8 |
| 11 | 120.0 | 9.473 | 2.438e-8 |
| 12 | 130.0 | 12.636 | 8.484e-9 |
| 13 | 140.0 | 16.149 | 3.845e-9 |
| 14 | 150.0 | 22.523 | 2.070e-9 |
| 15 | 180.0 | 29.740 | 5.464e-10 |
| 16 | 200.0 | 37.105 | 2.789e-10 |
| 17 | 250.0 | 45.546 | 7.248e-11 |
| 18 | 300.0 | 53.628 | 2.418e-11 |
| 19 | 350.0 | 53.298 | 9.518e-12 |
| 20 | 400.0 | 58.515 | 3.725e-12 |
| 21 | 450.0 | 60.828 | 1.585e-12 |
| 22 | 500.0 | 63.822 | 6.967e-13 |
| 23 | 600.0 | 71.835 | 1.454e-13 |
| 24 | 700.0 | 88.667 | 3.614e-14 |
| 25 | 800.0 | 124.64 | 1.170e-14 |
| 26 | 900.0 | 181.05 | 5.245e-15 |
| 27 | 1000.0 | 268.00 | 3.019e-15 |

### 2.3 GetDensity（密度查询——核心算法接口）

```cpp
// 根据几何高度查询大气密度
// 该模型不依赖纬度、经度、时间——仅使用高度
//
// 参数：
//   aEpoch - 查询时刻（本模型未使用该参数，仅保持接口统一），类型：const UtCalendar&
//   aLLA   - 经纬度高度位置对象，本模型仅使用其中的几何高度
// 返回：当前高度处的大气密度，单位：kg/m³
//
// 算法步骤（共 5 步，仅约 5 行核心代码）：
//   1. 提取几何高度 aLLA.GetAlt()，单位：m
//   2. 转为 km 并钳位：altKm = max(高度_m / 1000.0, 0.0)
//      （负高度钳位为 0 km，对应海平面）
//   3. 二分查找：std::upper_bound 找到第一个基准高度 > altKm 的行
//   4. 前移一位得到 altKm 实际所在分段
//   5. 计算指数衰减：ρ = ρ_ref * exp(-(altKm - h_ref) / H)
double GetDensity(const UtCalendar& aEpoch, const UtLLAPos& aLLA) const override;
```

### 2.4 Atmosphere（抽象基类——接口契约）

```cpp
// 大气模型的抽象基类，定义了所有大气密度模型必须实现的接口
class Atmosphere : public WsfObject {
public:
    // 纯虚函数：子类必须重写
    // 参数：aEpoch - 查询时刻（可为绝对历元），aLLA - 经纬度高度位置
    // 返回：大气密度 (kg/m³)
    virtual double GetDensity(const UtCalendar& aEpoch, const UtLLAPos& aLLA) const = 0;

    // 虚函数：处理脚本输入命令（如 central_body 命令）
    virtual bool ProcessInput(UtInput& aInput);

protected:
    const UtCentralBody* mCentralBodyPtr;  // 中心天体指针（默认 EarthEGM96）
};
```

## 3. 典型调用模式

```cpp
// ============================================================
// 1. 创建模型实例
// ============================================================
PiecewiseExponentialAtmosphere atmosphere;  // 构造时自动设置 cTYPE 标识

// ============================================================
// 2. 查询特定高度的大气密度
// ============================================================
UtCalendar epoch;      // 时间纪元（本模型不使用，可传入任意值）
UtLLAPos lla;           // 经纬度高度位置
lla.SetAlt(200000.0);   // 设置几何高度为 200 km（单位：m）

double rho = atmosphere.GetDensity(epoch, lla);
// rho ≈ 2.789e-10 kg/m³（使用第 16 段：基准高度 200 km，基准密度 2.789e-10 kg/m³）

// ============================================================
// 3. 查询不同高度的密度（常见使用场景）
// ============================================================
// 海平面 (h = 0 m)：
lla.SetAlt(0.0);
rho = atmosphere.GetDensity(epoch, lla);  // → 1.225 kg/m³

// 100 km：
lla.SetAlt(100000.0);
rho = atmosphere.GetDensity(epoch, lla);  // → 5.297e-7 kg/m³

// 500 km：
lla.SetAlt(500000.0);
rho = atmosphere.GetDensity(epoch, lla);  // → 6.967e-13 kg/m³

// 负高度（钳位到 0 km）：
lla.SetAlt(-1000.0);
rho = atmosphere.GetDensity(epoch, lla);  // → 1.225 kg/m³（钳位后使用第 0 段）

// > 1000 km（使用最后一段外推）：
lla.SetAlt(1500000.0);  // 1500 km
rho = atmosphere.GetDensity(epoch, lla);  // 使用第 27 段继续外推，密度极低

// ============================================================
// 4. 在大气阻力计算中的调用（由 WsfAtmosphericDragTerm 执行）
// ============================================================
// double rho = mAtmospherePtr->GetDensity(simTime, llaPos);
// double dragAccel = -0.5 * (Cd * A / mass) * rho * v_rel^2;
```

## 4. 坐标系与单位约定

此模型不涉及坐标系变换。仅使用一维几何高度。

| 物理量 | 输入/内部单位 | 输出单位 |
|--------|-------------|----------|
| 几何高度（输入） | m（通过 `aLLA.GetAlt()` 获取） | — |
| 几何高度（内部查表） | km（输入值 / 1000.0） | — |
| 基准高度（表中） | km | — |
| 标高（表中） | km | — |
| 基准密度（表中） | kg/m³ | — |
| 大气密度（输出） | — | kg/m³ |

## 5. 框架依赖解耦

| AFSIM 原始依赖 | 职责 | 替换方案 |
|---------------|------|----------|
| `WsfObject` | 基础对象框架（提供 SetType、GetName 等） | 可直接移除（PiecewiseExponentialAtmosphere 的算法逻辑完全不依赖 WsfObject） |
| `Atmosphere` (基类) | 抽象接口定义（GetDensity 纯虚函数） | 自定义 `IAtmosphereModel` 抽象类，仅含 `virtual double GetDensity(...) = 0` |
| `UtLLAPos` | 经纬度高度位置（提供 `GetAlt()` 方法） | 直接用 `double altitude_m` 参数替代 |
| `UtCalendar` | 时间纪元（本模型完全未使用） | 从函数签名中移除该参数 |
| `std::upper_bound`（STL） | 标准库二分查找算法 | 可替换为手写二分查找（约 5 行代码） |
| `std::exp`（STL/C math） | 标准指数函数 | 直接使用，任何语言的数学库均提供 |
| `std::array`（STL） | 静态数组容器 | 可替换为 C 风格数组 `const Row mTable[28]` |
| `WsfAtmosphericDragTerm` | 大气阻力项（密度消费者） | 任何调用 GetDensity 的组件均可，公式为 `a = -0.5·Cd·A·ρ·v²/m` |

> **可移植性评估：极高。** 核心算法仅 5 行代码（二分查找 + 指数衰减），移植到 Python/JavaScript/C/Fortran 等任何语言均可在 20 行以内完成。分段表数据 (28 行 x 3 列) 可直接硬编码。
