---
name: cpp-proj-functions
description: Phase 4: 函数/方法级深度提取 — 生成四层 function-index.jsonl 和函数体摘要 function-body-summary.jsonl。
metadata:
  phase: 4
  requires-codegraph: true
  produces: function-index.jsonl, function-body-summary.jsonl
---

# Phase 4: 函数/方法级深度提取

## 目标

在 Phase 3 符号精细化的基础上，对每个函数/方法进行**最深粒度**的提取：
- 完整的参数列表（含默认值、输入/输出方向、取值范围）
- 返回类型
- 函数体内调用链
- 读/写的关键状态
- 生命周期角色分类
- 算法模式识别
- 四层功能层次（System → Module → Class → Method）

本阶段是后续算法提取的**关键输入**。

## 输入

- `project-boundary/project-boundary.json`（Phase 1 产出）
- `source-index/file-index.jsonl`（Phase 2 产出）
- `source-index/symbol-index.jsonl`（Phase 3 精细化版）
- `source-index/macro-index.jsonl`（Phase 3 产出）
- `source-index/enum-index.jsonl`（Phase 3 产出）

## 执行步骤

### Step 1: 确定函数清单

从 Phase 3 的 `symbol-index.jsonl` 中筛选 `kind` 为 `function`、`method`、`constructor`、`destructor` 的条目，得到待提取函数清单 F。

候选进入 F 前必须通过函数真实性过滤：

1. `kind` 必须是 `function`、`method`、`constructor`、`destructor` 之一。
2. `signature` 必须包含函数参数括号 `(` 与 `)`，构造/析构函数也必须有可验证声明行。
3. `qualified_name`、`function_name`、`owner` 不得匹配 `.*(_EXPORT|_IMPORT|_API|_LIB_EXPORT)(::.*)?$`。
4. 若条目来自 macro-index 或变量/成员变量扫描结果，不能直接进入 F；只能作为 `macro_generated_unexpanded` 或 `variable_not_function` 跳过原因记录。
5. 类似 `POST_PROCESSOR_LIB_EXPORT::max` 的条目必须判定为导出宏伪成员/变量污染，不得生成 Method-level 条目。

补充候选来源，避免漏掉 Phase 3 未显式标出的函数：

1. 从 `file-index.jsonl.functions` 合并函数名候选。
2. 从已记录的头文件 inline 函数、模板函数、operator 重载、匿名 namespace/static 函数中补充候选。
3. 从 `compile_commands.json` 覆盖的编译单元中识别源文件清单，确保每个编译单元至少被纳入按文件读取分组。
4. 构建 `functions_to_extract` 基线，唯一键为 `qualified_name + signature + definition_path/declaration_path`。
5. 对同名重载函数，如果无法确定完整签名，必须在 `qualified_name` 中追加参数类型摘要，例如 `Class::Foo(int,double)`；禁止只用 `Class::Foo` 覆盖多条记录。
6. 对被真实性过滤剔除的候选，写入跳过统计，原因只能使用：`export_macro_pseudo_symbol`、`variable_not_function`、`macro_generated_unexpanded`、`declaration_only`、`parse_failed`。

### Step 2: 构建四层功能层次

**由底向上构建**：

