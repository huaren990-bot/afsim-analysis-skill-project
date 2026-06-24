# AFSIM 算法汇总文档

> **日期**：2026-06-11
> **状态**：draft
> **说明**：本文档汇总了从 AFSIM 源代码中提取的所有算法模型。每个算法对应一张独立的算法卡片。

---

## 一、飞行动力学（Flight Dynamics）

### 1A. wsf_p6dof（拟六自由度飞行器运动学插件 -- 旧模块）

### P6DOF Heun 修正欧拉积分器
1. 算法英文名称：P6DOF Heun's Modified Euler Integrator
2. 算法中文名称：P6DOF Heun 修正欧拉积分器
3. 算法功能：对飞行器/导弹在三维空间中的平移和旋转运动进行时间推进，采用 Heun 预测-校正法（二阶 RK）+ 四元数姿态积分
4. 算法所属模块：wsf_p6dof（拟六自由度飞行器运动学插件 -- 旧模块）
5. 算法对应卡片：[flight-dynamics-p6dof-heun-integrator-card.md](flight-dynamics-p6dof-heun-integrator-card.md)

### P6DOF 稳定性导数气动模型
1. 算法英文名称：P6DOF Stability-Derivative Aerodynamic Coefficient Model
2. 算法中文名称：P6DOF 稳定性导数气动系数模型
3. 算法功能：基于稳定性导数查表计算气动六分量（升力/阻力/侧力/滚转/俯仰/偏航力矩），支持单变量和多维查表
4. 算法所属模块：wsf_p6dof（拟六自由度飞行器运动学插件 -- 旧模块）
5. 算法对应卡片：[flight-dynamics-aero-coefficient-model-card.md](flight-dynamics-aero-coefficient-model-card.md)

### 1B. wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）

### 刚体六自由度积分器
1. 算法英文名称：Rigid Body Six-DOF Heun Predictor-Corrector Integrator
2. 算法中文名称：刚体六自由度 Heun 预测-校正积分器
3. 算法功能：标准刚体六自由度运动积分，使用 Heun 预测-校正法 + 四元数姿态积分 + 欧拉转动方程（含转动惯量张量），支持力/力矩限幅和简单偏航阻尼器
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-rigid-body-integrator-card.md](flight-dynamics-rigid-body-integrator-card.md)

### PointMass 六自由度 Heun 积分器
1. 算法英文名称：PointMass Six-DOF Heun Integrator
2. 算法中文名称：PointMass 六自由度 Heun 积分器
3. 算法功能：对点质飞行器模型进行 Heun 预测-校正法六自由度时间推进（平动 + 转动 + 半隐式欧拉法），含 1000G 平动限幅和燃油消耗更新
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-pointmass-integrator-card.md](flight-dynamics-pointmass-integrator-card.md)

### PointMass 稳定增稳系统 (SAS)
1. 算法英文名称：PointMass Stability Augmentation System (SAS)
2. 算法中文名称：PointMass 稳定增稳系统
3. 算法功能：控制-稳定解耦的旋转角加速度模型：控制项（一阶指令跟踪）+ 稳定项（俯仰/偏航二阶临界阻尼 + 一阶滚转滞后），各通道独立限幅
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-pointmass-sas-card.md](flight-dynamics-pointmass-sas-card.md)

### RigidBody 稳定性导数气动系数模型
1. 算法英文名称：RigidBody Stability-Derivative Aerodynamic Coefficient Model
2. 算法中文名称：RigidBody 稳定性导数气动系数模型
3. 算法功能：基于飞行状态（马赫数/攻角/侧滑角/角速率/攻角变化率/侧滑角变化率），通过高维查表获取稳定性导数，将静态 3D 表项与动态阻尼增量线性叠加后乘以动压、参考面积和参考长度，得到有量纲六分量气动力和力矩。支持简化频率无量纲化、显式参考面积和多模态切换
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-rigidbody-aero-coefficient-card.md](flight-dynamics-rigidbody-aero-coefficient-card.md)

### PointMass 气动力与旋转限幅模型
1. 算法英文名称：PointMass Aerodynamics Model with Rotation Authority and Stabilizing Frequency
2. 算法中文名称：PointMass 气动力与旋转限幅模型
3. 算法功能：PointMass 专属气动模型——在标准气动力基础上叠加非配平操纵面效果（减速板/襟翼/扰流板），并输出旋转加速度限幅基准和稳定化频率基准。旋转加速度限幅随总迎角衰减（cos alpha_total），模拟大迎角下操纵效能丧失
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-pointmass-aero-card.md](flight-dynamics-pointmass-aero-card.md)

