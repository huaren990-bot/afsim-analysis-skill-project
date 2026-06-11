# AFSIM 仿真框架架构文档

> **状态**：完成
> **日期**：2026-06-10
> **分析范围**：`source_root/src/wsf_plugins/` 全部 16 个插件模块
> **分析深度**：module（模块级 / 类级）
> **关联文档**：`docs/architecture/wsf_plugins/afsim-architecture.md`

---
## 0. 文档说明

**总体概述**：
wsf_plugins（插件系统）承载了 AFSIM 仿真框架中除核心引擎外的全部专业领域功能。本文档按照系统级（System-level）→ 模块级（Module-level）→ 类级（Class-level）→ 方法级（Method-level）四层功能体系组织，提供从宏观到微观的功能追溯能力。

**功能划分**：功能按四层体系组织：

| 层级 | 英文 | 定义 | 边界范围 | 对应索引 |
|------|------|------|----------|----------|
| **系统级** | System-level | 跨框架/域/插件层，组合多个模块完成的端到端业务能力 | 跨目录、跨子系统 | function-index level=System-level |
| **模块级** | Module-level | 在单一子系统/模块内，通过策略模式实现多变体的功能 | 同一目录或相邻目录 | function-index level=Module-level |
| **类级** | Class-level | 单个类（class）封装的职责集合 | 单个 .hpp + .cpp | function-index level=Class-level |
| **方法级** | Method-level | 单个函数/方法的具体算法实现 | 单个文件内的函数 | function-index level=Method-level |

---
## 1. 系统级功能总览

2.**功能对应条目**：见 `function-index.jsonl` 中 `level=System-level` 的 13 条条目（qualified_name 以 `wsf_plugins::` 开头）。

| # | 系统级功能 | 核心职责 |
|----|------|----------|
| 1 | 飞行器多保真度运动学仿真 | 为空中平台/导弹提供点质、拟6DOF、刚体6DOF、外部ARGO8等多级运动学模型 |
| 2 | 大尺度空战仿真 | 基于BRAWLER引擎的大规模多对多空战仿真 |
| 3 | 空战态势感知（SA） | 多传感器数据融合、目标识别、威胁评估、交战决策支持 |
| 4 | 综合防空系统指挥控制（IADS C2） | 防空资产调度、武器-目标匹配、拦截计算、C2网络分发 |
| 5 | 覆盖性分析（Coverage Analysis） | 基于网格的效能度量计算（MOE）、传感器/通信覆盖评估 |
| 6 | 多分辨率建模 | 保真度驱动的自适应模型选择和多轮次参数扫描 |
| 7 | 场景验证与合规性检查 | 自动化场景配置检查（19项SAT检查） |
| 8 | 非制导弹药弹道计算 | 火炮/迫击炮弹道表查询和弹道仿真 |
| 9 | 光谱光学传感器建模 | SOSM传感器接口集成和红外/光电传感器仿真 |
| 10 | SIMDIS 3D可视化 | 仿真数据的SIMDIS ASI格式输出（平台/航迹/武器事件） |
| 11 | OMS/UCI标准化消息通信 | 基于ASB中间件的UCI标准化消息收发 |
| 12 | 场景标注 | POI、范围环、装饰等场景标注信息的处理 |
| 13 | 备用位置管理 | 平台备用位置信息的仿真扩展 |

---
## 2. 飞行器多保真度运动学仿真系统功能

1.**系统功能概述**：为 AFSIM 中的空中平台和导弹提供多级保真度的运动学仿真能力。从最快的点质模型到高保真ARGO8刚体6DOF模型，用户可根据场景需求选择合适的保真度级别。

2.**模块级功能细览**：

| 系统级功能 | 模块级功能 | 核心职责 |
|------|----------|----------|
| 飞行器多保真度运动学仿真 | 拟6自由度（P6DOF）运动学 | 完整6DOF能力但简化旋转运动学，含自动驾驶、制导、编队 |
| 飞行器多保真度运动学仿真 | 6自由度（Six-DOF）运动学 | 点质+刚体双模式6DOF，含飞行控制系统 |
| 飞行器多保真度运动学仿真 | ARGO8导弹模型集成 | 外部ARGO8高保真导弹模型的AFSIM封装 |

### 2.1 拟6自由度（P6DOF）运动学模块级功能

