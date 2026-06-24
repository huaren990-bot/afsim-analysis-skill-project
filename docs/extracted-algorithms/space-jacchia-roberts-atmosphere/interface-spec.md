# Jacchia-Roberts 大气密度模型 — 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** space-jacchia-roberts-atmosphere-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────┐
│         JacchiaRobertsAtmosphere                      │
│  (Jacchia-Roberts 1977 大气密度模型)                    │
├──────────────────────────────────────────────────────┤
│  公共接口                                            │
│  + GetDensity(epoch, lla) → double (kg/m³)          │
│  + ProcessInput(input) → bool                        │
│  + Get/SetAverageSolarFlux()  (F10.7a)               │
│  + Get/SetSolarFlux()         (F10.7)                │
│  + Get/SetGeomagneticIndex()  (Kp)                   │
│                                                      │
│  内部核心计算链                                       │
│  - JacchiaRoberts(lla, epoch) → density (g/m³)       │
│    ├─ Exotherm(lla, sunDec, solarLon) → T (K)       │
│    ├─ Rho100(heightKm, T) → density (g/m³)          │
│    ├─ Rho125(heightKm, T) → density (g/m³)          │
│    ├─ RhoHigh(heightKm, T, T500, sunDec, lat)       │
│    └─ RhoCorrection(heightKm, a1Time, lat)          │
│  - Roots(a[], na, croots[][2], irl) (Newton求根)     │
│  - DeflatePolynomial(a[], n, root, anew[])           │
│                                                      │
│  mutable 中间状态（缓存，提升效率）                     │
│  - mRoot1, mRoot2, mX_Root, mY_Root                  │
│  - mTinfinity, mTx, mSum, mX_Temp                    │
│  - mLowAltWarned                                     │
└──────────┬───────────────────────────────────────────┘
           │ 继承自
           ▼
┌──────────────────────────────────────────────────────┐
│              Atmosphere (抽象基类)                    │
│  + GetDensity(epoch, lla) → double = 0               │
│  - mCentralBodyPtr (中心天体，用于获取椭球参数)         │
└──────────────────────────────────────────────────────┘
```

模型从 GMAT R2018a 移植，实现 Jacchia 1977 模型族。核心思想：太阳 EUV 辐射（以 F10.7 代理）和地磁活动（以 Kp 代理）决定外球温度 T_inf，T_inf 驱动高层大气温度剖面，温度剖面通过气压测高方程导出密度剖面，再施加各种修正因子（太阳活动、地磁活动、季节-纬度、日变化、半年周期）。

## 2. 核心接口定义

### 2.1 配置参数（F10.7 与 Kp —— 太阳/地磁活动输入）

```cpp
// 这些是 Jacchia-Roberts 模型的核心空间天气输入参数
// 通过脚本命令（solar_flux / average_solar_flux / geomagnetic_index）或 setter 方法设置

double mF107a{150.0};  // 81 天平均太阳 10.7 cm 辐射通量，单位：sfu（1 sfu = 10^-22 W/(m^2·Hz)）
                       // 默认值 150.0 对应平静期太阳
double mF107{150.0};   // 前一日瞬时太阳 10.7 cm 辐射通量，单位：sfu
                       // 默认值 150.0
double mKp{0.0};       // 地磁活动指数 Kp，取值范围 [0, 9]
                       // 默认值 0.0 对应地磁平静；输入时强制校验 [0, 9] 范围

// 对应的公共访问接口：
double GetAverageSolarFlux() const;        // 获取 F10.7a
double GetSolarFlux() const;              // 获取 F10.7
double GetGeomagneticIndex() const;       // 获取 Kp
void SetAverageSolarFlux(double aF107a);  // 设置 F10.7a
void SetSolarFlux(double aF107);          // 设置 F10.7
void SetGeomagneticIndex(double aKp);     // 设置 Kp
```

### 2.2 mutable 中间状态变量（缓存计算结果）

```cpp
// 以下成员变量在密度计算过程中被计算并缓存，标记为 mutable
// 使得 const 成员函数 GetDensity() 也能更新它们（逻辑上不改变对象外部可见状态）

