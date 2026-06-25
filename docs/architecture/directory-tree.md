# Source Root 目录表

> 根路径：`/Users/hjt/afsim/afsim-analysis-skill-project/source_root`
> 展示范围：`source_root` 可见目录；排除所有 `.` 开头的隐藏目录、隐藏文件和指定元数据文件。
> 展示方式：主目录表展示 depth 1-2；各二级目录表展示 depth 2-4。

## 1. 阅读说明

本表面向没有 AFSIM 基础的人工阅读者。每行对应一个目录或顶级文件，提供中文用途说明、文件计数和人工确认状态。红色“待人工确认”表示仅凭目录名无法可靠判断用途，需要后续人工或源码证据确认。

## 2. 主目录表

主目录表用于快速了解 `source_root` 和 `afsim-2_9` 的顶层组成。

| 层级 | 类型 | 路径 | 中文说明 | 可见文件 | 已分类 | 源/头 | 确认状态 |
|------|------|------|----------|----------|--------|-------|----------|
| 0 | 目录 | `source_root` | 源码根目录，承载本次分析输入；当前目录树只展示进入源码分析视野的可见目录。 | 39,894 | 39,876 | 17,342 | 已说明 |
| 1 | 目录 | `afsim-2_9` | AFSIM 2.9 主发布目录，包含源码、演示场景、文档、资源、工具与培训材料。 | 39,894 | 39,876 | 17,342 | 已说明 |
| 2 | 目录 | `afsim-2_9/demos` | 演示场景目录，保存可运行示例、平台、传感器、武器配置和演示输出。 | 5,183 | 5,183 | 0 | 已说明 |
| 2 | 目录 | `afsim-2_9/documentation` | 发布文档目录，保存 HTML 文档、变更记录和用户可读说明。 | 5,044 | 5,044 | 0 | 已说明 |
| 2 | 目录 | `afsim-2_9/resources` | 运行资源目录，保存地图、模型、shader、数据和运行时资源。 | 1,288 | 1,288 | 6 | 已说明 |
| 2 | 目录 | `afsim-2_9/swdev` | 软件开发目录，保存 C++ 源码、构建脚本和开发依赖，是默认架构分析的主要入口。 | 26,854 | 26,836 | 17,184 | 已说明 |
| 2 | 目录 | `afsim-2_9/tools` | 发布包工具目录，保存随包脚本和辅助工具。 | 101 | 101 | 0 | 已说明 |
| 2 | 目录 | `afsim-2_9/training` | 培训材料目录，保存面向开发者和用户的实验、教程和示例代码；默认不进入架构依赖分析。 | 1,423 | 1,423 | 152 | 已说明 |

## 3. 二级目录明细表

以下各表按 `afsim-2_9` 下的二级目录拆分，展示该目录向下到 depth 4 的结构。

### 3.1. demos目录表

