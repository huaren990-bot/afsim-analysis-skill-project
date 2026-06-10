AFSIM 源码认知分析计划
背景
根据 tools/prompts/afsim-source-cognition 系统提示词.md 的要求，作为 afsim-source-cognition 智能体，需要对 AFSIM 2.9.0 仿真框架的 C++ 源代码进行全面分析，产出：

4 个结构化索引文件（JSONL 格式）
2 个架构文档（Markdown + Mermaid 图表）
开发者校对循环
范围确定
经用户确认：核心框架优先 + 文件级完整分析。

分析目标模块（按优先级排序）
优先级	模块	路径	文件数	说明
P0	wsf/source	src/core/wsf/source/	~250 (仅 .hpp/.cpp，排除子目录)	AFSIM 仿真引擎核心
P0	wsf/source 子目录	src/core/wsf/source/{comm,dis,mover,observer,processor,script,sensor,traffic,xio,ext,event_pipe,xio_sim}/	~281	核心子系统
P1	wsf_mil/source	src/core/wsf_mil/source/	~213	军事域仿真扩展
P1	wsf_space/source	src/core/wsf_space/source/	~171	空间域仿真
P2	wsf_nx, wsf_parser, wsf_util	各 source 目录	~124	解析器和工具
P3	wsf_plugins（精选）	src/wsf_plugins/	按需	关键插件
首轮聚焦 P0：src/core/wsf/source/ 目录（约 531 个文件），这是整个框架的基石。

分析策略
由于文件数量巨大，采用 分批+多智能体并行 策略：

Phase 1: 目录探索与文件分组
将 wsf/source 的文件按子系统分为 10-15 个批次，每批 30-50 个文件：

核心基础：WsfApplication, WsfSimulation, WsfScenario, WsfObject, WsfComponent, WsfNamed
平台与运动：WsfPlatform, WsfPlatformPart, WsfMover*, WsfFuel
跟踪管理：WsfTrack, WsfTrackManager, WsfLocalTrack, WsfCorrelation*, WsfFusion*
传感器：WsfSensor*, WsfFieldOfView*, WsfEM_*, WsfSignature*, WsfAntennaPattern*
通信：comm/ 子目录下所有文件
武器：WsfWeapon*, WsfIntercept
行为树：WsfBehaviorTree*, WsfAdvancedBehaviorTree*
地形与环境：WsfTerrain, WsfZone*, WsfEnvironment, WsfEarthGravityModel
事件与消息：WsfEvent*, WsfMessage*, WsfCallback*
脚本与语法：script/ 子目录文件, WsfGrammarInterface
可视化与绘图：WsfDraw, WsfVisual*, WsfImage*
DIS/网络接口：dis/ 子目录
扩展与插件：WsfExtension*, WsfPluginManager
工具类：WsfUtil, WsfRandom*, WsfDateTime, WsfStringTable, WsfVariable
多线程：WsfMultiThreadManager, WsfThread*
Phase 2: 并行文件分析
对每个批次启动 Workflow，采用 pipeline 模式：

阶段1 — 阅读：每个文件由一个 agent 阅读，提取类、函数、枚举、宏、全局变量
阶段2 — 索引记录：将提取结果追加到对应的索引文件
阶段3 — 依赖识别：记录跨文件依赖关系
每个文件分析产出：

file-index.jsonl 中的一条记录
symbol-index.jsonl 中的 N 条记录（类、枚举、重要类型）
function-index.jsonl 中的 M 条记录（函数/方法）
dependency-index.jsonl 中的 K 条记录（调用/包含依赖）
Phase 3: 架构归纳
在所有文件分析完成后：

基于积累的索引推导子系统划分
用 Mermaid 绘制组件图和数据流图
编写架构草稿文档
Phase 4: 校对与定稿
向用户提交架构总结和关键问题
根据反馈修正
标记最终版本
输出目录结构
workspace/source-index/
├── file-index.jsonl        # 文件级索引
├── symbol-index.jsonl      # 符号索引（类、枚举、全局变量等）
├── function-index.jsonl    # 函数/方法索引
└── dependency-index.jsonl  # 依赖关系索引

docs/architecture/
├── afsim-architecture.md   # 架构文档（含 Mermaid 图）
└── module-dependency.md    # 模块依赖表
关键文件路径
提示词文件：tools/prompts/afsim-source-cognition 系统提示词.md
源码根目录：afsim_2.9.0_src_linux/src/core/wsf/source/
索引输出目录：workspace/source-index/
架构文档输出目录：docs/architecture/
验证方法
完整性验证：检查每个已分析的 .hpp/.cpp 文件在 file-index.jsonl 中都有对应记录
一致性验证：symbol-index 和 function-index 中引用的文件路径和行号与实际源码一致
依赖完整性：dependency-index 中记录的依赖关系目标在 symbol-index 中应有对应条目
架构图验证：Mermaid 图中的每个组件都能在索引文件中找到对应的类/模块
实施步骤
第一步：创建输出目录
mkdir -p workspace/source-index docs/architecture
第二步：分批次分析（使用 Workflow 并行化）
每批启动一个 Workflow，包含：

多个并行 agent 各自分析 5-10 个文件
每个 agent 输出结构化的索引记录
第三步：汇总与架构生成
基于所有索引记录，推导架构并生成文档。

第四步：用户校对
提交架构文档草稿，等待校对确认后定稿。