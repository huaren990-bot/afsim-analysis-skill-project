afsim_2.9.0_src_linux/
├── dependencies/              # 第三方依赖和资源文件
│   ├── 3rd_party/             # 预编译的第三方库包（curl/ffmpeg/gdal/geos/gtest/openssl/osg/osgEarth等）
│   └── resources/             # 仿真资源文件
│       ├── maps/              # 地图数据
│       └── models/            # 3D模型文件
│
└── src/                       # 全部源代码
    │
    ├── cmake/                 # CMake构建系统配置（模块/预设/模板/发行版/Logo）
    ├── doc/                   # 全局文档（changelog/开发者文档/用户手册/图片）
    │
    ├── core/                  # ═══ 核心框架 ═══
    │   ├── wsf/               # 武器系统框架（Weapon System Framework）— 仿真引擎核心
    │   │   ├── source/        # 基础类：WsfApplication/WsfSimulation/WsfPlatform/WsfComponent 等
    │   │   ├── source/comm/   # 通信子系统（通信设备/协议/路由器/媒体）
    │   │   ├── source/dis/    # IEEE 1278.1 DIS 分布式仿真协议实现
    │   │   ├── source/mover/  # 运动模型（空气/地面/海洋/跟随/旋翼等）
    │   │   ├── source/sensor/ # 传感器基类和通用传感器模型
    │   │   ├── source/processor/ # 数据处理器
    │   │   ├── source/observer/  # 观察者模式实现（各类事件监听器）
    │   │   ├── source/script/    # 脚本系统（语法接口/上下文/脚本管理器）
    │   │   ├── source/xio/       # 外部IO接口（序列化/反序列化）
    │   │   ├── source/xio_sim/   # 仿真IO
    │   │   ├── source/traffic/   # 交通流模拟
    │   │   ├── source/ext/       # 扩展接口
    │   │   └── source/event_pipe/# 事件流管道
    │   │
    │   ├── wsf_mil/           # 军事域扩展 — 武器/电子战/军事传感器/军事通信
    │   │   └── source/
    │   │       ├── weapon/    # 发射计算机（A2A/ATA/ATG/弹道/轨道/SAM）
    │   │       ├── mover/     # 制导运动模型
    │   │       ├── sensor/    # 军事传感器（光电/红外/表面波雷达等）
    │   │       ├── comm/      # 军事通信扩展
    │   │       ├── ew/        # 电子战模块
    │   │       ├── dis/       # DIS军事扩展
    │   │       ├── observer/  # 军事域观察者
    │   │       ├── processor/ # 军事域处理器
    │   │       ├── script/    # 军事脚本类（武器/激光/发射计算机脚本接口）
    │   │       └── xio/       # 军事域外部IO
    │   │
    │   ├── wsf_space/         # 空间域扩展 — 轨道力学/空间机动/空间传感器
    │   │   └── source/
    │   │       └── maneuvers/ # 空间机动模型
    │   │
    │   ├── wsf_nx/            # "下一代"框架 — 新版传感器/处理器实现
    │   │   └── source/
    │   │       ├── sensor/    # 新传感器模型
    │   │       ├── processor/ # 新处理器模型
    │   │       └── ew/        # 电子战扩展
    │   │
    │   ├── wsf_parser/        # 语法解析器 — 将输入文件（.txt场景定义）解析为C++对象
    │   │
    │   ├── wsf_util/          # 基础工具库 — UtStringId/UtException等底层类型
    │   │
    │   ├── wsf_ripr/          # RIPR（RIPR = ???）— JobBoard/Job/Manager 作业调度系统
    │   │
    │   ├── wsf_cyber/         # 网络战/赛博域 — 网络攻击/攻击参数/赛博组件角色
    │   │
    │   ├── wsf_l16/           # Link-16 战术数据链 — 消息格式/计算机处理器/解析器
    │   │
    │   ├── wsf_mtt/           # 多目标跟踪（Multi-Target Tracking）— 活动/候选/胚胎跟踪
    │   │
    │   ├── wsf_mil_parser/    # 军事域的语法解析器
    │   │
    │   ├── wsf_grammar_check/ # 语法检查器
    │   │
    │   ├── wsf_weapon_server/ # 武器服务器 — 独立武器计算服务
    │   │
    │   └── sensor_plot_lib/   # 传感器绘图库 — 传感器覆盖范围可视化
    │
    ├── engage/                # 交战分析工具 — 处理仿真事件输出/生成交战报告
    │
    ├── evt_reader/            # 事件读取器 — 读取和可视化 .evt 事件文件
    │
    ├── mission/               # 任务级仿真入口 — mission.cpp 可执行程序入口
    │
    ├── mystic/                # 后处理可视化工具 — 结果数据3D可视化（基于OSG）
    │   ├── exec/              # 可执行入口
    │   ├── lib/               # 可视化库（环境/平台/事件/结果数据）
    │   ├── plugins/           # 可视化插件（空战结果/轨道结果/态势感知显示）
    │   └── python/            # Python接口（pymystic.py）
    │
    ├── warlock/               # 实时仿真控制器 — 传感器控制/仿真命令/交互式场景管理
    │   ├── warlock_core/      # 核心库
    │   ├── warlock_exec/      # 可执行入口
    │   ├── plugins/           # 控制器插件（SensorController等）
    │   └── data/              # 示例场景数据
    │
    ├── wizard/                # 场景编辑向导 — GUI工具用于创建/编辑AFSIM场景文件
    │   ├── lib/               # 向导核心库
    │   ├── main/              # GUI主程序入口
    │   ├── plugins/           # 向导插件
    │   └── usmtf/             # USMTF（美军标准消息文本格式）解析/验证
    │
    ├── mover_creator/         # 运动体创建工具 — GUI工具用于定义飞行器/武器气动和运动参数
    │   ├── source/            # 气动几何/性能/脚本生成（支持6DOF/质点模型）
    │   ├── ui/                # Qt UI文件
    │   └── data/              # 预置数据（翼型/发动机/大气）
    │
    ├── weapon_tools/          # 武器分析工具 — 生成发射计算机配置/杀伤区计算
    │
    ├── sensor_plot/           # 传感器绘图工具 — 传感器覆盖范围2D可视化
    │
    ├── post_processor/        # 后处理器 — 仿真结果数据分析/轨迹可视化/报告生成
    │   ├── exec/              # 可执行入口
    │   ├── lib/               # 后处理核心库
    │   └── WizPostProcessor/  # 向导式后处理器（滤波器/发射机/报告）
    │
    ├── tools/                 # ═══ 辅助工具集 ═══
    │   ├── 3rd_party-cmake/   # 第三方CMake模块
    │   ├── artificer/         # Artificer工具（???）
    │   ├── dis/               # DIS协议工具
    │   ├── genio/             # 通用IO生成工具
    │   ├── geodata/           # 地理数据处理工具
    │   ├── misc/              # 杂项工具
    │   ├── packetio/          # 数据包IO工具
    │   ├── profiling/         # 性能分析工具
    │   ├── scene_gen/         # 场景生成工具
    │   ├── tracking_filters/  # 跟踪滤波器工具（Kalman/AlphaBeta参数调优）
    │   ├── util/              # 通用C++工具库
    │   ├── utilosg/           # OpenSceneGraph工具库
    │   ├── utilqt/            # Qt工具库
    │   ├── util_script/       # 脚本工具
    │   ├── vespatk/           # VESPA Toolkit（???）
    │   └── wkf/               # WKF工具（???）
    │
    └── wsf_plugins/           # ═══ 插件生态（23个） ═══
        ├── wsf_air_combat/        # 空战插件 — 空对空交战/态势感知
        ├── wsf_alternate_locations/ # 备用位置插件
        ├── wsf_annotation/        # 标注插件
        ├── wsf_argo8/             # ARGO8 插件（???）
        ├── wsf_brawler/           # Brawler 空战仿真引擎集成
        ├── wsf_coverage/          # 覆盖范围分析插件
        ├── wsf_fires/             # 火力支援插件 — 弹道/火力路径/火力平台
        ├── wsf_iads_c2_lib/       # 综合防空C2库 — 拦截计算/战损评估/武器配对
        ├── wsf_multiresolution/   # 多分辨率仿真插件
        ├── wsf_oms_uci/           # OMS/UCI 标准接口插件
        ├── wsf_p6dof/             # 质点6自由度插件 — 六自由度质点运动/制导
        ├── wsf_scenario_analyzer/ # 场景分析器
        ├── wsf_scenario_analyzer_iads_c2/ # IADS C2 场景分析器
        ├── wsf_simdis/            # SIMDIS 可视化集成
        ├── wsf_six_dof/           # 六自由度插件 — 六自由度刚体运动/制导
        └── wsf_sosm/              # SOSM（???）— 包含简单大气模型
