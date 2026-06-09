---
name: afsim-source-cognition
description: 当用户需要快速学习 AFSIM 源码、建立源码索引、理解目录结构、模块职责、核心类、函数索引、依赖关系、调用链、数据流、配置流、仿真生命周期，或生成可追溯的 AFSIM 架构认知报告时，使用本 skill。
metadata:
  short-description: 建立 AFSIM 源码认知索引和架构报告
---

# AFSIM 源码认知 Skill

## 目标

建立可追溯的 AFSIM 源码认知资产，服务后续算法提取、需求映射、功能迁移和知识沉淀。不要只复述目录结构；必须把源码路径、符号、生命周期、数据流和模块职责关联起来。

## 使用时机

使用本 skill 处理以下任务：

- 快速理解 AFSIM 总体源码结构、模块边界和核心职责。
- 为某个 AFSIM 模块建立文件、类、函数和依赖索引。
- 识别仿真初始化、场景加载、对象创建、模型更新、事件处理、输出和清理流程。
- 梳理状态对象、配置项、脚本或场景文件如何影响运行时行为。
- 生成 `workspace/source-index/` 索引和 `docs/architecture/` 架构报告。

如果用户请求算法公式、迁移代码或需求缺口分析，本 skill 只负责提供源码认知和候选位置；后续交给对应专项 skill。

## 输入要求

开始前确认以下输入，缺失时先从当前工作区探测，仍无法确认再询问用户：

- `source_root`：AFSIM 源码根目录。
- `analysis_scope`：本轮纳入的目录、模块、文件类型或用户指定主题。
- `exclude_paths`：构建产物、第三方依赖、缓存、临时文件和大体积生成目录。
- `baseline_docs`：用户提供的说明文档、历史报告、需求材料或已有索引。
- `analysis_depth`：`overview`、`module`、`symbol` 三档之一。

默认排除 `.git`、以 `.` 开头的文件，构建目录、包管理缓存、二进制产物和外部依赖镜像。不要在未说明范围的情况下扫描用户无关目录。

## 工作流

### 1. 确认边界

记录本轮分析的源码根目录、纳入范围、排除范围、分析深度和使用过的历史材料。所有正式产物都要能回到这个边界说明。

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

### 3. 建立符号索引

按“轻量扫描优先、AST 增强可选”的策略识别：

- `namespace`、`class`、`struct`、`enum`、`typedef`、`using`。
- 函数、成员函数、虚函数、模板函数、构造函数、析构函数。
- 入口点、生命周期回调、工厂注册、插件注册、配置解析函数。

跨文件声明和实现分离时，保留 `declaration_path` 与 `definition_path`。重载、模板和宏生成代码不能只按名称合并，必须保留签名或限定名。

### 4. 建立依赖索引

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

### 7. 生成报告

使用 `docs/templates/architecture-report.md` 生成或更新 `docs/architecture/afsim-architecture.md`。报告必须包含范围、模块图、生命周期、数据流、配置流、扩展点、关键符号、未知项和源码证据。

## 输出文件

所有索引写入 `workspace/source-index/`，使用 UTF-8 JSONL。每行必须是一个完整 JSON object，不允许尾逗号、注释、Markdown 代码块或跨行 JSON。字段缺失时使用 `null`、空数组或 `unknown`，不要省略必填字段。

### `file-index.jsonl`

一行一个文件。必填字段：

- `schema_version`：固定为 `1`。
- `path`：相对 `source_root` 的路径。
- `absolute_path`：源码文件绝对路径；无法稳定记录时为 `null`。
- `language`：`cpp`、`c`、`cmake`、`xml`、`json`、`yaml`、`python`、`shell`、`text`、`unknown`。
- `file_type`：`source`、`header`、`build`、`config`、`test`、`example`、`doc`、`generated`、`unknown`。
- `module`：模块名；无法确认时为 `unknown`。
- `responsibility`：一句话职责；不能确认时为 `unknown`。
- `key_symbols`：本文件关键符号数组。
- `includes`：直接 include/import 的路径数组。
- `evidence_level`：证据等级。
- `notes`：补充说明数组。

### `symbol-index.jsonl`

一行一个符号。必填字段：

