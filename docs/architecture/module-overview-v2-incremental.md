# Phase 2 模块概览增量版

> **日期**：2026-06-24
> **状态**：增量进行中
> **工作方式**：按最小目录单元逐步补强，完整工作清单见 `workspace/source-index/phase2-analysis-unit-worklist.jsonl`

## 0. 概览说明

Phase 2 v2 不再沿用旧版“107 个同层模块”组织方式，而是以 Phase 1 的 `module_hierarchy` 为准，按系统、子系统、最小目录单元逐步分析。

当前默认范围内共有 237 个最小目录单元、17,179 个 source/header 文件。已完成 60 个单元：

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
| 11 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultAnnotation/source` | 2 | 已完成 batch06 | 见第 11 节 |
| 12 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultComment/source` | 2 | 已完成 batch06 | 见第 12 节 |
| 13 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultEngagementAnalysis/source` | 2 | 已完成 batch06 | 见第 13 节 |
| 14 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultEventMarker/source` | 2 | 已完成 batch06 | 见第 14 节 |
| 15 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultHeadDownView/source` | 2 | 已完成 batch06 | 见第 15 节 |
| 16 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultHeadUpView/source` | 2 | 已完成 batch06 | 见第 16 节 |
| 17 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultInteractionLines/source` | 2 | 已完成 batch07 | 见第 17 节 |
| 18 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultOrbit/source` | 2 | 已完成 batch07 | 见第 18 节 |
| 19 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultProjector/source` | 2 | 已完成 batch07 | 见第 19 节 |
| 20 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultRoute/source` | 2 | 已完成 batch07 | 见第 20 节 |
| 21 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultSituationAwarenessDisplay/source` | 2 | 已完成 batch07 | 见第 21 节 |
| 22 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultVisualEffects/source` | 2 | 已完成 batch07 | 见第 22 节 |
| 23 | developer_tools | tools/wkf | `afsim-2_9/swdev/src/tools/wkf/plugins/Visibility/source` | 2 | 已完成 batch08 | 见第 23 节 |
| 24 | applications | wizard/main | `afsim-2_9/swdev/src/wizard/main/source` | 2 | 已完成 batch08 | 见第 24 节 |
| 25 | applications | wizard/plugins | `afsim-2_9/swdev/src/wizard/plugins/MapAnnotation/source` | 2 | 已完成 batch08 | 见第 25 节 |
| 26 | applications | wizard/plugins | `afsim-2_9/swdev/src/wizard/plugins/MysticLauncher/source` | 2 | 已完成 batch08 | 见第 26 节 |
| 27 | applications | wizard/plugins | `afsim-2_9/swdev/src/wizard/plugins/SIMDIS/source` | 2 | 已完成 batch08 | 见第 27 节 |
| 28 | applications | wizard/plugins | `afsim-2_9/swdev/src/wizard/plugins/UnitConversion/source` | 2 | 已完成 batch08 | 见第 28 节 |
| 29 | applications | sensor_plot/source | `afsim-2_9/swdev/src/sensor_plot/source` | 3 | 已完成 batch09 | 见第 29 节 |
| 30 | applications | warlock/warlock_exec | `afsim-2_9/swdev/src/warlock/warlock_exec/source` | 3 | 已完成 batch09 | 见第 30 节 |
| 31 | plugin_modules | wsf_plugins/wsf_argo8 | `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8/source` | 3 | 已完成 batch09 | 见第 31 节 |
| 32 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultBattleManagement/source` | 4 | 已完成 batch09 | 见第 32 节 |
| 33 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultCommVis/source` | 4 | 已完成 batch09 | 见第 33 节 |
| 34 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultDataAirCombat/source` | 4 | 已完成 batch09 | 见第 34 节 |
| 35 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultDataAnnotation/source` | 4 | 已完成 batch10 | 见第 35 节 |
| 36 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultDataCyber/source` | 4 | 已完成 batch10 | 见第 36 节 |
| 37 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultDataP6Dof/source` | 4 | 已完成 batch10 | 见第 37 节 |
| 38 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultDataSixDOF/source` | 4 | 已完成 batch10 | 见第 38 节 |
| 39 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultDataSpace/source` | 4 | 已完成 batch10 | 见第 39 节 |
| 40 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultDataWk/source` | 4 | 已完成 batch10 | 见第 40 节 |
| 41 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultDetectionReport/source` | 4 | 已完成 batch11 | 见第 41 节 |
| 42 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultQuantumTaskerData/source` | 4 | 已完成 batch11 | 见第 42 节 |
| 43 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultSensorVolumes/source` | 4 | 已完成 batch11 | 见第 43 节 |
| 44 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultVaScenarioManager/source` | 4 | 已完成 batch11 | 见第 44 节 |
| 45 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultWsfDraw/source` | 4 | 已完成 batch11 | 见第 45 节 |
| 46 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultZones/source` | 4 | 已完成 batch11 | 见第 46 节 |
| 47 | developer_tools | tools/wkf/plugins | `afsim-2_9/swdev/src/tools/wkf/plugins/ModelBrowser/source` | 4 | 已完成 batch12 | 见第 47 节 |
| 48 | developer_tools | tools/wkf/plugins | `afsim-2_9/swdev/src/tools/wkf/plugins/PositionConverterTool/source` | 4 | 已完成 batch12 | 见第 48 节 |
| 49 | developer_tools | tools/wkf/plugins | `afsim-2_9/swdev/src/tools/wkf/plugins/TerrainTools/source` | 4 | 已完成 batch12 | 见第 49 节 |
| 50 | developer_tools | tools/wkf/plugins | `afsim-2_9/swdev/src/tools/wkf/plugins/UnitConverterTool/source` | 4 | 已完成 batch12 | 见第 50 节 |
| 51 | applications | warlock/plugins | `afsim-2_9/swdev/src/warlock/plugins/AdHocScriptBrowser/source` | 4 | 已完成 batch12 | 见第 51 节 |
| 52 | applications | warlock/plugins | `afsim-2_9/swdev/src/warlock/plugins/Log/source` | 4 | 已完成 batch12 | 见第 52 节 |
| 53 | applications | wizard/plugins | `afsim-2_9/swdev/src/wizard/plugins/ACOImporter/source` | 4 | 已完成 batch13 | 见第 53 节 |
| 54 | applications | wizard/plugins | `afsim-2_9/swdev/src/wizard/plugins/ErrorList/source` | 4 | 已完成 batch13 | 见第 54 节 |
| 55 | applications | wizard/plugins | `afsim-2_9/swdev/src/wizard/plugins/ScenarioImporter/source` | 5 | 已完成 batch13 | 见第 55 节 |
| 56 | plugin_modules | wsf_plugins/wsf_annotation | `afsim-2_9/swdev/src/wsf_plugins/wsf_annotation/source` | 5 | 已完成 batch13 | 见第 56 节 |
| 57 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultAuxData/source` | 6 | 已完成 batch14 | 见第 57 节 |
| 58 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultInteractionPlots/source` | 6 | 已完成 batch14 | 见第 58 节 |
| 59 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultSatelliteTether/source` | 6 | 已完成 batch14 | 见第 59 节 |
| 60 | applications | mystic/plugins | `afsim-2_9/swdev/src/mystic/plugins/ResultTracks/source` | 6 | 已完成 batch14 | 见第 60 节 |

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

## 17. mystic/plugins/ResultInteractionLines/source

### 17.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultInteractionLines/source` |
| source/header 数 | 2 |
| 源文件 | `RvPluginInteraction.cpp`、`RvPluginInteraction.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 17.2 职责说明

`ResultInteractionLines` 是 Mystic 交互线可视化插件。它从 `rv::InteractionDb` 读取平台间 paired、one-time 与 unpaired interaction 事件，把 detect/track/fire/kill/jam/comm/task 等数据插件声明的交互类型转换为 `wkf::AttachmentInteraction` 上的 incoming/outgoing 线或卡片，并支持时间前进、时间回退、timeout 过期和 stacking 偏好。

### 17.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvInteraction::Plugin` | class | `RvPluginInteraction.hpp:33` | 交互线插件主体，继承 `rv::PluginT<wkf::InteractionPluginBase>`。 |
| `RvInteraction::Plugin::AdvanceTimeRead` | method | `RvPluginInteraction.cpp:39` | 从 InteractionDb 按时间窗口读取并应用 interaction add/remove。 |
| `RvInteraction::Plugin::SetPlatformOptionState` | method | `RvPluginInteraction.cpp:257` | 为平台创建交互附件并控制具体 interaction 类型显示。 |
| `RvInteraction::Plugin::AddInteraction` | method | `RvPluginInteraction.cpp:331` | 目标平台显示 incoming，源平台显示 outgoing。 |
| `RvInteraction::Plugin::PluginsLoaded` | method | `RvPluginInteraction.cpp:403` | 从 data extensions 注册 state card 与 interaction 类型。 |

### 17.4 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Interactions`、tag `mystic`；仅记录为 plugin registration metadata。 | `RvPluginInteraction.cpp:24` |
| 数据输入 | 通过 `aData.GetDb()->LockInteractionDb()` 读取 `rv::InteractionDb::Interaction`。 | `RvPluginInteraction.cpp:41-45` |
| 时间语义 | 前进时 start 添加、stop 移除；回退时反向遍历并反向应用。 | `RvPluginInteraction.cpp:75-219` |
| 显示输出 | `AttachmentInteraction::AddInteraction` / `RemoveInteraction` 挂到对应平台实体。 | `RvPluginInteraction.cpp:331-391` |

### 17.5 修正记录

旧 Phase 2 只记录了泛化 `RvPluginInteraction`、`Plugin` 与 `InteractionMap`。batch07 补入 InteractionDb 数据源、时间前进/回退处理、插件扩展注册和 attachment 输出路径。保留复核项：`GetPlatformOptionState` 未检查平台空指针；`mIdLookup[aId]` 会默认插入；回退迭代边界依赖 InteractionArray iterator 语义。

## 18. mystic/plugins/ResultOrbit/source

### 18.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultOrbit/source` |
| source/header 数 | 2 |
| 源文件 | `RvOrbitPlugin.cpp`、`RvOrbitPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 18.2 职责说明

`ResultOrbit` 是 Mystic 轨道显示插件。它对已启用轨道显示的平台读取 `rv::MsgOrbitalElements`，把半长轴、偏心率、RAAN、倾角、近地点幅角、真近点角、机动结果和轨道颜色写入 `wkf::AttachmentOrbit`，并维护每个平台已处理的 message index 以支持去重和时间回退重建。

### 18.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvOrbit::Plugin` | class | `RvOrbitPlugin.hpp:25` | 轨道显示插件主体，继承 `rv::PluginT<wkf::OrbitPluginBase>`。 |
| `RvOrbit::Plugin::AdvanceTimeRead` | method | `RvOrbitPlugin.cpp:61` | 读取 orbital elements 并更新 orbit attachment。 |
| `RvOrbit::Plugin::SetPlatformOptionState` | method | `RvOrbitPlugin.cpp:31` | 平台关闭轨道显示时清理 message index。 |
| `RvOrbit::Plugin::SetEpoch` | method | `RvOrbitPlugin.cpp:114` | 设置轨道 epoch 并添加月球轨道。 |

### 18.4 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Orbit`、tag `mystic`。 | `RvOrbitPlugin.cpp:24` |
| 数据输入 | `FindFirstBefore<rv::MsgOrbitalElements>(simTime)` 获取当前轨道根数。 | `RvOrbitPlugin.cpp:66-68` |
| 显示输出 | `AttachmentOrbit::Add` 写入轨道根数，`UpdateTimeAngle` 刷新当前时间角。 | `RvOrbitPlugin.cpp:96-106` |
| 基类能力 | `wkf::OrbitPluginBase` 管理 orbit interface、平台附件和偏好。 | `RvOrbitPlugin.hpp:25` |

### 18.5 修正记录

旧 Phase 2 只记录了 `RvOrbit` 和 `Plugin`。batch07 补入 orbital elements 数据链路、message index 缓存、颜色策略和 epoch/moon orbit 关系。保留复核项：`FindPlatform` 返回值未判空；`SetPlatformOptionState` 未检查平台空指针；`SetEpoch` 重复调用 `AddMoonOrbit` 是否幂等需结合基类确认。

## 19. mystic/plugins/ResultProjector/source

### 19.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultProjector/source` |
| source/header 数 | 2 |
| 源文件 | `RvProjectorPlugin.cpp`、`RvProjectorPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 19.2 职责说明

`ResultProjector` 是 Mystic 地形投影插件。它在平台上下文菜单中识别可投影的传感器 FOV，为其创建 terrain projector；时间推进时读取平台状态、传感器模式、FOV 与 articulation，合成 model-view/projection 矩阵并更新 `UtoCmeTerrain` 投影。

### 19.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvProjector::Plugin` | class | `RvProjectorPlugin.hpp:18` | 地形投影插件主体。 |
| `RvProjector::Plugin::BuildEntityContextMenu` | method | `RvProjectorPlugin.cpp:36` | 为满足条件的 sensor 添加 Add/Remove Projector 菜单。 |
| `RvProjector::Plugin::CreateProjector` | method | `RvProjectorPlugin.cpp:119` | 在 terrain 上创建 projector 并保存 id。 |
| `RvProjector::Plugin::AdvanceTimeRead` | method | `RvProjectorPlugin.cpp:169` | 根据平台状态和 articulation 更新 projector matrix。 |

### 19.4 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Projector`、tag `mystic`。 | `RvProjectorPlugin.cpp:29` |
| 菜单条件 | sensor 需 on、未 disabled/broken、有 beam、FOV shape 为 0 且角宽受限。 | `RvProjectorPlugin.cpp:58-96` |
| 数据输入 | `MsgEntityState`、`MsgPartArticulationStatus`、`MsgSensorModeChange` 和 `MsgEmitterModeDefinition`。 | `RvProjectorPlugin.cpp:176-207` |
| 显示输出 | `UtoCmeTerrain::AddProjector` / `UpdateProjectorMatrix`。 | `RvProjectorPlugin.cpp:132-135`, `RvProjectorPlugin.cpp:256-258` |

### 19.5 修正记录

旧 Phase 2 只记录了 `RvProjector` 和 `Plugin`。batch07 补入右键菜单筛选、terrain projector 生命周期、矩阵合成和传感器模式链路。保留复核项：`AdvanceTimeRead` 中平台和 `ResultPlatform` 未判空；FOV 只判断非空但访问 `[1]`；`CreateProjector` 中查到 `ent` 后未使用。

## 20. mystic/plugins/ResultRoute/source

### 20.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultRoute/source` |
| source/header 数 | 2 |
| 源文件 | `RvPluginRoute.cpp`、`RvPluginRoute.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 20.2 职责说明

`ResultRoute` 是 Mystic 航路显示插件。它注册平台 option `Route`，开启后创建 `wkf::AttachmentRoute`，从 `rv::MsgRouteChanged` 构建 waypoint 路线；同时提供 `RouteDialog` 表格显示 waypoint label、位置、高度、航向和 goto 信息，并支持附件选中联动表格行。

### 20.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvRoute::Plugin` | class | `RvPluginRoute.hpp:45` | 航路显示插件主体。 |
| `RvRoute::RouteDialog` | class | `RvPluginRoute.hpp:26` | 航路信息对话框。 |
| `GetRouteData` | function | `RvPluginRoute.cpp:31` | 查询平台当前 `MsgRouteChanged`。 |
| `RvRoute::Plugin::BuildRoute` | method | `RvPluginRoute.cpp:160` | 将 route message 转换为 attachment waypoint。 |
| `RvRoute::RouteDialog::Populate` | method | `RvPluginRoute.cpp:332` | 将 route message 填充到表格。 |

### 20.4 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Route`、tag `mystic`。 | `RvPluginRoute.cpp:27` |
| 平台 option | 构造函数调用 `RegisterOption(nullptr, "Route")`。 | `RvPluginRoute.cpp:53-57` |
| 数据输入 | `MsgRouteChanged` 提供 waypoint 列表、当前位置和 heading。 | `RvPluginRoute.cpp:160-263` |
| 显示输出 | `AttachmentRoute::AddWaypoints` 绘制路线；`RouteDialog` 展示 waypoint 表。 | `RvPluginRoute.cpp:260`, `RvPluginRoute.cpp:332-380` |

### 20.5 修正记录

旧 Phase 2 只记录了 `RvRoute`、`RouteDialog` 和 `Plugin`。batch07 补入 route option、route attachment 生命周期、相对 waypoint 转经纬度和表格联动逻辑。保留复核项：`ResetOptionStates` 平台查找未判空；`BuildRoute` 使用 `mRouteMap[aPlatform.GetIndex()]` 的隐式插入语义需确认；`AttachmentSelectedCB` 依赖只在 `mRoutePtr` 非空时连接。

## 21. mystic/plugins/ResultSituationAwarenessDisplay/source

### 21.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultSituationAwarenessDisplay/source` |
| source/header 数 | 2 |
| 源文件 | `RvSituationAwarenessDisplayPlugin.cpp`、`RvSituationAwarenessDisplayPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 21.2 职责说明

`ResultSituationAwarenessDisplay` 是 Mystic SA Display 适配插件，也是本批最接近 AFSIM 业务逻辑的结果显示入口。它把 result DB 中的飞行、导航、燃油、武器、航迹、感知资产、感知目标、优先威胁/目标、编组和 truth 数据转换为 `wkf::SA_Display` 数据容器，由基类 SA Display dock widget 显示。

### 21.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvSA_Display::Plugin` | class | `RvSituationAwarenessDisplayPlugin.hpp:29` | SA Display 适配插件主体。 |
| `RvSA_Display::Plugin::UpdateDataContainer` | method | `RvSituationAwarenessDisplayPlugin.cpp:127` | 聚合 truth 和各类 SA 消息并写入数据容器。 |
| `RvSA_Display::Plugin::PopulateEntityPerception` | method | `RvSituationAwarenessDisplayPlugin.cpp:81` | 映射单个感知实体字段。 |
| `RvSA_Display::Plugin::HasSA_Data` | method | `RvSituationAwarenessDisplayPlugin.cpp:657` | 检测平台是否有任一 SA 消息。 |

### 21.4 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Situation Awareness Display`、tag `mystic`，默认不加载。 | `RvSituationAwarenessDisplayPlugin.cpp:27-32` |
| 基类 UI | `wkf::SA_Display::PluginBase` 负责 Air Combat / SA View 菜单、dock 创建和 GUI 分发。 | `RvSituationAwarenessDisplayPlugin.hpp:29` |
| 数据输入 | 读取 `MsgSA_FlightKinematicsData`、`MsgSA_NavData`、`MsgSA_FuelData`、`MsgSA_WeaponsData`、`MsgSA_TrackData`、感知/威胁/编组消息。 | `RvSituationAwarenessDisplayPlugin.cpp:297-311` |
| 显示输出 | `mDataContainer.SetSA_Data` 和 `SetSA_TruthPlatforms`。 | `RvSituationAwarenessDisplayPlugin.cpp:651-653` |

### 21.5 修正记录

旧 Phase 2 只记录了 `rv`、`RvSA_Display`、`Plugin`。batch07 补入 SA 消息族、truth 聚合、数据容器输出和基类 UI 分发关系。该单元可作为下一步 AFSIM 业务逻辑分析中“态势感知处理结果如何被消费/解释”的入口。保留复核项：`mPlatformsOfInterest` 在派生类中未见读取；pitch/roll 单位转换疑点；无 `MsgEntityState` 时 truth entity 默认值是否安全；`HasSA_Data` 是消息存在性启发式而非真实处理器证明。

## 22. mystic/plugins/ResultVisualEffects/source

### 22.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果查看应用插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultVisualEffects/source` |
| source/header 数 | 2 |
| 源文件 | `RvPluginVisualEffects.cpp`、`RvPluginVisualEffects.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 22.2 职责说明

`ResultVisualEffects` 是 Mystic 视觉特效插件。它根据平台外观变化、武器终止和平台移除消息创建或删除尾迹、发动机烟、火焰、加力、爆炸、碎片和图标化爆炸效果；实际显示生命周期由 `wkf::VisualEffectsDisplayInterface` 管理。

### 22.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvVisualEffects::Plugin` | class | `RvPluginVisualEffects.hpp:23` | 视觉特效插件主体。 |
| `RvVisualEffects::Plugin::AppearanceData` | struct | `RvPluginVisualEffects.hpp:28` | 平台外观历史记录。 |
| `GetEngineData` | function | `RvPluginVisualEffects.cpp:35` | 从模型定义读取 engine 坐标。 |
| `RvVisualEffects::Plugin::AddEffectsBasedOnData` | method | `RvPluginVisualEffects.cpp:87` | 根据新 appearance 创建特效。 |
| `RvVisualEffects::Plugin::AdvanceTimeRead` | method | `RvPluginVisualEffects.cpp:458` | 处理外观变化、武器终止、平台移除和时间回退。 |
| `RvVisualEffects::Plugin::GetPositionAtTime` | method | `RvPluginVisualEffects.cpp:741` | 外推武器/目标爆炸位置。 |

### 22.4 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Visual Effects`、tag `mystic`。 | `RvPluginVisualEffects.cpp:60-63` |
| 数据输入 | `MsgPlatformAppearanceChanged`、`MsgWeaponTerminated`、`MsgPlatformStatus`、`MsgPlatformInfo`。 | `RvPluginVisualEffects.cpp:531-714`, `RvPluginVisualEffects.cpp:730-739` |
| 显示输出 | 向平台或 `anchor` entity 添加 `wkf::VisualEffect`，并由 display interface 更新/清理。 | `RvPluginVisualEffects.cpp:368-400`, `RvPluginVisualEffects.cpp:637-683` |
| 回放语义 | 时间回退时回滚 trailing effects 并暂时隐藏所有 visual effects。 | `RvPluginVisualEffects.cpp:468-529` |

### 22.5 修正记录

旧 Phase 2 只记录了 `RvVisualEffects`、`Plugin`、`AppearanceData`。batch07 补入外观/武器事件输入、特效类型映射、engine offset、爆炸位置外推和时间回退处理。保留复核项：`RemoveEffectsBasedOnData` 的 smoke=3 分支可能漏删组合烟效；武器/目标平台名查找缺少空指针检查；`GetPositionAtTime` 缺少平台空指针保护；appearance 历史时间使用当前 `simTime` 而非消息时间。

## 23. tools/wkf/plugins/Visibility/source

### 23.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF 工具插件） |
| 子系统 | `tools/wkf` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/Visibility/source` |
| source/header 数 | 2 |
| 源文件 | `VisibilityPlugin.cpp`、`VisibilityPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 23.2 职责说明

`Visibility` 是 WKF 用户层平台可见性过滤插件。它创建 `VisibilityDockWidget` 和 viewer 右键菜单，允许用户过滤选中或未选中平台；实际可见性由 `wkfEnv.RegisterPlatformVisibilityFilter` 注册的 lambda 查询 `mIsInvisible`，并通过 `PlatformVisibilityChanged` 通知地图和平台浏览等消费者。

### 23.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `Visibility::Plugin` | class | `VisibilityPlugin.hpp:21` | 可见性过滤插件主体，继承 `wkf::Plugin`。 |
| `Visibility::Plugin::BuildViewerContextMenu` | method | `VisibilityPlugin.cpp:45` | 添加 Visibility 菜单及过滤动作。 |
| `Visibility::Plugin::HideSelected` | method | `VisibilityPlugin.cpp:68` | 标记选中平台不可见。 |
| `Visibility::Plugin::HideUnselected` | method | `VisibilityPlugin.cpp:77` | 标记未选中平台不可见。 |
| `Visibility::Plugin::IsVisible` | method | `VisibilityPlugin.cpp:96` | 供环境过滤器查询平台是否可见。 |

### 23.4 修正记录

旧 Phase 2 只记录了 `Visibility` 和 `Plugin`。batch08 补入 dock widget、viewer context menu、platform visibility filter、选中/未选中过滤和场景移除清理关系。保留复核项：过滤器注册未见注销；`HideUnselected` 未检查 standard scenario 空指针；平台 index 复用语义需结合场景生命周期确认。

## 24. wizard/main/source

### 24.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 应用入口） |
| 子系统 | `wizard/main` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/main/source` |
| source/header 数 | 2 |
| 源文件 | `main.cpp`、`qtmain_win.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 24.2 职责说明

`wizard/main/source` 是 Wizard 可执行程序启动包装层。它设置应用异常日志，把版本、公司和产品信息传给外部 `wizard_main`；Windows GUI 子系统下由 `WinMain` 解析命令行并转发到 `main`。主要业务逻辑在 `wizard_core` / `wizard_main`，本目录只做启动、版本和平台适配。

### 24.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `main` | function | `main.cpp:26` | 初始化日志并调用 `wizard_main`。 |
| `wizard_main` | function declaration | `main.cpp:25` | Wizard core 真实入口声明。 |
| `NvOptimusEnablement` | variable | `main.cpp:21` | Windows NVIDIA Optimus 独显启用导出变量。 |
| `wideToMulti` | function | `qtmain_win.cpp:87` | Windows 宽字符命令行转本地多字节。 |
| `WinMain` | function | `qtmain_win.cpp:95` | Windows GUI 入口，构造 argv 后调用 `main`。 |

### 24.4 修正记录

旧 Phase 2 未给该目录建立粗符号。batch08 补入 Wizard 启动包装链路。保留复核项：`CP_ACP` 转换可能损坏非本地代码页路径；`wideToMulti` 未显式处理转换失败；完整 Wizard 初始化和插件加载需要后续分析 `wizard/lib/source/core/wizard.cpp`。

## 25. wizard/plugins/MapAnnotation/source

### 25.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/MapAnnotation/source` |
| source/header 数 | 2 |
| 源文件 | `WizAnnotationPlugin.cpp`、`WizAnnotationPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 25.2 职责说明

`MapAnnotation` 是 Wizard 侧地图 annotation 双向同步插件。它把 scenario 文本中的 `visual_elements`、`poi`、`decoration`、`range_ring` proxy 节点同步为 WKF/VA 地图对象和附件；同时把地图右键菜单、POI/range-ring 属性面板、装饰动作和删除动作反写回文本编辑器。

### 25.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WizAnnotation::Plugin` | class | `WizAnnotationPlugin.hpp:25` | Wizard annotation 同步插件主体，继承 `wizard::PluginT<Annotation::Plugin>`。 |
| `TextReplacementInfo` | struct | `WizAnnotationPlugin.cpp:48` | 描述文本替换范围、属性名和插入内容。 |
| `AnnotationWrapper` | class | `WizAnnotationPlugin.cpp:299` | 将 replacement 应用到 Wizard editor。 |
| `WizAnnotation::Plugin::OnProxyAvailable` | method | `WizAnnotationPlugin.cpp:596` | 注册 proxy watcher 并初始解析 annotation object maps。 |
| `WizAnnotation::Plugin::ParsePoiNode` | method | `WizAnnotationPlugin.cpp:699` | 将 POI proxy 转换为 POI/Bullseye entity。 |
| `WizAnnotation::Plugin::RingChange` | method | `WizAnnotationPlugin.cpp:909` | 响应 range ring proxy 变化并更新附件属性。 |
| `WizAnnotation::Plugin::InsertCommandIntoFile` | method | `WizAnnotationPlugin.cpp:1264` | 将新 annotation 命令插入 scenario 文件。 |
| `WizAnnotation::Plugin::ProcessRingChanges` | method | `WizAnnotationPlugin.cpp:1471` | 将 range ring 属性面板变化反写文本。 |

### 25.4 关键关系

| 关系 | 说明 | 证据 |
|------|------|------|
| 插件注册 | `WKF_PLUGIN_DEFINE_SYMBOLS` 注册显示名 `Annotations`、tag `wizard`，仅作 plugin registration metadata。 | `WizAnnotationPlugin.cpp:33-36` |
| 文本到地图 | `OnProxyAvailable` watch `decorations`、`pois`、`rangeRings`，并分派 `Parse*Node` / `*Change`。 | `WizAnnotationPlugin.cpp:596-620` |
| 地图到文本 | `DecorateHandler`、`ProcessPoiChanges`、`ProcessRingChanges`、`InsertCommandIntoFile` 通过 editor range 替换或插入命令。 | `WizAnnotationPlugin.cpp:1065`, `WizAnnotationPlugin.cpp:1264`, `WizAnnotationPlugin.cpp:1388`, `WizAnnotationPlugin.cpp:1471` |
| 兼容性开关 | `DisableFeatures` 对低于 2.6 的 WSF executable 禁用 annotation。 | `WizAnnotationPlugin.cpp:1633-1683` |

### 25.5 修正记录

旧 Phase 2 只记录了 `WizAnnotation`、`Plugin`、`ParserFunc`。batch08 补入文本 replacement helper、proxy watcher、POI/decoration/range ring parse/change、地图菜单和属性面板反写链路。该单元是后续分析 Wizard “场景文本编辑器与地图编辑状态一致性”的高价值入口。保留复核项：`DisableFeatures` 版本比较对 `2.10` 可能误判；added 分支直接使用 `nodeList[1]`；`FindIndexNode` 和 `ReplaceNameInNode` 对异常 proxy text 的假设较强；重复 entity name 行为在头文件中明确为 undefined。

## 26. wizard/plugins/MysticLauncher/source

### 26.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/MysticLauncher/source` |
| source/header 数 | 2 |
| 源文件 | `MysticLauncherPlugin.cpp`、`MysticLauncherPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 26.2 职责说明

`MysticLauncher` 为 Wizard 项目浏览器中的 `wsf_pipe` 文件提供 “Open with Mystic” 动作。它通过 `FileTypeCache` 注册文件头检测器，识别 `WSF_PIPE` 文件，推导 `mystic` / `mystic.exe` 路径并启动外部 Mystic 进程。

### 26.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `MysticLauncher::FileDetector` | class | `MysticLauncherPlugin.hpp:21` | 检测 `WSF_PIPE` 文件头。 |
| `MysticLauncher::Plugin` | class | `MysticLauncherPlugin.hpp:31` | Mystic 启动插件主体。 |
| `MysticLauncher::Plugin::ActionsForFileRequested` | method | `MysticLauncherPlugin.cpp:38` | 为 `wsf_pipe` 文件添加 “Open with Mystic”。 |
| `MysticLauncher::Plugin::Startup` | method | `MysticLauncherPlugin.cpp:95` | 启动 Mystic 进程并传入目标文件路径。 |

### 26.4 修正记录

旧 Phase 2 只记录了 `MysticLauncher`、`FileDetector`、`Plugin`。batch08 补入文件类型缓存、右键动作、Mystic 可执行文件推导和进程错误弹窗。保留复核项：`QProcess` 分配后未见释放；插件级 `mFileInfo` 可能被后续右键覆盖；错误输出仅读 2048 字节且未区分 stdout/stderr。

## 27. wizard/plugins/SIMDIS/source

### 27.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/SIMDIS/source` |
| source/header 数 | 2 |
| 源文件 | `SIMDIS_Plugin.cpp`、`SIMDIS_Plugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 27.2 职责说明

`SIMDIS` 是 Wizard 外部 SIMDIS 集成插件。它配置 SIMDIS 可执行文件和模型目录，为 `.asi` 文件提供 “Open with SIMDIS” 动作，并在 WSF 编辑器上下文中为平台/icon 或 simdis-interface-command 提供模型名替换和 beam color 替换。

### 27.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `wizard::SIMDIS::Plugin` | class | `SIMDIS_Plugin.hpp:30` | SIMDIS 集成插件主体。 |
| `ReplaceRangeAction` | struct | `SIMDIS_Plugin.cpp:41` | 封装 TextSource range 替换动作。 |
| `wizard::SIMDIS::Plugin::ConfigureSIMDIS` | method | `SIMDIS_Plugin.cpp:93` | 选择 SIMDIS exe 并定位模型目录。 |
| `wizard::SIMDIS::Plugin::onEditorContextMenu` | method | `SIMDIS_Plugin.cpp:181` | 基于 parse node 添加模型或颜色替换菜单。 |
| `wizard::SIMDIS::Plugin::ReplaceRangeWithColor` | method | `SIMDIS_Plugin.cpp:337` | 颜色选择并替换为十六进制颜色值。 |

### 27.4 修正记录

旧 Phase 2 只记录了 `wizard`、`SIMDIS`、`Plugin`。batch08 补入 Tools 菜单配置、模型目录递归扫描、`.asi` 文件启动、编辑器 parse node 替换和 settings 持久化。保留复核项：`BuildModelList` 假设扩展名长度为 3 且未过滤具体模型类型；颜色编码顺序需结合 SIMDIS 格式确认；`mModelMenu.disconnect()` 断开范围偏宽。

## 28. wizard/plugins/UnitConversion/source

### 28.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/UnitConversion/source` |
| source/header 数 | 2 |
| 源文件 | `UnitConversionPlugin.cpp`、`UnitConversionPlugin.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 28.2 职责说明

`UnitConversion` 是 Wizard 编辑器右键单位换算插件。它根据当前点击位置的 WSF parse value 查找 proxy basic type 的 unit type，解析文本中的 `<double> <unit>`，通过 `UtUnits` 转标准单位再转成同类其他单位，并生成 “Convert To” 子菜单替换原文本。

### 28.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `UnitConversion::Plugin` | class | `UnitConversionPlugin.hpp:25` | 单位换算插件主体。 |
| `UnitConversion::Plugin::OnEditorContextMenu` | method | `UnitConversionPlugin.cpp:32` | 识别 parse value 和 unit type 并生成转换菜单。 |
| `UnitConversion::Plugin::ReplaceRange` | method | `UnitConversionPlugin.cpp:112` | 替换编辑器文本范围。 |

### 28.4 修正记录

旧 Phase 2 只记录了 `wizard`、`UnitConversion`、`Plugin`。batch08 补入 parse/proxy/unit 系统关系、标准单位中转、菜单生成和文本替换链路。保留复核项：只支持 `double unit` 两段文本；默认 stream 输出精度和格式稳定性需确认；沿父节点扫描可能在嵌套 value 上生成多组转换菜单。

## 29. sensor_plot/source

### 29.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Sensor Plot 应用） |
| 子系统 | `sensor_plot/source` |
| 最小目录单元 | `afsim-2_9/swdev/src/sensor_plot/source` |
| source/header 数 | 3 |
| 源文件 | `sensor_plot.cpp`、`StubInterface.hpp`、`StubInterface.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 29.2 职责说明

`sensor_plot/source` 是 Sensor Plot 命令行应用入口，不实现传感器绘图算法本体。它开启 sensor plot mode，创建 `WsfStandardApplication`，注册本地 `SensorPlotExtension`、内置/可选 WSF extension 和 `xio_interface`，读取场景输入后调用 `WsfSensorPlotExtension::ExecutePlots()`。`StubInterface` 允许绘图工具在缺少完整仿真组件时吞掉指定输入命令，并注册一组 `WSF_DUMMY_*` 类型，避免完整作战场景中的无关对象阻断绘图。

