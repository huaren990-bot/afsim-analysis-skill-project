# Phase 2 模块概览增量版

> **日期**：2026-06-24
> **状态**：增量进行中
> **工作方式**：按最小目录单元逐步补强，完整工作清单见 `workspace/source-index/phase2-analysis-unit-worklist.jsonl`

## 0. 概览说明

Phase 2 v2 不再沿用旧版“107 个同层模块”组织方式，而是以 Phase 1 的 `module_hierarchy` 为准，按系统、子系统、最小目录单元逐步分析。

当前默认范围内共有 237 个最小目录单元、17,179 个 source/header 文件。已完成 10 个单元：

| # | 系统 | 子系统 | 最小目录单元 | 文件数 | 状态 | 详情 |
|---|------|--------|--------------|--------|------|------|
| 1 | core_framework | core/wsf_weapon_server | `afsim-2_9/swdev/src/core/wsf_weapon_server/source` | 2 | 已完成 batch01 | 见第 1 节 |
| 2 | core_framework | core/wsf_grammar_check | `afsim-2_9/swdev/src/core/wsf_grammar_check/source` | 2 | 已完成 batch02 | 见第 2 节 |
| 3 | applications | mission/source | `afsim-2_9/swdev/src/mission/source` | 2 | 已完成 batch03 | 见第 3 节 |
| 4 | plugin_modules | wsf_plugins/wsf_simdis | `afsim-2_9/swdev/src/wsf_plugins/wsf_simdis/source` | 2 | 已完成 batch04 | 见第 4 节 |
| 5 | plugin_modules | wsf_plugins/wsf_scenario_analyzer_iads_c2 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer_iads_c2/source` | 2 | 已完成 batch04 | 见第 5 节 |
| 6 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultAcesDisplay/source` | 2 | 已完成 batch04 | 见第 6 节 |
| 7 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultAirCombatVisualization/source` | 2 | 已完成 batch04 | 见第 7 节 |
| 8 | core_framework | core/wsf_parser | `afsim-2_9/swdev/src/core/wsf_parser/legacy_test/source` | 1 | 已完成 batch05 | 见第 8 节 |
| 9 | applications | mystic/exec | `afsim-2_9/swdev/src/mystic/exec/source` | 1 | 已完成 batch05 | 见第 9 节 |
| 10 | applications | post_processor/exec | `afsim-2_9/swdev/src/post_processor/exec/source` | 1 | 已完成 batch05 | 见第 10 节 |

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

## 8. core/wsf_parser/legacy_test/source

### 8.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework`（核心框架） |
| 子系统 | `core/wsf_parser`（WSF parser legacy 测试） |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_parser/legacy_test/source` |
| 文件数 | 1 |
| 源文件 | `wsf_core_parse_test.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 8.2 职责说明

`wsf_core_parse_test` 是 WSF legacy parser 的命令行测试入口。它加载 grammar 文件，构造 `WsfParseDefinitions` 和 `WsfParser`，逐个解析输入文件，统计 parser error 与无法识别的 token，并可通过 `-v` 输出 include 进入事件。

### 8.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `wsf_core_parse_test.cpp` | Parser legacy 测试可执行入口；加载 grammar，解析输入文件并打印错误。 | `ParseSourceProvider`, `GetLineNumber`, `CheckFile`, `PrintInclude`, `main` | `ParseSourceProvider::FindSource`, `GetLineNumber`, `CheckFile`, `PrintInclude`, `main` |

### 8.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `ParseSourceProvider` | class | `WsfParseSourceProvider` | `wsf_core_parse_test.cpp:22-32` | 测试本地 source provider，按文件路径创建 `WsfParseSource`。 |
| `ParseSourceProvider::FindSource` | method | 无 | `wsf_core_parse_test.cpp:26-31` | 在路径是文件时返回 file-backed parse source。 |
| `GetLineNumber` | function | 无 | `wsf_core_parse_test.cpp:33-42` | 根据 parse range 起点前的换行符计算错误行号。 |
| `CheckFile` | function | 无 | `wsf_core_parse_test.cpp:43-87` | 重置 parser、push 输入文件、读取 root node 并收集错误。 |
| `PrintInclude` | function | 无 | `wsf_core_parse_test.cpp:88-94` | 输出 include 进入信息。 |
| `main(int,char**)` | function | 无 | `wsf_core_parse_test.cpp:95-125` | 测试可执行入口。 |

