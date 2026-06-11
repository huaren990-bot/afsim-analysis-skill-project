# 算法卡片 — 太阳终结线与地影分析

> **状态**：draft
> **日期**：2026-06-11
> **索引证据**：function-index.jsonl (Propagate 为空间模块核心函数，地影计算在传播过程中调用)
> **关联文档**：space-integrating-propagator-card.md, space-conjunction-assessment-card.md

### 基础资料

- **算法名称**：Solar Terminator and Eclipse Analysis（太阳终结线与地影分析算法）
- **算法所属模块**：wsf_space（空间/轨道力学模块）
- **算法功能**：判断航天器相对于太阳和地球的照明状态。核心包含三大部分：(1) 天光阶段判别（GetPhaseOfDay）：基于太阳矢量在地面观测点 NED 坐标系中的余弦角，区分白天/黄昏/黑夜，支持民用、航海、天文三种黄昏阈值；(2) 地球遮挡判断（MaskedByHorizon）：通过视线与地球椭球的直线-椭球求交（二次方程求根）判定目标是否被地球遮挡；(3) 全影/半影/光照区判别（GetPlatformSolarIllumination）：以太阳的上下边缘为两个独立光源，分别判断其是否被地球椭球遮挡，从而区分全影（Umbra，上下边缘均被遮挡）、半影（Penumbra，仅下边缘被遮挡）和光照区（Illuminated，上下边缘均可见）。此外，EclipseEventManager 负责在仿真中周期性调度地影事件的检测和报告。

### 算法流程

整个算法流程图如下：

```mermaid
flowchart TD
    A[开始：输入平台/观测点位置与时间] --> B{处理类型？}
    
    B -->|天光阶段判别| C[1. 计算太阳矢量在观测点NED坐标系的向量]
    C --> D[2. 提取Z分量（天顶方向）的负余弦值 cosTheta]
    D --> E{cosTheta > cos90°50′?}
    E -->|是| F[返回：白天 cDAY]
    E -->|否| G{cosTheta > cos(limitDegrees)?}
    G -->|是| H[返回：黄昏 cTWILIGHT]
    G -->|否| I[返回：黑夜 cNIGHT]
    
    B -->|地影分析| J[3. 获取平台WCS位置]
    J --> K[4. 计算太阳上下边缘的WCS视线方向]
    K --> L[5. 分别对上下边缘执行地平线遮挡检查 MaskedByHorizon]
    L --> M{上下边缘均被遮挡?}
    M -->|是| N[返回：全影 cEARTH_UMBRA]
    M -->|否| O{仅下边缘被遮挡?}
    O -->|是| P[返回：半影 cEARTH_PENUMBRA]
    O -->|否| Q{仅上边缘被遮挡?}
    Q -->|是| R[断言失败，不可能仅上边缘被遮挡]
    Q -->|否| S[返回：光照区 cILLUMINATED]

    J --> T[MaskedByHorizon子流程：构造视线椭球求交]
    T --> U[6. 计算视线向量 T-O 及椭球参数 a, b, c]
    U --> V[7. 判別式 discrim = b² - 4ac >= 0?]
    V -->|否| W[视线不穿过地球，未被遮挡]
    V -->|是| X[求根 solnOne, solnTwo]
    X --> Y{solnOne > 容差<br/>且 solnTwo + 容差 < 目标距离?}
    Y -->|是| Z[被地球遮挡]
    Y -->|否| AA[未被遮挡或视线在地表以上]
    
    K --> AB[EclipseEventManager调度循环]
    AB --> AC[8. 轨道传播器计算入影/出影时间 GetEclipseTimes]
    AC --> AD{是否存在地影事件?}
    AD -->|是| AE[安排 ECLIPSE_ENTRY/EXIT 事件至相应时刻]
    AD -->|否| AF[1/4轨道周期后重新评估 cEVALUATE]
    AE --> AG[事件触发时通知观察者，重新计算下一地影时间]
    AF --> AG
```

其中，天光阶段判别（步骤1-2）基于太阳矢量 NED 坐标系中 Z 分量（沿天顶方向）的余弦角与预设阈值比较：$\cos \theta = -\text{太阳方向}_{\text{NED},z}$，$\cos \theta > \cos 90^\circ 50'$（太阳在地平线以下不到 50 角分）为白天；介于白天阈值与自定义黄昏限角之间为黄昏；否则为黑夜。地影分析（步骤3-7）通过直线-椭球二次方程求交判断视线是否穿越地球。EclipseEventManager（步骤8起）利用轨道外推器的 GetEclipseTimes 方法预测入影/出影时刻，并自动调度检测事件。