### 29.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `SensorPlotExtension` | class | `sensor_plot.cpp:40` | Sensor Plot 应用扩展。 |
| `SensorPlotExtension::ScenarioCreated` | method | `sensor_plot.cpp:50` | 向 scenario 注册 `stub_interface`。 |
| `main` | function | `sensor_plot.cpp:73` | Sensor Plot 命令行入口。 |
| `StubInterface` | class | `StubInterface.hpp:31` | 容错输入扩展。 |
| `WsfDummyObject<T>` | class | `StubInterface.cpp:37` | dummy WSF 对象模板。 |
| `StubInterface::ProcessInput` | method | `StubInterface.cpp:65` | 处理 `ignore_block`、`ignore_line`、`ignore_word`。 |

### 29.4 修正记录

旧 Phase 2 只记录了 `sensor_plot` 和 `StubInterface`。batch09 补入应用启动链、stub scenario extension、dummy mover/sensor/weapon 注册和输入吞掉规则。该单元可支撑下一步分析“AFSIM 场景如何在非完整仿真环境下被读取并转成传感器/天线绘图”。保留复核项：`StubInterface` 静默吞掉配置可能掩盖场景语义缺失；dummy 类型不能代表真实仿真模型；`WsfSensorPlotExtension::Find(scenario)` 后直接解引用。

## 30. warlock/warlock_exec/source

### 30.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 应用） |
| 子系统 | `warlock/warlock_exec` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/warlock_exec/source` |
| source/header 数 | 3 |
| 源文件 | `warlock.cpp`、`WarlockApplicationExtension.hpp`、`WarlockApplicationExtension.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 30.2 职责说明

`warlock_exec/source` 是 Warlock Qt/WKF 桌面应用入口和应用扩展层。它创建 `QApplication`、`WarlockApplication`、VTK/WKF/Warlock/Simulation environment 和 `RunManager`，处理配置/权限/最近场景/最小化等命令行选项，加载 scenario 并进入 Qt event loop。场景创建后还注册 `WarlockScenarioExtension`，在仿真创建时挂接 `WkSimulationObserver` 与 `wk::EventPipeInterface`。

### 30.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WarlockApplicationExtension` | class | `WarlockApplicationExtension.hpp:17` | Warlock 应用扩展。 |
| `WarlockScenarioExtension` | class | `WarlockApplicationExtension.cpp:35` | 场景级 event pipe/observer 扩展。 |
| `WarlockApplicationExtension::ProcessCommandLine` | method | `WarlockApplicationExtension.cpp:83` | 解析 Warlock 专用命令行。 |
| `Register_warlock` | function | `WarlockApplicationExtension.cpp:217` | 注册 `warlock` feature 和 extension。 |
| `wkExecute` | function | `warlock.cpp:107` | Warlock GUI 主运行流程。 |
| `WarlockApplication` | class | `warlock.cpp:273` | `WsfStandardApplication` 包装。 |
| `main` | function | `warlock.cpp:300` | Qt/Warlock 程序入口。 |

### 30.4 修正记录

旧 Phase 2 只记录了 `WarlockApplicationExtension`。batch09 补入 Qt/WKF/VTK/RunManager 生命周期、权限锁定、startup dialog、recent scenario、event pipe 和 simulation observer 链路。该单元是后续分析“Warlock GUI 如何加载场景并驱动仿真运行”的主入口。保留复核项：`-cf`/`-icf` 文件不可读时仍保存路径；`Find(aApp)` 返回值直接解引用；`wkExecute` 聚合多个环境生命周期，shutdown 顺序需谨慎；局部注释存在编码异常。

## 31. wsf_plugins/wsf_argo8/source

### 31.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（WSF 插件） |
| 子系统 | `wsf_plugins/wsf_argo8` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8/source` |
| source/header 数 | 3 |
| 源文件 | `WsfARGO8_Interface.cpp`、`WsfARGO8_Mover.hpp`、`WsfARGO8_Mover.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 31.2 职责说明

`wsf_argo8/source` 是 WSF 与 ARGO8 导弹模型的适配插件。`WsfARGO8_Interface.cpp` 注册 `wsf_argo8` extension，并把 `WSF_ARGO8_MOVER` 加入 scenario mover type 表。`WsfARGO8_Mover` 读取 missile/guidance/seeker/logging 输入，绑定 `WsfWeaponEngagement`、平台、航迹和传感器状态，把 AFSIM 数据转换为 ARGO8 所需 NED/ESD 数据，推进 `Argo8Missile` 状态，并将 miss distance、fuze/termination reason 和 engagement termination 写回 WSF weapon engagement。

### 31.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WsfARGO8_Extension` | class | `WsfARGO8_Interface.cpp:23` | 注册 ARGO8 mover type 的场景扩展。 |
| `Register_wsf_argo8` | function | `WsfARGO8_Interface.cpp:33` | 注册 `argo8` feature 和 extension。 |
| `WsfPluginSetup` | function | `WsfARGO8_Interface.cpp:56` | 插件加载入口。 |
| `WsfARGO8_Mover` | class | `WsfARGO8_Mover.hpp:23` | ARGO8 导弹 mover。 |
| `WsfARGO8_Mover::ProcessInput` | method | `WsfARGO8_Mover.cpp:185` | 读取 missile/guidance/seeker/logging 输入。 |
| `WsfARGO8_Mover::UpdateARGO8` | method | `WsfARGO8_Mover.cpp:434` | 正常交战状态下更新 truth/track guidance 和 seeker 数据。 |
| `WsfARGO8_Mover::TerminateMissile` | method | `WsfARGO8_Mover.cpp:679` | 将终止结果写回 `WsfWeaponEngagement`。 |

### 31.4 修正记录

旧 Phase 2 只记录了 `WsfARGO8_Mover`。batch09 补入插件注册、mover type 注入、场景输入命令、导弹 flyout 主循环、truth/track guidance、seeker 状态、坐标转换和 weapon engagement 结果回写。该单元是后续分析“武器交战结果如何由高保真导弹 flyout 影响”的关键入口。保留复核项：`argo_log_file_path` 路径结尾判断疑似 `||`/`&&` 错误；`Initialize2` 调 `SetRailData` 的 shooter/target 空指针保证需确认；`GetTargetTrack` 未判空 `WsfWeaponEngagement::Find`；`UpdateARGO8Coast` dead-target 分支可能使用未初始化数组。

## 32. mystic/plugins/ResultBattleManagement/source

### 32.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultBattleManagement/source` |
| source/header 数 | 4 |
| 源文件 | `RvBM_Plugin.hpp`、`RvBM_Plugin.cpp`、`RvBM_RuleSets.hpp`、`RvBM_RuleSets.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 32.2 职责说明

`ResultBattleManagement` 是 Mystic/Result Viewer 侧的 Battle Management 展示插件，不参与仿真决策。`RvBM::Plugin` 消费 `ResultData`、平台添加、武器发射和平台状态消息，维护 `mPlatformData`，并通过 WKF BM 基类刷新平台数量、类型和状态图。`RvBM_RuleSets` 从当前 `ResultDb` 中读取 `MsgEntityState` 和 `MsgAuxData`，映射为 damage factor、fuel、aux data 颜色/资源规则。

### 32.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvBM::Plugin` | class | `RvBM_Plugin.hpp:28` | Battle Management 插件主体。 |
| `RvBM::Plugin::InitializePlatformStatus` | method | `RvBM_Plugin.cpp:37` | 注册 Damage Factor/Fuel 规则集。 |
| `RvBM::Plugin::PlatformAddedRead` | method | `RvBM_Plugin.cpp:74` | 写入平台名称、类型、类别、阵营等数据。 |
| `RvBM::RuleSetDamageFactor` | class | `RvBM_RuleSets.hpp:20` | 损伤因子颜色规则。 |
| `RvBM::RuleSetFuel` | class | `RvBM_RuleSets.hpp:28` | 燃油资源规则。 |
| `GetAuxDataValue` | function | `RvBM_RuleSets.cpp:46` | 从 `MsgAuxData` 按 key/mode 取值。 |

### 32.4 修正记录

旧 Phase 2 只记录了 `RvBM` 和若干规则类名。batch09 补入 ResultDb 消费链、平台生命周期、武器标记、状态移除、damage/fuel/aux data 映射和 WKF BM 展示关系。该单元可支撑下一步分析“仿真结果如何被 Mystic 可视化为战斗管理状态”。保留复核项：`RuleSetWeaponCount` 仍为 TODO 且未注册；`GetRvPlatform` 未检查输入平台空指针；AuxData 只取当前时间前第一条匹配消息；`PlatformAddedRead` 使用 message 内 `simTime()` 而非参数。

## 33. mystic/plugins/ResultCommVis/source

### 33.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultCommVis/source` |
| source/header 数 | 4 |
| 源文件 | `RvCommVisPlugin.hpp`、`RvCommVisPlugin.cpp`、`RvCommVisDialog.hpp`、`RvCommVisDialog.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 33.2 职责说明

`ResultCommVis` 是 Mystic 结果层通信拓扑可视化入口。插件构造时向 Tools 菜单添加 `CommVis...` 动作；`NetworkInfoRead` 和 `CommInfoRead` 把 result event pipe 中的 network/comm/link 元数据转为 `wkf::CommEvent`，写入 `wkf::DataContainer` 并交给通用 `wkf::CommVisDialog` 绘制。该目录不实现 AFSIM 通信仿真、路由或物理链路逻辑。

### 33.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvCommVis::Plugin` | class | `RvCommVisPlugin.hpp:21` | CommVis 插件主体。 |
| `RvCommVis::Plugin::Start` | method | `RvCommVisPlugin.cpp:45` | 创建/显示 CommVis dialog 并发送 pending start event。 |
| `RvCommVis::Plugin::NetworkInfoRead` | method | `RvCommVisPlugin.cpp:60` | 转换 `MsgNetworkInfo` 为 AddNetwork event。 |
| `RvCommVis::Plugin::CommInfoRead` | method | `RvCommVisPlugin.cpp:71` | 转换 `MsgCommInfo` 与 links 为 AddComm event。 |
| `RvCommVis::CommVisDialog` | class | `RvCommVisDialog.hpp:22` | 本地 dialog 子类。 |

### 33.4 修正记录

旧 Phase 2 只记录了 `RvCommVis`、`Plugin`、`CommVisDialog`。batch09 补入 Tools 菜单动作、默认不加载插件元数据、network/comm/link 转换和通用 WKF CommVis UI 关系。该单元可支撑下一步分析“结果层通信拓扑如何被展示”。保留复核项：`RouterInfoRead` 和 `AdvanceTimeRead` 为空；本地 `RvCommVis::CommVisDialog` 子类未被 `Start()` 使用；link 字段只填 destination platform/comm；action ownership 需结合 `ut::qt::UiPointer` 与 Qt parent 语义确认。

## 34. mystic/plugins/ResultDataAirCombat/source

### 34.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 数据插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataAirCombat/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginDataAirCombat.hpp`、`RvPluginDataAirCombat.cpp`、`RvAirCombatDataExtension.hpp`、`RvAirCombatDataExtension.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 34.2 职责说明

`ResultDataAirCombat` 是 Mystic result data extension 插件，不是 UI 插件，也不实现空战战术逻辑。插件构造时向 `rvEnv` 注册 `rv::AirCombatDataExtension`。该扩展注册 WSF Air Combat event pipe serializer/schema，识别 11 类 `MsgSA_*` 空战态势、飞行、燃油、导航、飞控、武器、航迹、感知、编组和威胁/目标消息，并按 `platformIndex()` 将消息挂到对应 `ResultPlatform`，使 Mystic 的结果浏览、平台消息缓存和后续显示插件能够识别这些数据。

### 34.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvDataAirCombat::Plugin` | class | `RvPluginDataAirCombat.hpp:19` | Air Combat Data Extension 插件包装。 |
| `RvDataAirCombat::Plugin::Plugin` | constructor | `RvPluginDataAirCombat.cpp:24` | 注册 `AirCombatDataExtension` 到 `rvEnv`。 |
| `rv::AirCombatDataExtension` | class | `RvAirCombatDataExtension.hpp:32` | Air Combat result data extension。 |
| `rv::AirCombatDataExtension::HandlesMessage` | method | `RvAirCombatDataExtension.cpp:20` | 识别 11 类 `MsgSA_*` 消息。 |
| `rv::AirCombatDataExtension::AddMessage` | method | `RvAirCombatDataExtension.cpp:113` | 将消息加入对应 `ResultPlatform`。 |
| `rv::AirCombatDataExtension::RemoveMessage` | method | `RvAirCombatDataExtension.cpp:309` | 从对应 `ResultPlatform` 移除消息。 |
| `rv::AirCombatDataExtension::HandleSA_EngagementSummaryData` | method | `RvAirCombatDataExtension.cpp:461` | 展开 radar/jammer/mission/risk 等字段。 |

### 34.4 修正记录

旧 Phase 2 只记录了 `RvDataAirCombat`、`Plugin`、`AirCombatDataExtension`。batch09 补入 serializer/schema 注册、11 类 SA 消息清单、ResultPlatform 增删链路和 engagement summary 字段映射。该单元是后续追踪 AFSIM 空战业务逻辑的高价值入口：可从 `MsgSA_*` 反查 WSF Air Combat Extension 生产者，形成“仿真处理器/行为逻辑 -> event pipe -> ResultDb -> Mystic 显示”的链路。保留复核项：`HandleMessage()` 调用 handler 后未返回结果，最后总是空 `QVariant`；找不到平台时把 `platformIndex` 改为 0 但不添加消息；除 engagement summary 外多数 handler 只展开 owner/platform；`IsOneTimeMessage` 和 `IsEventMessage` 均为 false，需确认 threat/group 类消息是否需要事件级视图。

## 35. mystic/plugins/ResultDataAnnotation/source

### 35.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 数据插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataAnnotation/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginDataAnnotation.hpp`、`RvPluginDataAnnotation.cpp`、`RvAnnotationDataExtension.hpp`、`RvAnnotationDataExtension.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 35.2 职责说明

`ResultDataAnnotation` 是 WSF Annotation event pipe 进入 Mystic 的 data extension。插件构造时注册 `rv::AnnotationDataExtension`；扩展合并 `wsf_annotation_events.utpack` 生成的 serializer/schema，识别 `MsgAnnotationDecoration`、`MsgAnnotationPoi`、`MsgAnnotationRangeRing` 三类 one-time、非 event 消息。`AddMessage` 不写 `ResultPlatform` 或 `InteractionDb`，而是调用 `rvEnv.AddAnnotationMessage(*aMsg)`，由环境发出 `AnnotationRead` 信号供 ResultAnnotation 等 UI 消费。

### 35.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvDataAnnotation::Plugin` | class | `RvPluginDataAnnotation.hpp:18` | Annotation data 插件包装。 |
| `RvDataAnnotation::Plugin::Plugin` | constructor | `RvPluginDataAnnotation.cpp:23` | 注册 `AnnotationDataExtension`。 |
| `rv::AnnotationDataExtension` | class | `RvAnnotationDataExtension.hpp:24` | Annotation data extension。 |
| `rv::AnnotationDataExtension::HandlesMessage` | method | `RvAnnotationDataExtension.cpp:21` | 识别三类 annotation 消息。 |
| `rv::AnnotationDataExtension::AddMessage` | method | `RvAnnotationDataExtension.cpp:81` | 调用 `rvEnv.AddAnnotationMessage`。 |
| `rv::AnnotationDataExtension::HandleAnnotationRangeRing` | method | `RvAnnotationDataExtension.cpp:192` | 展示 range ring 字段。 |

### 35.4 修正记录

batch10 补入 annotation serializer/schema、one-time 分流、`rvEnv.AddAnnotationMessage` 和 decoration/POI/range-ring 字段展示。该单元是后续分析“场景注释、POI、范围环如何进入 Mystic 地图/附件显示”的入口。保留复核项：`MsgAnnotationRangeRing` schema 中存在 `lat/lon`，当前 handler 未展示；`alignPlatform` 以 `align north = !alignPlatform()` 展示，需确认命名语义；`DecorationType` 异常值返回空串。

## 36. mystic/plugins/ResultDataCyber/source

### 36.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 数据插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataCyber/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginDataCyber.hpp`、`RvPluginDataCyber.cpp`、`RvCyberDataExtension.hpp`、`RvCyberDataExtension.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 36.2 职责说明

`ResultDataCyber` 是 WSF Cyber 判定结果进入 Mystic 的 data extension。它识别 11 类 `MsgCyber*` attack/scan lifecycle 消息，注册 cyber serializer/schema，并在 `AddMessage` 中写入 `InteractionDb`：扫描、攻击使用 paired start/stop interaction，检测、归因、妥协、免疫、损伤等使用 unpaired interaction。它还向 Mystic 提供 Cyber state card 和 interaction metadata，使 ResultInteractionLines、事件表和状态卡可以展示 cyber 关系。

### 36.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvDataCyber::Plugin` | class | `RvPluginDataCyber.hpp:18` | Cyber data 插件包装。 |
| `rv::CyberDataExtension` | class | `RvCyberDataExtension.hpp:32` | Cyber data extension。 |
| `rv::CyberDataExtension::HandlesMessage` | method | `RvCyberDataExtension.cpp:20` | 识别 11 类 `MsgCyber*`。 |
| `rv::CyberDataExtension::AddMessage` | method | `RvCyberDataExtension.cpp:82` | 写入 `InteractionDb`。 |
| `rv::CyberDataExtension::RemoveMessage` | method | `RvCyberDataExtension.cpp:388` | 从 `InteractionDb` 移除。 |
| `rv::CyberDataExtension::GetStateCardList` | method | `RvCyberDataExtension.cpp:925` | 提供 Cyber 状态卡。 |
| `rv::CyberDataExtension::GetInteractionList` | method | `RvCyberDataExtension.cpp:935` | 提供 Cyber interaction metadata。 |

### 36.4 修正记录

batch10 补入 Cyber attack/scan initiated/succeeded/failed/detected/attributed/recovery 消息清单、事件表 handler、InteractionDb paired/unpaired 写入和 Cyber state card/interaction metadata。该单元是后续追踪“Cyber 仿真判定结果如何进入 Mystic 交互线和状态卡”的关键桥。保留复核项：`CyberAttackRecovery` 总是添加 `CyberImmune`，但 remove 仅在 `immunityStatus() > 0` 时移除；Add 对 owner/victim 双侧镜像写入，而 Remove 多数只按一组 owner/victim 调用，需结合 `InteractionDb` 语义确认对称性；`IsEventMessage` 未标 `override`。

## 37. mystic/plugins/ResultDataP6Dof/source

### 37.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 数据插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataP6Dof/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginDataP6Dof.hpp`、`RvPluginDataP6Dof.cpp`、`RvP6DofDataExtension.hpp`、`RvP6DofDataExtension.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 37.2 职责说明

`ResultDataP6Dof` 是旧 P6DOF telemetry 的 Mystic data extension，插件描述已标注 P6DOF movers/plugins 被 SixDOF 替代。扩展注册 P6DOF serializer/schema，识别 8 类 `MsgP6dof*`：core、kinematic、engine fuel、autopilot、autopilot limits、control inputs、control surfaces、force/moment。`AddTypedMessage`/`RemoveTypedMessage` 按 `platformIndex()` 将消息增删到对应 `ResultPlatform::mMessageMap`，供通用事件表和专用 P6DOF 数据界面读取。

### 37.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvDataP6Dof::Plugin` | class | `RvPluginDataP6Dof.hpp:18` | P6DOF data 插件包装。 |
| `rv::P6DofDataExtension` | class | `RvP6DofDataExtension.hpp:29` | P6DOF telemetry data extension。 |
| `rv::P6DofDataExtension::AddTypedMessage` | method | `RvP6DofDataExtension.hpp:55` | 模板化平台消息写入。 |
| `rv::P6DofDataExtension::HandlesMessage` | method | `RvP6DofDataExtension.cpp:18` | 识别 8 类 P6DOF 消息。 |
| `rv::P6DofDataExtension::HandleP6DofCoreData` | method | `RvP6DofDataExtension.cpp:136` | 展示核心飞行数据。 |
| `rv::P6DofDataExtension::HandleP6DofForceMoment` | method | `RvP6DofDataExtension.cpp:816` | 展示力和力矩数据。 |

### 37.4 修正记录

batch10 补入 P6DOF serializer/schema、8 类 telemetry 消息、ResultPlatform 增删模板和 core/kinematic/fuel/autopilot/limits/control/force 字段展示。该单元用于兼容/迁移对照；后续业务逻辑分析优先跟 SixDOF。保留复核项：`MsgP6dofControlSurfaces` 可入库/移除，但 `HandleMessage` 没有对应展示 handler；data extension 返回原始字段，专用 UI 可能进行单位转换，跨 UI 对比时需区分。

## 38. mystic/plugins/ResultDataSixDOF/source

### 38.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 数据插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataSixDOF/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginDataSixDOF.hpp`、`RvPluginDataSixDOF.cpp`、`RvSixDOF_DataExtension.hpp`、`RvSixDOF_DataExtension.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 38.2 职责说明

`ResultDataSixDOF` 是当前 SixDOF telemetry 的 Mystic data extension。它与 P6Dof 结构几乎同构，但使用 `MsgSixDOF_*` 消息和 `wsf_six_dof` event schema。扩展识别 8 类 SixDOF telemetry 消息，按平台写入 `ResultPlatform`，并为通用事件表提供 core、kinematic、engine fuel、autopilot、autopilot limits、control inputs、force/moment 固定列展示。

### 38.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvDataSixDOF::Plugin` | class | `RvPluginDataSixDOF.hpp:18` | SixDOF data 插件包装。 |
| `rv::SixDOF_DataExtension` | class | `RvSixDOF_DataExtension.hpp:29` | SixDOF telemetry data extension。 |
| `rv::SixDOF_DataExtension::AddTypedMessage` | method | `RvSixDOF_DataExtension.hpp:55` | 模板化平台消息写入。 |
| `rv::SixDOF_DataExtension::HandlesMessage` | method | `RvSixDOF_DataExtension.cpp:18` | 识别 8 类 SixDOF 消息。 |
| `rv::SixDOF_DataExtension::HandleSixDOF_CoreData` | method | `RvSixDOF_DataExtension.cpp:136` | 展示核心飞行数据。 |
| `rv::SixDOF_DataExtension::HandleSixDOF_ForceMoment` | method | `RvSixDOF_DataExtension.cpp:818` | 展示力和力矩数据。 |

### 38.4 修正记录

batch10 补入 SixDOF serializer/schema、8 类 telemetry 消息、ResultPlatform 增删模板和字段展示。该单元是后续追踪“SixDOF 飞行动力学 telemetry -> ResultDb -> 专用数据界面/事件表”的主入口。保留复核项：`MsgSixDOF_ControlSurfaces` 可入库/移除，但 `HandleMessage` 没有对应展示 handler；data extension 原始单位与专用 SixDOF UI 的单位转换需区分。

## 39. mystic/plugins/ResultDataSpace/source

### 39.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 数据插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataSpace/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginDataSpace.hpp`、`RvPluginDataSpace.cpp`、`RvSpaceDataExtension.hpp`、`RvSpaceDataExtension.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 39.2 职责说明

`ResultDataSpace` 是 WSF Space 轨道事件进入 Mystic 的 data extension。它只识别 `MsgOrbitalElements`，将其同时视为 one-time 和 event message，展示平台、轨道六根数和 orbit color，并通过 `AddMessage` 挂到对应 `ResultPlatform`。`OrbitEventHandler` 为 EventMarker 等消费者提供 “Orbital Elements Changed” 事件、平台 label、事件位置和事件颜色。

### 39.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvDataSpace::Plugin` | class | `RvPluginDataSpace.hpp:18` | Space data 插件包装。 |
| `rv::SpaceDataExtension` | class | `RvSpaceDataExtension.hpp:20` | Space data extension。 |
| `rv::SpaceDataExtension::OrbitEventHandler` | class | `RvSpaceDataExtension.hpp:31` | 轨道事件 handler。 |
| `rv::SpaceDataExtension::HandlesMessage` | method | `RvSpaceDataExtension.cpp:22` | 识别 `MsgOrbitalElements`。 |
| `rv::SpaceDataExtension::AddMessage` | method | `RvSpaceDataExtension.cpp:148` | 将轨道消息挂到 `ResultPlatform`。 |
| `rv::SpaceDataExtension::OrbitEventHandler::GetPosition` | method | `RvSpaceDataExtension.cpp:177` | 用实体状态外推事件位置。 |

### 39.4 修正记录

batch10 补入 Space serializer/schema、`MsgOrbitalElements` one-time/event 双重身份、轨道字段展示、ResultPlatform 写入和 event handler。该单元是后续分析“空间平台轨道态如何进入 Mystic Orbit/EventMarker/SatelliteTether”的入口。保留复核项：utpack 中 `resultOfManeuver` 当前未在 `HandleMessage` 展示；`OrbitEventHandler::GetPosition` 缺 `MsgEntityState` 时返回 `(0,0,0)`；`AddMessage` 的 `dynamic_cast` 后直接解引用依赖 message id 与实际类型一致；高频轨道更新的 one-time/event 保留策略需确认。

## 40. mystic/plugins/ResultDataWk/source

### 40.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 数据插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultDataWk/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginDataWk.hpp`、`RvPluginDataWk.cpp`、`RvWkDataExtension.hpp`、`RvWkDataExtension.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 40.2 职责说明

`ResultDataWk` 是 Warlock/WK event pipe 进入 Mystic 的 data extension。它识别 `MsgUserAction`、`MsgHUD_Data`、`MsgChatMessage`，注册 WK serializer/schema，并为事件表展示用户操作、HUD 平台和聊天消息字段。只有 `MsgHUD_Data` 进入 `ResultPlatform` 平台级缓存，供 HeadUpView 等回放 UI 按时间读取 HUD mode；UserAction 和 ChatMessage 主要保留在 all-message/事件表展示路径。

### 40.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvDataWk::Plugin` | class | `RvPluginDataWk.hpp:18` | Warlock data 插件包装。 |
| `rv::WkDataExtension` | class | `RvWkDataExtension.hpp:24` | WK data extension。 |
| `rv::WkDataExtension::HandlesMessage` | method | `RvWkDataExtension.cpp:22` | 识别 UserAction/HUD/Chat 三类消息。 |
| `rv::WkDataExtension::AddMessage` | method | `RvWkDataExtension.cpp:69` | 仅将 HUD_DATA 挂到 `ResultPlatform`。 |
| `rv::WkDataExtension::HandleUserAction` | method | `RvWkDataExtension.cpp:103` | 展示用户操作文本。 |
| `rv::WkDataExtension::HandleChatMessage` | method | `RvWkDataExtension.cpp:143` | 展示聊天 sender/channel/text。 |

### 40.4 修正记录

batch10 补入 WK serializer/schema、UserAction/HUD_Data/ChatMessage 分流、HUD 平台缓存和事件表展示字段。该单元是后续分析“Warlock 用户操作、HUD 模式、聊天消息如何进入 Mystic 回放”的入口。保留复核项：`MsgHUD_Data::hudMode` 未在事件表 handler 展示，但 HeadUpView 会消费；UserAction/ChatMessage 不进入二级索引；`HandleHUD_Data` 调 `LookupPlatformVariant` 时把 `platformIndex()` 值作为 valid 参数，需确认 index 0 语义；HUD add 找不到平台时把 index 置 0 但不挂到平台 0。

## 41. mystic/plugins/ResultDetectionReport/source

### 41.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果消费插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultDetectionReport/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginDetectionReport.hpp`、`RvPluginDetectionReport.cpp`、`RvSensorDetectionModel.hpp`、`RvSensorDetectionModel.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 41.2 职责说明

`ResultDetectionReport` 是传感器探测尝试的 Mystic 报表入口，不生产探测消息。它通过平台右键菜单读取 `ResultPlatform::GetDetectionAttemptMap()`，创建 `wkf::SensorDetectionReport`，并由 `RvDetectionReport::SensorDetectionModel` 将 `MsgDetectAttempt` 映射为表格和曲线数据。该链路用于后续追踪“传感器探测判定质量如何进入回放分析界面”：`WsfEventPipeInterface::SensorDetectionAttempt -> MsgDetectAttempt -> ResultPlatform::mDetectionAttemptMap -> SensorDetectionModel::data()`。

### 41.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvDetectionReport::Plugin` | class | `RvPluginDetectionReport.hpp:18` | Detection Report 插件类。 |
| `RvDetectionReport::Plugin::BuildEntityContextMenu` | method | `RvPluginDetectionReport.cpp:44` | 为有 detection attempt 的平台创建报表 action。 |
| `RvDetectionReport::Plugin::CreateReport` | method | `RvPluginDetectionReport.cpp:73` | 创建 WKF report，连接时间、清场、缓存和曲线右键跳转。 |
| `RvDetectionReport::SensorDetectionModel` | class | `RvSensorDetectionModel.hpp:20` | WKF detection report 的 AFSIM 数据模型。 |
| `RvDetectionReport::SensorDetectionModel::data` | method | `RvSensorDetectionModel.cpp:57` | 展示 Pd、required Pd、SNR、噪声、杂波、干扰、遮蔽、签名和状态。 |

### 41.4 修正记录

batch11 将该目录从泛化 UI 插件修正为 detection attempt 消费端，补入 event pipe 生产端、ResultDb/ResultPlatform 分流和报表字段映射。保留复核项：`BuildEntityContextMenu()` 创建 action 后未显式 `addAction`，需确认 `wkf::Action` 构造语义；`SetCacheRange()` 忽略入参并直接解引用 `mArray`，空数据场景需核对。

## 42. mystic/plugins/ResultQuantumTaskerData/source

### 42.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果消费插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultQuantumTaskerData/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginQuantumTaskerData.hpp`、`RvPluginQuantumTaskerData.cpp`、`RvPluginQuantumTaskerDialog.hpp`、`RvPluginQuantumTaskerDialog.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 42.2 职责说明

`ResultQuantumTaskerData` 虽然名称带 `Data`，但不是 data extension；它是 Quantum Tasker 矩阵查看器。插件向 Tools 菜单插入 “Show Quantum Tasker Matrix”，`Dialog::UpdateTable()` 从 `ResultDb::GetQuantumTaskerMatrix()` 读取全局 multimap，按当前仿真时间选择矩阵并填充 task/asset/resource/value/winner 表格。后续业务分析应从 `WsfQuantumTaskerProcessor -> WsfMilEventPipe::QuantumTaskerUpdate -> MsgQuantumTaskerUpdate -> ResultDb::Push -> Dialog::UpdateTable` 追踪任务分配矩阵。

### 42.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvQuantumTasker::Plugin` | class | `RvPluginQuantumTaskerData.hpp:20` | Quantum Tasker matrix 插件类。 |
| `RvQuantumTasker::Plugin::ShowMatrixDialog` | method | `RvPluginQuantumTaskerData.cpp:39` | 懒创建并显示矩阵 dialog。 |
| `RvQuantumTasker::Plugin::AdvanceTimeRead` | method | `RvPluginQuantumTaskerData.cpp:53` | 时间推进时刷新已打开 dialog。 |
| `RvQuantumTasker::Dialog` | class | `RvPluginQuantumTaskerDialog.hpp:21` | Quantum Tasker QTableWidget dialog。 |
| `RvQuantumTasker::Dialog::UpdateTable` | method | `RvPluginQuantumTaskerDialog.cpp:55` | 读取 ResultDb 矩阵并刷新表格。 |

### 42.4 修正记录

batch11 将该目录从“result data 插件”修正为全局矩阵 UI 消费端，补入 ResultDb special-case 分流和生产端事件管道。保留复核项：`ResultDb::Pop()` 未见 `MsgQuantumTaskerUpdate` 清理分支；首个矩阵时间为 `0.0` 时可能被 `mCurMatrixTime` 初始值跳过；Tools 菜单空 action 列表时 `insertAction(*actions().begin())` 需确认。

## 43. mystic/plugins/ResultSensorVolumes/source

### 43.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果消费插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultSensorVolumes/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginSensorVolumes.hpp`、`RvPluginSensorVolumes.cpp`、`RvPlatformSensorVolumes.hpp`、`RvPlatformSensorVolumes.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 43.2 职责说明

`ResultSensorVolumes` 是传感器/干扰机体积的三维可视化适配层，不写 ResultDb。它在时间推进中从 `ResultData/ResultPlatform` 读取 part status、sensor/weapon mode change、emitter mode definition 和 articulation，由 `PlatformVolumes::UpdateAndUnmark()` 创建或更新 `wkf::AttachmentSensorVolume`。该目录说明了“平台传感器模式与姿态消息如何变成 Mystic viewer 中的 sensor/jammer volume 和 boresight 菜单”。

### 43.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvSensorVolumes::Plugin` | class | `RvPluginSensorVolumes.hpp:33` | Sensor/Jammer Volumes 插件类。 |
| `RvSensorVolumes::Plugin::BuildViewerContextMenu` | method | `RvPluginSensorVolumes.cpp:52` | 为 immersive viewer 添加 boresight 菜单。 |
| `RvSensorVolumes::Plugin::AdvanceTimeRead` | method | `RvPluginSensorVolumes.cpp:196` | 读取平台 parts/modes/articulation 并更新 volume。 |
| `RvSensorVolumes::PlatformVolumes` | class | `RvPlatformSensorVolumes.hpp:36` | 单平台 volume 附件管理器。 |
| `RvSensorVolumes::PlatformVolumes::UpdateAndUnmark` | method | `RvPlatformSensorVolumes.cpp:107` | 按 draw mode 重建矩形、圆形、多边形、赤道 FOV、beam width 或 calculated volume。 |

### 43.4 修正记录

batch11 补入 Sensor Volumes 与 VA scenario 的依赖关系：它需要 Scenario Manager 先提供 `wkf::Platform`，再挂附件。保留复核项：`UpdateBoresight()` 中 `statusMsg->on()` 缺少空指针保护；赤道 FOV 路径可能解引用空 `aArticulation`；`FindPlatformByIndex` 返回实体的前置时序需和 Scenario Manager 一起验证。

## 44. mystic/plugins/ResultVaScenarioManager/source

### 44.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果消费插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultVaScenarioManager/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginVaScenarioManager.hpp`、`RvPluginVaScenarioManager.cpp`、`RvVaScenarioManagerInterface.hpp`、`RvVaScenarioManagerInterface.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 44.2 职责说明

`ResultVaScenarioManager` 是 Mystic 回放场景同步的核心消费端。`PlatformAdded()` 从 `ResultDb` 找到 `ResultPlatform` 并缓存平台元数据；`AdvanceTimeRead()` 读取 `MsgPlatformStatus`、`MsgEntityState`、`MsgPartStatus`、`MsgVisualPartDefinition`、`MsgPartArticulationStatus`；`GuiUpdate()` 创建或更新 `wkf::Platform` 和 visual subobject，并发出 observer 通知。该目录是后续分析多个显示插件的前置支点，因为 SensorVolumes、Zones、WsfDraw 等都依赖标准 `VaScenario` 中的平台实体。

