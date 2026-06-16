# 模块概览：AFSIM 2.9

## 模块清单

| # | 模块名 | 路径 | 文件总数 | 源码/头文件数 | 核心职责 |
|---|--------|------|-------------|---------------|---------------------|
| 1 | source | afsim-2_9 | 15718 | 15113 | 涵盖 swdev/src/ 全部代码的总括模块（15,113 个源码/头文件，跨核心库、插件、应用和工具） |
| 2 | wsf_six_dof | afsim-2_9 | 938 | 331 | 六自由度运动学插件（331 个源文件） |
| 3 | wsf_space | afsim-2_9 | 695 | 304 | 太空域仿真：开普勒/J2/NORAD 轨道力学、数值积分、姿态控制、星座管理 |
| 4 | test | afsim-2_9 | 445 | 268 | 测试基础设施：核心库与插件的单元测试（268 个源码/头文件） |
| 5 | wsf_p6dof | afsim-2_9 | 806 | 191 | 平台六自由度运动插件（191 个源文件） |
| 6 | iadsLib | afsim-2_9 | 158 | 146 | 综合防空系统（IADS）核心库，供 scene_gen 使用（146 个源文件） |
| 7 | wsf_parser | afsim-2_9 | 150 | 138 | 自定义 DSL 解析器：WsfPProxyStructType、WsfParseAction*、WsfPM_* 解析模型类、PProxy 序列化 |
| 8 | wsf_l16 | afsim-2_9 | 181 | 105 | Link-16 战术数据链：J 系列报文（2.x~31.x）、网络武器、PPLI、监视、武器协同 |
| 9 | p6dof | afsim-2_9 | 103 | 100 | 平台六自由度独立工具（100 个源文件） |
| 10 | wsf_cyber | afsim-2_9 | 209 | 85 | 网络战仿真：网络攻击、网络防御、网络约束、网络可视化 |
| 11 | wsf_nx | afsim-2_9 | 187 | 72 | 下一代扩展：箔条云/箔条包、ALARM 天线、电子战传感器、ESA 天线方向图 |
| 12 | src | afsim-2_9 | 2617 | 62 | 附加源码分析元数据（vx.json、markdown） |
| 13 | lib | afsim-2_9 | 55 | 51 | mystic/warlock 共享库（51 个源文件） |
| 14 | engage | afsim-2_9 | 158 | 45 | 主仿真引擎可执行文件：语法定义、源码、测试、插件模块 |
| 15 | sosm | afsim-2_9 | 48 | 45 | SOSM 独立工具（45 个源文件） |
| 16 | sensor_plot_lib | afsim-2_9 | 74 | 41 | 传感器绘图库：雷达包络、垂直覆盖、等高线滤波、杂波表、地图投影 |
| 17 | wsf_air_combat | afsim-2_9 | 143 | 31 | 空战仿真插件 |
| 18 | wsf_mtt | afsim-2_9 | 50 | 30 | 多目标跟踪：航迹关联、数据融合、MHT（多假设跟踪） |
| 19 | weapon_tools | afsim-2_9 | 91 | 26 | 武器系统分析（26 个源文件） |
| 20 | wsf_ripr | afsim-2_9 | 62 | 24 | RIPR 数据接口：作业处理、作业板调度、观察者模式 |
| 21 | wsf_fires | afsim-2_9 | 44 | 22 | 火力支援插件 |
| 22 | wsf_brawler | afsim-2_9 | 147 | 15 | Brawler 空战交战模型插件 |
| 23 | wsf_multiresolution | afsim-2_9 | 114 | 14 | 多分辨率建模插件 |
| 24 | brawler | afsim-2_9 | 15 | 12 | Brawler 交战模型独立工具（12 个源文件） |
| 25 | wsf_alternate_locations | afsim-2_9 | 22 | 7 | 备选位置与路径规划插件 |
| 26 | wsf_mil_parser | afsim-2_9 | 13 | 7 | 军事语法解析扩展 |
| 27 | resources | afsim-2_9 | 1349 | 6 | 静态资源：地图、模型、着色器（6 个源文件） |
| 28 | wsf_sosm | afsim-2_9 | 24 | 6 | 特种作战/太空作战模型（SOSM）插件 |
| 29 | profiling | afsim-2_9 | 12 | 5 | 性能分析工具（5 个源文件） |
| 30 | wsf_annotation | afsim-2_9 | 20 | 5 | 场景标注插件 |
| 31 | osgdb_osgearth_dted_tms | afsim-2_9 | 7 | 5 | OSGEarth DTED TMS 数据库插件（5 个源文件） |
| 32 | wizard | afsim-2_9 | 834 | 3 | 场景编辑向导：CRD 文件导入、USMTF 处理、主程序及子插件 |
| 33 | sensor_plot | afsim-2_9 | 80 | 3 | 传感器覆盖/探测距离可视化 |
| 34 | wsf_argo8 | afsim-2_9 | 18 | 3 | ARGO8 集成插件 |
| 35 | wsf_iads_c2_lib | afsim-2_9 | 98 | 3 | 综合防空系统（IADS）C2 库插件 |
| 36 | mission | afsim-2_9 | 28 | 2 | 任务规划工具（2 个源文件） |
| 37 | util | afsim-2_9 | 6 | 2 | 通用工具（2 个源文件） |
| 38 | wsf_grammar_check | afsim-2_9 | 8 | 2 | 场景脚本语法校验工具 |
| 39 | wsf_weapon_server | afsim-2_9 | 16 | 2 | 武器计算服务器 |
| 40 | mover | afsim-2_9 | 56 | 2 | 运动体工具（2 个源文件） |
| 41 | afperf | afsim-2_9 | 3 | 1 | 性能测量工具（1 个源文件） |
| 42 | cli | afsim-2_9 | 3 | 1 | 命令行工具（1 个源文件） |
| 43 | ReaderWriterMod | afsim-2_9 | 3 | 1 | OSG 模型读写插件（1 个源文件） |
| 44 | ReaderWriterOGL | afsim-2_9 | 3 | 1 | OpenGL 读写插件（1 个源文件） |
| 45 | exec | afsim-2_9 | 3 | 1 | 执行工具（1 个源文件） |
| 46 | legacy_test | afsim-2_9 | 4 | 1 | 遗留测试支持（1 个源文件） |
| 47 | proxy_test | afsim-2_9 | 14 | 1 | 代理测试支持（1 个源文件） |
| 48 | pack_to_cpp | afsim-2_9 | 3 | 1 | Pack 转 C++ 代码生成器（1 个源文件） |
| 49 | ARCHITECTURE.md | afsim-2_9 | 1 | 0 | 项目架构文档 |
| 50 | vx.json | afsim-2_9 | 1 | 0 | 插件元数据（vx.json 描述文件） |
| 51 | documentation | afsim-2_9 | 5075 | 0 | HTML 文档与更新日志 |
| 52 | tools | afsim-2_9 | 120 | 0 | 外部 Perl/Python 工具脚本（批处理、事件提取、数据转换、绘图） |
| 53 | training | afsim-2_9 | 1441 | 0 | 培训材料 |
| 54 | swdev | afsim-2_9 | 448 | 0 | 构建系统：CMake 模块、预设、模板 |
| 55 | demos | afsim-2_9 | 6304 | 0 | 67+ 演示场景（覆盖各作战域） |
| 56 | warlock | afsim-2_9 | 920 | 0 | 仿真分析与调试工具：warlock_core、warlock_exec、插件 |
| 57 | mover_creator | afsim-2_9 | 583 | 0 | 运动体（平台）批量创建工具 |
| 58 | post_processor | afsim-2_9 | 64 | 0 | 仿真结果后处理（WizPostProcessor） |
| 59 | scene_gen | afsim-2_9 | 22 | 0 | 场景生成工具 |
| 60 | misc | afsim-2_9 | 17 | 0 | 杂项工具 |
| 61 | util_script | afsim-2_9 | 2 | 0 | 工具脚本 |
| 62 | geodata | afsim-2_9 | 2 | 0 | 地理数据处理 |
| 63 | artificer | afsim-2_9 | 3 | 0 | 构件生成工具 |
| 64 | wsf_simdis | afsim-2_9 | 12 | 0 | SIMDIS 3D 可视化集成插件 |
| 65 | wsf_scenario_analyzer_iads_c2 | afsim-2_9 | 9 | 0 | IADS C2 场景分析插件 |
| 66 | wsf_oms_uci | afsim-2_9 | 163 | 0 | 开放任务系统/通用指挥控制接口插件 |
| 67 | wsf_coverage | afsim-2_9 | 129 | 0 | 覆盖分析插件 |
| 68 | wsf_scenario_analyzer | afsim-2_9 | 10 | 0 | 场景分析插件 |
| 69 | wsf_mil | afsim-2_9 | 637 | 0 | 军事领域扩展：通信、电子战（EW）、武器、运动体、传感器、观察器、处理器、脚本、DIS |
| 70 | wsf | afsim-2_9 | 1237 | 0 | 核心作战仿真框架：应用、场景、仿真、平台、组件、插件、行为树、航迹 |
| 71 | source_plugin | afsim-2_9 | 2 | 0 | 源插件元数据（wsf_module 标记） |
| 72 | usmtf | afsim-2_9 | 4 | 0 | USMTF 报文格式处理 |
| 73 | observer | afsim-2_9 | 26 | 0 | 观察者模式子系统 |
| 74 | comm | afsim-2_9 | 28 | 0 | 通信框架子系统 |
| 75 | component | afsim-2_9 | 18 | 0 | 组件模型子系统 |
| 76 | xio | afsim-2_9 | 124 | 0 | 外部 I/O 子系统 |
| 77 | sensor | afsim-2_9 | 18 | 0 | 传感器框架子系统 |
| 78 | weapon | afsim-2_9 | 18 | 0 | 武器模型子系统 |
| 79 | ResultModelBrowser | afsim-2_9 | 9 | 0 | 结果模型浏览器 |
| 80 | ResultCoverageOverlay | afsim-2_9 | 7 | 0 | 结果覆盖叠加 |
| 81 | ResultMapHoverInfo | afsim-2_9 | 10 | 0 | 结果地图悬停信息 |
| 82 | ResultVideoCapture | afsim-2_9 | 8 | 0 | 结果视频采集 |
| 83 | ResultPerformance | afsim-2_9 | 8 | 0 | 结果性能显示 |
| 84 | ResultVisibility | afsim-2_9 | 8 | 0 | 结果可见性显示 |
| 85 | ResultPositionConverterTool | afsim-2_9 | 6 | 0 | 结果位置转换器 |
| 86 | ResultMapDisplay | afsim-2_9 | 14 | 0 | 结果地图显示 |
| 87 | ResultUnitConverterTool | afsim-2_9 | 6 | 0 | 结果单位转换器 |
| 88 | ResultTerrainTools | afsim-2_9 | 8 | 0 | 结果地形工具 |
| 89 | ResultTetherView | afsim-2_9 | 9 | 0 | 结果系留视图 |
| 90 | Visibility | afsim-2_9 | 14 | 0 | 可见性分析工具 |
| 91 | MapHoverInfo | afsim-2_9 | 20 | 0 | 地图悬停信息显示 |
| 92 | ModelBrowser | afsim-2_9 | 18 | 0 | 模型浏览器可视化 |
| 93 | UnitConverterTool | afsim-2_9 | 12 | 0 | 单位转换工具 |
| 94 | VideoCapture | afsim-2_9 | 16 | 0 | 视频采集工具 |
| 95 | CoverageOverlay | afsim-2_9 | 14 | 0 | 覆盖叠加可视化 |
| 96 | CRDImporter | afsim-2_9 | 15 | 0 | CRD 文件导入向导插件 |
| 97 | TetherView | afsim-2_9 | 18 | 0 | 系留视图可视化 |
| 98 | TerrainTools | afsim-2_9 | 16 | 0 | 地形分析工具 |
| 99 | Performance | afsim-2_9 | 15 | 0 | 性能可视化 |
| 100 | MapDisplay | afsim-2_9 | 35 | 0 | 地图显示可视化 |
| 101 | PositionConverterTool | afsim-2_9 | 12 | 0 | 位置坐标转换器 |
| 102 | benchmark | afsim-2_9 | 3 | 0 | 性能基准测试基础设施 |
| 103 | version_lesser_library | afsim-2_9 | 3 | 0 | 版本比较库（小于测试） |
| 104 | version_greater_library | afsim-2_9 | 3 | 0 | 版本比较库（大于测试） |
| 105 | dummy_library | afsim-2_9 | 3 | 0 | 构建测试用虚拟库 |
| 106 | wsf_prompt | afsim-2_9 | 7 | 0 | 提示/命令插件 |
| 107 | wsf_plugins | src | 1 | 0 | 插件模块聚合器（元数据） |

