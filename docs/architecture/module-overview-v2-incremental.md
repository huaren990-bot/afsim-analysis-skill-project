# Phase 2 模块概览增量版

> **日期**：2026-06-24
> **状态**：增量进行中
> **工作方式**：按最小目录单元逐步补强，完整工作清单见 `workspace/source-index/phase2-analysis-unit-worklist.jsonl`

## 0. 概览说明

Phase 2 v2 不再沿用旧版“107 个同层模块”组织方式，而是以 Phase 1 的 `module_hierarchy` 为准，按系统、子系统、最小目录单元逐步分析。

当前默认范围内共有 237 个最小目录单元、17,179 个 source/header 文件。已完成 2 个单元：

| # | 系统 | 子系统 | 最小目录单元 | 文件数 | 状态 | 详情 |
|---|------|--------|--------------|--------|------|------|
| 1 | core_framework | core/wsf_weapon_server | `afsim-2_9/swdev/src/core/wsf_weapon_server/source` | 2 | 已完成 batch01 | 见第 1 节 |
| 2 | core_framework | core/wsf_grammar_check | `afsim-2_9/swdev/src/core/wsf_grammar_check/source` | 2 | 已完成 batch02 | 见第 2 节 |

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