### 44.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvVaScenarioManager::Plugin` | class | `RvPluginVaScenarioManager.hpp:25` | VA Scenario Manager 插件包装。 |
| `RvVaScenarioManager::Interface` | class | `RvVaScenarioManagerInterface.hpp:37` | ResultPlatform 到 VaScenario 的同步接口。 |
| `RvVaScenarioManager::Interface::PlatformAdded` | method | `RvVaScenarioManagerInterface.cpp:51` | 缓存平台元数据并写入 WKF 平台分组。 |
| `RvVaScenarioManager::Interface::AdvanceTimeRead` | method | `RvVaScenarioManagerInterface.cpp:108` | 读取平台状态、实体状态和 visual part 消息。 |
| `RvVaScenarioManager::Interface::GuiUpdate` | method | `RvVaScenarioManagerInterface.cpp:281` | 创建/更新 `wkf::Platform`、subobject、observer 和首次相机定位。 |

### 44.4 修正记录

batch11 将该目录明确为 ResultDb/ResultPlatform 到 WKF/VaScenario 的场景生产者。保留复核项：`PlatformAdded()` 中 `FindPlatform` 结果可能为空但后续缓存指针被解引用；`ClearScenario()` 未像 read/gui 路径一样显式加 `mMutex`；visual part dirty/read-time 逻辑可能吞掉同一时刻 definition/articulation 变化。

## 45. mystic/plugins/ResultWsfDraw/source

### 45.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果消费插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultWsfDraw/source` |
| source/header 数 | 4 |
| 源文件 | `RvPluginWsfDraw.hpp`、`RvPluginWsfDraw.cpp`、`RvWsfDrawInterface.hpp`、`RvWsfDrawInterface.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 45.2 职责说明

`ResultWsfDraw` 是 WSF draw command 的 Mystic overlay 适配层。`ResultDb::ProcessOneTimeMessage()` 遇到 `MsgDrawCommand` 后经 `rvEnv.AddDrawMessage` 发出 `DrawCommandRead`，本插件先缓存命令，再由 `Interface::DrawViewerCommand()` 按 layer 创建 `wkf::OverlayWsfDraw`，支持 line、point、icon、ellipse、erase、ellipsoid、quadrilateral、text 和 timer。该目录是后续追踪脚本或模型中 draw 命令如何落到回放地图的消费端。

### 45.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvWsfDraw::Plugin` | class | `RvPluginWsfDraw.hpp:28` | WSF Draw result 插件类。 |
| `RvWsfDraw::Plugin::DrawCommandRead` | method | `RvPluginWsfDraw.cpp:39` | 接收 `MsgDrawCommand` 并入队。 |
| `RvWsfDraw::Interface` | class | `RvWsfDrawInterface.hpp:22` | Overlay model 和 viewer/layer 管理器。 |
| `RvWsfDraw::Interface::MakeVertex` | method | `RvWsfDrawInterface.cpp:89` | 转换 draw vertex，支持相对平台和 placeholder。 |
| `RvWsfDraw::Interface::DrawViewerCommand` | method | `RvWsfDrawInterface.cpp:163` | 按 draw item 类型创建/更新 WKF overlay。 |

### 45.4 修正记录

batch11 补入 `MsgDrawCommand` 的 ResultDb one-time 分流、layer 菜单和 overlay 类型映射。保留复核项：`ProcessDeferredCommands()` 的 try_lock/lock 混合时序需验证；相对平台 placeholder 与真实平台生命周期关系需确认；non-standard viewer 新 layer 默认不可见，需结合 UI 验证。

## 46. mystic/plugins/ResultZones/source

### 46.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果消费插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultZones/source` |
| source/header 数 | 4 |
| 源文件 | `MysticPluginZoneBrowser.hpp`、`MysticPluginZoneBrowser.cpp`、`MysticPluginZoneDockWidget.hpp`、`MysticPluginZoneDockWidget.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 46.2 职责说明

`ResultZones` 是 zone 结果消息的 Mystic 浏览/绘制适配层。`ResultDb::ProcessOneTimeMessage()` 对 `MsgCircularZone`、`MsgEllipticalZone`、`MsgSphericalZone`、`MsgPolygonalZone`、`MsgZoneSet` 调用 `rvEnv.AddZone`，插件显式连接 `rvEnv.ZoneRead`，并把消息转换为 `wkf::ZoneSetData`。`DockWidget` 负责平台删除、reference platform delayed redraw 和基于 `ResultPlatform::IsActive` 的 anchor 判定。

### 46.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `MysticZoneBrowser::Plugin` | class | `MysticPluginZoneBrowser.hpp:29` | Zone browser 插件类。 |
| `CommonZoneVariableConversion` | function | `MysticPluginZoneBrowser.cpp:22` | 转换通用 zone 字段。 |
| `MysticZoneBrowser::Plugin::ZoneRead` | method | `MysticPluginZoneBrowser.cpp:125` | 分流五类 zone message 并转换为 `ZoneSetData`。 |
| `MysticZoneBrowser::Plugin::AddColors` | method | `MysticPluginZoneBrowser.cpp:204` | 使用消息颜色或偏好颜色设置 line/fill。 |
| `MysticZoneBrowser::DockWidget::RemovePlatform` | method | `MysticPluginZoneDockWidget.cpp:28` | 移除平台 zone attachment 并维护 delayed redraw。 |
| `MysticZoneBrowser::DockWidget::GetActiveAnchor` | method | `MysticPluginZoneDockWidget.cpp:95` | 结合 ResultPlatform active 状态返回 WKF anchor。 |

### 46.4 修正记录

batch11 补入 zone 消息 one-time 分流、五类形状字段转换、颜色策略和平台生命周期处理。保留复核项：`ClearScenario()` 只清 `mDataContainer`，未清 `mPlatformZoneData`；`ZoneRead()` 依赖 message id 与实际类型严格一致；reference platform 删除和 delayed redraw 需结合回退/重播场景验证。

## 47. tools/wkf/plugins/ModelBrowser/source

### 47.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF 工具插件） |
| 子系统 | `tools/wkf/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/ModelBrowser/source` |
| source/header 数 | 4 |
| 源文件 | `ModelBrowserPlugin.hpp`、`ModelBrowserPlugin.cpp`、`ModelBrowserWidget.hpp`、`ModelBrowserWidget.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 47.2 职责说明

`ModelBrowser` 是 WKF 模型资源查看/编辑工具。插件向 Tools 菜单注册 `Model Viewer...`，向 Developer 菜单注册 `Reload Model Database`；`Widget` 负责从 `vaEnv.GetModelDatabase()` 请求模型、显示 OSG 预览、加载外部模型文件、预览临时模型定义，并在 `ApplyDefinition()` 中写入或替换 `models.txt` 后重载模型数据库。它不是 AFSIM 仿真业务逻辑入口，但会影响可视化模型资源定义。

### 47.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `ModelBrowser::Plugin` | class | `ModelBrowserPlugin.hpp:19` | WKF Model Browser 插件壳。 |
| `ModelBrowser::Plugin::Launch` | method | `ModelBrowserPlugin.cpp:61` | 懒创建 dock 和 `Widget`。 |
| `ModelBrowser::Plugin::Reload` | method | `ModelBrowserPlugin.cpp:72` | 重置并重载模型数据库。 |
| `ModelBrowser::Widget` | class | `ModelBrowserWidget.hpp:31` | 模型浏览/预览/定义编辑 UI。 |
| `ModelBrowser::Widget::ShowModel` | method | `ModelBrowserWidget.cpp:82` | 从模型库请求模型并显示。 |
| `ModelBrowser::Widget::ApplyDefinition` | method | `ModelBrowserWidget.cpp:316` | 写入/替换 `models.txt` 并重载模型数据库。 |

### 47.4 修正记录

batch12 将该目录定位为 WKF 可视化资源工具，避免误归入 AFSIM 仿真逻辑。保留复核项：`ApplyDefinition()` 采用整文件替换写回 `models.txt`，需要确认原子性、目录创建和错误处理；临时定义预览异常路径需专项验证。

## 48. tools/wkf/plugins/PositionConverterTool/source

### 48.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF 工具插件） |
| 子系统 | `tools/wkf/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/PositionConverterTool/source` |
| source/header 数 | 4 |
| 源文件 | `PositionConverterPlugin.hpp`、`PositionConverterPlugin.cpp`、`PositionConverterDialog.hpp`、`PositionConverterDialog.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 48.2 职责说明

`PositionConverterTool` 是 WKF 工具菜单下的坐标格式转换器。插件创建 `Dialog` 并注册 `Position Converter Tool...`；`Dialog::Convert()` 根据当前页在 latitude/longitude 与 MGRS 间双向转换，使用 `UtEllipsoidalEarth` 和 WKF 经纬度格式偏好输出结果。它不读取或修改场景，不改变平台位置，不参与仿真执行。

### 48.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `PositionConverter::Plugin` | class | `PositionConverterPlugin.hpp:20` | WKF 插件壳。 |
| `PositionConverter::Plugin::Plugin` | constructor | `PositionConverterPlugin.cpp:22` | 注册 Tools 菜单入口。 |
| `PositionConverter::Dialog` | class | `PositionConverterDialog.hpp:22` | 坐标转换 dialog。 |
| `PositionConverter::Dialog::Dialog` | constructor | `PositionConverterDialog.cpp:23` | 初始化 UI 和信号连接。 |
| `PositionConverter::Dialog::Convert` | method | `PositionConverterDialog.cpp:60` | 执行 LL/MGRS 双向转换。 |

### 48.4 修正记录

batch12 将该目录明确为纯工具型 UI 插件。保留复核项：页切换时是否应主动触发 `Convert()`；`Convert()` 依赖页面 `isVisible()` 判断转换方向，需确认 UI 状态假设。

## 49. tools/wkf/plugins/TerrainTools/source

### 49.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF 工具插件） |
| 子系统 | `tools/wkf/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/TerrainTools/source` |
| source/header 数 | 4 |
| 源文件 | `TerrainToolsPlugin.hpp`、`TerrainToolsPlugin.cpp`、`LOS_Ruler.hpp`、`LOS_Ruler.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 49.2 职责说明

`TerrainTools` 是 WKF terrain line-of-sight 交互工具。插件在实体右键菜单中增加 `Line-of-sight from ...`，通过 rubberband 选择目标点或实体，再创建 `LOS_Ruler` 附件。`LOS_Ruler::Recalculate()` 向 WKF resource manager 提交 `LOS_Request` 并读取 `LOS_Result`，`Build()` 绘制可见/阻挡线段，`BuildImage()` 和 plot widget 输出地形剖面。它调用底层地形能力，但不实现仿真推进、传感器模型或战术决策。

### 49.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `TerrainTools::Plugin` | class | `TerrainToolsPlugin.hpp:28` | Terrain LOS 工具插件。 |
| `TerrainTools::Plugin::BuildEntityContextMenu` | method | `TerrainToolsPlugin.cpp:39` | 添加 LOS 右键菜单。 |
| `TerrainTools::Plugin::MakeLOS` | method | `TerrainToolsPlugin.cpp:76` | 创建 `LOS_Ruler` 附件。 |
| `TerrainTools::LOS_Ruler` | class | `LOS_Ruler.hpp:27` | LOS 可视化附件。 |
| `TerrainTools::LOS_Ruler::Build` | method | `LOS_Ruler.cpp:162` | 构建可见/阻挡线段几何。 |
| `TerrainTools::LOS_Ruler::Recalculate` | method | `LOS_Ruler.cpp:354` | 提交 LOS request 并计算阻挡比例。 |

### 49.4 修正记录

batch12 将该目录定位为地形资源能力的 GUI 查询入口。保留复核项：`mActiveRulerPtr` 只用于判断但未见赋值；`BuildImage()` 多处投影计算缺零分母保护；`Recalculate()` 提交 request 后立即取 result，需确认 resource manager 同步/异步语义。

## 50. tools/wkf/plugins/UnitConverterTool/source

### 50.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF 工具插件） |
| 子系统 | `tools/wkf/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/UnitConverterTool/source` |
| source/header 数 | 4 |
| 源文件 | `UnitConverterPlugin.hpp`、`UnitConverterPlugin.cpp`、`UnitConverterDialog.hpp`、`UnitConverterDialog.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 50.2 职责说明

`UnitConverterTool` 是 WKF 通用单位换算工具。插件注册 `Unit Converter Tool...` 菜单；`Dialog` 枚举 `UtUnits::mUnitTypes`，通过 `SetupMaps()` 建立单位类型到模板换算函数的分发表，`ConvertToUnit()` 先转标准单位再转目标单位。换算规则由 `UtUnits` 和 `Ut*Value` 类型族提供，本目录只负责 UI 和分发。

### 50.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `UnitConverter::Plugin` | class | `UnitConverterPlugin.hpp:21` | WKF Unit Converter 插件壳。 |
| `UnitConverter::Dialog` | class | `UnitConverterDialog.hpp:27` | 单位换算 dialog。 |
| `UnitConverter::Dialog::SetupMaps` | method | `UnitConverterDialog.cpp:51` | 建立单位类型分发表。 |
| `UnitConverter::Dialog::UnitTypeChanged` | method | `UnitConverterDialog.cpp:114` | 重建目标单位列表。 |
| `UnitConverter::Dialog::ConvertToUnit` | method | `UnitConverterDialog.cpp:179` | 标准单位中转换算。 |

### 50.4 修正记录

batch12 将该目录明确为纯工具型 UI 插件。保留复核项：`UnitTypeChanged()` 检查当前单位却调用 `mRepopulateMap[aString]()`，可能隐式插入空 function；`Repopulate()` 删除 child 控件的生命周期语义需核对；空输入时未显式清空旧结果。

## 51. warlock/plugins/AdHocScriptBrowser/source

### 51.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 开发者插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/AdHocScriptBrowser/source` |
| source/header 数 | 4 |
| 源文件 | `AdHocScriptBrowserPlugin.hpp`、`AdHocScriptBrowserPlugin.cpp`、`AdHocScriptBrowserDockWidget.hpp`、`AdHocScriptBrowserDockWidget.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 51.2 职责说明

`AdHocScriptBrowser` 是 Warlock 开发者菜单到 AFSIM 脚本执行的入口。插件创建 dock 并挂到 `Developer` 菜单；`DockWidget::OnExecuteClicked()` 读取用户脚本文本，选择 global 或 platform context，检查平台控制权限，将脚本包装成 `void AdHocScript_N()` 后调用 `warlock::ScriptSimInterface::ExecuteScript()`。它不是仿真业务模型实现，但可以触发或改变仿真业务行为。

### 51.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkAdHocScriptBrowser::Plugin` | class | `AdHocScriptBrowserPlugin.hpp:21` | Warlock 插件壳。 |
| `WkAdHocScriptBrowser::Plugin::DialogActionTriggered` | method | `AdHocScriptBrowserPlugin.cpp:56` | Developer 菜单动作与 file-load lock 检查。 |
| `WkAdHocScriptBrowser::DockWidget` | class | `AdHocScriptBrowserDockWidget.hpp:24` | 临时脚本输入 dock。 |
| `WkAdHocScriptBrowser::DockWidget::OnExecuteClicked` | method | `AdHocScriptBrowserDockWidget.cpp:39` | 构造并执行 global/platform ad hoc script。 |
| `WkAdHocScriptBrowser::DockWidget::PlatformOfInterestChanged` | method | `AdHocScriptBrowserDockWidget.cpp:70` | 同步当前关注平台。 |

### 51.4 修正记录

batch12 将该目录标为“可触发业务行为的开发者入口”，而不是核心业务算法。保留复核项：临时脚本执行权限边界、global context 是否需要额外权限、platform radio 选中但无平台的行为、`-lock_fileload` 是否覆盖所有显示/执行路径。

## 52. warlock/plugins/Log/source

### 52.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 展示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Log/source` |
| source/header 数 | 4 |
| 源文件 | `LogPlugin.hpp`、`LogPlugin.cpp`、`LogSubscriber.hpp`、`LogSubscriber.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 52.2 职责说明

`Log` 是 Warlock 日志展示插件。插件初始化 developer preset 日志 subscriber、raw console subscriber 和 console widget；`GuiUpdate()` 周期处理两个 subscriber 的消息并调用 `ApplyChanges()` 刷新 UI。`MessageProcessor` 将普通日志入队到 `PluginBase::QueueMessage`，`ConsoleProcessor` 将 raw console 文本入队到 console queue。该目录是观察/展示型插件，不生成业务事件，不解释仿真语义，不改变仿真状态。

### 52.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkLog::Plugin` | class | `LogPlugin.hpp:19` | Warlock 日志显示插件。 |
| `WkLog::Plugin::GuiUpdate` | method | `LogPlugin.cpp:35` | 处理 subscriber 消息并刷新 UI。 |
| `WkLog::MessageProcessor` | class | `LogSubscriber.hpp:19` | 普通日志消息处理器。 |
| `WkLog::MessageProcessor::Process` | method | `LogSubscriber.cpp:19` | 普通日志入队。 |
| `WkLog::ConsoleProcessor` | class | `LogSubscriber.hpp:32` | raw console 消息处理器。 |
| `WkLog::ConsoleProcessor::Process` | method | `LogSubscriber.cpp:29` | raw console 文本入队。 |

### 52.4 修正记录

batch12 将该目录明确为观察/展示型 Warlock 插件。保留复核项较低：日志量较大时 `GuiUpdate()` 中 `ProcessMessages()` 与 `ApplyChanges()` 的刷新成本，以及 raw console 文本是否需要过滤或截断。

## 53. wizard/plugins/ACOImporter/source

### 53.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 工具插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/ACOImporter/source` |
| source/header 数 | 4 |
| 源文件 | `AcoImporterPlugin.hpp`、`AcoImporterPlugin.cpp`、`ImporterDialog.hpp`、`ImporterDialog.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 53.2 职责说明

`ACOImporter` 是 Wizard 侧 ACO/ATO 导入转换工具。插件在 `Tools > Importers` 下注册 `ACO Importer ...` 和 `ATO Importer ...`；`Dialog::ImportPushButtonClicked()` 收集文件/目录、注册 USMTF requirement、解析并校验 ACO/ATO 消息，输出 `<basename>_Export.txt` 和错误日志。它是工具侧导入入口，不是仿真运行时核心业务逻辑。

### 53.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `AcoImporter::Plugin` | class | `AcoImporterPlugin.hpp:22` | ACO/ATO importer 插件壳。 |
| `AcoImporter::Plugin::Plugin` | constructor | `AcoImporterPlugin.cpp:27` | 注册 Wizard importer 菜单。 |
| `AcoImporter::Dialog` | class | `ImporterDialog.hpp:29` | ACO/ATO 导入 dialog。 |
| `AcoImporter::Dialog::ImportPushButtonClicked` | method | `ImporterDialog.cpp:268` | 执行 USMTF 解析、校验和导出。 |
| `AcoImporter::Dialog::RegisterAcoRequirements` | method | `ImporterDialog.cpp:556` | 注册 ACO requirements。 |
| `AcoImporter::Dialog::RegisterAtoRequirements` | method | `ImporterDialog.cpp:602` | 注册 ATO requirements。 |

### 53.4 修正记录

batch13 将该目录定位为 Wizard 导入工具，而非 AFSIM runtime 入口。保留复核项：`UnregisterAcoRequirements()` 中 `GEOLINE` 疑似调用了 `RegisterEntity`；`DeleteSelectedEntries()` 只删第一个选中项；`HandleResults` 只声明未见实现；目录导入时转小写文件名可能影响大小写敏感文件系统。

## 54. wizard/plugins/ErrorList/source

### 54.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 诊断插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/ErrorList/source` |
| source/header 数 | 4 |
| 源文件 | `ErrorListPlugin.hpp`、`ErrorListPlugin.cpp`、`ErrorDock.hpp`、`ErrorDock.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 54.2 职责说明

`ErrorList` 是 Wizard 当前项目解析错误列表插件。插件创建底部 `ErrorDock`；dock 订阅项目打开/关闭和 `Project::ParseUpdatedFull`，从 `ParseResults::errors()` 收集错误范围，排序去重后刷新列表，双击条目调用 `Project::GotoRange` 跳转。它只展示解析诊断，不产生 parse error，也不参与仿真模型执行。

### 54.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `ErrorList::Plugin` | class | `ErrorListPlugin.hpp:19` | Error List 插件壳。 |
| `ErrorList::ErrorDock` | class | `ErrorDock.hpp:28` | 解析错误列表 dock。 |
| `ErrorList::ErrorDock::ProjectOpened` | method | `ErrorDock.cpp:38` | 订阅项目 parse update。 |
| `ErrorList::ErrorDock::ItemActivated` | method | `ErrorDock.cpp:52` | 跳转到错误范围。 |
| `ErrorList::ErrorDock::Update` | method | `ErrorDock.cpp:63` | 收集、排序、去重并刷新错误列表。 |

### 54.4 修正记录

batch13 将该目录明确为 Wizard 诊断 UI。保留复核项较低：`mModelPtr` 裸指针释放责任需确认；`ProjectClosed()` 未显式断开 `ParseUpdatedFull`，需结合项目对象生命周期确认安全性。

## 55. wizard/plugins/ScenarioImporter/source

### 55.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 导入工具） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/ScenarioImporter/source` |
| source/header 数 | 5 |
| 源文件 | `ScenarioImporterPlugin.hpp`、`ScenarioImporterPlugin.cpp`、`Input.hpp`、`Output.hpp`、`Types.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 55.2 职责说明

`ScenarioImporter` 是 Wizard 侧文本/CSV 场景导入生成工具。它不直接注册 WSF 场景命令，也不参与仿真运行循环；核心流程由 `scenarioImporterProcess()` 串联预处理、过滤、列解析、模板展开和预览/输出。`Input.hpp` 提供 token 切分、列类型校验和过滤器；`Output.hpp` 提供输出模板语法、条件、函数和记录写入。

### 55.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `ScenarioImporter::Plugin` | class | `ScenarioImporterPlugin.hpp:72` | Scenario Importer GUI 插件。 |
| `ScenarioImporter::Config` | struct | `ScenarioImporterPlugin.hpp:213` | 导入配置。 |
| `ScenarioImporter::Data` | struct | `ScenarioImporterPlugin.hpp:235` | 各阶段中间数据。 |
| `ScenarioImporter::Plugin::scenarioImporterProcess` | method | `ScenarioImporterPlugin.cpp:2158` | 导入流水线主流程。 |
| `ScenarioImporter::parserNextToken` | function | `Input.hpp:145` | 输入 token 切分。 |
| `ScenarioImporter::OutputTemplate` | class | `Output.hpp:215` | 输出模板解析/写入器。 |

### 55.4 修正记录

batch13 将该目录定位为 Wizard 生成/导入辅助工具。保留复核项：`contains` 搜索边界可能漏匹配等长/末尾文本；`OutputTemplate::evaluateConditional` 的 token-token 数值比较疑似使用错误字段；`processTemplate` 进度分支存在不可达条件；析构中 `QCoreApplication::quit()` 是否可能误关宿主应用。

## 56. wsf_plugins/wsf_annotation/source

### 56.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（AFSIM 插件模块） |
| 子系统 | `wsf_plugins/wsf_annotation` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_annotation/source` |
| source/header 数 | 5 |
| 源文件 | `WsfAnnotation.hpp`、`WsfAnnotation.cpp`、`WsfAnnotationDataTypes.hpp`、`WsfAnnotationEventPipe.hpp`、`WsfAnnotationEventPipe.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 56.2 职责说明

`wsf_annotation` 是 AFSIM 场景输入插件，负责解析 `visual_elements` 下的 `decoration`、`poi`、`range_ring` 配置，保存 annotation 数据，并在 simulation extension 启动时通过 event pipe 输出 `MsgAnnotationPoi`、`MsgAnnotationDecoration` 和 `MsgAnnotationRangeRing`。它属于可视化注释业务域的场景输入入口，不是平台运动、传感器或交战核心算法。

### 56.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WsfAnnotationInput` | class | `WsfAnnotation.hpp:24` | `visual_elements` 输入解析器。 |
| `WsfAnnotationExtension` | class | `WsfAnnotation.hpp:37` | Annotation 场景扩展。 |
| `Register_wsf_annotation` | function | `WsfAnnotation.cpp:83` | 注册 annotation feature 和 scenario extension。 |
| `ProcessAnnotationInput` | function | `WsfAnnotation.cpp:104` | 分派 annotation 子命令。 |
| `wsf::annotation::EventPipe` | class | `WsfAnnotationEventPipe.hpp:24` | annotation event pipe logger。 |
| `wsf::annotation::EventPipe::AddMessages` | method | `WsfAnnotationEventPipe.cpp:59` | 输出 POI、decoration、range ring 消息。 |

### 56.4 修正记录

batch13 将该目录标为 AFSIM 插件/场景输入入口，和 batch10 的 `ResultDataAnnotation`、batch11 的 `ResultZones` 构成“场景 annotation 配置 -> event pipe -> Mystic data extension/UI 消费”的链路。保留复核项：`range_ring` 名称去重只在读取 `entity` 时执行；`ValidateDouble` 文案和边界条件需核对；`AddMessages` 仅在 event pipe 有输出文件名时发送是否符合预期。

## 57. mystic/plugins/ResultAuxData/source

### 57.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果展示插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultAuxData/source` |
| source/header 数 | 6 |
| 源文件 | `RvPluginAuxData.hpp`、`RvPluginAuxData.cpp`、`RvAuxDataUpdater.hpp`、`RvAuxDataUpdater.cpp`、`RvAuxDataPlotUpdater.hpp`、`RvAuxDataPlotUpdater.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 57.2 职责说明

`ResultAuxData` 是 Mystic AuxData 结果展示插件。它从 `rvEnv.GetData()->GetDb()` 获取 `ResultDb`，按当前关注平台查 `ResultPlatform`，再用 `FindFirstBefore<rv::MsgAuxData>(simTime)` 获取当前 AuxData；`Updater::ReadData()` 按 datum 名读取 bool/int/real/text；`PlotUpdater` 枚举平台、扫描 numeric keys，并基于 `ResultPlatform::GetArray<rv::MsgAuxData>()` 生成绘图序列。它只消费结果数据，不产生仿真事件，不改变 ResultDb。

### 57.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvAuxData::Plugin` | class | `RvPluginAuxData.hpp:30` | Aux Data 结果显示插件。 |
| `RvAuxData::Plugin::GetRvPlatform` | method | `RvPluginAuxData.cpp:45` | 从 ResultDb 查找 ResultPlatform。 |
| `RvAuxData::Plugin::UpdateAuxData` | method | `RvPluginAuxData.cpp:123` | 读取当前时刻前最新 `MsgAuxData`。 |
| `RvAuxData::Updater::ReadData` | method | `RvAuxDataUpdater.cpp:39` | 读取单个 AuxData datum。 |
| `RvAuxData::PlotUpdater::GetSeries` | method | `RvAuxDataPlotUpdater.cpp:115` | 生成 AuxData plot points。 |

### 57.4 修正记录

batch14 将该目录定位为 AuxData 结果消费端。后续业务逻辑分析价值较低，应优先追 `MsgAuxData` 生产方。保留复核项：旧节点删除逻辑被注释，可能导致 UI stale data。

## 58. mystic/plugins/ResultInteractionPlots/source

### 58.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果展示插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultInteractionPlots/source` |
| source/header 数 | 6 |
| 源文件 | `RvPluginInteraction.hpp`、`RvPluginInteraction.cpp`、`WaterfallPlot.hpp`、`WaterfallPlot.cpp`、`WaterfallPlotDialog.hpp`、`WaterfallPlotDialog.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 58.2 职责说明

`ResultInteractionPlots` 是 Mystic InteractionDb waterfall plot 插件。平台右键创建 `WaterfallPlotDialog`，类型下拉映射到 `Detect`、`Track`、`LocalTrack`、`Jam` 等 paired interaction；`WaterfallPlot::CollectData()` 锁定 `InteractionDb`，调用 `GetRangeData(platform, -1, maxTime, valid)`，拼接 start/stop 区间并绘制当前时间线；`Export()` 可导出 CSV。它只做结果交互关系可视化，不计算探测、跟踪或干扰本身。

### 58.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvInteractionPlots::Plugin` | class | `RvPluginInteraction.hpp:20` | Interaction Plots 插件。 |
| `RvInteractionPlots::Plugin::BuildEntityContextMenu` | method | `RvPluginInteraction.cpp:28` | 平台右键添加 Waterfall Plot。 |
| `RvInteractionPlots::WaterfallPlotDialog` | class | `WaterfallPlotDialog.hpp:20` | Waterfall plot dialog。 |
| `RvInteractionPlots::WaterfallPlot` | class | `WaterfallPlot.hpp:20` | InteractionDb waterfall plot。 |
| `RvInteractionPlots::WaterfallPlot::SetType` | method | `WaterfallPlot.cpp:84` | UI 类型映射 InteractionDb 类型。 |
| `RvInteractionPlots::WaterfallPlot::CollectData` | method | `WaterfallPlot.cpp:229` | 读取 paired interaction ranges。 |

### 58.4 修正记录

batch14 将该目录定位为 InteractionDb 可视化消费端。后续业务逻辑分析价值中低：它揭示 Mystic 关注的交互类别，但真正业务链路应继续追 `InteractionDb::AddMessage` 和对应 event message 生产方。保留复核项：`CollectData()` 手工锁/解锁 `InteractionDb`，并手工拼接未闭合区间，展示正确性需专项验证。

## 59. mystic/plugins/ResultSatelliteTether/source

### 59.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果展示插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultSatelliteTether/source` |
| source/header 数 | 6 |
| 源文件 | `RvSatelliteTetherPlugin.hpp`、`RvSatelliteTetherPlugin.cpp`、`RvSatelliteTetherDockWidget.hpp`、`RvSatelliteTetherDockWidget.cpp`、`RvSatelliteTetherAttachmentTrace.hpp`、`RvSatelliteTetherAttachmentTrace.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 59.2 职责说明

`ResultSatelliteTether` 是空间平台 tether 可视化插件。它只对 space platform 添加 tether 右键菜单；时间推进时更新 dock 中 tracked platforms。`DockWidget::Update()` 从 `ResultDb` 查平台、读取 `MsgOrbitalElements` 并通过 VA scenario 更新展示颜色；`AttachmentTrace::UpdateDataRange()` 读取两平台 `MsgEntityState` 序列，计算 RIC 相对坐标并写入 OSG vertex/color arrays。它是结果可视化消费端，不生成仿真事件，也不改变任务/传感器/航迹状态。

### 59.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvSatelliteTether::Plugin` | class | `RvSatelliteTetherPlugin.hpp:27` | Satellite Tether 插件。 |
| `RvSatelliteTether::Plugin::BuildEntityContextMenu` | method | `RvSatelliteTetherPlugin.cpp:43` | space platform 右键菜单。 |
| `RvSatelliteTether::DockWidget::Update` | method | `RvSatelliteTetherDockWidget.cpp:47` | 读取 orbital elements 并更新 trace。 |
| `RvSatelliteTether::AttachmentTrace` | class | `RvSatelliteTetherAttachmentTrace.hpp:20` | RIC 相对轨迹 attachment。 |
| `RvSatelliteTether::AttachmentTrace::UpdateDataRange` | method | `RvSatelliteTetherAttachmentTrace.cpp:133` | 计算两平台相对轨迹。 |

### 59.4 修正记录

batch14 将该目录定位为空间结果可视化消费端。后续业务逻辑分析价值低到中，适合连接 `ResultDataSpace` 的轨道元素消费链。保留复核项：`mWidgetNamer` 构造初始化需确认；`DockWidget::Update()` 对 `FindPlatformByName` 返回值直接解引用；`AttachmentTrace::UpdateData()` 对 `rvEnv.GetData()` 存在先解引用再判空路径。

## 60. mystic/plugins/ResultTracks/source

### 60.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果展示插件） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultTracks/source` |
| source/header 数 | 6 |
| 源文件 | `TracksPlugin.hpp`、`TracksPlugin.cpp`、`PlotUpdater.hpp`、`PlotUpdater.cpp`、`PlottingWidget.hpp`、`PlottingWidget.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 60.2 职责说明

`ResultTracks` 是 Mystic 航迹结果可视化和追踪解释插件。`DataUpdate()` 锁定 `TrackDb`，按 POI/可见性策略更新平台数据树和 VA track；`UpdateTracks()` 从 `TrackDb::SourceTracks` 读取本地航迹；`UpdateTrack()` 将 `MsgLocalTrackUpdate::track()` 映射为 `wkf::Track` 的位置、速度、side/type/icon/domain；`TraceTrack()` 调用 `ResultDb::TraceTrackId` 追溯传感器创建、本地创建、相关/去相关、任务、武器事件。它不是仿真运行时决策入口，但属于结果业务语义入口，适合后续追踪航迹生命周期。

### 60.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvTracks::Plugin` | class | `TracksPlugin.hpp:50` | Tracks 结果显示插件。 |
| `RvTracks::Plugin::DataUpdate` | method | `TracksPlugin.cpp:368` | 锁 TrackDb 并更新 VA track。 |
| `RvTracks::Plugin::UpdateTrack` | method | `TracksPlugin.cpp:530` | 将本地航迹映射到 `wkf::Track`。 |
| `RvTracks::Plugin::TraceTrack` | method | `TracksPlugin.cpp:633` | 调用 `TraceTrackId` 追踪事件链。 |
| `RvTracks::PlotUpdater::CollectContributorData` | method | `PlotUpdater.cpp:466` | 收集 contributor data。 |
| `RvTracks::PlottingWidget::BuildPlotsFromUpdater` | method | `PlottingWidget.cpp:118` | 渲染 track/truth/contributor plots。 |

### 60.4 修正记录

batch14 将该目录标为高价值结果业务语义入口。后续建议沿 `RvResultDb::TraceTrackId`、`RvTrackDb` ingestion、`MsgLocalTrack*`/`MsgSensorTrack*` 生成路径继续追。保留复核项：`PlotUpdater::CollectContributorData()` 调 `TraceTrackId` 后未删除 `eventList` 中的指针，而 `ResultDb` 注释说明 caller 负责清理；多处手动 `LockTrackDb`/`UnlockTrackDb` 需审查异常和早退安全性。

## 61. tools/wkf/plugins/Performance/source

### 61.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF 开发者工具） |
| 子系统 | `tools/wkf` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/Performance/source` |
| source/header 数 | 6 |
| 源文件 | `PerformancePlugin.hpp`、`PerformancePlugin.cpp`、`PerformanceDialog.hpp`、`PerformanceDialog.cpp`、`UtQtMemoryUsage.hpp`、`UtQtMemoryUsage.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 61.2 职责说明

