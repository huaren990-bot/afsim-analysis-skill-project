# Phase 1 后续问题处理验证报告

> **日期**：2026-06-24
> **验证对象**：`workspace/project-boundary/project-boundary.json`、`workspace/project-boundary/file-classification.jsonl`、`workspace/project-boundary/_scan-result.json`、`workspace/project-boundary/_classify-src*`
> **依据**：`docs/verification/phase1-supplement-verify-report.md` 的“后续问题处理状态”

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | 顶层 `src` 遗留根清理 | 通过 | `extract_roots=["afsim-2_9"]`，`top_level_dirs` 仅保留 `afsim-2_9`。 |
| 2 | `file-classification.jsonl` 清理 | 通过 | 总行数 43,586；顶层 `src/*` 记录 0 条；JSON 解析错误 0 条。 |
| 3 | 计数一致性 | 通过 | `project-boundary.total_file_count=43586`，与 JSONL 行数一致；`total_source_count=17342`，与 source/header 行数一致。 |
| 4 | 中间产物一致性 | 通过 | `_scan-result.json` 不再包含顶层 `src`；`_classify-src.jsonl` 已清空，summary 标记为 `removed_stale_extract_root`。 |
| 5 | training 边界约束 | 通过 | `training` 中 152 个 source/header 文件保留为边界外参考资产，默认排除于 Phase 2-7 架构分析。 |
| 6 | compile_commands 状态 | 部分通过 | 当前仍未发现 `compile_commands.json`；CMake 已开启导出，需要外部 configure 后生成。 |

## 已处理项

| 问题 | 处理动作 | 当前状态 |
|------|----------|----------|
| `file-classification.jsonl` 含 5 条顶层 `src/*` 旧记录 | 已删除 5 条旧记录，并同步更新总文件数。 | 已解决 |
| `project-boundary.json.extract_roots` 含不存在的 `src` | 已移除 `src`，当前仅保留 `afsim-2_9`。 | 已解决 |
| `analysis_boundaries.stale_or_missing_roots` 仍记录 `src` | 已清空，并把处理详情写入 `resolved_issues.phase1-stale-src-root`。 | 已解决 |
| `_classify-src*` 中间产物可能误导后续阶段 | 已清空 JSONL，并把 summary 标记为已移除的陈旧根。 | 已解决 |
| `training` 源码可能污染架构依赖 | 已保持在 `recommended_exclude_paths_for_architecture`，并记录 `source_header_count=152`。 | 已处理为后续阶段约束 |

## 仍待处理项

| 问题 | 严重度 | 处理建议 |
|------|--------|----------|
| 未生成 `compile_commands.json` | 低 | 在选定 build 目录执行 CMake configure，生成后再重跑 AST/宏/include path 依赖较高的 Phase 3/4。 |

## 结论

Phase 1 后续问题已处理到可供 Phase 2 消费的状态。后续阶段应以 `analysis_boundaries.primary_code_roots`、`module_hierarchy` 和 `recommended_exclude_paths_for_architecture` 为准，不再使用顶层 `src` 作为源码根，也不得把 `training` 纳入默认架构依赖分析。
