# 算法卡片 — 数值积分轨道传播器

> **状态**：draft
> **日期**：2026-06-11
> **索引证据**：function-index.jsonl (wsf_space, Propagate 为 math 标记), symbol-index.jsonl (WsfIntegratingPropagator 类)
> **关联文档**：space-norad-orbital-propagator-card.md, space-orbital-event-condition-card.md

### 基础资料

- **算法名称**：Numerical Integration Orbital Propagator with Adaptive Runge-Kutta（自适应 Runge-Kutta 数值积分轨道传播器）
- **算法所属模块**：wsf_space（空间/轨道力学模块）
- **算法功能**：使用嵌入型 Runge-Kutta 方法对航天器在任意力模型下的轨道运动进行数值积分。采用 Prince-Dormand 8(7) 13 阶段嵌入 Runge-Kutta 格式，配合自适应步长控制和误差估计，适用于高精度轨道预报、轨道机动仿真以及多体动力学场景。

### 算法流程

整个算法流程图如下：

```mermaid
flowchart TD
    A[开始: AdvanceToTime] --> step1[1. 输入: 初始轨道状态 + 目标时间 + 动力学模型]
    step1 --> step2[2. 确定积分方向: 根据目标时间的正负调整步长符号]
    step2 --> step3{3. 当前时间 < 目标时间?}
    step3 -->|是| step4[4. 若剩余时间小于当前步长, 截断步长到目标时间]
    step3 -->|否| F[结束: 返回最终轨道状态]
    step4 --> step5[5. TakeStep: 计算 13 阶段 RK 预测值]
    step5 --> step6[6. ComputeError: 用嵌入的 7 阶格式估算截断误差]
    step6 --> step7{7. 误差 < 容差?}
    step7 -->|是| step8[8. AdvanceState: 接受当前步, 更新轨道状态]
    step7 -->|否| step9{9. 调整尝试次数 > 最大限制?}
    step9 -->|否| step10[10. AdjustTimeStep: 根据误差缩小步长]
    step10 --> step5
    step8 --> step12[12. AdjustTimeStep: 根据误差调整下一步步长]
    step12 --> step3
```

其中，第一步接收初始轨道状态（含 ECI 位置、速度、加速度）和目标时间；第二步检测积分方向；第三步至第十二步为自适应步长控制的主循环；`TakeStep` 中依次计算 13 个阶段（含 FSAL 优化），每个阶段调用 `OrbitalDynamics::ComputeAcceleration()` 获取当前加速度；`ComputeError` 使用嵌入的 7 阶格式与 8 阶格式之差作为截断误差估计；`AdjustTimeStep` 根据误差与容差的比例缩放步长。

### 算法变量和常量

1. 输入 (input)：
   
   | 英文标识符 (Symbol)  | 中文名称 (Name) | 数据类型 (Type)               | 含义 (Meaning)                  | 单位 (Units)   | 所属函数 (Method)       |
   | --------------- | ----------- | ------------------------- | ----------------------------- | ------------ | ------------------- |
   | `aDynamics`     | 轨道动力学模型     | const WsfOrbitalDynamics& | 包含多个动力学项（引力、J2、太阳、月球等）的加速度计算器 | —            | Propagate |
   | `aFinalTime`    | 目标预报时间      | const UtCalendar&         | 需要预报到的最终时刻                    | —            | Propagate |
   | `aInitialState` | 初始轨道状态      | const ut::OrbitalState&   | 含 ECI 位置/速度/加速度的初始状态          | m, m/s, m/s² | Propagate |
   | `aMass`         | 航天器质量       | double                    | 用于加速度 = 力/质量 的计算              | kg           | Propagate |
   | `aPosition`     | ECI 位置      | const UtVec3d&            | 地心惯性系中的位置矢量                   | m            | Propagate |
   | `aVelocity`     | ECI 速度      | const UtVec3d&            | 地心惯性系中的速度矢量                   | m/s          | Propagate |

