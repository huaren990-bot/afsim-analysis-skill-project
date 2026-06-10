### 要求
一行一个函数方法。
`valid_range` 或 `typical_value` 字段尽量从注释、配置或使用上下文中推断，用于指导后续使用。

### 方法级功能必填字段

- `schema_version`：固定为 `1`。
- `function_name`：功能名称。
- `qualified_name`：限定名。
- `level`：`Method-level`。
- `brief`：简单描述函数功能和责任。
- `path`：定义所在相对路径。
- `line_start`、`line_end`：1-based 行号；未知时为 `null`。
- `return_type`：返回类型；未知时为 `unknown`。
- `parameters`：参数数组。
  - `name`：参数名。
  - `desc`：参数描述。
  - `input-output`:参数为输入参数还是输出参数。`input`、`output`。
  - `type`：参数数据类型。
  - `default_value`：默认值；未知时为 `unknown`。
  - `valid_range`：取值范围；未知时为 `unknown`。
- `calls`：静态可见的调用目标数组。
- `reads`：读取的关键字段、全局状态、配置项或输入对象数组。
- `writes`：写入的关键字段、状态或输出对象数组。
- `lifecycle_role`：`entry`、`scenario_load`、`object_create`、`simulation_loop`、`model_update`、`event_handling`、`output`、`shutdown`、`utility`、`unknown`。
- `algorithm_hint`：`math`、`state_update`、`routing`、`io`、`configuration`、`factory`、`none`、`unknown`。
- `dependencies`: 依赖的其他函数方法。
- `embedding`: embedding 字段预留给后续步骤生成向量表示，当前阶段填 `null`。
- `evidence_level`：证据等级。


### 系统级功能、模块级功能、类级功能必填字段

- `schema_version`：固定为 `1`。
- `function_name`：功能名称。
- `qualified_name`：限定名。
- `level`：`System-level`、`Module-level`、`Class-level`。
- `brief`：简单描述函数功能和责任。
- `sub-functions`：包含下一级别的功能数组。
- `evidence_level`：证据等级。