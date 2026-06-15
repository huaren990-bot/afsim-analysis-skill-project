# macro-index.jsonl

## 要求

一行一个宏定义。仅包含 `#define` 定义的宏常量（含带参数的函数宏），不包含 `*_EXPORT` 导出宏和 include guards (`_HPP`、`_H_` 后缀)。

## 必填字段

- `schema_version`：固定为 `1`。
- `macro_name`：宏名称。
- `path`：定义所在相对路径。
- `line_start`：1-based 行号。
- `replacement`：替换体文本（完整记录）。
- `has_parameters`：是否为带参数的函数宏（`true`/`false`）。
- `parameter_names`：参数名称数组；无参数时为 `[]`。
- `macro_type`：`constant` | `expression` | `function_like` | `include_guard` | `export_macro` | `other`。
- `estimated_type`：推断的替换体类型（如 `int`、`double`、`string`、`expression`）。
- `brief`：宏的用途描述。
- `used_in_files`：使用该宏的文件路径数组。
- `evidence_level`：证据等级。
