# Phase 2 模块概览增量版

> **日期**：2026-06-24
> **状态**：增量进行中
> **工作方式**：按最小目录单元逐步补强，完整工作清单见 `workspace/source-index/phase2-analysis-unit-worklist.jsonl`

## 0. 概览说明

Phase 2 v2 不再沿用旧版“107 个同层模块”组织方式，而是以 Phase 1 的 `module_hierarchy` 为准，按系统、子系统、最小目录单元逐步分析。

当前默认范围内共有 237 个最小目录单元、17,179 个 source/header 文件。已完成 7 个单元：

| # | 系统 | 子系统 | 最小目录单元 | 文件数 | 状态 | 详情 |
|---|------|--------|--------------|--------|------|------|
| 1 | core_framework | core/wsf_weapon_server | `afsim-2_9/swdev/src/core/wsf_weapon_server/source` | 2 | 已完成 batch01 | 见第 1 节 |
| 2 | core_framework | core/wsf_grammar_check | `afsim-2_9/swdev/src/core/wsf_grammar_check/source` | 2 | 已完成 batch02 | 见第 2 节 |
| 3 | applications | mission/source | `afsim-2_9/swdev/src/mission/source` | 2 | 已完成 batch03 | 见第 3 节 |
| 4 | plugin_modules | wsf_plugins/wsf_simdis | `afsim-2_9/swdev/src/wsf_plugins/wsf_simdis/source` | 2 | 已完成 batch04 | 见第 4 节 |
| 5 | plugin_modules | wsf_plugins/wsf_scenario_analyzer_iads_c2 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer_iads_c2/source` | 2 | 已完成 batch04 | 见第 5 节 |
| 6 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultAcesDisplay/source` | 2 | 已完成 batch04 | 见第 6 节 |
| 7 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultAirCombatVisualization/source` | 2 | 已完成 batch04 | 见第 7 节 |

默认边界外路径：

| 路径 | 处理 |
|------|------|
| `afsim-2_9/demos` | 不进入默认模块概览；可作场景证据。 |
| `afsim-2_9/documentation` | 不进入源码模块；可作文档证据。 |
| `afsim-2_9/training` | 不进入默认架构分析；如需分析需单独设定 scope。 |
| `afsim-2_9/resources` | 不进入默认源码模块；仅配置/资源流按需引用。 |

## 1. core/wsf_weapon_server/source

### 1.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework`（核心框架） |
| 子系统 | `core/wsf_weapon_server`（武器服务器） |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_weapon_server/source` |
| 文件数 | 2 |
| 源文件 | `WsfWeaponServer.cpp` |
| 头文件 | `WsfWeaponServer.hpp` |
| 证据 | CodeGraph node + 源码行号 |

### 1.2 职责说明

`wsf_weapon_server` 是核心框架中的武器服务器扩展。它负责在仿真运行期间连接外部武器服务器或客户端，解析 `RELEASE_STORE` 等外部命令，维护武器/控制器 track number 映射，处理 LAR（Launch Acceptability Region，发射可接受区）数据，并通过 DIS/TCP 与外部系统交换武器发射相关信息。

### 1.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `WsfWeaponServer.hpp` | 定义配置输入、场景扩展、仿真扩展主体、TCP 更新事件以及 LAR/发射/遥测消息结构。 | `WsfWeaponServerInput`, `WsfWeaponServerExtension`, `WsfWeaponServer`, `TCPUpdateEvent` | `ProcessInput`, `SimulationCreated`, `Initialize`, `Update`, `ProcessCommand` |
| `WsfWeaponServer.cpp` | 实现扩展注册、输入解析、TCP/DIS 通信、命令处理、LAR 数据处理和仿真回调。 | `Register_wsf_weapon_server`, `WsfWeaponServer`, `WsfWeaponServerExtension` | `Register_wsf_weapon_server`, `ProcessCommand`, `GenerateCommand`, `HandleSetDataPDU`, `GetLARData` |

### 1.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `WsfWeaponServerInput` | struct（结构体） | 无 | `WsfWeaponServer.hpp:46` | 保存武器名称映射、平台挂点映射、LAR 映射、DIS track number 和 TCP 连接参数。 |
| `WsfWeaponServerExtension` | class（类） | `WsfScenarioExtension`, `WsfWeaponServerInput` | `WsfWeaponServer.hpp:95` | 解析 `wsf_weapon_server` 输入块，并在仿真创建时注册运行时扩展。 |
| `WsfWeaponServer` | class（类） | `WsfWeaponServerInput`, `WsfSimulationExtension` | `WsfWeaponServer.hpp:106` | 武器服务器运行时扩展主体，维护连接、处理命令、回调平台/武器/DIS 接口。 |
| `IdentifierType` | enum（枚举） | 无 | `WsfWeaponServer.hpp:116` | 标识目标/武器/平台时可使用的识别方式位掩码。 |
| `ValidityType` | enum（枚举） | 无 | `WsfWeaponServer.hpp:127` | 外部命令中频率、MID、位置、速度等字段的有效性位掩码。 |
| `TCPUpdateEvent` | class（类） | `WsfEvent` | `WsfWeaponServer.hpp:396` | 定期触发 TCP socket 更新的仿真事件。 |

### 1.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 扩展注册 | `Register_wsf_weapon_server` 注册 `wsf_weapon_server` 扩展与 `weapon_server` feature。 | `WsfWeaponServer.cpp:80-88` |
| 依赖扩展 | 该扩展依赖 `wsf_mil` 与 `dis_interface`；启用 Link-16 时依赖 `wsf_l16`。 | `WsfWeaponServer.cpp:87-92` |
| 场景解析 | `WsfWeaponServerExtension::ProcessInput` 解析 `wsf_weapon_server` 块中的 host、port、weapon mapping、LAR 参数。 | `WsfWeaponServer.cpp:281-535` |
| 仿真接入 | `SimulationCreated` 从仿真中获取 `dis_interface` 并注册 `WsfWeaponServer`。 | `WsfWeaponServer.cpp:540-548` |
| 运行回调 | `InitiateCallbacks` 订阅平台初始化、添加、删除和 DIS SetData 接收事件。 | `WsfWeaponServer.cpp:258-266` |

### 1.6 修正记录

旧 Phase 2 把导出宏 `WSF_WEAPON_SERVER_EXPORT` 误识别为 struct 名。batch01 已将其修正为真实符号：

| 旧错误 | 修正后 |
|--------|--------|
| `symbol_name=WSF_WEAPON_SERVER_EXPORT`, `kind=struct` | `symbol_name=WsfWeaponServerInput`, `kind=struct` |

`WSF_WEAPON_SERVER_EXPORT` 仍保留在 `signature` 中，因为它是源码声明的一部分，但不再作为 `symbol_name` 或 `qualified_name`。

## 2. core/wsf_grammar_check/source

### 2.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework`（核心框架） |
| 子系统 | `core/wsf_grammar_check`（语法检查扩展） |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_grammar_check/source` |
| 文件数 | 2 |
| 源文件 | `WsfGrammarCheck.cpp` |
| 头文件 | `WsfGrammarCheck.hpp` |
| 证据 | CodeGraph node + 源码行号 |

### 2.2 职责说明

`wsf_grammar_check` 是核心框架中的语法一致性检查扩展。它在测试启用且应用提供 grammar 文本时，随场景文件加载创建 `WsfParser`，用 grammar 重新解析输入文件，并将 grammar 不匹配或解析失败输出为测试失败/解析错误日志。该模块不负责仿真业务逻辑，而是面向开发和测试阶段验证 `UtInput`/grammar 定义是否覆盖场景输入。

### 2.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `WsfGrammarCheck.hpp` | 声明语法检查场景扩展和 parser 源文件提供器。 | `WsfGrammarCheckExtension`, `ParseSourceProvider` | `FileLoaded`, `InitializeGrammar`, `FileLoad`, `FindSource` |
| `WsfGrammarCheck.cpp` | 实现扩展注册、grammar 初始化、场景文件解析检查、错误行号计算和源码文档读取。 | `Register_wsf_grammar_check`, `WsfGrammarCheckExtension`, `ParseSourceProvider`, `GetLineNumber` | `Register_wsf_grammar_check`, `FileLoaded`, `InitializeGrammar`, `FileLoad`, `FindSource` |

### 2.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `WsfGrammarCheckExtension` | class（类） | `WsfScenarioExtension` | `WsfGrammarCheck.hpp:30` | 场景扩展；在文件加载回调中读取应用 grammar，初始化 parser，并检查输入文件是否符合 grammar。 |
| `ParseSourceProvider` | class（类） | `WsfParseSourceProvider` | `WsfGrammarCheck.hpp:48` | parser 源码提供器；根据 `UtPath` 读取 `UtTextDocument` 并维护待释放指针列表。 |
| `Register_wsf_grammar_check` | function（函数） | 无 | `WsfGrammarCheck.cpp:37` | 向 `WsfApplication` 注册名为 `wsf_grammar_check` 的应用扩展。 |
| `GetLineNumber` | function（匿名命名空间辅助函数） | 无 | `WsfGrammarCheck.cpp:45` | 根据 `UtTextDocumentRange` 起点前的换行符数量计算错误行号。 |

### 2.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 扩展注册 | `Register_wsf_grammar_check` 注册 `WsfDefaultApplicationExtension<WsfGrammarCheckExtension>`。 | `WsfGrammarCheck.cpp:37-41` |
| 场景文件加载回调 | `FileLoaded` 仅在 `IsTestingEnabled()` 且 grammar 非空时执行语法检查。 | `WsfGrammarCheck.cpp:77-108` |
| grammar 初始化 | `InitializeGrammar` 创建 `WsfParseDefinitions`，加载 grammar，初始化后创建 `WsfParser`。 | `WsfGrammarCheck.cpp:111-147` |
| 文件解析检查 | `FileLoad` 调用 `ParseFiles`，再读取 root command，收集 parser error 和顶层未解析 command。 | `WsfGrammarCheck.cpp:150-205` |
| 源文档读取 | `ParseSourceProvider::FindSource` 在路径存在且请求读访问时创建 `UtTextDocument`。 | `WsfGrammarCheck.cpp:217-233` |

### 2.6 修正记录

旧 Phase 2 只记录了 `ParseSourceProvider`，遗漏 `WsfGrammarCheckExtension`，且没有把注册函数和匿名命名空间辅助函数作为 Phase 4 候选。batch02 已补充：

| 旧状态 | 修正后 |
|--------|--------|
| `symbol-index-phase2.jsonl` 仅有 `ParseSourceProvider`，且 `line_end=48`。 | 补入 `WsfGrammarCheckExtension`、完整 `ParseSourceProvider`、`Register_wsf_grammar_check`、`GetLineNumber`。 |
| `file-index.jsonl` 的 `.cpp` 只有笼统 `WsfGrammarCheck`。 | `.cpp` 记录注册、语法初始化、文件解析检查和 source provider 实现。 |
| `WSF_GRAMMAR_CHECK_EXPORT` 存在误识别风险。 | 导出宏仅保留在 `signature` 中，不作为 `symbol_name` 或 `qualified_name`。 |

下游注意：旧 Phase 3 精细索引曾将 `WsfGrammarCheckExtension` 的成员错误归属到 `ParseSourceProvider`。Phase 3 后续应以本节为依据重新精修该最小单元。

## 3. mission/source

### 3.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（应用层） |
| 子系统 | `mission/source`（Mission 标准仿真应用入口） |
| 最小目录单元 | `afsim-2_9/swdev/src/mission/source` |
| 文件数 | 2 |
| 源文件 | `mission.cpp` |
| 头文件 | `MissionVersion.hpp` |
| 证据 | CodeGraph node + 源码行号 |

### 3.2 职责说明

`mission` 是 AFSIM 的标准核心仿真应用入口。它读取包含 WSF 命令的文本输入文件，创建 `WsfStandardApplication`，注册内置扩展、可选扩展和 `xio_interface`，再创建 `WsfScenario` 与 `WsfSimulation`，按命令行选项执行事件步进、帧步进、实时/非实时或 Monte-Carlo 多轮仿真。

### 3.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `mission.cpp` | Mission 可执行程序入口；负责应用初始化、扩展注册、命令行处理、输入文件处理、仿真创建/初始化/运行。 | `main`, `WsfStandardApplication`, `WsfScenario`, `WsfSimulation` | `main`, `RegisterBuiltinExtensions`, `RegisterOptionalExtensions`, `CreateSimulation`, `InitializeSimulation`, `RunEventLoop` |
| `MissionVersion.hpp` | Mission 可执行文件版本与产品信息宏定义。 | `MISSION_VERSION_MAJOR`, `MISSION_VERSION_MINOR`, `MISSION_VERSION_PATCH`, `VER_FILEVERSION_STR`, `VER_PRODUCTNAME_STR` | 无函数 |

### 3.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `main(int,char**)` | function（函数） | 无 | `mission.cpp:80` | Mission 进程入口；负责从应用初始化到仿真事件循环的主流程。 |
| `MISSION_VERSION_MAJOR` | macro（宏） | 无 | `MissionVersion.hpp:14` | Mission 应用主版本号。 |
| `MISSION_VERSION_MINOR` | macro（宏） | 无 | `MissionVersion.hpp:15` | Mission 应用次版本号。 |
| `MISSION_VERSION_PATCH` | macro（宏） | 无 | `MissionVersion.hpp:16` | Mission 应用补丁版本号。 |
| `VER_FILEVERSION_STR` | macro（宏） | 无 | `MissionVersion.hpp:18` | 可执行文件版本字符串。 |
| `VER_PRODUCTVERSION_STR` | macro（宏） | 无 | `MissionVersion.hpp:19` | 产品版本字符串。 |
| `VER_PRODUCTNAME_STR` | macro（宏） | 无 | `MissionVersion.hpp:31` | 产品名称字符串，值为 `AFSIM Mission Application`。 |

### 3.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 应用初始化 | `main` 设置异常处理和应用日志，然后创建 `WsfStandardApplication app("mission", argc, argv)`。 | `mission.cpp:80-88` |
| 扩展注册 | `RegisterBuiltinExtensions(app)`、`RegisterOptionalExtensions(app)` 和 `WSF_REGISTER_EXTENSION(app, xio_interface)` 装配运行时扩展。 | `mission.cpp:90-101` |
| 命令行处理 | `app.ProcessCommandLine(options)` 解析运行模式和输入文件参数。 | `mission.cpp:102-116` |
| 场景输入 | 创建 `WsfScenario scenario(app)` 后调用 `app.ProcessInputFiles(scenario, options.mInputFiles)` 读取 WSF 输入文件。 | `mission.cpp:131-149` |
| 仿真循环 | 对每个 run number 创建 simulation、初始化 simulation，并调用 `app.RunEventLoop` 执行事件循环。 | `mission.cpp:151-192` |

### 3.6 修正记录

旧 Phase 2 对该单元只有笼统 `key_symbols=["mission"]`，没有把应用入口和版本宏拆开。batch03 已补充：

| 旧状态 | 修正后 |
|--------|--------|
| `mission.cpp` 只有泛化符号 `mission`。 | 记录 `main`、应用初始化、扩展注册、输入处理和仿真运行关键调用。 |
| `MissionVersion.hpp` 只有泛化符号 `MissionVersion`。 | 记录版本号、版本字符串和产品名称宏，供 Phase 3 macro-index 精修。 |
| `symbol-index-phase2.jsonl` 无 mission/source 条目。 | 新增 `main(int,char**)` 和 6 个版本/产品宏候选。 |

## 4. wsf_plugins/wsf_simdis/source

### 4.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（WSF 插件模块） |
| 子系统 | `wsf_plugins/wsf_simdis`（SIMDIS 输出插件） |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_simdis/source` |
| 文件数 | 2 |
| 源文件 | `WsfSIMDIS_Interface.cpp` |
| 头文件 | `WsfSIMDIS_Interface.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 4.2 职责说明

`wsf_simdis` 提供 `simdis_interface` 插件能力，用于读取场景输入中的 SIMDIS 输出配置，并在仿真运行期把平台初始化、平台损毁、武器命中、传感器航迹和 DeadReckon 更新写入 SIMDIS ASI 文件。

### 4.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `WsfSIMDIS_Interface.hpp` | 声明 `wsf::simdis::ScenarioExtension` 和 `wsf::simdis::Interface`。 | `wsf::simdis::ScenarioExtension`, `wsf::simdis::Interface` | `ProcessInput`, `SimulationCreated`, `AddedToSimulation`, `GetBeamColor`, `GetFHN` |
| `WsfSIMDIS_Interface.cpp` | 实现插件注册、SIMDIS 输入解析和 ASI 输出事件回调。 | `Register_wsf_simdis`, `WsfPluginVersion`, `WsfPluginSetup` | `ProcessInput`, `AddedToSimulation`, `PlatformInitialized`, `WeaponHit`, `SensorTrackInitiated`, `UpdatePlatform` |

### 4.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `wsf::simdis::ScenarioExtension` | class | `WsfScenarioExtension` | `WsfSIMDIS_Interface.hpp:44-76` | 解析 `simdis_interface` 输入并在 simulation 创建时注册运行期接口。 |
| `wsf::simdis::Interface` | class | `WsfSimulationExtension` | `WsfSIMDIS_Interface.hpp:79-129` | 监听仿真事件并写出 SIMDIS ASI 数据。 |
| `Register_wsf_simdis` | function | 无 | `WsfSIMDIS_Interface.cpp:41-45` | 注册 `simdis_interface` feature 和 `wsf_simdis` 应用扩展。 |
| `WsfPluginVersion` | function | 无 | `WsfSIMDIS_Interface.cpp:51-56` | C ABI 插件版本入口。 |
| `WsfPluginSetup` | function | 无 | `WsfSIMDIS_Interface.cpp:62-65` | C ABI 插件装配入口，调用 `Register_wsf_simdis`。 |

### 4.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WsfPluginSetup` 调用 `Register_wsf_simdis`，后者注册 feature 和 application extension。 | `WsfSIMDIS_Interface.cpp:41-65` |
| 仿真扩展创建 | `ScenarioExtension::SimulationCreated` 注册 `wsf::simdis::Interface`。 | `WsfSIMDIS_Interface.cpp:88-91` |
| 输入解析 | `ScenarioExtension::ProcessInput` 处理 `file`、图标、事件时长、beam color、reference LLA 和 FHN 映射。 | `WsfSIMDIS_Interface.cpp:93-184` |
| 事件订阅 | `Interface::AddedToSimulation` 连接平台、武器、传感器和 DeadReckon 回调。 | `WsfSIMDIS_Interface.cpp:239-272` |