| 层级 | 类型 | 路径 | 中文说明 | 可见文件 | 已分类 | 源/头 | 确认状态 |
|------|------|------|----------|----------|--------|-------|----------|
| 2 | 目录 | `afsim-2_9/demos` | 演示场景目录，保存可运行示例、平台、传感器、武器配置和演示输出。 | 5,183 | 5,183 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/acoustic` | 目录 acoustic/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/acoustic/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/acoustic/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/acoustic/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/aea_iads` | aea_iads 目录，保存综合防空系统相关示例、插件或配置。 | 45 | 45 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/aea_iads/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/aea_iads/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/aea_iads/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/aea_iads/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 7 | 7 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/aea_iads/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/aea_iads/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/aea_iads/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/aea_iads/sensors/esm_rwr` | 电子支援/雷达告警目录，保存 ESM/RWR 传感器配置。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/aea_iads/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/aea_iads/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/aea_iads/weapons/jammer` | 干扰器目录，保存电子干扰载荷或武器配置。 | 5 | 5 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/air_to_air` | 目录 air_to_air/ 的具体用途无法仅凭目录名可靠判断。 | 101 | 101 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 8 | 8 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/platforms/fxw` | 目录 fxw/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/prdata` | 概率或参数数据目录，保存场景运行所需的补充数据。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/rules` | 规则目录，保存交战规则、行为规则或示例规则文件。 | 20 | 20 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 7 | 7 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/sensors/esm_rwr` | 电子支援/雷达告警目录，保存 ESM/RWR 传感器配置。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/signatures/signature_conversion` | 目录 signature_conversion/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/six_dof_types` | six_dof_types 目录，保存六自由度飞行动力学或相关示例数据。 | 23 | 23 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/six_dof_types/aircraft` | 航空器目录，保存具体飞机或飞行器型号数据。 | 20 | 20 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/six_dof_types/environment` | 环境数据目录，保存大气、地形或运行环境相关配置。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/air_to_air/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 9 | 9 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/air_to_air/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 9 | 9 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/alternate_locations` | 目录 alternate_locations/ 的具体用途无法仅凭目录名可靠判断。 | 23 | 23 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/alternate_locations/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/alternate_locations/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/alternate_locations/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alternate_locations/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alternate_locations/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alternate_locations/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alternate_locations/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alternate_locations/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/alternate_locations/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alternate_locations/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alternate_locations/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/alternate_locations/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/alternate_locations/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/alv_routing` | 目录 alv_routing/ 的具体用途无法仅凭目录名可靠判断。 | 16 | 16 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/alv_routing/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/alv_routing/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alv_routing/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alv_routing/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alv_routing/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alv_routing/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/alv_routing/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 2 | 2 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/ballistic` | 目录 ballistic/ 的具体用途无法仅凭目录名可靠判断。 | 16 | 16 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/ballistic/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ballistic/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown` | 目录 ballistic_missile_shootdown/ 的具体用途无法仅凭目录名可靠判断。 | 32 | 32 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 7 | 7 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ballistic_missile_shootdown/weapons/ssm` | 地地或舰地导弹目录，保存地面或海上发射武器配置。 | 4 | 4 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/base_types` | 目录 base_types/ 的具体用途无法仅凭目录名可靠判断。 | 352 | 352 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/base_types/patterns` | 模式目录，保存路径、行为或任务模式配置。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/base_types/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 61 | 61 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/platforms/brawler` | brawler 目录，保存 Brawler 空战交战模型相关内容。 | 38 | 38 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/base_types/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 177 | 177 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/processors/quantum_agents` | Quantum 智能体目录，保存示例中的智能体行为配置。 | 66 | 66 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/processors/ripr_agents` | RIPR 智能体目录，保存 RIPR 相关代理或任务处理配置。 | 91 | 91 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/processors/timeline_agents` | 时间线智能体目录，保存按时间线驱动的行为配置。 | 18 | 18 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/base_types/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 25 | 25 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/sensors/eo_ir` | 光电/红外目录，保存 EO/IR 传感器配置。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/sensors/esm_rwr` | 电子支援/雷达告警目录，保存 ESM/RWR 传感器配置。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 21 | 21 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/base_types/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/signatures/plt` | 目录 plt/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/base_types/signatures/salram` | 目录 salram/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/base_types/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 78 | 78 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 24 | 24 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/weapons/other` | 目录 other/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/base_types/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 22 | 22 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types/weapons/ssm` | 地地或舰地导弹目录，保存地面或海上发射武器配置。 | 28 | 28 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/base_types_nx` | 目录 base_types_nx/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/base_types_nx/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/base_types_nx/weapons/ssm` | 地地或舰地导弹目录，保存地面或海上发射武器配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/bearing_only` | 目录 bearing_only/ 的具体用途无法仅凭目录名可靠判断。 | 16 | 16 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/bearing_only/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/bearing_only/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/bearing_only/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/bearing_only/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/bearing_only/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/bearing_only/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/behavior_tree` | 目录 behavior_tree/ 的具体用途无法仅凭目录名可靠判断。 | 129 | 129 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/behavior_tree/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/behavior_tree/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/behavior_tree/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/behavior_tree/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/behavior_tree/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 16 | 16 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/behavior_tree/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 87 | 87 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/behavior_tree/processors/quantum_agents` | Quantum 智能体目录，保存示例中的智能体行为配置。 | 87 | 87 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/behavior_tree/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 7 | 7 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/behavior_tree/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 7 | 7 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/brawler` | brawler 目录，保存 Brawler 空战交战模型相关内容。 | 64 | 64 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/brawler/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/brawler/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 42 | 42 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/brawler/platforms/alternatives` | 目录 alternatives/ 的具体用途无法仅凭目录名可靠判断。 | 33 | 33 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/brawler/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 10 | 10 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/brawler/processors/quantum_agents` | Quantum 智能体目录，保存示例中的智能体行为配置。 | 10 | 10 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/brawler/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/brawler/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/brawler/weapons/other` | 目录 other/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/chaff` | 目录 chaff/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/chaff/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/chaff/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/chaff/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/cislunar` | cislunar 目录，保存空间、卫星或月地空间相关场景/模型。 | 8 | 8 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cislunar/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cislunar/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cislunar/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cislunar/elements` | 目录 elements/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/cislunar/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cislunar/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cislunar/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/ciws` | 目录 ciws/ 的具体用途无法仅凭目录名可靠判断。 | 13 | 13 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/ciws/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ciws/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ciws/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ciws/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ciws/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ciws/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ciws/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ciws/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ciws/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ciws/weapons/guns` | 火炮目录，保存炮类武器配置。 | 2 | 2 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/comm` | 目录 comm/ 的具体用途无法仅凭目录名可靠判断。 | 11 | 11 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/comm/comms` | 通信配置目录，保存通信链路、网络或消息配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/comm/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/comm/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/comm/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/comm/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/comm/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/coverage_demos` | Coverage Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 40 | 40 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/coverage_data` | 目录 coverage_data/ 的具体用途无法仅凭目录名可靠判断。 | 0 | 0 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/coverage_grids` | 目录 coverage_grids/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/coverage_demos/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/coverage_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/dted` | 目录 dted/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/coverage_demos/dted/w107` | 目录 w107/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 7 | 7 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 5 | 5 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/terrain` | 目录 terrain/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/coverage_demos/zones` | 目录 zones/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/cyber` | cyber 目录，保存网络战或网络相关场景/模型。 | 81 | 81 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/cyber` | cyber 目录，保存网络战或网络相关场景/模型。 | 9 | 9 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/cyber/cyber_attacks` | cyber_attacks 目录，保存网络战或网络相关场景/模型。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/cyber/cyber_effects` | cyber_effects 目录，保存网络战或网络相关场景/模型。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/cyber/cyber_protections` | cyber_protections 目录，保存网络战或网络相关场景/模型。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/exfiltrate_demo` | Exfiltrate Demo 示例目录，保存与该主题相关的演示场景、配置和说明。 | 28 | 28 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/exfiltrate_demo/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/exfiltrate_demo/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 15 | 15 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/exfiltrate_demo/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/exfiltrate_demo/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/exfiltrate_demo/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 9 | 9 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 5 | 5 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/cyber/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/cyber/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/distributed_operations` | 目录 distributed_operations/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/distributed_operations/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/distributed_operations/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/draw` | 目录 draw/ 的具体用途无法仅凭目录名可靠判断。 | 7 | 7 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/draw/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/draw/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/draw/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/draw/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/draw/sensors/human` | 目录 human/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/draw/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/draw/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/draw/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/electronic_warfare` | 目录 electronic_warfare/ 的具体用途无法仅凭目录名可靠判断。 | 90 | 90 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/electronic_warfare/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/electronic_warfare/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/electronic_warfare/test_false_targets` | 目录 test_false_targets/ 的具体用途无法仅凭目录名可靠判断。 | 27 | 27 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_false_targets/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_false_targets/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 11 | 11 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_false_targets/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_false_targets/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_false_targets/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/electronic_warfare/test_multi_beam` | 目录 test_multi_beam/ 的具体用途无法仅凭目录名可靠判断。 | 17 | 17 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_multi_beam/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_multi_beam/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_multi_beam/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_multi_beam/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/electronic_warfare/test_multi_beam/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/engage` | 目录 engage/ 的具体用途无法仅凭目录名可靠判断。 | 24 | 24 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/engage/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/engage/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/engage/launchers` | 目录 launchers/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/engage/radars` | 目录 radars/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/engage/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/engage/targets` | 目录 targets/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/engage/trackers` | 目录 trackers/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/engage/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/example_scripts` | 目录 example_scripts/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/exchange_proc` | 目录 exchange_proc/ 的具体用途无法仅凭目录名可靠判断。 | 8 | 8 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/exchange_proc/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/exchange_proc/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/exchange_proc/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/fires` | 目录 fires/ 的具体用途无法仅凭目录名可靠判断。 | 25 | 25 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/fires/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/fires/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/fires/types` | 目录 types/ 的具体用途无法仅凭目录名可靠判断。 | 20 | 20 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/gun_engagement` | 目录 gun_engagement/ 的具体用途无法仅凭目录名可靠判断。 | 18 | 18 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/gun_engagement/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/gun_engagement/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/gun_engagement/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/gun_engagement/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/gun_engagement/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/gun_engagement/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/gun_engagement/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/gun_engagement/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/gun_engagement/weapons/guns` | 火炮目录，保存炮类武器配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/heatmap` | 目录 heatmap/ 的具体用途无法仅凭目录名可靠判断。 | 35 | 35 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/heatmap/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/heatmap/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/heatmap/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/heatmap/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/heatmap/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 15 | 15 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/heatmap/processors/quantum_agents` | Quantum 智能体目录，保存示例中的智能体行为配置。 | 14 | 14 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/heatmap/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/heatmap/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/heatmap/sensors/esm_rwr` | 电子支援/雷达告警目录，保存 ESM/RWR 传感器配置。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/heatmap/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/heatmap/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/heatmap/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/hel` | 目录 hel/ 的具体用途无法仅凭目录名可靠判断。 | 25 | 25 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/hel/atmosphere` | 目录 atmosphere/ 的具体用途无法仅凭目录名可靠判断。 | 15 | 15 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/hel/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/hel/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/hel/mesh` | 目录 mesh/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/hel/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/hellfire` | 目录 hellfire/ 的具体用途无法仅凭目录名可靠判断。 | 33 | 33 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/hellfire/active_radar_hellfire` | 目录 active_radar_hellfire/ 的具体用途无法仅凭目录名可靠判断。 | 9 | 9 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/hellfire/active_radar_hellfire/dted` | 目录 dted/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/hellfire/laser_designation_via_dis` | 目录 laser_designation_via_dis/ 的具体用途无法仅凭目录名可靠判断。 | 13 | 13 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/hellfire/laser_designation_via_dis/dted` | 目录 dted/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/hellfire/semiactive_laser_hellfire` | 目录 semiactive_laser_hellfire/ 的具体用途无法仅凭目录名可靠判断。 | 10 | 10 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/hellfire/semiactive_laser_hellfire/dted` | 目录 dted/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/iads` | iads 目录，保存综合防空系统相关示例、插件或配置。 | 78 | 78 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/iads/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 18 | 18 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 9 | 9 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 9 | 9 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/iads/sensors/esm_rwr` | 电子支援/雷达告警目录，保存 ESM/RWR 传感器配置。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/iads/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 8 | 8 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 10 | 10 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 9 | 9 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/iads/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/iads/weapons/jammer` | 干扰器目录，保存电子干扰载荷或武器配置。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/iads/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/iads_c2_demos` | Iads C2 Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 53 | 53 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/comm` | 目录 comm/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/iads_c2_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 12 | 12 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 5 | 5 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 5 | 5 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/setup` | 目录 setup/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/utils` | utils 目录，保存通用工具、辅助函数或支撑库。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/iads_c2_demos/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/iads_c2_demos/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/kinematic_mover` | 目录 kinematic_mover/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/kinematic_mover/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/kinematic_mover/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/l16_j11` | 目录 l16_j11/ 的具体用途无法仅凭目录名可靠判断。 | 10 | 10 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/l16_j11/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/l16_j11/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/l16_j11/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/l16_j11/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/laser_designator` | 目录 laser_designator/ 的具体用途无法仅凭目录名可靠判断。 | 20 | 20 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/laser_designator/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/laser_designator/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/laser_designator/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/laser_designator/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/laser_designator/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/laser_designator/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/laser_designator/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/laser_designator/sensors/geosensor` | geosensor 目录，保存传感器相关配置、源码或示例。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/laser_designator/sensors/laser` | 目录 laser/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/laser_designator/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/laser_designator/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/launcher` | 目录 launcher/ 的具体用途无法仅凭目录名可靠判断。 | 19 | 19 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/launcher/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/launcher/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/launcher/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/launcher/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/launcher/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/launcher/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/launcher/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/launcher/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/launcher/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/logistics` | 目录 logistics/ 的具体用途无法仅凭目录名可靠判断。 | 27 | 27 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/logistics/dis` | 目录 dis/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/logistics/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/logistics/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/logistics/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/logistics/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 7 | 7 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/logistics/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/logistics/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 7 | 7 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/logistics/statics_and_globals` | 目录 statics_and_globals/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/multiresolution_demos` | Multiresolution Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 31 | 31 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/comms` | 通信配置目录，保存通信链路、网络或消息配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/multiresolution_demos/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/multiresolution_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/fuel` | 目录 fuel/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/movers` | 目录 movers/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/multiresolution_demos/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 5 | 5 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/new_guidance` | 目录 new_guidance/ 的具体用途无法仅凭目录名可靠判断。 | 26 | 26 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/new_guidance/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/new_guidance/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/new_guidance/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/new_guidance/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/new_guidance/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/new_guidance/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/new_guidance/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/new_guidance/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/new_guidance/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/new_guidance/weapons/ssm` | 地地或舰地导弹目录，保存地面或海上发射武器配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/noise_cloud` | 目录 noise_cloud/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/noise_cloud/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/noise_cloud/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/noise_cloud/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/noise_cloud/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/orwaca_iads` | orwaca_iads 目录，保存综合防空系统相关示例、插件或配置。 | 76 | 76 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/orwaca_iads/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/orwaca_iads/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/orwaca_iads/jpg` | 目录 jpg/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/orwaca_iads/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/orwaca_iads/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 20 | 20 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/orwaca_iads/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/orwaca_iads/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 13 | 13 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/orwaca_iads/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 13 | 13 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/orwaca_iads/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 13 | 13 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/orwaca_iads/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 12 | 12 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/orwaca_iads/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 9 | 9 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/orwaca_iads/weapons/ssm` | 地地或舰地导弹目录，保存地面或海上发射武器配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/oth_radar` | 目录 oth_radar/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/oth_radar/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/oth_radar/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/oth_radar/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/oth_radar/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/oth_radar/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/outer_air_battle` | 目录 outer_air_battle/ 的具体用途无法仅凭目录名可靠判断。 | 39 | 39 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/outer_air_battle/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/outer_air_battle/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/outer_air_battle/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/outer_air_battle/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/outer_air_battle/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 9 | 9 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/outer_air_battle/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/outer_air_battle/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 7 | 7 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/outer_air_battle/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/outer_air_battle/sensors/esm_rwr` | 电子支援/雷达告警目录，保存 ESM/RWR 传感器配置。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/outer_air_battle/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 2 | 2 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/p6dof` | p6dof 目录，保存六自由度飞行动力学或相关示例数据。 | 1,244 | 1,244 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/config` | 目录 config/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/p6dof/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/p6dof/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/p6dof/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/p6dof_types` | p6dof_types 目录，保存六自由度飞行动力学或相关示例数据。 | 1,177 | 1,177 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/p6dof/p6dof_types/aircraft` | 航空器目录，保存具体飞机或飞行器型号数据。 | 643 | 643 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/p6dof/p6dof_types/environment` | 环境数据目录，保存大气、地形或运行环境相关配置。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/p6dof/p6dof_types/misc` | 目录 misc/ 的具体用途无法仅凭目录名可靠判断。 | 76 | 76 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/p6dof/p6dof_types/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 8 | 8 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/p6dof/p6dof_types/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 446 | 446 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 28 | 28 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/p6dof/weapon_effects` | weapon_effects 目录，保存武器相关配置、源码或示例。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/parachute` | 目录 parachute/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/parachute/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/parachute/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/parachute/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/route_finder_demos` | Route Finder Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 17 | 17 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/route_finder_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/route_finder_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/route_finder_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/route_finder_demos/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/route_finder_demos/processors/quantum_agents` | Quantum 智能体目录，保存示例中的智能体行为配置。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/route_finder_demos/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/route_finder_demos/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/satellite_demos` | Satellite Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 156 | 156 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/avionics` | 目录 avionics/ 的具体用途无法仅凭目录名可靠判断。 | 21 | 21 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/satellite_demos/avionics/comm` | 目录 comm/ 的具体用途无法仅凭目录名可靠判断。 | 21 | 21 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 7 | 7 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/satellite_demos/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/satellite_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/ground_networks` | 目录 ground_networks/ 的具体用途无法仅凭目录名可靠判断。 | 11 | 11 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/patterns` | 模式目录，保存路径、行为或任务模式配置。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 35 | 35 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/satellites` | satellites 目录，保存空间、卫星或月地空间相关场景/模型。 | 19 | 19 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/satellite_demos/satellites/orbit_nominal` | 目录 orbit_nominal/ 的具体用途无法仅凭目录名可靠判断。 | 7 | 7 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/satellite_demos/satellites/orbit_tle` | 目录 orbit_tle/ 的具体用途无法仅凭目录名可靠判断。 | 10 | 10 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/satellite_demos/satellites/satcat` | 目录 satcat/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/TLE` | 目录 TLE/ 的具体用途无法仅凭目录名可靠判断。 | 25 | 25 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/tspi` | 目录 tspi/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/satellite_demos/user_handhelds` | 目录 user_handhelds/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/script_demos` | Script Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 14 | 14 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/script_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/script_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/script_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/sensor_demos` | Sensor Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 31 | 31 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/sensor_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/sensor_demos/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/sensor_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/sensor_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/sensor_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/sensor_demos/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/sensor_plot` | sensor_plot 目录，保存传感器相关配置、源码或示例。 | 124 | 124 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/sensor_plot/antenna` | 目录 antenna/ 的具体用途无法仅凭目录名可靠判断。 | 38 | 38 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sensor_plot/clutter` | 目录 clutter/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sensor_plot/comm` | 目录 comm/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sensor_plot/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/sensor_plot/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/sensor_plot/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/sensor_plot/eoir` | 目录 eoir/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sensor_plot/esm` | 目录 esm/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sensor_plot/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 46 | 46 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/sensor_plot/sar` | 目录 sar/ 的具体用途无法仅凭目录名可靠判断。 | 22 | 22 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/ship_ad` | 目录 ship_ad/ 的具体用途无法仅凭目录名可靠判断。 | 42 | 42 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/ship_ad/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ship_ad/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ship_ad/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ship_ad/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 10 | 10 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ship_ad/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ship_ad/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ship_ad/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/ship_ad/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 13 | 13 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ship_ad/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ship_ad/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/ship_ad/weapons/ssm` | 地地或舰地导弹目录，保存地面或海上发射武器配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/shooter` | 目录 shooter/ 的具体用途无法仅凭目录名可靠判断。 | 25 | 25 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/shooter/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/shooter/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/shooter/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/shooter/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/shooter/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/shooter/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/shooter/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/shooter/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/shooter/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/signature_demos` | Signature Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 21 | 21 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/signature_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/signature_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/signature_demos/movers` | 目录 movers/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/signature_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/signature_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/signature_demos/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/signature_demos/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/signature_demos/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 4 | 4 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/simple_scenario` | 目录 simple_scenario/ 的具体用途无法仅凭目录名可靠判断。 | 15 | 15 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/simple_scenario/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/simple_scenario/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/simple_scenario/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/simple_scenario/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/simple_scenario/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/six_dof` | six_dof 目录，保存六自由度飞行动力学或相关示例数据。 | 1,334 | 1,334 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/config` | 目录 config/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/six_dof/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 23 | 23 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 12 | 12 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/six_dof_types` | six_dof_types 目录，保存六自由度飞行动力学或相关示例数据。 | 1,249 | 1,249 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof/six_dof_types/aircraft` | 航空器目录，保存具体飞机或飞行器型号数据。 | 561 | 561 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof/six_dof_types/environment` | 环境数据目录，保存大气、地形或运行环境相关配置。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof/six_dof_types/misc` | 目录 misc/ 的具体用途无法仅凭目录名可靠判断。 | 74 | 74 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/six_dof/six_dof_types/spacecraft` | spacecraft 目录，保存空间、卫星或月地空间相关场景/模型。 | 30 | 30 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof/six_dof_types/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 581 | 581 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof/weapon_effects` | weapon_effects 目录，保存武器相关配置、源码或示例。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/six_dof_with_brawler` | six_dof_with_brawler 目录，保存六自由度飞行动力学或相关示例数据。 | 39 | 39 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/config` | 目录 config/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/platforms/fxw` | 目录 fxw/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/six_dof_types` | six_dof_types 目录，保存六自由度飞行动力学或相关示例数据。 | 23 | 23 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/six_dof_types/aircraft` | 航空器目录，保存具体飞机或飞行器型号数据。 | 20 | 20 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/six_dof_with_brawler/six_dof_types/environment` | 环境数据目录，保存大气、地形或运行环境相关配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/sosm` | 目录 sosm/ 的具体用途无法仅凭目录名可靠判断。 | 116 | 116 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sosm/irimage` | 目录 irimage/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sosm/modtran` | 目录 modtran/ 的具体用途无法仅凭目录名可靠判断。 | 42 | 42 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sosm/sensor_plot` | sensor_plot 目录，保存传感器相关配置、源码或示例。 | 15 | 15 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/sosm/sensor_plot/hmap` | 目录 hmap/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/sosm/sensor_plot/smap` | 目录 smap/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/sosm/sensor_plot/vmap` | 目录 vmap/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sosm/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/sosm/targets` | 目录 targets/ 的具体用途无法仅凭目录名可靠判断。 | 38 | 38 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/sosm/targets/red_multirole_fighter_3` | 目录 red_multirole_fighter_3/ 的具体用途无法仅凭目录名可靠判断。 | 37 | 37 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/sosm/test_mission` | 目录 test_mission/ 的具体用途无法仅凭目录名可靠判断。 | 11 | 11 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/sosm/test_mission/a2a` | 目录 a2a/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/sosm/test_mission/query_atmosphere` | 目录 query_atmosphere/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/sosm/test_mission/query_detect` | 目录 query_detect/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/sosm/test_mission/query_target` | 目录 query_target/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/sosm/test_mission/simple_plot` | 目录 simple_plot/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/demos/space_operations` | space_operations 目录，保存空间、卫星或月地空间相关场景/模型。 | 132 | 132 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/comms` | 通信配置目录，保存通信链路、网络或消息配置。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/space_operations/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/space_operations/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/launch_vehicles` | 目录 launch_vehicles/ 的具体用途无法仅凭目录名可靠判断。 | 40 | 40 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/space_operations/launch_vehicles/atlas_v_401` | 目录 atlas_v_401/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/space_operations/launch_vehicles/delta_iv_m` | 目录 delta_iv_m/ 的具体用途无法仅凭目录名可靠判断。 | 7 | 7 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/space_operations/launch_vehicles/falcon_9` | 目录 falcon_9/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/space_operations/launch_vehicles/falcon_heavy` | 目录 falcon_heavy/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/space_operations/launch_vehicles/launcher_one` | 目录 launcher_one/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/space_operations/launch_vehicles/proton_m` | 目录 proton_m/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/space_operations/launch_vehicles/saturn_v` | 目录 saturn_v/ 的具体用途无法仅凭目录名可靠判断。 | 8 | 8 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/space_operations/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/patterns` | 模式目录，保存路径、行为或任务模式配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 19 | 19 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 5 | 5 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 16 | 16 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 14 | 14 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/space_operations/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/suppressor` | 目录 suppressor/ 的具体用途无法仅凭目录名可靠判断。 | 16 | 16 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/suppressor/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/suppressor/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/suppressor/patterns` | 模式目录，保存路径、行为或任务模式配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/suppressor/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/suppressor/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/suppressor/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/suppressor/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/suppressor/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/suppressor/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/swarm` | 目录 swarm/ 的具体用途无法仅凭目录名可靠判断。 | 17 | 17 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/swarm/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/swarm/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/swarm/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/swarm/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/swarm/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/swarm/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/swarm/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/swarm/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/swarm/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 2 | 2 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/tbm_demos` | Tbm Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 22 | 22 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/tbm_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/tbm_demos/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/tbm_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/tbm_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/tbm_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/tbm_demos/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/tbm_demos/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/tbm_demos/weapons/ssm` | 地地或舰地导弹目录，保存地面或海上发射武器配置。 | 3 | 3 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/terrain_following` | 目录 terrain_following/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/terrain_following/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/terrain_following/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/timeline` | 目录 timeline/ 的具体用途无法仅凭目录名可靠判断。 | 29 | 29 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/timeline/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/timeline/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 16 | 16 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/timeline/processors/quantum_agents` | Quantum 智能体目录，保存示例中的智能体行为配置。 | 16 | 16 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/timeline/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/timeline_lead` | 目录 timeline_lead/ 的具体用途无法仅凭目录名可靠判断。 | 20 | 20 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/timeline_lead/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/timeline_lead/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline_lead/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline_lead/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline_lead/processors` | 处理器配置目录，保存任务处理器、行为逻辑或智能体配置。 | 9 | 9 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/timeline_lead/processors/quantum_agents` | Quantum 智能体目录，保存示例中的智能体行为配置。 | 9 | 9 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline_lead/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/timeline_lead/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/timeline_lead/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/traffic_demos` | Traffic Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 63 | 63 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/traffic_demos/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/traffic_demos/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/traffic_demos/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/traffic_demos/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 24 | 24 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/traffic_demos/roads` | 目录 roads/ 的具体用途无法仅凭目录名可靠判断。 | 10 | 10 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/traffic_demos/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 13 | 13 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/visual_part` | 目录 visual_part/ 的具体用途无法仅凭目录名可靠判断。 | 8 | 8 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/visual_part/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/visual_part/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/visual_part/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/visual_part/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/demos/wargame` | 目录 wargame/ 的具体用途无法仅凭目录名可靠判断。 | 56 | 56 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/wargame/comms` | 通信配置目录，保存通信链路、网络或消息配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/wargame/configs` | 目录 configs/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/wargame/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 5 | 5 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/wargame/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/wargame/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 2 | 2 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/wargame/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/wargame/platforms` | 平台配置目录，保存飞机、舰船、地面站或其他仿真平台定义。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/wargame/scenario` | 目录 scenario/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/wargame/scenario/laydowns` | 目录 laydowns/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/wargame/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 6 | 6 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/wargame/sensors` | 传感器配置目录，保存雷达、红外、电子支援等传感器定义。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/wargame/sensors/radar` | 雷达目录，保存雷达传感器或雷达相关配置。 | 4 | 4 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/wargame/signatures` | 特征数据目录，保存目标特征、红外或雷达截面等签名数据。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/wargame/signatures/air_target` | 目录 air_target/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/demos/wargame/signatures/bomber` | 目录 bomber/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/demos/wargame/weapons` | 武器配置目录，保存导弹、炮、干扰器或其他武器系统定义。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/wargame/weapons/aam` | 空空导弹目录，保存空对空武器配置。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/wargame/weapons/agm` | 空地导弹目录，保存空对地武器配置。 | 2 | 2 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/demos/wargame/weapons/sam` | 地空导弹目录，保存防空导弹配置。 | 1 | 1 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/demos/wargame/zones` | 目录 zones/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |

### 3.2. documentation目录表

| 层级 | 类型 | 路径 | 中文说明 | 可见文件 | 已分类 | 源/头 | 确认状态 |
|------|------|------|----------|----------|--------|-------|----------|
| 2 | 目录 | `afsim-2_9/documentation` | 发布文档目录，保存 HTML 文档、变更记录和用户可读说明。 | 5,044 | 5,044 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/documentation/changelog` | 变更记录目录，保存版本变化和发布说明。 | 1 | 1 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/documentation/html` | HTML 文档目录，保存生成后的网页文档。 | 5,042 | 5,042 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/documentation/html/_images` | 目录 _images/ 的具体用途无法仅凭目录名可靠判断。 | 1,781 | 1,781 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/_images/math` | 目录 math/ 的具体用途无法仅凭目录名可靠判断。 | 764 | 764 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/documentation/html/_sources` | 目录 _sources/ 的具体用途无法仅凭目录名可靠判断。 | 1,603 | 1,603 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/_sources/docs` | 目录 docs/ 的具体用途无法仅凭目录名可靠判断。 | 1,602 | 1,602 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/documentation/html/_static` | 目录 _static/ 的具体用途无法仅凭目录名可靠判断。 | 46 | 46 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/_static/css` | 目录 css/ 的具体用途无法仅凭目录名可靠判断。 | 8 | 8 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/_static/javascript` | 目录 javascript/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/documentation/html/docs` | 目录 docs/ 的具体用途无法仅凭目录名可靠判断。 | 1,602 | 1,602 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/analyst_ocd` | 目录 analyst_ocd/ 的具体用途无法仅凭目录名可靠判断。 | 12 | 12 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 95 | 95 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/developer` | 目录 developer/ 的具体用途无法仅凭目录名可靠判断。 | 16 | 16 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/engage_event` | 目录 engage_event/ 的具体用途无法仅凭目录名可靠判断。 | 24 | 24 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/event` | 目录 event/ 的具体用途无法仅凭目录名可靠判断。 | 80 | 80 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/script` | 目录 script/ 的具体用途无法仅凭目录名可靠判断。 | 330 | 330 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 4 | 4 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/user` | 目录 user/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/user_manual` | 目录 user_manual/ 的具体用途无法仅凭目录名可靠判断。 | 14 | 14 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/documentation/html/docs/wkf_plugin` | 目录 wkf_plugin/ 的具体用途无法仅凭目录名可靠判断。 | 181 | 181 | 0 | <span style="color:red">待人工确认</span> |

### 3.3. resources目录表

| 层级 | 类型 | 路径 | 中文说明 | 可见文件 | 已分类 | 源/头 | 确认状态 |
|------|------|------|----------|----------|--------|-------|----------|
| 2 | 目录 | `afsim-2_9/resources` | 运行资源目录，保存地图、模型、shader、数据和运行时资源。 | 1,288 | 1,288 | 6 | 已说明 |
| 3 | 目录 | `afsim-2_9/resources/data` | 数据资源目录，保存运行时可读取的数据文件。 | 138 | 138 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/resources/data/3rd_party_licenses` | 目录 3rd_party_licenses/ 的具体用途无法仅凭目录名可靠判断。 | 14 | 14 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/data/fonts` | 目录 fonts/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/data/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/resources/data/images/particles` | 目录 particles/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/data/mover_creator` | 目录 mover_creator/ 的具体用途无法仅凭目录名可靠判断。 | 96 | 96 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/resources/data/mover_creator/AFSIM_Scripts` | 目录 AFSIM_Scripts/ 的具体用途无法仅凭目录名可靠判断。 | 0 | 0 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/resources/data/mover_creator/Airfoils` | 目录 Airfoils/ 的具体用途无法仅凭目录名可靠判断。 | 12 | 12 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/resources/data/mover_creator/Atmosphere` | 目录 Atmosphere/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/resources/data/mover_creator/Engines` | 目录 Engines/ 的具体用途无法仅凭目录名可靠判断。 | 45 | 45 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/resources/data/mover_creator/Vehicles` | 目录 Vehicles/ 的具体用途无法仅凭目录名可靠判断。 | 35 | 35 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/data/usmtf` | 目录 usmtf/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/data/wsf_scenario_analyzer` | 目录 wsf_scenario_analyzer/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/resources/data/wsf_scenario_analyzer/check_suites` | 目录 check_suites/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/resources/data/wsf_scenario_analyzer/session_note_suites` | 目录 session_note_suites/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/resources/maps` | 地图资源目录，保存地理底图或地图相关资源。 | 28 | 28 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/resources/maps/bald_earth_db` | 目录 bald_earth_db/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/maps/bluemarble_db` | 目录 bluemarble_db/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/maps/layers` | 目录 layers/ 的具体用途无法仅凭目录名可靠判断。 | 7 | 7 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/maps/naturalearth_db` | 目录 naturalearth_db/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/maps/political_db` | 目录 political_db/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/maps/wdb` | 目录 wdb/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/resources/models` | 模型资源目录，保存三维模型、平台模型或可视化模型资源。 | 1,015 | 1,015 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/resources/models/3d` | 目录 3d/ 的具体用途无法仅凭目录名可靠判断。 | 168 | 168 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/models/cockpits` | 目录 cockpits/ 的具体用途无法仅凭目录名可靠判断。 | 19 | 19 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/resources/models/cockpits/cockpit_v2` | 目录 cockpit_v2/ 的具体用途无法仅凭目录名可靠判断。 | 19 | 19 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/models/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 7 | 7 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/resources/models/mil-std2525d` | 目录 mil-std2525d/ 的具体用途无法仅凭目录名可靠判断。 | 608 | 608 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/resources/models/simple` | 目录 simple/ 的具体用途无法仅凭目录名可靠判断。 | 210 | 210 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/resources/shaders` | shader 资源目录，保存图形渲染用着色器文件。 | 107 | 107 | 6 | 已说明 |