2. 输出 (output)：
   
   | 英文标识符 (Symbol)       | 中文名称 (Name) | 数据类型 (Type)      | 含义 (Meaning)         | 单位 (Units)   | 所属函数 (Method) |
   | -------------------- | ----------- | ---------------- | -------------------- | ------------ | ------------- |
   | `retval`             | 传播后的轨道状态    | ut::OrbitalState | 含预报时刻的 ECI 位置/速度/加速度 | m, m/s, m/s² | AdvanceToTime |
   | `mPredictedPosition` | 预测位置        | UtVec3d          | 当前步的 8 阶预测位置         | m            | Propagate |
   | `mPredictedVelocity` | 预测速度        | UtVec3d          | 当前步的 8 阶预测速度         | m/s          | Propagate |
   | `mPosDiff`           | 位置误差        | UtVec3d          | 8 阶与 7 阶格式的位置差       | m            | Propagate |
   | `mVelDiff`           | 速度误差        | UtVec3d          | 8 阶与 7 阶格式的速度差       | m/s          | Propagate |

3. 常量 (constant):
   
   | 英文标识符 (Symbol)           | 中文名称 (Name)         | 数据类型 (Type)                | 含义 (Meaning)        | 单位 (Units) | 所属函数 (Method)   |
   | ------------------------ | ------------------- | -------------------------- | ------------------- | ---------- | --------------- |
   | `cCVALUES[13]`           | Butcher 表 C 节点      | constexpr double[13]       | RK 各阶段的时间节点（0 到 1）  | 无量纲        | SetOrbitalIntegrator |
   | `cBVALUES[13]`           | Butcher 表 B 权重（8 阶） | constexpr double[13]       | 8 阶解的权重系数           | 无量纲        | SetOrbitalIntegrator |
   | `cERRORVALUES[13]`       | Butcher 表误差权重       | constexpr double[13]       | 7 阶嵌入解的权重系数（用于误差估计） | 无量纲        | SetOrbitalIntegrator |
   | `cAVALUES[13][12]`       | Butcher 表 A 系数      | constexpr double[13][12]   | 阶段间依赖矩阵（严格下三角）      | 无量纲        | SetOrbitalIntegrator |
   | `mTolerance`             | 误差容差                | double (default: 1e-10)    | 单步截断误差的允许上限         | m 或 m/s    | Propagate |
   | `mMaxStepSize`           | 最大步长                | double                     | 步长的硬上限              | s          | Propagate |
   | `mMinStepSize`           | 最小步长                | double                     | 步长的硬下限（0 表示无下限）     | s          | Propagate |
   | `mInitialStepSize`       | 初始步长                | double (default: 0.1)      | 首次积分时使用的步长          | s          | Propagate |
   | `mMaxAdjustmentAttempts` | 最大调整次数              | unsigned int (default: 50) | 单步中重试的最大次数          | 次          | Propagate |
   | `cORDER`                 | 主格式阶数               | constexpr (8)              | 8 阶 Runge-Kutta 格式  | —          | Propagate |

### 关键数学公式

