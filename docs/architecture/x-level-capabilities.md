# AFSIM 仿真框架架构文档

> **状态**：已完成
> **日期**：2026-07-16
> **分析范围**：仿真模型相关功能，排除 training、demo、test、doc 工具性条目
> **分析深度**：System-level、Module-level、Class-level 完整索引支撑，Method-level 正文列代表性样例
> **关联文档**：`workspace/source-index/function-index.jsonl`、`docs/architecture/business-logic-readiness.md`

## 0. 文档说明

**总体概述**：本文按四层能力体系组织 AFSIM 功能。标题按 Phase7 验证规则固定为架构文档标题，正文内容为功能层次说明。

**功能划分**：功能按四层体系组织：

| 层级 | 英文 | 定义 | 边界范围 | 对应索引 |
|------|------|------|----------|----------|
| **系统级** | System-level | 跨框架、跨域、跨插件层组合多个模块完成的端到端能力 | 跨目录、跨子系统 | function-index level=System-level |
| **模块级** | Module-level | 单一子系统或模块内的能力集合 | 同一目录或相邻目录 | function-index level=Module-level |
| **类级** | Class-level | 单个 class（类）封装的职责集合 | 单个头文件和实现文件 | function-index level=Class-level |
| **方法级** | Method-level | 单个函数或方法的具体实现 | 单个文件内的函数 | function-index level=Method-level |

## 1. 系统级功能总览

**功能总览**：本次索引包含 System-level 1 条、Module-level 54 条、Class-level 5415 条、Method-level 49561 条。主要能力域为仿真生命周期、场景配置、对象创建、事件处理、通信消息、传感器与平台状态、输出与扩展注册。完整方法清单见 `workspace/source-index/function-index.jsonl`。

| # | 系统级功能 | 核心职责 |
|---|-----------|----------|
| 1 | AFSIM 函数级能力总览 | 汇总模块、类和方法级能力，为架构和业务逻辑分析提供入口 |

## 2. AFSIM 系统功能（总体仿真框架）

1. **AFSIM 系统功能概述**：系统级能力覆盖核心仿真、工具链、运行查看、结果分析和扩展接入。
2. **功能对应条目**：见 function-index.jsonl 中 `level=System-level` 的条目 `qualified_name=AFSIM::System::FunctionInventory`。
3. **模块级功能细览**：正文列仿真模型相关代表模块；完整 Module-level 清单见 `workspace/source-index/function-index.jsonl`。

| 系统级功能 | 模块级功能 | 核心职责 |
|-----------|-----------|----------|
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::core::wsf` | 汇总 core/wsf 模块的类级功能，覆盖 9427 个 Method-level 函数；主要生命周期角色：configuration、utility、simulation_loop、object… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::wizard` | 汇总 wizard 模块的类级功能，覆盖 8334 个 Method-level 函数；主要生命周期角色：configuration、utility、object_create、scenario_l… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::core::wsf_mil` | 汇总 core/wsf_mil 模块的类级功能，覆盖 5764 个 Method-level 函数；主要生命周期角色：configuration、object_create、utility、simu… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::mover_creator` | 汇总 mover_creator 模块的类级功能，覆盖 5609 个 Method-level 函数；主要生命周期角色：configuration、utility、object_create、shu… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::warlock` | 汇总 warlock 模块的类级功能，覆盖 3533 个 Method-level 函数；主要生命周期角色：configuration、simulation_loop、model_update、ut… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::mystic` | 汇总 mystic 模块的类级功能，覆盖 2324 个 Method-level 函数；主要生命周期角色：configuration、simulation_loop、utility、shutdown… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::wsf_plugins::wsf_iads_c2_lib` | 汇总 wsf_plugins/wsf_iads_c2_lib 模块的类级功能，覆盖 1041 个 Method-level 函数；主要生命周期角色：configuration、utility、sim… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::core::wsf_space` | 汇总 core/wsf_space 模块的类级功能，覆盖 899 个 Method-level 函数；主要生命周期角色：configuration、utility、simulation_loop、o… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::wsf_plugins::wsf_p6dof` | 汇总 wsf_plugins/wsf_p6dof 模块的类级功能，覆盖 610 个 Method-level 函数；主要生命周期角色：configuration、utility、simulation… |
| `AFSIM::System::FunctionInventory` | `AFSIM::Module::tools::vespatk` | 汇总 tools/vespatk 模块的类级功能，覆盖 604 个 Method-level 函数；主要生命周期角色：configuration、utility、object_create、simu… |

### 2.1 core/wsf 模块级功能（core/wsf 能力集合）

1. **core/wsf 模块功能概述**：汇总 core/wsf 模块的类级功能，覆盖 9427 个 Method-level 函数；主要生命周期角色：configuration、utility、simulation_loop、object_create；主要算法类型：none、io、control_flow、math。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=AFSIM::Module::core::wsf`。
3. **类级功能细览**：正文列该模块方法数较高的类级功能；完整 Class-level 清单见 `workspace/source-index/function-index.jsonl`。

