### 要求
一行一个文件。

### 必填字段

- `schema_version`：固定为 `1`。
- `path`：相对 `source_root` 的路径。
- `absolute_path`：源码文件绝对路径；无法稳定记录时为 `null`。
- `language`：`cpp`、`c`、`cmake`、`xml`、`json`、`yaml`、`python`、`shell`、`text`、`unknown`。
- `file_type`：`source`、`header`、`build`、`config`、`test`、`example`、`doc`、`generated`、`unknown`。
- `module`：模块名；无法确认时为 `unknown`。
- `key_symbols`：本文件关键符号数组。
- `functions`: 文件中包含的方法级功能名称数组。
- `includes`：直接 include/import 的路径数组。
- `line_count`：文件的行数。
- `brief`：文件内容和职责的简单描述。
- `evidence_level`：证据等级。
- `notes`：补充说明数组。