### 推进系统与燃油管理模型
1. 算法英文名称：Propulsion System and Fuel Management Model
2. 算法中文名称：推进系统与燃油管理模型
3. 算法功能：多发动机推进系统燃油管理——含燃油消耗率限制、多油箱间燃油传输比例协调、CG 位置线性插值（fuel fraction 插值）、百分比统一加油和总质量属性汇总
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-propulsion-fuel-card.md](flight-dynamics-propulsion-fuel-card.md)

### 喷气发动机推力模型
1. 算法英文名称：Jet Engine Thrust Model with Spool Dynamics
2. 算法中文名称：喷气发动机推力模型（含转速加减速动特性）
3. 算法功能：三层查表（Idle/Mil/AB）+ 油门转速加减速动特性（spool dynamics），模拟发动机从慢车到军推到加力的瞬态响应。含有效有效 TSFC 燃油消耗计算、熄火保护和进气口阻力
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-jet-engine-card.md](flight-dynamics-jet-engine-card.md)

### 自动驾驶仪 PID 嵌套回路控制
1. 算法英文名称：Autopilot PID Nested-Loop Control with Gain Scheduling
2. 算法中文名称：自动驾驶仪 PID 嵌套回路控制（含增益调度）
3. 算法功能：Bank-To-Turn/Yaw-To-Turn 自动驾驶仪——通过 20 个 PID 控制器组成三通道（垂直/横向/速度）嵌套反馈回路，支持增益调度、抗积分饱和（Kt anti-windup + 误差阈值死区）、低通滤波导数、前馈偏置和 α/β g-load 限幅
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-autopilot-pid-card.md](flight-dynamics-autopilot-pid-card.md)

### 角速率限制执行机构模型
1. 算法英文名称：Angular Rate-Limited Control Surface Actuator Model
2. 算法中文名称：舵机角速率限制执行机构模型
3. 算法功能：模拟真实舵机的有限角速率驱动——以最大正向/反向角速率将舵面从当前角度驱动到指令角度，受机械止动角约束。P6DOF 和刚体六自由度模块共用相同算法
4. 算法所属模块：wsf_p6dof 和 wsf_six_dof（飞行器运动学插件）
5. 算法对应卡片：[flight-dynamics-rate-limited-actuator-card.md](flight-dynamics-rate-limited-actuator-card.md)

### 一阶滞后滤波执行机构模型
1. 算法英文名称：First-Order Lag Filter Actuator Model
2. 算法中文名称：一阶滞后滤波执行机构模型
3. 算法功能：点质模型专属——通过一阶滞后滤波（隐式欧拉离散化）将飞控系统的归一化指令设定值平滑为实际控制面偏度百分比。输出范围为 [0,1]
4. 算法所属模块：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
5. 算法对应卡片：[flight-dynamics-first-order-lag-actuator-card.md](flight-dynamics-first-order-lag-actuator-card.md)

### 编队汇合/位置保持/追击三状态机动控制
1. 算法英文名称：Formation Form-Up / Station Keeping / Pursue Three-State Maneuver Control
2. 算法中文名称：编队汇合/位置保持/追击三状态机动控制
3. 算法功能：编队飞行中追击者的三状态自主机动控制——FormUp（远距离飞向目标）、KeepStation（ECS 坐标系 P+D+DD 偏差精细控制）、Pursue（圆形航迹模型追击），自动状态转移含防抖计数
4. 算法所属模块：wsf_p6dof 和 wsf_six_dof（飞行器运动学插件）
5. 算法对应卡片：[flight-dynamics-station-keeping-card.md](flight-dynamics-station-keeping-card.md)

---

## 二、空间/轨道力学（Space / Orbital Mechanics）

### 航天器姿态定向算法系统
1. 算法英文名称：Spacecraft Orientation Algorithm System (11 Attitude Modes)
2. 算法中文名称：航天器姿态定向算法系统（11 种卫星姿态模式）
3. 算法功能：基于 DCM（方向余弦矩阵）+ IEEE 1278.1-1995 DIS 欧拉角提取，提供 11 种航天器姿态定向模式——Nadir对地、Solar对日、Velocity速度矢量、Entity目标追踪、OrbitPlane轨道面约束，含 X-aligned / Z-aligned 双指向轴约定和铰接部件通用姿态计算
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-orientation-algorithms-card.md](space-orientation-algorithms-card.md)