### 8.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| grammar 初始化 | `main` 读取 `argv[1]`，调用 `AddGrammar` 和 `Initialize`。 | `wsf_core_parse_test.cpp:103-107` |
| 输入文件检查 | `main` 对 `argv[2..]` 调用 `CheckFile`；`-v` 连接 include 事件。 | `wsf_core_parse_test.cpp:109-120` |
| parser 错误采集 | `CheckFile` 调用 root `Read`、`ReadWord` 和 `GetErrors`，合并 parser error 与未识别 token。 | `wsf_core_parse_test.cpp:43-87` |

### 8.6 修正记录

旧 Phase 2 对该文件只有泛化 `wsf_core_parse_test` 符号。batch05 补入测试本地 provider 类、辅助函数和 `main`。保留复核项：该文件使用 `std::vector`、`std::string` 但未直接 include 对应标准头，且测试代码中存在 `new` 对象和注释掉的 `treePtr` delete。

## 9. mystic/exec/source

### 9.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic GUI 应用） |
| 子系统 | `mystic/exec` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/exec/source` |
| 文件数 | 1 |
| 源文件 | `mystic.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 9.2 职责说明

`mystic.cpp` 是 Mystic GUI 可执行入口。它设置 Qt 应用元数据和日志/异常处理，解析配置文件与控制台相关命令行参数，创建 WKF/VTK/Mystic 环境，打开 `.aer` event recording 或显示启动对话框，进入 Qt event loop，并在退出时关闭运行管理器和环境对象。

### 9.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `mystic.cpp` | Mystic GUI 应用入口和主运行流程。 | `main`, `(anonymous namespace)::rvExecute`, `ShowUsageDialog`, `IsFileReadable`, `associateFileTypes` | `main`, `rvExecute`, `ShowUsageDialog`, `IsFileReadable`, `associateFileTypes` |

### 9.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `(anonymous namespace)::associateFileTypes` | function | 无 | `mystic.cpp:42-71` | Windows-only `.aer` 文件关联 helper。 |
| `(anonymous namespace)::IsFileReadable` | function | 无 | `mystic.cpp:74-77` | 校验命令行文件参数可读性。 |
| `(anonymous namespace)::ShowUsageDialog` | function | 无 | `mystic.cpp:79-105` | 显示 Mystic 命令行用法对话框。 |
| `(anonymous namespace)::rvExecute` | function | 无 | `mystic.cpp:107-263` | Mystic 主运行流程。 |
| `main(int,char**)` | function | 无 | `mystic.cpp:266-291` | Mystic 应用入口，设置异常处理和 Qt attributes 后调用 `rvExecute`。 |

### 9.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 应用初始化 | `main` 设置异常处理、日志、Qt attributes，并创建 `QApplication`。 | `mystic.cpp:266-279` |
| 环境装配 | `rvExecute` 调用 `wkf::VtkEnvironment::Create(new rv::Factory)`、`wkf::Environment::Create`、`rv::Environment::Create`、`rv::RunManager::Create`。 | `mystic.cpp:207-213` |
| 输入记录打开 | 命令行有文件时直接 `rvEnv.OpenEventRecording(args[1])`，否则显示 `rv::StartupDialog`。 | `mystic.cpp:238-250` |
| 退出清理 | Qt event loop 返回后关闭 `RunManager`、`rvEnv` 和 `wkfEnv`。 | `mystic.cpp:253-262` |

### 9.6 修正记录

旧 Phase 2 对该文件只有泛化 `mystic` 符号。batch05 补入 `main`、`rvExecute` 和匿名命名空间 helper。保留复核项：`associateFileTypes` 在本文件内未发现调用；注释提到 `-ups`，但本文件未解析该参数；`mystic_version_defines.hpp` 未在源码树中发现，按构建生成头处理。