### 算法变量和常量

#### 输入变量（Input）

| 英文标识符(Symbol) | 中文名称(Name) | 数据类型(Type) | 含义(Meaning) | 单位(Units) | 所属函数(Method) |
| ---- | ---- | ---- | --- | ---- | --- |
| aLatDegrees | 纬度 | double | 地面观测点的地理纬度 | 度 | Propagate |
| aLonDegrees | 经度 | double | 地面观测点的地理经度 | 度 | Propagate |
| aTime | 时间 | UtCalendar& | 需要判断天光阶段的世界协调时 | — | Propagate |
| aLimitDegrees | 黄昏限角 | double | 自定义的黄昏结束角度（默认 96° 为民用黄昏） | 度 | Propagate |
| aObserverWCS[3] | 观测者WCS位置 | const double[3] | 观测者（或航天器）在地心固连坐标系中的位置 | m | Propagate |
| aTargetWCS[3] | 目标WCS位置 | const double[3] | 被观测目标（如太阳边缘点）在地心固连坐标系中的位置 | m | Propagate |
| aPlatformPtr | 平台指针 | WsfPlatform* | 需要判断地影状态的航天器平台 | — | Propagate |
| aSimTime | 仿真时间 | double | EclipseEventManager 被调用时的当前仿真时间 | s | Update |
| aSpaceMover | 空间运动体 | WsfSpaceMoverBase& | 包含轨道外推器的航天器运动体引用 | — | Update |

#### 输出变量（Output）

| 英文标识符(Symbol) | 中文名称(Name) | 数据类型(Type) | 含义(Meaning) | 单位(Units) | 所属函数(Method) |
| ---- | ---- | ---- | --- | ---- | --- |
| retval（GetPhaseOfDay） | 天光阶段 | PhaseOfDay | 枚举值 cDAY（白天）、cTWILIGHT（黄昏）、cNIGHT（黑夜） | — | Propagate |
| retval（MaskedByHorizon） | 是否被遮挡 | bool | true 表示目标被地球地平线遮挡，false 表示可见 | — | Propagate |
| retval（GetPlatformSolarIllumination） | 光照状态 | PlatformSolarIllumination | 枚举值 cILLUMINATED（光照）、cEARTH_PENUMBRA（半影）、cEARTH_UMBRA（全影）、cINVALID_PLATFORM（无效平台） | — | Propagate |
| timeToEntry | 至入影时间 | double | 从当前时刻算起到下一次进入地影的时间 | s | Update |
| timeToExit | 至出影时间 | double | 从当前时刻算起到下一次离开地影的时间 | s | Update |
| solutionExists | 地影事件是否存在 | bool | true 表示下一轨道周期内存在地影穿越事件 | — | Update |

#### 常量（Constant）