### 多级火箭——齐奥尔科夫斯基方程与分级管理
1. 算法英文名称：Multi-Stage Rocket — Tsiolkovsky Equation and Staging Management
2. 算法中文名称：多级火箭——齐奥尔科夫斯基方程与分级管理
3. 算法功能：基于齐奥尔科夫斯基火箭方程计算多级火箭的推力、ΔV、燃耗时间关系。支持多级串联火箭的自动分级管理（staging），每级独立配置推力/燃耗率/比冲/排气速度/质量属性
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-rocket-staging-card.md](space-rocket-staging-card.md)

### JPL 行星历表——切比雪夫多项式插值
1. 算法英文名称：JPL DE Planetary Ephemeris — Chebyshev Polynomial Interpolation
2. 算法中文名称：JPL 行星历表——切比雪夫多项式插值
3. 算法功能：读取 JPL DE 二进制历表文件（支持 DE102-DE438 共 21 个版本），通过切比雪夫多项式插值获取太阳系天体的 ICRF 位置和速度。含地月质心修正和 TDB 时间尺处理
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-de-ephemeris-card.md](space-de-ephemeris-card.md)

### 地球 J2 带谐项引力摄动
1. 算法英文名称：Earth J2 Zonal Harmonic Gravitational Perturbation
2. 算法中文名称：地球 J2 带谐项引力摄动
3. 算法功能：从 J2 引力势梯度推导 ECI 坐标系下的加速度扰动——在 WCS（地固非旋转）帧中计算 Legendre 多项式梯度 a = ∇U_J2，再纯旋转回 ECI 帧。支持 WGS84/EGM96 常数预设或手动指定 μ/J2/R
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-earth-j2-perturbation-card.md](space-earth-j2-perturbation-card.md)

### 月球第三体引力摄动
1. 算法英文名称：Moon Third-Body Gravitational Perturbation
2. 算法中文名称：月球第三体引力摄动
3. 算法功能：计算月球引力对地球轨道航天器的第三体摄动加速度——a_total = a_lunar_on_sc - a_lunar_on_earth（扣除 ECI 坐标系原点加速度）。月球位置支持默认模型（UtMoon + 四点三次样条插值）和 JPL DE 历表两大数据源
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-moon-third-body-card.md](space-moon-third-body-card.md)

### Walker 星座几何布局生成
1. 算法英文名称：Walker Constellation Geometry Layout Generation (Delta / Star / General)
2. 算法中文名称：Walker 星座几何布局生成（Delta / Star / General 三种模式）
3. 算法功能：基于 Walker 编队数学生成卫星星座几何布局——Walker Delta（RAAN 360° 分布）、Walker Star（RAAN 180° 分布）、General 通用布局（自定义 RAAN 范围和近点角相位差），所有轨道为圆轨道，含解体检测
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-walker-constellation-card.md](space-walker-constellation-card.md)

### NORAD SGP4/SDP4 轨道传播器
1. 算法英文名称：NORAD SGP4/SDP4 Orbital Propagator
2. 算法中文名称：NORAD SGP4/SDP4 轨道传播器
3. 算法功能：基于 TLE 双行根数输入，使用 SGP4/SDP4 解析模型对地球轨道卫星进行位置和速度预报，含 J2/J3/J4 摄动和日月引力摄动
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-norad-orbital-propagator-card.md](space-norad-orbital-propagator-card.md)

### 数值积分轨道传播器
1. 算法英文名称：Numerical Integration Orbital Propagator with Adaptive Runge-Kutta
2. 算法中文名称：自适应 Runge-Kutta 数值积分轨道传播器
3. 算法功能：使用 Prince-Dormand 8(7)13M 嵌入型 RK 方法对任意力模型下的轨道运动进行数值积分，含自适应步长控制和 FSAL 优化
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-integrating-propagator-card.md](space-integrating-propagator-card.md)

### 轨道事件条件
1. 算法英文名称：Orbital Event Condition — Bisection Root-Finding
2. 算法中文名称：轨道事件条件（二分搜索求根）
3. 算法功能：在轨道传播中寻找满足近地点/远地点/升交点/降交点/地影等几何条件的时刻，使用二分搜索在时间轴求根
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-orbital-event-condition-card.md](space-orbital-event-condition-card.md)

### Lambert 问题求解器
1. 算法英文名称：Lambert Problem Solver
2. 算法中文名称：Lambert 问题求解器
3. 算法功能：求解 Lambert 边界值问题——已知两个位置矢量和飞行时间，用 f/g 级数展开方法确定连接轨道和速度矢量
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-lambert-solver-card.md](space-lambert-solver-card.md)

### 仅角度初始轨道确定 (Angles-Only IOD)
1. 算法英文名称：Angles-Only Initial Orbit Determination
2. 算法中文名称：仅角度初始轨道确定
3. 算法功能：从两次传感器角度测量（方位/俯仰），通过 Gauss 方法迭代交替求解距离和速度，确定航天器初始轨道
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-angles-only-iod-card.md](space-angles-only-iod-card.md)