mutable double mRoot1{};      // 温度多项式的第一个实根（高度 < 125 km 时 Newton 迭代求解）
mutable double mRoot2{};      // 温度多项式的第二个实根（经 DeflatePolynomial 缩减法求解）
mutable double mX_Root{};     // 缩减法后复数根的实部（用于 Rho100/Rho125 多项式分解）
mutable double mY_Root{};     // 缩减法后复数根的虚部绝对值（用于 Rho100 的 atan 项）
mutable double mTinfinity{};  // 外球温度 T∞ (K)，高层大气温度剖面的渐近值——密度计算核心驱动量
mutable double mTx{};         // 125 km 高度处温度 T_x (K)，温度 profile 过渡参考点
mutable double mSum{};        // 温度多项式当前值 (K)，构造牛顿求根多项式时使用
mutable double mX_Temp{};     // 太阳加热项 T_x = 379 + 3.24·F10.7a + 1.3·(F10.7 - F10.7a) (K)
mutable bool mLowAltWarned{false};  // 低于 100 km 首次调用警告标志（防止重复日志输出）
```

### 2.3 GetDensity（密度查询——公共入口）

```cpp
// Jacchia-Roberts 大气密度模型的公共入口
// 根据几何高度、时间（用于太阳位置计算）以及预设的空间天气参数计算大气密度
//
// 参数：
//   aEpoch - 查询历元（用于计算太阳赤经/赤纬/黄经），类型：const UtCalendar&
//   aLLA   - 经纬度高度位置，本模型使用高度、纬度和经度
// 返回：大气密度，单位：kg/m³（内部以 g/m³ 计算，返回时乘以 1000）
//
// 高度处理（边界条件）：
//   height_km <= 0.0   → 返回 cRHO_ZERO * 1000 (3.46e-3 g/m^3 即 3.46e-6 kg/m^3)
//   height_km <= 100.0 → 首次打印警告 "模型适用于 100 km 以上"
//   height_km > 0.0    → 调用 JacchiaRoberts() 核心计算
double GetDensity(const UtCalendar& aEpoch, const UtLLAPos& aLLA) const override;
```

### 2.4 ProcessInput（脚本输入处理）

```cpp
// 处理 AFSIM 脚本中的配置命令
// 支持三个输入命令：
//   solar_flux <value>          —— 设置 F10.7（必须 > 0）
//   average_solar_flux <value>  —— 设置 F10.7a（必须 > 0）
//   geomagnetic_index <value>   —— 设置 Kp（必须在 [0, 9] 闭区间）
// 其他命令委托给基类 Atmosphere::ProcessInput()（如 central_body 命令）
bool ProcessInput(UtInput& aInput) override;
```

### 2.5 JacchiaRoberts（核心密度计算——私有方法）

```cpp
// 内部核心入口：根据高度分段调用不同的密度计算函数
// 返回单位为 g/m³（在 GetDensity 中乘以 1000 转为 kg/m³）
//
// 高度分段策略：
//   height_km <= 90.0    → 返回常量 cRHO_ZERO (3.46e-6 g/m³)
//   height_km < 100.0    → Exotherm() + Rho100()（温度多项式 Newton 求根 + 系数展开）
//   height_km <= 125.0   → Exotherm() + Rho125()（含 5 种大气组分密度求和）
//   height_km <= 2500.0  → Exotherm() + RhoHigh()（含 H 组分，>500 km 时启用）
//   height_km > 2500.0   → 返回 0.0
// 所有高度 > 90 km 的结果均乘以 RhoCorrection()（地磁/季节-纬度/半年周期修正）
double JacchiaRoberts(const UtLLAPos& aLLA, const UtCalendar& aEpoch) const;
```

### 2.6 Exotherm（外球温度计算——私有方法）

```cpp
// 计算给定高度处的大气温度 (K)，并缓存多项中间变量（mRoot1/2, mX_Root, mY_Root, mTinfinity, mTx, mSum）
//
// 主要计算步骤：
//   1. 计算太阳时角 hourAngle = lon - solarLon
//   2. 计算 theta = 0.5·|lat + sunDec|, eta = 0.5·|lat - sunDec|
//   3. 计算 tau = hourAngle - 0.64577... + 0.10472...·sin(hourAngle + 0.75049...)
//      tau 钳位到 [-π, π]
//   4. 计算太阳位置依赖温度项 t1（含 sin²·²(theta) 和 cos(eta) 复杂项）
//   5. 计算外球温度 mTinfinity：
//      - alt_km < 200:  Tinf = t1 + 14·Kp + 0.02·exp(Kp)
//      - alt_km >= 200: Tinf = t1 + 28·Kp + 0.03·exp(Kp)
//   6. 计算 125 km 处温度 mTx = 371.6678 + 0.0518806·Tinf - 294.3505·exp(-0.00216222·Tinf)
//   7. 计算当前高度温度：
//      - alt_km < 125: 使用 cCON_C 多项式 + Newton 求根 (Roots)
//      - alt_km == 125: T = mTx
//      - alt_km > 125: 使用 cCON_L 多项式 + 指数衰减从 mTx 过渡到 mTinfinity
double Exotherm(const UtLLAPos& aLLA, double aSunDec, double aSolarLon) const;
```

### 2.7 Rho100 / Rho125 / RhoHigh（分高度段密度计算——私有方法）

```cpp
// [90, 100) km 段密度计算
// 使用温度多项式求根结果 (mRoot1/2, mX_Root, mY_Root)
// 通过极半径、多项式值和对数展开计算基准密度剖面
// 参数：aHeightKm - 高度 (km)，aTemperature - 当前高度温度 (K)
// 返回：密度 (g/m³)
double Rho100(double aHeightKm, double aTemperature) const;