## 10. post_processor/exec/source

### 10.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Post Processor CLI 应用） |
| 子系统 | `post_processor/exec` |
| 最小目录单元 | `afsim-2_9/swdev/src/post_processor/exec/source` |
| 文件数 | 1 |
| 源文件 | `post_processor.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 10.2 职责说明

`post_processor.cpp` 是 Post Processor 命令行可执行入口。它打印版本和构建时间，构造 `Configuration` 解析命令行/配置，执行 CSV 事件输出后处理报表生成，输出耗时，并将 `UtException` 转换为失败退出码。

### 10.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `post_processor.cpp` | Post Processor CLI 入口和报表生成调用链起点。 | `main`, `Configuration`, `UtWallClock`, `UtException`, `POST_PROCESSOR_VERSION` | `main`, `Configuration::Execute`, `Configuration::GetReportTypeStr`, `UtWallClock::GetClock` |

### 10.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `main(int,char**)` | function | 无 | `post_processor.cpp:27-51` | Post Processor CLI 入口；构造配置、执行报表生成、输出耗时并处理异常。 |

### 10.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 版本输出 | `main` 打印 `POST_PROCESSOR_VERSION` 和构建日期/时间。 | `post_processor.cpp:31-32` |
| 配置执行 | `Configuration config({argv, argc})` 后调用 `config.Execute()`。 | `post_processor.cpp:34-39` |
| 耗时输出 | 成功或未生成报表后输出 `UtWallClock::GetClock()`。 | `post_processor.cpp:29-43` |
| 异常处理 | 捕获 `UtException`，输出错误并返回 1。 | `post_processor.cpp:45-50` |

### 10.6 修正记录

旧 Phase 2 对该文件只有泛化 `post_processor` 符号。batch05 补入真实 `main` 入口，并在 file-index 记录 `Configuration::Execute`、`UtWallClock`、`UtException` 等跨模块调用关系。`post_processor_version_defines.hpp` 未在源码树中发现，按构建生成头处理；`Report.hpp` 直接 include 但 `main` 未直接引用，保留为 include hygiene 复核项。

## 11. mystic/plugins/ResultAnnotation/source

### 11.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultAnnotation/source` |
| source/header 数 | 2 |
| 源文件 | `RvPluginAnnotation.cpp`、`RvPluginAnnotation.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 11.2 职责说明

`ResultAnnotation` 是 Mystic 注记显示插件。它消费 annotation event-pipe 消息，将 POI、bullseye、decoration 和 range ring 转换为 WKF 地图注记对象；平台相关 annotation 可能先于平台激活到达，因此插件维护 deferred decoration/range-ring 状态，并在平台激活后补挂显示对象。

### 11.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `RvPluginAnnotation.hpp` | Annotation 插件声明；继承 `rv::PluginT<Annotation::Plugin>` 并维护延迟显示状态。 | `RvAnnotation::Plugin` | `AnnotationReadCB`, `PlatformActiveChangedCB` |
| `RvPluginAnnotation.cpp` | Annotation 插件实现与注册；处理 annotation 消息并驱动 WKF annotation display interface。 | `WKF_PLUGIN_DEFINE_SYMBOLS`, `Vec3fToQColor`, `GetRangeRingProperties` | `RvAnnotation::Plugin::Plugin`, `AnnotationReadCB`, `PlatformActiveChangedCB` |

### 11.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `RvAnnotation::Plugin` | class | `rv::PluginT<Annotation::Plugin>` | `RvPluginAnnotation.hpp:26-42` | Mystic Annotation 插件主体。 |
| `(anonymous namespace)::Vec3fToQColor` | function | 无 | `RvPluginAnnotation.cpp:21-26` | 将 result message 颜色向量转换为 `QColor`。 |
| `(anonymous namespace)::GetRangeRingProperties` | function | 无 | `RvPluginAnnotation.cpp:28-49` | 将 `MsgAnnotationRangeRing` 转换为 WKF range ring 属性。 |
| `RvAnnotation::Plugin::AnnotationReadCB` | method | 无 | `RvPluginAnnotation.cpp:68-138` | 处理 decoration、POI、bullseye 和 range-ring 消息。 |
| `RvAnnotation::Plugin::PlatformActiveChangedCB` | method | 无 | `RvPluginAnnotation.cpp:140-183` | 平台激活后补挂 deferred decoration/range-ring。 |

### 11.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Annotation`、tag `mystic`。 | `RvPluginAnnotation.cpp:52-55` |
| 消息输入 | 构造函数连接 `rvEnv.AnnotationRead` 到 `AnnotationReadCB`。 | `RvPluginAnnotation.cpp:57-64` |
| 显示输出 | `AnnotationReadCB` 调用 `mDisplayInterface` 添加 POI、bullseye、decoration 和 range ring。 | `RvPluginAnnotation.cpp:68-138` |