### 分段指数大气密度模型
1. 算法英文名称：Piecewise Exponential Atmosphere Model
2. 算法中文名称：分段指数大气密度模型
3. 算法功能：按高度分段的指数衰减大气密度模型——计算地球轨道任意位置的大气密度，模型简单计算快速
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-piecewise-exponential-atmosphere-card.md](space-piecewise-exponential-atmosphere-card.md)

### Jacchia-Roberts 大气密度模型
1. 算法英文名称：Jacchia-Roberts Atmosphere Model
2. 算法中文名称：Jacchia-Roberts 大气密度模型
3. 算法功能：高层大气高保真密度模型——含太阳 10.7 cm 辐射通量 (F10.7) 和地磁活动指数 (Kp) 修正，适用于轨道长期预报
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-jacchia-roberts-atmosphere-card.md](space-jacchia-roberts-atmosphere-card.md)

### NASA 卫星碎片解体模型
1. 算法英文名称：NASA Standard Satellite Breakup Model
2. 算法中文名称：NASA 标准卫星碎片解体模型
3. 算法功能：模拟卫星爆炸/碰撞解体事件，生成符合 NASA 统计分布的碎片云（含幂律尺寸分布、面质比分布、Delta-V 分布和动量守恒修正）
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-nasa-breakup-model-card.md](space-nasa-breakup-model-card.md)

### 经典轨道机动模型
1. 算法英文名称：Classical Orbital Maneuvers — Delta-V, Element Change, Hohmann Transfer
2. 算法中文名称：经典轨道机动模型（Delta-V 机动、轨道要素变更、Hohmann 转移）
3. 算法功能：瞬时 Delta-V 脉冲机动、偏心率/倾角/RAAN 变更、Hohmann 共面圆轨道最优转移
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-orbital-maneuvers-card.md](space-orbital-maneuvers-card.md)

### 轨道交会与拦截瞄准
1. 算法英文名称：Orbital Rendezvous and Intercept Targeting
2. 算法中文名称：轨道交会与拦截瞄准
3. 算法功能：以 Lambert 求解器为核心，在飞行时间范围内搜索最小化 ΔV 的最优交会/拦截转移轨道
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-rendezvous-targeting-card.md](space-rendezvous-targeting-card.md)

### 拉格朗日点计算
1. 算法英文名称：Libration Point Computation — Circular Restricted Three-Body Problem
2. 算法中文名称：拉格朗日点计算（限制性三体问题）
3. 算法功能：计算地-月/日-地系 L1-L5 拉格朗日点位置，含 Gamma 系数 Newton 迭代和 Halo 轨道近似
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-libration-point-card.md](space-libration-point-card.md)

### 轨道交会判别
1. 算法英文名称：Orbital Conjunction Assessment
2. 算法中文名称：轨道交会判别算法
3. 算法功能：对两个空间目标进行五级逐层交会判别：快速过滤器（近/远地点距离排除）、步进预测（轨道角步长推进）、最近点搜索（五次样条插值极值搜索）、相遇计算（协方差椭球求根 + Vallado 碰撞概率）、根收缩算法
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-conjunction-assessment-card.md](space-conjunction-assessment-card.md)

### 太阳终结线与地影分析
1. 算法英文名称：Solar Terminator and Eclipse Analysis
2. 算法中文名称：太阳终结线与地影分析算法
3. 算法功能：判断航天器照明状态，包含天光阶段判别（白天/黄昏/黑夜，基于太阳矢量 NED 余弦角）、地球椭球遮挡判断（直线-椭球二次方程求交）、全影/半影/光照区判别（太阳上下边缘独立遮挡判断）、EclipseEventManager 自动地影事件调度
4. 算法所属模块：wsf_space（空间/轨道力学）
5. 算法对应卡片：[space-solar-terminator-card.md](space-solar-terminator-card.md)

---

## 算法统计