### 3.4. swdev目录表

| 层级 | 类型 | 路径 | 中文说明 | 可见文件 | 已分类 | 源/头 | 确认状态 |
|------|------|------|----------|----------|--------|-------|----------|
| 2 | 目录 | `afsim-2_9/swdev` | 软件开发目录，保存 C++ 源码、构建脚本和开发依赖，是默认架构分析的主要入口。 | 26,854 | 26,836 | 17,184 | 已说明 |
| 3 | 目录 | `afsim-2_9/swdev/dependencies` | 构建依赖目录，保存外部依赖说明或依赖管理材料。 | 450 | 432 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/swdev/dependencies/3rd_party` | 目录 3rd_party/ 的具体用途无法仅凭目录名可靠判断。 | 18 | 0 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/dependencies/resources` | 目录 resources/ 的具体用途无法仅凭目录名可靠判断。 | 432 | 432 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/dependencies/resources/maps` | 目录 maps/ 的具体用途无法仅凭目录名可靠判断。 | 28 | 28 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/dependencies/resources/models` | 目录 models/ 的具体用途无法仅凭目录名可靠判断。 | 404 | 404 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/swdev/src` | 核心开发源码根目录，包含核心框架、插件、应用、工具和可视化组件。 | 26,404 | 26,404 | 17,184 | 已说明 |
| 4 | 目录 | `afsim-2_9/swdev/src/cmake` | CMake 配置目录，保存构建脚本、宏和构建辅助模块。 | 99 | 99 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/cmake/logos` | 目录 logos/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/cmake/Modules` | 目录 Modules/ 的具体用途无法仅凭目录名可靠判断。 | 82 | 82 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/cmake/Presets` | 目录 Presets/ 的具体用途无法仅凭目录名可靠判断。 | 7 | 7 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/cmake/Release` | 目录 Release/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/cmake/Templates` | 目录 Templates/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/core` | 核心框架目录，包含 WSF 基础仿真服务、解析器、工具库、军事、空间、网络等核心库。 | 4,998 | 4,998 | 2,439 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/core/sensor_plot_lib` | sensor_plot_lib 目录，保存传感器相关配置、源码或示例。 | 74 | 74 | 44 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf` | 目录 wsf/ 的具体用途无法仅凭目录名可靠判断。 | 2,313 | 2,313 | 1,125 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_cyber` | wsf_cyber 目录，保存网络战或网络相关场景/模型。 | 202 | 202 | 88 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_grammar_check` | 目录 wsf_grammar_check/ 的具体用途无法仅凭目录名可靠判断。 | 6 | 6 | 2 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_l16` | 目录 wsf_l16/ 的具体用途无法仅凭目录名可靠判断。 | 164 | 164 | 105 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_mil` | 目录 wsf_mil/ 的具体用途无法仅凭目录名可靠判断。 | 1,043 | 1,043 | 432 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_mil_parser` | wsf_mil_parser 目录，保存解析器、语法或输入语言处理相关内容。 | 11 | 11 | 7 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_mtt` | 目录 wsf_mtt/ 的具体用途无法仅凭目录名可靠判断。 | 45 | 45 | 30 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_nx` | 目录 wsf_nx/ 的具体用途无法仅凭目录名可靠判断。 | 166 | 166 | 72 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_parser` | wsf_parser 目录，保存解析器、语法或输入语言处理相关内容。 | 181 | 181 | 158 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_ripr` | 目录 wsf_ripr/ 的具体用途无法仅凭目录名可靠判断。 | 52 | 52 | 24 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_space` | wsf_space 目录，保存空间、卫星或月地空间相关场景/模型。 | 704 | 704 | 329 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_util` | wsf_util 目录，保存通用工具、辅助函数或支撑库。 | 25 | 25 | 21 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/core/wsf_weapon_server` | wsf_weapon_server 目录，保存武器相关配置、源码或示例。 | 11 | 11 | 2 | 已说明 |
| 4 | 目录 | `afsim-2_9/swdev/src/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 90 | 90 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/doc/changelog` | 变更记录目录，保存该示例或模块的历史变化说明。 | 15 | 15 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/doc/developer` | 目录 developer/ 的具体用途无法仅凭目录名可靠判断。 | 14 | 14 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 44 | 44 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/doc/user` | 目录 user/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/doc/user_manual` | 目录 user_manual/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/engage` | Engage 应用目录，保存主仿真应用相关源码和插件入口。 | 120 | 120 | 45 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/engage/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 31 | 31 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/engage/grammar` | 语法目录，保存解析器或场景语言的 grammar 定义文件。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/engage/source` | 源码目录，保存该模块或插件的 C++ 源文件和头文件。 | 48 | 48 | 45 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/engage/tests` | 目录 tests/ 的具体用途无法仅凭目录名可靠判断。 | 35 | 35 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/evt_reader` | 目录 evt_reader/ 的具体用途无法仅凭目录名可靠判断。 | 19 | 19 | 5 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/evt_reader/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 7 | 7 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/evt_reader/source` | 源码目录，保存该模块或插件的 C++ 源文件和头文件。 | 7 | 7 | 5 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/evt_reader/wsftheme` | 目录 wsftheme/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/mission` | Mission 应用目录，保存任务相关可执行入口和版本信息。 | 22 | 22 | 2 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mission/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 9 | 9 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mission/source` | 源码目录，保存该模块或插件的 C++ 源文件和头文件。 | 7 | 7 | 2 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mission/tests` | 目录 tests/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/mover_creator` | Mover Creator 应用目录，保存运动体或平台创建工具相关源码。 | 761 | 761 | 225 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mover_creator/data` | 目录 data/ 的具体用途无法仅凭目录名可靠判断。 | 96 | 96 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/mover_creator/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 218 | 218 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mover_creator/source` | 源码目录，保存该模块或插件的 C++ 源文件和头文件。 | 227 | 227 | 225 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mover_creator/ui` | 目录 ui/ 的具体用途无法仅凭目录名可靠判断。 | 213 | 213 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/mover_creator/wsftheme` | 目录 wsftheme/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/mystic` | Mystic 结果可视化目录，保存仿真结果显示、分析和 UI 插件。 | 926 | 926 | 291 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mystic/exec` | 可执行入口目录，保存程序 main 入口或执行器源码。 | 66 | 66 | 1 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mystic/lib` | 库目录，保存可复用库源码或公共组件。 | 106 | 106 | 52 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mystic/plugins` | 插件目录，保存应用或框架的可加载插件。 | 746 | 746 | 238 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/mystic/python` | 目录 python/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/post_processor` | 后处理应用目录，保存仿真结果后处理工具源码。 | 171 | 171 | 101 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/post_processor/exec` | 可执行入口目录，保存程序 main 入口或执行器源码。 | 13 | 13 | 1 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/post_processor/lib` | 库目录，保存可复用库源码或公共组件。 | 33 | 33 | 20 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/post_processor/WizPostProcessor` | 目录 WizPostProcessor/ 的具体用途无法仅凭目录名可靠判断。 | 119 | 119 | 80 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/sensor_plot` | 传感器绘图应用目录，保存传感器覆盖和探测范围可视化工具。 | 71 | 71 | 3 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/sensor_plot/data` | 目录 data/ 的具体用途无法仅凭目录名可靠判断。 | 38 | 38 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/sensor_plot/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/sensor_plot/grammar` | 语法目录，保存解析器或场景语言的 grammar 定义文件。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/sensor_plot/source` | 源码目录，保存该模块或插件的 C++ 源文件和头文件。 | 6 | 6 | 3 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/sensor_plot/tests` | 目录 tests/ 的具体用途无法仅凭目录名可靠判断。 | 19 | 19 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/tools` | 源码树内开发工具目录，包含与构建、数据处理、可视化或开发辅助相关的 C++ 工具。 | 4,082 | 4,082 | 2,491 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/3rd_party-cmake` | 目录 3rd_party-cmake/ 的具体用途无法仅凭目录名可靠判断。 | 13 | 13 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/artificer` | 目录 artificer/ 的具体用途无法仅凭目录名可靠判断。 | 44 | 44 | 40 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/dis` | 目录 dis/ 的具体用途无法仅凭目录名可靠判断。 | 444 | 444 | 433 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/genio` | 目录 genio/ 的具体用途无法仅凭目录名可靠判断。 | 148 | 148 | 145 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/geodata` | 目录 geodata/ 的具体用途无法仅凭目录名可靠判断。 | 107 | 107 | 98 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/misc` | 目录 misc/ 的具体用途无法仅凭目录名可靠判断。 | 16 | 16 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/packetio` | 目录 packetio/ 的具体用途无法仅凭目录名可靠判断。 | 49 | 49 | 48 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/profiling` | 目录 profiling/ 的具体用途无法仅凭目录名可靠判断。 | 33 | 33 | 18 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/scene_gen` | 目录 scene_gen/ 的具体用途无法仅凭目录名可靠判断。 | 34 | 34 | 21 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/tracking_filters` | 目录 tracking_filters/ 的具体用途无法仅凭目录名可靠判断。 | 13 | 13 | 12 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/util` | util 目录，保存通用工具、辅助函数或支撑库。 | 415 | 415 | 404 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/util_script` | util_script 目录，保存通用工具、辅助函数或支撑库。 | 124 | 124 | 109 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/utilosg` | utilosg 目录，保存通用工具、辅助函数或支撑库。 | 228 | 228 | 222 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/utilqt` | utilqt 目录，保存通用工具、辅助函数或支撑库。 | 117 | 117 | 107 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/vespatk` | 目录 vespatk/ 的具体用途无法仅凭目录名可靠判断。 | 905 | 905 | 159 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/tools/wkf` | 目录 wkf/ 的具体用途无法仅凭目录名可靠判断。 | 1,392 | 1,392 | 675 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/warlock` | Warlock 工具目录，保存场景调试、分析和战术可视化相关源码。 | 1,375 | 1,375 | 616 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/warlock/data` | 目录 data/ 的具体用途无法仅凭目录名可靠判断。 | 55 | 55 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/warlock/plugins` | 插件目录，保存应用或框架的可加载插件。 | 1,113 | 1,113 | 552 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/warlock/warlock_core` | 目录 warlock_core/ 的具体用途无法仅凭目录名可靠判断。 | 126 | 126 | 61 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/warlock/warlock_exec` | 目录 warlock_exec/ 的具体用途无法仅凭目录名可靠判断。 | 77 | 77 | 3 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/weapon_tools` | 武器工具目录，保存武器数据、武器分析或武器辅助工具源码。 | 84 | 84 | 26 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/weapon_tools/data` | 目录 data/ 的具体用途无法仅凭目录名可靠判断。 | 10 | 10 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/weapon_tools/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 18 | 18 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/weapon_tools/grammar` | 语法目录，保存解析器或场景语言的 grammar 定义文件。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/weapon_tools/source` | 源码目录，保存该模块或插件的 C++ 源文件和头文件。 | 29 | 29 | 26 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/weapon_tools/source_plugin` | 目录 source_plugin/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/weapon_tools/tests` | 目录 tests/ 的具体用途无法仅凭目录名可靠判断。 | 21 | 21 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/wizard` | Wizard 场景编辑向导目录，保存图形化场景编辑和导入插件源码。 | 1,914 | 1,914 | 1,059 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wizard/data` | 目录 data/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wizard/lib` | 库目录，保存可复用库源码或公共组件。 | 385 | 385 | 248 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wizard/main` | 目录 main/ 的具体用途无法仅凭目录名可靠判断。 | 88 | 88 | 2 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wizard/plugins` | 插件目录，保存应用或框架的可加载插件。 | 1,087 | 1,087 | 555 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wizard/test` | 测试目录，保存单元测试、集成测试或测试辅助代码。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wizard/tests` | 目录 tests/ 的具体用途无法仅凭目录名可靠判断。 | 11 | 11 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wizard/usmtf` | 目录 usmtf/ 的具体用途无法仅凭目录名可靠判断。 | 335 | 335 | 254 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/swdev/src/wsf_plugins` | WSF 插件目录，包含可选仿真模型、领域扩展和分析插件。 | 11,666 | 11,666 | 9,881 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_air_combat` | 目录 wsf_air_combat/ 的具体用途无法仅凭目录名可靠判断。 | 118 | 118 | 34 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_alternate_locations` | 目录 wsf_alternate_locations/ 的具体用途无法仅凭目录名可靠判断。 | 16 | 16 | 7 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_annotation` | 目录 wsf_annotation/ 的具体用途无法仅凭目录名可靠判断。 | 15 | 15 | 5 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8` | 目录 wsf_argo8/ 的具体用途无法仅凭目录名可靠判断。 | 25 | 25 | 14 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_brawler` | wsf_brawler 目录，保存 Brawler 空战交战模型相关内容。 | 150 | 150 | 27 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_coverage` | 目录 wsf_coverage/ 的具体用途无法仅凭目录名可靠判断。 | 239 | 239 | 118 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_fires` | 目录 wsf_fires/ 的具体用途无法仅凭目录名可靠判断。 | 37 | 37 | 22 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_iads_c2_lib` | wsf_iads_c2_lib 目录，保存综合防空系统相关示例、插件或配置。 | 399 | 399 | 308 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_multiresolution` | 目录 wsf_multiresolution/ 的具体用途无法仅凭目录名可靠判断。 | 111 | 111 | 17 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_oms_uci` | 目录 wsf_oms_uci/ 的具体用途无法仅凭目录名可靠判断。 | 8,785 | 8,785 | 8,642 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof` | wsf_p6dof 目录，保存六自由度飞行动力学或相关示例数据。 | 819 | 819 | 292 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer` | 目录 wsf_scenario_analyzer/ 的具体用途无法仅凭目录名可靠判断。 | 15 | 15 | 8 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer_iads_c2` | wsf_scenario_analyzer_iads_c2 目录，保存综合防空系统相关示例、插件或配置。 | 9 | 9 | 2 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_simdis` | 目录 wsf_simdis/ 的具体用途无法仅凭目录名可靠判断。 | 12 | 12 | 2 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof` | wsf_six_dof 目录，保存六自由度飞行动力学或相关示例数据。 | 849 | 849 | 332 | 已说明 |
| 5 | 目录 | `afsim-2_9/swdev/src/wsf_plugins/wsf_sosm` | 目录 wsf_sosm/ 的具体用途无法仅凭目录名可靠判断。 | 66 | 66 | 51 | <span style="color:red">待人工确认</span> |

### 3.5. tools目录表

| 层级 | 类型 | 路径 | 中文说明 | 可见文件 | 已分类 | 源/头 | 确认状态 |
|------|------|------|----------|----------|--------|-------|----------|
| 2 | 目录 | `afsim-2_9/tools` | 发布包工具目录，保存随包脚本和辅助工具。 | 101 | 101 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/tools/afpy` | 目录 afpy/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/tools/Chugger` | 目录 Chugger/ 的具体用途无法仅凭目录名可靠判断。 | 17 | 17 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/tools/Chugger/chugger` | 目录 chugger/ 的具体用途无法仅凭目录名可靠判断。 | 15 | 15 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/tools/Chugger/chugger/client` | 目录 client/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/tools/Chugger/chugger/parser` | parser 目录，保存解析器、语法或输入语言处理相关内容。 | 6 | 6 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/tools/Chugger/chugger/server` | 目录 server/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/tools/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 26 | 26 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/tools/doc/images` | 图片资源目录，通常为文档或说明页面提供配图。 | 20 | 20 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/tools/doc/scripts` | 脚本目录，保存场景运行、数据生成或自动化辅助脚本。 | 4 | 4 | 0 | 已说明 |
| 3 | 目录 | `afsim-2_9/tools/pyrunplotter` | 目录 pyrunplotter/ 的具体用途无法仅凭目录名可靠判断。 | 20 | 20 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/tools/pyrunplotter/demos` | Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 7 | 7 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/tools/pyrunplotter/demos/multiresolution_demos` | Multiresolution Demos 示例目录，保存与该主题相关的演示场景、配置和说明。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/tools/pyrunplotter/demos/outer_air_battle` | 目录 outer_air_battle/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/tools/pyrunplotter/demos/six_dof` | six_dof 目录，保存六自由度飞行动力学或相关示例数据。 | 3 | 3 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/tools/pyrunplotter/output` | 输出目录，通常保存示例运行结果、日志或生成文件。 | 0 | 0 | 0 | 已说明 |

