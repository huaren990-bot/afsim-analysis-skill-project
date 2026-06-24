# Phase 1 边界补充分析

> **日期**：2026-06-24
> **依据**：修改后的 `cpp-project-analyzer` skill、现有 Phase 1 产物、CodeGraph 查询、源码构建文件、人工检查报告 `人工检查report01.md`
> **状态**：已补充；2026-06-24 已处理 Phase 1 补充验证中的后续项

## 1. 补充结论

本次补充不重跑完整 Phase 1，而是在已有 `project-boundary.json`、`file-classification.jsonl`、`directory-tree.md` 基础上补齐大型 C++ 项目分析所需的边界说明。

核心结论：

1. 机器可读索引仍保留在 `workspace/`，Markdown 文档已迁移到 `docs/`。
2. `source_root/afsim-2_9/.codegraph` 存在，后续源码理解应优先使用 CodeGraph。
3. `swdev/src/CMakeLists.txt` 设置了 `CMAKE_EXPORT_COMPILE_COMMANDS ON`，但当前源码树下未生成 `compile_commands.json`。
4. 真实源码主线是 `afsim-2_9/swdev/src/`，其中 `core/` 是核心框架，`wsf_plugins/` 是插件集合，应用和工具目录是单独层级。
5. `demos/`、`documentation/`、`training/`、`resources/` 是发布资产、文档、培训实验或运行资源，默认不应作为架构依赖分析的源码模块。
6. 旧 Phase 1 中的 `extract_roots=["afsim-2_9","src"]` 遗留问题已处理：当前文件系统不存在 `source_root/src`，已从 `extract_roots`、`top_level_dirs`、`file-classification.jsonl` 和 `_classify-src*` 中移除顶层 `src/*` 记录。

## 2. 人工检查意见对应处理

| 人工检查意见 | Phase 1 处理 |
|--------------|--------------|
| Markdown 文件应放置到 `docs` | 已迁移现有 `.md` 产物，并更新 skill 输出路径。 |
| 目录总览需要详细完整，不能使用省略号 | `directory-tree.md` 保留完整树；本补充文档增加目录角色解释，避免只给树形列表而缺少含义。 |
| 模块级别如何区分，为什么 `source`、`wsf_six_dof`、`test` 同层 | 新增 `module_hierarchy`，按系统/子系统/模块三层解释，不再把普通目录名当同级模块语义。 |
| 子系统和模块需要区分 | 明确 `core_framework`、`plugin_modules`、`applications`、`developer_tools`、`non_architecture_assets`。 |
| `training` 路径不应进入依赖分析 | 新增 `recommended_exclude_paths_for_architecture`，后续 Phase 5-7 默认排除 `training`。 |

## 3. 源码证据

| 证据 | 位置 | 说明 |
|------|------|------|
| C++ 标准 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:32-34` | 设置 `CMAKE_CXX_STANDARD 14`。 |
| 编译数据库开关 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:36` | 设置 `CMAKE_EXPORT_COMPILE_COMMANDS ON`。 |
| 插件默认构建 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:45` | `WSF_PLUGIN_BUILD` 默认 `TRUE`。 |
| demos 默认不安装 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:48` | `WSF_INSTALL_DEMOS` 默认 `FALSE`。 |
| training 默认不安装 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:51` | `WSF_INSTALL_TRAINING` 默认 `FALSE`。 |
| documentation 默认不安装 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:52-53` | Doxygen 和 documentation 默认 `FALSE`。 |
| 模块标记机制 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:135-164` | 使用 `wsf_module` 查找扩展目录。 |
| 核心根 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:167-169` | 设置 `WSF_ROOT` 为 `PROJECT_SOURCE_DIR/core`。 |
| 工具根 | `source_root/afsim-2_9/swdev/src/CMakeLists.txt:171-172` | 设置 `TOOLS_DIRECTORY`。 |
| CodeGraph 证据 | `source_root/afsim-2_9/.codegraph` | `codegraph explore` 返回 `swdev/src/core/wsf_*` 与 `swdev/src/core/wsf_plugins` 相关源码片段和调用关系。 |

