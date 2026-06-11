---
name: afsim-source-cognition
description: 当用户需要快速学习 AFSIM 源码、建立源码索引、理解目录结构、模块职责、核心类、函数索引、依赖关系、调用链、数据流、配置流、仿真生命周期，或生成可追溯的 AFSIM 架构认知报告时，使用本 skill。
metadata:
  short-description: 建立 AFSIM 源码认知索引和架构报告
---

# AFSIM 源码认知 Skill

## 目标

任务是将 AFSIM 源码转化为结构化的认知产物：架构文档、模块依赖图、以及可被下游 Agent 检索的细粒度索引文件，建立可追溯的 AFSIM 源码认知资产，服务后续算法提取、需求映射、功能迁移和知识沉淀。不要只复述目录结构；必须把源码路径、符号、生命周期、数据流和模块职责关联起来。严格使用提供的工具，遵循分步推理，并在理解不确定时主动向开发人员请求校对，而非臆断。
按照“系统级功能(`System-level`) ─ 跨框架/域/插件层，组合多个模块；模块级功能(`Module-level`)  ─ 主要在一个模块内，通过策略模式多态；类级功能(`Class-level`)  ─ 单个类的职责范围；方法级功能(`Method-level`)  ─ 单个函数/算法实现“分类解析afsim中的功能。

## 使用时机

使用本 skill 处理以下任务：

- 快速理解 AFSIM 总体源码结构、模块边界和核心职责。
- 为某个 AFSIM 模块建立文件、类、函数和依赖索引。
- 识别仿真初始化、场景加载、对象创建、模型更新、事件处理、输出和清理流程。
- 梳理状态对象、配置项、脚本或场景文件如何影响运行时行为。
- 生成 `workspace/source-index/` 索引和 `docs/architecture/` 架构报告。
- 发现算法核心、框架封装、配置依赖和可迁移代码位置。

**重要**：每次被调用时，必须先读取本 skill 的"已完成的基线记录"一节，确认当前分析范围是否已被覆盖。如果已有基线覆盖了目标范围，直接复用已有索引作为起点进行增量更新，**不要重新扫描已完整索引的源码目录**。如果分析边界超出已有基线，在基线记录中追加新条目。

## 输入要求

开始前确认以下输入，缺失时先从当前工作区探测，仍无法确认再询问用户：

- `source_root`：AFSIM 源码根目录。
- `extract_root`：本次需要解析的根目录。
- `analysis_scope`：本轮纳入的目录、模块、文件类型或用户指定主题。
- `exclude_paths`：构建产物、第三方依赖、缓存、临时文件和大体积生成目录。
- `baseline_docs`：用户提供的说明文档、历史报告、需求材料或已有索引。
- `analysis_depth`：`overview`、`module`、`symbol` 三档之一。

默认排除 `.git`、以 `.` 开头的文件，构建目录、包管理缓存、二进制产物和外部依赖镜像。不要在未说明范围的情况下扫描用户无关目录。

## 工作流

### 1. 确认边界

记录本轮分析的源码根目录、纳入范围、排除范围、分析深度和使用过的历史材料。所有正式产物都要能回到这个边界说明。并在分析前先读取已存在的输出产物，确认是否需要覆盖或增量更新。不要在不清楚范围的情况下盲目扫描整个源码树；也不要把用户无关目录当作事实来源。

### 2. 发现文件

优先用 `rg --files` 获取候选文件，并分类为：

- `source`：`.h`、`.hpp`、`.hh`、`.c`、`.cc`、`.cpp`、`.cxx`。
- `build`：`CMakeLists.txt`、`Makefile`、`.cmake`、工程配置。
- `config`：XML、JSON、YAML、INI、脚本、场景和运行参数文件。
- `test`：测试目录、测试源码、验证脚本。
- `example`：示例、demo、样例场景。
- `doc`：README、设计说明、接口文档。
- `generated`：生成文件或机器产物，默认不作为事实来源。

文件职责先给保守结论；没有源码证据时使用 `unknown`，不要从文件名直接推断成事实。

### 3. 参数与取值深入提取

- 对于函数/方法参数，若有默认值，必须记录默认值表达式或字面量。若默认值依赖其他常量，则说明引用关系。
- 对于类成员变量，记录其类型、访问修饰符、构造函数中或声明时初始化的默认值。
- 对于全局变量（包括命名空间内的变量、静态全局变量），记录其声明位置、类型、初始值（若可见），并尝试推断其用途（例如：“全局时间步长，默认值0.001s”）。
- 对于 `#define` 宏常量和 `const`/`constexpr` 常量，记录其名称、定义位置、值和用途。
- 对于枚举，记录枚举名、所有枚举值及对应的整数值（若有显式赋值）。
- 如果代码中有明显的调参建议注释（如 “Tuned for 100Hz loop”），应作为参考值说明记录下来。

