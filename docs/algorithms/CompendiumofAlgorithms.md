# AFSIM 算法汇总文档

> **日期**：2026-07-27
> **状态**：持续提取中
> **说明**：本文档包含 32 项历史提取结果和当前候选账本流程新增的已验证算法；它不是全量 AFSIM 算法完成声明。当前候选与状态见 `workspace/algorithm-extraction/algorithm-coverage.jsonl`。

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

## 三、传感器与声学（Sensors and Acoustics）

### ALG-SENSORS-ACOUSTIC-ATMOSPHERIC-ABSORPTION：均匀大气声吸收

1. 算法英文名称：Uniform-Atmosphere Acoustic Absorption
2. 算法中文名称：均匀大气声吸收算法
3. 算法功能：依据路径中点的温度、相对湿度、压力比和频率，计算氧、氮分子弛豫及经典吸收合成的 dB/100 m 声衰减。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfAcousticSensor::AtmosphericAttenuation#14341903e4`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfAcousticSensor.cpp:648-676`
6. 算法对应卡片：[sensors-acoustic-atmospheric-absorption-card.md](sensors-acoustic-atmospheric-absorption-card.md)
7. 接口规格：[sensors-acoustic-atmospheric-absorption-interface-spec.md](../extracted-algorithms/acoustic-atmospheric-absorption/sensors-acoustic-atmospheric-absorption-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-ACOUSTIC-DETECTION-PROBABILITY：声学探测概率高斯近似

1. 算法英文名称：Acoustic Detection-Probability Gaussian Approximation
2. 算法中文名称：声学探测概率高斯近似算法
3. 算法功能：将接收声级相对有效噪声和检测门限的裕量，通过标准正态累积分布多项式近似映射为探测概率。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfAcousticSensor::ComputeProbabilityOfDetection#867e4f1774`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfAcousticSensor.cpp:686-752`
6. 算法对应卡片：[sensors-acoustic-detection-probability-card.md](sensors-acoustic-detection-probability-card.md)
7. 接口规格：[sensors-acoustic-detection-probability-interface-spec.md](../extracted-algorithms/acoustic-detection-probability/sensors-acoustic-detection-probability-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-ACOUSTIC-DOPPLER-COEFFICIENT：声学 Doppler 频率系数

1. 算法英文名称：Acoustic Doppler Frequency Coefficient
2. 算法中文名称：声学 Doppler 频率系数算法
3. 算法功能：把收发两端沿视线速度和路径中点声速组合为频率倍率，并识别源码定义的超声速不可听条件。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfAcousticSensor::ComputeDopplerTerm#8805cb99d3`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfAcousticSensor.cpp:983-1026`
6. 算法对应卡片：[sensors-acoustic-doppler-coefficient-card.md](sensors-acoustic-doppler-coefficient-card.md)
7. 接口规格：[sensors-acoustic-doppler-coefficient-interface-spec.md](../extracted-algorithms/acoustic-doppler-coefficient/sensors-acoustic-doppler-coefficient-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-ACOUSTIC-GROUND-EFFECT：声学地面效应与反射干涉

1. 算法英文名称：Acoustic Ground Effect and Reflection Interference
2. 算法中文名称：声学地面效应与反射干涉算法
3. 算法功能：结合反射几何、湍流相干性、复地面阻抗、边界损失和直达/反射路径差，计算源码兼容的地面效应修正值。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfAcousticSensor::GroundEffectAttenuation#7f17591001`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfAcousticSensor.cpp:761-911`
6. 算法对应卡片：[sensors-acoustic-ground-effect-card.md](sensors-acoustic-ground-effect-card.md)
7. 接口规格：[sensors-acoustic-ground-effect-interface-spec.md](../extracted-algorithms/acoustic-ground-effect/sensors-acoustic-ground-effect-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-ACOUSTIC-AUDITORY-FILTER-WEIGHTING：三分之一倍频程听觉加权

1. 算法英文名称：One-Third-Octave Auditory Filter Weighting
2. 算法中文名称：三分之一倍频程听觉加权算法
3. 算法功能：使用固定 5×24 经验权重矩阵，对目标声谱或背景谱的相邻三分之一倍频程线性声级进行局部加权求和。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfAcousticSensor::ApplyFilterWeighting#e15d7f9c4e`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfAcousticSensor.cpp:584-628`
6. 算法对应卡片：[sensors-acoustic-auditory-filter-weighting-card.md](sensors-acoustic-auditory-filter-weighting-card.md)
7. 接口规格：[sensors-acoustic-auditory-filter-weighting-interface-spec.md](../extracted-algorithms/acoustic-auditory-filter-weighting/sensors-acoustic-auditory-filter-weighting-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-OTH-IONOSPHERIC-CHARACTERISTICS：OTH 电离层传播特性

1. 算法英文名称：OTH Ionospheric Propagation Characteristics
2. 算法中文名称：OTH 电离层传播特性算法
3. 算法功能：依据雷达纬度、年内日、太阳时、电离层峰值参数和载频，计算太阳几何、反射高度电子密度、临界/最低可用频率、最大入射角及球形地球单跳范围。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`OTH_Beam::ComputeIonosphericCharacteristics#2d5548a2cc`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfOTH_RadarSensor.cpp:1000-1089`
6. 算法对应卡片：[sensors-oth-ionospheric-characteristics-card.md](sensors-oth-ionospheric-characteristics-card.md)
7. 接口规格：[sensors-oth-ionospheric-characteristics-interface-spec.md](../extracted-algorithms/oth-ionospheric-characteristics/sensors-oth-ionospheric-characteristics-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-OPTICAL-GLIMPSE-ANGULAR-CDF：光学掠视角分离 Monte Carlo CDF

1. 算法英文名称：Optical Glimpse Angular-Separation Monte Carlo CDF
2. 算法中文名称：光学掠视角分离 Monte Carlo 累积分布算法
3. 算法功能：在方位/俯仰球面视场内独立抽样视线点和目标点，以 1° 分箱估计两者角分离的 181 节点累积分布。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`GlimpseProbability::ComputeProbabilityDistribution#a7048f096e`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfOpticalSensor.cpp:625-697`
6. 算法对应卡片：[sensors-optical-glimpse-angular-cdf-card.md](sensors-optical-glimpse-angular-cdf-card.md)
7. 接口规格：[sensors-optical-glimpse-angular-cdf-interface-spec.md](../extracted-algorithms/optical-glimpse-angular-cdf/sensors-optical-glimpse-angular-cdf-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-SAR-DWELL-TIME：SAR 方位分辨率驻留时间

1. 算法英文名称：SAR Resolution-Driven Dwell Time
2. 算法中文名称：SAR 方位分辨率驻留时间算法
3. 算法功能：由波长、斜距、速度、方位分辨率、斜视角和擦地角计算合成孔径驻留时间，并保留扫描背面哨兵与 1000 s 源码硬上限。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfSAR_Sensor::ComputeDwellTime#e973416337`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2133-2162`
6. 算法对应卡片：[sensors-sar-dwell-time-card.md](sensors-sar-dwell-time-card.md)
7. 接口规格：[sensors-sar-dwell-time-interface-spec.md](../extracted-algorithms/sar-dwell-time/sensors-sar-dwell-time-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-SAR-AZIMUTH-RESOLUTION：SAR 驻留时间反算方位分辨率

1. 算法英文名称：SAR Dwell-Time Azimuth Resolution
2. 算法中文名称：SAR 驻留时间反算方位分辨率算法
3. 算法功能：由 SAR 几何、载频、Doppler 展宽因子和驻留时间反算可达方位分辨率，并保留旧角分辨率路径、背面扫描和退化几何的 1000 m 源码哨兵。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfSAR_Sensor::ComputeAzimuthResolution#091f833369`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2192-2232`
6. 算法对应卡片：[sensors-sar-azimuth-resolution-card.md](sensors-sar-azimuth-resolution-card.md)
7. 接口规格：[sensors-sar-azimuth-resolution-interface-spec.md](../extracted-algorithms/sar-azimuth-resolution/sensors-sar-azimuth-resolution-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-SAR-CLUTTER-TO-NOISE-RATIO：SAR 地杂波噪声比

1. 算法英文名称：SAR Clutter-to-Noise Ratio
2. 算法中文名称：SAR 地杂波噪声比算法
3. 算法功能：计算地面分辨率单元等效 RCS，经 AFSIM 双程 RF 功率、脉冲压缩、脉冲积分、积分增益和调整因子得到线性 CNR。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfSAR_Sensor::ComputeCNR#1c885b981d`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2063-2129`
6. 算法对应卡片：[sensors-sar-clutter-to-noise-ratio-card.md](sensors-sar-clutter-to-noise-ratio-card.md)
7. 接口规格：[sensors-sar-clutter-to-noise-ratio-interface-spec.md](../extracted-algorithms/sar-clutter-to-noise-ratio/sensors-sar-clutter-to-noise-ratio-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-SAR-IMAGE-FIELD-OF-VIEW：SAR 图像尺寸视场反算

1. 算法英文名称：SAR Image-Size Field-of-View
2. 算法中文名称：SAR 图像尺寸视场反算算法
3. 算法功能：当用户指定 SAR 图像宽高并存在 cue 时，由图像中心、斜距、NED down 分量和俯角反算天线方位/俯仰视场，并更新图像中心状态。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfSAR_Sensor::ComputeFOV#e0203ca715`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2628-2688`
6. 算法对应卡片：[sensors-sar-image-field-of-view-card.md](sensors-sar-image-field-of-view-card.md)
7. 接口规格：[sensors-sar-image-field-of-view-interface-spec.md](../extracted-algorithms/sar-image-field-of-view/sensors-sar-image-field-of-view-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-SAR-GROUND-RANGE-RESOLUTION：SAR 距离向地距分辨率

1. 算法英文名称：SAR Ground-Range Resolution
2. 算法中文名称：SAR 距离向地距分辨率算法
3. 算法功能：由发射机脉宽或接收机带宽、脉冲压缩比和擦地角投影计算 SAR 距离向地距分辨率，并保留旧角分辨率路径。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfSAR_Sensor::ComputeGroundRangeResolution#ac1540f0b7`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2235-2261`
6. 算法对应卡片：[sensors-sar-ground-range-resolution-card.md](sensors-sar-ground-range-resolution-card.md)
7. 接口规格：[sensors-sar-ground-range-resolution-interface-spec.md](../extracted-algorithms/sar-ground-range-resolution/sensors-sar-ground-range-resolution-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-SAR-SLANT-RANGE-GRAZING：SAR 曲率地球斜距与擦地角

1. 算法英文名称：SAR Curved-Earth Slant Range and Grazing Angle
2. 算法中文名称：SAR 曲率地球斜距与擦地角算法
3. 算法功能：在球形地球几何下，由传感器高度、positive-down 俯角和有效地球半径倍数计算地面关注点斜距与擦地角。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfSAR_Sensor::ComputeSlantRange#bb0631eb2b`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2273-2338`
6. 算法对应卡片：[sensors-sar-slant-range-grazing-card.md](sensors-sar-slant-range-grazing-card.md)
7. 接口规格：[sensors-sar-slant-range-grazing-interface-spec.md](../extracted-algorithms/sar-slant-range-grazing/sensors-sar-slant-range-grazing-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-SAR-PRF-UNAMBIGUOUS-RANGE：SAR 非模糊距离 PRF 选择

1. 算法英文名称：SAR Unambiguous-Range PRF Selection
2. 算法中文名称：SAR 非模糊距离 PRF 选择算法
3. 算法功能：根据当前斜距选择位于非模糊距离边界内的脉冲重复频率；普通路径保留 0.9 裕度，约束图路径使用边界值。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfSAR_Sensor::ComputePRF#3eaf3fdd9f`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2165-2189`
6. 算法对应卡片：[sensors-sar-prf-unambiguous-range-card.md](sensors-sar-prf-unambiguous-range-card.md)
7. 接口规格：[sensors-sar-prf-unambiguous-range-interface-spec.md](../extracted-algorithms/sar-prf-unambiguous-range/sensors-sar-prf-unambiguous-range-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-SAR-ONE-M2-CALIBRATION：SAR 1 m² 目标自由空间校准

1. 算法英文名称：SAR One-Square-Meter Calibration
2. 算法中文名称：SAR 1 m² 目标自由空间校准算法
3. 算法功能：用单基地自由空间雷达方程在 1 m² 检测距离和接收机噪声功率之间互算，并计算当前配置对应的自由空间检测距离。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfSAR_Sensor::Calibrate#7f7c2eeadf`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2704-2843`
6. 算法对应卡片：[sensors-sar-one-m2-calibration-card.md](sensors-sar-one-m2-calibration-card.md)
7. 接口规格：[sensors-sar-one-m2-calibration-interface-spec.md](../extracted-algorithms/sar-one-m2-calibration/sensors-sar-one-m2-calibration-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-LADAR-PLANCK-SPECTRAL-RADIANT-EMITTANCE：LADAR 普朗克谱辐射出射度

1. 算法英文名称：LADAR Planck Spectral Radiant Emittance
2. 算法中文名称：LADAR 普朗克谱辐射出射度
3. 算法功能：按源码常数和 `expm1` 数值稳定分母，计算指定温度及微米波长的黑体谱辐射出射度。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfLADAR_Sensor::SpectralRadiantEmittance#e62bac53c9`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfLADAR_Sensor.cpp:205-232`
6. 算法对应卡片：[sensors-ladar-planck-spectral-radiant-emittance-card.md](sensors-ladar-planck-spectral-radiant-emittance-card.md)
7. 接口规格：[sensors-ladar-planck-spectral-radiant-emittance-interface-spec.md](../extracted-algorithms/ladar-planck-spectral-radiant-emittance/sensors-ladar-planck-spectral-radiant-emittance-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-LADAR-BACKGROUND-RADIANCE：LADAR 黑体背景谱辐照度初始化

1. 算法英文名称：LADAR Blackbody Background Radiance Initialization
2. 算法中文名称：LADAR 黑体背景谱辐照度初始化
3. 算法功能：仅在背景温度为正时，以接收机波长调用普朗克谱量并按源码 $10^6$ 步骤写入背景谱辐照度状态。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfLADAR_Sensor::ComputeBackgroundRadiance#5c2a42d009`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfLADAR_Sensor.cpp:234-244`
6. 算法对应卡片：[sensors-ladar-background-radiance-card.md](sensors-ladar-background-radiance-card.md)
7. 接口规格：[sensors-ladar-background-radiance-interface-spec.md](../extracted-algorithms/ladar-background-radiance/sensors-ladar-background-radiance-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-LADAR-TARGET-SOLAR-IRRADIANCE：LADAR 目标太阳反射谱辐照度

1. 算法英文名称：LADAR Target Solar Irradiance
2. 算法中文名称：LADAR 目标太阳反射谱辐照度
3. 算法功能：用背景谱辐照度、目标面积与反射率、单程传输率和距离平方计算接收端太阳噪声谱辐照度。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfLADAR_Sensor::ComputeTargetSolarIrradiance#ad32e21a39`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfLADAR_Sensor.cpp:259-281`
6. 算法对应卡片：[sensors-ladar-target-solar-irradiance-card.md](sensors-ladar-target-solar-irradiance-card.md)
7. 接口规格：[sensors-ladar-target-solar-irradiance-interface-spec.md](../extracted-algorithms/ladar-target-solar-irradiance/sensors-ladar-target-solar-irradiance-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-LADAR-GAUSSIAN-DETECTION-PROBABILITY：LADAR Gaussian 探测概率近似

1. 算法英文名称：LADAR Gaussian Detection Probability Approximation
2. 算法中文名称：LADAR Gaussian 探测概率近似
3. 算法功能：按源码给出的分段多项式近似，将光子计数 S/N 相对阈值的裕量映射为探测概率。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfLADAR_Sensor::ComputeGaussianDetectionProbability#a63ba7cb81`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfLADAR_Sensor.cpp:638-681`
6. 算法对应卡片：[sensors-ladar-gaussian-detection-probability-card.md](sensors-ladar-gaussian-detection-probability-card.md)
7. 接口规格：[sensors-ladar-gaussian-detection-probability-interface-spec.md](../extracted-algorithms/ladar-gaussian-detection-probability/sensors-ladar-gaussian-detection-probability-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-LADAR-DETECTION-PROBABILITY-SELECTION：LADAR 探测概率选择与噪声功率换算

1. 算法英文名称：LADAR Detection Probability Selection
2. 算法中文名称：LADAR 探测概率选择与噪声功率换算
3. 算法功能：由信号/噪声光子计数计算 S/N 和接收机噪声功率，并按查表优先、Gaussian 回退规则确定探测概率。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfLADAR_Sensor::ComputeProbabilityOfDetection#04d3a9fa19`，`afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfLADAR_Sensor.cpp:601-627`
6. 算法对应卡片：[sensors-ladar-detection-probability-selection-card.md](sensors-ladar-detection-probability-selection-card.md)
7. 接口规格：[sensors-ladar-detection-probability-selection-interface-spec.md](../extracted-algorithms/ladar-detection-probability-selection/sensors-ladar-detection-probability-selection-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-OPTICAL-CURVED-EARTH-PATH-HEIGHT：光学路径球形地球高度

1. 算法英文名称：Optical Curved-Earth Path Height
2. 算法中文名称：光学路径球形地球高度
3. 算法功能：以球形地球两端半径、总斜距和路径距离两次应用余弦定理，计算光学积分路径任一点的 MSL 高度。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`Integrand::Height#1312e6167f`，`afsim-2_9/swdev/src/core/wsf_mil/source/WsfOpticalPath.cpp:176-193`
6. 算法对应卡片：[sensors-optical-curved-earth-path-height-card.md](sensors-optical-curved-earth-path-height-card.md)
7. 接口规格：[sensors-optical-curved-earth-path-height-interface-spec.md](../extracted-algorithms/optical-curved-earth-path-height/sensors-optical-curved-earth-path-height-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-OPTICAL-BOX-PROJECTED-AREA：光学长方体投影面积

1. 算法英文名称：Optical Box Projected Area
2. 算法中文名称：光学长方体投影面积
3. 算法功能：在无显式光学签名且平台长宽高均有效时，以视线方位/俯仰余弦计算三个正交面投影面积之和。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfOpticalSignature::GetValue#6d56123998`，`afsim-2_9/swdev/src/core/wsf_mil/source/WsfOpticalSignature.cpp:166-222`
6. 算法对应卡片：[sensors-optical-box-projected-area-card.md](sensors-optical-box-projected-area-card.md)
7. 接口规格：[sensors-optical-box-projected-area-interface-spec.md](../extracted-algorithms/optical-box-projected-area/sensors-optical-box-projected-area-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-OPTICAL-LAYERED-SIMPLE-ATTENUATION：光学分层简单大气透过率

1. 算法英文名称：Optical Layered Simple Attenuation
2. 算法中文名称：光学分层简单大气透过率
3. 算法功能：按 1000 m 高度层的平均相对大气密度，将海平面消光系数离散积分为简单平地路径透过率。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfOpticalAttenuation::ComputeSimpleAttenuation#95cb075c59`，`afsim-2_9/swdev/src/core/wsf_mil/source/WsfOpticalAttenuation.cpp:298-363`
6. 算法对应卡片：[sensors-optical-layered-simple-attenuation-card.md](sensors-optical-layered-simple-attenuation-card.md)
7. 接口规格：[sensors-optical-layered-simple-attenuation-interface-spec.md](../extracted-algorithms/optical-layered-simple-attenuation/sensors-optical-layered-simple-attenuation-interface-spec.md)
8. 验证状态：verified

### ALG-AERODYNAMICS-BODY-TOTAL-DRAG-COEFFICIENT：气动体总阻力系数

1. 算法英文名称：Aero Body Total Drag Coefficient
2. 算法中文名称：气动体总阻力系数
3. 算法功能：由迎角/侧滑姿态阻力、升力和侧力诱导阻力、表面摩擦及 Mach 外形阻力汇总机体无量纲阻力系数。
4. 算法所属模块：`mover_creator/source`
5. 核心源码证据：`AeroBody::CalcDragCoefficient#afedea7029`，`afsim-2_9/swdev/src/mover_creator/source/AeroBody.cpp:293-319`
6. 算法对应卡片：[aerodynamics-body-total-drag-coefficient-card.md](aerodynamics-body-total-drag-coefficient-card.md)
7. 接口规格：[aerodynamics-body-total-drag-coefficient-interface-spec.md](../extracted-algorithms/aero-body-total-drag-coefficient/aerodynamics-body-total-drag-coefficient-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-ESA-TAYLOR-DISTRIBUTION-WEIGHTS：ESA Taylor 阵元幅度加权

1. 算法英文名称：ESA Taylor Distribution Weights
2. 算法中文名称：ESA Taylor 阵元幅度加权算法
3. 算法功能：分别生成阵面 X/Y 方向的离散 Taylor 权重，峰值归一化后按 AFSIM 顺序量化二维阵元权重与轴向权重。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfESA_AntennaPattern::ComputeDistributionWeights#9a5cd098f9`，`afsim-2_9/swdev/src/core/wsf_mil/source/WsfESA_AntennaPattern.cpp:303-437`
6. 算法对应卡片：[sensors-esa-taylor-distribution-weights-card.md](sensors-esa-taylor-distribution-weights-card.md)
7. 接口规格：[sensors-esa-taylor-distribution-weights-interface-spec.md](../extracted-algorithms/esa-taylor-distribution-weights/sensors-esa-taylor-distribution-weights-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-ESA-WEIGHTED-ARRAY-FACTOR：ESA 加权相控阵阵因子

1. 算法英文名称：ESA Weighted Phased-Array Factor
2. 算法中文名称：ESA 加权相控阵阵因子算法
3. 算法功能：对带幅度权重的阵元位置执行电子转向相位量化和复数远场求和，按阵元总数平方归一化为线性功率阵因子。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfESA_AntennaPattern::ComputeArrayFactor#0e651783ae`，`afsim-2_9/swdev/src/core/wsf_mil/source/WsfESA_AntennaPattern.cpp:440-498`
6. 算法对应卡片：[sensors-esa-weighted-array-factor-card.md](sensors-esa-weighted-array-factor-card.md)
7. 接口规格：[sensors-esa-weighted-array-factor-interface-spec.md](../extracted-algorithms/esa-weighted-array-factor/sensors-esa-weighted-array-factor-interface-spec.md)
8. 验证状态：verified

### ALG-SENSORS-ESA-APERTURE-EFFICIENCY：ESA 幅度权重孔径效率

1. 算法英文名称：ESA Amplitude-Weight Aperture Efficiency
2. 算法中文名称：ESA 幅度权重孔径效率算法
3. 算法功能：由 X/Y 轴权重和已包含量化、随机失效的二维阵元权重，计算轴向及总归一化孔径效率。
4. 算法所属模块：`core/wsf_mil`
5. 核心源码证据：`WsfESA_AntennaPattern::ComputeApertureEfficiency#5c73ecce1d`，`afsim-2_9/swdev/src/core/wsf_mil/source/WsfESA_AntennaPattern.cpp:609-649`
6. 算法对应卡片：[sensors-esa-aperture-efficiency-card.md](sensors-esa-aperture-efficiency-card.md)
7. 接口规格：[sensors-esa-aperture-efficiency-interface-spec.md](../extracted-algorithms/esa-aperture-efficiency/sensors-esa-aperture-efficiency-interface-spec.md)
8. 验证状态：verified

---

## 算法统计

| 分类 | 算法数量 | 算法名称 |
|------|---------|---------|
| 飞行动力学 (wsf_p6dof, 旧模块) | 4 | P6DOF Heun 积分器, 稳定性导数气动模型, 角速率限制执行机构, 编队三状态机动控制 |
| 飞行动力学 (wsf_six_dof, 新模块) | 12 | 刚体积分器, PointMass 积分器, PointMass SAS, RigidBody 气动, PointMass 气动, 推进燃油, 喷气发动机, 自动驾驶仪 PID, 角速率限制执行机构, 一阶滞后执行机构, 编队三状态机动控制 |
| 飞行动力学 (跨模块) | 3 | 角速率限制执行机构（p6dof + six_dof）, 编队三状态机动控制（p6dof + six_dof）, 稳定性导数气动模型（p6dof + six_dof） |
| 空间/轨道力学 | 19 | 姿态定向, 多级火箭, JPL DE 历表, J2 摄动, 月球第三体, Walker 星座, NORAD 传播器, 数值积分传播器, 轨道事件条件, Lambert, 仅角度 IOD, 分段指数大气, Jacchia-Roberts 大气, NASA 碎片, 轨道机动, 交会瞄准, 拉格朗日点, 交会判别, 太阳终结线 |
| 传感器/声学 (`core/wsf_mil`) | 26 | 均匀大气声吸收, 声学探测概率高斯近似, 声学 Doppler 频率系数, 声学地面效应与反射干涉, 三分之一倍频程听觉加权, OTH 电离层传播特性, 光学掠视角分离 CDF, SAR 驻留时间, SAR 方位分辨率, SAR 地杂波噪声比, SAR 图像视场反算, SAR 地距分辨率, SAR 斜距与擦地角, SAR PRF 选择, SAR 1 m² 校准, LADAR 普朗克谱辐射, LADAR 背景谱辐照度, LADAR 太阳反射谱辐照度, LADAR Gaussian 探测概率, LADAR 探测概率选择, 光学球面路径高度, 光学长方体投影面积, 光学分层简单透过率, ESA Taylor 幅度加权, ESA 加权阵因子, ESA 孔径效率 |
| **合计** | **59** | |

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
| 均匀大气声吸收 | **高** | 核心为无状态标量公式；只需把 AFSIM 大气采样替换为显式 SI 输入 |
| 声学探测概率高斯近似 | **极高** | 无状态分段标量函数，仅依赖指数运算；需确认是否保留非正 dB 信号早退语义 |
| 声学 Doppler 频率系数 | **极高** | 两个视线速度投影和一个标量比值；需按调用者乘法解释倍率 |
| 声学地面效应与反射干涉 | 中 | 复数核心可移植，但反射几何、地形/地表与返回值单位存在阻塞性疑点 |
| 三分之一倍频程听觉加权 | **高** | 固定短窗加权与谱采样回调易解耦；经验权重和线性声级单位需追溯 |
| OTH 电离层传播特性 | 中高 | 标量核心易迁移；当地太阳时、夜侧不稳定链和最小距离反三角定义域必须显式处理 |
| 光学掠视角分离 CDF | 中高 | 球面采样与分箱易迁移；逐位兼容取决于标准库实数随机映射和 float 累计语义 |
| SAR 方位分辨率驻留时间 | **极高/中** | 公式极简；背面哨兵、1000 s 硬上限和调用者二次裁剪需要保持调用契约 |
| SAR 驻留时间反算方位分辨率 | **极高/中** | 闭式标量公式易迁移；旧角分辨率路径、背面门禁和 1000 m 哨兵需保留兼容语义 |
| SAR 地杂波噪声比 | 中 | RCS 与脉冲积分链可迁移；双程 RF 功率、临时地面目标和噪声模型强依赖 AFSIM |
| SAR 图像尺寸视场反算 | 中 | 三角反算核心简单；cue、WCS/NED 转换、地形中心修正和天线写回耦合框架 |
| SAR 距离向地距分辨率 | **高** | 纯标量公式；参数来源于发射机、接收机和旧配置路径 |
| SAR 曲率地球斜距与擦地角 | **高** | 球面三角公式自包含；有效地球半径倍数需从 AFSIM 配置映射 |
| SAR 非模糊距离 PRF 选择 | **极高** | 一行非模糊距离公式；需保留 0.9 裕度和 `2R+1` 分母保护 |
| SAR 1 m² 目标自由空间校准 | 中高 | 标准双程雷达方程；初始化时写回接收机噪声功率的副作用需显式处理 |
| ESA Taylor 阵元幅度加权 | **高** | 离散公式自包含；需保留功率比语义、向零截断及二维先量化的更新顺序 |
| ESA 加权相控阵阵因子 | **高/中** | 平面阵列复数和易迁移；零频率回退和非平面 Z 相位差异需显式兼容策略 |
| ESA 幅度权重孔径效率 | **极高** | 纯标量归约；100% 失效的全零权重必须用状态替代源码 NaN |