## 4. 建议边界

### 4.1 主分析根

| 层级 | 路径 | 角色 | 源码/头文件数 | 说明 |
|------|------|------|---------------|------|
| 系统 | `afsim-2_9/swdev/src/core` | 核心框架 | 2439 | 仿真框架、解析器、通信、军事、空间、工具基础库。 |
| 系统 | `afsim-2_9/swdev/src/wsf_plugins` | 插件集合 | 9881 | 可选插件和领域扩展。 |
| 系统 | `afsim-2_9/swdev/src/{engage,mission,mover_creator,mystic,post_processor,sensor_plot,warlock,weapon_tools,wizard}` | 应用层 | 2368 | 应用、可视化、后处理和编辑器。 |
| 系统 | `afsim-2_9/swdev/src/tools` | 开发工具 | 2491 | 构建/开发辅助工具和支撑库。 |

### 4.2 默认不进入架构依赖的根

| 路径 | 原因 | 处理方式 |
|------|------|----------|
| `afsim-2_9/demos` | 示例场景和演示数据，不是源码架构主线。 | 可作配置/场景证据，不进入模块依赖图。 |
| `afsim-2_9/documentation` | 发布文档和 HTML 文档。 | 可作文档证据，不进入源码模块。 |
| `afsim-2_9/training` | 培训实验和样例代码，CMake 默认不安装。 | 后续依赖分析默认排除；如需分析应单独设 scope。 |
| `afsim-2_9/resources` | 资源、shader、配置和数据文件。 | 仅在资源流/配置流使用。 |
| `src` | 当前 `source_root/src` 不存在。 | 已从 Phase 1 当前产物移除；仅在 `project-boundary.json.resolved_issues` 中保留处理记录。 |

## 4.3 后续问题处理结果（2026-06-24）

| 问题 | 处理结果 | 当前状态 |
|------|----------|----------|
| `file-classification.jsonl` 含 5 条顶层 `src/*` 旧记录 | 已删除 5 条顶层 `src/*`；`total_file_count` 从 43,591 更新为 43,586；`total_source_count` 保持 17,342。 | 已解决 |
| `extract_roots` 含不存在的 `src` | 已改为仅包含 `afsim-2_9`，并从 `top_level_dirs` 移除 `source_root/src`。 | 已解决 |
| `_classify-src*` 中间产物仍像有效输入 | `_classify-src.jsonl` 已清空，`_classify-src-summary.json` 标记为 `removed_stale_extract_root`。 | 已解决 |
| `training` 中有 152 个 source/header 文件 | 已在 `analysis_boundaries.secondary_reference_roots` 记录 `source_header_count=152`，并保持 `recommended_exclude_paths_for_architecture` 默认排除。 | 已处理为后续阶段约束 |
| 缺少 `compile_commands.json` | 当前源码树未发现该文件；CMake 已开启 `CMAKE_EXPORT_COMPILE_COMMANDS`，需要一次外部 CMake configure 才能生成。 | 待外部构建配置 |

## 5. 后续阶段约束

Phase 2 启动时应读取 `workspace/project-boundary/project-boundary.json` 中新增的 `analysis_boundaries` 和 `module_hierarchy` 字段，并遵守：

1. 模块概览按“系统 -> 子系统 -> 模块”组织。
2. `training`、`demos`、`documentation` 不作为默认模块清单。
3. 顶层 `src/*` 旧记录已移除；后续阶段不得重新引入不存在的 `source_root/src`。
4. 没有 `compile_commands.json` 时，Phase 3/4 需要将 AST/宏/include path 不确定性记录为 known issue。
5. 所有 Markdown 输出继续写入 `docs/`，所有 JSON/JSONL 继续写入 `workspace/`。
