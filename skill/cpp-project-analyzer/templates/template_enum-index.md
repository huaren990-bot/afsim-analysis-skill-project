# enum-index.jsonl

## 要求

一行一个枚举定义。

## 必填字段

- `schema_version`：固定为 `1`。
- `enum_name`：枚举名称。
- `qualified_name`：含命名空间或类名的限定名。
- `kind`：`enum` | `enum_class`。
- `owner`：所属类或命名空间；无所属时为 `null`。
- `path`：定义所在相对路径。
- `line_start`、`line_end`：1-based 行号。
- `underlying_type`：底层类型（如 `int`、`uint32_t`）；未知时为 `unknown`。
- `values`：枚举值数组，每个含：
  - `name`：枚举值名称。
  - `value`：显式赋值（字符串形式）；无显式赋值时为 `"implicit"`。
  - `brief`：该枚举值的含义。
- `brief`：枚举整体用途描述。
- `used_in_files`：使用该枚举的文件路径数组。
- `evidence_level`：证据等级。
