# Phase 1 验证报告

> **日期**：2026-06-15
> **验证对象**：project-boundary.json, file-classification.jsonl

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | 结构完整性 | ✅ PASS | 12 项必填字段全部通过验证 |
| 2 | 格式正确性 | ✅ PASS | 43591 行全部 JSON 解析成功，行数与 total_file_count 一致 |
| 3 | 字段完整性 | ❌ FAIL | 枚举值不规范：language 使用小写（cpp/text/json/cmake），file_type 含非标准值（doc/generated） |
| 4 | 分类合理性 | ✅ PASS | 抽样 20 条，.cpp→source、.hpp→header、CMakeLists.txt→build 均正确 |
| 5 | 排除合规性 | ✅ PASS | .git/build/3rd_party/node_modules 下无文件泄漏到 JSONL |
| 6 | 证据等级 | ✅ PASS | 全部 43591 条均为 source-cited，unknown 比例 0%，合法值 100% |

## 不通过项详情

### 检查 3: 字段完整性 — 枚举值不规范

**问题描述**：所有 11 个必填字段在抽样 2179 条记录中均完整存在，module 字段与 project-boundary.json 中的模块名完全一致。但 `language` 和 `file_type` 的枚举值使用了与 SKILL_VERIFY.md 定义不同的命名约定。

#### language 字段实际分布（全量 43591 条）

| 实际值 | 数量 | 对应标准值 | 状态 |
|--------|------|-----------|------|
| `cpp` | 17,358 | `C++` | ⚠️ 大小写不一致 |
| `text` | 14,871 | `Text` | ⚠️ 大小写不一致 |
| `unknown` | 6,511 | `Unknown` / `unknown` | ✅ 可接受 |
| `json` | 3,719 | `JSON` | ⚠️ 大小写不一致 |
| `cmake` | 643 | `CMake` | ⚠️ 大小写不一致 |
| `xml` | 335 | `XML` | ⚠️ 大小写不一致 |
| `python` | 80 | `Python` | ⚠️ 大小写不一致 |
| `shell` | 74 | `Shell` | ⚠️ 大小写不一致 |

**影响**：不影响数据语义正确性，但与验证规范定义的枚举值大小写不一致。下游消费者若做精确匹配会失败。

#### file_type 字段实际分布（全量 43591 条）

| 实际值 | 数量 | 是否在标准枚举中 | 状态 |
|--------|------|-----------------|------|
| `doc` | 14,556 | ❌ 不在 {documentation} | ⚠️ 应为 `documentation` |
| `header` | 13,055 | ✅ | OK |
| `unknown` | 7,087 | ✅ | OK |
| `source` | 4,287 | ✅ | OK |
| `config` | 3,710 | ✅ | OK |
| `build` | 639 | ✅ | OK |
| `test` | 255 | ✅ | OK |
| `generated` | 2 | ❌ 不在标准枚举中 | ⚠️ 新增类型 |

**影响**：
- `doc` (14,556 条) 应统一为 `documentation`，否则按标准枚举匹配会丢失约 33% 的文件分类
- `generated` (2 条) 是合理的新增类型，建议纳入标准枚举

#### 修复建议

1. **方案 A（推荐）**：修改 file-classification.jsonl 生成逻辑，将 language 值统一为标准大小写格式（`C++`, `Text`, `JSON`, `CMake`, `XML`, `Python`, `Shell`），将 `doc` 替换为 `documentation`
2. **方案 B**：更新 SKILL_VERIFY.md 中的合法枚举定义，接纳小写值和 `doc`/`generated` 作为合法值
3. **注意**：无论选择哪种方案，需确保下游 Phase 2+ 的消费者使用一致的枚举约定

## 各检查项详细数据

### 检查 1: 结构完整性

| 子项 | 字段 | 值 | 状态 |
|------|------|----|------|
| 1 | schema_version | `"1"` | ✅ |
| 2 | source_root | `/Users/hjt/.../source_root` (目录存在) | ✅ |
| 3 | extract_roots | `["afsim-2_9", "src"]` | ✅ |
| 4 | exclude_paths | `[".git", "build", "3rd_party", "node_modules"]` | ✅ |
| 5 | analysis_depth | `"full"` | ✅ |
| 6 | language_standard | `"C++14"` | ✅ |
| 7 | build_system | `"CMake"` | ✅ |
| 8 | total_file_count | `43591` | ✅ |
| 9 | total_source_count | `17342` | ✅ |
| 10 | module_count vs modules | `107 == len(modules)=107` | ✅ |
| 11 | modules 必填字段 | 全部 107 个模块均含 name/path/file_count/source_count/has_cmake/is_plugin/brief | ✅ |
| 12 | top_level_dirs | 2 项，均含 name/path/file_count/brief | ✅ |

### 检查 2: 格式正确性

- 总行数：43,591
- JSON 解析成功：43,591 (100%)
- 解析失败：0
- 与 total_file_count (43,591) 比对：**一致** ✅

### 检查 3: 字段完整性

- 抽样数量：2,179 条（5%）
- 必填字段缺失：**0** ✅
- module 字段一致性：**100%** ✅
- language 枚举合规：**不合规**（见上方详情）❌
- file_type 枚举合规：**不合规**（见上方详情）❌

### 检查 4: 分类合理性

- .cpp/.c/.cxx → source：5/5 正确 ✅
- .hpp/.h/.hh → header：5/5 正确 ✅
- CMakeLists.txt → build：5/5 正确 ✅
- test/ 目录文件：5/5 合理 ✅
- 候选池统计：source 扩展名 4,303 条、header 扩展名 13,045 条、CMakeLists.txt 341 条、test 目录 598 条

### 检查 5: 排除路径合规性

| 排除路径 | 泄漏文件数 | 状态 |
|----------|-----------|------|
| `.git` | 0 | ✅ |
| `build` | 0 | ✅ |
| `3rd_party` | 0 | ✅ |
| `node_modules` | 0 | ✅ |

关键目录检查：`src/`、`source/`、`lib/` 均有文件存在于 JSONL 中，未被误排除 ✅

### 检查 6: 证据等级合理性

| evidence_level | 数量 | 占比 |
|---------------|------|------|
| source-cited | 43,591 | 100.0% |
| document-cited | 0 | 0.0% |
| index-derived | 0 | 0.0% |
| inferred | 0 | 0.0% |
| unknown | 0 | 0.0% |

- 非法值：0 ✅
- unknown 比例：0.0% < 20% ✅

## 总体评价

- **通过项**：5/6
- **不通过项**：1/6（检查 3: 枚举值命名约定不一致）
- **质量门槛判定**：检查 2（格式正确性）✅ 通过；检查 3（字段完整性）❌ 未完全通过（字段齐全但枚举值不规范）

### 建议：修正后重新验证

**核心问题**：数据本身质量良好（字段完整、分类正确、无排除泄漏、证据充分），唯一问题是枚举值的命名约定与验证规范不一致。这属于 **规范化问题** 而非 **数据质量问题**。

**推荐操作**：
1. 确认项目采用的枚举约定（全小写 or 混合大小写），并统一写入 Schema 文档
2. 若采用标准枚举：对 file-classification.jsonl 做批量替换（`cpp→C++`, `doc→documentation` 等）
3. 若采用小写约定：更新 SKILL_VERIFY.md 的合法枚举列表
4. 将 `generated` 加入 file_type 合法枚举（仅 2 条，但语义合理）
5. 修正后重跑本验证脚本确认通过