1.**模块概述**：P6DOF 是 AFSIM 的主要飞行器运动学模拟插件，由 Boeing 研发。核心 `WsfP6DOF_Mover` 类拥有超过 150 个公共方法，提供气动计算、推力管理、燃油管理、飞行控制界面、自动驾驶等完备能力。通过 `P6DofVehicle` 独立核心库实现与 AFSIM 框架的解耦。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| P6DOF运动学 | WsfP6DOF_Mover | P6DOF运动器主类 — 框架接口、自动驾驶、航路管理 |
| P6DOF运动学 | WsfP6DOF_GuidanceComputer | 制导计算机 — 拦截弹道计算 |
| P6DOF运动学 | WsfP6DOF_Fuel | 燃油系统 — 燃油箱、燃油传输 |
| P6DOF运动学 | WsfP6DOF_ExplicitWeapon | 显式武器 — 制导弹药模型 |
| P6DOF运动学 | WsfP6DOF_Observer | 观察者 — 仿真事件回调 |
| P6DOF运动学 | WsfP6DOF_TypeManager | 类型管理器 — 飞行器类型注册 |
| P6DOF运动学 | WsfP6DOF_ObjectManager | 对象管理器 — 子对象/抛离物管理 |

#### 2.1.1 WsfP6DOF_Mover 类级功能

1.**类概述**：WsfP6DOF_Mover 是 P6DOF 模块的核心类，继承自 `WsfMover`，拥有 ~3000 行代码。提供以下方法级功能组：

2.**方法级功能细览**：

| 类级功能 | 方法级功能 | 核心职责 |
|------|----------|----------|
| WsfP6DOF_Mover | WsfP6DOF_Mover::Initialize, WsfP6DOF_Mover::Update, WsfP6DOF_Mover::Clone, WsfP6DOF_Mover::ProcessInput | 框架集成：初始化、更新循环、克隆、输入处理 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::GetStateData, WsfP6DOF_Mover::GetSpeed_fps, WsfP6DOF_Mover::GetAlt_m, WsfP6DOF_Mover::GetHeading, WsfP6DOF_Mover::GetPitch, WsfP6DOF_Mover::GetRoll 等80+个getter方法 | 丰富状态查询：80+ getter 方法获取飞行器姿态/速度/质量/力/力矩 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::SetAutopilotPitchAngle, WsfP6DOF_Mover::SetAutopilotRollAngle, WsfP6DOF_Mover::GoToLocation, WsfP6DOF_Mover::TurnToHeading | 自动驾驶控制：横向/纵向/速度三通道模式 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::SetDirectControlInputs, WsfP6DOF_Mover::GetAngleOfControlSurface, WsfP6DOF_Mover::GetListOfControlSurfaceNames, WsfP6DOF_Mover::GetAileronsBothPosition, WsfP6DOF_Mover::GetStabilatorLeftPosition, WsfP6DOF_Mover::GetStabilatorRightPosition, WsfP6DOF_Mover::GetRudderPosition, WsfP6DOF_Mover::GetFlapsPosition, WsfP6DOF_Mover::GetSpoilersPosition, WsfP6DOF_Mover::GetSpeedBrakePosition, WsfP6DOF_Mover::GetNormalizedAileronLeft, WsfP6DOF_Mover::GetNormalizedAileronRight | 舵面/控制界面状态查询和控制 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::AddFuel, WsfP6DOF_Mover::GetTotalFuelRemaining, WsfP6DOF_Mover::SetJokerFuelState, WsfP6DOF_Mover::SetBingoFuelState | 燃油系统：加油、查询、Joker/Bingo状态 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::GetTotalThrust, WsfP6DOF_Mover::GetEngineThrust, WsfP6DOF_Mover::StartupEngines, WsfP6DOF_Mover::ShutdownEngines, WsfP6DOF_Mover::GetTotalFuelFlowRate, WsfP6DOF_Mover::GetEngineFuelFlowRate, WsfP6DOF_Mover::GetAfterburnerOn, WsfP6DOF_Mover::GetEngineAfterburnerOn | 推力/发动机管理 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::GoToWaypoint, WsfP6DOF_Mover::SetRoute, WsfP6DOF_Mover::ReturnToRoute | 航路/航点管理 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::ExecuteManeuver, WsfP6DOF_Mover::ExecuteManeuverSequence, WsfP6DOF_Mover::CancelManeuvers | 机动动作和编队执行 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::SetDamageFactor, WsfP6DOF_Mover::SetDestroyed, WsfP6DOF_Mover::GetIsDestroyed | 损伤状态管理 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::GetContrailTrailingEffect, WsfP6DOF_Mover::MakeEnginesSmoke, WsfP6DOF_Mover::SetFlamesArePresent, WsfP6DOF_Mover::SetDamageSmokeTrailingEffect, WsfP6DOF_Mover::SetRisingSmokePlumeIsPresent, WsfP6DOF_Mover::SetLaunchFlashSmokeIsPresent | 视觉外观效果控制 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::RetractLandingGear, WsfP6DOF_Mover::LowerLandingGear, WsfP6DOF_Mover::SetParkingBrake, WsfP6DOF_Mover::ApplyLeftGearBrake, WsfP6DOF_Mover::ApplyRightGearBrake, WsfP6DOF_Mover::ReleaseWheelBrakes | 地面操作管理 |
| WsfP6DOF_Mover | WsfP6DOF_Mover::SetTestingIgnoreAllCrashes, WsfP6DOF_Mover::GetTestingIgnoreAllCrashes, WsfP6DOF_Mover::SetTestingClampToSealLevelMinAlt, WsfP6DOF_Mover::GetTestingClampToSealLevelMinAlt, WsfP6DOF_Mover::GetTestSupportObject | 测试辅助 |