### 11.6 修正记录

旧 Phase 2 只记录了泛化 `RvPluginAnnotation`。batch06 补入 `RvAnnotation::Plugin`、匿名命名空间 helper、注册宏调用和两个核心回调。保留复核项：generated annotation event-pipe headers 未在当前源码树中找到；`mLastTime` 在本单元内未发现使用；`PlatformActiveChangedCB` 中 deferred range ring 平台路径缺少显式空指针保护。

## 12. mystic/plugins/ResultComment/source

### 12.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultComment/source` |
| source/header 数 | 2 |
| 源文件 | `RvCommentPlugin.cpp`、`RvCommentPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 12.2 职责说明

`ResultComment` 是 Mystic comment bubble 插件。它读取 `MsgComment`，按仿真时间缓存评论，向 comment dock 转发日志文本，并在地图平台对象上创建/更新/删除限时 comment bubble attachment。

### 12.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `RvCommentPlugin.hpp` | Comment 插件声明；定义 `CommentData` 缓存和 `FindCommentByIndex` 匹配谓词。 | `RvComment::Plugin`, `CommentData`, `FindCommentByIndex` | `CommentRead`, `ClearComments`, `AdvanceTimeRead` |
| `RvCommentPlugin.cpp` | Comment 插件实现与注册；处理评论输入、偏好变化和地图气泡重绘。 | `WKF_PLUGIN_DEFINE_SYMBOLS`, `RvComment::Plugin` | `CommentRead`, `Redraw`, `PreferencesChanged`, `FormatMessage` |

### 12.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `RvComment::CommentData` | using | 无 | `RvCommentPlugin.hpp:28` | 按 sim time 存储 attachment id 与 `MsgComment` 的缓存。 |
| `RvComment::FindCommentByIndex` | struct | 无 | `RvCommentPlugin.hpp:31-45` | 用于查找同平台/同 attachment id 的 comment。 |
| `RvComment::Plugin` | class | `rv::Plugin` | `RvCommentPlugin.hpp:47-71` | Mystic Comment Bubbles 插件主体。 |
| `RvComment::Plugin::CommentRead` | method | 无 | `RvCommentPlugin.cpp:36-66` | 接收 comment 消息并更新缓存。 |
| `RvComment::Plugin::Redraw` | method | 无 | `RvCommentPlugin.cpp:104-173` | 根据当前时间、timeout 和偏好更新平台 comment bubble。 |
| `RvComment::Plugin::FormatMessage` | method | 无 | `RvCommentPlugin.cpp:202-215` | 根据偏好在评论前附加时间戳。 |

### 12.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Comment Bubbles`、tag `mystic`。 | `RvCommentPlugin.cpp:31-34` |
| 消息输入 | `rv::PluginT` 将 `rvEnv.CommentRead` 接入 `CommentRead` override。 | `RvCommentPlugin.hpp:55`, `RvCommentPlugin.cpp:36-66` |
| 双路输出 | `CommentRead` 调用 `CommentForwardingService::CommentReceived`；`Redraw` 创建 `wkf::AttachmentDecorator`。 | `RvCommentPlugin.cpp:41-43`, `RvCommentPlugin.cpp:104-173` |

