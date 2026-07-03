### 要求
一行一个依赖关系。

### 必填字段

- `schema_version`：固定为 `1`。
- `context`: 一句话描述依赖关系。
- `source`：依赖发起方文件或符号。
- `target`：依赖目标文件或符号。
- `relation`：`include`、`build`、`inheritance`、`composition`、`call`、`read`、`write`、`registration`、`configuration`、`runtime`、`test`、`unknown`。
- `path`：证据所在相对路径。
- `line_start`、`line_end`：证据行号；未知时为 `null`。
- `symbol`：相关符号名；不适用时为 `null`。
- `evidence`：短证据文本或证据摘要，不粘贴大段源码。
- `evidence_level`：证据等级。
- `notes`：补充说明数组。