### 4.6 修正记录

旧 Phase 2 该目录只有 namespace 粗条目和文件级泛化说明。batch04 已补充两个核心类、插件入口函数和主要事件方法，并将 `simdis` namespace 的限定名修正为 `wsf::simdis`。

## 5. wsf_plugins/wsf_scenario_analyzer_iads_c2/source

### 5.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（WSF 插件模块） |
| 子系统 | `wsf_plugins/wsf_scenario_analyzer_iads_c2`（IADS C2 场景分析插件） |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer_iads_c2/source` |
| 文件数 | 2 |
| 源文件 | `ScenarioAnalyzerIADSC2.cpp` |
| 头文件 | `ScenarioAnalyzerIADSC2.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 5.2 职责说明

`wsf_scenario_analyzer_iads_c2` 是 IADS C2 场景检查插件。它实现一组围绕 C2 能力、指挥链、传感器/武器管理器、TAR/TTR 和 WMAI 配置的检查函数，并通过 `UtScriptClass` 暴露脚本静态方法，最后由 C ABI 插件入口注册到应用扩展系统。

### 5.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `ScenarioAnalyzerIADSC2.hpp` | 导出 IADS C2 检查 API 声明。 | `ScenarioAnalyzerIADSC2RegisterScriptTypes`, 26 个 `check*` 声明 | `checkAssetManagersHaveUpdateInterval`, `checkBattleManagersDontConflict`, `checkWMAIPlatformDetectsEnemyTTRs` |
| `ScenarioAnalyzerIADSC2.cpp` | 实现检查 helper、公开检查包装、脚本桥接、应用扩展和插件入口。 | `ScenarioAnalyzerIADSC2ScriptClass`, `ScenarioAnalyzerIADSC2Extension`, `Register_wsf_scenario_analyzer_iads_c2` | `runSuiteCheck` 包装函数、`AddedToApplication`, `WsfPluginSetup` |