### 12.6 修正记录

旧 Phase 2 只记录了泛化 `RvCommentPlugin`。batch06 补入 comment 缓存类型、匹配谓词和插件核心方法。保留复核项：`MsgComment` generated 定义未在普通源码头中展开；`FindCommentByIndex` 使用 attachment id 匹配，重复同一 simTime/platform comment 的替换行为需要后续确认；显示窗口使用严格 `currentTime > creationTime && currentTime < creationTime + timeout`。

## 13. mystic/plugins/ResultEngagementAnalysis/source

### 13.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultEngagementAnalysis/source` |
| source/header 数 | 2 |
| 源文件 | `RvPluginEngagement.cpp`、`RvPluginEngagement.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 13.2 职责说明

`ResultEngagementAnalysis` 是 Mystic 交战统计插件。它缓存 weapon fired/terminated 事件，在用户打开 Tools 菜单中的 engagement statistics 窗口后，将事件转换为统计行；右键 trace 可从 weapon/track id 回溯武器发射、终止、task update、track 创建/相关/去相关等事件时间线。

### 13.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `RvPluginEngagement.hpp` | Engagement Analysis 插件声明；维护统计窗口、事件缓存和互斥锁。 | `RvEngagement::Plugin` | `WeaponFiredEventRead`, `WeaponTerminatedEventRead`, `TraceEvent` |
| `RvPluginEngagement.cpp` | Engagement Analysis 插件实现与注册；处理统计窗口、事件聚合和 trace 对话框。 | `WKF_PLUGIN_DEFINE_SYMBOLS`, `RvEngagement::Plugin` | `ShowEngagements`, `ProcessWeaponFired`, `ProcessWeaponTerminated`, `TraceEvent`, `EngageSort` |

### 13.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `RvEngagement::Plugin` | class | `rv::Plugin` | `RvPluginEngagement.hpp:29-60` | Mystic Engagement Analysis 插件主体。 |
| `RvEngagement::Plugin::ShowEngagements` | method | 无 | `RvPluginEngagement.cpp:52-76` | 创建 engagement statistics 窗口并连接过滤/右键信号。 |
| `RvEngagement::Plugin::WeaponFiredEventRead` | method | 无 | `RvPluginEngagement.cpp:87-96` | 缓存 weapon fired 事件并在窗口存在时立即处理。 |
| `RvEngagement::Plugin::ProcessWeaponTerminated` | method | 无 | `RvPluginEngagement.cpp:148-186` | 将 weapon terminated 事件加入统计模型。 |
| `RvEngagement::Plugin::TraceEvent` | method | 无 | `RvPluginEngagement.cpp:218-435` | 构建 weapon/track 相关事件时间线。 |
| `RvEngagement::Plugin::EngageSort` | method | 无 | `RvPluginEngagement.cpp:437-464` | 按时间与事件优先级排序 trace 事件。 |

### 13.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Engagement Analysis`、tag `mystic`。 | `RvPluginEngagement.cpp:32` |
| 统计入口 | 构造函数向 Tools 菜单插入 `Show Engagement Statistics`。 | `RvPluginEngagement.cpp:34-50` |
| 事件聚合 | `WeaponFiredEventRead` 和 `WeaponTerminatedEventRead` 将事件缓存到 `mEngagementEvents`，并在窗口存在时处理。 | `RvPluginEngagement.cpp:87-107` |
| 事件追踪 | `TraceEvent` 调用 `FindWeaponTerminationByWeaponId`、`FindWeaponFireByWeaponId` 和 `TraceTrackId`。 | `RvPluginEngagement.cpp:218-267` |

### 13.6 修正记录

旧 Phase 2 只记录了泛化 `RvPluginEngagement`。batch06 补入统计窗口、事件读取、事件处理和 trace 相关方法。保留复核项：`ProcessWeaponFired` / `ProcessWeaponTerminated` 查询 `tplat` 后检查变量疑似写成 `aplat`；`TraceEvent` 中对 eventList 指针执行 `delete` 的所有权需要确认；`mUnprocessedEngagementEvents` 声明后未发现使用。

