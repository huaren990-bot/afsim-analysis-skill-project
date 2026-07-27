# cpp-project-analyzer 上游契约

## 必需文件

| 文件 | 本 skill 使用的关键字段 |
| --- | --- |
| `function-index.jsonl` | `candidate_id`、`function_name`、`qualified_name`、`canonical_qualified_name`、`level`、`path`、`line_start`、`line_end`、`parameters`、`calls`、`reads`、`writes`、`lifecycle_role`、`algorithm_hint`、`evidence_level` |
| `function-body-summary.jsonl` | `candidate_id`、`qualified_name`、`control_flow_summary`、`key_variables`、`computation_density`、`math_operations`、`algorithm_pattern` |
| `symbol-index.jsonl` | 类型、成员、继承、枚举和变量声明 |
| `dependency-index.jsonl` | include、inheritance、composition、call、registration 等关系 |
| `file-index.jsonl` | 文件归属、类型和模块上下文 |

## 记录过滤

- 仅把 `level == "Method-level"` 且 `path` 非空的记录作为算法候选。
- `function_name` 是短名称；`qualified_name` 是带重载摘要的稳定定位名称。卡片中的 Method 使用 `qualified_name`，不要搜索不存在的 `function` 字段。
- 用 `candidate_id` 作为跨 `function-index` 与 `function-body-summary` 的首选连接键。
- System-level、Module-level 和 Class-level 记录只用于上下文，不作为函数体候选。

## 模块解析

不得把 `path` 的第一级目录直接当模块。优先从路径中 `src/` 后的层级推导，例如：

- `.../src/core/wsf/...` → `core/wsf`
- `.../src/wsf_plugins/wsf_six_dof/...` → `wsf_plugins/wsf_six_dof`

如果目录布局不符合该形式，从 `file-index.jsonl` 或架构报告确认模块，并将无法确认的记录标为 `deferred`。

## 源码路径解析

索引路径可能包含 AFSIM 版本目录，也可能相对版本根目录。按以下顺序解析，命中后停止：

1. `<source-root>/<index-path>`
2. `<source-root-parent>/<index-path>`
3. 若 `<index-path>` 首段等于 `<source-root>` 目录名，使用 `<source-root>/<去掉首段后的路径>`

不得只凭文件名全盘搜索后静默选取同名文件。出现多个命中时，使用模块、qualified name 和行号消歧；仍不唯一则停止。

## 证据等级

1. `source-cited`：当前源码文件与行号直接支持。
2. `cross-source`：源码结论同时被调用链、配置、官方文档或演示支持。
3. `index-derived`：仅从索引推断，只能作为候选或待验证结论。
4. `inferred`：分析推断，必须写明假设和验证方法。
5. `unknown`：证据不足，不得提升为确定结论。

关于算法行为、公式、单位和状态更新的最终结论至少需要 `source-cited`。