`Performance` 是 WKF Performance Analyzer 开发者诊断插件。`Performance::Plugin` 通过 `WKF_PLUGIN_DEFINE_SYMBOLS` 注册，并在 Developer 菜单添加 Performance Analyzer 动作；`Performance::Dialog::Build()` 构造内存曲线 UI，`Dialog::Update()` 周期刷新；`UtQtMemoryUsage::Update()` 读取当前进程内存。它只观察工具进程资源占用，不读取仿真业务对象，也不改变仿真状态。

### 61.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `Performance::Plugin` | class | `PerformancePlugin.hpp:19` | WKF Performance 插件入口。 |
| `Performance::Plugin::GuiUpdate` | method | `PerformancePlugin.cpp:42` | 驱动性能对话框刷新。 |
| `Performance::Dialog` | class | `PerformanceDialog.hpp:23` | Performance Analyzer 对话框。 |
| `Performance::Dialog::Build` | method | `PerformanceDialog.cpp:31` | 构建内存曲线 UI。 |
| `UtQtMemoryUsage` | class | `UtQtMemoryUsage.hpp:20` | 当前进程内存统计辅助类。 |

### 61.4 修正记录

batch15 将该目录定位为开发者诊断工具，后续业务逻辑分析价值低，不应作为 AFSIM 业务入口。

## 62. warlock/plugins/AcesDisplay/source

### 62.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/AcesDisplay/source` |
| source/header 数 | 6 |
| 源文件 | `AcesDisplayPlugin.hpp`、`AcesDisplayPlugin.cpp`、`AcesDisplaySimInterface.hpp`、`AcesDisplaySimInterface.cpp`、`AcesDisplayEvents.hpp`、`AcesDisplayEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 62.2 职责说明

`AcesDisplay` 是 Warlock ACES 显示适配插件。`WkAcesDisplay::Plugin` 注册插件并维护 display 实例；`SimInterface::WallClockRead()` 从 `WsfSimulation` 周期读取数据；`PlatformAdded()`、`PopulateEntityPerception()`、`PopulateEngagementData()` 把平台、感知、交战和 SA 信息映射到 `wkf::AcesDisplay::DataContainer`。它不实现空战规则，但保留 ACES/SA 业务语义的显示侧证据。

### 62.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkAcesDisplay::Plugin` | class | `AcesDisplayPlugin.hpp:21` | ACES Display Warlock 插件入口。 |
| `WkAcesDisplay::Plugin::GuiUpdate` | method | `AcesDisplayPlugin.cpp:81` | 处理 ACES display GUI 刷新。 |
| `WkAcesDisplay::Plugin::NewDisplay` | method | `AcesDisplayPlugin.cpp:98` | 创建 ACES display 实例。 |
| `WkAcesDisplay::SimInterface` | class | `AcesDisplaySimInterface.hpp:29` | ACES 数据读取接口。 |
| `WkAcesDisplay::SimInterface::PopulateEntityPerception` | method | `AcesDisplaySimInterface.cpp:534` | 填充实体感知信息。 |
| `WkAcesDisplay::SimInterface::PopulateEngagementData` | method | `AcesDisplaySimInterface.cpp:583` | 填充交战数据。 |

### 62.4 修正记录

batch15 将该目录标为中高价值显示观察入口。后续业务逻辑分析应向上追 `WsfSA_Processor`、`WsfSA_Assess`、`WsfTrackManager` 和 `wsf_air_combat`，本目录只作为消费侧证据。

## 63. warlock/plugins/AirCombatVisualization/source

### 63.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/AirCombatVisualization/source` |
| source/header 数 | 6 |
| 源文件 | `AirCombatVisualizationPlugin.hpp`、`AirCombatVisualizationPlugin.cpp`、`AirCombatVisualizationSimInterface.hpp`、`AirCombatVisualizationSimInterface.cpp`、`AirCombatVisualizationSimEvents.hpp`、`AirCombatVisualizationSimEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 63.2 职责说明

`AirCombatVisualization` 是 Warlock 空战可视化插件。`WkAirCombat::Plugin` 构建 viewer 上下文菜单和偏好页；`SimInterface::WallClockRead()` 调用 `PopulateData()`，从平台、SA processor、assess 和 weapon engagement 状态生成 display data；平台增删和仿真结束通过 `AirCombatSimEvent` 派发到 GUI。它是空战语义的显示入口，不是决策算法源头。

### 63.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkAirCombat::Plugin` | class | `AirCombatVisualizationPlugin.hpp:26` | 空战可视化插件入口。 |
| `WkAirCombat::Plugin::BuildViewerContextMenu` | method | `AirCombatVisualizationPlugin.cpp:121` | 创建 viewer 菜单入口。 |
| `WkAirCombat::Plugin::GuiUpdate` | method | `AirCombatVisualizationPlugin.cpp:183` | 处理显示事件。 |
| `WkAirCombat::SimInterface` | class | `AirCombatVisualizationSimInterface.hpp:20` | 空战显示仿真接口。 |
| `WkAirCombat::SimInterface::PopulateData` | method | `AirCombatVisualizationSimInterface.cpp:159` | 填充空战显示数据。 |
| `WkAirCombat::UpdateEvent` | class | `AirCombatVisualizationSimEvents.hpp:31` | 空战显示数据刷新事件。 |

### 63.4 修正记录

batch15 将该目录标为中高价值显示观察入口。保留复核项：`try_lock` 跳过可能导致显示缺帧，target 去重和 `BuildViewerContextMenu()` 对 viewer/context 对象的非空假设需后续验证。

## 64. warlock/plugins/Annotation/source

### 64.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Annotation/source` |
| source/header 数 | 6 |
| 源文件 | `AnnotationPlugin.hpp`、`AnnotationPlugin.cpp`、`AnnotationSimInterface.hpp`、`AnnotationSimInterface.cpp`、`AnnotationSimEvents.hpp`、`AnnotationSimEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 64.2 职责说明

`Annotation` 是 Warlock 场景标注显示桥。`SimInterface::SimulationStarting()` 从 `WsfAnnotationExtension::GetAnnotationInfo()` 读取 annotation 信息；`SimStartingEvent::Process()` 创建 POI、bullseye、decorations 和 range rings，并处理暂时缺失 entity 的 deferred attachment。它消费场景标注，不影响仿真运行时决策。

### 64.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkAnnotation::Plugin` | class | `AnnotationPlugin.hpp:21` | Annotation Warlock 插件入口。 |
| `WkAnnotation::Plugin::GuiUpdate` | method | `AnnotationPlugin.cpp:27` | 处理 annotation 显示事件。 |
| `WkAnnotation::SimInterface` | class | `AnnotationSimInterface.hpp:22` | annotation 仿真接口。 |
| `WkAnnotation::SimInterface::SimulationStarting` | method | `AnnotationSimInterface.cpp:25` | 仿真开始时读取 annotation extension。 |
| `WkAnnotation::SimStartingEvent` | class | `AnnotationSimEvents.hpp:22` | annotation 初始化显示事件。 |
| `WkAnnotation::GetRangeRingProperties` | function | `AnnotationSimEvents.cpp:27` | 构造 range ring 显示属性。 |

### 64.4 修正记录

batch15 将该目录定位为 annotation 显示消费端，可与 batch13 的 `wsf_annotation` 生产链串联。业务逻辑分析价值中等，主要用于确认场景文本标注最终如何在 Warlock 中显示。

## 65. warlock/plugins/ApplicationLauncher/source

### 65.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 工具插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/ApplicationLauncher/source` |
| source/header 数 | 6 |
| 源文件 | `ApplicationLauncherPlugin.hpp`、`ApplicationLauncherPlugin.cpp`、`ApplicationLauncherToolbar.hpp`、`ApplicationLauncherToolbar.cpp`、`ApplicationLauncherSimInterface.hpp`、`ApplicationLauncherSimInterface.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 65.2 职责说明

`ApplicationLauncher` 是 Warlock 外部应用启动工具。`Toolbar::HandleWizardAction()` 和 `HandleMysticAction()` 根据当前 scenario、config 和 event pipe output file 组装参数，`StartApplication()` 启动 Wizard 或 Mystic；`SimInterface::SimulationInitializing()` 捕获当前 event pipe output 文件。它只协调工具链，不承载 AFSIM 业务规则。

### 65.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkApplicationLauncher::Plugin` | class | `ApplicationLauncherPlugin.hpp:20` | Application Launcher 插件入口。 |
| `WkApplicationLauncher::Toolbar` | class | `ApplicationLauncherToolbar.hpp:26` | Wizard/Mystic 启动工具条。 |
| `WkApplicationLauncher::Toolbar::HandleWizardAction` | method | `ApplicationLauncherToolbar.cpp:42` | 启动 Wizard。 |
| `WkApplicationLauncher::Toolbar::HandleMysticAction` | method | `ApplicationLauncherToolbar.cpp:60` | 启动 Mystic。 |
| `WkApplicationLauncher::Toolbar::StartApplication` | method | `ApplicationLauncherToolbar.cpp:85` | 创建外部进程。 |
| `WkApplicationLauncher::SimInterface::SimulationInitializing` | method | `ApplicationLauncherSimInterface.cpp:22` | 捕获 event pipe output 路径。 |

### 65.4 修正记录

batch15 将该目录定位为工具流程入口。后续业务逻辑分析价值低，但对“Warlock 如何把当前运行上下文交给 Mystic/Wizard”有流程说明价值。

## 66. warlock/plugins/CommVis/source

### 66.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/CommVis/source` |
| source/header 数 | 6 |
| 源文件 | `CommVisPlugin.hpp`、`CommVisPlugin.cpp`、`CommVisSimInterface.hpp`、`CommVisSimInterface.cpp`、`CommVisSimEvents.hpp`、`CommVisSimEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 66.2 职责说明

`CommVis` 是 Warlock 通信可视化桥。`SimInterface::SimulationInitializing()` 构建初始网络和通信对象，`AddNetworks()`、`AddComms()`、`RemoveComm()`、`TurnOnComm()`、`TurnOffComm()`、`MessageTransmitted()` 和 `MessageHop()` 把通信运行时事件转换成 `CommVisEvent`；GUI 侧事件再更新 `wkf::CommVisDisplay`。它不实现通信规则，但集中暴露通信网络、节点和消息路径的观察点。

### 66.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkCommVis::Plugin` | class | `CommVisPlugin.hpp:23` | CommVis Warlock 插件入口。 |
| `WkCommVis::Plugin::GuiUpdate` | method | `CommVisPlugin.cpp:54` | 处理通信可视化事件。 |
| `WkCommVis::SimInterface` | class | `CommVisSimInterface.hpp:25` | 通信事件到显示的桥接接口。 |
| `WkCommVis::SimInterface::AddComms` | method | `CommVisSimInterface.cpp:158` | 添加通信对象。 |
| `WkCommVis::SimInterface::MessageTransmitted` | method | `CommVisSimInterface.cpp:325` | 处理消息发送事件。 |
| `WkCommVis::SimInterface::MessageHop` | method | `CommVisSimInterface.cpp:384` | 处理消息跳转事件。 |

### 66.4 修正记录

batch15 将该目录标为中高价值通信观察入口。后续业务逻辑分析应向上追通信核心模型、message routing 和 event source；本目录只作为显示消费侧证据。

## 67. warlock/plugins/EventMarker/source

### 67.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/EventMarker/source` |
| source/header 数 | 6 |
| 源文件 | `EventMarkerPlugin.hpp`、`EventMarkerPlugin.cpp`、`EventMarkerSimInterface.hpp`、`EventMarkerSimInterface.cpp`、`EventMarkerSimEvents.hpp`、`EventMarkerSimEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 67.2 职责说明

`EventMarker` 是 Warlock 事件标记显示插件。`SimInterface::SimulationInitializing()` 订阅 `WsfObserver::PlatformBroken`、`PlatformDeleted` 和 `WeaponTerminated`，把平台损坏/删除、武器命中/脱靶等事件包装为 `PlatformMarkerEvent` 或 `WeaponMarkerEvent`；事件处理侧创建 `wkf::PlatformEventMarker` 或 `wkf::WeaponEventMarker` 并交给 `wkf::EventMarkerDisplayInterface`。它只负责可视化，不决定平台生命周期或武器效果。

### 67.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkEventMarker::Plugin` | class | `EventMarkerPlugin.hpp:20` | Event Marker 插件入口。 |
| `WkEventMarker::Plugin::GuiUpdate` | method | `EventMarkerPlugin.cpp:37` | 处理事件标记 GUI 更新。 |
| `WkEventMarker::SimInterface` | class | `EventMarkerSimInterface.hpp:20` | 事件标记仿真接口。 |
| `WkEventMarker::SimInterface::SimulationInitializing` | method | `EventMarkerSimInterface.cpp:36` | 注册平台和武器 observer 回调。 |
| `WkEventMarker::PlatformMarkerEvent` | class | `EventMarkerSimEvents.hpp:51` | 平台事件 marker。 |
| `WkEventMarker::WeaponMarkerEvent` | class | `EventMarkerSimEvents.hpp:62` | 武器事件 marker。 |

### 67.4 修正记录

batch16 将该目录定位为事件可视化消费侧。后续业务逻辑分析价值中等，应向上追 `WsfPlatform` 生命周期、`WsfWeaponEngagement::GetGeometryResult()` 和命中/脱靶枚举。

## 68. warlock/plugins/HeadDownView/source

### 68.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/HeadDownView/source` |
| source/header 数 | 6 |
| 源文件 | `HDD_Plugin.hpp`、`HDD_Plugin.cpp`、`HDD_SimInterface.hpp`、`HDD_SimInterface.cpp`、`HDD_SimEvents.hpp`、`HDD_SimEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 68.2 职责说明

`HeadDownView` 是 Warlock HDD 玻璃座舱视图插件。UI 侧创建 HDD dockable 窗口和偏好页；`HDD::SimInterface::WallClockRead()` 从 `WsfSimulation`、`WsfPlatform`、`WsfSA_Processor` 读取平台、燃油、导航、飞控、武器、航迹和感知资产数据；`HDD::Plugin::Update()` 将数据写入 HDD 页面 setter。它不是仿真规则入口，但高度集中地暴露 SA/air-combat 状态字段如何被座舱 UI 消费。

### 68.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `HDD::Plugin` | class | `HDD_Plugin.hpp:25` | Head Down View 插件入口。 |
| `HDD::Plugin::ConnectToPlatform` | method | `HDD_Plugin.cpp:67` | 创建并连接 HDD dockable 窗口。 |
| `HDD::Plugin::RequestPlatformResourceInstance` | method | `HDD_Plugin.cpp:169` | 响应跨插件平台资源请求。 |
| `HDD::Plugin::Update` | method | `HDD_Plugin.cpp:179` | 更新 HDD 页面数据。 |
| `HDD::SimInterface` | class | `HDD_SimInterface.hpp:30` | HDD 数据采集接口。 |
| `HDD::SimInterface::WallClockRead` | method | `HDD_SimInterface.cpp:108` | 读取 SA processor 输出。 |

### 68.4 修正记录

batch16 将该目录标为高价值消费侧入口。后续应向上追 `WsfSA_Processor`、`WsfSA_Perceive`、`WsfTrackManager`、`WsfPlatform`，并向下追 `hdd/WkfHDD_DataContainer.hpp` 和 HDD 页面 setter。

## 69. warlock/plugins/HeadUpView/source

### 69.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/HeadUpView/source` |
| source/header 数 | 6 |
| 源文件 | `HUD_Plugin.hpp`、`HUD_Plugin.cpp`、`HUD_SimInterface.hpp`、`HUD_SimInterface.cpp`、`HUD_SimEvents.hpp`、`HUD_SimEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 69.2 职责说明

`HeadUpView` 是 Warlock HUD 抬头显示插件。`BuildEntityContextMenu()` 只对存在 SA processor 的平台添加 HUD 菜单；`ConnectToPlatform()` 创建 `wkf::HUD_DockWidget`；`SimInterface::ReadPlatformData()` 从 `WsfSA_Processor` 读取 flight/control/nav/fuel/weapon summary 并通过 `UpdateEvent` 更新 HUD 数据容器。它用于显示派生字段，不负责平台行为或武器决策。

### 69.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `HeadsUpDisplay::Plugin` | class | `HUD_Plugin.hpp:28` | Head Up View 插件入口。 |
| `HeadsUpDisplay::Plugin::BuildEntityContextMenu` | method | `HUD_Plugin.cpp:53` | 为有 SA processor 的平台添加 HUD 菜单。 |
| `HeadsUpDisplay::Plugin::ConnectToPlatform` | method | `HUD_Plugin.cpp:78` | 创建 HUD dock widget。 |
| `HeadsUpDisplay::Plugin::GuiUpdate` | method | `HUD_Plugin.cpp:143` | 处理 HUD 事件并刷新。 |
| `HeadsUpDisplay::SimInterface` | class | `HUD_SimInterface.hpp:26` | HUD 数据采集接口。 |
| `HeadsUpDisplay::SimInterface::ReadPlatformData` | method | `HUD_SimInterface.cpp:171` | 读取平台 HUD 数据。 |

### 69.4 修正记录

batch16 将该目录标为中等价值消费端。后续业务逻辑分析应向上追 `WsfSA_Processor::GetAircraftKinematics()`、`GetFlightControlsDataSummary()`、`GetNavigationDataSummary()`、`GetFuelSystemData()`、`GetWeaponsDataSummary()`。

## 70. warlock/plugins/Interactions/source

### 70.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Interactions/source` |
| source/header 数 | 6 |
| 源文件 | `InteractionsPlugin.hpp`、`InteractionsPlugin.cpp`、`InteractionsSimInterface.hpp`、`InteractionsSimInterface.cpp`、`InteractionsSimEvents.hpp`、`InteractionsSimEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 70.2 职责说明

`Interactions` 是 Warlock 跨域 interaction 可视化插件。插件注册 jamming、track、message、task、detection、weapon、kill、cyber 等显示类型；`SimInterface::SimulationInitializing()` 注册大量 `WsfObserver` 回调，生成 `InteractionEvent`；事件处理侧查找 source/target platform 并创建或更新 `wkf::AttachmentInteraction`。它不是业务规则源头，但集中暴露 AFSIM 哪些跨域事件被可视化。

### 70.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkInteractions::Plugin` | class | `InteractionsPlugin.hpp:20` | Interactions 插件入口。 |
| `WkInteractions::Plugin::GuiUpdate` | method | `InteractionsPlugin.cpp:46` | 处理 interaction 显示事件。 |
| `WkInteractions::SimInterface` | class | `InteractionsSimInterface.hpp:27` | interaction 事件采集接口。 |
| `WkInteractions::SimInterface::SimulationInitializing` | method | `InteractionsSimInterface.cpp:62` | 注册跨域 observer 回调。 |
| `WkInteractions::SimInterface::MessageId` | class | `InteractionsSimInterface.hpp:45` | message hop 跟踪 key。 |
| `WkInteractions::InteractionEvent::Process` | method | `InteractionsSimEvents.cpp:22` | 创建或更新交互线 attachment。 |

### 70.4 修正记录

batch16 将该目录标为高价值跨域事件消费入口。后续应向上追 `WsfObserver` 事件源、`WsfWeaponEngagement`、`WsfTask`、`WsfSensorResult`、`WsfMessage`、`wsf::cyber::Engagement`。

## 71. warlock/plugins/PlatformHistory/source

### 71.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/PlatformHistory/source` |
| source/header 数 | 6 |
| 源文件 | `PlatformHistoryPlugin.hpp`、`PlatformHistoryPlugin.cpp`、`PlatformHistorySimInterface.hpp`、`PlatformHistorySimInterface.cpp`、`PlatformHistorySimEvents.hpp`、`PlatformHistorySimEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 71.2 职责说明

`PlatformHistory` 是 Warlock 平台历史可视化插件。`SimInterface::SimulationInitializing()` 订阅 sensor detection、track initiated/dropped、weapon fired/terminated、platform deleted；`DetectedEvent`、`TrackedEvent`、`AttackedEvent` 更新 trace line 状态；`TracelineData::Update()` 追加 ECEF 点；`WingRibbonData::Update()` 采样翼尖、姿态、速度、高度和 team color 并追加 ribbon 点。它观察 detection/track/attack 生命周期，不实现传感器、航迹或武器规则。

### 71.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkPlatformHistory::Plugin` | class | `PlatformHistoryPlugin.hpp:45` | Platform History 插件入口。 |
| `WkPlatformHistory::Plugin::TraceLineStateData` | struct | `PlatformHistoryPlugin.hpp:103` | trace line 状态数据。 |
| `WkPlatformHistory::Plugin::TracelineData` | struct | `PlatformHistoryPlugin.hpp:112` | trace line 几何和状态缓存。 |
| `WkPlatformHistory::Plugin::WingRibbonData` | struct | `PlatformHistoryPlugin.hpp:157` | wing ribbon 几何和状态缓存。 |
| `WkPlatformHistory::Plugin::GuiUpdate` | method | `PlatformHistoryPlugin.cpp:151` | 刷新 trace line 和 wing ribbon。 |
| `WkPlatformHistory::SimInterface::SimulationInitializing` | method | `PlatformHistorySimInterface.cpp:25` | 订阅 detection/track/weapon 事件。 |

### 71.4 修正记录

batch16 将该目录标为中等价值生命周期显示入口。后续业务逻辑分析应向上追 `WsfObserver::SensorDetectionChanged`、`SensorTrackInitiated`、`SensorTrackDropped`、`WeaponFired`、`WeaponTerminated`。

## 72. warlock/plugins/SituationAwarenessDisplay/source

### 72.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/SituationAwarenessDisplay/source` |
| source/header 数 | 6 |
| 源文件 | `SA_DisplayPlugin.hpp`、`SA_DisplayPlugin.cpp`、`SA_DisplaySimInterface.hpp`、`SA_DisplaySimInterface.cpp`、`SA_DisplayEvents.hpp`、`SA_DisplayEvents.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 72.2 职责说明

`SituationAwarenessDisplay` 是 Warlock SA 显示插件。`Plugin::NewDisplay()` 启用仿真接口并添加关注平台；`SimInterface::WallClockRead()` 读取 truth、SA kinematics、fuel、nav、weapons、tracks、perceptions 和 groups；`PopulateEntityPerception()` 将 `WsfSA_EntityPerception` 映射为显示容器。它不是 SA 计算源，但集中暴露 `WsfSA_Processor`、`WsfSA_Perceive`、`WsfSA_Assess` 输出结构。

### 72.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkSA_Display::Plugin` | class | `SA_DisplayPlugin.hpp:21` | Situation Awareness Display 插件入口。 |
| `WkSA_Display::Plugin::NewDisplay` | method | `SA_DisplayPlugin.cpp:44` | 创建 SA display 并关注平台。 |
| `WkSA_Display::SimInterface` | class | `SA_DisplaySimInterface.hpp:27` | SA display 仿真接口。 |
| `WkSA_Display::SimInterface::WallClockRead` | method | `SA_DisplaySimInterface.cpp:30` | 读取 SA 数据主入口。 |
| `WkSA_Display::SimInterface::PopulateEntityPerception` | method | `SA_DisplaySimInterface.cpp:475` | 映射实体感知数据。 |
| `WkSA_Display::UpdateSA_DataEvent` | class | `SA_DisplayEvents.hpp:43` | SA 数据更新事件。 |

### 72.4 修正记录

batch16 将该目录标为高价值 SA 输出消费端。后续应向上追 `WsfSA_Processor`、`WsfSA_Perceive::PerceivedAssets/Bogies/Bandits`、`WsfSA_Assess::GetPrioritizedThreatEntities/GetPrioritizedTargetEntities/PerceivedGroups` 和 `WsfSA_Group`。

## 73. warlock/plugins/VisualEffects/source

### 73.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 运行时显示插件） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/VisualEffects/source` |
| source/header 数 | 6 |
| 源文件 | `VisualEffectsPlugin.hpp`、`VisualEffectsPlugin.cpp`、`VisualEffectsSimInterface.hpp`、`VisualEffectsSimInterface.cpp`、`VisualEffectsSimEvents.hpp`、`VisualEffectsSimEvents.cpp` |
| 证据 | CodeGraph node + 源码行号 |

### 73.2 职责说明

`VisualEffects` 是 Warlock 粒子/视觉效果桥。`SimInterface::SimulationInitializing()` 订阅平台 appearance 变化、weapon termination、simulation pause/resume；根据 `DisEntityAppearance` 的 trailing/smoke/fire/afterburner/powerplant 字段生成 smoke、fire、afterburner、engine、explosion 等 `VisualEffectsSimEvent`；GUI 侧 `Plugin::GuiUpdate()` 先清理旧 effect，再把事件交给 `wkf::VisualEffectsDisplayInterface`。它消费运行时状态，不实现 appearance 或 weapon 规则。

### 73.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkVisualEffects::Plugin` | class | `VisualEffectsPlugin.hpp:24` | Visual Effects 插件入口。 |
| `WkVisualEffects::Plugin::GuiUpdate` | method | `VisualEffectsPlugin.cpp:40` | 清理旧 effect 并处理新事件。 |
| `WkVisualEffects::SimInterface` | class | `VisualEffectsSimInterface.hpp:24` | visual effects 仿真接口。 |
| `WkVisualEffects::SimInterface::SimulationInitializing` | method | `VisualEffectsSimInterface.cpp:36` | 注册 appearance/weapon/pause observer。 |
| `WkVisualEffects::EffectInfo` | struct | `VisualEffectsSimEvents.hpp:35` | effect 位置和源平台信息。 |
| `EffectEvent<EFFECT_TYPE>` | class | `VisualEffectsSimEvents.hpp:49` | 模板 effect 创建事件。 |

### 73.4 修正记录

batch17 将该目录定位为中等价值显示消费侧。后续可向上追 `WsfObserver::PlatformAppearanceChanged`、`WsfWeaponEngagement::GetGeometryResult()` 和 `DisEntityAppearance` 字段含义。

## 74. wizard/plugins/ColorUtils/source

### 74.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 编辑器插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/ColorUtils/source` |
| source/header 数 | 6 |
| 源文件 | `ColorUtilPlugin.hpp`、`ColorUtilPlugin.cpp`、`ColorUtils.hpp`、`ColorUtils.cpp`、`ColorTips.hpp`、`ColorTips.cpp` |
| 证据 | CodeGraph 未覆盖，回退文本证据 + 源码行号 |

### 74.2 职责说明

`ColorUtils` 是 Wizard 文本编辑器颜色辅助插件。插件监听 active editor、context menu 和 tooltip 事件；当用户在 `Color.Construct` 上右键时打开 `QColorDialog` 并替换源码范围；`ColorTips` 根据 parse results 识别脚本颜色或 platform side，显示颜色小块提示。它提升场景脚本编辑体验，不改变仿真模型。

### 74.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `ColorUtils::Plugin` | class | `ColorUtilPlugin.hpp:24` | Color Utils 插件入口。 |
| `ColorUtils::Plugin::ColorConstruct` | method | `ColorUtilPlugin.cpp:44` | 打开颜色对话框并写回 `Color.Construct`。 |
| `ColorUtils::Plugin::EditorContextMenu` | method | `ColorUtilPlugin.cpp:87` | 在 editor 右键菜单添加颜色选择动作。 |
| `ColorUtils::IdentifierAtPosition` | function | `ColorUtils.cpp:28` | 查找 editor 光标处标识符。 |
| `ColorUtils::IsValidColor` | function | `ColorUtils.cpp:131` | 验证十六进制或 RGB/RGBA 颜色字符串。 |
| `wizard::ColorTips::SetSideColor` | method | `ColorTips.cpp:291` | 根据 platform side 显示 team color。 |

### 74.4 修正记录

batch17 将该目录定位为低到中价值编辑器工具，不作为 AFSIM 业务入口。保留复核项：`ColorConstruct()` 行内下标、`mColorTipsPtr` 生命周期和 `UpdateScenario()` 重复连接。

## 75. wizard/plugins/DemoBrowser/source

### 75.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 启动/帮助插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/DemoBrowser/source` |
| source/header 数 | 6 |
| 源文件 | `DemoBrowserPlugin.hpp`、`DemoBrowserPlugin.cpp`、`DemoBrowserDialog.hpp`、`DemoBrowserDialog.cpp`、`CollapsibleGroup.hpp`、`CollapsibleGroup.cpp` |
| 证据 | CodeGraph node + 回退文本证据 + 源码行号 |

### 75.2 职责说明

`DemoBrowser` 是 Wizard demo、scenario、training 浏览和启动插件。插件在 Help 菜单和 startup dialog 添加 Demo Browser；`DemoBrowserDialog::PopulatePages()` 扫描 demo search paths 中的 `*.rst`；`Item` 解析 rst replacement 属性，生成 documentation/open project/copy project URL；搜索可按属性或 `*.txt` 文件内容匹配。它属于工具入口，默认不把 demo/training 内容纳入核心架构结论。

### 75.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `DemoBrowser::Plugin` | class | `DemoBrowserPlugin.hpp:19` | Demo Browser 插件入口。 |
| `DemoBrowser::Plugin::GetStartupWidgets` | method | `DemoBrowserPlugin.cpp:35` | 在 startup dialog 添加按钮。 |
| `DemoBrowser::Plugin::Show` | method | `DemoBrowserPlugin.cpp:47` | 创建并显示 Demo Browser dialog。 |
| `DemoBrowser::DemoBrowserDialog` | class | `DemoBrowserDialog.hpp:56` | demo/scenario/training 浏览对话框。 |
| `DemoBrowser::DemoBrowserDialog::PopulatePages` | method | `DemoBrowserDialog.cpp:143` | 扫描 demo search paths。 |
| `DemoBrowser::Item::Matches` | method | `DemoBrowserDialog.cpp:386` | 按属性或文件内容搜索。 |

### 75.4 修正记录

batch17 将该目录定位为工具和样例浏览入口。它可辅助查找示例项目，但 demo/training 内容仍遵守 Phase 1 边界，不进入核心架构结论。

## 76. wizard/plugins/LogServer/source

### 76.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 日志插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/LogServer/source` |
| source/header 数 | 6 |
| 源文件 | `LogServer.hpp`、`LogServer.cpp`、`LogServerThread.hpp`、`LogServerThread.cpp`、`LogServerPrefWidget.hpp`、`LogServerPrefWidget.cpp` |
| 证据 | CodeGraph node + 回退文本证据 + 源码行号 |

### 76.2 职责说明

`LogServer` 是 Wizard 仿真日志 TCP 聚合插件。`LogServer::Plugin` 继承 `wkf::log::PluginBase`，启动 `LogServerThread` 监听端口，收到 `log_server::LogPacket` 后通过 signal 投递 `ut::log::Message`，再 `QueueMessage()` 到交互日志 UI；端口偏好变化会停止并重启线程；Wizard 开始执行仿真时清空已有日志。它是运行输出观察入口，不实现仿真业务逻辑。

### 76.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `LogServer::Plugin` | class | `LogServer.hpp:30` | Log Server 插件入口。 |
| `LogServer::Plugin::HandleLogMessageReceived` | method | `LogServer.cpp:51` | 接收 TCP thread 投递的日志消息。 |
| `LogServer::Plugin::PreferencesChanged` | method | `LogServer.cpp:63` | 重启日志服务器端口。 |
| `LogServerThread` | class | `LogServerThread.hpp:26` | TCP 日志服务器线程。 |
| `LogServerThread::run` | method | `LogServerThread.cpp:32` | 循环处理连接和消息。 |
| `LogServer::PrefWidget` | class | `LogServerPrefWidget.hpp:21` | 日志服务器端口偏好 UI。 |

### 76.4 修正记录

batch17 将该目录定位为中等价值日志观察入口。后续业务逻辑分析可用它定位仿真日志如何进入 Wizard，但真正业务含义仍应追日志生产方。

## 77. wizard/plugins/MapRoute/source