### 2.2 6自由度（Six-DOF）运动学模块级功能

1.**模块概述**：Six-DOF 提供比 P6DOF 更高保真的选项。核心分为点质模型（`wsf::six_dof::PointMassMover`）和刚体模型（`WsfRigidBodySixDOF_Mover`）两大变体。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| Six-DOF运动学 | wsf::six_dof::PointMassMover | 点质6DOF运动器 — 简化旋转运动学 |
| Six-DOF运动学 | WsfRigidBodySixDOF_Mover | 刚体6DOF运动器 — 完整转动惯量 |
| Six-DOF运动学 | PointMassAeroCoreObject | 点质气动核心 — 升力/阻力/侧力 |
| Six-DOF运动学 | RigidBodyAeroCoreObject | 刚体气动核心 |
| Six-DOF运动学 | PointMassIntegrator | 点质积分器 — 运动方程数值积分 |
| Six-DOF运动学 | PointMassFlightControlSystem | 飞行控制系统 |
| Six-DOF运动学 | PointMassPropulsionSystem | 推力系统 |
| Six-DOF运动学 | PointMassPilotManager | 飞行员管理器 |
| Six-DOF运动学 | PilotObject / SyntheticPilot | 飞行员对象（手动/合成） |

### 2.3 ARGO8导弹模型集成模块级功能

1.**模块概述**：wsf_argo8 将 AFRL 的 ARGO8 6DOF 导弹模型封装为 AFSIM Mover。核心类 `WsfARGO8_Mover` 包含 ARGO8 特有的导引头模式、制导方式、导弹状态管理等。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| ARGO8集成 | WsfARGO8_Mover | ARGO8导弹运动器 — ARGO8模型封装 |
| ARGO8集成 | Argo8Missile | ARGO8导弹物理模型 |

---
## 3. 空战态势感知（SA）系统功能

1.**系统功能概述**：空战SA（Situational Awareness，态势感知）通过模块化子模块（感知→预测→评估）架构，为空战平台提供从传感器数据到战术决策建议的完整认知链条。

2.**模块级功能细览**：

| 系统级功能 | 模块级功能 | 核心职责 |
|------|----------|----------|
| 空战态势感知 | 感知（Perceive） | 多传感器数据融合、目标检测与跟踪 |
| 空战态势感知 | 预测（Predict） | 目标运动预测 |
| 空战态势感知 | 评估（Assess） | 威胁评估和交战建议 |
| 空战态势感知 | 群组管理（Group Management） | 协同作战群组创建和管理 |

### 3.1 有关空战SA核心类级功能

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| SA处理器 | WsfSA_Processor | SA主控制器 — 协调各子模块更新 |
| SA模块基类 | WsfSA_Module | 所有SA子模块的抽象基础 |
| 感知 | WsfSA_Perceive | 传感器数据融合和目标感知 |
| 预测 | WsfSA_Predict | 目标运动轨迹预测 |
| 评估 | WsfSA_Assess | 威胁等级评估和交战建议生成 |
| 群组管理 | WsfSA_Group | 群组对象 |
| 群组管理 | WsfSA_GroupManager | 群组管理器 — 群组生命周期 |
| 消息 | WsfSA_EntityMessage | 实体间消息通信 |
| 数据 | WsfSA_EntityPerception | 感知结果数据结构 |
| 数据 | WsfSA_PerceivedItem | 单个目标感知状态 |