- `schema_version`：固定为 `1`。
- `symbol`：短名称。
- `qualified_name`：含命名空间或类名的限定名；无法确认时等于 `symbol`。
- `kind`：`namespace`、`class`、`struct`、`enum`、`function`、`method`、`constructor`、`destructor`、`typedef`、`using`、`macro`、`variable`、`unknown`。
- `path`：定义所在相对路径。
- `line_start`、`line_end`：1-based 行号；未知时为 `null`。
- `signature`：函数或类型签名；不适用时为 `null`。
- `owner`：所属类、命名空间或模块；无所属时为 `null`。
- `declaration_path`：声明文件路径；未知时为 `null`。
- `definition_path`：实现文件路径；未知时为 `null`。
- `base_symbols`：基类或接口数组。
- `responsibility`：源码证据支持的职责描述。
- `evidence_level`：证据等级。

### `function-index.jsonl`

一行一个函数或方法。必填字段：

- `schema_version`：固定为 `1`。
- `function`：短名称。
- `qualified_name`：限定名。
- `path`：定义所在相对路径。
- `line_start`、`line_end`：1-based 行号；未知时为 `null`。
- `return_type`：返回类型；未知时为 `unknown`。
- `parameters`：参数数组，元素包含 `name`、`type`、`default`。
- `calls`：静态可见的调用目标数组。
- `reads`：读取的关键字段、全局状态、配置项或输入对象数组。
- `writes`：写入的关键字段、状态或输出对象数组。
- `lifecycle_role`：`entry`、`scenario_load`、`object_create`、`simulation_loop`、`model_update`、`event_handling`、`output`、`shutdown`、`utility`、`unknown`。
- `algorithm_hint`：`math`、`state_update`、`routing`、`io`、`configuration`、`factory`、`none`、`unknown`。
- `evidence_level`：证据等级。

### `dependency-index.jsonl`

一行一个依赖关系。必填字段：

- `schema_version`：固定为 `1`。
- `source`：依赖发起方文件或符号。
- `target`：依赖目标文件或符号。
- `relation`：`include`、`build`、`inheritance`、`composition`、`call`、`read`、`write`、`registration`、`configuration`、`runtime`、`test`、`unknown`。
- `path`：证据所在相对路径。
- `line_start`、`line_end`：证据行号；未知时为 `null`。
- `symbol`：相关符号名；不适用时为 `null`。
- `evidence`：短证据文本或证据摘要，不粘贴大段源码。
- `evidence_level`：证据等级。
- `notes`：补充说明数组。

### 架构文档

- `docs/architecture/afsim-architecture.md`：总体架构认知报告。
- `docs/architecture/module-dependency.md`：模块依赖说明；可包含 Mermaid 图，但图中的边必须能追溯到 `dependency-index.jsonl` 或源码位置。

## 证据等级

只能使用以下值：

- `source-cited`：由源码路径、符号和行号直接支持。
- `document-cited`：由用户文档、设计文档或历史报告支持。
- `index-derived`：由本轮生成的索引汇总得到。
- `inferred`：由相邻证据推断，但源码未直接说明。
- `unknown`：证据不足。

重要架构结论优先使用 `source-cited`。`inferred` 结论必须说明推断依据；`unknown` 必须进入报告的未知项。

## 质量门槛

交付前检查：

- 四个 JSONL 索引文件存在，且每行都能被 JSON parser 解析。
- 每个 JSON object 都包含对应文件的必填字段和 `schema_version`。
- 枚举字段只使用本 skill 规定的值。
- 文件路径相对 `source_root` 可定位；行号使用 1-based 编号。
- 架构报告包含模板要求的全部章节。
- 模块职责、生命周期、数据流、配置流和扩展点都有证据等级。
- 不把文件名相似、路径相近或命名相近当作功能等价证据。
- 未阅读、无法解析或证据不足的内容标记为 `unknown` 或 `inferred`。
- 输出只记录可审查的证据、假设、决策、结论和风险，不记录隐藏推理过程。

## 交付摘要

完成后向用户简要说明：

- 分析范围和排除范围。
- 生成或更新的索引与报告文件。
- 已确认的关键模块、生命周期阶段和扩展点。
- 仍为 `unknown` 或需要人工确认的问题。
