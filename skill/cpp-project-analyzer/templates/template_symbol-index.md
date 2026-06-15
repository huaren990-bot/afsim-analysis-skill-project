# symbol-index.jsonl

## 要求

一行一个符号。覆盖所有 class、struct、enum、typedef、using、macro、variable 定义（剔除前向声明和 `*_EXPORT` 宏）。

## 必填字段

- `schema_version`：固定为 `1`。
- `symbol_name`：符号标识名称。
- `qualified_name`：含命名空间或类名的限定名；无法确认时等于 `symbol_name`。
- `kind`：`namespace` | `class` | `struct` | `enum` | `enum_class` | `function` | `method` | `constructor` | `destructor` | `typedef` | `using` | `macro` | `variable` | `unknown`。
- `type`：符号的数据类型。对于 class/struct 填写其完全限定名；对于变量填写其声明的类型；对于 function/method 填写返回类型；对于 macro 填写替换体类型（如 `int`、`string`、`expression`）。
- `owner`：所属类、命名空间或模块；无所属时为 `null`。
- `path`：定义所在相对路径。
- `line_start`、`line_end`：1-based 行号；未知时为 `null`。
- `signature`：函数或类型完整签名；不适用时为 `null`。
- `declaration_path`：声明文件路径；未知时为 `null`。
- `definition_path`：实现文件路径；未知时为 `null`。
- `initial_value`：变量/宏/枚举的初始值；不适用时为 `null`。
- `base_symbols`：基类或接口数组；不适用时为 `[]`。
- `access_modifier`：`public` | `protected` | `private` | `null`（非类成员时为 null）。
- `is_virtual`：是否为虚函数；不适用时为 `null`。
- `is_static`：是否为静态成员；不适用时为 `null`。
- `is_const`：是否为 const 成员函数；不适用时为 `null`。
- `used_by`：使用该符号的类或函数数组。
- `brief`：源码证据支持的职责描述。
- `responsibility`：更详细的职责说明。
- `evidence_level`：证据等级。
- `notes`：补充说明数组。