---
## 4. 综合防空系统指挥控制（IADS C2）系统功能

1.**系统功能概述**：IADS C2（Integrated Air Defense System Command and Control，综合防空系统指挥控制）是 wsf_plugins 中规模最大的作战管理模块。由 Radiance Technologies 开发，提供完整的防空作战管理能力。

2.**模块级功能细览**：

| 系统级功能 | 模块级功能 | 核心职责 |
|------|----------|----------|
| IADS C2 | 战场管理（Battle Management） | 全局战场态势监控和决策 |
| IADS C2 | 资产管理（Asset Management） | 防空资产跟踪、能力和状态管理 |
| IADS C2 | 交战评估（Engagement Assessment） | 交战结果评判和反馈 |
| IADS C2 | 拦截计算（Intercept Calculation） | 拦截几何解算和到达时间预测 |
| IADS C2 | C2分发（C2 Dissemination） | 指挥信息在C2网络中的分发 |
| IADS C2 | 任务分配（Assignment） | 武器-目标匹配和任务分配 |
| IADS C2 | 事件输出（Event Output） | 作战事件记录和CSV输出 |
| IADS C2 | 地形分析（Terrain） | 地形遮蔽和视线分析 |

### 4.1 IADS C2 核心类级功能

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| 战场管理 | WsfBattleManager | 战场管理器 — 继承自 WsfScriptProcessor 的 IADS C2 核心 |
| 战场管理 | WsfDefaultBattleManagerImpl | 默认战场管理实现 |
| 资产管理 | WsfAssetManager | 资产管理器 |
| 资产管理 | WsfAssetMap | 资产映射 |
| 资产管理 | WsfBMAssetRecord | 资产记录 |
| 交战评估 | WsfBMAssessEngagements | 交战评估处理器 |
| 拦截计算 | WsfInterceptCalc | 拦截计算器 |
| C2分发 | WsfBMDisseminateC2 | C2信息分发 |
| 任务分配 | WsfBMEvalAssignment | 武器-目标匹配评估 |
| 消息系统 | WsfBMAssignmentMessage | 任务分配消息 |
| 消息系统 | WsfBMCueMessage | 提示消息 |
| 消息系统 | WsfBMAssignmentTrackMessage | 航迹分配消息 |
| 事件输出 | WsfBMEventOutput | 事件输出接口 |
| 事件输出 | WsfBMCSV_EventOutput | CSV事件输出 |
| 效能度量 | WsfBMMOELogger | MOE日志记录器 |
| 地形 | WsfBMTerrainInterface | 地形分析接口 |

---
## 5. 覆盖性分析（Coverage Analysis）系统功能

1.**系统功能概述**：覆盖性分析（Coverage Analysis）是 AFSIM 的效能评估核心工具。它通过将仿真中的自由平台与网格化测试点之间的交互记录为"访问区间"（AccessIntervals），再通过可扩展的"效能度量"（Measures）对这些区间进行统计分析，最终生成覆盖性报告。支持多种网格类型、资产规格和约束条件。

2.**模块级/类级功能细览**：

| 系统级功能 | 模块级/类级功能 | 核心职责 |
|------|----------|----------|
| 覆盖性分析 | wsf::coverage::Coverage（抽象基类） | 覆盖性计算框架 — 管理资产、网格、度量、约束和输出 |
| 覆盖性分析 | 网格系统（Grid Hierarchy） | LatLonGrid（经纬度网格）、DistanceSteppedGrid（距离步进）、ExistingPlatformGrid（现有平台）、CompositeGrid（复合网格） |
| 覆盖性分析 | 资产系统（Asset System） | GridAsset（网格资产）、FreeAsset（自由资产）、AssetSpecification（资产规格） |
| 覆盖性分析 | 效能度量（Measure Hierarchy） | GridStats（网格统计）、LatLonStats（经纬度统计）、自定义MOE |
| 覆盖性分析 | 约束系统（IntervalConstraint） | 区间过滤约束 — 过滤无效/非目标交互 |
| 覆盖性分析 | 数据输出（RawDataOutput） | 原始数据输出、CSV输出 |

---
## 6. 多分辨率建模系统功能

