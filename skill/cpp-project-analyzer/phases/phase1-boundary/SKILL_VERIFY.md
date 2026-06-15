---
name: cpp-proj-boundary-verify
description: Phase 1 验证: 检查 project-boundary.json 和 file-classification.jsonl 的输出质量、完整性、模板合规性。
metadata:
  phase: 1
  role: verifier
  verifies: cpp-proj-boundary
---

# Phase 1 验证: 边界确认与结构发现

## 目标

验证 Phase 1 分析 Agent (`cpp-proj-boundary`) 的产出质量，确保输出完整、格式正确、分类合理。

## 验证对象

- `project-boundary/project-boundary.json`
- `project-boundary/file-classification.jsonl`

## 验证步骤

### 检查 1: project-boundary.json 结构完整性

逐项检查必填字段：

| # | 字段 | 检查方式 |
|---|------|---------|
| 1 | `schema_version` = "1" | 直接读取 |
| 2 | `source_root` 非空且目录存在 | `ls` 验证 |
| 3 | `extract_roots` 非空数组 | 直接读取 |
| 4 | `exclude_paths` 数组 | 直接读取 |
| 5 | `analysis_depth` 为合法值 | 枚举检查 |
| 6 | `language_standard` 非 "unknown" | 检查是否从 CMakeLists.txt 提取 |
| 7 | `build_system` 非 "unknown" | 检查是否从构建文件推断 |
| 8 | `total_file_count` > 0 且为数字 | 直接读取 |
| 9 | `total_source_count` > 0 且为数字 | 直接读取 |
| 10 | `module_count` 与 `modules` 数组长度一致 | 计数比对 |
| 11 | `modules` 中每个模块含必填字段 | 逐项检查 |
| 12 | `top_level_dirs` 非空数组 | 直接读取 |

### 检查 2: file-classification.jsonl 格式正确性

1. 逐行解析 JSON，记录无法解析的行号和错误信息。
2. 统计总行数，与 `project-boundary.json` 中的 `total_file_count` 比对。

### 检查 3: file-classification.jsonl 字段完整性

随机抽样 5% 的条目（最少 50 条），检查：
1. 每条含全部必填字段。
2. `language` 和 `file_type` 为合法枚举值。
3. `module` 字段与 `project-boundary.json` 中登记的模块名一致。

### 检查 4: file_type 分类合理性

随机抽样 20 条，人工判断分类是否合理：
1. `.cpp/.c/.cxx` 应分类为 `source`。
2. `.hpp/.h/.hh` 应分类为 `header`。
3. `CMakeLists.txt` 应分类为 `build`。
4. 位于 `test/` 目录下的应分类为 `test`。
5. 识别分类错误的条目，记录。

### 检查 5: 排除路径合规性

1. 抽样检查 10 个排除路径下的文件，确认不在 file-classification.jsonl 中。
2. 检查是否误排除了关键目录（如 `src/` 被错误排除）。

### 检查 6: 证据等级合理性

1. 检查 `evidence_level` 字段是否只使用合法值。
2. 检查是否有大量 `unknown` — 如果有（>20%），标记为质量问题。

## 输出

生成验证报告 `verification/phase1-verify-report.md`，包含：

```markdown
# Phase 1 验证报告

> **日期**：
> **验证对象**：project-boundary.json, file-classification.jsonl

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | 结构完整性 | ✅/❌ | ... |
| 2 | 格式正确性 | ✅/❌ | ... |
| 3 | 字段完整性 | ✅/❌ | ... |
| 4 | 分类合理性 | ✅/❌ | ... |
| 5 | 排除合规性 | ✅/❌ | ... |
| 6 | 证据等级 | ✅/❌ | ... |

## 不通过项详情

（逐项说明不通过的原因和建议修复方法）

## 总体评价

- 通过项：N/6
- 不通过项：M/6
- 建议：通过 / 修正后重新验证 / 人工介入
```

## 质量门槛

1. 6 项检查中至少 4 项通过。
2. 检查 2（格式正确性）和检查 3（字段完整性）必须通过。
3. 如有不通过项，明确写出修复指引。