### 77.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 地图/编辑插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/MapRoute/source` |
| source/header 数 | 6 |
| 源文件 | `MapRoutePlugin.hpp`、`MapRoutePlugin.cpp`、`Route.hpp`、`Route.cpp`、`RouteTerrainQuery.hpp`、`RouteTerrainQuery.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 77.2 职责说明

`MapRoute` 是 Wizard route/orbit 可视化与编辑桥。`Plugin::PlatformUpdated()` 为本地平台 route 重建 attachment；`Route::BuildRoute(WsfPM_Mover,double)` 使用 `WsfPathComputer`、`WsfPathConstraints` 和 `WsfPM_Waypoint` 生成路径状态；global route 通过 `OnProxyAvailable()`、`GlobalRouteAdded()`、`GlobalRouteAddWaypoints()` 创建 `_anchor` entity 和 attachment；右键菜单支持创建、删除、插入 waypoint，并通过 editor/proxy 写回源文档。它虽是显示插件，但包含 route mover/path/orbit 业务语义。

### 77.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `MapRoute::Plugin` | class | `MapRoutePlugin.hpp:32` | Map Route 插件入口。 |
| `MapRoute::Plugin::PlatformUpdated` | method | `MapRoutePlugin.cpp:152` | 平台更新时重建 route attachment。 |
| `MapRoute::Plugin::EditGlobalRoute` | method | `MapRoutePlugin.cpp:722` | 编辑器写回 global route 文本。 |
| `MapRoute::Route` | class | `Route.hpp:47` | route path/orbit 构建器。 |
| `MapRoute::Route::BuildRoute` | method | `Route.cpp:321` | 基于 WSF path computer 构建路径。 |
| `MapRoute::RouteTerrainQuery::GetWaypointAltitude` | method | `RouteTerrainQuery.cpp:105` | 计算 waypoint 地形高度。 |

### 77.4 修正记录

batch17 将该目录标为高价值业务语义入口。后续建议优先追 `WsfPM_Mover`、`WsfPM_Route`、`WsfPM_Waypoint`、`WsfPathComputer`、`WsfPathConstraints` 与 editor/proxy 写回链路。

## 78. wizard/plugins/PlatformData/source

### 78.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 平台数据插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/PlatformData/source` |
| source/header 数 | 6 |
| 源文件 | `PluginPlatformData.hpp`、`PluginPlatformData.cpp`、`PlatformDataInterface.hpp`、`PlatformDataInterface.cpp`、`PlatformDataUpdater.hpp`、`PlatformDataUpdater.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 78.2 职责说明

`PlatformData` 是 Wizard 平台初始状态数据面板。`Interface::SetPlatformOfInterest()` 从 `wizard::Platform`/`WsfPM_Platform` 抽取 type、side、icon、lat/lon/alt、yaw/pitch/roll、speed、Mach 等字段；`Plugin::UpdateGui()` 填充 tree widgets；多个 `PlatformUpdater` 派生类通过 `wkfEnv.RegisterUpdater()` 暴露可格式化字段。它不推进仿真，但对平台字段和单位系统的后续分析有索引价值。

### 78.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `PlatformData::Plugin` | class | `PluginPlatformData.hpp:28` | Platform Data 插件入口。 |
| `PlatformData::Plugin::ePlatformData` | enum | `PluginPlatformData.hpp:45` | 平台字段枚举。 |
| `PlatformData::Plugin::UpdateGui` | method | `PluginPlatformData.cpp:115` | 填充平台数据树。 |
| `PlatformData::Interface` | class | `PlatformDataInterface.hpp:20` | 平台数据提取接口。 |
| `PlatformData::Interface::PlatformData` | struct | `PlatformDataInterface.hpp:30` | 平台状态数据结构。 |
| `PlatformData::GetWizardPlatform` | function | `PlatformDataUpdater.cpp:25` | 从平台名查找 Wizard platform。 |

### 78.4 修正记录

batch17 将该目录标为中等价值平台字段入口。后续可向上追 `wizard::Platform`、`WsfPM_Platform`、`WsfPM_Root::platforms()` 和单位/偏好系统。

## 79. wizard/plugins/ZoneEditor/source

### 79.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 编辑/显示插件） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/ZoneEditor/source` |
| source/header 数 | 6 |
| 源文件 | `ZoneEditorPlugin.hpp`、`ZoneEditorPlugin.cpp`、`DockWidget.hpp`、`DockWidget.cpp`、`CreateZoneDialog.hpp`、`CreateZoneDialog.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 79.2 职责说明

`ZoneEditor` 是 Wizard zone 配置编辑和地图可视化插件。`Plugin::OnProxyAvailable()` 订阅 root proxy；`CreateZoneSet()`、`AddZone()` 和 `Extract*Vars()` 将 `WsfPM_Zone`、`WsfPM_ZoneDefinition`、`WsfPM_ZoneSet` 转换为 `wkf::ZoneSetData` 与各类 zone variables；`DockWidget::DrawZone()` 把 zone 画成附件；`CreateZoneDialog::CreateZone()` 拼接 WSF zone 定义文本并写回源码。它不是运行时判定核心，但连接 zone 配置、显示和编辑写回。

### 79.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `ZoneEditor::Plugin` | class | `ZoneEditorPlugin.hpp:30` | Zone Editor 插件入口。 |
| `ZoneEditor::Plugin::CreateZoneSet` | method | `ZoneEditorPlugin.cpp:572` | 构造 zone set 显示数据。 |
| `ZoneEditor::Plugin::AddZone` | method | `ZoneEditorPlugin.cpp:676` | 把 proxy zone 加入显示数据。 |
| `ZoneEditor::DockWidget` | class | `DockWidget.hpp:20` | Zone Browser dock widget。 |
| `ZoneEditor::DockWidget::DrawZone` | method | `DockWidget.cpp:381` | 绘制 zone attachment。 |
| `ZoneEditor::CreateZoneDialog::CreateZone` | method | `CreateZoneDialog.cpp:188` | 创建 WSF zone 定义文本。 |

### 79.4 修正记录

batch18 将该目录标为中等价值配置编辑/可视化入口。后续业务逻辑分析应向上追 `WsfPM_Root::zones/platforms`、`wizard::ProxyWatcher` 和 zone parser，向下追 `wkf::ZoneBrowserDataContainer` 与 `wkf::AttachmentZone*`。

## 80. wsf_plugins/wsf_sosm/source

### 80.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（WSF 运行时插件） |
| 子系统 | `wsf_plugins/wsf_sosm` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_sosm/source` |
| source/header 数 | 6 |
| 源文件 | `WsfSOSM_Interface.hpp`、`WsfSOSM_Interface.cpp`、`WsfSOSM_Sensor.hpp`、`WsfSOSM_Sensor.cpp`、`WsfSOSM_Interaction.hpp`、`WsfSOSM_Interaction.cpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 80.2 职责说明

`wsf_sosm` 是 WSF SOSM 传感器运行时插件。`Register_wsf_sosm()` 注册 scenario extension 和 `WSF_SOSM_SENSOR`；`WsfSOSM_Interface::ProcessInput()` 处理 `sosm_interface`、`load`、`map_sensor_type`、`map_target_type` 输入；`WsfSOSM_Sensor::SOSM_Mode::Initialize()` 配置频率、带宽、阈值和接收机；`AttemptToDetect()` 调用 SOSM manager 和 sensor-target pair，计算探测概率、接收功率、信噪比并写入 `WsfSensorResult`。这是本批最重要的运行时业务入口。

### 80.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `Register_wsf_sosm` | function | `WsfSOSM_Interface.cpp:35` | 注册 SOSM extension 和 sensor type。 |
| `WsfSOSM_Interface` | class | `WsfSOSM_Interface.hpp:33` | SOSM scenario extension。 |
| `WsfSOSM_Interface::ProcessInput` | method | `WsfSOSM_Interface.cpp:119` | 解析 SOSM 输入块。 |
| `WsfSOSM_Sensor` | class | `WsfSOSM_Sensor.hpp:27` | WSF_SOSM_SENSOR 实现。 |
| `WsfSOSM_Sensor::SOSM_Mode` | class | `WsfSOSM_Sensor.hpp:45` | SOSM sensor mode。 |
| `WsfSOSM_Sensor::SOSM_Mode::AttemptToDetect` | method | `WsfSOSM_Sensor.cpp:252` | 执行 SOSM 概率探测。 |

### 80.4 修正记录

batch18 将该目录标为高价值传感器运行时入口。后续应继续追 `wsf_sosm/sosm/source/SOSM_Manager.cpp`、`SOSM_SensorTarget`、`WsfSensorResult` 和 `WsfSensorComponent::PostAttemptToDetect`。

## 81. core/wsf_mil_parser/source

### 81.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework`（MIL proxy 访问层） |
| 子系统 | `core/wsf_mil_parser` |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_mil_parser/source` |
| source/header 数 | 7 |
| 源文件 | `WsfPM_MilPlatform.hpp`、`WsfPM_MilPlatform.cpp`、`WsfPM_MilRoot.hpp`、`WsfPM_MilRoot.cpp`、`WsfPM_RF_Jammer.hpp`、`WsfPM_RF_Jammer.cpp`、`WsfPM_Weapon.hpp` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号 |

### 81.2 职责说明

`wsf_mil_parser` 是 MIL 场景 proxy typed accessor 层。它用 `WsfPProxyNode` 和 `WsfPM_ObjectMapT` 包装 platform、weapon、RF jammer 等配置对象，提供 `weapons()`、`FindPart()`、`weaponTypes()`、`platforms()`、`Mode::transmitter()` 等访问器。它不执行运行时仿真算法，但对追踪 MIL 配置字段如何映射到工具和运行时对象有价值。

### 81.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WsfPM_MilPlatform` | class | `WsfPM_MilPlatform.hpp:21` | MIL platform proxy wrapper。 |
| `WsfPM_MilPlatform::Weapons` | method | `WsfPM_MilPlatform.cpp:23` | 读取 weapon map。 |
| `WsfPM_MilRoot` | class | `WsfPM_MilRoot.hpp:24` | MIL root proxy wrapper。 |
| `Register_wsf_mil_parser` | function | `WsfPM_MilRoot.cpp:22` | MIL parser 注册入口，当前注册语句被注释。 |
| `WsfPM_RF_Jammer` | class | `WsfPM_RF_Jammer.hpp:22` | RF jammer proxy wrapper。 |
| `WsfPM_RF_Jammer::Mode::transmitter` | method | `WsfPM_RF_Jammer.cpp:14` | 读取 transmitter proxy。 |

### 81.4 修正记录

batch18 将该目录标为中等价值 proxy 字段入口。后续应向上追 `WsfPM_Root`、`WsfPM_Platform`、`WsfPProxyNode`，向下追工具侧调用者和真实 MIL/WSF 运行时对象映射。

## 82. tools/profiling/source

### 82.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（profiling 基础设施） |
| 子系统 | `tools/profiling` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/profiling/source` |
| source/header 数 | 7 |
| 源文件 | `ProfilingHooks.hpp`、`ProfilingRegion.hpp`、`ProfilingRegion.cpp`、`ProfilingSystem.hpp`、`ProfilingSystem.cpp`、`TimedRegion.hpp`、`TimedRegion.cpp` |
| 头模板 | `ProfilingMacros.hpp.in` |
| 证据 | 子 agent 证据采集 + CodeGraph node + 源码行号；头模板回退文本证据 |

### 82.2 职责说明

`profiling` 是性能分析基础设施。它定义 profiling hook ABI、动态加载 `afperf` hooks、管理全局 profiling lifecycle，并提供 `ProfilingRegion`、`TimedRegion` 等 RAII/计时辅助。它对业务语义贡献低，但对理解性能开关、运行入口和外部 profiling 动态库有价值。

### 82.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `profiling::ProfilingHooks` | struct | `ProfilingHooks.hpp:195` | profiling hook 函数表。 |
| `profiling::ProfilingRegion` | class | `ProfilingRegion.hpp:96` | profiling RAII region。 |
| `profiling::ProfilingSystemArguments` | struct | `ProfilingSystem.hpp:34` | profiling system 参数。 |
| `profiling::ProfilingSystem` | class | `ProfilingSystem.hpp:77` | profiling 全局 lifecycle 管理。 |
| `LoadProfilingHooks` | function | `ProfilingSystem.cpp:211` | 加载 profiling hook 符号。 |
| `profiling::TimedRegion` | class | `TimedRegion.hpp:85` | 墙钟/CPU 计时 region。 |

### 82.4 修正记录

batch18 将该目录定位为低价值业务入口、较高价值性能基础设施入口。后续可追 `WsfProfilingApplicationExtension.cpp`、`mission.cpp`、`WsfStandardApplication.cpp` 和 `afperf` 实现库。

## 83. warlock/plugins/PlatformBrowser/source

### 83.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 工具/运行时桥） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/PlatformBrowser/source` |
| source/header 数 | 7 |
| 源文件 | `PlatformBrowserPlugin.hpp`、`PlatformBrowserPlugin.cpp`、`PlatformBrowserInterface.hpp`、`PlatformBrowserInterface.cpp`、`PlatformBrowserSimInterface.hpp`、`PlatformBrowserSimCommands.hpp`、`PlatformBrowserSimCommands.cpp` |
| 证据 | 子 agent 证据采集；CodeGraph 目录查询噪声后回退文本证据 |

### 83.2 职责说明

`PlatformBrowser` 是 Warlock 平台浏览和删除入口。UI 侧复用 `wkf::PlatformBrowserInterface` 和 dock；`BuildEntityContextMenu()` 为平台添加删除动作；`Interface::DeletePlatform()` 做权限检查和确认，然后提交 `DeletePlatformsCommand`；命令在 simulation thread 中调用 `WsfSimulation::DeletePlatform()` 或发送 `WsfXIO_DeletePlatformPkt`。它是本批高价值 mutation 入口。

### 83.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkPlatformBrowser::Plugin` | class | `PlatformBrowserPlugin.hpp:28` | Platform Browser 插件入口。 |
| `WkPlatformBrowser::Plugin::BuildEntityContextMenu` | method | `PlatformBrowserPlugin.cpp:41` | 创建删除平台右键动作。 |
| `WkPlatformBrowser::Interface` | class | `PlatformBrowserInterface.hpp:24` | Platform Browser UI interface。 |
| `WkPlatformBrowser::Interface::DeletePlatform` | method | `PlatformBrowserInterface.cpp:44` | 权限检查并提交删除命令。 |
| `WkPlatformBrowser::DeletePlatformsCommand` | class | `PlatformBrowserSimCommands.hpp:20` | 删除平台 sim command。 |
| `WkPlatformBrowser::DeletePlatformsCommand::Process` | method | `PlatformBrowserSimCommands.cpp:21` | 删除本地平台或发送 XIO 删除包。 |

### 83.4 修正记录

batch18 将该目录标为高价值平台 mutation 入口。后续应继续追 `warlock::HasPermissionToCreateOrRemovePlatforms()`、`WsfSimulation::DeletePlatform()`、`WsfXIO_DeletePlatformPkt` 和 `WkObserver::SimulationUserAction`。

## 84. warlock/plugins/ScriptBrowser/source

### 84.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 脚本执行工具） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/ScriptBrowser/source` |
| source/header 数 | 7 |
| 源文件 | `ScriptBrowserPlugin.hpp`、`ScriptBrowserPlugin.cpp`、`ScriptBrowserDockWidget.hpp`、`ScriptBrowserDockWidget.cpp`、`ScriptBrowserSimInterface.hpp`、`ScriptBrowserSimInterface.cpp`、`ScriptBrowserSimEvents.hpp` |
| 证据 | 子 agent 证据采集；CodeGraph 目录查询噪声后回退文本证据 |

### 84.2 职责说明

`ScriptBrowser` 是 Warlock 脚本浏览和执行插件。`DockWidget::SimulationStarting()` 加载 global scripts；`PopulateGlobalTableWidget()` 和 `PopulatePlatformTableWidget()` 过滤 `WARLOCK_` 脚本；`ExecutePushButtonClicked()` 从 UI 收集参数并调用 `warlock::ScriptSimInterface::ExecuteScript()`；`ReturnValueReadyCB()` 消费脚本返回值。它是 Warlock GUI 到 global/platform script 执行环境的直接入口。

### 84.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkScriptBrowser::Plugin` | class | `ScriptBrowserPlugin.hpp:20` | Script Browser 插件入口。 |
| `WkScriptBrowser::DockWidget` | class | `ScriptBrowserDockWidget.hpp:53` | 脚本浏览和执行 dock。 |
| `WkScriptBrowser::DockWidget::SimulationStarting` | method | `ScriptBrowserDockWidget.cpp:65` | 加载 global scripts。 |
| `WkScriptBrowser::DockWidget::ExecutePushButtonClicked` | method | `ScriptBrowserDockWidget.cpp:112` | 收集参数并执行脚本。 |
| `WkScriptBrowser::DataWidget` | class | `ScriptBrowserDockWidget.hpp:28` | 脚本参数输入 widget。 |
| `WkScriptBrowser::SimInterface` | class | `ScriptBrowserSimInterface.hpp:20` | Script Browser sim interface。 |

### 84.4 修正记录

batch18 将该目录标为高价值脚本执行入口。后续业务逻辑分析应继续追 `warlock::ScriptSimInterface`、`warlock::script::Data/Instance/Argument/ReturnValue`、XIO script-info 更新、脚本权限和脚本执行副作用。

## 85. wsf_plugins/wsf_alternate_locations/source

### 85.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（WSF runtime 插件） |
| 子系统 | `wsf_plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_alternate_locations/source` |
| source/header 数 | 7 |
| 源文件 | `WsfAltLoc.cpp`、`WsfAltLocComponent.hpp/.cpp`、`WsfAltLocSimulationExtension.hpp/.cpp`、`WsfAltLocEventResults.hpp/.cpp` |
| 证据 | 子 agent CodeGraph/源码证据；`vx.json` 仅作为元数据，不计入源码数 |

### 85.2 职责说明

`wsf_alternate_locations` 是平台替代位置初始化插件。它解析平台 `alternate_locations` 配置，按权重、引用平台、LLA/ARA 偏移和全局 draw 决定最终初始位置，在 `Component::PreInitialize()` 中调用平台位置/朝向写入接口，并通过 `event_output` 输出 `ALTERNATE_LOCATIONS_INITIALIZED` 事件。

### 85.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WsfAltLoc::Component` | class | `WsfAltLocComponent.hpp:49` | 平台 alternate locations 组件。 |
| `WsfAltLoc::WeightedLocation` | struct | `WsfAltLocComponent.hpp:27` | 带权重的位置候选。 |
| `WsfAltLoc::SimulationExtension` | class | `WsfAltLocSimulationExtension.hpp:40` | 保存全局 draw/debug 配置并注册事件输出。 |
| `WsfAltLoc::ComponentInitialized` | class | `WsfAltLocEventResults.hpp:20` | 替代位置初始化事件输出。 |
| `Register_wsf_alternate_locations` | function | `WsfAltLoc.cpp:126` | 插件注册入口。 |

### 85.4 后续深挖点

高价值业务入口是 `Component::ProcessInput()` 和 `Component::PreInitialize()`：前者定义配置合法性，后者定义平台 availability、引用位置、地形 AGL 修正和最终平台状态写入。需继续确认 `offset_lla` 单位/越界语义和引用平台未实例化时对仿真的影响。

## 86. mystic/plugins/ResultMerger/source

### 86.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果工具） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultMerger/source` |
| source/header 数 | 8 |
| 源文件 | `RvPluginMerger.hpp/.cpp`、`RvMergeDialog.hpp/.cpp`、`RvMergerThread.hpp/.cpp`、`RvMergerUtils.hpp/.cpp` |
| 证据 | 子 agent CodeGraph/源码证据；`CMakeLists.txt` 作为构建证据 |

### 86.2 职责说明

`ResultMerger` 是 Mystic recording 合并工具。插件向工具菜单注册 “Merge Recordings...”，通过 `MergeDialog` 选择多个 `.aer` 输入、master recording 和输出文件，并由 `MergerThread` 校验 schema、计算时间偏移、重映射平台 index、过滤/输出消息。

### 86.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvMerger::Plugin` | class | `RvPluginMerger.hpp:21` | Recording Merger 插件入口。 |
| `RvMerger::MergeDialog` | class | `RvMergeDialog.hpp:22` | 合并参数对话框。 |
| `RvMerger::MergerThread` | class | `RvMergerThread.hpp:27` | 后台合并线程。 |
| `RvMerger::RecordingFileReader` | class | `RvMergerUtils.hpp:69` | AER recording 读取器。 |
| `RvMerger::RecordingFileWriter` | class | `RvMergerUtils.hpp:128` | AER recording 写入器。 |
| `RvMerger::PlatformDatabase` | class | `RvMergerUtils.hpp:145` | 跨 recording 平台 DIS id 合并表。 |

### 86.4 后续深挖点

高价值入口是 `MergerThread::run()`、`InitializeSerializer()`、`DetermineTimeOffset()` 和 `PlatformDatabase::Add()`。需要验证 `GetNextMessage()` 时间排序是否正确使用 offset，以及 `simIndex()==0` 过滤是否符合所有 recording 合并场景。

## 87. mystic/plugins/ResultOrbitalData/source

### 87.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 空间结果展示） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultOrbitalData/source` |
| source/header 数 | 8 |
| 源文件 | `RvPluginOrbitalData.hpp/.cpp`、`RvOrbitalDataInterface.hpp/.cpp`、`RvOrbitalDataUpdaters.hpp/.cpp`、`RvOrbitalDataPlotUpdaters.hpp/.cpp` |
| 证据 | 子 agent CodeGraph/源码证据 |

### 87.2 职责说明

`ResultOrbitalData` 从空间平台的 `MsgEntityState` 和 `MsgPlatformInfo` 中计算轨道根数，包括偏心率、半长轴、倾角、RAAN、近拱点幅角和真近点角，并提供平台详情树、单值 updater 和 plot updater。

### 87.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvOrbitalData::Plugin` | class | `RvPluginOrbitalData.hpp:26` | Orbital Data 插件入口。 |
| `RvOrbitalData::Plugin::OrbitalDataType` | enum | `RvPluginOrbitalData.hpp:78` | 轨道根数字段枚举。 |
| `RvOrbitalData::OrbitalDataContainer` | struct | `RvOrbitalDataInterface.hpp:26` | 轨道根数数据容器。 |
| `RvOrbitalData::Interface` | class | `RvOrbitalDataInterface.hpp:40` | 轨道数据读取接口。 |
| `RvOrbitalData::PlotUpdater` | class | `RvOrbitalDataPlotUpdaters.hpp:28` | 轨道数据绘图 updater。 |

### 87.4 后续深挖点

`Interface::GenerateOrbitalData()` 是空间业务语义入口，需继续确认 TOD/ECI 转换、地球模型、单位转换和 `MsgPlatformInfo::spatialDomain()==space` 的可见性规则。`PlotUpdater::GetSeries()` 需要检查采样性能和 `mLastUpdate` 状态。

## 88. mystic/plugins/ResultP6DOFData/source

### 88.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic deprecated P6DOF 结果展示） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultP6DOFData/source` |
| source/header 数 | 8 |
| 源文件 | `RvPluginP6DOFData.hpp/.cpp`、`RvP6DOFDataInterface.hpp/.cpp`、`RvP6DOFDataUpdater.hpp/.cpp`、`RvP6DOFDataPlotUpdater.hpp/.cpp` |
| 证据 | 子 agent CodeGraph/源码证据 |

### 88.2 职责说明

`ResultP6DOFData` 消费 deprecated P6DOF 结果消息，展示 Core、Kinematic、Engine/Fuel、Autopilot、Control Inputs、Control Surfaces 和 Force/Moment 等字段，并注册大量 updater 与绘图轴映射。

### 88.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvP6DOFData::Plugin` | class | `RvPluginP6DOFData.hpp:26` | P6DOF Data 插件入口。 |
| `RvP6DOFData::Plugin::eP6dofDataType` | enum | `RvPluginP6DOFData.hpp:86` | P6DOF 数据分组枚举。 |
| `RvP6DOFData::Interface` | class | `RvP6DOFDataInterface.hpp:28` | P6DOF 结果消息读取接口。 |
| `RvP6DOFData::Interface::P6dofDataContainer` | struct | `RvP6DOFDataInterface.hpp:47` | P6DOF 多消息聚合容器。 |
| `RvP6DOFData::PlotUpdater` | class | `RvP6DOFDataPlotUpdater.hpp:51` | P6DOF 绘图 updater。 |

### 88.4 后续深挖点

后续应对照 SixDOF 数据插件继续确认字段映射。已发现需人工/函数级验证的疑点包括 `KTAS_Updater` 读取 `KCAS()`、若干 plot X 轴分支用 `aYAxis` 取值、构造函数空指针保护和 AutopilotLimits 绘图覆盖范围。

## 89. mystic/plugins/ResultPlatformBrowser/source

### 89.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 平台浏览适配） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultPlatformBrowser/source` |
| source/header 数 | 8 |
| 源文件 | `RvPluginPlatformBrowser.hpp/.cpp`、`RvPlatformBrowserInterface.hpp/.cpp`、`RvPlatformBrowserPrefObject.hpp/.cpp`、`RvPlatformBrowserPrefWidget.hpp/.cpp` |
| 证据 | 子 agent CodeGraph/源码证据 |

### 89.2 职责说明

`ResultPlatformBrowser` 是 Mystic 平台浏览 dock 的薄适配层。它注册 “Platform Browser” 插件，创建偏好页和 `RvPlatformBrowser::Interface`，在 GUI tick 中转发 `UpdateInfo()`，并把 `showInactive` 偏好同步到 dock。

### 89.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvPlatformBrowser::Plugin` | class | `RvPluginPlatformBrowser.hpp:20` | Platform Browser 插件入口。 |
| `RvPlatformBrowser::Interface` | class | `RvPlatformBrowserInterface.hpp:26` | Mystic 平台浏览适配接口。 |
| `RvPlatformBrowser::PrefData` | struct | `RvPlatformBrowserPrefObject.hpp:18` | 平台浏览偏好数据。 |
| `RvPlatformBrowser::PrefObject` | class | `RvPlatformBrowserPrefObject.hpp:23` | 平台浏览偏好对象。 |
| `RvPlatformBrowser::PrefWidget` | class | `RvPlatformBrowserPrefWidget.hpp:21` | 平台浏览偏好 UI。 |

### 89.4 后续深挖点

本目录不应被误判为平台列表构建核心。后续如需分析平台浏览业务，应追 `wkf::PlatformBrowserInterface` 和 `WkfPlatformBrowserDockWidget` 的平台枚举、inactive 过滤、选择和刷新逻辑。

## 90. mystic/plugins/ResultPlatformData/source

### 90.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 平台结果数据消费） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultPlatformData/source` |
| source/header 数 | 8 |
| 源文件 | `RvPluginPlatformData.hpp/.cpp`、`RvPlatformDataInterface.hpp/.cpp`、`RvPlatformDataUpdater.hpp/.cpp`、`RvPlatformDataPlotUpdater.hpp/.cpp` |
| 证据 | 子 agent CodeGraph/源码证据 |

### 90.2 职责说明

`ResultPlatformData` 是 Mystic 平台结果数据消费核心之一。它从 `ResultData/ResultPlatform` 读取平台信息、状态、部件、类别、传感器/武器模式和运动数据，驱动平台详情树、data ring 附件、单值 updater 和 plotting widget。

### 90.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvPlatformData::Plugin` | class | `RvPluginPlatformData.hpp:26` | Platform Data 插件入口。 |
| `RvPlatformData::Plugin::ePlatformData` | enum | `RvPluginPlatformData.hpp:64` | 平台数据树字段枚举。 |
| `RvPlatformData::Interface` | class | `RvPlatformDataInterface.hpp:28` | 平台结果数据读取接口。 |
| `RvPlatformData::Interface::PlatformData` | struct | `RvPlatformDataInterface.hpp:40` | 平台展示数据聚合结构。 |
| `RvPlatformData::PlotUpdater` | class | `RvPlatformDataPlotUpdater.hpp:31` | 平台数据绘图 updater。 |

### 90.4 后续深挖点

高价值入口是 `Interface::AdvanceTimeRead()`、`Plugin::GuiUpdate()`、`PlotUpdater::GetSeries()/GetData()` 和 data ring 菜单生命周期。需确认 `infoPtr` 空指针路径、平台 index 0 语义、`mLastUpdate` 线程安全和 `FuelUpdater` 是否未注册。

## 91. mystic/plugins/ResultRelativeGeometry/source

### 91.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 相对几何结果工具） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultRelativeGeometry/source` |
| source/header 数 | 8 |
| 源文件 | `RelativeGeometryPlugin.hpp/.cpp`、`RelativeGeometryDialog.hpp/.cpp`、`RelativeGeometryUpdater.hpp/.cpp`、`RelativeGeometryPlotUpdater.hpp/.cpp` |
| 证据 | 子 agent CodeGraph/源码证据 |

### 91.2 职责说明

`ResultRelativeGeometry` 是 Mystic 双平台相对几何工具。它从平台上下文菜单打开 dock，维护 From/To 平台，按空间域选择线性距离、径向/横向/航向、方位、俯仰和距离率等指标，并基于 `MsgEntityState` 生成实时 updater 与历史绘图序列。

### 91.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RelativeGeometry::Plugin` | class | `RelativeGeometryPlugin.hpp:23` | 插件入口。 |
| `RelativeGeometry::Dialog` | class | `RelativeGeometryDialog.hpp:22` | 相对几何 dock。 |
| `RelativeGeometry::DualPlatformUpdaterT` | class | `RelativeGeometryUpdater.hpp:24` | 双平台 updater 模板。 |
| `RelativeGeometry::LinearRangeUpdater` | class | `RelativeGeometryUpdater.hpp:84` | 线性距离 updater。 |
| `RelativeGeometry::PlotUpdater` | class | `RelativeGeometryPlotUpdater.hpp:30` | 相对几何绘图 updater。 |

### 91.4 后续深挖点

应继续追 `RelativeGeometryPlotUpdater::GetSeries()` 的双平台时间对齐和采样策略，以及 `UtRelativeGeometry::Calculate*` 的坐标系/空间域语义。`Plugin::GetUpdater()` 依赖 `"from to"` 标题拆分，平台名含空格时可能脆弱。

## 92. mystic/plugins/ResultScriptDataFeed/source

### 92.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 脚本数据消费） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultScriptDataFeed/source` |
| source/header 数 | 8 |
| 源文件 | `RvPluginScriptDataFeed.hpp/.cpp`、`RvScriptDataInterface.hpp/.cpp`、`RvScriptDataUpdater.hpp/.cpp`、`RvScriptDataPlotUpdater.hpp/.cpp` |
| 证据 | 子 agent CodeGraph/源码证据 |

### 92.2 职责说明

`ResultScriptDataFeed` 消费 `MsgScriptData` keyed map，将脚本发布的 floating、integer、boolean、text 数据挂入平台详情树。数值类型会标为可绘图并提供 `PlotUpdater`，所有类型可通过 `Updater::GetValueString()` 在平台数据面板显示。

### 92.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvScriptDataFeed::Plugin` | class | `RvPluginScriptDataFeed.hpp:45` | Script Data Feed 插件入口。 |
| `RvScriptDataFeed::UnionTreeItem` | class | `RvPluginScriptDataFeed.hpp:29` | union 值显示树项。 |
| `RvScriptDataFeed::Interface` | class | `RvScriptDataInterface.hpp:27` | script data 读取接口。 |
| `RvScriptDataFeed::Updater` | class | `RvScriptDataUpdater.hpp:19` | script data 单值 updater。 |
| `RvScriptDataFeed::PlotUpdater` | class | `RvScriptDataPlotUpdater.hpp:27` | script data 绘图 updater。 |

### 92.4 后续深挖点

高价值入口是 `Interface::AdvanceTimeRead()` 和 `PlotUpdater::GetSeries()`。后续应向上追 `MsgScriptData` 在 WSF event pipe 中的发布点，并确认 `GetPlatformData()` 返回锁内引用、`MenuPlot()` 仅声明未实现、平台 index 0 语义等问题。

## 93. mystic/plugins/ResultSixDOF_Data/source

### 93.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic SixDOF 结果展示） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultSixDOF_Data/source` |
| source/header 数 | 8 |
| 源文件 | `RvPluginSixDOF_Data.hpp/.cpp`、`RvSixDOF_DataInterface.hpp/.cpp`、`RvSixDOF_DataUpdater.hpp/.cpp`、`RvSixDOF_DataPlotUpdater.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因连接中断失败 |

### 93.2 职责说明

`ResultSixDOF_Data` 消费 SixDOF Core、Kinematic、EngineFuel、Autopilot、AutopilotLimits、ControlInputs、ControlSurfaces 和 ForceMoment 消息，展示飞行状态、燃油、自动驾驶、操纵和力矩字段，并注册大量 updater 与绘图轴。

### 93.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvSixDOF_Data::Plugin` | class | `RvPluginSixDOF_Data.hpp:26` | SixDOF Data 插件入口。 |
| `RvSixDOF_Data::Plugin::eSixDOF_DataType` | enum | `RvPluginSixDOF_Data.hpp:86` | SixDOF 数据字段枚举。 |
| `RvSixDOF_Data::Interface` | class | `RvSixDOF_DataInterface.hpp:27` | SixDOF 结果消息读取接口。 |
| `RvSixDOF_Data::Interface::SixDOF_DataContainer` | struct | `RvSixDOF_DataInterface.hpp:40` | SixDOF 多消息聚合容器。 |
| `RvSixDOF_Data::PlotUpdater` | class | `RvSixDOF_DataPlotUpdater.hpp:51` | SixDOF 绘图 updater。 |

### 93.4 后续深挖点

应和 batch19 的 `ResultP6DOFData` 对照分析。`PlotUpdater::GetSeries()` 中多个 X 轴分支使用 `aYAxis` 取值，构造函数直接访问平台和 control surfaces，平台 index 0 语义也需统一确认。

## 94. mystic/plugins/ResultStatistics/source

### 94.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Mystic 结果统计和事件表） |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultStatistics/source` |
| source/header 数 | 8 |
| 源文件 | `RvPluginStatistics.hpp/.cpp`、`RvEventTableModel.hpp/.cpp`、`RvMetaDataDialog.hpp/.cpp`、`RvStatisticsRules.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因连接中断失败 |

### 94.2 职责说明

`ResultStatistics` 提供三类 Mystic 结果辅助能力：按 schema 统计消息数量/字节并绘制饼图；展示全量 paged/one-time event list 并支持过滤/绘图；读取 `MsgExecData` 展示 AFSIM executable、路径、命令行、features 和 extensions。

### 94.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RvStatistics::Plugin` | class | `RvPluginStatistics.hpp:23` | Statistics 插件入口。 |
| `RvStatistics::EventTableModel` | class | `RvEventTableModel.hpp:75` | 结果消息事件表模型。 |
| `RvStatistics::StatisticsRule` | struct | `RvStatisticsRules.hpp:20` | 统计过滤规则基类。 |
| `RvStatistics::StatisticsRuleSide` | struct | `RvStatisticsRules.hpp:28` | 按 side 过滤规则。 |
| `RvStatistics::MetaDataDialog` | class | `RvMetaDataDialog.hpp:20` | AFSIM 执行元数据对话框。 |

### 94.4 后续深挖点

`EventTableModel::data()` 是 Result 消息解释总入口，覆盖 `MsgEntityState`、track、sensor、weapon、zone、comm/network 等大量消息，并通过 `rvEnv.GetExtensions()` 处理扩展消息。后续业务逻辑分析可把它作为“结果消息字段如何被人工检查”的索引入口。

## 95. tools/wkf/plugins/MapHoverInfo/source

### 95.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF 交互工具） |
| 子系统 | `tools/wkf/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/MapHoverInfo/source` |
| source/header 数 | 8 |
| 源文件 | `MapHoverInfoPlugin.hpp/.cpp`、`MapHoverInfoPrefObject.hpp/.cpp`、`MapHoverInfoPrefWidget.hpp/.cpp`、`MapHoverInfoListSelectionWidget.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因连接中断失败 |

### 95.2 职责说明

`MapHoverInfo` 在地图 widget 安装 `HoverManager` event filter，捕捉 tooltip 事件后通过 viewer picking 找到附件或实体。平台使用 `wkf::Updater` 生成字段，非平台实体使用 `NamedInfo`，偏好页控制显示名称、标签和字段列表。

### 95.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `MapHoverInfo::Plugin` | class | `MapHoverInfoPlugin.hpp:59` | Map Hover Info 插件入口。 |
| `MapHoverInfo::HoverManager` | class | `MapHoverInfoPlugin.hpp:27` | hover 事件管理器。 |
| `MapHoverInfo::HoverStyle` | class | `MapHoverInfoPlugin.hpp:80` | tooltip 唤醒延迟样式。 |
| `MapHoverInfo::PrefData` | struct | `MapHoverInfoPrefObject.hpp:22` | hover 偏好数据。 |
| `MapHoverInfo::ListSelectionWidget` | class | `MapHoverInfoListSelectionWidget.hpp:20` | hover 字段选择控件。 |

### 95.4 后续深挖点

高价值入口是 `HoverManager::HandleHoverEvent()`、`GetPlatformString()` 和 `GetNonPlatformString()`。需要验证实体销毁/场景切换时 updater 缓存生命周期，以及当前逻辑只处理第一个 hit 是否符合用户交互预期。

## 96. tools/wkf/plugins/TetherView/source

### 96.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF 二级视窗工具） |
| 子系统 | `tools/wkf/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/TetherView/source` |
| source/header 数 | 8 |
| 源文件 | `TetherViewPlugin.hpp/.cpp`、`TetherViewDockWidget.hpp/.cpp`、`TetherViewPrefObject.hpp/.cpp`、`TetherViewPrefWidget.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因连接中断失败 |

### 96.2 职责说明