1.**系统功能概述**：多分辨率建模（Multi-resolution Modeling）由 Stellar Science 开发。通过 `WsfMultiresolutionPlatformComponent<T>` 模板基类，为 AFSIM 平台提供了一个保真度（Fidelity）参数驱动的模型选择机制。配合 `WsfMultiresolutionMultirunTable` 可实现多轮次自动保真度扫描。

2.**类级功能细览**：

| 系统级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| 多分辨率建模 | WsfMultiresolutionPlatformComponent\<T\> | 模板基类 — 保真度驱动的模型生成 |
| 多分辨率建模 | WsfMultiresolutionMultirunTable | 多轮次参数表 — 保真度参数扫描 |
| 多分辨率建模 | WsfMultiresolutionWrapperMetaModel | 元模型包装 — 外部模型的AFSIM适配 |

---
## 7. 场景验证与合规性检查系统功能

1.**系统功能概述**：场景分析器（Scenario Analyzer）是自动化场景质量保证工具。它提供 19 项预定义场景合规性检查，覆盖通信、指挥链、传感器、航迹处理、武器、运动学等领域。

2.**检查功能分类**：

| 检查类别 | 具体检查项 | 说明 |
|------|------|----------|
| 指挥链检查 | checkCommanderInDeclaredCommandChain | 确认声明的指挥链中存在指挥官 |
| 指挥链检查 | checkDeclaredCommandChainHasStructure | 确认指挥链结构完整性 |
| 指挥链检查 | checkLargeScenarioHasCommandChain | 大规模场景中指挥链是否配置 |
| 通信检查 | checkCommInternallyLinked | 通信设备内部链接检查 |
| 通信检查 | checkPlatformInCommandChainHasComm | 指挥链中平台的通信设备检查 |
| 传感器检查 | checkSensorInternallyLinked | 传感器内部链接检查 |
| 传感器检查 | checkSensorInternallyLinkedToTrackProcessor | 传感器到航迹处理器链接 |
| 传感器检查 | checkSensorOn | 传感器是否开启 |
| 信号检查 | checkPlatformHasRequiredSignatures | 平台特征信号完整性 |
| 信号检查 | checkSignaturesDetectableByEnemySensor | 特征信号可检测性验证 |
| 航迹处理检查 | checkTrackProcessorHasPurgeInterval | 航迹清除间隔配置 |
| 航迹处理检查 | checkPurgeIntervalLongEnoughToMaintainTrack | 清除间隔是否足够维持航迹 |
| 航迹处理检查 | checkPurgeIntervalLongEnoughToEstablishTrack | 清除间隔是否足够建立航迹 |
| 航迹处理检查 | checkTrackProcessorsDontReportFusedTracksToEachOther | 航迹融合循环检查 |
| 脚本处理器检查 | checkScriptProcessorHasUpdateInterval | 脚本处理器更新间隔 |
| 运动器检查 | checkUserConfiguredSpeedsWithinMoverCapabilities | 配置速度是否在运动器能力范围内 |
| 武器检查 | checkWeaponsNonzeroQuantity | 武器数量非零检查 |
| 平台检查 | checkPlatformHasMeaningfulLocation | 平台位置有效性 |
| 会话通知 | notifyOfPlatformsNotPresentInSimulation | 通知未在仿真中出现的平台 |

---
## 8. 非制导弹药弹道计算系统功能

1.**系统功能概述**：wsf_fires（火力）提供非制导弹药（如炮弹、迫击炮）的弹道计算能力。核心数据结构 `FiresTable` 从外部数据文件加载射表，通过优化过的查表算法实现快速射程/弹道高度/飞行时间/发射仰角等参数计算。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| 弹道计算 | Fires::FiresTable | 射表 — 弹道数据存储和查询 |
| 弹道计算 | FiresTableLookup | 查表上下文 — 优化的插值/查找算法 |
| 弹道计算 | FiresTableLoader | 射表加载器 — 从文件加载弹道数据 |
| 弹道计算 | FiresPath | 弹道路径 — 弹道轨迹模拟 |
| 弹道计算 | BallisticPath | 弹道航路 |
| 弹道计算 | FiresMover | 火力运动器 |
| 弹道计算 | FiresLaunchComputer | 发射计算机 — 目标解算 |

---
## 9. 光谱光学传感器建模系统功能

