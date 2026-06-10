# AFSIM 功能说明（四层功能体系）

> **状态**：🔴 草稿 — 等待开发人员校对
> **日期**：2026-06-09
> **关联文档**：[afsim-architecture.md](afsim-architecture.md) | [module-dependency.md](module-dependency.md)

---

## 1. 功能划分

AFSIM 功能按四层体系组织：

| 层级 | 英文 | 定义 | 边界范围 | 对应索引 |
|------|------|------|----------|----------|
| **系统级** | System-level | 跨框架/域/插件层，组合多个模块完成的端到端业务能力 | 跨目录、跨子系统 | function-index level=System-level |
| **模块级** | Module-level | 在单一子系统/模块内，通过策略模式实现多变体的功能 | 同一目录或相邻目录 | function-index level=Module-level |
| **类级** | Class-level | 单个类（class）封装的职责集合 | 单个 .hpp + .cpp | function-index level=Class-level |
| **方法级** | Method-level | 单个函数/方法的具体算法实现 | 单个文件内的函数 | function-index level=Method-level |

---

## 2. 系统级功能分解

### 2.1 仿真生命周期管理（Simulation Lifecycle Management，仿真生命周期管理）

**简介**：控制仿真从启动到结束的完整七阶段生命周期，管理场景加载、对象创建、事件循环、结果输出和资源释放。
**对应子系统**：[仿真引擎系统](afsim-architecture.md) + [应用管理系统](afsim-architecture.md)

| 层级 | 功能名称 | 简介 |
|------|----------|------|
| 模块级 | 应用启动与配置（Application Bootstrap） | 解析命令行参数、创建 WsfApplication 单例、注册扩展和加载插件 |
| 模块级 | 场景加载与解析（Scenario Loading） | 从 .txt 输入文件解析平台类型/实例定义、环境配置、组件工厂注册 |
| 模块级 | 对象创建与初始化（Object Creation & Init） | 创建仿真实例、按初始化顺序例化所有平台及子系统组件 |
| 模块级 | 仿真循环调度（Simulation Loop） | 时间推进、事件队列管理、帧/事件步进调度 |
| 模块级 | 结果输出（Result Output） | 事件日志写入、CSV/二进制结果文件生成、外部接口通知 |
| 模块级 | 资源清理（Shutdown） | 平台销毁、仿真资源释放、插件卸载 |

### 2.2 平台运动与动力学（Platform Motion & Dynamics，平台运动与动力学）

**简介**：管理仿真实体在三维空间中的运动状态，包括位置、速度、姿态的计算和更新，及燃油消耗管理。
**对应子系统**：[运动模型系统](afsim-architecture.md) + [平台实体系统](afsim-architecture.md)

| 层级 | 功能名称 | 简介 |
|------|----------|------|
| 模块级 | 空气动力学运动（Aerodynamic Motion） | 固定翼/旋翼飞行器的气动力计算和六自由度运动积分 |
| 模块级 | 地面运动（Ground Motion） | 车辆/地面平台的地形跟随和轮式运动 |
| 模块级 | 水面/水下运动（Surface/Subsurface Motion） | 舰船/潜艇的运动模型 |
| 模块级 | 空间轨道运动（Orbital Motion） | 卫星/空间平台的轨道力学计算 |
| 模块级 | 制导运动（Guided Motion） | 导弹/制导武器的寻的运动和比例导引 |
| 模块级 | 燃油管理（Fuel Management） | 燃油消耗率计算、燃油质量对总质量的影响 |
| 模块级 | 平台质量计算（Mass Accounting） | 空重+燃油+载荷的总质量维护 |

### 2.3 传感器探测与跟踪（Sensor Detection & Tracking，传感器探测与跟踪）

**简介**：从电磁环境感知到目标跟踪建立的完整感知链路，包括信号检测、航迹关联、航迹融合和外推。
**对应子系统**：[传感器系统](afsim-architecture.md) + [电磁系统](afsim-architecture.md) + [跟踪系统](afsim-architecture.md)

