### 要求
一行一个符号。

### 必填字段

- `schema_version`：固定为 `1`。。
- `brief`：简单描述符号的功能和责任。
- `symbol_name`：符号标识名称。
- `qualified_name`：含命名空间或类名的限定名；无法确认时等于 `symbol`。
- `kind`：`namespace`、`class`、`struct`、`enum`、`function`、`method`、`constructor`、`destructor`、`typedef`、`using`、`macro`、`variable`、`unknown`。
- `type`: 符号数据类型。
- `owner`: 所属类、命名空间或模块；无所属时为 `null`。
- `path`：定义所在相对路径。
- `line_start`、`line_end`：1-based 行号；未知时为 `null`。
- `signature`：函数或类型签名；不适用时为 `null`。
- `owner`：所属类、命名空间或模块；无所属时为 `null`。
- `declaration_path`：声明文件路径；未知时为 `null`。
- `definition_path`：实现文件路径；未知时为 `null`。
- `initial_value`: 值。
- `used_by`: 使用该符号的类或函数。
- `base_symbols`：基类或接口数组。
- `responsibility`：源码证据支持的职责描述。
- `evidence_level`：证据等级。