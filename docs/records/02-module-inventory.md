# 02 — 模块清单

**日期**：2026-06-08
**状态**：初稿（P0 详细，P1-P3 概览）

---

## P0：wsf/source — 核心仿真框架（~1,113 文件）

### 顶层核心类（~380 文件：190 .hpp + 190 .cpp）

按功能域分组：

#### 1. 应用与仿真管理（~20 文件）
| 文件 | 说明 |
|------|------|
| WsfApplication.hpp/cpp | 应用主类，维护扩展、插件、系统日志 |
| WsfStandardApplication.hpp/cpp | 标准应用，提供更便捷的创建方式 |
| WsfApplicationExtension.hpp/cpp | 应用扩展基类 |
| WsfSimulation.hpp/cpp | 仿真主循环，管理所有平台 |
| WsfSimulationExtension.hpp/cpp | 仿真扩展 |
| WsfSimulationInput.hpp/cpp | 仿真输入处理 |
| WsfScenario.hpp/cpp | 场景定义，平台类型和实例容器 |
| WsfScenarioExtension.hpp/cpp | 场景扩展 |
| WsfFrameStepSimulation.hpp/cpp | 帧步进仿真模式 |
| WsfEventStepSimulation.hpp/cpp | 事件步进仿真模式 |
| WsfProfilingApplicationExtension.hpp/cpp | 性能分析扩展 |

#### 2. 平台与组件模型（~30 文件）
| 文件 | 说明 |
|------|------|
| WsfPlatform.hpp/cpp | **核心**：仿真中的实体容器，聚合 Mover/Sensor/Comm/Processor |
| WsfPlatformPart.hpp/cpp | 平台部件 |
| WsfPlatformPartEvent.hpp/cpp | 平台部件事件 |
| WsfPlatformTypes.hpp/cpp | 平台类型定义 |
| WsfPlatformAvailability.hpp/cpp | 平台可用性 |
| WsfObject.hpp/cpp | 对象基类 |
| WsfComponent.hpp/cpp | 组件基类（Sensor/Comm/Processor 等父类） |
| WsfComponentFactory.hpp/cpp | 组件工厂 |
| WsfComponentList.hpp/cpp | 组件列表管理 |
| WsfComponentRoles.hpp | 组件角色定义 |
| WsfSimpleComponent.hpp | 简单组件模板 |
| WsfArticulatedPart.hpp/cpp | 铰接部件 |
| WsfArticulatedPartEvent.hpp/cpp | 铰接部件事件 |
| WsfAuxDataEnabled.hpp/cpp | 辅助数据支持 mixin |

#### 3. 运动系统（mover/ 子目录：~101 文件）
| 关键文件 | 说明 |
|----------|------|
| WsfMover*.hpp/cpp | 各类运动模型（基础、空气、地面、海洋、空间等） |

#### 4. 跟踪系统（~50 文件）
| 文件 | 说明 |
|------|------|
| WsfTrack.hpp/cpp | 跟踪目标表示 |
| WsfTrackManager.hpp/cpp | 跟踪管理器 |
| WsfLocalTrack.hpp/cpp | 本地跟踪 |
| WsfTrackId.hpp/cpp | 跟踪 ID |
| WsfTrackMessage.hpp/cpp | 跟踪消息 |
| WsfTrackReportingStrategy*.hpp/cpp | 跟踪上报策略 |
| WsfTrackExtrapolation*.hpp/cpp | 跟踪外推 |
| WsfTrackStateController.hpp/cpp | 跟踪状态控制 |
| WsfCorrelationStrategy*.hpp/cpp | 关联策略（最近邻等） |
| WsfFusionStrategy*.hpp/cpp | 融合策略 |
| WsfDefaultFusion.hpp/cpp | 默认融合 |
| WsfTruthCorrelation.hpp/cpp | 真值关联 |
| WsfPerfectCorrelation.hpp/cpp | 完美关联 |
| WsfNearestNeighborCorrelation.hpp/cpp | 最近邻关联 |
| WsfBatchTrackReporting.hpp/cpp | 批量跟踪上报 |
| WsfCyclicTrackReporting.hpp/cpp | 周期性跟踪上报 |

