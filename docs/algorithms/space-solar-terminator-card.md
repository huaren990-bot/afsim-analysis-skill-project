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

#### 内部状态

本节列出跨帧或跨调用持久化的变量。由于 `WsfSolarTerminator` 本身是**无状态**的命名空间（所有函数为纯函数，不持有成员变量），真正的内部状态集中在 `WsfEclipseEventManager` 及其内部类 `EclipseEvent` 中。

##### WsfEclipseEventManager 内部状态

| 变量名 | 类型 | 初始值 | 物理含义 | 更新时机 |
|--------|------|--------|----------|----------|
| `mIsEnabled` | `bool` | `false`（构造函数初始化） | 地影事件监测是否已启用。为 false 时不消耗计算资源 | `Enable()` 设为 true；`Disable()` 设为 false |
| `mCallbacks` | `UtCallbackHolder` | 空（构造时默认） | 持有平台生命周期回调句柄（平台初始化、删除、轨道机动更新、轨道机动完成） | `Enable()` 注册 4 个回调；`Disable()` 清空 |
| `mPlatformToCurrentEventIdMap` | `std::map<WsfStringId, size_t>` | 空（构造时默认） | 平台名称 → 当前有效事件 ID 的映射，用于在 `EclipseEvent::Execute()` 中验证事件是否仍是最新的（防止轨道机动后旧事件误触发） | `InitiateEclipseEvent()` 插入/更新；`CeaseMonitoring()` 删除；`Disable()` 清空 |

##### EclipseEvent（内部类）内部状态

| 变量名 | 类型 | 初始值 | 物理含义 | 更新时机 |
|--------|------|--------|----------|----------|
| `mType` | `EclipseEvent::Type`（枚举：cENTRY / cEXIT / cEVALUATE） | 构造函数传入 | 当前事件类型：入影、出影还是重新评估。决定 Execute() 执行哪条分支 | 构造函数设置；`Execute()` 中根据 GetEclipseTimes 结果更新（cENTRY→cEXIT 或反之）；`SetType()` 直接设置 |
| `mId` | `size_t` | 构造函数传入 | 本事件的唯一 ID（与 InitiateEclipseEvent 调用时的 aId 一致）。用于和 mPlatformToCurrentEventIdMap 比对，判断事件是否过期 | 构造时赋值，之后不变 |
| `mEclipseManager` | `WsfEclipseEventManager&` | 构造函数传入的引用 | 指向所属的 EclipseEventManager，用于访问 mPlatformToCurrentEventIdMap 和 IsEnabled() | 构造时绑定，之后不变 |
| `mSpaceMoverPtr` | `WsfSpaceMoverBase*` | 构造函数传入 | 指向关联的航天器运动体，用于在事件执行时获取轨道外推器和更新运动状态 | 构造时绑定，之后不变 |
| `mPlatformIndex` | `size_t` | 构造函数从 `aSpaceMoverPtr->GetPlatform()->GetIndex()` 获取 | 航天器在仿真中的索引号，用于在 Execute() 中验证平台是否仍然存在 | 构造时赋值，之后不变 |

> **关键设计说明**：`EclipseEvent` 对象被仿真事件队列持有，在其 `Execute()` 返回 `cRESCHEDULE` 后重新入队到新的仿真时刻。因此 `mType`、`mSpaceMoverPtr` 等成员变量实现了跨帧的状态记忆，使得同一事件对象可以在不同仿真帧之间切换 cENTRY/cEXIT 状态。

#### 变量映射表

本节建立源代码中变量与数学公式变量之间的对应关系，方便读者在阅读公式时回溯源码。

##### MaskedByHorizon 相关变量