| 模块级功能 | 类级功能 | 核心职责 |
|-----------|---------|----------|
| `AFSIM::Module::core::wsf` | `AFSIM::Module::core::wsf::Class::wsf::comm::WsfSimulation` | 汇总 core/wsf 模块中 wsf::comm::WsfSimulation 的函数职责，覆盖 146 个 Method-level 函数；主要生命周期角色：configuration、simu… |
| `AFSIM::Module::core::wsf` | `AFSIM::Module::core::wsf::Class::wsf::comm::WsfDisInterface` | 汇总 core/wsf 模块中 wsf::comm::WsfDisInterface 的函数职责，覆盖 131 个 Method-level 函数；主要生命周期角色：configuration、si… |
| `AFSIM::Module::core::wsf` | `AFSIM::Module::core::wsf::Class::ut::script::wsf::WsfPlatform` | 汇总 core/wsf 模块中 ut::script::wsf::WsfPlatform 的函数职责，覆盖 124 个 Method-level 函数；主要生命周期角色：configuration、… |
| `AFSIM::Module::core::wsf` | `AFSIM::Module::core::wsf::Class::wsf::comm::router::medium::WsfScenario` | 汇总 core/wsf 模块中 wsf::comm::router::medium::WsfScenario 的函数职责，覆盖 114 个 Method-level 函数；主要生命周期角色：conf… |
| `AFSIM::Module::core::wsf` | `AFSIM::Module::core::wsf::Class::WsfTrackManager` | 汇总 core/wsf 模块中 WsfTrackManager 的函数职责，覆盖 88 个 Method-level 函数；主要生命周期角色：configuration、simulation_loo… |
| `AFSIM::Module::core::wsf` | `AFSIM::Module::core::wsf::Class::wsf::comm::eventpipe::WsfEventPipeInterface` | 汇总 core/wsf 模块中 wsf::comm::eventpipe::WsfEventPipeInterface 的函数职责，覆盖 84 个 Method-level 函数；主要生命周期角色：… |

#### 2.1.1 AFSIM::Module::core::wsf::Class::wsf::comm::WsfSimulation 类级功能（类职责集合）

1. **AFSIM::Module::core::wsf::Class::wsf::comm::WsfSimulation 类功能概述**：汇总 core/wsf 模块中 wsf::comm::WsfSimulation 的函数职责，覆盖 146 个 Method-level 函数；主要生命周期角色：configuration、simulation_loop、utility、event_handling；主要算法类型：none、configuration…
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::core::wsf::Class::wsf::comm::WsfSimulation`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::core::wsf::Class::wsf::comm::WsfSimulation` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::core::wsf::Class::wsf::comm::WsfSimulation` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::core::wsf::Class::wsf::comm::WsfSimulation` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

#### 2.1.2 AFSIM::Module::core::wsf::Class::wsf::comm::WsfDisInterface 类级功能（类职责集合）