#### 5. 电磁/传感器系统（~80 文件）
| 文件 | 说明 |
|------|------|
| WsfEM_Manager.hpp/cpp | EM 管理器 |
| WsfEM_Antenna.hpp/cpp | 天线模型 |
| WsfEM_Xmtr.hpp/cpp | 发射机 |
| WsfEM_Rcvr.hpp/cpp | 接收机 |
| WsfEM_XmtrRcvr.hpp/cpp | 收发机 |
| WsfEM_Propagation*.hpp/cpp | 传播模型 |
| WsfEM_Attenuation*.hpp/cpp | 衰减模型 |
| WsfEM_Noise.hpp/cpp | 噪声模型 |
| WsfEM_Clutter*.hpp/cpp | 杂波模型 |
| WsfEM_Interaction.hpp/cpp | EM 交互 |
| WsfEM_Types.hpp | EM 类型定义 |
| WsfEM_Util.hpp/cpp | EM 工具函数 |
| WsfAntennaPattern*.hpp/cpp | 天线方向图 |
| WsfStandardAntennaPattern.hpp/cpp | 标准天线方向图 |
| WsfMaskingPattern*.hpp/cpp | 遮蔽方向图 |
| WsfFieldOfView*.hpp/cpp | 视场定义 |
| WsfSensor*.hpp/cpp (sensor/ 子目录) | 各类传感器模型 |
| WsfSignature*.hpp/cpp | 目标特征 |
| WsfRadarSignature*.hpp/cpp | 雷达特征 |
| WsfStandardRadarSignature.hpp/cpp | 标准雷达特征 |
| WsfIFF_Manager.hpp/cpp | 敌我识别管理 |
| WsfLOS_Manager.hpp/cpp | 视线管理 |
| WsfMoonLOS_SensorComponent.hpp/cpp | 月光视线传感器 |
| WsfSolarElevationAtTargetComponent.hpp/cpp | 太阳高度角组件 |
| WsfSolarIlluminationComponent.hpp/cpp | 太阳光照组件 |
| WsfThermalSystem*.hpp/cpp | 热成像系统 |

#### 6. 滤波器（~6 文件）
| 文件 | 说明 |
|------|------|
| WsfFilter.hpp/cpp | 滤波器基类 |
| WsfFilterTypes.hpp/cpp | 滤波器类型 |
| WsfAlphaBetaFilter.hpp | α-β 滤波器 |
| WsfAlphaBetaGammaFilter.hpp | α-β-γ 滤波器 |
| WsfKalmanFilter.hpp | 卡尔曼滤波器 |
| WsfKalmanFilter2D_RB.hpp | 2D 距离-方位卡尔曼滤波器 |

#### 7. 行为树（~8 文件）
| 文件 | 说明 |
|------|------|
| WsfBehaviorTree.hpp/cpp | 行为树引擎 |
| WsfBehaviorTreeNode.hpp/cpp | 行为树节点 |
| WsfAdvancedBehaviorTree.hpp/cpp | 高级行为树 |
| WsfAdvancedBehaviorTreeNode.hpp/cpp | 高级行为树节点 |

#### 8. 地形与环境（~15 文件）
| 文件 | 说明 |
|------|------|
| WsfTerrain.hpp/cpp | 地形接口 |
| WsfTerrainProfiler.hpp/cpp | 地形剖面器 |
| WsfDtedRect.hpp/cpp | DTED 矩形区域 |
| WsfLandCover.hpp | 地表覆盖 |
| WsfEarthGravityModel.hpp/cpp | 地球重力模型 |
| WsfEnvironment.hpp/cpp | 环境参数 |
| WsfIntersectMesh*.hpp/cpp | 网格求交 |

#### 9. 区域系统（~18 文件）
| 文件 | 说明 |
|------|------|
| WsfZone.hpp/cpp | 区域基类 |
| WsfZoneDefinition.hpp/cpp | 区域定义 |
| WsfZoneReference.hpp/cpp | 区域引用 |
| WsfZoneSet.hpp/cpp | 区域集合 |
| WsfZoneRouteFinder.hpp/cpp | 区域路径查找 |
| WsfZoneTypes.hpp/cpp | 区域类型 |
| WsfZoneAttenuation.hpp/cpp | 区域衰减 |
| WsfCodedZone.hpp/cpp | 编码区域 |
| WsfConvexHull.hpp/cpp | 凸包 |

#### 10. 事件系统（~18 文件）
| 文件 | 说明 |
|------|------|
| WsfEvent.hpp | 事件基类 |
| WsfEventManager.hpp/cpp | 事件管理器 |
| WsfStableOrderEventManager.hpp | 稳定顺序事件管理器 |
| WsfEventOutput.hpp/cpp | 事件输出 |
| WsfEventOutputBase.hpp/cpp | 事件输出基类 |
| WsfCSV_EventOutput.hpp/cpp | CSV 事件输出 |
| WsfEventResult.hpp | 事件结果 |
| WsfEventResults.hpp/cpp | 事件结果集 |
| WsfEventUtils.hpp/cpp | 事件工具 |
| WsfCallback.hpp/cpp | 回调机制 |
| WsfCallbackTypes.hpp/cpp | 回调类型 |

#### 11. 消息系统（~20 文件）
| 文件 | 说明 |
|------|------|
| WsfMessage.hpp/cpp | 消息基类 |
| WsfMessageTable.hpp/cpp | 消息表 |
| WsfTrackMessage.hpp/cpp | 跟踪消息 |
| WsfTrackDropMessage.hpp/cpp | 跟踪删除消息 |
| WsfTrackNotifyMessage.hpp/cpp | 跟踪通知消息 |
| WsfAssociationMessage.hpp/cpp | 关联消息 |
| WsfControlMessage.hpp/cpp | 控制消息 |
| WsfImageMessage.hpp/cpp | 图像消息 |
| WsfStatusMessage.hpp/cpp | 状态消息 |
| WsfVideoMessage.hpp/cpp | 视频消息 |