### 4. 建立索引

每识别出一个代码单元，立即以 JSON 行格式追加到以下三个索引文件（使用 `append_to_file` 工具）：

1.建立文件索引

2.建立符号索引

按“轻量扫描优先、AST 增强可选”的策略识别：

- `namespace`、`class`、`struct`、`enum`、`typedef`、`using`。
- 函数、成员函数、虚函数、模板函数、构造函数、析构函数。
- 入口点、生命周期回调、工厂注册、插件注册、配置解析函数。

跨文件声明和实现分离时，保留 `declaration_path` 与 `definition_path`。重载、模板和宏生成代码不能只按名称合并，必须保留签名或限定名。

3.建立依赖索引

从这些证据提取依赖：

- `#include`、前向声明、命名空间引用。
- 继承、组合、成员字段、函数参数和返回类型。
- 构建 target、library、include directory、compile definition。
- 函数调用、生命周期回调、事件订阅、消息分发。
- 工厂、注册表、插件声明、脚本绑定和配置映射。

依赖类型只能使用输出约束中的枚举。运行时关系无法静态证明时，标记为 `inferred` 或 `unknown`。

### 5. 识别仿真生命周期

围绕以下阶段建立生命周期视图：

- `entry`：程序入口和命令行参数解析。
- `scenario_load`：场景、平台、模型和全局配置加载。
- `object_create`：对象创建、注册、连接和初始化。
- `simulation_loop`：时间推进、调度循环、事件处理和模型更新。
- `model_update`：平台、传感器、武器、通信或环境模型计算。
- `output`：日志、统计、结果文件和外部接口输出。
- `shutdown`：仿真结束、资源释放和清理。

每个阶段尽量关联入口函数、关键类、配置来源、主要状态对象和证据位置。证据不足的阶段写入架构报告 `Unknowns`。

### 6. 分析数据流和配置流

数据流按 `state_source -> state_owner -> update_function -> consumers -> outputs` 描述。配置流按 `config_file -> parser -> factory_or_registry -> object_property -> runtime_behavior` 描述。

重点记录状态对象、实体对象、模型对象、事件对象、消息对象、单位、坐标系、时间基准和枚举含义。无法确认的单位、坐标系或语义必须标记 `unknown`。

### 7. 生成架构文件

将推导结果写入 `afsim-architecture.md`、`module-dependency.md`和 `x-level-capabilities.md`。

## 输出文件

- 把每一步的决策依据和执行计划生成文档进行记录归档，放在目录docs/records里面，方便追溯。
- 每解析一个`extract_root`，就创建新目录`docs/architecure/extract_root`和`workspace/source-index/extract_root`，如果目录存在则不用新建。
- 在`docs/architecure/extract_root`下放置所有输出的`.md`文件，`.md`文件中所有英文标识、英文别称都应说明其中文翻译，保证中文可读性。
- 在`workspace/source-index/extract_root`下放置所有输出的`.jsonl`文件。
- 所有索引写入`.jsonl`文件，使用 UTF-8 。每行必须是一个完整 JSON object，不允许尾逗号、注释、Markdown 代码块或跨行 JSON。字段缺失时使用 `null`、空数组或 `unknown`，不要省略必填字段。
- 要求所有输出文件用词统一，文件名、模块名、符号名、函数名、依赖名在所有文件中都保持一致，不应产生歧义。
- 不能使用省略号省略列举内容，如果列举的条目多于30，而应当新建个文件将省略内容全部列出，并将文件连接放置到原本的省略位置。

### `afsim-architecture.md`

总体架构认知报告。要求和模板参考skill/afsim-source-cognition/template_list/template_architecture.md

### `module-depencency.md`

模块依赖说明；可包含 Mermaid 图，但图中的边必须能追溯到 `dependency-index.jsonl` 或源码位置。格式应当严格遵循模板skill/afsim-source-cognition/template_list/template_module-depencency.md。

### `x-level-capabilities.md`

x-level-capabilities.md是afsim功能的功能说明文件。

格式应当严格遵循模板skill/afsim-source-cognition/template_list/template_x-level-capabilities.md，不要擅自修改表格和标题顺序。

文件中的方法级功能必须能追溯到`function-index.jsonl`。