## 各模块详情

### 模块：source

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/`
**源码/头文件数：** 15113
**描述：** 涵盖 swdev/src/ 全部代码的总括模块（15,113 个源码/头文件，跨核心库、插件、应用和工具） 

#### 子系统结构 (source umbrella module)

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| core/wsf | `swdev/src/core/wsf/source/` | 1237 | 核心框架：应用、场景、仿真、平台、组件、插件、航迹、事件、传感器、运动体、通信 |
| core/wsf_util | `swdev/src/core/wsf_util/source/` | -- | 基础工具：缓冲区、打包/反射、矩阵、三维向量、路径、回调 |
| core/wsf_parser | `swdev/src/core/wsf_parser/source/` | 138 | 自定义 DSL 解析器：WsfPProxyStructType、WsfParseAction*、WsfPM_* 解析模型类 |
| core/wsf_mil | `swdev/src/core/wsf_mil/source/` | 637 | 军事领域：通信、电子战、武器、运动体、传感器扩展 |
| core/wsf_space | `swdev/src/core/wsf_space/source/` | 304 | 太空域：轨道力学、姿态控制、星座管理lations, rendezvous |
| core/wsf_cyber | `swdev/src/core/wsf_cyber/source/` | 85 | 网络战：攻击、防御、约束、网络模型ls |
| core/wsf_mtt | `swdev/src/core/wsf_mtt/source/` | 30 | 多目标跟踪：关联、融合、MHT |
| core/wsf_l16 | `swdev/src/core/wsf_l16/source/` | 105 | Link-16：J 系列报文、PPLI、监视、武器协同ation |
| core/wsf_nx | `swdev/src/core/wsf_nx/source/` | 72 | 下一代：箔条模型、ALARM 天线、ESA 方向图、电子战 |
| core/wsf_ripr | `swdev/src/core/wsf_ripr/source/` | 24 | RIPR 数据接口：作业处理、调度 |
| core/wsf_weapon_server | `swdev/src/core/wsf_weapon_server/source/` | 2 | 武器计算服务器 |
| core/wsf_grammar_check | `swdev/src/core/wsf_grammar_check/source/` | 2 | 语法校验 |
| core/wsf_mil_parser | `swdev/src/core/wsf_mil_parser/source/` | 7 | 军事解析器扩展 |
| core/sensor_plot_lib | `swdev/src/core/sensor_plot_lib/source/` | 41 | 传感器绘图：雷达包络、覆盖范围、等高线ours |
| engage | `swdev/src/engage/source/` | 45 | 主仿真引擎可执行文件及语法定义 |
| wsf_plugins | `swdev/src/wsf_plugins/*/source/` | -- | 17 个插件模块（空战、brawler、火力、iads_c2、六自由度等） |
| wizard | `swdev/src/wizard/` | 3+ | 场景编辑器：解析结果、CRD 导入、脚本编辑 |
| warlock | `swdev/src/warlock/` | 0+ | 分析/调试：核心、执行器、插件 |
| mystic | `swdev/src/mystic/` | 0+ | Python 分析环境：执行器、库、插件、Python 绑定 |
| tools | `swdev/src/tools/` | -- | 内部工具：场景生成、地理数据、跟踪滤波器、artificer、性能分析等 |
| mission | `swdev/src/mission/source/` | 2 | 任务规划与执行 |
| mover_creator | `swdev/src/mover_creator/source/` | 225 | 平台/运动体批量创建器 |
| sensor_plot | `swdev/src/sensor_plot/source/` | 3 | 传感器覆盖可视化 |
| weapon_tools | `swdev/src/weapon_tools/source/` | 26 | 武器分析工具 |
| post_processor | `swdev/src/post_processor/` | -- | 后处理：WizPostProcessor |
| evt_reader | `swdev/src/evt_reader/source/` | 5 | 事件日志读取器 |

#### 核心类（从 4826 个 class/struct 符号中抽取的代表性样本）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfVisualization | class（类） | 无 | 可视化框架基类 |
| WsfEM_Antenna | class（类） | UtScriptAccessible, WsfSinglePlatformObserver | 电磁天线模型 |
| WsfFusionStrategy | class（类） | WsfObject | 传感器融合策略基类 |
| WsfGroup | class（类） | WsfObject, WsfAuxDataEnabled | 平台编组管理 |
| WsfMultiThreadManager | class（类） | 无 | 多线程仿真管理器 |
| WsfPlatformPart | class（类） | WsfObject, WsfPlatformComponent, WsfUniqueId, WsfAuxDataEnabled | 平台部件组件 |
| WsfSolarIlluminationComponent | class（类） | WsfSensorComponent | 太阳光照传感器 |
| WsfComponentFactoryList | class（类） | 无 | 组件工厂注册表 |
| SimulationUpdateThread | class（类） | WsfThread | 仿真更新周期线程 |
| WsfComponentRole | struct（结构体） | 无 | 组件角色定义 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：wsf_six_dof

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_six_dof/source/`
**源码/头文件数：** 331
**描述：** 六自由度运动学插件，包含刚体飞行动力学、自动驾驶仪、制导和气动模型。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 331 | 六自由度主源码：飞行器数据、飞行控制、气动、推力、制导 |
| test | `test/` | 1 | 六自由度模型单元测试 |
| grammar | `grammar/` | 0 | 语法定义文件 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 57 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| ObjectManager | class（类） | WsfSimulationExtension | 六自由度仿真对象生命周期管理器 |
| TypeManager | class（类） | WsfScenarioExtension | 六自由度类型管理 |
| Environment | class（类） | WsfScenarioExtension | 六自由度环境参数 |
| EventPipe | class（类） | WsfEventPipeLogger | 六自由度事件管道（日志） |
| EventPipeInterface | class（类） | WsfSimulationExtension | 六自由度事件管道接口 |
| RigidBodyControlActuator | class（类） | 无 | 刚体控制执行器基类 |
| AutopilotWaypointData | struct（结构体） | 无 | 自动驾驶仪导航航路点数据 |
| AutopilotData | struct（结构体） | 无 | 完整自动驾驶仪配置数据 |
| PidGainData | struct（结构体） | 无 | PID 控制器增益参数 |
| FreezeFlags | struct（结构体） | 无 | 六自由度仿真冻结状态标志 |
| ControlInputValue | struct（结构体） | 无 | 飞行控制输入值 |
| ControlSurfaceElement | struct（结构体） | 无 | 操纵面定义 |
| NavWaypointParameters | struct（结构体） | 无 | 导航航路点参数 |
| AutopilotPidGroupValueData | struct（结构体） | 无 | 自动驾驶仪 PID 组值 |
| ControlSignalModifier | struct（结构体） | 无 | 控制信号修正器配置 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 六自由度扩展 WsfMover 实现运动学模型 |

---

### 模块：wsf_space

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_space/source/`
**源码/头文件数：** 304
**描述：** 太空域仿真：开普勒/J2/NORAD 轨道力学、数值积分、姿态控制、星座管理、交会评估、大气模型。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 304 | 太空域主源码 |
| test | `test/` | 25 | 太空模型单元测试 |
| grammar | `grammar/` | 0 | 语法定义 |
| tools | `tools/` | 0 | 太空域工具 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 129 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfScriptPiecewiseExponentialAtmosphere | class（类） | WsfScriptAtmosphere | 分段指数大气模型 |
| WsfScriptPrinceDormand78Integrator | class（类） | WsfScriptOrbitalIntegrator | Prince-Dormand 7/8 数值积分器 |
| WsfEarthJ2Term | class（类） | WsfOrbitalDynamicsTerm | 地球 J2 引力摄动 |
| WsfScriptPrinceDormand45Integrator | class（类） | WsfScriptOrbitalIntegrator | Prince-Dormand 4/5 数值积分器 |
| SpaceModel | class（类） | WsfMover::KinematicModel | 太空运动体运动学模型基类 |
| WsfDE_FileManager | class（类） | WsfSimulationExtension | 微分方程文件管理器 |
| OrbitalMissionContext | class（类） | 无 | 轨道任务执行上下文 |
| RadiusCondition | class（类） | OrbitalPropagatorOptimizingCondition | 轨道传播器半径停止条件 |
| Rocket | class（类） | 无 | 火箭推进模型 |
| WsfOrbitalManeuveringTypes | class（类） | WsfObjectTypeList<WsfOrbitalManeuvering> | 轨道机动类型注册表 |
| OrbitalMissionSimulationContext | class（类） | OrbitalMissionContext | 轨道任务仿真上下文 |
| WsfScriptTargetPoint | class（类） | UtScriptClass | 轨道机动的可脚本化目标点 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 太空域运动体扩展 WsfMover，平台扩展 WsfPlatform |

---

### 模块：test

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/test/` （或分布在各模块的 `test/` 目录中）
**源码/头文件数：** 268
**描述：** 测试基础设施：核心库与插件的单元测试（268 个源码/头文件）

#### 子系统结构

平铺结构 —— 测试源文件按被测试模块组织，分布在代码库各模块的 `test/` 子目录中。ectories.

#### 核心类（来自 13 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| UserDefinedSet | class（类） | 无 | 用户自定义类型集合的测试工具 |
| UserDefinedMessage | class（类） | 无 | 用户自定义消息的测试工具 |
| CoverageTestService | class（类） | 无 | 覆盖率测试服务基类 |
| SpaceTestService | class（类） | 无 | 太空域测试服务 |
| TestWriter | class（类） | 无 | 测试输出写入器 |
| TestCoverage | class（类） | 无 | 测试覆盖率度量 |
| TestMeasure | class（类） | 无 | 测试度量工具 |
| TestGrid | class（类） | 无 | 测试覆盖率网格 |
| InputFile | class（类） | 无 | 测试输入文件处理 |
| MockSourceProvider | class（类） | WsfParseSourceProvider | 解析源模拟提供器（测试用） |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 所有核心库的测试 |
| engage | 应用 | 仿真引擎集成测试 |

---

### 模块：wsf_p6dof

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_p6dof/source/`
**源码/头文件数：** 191
**描述：** 平台六自由度运动插件，包含编队飞行、站位保持和相对机动模型。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 191 | P6DOF 主源码 |
| p6dof | `p6dof/` | 101 | 共享 p6dof 库（P6DofPID、序列器、飞行器数据） |
| grammar | `grammar/` | 0 | 语法定义 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 22 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfP6DOF_TypeManager | class（类） | WsfScenarioExtension, P6DofTypeManager | 平台六自由度类型管理器 |
| WsfP6DOF_ObjectManager | class（类） | WsfSimulationExtension | P6DOF 对象生命周期管理器 |
| WsfFormationUpdateStationKeeping | class（类） | 无 | 编队站位保持更新逻辑 |
| WsfManeuverConstraint | class（类） | 无 | 机动约束执行 |
| RelativeManeuverState | class（类） | 无 | 相对机动状态基类 |
| FormUpStationKeepingManeuverState | class（类） | RelativeManeuverState | 编队/站位保持状态基类 |
| FormUpState | class（类） | FormUpStationKeepingManeuverState | 编队集结状态 |
| KeepStationState | class（类） | FormUpStationKeepingManeuverState | 站位保持状态 |
| PursueState | class（类） | FormUpStationKeepingManeuverState | 追击状态 |
| Constraint | class（类） | UtScriptAccessible | 编队约束定义 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 平台六自由度扩展 WsfPlatform/Kinematic |
| p6dof | 库 | 共享 p6dof 库，提供 PID、序列器、飞行器数据 |

---

### 模块：iadsLib

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_iads_c2_lib/iadsLib/`
**源码/头文件数：** 146
**描述：** 综合防空系统（IADS）核心仿真库。

#### 子系统结构

平铺结构 —— 单层目录，含 146 个源码/头文件。

#### 核心类（来自 19 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| Vector3 | class（类） | Vector<T> | 三维向量数学工具 |
| Vector4 | class（类） | Vector<T> | 四维向量数学工具 |
| Vector | class（类） | 无 | 通用向量模板 |
| VclInterceptCalculator | class（类） | InterceptCalculatorIface | VCL 拦截计算 |
| InterceptCalculatorIface | class（类） | 无 | 拦截计算器接口 |
| WeaponSystem | struct（结构体） | 无 | 武器系统战斗状态定义 |
| WeaponPairing | class（类） | 无 | 武器-目标配对逻辑 |
| AIScriptingParams | class（类） | 无 | 武器管理器的 AI 脚本参数 |
| ResponsibleAssignments | class（类） | 无 | 责任单元分配跟踪 |
| ActiveCues | class（类） | 无 | 主动雷达线索管理 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 for platform and weapon models |

---

### 模块：wsf_parser

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_parser/source/`
**源码/头文件数：** 138
**描述：** 自定义 DSL 解析器：WsfPProxyStructType、WsfParseAction*、WsfPM_* 解析模型类、PProxy 序列化、场景脚本解析。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 138 | 解析器主源码 |
| test | `test/` | 18 | 解析器单元测试 |
| legacy_test | `legacy_test/` | 2 | 遗留解析器测试支持 |

#### 核心类（来自 80 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfPProxyStructType | class（类） | WsfPProxyType | PProxy 结构体类型定义 |
| WsfPM_Fuel | class（类） | WsfPM_PlatformPart | 燃油组件解析器模型 |
| WsfPProxyHash | class（类） | 无 | PProxy 结构体查找哈希表 |
| WsfParseActionAddress | class（类） | 无 | 解析动作地址解析 |
| WsfParseActionAssign | class（类） | WsfParseActionPart | 赋值解析动作 |
| WsfParseActionCopy | class（类） | WsfParseActionPart | 拷贝解析动作 |
| WsfParseActionPush | class（类） | WsfParseActionPart | 栈压入解析动作 |
| WsfParseActionPrint | class（类） | WsfParseActionPart | 打印解析动作 |
| WsfParseActionListOp | class（类） | WsfParseActionPart | 列表操作解析动作 |
| WsfParseActionFunction | class（类） | 无 | 函数调用解析动作 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 将场景脚本解析为 WSF 对象 |
| wsf_util | 库 | 使用 UtInput 进行解析 |

---

### 模块：wsf_l16

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_l16/source/`
**源码/头文件数：** 105
**描述：** Link-16 战术数据链：J 系列报文（2.x~31.x）、网络武器、PPLI、监视、武器协同.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 105 | Link-16 主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 379 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| MessageAccessorType | class（类） | 无 | 报文字段访问器类型系统 |
| MessageScriptClass | class（类） | UtScriptClass | 可脚本化报文类 |
| MessageInitialScriptClass | class（类） | MessageScriptClass | 初始报文脚本类 |
| MessageContinuationScriptClass | class（类） | MessageScriptClass | 续传报文脚本类 |
| WeaponsCoordinationPart | class（类） | ComputerPart | 武器协同计算部件 |
| HeaderTDL100 | struct（结构体） | 无 | TDL-100（Link-16）报文头 |
| WSF_HeaderTDL100 | struct（结构体） | 无 | WSF 版 Link-16 报文头 |
| Initial (Message9_0) | class（类） | InitialBase | J9.0 报文初始字 |
| Continuation1 (Message9_0) | class（类） | ContinuationBase | J9.0 报文续传字 1 |
| Extension0 (Message9_0) | class（类） | ExtensionBase | J9.0 报文扩展字 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | Link-16 使用 WsfCommQueue 进行报文路由 |

---

### 模块：p6dof

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_p6dof/p6dof/`
**源码/头文件数：** 100
**描述：** 平台六自由度独立共享库：PID 控制器、序列器、飞行器数据结构。

#### 子系统结构

平铺结构 —— 单层目录，含 100 个源码/头文件，在 wsf_p6dof 插件与独立工具间共享。

#### 核心类（来自 32 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| P6DofPID | class（类） | 无 | 六自由度 PID 控制器 |
| P6DofSequencer | class（类） | P6DofObject | 六自由度机动事件序列器 |
| AutopilotData | struct（结构体） | 无 | 完整自动驾驶仪配置 |
| ControlSurfaceValue | struct（结构体） | 无 | 操纵面状态值 |
| FlightControlInputValue | struct（结构体） | 无 | 飞行控制输入值 |
| AutopilotWaypointData | struct（结构体） | 无 | 自动驾驶仪航路点数据 |
| PidGainData | struct（结构体） | 无 | PID 增益参数 |
| TrackData | struct（结构体） | 无 | 制导跟踪数据 |
| AutopilotPidGroupValueData | struct（结构体） | 无 | PID 组值 |
| NavWaypointParameters | struct（结构体） | 无 | 导航航路点参数 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：wsf_cyber

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_cyber/source/`
**源码/头文件数：** 85
**描述：** 网络战仿真：网络攻击、网络防御、网络约束、网络可视化.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 85 | 网络战主源码 |
| test | `test/` | 3 | 网络战单元测试 |
| grammar | `grammar/` | 0 | 语法定义 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 39 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| ConstraintTypes | class（类） | WsfObjectTypeList<Constraint> | 网络约束类型注册表 |
| ProtectTypes | class（类） | WsfObjectTypeList<Protect> | 网络防护类型注册表 |
| EffectTypes | class（类） | WsfObjectTypeList<Effect> | 网络效应类型注册表 |
| ProtectedAttack | class（类） | WsfNamed | 受保护网络攻击定义 |
| EngagementData | class（类） | 无 | 网络交战数据容器 |
| EventPipe | class（类） | WsfEventPipeLogger | 网络事件管道（日志） |
| RandomManager | class（类） | 无 | 网络效应随机化管理器 |
| VisualizationManager | class（类） | Visualization | 网络可视化管理器 |
| Visualization | class（类） | 无 | 网络可视化基类 |
| VisualizationDraw | class（类） | Visualization | 绘制专用可视化 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 网络战扩展核心仿真框架 |

---

### 模块：wsf_nx

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_nx/source/`
**源码/头文件数：** 72
**描述：** 下一代扩展：箔条云/箔条包、ALARM 天线、电子战传感器、ESA 天线方向图.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 72 | 下一代扩展主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| test_sensor_plot | `test_sensor_plot/` | 0 | 传感器绘图测试支持 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 49 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfChaffParcel | class（类） | WsfChaffParcelInterface, WsfObject, WsfSimplePlatformComponent | 单个箔条包 |
| WsfChaffMover | class（类） | WsfMover | 箔条云运动模型 |
| WsfChaffRadarSignature | class（类） | WsfRadarSignature | 箔条雷达散射截面特征 |
| WsfScriptChaffWeaponClass | class（类） | WsfScriptWeaponClass | 可脚本化箔条武器类 |
| WsfEM_ALARM_Propagation | class（类） | WsfEM_Propagation | ALARM 传播模型 |
| WsfEM_ALARM_Terrain | class（类） | 无 | ALARM 地形建模 |
| WsfEM_EARCE_Attenuation | class（类） | WsfEM_Attenuation | EARCE 衰减模型 |
| WsfElementESA_AntennaPattern | class（类） | WsfESA_AntennaPattern | 单元级 ESA 天线方向图 |
| WsfESA_NX_AntennaPattern | class（类） | WsfESA_AntennaPattern | 下一代 ESA 天线方向图 |
| WsfLink16Correlation | class（类） | WsfCorrelationStrategy | Link-16 关联策略 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 下一代传感器与对抗措施扩展 WsfSensor/WsfSignature |

---

### 模块：src

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/` (utilosg utilities)
**源码/头文件数：** 62
**描述：** 附加源码分析元数据与工具库（OSG 可视化工具）。

#### 子系统结构

平铺结构 —— 单层目录，含 62 个源码/头文件（OSG 工具类型）。

#### 核心类（来自 28 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| UtoCameraPerspective | class（类） | UtoCamera | 透视相机工具 |
| UtoCameraOrtho | class（类） | UtoCamera | 正交相机工具 |
| UtoGLShape | class（类） | UtoGLShapeBase | OpenGL 形状工具 |
| UtoColor | class（类） | 无 | 颜色工具类 |
| UtoCmeLineFunctor | class（类） | PrimitiveFunctor, T | CME 线函子 |
| UtoViewFilter | class（类） | 无 | 视图过滤器工具 |
| CmeIntersectState | class（类） | 无 | CME 交集状态 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| OSG | 库 | 依赖 OpenSceneGraph |
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：lib

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/mystic/lib/`
**源码/头文件数：** 51
**描述：** mystic/warlock 共享库：CRD 状态机元素、仿真数据、文本工具。

#### 子系统结构

平铺结构 —— 单层目录，含 51 个源码/头文件。

#### 核心类（来自 28 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| ElementBase | class（类） | 无 | 所有 CRD 元素的基类 |
| CrdTransition | class（类） | ElementBase | CRD 状态迁移 |
| CrdState | class（类） | ElementBase | CRD 状态定义 |
| CrdMission | class（类） | ElementBase | CRD 任务定义 |
| OrbitIntent | class（类） | ElementBase | 轨道意图元素 |
| Point | class（类） | ElementBase | 航路点元素 |
| Intent | class（类） | ElementBase | 意图元素 |
| Path | class（类） | ElementBase | 路径元素 |
| Route | class（类） | ElementBase | 航线元素 |
| Vehicle | class（类） | ElementBase | 载具元素 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：engage

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/engage/source/`
**源码/头文件数：** 45
**描述：** 主仿真引擎可执行文件：语法定义、源码、测试、插件模块.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 45 | 主仿真引擎源码 |
| grammar | `grammar/` | 0 | 语法定义 (scenario DSL) |
| tests | `tests/` | 0 | 集成测试 |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 54 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| Simulation | class（类） | WsfFrameStepSimulation | 主仿真引擎实例 |
| ApplicationExtension | class（类） | WsfApplicationExtension | engage 应用级扩展 |
| SimulationExtension | class（类） | WsfSimulationExtension | engage 仿真级扩展 |
| SimulationThread | class（类） | UtThread | 专用仿真线程 |
| Platform | class（类） | 无 | engage 专用平台模型 |
| Task | class（类） | 无 | 任务表示 |
| TaskOutput | class（类） | 无 | 任务输出数据 |
| TargetConfig | class（类） | 无 | 目标配置 |
| RunConfig | class（类） | 无 | 运行配置参数 |
| OutputConfig | class（类） | 无 | 输出配置 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 主可执行文件链接所有 wsf 库 |
| wsf_parser | 库 | 使用语法定义进行场景解析 |

---

### 模块：sosm

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_sosm/sosm/`
**源码/头文件数：** 45
**描述：** 特种作战/太空作战模型独立工具：标量表、光谱对象、传感器-目标交互建模。

#### 子系统结构

平铺结构 —— 单层目录，含 45 个源码/头文件。

#### 核心类（来自 25 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| SOSM_SimpleTarget | class（类） | SOSM_Target | 简单目标模型 |
| SOSM_SimpleInteraction | class（类） | SOSM_Interaction | 简单传感器-目标交互 |
| SOSM_ScalarTable2D | class（类） | 无 | 二维标量查表 |
| SOSM_ScalarTable3D | class（类） | 无 | 三维标量查表 |
| SOSM_SpectralTable2D | class（类） | SOSM_SpectralObject | 二维光谱表 |
| SOSM_TableTarget | class（类） | SOSM_Target | 基于表格的目标模型 |
| SOSM_BlackBody | class（类） | 无 | 黑体辐射模型 |
| SOSM_TableVar | class（类） | 无 | 表变量定义 |
| StateBase | class（类） | SOSM_SpectralObject | 目标状态基类 |
| ResponsePoint | class（类） | 无 | 传感器响应点 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 for spectral/sensor models |

---

### 模块：sensor_plot_lib

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/sensor_plot_lib/source/`
**源码/头文件数：** 41
**描述：** 传感器绘图库：雷达包络、垂直覆盖、等高线滤波、杂波表、地图投影.

#### 子系统结构

平铺结构 —— 单层目录，含 41 个源码/头文件。

#### 核心类（来自 30 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| RadarEnvelopeFunction | class（类） | Function | 雷达包络计算 |
| VerticalCoverageFunction | class（类） | Function | 垂直覆盖计算 |
| ContourFilter2D | class（类） | 无 | 二维等高线滤波 |
| MapProjection | class（类） | 无 | 地图投影工具 |
| ClutterTableFunction | class（类） | Function | 杂波表查找函数 |
| RadarLookupTableFunction | class（类） | Function | 雷达查表函数 |
| VerticalMapFunction | class（类） | MapPlotFunction | 垂直地图绘图函数 |
| MapPlotVariable | class（类） | 无 | 地图绘图变量定义 |
| Target | class（类） | 无 | 绘图目标表示 |
| Sensor | class（类） | 无 | 绘图传感器表示 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：wsf_air_combat

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_air_combat/source/`
**源码/头文件数：** 31
**描述：** 空战仿真插件：态势感知处理器、事件管道、交战跟踪。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 31 | 空战主源码 |
| test | `test/` | 3 | 单元测试 |
| grammar | `grammar/` | 0 | 语法定义 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 24 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| EventPipe | class（类） | WsfEventPipeLogger | 空战事件管道 |
| EventPipeInterface | class（类） | WsfSimulationExtension | 空战事件管道 interface |
| SA_EngagedTarget | struct（结构体） | 无 | 交战目标态势感知数据 |
| PerceiveData | struct（结构体） | 无 | 态势感知处理器感知数据 |
| SA_AircraftKinematics | struct（结构体） | 无 | 飞机运动学（态势感知） |
| SA_FuelSystemData | struct（结构体） | 无 | 燃油系统数据（态势感知） |
| SA_NavigationDataSummary | struct（结构体） | 无 | 导航数据摘要 |
| SA_FlightControlsDataSummary | struct（结构体） | 无 | 飞控摘要 |
| SA_WeaponNameQtyPair | struct（结构体） | 无 | 武器名称/数量对 |
| SA_TrackManagerData | struct（结构体） | 无 | 航迹管理器状态数据 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 空战扩展 WsfWeapon、WsfMover |

---

### 模块：wsf_mtt

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_mtt/source/`
**源码/头文件数：** 30
**描述：** 多目标跟踪：航迹关联、数据融合、MHT（多假设跟踪）.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 30 | MTT 主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| doc | `doc/` | 0 | Documentation |
| data | `data/` | 0 | 数据文件 |

#### 核心类（来自 22 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| MTT_Track | class（类） | 无 | 多目标跟踪基类航迹 |
| MTT_EmbryonicTrack | class（类） | MTT_Track | 胚胎（未确认）航迹 |
| MTT_PerceivedCluster | class（类） | 无 | 感知目标群 |
| MTT_Parameters | class（类） | 无 | MTT 算法参数 |
| MTT | class（类） | 无 | 多目标跟踪器核心 |
| MTT_NonlocalTrack | class（类） | 无 | 非本地（远程）航迹 |
| WsfMTT_Observer | class（类） | WsfSimulationExtension | MTT 仿真观察器 |
| WsfMTT_Fusion | class（类） | WsfDefaultFusion | MTT 传感器融合实现 |
| WsfMTT_ReferencePoint | class（类） | 无 | MTT 坐标系参考点 |
| SupBlock | class（类） | 无 | 航迹管理支持块 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 跟踪算法集成 WsfTrack 和 WsfSensor |

---

### 模块：weapon_tools

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/weapon_tools/source/`
**源码/头文件数：** 26
**描述：** 武器系统分析工具：LAR（可发射区域）、发射计算机、地空导弹分析。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 26 | 武器工具主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| tests | `tests/` | 0 | Tests |
| source_plugin | `source_plugin/` | 0 | Plugin source metadata |
| doc | `doc/` | 0 | Documentation |
| data | `data/` | 0 | 数据文件 |

#### 核心类（来自 4 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| AltAndSpeed | class（类） | 无 | LAR 生成的高度-速度对 |
| LocationPoint | class（类） | 无 | 地理位置点 |
| LAR_Condition | struct（结构体） | 无 | 可发射区域条件 |
| TestPoint | struct（结构体） | 无 | 地空导弹发射计算机测试点 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 for weapon modeling |

---

### 模块：wsf_ripr

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_ripr/source/`
**源码/头文件数：** 24
**描述：** RIPR 数据接口：作业处理、作业板调度、观察者模式、基于 XIO 报文的通信。

#### 子系统结构

平铺结构 —— 单层目录，含 24 个源码/头文件（可能分布在多个位置）。

#### 核心类（来自 27 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfRIPRProcessor | class（类） | WsfScriptProcessor | RIPR 处理引擎 |
| WsfXIO_RIPRExtension | class（类） | 无 | RIPR 的 XIO 扩展 |
| WsfXIO_JobBoardPacketRegistry | class（类） | 无 | 作业板报文注册表 |
| WsfXIO_JobBoardRequestPkt | class（类） | WsfXIO_RequestDataPkt | 作业板请求报文 |
| WsfXIO_JobBoardInitPkt | class（类） | WsfXIO_ResponsePkt | 作业板初始化报文 |
| WsfXIO_JobBoardUpdatePkt | class（类） | WsfXIO_ResponsePkt | 作业板更新报文 |
| WsfXIO_JobBoardWinnersUpdatePkt | class（类） | WsfXIO_ResponsePkt | 作业板获胜方更新 |
| WsfXIO_JobBoardCommandPkt | class（类） | WsfXIO_Packet | 作业板命令报文 |
| WsfXIO_RIPRManagerRequestPkt | class（类） | WsfXIO_RequestDataPkt | RIPR 管理器请求 |
| WsfXIO_ChannelIdUpdatePkt | class（类） | WsfXIO_ResponsePkt | 通道 ID 更新 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |
| xio | 库 | 使用基于 XIO 报文的通信 |

---

### 模块：wsf_fires

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_fires/source/`
**源码/头文件数：** 22
**描述：** 火力支援插件：弹道路径计算、火力运动体、射表加载。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 22 | 火力插件主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |
| data | `data/` | 0 | 数据文件 |

#### 核心类（来自 5 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| FiresMover | class（类） | WsfMover, FiresPath | 弹道火力运动体 |
| FiresTableLoader | class（类） | 无 | 射表加载器 |
| FiresPath | class（类） | 无 | 弹道路径模型 |
| EngagementData | struct（结构体） | 无 | 火力交战数据 |
| Point | struct（结构体） | 无 | 弹道路径点 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 火力支援集成 WsfWeapon 和 WsfMover |

---

### 模块：wsf_brawler

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_brawler/source/`
**源码/头文件数：** 15
**描述：** Brawler 空战交战模型插件：交战跟踪意识事件。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 15 | brawler 插件主源码 |
| brawler | `brawler/` | 12 | brawler 共享库 |
| grammar | `grammar/` | 0 | 语法定义 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |
| data | `data/` | 0 | 数据文件 |
| conversion | `conversion/` | 0 | 格式转换工具 |

#### 核心类（来自 1 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfBrawlerConsicousnessEvent | class（类） | WsfEvent | Brawler 意识/感知事件 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | Brawler 与 WsfWeapon/WsfPlatform 模型交战 |
| brawler | 库 | 依赖 brawler 独立库 |

---

### 模块：wsf_multiresolution

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_multiresolution/source/`
**源码/头文件数：** 14
**描述：** 多分辨率建模插件：基于保真度的平台组件替换。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 14 | 多分辨率插件主源码 |
| test | `test/` | 3 | 单元测试 |
| grammar | `grammar/` | 0 | 语法定义 |
| test_mission | `test_mission/` | 0 | Test mission scenarios |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 11 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfMultiresolutionPlatformComponent | class（类） | WsfPlatformComponent, WsfObject | 多分辨率平台组件基类 |
| WsfMultiresolutionTypes | class（类） | WsfObjectTypeList<...> | 多分辨率类型注册表 |
| WsfMultiresolutionTypesRegistration | class（类） | WsfScenarioExtension | 类型注册扩展 |
| MultiresolutionComponentFactory | class（类） | WsfComponentFactory<WsfPlatform> | 多分辨率组件工厂 |
| WsfMultiresolutionWrapperMetaModel | class（类） | WsfMultiresolutionPlatformComponent<DerivedComponent> | 包装器元模型模板 |
| FidelityRange | struct（结构体） | 无 | 保真度范围定义 |
| ComponentName | struct（结构体） | 无 | 组件名辅助 |
| PlatformComponentName | struct（结构体） | 无 | 平台组件名辅助 |
| ModelWithFidelity | struct（结构体） | 无 | 带保真度级别的模型 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 多分辨率挂接 WsfSimulation/WsfPlatform |

---

### 模块：brawler

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_brawler/brawler/`
**源码/头文件数：** 12
**描述：** Brawler 交战模型独立库。

#### 子系统结构

平铺结构 —— 单层目录，含 12 个源码/头文件。

#### 核心类（来自 1 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| BrawlerMIND | class（类） | 无 | Brawler MIND（任务/意图/导航/决策）模型 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：wsf_alternate_locations

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_alternate_locations/source/`
**源码/头文件数：** 7
**描述：** 备选位置与路径规划插件：加权位置选择、平台组件集成。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 7 | 备选位置主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 5 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| SimulationExtension | class（类） | WsfSimulationExtension | 备选位置仿真扩展 |
| Component | class（类） | WsfObject, WsfPlatformComponent | 备选位置平台组件 |
| ComponentInitialized | class（类） | 无 | 组件初始化事件结果 |
| WeightedLocation | struct（结构体） | 无 | 加权位置候选 |
| InputData | struct（结构体） | 无 | 仿真扩展输入数据 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：wsf_mil_parser

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_mil_parser/source/`
**源码/头文件数：** 7
**描述：** 军事语法解析扩展: RF jammer parser model.

#### 子系统结构

平铺结构 —— 单层目录（`source/`），含 7 个源码/头文件。

#### 核心类（来自 1 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| Mode | class（类） | WsfPProxyNode | RF 干扰机模式解析模型（WsfPM_RF_Jammer） |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf_parser | 库 | 扩展解析器的 WsfPProxyNode |
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：resources

**路径：** `afsim-2_9`
**源码位置：** `resources/shaders/`
**源码/头文件数：** 6
**描述：** 静态资源：地图、模型、着色器（6 个着色器源码/头文件）。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| shaders | `shaders/` | 6 | GLSL 着色器源文件 |
| maps | `maps/` | 0 | 地图资源文件 |
| models | `models/` | 0 | 3D 模型文件 |
| data | `data/` | 0 | 数据文件 |

#### 核心类

该模块在符号索引中无 class/struct 符号（着色器文件不包含 C++ 类）。

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | WSF 可视化使用的资源 |

---

### 模块：wsf_sosm

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_sosm/source/`
**源码/头文件数：** 6
**描述：** 特种作战/太空作战模型（SOSM）插件：SOSM 传感器模式集成。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 6 | SOSM 插件主源码 |
| sosm | `sosm/` | 45 | SOSM 共享库 |
| grammar | `grammar/` | 0 | 语法定义 |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 1 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| SOSM_Mode | class（类） | WsfSensorMode | SOSM 传感器模式实现 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |
| sosm | 库 | 使用 SOSM 共享库进行光谱计算 |

---

### 模块：profiling

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/tools/profiling/`
**源码/头文件数：** 5
**描述：** 性能分析工具：CSV 工具、计时、版本信息。

#### 子系统结构

平铺结构 —— 单层目录，含 5 个源码/头文件。

#### 核心类（来自 3 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| Exception | class（类） | UtException | 性能分析异常类型 |
| VersionInfo | struct（结构体） | 无 | 性能分析版本信息 |
| QuotedStringAndNewStartPos | struct（结构体） | 无 | CSV 解析辅助 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：wsf_annotation

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_annotation/source/`
**源码/头文件数：** 5
**描述：** 场景标注插件：装饰、兴趣点、距离环、事件管道集成。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 5 | 标注插件主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 8 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| WsfAnnotationExtension | class（类） | WsfScenarioExtension, WsfAnnotationInput | 标注场景扩展 |
| WsfAnnotationInput | class（类） | 无 | 标注输入配置 |
| EventPipe | class（类） | WsfEventPipeLogger | 标注事件管道 |
| EventPipeInterface | class（类） | WsfSimulationExtension | 标注事件管道接口 |
| DecorationData | struct（结构体） | 无 | 装饰显示数据 |
| PoiData | struct（结构体） | 无 | 兴趣点数据 |
| RangeRingData | struct（结构体） | 无 | 距离环显示数据 |
| AnnotationInfo | struct（结构体） | 无 | 标注信息容器 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：osgdb_osgearth_dted_tms

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/?`
**源码/头文件数：** 5
**描述：** OSGEarth DTED TMS 数据库插件：地形瓦片源。

#### 子系统结构

平铺结构 —— 单层目录，含 5 个源码/头文件。

#### 核心类（来自 2 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| DtedTmsTileSource | class（类） | TileSource | DTED TMS 地形瓦片源 |
| DtedTmsOptions | class（类） | TileSourceOptions | DTED TMS 配置选项 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| OSGEarth | 库 | 依赖 OSGEarth 瓦片源框架 |

---

### 模块：wizard

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wizard/`
**源码/头文件数：** 3
**描述：** 场景编辑向导：CRD 文件导入、USMTF 处理、主程序及子插件.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| main | `main/` | 2 | 向导主程序 |
| lib | `lib/` | 248 | 向导共享库 |
| plugins | `plugins/` | 555 | 向导子插件 |
| usmtf | `usmtf/` | 254 | USMTF 报文处理 |
| test | `test/` | 2 | 单元测试 |
| tests | `tests/` | 0 | 集成测试 |
| data | `data/` | 0 | 数据文件 |

#### 核心类（来自 1 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| DerivedMessageForTest | class（类） | MapUtils::Message | 地图工具测试消息类 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |
| lib | 库 | 使用共享 CRD 元素库 |

---

### 模块：sensor_plot

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/sensor_plot/`
**源码/头文件数：** 3
**描述：** 传感器覆盖/探测距离可视化 tool.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 3 | 传感器绘图主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| tests | `tests/` | 0 | Tests |
| doc | `doc/` | 0 | Documentation |
| data | `data/` | 0 | 数据文件 |

#### 核心类（来自 1 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| StubInterface | class（类） | WsfScenarioExtension | 传感器绘图扩展桩接口 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |
| sensor_plot_lib | 库 | 使用传感器绘图库进行计算 |

---

### 模块：wsf_argo8

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_argo8/source/`
**源码/头文件数：** 3
**描述：** ARGO8 集成插件.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 3 | ARGO8 插件主源码 |
| argo8 | `argo8/` | 11 | ARGO8 共享库 |
| grammar | `grammar/` | 0 | 语法定义 |
| doc | `doc/` | 0 | Documentation |

#### 核心类

该模块在符号索引中无 class/struct 符号。

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：wsf_iads_c2_lib

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/wsf_plugins/wsf_iads_c2_lib/source/`
**源码/头文件数：** 3
**描述：** 综合防空系统（IADS）C2 库插件.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 159 | IADS C2 插件主源码（含 iadsLib 副本） |
| iadsLib | `iadsLib/` | 149 | IADS 核心库 |
| test | `test/` | 3 | 单元测试 |
| grammar | `grammar/` | 0 | 语法定义 |
| doc | `doc/` | 0 | Documentation |

#### 核心类

该模块的类符号在符号索引中归属于 `iadsLib` 模块名。核心类参见上方的 `iadsLib` 模块。

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | IADS C2 扩展平台/传感器/武器协同 |
| iadsLib | 库 | Uses IADS 核心库 |

---

### 模块：mission

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/mission/source/`
**源码/头文件数：** 2
**描述：** 任务规划工具（2 个源文件）.

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 2 | 任务主源码 |
| tests | `tests/` | 0 | Tests |
| doc | `doc/` | 0 | Documentation |

#### 核心类

该模块在符号索引中无 class/struct 符号。

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：util

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/tools/util/`
**源码/头文件数：** 2
**描述：** 通用工具：代码计时工具。

#### 子系统结构

平铺结构 —— 单层目录，含 2 个源码/头文件。

#### 核心类（来自 2 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| UtCodeTimerNode | class（类） | 无 | 性能测量代码计时节点 |
| UtScopeTimer | class（类） | 无 | RAII 作用域代码计时器 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：wsf_grammar_check

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_grammar_check/source/`
**源码/头文件数：** 2
**描述：** 场景脚本语法校验工具.

#### 子系统结构

平铺结构 —— 单层目录（`source/`），含 2 个源码/头文件。

#### 核心类（来自 1 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| ParseSourceProvider | class（类） | WsfParseSourceProvider | 语法检查解析源提供器 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf_parser | 库 | 扩展解析器的 WsfParseSourceProvider |

---

### 模块：wsf_weapon_server

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/core/wsf_weapon_server/source/`
**源码/头文件数：** 2
**描述：** 武器计算服务器：LAR 计算、基于 TCP 的武器遥测。

#### 子系统结构

| 子系统 | 位置 | 文件数 | 描述 |
|-----------|----------|--------|------|
| source | `source/` | 2 | 武器服务器主源码 |
| grammar | `grammar/` | 0 | 语法定义 |
| doc | `doc/` | 0 | Documentation |

#### 核心类（来自 11 个 class/struct 符号）

| 类名 | 类型 | 基类 | 描述 |
|-------|------|-------------|-------------|
| UniqueWeaponKey | class（类） | 无 | 武器唯一标识 |
| TCPUpdateEvent | class（类） | WsfEvent | 武器服务器 TCP 更新事件 |
| LARInputType | struct（结构体） | 无 | 可发射区域输入数据 |
| LAROutputType | struct（结构体） | 无 | LAR 计算输出 |
| MissileIdType | struct（结构体） | 无 | 导弹标识类型 |
| InitVariablesType | struct（结构体） | 无 | 初始化变量 |
| UmbilicalVariablesType | struct（结构体） | 无 | 脐带连接变量 |
| LaunchVariablesType | struct（结构体） | 无 | 发射参数 |
| TelemetryVariablesType | struct（结构体） | 无 | 遥测数据变量 |
| LaunchMessageType | struct（结构体） | 无 | 发射报文格式 |

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 模块：mover

**路径：** `afsim-2_9`
**源码位置：** `swdev/src/?`
**源码/头文件数：** 2
**描述：** 运动体工具（2 个源文件）.

#### 子系统结构

平铺结构 —— 单层目录，含 2 个源码/头文件。

#### 核心类

该模块在符号索引中无 class/struct 符号。

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |

---

### 单文件模块：afperf、cli、ReaderWriterMod、ReaderWriterOGL、exec、legacy_test、proxy_test、pack_to_cpp

以下为单文件模块，各含 1 个源码/头文件，均为平铺结构。

#### 子系统结构

平铺结构 —— 每个模块为单层目录，含 1 个源码/头文件。

#### 核心类

这些模块在符号索引中无 class/struct 符号（单文件工具、读写插件或测试基础设施）。

#### 关键依赖

| 依赖项 | 类型 | 描述 |
|------------|------|-------------|
| wsf | 框架 | 依赖核心 WSF 框架 |
| OSG | 库 | ReaderWriterMod/ReaderWriterOGL 依赖 OpenSceneGraph |

---

## 架构说明

1. **源码位置**：边界文件中的模块名对应逻辑模块分组。实际 C++ 源码位于 `swdev/src/` 下：
   - 核心库：`swdev/src/core/wsf*/source/`
   - Plugins: `swdev/src/wsf_plugins/wsf_*/source/`
   - 应用：`swdev/src/engage/`、`swdev/src/wizard/`、`swdev/src/warlock/`、`swdev/src/mystic/`
   - 工具：`swdev/src/tools/`、`swdev/src/mission/`、`swdev/src/sensor_plot/` 等

2. **三层扩展模型**：Application（应用）> Scenario（场景）> Simulation（仿真）三层扩展提供生命周期钩子（WsfApplicationExtension、WsfScenarioExtension、WsfSimulationExtension）。

3. **组件模型**：所有仿真对象均通过 WsfComponentFactory 派生自 WsfComponent。WsfPlatformComponent 是挂载到平台的组件的基类。

4. **插件发现**：构建系统通过 `wsf_module` 标记文件发现可选模块。

5. **自定义 DSL**：AFSIM 使用自定义领域特定语言，由 wsf_parser 通过 PProxy 序列化（WsfPProxyStructType、WsfParseAction* 类）进行解析。

6. **信号/特征框架**：通过 WsfRadarSignature、WsfChaffRadarSignature 等实现多域特征（RCS、红外、光学、声学）。

7. **行为树**：wsf 核心中包含两级行为树引擎（WsfBehaviorTree + WsfAdvancedBehaviorTree）。

8. **模块层次**：`source` 是总括模块；逻辑模块为核心库（wsf_*）、插件和应用。

9. **构建系统**：CMake 3.7+，每个模块配有自定义 `wsf_cmake_extension.cmake`。

10. **类名来源**：本文档中所有类名均来自 `symbol-index.jsonl`，可通过索引追溯至实际 C++ 声明。
