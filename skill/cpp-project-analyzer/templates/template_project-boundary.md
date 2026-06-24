# project-boundary.json

## 要求

单文件 JSON object（非 JSONL），描述项目分析边界。

## 必填字段

- `schema_version`：固定为 `1`。
- `source_root`：源码根目录绝对路径。
- `extract_roots`：本次分析纳入的所有根目录数组。
- `exclude_paths`：本次排除的目录和文件模式数组。
- `analysis_depth`：`full` | `module` | `overview`。
- `language_standard`：如 `C++14`、`C++17`、`C++20`、`unknown`。
- `build_system`：`CMake` | `Makefile` | `Bazel` | `Meson` | `Visual Studio` | `Xcode` | `unknown` | `mixed`。
- `compile_commands`：编译数据库信息对象。不存在时 `exists=false`，并在 `notes` 说明影响。
  - `exists`：是否找到 `compile_commands.json`。
  - `path`：编译数据库路径；不存在时为 `null`。
  - `translation_unit_count`：编译单元数量；未知时为 `null`。
  - `covered_source_count`：编译数据库覆盖到的源码文件数量；未知时为 `null`。
- `total_file_count`：纳入分析的文件总数。
- `total_source_count`：源码文件(.h/.hpp/.c/.cpp/.cxx)总数。
- `module_count`：识别到的模块数（若有模块结构）。
- `modules`：模块数组，每个模块含以下字段：
  - `name`：模块名称。
  - `path`：模块根目录（相对 source_root）。
  - `file_count`：模块内文件数。
  - `source_count`：模块内源码文件数。
  - `has_cmake`：是否有 CMakeLists.txt。
  - `is_plugin`：是否为插件模块。
  - `brief`：模块简述。
- `top_level_dirs`：顶级目录数组，每个含 `name`、`path`、`file_count`、`brief`。
- `evidence_level`：证据等级。
- `notes`：补充说明。

## 示例

```json
{
  "schema_version": "1",
  "source_root": "/path/to/project",
  "extract_roots": ["src/core", "src/plugins"],
  "exclude_paths": [".git", "build", "3rd_party"],
  "analysis_depth": "full",
  "language_standard": "C++14",
  "build_system": "CMake",
  "compile_commands": {
    "exists": true,
    "path": "/path/to/project/build/compile_commands.json",
    "translation_unit_count": 1200,
    "covered_source_count": 1180
  },
  "total_file_count": 5000,
  "total_source_count": 3500,
  "module_count": 15,
  "modules": [
    {
      "name": "wsf",
      "path": "src/core/wsf",
      "file_count": 400,
      "source_count": 380,
      "has_cmake": true,
      "is_plugin": false,
      "brief": "基础仿真框架核心库"
    }
  ],
  "top_level_dirs": [
    {"name": "src", "path": "src", "file_count": 4500, "brief": "源代码主目录"},
    {"name": "tests", "path": "tests", "file_count": 300, "brief": "测试代码"}
  ],
  "evidence_level": "source-cited",
  "notes": ["analyzed via bash find + codegraph_explore"]
}
```