### 3.6. training目录表

| 层级 | 类型 | 路径 | 中文说明 | 可见文件 | 已分类 | 源/头 | 确认状态 |
|------|------|------|----------|----------|--------|-------|----------|
| 2 | 目录 | `afsim-2_9/training` | 培训材料目录，保存面向开发者和用户的实验、教程和示例代码；默认不进入架构依赖分析。 | 1,423 | 1,423 | 152 | 已说明 |
| 3 | 目录 | `afsim-2_9/training/developer` | 开发者培训目录，保存面向开发者的实验、核心库练习和示例工程。 | 436 | 436 | 152 | 已说明 |
| 4 | 目录 | `afsim-2_9/training/developer/core` | 目录 core/ 的具体用途无法仅凭目录名可靠判断。 | 374 | 374 | 110 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/developer/core/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/developer/core/labs` | 目录 labs/ 的具体用途无法仅凭目录名可靠判断。 | 360 | 360 | 110 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/developer/core/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 13 | 13 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/developer/wkf` | 目录 wkf/ 的具体用途无法仅凭目录名可靠判断。 | 62 | 62 | 42 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/developer/wkf/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/developer/wkf/labs` | 目录 labs/ 的具体用途无法仅凭目录名可靠判断。 | 58 | 58 | 42 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/developer/wkf/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 3 | 目录 | `afsim-2_9/training/user` | 用户培训目录，保存面向使用者的场景教程、示例输入和课程材料。 | 987 | 987 | 0 | 已说明 |
| 4 | 目录 | `afsim-2_9/training/user/1_AFSIM_Intro` | 目录 1_AFSIM_Intro/ 的具体用途无法仅凭目录名可靠判断。 | 5 | 5 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/user/1_AFSIM_Intro/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 3 | 3 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/1_AFSIM_Intro/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/10_Other_Topics` | 目录 10_Other_Topics/ 的具体用途无法仅凭目录名可靠判断。 | 570 | 570 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/user/10_Other_Topics/bam` | 目录 bam/ 的具体用途无法仅凭目录名可靠判断。 | 570 | 570 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/2_Platforms_and_Movers` | 目录 2_Platforms_and_Movers/ 的具体用途无法仅凭目录名可靠判断。 | 24 | 24 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/user/2_Platforms_and_Movers/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 22 | 22 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/2_Platforms_and_Movers/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/3_Weapons` | 3_Weapons 目录，保存武器相关配置、源码或示例。 | 22 | 22 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/3_Weapons/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 21 | 21 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/3_Weapons/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/4_Sensors` | 4_Sensors 目录，保存传感器相关配置、源码或示例。 | 48 | 48 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/4_Sensors/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 45 | 45 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/4_Sensors/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/5_Scripting` | 目录 5_Scripting/ 的具体用途无法仅凭目录名可靠判断。 | 59 | 59 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/user/5_Scripting/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 57 | 57 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/5_Scripting/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/6_Task_Processors_and_Comms` | 目录 6_Task_Processors_and_Comms/ 的具体用途无法仅凭目录名可靠判断。 | 79 | 79 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/user/6_Task_Processors_and_Comms/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 77 | 77 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/6_Task_Processors_and_Comms/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 2 | 2 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/7_Warlock_Features` | 目录 7_Warlock_Features/ 的具体用途无法仅凭目录名可靠判断。 | 44 | 44 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/user/7_Warlock_Features/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/7_Warlock_Features/resources` | 目录 resources/ 的具体用途无法仅凭目录名可靠判断。 | 1 | 1 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/user/7_Warlock_Features/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 39 | 39 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/7_Warlock_Features/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/8_Mystic_Features` | 目录 8_Mystic_Features/ 的具体用途无法仅凭目录名可靠判断。 | 43 | 43 | 0 | <span style="color:red">待人工确认</span> |
| 5 | 目录 | `afsim-2_9/training/user/8_Mystic_Features/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/8_Mystic_Features/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 39 | 39 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/8_Mystic_Features/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 3 | 3 | 0 | <span style="color:red">待人工确认</span> |
| 4 | 目录 | `afsim-2_9/training/user/9_Space` | 9_Space 目录，保存空间、卫星或月地空间相关场景/模型。 | 93 | 93 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/9_Space/doc` | 文档子目录，通常保存该场景或模块的说明、变更记录和图片。 | 1 | 1 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/9_Space/scenarios` | 场景配置目录，保存可运行的仿真场景输入文件。 | 88 | 88 | 0 | 已说明 |
| 5 | 目录 | `afsim-2_9/training/user/9_Space/slides` | 目录 slides/ 的具体用途无法仅凭目录名可靠判断。 | 4 | 4 | 0 | <span style="color:red">待人工确认</span> |

## 4. 顶级文件说明

| 文件 | 中文说明 | 可见文件 | 已分类 | 源/头 | 确认状态 |
|------|----------|----------|--------|-------|----------|
| `afsim-2_9/ARCHITECTURE.md` | AFSIM 随包架构说明文件，用于理解发布包中的总体结构。 | 1 | 1 | 0 | 已说明 |

## 5. 统计摘要

| 项 | 值 |
|----|----|
| 可见文件数（排除隐藏目录、隐藏文件、指定元数据文件） | 39,894 |
| Phase 1 已分类文件数（排除指定元数据文件后的目录表口径） | 39,876 |
| Phase 1 原始分类条目数 | 43,586 |
| Phase 1 source/header 文件数 | 17,342 |
| 本文档展示的二级目录表数量 | 6 |
| 已排除的隐藏目录数（文件系统中存在） | 4 |
| 已排除的指定元数据文件数（文件系统中存在） | 3,712 |
| 已排除的指定元数据文件数（Phase 1 分类中存在） | 3,710 |

## 6. 人工确认项

<span style="color:red">待人工确认：本文档已按人工要求排除指定元数据文件；这些元数据文件是否需要在边界补充分析文档中单独解释，等待人工确认。</span>