### 5.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `ScenarioAnalyzerIADSC2` | class | 无 | `ScenarioAnalyzerIADSC2.cpp:1603-1610` | 脚本暴露用的场景分析类名载体。 |
| `ScenarioAnalyzerIADSC2ScriptClass` | class | `UtScriptClass` | `ScenarioAnalyzerIADSC2.cpp:1612-1676` | 将 IADS C2 检查函数注册为脚本静态方法。 |
| `ScenarioAnalyzerIADSC2Extension` | class | `WsfApplicationExtension` | `ScenarioAnalyzerIADSC2.cpp:1860-1868` | 在应用加入时注册脚本类型。 |
| `Register_wsf_scenario_analyzer_iads_c2` | function | 无 | `ScenarioAnalyzerIADSC2.cpp:1870-1879` | 注册插件 feature、依赖和 application extension。 |
| `WsfPluginSetup` | function | 无 | `ScenarioAnalyzerIADSC2.cpp:1890-1893` | C ABI 插件装配入口。 |

### 5.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 检查套件 | 公开 `check*` 函数调用 `runSuiteCheck(cSUITE_NAME, ..., helper)` 执行具体检查。 | `ScenarioAnalyzerIADSC2.cpp:1426-1599` |
| 脚本桥接 | `ScenarioAnalyzerIADSC2ScriptClass` 声明并注册静态方法，`UT_DEFINE_SCRIPT_METHOD` 从脚本上下文取 simulation。 | `ScenarioAnalyzerIADSC2.cpp:1612-1858` |
| 应用扩展 | `AddedToApplication` 将脚本类注册到 `app.GetScriptTypes()`。 | `ScenarioAnalyzerIADSC2.cpp:1863-1867` |
| 插件依赖 | 注册函数声明依赖 `wsf_scenario_analyzer` 和 `wsf_iads_c2`。 | `ScenarioAnalyzerIADSC2.cpp:1870-1879` |