1. **AFSIM::Module::core::wsf::Class::wsf::comm::WsfDisInterface 类功能概述**：汇总 core/wsf 模块中 wsf::comm::WsfDisInterface 的函数职责，覆盖 131 个 Method-level 函数；主要生命周期角色：configuration、simulation_loop、utility、object_create；主要算法类型：math、control_flow…
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::core::wsf::Class::wsf::comm::WsfDisInterface`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::core::wsf::Class::wsf::comm::WsfDisInterface` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::core::wsf::Class::wsf::comm::WsfDisInterface` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::core::wsf::Class::wsf::comm::WsfDisInterface` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

### 2.2 wizard 模块级功能（wizard 能力集合）

1. **wizard 模块功能概述**：汇总 wizard 模块的类级功能，覆盖 8334 个 Method-level 函数；主要生命周期角色：configuration、utility、object_create、scenario_load；主要算法类型：none、io、configuration、control_flow。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=AFSIM::Module::wizard`。
3. **类级功能细览**：正文列该模块方法数较高的类级功能；完整 Class-level 清单见 `workspace/source-index/function-index.jsonl`。

| 模块级功能 | 类级功能 | 核心职责 |
|-----------|---------|----------|
| `AFSIM::Module::wizard` | `AFSIM::Module::wizard::Class::Project` | 汇总 wizard 模块中 Project 的函数职责，覆盖 107 个 Method-level 函数；主要生命周期角色：configuration、scenario_load、simulatio… |
| `AFSIM::Module::wizard` | `AFSIM::Module::wizard::Class::wizard::Project` | 汇总 wizard 模块中 wizard::Project 的函数职责，覆盖 107 个 Method-level 函数；主要生命周期角色：configuration、scenario_load、s… |
| `AFSIM::Module::wizard` | `AFSIM::Module::wizard::Class::Editor` | 汇总 wizard 模块中 Editor 的函数职责，覆盖 93 个 Method-level 函数；主要生命周期角色：configuration、utility、model_update、even… |
| `AFSIM::Module::wizard` | `AFSIM::Module::wizard::Class::UsCtx` | 汇总 wizard 模块中 UsCtx 的函数职责，覆盖 86 个 Method-level 函数；主要生命周期角色：utility、configuration、object_create、even… |
| `AFSIM::Module::wizard` | `AFSIM::Module::wizard::Class::WsfEditor` | 汇总 wizard 模块中 WsfEditor 的函数职责，覆盖 70 个 Method-level 函数；主要生命周期角色：configuration、model_update、scenario_… |
| `AFSIM::Module::wizard` | `AFSIM::Module::wizard::Class::wizard::WsfEditor` | 汇总 wizard 模块中 wizard::WsfEditor 的函数职责，覆盖 69 个 Method-level 函数；主要生命周期角色：configuration、model_update、s… |

#### 2.2.1 AFSIM::Module::wizard::Class::Project 类级功能（类职责集合）

1. **AFSIM::Module::wizard::Class::Project 类功能概述**：汇总 wizard 模块中 Project 的函数职责，覆盖 107 个 Method-level 函数；主要生命周期角色：configuration、scenario_load、simulation_loop、utility；主要算法类型：io、configuration、none、math。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::wizard::Class::Project`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::wizard::Class::Project` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::wizard::Class::Project` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::wizard::Class::Project` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

#### 2.2.2 AFSIM::Module::wizard::Class::wizard::Project 类级功能（类职责集合）

1. **AFSIM::Module::wizard::Class::wizard::Project 类功能概述**：汇总 wizard 模块中 wizard::Project 的函数职责，覆盖 107 个 Method-level 函数；主要生命周期角色：configuration、scenario_load、simulation_loop、utility；主要算法类型：io、configuration、none、math。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::wizard::Class::wizard::Project`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::wizard::Class::wizard::Project` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::wizard::Class::wizard::Project` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::wizard::Class::wizard::Project` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

### 2.3 core/wsf_mil 模块级功能（core/wsf_mil 能力集合）

1. **core/wsf_mil 模块功能概述**：汇总 core/wsf_mil 模块的类级功能，覆盖 5764 个 Method-level 函数；主要生命周期角色：configuration、object_create、utility、simulation_loop；主要算法类型：none、control_flow、math、io。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=AFSIM::Module::core::wsf_mil`。
3. **类级功能细览**：正文列该模块方法数较高的类级功能；完整 Class-level 清单见 `workspace/source-index/function-index.jsonl`。