| 英文标识符(Symbol) | 中文名称(Name) | 数据类型(Type) | 含义(Meaning) | 单位(Units) | 所属函数(Method) |
| ---- | ---- | ---- | --- | ---- | --- |
| cTWILIGHT_CIVIL | 民用黄昏角度 | constexpr double | 民用黄昏定义（太阳在地平线下 96°） | 度 | Propagate |
| cTWILIGHT_NAUTICAL | 航海黄昏角度 | constexpr double | 航海黄昏定义（太阳在地平线下 102°） | 度 | Propagate |
| cTWILIGHT_ASTRONOMICAL | 天文黄昏角度 | constexpr double | 天文黄昏定义（太阳在地平线下 108°） | 度 | Propagate |
| cCOS_TWILIGHT_BEGIN | 黄昏起始余弦角 | const double | cos(1.5853407372281827 rad) = cos(90°50')，太阳在地平线下 50 角分时黄昏开始 | — | Propagate |
| cMASKED_BY_EARTH_TOLERANCE | 遮挡容差 | constexpr double | 0.05 m，用于判断视线是否恰好穿过地球表面 | m | Propagate |
| UtEarth::cA | 地球椭球赤道半径 | const | 地球 WGS-84 椭球长半轴 | m | Propagate |
| UtEarth::cB | 地球椭球极半径 | const | 地球 WGS-84 椭球短半轴 | m | Propagate |
| UtSun::cMEAN_RADIUS | 太阳平均半径 | const | 太阳平均半径，用于计算太阳边缘位置 | m | Propagate |
| — | 轨道再评估比例 | const | 1/4 轨道周期，用于无地影事件时的重新评估间隔 | — | Update |

### 关键数学公式

1. **天光阶段判别的余弦角计算**：
   天光阶段通过太阳方向矢量在 NED 坐标系中 Z 分量（即天底方向的分量，取负后为天顶方向）的余弦值判定：
   $$\cos \theta = -\hat{\mathbf{s}}_{\text{NED}, z}$$
   其中：
   - $\hat{\mathbf{s}}_{\text{NED}}$ 为太阳方向在 NED（北-东-地）坐标系中的单位矢量。
   - $\cos \theta = 1$ 表示太阳在天顶，$\cos \theta = -1$ 表示太阳在天底。
   - $\cos \theta_{\text{begin}} = \cos 90^\circ 50' = \cos(1.5853407 \text{ rad}) \approx -0.014544$：太阳在地平线下 50 角分，黄昏开始。
   - $\cos \theta_{\text{limit}} = \cos(aLimitDegrees)$：黄昏结束角度，默认取民用黄昏 $\cos 96^\circ$。
   - 判断规则：若 $\cos\theta > \cos\theta_{\text{begin}}$ 为白天；若 $\cos\theta > \cos\theta_{\text{limit}}$ 为黄昏；否则为黑夜。

2. **椭球内积函数**（用于直线-椭球求交的系数计算）：
   定义地球椭球面标准二次型的内积：
   $$\langle \mathbf{a}, \mathbf{b} \rangle_E = \frac{a_x b_x + a_y b_y}{A^2} + \frac{a_z b_z}{B^2}$$
   其中 $A = \text{UtEarth::cA}$（赤道半径），$B = \text{UtEarth::cB}$（极半径）。该内积将空间坐标映射到椭球的归一化坐标空间。

3. **椭球函数**（描述点相对于椭球表面的位置）：
   $$F(\mathbf{p}) = \langle \mathbf{p}, \mathbf{p} \rangle_E - 1$$
   $F(\mathbf{p}) = 0$ 表示点在椭球表面上，$F(\mathbf{p}) < 0$ 表示在椭球内部，$F(\mathbf{p}) > 0$ 表示在椭球外部。

4. **直线-椭球遮挡判定的二次方程**：
   从观测者 $\mathbf{O}$ 到目标 $\mathbf{T}$ 的视线参数方程为 $\mathbf{p}(\lambda) = \mathbf{O} + \lambda(\mathbf{T} - \mathbf{O})$，代入椭球函数得二次方程：
   $$a\lambda^2 + b\lambda + c = 0$$
   其中：
   $$a = \langle \mathbf{T} - \mathbf{O}, \mathbf{T} - \mathbf{O} \rangle_E \quad (\text{恒正})$$
   $$b = 2 \langle \mathbf{O}, \mathbf{T} - \mathbf{O} \rangle_E$$
   $$c = \langle \mathbf{O}, \mathbf{O} \rangle_E - 1 = F(\mathbf{O})$$
   判别式 $\Delta = b^2 - 4ac$，若 $\Delta \ge 0$，两根为：
   $$\lambda_1 = \frac{-b + \sqrt{\Delta}}{2a}, \quad \lambda_2 = \frac{-b - \sqrt{\Delta}}{2a}$$
   目标 $\mathbf{T}$ 的归一化距离 $\lambda_{\text{target}} = \|\mathbf{T} - \mathbf{O}\|$（即参数到目标处的值）。
   遮挡判定条件：$\lambda_1 > \varepsilon$ 且 $\lambda_2 + \varepsilon < \lambda_{\text{target}}$（其中 $\varepsilon = 0.05$ m 为容差），表示视线在到达目标前穿过了地球表面。

5. **全影/半影判别**：
   将太阳视为具有有限半径（cMEAN_RADIUS）的圆盘，取太阳的两个边缘点：
   - 太阳上边缘（远离地球地平线的边缘）：$\mathbf{P}_{\text{upper}} = \mathbf{P}_{\text{Sun}} + R_{\odot} \cdot \hat{\mathbf{u}}$
   - 太阳下边缘（靠近地球地平线的边缘）：$\mathbf{P}_{\text{lower}} = \mathbf{P}_{\text{Sun}} - R_{\odot} \cdot \hat{\mathbf{u}}$
   其中 $\hat{\mathbf{u}}$ 为垂直于太阳方向且指向地平方向上方的单位矢量（由 $\hat{\mathbf{u}} = \hat{\mathbf{r}}_{\text{loc}} \times \hat{\mathbf{s}}_{\text{Sun}}$ 构造，再规范化）。
   依次对上下边缘执行 MaskedByHorizon：
   - 上下均被遮挡：全影 (Umbra)
   - 仅下边缘被遮挡：半影 (Penumbra)
   - 上下均可见：光照区 (Illuminated)
   - 仅上边缘被遮挡：物理上不可能，触发断言。

6. **EclipseEventManager 调度逻辑**：
   地影事件由轨道外推器的 GetEclipseTimes 方法预测入影/出影的相对时间：
   - 若当前不在阴影中：$t_{\text{entry}} < t_{\text{exit}}$，安排 ECLIPSE_ENTRY 事件在 $t_0 + t_{\text{entry}}$。
   - 若当前在阴影中：$t_{\text{entry}} > t_{\text{exit}}$，安排 ECLIPSE_EXIT 事件在 $t_0 + t_{\text{exit}}$（因已通过入影点，下一次事件是出影）。
   - 若无阴影穿越：安排 1/4 轨道周期后重新评估：
     $$\Delta t_{\text{eval}} = \frac{0.25}{n \cdot 2\pi} = \frac{1}{8\pi n}$$
     其中 $n$ 为平运动角速率（rad/s）。

### 算法伪代码

```
// ========== 天光阶段判别算法 ==========
// 算法目标：根据地面上指定经纬度处的太阳天顶角判断白天/黄昏/黑夜
// 调用上下文：用于传感器视距分析、热控分析等场景

function GetPhaseOfDay(aLatDegrees, aLonDegrees, aTime, aLimitDegrees = cTWILIGHT_CIVIL):
    // 第一步：获取太阳矢量在观测点 NED 坐标系中的方向
    vecNED ← UtSun.GetSunVecNED(aLatDegrees, aLonDegrees, aTime)
    // vecNED[0] = 北分量，vecNED[1] = 东分量，vecNED[2] = 地心方向分量（朝下为正）

    // 第二步：计算太阳天顶角的余弦值
    // cosTheta = -vecNED.z：取负号将"天底方向"转为"天顶方向"
    cosTheta ← -vecNED.Get(2)    // cos(天顶角)

    // 第三步：计算用户指定的黄昏结束角度对应的余弦值
    cosLimit ← cos(aLimitDegrees * UtMath.cRAD_PER_DEG) // 度转弧度后取余弦

    // 第四步：三区判别
    if cosTheta > cCOS_TWILIGHT_BEGIN:    // 太阳在地平线下不到 50 角分
        retval ← cDAY     // 白天：太阳几乎在地平线以上
    else if cosTheta > cosLimit:    // 太阳在天顶角 limit 之内
        retval ← cTWILIGHT    // 黄昏：处于白天与黑夜之间的过渡
    else:    // 太阳天顶角超过限值
        retval ← cNIGHT    // 黑夜：太阳充分在地平线以下
    return retval

// ========== 地球地平线遮挡判别算法 ==========
// 算法目标：判断从观测者视线方向的目标是否被地球椭球遮挡
// 核心方法：视线（线段）与地球椭球的几何求交

function MaskedByHorizon(aObserverWCS[3], aTargetWCS[3]):
    // 第一步：计算视线向量 T - O
    TminusO ← Subtract(aTargetWCS, aObserverWCS)    // 视线方向 = 目标 - 观测者
    lambdaTarget ← Normalize(TminusO)    // 归一化并获取目标距离（参数化长度）

    // 第二步：计算二次方程系数 a, b, c
    // a = <T-O, T-O>_E —— 视线在椭球归一化空间中的长度平方
    aCoeff ← EllipsoidalInnerProduct(TminusO, TminusO)
    // b = 2 * <O, T-O>_E —— 观测者位置与视线的交叉项
    bCoeff ← 2.0 * EllipsoidalInnerProduct(aObserverWCS, TminusO)
    // c = F(O) = <O, O>_E - 1 —— 观测者相对于椭球表面的位置函数
    cCoeff ← EllipsoidalFunction(aObserverWCS)

    // 第三步：判別式计算
    retval ← false
    discrim ← bCoeff * bCoeff - 4.0 * aCoeff * cCoeff
    if discrim >= 0.0:    // 视线与椭球有交点（或相切）
        sqrtDiscrim ← sqrt(discrim)

        // 第四步：求解两个根（因为 aCoeff > 0，所以 solnOne >= solnTwo）
        solnOne ← (-bCoeff + sqrtDiscrim) / (2.0 * aCoeff)  // 较大根（远端交点）
        solnTwo ← (-bCoeff - sqrtDiscrim) / (2.0 * aCoeff)  // 较小根（近端交点）

        // 第五步：遮挡判定 —— 条件为第一个交点在地表外侧（> 容差）
        // 且第二个交点在到达目标之前（< 目标距离 - 容差）
        // 容差 cMASKED_BY_EARTH_TOLERANCE = 0.05 m 处理数值误差
        retval ← (solnOne > cMASKED_BY_EARTH_TOLERANCE)
                 and (solnTwo + cMASKED_BY_EARTH_TOLERANCE < lambdaTarget)

    return retval

// ========== 椭球内积辅助函数 ==========
// 功能：计算两个 WCS 矢量在椭球归一化空间中的内积
// 公式：<a,b>_E = (a_x*b_x + a_y*b_y) / A^2 + (a_z*b_z) / B^2
function EllipsoidalInnerProduct(aVectorA_WCS[3], aVectorB_WCS[3]):
    return (aVectorA[0]*aVectorB[0] + aVectorA[1]*aVectorB[1]) / (UtEarth.cA * UtEarth.cA)
           + (aVectorA[2] * aVectorB[2]) / (UtEarth.cB * UtEarth.cB)

// ========== 椭球函数 ==========
// 功能：计算点相对于地球椭球表面的位置（正值 = 在外，负值 = 在内，零 = 在表面）
function EllipsoidalFunction(aLocationWCS[3]):
    return EllipsoidalInnerProduct(aLocationWCS, aLocationWCS) - 1.0

// ========== 计算太阳上下边缘视线方向 ==========
// 功能：以观测者为原点，计算太阳圆盘上下边缘的 WCS 位置
function GetDisplacementToSolarLimbs(aLocationWCS[3], aTime, aUpperLimbWCS[3], aLowerLimbWCS[3]):
    // 第一步：获取太阳在地心固连坐标系（WCS）中的位置
    sunLoc[3] ← UtSun.GetSunLocationWCS(aTime)
    // sunHat 为太阳方向单位矢量
    sunHat ← Normalize(sunLoc)

    // 第二步：构造"向上"矢量 —— 垂直于太阳方向和地心方向
    locHat ← Normalize(aLocationWCS)    // 观测者的地心方向单位矢量
    upVec ← CrossProduct(locHat, sunHat)    // upVec = 地心方向 × 太阳方向
    scale ← Magnitude(upVec)

    if scale < 1.0e-6:    // 地球-太阳-观测者共线（对应约 1 角秒精度）
        // 此时地心方向和太阳方向平行，任选一个垂直于 sunHat 的方向作为 up
        maxIter ← max_element(sunHat)    // 找 sunHat 最大分量位置
        minIter ← min_element(sunHat)    // 找 sunHat 最小分量位置
        upVec ← 零向量
        upVec[maxIter位置] ← -sunHat[minIter位置]    // 构造正交分量
        upVec[minIter位置] ← sunHat[maxIter位置]
    Normalize(upVec)    // 归一化 upVec

    // 第三步：构造太阳"侧向"矢量 —— 垂直于太阳方向和 up 方向
    limbVec ← CrossProduct(sunHat, upVec)    // 在太阳圆盘平面内的正交方向
    // 乘以太阳平均半径得到边缘偏移量
    limbVec ← limbVec * UtSun.cMEAN_RADIUS

    // 第四步：计算上下边缘位置
    aUpperLimbWCS ← sunLoc + limbVec    // 太阳中心 + 边缘偏移 = 上边缘
    aLowerLimbWCS ← sunLoc - limbVec    // 太阳中心 - 边缘偏移 = 下边缘

// ========== 航天器光照状态判别（全影/半影/光照） ==========
// 算法目标：判断航天器当前处于地球全影、半影还是光照区
function GetPlatformSolarIllumination(aPlatformPtr):
    if aPlatformPtr 未关联仿真:
        return cINVALID_PLATFORM    // 无法获取时间信息

    // 第一步：获取航天器当前位置
    platformLocation ← aPlatformPtr.GetLocationWCS()

    // 第二步：获取当前仿真时间
    time ← 当前仿真时间（由平台上次更新时间和仿真日历推算）

    // 第三步：计算太阳上下边缘在 WCS 中的位置
    GetDisplacementToSolarLimbs(platformLocation, time, upperLimb, lowerLimb)

    // 第四步：分别检查上下边缘是否被地球遮挡
    upperMasked ← MaskedByHorizon(platformLocation, upperLimb)  // 太阳上边缘是否可见
    lowerMasked ← MaskedByHorizon(platformLocation, lowerLimb)  // 太阳下边缘是否可见

    // 第五步：根据遮挡情况判定光照状态
    if upperMasked and lowerMasked:    // 上下边缘均被遮挡
        retval ← cEARTH_UMBRA    // 全影：太阳完全被地球遮挡
    else if not upperMasked and lowerMasked:    // 仅下边缘被遮挡
        retval ← cEARTH_PENUMBRA    // 半影：太阳部分被地球遮挡
    else if upperMasked and not lowerMasked:    // 仅上边缘被遮挡
        assert(false) // 物理上不可能：若下边缘可见，上边缘一定也可见
    else:    // 上下边缘均可见
        retval ← cILLUMINATED    // 光照区：太阳完全可见
    return retval

// ========== 地影事件管理器调度逻辑 ==========
// 算法目标：预测航天器的入影/出影时间，并安排事件触发
// 调用上下文：平台初始化、轨道机动后、每次地影事件触发后

function InitiateEclipseEvent(aSimTime, aId, aSpaceMover):
    if 仿真未激活:
        // 仿真尚未启动，安排仿真开始后立即重新评估
        eventPtr ← new EclipseEvent(cEVALUATE)
        eventPtr.SetTime(aSimTime + 1.0e-6)
        return

    // 调用轨道外推器的地影预测方法
    solutionExists ← aSpaceMover.GetPropagator().GetEclipseTimes(timeToEntry, timeToExit)

    if solutionExists:
        if timeToEntry > timeToExit:    // 当前已在阴影中
            eventPtr ← new EclipseEvent(cEXIT)    // 下一个事件是出影
            eventPtr.SetTime(aSimTime + timeToExit) // 安排出影时刻
        else:    // 当前在光照中
            eventPtr ← new EclipseEvent(cENTRY)    // 下一个事件是入影
            eventPtr.SetTime(aSimTime + timeToEntry) // 安排入影时刻
    else:    // 当前轨道周期内无地影穿越
        eventPtr ← new EclipseEvent(cEVALUATE)     // 安排重新评估
        // 评估间隔 = 1/4 轨道周期 = 0.25 / (n * 2π)（轨道周期 = 2π/n）
        timeToEval ← 0.25 / (aSpaceMover.GetPropagator()
                              .GetOrbitalState()
                              .GetOrbitalElements()
                              .GetMeanMotion() * UtMath.cTWO_PI)
        eventPtr.SetTime(aSimTime + timeToEval)

    // 将事件加入仿真事件队列
    GetSimulation().AddEvent(eventPtr)

// ========== 地影事件执行 ==========
// 当某个地影事件到达预定时刻时被仿真引擎调用
function EclipseEvent.Execute():
    if 事件已失效（平台被删除或轨道机动导致非最新事件）:
        return cDELETE    // 删除此过期事件

    // 更新运动体状态至当前仿真时刻
    mSpaceMoverPtr.Update(GetTime())

    // 重新计算入影/出影时间
    solutionExists ← mSpaceMoverPtr.GetPropagator().GetEclipseTimes(timeToEntry, timeToExit)

    if solutionExists:
        if mType == cENTRY:    // 入影事件触发
            // 通知所有观察者：航天器进入地影
            WsfObserver.EclipseEntry(GetTime(), mSpaceMoverPtr)
            mType ← cEXIT    // 切换为等待出影
            SetTime(GetTime() + timeToExit)    // 安排出影时刻
        else if mType == cEXIT:    // 出影事件触发
            // 通知所有观察者：航天器离开地影
            WsfObserver.EclipseExit(GetTime(), mSpaceMoverPtr)
            mType ← cENTRY    // 切换为等待入影
            SetTime(GetTime() + timeToEntry)    // 安排下一次入影时刻
        else: // cEVALUATE —— 重新评估
            if timeToEntry > timeToExit:    // 当前在阴影中
                mType ← cEXIT
                SetTime(GetTime() + timeToExit)
            else:    // 当前在光照中
                mType ← cENTRY
                SetTime(GetTime() + timeToEntry)
    else:    // 仍无地影穿越
        mType ← cEVALUATE
        // 1/4 轨道周期后再次评估
        timeToEval ← 0.25 / (GetPropagator().GetOrbitalState()
                              .GetOrbitalElements().GetMeanMotion() * UtMath.cTWO_PI)
        SetTime(GetTime() + timeToEval)

    return cRESCHEDULE    // 重新安排此事件到新的时刻
```

### 源码使用说明

#### 入口和调用链

```
→ GetPhaseOfDay(aLatDegrees, aLonDegrees, aTime, aLimitDegrees)
   // 天光阶段判别入口：输入经纬度和时间，返回白天/黄昏/黑夜
   → UtSun::GetSunVecNED(aLatDegrees, aLonDegrees, aTime, vecNED)
      // 计算太阳方向在观测点 NED 坐标系中的单位矢量

→ GetPlatformSolarIllumination(aPlatformPtr)
   // 航天器地影判别入口：输入平台指针，返回光照/半影/全影状态

   → GetDisplacementToSolarLimbs(platformLocation, time, upperLimb, lowerLimb)
      // 计算太阳上下边缘的 WCS 位置
      → UtSun::GetSunLocationWCS(aTime, sunLoc)
         // 获取太阳在地心固连坐标系中的位置

   → MaskedByHorizon(platformLocation, upperLimb)
      // 检查太阳上边缘是否被地球遮挡
      → EllipsoidalInnerProduct(aObserverWCS, TminusO)
         // 计算椭球归一化空间中的内积：<a,b>_E = (ax*bx+ay*by)/A^2 + (az*bz)/B^2

      → EllipsoidalFunction(aObserverWCS)
         // 计算观测者相对于椭球表面的位置函数：F(p) = <p,p>_E - 1

   → MaskedByHorizon(platformLocation, lowerLimb)
      // 检查太阳下边缘是否被地球遮挡（同上层计算逻辑）

→ WsfEclipseEventManager::Initialize()
   // 地影事件管理器初始化：检查是否有 ECLIPSE_ENTRY/EXIT 事件订阅者

→ WsfEclipseEventManager::Enable(aSimTime)
   // 启用地影事件监测：注册平台生命周期回调

   → InitiateMonitoring(aSimTime, platformPtr)
      // 对每个空间平台启动地影监测
      → InitiateEclipseEvent(aSimTime, platformId, spaceMover)
         // 调用轨道外推器的 GetEclipseTimes 预测入影/出影时刻

→ WsfEclipseEventManager::UpdateMonitoring(aSimTime, spaceMoverPtr, maneuver)
   // 轨道机动后重新计算地影事件（本质上是重新调用 InitiateEclipseEvent）

→ EclipseEvent::Execute()
   // 地影事件到期执行：通知观察者、重新计算下一事件
   → WsfObserver::EclipseEntry() / WsfObserver::EclipseExit()
      // 通知地影进入/退出观察者回调

   → mSpaceMoverPtr->GetPropagator().GetEclipseTimes(timeToEntry, timeToExit)
      // 重新调用轨道外推器的入影/出影预测

→ WsfConfigureEclipseEventManger::SimulationCreated(aSimulation)
   // 场景扩展点：在仿真创建时注册 WsfEclipseEventManager 扩展
```

#### 源码位置

| File | Symbol | 中文说明 |
|------|--------|----------|
| [WsfSolarTerminator.hpp](source_root/src/core/wsf_space/source/WsfSolarTerminator.hpp) | `WsfSolarTerminator` | 太阳终结线命名空间，包含天光阶段枚举和地影判别函数声明 |
| [WsfSolarTerminator.cpp](source_root/src/core/wsf_space/source/WsfSolarTerminator.cpp) | `GetPhaseOfDay()` | 天光阶段判别（白天/黄昏/黑夜）（Line 108-129） |
| 同上 | `MaskedByHorizon()` | 地球椭球遮挡判断（直线-椭球求交）（Line 136-178） |
| 同上 | `GetPlatformSolarIllumination()` | 航天器全影/半影/光照区判别（Line 187-227） |
| 同上 | `GetDisplacementToSolarLimbs()` | 计算太阳上下边缘的 WCS 位置（匿名命名空间，Line 60-99） |
| 同上 | `EllipsoidalInnerProduct()` | 椭球归一化内积（匿名命名空间，Line 39-43） |
| 同上 | `EllipsoidalFunction()` | 椭球表面位置函数 $F(p) = \langle p,p\rangle_E - 1$（匿名命名空间，Line 50-53） |
| [WsfEclipseEventManager.hpp](source_root/src/core/wsf_space/source/WsfEclipseEventManager.hpp) | `WsfEclipseEventManager` | 地影事件管理器类声明，封装 EclipseEvent 内部类 |
| [WsfEclipseEventManager.cpp](source_root/src/core/wsf_space/source/WsfEclipseEventManager.cpp) | `Initialize()` | 初始化检查是否有地影事件订阅者（Line 30-41） |
| 同上 | `Enable()` | 启用地影监测并注册平台生命周期回调（Line 46-73） |
| 同上 | `InitiateEclipseEvent()` | 调用 GetEclipseTimes 预测入影/出影时刻（Line 113-152） |
| 同上 | `EclipseEvent::Execute()` | 地影事件执行：通知观察者并重新计算（Line 183-241） |
| 同上 | `UpdateMonitoring()` | 轨道机动后重新计算地影（Line 156-161） |

#### 框架依赖

- **UtSun**：提供太阳位置计算（GetSunLocationWCS 获取太阳 WCS 位置，GetSunVecNED 获取太阳 NED 方向矢量）和太阳平均半径常量 cMEAN_RADIUS。
- **UtEarth**：提供地球椭球参数（cA 赤道半径，cB 极半径）。
- **UtVec3d**：三维矢量运算（加减、归一化、叉积、点积、模长）。
- **UtMath**：角度转换常量 cRAD_PER_DEG、cTWO_PI。
- **UtCalendar**：日历时间类。
- **WsfSimulation / WsfPlatform / WsfDateTime**：仿真框架基础设施，提供平台位置、仿真时间等。
- **UtOrbitalPropagatorBase**：轨道外推器接口，其 GetEclipseTimes 方法为地影预测核心。
- **WsfSpaceMoverBase**：空间运动体，包含轨道外推器引用。
- **WsfObserver**：观察者模式，用于事件回调通知。
- **WsfEvent**：仿真事件调度框架。

#### 测试和验证计划

1. **天光阶段判别测试**：选取赤道春分点（当地时间正午、黄昏起、黄昏末、午夜），分别验证 GetPhaseOfDay 返回正确的 cDAY / cTWILIGHT / cNIGHT。可选用民用黄昏（96度）、航海黄昏（102度）、天文黄昏（108度）三种阈值分别测试。
2. **地平线遮挡边界测试**：将观测者置于地球表面赤道半径处（WCS [6378137, 0, 0]），目标置于刚好在地平线上方（视线切于椭球面）。验证 MaskedByHorizon 在切点附近的判定正确性，包括数值容差 cMASKED_BY_EARTH_TOLERANCE 的处理。
3. **全影/半影判别测试**：将航天器置于地球阴影锥的全影区和半影区位置，验证 GetPlatformSolarIllumination 正确返回 cEARTH_UMBRA 和 cEARTH_PENUMBRA。
4. **EclipseEventManager 状态机测试**：构造已知轨道（如 LEO 极轨道），验证 EclipseEventManager 正确预测入影/出影时间并在仿真中触发相应事件。测试轨道机动后事件的重新计算是否正确。
5. **地球-太阳-观测者共线边缘情况**：测试当太阳方向与地心方向平行时（scale < 1e-6），GetDisplacementToSolarLimbs 中的正交矢量构造替代逻辑是否正常工作。

#### 可移植性评分

**可移植性**：高

**原因**：
1. 天光阶段判别仅为简单的余弦角阈值比较，与任何框架无关，可直接用任何语言实现。
2. 地球遮挡判定基于直线-椭球求交的二次方程，是标准解析几何方法，公式完全自包含，不依赖特殊框架组件。
3. 全影/半影判别利用太阳边缘点到观测者的视线遮挡判定组合，逻辑清晰，易于在其他仿真环境中复现。
4. EclipseEventManager 的调度逻辑（状态机 + 1/4 轨道周期再评估）高度依赖 AFSIM 的仿真事件调度框架（WsfEvent）和观察者模式（WsfObserver），但核心的地影预测逻辑（GetEclipseTimes）位于轨道外推器中，调度策略本身可简单模仿。
5. 算法依赖的物理常量（地球赤道/极半径、太阳平均半径、黄昏角度定义）均为公开标准值。