// [100, 125] km 段密度计算
// 对 5 种大气组分 (N2, Ar, He, O2, O) 分别计算密度并求和
// 使用各组分分子量和数量密度数据
// He 组分有 -0.38 的指数修正
// 返回：各组分密度之和 (g/m³)
double Rho125(double aHeightKm, double aTemperature) const;

// (125, 2500] km 段密度计算
// 对 6 种大气组分 (N2, Ar, He, O2, O, H) 分别计算
// 每个组分的密度 = f * cMOL_MASS[i] * di * (mTx/T)^exp1 * ((Tinf-T)/(Tinf-mTx))^gamma
// H 组分仅在 height > 500 km 时计算
// He 组分有非平凡的赤纬/纬度修正因子 f
// 返回：各组分密度之和 (g/m³)
double RhoHigh(double aHeightKm, double aTemperature, double aT_500,
               double aSunDec, double aGeoLat) const;
```

### 2.8 RhoCorrection（密度修正因子——私有方法）

```cpp
// 对基准密度施加三类修正，返回修正因子（10 的幂次形式）
//
// 三类修正：
//   1. 地磁活动修正 (geoCor)：
//      - height < 200 km: geoCor = 0.012·Kp + 0.000012·exp(Kp)
//      - height >= 200 km: geoCor = 0.0（高层由温度剖面单独处理）
//   2. 半年周期修正 (semianCor)：基于 A.1 时间系统的日数计算
//      包含复杂的 sin/cos/pow 组合项
//   3. 季节-纬度修正 (slatCor)：
//      slatCor = 0.014·(h-90)·sin(Lat)*|sin(Lat)|·sin(2π·day+1.72)·exp(-0.0013·(h-90)^2)
//
// 参数：aHeightKm - 高度 (km)，aA1_Time - A.1 时间系统日期，aGeoLat - 地心纬度 (rad)
// 返回：10^(geoCor + semianCor + slatCor)
double RhoCorrection(double aHeightKm, double aA1_Time, double aGeoLat) const;
```

### 2.9 Roots / DeflatePolynomial（多项式求根工具——静态私有方法）

```cpp
// Newton 迭代法求多项式实根（支持复数初值）
// 收敛判据：迭代中实部和虚部的相对变化量之和 <= 1.0e-14
// 参数：
//   aA[]     - 多项式系数数组（按降幂排列）
//   aNa      - 系数个数
//   aCroots[][] - 根数组（[i][0]=实部, [i][1]=虚部），输入时含初值，输出时为结果
//   aIrl     - 要求解的根的个数
static void Roots(double aA[], int aNa, double aCroots[][2], int aIrl);

