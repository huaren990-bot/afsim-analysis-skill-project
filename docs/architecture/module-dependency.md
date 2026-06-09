# AFSIM 模块依赖关系表

> **状态**：🔴 草稿 — 等待开发人员校对
> **日期**：2026-06-09
> **关联文档**：[afsim-architecture.md](afsim-architecture.md)

---

## 模块依赖

### 框架层（Framework Layer）— P0

| 子系统 | 模块（类） | 依赖模块 | 强度 | 依赖说明 |
|--------|-----------|----------|------|----------|
| 对象与类型系统 | WsfObject（基础对象） | UtScriptAccessible（脚本可访问） | 强 | 继承：使所有 WSF 对象可被脚本访问 |
| 对象与类型系统 | WsfObject | UtReferenceTracked（引用跟踪） | 强 | 继承：支持引用计数和智能指针 |
| 对象与类型系统 | WsfObject | WsfStringId（字符串ID） | 强 | 组合：mName 和类型管理依赖 WsfStringId |
| 组件模型系统 | WsfComponent（组件基类） | WsfComponentRoles（组件角色） | 强 | 包含：定义 cWSF_COMPONENT_* 角色常量 |
| 组件模型系统 | WsfComponentT（类型化组件） | WsfComponent | 强 | 继承：复用通用组件接口 |
| 组件模型系统 | WsfPlatformComponent（平台组件） | WsfPlatform（平台实体） | 强 | 模板绑定：PARENT_TYPE = WsfPlatform |
| 应用管理系统 | WsfApplication（应用主类） | WsfExtensionList（扩展列表） | 强 | 组合：维护已注册的应用扩展 |
| 应用管理系统 | WsfApplication | WsfPluginManager（插件管理器） | 中 | 组合：管理动态插件加载 |
| 应用管理系统 | WsfApplication | WsfSystemLog（系统日志） | 弱 | 组合：记录应用级日志 |
| 场景管理系统 | WsfScenario（场景容器） | WsfApplication | 强 | 依赖：需要 Application 实例才能构造 |
| 场景管理系统 | WsfScenario | WsfEnvironment（环境参数） | 中 | 组合：场景级环境配置 |
| 场景管理系统 | WsfScenario | WsfTerrain（地形接口） | 中 | 组合：场景级地形数据 |
| 场景管理系统 | WsfScenario | WsfComponentFactory（组件工厂） | 强 | 聚合：管理所有组件的工厂注册 |
| 仿真引擎系统 | WsfSimulation（仿真控制器） | WsfEventManager（事件队列） | 强 | 组合：事件队列驱动仿真循环 |
| 仿真引擎系统 | WsfSimulation | WsfEM_Manager（EM管理器） | 强 | 组合：管理活跃收发机 |
| 仿真引擎系统 | WsfSimulation | WsfMultiThreadManager（多线程） | 中 | 组合：多线程平台更新调度 |
| 仿真引擎系统 | WsfSimulation | WsfGroupManager（编组管理） | 中 | 组合：平台编组管理 |
| 仿真引擎系统 | WsfSimulation | WsfPlatform | 强 | 聚合：管理所有平台生命周期 |
| 平台实体系统 | WsfPlatform（平台实体） | WsfObject | 强 | 继承：复用 name+type 基础 |
| 平台实体系统 | WsfPlatform | WsfPlatformComponent | 强 | 继承：使平台本身可被视为组件 |
| 平台实体系统 | WsfPlatform | WsfUniqueId（唯一ID） | 强 | 继承：提供仿真内唯一索引 |
| 平台实体系统 | WsfPlatform | WsfMover（运动模型） | 强 | 组合：mMoverPtr，平台无Mover则不能移动 |
| 平台实体系统 | WsfPlatform | WsfFuel（燃油模型） | 弱 | 组合：可选燃油消耗管理 |
| 平台实体系统 | WsfPlatform | WsfSignatureList（特征列表） | 中 | 组合：管理平台可检测特征 |
| 平台实体系统 | WsfPlatform | wsf::Terrain（地形） | 强 | 组合：地形高度查询和地表交互 |
| 平台实体系统 | WsfPlatform | WsfTrackManager（跟踪管理） | 中 | 组合：维护平台本地跟踪列表 |
| 跟踪系统 | WsfTrackManager（跟踪管理） | WsfCorrelationStrategy（关联策略） | 强 | 策略模式：默认 PerfectCorrelation |
| 跟踪系统 | WsfTrackManager | WsfFusionStrategy（融合策略） | 强 | 策略模式：默认 DefaultFusion |
| 跟踪系统 | WsfTrackManager | WsfLocalTrack（本地航迹） | 强 | 聚合：维护本地跟踪列表 |
| 跟踪系统 | WsfTrackManager | WsfTrack（原始航迹） | 中 | 聚合：接收原始 Track Report |
| 跟踪系统 | WsfNearestNeighborCorrelation（最近邻关联） | WsfCorrelationStrategy | 强 | 继承：最近邻关联的具体实现 |
| 跟踪系统 | WsfDefaultFusion（默认融合） | WsfFusionStrategy | 强 | 继承：默认融合策略实现 |
| 电磁系统 | WsfEM_Manager（EM管理器） | WsfEM_Xmtr（发射机） | 强 | 聚合：维护活跃发射机列表 |
| 电磁系统 | WsfEM_Manager | WsfEM_Rcvr（接收机） | 强 | 聚合：维护活跃接收机列表 |
| 电磁系统 | WsfEM_XmtrRcvr（收发机） | WsfEM_Propagation（传播模型） | 强 | 组合：路径损耗计算 |
| 电磁系统 | WsfEM_XmtrRcvr | WsfEM_Attenuation（衰减模型） | 强 | 组合：大气衰减计算 |
| 电磁系统 | WsfEM_XmtrRcvr | WsfEM_Noise（噪声模型） | 中 | 组合：噪声影响计算 |
| 电磁系统 | WsfEM_Antenna（天线） | 天线方向图（Pattern） | 强 | 组合：WsfAntennaPattern 定义方向图 |
| 传感器系统 | WsfSensor（传感器） | WsfEM_Rcvr | 强 | 组合：通过接收机感知电磁环境 |
| 传感器系统 | WsfSensor | WsfFieldOfView（视场） | 强 | 组合：空间覆盖范围限制 |
| 传感器系统 | WsfSensor | WsfTrackManager | 强 | 依赖：输出 Track Report 到 TrackManager |
| 通信系统 | WsfComm（通信设备） | WsfEM_XmtrRcvr | 强 | 组合：通过收发机实现通信 |
| 通信系统 | WsfComm | WsfMessage（消息） | 强 | 组合：收发各类消息 |
| 处理器系统 | WsfProcessor（处理器） | WsfTrackManager | 强 | 依赖：处理跟踪数据 |
| 事件系统 | WsfEventManager | WsfEvent（事件） | 强 | 聚合：存储和排序事件 |
| 事件系统 | WsfEventManager | WsfSimulation | 强 | 关联：绑定所属仿真实例 |
| 脚本系统 | WsfScriptContext（脚本上下文） | WsfPlatform | 强 | 关联：为平台提供脚本执行环境 |
| 行为树系统 | WsfBehaviorTree（行为树） | WsfBehaviorTreeNode（行为树节点） | 强 | 聚合：树结构由节点组合而成 |
| 滤波器系统 | WsfFilter（滤波器） | WsfMeasurement（测量值） | 强 | 依赖：处理测量值序列 |
| 区域系统 | WsfZoneSet（区域集合） | WsfZone（区域） | 强 | 聚合：区域集合包含多个区域 |
| 地形环境系统 | WsfTerrain（地形） | wsf::TerrainInterface（地形接口） | 强 | 实现：框架定义接口，具体数据源实现 |
| 地形环境系统 | WsfEarthGravityModel（重力模型） | WsfMover | 弱 | 依赖：运动模型使用重力计算 |
| 基础工具系统 | WsfRandomVariable（随机变量） | ut::Random（随机数生成器） | 强 | 组合：底层随机数引擎 |
| 基础工具系统 | WsfVariable\<T\>（可变参数） | WsfVariableBase（变量基类） | 强 | 继承：类型无关基础设施 |