1. **13 阶段显式 Runge-Kutta 格式**：
   Prince-Dormand 8(7)13M 是一种嵌入型显式 Runge-Kutta 方法。使用 13 次函数评估得到 8 阶解，同时利用嵌入的 7 阶解进行误差估计。
   
   第 $i$ 阶段的状态计算：
   
   $\mathbf{y}_i = \mathbf{y}_0 + h \sum_{j=0}^{i-1} a_{ij} \cdot \mathbf{k}_j$
   
   其中：
   
   - $\mathbf{y}_0$ 为初始状态 $(\mathbf{r}_0, \mathbf{v}_0)$。
   - $h$ 为当前步长。
   - $a_{ij}$ 为 Butcher 表系数（`cAVALUES[i][j]`）。
   - $\mathbf{k}_j = (\mathbf{v}_j, \mathbf{a}_j)$ 为第 $j$ 阶段的右端函数值。
   - $\mathbf{a}_j = \text{ComputeAcceleration}(mass, t_0 + c_j h, \mathbf{r}_j, \mathbf{v}_j)$ 为第 $j$ 阶段的加速度。
   
   12 个非零节点值 $c_i$：
   
   $c_1 = \frac{1}{18},\ c_2 = \frac{1}{12},\ c_3 = \frac{1}{8},\ c_4 = \frac{5}{16},\ c_5 = \frac{3}{8},\ c_6 = \frac{59}{400}$
   
   $c_7 = \frac{93}{200},\ c_8 = \frac{5490023248}{9719169821},\ c_9 = \frac{13}{20},\ c_{10} = \frac{1201146811}{1299019798},\ c_{11} = 1,\ c_{12} = 1$

2. **8 阶解与 7 阶嵌入解的加权组合**：
   最终解通过加权组合各阶段的右端函数值得到：
   
   $\mathbf{y}_{n+1}^{(8)} = \mathbf{y}_n + h \sum_{i=0}^{12} b_i \cdot \mathbf{k}_i$ （8 阶预测）
   
   $\mathbf{y}_{n+1}^{(7)} = \mathbf{y}_n + h \sum_{i=0}^{12} \hat{b}_i \cdot \mathbf{k}_i$ （7 阶嵌入解，仅用于误差估计）
   
   其中：
   
   - $b_i$ 为 8 阶权重（`cBVALUES`，如 $b_0 = \frac{14005451}{335480064}$, $b_{12} = \frac{1}{4}$）。
   - $\hat{b}_i = b_i + e_i$ 为 7 阶权重，$e_i$ 为误差系数（`cERRORVALUES`）。

3. **FSAL 优化（First Same As Last）**：
   由于 $c_{12} = c_{11} = 1$ 且 $b_{12} \neq 0$，该格式具有 FSAL 性质：当前步第 12 阶段的加速度 $\mathbf{a}_{12}$ 可直接作为下一步的 $\mathbf{k}_0$ 的加速度分量，省去一次函数评估。

4. **局部截断误差估计**：
   使用 8 阶和 7 阶解之差估计局部截断误差：
   
   $\Delta \mathbf{r} = \mathbf{r}_{n+1}^{(8)} - \mathbf{r}_{n+1}^{(7)} = h \sum_{i=0}^{12} (b_i - \hat{b}_i) \cdot \mathbf{v}_i$
   
   $\Delta \mathbf{v} = \mathbf{v}_{n+1}^{(8)} - \mathbf{v}_{n+1}^{(7)} = h \sum_{i=0}^{12} (b_i - \hat{b}_i) \cdot \mathbf{a}_i$
   
   支持两种误差范数：
   
   - **$L_\infty$ 范数**：$err = \max(\|\Delta \mathbf{r}\|_\infty, \|\Delta \mathbf{v}\|_\infty)$
   - **$L_2$ 范数**（默认）：$err = \max\left(\frac{\|\Delta \mathbf{r}\|_2}{\max(\|\mathbf{r}_{step}\|_2, 0.1)}, \frac{\|\Delta \mathbf{v}\|_2}{\max(\|\mathbf{v}_{step}\|_2, 0.1)}\right)$

5. **自适应步长控制**：
   根据误差与容差的比例调整步长，使用标准的最优步长公式：
   
   如果误差未通过（$err > tol$）：
   
   $h_{new} = 0.9 \cdot h \cdot \left(\frac{tol}{err}\right)^{\frac{1}{p-1}}$
   
   其中 $p = cORDER = 8$，故指数为 $\frac{1}{7}$。
   
   如果误差已通过（$err \leq tol$）：
   
   $h_{new} = 0.9 \cdot h \cdot \left(\frac{tol}{err}\right)^{\frac{1}{p}}$
   
   指数为 $\frac{1}{8}$。
   
   乘以 0.9 的安全因子避免步长过度振荡。调整后的步长被钳制在 $[h_{min}, h_{max}]$ 范围内。

