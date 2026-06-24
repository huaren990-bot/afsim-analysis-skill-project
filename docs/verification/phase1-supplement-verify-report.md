# Phase 1 补充验证报告

> **日期**：2026-06-24
> **验证对象**：`workspace/project-boundary/project-boundary.json`、`docs/project-boundary/directory-tree.md`、`docs/project-boundary/phase1-boundary-supplement.md`
> **验证目的**：检查修改后 skill 要求的 Phase 1 补充项是否已落地，并记录 2026-06-24 后续问题处理状态。

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | Markdown 输出位置 | 通过 | `directory-tree.md` 与补充文档均位于 `docs/project-boundary/`。 |
| 2 | CodeGraph 状态 | 通过 | `project-boundary.json.codegraph.exists=true`，路径为 `source_root/afsim-2_9/.codegraph`。 |
| 3 | compile_commands 状态 | 部分通过 | 已补充 `compile_commands` 字段；当前未生成 `compile_commands.json`，但 CMake 已开启导出。 |
| 4 | 模块层级说明 | 通过 | 已新增 `module_hierarchy`，区分核心框架、插件、应用、工具、非架构资产。 |
| 5 | training/demos/documentation 边界 | 通过 | 已加入 `analysis_boundaries.secondary_reference_roots` 和 `recommended_exclude_paths_for_architecture`。 |
| 6 | `src` 遗留根问题 | 通过 | 已移除顶层 `src` extract root 和 5 条 `src/*` 旧记录；`source_root/src` 不再作为 Phase 2 输入。 |
| 7 | 人工检查意见回应 | 通过 | 已在 `phase1-boundary-supplement.md` 建立人工检查意见到处理动作的映射。 |

## 补充字段检查

| 字段 | 状态 | 说明 |
|------|------|------|
| `compile_commands` | 已补充 | 记录不存在、CMake 支持导出、证据位置和建议。 |
| `codegraph` | 已补充 | 记录 `.codegraph` 路径和 CodeGraph 查询证据。 |
| `analysis_boundaries.primary_code_roots` | 已补充 | 定义 Phase 2-7 默认源码主线。 |
| `analysis_boundaries.secondary_reference_roots` | 已补充 | 定义 demos、documentation、training、resources 的默认用途。 |
| `analysis_boundaries.stale_or_missing_roots` | 已清空 | 顶层 `src` 遗留根已处理；处理记录保留在 `resolved_issues`。 |
| `module_hierarchy` | 已补充 | 提供系统级分层和非架构资产分组。 |
| `known_issues` | 已更新 | `src` 遗留已移至 `resolved_issues`；保留 training 边界风险和 compile_commands 缺失。 |

## 后续问题处理状态

| # | 问题 | 严重度 | 建议 |
|---|------|--------|------|
| 1 | `file-classification.jsonl` 曾含 5 条 `src/*` 旧记录 | 中 | 已处理：删除旧记录，`total_file_count=43586`，`extract_roots=["afsim-2_9"]`。 |
| 2 | `training` 中有 152 个 source/header 文件 | 中 | 已处理为后续阶段约束：默认从 Phase 2-7 架构分析中排除；如需培训样例分析，单独设定 `analysis_scope=training`。 |
| 3 | 缺少实际 `compile_commands.json` | 低 | 仍待外部 CMake configure；生成后再运行 Phase 3/4，可提升 AST、宏和 include path 准确性。 |

## 结论

Phase 1 补充项可交付。`src` 遗留根已解决；后续 Phase 2 应以 `analysis_boundaries.primary_code_roots` 和 `module_hierarchy` 为边界，不再直接沿用旧的 107 个同层模块作为架构模块清单。`training` 默认作为边界外参考资产，`compile_commands.json` 仍是可选但推荐的后续构建配置项。