### 军事域层（Military Domain Layer）— P0

| 子系统 | 模块（类） | 依赖模块 | 强度 | 依赖说明 |
|--------|-----------|----------|------|----------|
| 武器子系统 | WsfLaunchComputer（发射计算机） | WsfPlatform | 强 | 关联：发射计算机属于特定平台 |
| 武器子系统 | WsfBallisticMissileLaunchComputer（弹道导弹发射计算机） | WsfLaunchComputer | 强 | 继承：弹道导弹的发射决策 |
| 武器子系统 | WsfOrbitalLaunchComputer（轨道发射计算机） | WsfLaunchComputer | 强 | 继承：轨道武器的发射决策 |
| 武器子系统 | WsfSAM_LaunchComputer（地对空发射计算机） | WsfLaunchComputer | 强 | 继承：地对空导弹的发射决策 |
| 武器子系统 | WsfATA_LaunchComputer（空对空发射计算机） | WsfLaunchComputer | 强 | 继承：空对空导弹的发射决策 |
| 军事传感器 | WsfEOIR_Sensor（光电红外传感器） | WsfSensor | 强 | 继承：从框架传感器派生 |
| 军事传感器 | WsfIRST_Sensor（红外搜索跟踪传感器） | WsfSensor | 强 | 继承：红外传感器特化 |
| 军事运动 | WsfGuidedMover（制导运动体） | WsfMover | 强 | 继承：增加制导逻辑 |
| 电子战 | EW模块 | WsfEM_* | 强 | 依赖：电子战依托电磁系统 |