1. **Method-level**：**按文件分组批量提取**（⚠️ 禁止逐函数调用 codegraph_node）：

   ```
   将函数清单 F 按所在文件 file_path 分组
   for each file_path in 分组:
       读取 file_path 一次（优先 codegraph_node，失败则 Read）
       从该文件内容中一次性提取所有 F 中函数的细节
       若 codegraph_node 与 Read 均失败 → 标记这些函数为 evidence_level: "unknown"，不重试
   ```

   **头文件声明到源文件定义增强匹配（强制）**：
   - 对每个候选函数，不得只搜索 `path` 或 `definition_path`。必须构建搜索文件集合：
     1. `definition_path`
     2. `path`
     3. `declaration_path`
     4. 与上述路径同 stem 的 `.hpp/.h/.hh/.hxx/.cpp/.cc/.cxx/.C/.inl/.ipp/.tpp`
     5. 从 `owner` / `qualified_name` 提取类名后，与该类名同 stem 的 `.hpp/.h/.hh/.hxx/.cpp/.cc/.cxx/.C/.inl/.ipp/.tpp`
   - 搜索文件集合必须去重，并且每个文件最多读取一次，文件内容进入缓存后供同批次全部候选复用。
   - 若声明头文件名与实现类名不同，例如 `Bounds.hpp` 声明 `TimeBounds` 而 `TimeBounds.cpp` 存放定义，必须通过类名 stem 搜索补齐，不得直接判定为 `declaration_only`。
   - 若函数体命中 `declaration_path` 或同名头/inline 文件，应把 Method-level 的 `path`、`line_start`、`line_end` 写为真实命中文件和行号，并在 `notes` 中记录 `"函数体命中声明/同名头文件: <path>"`。
   - 对头文件 inline getter/setter、模板成员、类内短函数体，必须优先生成 Method-level 条目，不能因为 `definition_path` 指向 `.cpp` 而误判为 `declaration_only`。
   - 匹配函数体时必须跳过字符串、行注释、块注释，以及参数列表后的行尾注释（如 `) // = 0`），避免多行函数定义被误判为无函数体。
   - 若 `qualified_name + signature_digest` 仍重复，必须追加稳定候选 ID 或路径摘要作为最后兜底，确保 `qualified_name` 全文件唯一。
   - 只有在上述搜索集合全部未定位到函数体时，才允许记录 `declaration_only`。
   - 推荐复用项目脚本 `tools/indexers/phase4_extract_batch.py --batch-id <batch_id> --root <project_root>` 执行批次提取；该脚本已实现上述增强匹配、文件缓存、重载签名摘要和批次跳过清单。

   对每个函数提取：
   - 完整参数列表（名称、类型、默认值、方向）
   - 返回类型
   - 识别函数体内调用的其他函数（`calls`）
   - 识别读/写的成员变量和全局状态（`reads`、`writes`）
   - 分类 `lifecycle_role`
   - 分类 `algorithm_hint`
   - 记录条件编译上下文（如函数体位于 `#ifdef` 分支内）
   - 对模板函数记录模板参数；无法实例化时不生成虚假实例化条目

   **防重复保护**：
   - 同一 file_path 在 Method-level 阶段只读 1 次（即使含 50 个函数）。
   - 若函数实现跨多个 .cpp 文件，每个 .cpp 也只读 1 次。
   - 维护 `已读文件集合`，任何读取前先检查。

2. **Class-level**：对每个 class/struct，汇总其所有 Method-level 功能：
   - `function_name`：以类的核心职责命名（中文），如 "轨道预报器"
   - `qualified_name`：类的限定名
   - `sub_functions`：该类所有 Method-level 功能的 qualified_name 数组
   - `brief`：类的核心职责描述（必须非空）

3. **Module-level**：对每个模块，汇总其所有 Class-level 功能：
   - `function_name`：以模块的核心职责命名（中文）
   - `qualified_name`：模块的限定名
   - `sub_functions`：该模块所有 Class-level 功能的 qualified_name 数组
   - `brief`：模块的核心职责描述（必须非空）

4. **System-level**：跨模块汇总：
   - `function_name`：以系统级功能命名（中文），如 "仿真生命周期管理"
   - `qualified_name`：系统级功能的限定名
   - `sub_functions`：该系统功能涉及的 Module-level 功能数组
   - `brief`：系统功能的端到端描述（必须非空）

### Step 3: 生成 function-body-summary.jsonl（复用已读文件）

**⚠️ 关键规则：复用 Step 2 已读过的文件内容，不发起新的读取。禁止逐函数调用 codegraph_node。**

对每个 Method-level 条目：

1. **优先复用** Step 2 中已经读取过的该函数所在文件内容。
2. 仅当 Step 2 未读过该文件时，才读取一次（`Read <file_path>`）。
3. 从函数体源码中分析：
   - `computation_density`：统计数学运算符、矩阵调用、迭代循环的密度。
   - `math_operations`：查找矩阵乘法、积分、插值、优化等操作。
   - `algorithm_pattern`：匹配已知算法模式（Kalman、RK4、Monte Carlo 等）。
   - `key_variables`：识别函数中的关键变量及其角色。
   - `control_flow_summary`：用中文撰写主要分支和循环结构。
4. **防重复保护**：
   - 同一 file_path 在本 Step 内绝不重复读取。
   - 若函数体跨多个文件（如 template 特化），每个文件也只读 1 次。
   - 若读取失败，将该函数标记为 `computation_density: "unknown"` 并继续，不重试。

### Step 3.5: 函数覆盖闭环

在生成 `function-index.jsonl` 前必须闭环 `functions_to_extract`：