- 文件中每一层的功能必须能通过 `qualified_name` 追溯到 `function-index.jsonl` 中的对应条目。
- 文档标题必须为 `# AFSIM 仿真框架架构文档`，不可擅自修改。
- 方法级功能表格中必须使用个体的 `qualified_name`（如 WsfP6DOF_Mover::Initialize），不可写成抽象群组（如"生命周期方法"）。
- 每个功能层级必须包含"功能对应条目"段落，明确写出对应 function-index.jsonl 中 level=xxx 的条目 qualified_name。
- 表格列必须与模板完全一致，不可增删列、不可修改表头文字。

### `file-index.jsonl`

格式应当严格遵循模板skill/afsim-source-cognition/template_list/template_file-index.md

- `source`/`header` 文件的 `includes` 数组必须解析 `#include` 指令并填充，不可全部为 `[]`。

### `symbol-index.jsonl`

格式应当严格遵循模板skill/afsim-source-cognition/template_list/template_symbol-index.md

- `kind` 为 `macro` 的符号只包含 `#define` 定义的宏常量；`__declspec(dllexport)` 生成的 `*_EXPORT` 宏不纳入符号索引。
- 前向声明（仅 `class X;` 而无后续定义的）不纳入符号索引。

### `function-index.jsonl`

格式应当严格遵循模板skill/afsim-source-cognition/template_list/template_function-index.md

- 必须同时包含 System-level、Module-level、Class-level、Method-level 四层条目，不可只有 Method-level 一层。
- Method-level 条目的 `parameters` 必须填写参数信息，不可全部为 `[]`。至少包含 `name` 和 `type`；若有默认值必须记录 `default_value`。
- 如果无法解析所有函数的参数，必须在对应条目的 `notes` 字段中标记"待AST解析"，而不可保持空数组了事。
- System/Module/Class 级条目的 `brief` 不可为空。
- `qualified_name` 必须在全文件中唯一。

### `dependency-index.jsonl`

格式应当严格遵循模板skill/afsim-source-cognition/template_list/template_dependency-index.md

- 依赖关系条目数应不少于 200 条（覆盖 build + inheritance + composition + include + call + registration 六种 relation）。
- 对于 1 万文件以上的分析范围，仅 60+ 条是不够的。

## 证据等级

只能使用以下值：

- `source-cited`：由源码路径、符号和行号直接支持。
- `document-cited`：由用户文档、设计文档或历史报告支持。
- `index-derived`：由本轮生成的索引汇总得到。
- `inferred`：由相邻证据推断，但源码未直接说明。
- `unknown`：证据不足。

重要架构结论优先使用 `source-cited`。`inferred` 结论必须说明推断依据；`unknown` 必须进入报告的未知项。

## 质量门槛

交付前逐项检查，全部通过方可标记为"完成"。

### 通用检查
1. 四个 JSONL 索引文件存在，且每行都能被 JSON parser 解析。
2. 每个 JSON object 都包含对应模板的全部必填字段和 `schema_version`。
3. 枚举字段只使用本 skill 规定的值。
4. 文件路径相对 `source_root` 可定位；行号使用 1-based 编号。
5. 不把文件名相似、路径相近或命名相近当作功能等价证据。
6. 未阅读、无法解析或证据不足的内容标记为 `unknown` 或 `inferred`。
7. 输出之间用词统一，`qualified_name`、模块名、符号名在所有文件中保持一致。
8. 不能使用省略号省略列举内容；如果列举条目多于30条，新建独立文件将完整内容列出。

### file-index.jsonl 专项检查
9. `source`/`header` 类型文件的 `includes` 数组已解析填充，不可全部为 `[]`。

### symbol-index.jsonl 专项检查
10. `kind=macro` 仅包含 `#define` 宏常量，不含 `*_EXPORT` 导出宏。
11. 不含前向声明（`class X;` 形式）条目。

### function-index.jsonl 专项检查
12. 包含 System-level、Module-level、Class-level、Method-level 四层条目。
13. System/Module/Class 级条目的 `brief` 非空。
14. Method-level 条目的 `parameters` 数组已填写参数信息（至少 name + type）。无法解析的条目在 `notes` 中标明"待AST解析"。
15. `qualified_name` 全文件唯一。

### dependency-index.jsonl 专项检查
16. 条目数 ≥ 200。至少覆盖 build、inheritance、composition、include、call、registration 六种 relation。

### x-level-capabilities.md 专项检查
17. 文档标题为 `# AFSIM 仿真框架架构文档`。
18. 表格列与模板 `template_x-level-capabilities.md` 完全一致，无增删改。
19. 每个功能层级包含"功能对应条目：见 function-index.jsonl 中 ..."段落。
20. 方法级功能表格中的 `qualified_name` 可在 function-index.jsonl 中查到。