### 插件层（Plugin Layer）— P1

| 子系统 | 模块（类） | 依赖模块 | 强度 | 依赖说明 |
|--------|-----------|----------|------|----------|
| 空战插件 | SA处理器（态势感知） | WsfProcessor | 强 | 继承：基于框架处理器 |
| 空战插件 | SA实体感知（EntityPerception） | WsfTrack | 中 | 依赖：基于跟踪数据构建感知 |
| 火力支援 | FiresPath（火力路径） | WsfMover | 强 | 继承/组合：弹道运动路径 |
| 火力支援 | BallisticPlatforms（弹道平台） | WsfPlatform | 强 | 继承：弹道武器平台 |
| IADS C2 | WsfInterceptCalc（拦截计算） | WsfLaunchComputer | 强 | 依赖：调用发射计算机进行拦截计算 |
| IADS C2 | WsfBattleManager（战斗管理） | WsfPlatform | 强 | 依赖：管理所有防空平台 |
| IADS C2 | InterceptPrediction（拦截预测） | vclMath | 强 | 依赖：底层数学库 |
| 六自由度 | WsfSixDOF_Sequencer（6DOF序列器） | WsfMover | 强 | 依赖：基于运动模型框架 |
| 六自由度 | WsfSixDOF_GuidanceComputer（制导计算机） | WsfLaunchComputer | 中 | 继承/组合：制导逻辑 |

---

## 全局变量/常量依赖

| 依赖方 | 全局常量 | 定义位置 | 作用 |
|--------|----------|----------|------|
| WsfTrackManager | cWSF_INITIALIZE_ORDER_TRACK_MANAGER = -900,000,000 | [WsfComponentRoles.hpp](src/core/wsf/source/WsfComponentRoles.hpp:166) | 跟踪管理器初始化顺序（全局初始化优先级常量） |
| WsfMover | cWSF_INITIALIZE_ORDER_MOVER = -800,000,000 | [WsfComponentRoles.hpp](src/core/wsf/source/WsfComponentRoles.hpp:168) | 运动模型初始化顺序 |
| WsfSensor | cWSF_INITIALIZE_ORDER_SENSOR = -500,000,000 | [WsfComponentRoles.hpp](src/core/wsf/source/WsfComponentRoles.hpp:177) | 传感器初始化顺序 |
| WsfPlatform | WSF_SPATIAL_DOMAIN_UNKNOWN = 0 | [WsfTypes.hpp](src/core/wsf/source/WsfTypes.hpp:33) | 默认空间域（未知） |
| WsfPlatform | cON_BROKEN_REMOVE = 0 | [WsfPlatform.hpp](src/core/wsf/source/WsfPlatform.hpp:125) | 默认摧毁处理动作（移除） |
| WsfSimulation | WSF_APPLICATION_FEATURE_* | 运行时注册 | 操作系统/CPU/构建类型等 Feature 标志 |
| wsf::version | WSF_VERSION_MAJOR/MINOR/PATCH | wsf_version_defines.hpp | 编译时版本号常量 |

---

## 依赖强度说明

| 强度 | 含义 | 示例 |
|------|------|------|
| **强** | 编译期依赖，缺少则无法编译 | 继承关系、值类型成员、模板实例化 |
| **中** | 逻辑依赖，运行时通常需要，但有默认/null 替代 | 指针类型成员、可选策略模式 |
| **弱** | 松耦合，仅在特定场景使用 | 日志、调试、可选功能 |