| 代码变量 | 数学符号 | 含义 |
|----------|----------|------|
| `aObserverWCS` | $\mathbf{O}$ | 观测者在地心固连坐标系（WCS）中的位置矢量（3 分量数组） |
| `aTargetWCS` | $\mathbf{T}$ | 目标（太阳边缘点）在地心固连坐标系中的位置矢量 |
| `TminusO` | $\mathbf{T} - \mathbf{O}$ | 视线方向矢量（目标减去观测者） |
| `lambdaTarget` | $\lambda_{\text{target}}$ | 视线从观测者到目标的归一化距离（即 $\|\mathbf{T} - \mathbf{O}\|$，同时 TminusO 被原地归一化） |
| `aCoeff` | $a$ | 二次方程二次项系数 $a = \langle \mathbf{T}-\mathbf{O}, \mathbf{T}-\mathbf{O} \rangle_E$ |
| `bCoeff` | $b$ | 二次方程一次项系数 $b = 2\langle \mathbf{O}, \mathbf{T}-\mathbf{O} \rangle_E$ |
| `cCoeff` | $c$ | 二次方程常数项 $c = F(\mathbf{O}) = \langle \mathbf{O},\mathbf{O} \rangle_E - 1$ |
| `discrim` | $\Delta$ | 二次方程判别式 $\Delta = b^2 - 4ac$ |
| `sqrtDiscrim` | $\sqrt{\Delta}$ | 判别式的平方根 |
| `solnOne` | $\lambda_1$ | 较大根 $\lambda_1 = \frac{-b + \sqrt{\Delta}}{2a}$（视线与椭球的远端交点参数） |
| `solnTwo` | $\lambda_2$ | 较小根 $\lambda_2 = \frac{-b - \sqrt{\Delta}}{2a}$（视线与椭球的近端交点参数） |
| `cMASKED_BY_EARTH_TOLERANCE` | $\varepsilon$ | 遮挡判定的数值容差（0.05 m），用于处理观测者恰好位于地表时的浮点误差 |
| `retval` | — | 布尔返回值：true = 被地球遮挡，false = 可见 |

##### GetDisplacementToSolarLimbs 相关变量

| 代码变量 | 数学符号 | 含义 |
|----------|----------|------|
| `aLocationWCS` | $\mathbf{P}_{\text{obs}}$ | 观测者（航天器）在地心固连坐标系中的位置 |
| `aTime` | $t$ | 当前仿真时间（UtCalendar 类型） |
| `sunLoc` | $\mathbf{P}_{\odot}$ | 太阳中心在地心固连坐标系中的位置（由 UtSun::GetSunLocationWCS 计算） |
| `sunHat` | $\hat{\mathbf{s}}$ | 太阳方向的单位矢量（从地心指向太阳） |
| `locHat` | $\hat{\mathbf{r}}$ | 观测者地心方向的单位矢量 |
| `upVec`（归一化前） | $\hat{\mathbf{r}} \times \hat{\mathbf{s}}$ | “向上”矢量：垂直于地心方向和太阳方向，指向地平面上方 |
| `upVec`（归一化后） | $\hat{\mathbf{u}}$ | 归一化后的“向上”单位矢量 |
| `limbVec`（归一化后） | $\hat{\mathbf{l}} = \hat{\mathbf{s}} \times \hat{\mathbf{u}}$ | 太阳圆盘平面内垂直于 $\hat{\mathbf{u}}$ 的单位矢量（边缘方向） |
| `limbVec`（乘 R 后） | $R_{\odot} \cdot \hat{\mathbf{l}}$ | 太阳边缘相对于太阳中心的位移矢量 |
| `aUpperLimbWCS` | $\mathbf{P}_{\text{upper}}$ | 太阳上边缘（远离地平线的边缘）的 WCS 位置 = $\mathbf{P}_{\odot} + R_{\odot} \cdot \hat{\mathbf{l}}$ |
| `aLowerLimbWCS` | $\mathbf{P}_{\text{lower}}$ | 太阳下边缘（靠近地平线的边缘）的 WCS 位置 = $\mathbf{P}_{\odot} - R_{\odot} \cdot \hat{\mathbf{l}}$ |
| `scale` | $\|\hat{\mathbf{r}} \times \hat{\mathbf{s}}\|$ | 叉积的模长，用于检测地球-太阳-观测者是否共线（scale < 1e-6 时触发替代正交构造） |

##### GetPhaseOfDay 相关变量

