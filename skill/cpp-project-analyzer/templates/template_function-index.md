# function-index.jsonl

## 要求

一行一个函数/方法。**必须同时包含 System-level、Module-level、Class-level、Method-level 四层条目**，不可只有 Method-level 一层。

## Method-level 必填字段

- `schema_version`：固定为 `1`。
- `function_name`：函数短名称。
- `qualified_name`：限定名（含命名空间::类名::函数名），全文件唯一。
- `level`：`Method-level`。
- `brief`：简单描述函数功能和责任。
- `path`：定义所在相对路径。
- `line_start`、`line_end`：1-based 行号；未知时为 `null`。
- `return_type`：返回类型；未知时为 `unknown`。
- `parameters`：参数数组，每个含：
  - `name`：参数名。
  - `desc`：参数描述（中文）。
  - `input_output`：`input` | `output` | `inout`。
  - `type`：参数数据类型。
  - `default_value`：默认值表达式；无默认值时为 `null`；未知时为 `"unknown"`。
  - `valid_range`：取值范围说明；未知时为 `"unknown"`。
- `calls`：静态可见的调用目标数组。
- `reads`：读取的关键字段、全局状态、配置项或输入对象数组。
- `writes`：写入的关键字段、状态或输出对象数组。
- `lifecycle_role`：`entry` | `scenario_load` | `object_create` | `simulation_loop` | `model_update` | `event_handling` | `output` | `shutdown` | `utility` | `unknown`。
- `algorithm_hint`：`math` | `state_update` | `routing` | `io` | `configuration` | `factory` | `control_flow` | `none` | `unknown`。
- `dependencies`：依赖的其他函数 qualified_name 数组。
- `is_virtual`：是否为虚函数。
- `is_override`：是否为 override。
- `is_const`：是否为 const 成员函数。
- `is_static`：是否为静态函数。
- `access_modifier`：`public` | `protected` | `private` | `null`（非成员函数）。
- `embedding`：embedding 字段预留给后续步骤生成向量表示，当前阶段填 `null`。
- `evidence_level`：证据等级。
- `notes`：补充说明数组。

## System/Module/Class-level 必填字段

- `schema_version`：固定为 `1`。
- `function_name`：功能名称（中文）。
- `qualified_name`：限定名，全文件唯一。
- `level`：`System-level` | `Module-level` | `Class-level`。
- `brief`：简单描述功能，**不可为空**。
- `sub_functions`：包含下一级别功能的 qualified_name 数组。
- `evidence_level`：证据等级。
- `notes`：补充说明数组。
