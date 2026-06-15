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

   对每个函数提取：
   - 完整参数列表（名称、类型、默认值、方向）
   - 返回类型
   - 识别函数体内调用的其他函数（`calls`）
   - 识别读/写的成员变量和全局状态（`reads`、`writes`）
   - 分类 `lifecycle_role`
   - 分类 `algorithm_hint`

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

## 质量门槛

1. **必须同时包含** System-level、Module-level、Class-level、Method-level 四层条目。
2. System/Module/Class 级条目的 `brief` 不可为空。
3. Method-level 条目的 `parameters` 数组已填写参数信息（至少 `name` + `type`）。无法解析全部参数的条目在 `notes` 中标记 "待AST解析"。
4. `qualified_name` 全文件唯一。
5. 每个 `sub_functions` 数组中的 qualified_name 可在本文件的更低层级中找到对应条目。
6. `lifecycle_role` 为 `unknown` 的 Method-level 条目比例不应超过 50%。

## 并行化策略

按模块并行执行 Step 2（Method-level 提取），每个模块一个 Agent。