`TetherView` 为平台、track 和 point-of-interest 的上下文菜单增加 tether/look-at 操作，并提供 `Ctrl+Shift+T` 快捷动作。它创建 `DockWidget` 二级视窗，支持启动时恢复可见 tether 平台，偏好控制航向锁定和灯光。

### 96.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `TetherView::Plugin` | class | `TetherViewPlugin.hpp:24` | Tether View 插件入口。 |
| `TetherView::DockWidget` | class | `TetherViewDockWidget.hpp:31` | tether/look-at 二级视窗。 |
| `TetherView::PrefData` | struct | `TetherViewPrefObject.hpp:21` | tether 偏好数据。 |
| `TetherView::PrefObject` | class | `TetherViewPrefObject.hpp:27` | tether 偏好对象。 |
| `TetherView::PrefWidget` | class | `TetherViewPrefWidget.hpp:20` | tether 偏好 UI。 |

### 96.4 后续深挖点

应继续追 `ConnectToPlatform()`、`LookAt()` 和 `DockWidget` 的 immersive viewer 行为。启动恢复只保存平台 tether，不保存 look-at 组合；多窗口对象名和销毁回调对生命周期正确性有影响。

## 97. warlock/plugins/BattleManagement/source

### 97.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock Battle Management） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/BattleManagement/source` |
| source/header 数 | 8 |
| 源文件 | `BM_Plugin.hpp/.cpp`、`BM_SimInterface.hpp/.cpp`、`BM_SimEvent.hpp/.cpp`、`BM_RuleSets.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因用量/连接限制失败 |

### 97.2 职责说明

`BattleManagement` 在 Warlock 中维护平台状态、damage/fuel 和 aux data/resource aux data 规则。`SimInterface` 在平台加入、仿真初始化和 clock read 阶段采集平台 side/type/category、weapon 标记、damage/fuel 与 aux data keys，再通过 BM event 更新 `wkf::bm::PluginBase` 的平台状态和规则集。

### 97.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkBM::Plugin` | class | `BM_Plugin.hpp:24` | Battle Management 插件入口。 |
| `WkBM::SimInterface` | class | `BM_SimInterface.hpp:21` | 采集平台和 BM 状态事件的仿真接口。 |
| `WkBM::PlatformState` | struct | `BM_RuleSets.hpp:22` | 平台 damage/fuel 状态缓存。 |
| `WkBM::RuleSetDamageFactor` | class | `BM_RuleSets.hpp:31` | damage factor 颜色规则。 |
| `WkBM::AuxDataRuleSet` | class | `BM_RuleSets.hpp:64` | aux data 颜色规则。 |

### 97.4 后续深挖点

高价值入口是 `SimInterface::SimulationClockRead()` 和 `AuxDataEvent::Process()`。后续应继续追 aux data key 的生产方、weapon count TODO 的真实业务意图，以及 BM 颜色/资源规则如何影响指挥控制界面判断。

## 98. warlock/plugins/Comment/source

### 98.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock comment bubble） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Comment/source` |
| source/header 数 | 8 |
| 源文件 | `CommentPlugin.hpp/.cpp`、`CommentSimInterface.hpp/.cpp`、`CommentSimEvents.hpp/.cpp`、`CommentDataContainer.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因用量/连接限制失败 |

### 98.2 职责说明

`Comment` 监听 `WsfObserver::Comment`，将仿真 comment 转换为 Warlock 地图上的 comment decorator 或 attachment。插件按偏好控制显示方式、team color 和过期清理，并通过 `DataContainer` 管理当前 comment 集合。

### 98.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkComment::Plugin` | class | `CommentPlugin.hpp:22` | Comment Bubbles 插件入口。 |
| `WkComment::SimInterface` | class | `CommentSimInterface.hpp:20` | 连接 `WsfObserver::Comment` 的仿真接口。 |
| `WkComment::CommentData` | struct | `CommentDataContainer.hpp:20` | 单条 comment 显示数据。 |
| `WkComment::DataContainer` | class | `CommentDataContainer.hpp:29` | comment 数据容器。 |
| `WkComment::AddEvent` | class | `CommentSimEvents.hpp:32` | 添加 comment 显示事件。 |

### 98.4 后续深挖点

应沿 `WsfObserver::Comment` 继续向 comment 生产方追踪。当前模块本身主要负责可视化和过期清理，不决定 comment 的业务含义。

## 99. warlock/plugins/CyberEngagementController/source

### 99.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock cyber 控制） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/CyberEngagementController/source` |
| source/header 数 | 8 |
| 源文件 | `CyberEngagementControllerPlugin.hpp/.cpp`、`CyberEngagementControllerSimInterface.hpp/.cpp`、`CyberEngagementControllerSimCommand.hpp/.cpp`、`CyberEngagementControllerSimEvents.hpp`、`CyberEngagementControllerDataContainer.hpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因用量/连接限制失败 |

### 99.2 职责说明

`CyberEngagementController` 在实体上下文菜单中提供 cyber attack 和 cyber scan。`SimInterface::SimulationInitializing()` 从 cyber scenario extension 读取 attack types，过滤需要额外输入或基类类型的 attack。菜单动作先检查平台控制权限，再提交 `CyberEngagementControllerCommand` 或 `CyberScanCommand` 到仿真线程。

### 99.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkCyberEngagementController::Plugin` | class | `CyberEngagementControllerPlugin.hpp:23` | Cyber Engagement Controller 插件入口。 |
| `WkCyberEngagementController::SimInterface` | class | `CyberEngagementControllerSimInterface.hpp:22` | 采集 cyber attack types 的仿真接口。 |
| `WkCyberEngagementController::DataContainer` | class | `CyberEngagementControllerDataContainer.hpp:25` | cyber attack type 容器。 |
| `WkCyberEngagementController::CyberEngagementControllerCommand` | class | `CyberEngagementControllerSimCommand.hpp:21` | 执行 `CyberAttack` 的仿真命令。 |
| `WkCyberEngagementController::CyberScanCommand` | class | `CyberEngagementControllerSimCommand.hpp:42` | 执行 `CyberScan` 的仿真命令。 |

### 99.4 后续深挖点

高价值入口是 `CyberEngagementControllerCommand::Process()` 和 `CyberScanCommand::Process()`，它们分别调用 `WsfCyberEngagementManager::CyberAttack()` 与 `CyberScan()`。后续业务逻辑应继续进入 `wsf::cyber::ScenarioExtension` 和 engagement manager。

## 100. warlock/plugins/NetworkBrowser/source

### 100.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock network browser） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/NetworkBrowser/source` |
| source/header 数 | 8 |
| 源文件 | `NetworkBrowserPlugin.hpp/.cpp`、`NetworkBrowserSimInterface.hpp/.cpp`、`NetworkBrowserSimEvents.hpp`、`NetworkBrowserDataContainer.hpp`、`NetworkBrowserDockWidget.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因用量/连接限制失败 |

### 100.2 职责说明

`NetworkBrowser` 在仿真启动时采集 DIS interface、DIS exercise/site/application/device config，以及 XIO UDP 连接 target，再通过 dock widget 展示。它是网络配置和运行状态的审计/显示入口，不直接修改仿真状态。

### 100.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkNetworkBrowser::Plugin` | class | `NetworkBrowserPlugin.hpp:21` | Network Browser 插件入口。 |
| `WkNetworkBrowser::SimInterface` | class | `NetworkBrowserSimInterface.hpp:25` | 采集 DIS/XIO 网络配置的仿真接口。 |
| `WkNetworkBrowser::DataContainer` | class | `NetworkBrowserDataContainer.hpp:25` | 网络信息容器。 |
| `WkNetworkBrowser::InitialEvent` | class | `NetworkBrowserSimEvents.hpp:25` | 初始网络信息事件。 |
| `WkNetworkBrowser::DockWidget` | class | `NetworkBrowserDockWidget.hpp:21` | 网络信息 dock。 |

### 100.4 后续深挖点

应沿 `WsfDisInterface::Find()`、`WsfXIO_Extension::Find()` 继续追网络配置来源。当前采集发生在 `SimulationStarting()`，动态网络变更是否需要刷新未在本单元看到证据。

## 101. warlock/plugins/Orbit/source

### 101.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock orbit display） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Orbit/source` |
| source/header 数 | 8 |
| 源文件 | `OrbitPlugin.hpp/.cpp`、`OrbitSimInterface.hpp/.cpp`、`OrbitSimEvents.hpp/.cpp`、`OrbitSimCommands.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因用量/连接限制失败 |

### 101.2 职责说明

`Orbit` 连接 Warlock runtime 与 WKF orbit interface。它在 space platform 初始化后按 mover update interval 调度 orbit update event，监听轨道颜色和机动取消/完成 observer，并在 clock read 阶段周期更新轨道角与月球轨道。

### 101.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkOrbit::Plugin` | class | `OrbitPlugin.hpp:22` | Orbit 插件入口。 |
| `WkOrbit::SimInterface` | class | `OrbitSimInterface.hpp:26` | space mover 和 orbital observer 仿真接口。 |
| `WkOrbit::OrbitEvent` | class | `OrbitSimEvents.hpp:22` | Orbit UI 事件基类。 |
| `WkOrbit::OrbitalElementsUpdateEvent` | class | `OrbitSimEvents.hpp:82` | 平台轨道元素更新事件。 |
| `WkOrbit::RequestOrbitUpdateCommand` | class | `OrbitSimCommands.hpp:24` | 请求立即更新轨道的仿真命令。 |

### 101.4 后续深挖点

应继续沿 `WsfSpaceMoverBase`、`WsfOrbitalEvent` 和 maneuver observer 追空间平台轨道业务逻辑。`SimulationClockRead()` 中 1 秒和 500 秒两个周期也需要结合 UI 刷新和性能需求验证。

## 102. warlock/plugins/Projector/source

### 102.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock sensor projector） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Projector/source` |
| source/header 数 | 8 |
| 源文件 | `ProjectorPlugin.hpp/.cpp`、`ProjectorSimInterface.hpp/.cpp`、`ProjectorSimEvents.hpp/.cpp`、`ProjectorSimCommands.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 因用量/连接限制失败 |

### 102.2 职责说明

`Projector` 为平台传感器添加/移除 terrain projector。插件侧提供上下文菜单和 projector map，仿真侧在传感器开关、模式变化和周期 updater 中提取 sensor beam、EM receiver、rectangular FOV、pitch/yaw/roll/tilt，再通过 UI event 更新地形投影矩阵。

### 102.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `Projector::Plugin` | class | `ProjectorPlugin.hpp:19` | Projector 插件入口。 |
| `Projector::SimInterface` | class | `ProjectorSimInterface.hpp:39` | 传感器 projector updater 仿真接口。 |
| `Projector::SensorState` | struct | `ProjectorSimEvents.hpp:23` | 可投影传感器姿态和 FOV 状态。 |
| `Projector::UpdateEvent` | class | `ProjectorSimEvents.hpp:51` | 传感器 projector 状态更新事件。 |
| `Projector::InstallProjectorUpdaterCommand` | class | `ProjectorSimCommands.hpp:23` | 安装传感器周期 updater 命令。 |

### 102.4 后续深挖点

`OnSensorUpdate()` 和 `CheckProjectability()` 多处使用 `GetAzimuthFieldOfView(emin, emax)` 填充 elevation 范围，疑似应调用 elevation FOV。后续若进入缺陷修复或业务准确性验证，应优先确认该处是否导致 projector 垂直视场错误。

## 103. warlock/plugins/RelativeGeometry/source

### 103.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock 相对几何） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/RelativeGeometry/source` |
| source/header 数 | 8 |
| 源文件 | `RelativeGeometryPlugin.hpp/.cpp`、`RelativeGeometryDialog.hpp/.cpp`、`RelativeGeometryUpdater.hpp/.cpp`、`RelativeGeometryPlotUpdater.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 103.2 职责说明

`RelativeGeometry` 在 Warlock 中提供双平台相对几何查看和绘图。插件通过实体右键菜单创建 dock，`GetUpdater()` 根据 datum 名称创建距离、径向、航迹/交叉航迹、方位、仰角、地面 down/cross range 和 range rate updater。

### 103.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `RelativeGeometry::Plugin` | class | `RelativeGeometryPlugin.hpp:23` | 相对几何插件入口。 |
| `RelativeGeometry::Dialog` | class | `RelativeGeometryDialog.hpp:22` | 相对几何 dock。 |
| `RelativeGeometry::DualPlatformUpdaterT` | class | `RelativeGeometryUpdater.hpp:27` | 双平台 updater 模板。 |
| `RelativeGeometry::LinearRangeUpdater` | class | `RelativeGeometryUpdater.hpp:101` | 直线距离 updater。 |
| `RelativeGeometry::PlotUpdater` | class | `RelativeGeometryPlotUpdater.hpp:21` | 相对几何绘图 updater。 |

### 103.4 后续深挖点

应追 `UtRelativeGeometry::Calculate*` 系列计算函数。当前平台名通过空格拆分复合名，平台名含空格时可能脆弱；右键 item 和双平台更新时间触发也需结合 UI 时序验证。

## 104. warlock/plugins/WsfDraw/source

### 104.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock draw overlay） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/WsfDraw/source` |
| source/header 数 | 8 |
| 源文件 | `WsfDrawPlugin.hpp/.cpp`、`WsfDrawSimInterface.hpp/.cpp`、`WsfDrawSimEvents.hpp`、`WsfDrawObject.hpp/.cpp`、`WkWsfDrawDockWidget.hpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 104.2 职责说明

`WsfDraw` 监听 `WsfDrawManager::DrawUpdate` 和可选 XIO draw packet，将 `WsfDraw::DrawEvent` 转换为 Warlock viewer 图层对象，并提供图层可见性控制和网络 draw 接收开关。

### 104.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkWsfDraw::Plugin` | class | `WsfDrawPlugin.hpp:21` | WsfDraw 插件入口。 |
| `WkWsfDraw::SimInterface` | class | `WsfDrawSimInterface.hpp:25` | draw 仿真接口。 |
| `WkWsfDraw::WsfDrawObject` | class | `WsfDrawObject.hpp:22` | viewer draw object 管理器。 |
| `WkWsfDraw::EventInfo` | struct | `WsfDrawObject.hpp:64` | draw event 元数据。 |
| `WkWsfDraw::DrawEvent` | class | `WsfDrawSimEvents.hpp:40` | draw 更新事件。 |

### 104.4 后续深挖点

应继续追 `WsfDrawObject::AddEvents()` 和顶点转换。`HandleDrawPkt()` 只显式映射前两个顶点的平台索引，多顶点网络绘制和默认关闭的网络 draw 接收开关需要运行验证。

## 105. wizard/plugins/CRDImporter/source

### 105.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard CRD 导入） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/CRDImporter/source` |
| source/header 数 | 8 |
| 源文件 | `CrdImporterPlugin.hpp/.cpp`、`CrdImporterDialog.hpp/.cpp`、`ImportWorker.hpp/.cpp`、`StatusAndResultsDialog.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 105.2 职责说明

`CRDImporter` 从 Wizard Tools 菜单打开导入对话框，收集 `.crd` 输入文件、输出目录、轨道/平台 stub/格式/容差等选项，并通过 `ImportWorker` 调用 `CrdFileImporter::ParseCrdFiles()`。

### 105.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `CrdImporter::Plugin` | class | `CrdImporterPlugin.hpp:19` | CRD Importer 插件入口。 |
| `CrdImporter::Dialog` | class | `CrdImporterDialog.hpp:29` | CRD 导入对话框。 |
| `CrdImporter::ImportWorker` | class | `ImportWorker.hpp:23` | 后台转换 worker。 |
| `StatusAndResults::Dialog` | class | `StatusAndResultsDialog.hpp:18` | 转换状态和结果对话框。 |

### 105.4 后续深挖点

应沿 `CrdFileImporter` 深挖 CRD 语义转换。局部 `ImportWorker` 与 thread 生命周期、目录扫描中的大小写路径处理、取消流程均需进一步确认。

## 106. wsf_plugins/wsf_argo8/argo8/source

### 106.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（ARGO8 外部模型适配） |
| 子系统 | `wsf_plugins/wsf_argo8` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_argo8/argo8/source` |
| source/header 数 | 8 |
| 源文件 | `Argo8Missile.hpp/.cpp`、`Argo8Model.hpp/.cpp`、`Argo8Util.hpp/.cpp`、`Argo8Structs.h`、`Argo8ModelDefs.h` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 106.2 职责说明

`wsf_argo8/argo8` 封装外部 ARGO8 动态库 ABI、模型函数指针、导弹 rail/dynamic/fuze 输入和 flyout 输出。`Argo8Missile::Update()` 是 ARGO8 导弹状态推进与终止状态处理的核心入口。

### 106.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `Argo8Missile` | class | `Argo8Missile.hpp:27` | ARGO8 导弹系统封装。 |
| `Argo8Model` | class | `Argo8Model.hpp:25` | 外部模型封装。 |
| `Argo8Util` | class | `Argo8Util.hpp:25` | ARGO8 工具函数。 |
| `RailData` | struct | `Argo8Structs.h:65` | 发射 rail 输入数据。 |
| `Argo8Output` | struct | `Argo8Structs.h:143` | ARGO8 输出数据。 |

### 106.4 后续深挖点

应继续追 `WsfARGO8_Mover` 与 `Argo8Missile` 的调用边界。未知模型类型、空 `mArgoModel`、macOS 动态库后缀和 `GetFlyout()` 长参数输出方向需要重点验证。

## 107. wsf_plugins/wsf_scenario_analyzer/source

### 107.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（场景规则检查） |
| 子系统 | `wsf_plugins/wsf_scenario_analyzer` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer/source` |
| source/header 数 | 8 |
| 源文件 | `ScenarioAnalyzerPlugin.hpp/.cpp`、`ScenarioAnalyzerPluginRegistration.cpp`、`ScenarioAnalyzerMessage.hpp/.cpp`、`ScenarioAnalyzerUtilities.hpp/.cpp`、`ScenarioFileLocation.hpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 107.2 职责说明

`wsf_scenario_analyzer` 注册 WSF 插件扩展和脚本类型，提供武器数量、传感器开启/链接、track processor purge interval、通信/指挥链、signature、location、速度与 mover 能力等场景健康检查规则。

### 107.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `ScenarioAnalyzerMessage` | class | `ScenarioAnalyzerMessage.hpp:39` | 场景检查消息。 |
| `ScenarioAnalyzerMessage::SeverityLevel` | enum | `ScenarioAnalyzerMessage.hpp:43` | 严重级别。 |
| `ScriptScenarioAnalyzerMessageClass` | class | `ScenarioAnalyzerMessage.hpp:105` | 脚本消息类。 |
| `ScenarioFileLocation` | struct | `ScenarioFileLocation.hpp:44` | 场景文件位置。 |
| `ScenarioAnalyzerExtension` | class | `ScenarioAnalyzerPluginRegistration.cpp:32` | 应用扩展注册器。 |

### 107.4 后续深挖点

这是后续“场景质量规则”分析的高价值入口。`runSuiteCheck()` 的 stdout 输出语义、复杂通信图循环/重复处理和分散的规则阈值需要继续梳理。

## 108. warlock/plugins/Scoreboard/source

### 108.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock weapon scoreboard） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Scoreboard/source` |
| source/header 数 | 9 |
| 源文件 | `ScoreboardPlugin.hpp/.cpp`、`ScoreboardSimInterface.hpp/.cpp`、`ScoreboardSimEvents.hpp/.cpp`、`ScoreboardDataContainer.hpp`、`ScoreboardDialog.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 108.2 职责说明

`Scoreboard` 监听 `WsfObserver::WeaponFired` 和 `WeaponTerminated`，将 fired、hit、kill、miss、in-flight 聚合到 `DataContainer`，并在 dialog 中按 team/platform type/platform name/weapon type 汇总、过滤和导出。

### 108.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkScoreboard::Plugin` | class | `ScoreboardPlugin.hpp:22` | Scoreboard 插件入口。 |
| `WkScoreboard::SimInterface` | class | `ScoreboardSimInterface.hpp:24` | 武器事件仿真接口。 |
| `WkScoreboard::DataContainer` | class | `ScoreboardDataContainer.hpp:107` | 计分数据容器。 |
| `WkScoreboard::WeaponEvent` | struct | `ScoreboardDataContainer.hpp:34` | 武器事件记录。 |
| `WkScoreboard::Dialog` | class | `ScoreboardDialog.hpp:48` | 计分对话框。 |

### 108.4 后续深挖点

应沿 `WsfWeaponEngagement` 继续追终止原因和 damage 语义。仿真完成时清空数据、`GetDamageFactor() == 1.0` 精确比较，以及网络仿真数据有效性需确认。

## 109. wizard/plugins/TablePlotter/source

### 109.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 表格绘图） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/TablePlotter/source` |
| source/header 数 | 9 |
| 源文件 | `TablePlotterPlugin.hpp/.cpp`、`TablePlotterDialog.hpp/.cpp`、`PlotParser.hpp`、`AFSIM_Parser.hpp/.cpp`、`CsvParser.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 109.2 职责说明

`TablePlotter` 解析 AFSIM `regular_table`、`irregular_table`、`curve` 和 CSV 文件，将数据转换为 `UtQtGL2DPlot` 曲线，用于 Wizard 中快速检查表格配置和调参数据。

### 109.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `TablePlotter::Plugin` | class | `TablePlotterPlugin.hpp:19` | Table Plotter 插件入口。 |
| `TablePlotterDialog` | class | `TablePlotterDialog.hpp:25` | 表格绘图对话框。 |
| `PlotParser` | class | `PlotParser.hpp:19` | 绘图解析器基类。 |
| `AFSIM_Parser` | class | `AFSIM_Parser.hpp:43` | AFSIM table/curve 解析器。 |
| `CsvParser` | class | `CsvParser.hpp:20` | CSV 绘图解析器。 |

### 109.4 后续深挖点

应结合真实 table/curve 样例验证错误恢复。`ActionsForCommandContentsRequested` 先创建 dialog 再判断命令、CSV 判断使用 `contains(".csv")`，都存在边界风险。

## 110. warlock/plugins/CreatePlatform/source

### 110.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock runtime platform creation） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/CreatePlatform/source` |
| source/header 数 | 10 |
| 源文件 | `CreatePlatformPlugin.hpp/.cpp`、`CreatePlatformDockWidget.hpp/.cpp`、`CreatePlatformSimInterface.hpp/.cpp`、`CreatePlatformSimCommand.hpp/.cpp`、`CreatePlatformSimEvents.hpp`、`CreatePlatformDataContainer.hpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 110.2 职责说明

`CreatePlatform` 在 Warlock 右侧 dock 中收集平台类型、名称、side、LLA、航向和速度，提交 `CreatePlatformCommand` 到仿真线程；命令 clone 平台类型、设置状态并调用 `WsfSimulation::AddPlatform()`。

### 110.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkCreatePlatform::Plugin` | class | `CreatePlatformPlugin.hpp:21` | Create Platform 插件入口。 |
| `WkCreatePlatform::DockWidget` | class | `CreatePlatformDockWidget.hpp:23` | 创建平台 dock。 |
| `WkCreatePlatform::CreatePlatformCommand` | class | `CreatePlatformSimCommand.hpp:18` | 创建平台仿真命令。 |
| `WkCreatePlatform::DataContainer` | class | `CreatePlatformDataContainer.hpp:22` | 平台类型列表容器。 |
| `WkCreatePlatform::SimInterface` | class | `CreatePlatformSimInterface.hpp:22` | 创建平台仿真接口。 |

### 110.4 后续深挖点

这是 runtime mutation 高价值入口。`CreatePlatformDockWidget::CreatePlatform()` 经纬度校验重复检查 latitude、未校验 longitude；`Clone(mType)` 返回空时后续直接解引用，建议后续修复验证。

## 111. warlock/plugins/OrbitalData/source

### 111.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock orbital data） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/OrbitalData/source` |
| source/header 数 | 10 |
| 源文件 | `OrbitalDataPlugin.hpp/.cpp`、`OrbitalDataContainer.hpp`、`OrbitalDataSimInterface.hpp/.cpp`、`OrbitalDataSimEvents.hpp`、`OrbitalDataUpdaters.hpp/.cpp`、`OrbitalDataPlotUpdaters.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 111.2 职责说明

`OrbitalData` 对 space mover 直接读取轨道状态，对 space-domain DIS mover 从 ECI 位置/速度推导轨道元素，并提供 eccentricity、SMA、inclination、RAAN、argument of periapsis 和 true anomaly 的 updater/plotter。

### 111.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkOrbitalData::Plugin` | class | `OrbitalDataPlugin.hpp:27` | OrbitalData 插件入口。 |
| `WkOrbitalData::DataContainer` | class | `OrbitalDataContainer.hpp:21` | 轨道数据容器。 |
| `WkOrbitalData::OrbitalData` | struct | `OrbitalDataContainer.hpp:27` | 轨道六要素数据。 |
| `WkOrbitalData::SimInterface` | class | `OrbitalDataSimInterface.hpp:26` | 轨道数据仿真接口。 |
| `WkOrbitalData::OrbitalUpdaterT` | class | `OrbitalDataUpdaters.hpp:24` | 轨道 updater 模板。 |

### 111.4 后续深挖点

应对照 batch21 `Orbit` 插件分析显示链差异。`mMutex.tryLock()` 失败会静默跳过本帧；DIS 空间平台由瞬时 ECI 状态推导轨道元素，参考历元和精度需业务确认。

## 112. warlock/plugins/P6DOF_Data/source

### 112.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock P6DOF data） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/P6DOF_Data/source` |
| source/header 数 | 10 |
| 源文件 | `P6DOF_DataPlugin.hpp/.cpp`、`P6DOF_DataContainer.hpp`、`P6DOF_DataSimInterface.hpp/.cpp`、`P6DOF_DataSimEvents.hpp`、`P6DOF_DataUpdaters.hpp/.cpp`、`P6DOF_DataPlotUpdaters.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 112.2 职责说明

`P6DOF_Data` 是旧 P6DOF mover 的飞行状态兼容显示层，采集高度、速度、Mach、姿态、载荷、角速度、气动、燃油、操纵输入、speedbrake、重量和 weight-on-wheels。

### 112.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkP6DOF_Data::Plugin` | class | `P6DOF_DataPlugin.hpp:26` | P6DOF Data 插件入口。 |
| `WkP6DOF_Data::DataContainer` | class | `P6DOF_DataContainer.hpp:21` | P6DOF 数据容器。 |
| `WkP6DOF_Data::PlatformData` | struct | `P6DOF_DataContainer.hpp:27` | P6DOF 平台状态数据。 |
| `WkP6DOF_Data::SimInterface` | class | `P6DOF_DataSimInterface.hpp:25` | P6DOF 数据仿真接口。 |
| `WkP6DOF_Data::P6DOF_UpdaterT` | class | `P6DOF_DataUpdaters.hpp:20` | P6DOF updater 模板。 |

### 112.4 后续深挖点

插件源码标记已被 SixDOF 替代，业务上应避免继续扩展。`Speed_Brake_Extended` 名称和 handle 约定、plot/updater 与 SixDOF 的字段差异需后续对照。

## 113. warlock/plugins/PlatformData/source

### 113.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock platform data） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/PlatformData/source` |
| source/header 数 | 10 |
| 源文件 | `PlatformDataPlugin.hpp/.cpp`、`PlatformDataContainer.hpp`、`PlatformDataSimInterface.hpp/.cpp`、`PlatformDataSimEvents.hpp`、`PlatformDataUpdaters.hpp/.cpp`、`PlatformDataPlotUpdaters.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 113.2 职责说明

`PlatformData` 是通用平台详情基座，采集平台 LLA、速度、Mach、姿态、side/type/domain/index、damage、fuel、DIS id/type/marking、XIO locality 和 aux data，并提供上下文菜单、updater 和 plotter。

### 113.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkPlatformData::Plugin` | class | `PlatformDataPlugin.hpp:27` | PlatformData 插件入口。 |
| `WkPlatformData::PlatformData` | struct | `PlatformDataContainer.hpp:20` | 平台通用状态数据。 |
| `WkPlatformData::SimInterface` | class | `PlatformDataSimInterface.hpp:25` | 平台数据仿真接口。 |
| `WkPlatformData::PlatformUpdater` | class | `PlatformDataUpdaters.hpp:20` | 平台字段 updater。 |
| `WkPlatformData::PlotUpdater` | class | `PlatformDataPlotUpdaters.hpp:24` | 平台数据绘图 updater。 |

### 113.4 后续深挖点

这是后续平台状态业务分析的核心入口。aux data 仅处理 int/double/string/bool，container 和其他 attribute 类型显示为 `unknown_type`；Mach、fuel capacity 等显示策略需结合业务规则确认。

## 114. warlock/plugins/SixDOF_Data/source

### 114.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock SixDOF data） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/SixDOF_Data/source` |
| source/header 数 | 10 |
| 源文件 | `SixDOF_DataPlugin.hpp/.cpp`、`SixDOF_DataContainer.hpp`、`SixDOF_DataSimInterface.hpp/.cpp`、`SixDOF_DataSimEvents.hpp`、`SixDOF_DataUpdaters.hpp/.cpp`、`SixDOF_DataPlotUpdaters.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 114.2 职责说明

`SixDOF_Data` 是当前 SixDOF mover 的平台详情、updater 和 plot 数据源，采集飞行、气动、燃油、操纵、afterburner、speedbrake、重量和 weight-on-wheels 状态。

### 114.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkSixDOF_Data::Plugin` | class | `SixDOF_DataPlugin.hpp:26` | SixDOF Data 插件入口。 |
| `WkSixDOF_Data::DataContainer` | class | `SixDOF_DataContainer.hpp:21` | SixDOF 数据容器。 |
| `WkSixDOF_Data::PlatformData` | struct | `SixDOF_DataContainer.hpp:27` | SixDOF 平台状态数据。 |
| `WkSixDOF_Data::SimInterface` | class | `SixDOF_DataSimInterface.hpp:25` | SixDOF 数据仿真接口。 |
| `WkSixDOF_Data::SixDOF_UpdaterT` | class | `SixDOF_DataUpdaters.hpp:28` | SixDOF updater 模板。 |

### 114.4 后续深挖点

应与 P6DOF 对照字段演进。`GetSpeedBrakePosition()` 的语义是角度还是归一化位置需结合 mover API 确认；高度重复代码也提示后续维护风险。

## 115. warlock/plugins/ZoneBrowser/source

### 115.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock zone browser） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/ZoneBrowser/source` |
| source/header 数 | 10 |
| 源文件 | `ZoneBrowserPlugin.hpp/.cpp`、`ZoneBrowserDockWidget.hpp/.cpp`、`ZoneBrowserSimInterface.hpp/.cpp`、`ZoneBrowserSimCommands.hpp/.cpp`、`ZoneBrowserSimEvents.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 115.2 职责说明

`ZoneBrowser` 在仿真开始时扫描全局 zone 和平台组件 zone，把 `WsfZoneDefinition`、`WsfZoneSet`、`WsfZoneReference` 解释为 WKF zone browser 数据，并监听 fill/line color 变化。

### 115.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkZoneBrowser::Plugin` | class | `ZoneBrowserPlugin.hpp:24` | ZoneBrowser 插件入口。 |
| `WkZoneBrowser::DockWidget` | class | `ZoneBrowserDockWidget.hpp:23` | zone browser dock。 |
| `WkZoneBrowser::SimInterface` | class | `ZoneBrowserSimInterface.hpp:28` | zone 数据仿真接口。 |
| `WkZoneBrowser::ZoneCommand` | class | `ZoneBrowserSimCommands.hpp:22` | zone 命令基类。 |
| `WkZoneBrowser::ZoneEvent` | class | `ZoneBrowserSimEvents.hpp:22` | zone 事件基类。 |

### 115.4 后续深挖点

应确认运行中新建 zone 的覆盖程度。`MakeAuxDataMap()` 会扁平化嵌套 aux data，可能存在同名覆盖语义；颜色命令的 sim/UI 线程时序也需验证。

## 116. wizard/plugins/OSMConverter/source

### 116.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard OSM 转换） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/OSMConverter/source` |
| source/header 数 | 10 |
| 源文件 | `OSMConverterPlugin.hpp/.cpp`、`OSMConverterDialog.hpp/.cpp`、`OSMConverterDataContainer.hpp/.cpp`、`OSMConverterTable.hpp/.cpp`、`OSMConverterCustomWidgets.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 116.2 职责说明

`OSMConverter` 解析 OpenStreetMap XML 的 node/way/tag，按过滤规则生成 AFSIM `route_network` 文本，输出 position、way/node aux_data、intersection node id 和 tag 命中统计。

### 116.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `OsmConverter::Plugin` | class | `OSMConverterPlugin.hpp:20` | OSM Converter 插件入口。 |
| `OSMConverterDialog` | class | `OSMConverterDialog.hpp:21` | OSM 转换对话框。 |
| `OSMConverterDataContainer` | class | `OSMConverterDataContainer.hpp:35` | OSM 数据容器。 |
| `OSMConverterDataContainer::FilterData` | struct | `OSMConverterDataContainer.hpp:47` | OSM 过滤数据。 |
| `OSMConverterTable` | class | `OSMConverterTable.hpp:22` | OSM 表格对话框。 |

### 116.4 后续深挖点

应结合真实 OSM 文件验证输出。`OSMConverterDialog` 使用 `new` 分配 data container 但析构默认；错误信息中若使用 `FindAttribute("id")->Name()` 可能输出属性名而非 id 值；tag 值类型转换需下游解析验证。

## 117. wizard/plugins/PlatformBrowser/source

### 117.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 平台浏览） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/PlatformBrowser/source` |
| source/header 数 | 10 |
| 源文件 | `PlatformBrowserPlugin.hpp/.cpp`、`DockWidget.hpp/.cpp`、`Model.hpp/.cpp`、`Item.hpp/.cpp`、`View.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 117.2 职责说明

`PlatformBrowser` 基于 Wizard parse/proxy 结果展示平台树和组件节点，支持过滤、拖拽 proxy node、打开定义位置，并与 WKF/Warlock 平台选择同步。

### 117.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `PlatformBrowser::Plugin` | class | `PlatformBrowserPlugin.hpp:22` | Platform Browser 插件入口。 |
| `PlatformBrowser::DockWidget` | class | `DockWidget.hpp:33` | 平台浏览 dock。 |
| `PlatformBrowser::Model` | class | `Model.hpp:28` | 平台树模型。 |
| `PlatformBrowser::Item` | class | `Item.hpp:24` | 平台树节点。 |
| `PlatformBrowser::View` | class | `View.hpp:24` | 平台浏览树视图。 |

### 117.4 后续深挖点

`SelectSearchResult()` 和 `Hibernate()` 为空实现，`TryCopy()` 的空选择判断也可疑。后续应结合 UI 流程验证搜索、复制和 stale view 行为。

## 118. wizard/plugins/TypeBrowser/source

### 118.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard 类型浏览） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/TypeBrowser/source` |
| source/header 数 | 10 |
| 源文件 | `TypeBrowserPlugin.hpp/.cpp`、`DockWidget.hpp/.cpp`、`Model.hpp/.cpp`、`Item.hpp/.cpp`、`View.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 118.2 职责说明

`TypeBrowser` 扫描 proxy type map 和场景类型，按 platform、processor、weapon、route、zone、signature、EW 等类型族构建类型树，支持显示未使用类型、过滤、拖拽和定义/文档跳转。

### 118.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `TypeBrowser::Plugin` | class | `TypeBrowserPlugin.hpp:19` | Type Browser 插件入口。 |
| `TypeBrowser::DockWidget` | class | `DockWidget.hpp:29` | 类型浏览 dock。 |
| `TypeBrowser::Model` | class | `Model.hpp:32` | 类型树模型。 |
| `TypeBrowser::Item` | class | `Item.hpp:22` | 类型树节点。 |
| `TypeBrowser::TypeSource` | struct | `Model.hpp:92` | 类型来源信息。 |

### 118.4 后续深挖点

超大场景下全量重建和 1 秒 deferred timer 的性能需验证。`SelectSearchResult()` 未实现，文档 URL 特例也只覆盖部分 EW 名称。

## 119. tools/profiling

### 119.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（profiling 基础设施） |
| 子系统 | `tools/profiling` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/profiling` |
| source/header 数 | 18 |
| 源文件 | `source/ProfilingSystem.hpp/.cpp`、`source/ProfilingHooks.hpp`、`source/ProfilingRegion.hpp/.cpp`、`source/TimedRegion.hpp/.cpp`、`source/ProfilingCommon.hpp`、`source/afperf.cpp`、`source/ProfilingCsvUtil.hpp/.cpp`、`source/ProfilingTimeUtil.hpp/.cpp`、测试源文件等 |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 119.2 职责说明