## 14. mystic/plugins/ResultEventMarker/source

### 14.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultEventMarker/source` |
| source/header 数 | 2 |
| 源文件 | `RvEventMarkerPlugin.cpp`、`RvEventMarkerPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 14.2 职责说明

`ResultEventMarker` 是 Mystic 事件标记插件。它在结果回放时间推进时读取平台状态、武器终止和 data extension 自定义事件，在 viewer 上创建 DAMAGED、REMOVED、WEAPON_HIT、WEAPON_MISSED 或自定义事件 marker，并用最近的 entity state 推算事件位置。

### 14.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `RvEventMarkerPlugin.hpp` | Event Marker 插件声明；维护上次处理时间和自定义事件 handler。 | `RvEventMarker::Plugin`, `rv::DataExtension::EventHandler` | `AdvanceTimeRead`, `GetPositionAtTime`, `PluginsLoaded` |
| `RvEventMarkerPlugin.cpp` | Event Marker 插件实现与注册；按时间窗口读取事件并创建 marker。 | `WKF_PLUGIN_DEFINE_SYMBOLS`, `RvEventMarker::Plugin` | `AdvanceTimeRead`, `ClearScenario`, `GetPositionAtTime`, `PluginsLoaded` |

### 14.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `RvEventMarker::Plugin` | class | `rv::PluginT<wkf::EventMarkerPluginBase>` | `RvEventMarkerPlugin.hpp:29-45` | Mystic Event Markers 插件主体。 |
| `RvEventMarker::Plugin::AdvanceTimeRead` | method | 无 | `RvEventMarkerPlugin.cpp:33-211` | 读取近期事件并创建 marker。 |
| `RvEventMarker::Plugin::GetPositionAtTime` | method | 无 | `RvEventMarkerPlugin.cpp:220-244` | 按事件时间推算平台位置。 |
| `RvEventMarker::Plugin::PluginsLoaded` | method | 无 | `RvEventMarkerPlugin.cpp:246-257` | 从已加载 data extension 注册自定义事件 handler。 |

### 14.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Event Markers`、tag `mystic`。 | `RvEventMarkerPlugin.cpp:25` |
| 时间窗口 | 仅当 `time > mLastTime` 时处理 `[max(mLastTime, time-timeout), time)`。 | `RvEventMarkerPlugin.cpp:33-73` |
| 内置事件分类 | 平台 broken/removed 生成 DAMAGED/REMOVED；武器终止按 `geometryResult()` 映射为 WEAPON_HIT/WEAPON_MISSED。 | `RvEventMarkerPlugin.cpp:73-207` |
| 自定义事件 | `PluginsLoaded` 遍历 `rvEnv.GetExtensions()` 并注册 `EventHandler`。 | `RvEventMarkerPlugin.cpp:246-257` |

### 14.6 修正记录

旧 Phase 2 只记录了泛化 `RvEventMarkerPlugin`。batch06 补入内置事件、自定义事件和位置推算相关方法。保留复核项：custom event marker 是否被 `ClearScenario` 完整删除需要确认；DAMAGED/REMOVED 分支直接解引用 `FindPlatformByIndex` 结果；`GetPositionAtTime` 找不到平台或状态时返回原点。

## 15. mystic/plugins/ResultHeadDownView/source