| 模块级功能 | 类级功能 | 核心职责 |
|-----------|---------|----------|
| `AFSIM::Module::core::wsf_mil` | `AFSIM::Module::core::wsf_mil::Class::WsfGuidanceComputer` | 汇总 core/wsf_mil 模块中 WsfGuidanceComputer 的函数职责，覆盖 104 个 Method-level 函数；主要生命周期角色：object_create、simul… |
| `AFSIM::Module::core::wsf_mil` | `AFSIM::Module::core::wsf_mil::Class::wsf::WsfGuidanceComputer` | 汇总 core/wsf_mil 模块中 wsf::WsfGuidanceComputer 的函数职责，覆盖 102 个 Method-level 函数；主要生命周期角色：object_create、… |
| `AFSIM::Module::core::wsf_mil` | `AFSIM::Module::core::wsf_mil::Class::WsfGuidedMover` | 汇总 core/wsf_mil 模块中 WsfGuidedMover 的函数职责，覆盖 80 个 Method-level 函数；主要生命周期角色：configuration、simulation_… |
| `AFSIM::Module::core::wsf_mil` | `AFSIM::Module::core::wsf_mil::Class::WsfFalseTargetScreener` | 汇总 core/wsf_mil 模块中 WsfFalseTargetScreener 的函数职责，覆盖 79 个 Method-level 函数；主要生命周期角色：configuration、sim… |
| `AFSIM::Module::core::wsf_mil` | `AFSIM::Module::core::wsf_mil::Class::WsfLaunchComputer` | 汇总 core/wsf_mil 模块中 WsfLaunchComputer 的函数职责，覆盖 78 个 Method-level 函数；主要生命周期角色：configuration、simulati… |
| `AFSIM::Module::core::wsf_mil` | `AFSIM::Module::core::wsf_mil::Class::WsfRF_Jammer` | 汇总 core/wsf_mil 模块中 WsfRF_Jammer 的函数职责，覆盖 72 个 Method-level 函数；主要生命周期角色：configuration、object_create… |

#### 2.3.1 AFSIM::Module::core::wsf_mil::Class::WsfGuidanceComputer 类级功能（类职责集合）

1. **AFSIM::Module::core::wsf_mil::Class::WsfGuidanceComputer 类功能概述**：汇总 core/wsf_mil 模块中 WsfGuidanceComputer 的函数职责，覆盖 104 个 Method-level 函数；主要生命周期角色：object_create、simulation_loop、utility、configuration；主要算法类型：none、state_update、io…
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::core::wsf_mil::Class::WsfGuidanceComputer`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::core::wsf_mil::Class::WsfGuidanceComputer` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::core::wsf_mil::Class::WsfGuidanceComputer` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::core::wsf_mil::Class::WsfGuidanceComputer` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

#### 2.3.2 AFSIM::Module::core::wsf_mil::Class::wsf::WsfGuidanceComputer 类级功能（类职责集合）

1. **AFSIM::Module::core::wsf_mil::Class::wsf::WsfGuidanceComputer 类功能概述**：汇总 core/wsf_mil 模块中 wsf::WsfGuidanceComputer 的函数职责，覆盖 102 个 Method-level 函数；主要生命周期角色：object_create、simulation_loop、configuration、utility；主要算法类型：none、state_upda…
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::core::wsf_mil::Class::wsf::WsfGuidanceComputer`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::core::wsf_mil::Class::wsf::WsfGuidanceComputer` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::core::wsf_mil::Class::wsf::WsfGuidanceComputer` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::core::wsf_mil::Class::wsf::WsfGuidanceComputer` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

### 2.4 mover_creator 模块级功能（mover_creator 能力集合）