`tools/profiling` 提供可插拔 profiling ABI、默认 `afperf` hook 实现、动态库版本/符号检查、global hooks 生命周期，以及 `ProfilingRegion`、`TimedRegion` 的 region/section 采样 API。

### 119.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `profiling::ProfilingSystem` | class | `ProfilingSystem.hpp:77` | profiling scope guard 系统。 |
| `profiling::ProfilingSystemArguments` | struct | `ProfilingSystem.hpp:34` | profiling 命令行参数。 |
| `profiling::ProfilingHooks` | struct | `ProfilingHooks.hpp:195` | profiling 动态库 hooks。 |
| `profiling::ProfilingRegion` | class | `ProfilingRegion.hpp:96` | profiling region。 |
| `profiling::TimedRegion` | class | `TimedRegion.hpp:85` | 计时 region。 |

### 119.4 后续深挖点

这是性能分析基础设施，不直接属于仿真业务规则。global hooks、region stack、输出文件是全局状态，文档也提示 region 不支持多线程并发创建；section id 边界和多进程 append 输出需要验证。

## 120. warlock/plugins/DemoMode/source

### 120.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock demo mode） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/DemoMode/source` |
| source/header 数 | 11 |
| 源文件 | `DemoModePlugin.hpp/.cpp`、`DemoModeSimInterface.hpp/.cpp`、`DemoModeSimCommands.hpp`、`DemoModeSimEvents.hpp/.cpp`、`DemoModePrefObject.hpp/.cpp`、`DemoModePrefWidget.hpp/.cpp` |
| 证据 | 主 agent CodeGraph/源码证据；子 agent 只读交叉验证 |

### 120.2 职责说明

`DemoMode` 面向演示运行，按偏好启用/禁用 demo mode，设置仿真 clock rate，在仿真完成后延迟重启最近场景，并可自动选中配置的平台。

### 120.3 核心符号

| 符号 | 类型 | 源码位置 | 中文说明 |
|------|------|----------|----------|
| `WkDemoMode::Plugin` | class | `DemoModePlugin.hpp:32` | DemoMode 插件入口。 |
| `WkDemoMode::SimInterface` | class | `DemoModeSimInterface.hpp:19` | 演示模式仿真接口。 |
| `WkDemoMode::RunSpeedCommand` | class | `DemoModeSimCommands.hpp:20` | 运行速度命令。 |
| `WkDemoMode::DemoModeEvent` | class | `DemoModeSimEvents.hpp:21` | 演示模式事件基类。 |
| `WkDemoMode::PrefData` | struct | `DemoModePrefObject.hpp:19` | 演示模式偏好数据。 |

### 120.4 后续深挖点

快捷键直接修改 enable 状态，是否回写偏好对象/UI 状态需验证；重启逻辑使用 recent scenarios 的 first，排序和失败处理未确认；自动选平台依赖精确平台名匹配。

## 121. warlock/plugins/NetworkLog/source

### 121.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock network log） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/NetworkLog/source` |
| source/header 数 | 11 |
| 核心符号 | `NetworkLog::Plugin`、`NetworkLog::Model`、`NetworkLog::PacketVisitor`、`NetworkLog::PlatformRule`、`NetworkLog::PacketEntry` |

### 121.2 职责说明

`NetworkLog` 是 Warlock 网络包日志插件，负责连接 Warlock network、记录发送/接收/error/reconnect 事件，按平台、side、type、category 和时间过滤，并用 visitor 展开 packet 字段。

### 121.3 后续深挖点

这是 Warlock 网络可观测性入口。后续可沿 `PingPacket`、`AckPacket`、`PacketVisitor` 和网络订阅链路追踪分布式 Warlock 插件如何同步运行态。

## 122. warlock/plugins/WeaponBrowser/source

### 122.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock weapon browser） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/WeaponBrowser/source` |
| source/header 数 | 11 |
| 核心符号 | `WkWeaponBrowser::Plugin`、`DataContainer`、`DockWidget`、`FireCommand`、`WeaponQuantityEvent` |

### 122.2 职责说明

`WeaponBrowser` 是 Warlock 武器浏览与开火控制插件，聚合平台武器数量、平台删除/切换事件，并向仿真线程提交 `FireCommand`。

### 122.3 后续深挖点

这是武器业务的操作侧入口。Phase 3/4 应追踪 `FireCommand::Process` 到 `WsfWeapon`、`WsfWeaponEngagement` 和目标 track 选择逻辑。

## 123. wizard/plugins/CommandChainBrowser/source

### 123.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard command chain browser） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/CommandChainBrowser/source` |
| source/header 数 | 11 |
| 核心符号 | `CommandChain::Plugin`、`DockWidget`、`Model`、`Item`、`View` |

### 123.2 职责说明

`CommandChainBrowser` 是 Wizard 命令链浏览与编辑插件，基于 proxy/parse 结果展示 command chain 树，支持过滤、URL 定位、新建、编辑和拖拽。

### 123.3 后续深挖点

可承接“场景文本 command_chain 如何驱动 Wizard 结构化编辑”的分析；运行时执行语义需要继续追 `core/wsf` command chain。

## 124. tools/tracking_filters/source

### 124.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（tracking filter algorithms） |
| 子系统 | `tools/tracking_filters` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/tracking_filters/source` |
| source/header 数 | 12 |
| 核心符号 | `TrackingFilters::Filter`、`AlphaBetaFilter`、`AlphaBetaGammaFilter`、`KalmanFilter`、`OrbitDeterminationKalmanFilter` |

### 124.2 职责说明

`tracking_filters` 提供 Filter 抽象、alpha-beta、alpha-beta-gamma、线性 Kalman、2D range-bearing Kalman 和轨道确定 Kalman filter。

### 124.3 后续深挖点

这是测量数据到航迹估计的算法入口。后续应追踪 `Initialize`、`ProcessInput`、`Reset`、`Clone`、track score 和协方差输出如何被航迹管理器使用。

## 125. warlock/plugins/SensorController/source

### 125.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock sensor controller） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/SensorController/source` |
| source/header 数 | 12 |
| 核心符号 | `WkSensorController::Plugin`、`DataContainer`、`SensorCommand`、`SlewToTrackCommand`、`SensorEvent` |

### 125.2 职责说明

`SensorController` 是 Warlock 传感器控制插件，展示传感器开关能力、slew 能力和方位/俯仰限制，并提交 turn on/off、按角度 slew、按 track slew 命令。

### 125.3 后续深挖点

这是传感器人工控制业务入口。后续应追 `TurnOnCommand`、`SlewToAzElCommand`、`SlewToTrackCommand` 与 `WsfSensor` 控制 API。

## 126. warlock/plugins/SensorVolumes/source

### 126.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock sensor volumes） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/SensorVolumes/source` |
| source/header 数 | 12 |
| 核心符号 | `WkSensorVolumes::Plugin`、`Platform`、`SensorVolumePacket`、`VolumeUpdateEvent`、`SimInterface` |

### 126.2 职责说明

`SensorVolumes` 管理 Warlock 传感器/武器视场体显示，维护平台 FOV、mode、beam、articulation 数据，并通过网络包同步被动 sensor volume。

### 126.3 后续深挖点

这是传感器视场可视化高价值入口，应与 Mystic `ResultSensorVolumes` 和 WKF `sensor_volume` 偏好对象串联。

## 127. warlock/plugins/TaskAssigner/source

### 127.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock task assigner） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/TaskAssigner/source` |
| source/header 数 | 12 |
| 核心符号 | `WkTaskAssigner::Plugin`、`DataContainer`、`AssignTaskCommand`、`MilAssignJammerTaskCommand`、`TaskUpdateEvent` |

### 127.2 职责说明

`TaskAssigner` 是 Warlock 任务分派插件，汇总平台 command chain、jammer、processor、sensor、weapon 数据，并向仿真提交通用/军用任务分派命令。

### 127.3 后续深挖点

这是任务业务操作侧入口，应追 `AssignTaskCommand`、`MilAssignJammerTaskCommand`、`MilAssignWeaponTaskCommand` 到 `WsfTask` 与 processor 行为。

## 128. warlock/plugins/TaskStatus/source

### 128.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock task status） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/TaskStatus/source` |
| source/header 数 | 12 |
| 核心符号 | `WkTaskStatus::Plugin`、`DataContainer`、`DockWidget`、`CancelTaskCommand`、`TaskUpdateEvent` |

### 128.2 职责说明

`TaskStatus` 是 Warlock 任务状态插件，显示 processor/task 状态，接收 `TaskUpdateEvent`，并向仿真提交 `CancelTaskCommand`。

### 128.3 后续深挖点

这是任务生命周期的状态观察和取消入口，应与 `TaskAssigner`、Wizard `TaskList` 和 `WsfTask` 状态变化串联。

## 129. warlock/plugins/TrackDetailsDisplay/source

### 129.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock track details display） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/TrackDetailsDisplay/source` |
| source/header 数 | 12 |
| 核心符号 | `WkTrackDetailsDisplay::Plugin`、`DataContainer`、`TrackDataExtractor`、`Dialog`、`UpdateEvent` |

### 129.2 职责说明

`TrackDetailsDisplay` 展示平台/本地航迹细节，抽取 track id、local track、平台 track 表、传感器/地理/状态/manager 视图数据。

### 129.3 后续深挖点

这是航迹业务消费侧入口，后续应从 `TrackDataExtractor` 反追 `WsfTrackManager`、local track 和 sensor track 来源。

## 130. wizard/plugins/ProjectBrowser/source

### 130.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard project browser） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/ProjectBrowser/source` |
| source/header 数 | 12 |
| 核心符号 | `ProjectBrowser::Plugin`、`DockWidget`、`Item`、`RootItem`、`View` |

### 130.2 职责说明

`ProjectBrowser` 是 Wizard 项目文件浏览器，管理项目根、外部文件/目录、隐藏根节点、过滤和文件打开/新建动作。

### 130.3 后续深挖点

它支撑场景工程组织，不直接代表仿真业务规则；可作为配置文件定位和项目资源入口。

## 131. wsf_plugins/wsf_brawler/brawler/source

### 131.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules`（Brawler air combat model） |
| 子系统 | `wsf_plugins/wsf_brawler` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_brawler/brawler/source` |
| source/header 数 | 12 |
| 核心符号 | `BrawlerMover`、`BrawlerPlatform`、`BrawlerMIND`、`BrawlerEvaluation`、`BrawlerCoordinateConversion` |

### 131.2 职责说明

`brawler/source` 提供 Brawler 平台、mover、MIND、评估、坐标转换和枚举工具，是 Brawler 空战模型的核心源码片段。

### 131.3 后续深挖点

这是空战机动/评估业务高价值入口，应继续追 `BrawlerMover::Initialize`、`BrawlerPlatform` 状态、`BrawlerMIND` 决策和枚举参数。

## 132. warlock/plugins/CyberEngagementBrowser/source

### 132.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock cyber engagement browser） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/CyberEngagementBrowser/source` |
| source/header 数 | 13 |
| 核心符号 | `WkCyberEngagementBrowser::Plugin`、`DataContainer`、`CyberEvent`、`SimInterface`、`CyberEngagementEvent` |

### 132.2 职责说明

`CyberEngagementBrowser` 是 Warlock 网络/赛博交战事件浏览插件，缓存 cyber event、仿真完成事件和显示偏好。

### 132.3 后续深挖点

这是 cyber 结果消费入口，应与 `core/wsf_cyber`、Mystic `ResultDataCyber` 和 `InteractionDb` 生产链串联。

## 133. warlock/plugins/P6DOF_Tuner/source

### 133.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock P6DOF tuner） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/P6DOF_Tuner/source` |
| source/header 数 | 13 |
| 核心符号 | `WkTuner::Plugin`、`MainWidget`、`SimInterface`、`Gui2SimData`、`WriteDataEvent` |

### 133.2 职责说明

`P6DOF_Tuner` 是 Warlock P6DOF 调参插件，提供主面板、命令对话框、偏好、PID 标志、GUI/仿真数据交换和事件写回。

### 133.3 后续深挖点

这是 P6DOF 飞行动力学调参入口，应追 `Gui2SimData`、`GuiAutoTuneCommand`、`WriteDataEvent` 与 p6dof vehicle/controller 的交互。插件描述已标注 deprecated，后续应优先与 SixDOF 调参链路对照。

## 134. wizard/plugins/TaskList/source

### 134.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Wizard task list） |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/TaskList/source` |
| source/header 数 | 13 |
| 核心符号 | `TaskList::Plugin`、`DockWidget`、`Task`、`Item`、`PrefObject` |

### 134.2 职责说明

`TaskList` 是 Wizard TODO/问题任务列表插件，聚合 parse 结果、文本源路径、任务项、过滤列和偏好显示。

### 134.3 后续深挖点

它主要服务开发/场景编辑诊断，不是运行时任务业务本身；可辅助定位脚本/配置中的任务注释或解析问题。

## 135. tools/wkf/plugins/CoverageOverlay/source

### 135.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools`（WKF coverage overlay） |
| 子系统 | `tools/wkf/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/CoverageOverlay/source` |
| source/header 数 | 14 |
| 核心符号 | `CoverageOverlay::Plugin`、`CoverageData`、`CoverageDataManager`、`CoverageDataReader`、`HeatmapOverlay` |

### 135.2 职责说明

`CoverageOverlay` 是 WKF 覆盖分析热力图叠加插件，读取 `.cvg` 覆盖数据，构建 coverage data、heatmap fields 和 OSG overlay。

### 135.3 后续深挖点

这是 coverage 结果消费入口，后续可沿 `CoverageDataReader` 反追 `wsf_coverage` 输出格式和 coverage 业务指标。

## 136. warlock/plugins/Astrolabe/source

### 136.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock Astrolabe） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Astrolabe/source` |
| source/header 数 | 14 |
| 核心符号 | `WkAstrolabe::Plugin`、`DockWidget`、`SimInterface`、`VerifyMissionCommand`、`MissionVerifier` |

### 136.2 职责说明

`Astrolabe` 是 Warlock 轨道任务序列插件，提供空间平台可用性、任务验证、注入、取消 maneuver、创建 mission sequence 的 UI/仿真桥。

### 136.3 后续深挖点

这是空间任务业务高价值入口，应追 `InjectMissionSequenceCommand`、`VerifyMissionCommand`、`MissionVerifier` 与 `WsfSpaceMoverBase`/mission sequence。

## 137. warlock/plugins/PlatformPartBrowser/source

### 137.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock platform part browser） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/PlatformPartBrowser/source` |
| source/header 数 | 14 |
| 核心符号 | `WkPlatformPartBrowser::Plugin`、`DataContainer`、`ChangePartCommand`、`PartUpdateEvent`、`PlatformPart` |

### 137.2 职责说明

`PlatformPartBrowser` 是平台 part 浏览与属性变更插件，抽象 part 类型、属性名、数据容器，并通过 `ChangePartCommand` 修改平台 part 状态。

### 137.3 后续深挖点

这是平台组件、传感器、雷达和运动部件状态修改入口，应继续追 `ChangePartCommand` 对 `WsfPlatformPart`、`WsfRadarSensor`、`WsfMover` 的影响。

## 138. warlock/plugins/SatelliteTether/source

### 138.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications`（Warlock satellite tether） |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/SatelliteTether/source` |
| source/header 数 | 14 |
| 核心符号 | `SatelliteTether::Plugin`、`DockWidget`、`PropagationManager`、`AddTrackCommand`、`SatelliteTetherEvent` |

### 138.2 职责说明

`SatelliteTether` 是 Warlock 卫星 tether 视图插件，创建 dock、轨道 propagator、attachment trace，并用事件同步轨道颜色、track 和 initial epoch。

### 138.3 后续深挖点

这是空间轨迹/卫星可视化入口，应与 Mystic `ResultSatelliteTether`、WKF `TetherView` 和 `WsfOrbitalEvent` 生产链串联。

## 139. warlock/plugins/SixDOF_Tuner/source

### 139.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/SixDOF_Tuner/source` |
| source/header 数 | 14 |
| 核心符号 | `wkf::WkSixDOF_Tuner::CommandDialog`、`WkSixDOF_Tuner::Plugin`、`six_dof::WkSixDOF_Tuner::SimInterface`、`six_dof::WkSixDOF_Tuner::WriteDataEvent`、`wkf::WkSixDOF_Tuner::MainWidget` |

### 139.2 职责说明

Warlock SixDOF 调参 UI、仿真桥和控制事件入口。

### 139.3 后续深挖点

SixDOF 调参与运行时控制入口，后续应追 six_dof vehicle/controller 与调参命令。

## 140. warlock/plugins/Tracks/source

### 140.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Tracks/source` |
| source/header 数 | 14 |
| 核心符号 | `WkTracks::PlatformTracksRequestCommand`、`wkf::WkTracks::Plugin`、`WkTracks::SimInterface`、`WkTracks::AllTracksRequestCommand`、`WkTracks::TeamTracksRequestCommand` |

### 140.2 职责说明

Warlock tracks 显示、track state 更新和平台航迹消费入口。

### 140.3 后续深挖点

航迹显示消费侧入口，后续应与 track db 和 sensor/local track 消息生产链串联。

## 141. warlock/plugins/WsfPrompt/source

### 141.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/WsfPrompt/source` |
| source/header 数 | 14 |
| 核心符号 | `WkWsfPrompt::Plugin`、`WkWsfPrompt::SimInterface`、`WkWsfPrompt::PromptDialog`、`WkWsfPrompt::PauseCommand`、`WkWsfPrompt::ResumeCommand` |

### 141.2 职责说明

Warlock WSF prompt/命令输入插件，提供运行时命令交互入口。

### 141.3 后续深挖点

运行时命令侧入口，后续应追 prompt command 如何进入 sim/script 解释链。

## 142. wizard/plugins/RouteBrowser/source

### 142.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/RouteBrowser/source` |
| source/header 数 | 14 |
| 核心符号 | `RouteBrowser::RouteBrowserCreateDialog`、`RouteBrowser::RouteBrowserEditDialog`、`wizard::RouteBrowser::RouteBrowserInterface`、`RouteBrowser::CreateGlobalRouteDialog`、`RouteBrowser::Plugin` |

### 142.2 职责说明

Wizard route browser，提供路线对象浏览、选择和编辑辅助。

### 142.3 后续深挖点

场景 route 配置消费/编辑入口，后续应与 MapRoute、route parser 和 platform route 绑定逻辑串联。

## 143. wizard/plugins/ScenarioAnalyzer/source

### 143.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/ScenarioAnalyzer/source` |
| source/header 数 | 14 |
| 核心符号 | `ScenarioAnalyzer::ScenarioAnalyzerPlugin`、`ScenarioAnalyzer::Plugin`、`ScenarioAnalyzer::ScenarioAnalyzerPluginRegistration`、`ScenarioAnalyzer::ExpandingResultsGroupModel`、`ScenarioAnalyzer::ResultsTreeView` |

### 143.2 职责说明

Wizard scenario analyzer 插件，承接场景分析脚本、检查结果和 UI 展示。

### 143.3 后续深挖点

场景静态分析入口，后续应追注册脚本类型和检查器输出。

## 144. wsf_plugins/wsf_multiresolution/source

### 144.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules` |
| 子系统 | `wsf_plugins/wsf_multiresolution` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_multiresolution/source` |
| source/header 数 | 14 |
| 核心符号 | `RvPlatformHistory::Plugin`、`RvPlatformHistory::StateData`、`RvPlatformHistory::TracelineData`、`RvPlatformHistory::WingRibbonData`、`RvPlatformHistory::BehaviorStateData` |

### 144.2 职责说明

WSF multiresolution 插件源码，处理多分辨率模型扩展与注册。

### 144.3 后续深挖点

模型分辨率/聚合行为入口，后续应追 extension 注册和 scenario 输入参数。

## 145. mystic/plugins/ResultPlatformHistory/source

### 145.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultPlatformHistory/source` |
| source/header 数 | 15 |
| 核心符号 | `WsfBrawler`、`WsfBrawlerProcessor`、`WsfBrawlerMover`、`WsfBrawlerFuel`、`WsfBrawlerConsicousnessEvent` |

### 145.2 职责说明

Mystic 平台历史结果视图，消费平台历史轨迹/状态。

### 145.3 后续深挖点

结果平台历史消费入口，后续应追 ResultPlatform 时间序列字段来源。

## 146. wsf_plugins/wsf_brawler/source

### 146.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules` |
| 子系统 | `wsf_plugins/wsf_brawler` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_brawler/source` |
| source/header 数 | 15 |
| 核心符号 | `Joystick::Plugin`、`Joystick::SimInterface`、`Joystick::ActivatePilotCommand`、`Joystick::ControlCommand`、`Joystick::JoystickDataContainer` |

### 146.2 职责说明

WSF Brawler 插件适配层，承接 Brawler 模型注册和仿真集成。

### 146.3 后续深挖点

空战 Brawler 模型入口，后续应与 brawler/source 的 mover/MIND/评估逻辑串联。

## 147. warlock/plugins/Joystick/source

### 147.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Joystick/source` |
| source/header 数 | 16 |
| 核心符号 | `Engage::Plugin`、`Engage::Dialog`、`Engage::TableWidget`、`Engage::TableRow`、`Engage::OutputItem` |

### 147.2 职责说明

Warlock joystick 插件，提供外部操纵输入到仿真控制的桥接。

### 147.3 后续深挖点

人为操纵/控制输入入口，后续应追 joystick command/event 对 platform/mover 的影响。

## 148. wizard/plugins/Engage/source

### 148.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/Engage/source` |
| source/header 数 | 16 |
| 核心符号 | `Configuration`、`Options`、`Report`、`CommunicationReport`、`DetectionReport` |

### 148.2 职责说明

Wizard Engage 插件，提供交战相关场景配置/展示入口。

### 148.3 后续深挖点

交战配置侧入口，后续应与 engage/source 和 weapon engagement 事件生产链对齐。

## 149. post_processor/lib/source

### 149.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `post_processor/lib` |
| 最小目录单元 | `afsim-2_9/swdev/src/post_processor/lib/source` |
| source/header 数 | 17 |
| 核心符号 | `RvTimeController::Plugin`、`RvTimeController::Interface`、`RvTimeController::Toolbar`、`RvTimeController::StatusWidget`、`RvTimeController::BookmarkBrowser` |

### 149.2 职责说明

post_processor 公共库，提供结果后处理、报表和数据处理支撑。

### 149.3 后续深挖点

后处理基础库入口，后续按调用者追具体业务指标。

## 150. mystic/plugins/ResultTimeController/source

### 150.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultTimeController/source` |
| source/header 数 | 18 |
| 核心符号 | `RvTimeController::Plugin`、`RvTimeController::Interface`、`RvTimeController::Toolbar`、`RvTimeController::StatusWidget`、`RvTimeController::BookmarkBrowser` |

### 150.2 职责说明

Mystic 结果时间控制插件，驱动结果播放时间、速率和 UI 同步。

### 150.3 后续深挖点

结果回放控制入口，后续应与 ResultDb 时钟、平台插值和播放状态串联。

## 151. tools/vespatk/vespatk_qt/source

### 151.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `tools/vespatk` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/vespatk/vespatk_qt/source` |
| source/header 数 | 18 |
| 核心符号 | `vespa::VaWidget`、`vespa::VaOverlayMapGrid`、`vespa::VaOverlayMapRings`、`vespa::VaDecoratorNode`、`vespa::AngleEntry` |

### 151.2 职责说明

VESPA Qt 工具层，提供 Qt/OpenGL 嵌入 OSG/VESPA viewer、地图网格/测距环 overlay、decorator 和 scenegraph 浏览器。

### 151.3 后续深挖点

VESPA 工具 UI 入口，后续重点检查 observer 生命周期、相机更新几何和跨日期线/单位切换。

## 152. warlock/plugins/PlatformMovement/source

### 152.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/PlatformMovement/source` |
| source/header 数 | 18 |
| 核心符号 | `WkPlatformMovement::Plugin`、`WkPlatformMovement::RouteBrowserInterface`、`WkPlatformMovement::SimInterface`、`vespa::WkPlatformMovement::RouteEvent`、`WkPlatformMovement::Command` |

### 152.2 职责说明

Warlock 平台移动插件，提供路线浏览/编辑以及 altitude/location/speed/heading/route 等仿真命令。

### 152.3 后续深挖点

高价值运行时 mutation 入口，后续应追 PlatformMovementSimCommands 对平台 mover/route 的具体修改。

## 153. warlock/plugins/DialogBuilder/source

### 153.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/DialogBuilder/source` |
| source/header 数 | 19 |
| 核心符号 | `WkDialogBuilder::Plugin`、`WkDialogBuilder::DockWidget`、`WkDialogBuilder::MainDialog`、`WkDialogBuilder::DialogDef`、`WkDialogBuilder::ScriptCreator` |

### 153.2 职责说明

Warlock 动态对话框构建插件，支持自定义脚本按钮、参数、过滤器、快捷键和返回值展示。

### 153.3 后续深挖点

脚本执行 UI 入口，后续应追 HandleScriptExecution、BuildScriptInstance、ExecuteScriptInstance 的权限和参数链。

## 154. wizard/plugins/ModelImport/source

### 154.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/ModelImport/source` |
| source/header 数 | 19 |
| 核心符号 | `ModelImport::Plugin`、`ModelImport::DockWidget`、`ModelImport::DirectoryReaderThread`、`ModelImport::FileData`、`ParserLite::FileInput` |

### 154.2 职责说明

Wizard 模型导入器，扫描模型目录、生成/读取 JSON 元数据、递归导入文件及依赖。

### 154.3 后续深挖点

资源导入入口，后续应复核 ImportRecursionHelper 拷贝条件和后台解析线程数据所有权。

## 155. core/wsf_util/source

### 155.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework` |
| 子系统 | `core/wsf_util` |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_util/source` |
| source/header 数 | 20 |
| 核心符号 | `UtPackSchema`、`UtBuffer`、`UtPackSerializer`、`UtPackMessageStream`、`UtmlObject` |

### 155.2 职责说明

WSF utility 小源码单元，提供 UtPack、UTML、字节缓冲、CSV、tar 打包和 SHA digest 等基础工具。

### 155.3 后续深挖点

通用工具入口，后续重点看 UtPack schema/layout 同步和 UtBuffer 边界调用责任。

## 156. mystic/plugins/ResultBehaviorAnalysisTool/source

### 156.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `mystic/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/plugins/ResultBehaviorAnalysisTool/source` |
| source/header 数 | 21 |
| 核心符号 | `RvBAT::Plugin`、`rv::RvBAT::DockWindow`、`rv::RvBAT::Interface`、`RvBAT::ABTScene`、`RvBAT::FSMScene` |

### 156.2 职责说明

Mystic 行为分析结果工具，读取 ABT/FSM 消息并构建 QGraphicsScene 展示节点、状态、转换和 blackboard。

### 156.3 后续深挖点

行为分析消费侧入口，后续应追 ABT/FSM 消息生产端和大图布局性能。

## 157. tools/scene_gen/source

### 157.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `tools/scene_gen` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/scene_gen/source` |
| source/header 数 | 21 |
| 核心符号 | `sceneGen::SceneGenPlatformTeam`、`sceneGen::SceneGenPlatformGroup`、`sceneGen::SceneGenInputFileReader`、`sceneGen::SceneGenInputData`、`sceneGen::SceneGenGeoPathGen` |

### 157.2 职责说明

scene_gen 命令行工具，从输入场景描述读取平台组并生成平台布局脚本和 startup 脚本。

### 157.3 后续深挖点

场景生成工具入口，后续应追输出脚本格式、路径拼接和命令行缺参边界。

## 158. warlock/plugins/Chat/source

### 158.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/Chat/source` |
| source/header 数 | 21 |
| 核心符号 | `Chat::Plugin`、`Chat::SimInterface`、`Chat::DockWidget`、`Chat::ChatCommand`、`Chat::Network` |

### 158.2 职责说明

Warlock chat 插件，管理聊天 UI、频道/分组、网络包收发，并映射到仿真 command/event pipe。

### 158.3 后续深挖点

用户消息入口，后续应复核 roll call/channel 字段、网络来源信任和链接解析。

## 159. tools/wkf/plugins/MapDisplay/source

### 159.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `tools/wkf/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/plugins/MapDisplay/source` |
| source/header 数 | 22 |
| 核心符号 | `wkf::Map::Plugin`、`wkf::Map::DockWidget`、`Map::OverlayScale`、`vespa::Map::CameraMotion`、`wkf::Map::ToolBar` |

### 159.2 职责说明

WKF map display 插件，提供通用 3D 地图、viewer、toolbar、cursor status、测距尺和实体菜单。

### 159.3 后续深挖点

地图显示基础入口，后续应沿 viewer/overlay、选择删除和拖放打开文件路径继续追。

## 160. warlock/plugins/SimController/source

### 160.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/SimController/source` |
| source/header 数 | 22 |
| 核心符号 | `WkSimController::Plugin`、`WkSimController::SimControllerEvent`、`WkSimController::SimInterface`、`WkSimController::PauseCommand`、`wkf::WkSimController::Toolbar` |

### 160.2 职责说明

Warlock 仿真控制插件，处理加载场景、暂停/继续/终止/重启、时钟速率和落后状态。

### 160.3 后续深挖点

高价值仿真生命周期入口，后续应追 SimControllerSimCommands/Events 与 DIS/XIO 联机控制。

## 161. wizard/plugins/MapUtils/source

### 161.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/MapUtils/source` |
| source/header 数 | 22 |
| 核心符号 | `RotateScenario::TranslateScenario::Plugin`、`MapUtils::Message`、`MapUtils::ScenarioTransformation::DialogMenuAndButtonsWidget`、`MapUtils::PluginUtil::LineEditSliderManager`、`ScenarioTransformation::RotateScenario::Dialog` |

### 161.2 职责说明

Wizard 地图辅助工具，支持创建/克隆/删除平台、场景/实体旋转平移和 ghost 预览。

### 161.3 后续深挖点

场景编辑 mutation 入口，后续应复核 Apply*Change 类型判断、route waypoint size 和撤销路径。

## 162. wizard/plugins/SimulationManager/source

### 162.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/SimulationManager/source` |
| source/header 数 | 22 |
| 核心符号 | `wizard::SimulationManager::Plugin`、`SimulationManager::Toolbar`、`wizard::SimulationManager::WsfScriptDebugger`、`wizard::SimulationManager::OutputDock`、`SimulationManager::ScriptBreakpointControl` |

### 162.2 职责说明

Wizard 仿真执行与调试插件，管理 WSF executable、运行/调试/停止/重启、输出面板、断点/调用栈/watch。

### 162.3 后续深挖点

仿真启动配置入口，后续应复核 NewExecution 参数 quoting、输出链接打开和 XIO debug 生命周期。

## 163. wsf_plugins/wsf_fires/source

### 163.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules` |
| 子系统 | `wsf_plugins/wsf_fires` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_fires/source` |
| source/header 数 | 22 |
| 核心符号 | `Fires::FiresTables`、`Fires::FiresTableLoader`、`Fires::BallisticPath`、`Fires::FiresLaunchComputer`、`Fires::FiresMover` |

### 163.2 职责说明

WSF fires 插件源码，注册火力扩展、弹道表、launch computer、fires mover 和 DIS observer。

### 163.3 后续深挖点

火力业务入口，后续应追 FiresMover/FiresPath/FiresLaunchComputer 的发射与弹道计算链。

## 164. core/wsf_ripr/source

### 164.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework` |
| 子系统 | `core/wsf_ripr` |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_ripr/source` |
| source/header 数 | 24 |
| 核心符号 | `wizard::EventOutput::Plugin`、`wizard::EventOutput::Dialog`、`wizard::EventOutput::editor::Editor`、`wizard::EventOutput::tokenizer::Tokenizer`、`wizard::EventOutput::event::Widget` |

### 164.2 职责说明

WSF RIPR 协作任务框架，管理 processor、任务板、投标/分配/进度、脚本 API 和 XIO 同步。

### 164.3 后续深挖点

外部协作/任务分配入口，后续重点复核 JobBoard 所有权、processor 判空和 XIO 同步边界。

## 165. wizard/plugins/EventOutput/source

### 165.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/EventOutput/source` |
| source/header 数 | 24 |
| 核心符号 | `WkP6DOF_Controller::Plugin`、`WkP6DOF_Controller::PluginObject`、`WkP6DOF_Controller::SimInterface`、`WkP6DOF_Controller::P6DOF_ControllerDataContainer`、`WkP6DOF_Controller::HUD` |

### 165.2 职责说明

Wizard event output 插件，用图形化方式编辑 csv_event_output/event_output block 并写回文本。

### 165.3 后续深挖点

事件输出配置入口，后续应复核 tokenizer/editor 写回、右键 connect 和空 current file。

## 166. warlock/plugins/P6DOF_Controller/source

### 166.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/plugins/P6DOF_Controller/source` |
| source/header 数 | 26 |
| 核心符号 | `WkP6DOF_Controller::Plugin`、`WkP6DOF_Controller::PluginObject`、`WkP6DOF_Controller::SimInterface`、`WkP6DOF_Controller::P6DOF_ControllerDataContainer`、`WkP6DOF_Controller::HUD` |