// 多项式缩减法：用已知根 aRoot 降低多项式阶数
// 新多项式系数存入 aCnew[]（长度为 aN-1）
// 等价于多项式除以 (x - aRoot)
static void DeflatePolynomial(double aC[], int aN, double aRoot, double aCnew[]);
```

### 2.10 物理常量（匿名命名空间中的 const/constexpr）

```cpp
// 以下常量定义于 WsfJacchiaRobertsAtmosphere.cpp 的匿名命名空间

constexpr double cRHO_ZERO = 3.46e-6;       // 低层大气恒定密度 (g/m³)
constexpr double cT_ZERO = 183.0;           // 90 km 高度处温度 (K)
const double cG_ZERO = 9.80665;             // 海平面重力加速度 (m/s²)
const double cGAS_CON = 8.31432;            // 普适气体常数 (J/(K·mol))
constexpr double cN_AVOGADRO = 6.022045e23; // 阿伏伽德罗常数

// 大气组分分子量 (g/mol)
const double cMOL_MASS[6] = {
    28.0134,   // N2 - 氮气
    39.948,    // Ar - 氩气
    4.0026,    // He - 氦气
    31.9988,   // O2 - 分子氧
    15.9994,   // O  - 原子氧
    1.00797    // H  - 氢
};

// 温度多项式的系数表 (cCON_C[5])、外球温度系数表 (cCON_L[5])
// Rho100 中使用的 M(z) 系数（7 项）、S(z) 系数（6 项）、S_beta 系数（6 项）
// Rho125 中使用的 zeta 系数（7 项）、数量密度数据（5 组分）
// RhoHigh 中使用的密度对数系数 cCON_DEN[5][7]（5 组分 x 7 系数）
// （以上大量经验系数表均硬编码于源文件中，移植时需完整复制）
```

## 3. 典型调用模式

```cpp
// ============================================================
// 1. 创建模型实例 + 设置空间天气参数
// ============================================================
JacchiaRobertsAtmosphere atmosphere;

// 方式一：通过 setter 设置
atmosphere.SetAverageSolarFlux(140.0);   // F10.7a = 140 sfu（中等太阳活动）
atmosphere.SetSolarFlux(150.0);          // F10.7 = 150 sfu（瞬时值）
atmosphere.SetGeomagneticIndex(3.0);     // Kp = 3（轻微地磁扰动）

// 方式二：通过脚本命令设置（由 ProcessInput 解析）
//   脚本中写：solar_flux 150.0
//            average_solar_flux 140.0
//            geomagnetic_index 3.0

// ============================================================
// 2. 查询特定位置和时间的密度
// ============================================================
UtCalendar epoch;        // 查询历元（影响太阳位置计算）
UtLLAPos lla;
lla.SetAlt(400000.0);    // 高度 400 km（单位：m），这是 JR 模型的典型适用范围

double rho = atmosphere.GetDensity(epoch, lla);  // 返回 kg/m³

// ============================================================
// 3. 不同太阳活动水平的对比
// ============================================================

// 太阳活动平静期（F10.7 = 70，太阳极小）：
atmosphere.SetSolarFlux(70.0);
atmosphere.SetAverageSolarFlux(70.0);
double rho_quiet = atmosphere.GetDensity(epoch, lla);

// 太阳活动活跃期（F10.7 = 250，太阳极大）：
atmosphere.SetSolarFlux(250.0);
atmosphere.SetAverageSolarFlux(250.0);
double rho_active = atmosphere.GetDensity(epoch, lla);
// rho_active 可能是 rho_quiet 的 10~100 倍