1. **mover_creator 模块功能概述**：汇总 mover_creator 模块的类级功能，覆盖 5609 个 Method-level 函数；主要生命周期角色：configuration、utility、object_create、shutdown；主要算法类型：none、math、io、factory。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=AFSIM::Module::mover_creator`。
3. **类级功能细览**：正文列该模块方法数较高的类级功能；完整 Class-level 清单见 `workspace/source-index/function-index.jsonl`。

| 模块级功能 | 类级功能 | 核心职责 |
|-----------|---------|----------|
| `AFSIM::Module::mover_creator` | `AFSIM::Module::mover_creator::Class::VehicleAeroCore` | 汇总 mover_creator 模块中 VehicleAeroCore 的函数职责，覆盖 222 个 Method-level 函数；主要生命周期角色：utility、configuration、… |
| `AFSIM::Module::mover_creator` | `AFSIM::Module::mover_creator::Class::VehicleAero` | 汇总 mover_creator 模块中 VehicleAero 的函数职责，覆盖 216 个 Method-level 函数；主要生命周期角色：configuration、shutdown、obj… |
| `AFSIM::Module::mover_creator` | `AFSIM::Module::mover_creator::Class::GeometryGLWidget` | 汇总 mover_creator 模块中 GeometryGLWidget 的函数职责，覆盖 187 个 Method-level 函数；主要生命周期角色：configuration、utility… |
| `AFSIM::Module::mover_creator` | `AFSIM::Module::mover_creator::Class::Designer::GeometryGLWidget` | 汇总 mover_creator 模块中 Designer::GeometryGLWidget 的函数职责，覆盖 149 个 Method-level 函数；主要生命周期角色：configurati… |
| `AFSIM::Module::mover_creator` | `AFSIM::Module::mover_creator::Class::Designer::GeometryWing` | 汇总 mover_creator 模块中 Designer::GeometryWing 的函数职责，覆盖 133 个 Method-level 函数；主要生命周期角色：configuration、u… |
| `AFSIM::Module::mover_creator` | `AFSIM::Module::mover_creator::Class::GeometryWing` | 汇总 mover_creator 模块中 GeometryWing 的函数职责，覆盖 133 个 Method-level 函数；主要生命周期角色：configuration、utility、shu… |

#### 2.4.1 AFSIM::Module::mover_creator::Class::VehicleAeroCore 类级功能（类职责集合）

1. **AFSIM::Module::mover_creator::Class::VehicleAeroCore 类功能概述**：汇总 mover_creator 模块中 VehicleAeroCore 的函数职责，覆盖 222 个 Method-level 函数；主要生命周期角色：utility、configuration、shutdown；主要算法类型：none、math。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::mover_creator::Class::VehicleAeroCore`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::mover_creator::Class::VehicleAeroCore` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::mover_creator::Class::VehicleAeroCore` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::mover_creator::Class::VehicleAeroCore` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

#### 2.4.2 AFSIM::Module::mover_creator::Class::VehicleAero 类级功能（类职责集合）

1. **AFSIM::Module::mover_creator::Class::VehicleAero 类功能概述**：汇总 mover_creator 模块中 VehicleAero 的函数职责，覆盖 216 个 Method-level 函数；主要生命周期角色：configuration、shutdown、object_create、output；主要算法类型：none、io、math、factory。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::mover_creator::Class::VehicleAero`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::mover_creator::Class::VehicleAero` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::mover_creator::Class::VehicleAero` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::mover_creator::Class::VehicleAero` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

### 2.5 warlock 模块级功能（warlock 能力集合）

1. **warlock 模块功能概述**：汇总 warlock 模块的类级功能，覆盖 3533 个 Method-level 函数；主要生命周期角色：configuration、simulation_loop、model_update、utility；主要算法类型：none、io、control_flow、state_update。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=AFSIM::Module::warlock`。
3. **类级功能细览**：正文列该模块方法数较高的类级功能；完整 Class-level 清单见 `workspace/source-index/function-index.jsonl`。