### 5.6 修正记录

旧 Phase 2 对该目录没有粗符号条目，文件说明也只有笼统 `ScenarioAnalyzerIADSC2`。batch04 已补充 3 个类、插件入口、26 个公开检查函数和 29 个核心 helper。保留两个源码事实作为后续复核项：`ScenarioAnalyzerIADSC2RegisterScriptTypes` 在头文件声明但未在本轮证据中发现定义；`checkMaxAquisitionTimeLongEnoughForSensorsToFormTracks` 与 `checkWeaponsOnWMAIPlatformHavRequiredAuxData` 的拼写按源码原样保留。

## 6. mystic/plugins/ResultAcesDisplay/source

### 6.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultAcesDisplay/source` |
| 文件数 | 2 |
| 源文件 | `RvAcesDisplayPlugin.cpp` |
| 头文件 | `RvAcesDisplayPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 6.2 职责说明

`ResultAcesDisplay` 是 Mystic Results-Vis 的 ACES Display 插件。它注册 `Aces Display` 插件，把 `.aer`/ResultDb/ResultData 中的平台、SA、航电、武器、航迹、交战、行为树和注释消息转换为 `wkf::AcesDisplay` 数据结构。

### 6.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `RvAcesDisplayPlugin.hpp` | 声明 `RvAcesDisplay::Plugin` 及结果读取、场景清理、SA 判断、数据填充 hooks。 | `RvAcesDisplay::Plugin` | `PlatformAddedRead`, `CommentRead`, `UpdateDataContainer`, `HasSA_Data` |
| `RvAcesDisplayPlugin.cpp` | 注册并实现 ACES Display 插件行为。 | `WKF_PLUGIN_DEFINE_SYMBOLS`, `RvAcesDisplay::Plugin` | `Plugin`, `PlatformAddedRead`, `PopulateEngagementData`, `PopulateBehaviorHistory`, `UpdateDataContainer` |

### 6.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `RvAcesDisplay::Plugin` | class | `rv::PluginT<wkf::AcesDisplay::PluginBase>` | `RvAcesDisplayPlugin.hpp:29-116` | ACES Display 插件主类。 |
| `WKF_PLUGIN_DEFINE_SYMBOLS(RvAcesDisplay::Plugin)` | macro_invocation | 无 | `RvAcesDisplayPlugin.cpp:27-32` | Mystic 插件注册入口。 |
| `RvAcesDisplay::Plugin::UpdateDataContainer` | method | 无 | `RvAcesDisplayPlugin.cpp:374-933` | 汇总平台、飞行、导航、燃油、武器、航迹、交战和行为数据。 |
| `RvAcesDisplay::Plugin::HasSA_Data` | method | 无 | `RvAcesDisplayPlugin.cpp:935-1049` | 判断平台是否具备 SA 数据。 |

### 6.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册 `Aces Display`，provider/category 为 `mystic`，默认不加载。 | `RvAcesDisplayPlugin.cpp:27-32` |
| 结果数据读取 | 插件调用 `rv::ResultDb`、`rv::ResultData`、`rv::ResultPlatform` 读取平台和消息流。 | `RvAcesDisplayPlugin.cpp:86-1049` |
| ACES 数据输出 | 插件写入 `mDataContainer` 并驱动 `wkf::AcesDisplay::PluginBase` 消费。 | `RvAcesDisplayPlugin.cpp:157-933` |

### 6.6 修正记录

旧 Phase 2 只有 namespace/class 粗条目，且 `Plugin` 缺少完整限定名、类范围和基类。batch04 已修正 `RvAcesDisplay::Plugin` 的继承关系并补充插件注册宏和方法级候选。源码中 `RvAcesDisplay::Plugin::Plugin::PlatformAddedRead` 带额外 `Plugin::` 限定，本轮在报告中保留为待复核源码事实，索引按稳定语义归属到 `RvAcesDisplay::Plugin::PlatformAddedRead`。

## 7. mystic/plugins/ResultAirCombatVisualization/source

### 7.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultAirCombatVisualization/source` |
| 文件数 | 2 |
| 源文件 | `RvAirCombatVisualization.cpp` |
| 头文件 | `RvAirCombatVisualization.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 7.2 职责说明

`ResultAirCombatVisualization` 是 Mystic 的空战可视化插件。它注册 `Air Combat Visualization` 插件，读取结果数据中的 SA 空战消息，填充 `wkf::DataContainer`，并通过 `wkf::AirCombatDisplayInterface` 创建或更新地图/沉浸式 viewer 中的装饰、交互线和 overlay。

### 7.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `RvAirCombatVisualization.hpp` | 声明空战可视化插件类及 GUI/偏好/结果读取 hooks。 | `RvAirCombatVisualization::Plugin` | `BuildViewerContextMenu`, `GuiUpdate`, `GetPreferencesWidgets`, `AdvanceTimeRead`, `PopulateData`, `HasSA_Data` |
| `RvAirCombatVisualization.cpp` | 实现插件注册、平台选择响应、空战数据采集和 overlay 更新。 | `WKF_PLUGIN_DEFINE_SYMBOLS`, `(anonymous namespace)::ExtractEngagementSummary`, `RvAirCombatVisualization::Plugin` | `ExtractEngagementSummary`, `BuildViewerContextMenu`, `AdvanceTimeRead`, `PopulateData`, `HasSA_Data` |

### 7.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `RvAirCombatVisualization::Plugin` | class | `rv::Plugin` | `RvAirCombatVisualization.hpp:23-52` | 空战可视化插件主类。 |
| `(anonymous namespace)::ExtractEngagementSummary` | function | 无 | `RvAirCombatVisualization.cpp:30-43` | 从结果平台提取空战交战摘要基础字段。 |
| `WKF_PLUGIN_DEFINE_SYMBOLS(RvAirCombatVisualization::Plugin)` | macro_invocation | 无 | `RvAirCombatVisualization.cpp:46-51` | Mystic 插件注册入口。 |
| `RvAirCombatVisualization::Plugin::PopulateData` | method | 无 | `RvAirCombatVisualization.cpp:301-493` | 将飞行、燃油、武器和交战摘要消息复制到 WKF 空战数据结构。 |

### 7.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册 `Air Combat Visualization`，默认不加载。 | `RvAirCombatVisualization.cpp:46-51` |
| 环境事件 | 构造函数连接 WKF 初始化和平台选择变化。 | `RvAirCombatVisualization.cpp:53-181` |
| Viewer 集成 | `BuildViewerContextMenu` 为 immersive viewer 添加或移除 Air Combat overlay。 | `RvAirCombatVisualization.cpp:183-229` |
| 显示更新 | `GuiUpdate` 调用 `mDisplayInterfacePtr->Update(mDataContainer)`。 | `RvAirCombatVisualization.cpp:231-234` |

### 7.6 修正记录

旧 Phase 2 记录了 namespace/class，但 `Plugin` 缺少 `rv::Plugin` 基类，方法级职责和插件注册入口也未显式索引。batch04 已补充 class 基类、匿名命名空间辅助函数、插件注册宏和主要方法。