6. **轨道动力学加速度合成**：
   传播器本身不实现物理模型，而是通过 `WsfOrbitalDynamics` 聚合多个 `WsfOrbitalDynamicsTerm` 来合成总加速度：
   
   $\mathbf{a}_{ECI} = \frac{1}{m} \sum_{k} \mathbf{F}_k(\mathbf{r}, \mathbf{v}, t)$
   
   典型的动力学项包括：
   
   - 地球中心引力：$\mathbf{a}_{Earth} = -\frac{\mu_E}{r^3} \mathbf{r}$
   - J2 摄动：包含 $J_2 \frac{R_E^2}{r^4}$ 项的加速度修正
   - 太阳/月球第三体引力：$\mathbf{a}_{3rd} = -\mu_{body} \left(\frac{\mathbf{r} - \mathbf{r}_{body}}{|\mathbf{r} - \mathbf{r}_{body}|^3} + \frac{\mathbf{r}_{body}}{r_{body}^3}\right)$
   - 大气阻力、太阳辐射压等非保守力

### 算法伪代码

```
// === 自适应步长 Runge-Kutta 轨道积分器 ===
// 整体目标：从初始轨道状态推进到目标时刻，精度由误差容差控制

function AdvanceToTime(aDynamics, aFinalTime, aInitialState):
    state = aInitialState.Copy()
    finalTime = aFinalTime - state.epoch
    currentTime = 0.0

    // 1. 检测积分方向
    if (finalTime < 0 and stepSize > 0) or (finalTime > 0 and stepSize < 0):
        stepSize = -stepSize

    // 2. 主积分循环
    while |currentTime| < |finalTime|:
        // 2a. 如果剩余时间小于当前步长，截断步长
        if |stepSize + currentTime| > |finalTime|:
            stepSize = finalTime - currentTime

        // 2b. 执行一步 13 阶段 RK
        TakeStep(aDynamics, state)
          → for i = 1 to 12:  // i=0 由 FSAL 提供
                // 构造第 i 阶段的预测状态
                y_pos = state.pos + h * Σ(a[i][j] * rhs_pos[j]) for j < i
                y_vel = state.vel + h * Σ(a[i][j] * rhs_vel[j]) for j < i
                // 计算第 i 阶段的右端函数
                rhs_pos[i] = y_vel
                rhs_vel[i] = aDynamics.ComputeAcceleration(mass, t0+c[i]*h, y_pos, y_vel)
            // 加权合成 8 阶预测和 7 阶对比值
            pred_pos = state.pos + h * Σ(b[i] * rhs_pos[i])
            pred_vel = state.vel + h * Σ(b[i] * rhs_vel[i])
            pos_diff = h * Σ(error_b[i] * rhs_pos[i])
            vel_diff = h * Σ(error_b[i] * rhs_vel[i])

        // 2c. 计算截断误差
        error = ComputeError(state)
          → if L_2:
                pos_err = |pos_diff|₂ / max(|Δpos|₂, 0.1)
                vel_err = |vel_diff|₂ / max(|Δvel|₂, 0.1)
                return max(pos_err, vel_err)
             if L_∞:
                return max(max|pos_diff|, max|vel_diff|)

        // 2d. 接受或拒绝当前步
        if error < tolerance:
            acceptStep = true
        else:
            attempts++
            acceptStep = false
            if attempts > maxAdjustmentAttempts:
                acceptStep = true  // 强制接受
                warn("Unable to find acceptable step size")

        // 2e. 如果接受，推进状态
        if acceptStep:
            state.epoch += stepSize
            state.pos = pred_pos     // 使用 8 阶解
            state.vel = pred_vel
            state.acceleration = rhs_vel[12]  // FSAL: 保存最后阶段的加速度
            attempts = 0
            currentTime += stepSize

        // 2f. 调整下一步长
        AdjustTimeStep(error)
          → if error > tol:
                h *= 0.9 * (tol/error)^(1/7)  // 拒绝，缩小步长
             else:
                h *= 0.9 * (tol/error)^(1/8)  // 接受，调整步长
             clamp |h| ∈ [minStepSize, maxStepSize]

    return state
```