### 15.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultHeadDownView/source` |
| source/header 数 | 2 |
| 源文件 | `RvHeadDownViewPlugin.cpp`、`RvHeadDownViewPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 15.2 职责说明

`ResultHeadDownView` 是 Mystic head-down-display 插件。它只对有 SA 数据的平台添加 Air Combat 右键菜单入口，打开 `HDD::Dockable` 窗口，并把 ResultData 中平台、飞控、导航、燃油、武器、航迹和资产消息转换为 `HDD::HDD_Data`，再推送给打开的 HDD 窗口。

### 15.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `RvHeadDownViewPlugin.hpp` | Head Down View 插件声明；维护 `HDD::DataContainer`、平台到 HDD 窗口映射和偏好控件。 | `RvHeadsDownDisplay::Plugin`, `HDD::DataContainer`, `HDD::Dockable` | `AdvanceTimeRead`, `ConnectToPlatform`, `UpdateDataContainer`, `HasSA_Data` |
| `RvHeadDownViewPlugin.cpp` | Head Down View 插件实现与注册；处理右键菜单、HDD 窗口生命周期和数据转换。 | `WKF_PLUGIN_DEFINE_SYMBOLS`, `RvHeadsDownDisplay::Plugin` | `BuildEntityContextMenu`, `GuiUpdate`, `UpdateDataContainer`, `HasSituationAwarenessProcessor`, `HasSA_Data` |

### 15.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `RvHeadsDownDisplay::Plugin` | class | `rv::Plugin` | `RvHeadDownViewPlugin.hpp:21-95` | Mystic Head Down View 插件主体。 |
| `RvHeadsDownDisplay::Plugin::BuildEntityContextMenu` | method | 无 | `RvHeadDownViewPlugin.cpp:69-91` | 为 SA 平台添加 Air Combat / Head Down View action。 |
| `RvHeadsDownDisplay::Plugin::ConnectToPlatform` | method | 无 | `RvHeadDownViewPlugin.cpp:99-151` | 创建并显示平台 HDD 窗口。 |
| `RvHeadsDownDisplay::Plugin::GuiUpdate` | method | 无 | `RvHeadDownViewPlugin.cpp:182-232` | 将数据容器中的平台/航迹/燃油/武器/导航等数据推给 HDD 窗口。 |
| `RvHeadsDownDisplay::Plugin::UpdateDataContainer` | method | 无 | `RvHeadDownViewPlugin.cpp:259-706` | 从 ResultData 平台消息构造 `HDD::HDD_Data`。 |
| `RvHeadsDownDisplay::Plugin::HasSA_Data` | method | 无 | `RvHeadDownViewPlugin.cpp:727-841` | 检测平台是否存在 SA 相关消息。 |

### 15.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Head Down View`、tag `mystic`，默认不加载。 | `RvHeadDownViewPlugin.cpp:35-39` |
| UI 入口 | 右键菜单只对 `wkf::Platform` 且具备 SA 数据、未打开 HDD 的平台添加 action。 | `RvHeadDownViewPlugin.cpp:69-91` |
| 数据输入 | `UpdateDataContainer` 读取 `MsgEntityState`、`MsgSA_FlightKinematicsData`、`MsgSA_FlightControlsData`、`MsgSA_NavData`、`MsgSA_FuelData`、`MsgSA_WeaponsData`、`MsgSA_TrackData`、`MsgSA_PerceivedAssetsData`。 | `RvHeadDownViewPlugin.cpp:259-706` |
| GUI 输出 | `GuiUpdate` 将 `HDD::HDD_Data` 推给 `HDD::Dockable` setter。 | `RvHeadDownViewPlugin.cpp:182-232` |

### 15.6 修正记录

旧 Phase 2 只记录了泛化 `RvHeadDownViewPlugin`。batch06 补入 UI 入口、窗口生命周期、数据转换和 SA 检测方法。保留复核项：`cHEADS_DOWN_DISPLAY` 未发现使用；`ConnectToPlatformActionHandler` 先读取 `sender->data()` 再检查 sender；EntityState fallback 中 heading 使用 `cDEG_PER_RAD`，pitch/roll 使用 `cRAD_PER_DEG`，单位转换需复核。

## 16. mystic/plugins/ResultHeadUpView/source

