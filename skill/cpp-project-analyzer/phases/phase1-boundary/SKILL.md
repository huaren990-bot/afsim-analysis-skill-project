---
name: cpp-proj-boundary
description: Phase 1: C++项目边界确认与结构发现 — 扫描目录树、识别构建系统、文件分类、模块识别。产出 project-boundary.json 和 file-classification.jsonl。
metadata:
  phase: 1
  requires-codegraph: false
  produces: project-boundary.json, file-classification.jsonl, directory-tree.md
---

# Phase 1: 项目边界确认与结构发现

## 目标

对 C++ 项目的源码根目录进行**粗粒度扫描**，识别：
- 目录结构与模块划分
- 构建系统类型
- 文件分类（源码/头文件/构建/配置/测试/示例/文档/生成文件）
- 分析边界与排除范围

本阶段不深入源码内容，侧重建立项目"骨架视图"。

## 输入要求

开始前确认以下输入：

- `source_root`：源码根目录绝对路径。
- `extract_roots`：本次需要解析的根目录数组。
- `analysis_scope`：用户指定的范围；未指定则默认覆盖整个 `extract_roots`。
- `exclude_paths`：排除目录列表。默认排除 `.git`、隐藏文件、`build/`、`3rd_party/`、`node_modules/`。
- `analysis_depth`：`full` | `module` | `overview`。

## 执行步骤

### Step 1: 目录树扫描

1. 使用 `find <extract_root> -maxdepth 4 -type d` 获取 4 层目录结构。
2. 识别 `CMakeLists.txt`、`Makefile`、`BUILD` 等构建标记文件位置。
3. 识别 `wsf_module` 或类似模块标记文件（如有）。
4. 记录顶级目录名称、文件计数、用途描述。

### Step 2: 构建系统分析

1. 读取顶层 `CMakeLists.txt`（如有），提取：
   - `project()` 名称
   - `cmake_minimum_required` 版本
   - C++ 标准（`CMAKE_CXX_STANDARD`）
   - 子目录引用（`add_subdirectory`）
   - 编译选项和宏定义
2. 统计 `CMakeLists.txt` 文件数量，识别构建层级。
3. 查找 `compile_commands.json`：
   - 优先位置：`<source_root>/compile_commands.json`、`<source_root>/build/compile_commands.json`、`<extract_root>/build/compile_commands.json`。
   - 若存在，记录路径、编译单元数量、覆盖到的 `.cpp/.cc/.cxx/.c` 文件数量。
   - 若不存在，在 `project-boundary.json.notes` 中记录 `"compile_commands.json not found; AST-level checks may be incomplete"`。
   - 禁止为寻找编译数据库递归扫描整个大仓库多次；使用一次 `find <source_root> -name compile_commands.json -maxdepth 4` 即可。

### Step 3: 模块识别

1. 根据目录中的 `CMakeLists.txt` 或 `wsf_module` 标记，将文件归类到模块。
2. 对于每个模块，记录：
   - 模块名称、路径、文件计数
   - 是否有独立构建目标
   - 是否为插件模块
3. 无明确模块归属的文件标记为 `module: "unknown"`。

### Step 4: 文件分类

用 `find` 或 `rg --files` 获取所有文件，然后对每个文件分类：

| file_type | 判断依据 |
|-----------|---------|
| `source` | `.cpp`, `.cc`, `.cxx`, `.c` |
| `header` | `.hpp`, `.hh`, `.h`, `.hxx` |
| `build` | `CMakeLists.txt`, `Makefile`, `.cmake`, `.mk` |
| `config` | `.json`, `.xml`, `.yaml`, `.ini`, `.cfg`, `.txt`（配置类） |
| `test` | 位于 `test/`、`tests/` 目录下，或文件名含 `test`/`_test` |
| `example` | 位于 `demo/`、`examples/`、`sample/` 目录下 |
| `doc` | `.md`, `.rst`, `.txt`（文档类），位于 `doc/` 目录 |
| `generated` | 自动生成的文件（如 `.pb.h`, `_generated.h`, 由代码生成器产生的文件） |
| `unknown` | 无法明确分类 |

完成分类后，必须生成覆盖基线统计：

1. `all_file_count`：纳入分析的全部文件数。
2. `cpp_file_count`：`source` + `header` 文件数。
3. `build_file_count`：构建文件数量。
4. `excluded_file_count`：被排除文件数量（如可统计）。
5. `files_to_index`：后续 Phase 2 必须覆盖的源码/头文件清单，来源为 `file_type in ["source","header"]`。

如果文件数超过 1000，必须在 `notes` 中建议后续 Phase 2-4 按模块或子目录分片；如果超过 10000，必须分片，不允许单 Agent 一次性深挖全部文件。

### Step 5: 目录树生成

1. 使用 `find <extract_root> -maxdepth 4 -type d` 获取 4 层目录结构。
2. 以树形文本格式（`├──`、`└──`、`│`）组织目录关系。
3. 统计每个顶级目录的文件数量和各级子目录数量。
4. 按模板 `template_directory-tree.md` 格式输出。

### Step 6: 生成输出

1. **project-boundary.json**：按模板 `template_project-boundary.md` 格式输出。
2. **file-classification.jsonl**：按模板 `template_file-classification.md` 格式输出。
3. **directory-tree.md**：按模板 `template_directory-tree.md` 格式输出。

## 输出文件

- `project-boundary/project-boundary.json`
- `project-boundary/file-classification.jsonl`
- `docs/architecture/directory-tree.md`

## 质量门槛

1. `project-boundary.json` 包含全部必填字段。
2. `file-classification.jsonl` 每行可被 JSON parser 解析。
3. 所有文件 100% 分类，无遗漏。
4. `module_count` 与实际识别的模块数一致。
5. `total_file_count` 与 file-classification.jsonl 行数一致。
6. 排除路径下的文件不纳入分类。
7. `directory-tree.md` 覆盖所有 `extract_roots`，深度为 4 层。
8. 若存在 `compile_commands.json`，必须记录其路径和编译单元数量；若不存在，必须在 `notes` 中说明。
9. `source` + `header` 文件必须形成后续 `files_to_index` 覆盖基线。

## 使用 CodeGraph 的策略

本阶段主要依赖 shell 命令（`find`、`rg`、`ls`），仅在需要快速了解项目整体结构时可使用：

```
codegraph explore "project main entry points and top-level architecture"
```

## 注意事项

- 不要深入源码文件内容，本阶段只做文件名和路径级别的分类。
- `generated` 类型的文件必须在 `notes` 中说明其生成来源（如 `protobuf generated`、`cmake configure_file output`）。
- 如果分析范围超过 10 万文件，在 Step 4 中询问用户是否需要缩小范围。

## ⚠️ 防重复工具调用

1. `find`、`rg --files`、`ls` 等命令在整个 Phase 内每个模式**只执行 1 次**。如第一次返回错误或空，改为换工具（如 `find` → `rg --files` → `ls -R`），不可用相同参数重试。
2. 读取 CMakeLists.txt 时，**每个文件只读 1 次**。如果多个模块引用同一 CMakeLists.txt，复用首次读取的内容。
3. 分类阶段**不要**对每个文件调用 `file` 命令或读取内容 — 仅基于路径和扩展名分类。
4. 维护一个 `已执行命令集合`，每次调用 shell 命令前先检查是否已执行过等价命令。