| 层级 | 功能名称 | 简介 |
|------|----------|------|
| 模块级 | 电磁传播计算（EM Propagation） | 发射-接收路径损耗、大气衰减、多径效应计算 |
| 模块级 | 传感器信号检测（Sensor Signal Detection） | 基于信噪比/检测概率判断目标是否被感知 |
| 模块级 | 视场约束（Field of View） | 圆形/矩形/多边形/赤道视场范围内的目标筛选 |
| 模块级 | 航迹关联（Track Correlation） | 将新检测与已有航迹关联（最近邻/完美/真值关联） |
| 模块级 | 航迹融合（Track Fusion） | 多源航迹数据融合为单一本地航迹 |
| 模块级 | 航迹外推（Track Extrapolation） | 在无新检测时按运动模型外推航迹状态 |
| 模块级 | 航迹上报（Track Reporting） | 周期性/批量方式向其他平台或处理器上报航迹 |
| 模块级 | 目标特征管理（Signature Management） | 雷达散射截面（RCS）/红外/光学特征的维护和查询 |

### 2.4 武器交战与拦截（Weapon Engagement & Intercept，武器交战与拦截）

**简介**：从目标分配到武器发射再到拦截判定的完整杀伤链，支持多种武器类型和发射模式。
**对应子系统**：[军事武器子系统](afsim-architecture.md) + [火力支援插件](afsim-architecture.md) + [IADS C2插件](afsim-architecture.md)

| 层级 | 功能名称 | 简介 |
|------|----------|------|
| 模块级 | 发射决策（Launch Decision） | 判断是否满足发射条件（射程/杀伤区/能量/时间窗口） |
| 模块级 | 拦截点计算（Intercept Point Calculation） | 预测武器与目标的交会点坐标和交会时间 |
| 模块级 | 弹道计算（Ballistic Calculation） | 弹道导弹/火炮的弹道轨迹计算 |
| 模块级 | 杀伤区计算（LAR/Launch Acceptability Region） | 计算武器可攻击的空域范围 |
| 模块级 | 武器-目标配对（Weapon-Target Pairing） | 多目标场景中的最优武器分配 |
| 模块级 | 战损评估（Battle Damage Assessment） | 武器命中后的毁伤效果评估 |

### 2.5 通信与网络（Communication & Networking，通信与网络）

**简介**：平台间消息传递、网络路由、协议栈实现和外部系统交互。
**对应子系统**：[通信系统](afsim-architecture.md) + [DIS协议](afsim-architecture.md) + [Link-16](afsim-architecture.md)

| 层级 | 功能名称 | 简介 |
|------|----------|------|
| 模块级 | 消息收发（Message Send/Receive） | Track/Status/Control/Image/Video 等消息类型的发送和接收 |
| 模块级 | 网络路由（Network Routing） | 多跳网络中的消息路由（RIPv2/OSPF/多播/自组网） |
| 模块级 | DIS协议交互（DIS Protocol） | IEEE 1278.1 分布式交互仿真协议的消息编解码和状态同步 |
| 模块级 | Link-16数据链（Link-16 Data Link） | MIL-STD-6016 战术数据链消息格式和时序 |
| 模块级 | 外部IO（External IO/XIO） | 与外部仿真系统/真实设备的序列化数据交换 |

### 2.6 行为与决策（Behavior & Decision，行为与决策）

**简介**：平台自主行为的建模，包括行为树执行、脚本驱动决策和状态机逻辑。
**对应子系统**：[行为树系统](afsim-architecture.md) + [脚本系统](afsim-architecture.md)

| 层级 | 功能名称 | 简介 |
|------|----------|------|
| 模块级 | 行为树执行（Behavior Tree Execution） | 顺序/选择/并行/优先级/加权随机节点的遍历和执行 |
| 模块级 | 高级行为树（Advanced Behavior Tree） | 带记忆/装饰器/逆变器/重复器的扩展行为树 |
| 模块级 | 脚本指令执行（Script Command Execution） | 在仿真时间点执行用户定义的脚本命令 |

---

## 3. 类级功能与方法级功能（代表性示例）

### 3.1 WsfApplication — 应用生命周期管理（Application Lifecycle Management，应用生命周期管理）

| 类级功能 | 包含的方法级功能 |
|----------|----------------|
| 应用初始化（Initialization） | `WsfApplication::WsfApplication(name,argc,argv,paths)` — 构造应用单例，注册默认 Feature（操作系统/CPU/构建类型） |
| 扩展管理（Extension Management） | `RegisterExtension(name,ext)` — 注册应用扩展；`ExtensionDepends(a,b,req)` — 声明扩展依赖关系；`FindExtension(name)` — 查找已注册扩展 |
| 命令行处理（Command Line） | `GetCommandLineArguments(argc,argv)` — 获取命令行参数；`RemoveCommandLineOptions(argc,count)` — 消费已处理参数 |
| 功能注册（Feature Registration） | `RegisterFeature(feature,project)` — 注册应用功能标志；`GetRegisteredFeatures()` — 返回已注册功能列表 |
| 测试环境（Test Environment） | `IsTestingEnabled()` — 返回是否在自动化测试环境中运行，默认值 `mIsTestingEnabled = false` |