// ============================================================
// 4. 在大气阻力计算中的典型调用（由 WsfAtmosphericDragTerm 执行）
// ============================================================
// double rho = mAtmospherePtr->GetDensity(simTime, llaPos);
// double dragAccel = -0.5 * (Cd * A / mass) * rho * v_rel^2;
```

## 4. 坐标系与单位约定

| 坐标系/参考系 | 用途 |
|-------------|------|
| **LLA (Lat/Lon/Alt)** | 输入位置（地心纬度 + 经度 + 几何高度），纬度/经度影响太阳时角、季节-纬度修正 |
| **ECI (J2000 赤道惯性系)** | 太阳赤经/赤纬计算（由 UtSun 提供） |
| **极半径** | 由中心天体椭球 (`mCentralBodyPtr->GetEllipsoid()`) 提供，用于多项式中的极半径相关项 |

**单位约定**：

| 物理量 | 单位 | 备注 |
|--------|------|------|
| 几何高度（输入） | m（通过 `aLLA.GetAlt()` 获取） | 内部转换为 km |
| 几何高度（内部计算） | km | 用于分段判断和多项式计算 |
| 纬度/经度（输入） | 度 | 通过 `aLLA.GetLat()/GetLon()` 获取 |
| 纬度（内部计算） | rad | 乘以 `cRAD_PER_DEG` 转换 |
| 太阳赤纬/赤经 | rad | 由 `UtSun::GetSunLocationRA_Dec()` 返回 |
| 太阳黄经 | rad | 由 `UtSun::GetSunLongitude()` 返回 |
| 温度 | K | 所有温度均为开尔文 |
| 密度（内部） | g/m³ | JacchiaRoberts() 内部返回 g/m³ |
| 密度（输出） | kg/m³ | GetDensity() 返回 kg/m³（乘以 1000） |
| F10.7 太阳通量 | sfu | 1 sfu = 10^(-22) W/(m^2·Hz) |
| Kp 地磁指数 | 无量纲 | 范围 [0, 9] |
| 时间（A.1 系统） | 儒略日 | 用于半年周期和季节-纬度修正 |

## 5. 框架依赖解耦

| AFSIM 原始依赖 | 职责 | 替换方案 |
|---------------|------|----------|
| `WsfObject` / `Atmosphere` (基类) | 基础对象框架 + 密度查询接口 | 自定义 `IAtmosphereModel` 抽象类，仅含 `GetDensity` 纯虚函数 |
| `UtLLAPos` | 经纬度高度位置对象 | 自定义 `GeoPosition` 结构体：`{double lat_deg, lon_deg, alt_m}` |
| `UtCalendar` | 日历时间（儒略日、DeltaAT 等） | 自定义 `DateTime` 类（含儒略日和 DeltaAT）或直接使用 `double julianDay` |
| `UtSun` | 太阳位置计算（赤经/赤纬/黄经） | 自定义 `SolarPosition` 函数（Meeus 或 Vallado 太阳星历算法） |
| `UtCentralBody / UtCentralBodyEllipsoid` | 中心天体椭球参数（用于极半径计算） | 直接硬编码地球 WGS-84 极半径常量（6356752.314 m） |
| `UtMath` | 常量 `cRAD_PER_DEG`、`cPI`、`cTWO_PI`、`ErrorFunction` | 直接使用 `M_PI`、`M_PI/180.0` 等宏；本模型不使用 ErrorFunction |
| `UtInput` | 脚本输入解析 | 可替换为任意配置系统（JSON/YAML/命令行参数） |
| `UtLog` | 警告日志输出（低高度警告） | 替换为 `printf`、`std::cerr` 或日志库 |
| `UtVec3` | 本模型中未实际使用（仅头文件包含） | 可移除 |
| `std::exp`、`std::log`、`std::pow`、`std::sin`、`std::cos`、`std::sqrt`、`std::fabs`、`std::atan` | 标准数学函数 | 直接使用，任何语言均提供 |
| `WsfAtmosphericDragTerm` | 密度消费者（大气阻力计算） | 任何调用 GetDensity 的组件均可 |

> **可移植性评估：高。** 所有经验系数表为编译期常量，可完整复制。核心数学公式有公开文献支撑（Jacchia 1977, SAO Special Report 375; Vallado Appendix B）。移植工作主要是 (1) 复制大量经验系数表，(2) 实现太阳星历以计算太阳赤经/赤纬/黄经，(3) 实现 Newton 多项式和 DeflatePolynomial。不需要 AFSIM 仿真框架的特殊功能。F10.7 和 Kp 数据需外部观测源或用户输入。