### afsim-architecture.md 专项检查
21. 包含模板要求的全部章节：目录结构总览、模块总览、仿真生命周期、数据流、配置流、扩展点、关键符号、未知项、源码证据。

### module-dependency.md 专项检查
22. Mermaid 图中的每一条边可追溯到 dependency-index.jsonl 或源码位置。

## 已完成的基线记录

每次完成一轮分析后，将分析边界、产出和统计信息追加到本节。**后续使用本 skill 时必须先读取本节，确认已有分析资产，避免重复扫描已索引的源码。**

---

### 基线 1：core/ 全覆盖 module 深度分析

| 字段             | 值                                                                                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 完成日期           | 2026-06-09                                                                                                                                                                                        |
| source_root    | `source_root/afsim-2_9/swdev/src/core/`                                                                                                                                                           |
| analysis_scope | core/ 全部 14 个模块（wsf / wsf_mil / wsf_space / wsf_nx / wsf_parser / wsf_mil_parser / wsf_grammar_check / wsf_util / wsf_ripr / wsf_cyber / wsf_l16 / wsf_mtt / wsf_weapon_server / sensor_plot_lib） |
| analysis_depth | module（含符号级扫描 + 7 个核心头文件源码验证）                                                                                                                                                                     |
| exclude_paths  | `.git`, `.` 开头文件, `build/`, `3rd_party/`, `.tar.gz`, `*.osgb`, `*.dll`, `*.so`, 测试目录未深度展开                                                                                                         |
| baseline_docs  | `docs/baseline/WsfSimulation_Design_Document.md`, `docs/baseline/WsfSimulation_Core_Design_Document.md`                                                                                           |

#### 产出文件

| 文件                                              | 行数    | 内容                                                                                              |
| ----------------------------------------------- | ----- | ----------------------------------------------------------------------------------------------- |
| `workspace/source-index/file-index.jsonl`       | 4,997 | 全文件索引，2,413 文件含 includes 数组                                                                     |
| `workspace/source-index/symbol-index.jsonl`     | 3,255 | 去重符号索引（class/struct/enum/typedef/using），含行号和继承                                                  |
| `workspace/source-index/function-index.jsonl`   | 4,099 | 函数/方法索引，含返回类型、参数、生命周期角色、算法提示                                                                    |
| `workspace/source-index/dependency-index.jsonl` | 1,113 | 依赖索引：inheritance(1014) + composition(50) + call(16) + build(14) + include(10) + registration(9) |
| `docs/architecture/afsim-architecture.md`       | —     | 完整架构报告：模块总览、生命周期、数据流、配置流、扩展点、未知项                                                                |
| `docs/architecture/module-dependency.md`        | —     | 模块依赖说明：构建依赖图、架构继承/组合关系、子系统间依赖                                                                   |

#### 已确认的关键资产

- **14 个模块**的文件统计、核心职责、构建依赖链
- **7 阶段仿真生命周期**：entry → scenario_load → object_create → simulation_loop → model_update → output → shutdown，每个阶段的入口函数、关键类、配置来源和主要状态对象
- **13 个扩展点机制**：ApplicationExtension / SimulationExtension / ScenarioExtension / ComponentFactory / PluginManager / CorrelationStrategy / FusionStrategy / TrackExtrapolationStrategy / TrackReportingStrategy / Observer 系统 / EventPipe / XIO / ScriptSystem
- **核心组合关系**已从 WsfSimulation.hpp (33 个成员字段)、WsfPlatform.hpp (11 个成员字段)、WsfComponentFactory.hpp、WsfExtension.hpp、WsfPluginManager.hpp 源码验证
- **核心调用链**：Initialize → CreateClock → AddInputPlatforms → Start → AdvanceTime → DispatchEvents → Complete

#### 仍为 unknown 的项

1. RIPR 全称 — CMake/源码中未找到展开名
2. wsf_mtt 与 WsfTrackManager 的调用链交互细节 — 需读 .cpp 实现文件
3. wsf_nx ALARM 电磁模型与 wsf EM 模型的关系 — 函数级分析未展开
4. 约 75.6% 函数的 lifecycle_role 仍为 unknown — 仅对核心控制类和关键接口方法做了手动分类，大量内部实现函数未被覆盖，进一步精细化需要 AST 级分析

#### 复用指引

- 再次分析 core/ 时，直接读取已有索引文件作为起点，按需增量更新
- 如需扩展到 `wsf_plugins/`、`tools/`、应用层（mission/warlock/mystic 等），新建基线记录
- 如需 symbol 深度（逐函数 full signature + AST），在 module 索引基础上执行符号级增强

