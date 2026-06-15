# file-classification.jsonl

## 要求

一行一个文件。

## 必填字段

- `schema_version`：固定为 `1`。
- `path`：相对 `source_root` 的路径。
- `absolute_path`：文件绝对路径；无法确定时为 `null`。
- `language`：`cpp` | `c` | `cmake` | `xml` | `json` | `yaml` | `python` | `shell` | `text` | `unknown`。
- `file_type`：`source` | `header` | `build` | `config` | `test` | `example` | `doc` | `generated` | `unknown`。
- `module`：所属模块名；无法确认时为 `unknown`。
- `line_count`：文件行数。
- `size_bytes`：文件大小（字节）。
- `brief`：一句话描述文件职责。
- `evidence_level`：证据等级。
- `notes`：补充说明数组。