| 模块级功能 | 类级功能 | 核心职责 |
|-----------|---------|----------|
| `AFSIM::Module::warlock` | `AFSIM::Module::warlock::Class::WkPlatformHistory::Plugin` | 汇总 warlock 模块中 WkPlatformHistory::Plugin 的函数职责，覆盖 83 个 Method-level 函数；主要生命周期角色：configuration、simul… |
| `AFSIM::Module::warlock` | `AFSIM::Module::warlock::Class::wkf::vespa::WkPlatformHistory::Plugin` | 汇总 warlock 模块中 wkf::vespa::WkPlatformHistory::Plugin 的函数职责，覆盖 81 个 Method-level 函数；主要生命周期角色：configu… |
| `AFSIM::Module::warlock` | `AFSIM::Module::warlock::Class::six_dof::WkSixDOF_Tuner::SimInterface` | 汇总 warlock 模块中 six_dof::WkSixDOF_Tuner::SimInterface 的函数职责，覆盖 80 个 Method-level 函数；主要生命周期角色：configu… |
| `AFSIM::Module::warlock` | `AFSIM::Module::warlock::Class::wkf::sdl::WkP6DOF_Controller::PluginObject` | 汇总 warlock 模块中 wkf::sdl::WkP6DOF_Controller::PluginObject 的函数职责，覆盖 74 个 Method-level 函数；主要生命周期角色：ut… |
| `AFSIM::Module::warlock` | `AFSIM::Module::warlock::Class::WkTuner::SimInterface` | 汇总 warlock 模块中 WkTuner::SimInterface 的函数职责，覆盖 73 个 Method-level 函数；主要生命周期角色：configuration、event_han… |
| `AFSIM::Module::warlock` | `AFSIM::Module::warlock::Class::wsf::six_dof::WkSixDOF_Tuner::SimInterface` | 汇总 warlock 模块中 wsf::six_dof::WkSixDOF_Tuner::SimInterface 的函数职责，覆盖 73 个 Method-level 函数；主要生命周期角色：co… |

#### 2.5.1 AFSIM::Module::warlock::Class::WkPlatformHistory::Plugin 类级功能（类职责集合）

1. **AFSIM::Module::warlock::Class::WkPlatformHistory::Plugin 类功能概述**：汇总 warlock 模块中 WkPlatformHistory::Plugin 的函数职责，覆盖 83 个 Method-level 函数；主要生命周期角色：configuration、simulation_loop、object_create、scenario_load；主要算法类型：none、control_f…
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::warlock::Class::WkPlatformHistory::Plugin`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::warlock::Class::WkPlatformHistory::Plugin` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::warlock::Class::WkPlatformHistory::Plugin` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::warlock::Class::WkPlatformHistory::Plugin` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

#### 2.5.2 AFSIM::Module::warlock::Class::wkf::vespa::WkPlatformHistory::Plugin 类级功能（类职责集合）

1. **AFSIM::Module::warlock::Class::wkf::vespa::WkPlatformHistory::Plugin 类功能概述**：汇总 warlock 模块中 wkf::vespa::WkPlatformHistory::Plugin 的函数职责，覆盖 81 个 Method-level 函数；主要生命周期角色：configuration、simulation_loop、object_create、scenario_load；主要算法类型：no…
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::warlock::Class::wkf::vespa::WkPlatformHistory::Plugin`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::warlock::Class::wkf::vespa::WkPlatformHistory::Plugin` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::warlock::Class::wkf::vespa::WkPlatformHistory::Plugin` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::warlock::Class::wkf::vespa::WkPlatformHistory::Plugin` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

### 2.6 mystic 模块级功能（mystic 能力集合）