1.**系统功能概述**：wsf_sosm 将 Boeing 的 SOSM（Spectral Optical Sensor Model）集成到 AFSIM 传感器框架中。`WsfSOSM_Interface` 作为场景扩展读取 SOSM 配置，`WsfSOSM_Sensor` 作为自定义 AFSIM 传感器实现 SOSM 物理计算。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| SOSM集成 | WsfSOSM_Interface | 场景扩展 — SOSM 配置输入、传感器/目标类型映射 |
| SOSM集成 | WsfSOSM_Sensor | 传感器接口 — SOSM 物理计算委托 |
| SOSM集成 | WsfSOSM_Interaction | 交互管理 — SOSM 传感器-目标交互 |

---
## 10. SIMDIS 3D可视化系统功能

1.**系统功能概述**：wsf_simdis 支持将 AFSIM 仿真数据输出为 SIMDIS 的 ASI（ASCII Scenario Input）格式文件，用于 3D 可视化。由 Lockheed Martin 开发。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| SIMDIS输出 | wsf::simdis::ScenarioExtension | 场景扩展 — 读取 SIMDIS 输出配置 |
| SIMDIS输出 | wsf::simdis::Interface | 仿真接口 — 处理仿真事件（平台初始化/击杀、武器命中、航迹等）并写 ASI 文件 |

---
## 11. OMS/UCI标准化消息通信系统功能

1.**系统功能概述**：wsf_oms_uci 实现了 AFSIM 与 OMS（Open Mission Systems）/ UCI（Universal Command and Control Interface）标准化消息协议的对接。它基于 ASB（Abstract Service Bus，抽象服务总线）中间件，支持 AMTI、ESM、POST 等多种传感器/能力类型的 UCI 消息收发。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| UCI接口 | wsf::UCI_Interface | 核心接口 — ASB 连接管理、消息收发、组件注册 |
| UCI组件 | UCI_Component | 组件基类 |
| UCI组件 | UCI_AMTI_Component | AMTI（空中动目标指示）传感器组件 |
| UCI组件 | UCI_ESM_Component | ESM（电子支援措施）传感器组件 |
| UCI组件 | UCI_IRST_Component | IRST（红外搜索跟踪）传感器组件 |
| UCI服务 | UCI_FactoryService | 工厂服务 — 消息类型工厂创建 |
| UCI服务 | UCI_MessageService | 消息服务 — 消息主题订阅和收发 |
| UCI服务 | UCI_GenericListener | 通用消息监听器 |

---
## 12. 场景标注系统功能

1.**系统功能概述**：wsf_annotation 提供场景标注功能。`WsfAnnotationExtension` 处理 POI（兴趣点）、RangeRing（范围环）、Decoration（装饰）等标注输入，并通过 EventPipe 在组件间分发标注数据。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| 标注 | WsfAnnotationExtension | 标注主扩展 — 场景+仿真双扩展，处理标注输入 |
| 标注 | WsfAnnotationInput | 标注输入处理器 — POI/RangeRing/Decoration 解析 |
| 标注数据 | AnnotationData::AnnotationInfo | 标注信息数据结构 |

---
## 13. 备用位置管理系统功能

1.**系统功能概述**：wsf_alternate_locations 提供备用位置（Alternate Locations）仿真扩展。通过 `wsf::altloc::SimulationExtension` 管理平台备用位置信息，并在 `WsfObserver` 命名空间中注册自定义事件回调。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| 备用位置 | wsf::altloc::SimulationExtension | 仿真扩展 — 备用位置管理、Observer回调注册 |
| 备用位置 | wsf::altloc::Component | 位置组件 — 备用位置数据结构 |

---
## 14. BRAWLER 大尺度空战仿真系统功能

1.**系统功能概述**：BRAWLER 是 Boeing 研发的大尺度多对多空战仿真模型，wsf_brawler 将其集成到 AFSIM 平台。`WsfBrawler` 作为场景扩展注册 BRAWLER 类型，`WsfBrawlerMover` 封装 BRAWLER 动力学引擎。

2.**类级功能细览**：

| 模块级功能 | 类级功能 | 核心职责 |
|------|----------|----------|
| BRAWLER集成 | WsfBrawler | 场景扩展 — BRAWLER 脚本类型注册 |
| BRAWLER集成 | WsfBrawlerMover | 运动器 — BRAWLER 空战动力学 |
| BRAWLER集成 | WsfBrawlerProcessor | 处理器 — BRAWLER 仿真逻辑 |
| BRAWLER集成 | WsfBrawlerComponents | 组件集合 |
| BRAWLER集成 | WsfBrawlerFuel | 燃油模型 |