### 166.2 职责说明

Warlock deprecated P6DOF 飞行控制插件，连接 P6DOF 平台、SDL 输入、HUD/音频和 sim bridge。

### 166.3 后续深挖点

旧 P6DOF 控制入口，后续与 Joystick/HeadUpView/SixDOF_Tuner 对照。

## 167. weapon_tools/source

### 167.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `weapon_tools` |
| 最小目录单元 | `afsim-2_9/swdev/src/weapon_tools/source` |
| source/header 数 | 26 |
| 核心符号 | `ToolManager`、`Tool`、`WeaponToolsExtension`、`WeaponObserver`、`TargetMover` |

### 167.2 职责说明

weapon_tools 应用入口，加载扩展、处理输入、驱动 WsfEventStepSimulation，并批量生成武器工具输出。

### 167.3 后续深挖点

武器工具高价值入口，后续应追 ToolManager、Tool、LaunchComputer generator 和主循环结束条件。

## 168. tools/wkf/comm_vis/wkf_comm_vis_common/source

### 168.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `tools/wkf/comm_vis` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/comm_vis/wkf_comm_vis_common/source` |
| source/header 数 | 29 |
| 核心符号 | `MTT`、`WsfMTT_Interface`、`WsfMTT_Correlation`、`WsfMTT_Fusion`、`MTT_ActiveTrack` |

### 168.2 职责说明

WKF 通信可视化公共组件，缓存通信事件，构建节点/链路并动画显示 packet/hop。

### 168.3 后续深挖点

通信拓扑/packet 可视化公共入口，后续可与 Warlock/Mystic/Wizard CommVis 生产消费链合并。

## 169. core/wsf_mtt/source

### 169.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework` |
| 子系统 | `core/wsf_mtt` |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_mtt/source` |
| source/header 数 | 30 |
| 核心符号 | `WsfSA_Processor`、`WsfSA_Perceive`、`WsfSA_Assess`、`WsfSA_Predict`、`WsfAirCombatTypeManager` |

### 169.2 职责说明

WSF multi-target tracking 源码单元，处理多目标跟踪基础能力。

### 169.3 后续深挖点

高价值 tracking 业务入口，后续应追 track update/filter/fusion 调用链。

## 170. wsf_plugins/wsf_air_combat/source

### 170.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules` |
| 子系统 | `wsf_plugins/wsf_air_combat` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_air_combat/source` |
| source/header 数 | 31 |
| 核心符号 | `WizCommVis::Plugin`、`WizCommVis::CommVisDialog`、`WizCommVis::CommVisEditDialog`、`WizCommVis::CommVisAddCommDialog`、`WizCommVis::CommVisRouterNodeDialog` |

### 170.2 职责说明

WSF air combat 插件源码，承接空战模型扩展和注册。

### 170.3 后续深挖点

高价值空战业务入口，后续应与 ResultDataAirCombat、Brawler 和 SA 生产链串联。

## 171. wizard/plugins/CommVis/source

### 171.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/CommVis/source` |
| source/header 数 | 32 |
| 核心符号 | `artificer::V1Parser`、`artificer::V1PrototypeSummarizer`、`artificer::RunData`、`artificer::SimulationData`、`artificer::TextTable` |

### 171.2 职责说明

Wizard CommVis 插件，提供通信可视化配置/编辑入口。

### 171.3 后续深挖点

通信可视化配置入口，后续与 WKF common、Warlock/Mystic CommVis 串联。

## 172. tools/artificer/source

### 172.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `tools/artificer` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/artificer/source` |
| source/header 数 | 34 |
| 核心符号 | `SPLAT::Plugin`、`SPLAT::SensorAnalysisDialog`、`SPLAT::ProxyInterface`、`SPLAT::PlotOptionsDialog`、`SPLAT::PlotOptionsWidget` |

### 172.2 职责说明

Artificer 工具源码，提供模型/场景工件生成或编辑支持。

### 172.3 后续深挖点

工具生成入口，后续按输出类型追到场景或资源消费方。

## 173. wizard/plugins/SPLAT/source

### 173.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/SPLAT/source` |
| source/header 数 | 40 |
| 核心符号 | `WsfSensorPlotExtension`、`Function`、`MapPlotFunction`、`MapPlotVariables`、`Sensor` |

### 173.2 职责说明

Wizard SPLAT 插件，提供地形/传播/覆盖相关工具入口。

### 173.3 后续深挖点

传播/地形辅助入口，后续应与 sensor plot、coverage 或地形数据库调用链对齐。

## 174. core/sensor_plot_lib/source

### 174.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework` |
| 子系统 | `core/sensor_plot_lib` |
| 最小目录单元 | `afsim-2_9/swdev/src/core/sensor_plot_lib/source` |
| source/header 数 | 41 |
| 核心符号 | `WsfSensorPlotExtension`、`Function`、`MapPlotFunction`、`MapPlotVariables`、`Sensor` |

### 174.2 职责说明

sensor_plot_lib 核心库，提供传感器图/覆盖绘制与计算支撑。

### 174.3 后续深挖点

高价值传感器可视化/覆盖入口，后续应追 sensor volumes、projector 和 coverage 生产链。

## 175. wizard/plugins/PartManager/source

### 175.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/PartManager/source` |
| source/header 数 | 43 |
| 核心符号 | `PartManager::Plugin`、`PartManager::Browser`、`PartManager::Widget`、`PartManager::WidgetFactory`、`PartManager::AddPlatformPart` |

### 175.2 职责说明

Wizard PartManager 插件，用于浏览、添加和编辑平台 part、sensor、articulated part 及其属性控件。

### 175.3 后续深挖点

场景平台部件编辑入口，后续应追 `PartManager::Plugin::ActionsForNodeRequested` → `ManagePlatformParts::operator()` → `Browser::OpenLink/CreateWidget` → `WidgetFactory::CreateUi` → `Widget/SingleAttribute` 的 proxy/source range 文本写回链。

## 176. tools/packetio/source

### 176.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `tools/packetio` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/packetio/source` |
| source/header 数 | 48 |
| 核心符号 | `PakPacket`、`PakConnection`、`PakI`、`PakO`、`PakSerialization::Serialize` |

### 176.2 职责说明

packetio 工具库，提供 packet、archive、buffer、socket reactor 和模板序列化基础设施。

### 176.3 后续深挖点

二进制包/网络序列化入口，后续应追 `PakProcessor::RegisterPacket/ReadPacket/ProcessPacket`、`PakTCP_IO`/`PakUDP_IO` 收发、`PakSocketReactor` 事件循环、`PakThreadedIO` 接收队列和 `PakSerialize` 模板序列化链。

## 177. engage/source

### 177.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `engage` |
| 最小目录单元 | `afsim-2_9/swdev/src/engage/source` |
| source/header 数 | 45 |
| 核心符号 | `engage::Simulation`、`engage::TaskManager`、`engage::Events`、`engage::EventItem`、`engage::Task` |

### 177.2 职责说明

Engage 核心源码，提供 frame-step simulation、任务管理、事件采集、输出和传感器/武器交战事件模型。

### 177.3 后续深挖点

交战业务高价值入口，后续应追 `main` → `TaskManager::Execute` → `Task::Execute` → `RunConfig::CreatePlatforms` → `Simulation::AdvanceTime/SimulationExtension` observer callbacks → `TaskOutput` 的批运行与输出链。

## 178. wsf_plugins/wsf_sosm/sosm/source

### 178.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules` |
| 子系统 | `wsf_plugins/wsf_sosm` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_sosm/sosm/source` |
| source/header 数 | 45 |
| 核心符号 | `SOSM_Manager`、`SOSM_Sensor`、`SOSM_SensorTarget`、`SOSM_Atmosphere`、`SOSM_Interaction` |

### 178.2 职责说明

SOSM 传感器/目标/大气/光谱交互模型源码，支撑 WSF SOSM 探测仿真。

### 178.3 后续深挖点

传感器探测业务高价值入口，后续应追 `SOSM_Manager::ProcessInput/Load*Type` → `SOSM_SensorTarget::Initialize` → `ComputeTargetIrradiance` → `SOSM_Sensor::ComputeProbabilityOfDetection`，并验证 atmosphere/target/interaction 表缓存。

## 179. mystic/lib/source

### 179.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `mystic` |
| 最小目录单元 | `afsim-2_9/swdev/src/mystic/lib/source` |
| source/header 数 | 52 |
| 核心符号 | `rv::PluginT`、`rv::RunManager`、`rv::EventThread`、`rv::TrackDb`、`rv::ResultMessageArray` |

### 179.2 职责说明

Mystic 公共库，提供 result viewer 插件基类、run manager、event thread、track db、plotting/startup/preference 等基础设施。

### 179.3 后续深挖点

结果查看基础设施入口，后续应追 `Factory::UserOpenFile` → `rv::Environment::OpenEventRecording` → `RvWsfPipe::FileStreamer` → `ResultDb::ProcessOneTimeMessage` → `rv::PluginT` 插件事件分发和 `ResultPlatform/TrackDb/InteractionDb` 查询链。

## 180. wizard/plugins/SpaceTools/source

### 180.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `wizard/plugins` |
| 最小目录单元 | `afsim-2_9/swdev/src/wizard/plugins/SpaceTools/source` |
| source/header 数 | 52 |
| 核心符号 | `SpaceTools::Plugin`、`SpaceTools::Astrolabe`、`SpaceTools::ConstellationMaker`、`SpaceTools::SatelliteInserterDialog`、`SpaceTools::SatelliteInserterModel` |

### 180.2 职责说明

Wizard SpaceTools 插件，提供 Astrolabe、constellation maker、satellite inserter、TLE 和轨道尺寸/起始时间 UI。

### 180.3 后续深挖点

空间场景编辑入口，后续应追 `SpaceTools::Plugin` 菜单/上下文注册、`Astrolabe` mission sequence 读写、`InputReader/InputWriter`、`OrbitalSequenceToInput`、`ConstellationMaker` 和 `SatelliteInserterHandler` 写回链。

## 181. wsf_plugins/wsf_iads_c2_lib/iadsLib/source

### 181.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules` |
| 子系统 | `wsf_plugins/wsf_iads_c2_lib` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_iads_c2_lib/iadsLib/source` |
| source/header 数 | 54 |
| 核心符号 | `VclInterceptCalculator::CanIntercept`、`assetRecord::calculateAssignmentDelays`、`unclassifiedBattleManager::run`、`unclassifiedBattleManager::PerformWeaponPairings`、`weaponsManagerAI::Clone` |

### 181.2 职责说明

IADS C2 库实现层，包含 asset/track/weapon/zone/message 记录、weapon pairing、battle manager 和 intercept 计算。

### 181.3 后续深挖点

防空 C2/武器分配高价值入口，后续应追 `AssetManagerInterface::processMessage` → `PrepareTracksForEvaluation` → `unclassifiedBattleManager::run` → `PerformWeaponPairings/AssignWeapons` → `DisseminateC2Interface::updateOutgoingMessages` 的 assignment/cue/status 消息链。

## 182. warlock/warlock_core/source

### 182.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `warlock/warlock_core` |
| 最小目录单元 | `afsim-2_9/swdev/src/warlock/warlock_core/source` |
| source/header 数 | 61 |
| 核心符号 | `warlock::CoreSimInterface`、`warlock::CoreSimEvent`、`warlock::RunManager`、`wk::EventPipe`、`warlock::ScriptSimInterface` |

### 182.2 职责说明

Warlock core 公共库，提供插件基类、sim interface、core sim events、event pipe、run manager、script sim interface 和平台数据 UI。

### 182.3 后续深挖点

Warlock 运行时插件基础设施入口，后续应追 `RunManager::StartLoading/LoadThread::run/SimThread::run`、`SimEnvironment::InitializeCallbacks`、`CoreSimInterface` → `CoreSimEvents::*::Process`、`SimInterfaceBase::AddSimCommand/ProcessCommands` 和 `EventPipe::RegisterEvents`。

## 183. tools/wkf/wsfg/wsf_spaceg/source

### 183.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `tools/wkf/wsfg/wsf_spaceg` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/wkf/wsfg/wsf_spaceg/source` |
| source/header 数 | 62 |
| 核心符号 | `AstrolabeDockWidgetBase`、`AstrolabeConfig`、`ConfigWidgetFactory`、`OrbitalMissionModel`、`MissionVerifierBase::Verify` |

### 183.2 职责说明

WKF/WSFG 的 Astrolabe 轨道任务编辑核心库，负责 JSON 配置控件、mission sequence 模型、验证、模型/序列转换和轨道预览。

### 183.3 后续深挖点

Astrolabe 业务入口链：`AstrolabeDockWidgetBase::OnVerify/OnApply` -> `MissionVerifierBase::Verify` -> `OrbitalModelToSequence::Transform` -> `OrbitalMissionVerificationContext::VerifyMission` -> `OrbitPreviewManager` 预览更新。


## 184. post_processor/WizPostProcessor/source

### 184.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `applications` |
| 子系统 | `post_processor/WizPostProcessor` |
| 最小目录单元 | `afsim-2_9/swdev/src/post_processor/WizPostProcessor/source` |
| source/header 数 | 80 |
| 核心符号 | `PostProcessor::Plugin`、`PostProcessor::ReportDialog`、`PostProcessor::ProxyInterface`、`PostProcessor::GeneralOutput`、`PostProcessor::ReportDialog::GenerateClickedHandler` |

### 184.2 职责说明

Wizard Post Processor 报表生成插件，提供 Communication、Detection、DSV、Eclipse、Engagement、Trajectory 等报表 UI，并把选择写成 post_processor 配置执行。

### 184.3 后续深挖点

报表生成入口链：`PostProcessor::Plugin` 菜单 action -> `Show*Dialog` -> `ProxyInterface::Update` -> widget 候选项刷新 -> `ReportDialog::GenerateClickedHandler` -> `ReportWidget::WriteData` -> `Configuration::Execute`。


## 185. core/wsf_nx/source

### 185.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework` |
| 子系统 | `core/wsf_nx` |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_nx/source` |
| source/header 数 | 72 |
| 核心符号 | `Register_wsf_nx`、`WsfNonExportableExtension::AddedToScenario`、`WsfChaffWeapon::DropChaffCloud`、`WsfEM_ALARM_Propagation`、`WsfCoherentSensorProcessor::ProcessResults` |

### 185.2 职责说明

WSF NX 非公开扩展能力包，注入高级雷达/电磁传播、天线模型、相干传感器融合、TRIMSIM、chaff 云/箔条武器与 EW 效果。

### 185.3 后续深挖点

扩展注册和业务链：`Register_wsf_nx` -> `WsfNonExportableExtension::AddedToScenario` 注册类型 -> `WSF_CHAFF_WEAPON/ejector` 或传感器处理器配置 -> `DropChaffCloud/EjectParcel` 或 `WsfCoherentSensorProcessor::ProcessResults`。


## 186. tools/utilosg

### 186.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `developer_tools` |
| 子系统 | `tools/utilosg` |
| 最小目录单元 | `afsim-2_9/swdev/src/tools/utilosg` |
| source/header 数 | 222 |
| 核心符号 | `UtoViewer`、`UtoWorld`、`UtoResourceDB`、`UtoShapeFactory`、`DtedTmsTileSource::createImage` |

### 186.2 职责说明

AFSIM 工具侧 OSG 可视化基础库，提供 viewer/window/world/overlay/entity/resource/shape/terrain 抽象和 OSG/osgEarth 资源插件。

### 186.3 后续深挖点

可视化入口链：应用创建 `UtoViewer` -> `UtoWorld`/window/overlay manager -> `UtoResourceDB` 解析资源定义 -> `UtoShapeFactory/UtoTerrainFactory` 创建对象 -> OSG scene graph 渲染；外部资源走 `ReaderWriter*.readNode` 和 `DtedTmsTileSource::createImage`。


## 187. wsf_plugins/wsf_coverage/source

### 187.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `plugin_modules` |
| 子系统 | `wsf_plugins/wsf_coverage` |
| 最小目录单元 | `afsim-2_9/swdev/src/wsf_plugins/wsf_coverage/source` |
| source/header 数 | 81 |
| 核心符号 | `Register_wsf_coverage`、`wsf::coverage::ScenarioExtension`、`wsf::coverage::SimulationExtension`、`wsf::coverage::Coverage`、`wsf::coverage::Measure` |

### 187.2 职责说明

WSF coverage 插件核心，提供 coverage/grid/measure/output 类型体系，计算传感器或资产访问区间、覆盖时间、revisit/gap/access 指标并输出文本/CSV/overlay/raw data。

### 187.3 后续深挖点

覆盖分析入口链：`WsfPluginSetup` -> `Register_wsf_coverage` -> `ScenarioExtension::AddedToScenario` 注册 grid/coverage/measure/output 类型 -> `SimulationExtension::ProcessInput(grid/coverage)` -> `SimulationExtension::Initialize` -> `Coverage::Initialize`/`Grid::Initialize` -> `Coverage::PendingStart` -> `SensorCoverage::OnSensorDetectionChanged` -> `Coverage::AddIntervalStart/EndToData` -> `Measure::CollectionCompleting` -> raw/MOE CSV/overlay/grid data 输出。


## 188. core/wsf_cyber/source

### 188.1 单元信息

| 字段 | 值 |
|------|-----|
| 系统 | `core_framework` |
| 子系统 | `core/wsf_cyber` |
| 最小目录单元 | `afsim-2_9/swdev/src/core/wsf_cyber/source` |
| source/header 数 | 85 |
| 核心符号 | `Register_wsf_cyber`、`wsf::cyber::ScenarioExtension`、`wsf::cyber::SimulationExtension`、`wsf::cyber::EngagementManager`、`wsf::cyber::Event::Execute` |

### 188.2 职责说明

WSF cyber 核心模型，提供 cyber attack/scan/protect/constraint/effect/trigger/engagement/event pipe/script extension，并把结果写入 event output 与 observer。

### 188.3 后续深挖点

Cyber 业务入口链：`Register_wsf_cyber` -> `ScenarioExtension::AddedToScenario` 注册 attack/effect/protect/trigger/constraint 类型和组件 -> `SimulationExtension::AddedToSimulation/Initialize` 注册 observer/event output/script observer/event_pipe -> trigger 或脚本 `CyberAttack/CyberScan` -> `EngagementManager` -> `EventManager/Event::Execute` 延迟阶段 -> `CyberAttackEffect`/具体 effect -> `CyberResult/EventPipe` 输出。


## batch41-batch43 最小目录单元补充（2026-07-14）

| 批次 | 最小目录单元 | source/header 数 | 模块职责 | 业务逻辑承接入口 |
|------|------|------:|------|------|
| batch41 | `tools/geodata/source` | 93 | 地理数据基础库，读取 DTED、GeoTIFF、shapefile、land use、geoid 等外部数据并提供高程/瓦片/几何查询。 | `DtedTileManager::LoadTile`、`GeotiffTileManager::AddDirectory/LoadTile`、`GeoShapeFile::ReadShapeFile` 可承接地形、高程、地图和相交逻辑分析。 |
| batch41 | `tools/artificer` | 40 | afperf 性能记录转换工具，从 v1 事件流汇总 run/region/section/measurement 统计。 | `main -> TransformFile -> V1Parser::Parse -> V1PrototypeSummarizer -> RunData::CollectStats` 可承接性能事件语义分析。 |
| batch42 | `tools/vespatk/source` | 135 | VESPA viewer/camera/entity/attachment/overlay/model database 可视化基础库。 | `VaEnvironment::Initialize -> VaScenario::Initialize/Load/UpdateFrame -> VaFactory -> VaViewer` 可承接仿真对象到三维显示的映射分析。 |
| batch42 | `core/wsf_l16/source` | 105 | Link-16 扩展，处理 feature 注册、接口配置、DIS Signal、J-series 消息和 computer parts。 | `Register_wsf_l16 -> Interface::Initialize -> Factory::ReadMessage/Interface::SendJMessage -> ComputerProcessor` 可承接战术数据链业务逻辑分析。 |
| batch43 | `tools/utilqt/source` | 105 | Qt 工具基础设施库，提供 dock、model/view、OpenGL 绘图、渐变、XML、网络/进程辅助。 | `UtQtDockArea/UtQtDockControl`、`UtQtGLWidgetBase`、`UtQtXmlReader` 可承接 GUI 工具框架行为分析。 |
| batch43 | `tools/util_script/source` | 107 | AFSIM 内嵌脚本系统，覆盖 parser/scanner、类型注册、字节码、VM 执行和对象绑定。 | `UtScriptContext::Parse/Execute -> UtScriptParser -> Parser::func_def -> UtScriptExecutor::Execute` 可承接场景脚本如何驱动仿真对象的业务分析。 |

## batch44-batch46 最小目录单元补充（2026-07-15）

| 批次 | 最小目录单元 | source/header 数 | 模块职责 | 业务逻辑承接入口 |
|------|------|------:|------|------|
| batch44 | `core/wsf_util` | 21 | WSF 底层工具库，提供 byte buffer、CSV、UTML、tar、SHA 与 UtPack 反射/schema/二进制消息序列化能力。 | `UtPackSchema::Read -> Resolve -> UtPackSerializer::Initialize/RegisterMessage` 串起 schema 装载、类型注册和消息序列化；`UtCsv::Parser::ReadRow` 与 `UtmlParser` 可承接文本输入解析分析。 |
| batch44 | `post_processor/lib` | 20 | 仿真后处理报表库，读取命令行、配置文件和输出 CSV，生成通信、探测、交战、eclipse、轨迹与 DSV 报表。 | `Configuration::Execute -> ProcessConfigurationFile -> CreateReport -> InitReport -> Report::PrintReport` 是后处理业务主链；派生 report 的 `ProcessHeaders/ProcessData/PrintReport` 是报表字段语义入口。 |
| batch44 | `wsf_plugins/wsf_argo8` | 14 | ARGO8 导弹/飞行模型插件，把外部或标准 ARGO8 模型包装进 WSF mover 生命周期。 | `Register_wsf_argo8 -> WsfARGO8_Extension::AddedToScenario -> WsfARGO8_Mover` 建立 mover 类型；运行时沿 `WsfARGO8_Mover::Update -> Argo8Missile::Update -> Argo8Model::Update` 进入飞行/制导逻辑。 |
| batch44 | `wsf_plugins/wsf_multiresolution` | 17 | 多分辨率组件插件，为 mover、sensor、processor、fuel、comm 和 signature 等组件按 fidelity 选择具体模型实现。 | `Register_wsf_multiresolution -> WsfMultiresolutionTypesRegistration::AddedToScenario -> AddMultiresolutionType` 注册 wrapper；运行时 `PreInitialize -> GetFidelity -> ModelIndexForFidelity -> Clone` 选择 fidelity 对应模型。 |
| batch45 | `core/sensor_plot_lib` | 44 | AFSIM 传感器绘图/分析函数库，注册 antenna plot、map plot、lookup table、vertical coverage 等分析函数，并在临时仿真中采样输出。 | `Register_sensor_plot_lib -> WsfSensorPlotExtension::AddedToScenario -> ProcessInput -> ExecutePlots -> RunFunction -> Function::Execute` 是 plot 执行链；`MapPlotFunction` 等派生类承接具体采样语义。 |
| batch45 | `wsf_plugins/wsf_air_combat` | 34 | 空战态势感知插件，注册 `WSF_SA_PROCESSOR`，提供感知、评估、预测与空战事件管道。 | `Register_wsf_air_combat -> WsfAirCombatTypeManager::AddedToScenario -> WSF_SA_PROCESSOR` 建立处理器；运行时 `WsfSA_Processor::ProcessInput/Update` 串起 perceive、assess、predict 和 event pipe 输出。 |
| batch46 | `tools/wkf/air_combat/wkf_air_combat_common/source` | 94 | WKF 空战可视化公共库，提供 SA、ACES、HUD、HDD 与 overlay 绘制的数据容器、显示接口和 Qt/OSG 插件基类。 | `AirCombatDisplayInterface::Update` 消费 `DataContainer` 中的 engagement、fuel、weapons、track、SA 等字段更新 decorators/interactions/overlays；SA/ACES 插件通过 context menu 接入平台显示。 |
| batch46 | `wizard/plugins/PatternVisualization/source` | 95 | Wizard 天线 pattern 与雷达/光学/红外/声学 signature 可视化插件，生成临时 SigView 输入，构建会话并用 Qt/OpenGL 渲染 2D/3D pattern。 | `Plugin::RunPatternVisualization -> DockWidget::ReadPatternFile -> Session::LoadPatterns -> Session::RequestPatternUpdate -> PatternUpdateManager -> Canvas::AddOrUpdatePattern/paintGL` 是从 Wizard 节点到 pattern 渲染的主链。 |

## batch47-batch52 最小目录单元补充（2026-07-15）

| 批次 | 最小目录单元 | source/header 数 | 模块职责 | 业务逻辑承接入口 |
|------|------|------:|------|------|
| batch47 | `tools/geodata` | 5 | geodata 父级 residual：覆盖构建入口与 DTED/GeoTIFF/FloatGrid 单元测试，不重复 source/ 地形瓦片与投影实现。 | `CMakeLists.txt -> add_subdirectory(source) -> test/main.cpp -> gtest cases -> DtedTile/GeotiffTile/FloatGridTile`，用于验证地理数据读取链。 |
| batch47 | `tools/vespatk` | 6 | vespatk 父级 residual：覆盖 shader header 与资源/安装辅助入口，不重复 source/ VESPA viewer 与资源管理核心。 | CMake helper 安装/提取 resources、maps、models、shaders，运行时由 `VaResourceManager`/viewer 链消费。 |
| batch47 | `tools/util_script` | 2 | util_script 父级 residual：覆盖顶层构建与 UtScriptData/UtScriptDataPack 回归测试，不重复 source/ parser、类型系统和 VM。 | `CMakeLists.txt -> gtest -> UtScriptData/UtScriptDataPack`，验证脚本数据对象、排序、constructors 和 pack/unpack。 |
| batch47 | `tools/utilqt` | 2 | utilqt 父级 residual：覆盖 Qt code timer GUI 观察器和旧 `.pro` 工程入口，不重复 source/ 通用控件库。 | `UtQtCodeTimer::Initialize -> QTimer::timeout -> UtCodeTimer::Update -> UtQtCodeTimerObserver::Update/ReportChildren`。 |
| batch47 | `core/wsf_cyber` | 3 | wsf_cyber 父级 residual：覆盖 CMake、grammar、event pipe schema、doc 与测试资产，不重复 source/ cyber attack/effect/trigger 实现。 | `wsf_cmake_extension.cmake -> grammar/wsf_cyber.ag -> scenario input -> source extension/managers -> event pipe schema`。 |
| batch47 | `wizard/plugins` | 22 | Wizard 插件集合父级 residual：覆盖插件清单、wizard_plugin.cmake、CRDImporter lib/exec/test 等包装层，不重复各插件 source/ 业务实现。 | `wizard_plugin.cmake -> WIZARD_PLUGIN_NAME/source path -> plugin target -> plugin constructor registers actions/docks/preferences`。 |
| batch47 | `wsf_plugins/wsf_coverage` | 37 | wsf_coverage 父级 residual：覆盖顶层 CMake、coverage grammar、doc、test 与 test_mission 资产，不重复 source/ coverage/grid/measure 实现。 | `wsf_cmake_extension.cmake -> grammar/wsf_coverage.ag -> scenario input -> source SimulationExtension -> grid/coverage/measure/output`。 |
| batch47 | `tools/utilosg/source` | 0 | utilosg/source 闭环确认：该源码目录已由 batch40 的 parent `tools/utilosg` 覆盖，本轮只关闭重叠 pending 单元。 | 已归属链仍为 `UtoShapeFactory/UtoTerrainFactory -> UtoResourceDB -> UtoViewer`；本轮不重新分摊子树。 |
| batch48 | `wsf_plugins/wsf_p6dof/p6dof/source` | 100 | P6DOF 核心飞行动力学源码，覆盖 vehicle/type manager、6DOF 积分、气动、控制、推进、燃料、自动驾驶、航路、环境与 sequencer。 | `P6DofTypeManager::ProcessInput -> P6DofVehicleType::ProcessInput -> P6DofVehicle::InitializeDetails -> UpdateObject -> P6DofIntegrator::Update`。 |
| batch49 | `core/wsf_parser/source` | 138 | WSF parser 核心源码，负责 grammar 定义加载、运行期 parse、parse tree、规则/动作/类型系统和 PProxy 可编辑模型映射。 | `WsfParseDefinitions::AddGrammar -> grammar_parse Parser -> Initialize -> WsfParser::ParseFiles -> WsfParseRule::Read -> WsfPProxyDeserialize/Serialize/Satisfy`。 |
| batch50 | `tools/genio/source` | 145 | 通用 I/O 与序列化基础库，覆盖缓冲、字节序、GenI/GenO 抽象、文件/内存/pipe/TCP/UDP/UMP 传输和消息封装。 | 输入链 `Receive -> GenBufXferI -> GenI::Get -> GenIConvert*`；输出链 `GenO::Put -> GenBufXferO -> GenOConvert* -> Send`；消息链 `GenMsg::Put/Get`。 |
| batch51 | `wsf_plugins/wsf_iads_c2_lib/source` | 159 | IADS C2 插件 source 包，覆盖 asset/battle/dissemination/sensors/weapons manager、default impl、C2 message wrappers、script binding、records 与 event/MOE 输出。 | 初始化链连接同平台 asset/dissemination/battle/sensors/weapons manager；出站链 `WsfBMDisseminateC2::Update -> WsfDefaultDisseminationImpl::on_update -> SendMessage`；入站链进入 `WsfDefaultAssetManagerImpl::on_message`。 |
| batch52 | `tools/wkf/core/source` | 165 | WKF Qt/VESPA 基础库，覆盖 Environment 单例、MainWindow、Plugin/PluginManager、VtkEnvironment、Scenario/Viewer/Platform、Observer、配置/权限/资源/单位。 | `Environment::Create -> Environment ctor -> MainWindow::InitializeDialogs -> Environment::StartUp -> PluginManager::Initialize/LoadPluginInitialize -> QTimer TimerHandler/UpdateFrame`。 |


## batch53-batch58 最终 22 个最小目录单元补充（2026-07-15）

| 批次 | 最小目录单元 | source/header 数 | Phase2 结论 |
|---|---|---:|---|
| batch53 | `afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof` | 1 | P6DOF 插件父目录 residual，仅保留顶层/测试闭环；真正运动模型在 p6dof/source 与 wsf_p6dof/source。 |
| batch53 | `afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof` | 1 | SixDOF 插件父目录 residual，闭合顶层构建入口；动力学、发动机和推进系统在 source 子目录。 |
| batch53 | `afsim-2_9/swdev/src/tools/wkf` | 2 | WKF 父目录 residual，闭合 common/core 等已拆分单元之外的顶层入口。 |
| batch53 | `afsim-2_9/swdev/src/core/wsf_mil` | 3 | 军事感知/特征父目录 residual；source 子目录承载贝叶斯、光学、声学与聚类实现。 |
| batch53 | `afsim-2_9/swdev/src/core/wsf` | 12 | WSF 核心父目录 residual，闭合主 source、parser、space 等子单元之外的残留入口。 |
| batch53 | `afsim-2_9/swdev/src/core/wsf_parser` | 19 | WSF 解析器父目录 residual，负责解析动作、脚本扫描和 parse-source 周边入口。 |
| batch53 | `afsim-2_9/swdev/src/core/wsf_space` | 25 | 空间/轨道父目录 residual；source 子目录承载轨道传播器和大气扩展。 |
| batch53 | `afsim-2_9/swdev/src/tools/util` | 63 | 通用工具父目录 residual；source 子目录承载日志、字符串、异常和历史映射。 |
| batch53 | `afsim-2_9/swdev/src/wizard/usmtf` | 72 | USMTF Wizard 父目录 residual；source 子目录承载字段、消息、时间点与枚举校验。 |
| batch53 | `afsim-2_9/swdev/src/wsf_plugins/wsf_iads_c2_lib` | 95 | IADS C2 库父目录 residual，补齐脚本可覆写处理器、事件输出与场景扩展边界。 |
| batch54 | `afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof/source` | 191 | WSF P6DOF 插件封装层，连接类型管理、对象管理、事件管道、燃料和 mover 生命周期。 |
| batch54 | `afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source` | 331 | WSF SixDOF 插件实现，覆盖发动机、推进系统、刚体推力对象和点质量表工具。 |
| batch55 | `afsim-2_9/swdev/src/wizard/usmtf/source` | 182 | USMTF 字段/消息/段结构解析与校验，面向 Wizard 输入合法性和格式约束。 |
| batch55 | `afsim-2_9/swdev/src/mover_creator/source` | 225 | Mover Creator 图形工具，编辑气动、几何、发动机、脚本生成和车辆性能数据。 |
| batch55 | `afsim-2_9/swdev/src/tools/wkf/common/source` | 247 | WKF 公共可视化/事件标记组件，提供视觉效果、轨迹效果和显示接口。 |
| batch55 | `afsim-2_9/swdev/src/wizard/lib/source` | 248 | Wizard 编辑器基础库，覆盖文本源读写、语法折叠、编辑器初始化和解析结果聚合。 |
| batch56 | `afsim-2_9/swdev/src/core/wsf_space/source` | 304 | WSF 空间与轨道传播实现，覆盖积分传播器、机动、轨道类型和大气仿真扩展。 |
| batch56 | `afsim-2_9/swdev/src/tools/util/source` | 341 | 跨模块通用工具实现，覆盖历史映射、日志流、字符串解析、异常记录和实体工具。 |
| batch56 | `afsim-2_9/swdev/src/core/wsf_mil/source` | 429 | 军事环境感知与特征模型，覆盖贝叶斯分类、光学路径、声学/光学特征和聚类。 |
| batch56 | `afsim-2_9/swdev/src/tools/dis/source` | 433 | DIS 协议数据结构与 PDU 读写，覆盖实体类型、IFF、AIS、坐标和动作响应。 |
| batch57 | `afsim-2_9/swdev/src/core/wsf/source` | 1113 | WSF 主仿真内核，覆盖应用输入、场景/仿真初始化、平台对象、通信队列、行为树和帧步更新。 |
| batch58 | `afsim-2_9/swdev/src/wsf_plugins/wsf_oms_uci/source` | 8642 | OMS-UCI 插件桥接层，连接 WSF computer/part/message service 与大量 UCI schema 生成类型、读写器和工厂。 |

本轮完成 Phase2 剩余 22 个单元。后续业务逻辑分析建议以 `core/wsf/source` 的仿真生命周期、`wsf_oms_uci/source` 的 WSF-UCI 包装层、P6DOF/SixDOF 的 mover/propulsion 生命周期、DIS PDU 读写链路为首批入口。