1. **mystic 模块功能概述**：汇总 mystic 模块的类级功能，覆盖 2324 个 Method-level 函数；主要生命周期角色：configuration、simulation_loop、utility、shutdown；主要算法类型：none、io、control_flow、state_update。
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=AFSIM::Module::mystic`。
3. **类级功能细览**：正文列该模块方法数较高的类级功能；完整 Class-level 清单见 `workspace/source-index/function-index.jsonl`。

| 模块级功能 | 类级功能 | 核心职责 |
|-----------|---------|----------|
| `AFSIM::Module::mystic` | `AFSIM::Module::mystic::Class::RvStatistics::EventTableModel` | 汇总 mystic 模块中 RvStatistics::EventTableModel 的函数职责，覆盖 59 个 Method-level 函数；主要生命周期角色：utility、simulati… |
| `AFSIM::Module::mystic` | `AFSIM::Module::mystic::Class::RvBAT::GraphicsNode` | 汇总 mystic 模块中 RvBAT::GraphicsNode 的函数职责，覆盖 58 个 Method-level 函数；主要生命周期角色：configuration、utility、mode… |
| `AFSIM::Module::mystic` | `AFSIM::Module::mystic::Class::rv::RvStatistics::EventTableModel` | 汇总 mystic 模块中 rv::RvStatistics::EventTableModel 的函数职责，覆盖 58 个 Method-level 函数；主要生命周期角色：utility、simu… |
| `AFSIM::Module::mystic` | `AFSIM::Module::mystic::Class::RvPlatformHistory::Plugin` | 汇总 mystic 模块中 RvPlatformHistory::Plugin 的函数职责，覆盖 43 个 Method-level 函数；主要生命周期角色：simulation_loop、conf… |
| `AFSIM::Module::mystic` | `AFSIM::Module::mystic::Class::phase2-batch11` | 汇总 mystic 模块中 phase2-batch11 的函数职责，覆盖 40 个 Method-level 函数；主要生命周期角色：configuration、object_create、sim… |
| `AFSIM::Module::mystic` | `AFSIM::Module::mystic::Class::phase2_batch07` | 汇总 mystic 模块中 phase2_batch07 的函数职责，覆盖 37 个 Method-level 函数；主要生命周期角色：simulation_loop、configuration、s… |

#### 2.6.1 AFSIM::Module::mystic::Class::RvStatistics::EventTableModel 类级功能（类职责集合）

1. **AFSIM::Module::mystic::Class::RvStatistics::EventTableModel 类功能概述**：汇总 mystic 模块中 RvStatistics::EventTableModel 的函数职责，覆盖 59 个 Method-level 函数；主要生命周期角色：utility、simulation_loop、event_handling、configuration；主要算法类型：control_flow、fac…
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::mystic::Class::RvStatistics::EventTableModel`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::mystic::Class::RvStatistics::EventTableModel` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::mystic::Class::RvStatistics::EventTableModel` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::mystic::Class::RvStatistics::EventTableModel` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

#### 2.6.2 AFSIM::Module::mystic::Class::RvBAT::GraphicsNode 类级功能（类职责集合）

1. **AFSIM::Module::mystic::Class::RvBAT::GraphicsNode 类功能概述**：汇总 mystic 模块中 RvBAT::GraphicsNode 的函数职责，覆盖 58 个 Method-level 函数；主要生命周期角色：configuration、utility、model_update、scenario_load；主要算法类型：none、configuration、io、state_up…
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=AFSIM::Module::mystic::Class::RvBAT::GraphicsNode`。
3. **方法级功能摘要**：正文列代表性 Method-level 条目；完整方法级清单见 `workspace/source-index/function-index.jsonl`。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| `AFSIM::Module::mystic::Class::RvBAT::GraphicsNode` | InitializeSensorPlatforms | `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `AFSIM::Module::mystic::Class::RvBAT::GraphicsNode` | InitializeSensorPlatforms | `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `AFSIM::Module::mystic::Class::RvBAT::GraphicsNode` | CreateAndInitialize | `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |

## 附录：方法级功能完整清单

Method-level 条目数量超过正文可读范围，正文保留代表性样例。完整清单见 `workspace/source-index/function-index.jsonl`，该索引逐行记录 `qualified_name`、`lifecycle_role`、`algorithm_hint`、源码路径、行号和调用摘要。

| qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|----------------|----------------|----------------|----------|
| `FlightPathAnalysisFunction::InitializeSensorPlatforms#5951e90c26` | object_create | math | method: void InitializeSensorPlatforms() |
| `HorizontalMapFunction::InitializeSensorPlatforms#b952c2c7d5` | object_create | control_flow | method: void InitializeSensorPlatforms(double aSimTime) |
| `Sensor::CreateAndInitialize#a49a527240` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSimulation) |
| `Target::CreateAndInitialize#3924fb0080` | scenario_load | configuration | method: bool CreateAndInitialize(WsfSimulation& aSim) |
| `WsfAdvancedBehaviorTree::Initialize#43a4d4a5e4` | scenario_load | io | method: bool Initialize(double aSimTime, WsfScriptProcessor* aParentPtr, WsfScriptContext* aParentC… |
| `BT::WsfAdvancedBehaviorTreeCompositeNode::Initialize#816a3c95a6` | object_create | none | method: bool Initialize(double aSimTime, WsfScriptContext* aParentContextPtr) override |
| `BT::WsfAdvancedBehaviorTreeNode::Initialize#d6d272b7bd` | object_create | control_flow | method: virtual bool Initialize(double aSimTime, WsfScriptContext* aParentContextPtr) |
| `BaseData::Initialize#2673dc8d64` | object_create | none | method: virtual bool Initialize(WsfAntennaPattern& aAntennaPattern) |
| `BaseData::InitializeAverageGain#b40b477985` | object_create | math | method: virtual void InitializeAverageGain(double aFrequency) |
| `WsfAntennaPattern::Initialize#2673dc8d64` | object_create | none | method: virtual bool Initialize(WsfAntennaPattern& aAntennaPattern) |
| `WsfAntennaPattern::Initialize#1a530f5394` | object_create | none | method: virtual bool Initialize(WsfSimulation* aSimulationPtr) |
| `WsfAntennaPattern::InitializeAverageGain#b40b477985` | object_create | math | method: virtual void InitializeAverageGain(double aFrequency) |
| `WsfAntennaPatternTypes::InitializeType#d4ece0ba7c` | object_create | none | method: bool InitializeType(WsfAntennaPattern* aObjectPtr) override |
| `WsfApplication::InitializeTestEnvironment#ec3693bcf6` | object_create | control_flow | method: bool InitializeTestEnvironment() |
| `WsfArticulatedPart::Initialize#271bbe4cdd` | scenario_load | io | method: bool Initialize(double aSimTime) override |
| `WsfBehaviorTree::Initialize#43a4d4a5e4` | object_create | none | method: bool Initialize(double aSimTime, WsfScriptProcessor* aParentPtr, WsfScriptContext* aParentC… |
| `WsfBehaviorTreeNode::Initialize#bdd2f9fc68` | object_create | control_flow | method: virtual bool Initialize(double aSimTime, WsfScriptContext* aParentContext) |
| `WsfComponent::Initialize#9c9b3829f1` | object_create | none | method: virtual bool Initialize(double aSimTime) |
| `WsfComponent::Initialize2#57ee9d3c2f` | utility | none | method: virtual bool Initialize2(double aSimTime) |
| `WsfComponent::PreInitialize#8d53da36f3` | object_create | none | method: virtual bool PreInitialize(double aSimTime) |
| `WsfComponentFactory::PreInitialize#d043845bab` | object_create | factory | method: virtual bool PreInitialize(double aSimTime, PARENT_TYPE& aParent) |
| `WsfDefaultFusion::Initialize#58e00c25e3` | simulation_loop | state_update | method: bool Initialize(WsfTrackManager* aTrackManagerPtr) override |
| `WsfEM_Antenna::Initialize#5c3e794630` | object_create | none | method: virtual bool Initialize(WsfArticulatedPart* aArticulatedPartPtr) |
| `WsfEM_Attenuation::Initialize#060255d34d` | object_create | none | method: virtual bool Initialize(WsfEM_Xmtr* aXmtrPtr) |