### 16.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultHeadUpView/source` |
| source/header 数 | 2 |
| 源文件 | `RvHeadUpViewPlugin.cpp`、`RvHeadUpViewPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 16.2 职责说明

`ResultHeadUpView` 是 Mystic HUD/OTW 插件。它对有 SA 数据的平台添加 Air Combat / Head Up View 菜单入口，打开 HUD dock widget，将平台状态、HUD 模式、姿态插值、飞行、飞控、导航、燃油和武器消息转换为 `wkf::HUD_DataContainer::PlatformData`，并在 GUI 更新时写入 HUD。

### 16.3 文件清单

| 文件 | 中文说明 | 关键符号 | 关键函数 |
|------|----------|----------|----------|
| `RvHeadUpViewPlugin.hpp` | Head Up View 插件声明；维护 HUD 数据容器、平台到 HUD 窗口映射和 HUD 偏好控件。 | `RvHeadsUpDisplay::Plugin`, `wkf::HUD_DataContainer`, `wkf::HUD_DockWidget` | `AdvanceTimeRead`, `ConnectToPlatform`, `UpdateDataContainer`, `UpdateDataForHud`, `HasSA_Data` |
| `RvHeadUpViewPlugin.cpp` | Head Up View 插件实现与注册；处理右键菜单、HUD 窗口生命周期、HUD 数据转换和 GUI 推送。 | `WKF_PLUGIN_DEFINE_SYMBOLS`, `RvHeadsUpDisplay::Plugin` | `BuildEntityContextMenu`, `ConnectToPlatform`, `GuiUpdate`, `UpdateDataContainer`, `UpdateDataForHud`, `HasSituationAwarenessProcessor` |

### 16.4 核心符号

| 符号 | 类型 | 基类 | 源码位置 | 中文说明 |
|------|------|------|----------|----------|
| `RvHeadsUpDisplay::Plugin` | class | `rv::Plugin` | `RvHeadUpViewPlugin.hpp:21-107` | Mystic Head Up View 插件主体。 |
| `RvHeadsUpDisplay::Plugin::BuildEntityContextMenu` | method | 无 | `RvHeadUpViewPlugin.cpp:59-81` | 为 SA 平台添加 Air Combat / Head Up View action。 |
| `RvHeadsUpDisplay::Plugin::ConnectToPlatform` | method | 无 | `RvHeadUpViewPlugin.cpp:88-142` | 创建并初始化 HUD dock widget。 |
| `RvHeadsUpDisplay::Plugin::UpdateDataContainer` | method | 无 | `RvHeadUpViewPlugin.cpp:208-648` | 从 ResultData 平台消息构造 HUD 平台数据。 |
| `RvHeadsUpDisplay::Plugin::UpdateDataForHud` | method | 无 | `RvHeadUpViewPlugin.cpp:650-682` | 将数据容器中对应平台的数据写入 HUD。 |
| `RvHeadsUpDisplay::Plugin::HasSA_Data` | method | 无 | `RvHeadUpViewPlugin.cpp:710-824` | 检测平台是否存在 SA 相关消息。 |

### 16.5 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Head Up View`、tag `mystic`，默认不加载。 | `RvHeadUpViewPlugin.cpp:35-40` |
| UI 入口 | 右键菜单只对 `wkf::Platform` 且具备 SA 数据、未打开 HUD 的平台添加 action。 | `RvHeadUpViewPlugin.cpp:59-81` |
| 数据输入 | `UpdateDataContainer` 读取 `MsgPlatformStatus`、`MsgHUD_Data`、`MsgEntityState`、`MsgSA_FlightKinematicsData`、`MsgSA_FlightControlsData`、`MsgSA_NavData`、`MsgSA_FuelData`、`MsgSA_WeaponsData`。 | `RvHeadUpViewPlugin.cpp:208-648` |
| GUI 输出 | `GuiUpdate` 调用 `UpdateDataForHud`，最终写入 `hud->mPlatData`。 | `RvHeadUpViewPlugin.cpp:165-171`, `RvHeadUpViewPlugin.cpp:650-682` |

### 16.6 修正记录

旧 Phase 2 只记录了泛化 `RvHeadUpViewPlugin`。batch06 补入 UI 入口、窗口生命周期、数据转换、HUD 推送和 SA 检测方法。保留复核项：`cHEADS_UP_VIEW` 未发现使用；`ConnectToPlatform` 先读取 `sender->data()` 再检查 sender；`tempPlatData` 在平台循环外创建，需复核是否可能存在跨平台字段残留；`FirstPerson`/`ShowHUD` 在本文件内未见 action 连接。