### 源码使用说明

#### 入口和调用链

```
// 仿真引擎通过 WsfSpaceMover 驱动数值积分传播器
WsfSimulation::Update()                                          // AFSIM 仿真引擎主循环
  → WsfSpaceMoverBase::Update()                                 // 空间运动器更新
    → WsfIntegratingPropagator::Propagate(currentTime)          // 积分传播器入口
      → WsfOrbitalIntegrator::AdvanceToTime(dynamics, finalTime, initialState)
        // 自适应步长 RK 主循环
        → TakeStep(dynamics, state)  × N                    // 13 阶段 RK 推进
          → dynamics.ComputeAcceleration(mass, t, r, v) × 12 // 计算各阶段加速度
            → Σ term.ComputeAcceleration(mass, t, r, v)      // 合成所有动力学项
        → ComputeError()                                     // 嵌入格式误差估计
        → AdjustTimeStep(error)                              // 步长自适应控制
        → AdvanceState(state)                                // 状态更新
      → UpdateOrbitalState()                                 // 回写到基类
```

#### 源码位置

| File                                                                                                                     | Symbol                                | Lines   | Evidence level | 中文说明                                     |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------- | ------- | -------------- | ---------------------------------------- |
| [WsfIntegratingPropagator.hpp](source_root/src/core/wsf_space/source/WsfIntegratingPropagator.hpp)                       | `WsfIntegratingPropagator`            | 36-102  | source-cited   | 积分传播器主类 — 组装积分器 + 动力学模型                  |
| [WsfIntegratingPropagator.cpp](source_root/src/core/wsf_space/source/WsfIntegratingPropagator.cpp)                       | `Propagate()`                         | —       | source-cited   | 传播入口 — 调用积分器的 AdvanceToTime              |
| [WsfOrbitalIntegrator.hpp](source_root/src/core/wsf_space/source/WsfOrbitalIntegrator.hpp)                               | `WsfOrbitalIntegrator`                | 23-52   | source-cited   | 积分器抽象接口 — AdvanceToTime 纯虚函数             |
| [WsfRungeKuttaOrbitalIntegrator.hpp](source_root/src/core/wsf_space/source/WsfRungeKuttaOrbitalIntegrator.hpp)           | `AdvanceToTime()`                     | 150-215 | source-cited   | 自适应步长 RK 主循环 — 接受/拒绝步 + 步长调整             |
| [WsfRungeKuttaOrbitalIntegrator.hpp](source_root/src/core/wsf_space/source/WsfRungeKuttaOrbitalIntegrator.hpp)           | `TakeStep()`                          | 265-325 | source-cited   | 13 阶段 RK 推进 — Butcher 表计算 + FSAL         |
| [WsfRungeKuttaOrbitalIntegrator.hpp](source_root/src/core/wsf_space/source/WsfRungeKuttaOrbitalIntegrator.hpp)           | `ComputeError()`                      | 223-259 | source-cited   | 误差估计 — L₂ 和 L∞ 两种范数                      |
| [WsfRungeKuttaOrbitalIntegrator.hpp](source_root/src/core/wsf_space/source/WsfRungeKuttaOrbitalIntegrator.hpp)           | `AdjustTimeStep()`                    | 327-368 | source-cited   | 步长自适应 — 基于误差/容差比的步长缩放                    |
| [WsfPrinceDormand78OrbitalIntegrator.hpp](source_root/src/core/wsf_space/source/WsfPrinceDormand78OrbitalIntegrator.hpp) | `WsfPrinceDormand78OrbitalIntegrator` | 26-269  | source-cited   | PD 8(7) 系数 — 完整的 Butcher 表 (c, b, b̂, A) |
| [WsfOrbitalDynamics.hpp](source_root/src/core/wsf_space/source/WsfOrbitalDynamics.hpp)                                   | `WsfOrbitalDynamics`                  | 31-101  | source-cited   | 轨道动力学 — 多动力学项合成加速度                       |
| [WsfOrbitalDynamicsTerm.hpp](source_root/src/core/wsf_space/source/WsfOrbitalDynamicsTerm.hpp)                           | `WsfOrbitalDynamicsTerm`              | 31-89   | source-cited   | 动力学项抽象接口 — ComputeAcceleration 纯虚函数      |