#### 12. 通信（comm/ 子目录：~108 文件）
通信协议和网络接口模型。

#### 13. DIS 协议（dis/ 子目录：~120 文件）
IEEE 1278.1 分布式交互仿真协议实现。

#### 14. 脚本系统（script/ 子目录：~108 文件）
| 关键文件 | 说明 |
|----------|------|
| WsfGrammarInterface.hpp/cpp | 语法解析接口 |
| WsfScriptContext.hpp | 脚本上下文 |

#### 15. 处理器（processor/ 子目录：~40 文件）
数据处理和分析组件。

#### 16. 观察者（observer/ 子目录：~32 文件）
观察者模式实现，用于事件监听和数据收集。

#### 17. 外部 IO（xio/ + xio_sim/：~107 文件）
外部系统接口和仿真 IO。

#### 18. 事件管道（event_pipe/：~15 文件）
事件流处理管道。

#### 19. 扩展接口（ext/：~16 文件）
第三方扩展接口。

#### 20. 交通（traffic/：~13 文件）
交通流模拟。

#### 21. 工具与基础类（~30 文件）
| 文件 | 说明 |
|------|------|
| WsfUtil.hpp/cpp | 通用工具函数 |
| WsfNamed.hpp/cpp | 命名对象基类 |
| WsfStringId.hpp | 字符串 ID（高效的字符串查找） |
| WsfStringTable.hpp/cpp | 字符串表 |
| WsfTypes.hpp/cpp | 核心枚举和类型定义 (WsfSpatialDomain) |
| WsfVariable.hpp/cpp | 可变参数封装 |
| WsfRandom.hpp/cpp | 随机数生成 |
| WsfRandomVariable.hpp/cpp | 随机变量（支持分布） |
| WsfDateTime.hpp/cpp | 日期时间 |
| WsfGeoPoint.hpp/cpp | 地理坐标点 |
| WsfCovariance.hpp | 协方差矩阵 |
| WsfNoiseCloud.hpp/cpp | 噪声云 |
| WsfUniqueId.hpp/cpp | 唯一 ID |
| WsfClockSource.hpp/cpp | 时钟源 |
| WsfRealTimeClockSource.hpp/cpp | 实时钟 |
| WsfConsole.hpp/cpp | 控制台 |
| WsfSystemLog.hpp/cpp | 系统日志 |
| WsfException.hpp | 异常定义 |
| WsfVersion.hpp | 版本信息 |
| WsfDraw.hpp/cpp | 绘图工具 |
| WsfVisual*.hpp/cpp | 可视化部件 |
| WsfImage.hpp/cpp | 图像 |
| WsfPlugin.hpp, WsfPluginManager.hpp/cpp | 插件管理 |
| WsfExtension.hpp/cpp, WsfExtensionList.hpp/cpp | 扩展列表 |
| WsfExternalLinks.hpp/cpp | 外部链接 |
| WsfInternalLinks.hpp/cpp | 内部链接 |
| WsfNetworkInterface.hpp/cpp | 网络接口 |
| WsfCommandChain.hpp/cpp | 命令链 |
| WsfExchange.hpp/cpp | 数据交换 |
| WsfGroup*.hpp/cpp | 编组管理 |
| WsfCategoryList.hpp/cpp | 类别列表 |
| WsfMode.hpp/cpp, WsfModeList.hpp/cpp | 模式管理 |
| WsfAttribute*.hpp/cpp | 属性容器 |
| WsfMeasurement.hpp/cpp | 测量值 |
| WsfIntercept.hpp/cpp | 拦截 |
| WsfDeferredInput.hpp/cpp | 延迟输入 |
| WsfTimeDelayQueue.hpp/cpp | 时间延迟队列 |
| WsfMultiThreadManager.hpp/cpp | 多线程管理 |
| WsfThread.hpp/cpp, WsfThreadPool.hpp | 线程池 |

## P1：军事域扩展 wsf_mil/source（~213 文件）

包含 comm, dis, ew, mover, observer, processor, script, sensor, weapon, xio 等子目录，为军事仿真提供领域特定实现。

## P1：空间域扩展 wsf_space/source（~171 文件）

包含 maneuvers 子目录，为空间环境仿真提供轨道力学等模型。

## P2：基础设施（~124 文件）

| 模块 | 文件数 | 说明 |
|------|--------|------|
| wsf_nx/source | 34 | 下一代框架（新传感器、处理器实现） |
| wsf_parser/source | 81 | 语法解析器（输入文件解析） |
| wsf_util | 9 | 基础工具库 |

## P3：关键插件（按需选择）

wsf_plugins 包含 23 个子插件模块（9,884 文件），常用的包括：
- wsf_air_combat, wsf_brawler, wsf_fires — 空战/火力
- wsf_iads_c2_lib — 综合防空指挥控制
- wsf_p6dof, wsf_six_dof — 六自由度模型
- wsf_coverage, wsf_multiresolution — 覆盖/多分辨率
- wsf_simdis, wsf_sosm — 可视化集成