1. 对每个候选函数，必须生成一个 Method-level 条目，或记录跳过原因：
   - `declaration_only`：只有声明无函数体。
   - `implicit_special_member`：隐式构造/析构/赋值函数。
   - `macro_generated_unexpanded`：宏生成，无法展开。
   - `variable_not_function`：变量、局部对象直接初始化、throw/return/typeid/流输出表达式等被旧索引误识别为函数。
   - `template_uninstantiated`：模板声明无法确定实例化。
   - `parse_failed`：源码解析失败。
2. 计算函数候选覆盖率：`Method-level 条目数 / 有效候选数量`；有效候选数量必须从 `functions_to_extract` 中剔除明确的 `variable_not_function` 误报，同时保留 `raw_coverage = Method-level 条目数 / functions_to_extract 原始数量`。
3. 对未覆盖项列出前 50 项，并把完整清单写入 context-handoff 或验证报告。
4. 覆盖率低于 90% 时，本阶段不得标记为完全通过，除非用户明确缩小分析范围。

### Step 4: 参数默认值特殊处理

对于参数的 `default_value` 字段：

1. 如果默认值是字面量（如 `0.0`、`true`、`nullptr`），直接记录。
2. 如果默认值引用其他常量（如 `std::numeric_limits<size_t>::max()`），记录完整表达式并附加说明引用关系。
3. 如果默认值依赖全局变量或编译宏，记录依赖关系并在 `notes` 中标记。

### Step 5: 生命周期角色分类指导

| lifecycle_role | 判断依据 |
|----------------|---------|
| `entry` | main()、应用启动、命令行解析 |
| `scenario_load` | 解析场景文件、读取配置、创建初始对象 |
| `object_create` | new/工厂创建、对象初始化、注册 |
| `simulation_loop` | 时间推进、帧步进、主循环 |
| `model_update` | 物理模型更新、状态更新、动力学计算 |
| `event_handling` | 事件发布、订阅、分发、响应 |
| `output` | 日志、结果文件写入、可视化输出 |
| `shutdown` | 资源释放、析构、清理 |
| `utility` | 通用工具函数（数学、字符串、IO 辅助） |
| `unknown` | 无法确定（必须在 notes 中说明原因） |

### Step 6: 算法提示分类指导

| algorithm_hint | 判断依据 |
|----------------|---------|
| `math` | 含数学公式、矩阵运算、数值积分、优化求解 |
| `state_update` | 更新对象状态变量（非数学密集型） |
| `routing` | 路径搜索、图算法、最短路径 |
| `io` | 文件读写、网络IO、序列化/反序列化 |
| `configuration` | 解析配置、设置参数、构建对象 |
| `factory` | 工厂方法、对象创建、注册 |
| `control_flow` | 状态机、决策树、行为树节点 |
| `none` | 无特殊算法（getter/setter/简单转发） |
| `unknown` | 无法确定 |

## 输出文件

- `source-index/function-index.jsonl`
- `source-index/function-body-summary.jsonl`

批次产物全部完成后，推荐使用项目脚本合并最终四层产物：

```bash
python3 tools/indexers/phase4_merge_outputs.py --root <project_root>
```

该脚本负责合并 `phase4-batches/` 下的 Method-level 与 body summary，回填候选元数据，构建 Class/Module/System 三层聚合，输出最终 `function-index.jsonl`、`function-body-summary.jsonl` 和 `phase4-function-skips.jsonl`。

## 质量门槛

1. **必须同时包含** System-level、Module-level、Class-level、Method-level 四层条目。
2. System/Module/Class 级条目的 `brief` 不可为空。
3. Method-level 条目的 `parameters` 数组已填写参数信息（至少 `name` + `type`）。无法解析全部参数的条目在 `notes` 中标记 "待AST解析"。
4. `qualified_name` 全文件唯一。
5. 每个 `sub_functions` 数组中的 qualified_name 可在本文件的更低层级中找到对应条目。
6. `lifecycle_role` 为 `unknown` 的 Method-level 条目比例不应超过 50%。
7. `functions_to_extract` 覆盖率必须 ≥ 90%，未覆盖项必须有跳过原因。
8. 重载函数的 `qualified_name` 必须唯一且能区分签名；不得静默覆盖。
9. 头文件 inline 函数、模板函数声明、operator 重载、匿名 namespace/static 函数必须纳入候选或明确记录跳过原因。
10. `function-index.jsonl` 不得包含导出宏伪函数、变量/成员变量伪函数，且所有 Method-level 条目必须有可验证函数签名。

## 并行化策略

按模块并行执行 Step 2（Method-level 提取），每个模块一个 Agent。