#### 框架依赖

| AFSIM 原始依赖                                                 | 依赖类型        | 替换方案                                         |
| ---------------------------------------------------------- | ----------- | -------------------------------------------- |
| `WsfOrbitalIntegrator`                                     | 抽象积分器接口     | 自定义 `OrbitalIntegrator` 抽象类                  |
| `WsfRungeKuttaOrbitalIntegrator<Order, Steps, Integrator>` | 模板基类（核心算法）  | 可直接移植模板代码，Butcher 表用常量定义                     |
| `WsfOrbitalDynamics`                                       | 动力学模型容器     | 自定义 `DynamicsModel` 聚合类                      |
| `WsfOrbitalDynamicsTerm`                                   | 动力学项接口      | 自定义 `ForceModel` 抽象接口                        |
| `UtCalendar`                                               | 时间表示        | `double` (秒) 或 `std::chrono`                 |
| `UtOrbitalState / UtOrbitalStateVector`                    | 轨道状态容器      | 自定义 `OrbitalState` (pos + vel + acc + epoch) |
| `UtVec3d`                                                  | 三维矢量        | `Eigen::Vector3d`                            |
| `WsfNonClassicalOrbitalPropagator`                         | 基类          | 合并到自定义传播器基类中                                 |
| `WsfObject`                                                | 脚本系统基类（配置用） | 移除，直接用构造函数或 setter 配置参数                      |

#### 测试和验证计划

1. **单元测试 — 二体问题**：使用纯 Kepler 二体动力学（仅地球中心引力项），对比解析解（Kepler 方程），验证 8 阶收敛速度和精度。
2. **回归测试 — J2 摄动**：加入 J2 项，与 NORAD SGP4 在近地轨道上的预报结果对比（短弧段内）。
3. **精度验证**：改变容差（如 $10^{-8}$、$10^{-10}$、$10^{-12}$），验证误差与指定的容差一致。
4. **步长调整验证**：在椭圆轨道近地点（高加速度）和远地点（低加速度）处，步长应自动缩小/放大。
5. **边界测试**：零质量、零步长、反向积分、最大步长限制、最小步长限制。
6. **FSAL 验证**：确认每步的函数评估次数 = 12（而非 13）。

#### 可移植性评分

**可移植性**：高

**原因**：

1. Prince-Dormand 8(7)13M 的 Butcher 表系数是公开的数学常数（来自 Prince & Dormand, 1981），可直接复制到任何语言。
2. 自适应步长控制算法是标准方法（误差/容差比的分数次幂缩放），不依赖任何专有代码。
3. 核心算法已实现为 C++ 模板（`WsfRungeKuttaOrbitalIntegrator`），仅依赖 Butcher 系数（编译时常量），移植到其他语言非常直接。
4. 动力学模型通过抽象接口（`WsfOrbitalDynamicsTerm`）解耦——用户可自定义任意力模型，传播器不关心加速度的来源。
5. 框架耦合仅限于初始化/配置部分，核心积分器（RK 基类 + PD78 系数）几乎不依赖 AFSIM 基础设施。
