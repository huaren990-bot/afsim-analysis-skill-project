# dependency-index.jsonl

## 要求

一行一个依赖关系。必须覆盖至少 6 种 `relation` 类型：`build`、`inheritance`、`composition`、`include`、`call`、`registration`。条目数不少于 200。

## 必填字段

- `schema_version`：固定为 `1`。
- `source`：依赖发起方文件或符号（qualified_name 或文件路径）。
- `target`：依赖目标文件或符号（qualified_name 或文件路径）。
- `relation`：`include` | `build` | `inheritance` | `composition` | `call` | `read` | `write` | `registration` | `configuration` | `runtime` | `test` | `unknown`。
- `context`：一句话中文描述依赖关系的含义。
- `path`：证据所在相对路径（源文件路径）。
- `line_start`、`line_end`：证据行号；未知时为 `null`。
- `symbol`：与此依赖相关的核心符号名；不适用时为 `null`。
- `evidence`：短证据文本或证据摘要（如 "class WsfHEL_Lethality : public WsfWeaponEffects"）。
- `evidence_level`：证据等级。
- `strength`：`strong` | `medium` | `weak`。
  - `strong`：编译期依赖，缺少则编译失败（继承、值类型成员、include、build）。
  - `medium`：逻辑依赖，运行时通常需要但有默认/null 替代（指针成员、可选策略）。
  - `weak`：松耦合，仅在特定场景使用（日志、调试、可选功能）。
- `notes`：补充说明数组。