---

### 基线 2：wsf_plugins/ 全覆盖 module 深度分析

| 字段             | 值                                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| 完成日期           | 2026-06-10                                                                                           |
| source_root    | `source_root/src/wsf_plugins/`                                                                       |
| analysis_scope | wsf_plugins/ 全部 16 个插件模块                                                                             |
| analysis_depth | module（含符号级扫描 + 每模块至少 1 个核心头文件源码验证）                                                                  |
| exclude_paths  | `.git`, `.` 开头文件, OCI 自动生成头文件 (wsf_oms_uci/lib/ocl/ 下的 8588 个文件), 预编译库 (.so/.dll/.lib), 文档目录, 测试任务目录 |
| baseline_docs  | 基线 1 core/ 分析输出                                                                                      |

#### 产出文件

| 文件                                                          | 行数     | 内容                                                                                     |
| ----------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------- |
| `workspace/source-index/wsf_plugins/file-index.jsonl`       | 11,666 | 全文件索引                                                                                  |
| `workspace/source-index/wsf_plugins/symbol-index.jsonl`     | 14,785 | 符号索引（class/struct/enum），含行号和继承                                                         |
| `workspace/source-index/wsf_plugins/function-index.jsonl`   | 36,813 | 函数/方法索引，含返回类型、生命周期角色、算法提示                                                              |
| `workspace/source-index/wsf_plugins/dependency-index.jsonl` | 61     | 依赖索引：build(33) + inheritance(13) + composition(5) + registration(7) + configuration(1) |
| `docs/architecture/wsf_plugins/afsim-architecture.md`       | —      | 完整架构报告：16 模块总览、目录结构、生命周期、数据流、配置流、扩展点、未知项                                               |
| `docs/architecture/wsf_plugins/module-dependency.md`        | —      | 模块依赖说明：构建依赖 Mermaid 图、架构继承/组合关系表、子系统间依赖图                                               |
| `docs/architecture/wsf_plugins/x-level-capabilities.md`     | —      | 功能层次说明：13 个系统级功能 → 34+ 个模块级功能 → 60+ 个类级功能                                              |

#### 已确认的关键资产

- **16 个插件模块**的文件统计、核心职责、构建依赖链
- **4 大子系统**：运动学系统（P6DOF/Six-DOF/ARGO8）、作战管理系统（空战SA/IADS C2）、传感器与分析系统（SOSM/Coverage/Multi-resolution/Scenario Analyzer）、可视化与数据交换系统（SIMDIS/OMS-UCI/Annotation）
- **3 层运动学模型等级**：点质6DOF → 拟6DOF → 刚体6DOF+ARGO8，保真度递增
- **5 个独立核心库**：p6dof, brawler, argo8, iadsLib, sosm
- **33 条构建依赖链**从 CMakeLists.txt 提取
- **13 条核心继承关系**：WsfScenarioExtension, WsfSimulationExtension, WsfMover, WsfScriptProcessor, WsfPlatformComponent
- **5 个组合关系**：从源码直接读取的 unique_ptr/shared_ptr/CloneablePtr 成员
- **4 个 EventPipe 注册**：wsf_air_combat, wsf_p6dof, wsf_six_dof, wsf_annotation
- **19 项场景合规检查**（Scenario Analyzer）

#### 仍为 unknown 的项

1. wsf_oms_uci/lib/ 中 ASB 预编译库内部实现 — 外部闭源二进制库
2. wsf_argo8/argo8/models/ 预编译模型内部细节 — ARGO8 外部编译产物
3. maneuver/ 和 formation/ 子目录下完整类列表 — 仅读取核心类
4. wsf_iads_c2_lib/iadsLib/ 内部类详细信息 — 需深入 include/ 目录
5. OCI 自动生成头文件（8588 个）的生成逻辑 — 由外部 OCI 代码生成工具产生
6. 大部分 .cpp 实现文件的函数内部算法细节 — module 级分析

#### 复用指引

- 再次分析 wsf_plugins/ 时，直接读取已有索引文件作为起点
- 如需扩展到 `mission/`、`warlock/`、应用层，新建基线记录
- 如需 symbol 深度（逐函数 full signature + AST），在 module 索引基础上执行符号级增强

---

## 交付摘要

完成后向用户简要说明：

- 分析范围和排除范围。
- 生成或更新的索引与报告文件。
- 已确认的关键模块、生命周期阶段和扩展点。
- 仍为 `unknown` 或需要人工确认的问题。