### 3.2 WsfPlatform — 平台实体管理（Platform Entity Management，平台实体管理）

| 类级功能 | 包含的方法级功能 |
|----------|----------------|
| 仿真更新（Simulation Update） | `Update(simTime)` — 在 `mLastUpdateTime < simTime` 且未锁定时调用 DoUpdate |
| 运动管理（Motion Management） | `SetMover(mover)` — 设置运动模型；`GetMover()` — 获取运动模型指针（默认 nullptr）；`SwapMover(time,new,old)` — 运行时替换运动模型 |
| 质量计算（Mass Calculation） | `GetMass()` — 返回空重+燃油+载荷之和（三个质量分量默认均为 0.0） |
| 编组管理（Group Management） | `JoinGroup(group)` / `LeaveGroup(group)` / `IsGroupMember(id)` |
| 类别管理（Category Management） | `AddCategory(id)` / `IsCategoryMember(id)` |
| 摧毁处理（Broken Handling） | `OnBrokenEvent(time)` — 根据 mOnBrokenAction（默认 cON_BROKEN_REMOVE）移除/禁用平台 |
| 观察者通知（Observer Notification） | `AttachObserver(observer)` / `DetachObserver(observer)` / `NotifyDeleted(time)` |

### 3.3 WsfLaunchComputer — 发射决策（Launch Decision，发射决策）

| 类级功能 | 包含的方法级功能 |
|----------|----------------|
| 拦截点预测（Intercept Prediction） | 在派生类 `WsfBallisticMissileLaunchComputer` 和 `WsfOrbitalLaunchComputer` 中实现 |
| 杀伤区计算（LAR Calculation） | 在 `weapon_tools/` 工具中辅助计算 |
| 发射条件判断（Launch Condition） | 各派生类实现——判断射程/能量/时间窗口是否满足 |

---

## 4. 功能-子系统/模块映射

| 系统级功能 | 对应子系统 |
|-----------|-----------|
| 仿真生命周期管理 | 应用管理系统 + 场景管理系统 + 仿真引擎系统 + 事件系统 |
| 平台运动与动力学 | 运动模型系统 + 平台实体系统 + 地形环境系统 + 空间域子系统 |
| 传感器探测与跟踪 | 传感器系统 + 电磁系统 + 跟踪系统 + 滤波器系统 |
| 武器交战与拦截 | 军事武器子系统 + 火力支援插件 + IADS C2 插件 |
| 通信与网络 | 通信系统 + DIS协议 + Link-16 + 外部IO |
| 行为与决策 | 行为树系统 + 脚本系统 + 赛博域子系统 |

| 模块级功能 | 对应模块（类） |
|-----------|--------------|
| 空气动力学运动 | WsfAirMover, WsfAero, WsfAero2D — [mover/](src/core/wsf/source/mover/) |
| 电磁传播计算 | WsfEM_Propagation, WsfEM_Attenuation, WsfEM_BlakeAttenuation, WsfEM_ITU_Attenuation |
| 航迹关联 | WsfCorrelationStrategy, WsfNearestNeighborCorrelation, WsfPerfectCorrelation, WsfTruthCorrelation |
| 航迹融合 | WsfFusionStrategy, WsfDefaultFusion |
| 发射决策 | WsfLaunchComputer, WsfBallisticMissileLaunchComputer, WsfOrbitalLaunchComputer, WsfSAM_LaunchComputer, WsfATA_LaunchComputer — [weapon/](src/core/wsf_mil/source/weapon/) |
| 拦截点计算 | WsfInterceptCalc — [wsf_iads_c2_lib/](src/wsf_plugins/wsf_iads_c2_lib/), InterceptPrediction — [vclMath/](src/wsf_plugins/wsf_iads_c2_lib/iadsLib/include/vclMath/) |
| 行为树执行 | WsfBehaviorTree, WsfBehaviorTreeNode → SequenceNode/SelectorNode/ParallelNode/PrioritySelectorNode/WeightedRandomNode |
| 网络路由 | comm/ 子目录下 Router/Protocol 类 |
| DIS协议交互 | dis/ 子目录下所有类 |
| 消息收发 | WsfMessage, WsfMessageTable, WsfTrackMessage, WsfStatusMessage 等 |