| 分类 | 算法数量 | 算法名称 |
|------|---------|---------|
| 飞行动力学 (wsf_p6dof, 旧模块) | 4 | P6DOF Heun 积分器, 稳定性导数气动模型, 角速率限制执行机构, 编队三状态机动控制 |
| 飞行动力学 (wsf_six_dof, 新模块) | 12 | 刚体积分器, PointMass 积分器, PointMass SAS, RigidBody 气动, PointMass 气动, 推进燃油, 喷气发动机, 自动驾驶仪 PID, 角速率限制执行机构, 一阶滞后执行机构, 编队三状态机动控制 |
| 飞行动力学 (跨模块) | 3 | 角速率限制执行机构（p6dof + six_dof）, 编队三状态机动控制（p6dof + six_dof）, 稳定性导数气动模型（p6dof + six_dof） |
| 空间/轨道力学 | 19 | 姿态定向, 多级火箭, JPL DE 历表, J2 摄动, 月球第三体, Walker 星座, NORAD 传播器, 数值积分传播器, 轨道事件条件, Lambert, 仅角度 IOD, 分段指数大气, Jacchia-Roberts 大气, NASA 碎片, 轨道机动, 交会瞄准, 拉格朗日点, 交会判别, 太阳终结线 |
| **合计** | **32** | |

---

## 可移植性总览

| 算法 | 可移植性 | 关键因素 |
|------|---------|---------|
| P6DOF Heun 积分器 | 中 | 核心方法标准，但框架耦合重 |
| 稳定性导数气动模型 | 高/低 | 数学标准，数据表为各飞行器特有 |
| 刚体六自由度积分器 | 中 | 标准 Heun 框架 + 四元数积分，但强依赖六自由度框架 |
| PointMass 积分器 | 中/高 | Heun 预测-校正为标准二阶 RK 方法，与力模型解耦 |
| PointMass SAS | 中/高 | 控制-稳定解耦设计可用标准控制理论公式重实现 |
| RigidBody 稳定性导数气动 | 中 | 稳定性导数法为航空工程标准方法，但依赖多维查表和框架专属类 |
| PointMass 气动力与旋转限幅 | 高 | 核心算法仅 70 行基本数学运算，操纵面线性叠加和总迎角衰减律均极简 |
| 推进系统与燃油管理 | 高 | CG 线性插值和传输比例协调均为基本四则运算，无领域黑盒 |
| 喷气发动机推力模型 | 中 | Spool dynamics 为标准建模技术，但查表种类多（9 表 4 spin rate 格式）耦合重 |
| 自动驾驶仪 PID 嵌套回路控制 | 中 | PID 为标准控制算法，但嵌套回路架构和 20 个 PID 实例的组装耦合飞行器框架 |
| 角速率限制执行机构 | **高** | 核心仅条件判断+乘法+加法，两模块算法一致，无外部数学库依赖 |
| 一阶滞后滤波执行机构 | **高** | 一行隐式欧拉公式，输入输出均为无量纲值，无物理单位依赖 |
| 编队三状态机动控制 | 中 | 控制律简单（P+D+DD 线性组合），但与 AFSIM 坐标系（ECS/TurnCircle）耦合紧密，大量硬编码经验增益 |
| NORAD 传播器 | 中 | 核心公式公开，但 WGS72 常数和框架耦合 |
| 数值积分传播器 | **高** | PD78 Butcher 表为公开常数，模板化设计 |
| 轨道事件条件 | **高** | 二分搜索极其标准 |
| Lambert 求解器 | **高** | 标准航天动力学算法 |
| 仅角度 IOD | **高** | Gauss 方法变体，纯几何和代数运算 |
| 分段指数大气 | **高** | 纯数学公式，分段表参数公开 |
| Jacchia-Roberts 大气 | **高** | 经验系数表公开可查 (Jacchia 1977) |
| NASA 碎片模型 | **高** | 所有系数来自 NASA 公开文献 |
| 轨道机动模型 | **高** | 标准航天动力学公式 |
| 交会瞄准 | **高** | Lambert 求解器 + 一维代价函数优化 |
| 航天器姿态定向算法系统 | **高** | 核心算法（DCM构造+欧拉角提取）为航天标准方法，100%自包含矢量运算 |
| 多级火箭模型 | **高** | 齐奥尔科夫斯基方程为航天标准公式，仅基础代数运算 |
| JPL DE 行星历表 | **高** | Chebyshev多项式+NOVAS C 3.1标准算法，文件格式为JPL公开规范 |
| 地球 J2 摄动 | **极高** | 完全自包含的J2模型，标准天体力学梯度公式+公开常数(WGS84/EGM96) |
| 月球第三体摄动 | **高** | 标准第三天体摄动公式，与AFSIM框架解耦 |
| Walker 星座布局 | **高** | Walker编队数学为标准方法，RAAN/近点角线性分布+归一化 |
| 拉格朗日点 | **高** | 标准三体问题公式 |
| 轨道交会判别 | 中 | 核心公式标准（Vallado），但强依赖轨道外推器和样条插值框架 |
| 太阳终结线与地影分析 | **高** | 标准解析几何方法，直线-椭球求交自包含 |