| 代码变量 | 数学符号 | 含义 |
|----------|----------|------|
| `aLatDegrees` | $\phi$ | 地面观测点的地理纬度（度） |
| `aLonDegrees` | $\lambda$ | 地面观测点的地理经度（度） |
| `aTime` | $t$ | 需要判断天光阶段的世界协调时 |
| `aLimitDegrees` | $\theta_{\text{limit}}$ | 黄昏结束角度（度），默认取 cTWILIGHT_CIVIL = 96° |
| `vecNED` | $\hat{\mathbf{s}}_{\text{NED}}$ | 太阳方向在 NED（北-东-地）坐标系中的单位矢量 |
| `vecNED.Get(2)` | $\hat{\mathbf{s}}_{\text{NED},z}$ | NED 矢量的 Z 分量（沿地心方向，向下为正） |
| `cosTheta` | $\cos\theta$ | 太阳天顶角的余弦值，$\cos\theta = -\hat{\mathbf{s}}_{\text{NED},z}$（取负号因为 NED 的 Z 轴朝下） |
| `cosLimit` | $\cos\theta_{\text{limit}}$ | 黄昏结束角度的余弦值 |
| `cCOS_TWILIGHT_BEGIN` | $\cos\theta_{\text{begin}} = \cos(90^\circ 50')$ | 黄昏开始的余弦阈值，太阳在地平线下 50 角分 |
| `retval` | — | PhaseOfDay 枚举返回值：cDAY / cTWILIGHT / cNIGHT |

##### EclipseEventManager 相关变量

| 代码变量 | 数学符号 | 含义 |
|----------|----------|------|
| `aSimTime` | $t_0$ | 当前仿真时间（起点时刻） |
| `timeToEntry` | $t_{\text{entry}}$ | 从当前时刻到下一次进入地影的相对时间 |
| `timeToExit` | $t_{\text{exit}}$ | 从当前时刻到下一次离开地影的相对时间 |
| `solutionExists` | — | 布尔值：当前轨道周期内是否存在地影穿越事件 |
| `timeToEval` | $\Delta t_{\text{eval}}$ | 无地影事件时的重新评估间隔 = $\frac{0.25}{n \cdot 2\pi}$ |
| `mType` | — | 事件类型枚举：cENTRY（等待入影）、cEXIT（等待出影）、cEVALUATE（等待重新评估） |
| `n`（平运动角速率，在源码中不直接命名） | $n$ | 轨道平运动角速率（rad/s），通过 `GetMeanMotion()` 获取 |

##### EllipsoidalInnerProduct 相关变量

| 代码变量 | 数学符号 | 含义 |
|----------|----------|------|
| `aVectorA_WCS` | $\mathbf{a}$ | 椭球内积的第一个 WCS 矢量 |
| `aVectorB_WCS` | $\mathbf{b}$ | 椭球内积的第二个 WCS 矢量 |
| `UtEarth::cA` | $A$ | 地球 WGS-84 椭球赤道半径（长半轴），约 6378137 m |
| `UtEarth::cB` | $B$ | 地球 WGS-84 椭球极半径（短半轴），约 6356752 m |

##### 物理常量

| 代码常量 | 数值 | 含义 |
|----------|------|------|
| `UtSun::cMEAN_RADIUS` | $6.963420 \times 10^8$ m | 太阳平均半径（来源：Emilio et al., 2012, The Astrophysical Journal） |
| `UtEarth::cA` | 约 6378137 m | 地球赤道半径（WGS-84 长半轴） |
| `UtEarth::cB` | 约 6356752 m | 地球极半径（WGS-84 短半轴） |

#### 边界条件

本节列出算法中所有数值稳定性保护、无效输入处理、限幅阈值及回退行为。这些细节是实现时最容易遗漏的部分。

##### 1. MaskedByHorizon — 观测者恰好在地球表面附近

- **问题**：当观测者恰好位于地球椭球表面上时，椭圆函数 $F(\mathbf{O}) \approx 0$，二次方程常数项 $c \approx 0$，导致近端根 $\lambda_2 \approx 0$。此时浮点误差可能将 $\lambda_2$ 计算为一个极小的正数或负数，造成误判。
- **保护**：容差常量 `cMASKED_BY_EARTH_TOLERANCE = 0.05` m（约 5 cm）在遮挡判定条件中发挥关键作用：
  - `solnOne > 0.05`：要求远端交点在观测者之外至少 5 cm（排除观测者恰好位于地表内侧的数值抖动）。
  - `solnTwo + 0.05 < lambdaTarget`：要求近端交点 + 5 cm 仍小于目标距离（排除视线恰好擦过地表的边界情况）。
- **效果**：该容差排除了注释中列出的情况 2、5、6、7（不应视为遮挡），正确识别情况 1、3、4（应视为遮挡）。

##### 2. MaskedByHorizon — 判别式为负

- **处理**：`if (discrim >= 0.0)` — 若 $\Delta < 0$，则视线与椭球无交点。直接返回 `retval = false`（未被遮挡），不执行任何求根操作。
- **原因**：$\Delta < 0$ 表示二次方程无实根，视线完全在椭球外部穿过。

##### 3. MaskedByHorizon — aCoeff 为正的隐含前提

- **源码注释**：`aCoeff` 由 `EllipsoidalInnerProduct(TminusO, TminusO)` 计算，因为椭球内积是正定的，所以 $a > 0$（除非观测者位于太阳中心，这在物理上不可能）。
- **意义**：$a > 0$ 保证了 $\lambda_1 \ge \lambda_2$（较大根在前），使得遮挡判定逻辑中的大小比较有意义。
- **无显式保护**：代码未对 $a \le 0$ 做防御性检查，因为物理上不可能出现。

##### 4. GetDisplacementToSolarLimbs — 地球-太阳-观测者共线

- **问题**：当 $\hat{\mathbf{r}}$（地心方向）与 $\hat{\mathbf{s}}$（太阳方向）平行或反平行时，叉积 $\hat{\mathbf{r}} \times \hat{\mathbf{s}} = \mathbf{0}$，无法构造“向上”矢量。
- **检测阈值**：`scale < 1.0e-6`（约对应 1 角秒精度）。当叉积模长小于此阈值时，认为地心方向与太阳方向共线。
- **回退行为**（源码 WsfSolarTerminator.cpp Line 78-89）：
  1. 将 `sunHat` 复制到 `upVec`。
  2. 找出 `sunHat` 的最大分量索引 `maxIter` 和最小分量索引 `minIter`。
  3. 将 `upVec` 所有分量清零。
  4. 设置 `upVec[maxIter位置] = -sunHat[minIter位置]`，`upVec[minIter位置] = sunHat[maxIter位置]`。
  5. 最后归一化 `upVec`。
- **效果**：这构造了一个与 `sunHat` 正交的方向作为替代的“向上”矢量。虽然不是物理上精确的“地平面上方”，但在共线情况下任何正交方向都等价，不影响遮挡判定结果。

##### 5. GetPlatformSolarIllumination — 平台未关联仿真

- **检测**：`if (aPlatformPtr->GetSimulation() == nullptr)`。
- **处理**：返回 `PlatformSolarIllumination::cINVALID_PLATFORM`（枚举值 0），不执行任何后续计算。
- **原因**：地影判别需要仿真时间信息来获取太阳位置和平台最后更新时间，脱离仿真上下文无法完成计算。

##### 6. GetPlatformSolarIllumination — 仅上边缘被遮挡（物理不可能）

- **断言**：`assert(0 && "The upper limb should never be masked if the lower is not.")`。
- **含义**：太阳下边缘比上边缘更靠近地球地平线。如果下边缘可见（未被遮挡），上边缘（更远离地平线）一定也可见。因此“仅上边缘被遮挡”在物理上不可能发生。
- **程序行为**：Debug 模式下触发断言中止；Release 模式下会继续执行到最后的 `else` 分支，返回 `cILLUMINATED`（安全回退）。

##### 7. EclipseEventManager — 仿真未激活

- **场景**：`InitiateEclipseEvent()` 在 `GetSimulation().IsActive()` 为 false 时被调用（例如仿真尚未启动的初始化阶段）。
- **处理**（Line 144-149）：创建一个 `cEVALUATE` 类型事件，安排在当前时间 + 1e-6 秒后触发。仿真启动后立即重新评估。
- **原因**：仿真未激活时轨道外推器可能尚未就绪，无法调用 `GetEclipseTimes()`。

##### 8. EclipseEvent — 事件过期（过期事件保护）

- **检测条件**（Execute() Line 186-187）：
  - `mEclipseManager.IsEnabled()` 为 false（地影监测已被禁用）；或
  - 平台已被删除（`!GetSimulation()->PlatformExists(mPlatformIndex)`）；或
  - 事件 ID 不是该平台的最新事件 ID（轨道机动导致新事件已创建，旧事件过期）。
- **处理**：返回 `WsfEvent::cDELETE`，从仿真事件队列中移除该事件。
- **意义**：防止轨道机动后旧轨道的地影事件被错误触发，或已删除平台的地影事件继续产生回调。

##### 9. EclipseEventManager — 无地影穿越时的重评估间隔

- **场景**：`GetEclipseTimes()` 返回 `solutionExists == false`（当前轨道周期内无地影穿越）。
- **处理**：不放弃监测，而是安排 1/4 轨道周期后重新评估。
- **公式**：$\Delta t_{\text{eval}} = \frac{0.25}{n \cdot 2\pi}$（平运动 $n$ 取自轨道外推器当前轨道要素）。
- **原因**：地球绕太阳公转导致阴影锥方向缓慢旋转，当前无地影的轨道可能在 1/4 圈后进入阴影。
- **异常场景**：若 `n = 0`（非轨道运动，理论上不会发生在空间平台上），则 `timeToEval` 为无穷大。源码未对此做显式保护，依赖调用上下文保证 $n > 0$。

##### 10. GetPhaseOfDay — 黄昏限角范围

- **默认值**：`aLimitDegrees` 默认取 `cTWILIGHT_CIVIL = 96.0` 度（民用黄昏定义）。
- **预设三种标准阈值**：
  - `cTWILIGHT_CIVIL = 96.0`（民用黄昏：太阳在地平线下 6°）
  - `cTWILIGHT_NAUTICAL = 102.0`（航海黄昏：太阳在地平线下 12°）
  - `cTWILIGHT_ASTRONOMICAL = 108.0`（天文黄昏：太阳在地平线下 18°）
- **阈值定义来源**：Fundamentals of Astrodynamics and Applications, 4th Ed., p. 281。
- **无范围校验**：函数不检查 `aLimitDegrees` 是否在合理范围内（0～180 度）。传入负值会导致 `cosTheta` 阈值大于 1，所有情况均返回黑夜；传入大于 180 的值同理。调用者需自行保证输入合理。

#### 提取策略

本节说明如何从 AFSIM 源码中系统地提取本算法的所有代码元素和数学关系。

##### 提取源文件

| 源文件 | 提取目标 | 提取方式 |
|--------|----------|----------|
| `wsf_space/source/WsfSolarTerminator.hpp` | 公开 API 声明、枚举类型定义、常量声明 | 直接解析头文件：提取 `namespace WsfSolarTerminator` 内的所有函数声明、`enum class PhaseOfDay`、`enum class PlatformSolarIllumination`、`constexpr double` 常量 |
| `wsf_space/source/WsfSolarTerminator.cpp` | 核心算法实现（5 个函数 + 2 个辅助函数） | 逐函数分析：匿名命名空间中的 `EllipsoidalInnerProduct()`、`EllipsoidalFunction()`、`GetDisplacementToSolarLimbs()`；公开函数 `GetPhaseOfDay()`、`MaskedByHorizon()`、`GetPlatformSolarIllumination()` |
| `wsf_space/source/WsfEclipseEventManager.hpp` | EclipseEventManager 类声明、EclipseEvent 内部类声明 | 解析类成员变量和私有方法签名：`mIsEnabled`、`mCallbacks`、`mPlatformToCurrentEventIdMap`、`EclipseEvent::Type` 枚举 |
| `wsf_space/source/WsfEclipseEventManager.cpp` | 事件管理器实现（调度逻辑 + 状态机） | 逐方法分析：`Initialize()`、`Enable()`、`Disable()`、`InitiateEclipseEvent()`、`EclipseEvent::Execute()` |
| `tools/util/source/UtSun.hpp` | 太阳物理常量 | 提取 `UtSun::cMEAN_RADIUS`、`UtSun::cGRAVITATIONAL_PARAMETER`；提取 `GetSunLocationWCS()` 和 `GetSunVecNED()` 函数声明 |
| `tools/util/source/UtEarth.hpp` | 地球椭球参数 | 提取 `UtEarth::cA`（赤道半径）、`UtEarth::cB`（极半径） |

##### 提取流程

1. **头文件扫描**（第一步）
   - 打开 `WsfSolarTerminator.hpp`，提取所有 `WSF_SPACE_EXPORT` 函数声明作为算法入口点列表。
   - 提取枚举定义（`PhaseOfDay`、`PlatformSolarIllumination`）的枚举项及其数值。
   - 提取 `constexpr double` 常量（`cTWILIGHT_CIVIL` 等）及其数值和注释说明。

2. **cpp 实现分析**（第二步）
   - 打开 `WsfSolarTerminator.cpp`，定位匿名命名空间（Line 26-100）获取私有辅助函数和常量。
   - 对每个函数：从 Doxygen 注释中提取功能描述，从函数体中提取算法步骤、条件分支、数学公式。
   - 识别依赖调用链：如 `MaskedByHorizon` 调用 `EllipsoidalInnerProduct` 和 `EllipsoidalFunction`。

3. **事件管理器分析**（第三步）
   - 打开 `WsfEclipseEventManager.hpp`，提取类结构、成员变量和内部类定义。
   - 打开 `WsfEclipseEventManager.cpp`，分析状态机逻辑：
     - `InitiateEclipseEvent()`：预测入影/出影时间并安排事件。
     - `EclipseEvent::Execute()`：事件触发时的状态迁移（cENTRY → cEXIT，cEXIT → cENTRY，cEVALUATE → cENTRY/cEXIT）。
   - 识别平台生命周期回调注册（`PlatformInitialized`、`PlatformDeleted`、`OrbitalManeuverUpdated`、`OrbitalManeuverCompleted`）。

4. **物理常量提取**（第四步）
   - 从 `UtSun.hpp` 提取太阳半径常量和函数声明。
   - 从 `UtEarth.hpp` 提取地球椭球参数。若 `UtEarth` 常量在其他头文件（如 `UtCentralBody.hpp`）中定义，则追踪引用链。

5. **跨文件调用链重建**（第五步）
   - 从 `GetPlatformSolarIllumination()` 向下追踪：`GetDisplacementToSolarLimbs()` → `UtSun::GetSunLocationWCS()` → `MaskedByHorizon()` → `EllipsoidalInnerProduct()` / `EllipsoidalFunction()`。
   - 从 `EclipseEvent::Execute()` 向下追踪：`GetPropagator().GetEclipseTimes()` → `WsfObserver::EclipseEntry/EclipseExit()`。
   - 将调用链整理为层次化的树状结构（见"源码使用说明"章节）。

##### function-index.jsonl 覆盖情况

该索引文件当前**未收录** `WsfSolarTerminator` 命名空间内的函数和 `WsfEclipseEventManager` 的方法。原因可能是索引构建时 `wsf_space` 模块尚未被完全扫描，或 solar terminator 相关函数被识别为工具函数而非核心算法。因此，本卡片的提取**完全基于直接阅读源文件**，而非依赖 function-index 的元数据。

##### 提取注意事项

- **匿名命名空间**：`EllipsoidalInnerProduct`、`EllipsoidalFunction`、`GetDisplacementToSolarLimbs` 三个函数位于 .cpp 文件的匿名命名空间中（`namespace {}`），是**翻译单元内部函数**，不会出现在头文件或符号导出表中。提取时必须直接阅读 .cpp 文件。
- **const vs constexpr**：注意区分编译期常量（`cTWILIGHT_CIVIL`、`cMASKED_BY_EARTH_TOLERANCE` 等 `constexpr`）和运行期常量（`cCOS_TWILIGHT_BEGIN` 为 `const double`，因其由 `cos()` 函数计算，无法在编译期求值）。
- **物理常量来源**：卡片中物理常量的数值注释来自源码中的 Doxygen 注释和代码内联注释（如 `UtSun.hpp` 中引用的 JPL 和 IAU 数据来源），提取时需同时记录来源文献，以便验证。
- **Enum Class 数值**：`PhaseOfDay` 枚举值从 1 开始（cDAY=1, cTWILIGHT=2, cNIGHT=3），`PlatformSolarIllumination` 枚举值从 0 开始（cINVALID_PLATFORM=0）。提取时不宜假设起始值，而应直接记录源码中的定义。

#### 可移植性评分

**可移植性**：高

**原因**：
1. 天光阶段判别仅为简单的余弦角阈值比较，与任何框架无关，可直接用任何语言实现。
2. 地球遮挡判定基于直线-椭球求交的二次方程，是标准解析几何方法，公式完全自包含，不依赖特殊框架组件。
3. 全影/半影判别利用太阳边缘点到观测者的视线遮挡判定组合，逻辑清晰，易于在其他仿真环境中复现。
4. EclipseEventManager 的调度逻辑（状态机 + 1/4 轨道周期再评估）高度依赖 AFSIM 的仿真事件调度框架（WsfEvent）和观察者模式（WsfObserver），但核心的地影预测逻辑（GetEclipseTimes）位于轨道外推器中，调度策略本身可简单模仿。
5. 算法依赖的物理常量（地球赤道/极半径、太阳平均半径、黄昏角度定义）均为公开标准值。
