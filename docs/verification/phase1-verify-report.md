# Phase 1 验证报告

> **日期**：2026-06-16
> **验证对象**：project-boundary.json, file-classification.jsonl, directory-tree.md
> **后续更新**：2026-06-24 已处理顶层 `src` 遗留根问题，当前可消费状态见 `docs/verification/phase1-followup-fix-report.md`。

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 0 | 目录树完整性 | ✅ PASS | 91 KB 非空；覆盖 afsim-2_9/ 和 src/ 两个 extract_roots；深度 ≤ 4 层；约 2379 行 |
| 1 | 结构完整性 | ✅ PASS | 12 项必填字段全部通过验证 |
| 2 | 格式正确性 | ✅ PASS | 43591 行全部 JSON 解析成功，行数与 total_file_count 一致 |
| 3 | 字段完整性 | ✅ PASS | 全量 43591 条无必填字段缺失；language/file_type/evidence_level 枚举值 100% 合法；module 与 project-boundary.json 模块名一致 |
| 4 | 分类合理性 | ✅ PASS | 全量验证：source 扩展名文件全部为 source(0 误分)；header 扩展名文件全部为 header(0 误分) |
| 5 | 排除合规性 | ✅ PASS | .git/build/3rd_party/node_modules 下无文件泄漏到 JSONL |
| 6 | 证据等级 | ✅ PASS | 全部 43591 条均为 source-cited，unknown 比例 0%，合法值 100% |

## 各检查项详细数据

### 检查 0: 目录树完整性

- 文件大小：90,679 字节（非空）✅
- 覆盖 extract_roots：
  - `afsim-2_9/`：2,376 行（144 个顶级子目录）✅
  - `src/`：3 行 ✅
- 深度：≤ 4 ✅
- 格式：使用 `├──`、`└──`、`│` 树形字符 ✅
- 统计摘要：`afsim-2_9` 43,633 文件，`src` 5 文件 ✅

### 检查 1: 结构完整性

| # | 字段 | 值 | 状态 |
|---|------|----|------|
| 1 | schema_version | `"1"` | ✅ |
| 2 | source_root | `/Users/hjt/afsim/afsim-analysis-skill-project/source_root` (目录存在) | ✅ |
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
- schema_version 异常：**0** ✅
- module 字段一致性：**100%** ✅

#### language 枚举值分布（抽样）

| 值 | 抽样数量 | 模板合法性 |
|----|---------|-----------|
| `cpp` | 864 | ✅ |
| `text` | 755 | ✅ |
| `unknown` | 303 | ✅ |
| `json` | 198 | ✅ |
| `cmake` | 39 | ✅ |
| `xml` | 15 | ✅ |
| `python` | 3 | ✅ |
| `shell` | 2 | ✅ |
| 非法值 | 0 | — |

#### file_type 枚举值分布（抽样）

| 值 | 抽样数量 | 模板合法性 |
|----|---------|-----------|
| `doc` | 741 | ✅ |
| `header` | 669 | ✅ |
| `unknown` | 326 | ✅ |
| `config` | 199 | ✅ |
| `source` | 194 | ✅ |
| `build` | 39 | ✅ |
| `test` | 11 | ✅ |
| 非法值 | 0 | — |

> **注**：枚举值依据 `template_file-classification.md` 模板（全小写），非上一版报告引用的混合大小写约定。实际数据与模板定义完全一致。

#### 全量验证结果

- 必填字段缺失（全量 43,591 条）：**0**
- 非法 language 值：**0**
- 非法 file_type 值：**0**
- 非法 evidence_level 值：**0**
- module 不匹配：**0**

### 检查 4: 分类合理性

#### 全量扩展名一致性

| 扩展名类型 | 文件数 | 误分类数 | 状态 |
|-----------|--------|---------|------|
| source (.cpp/.cc/.cxx/.c) | 4,287 | 0 | ✅ |
| header (.hpp/.hh/.h/.hxx) | 13,055 | 0 | ✅ |
| CMakeLists.txt | 341 | — | ✅ |

#### 抽样检查

抽样 50 条人工交叉验证：
- .cpp/.cxx 文件 → source：正确 ✅
- .hpp/.h/.hxx 文件 → header：正确 ✅
- CMakeLists.txt → build：正确 ✅
- .txt 配置类 → config：正确 ✅
- .json 配置文件 → config：正确 ✅
- test/ 目录文件 → test：正确 ✅

### 检查 5: 排除路径合规性

| 排除路径 | 泄漏文件数 | 状态 |
|----------|-----------|------|
| `.git` | 0 | ✅ |
| `build` | 0 | ✅ |
| `3rd_party` | 0 | ✅ |
| `node_modules` | 0 | ✅ |

关键目录覆盖检查：
- `source/` 目录：17,569 条记录 ✅
- `src/` 目录：28,344 条记录 ✅
- `lib/` 目录：1,120 条记录 ✅
- `test/` 目录：498 条记录 ✅
- `wsf_` 前缀目录：15,705 条记录 ✅

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

## 与上一版报告（2026-06-15）的差异说明

上一版报告将检查 3 判为 FAIL，原因是 `language`/`file_type` 枚举值使用小写形式（如 `cpp`、`doc`），与当时引用的标准枚举列表（如 `C++`、`documentation`）不一致。

**但 `template_file-classification.md` 定义的有效枚举值本身就是全小写形式：**

- `language`: `cpp` | `c` | `cmake` | `xml` | `json` | `yaml` | `python` | `shell` | `text` | `unknown`
- `file_type`: `source` | `header` | `build` | `config` | `test` | `example` | `doc` | `generated` | `unknown`

实际输出值完全符合模板规范 —— 上一版报告的枚举问题是 **false positive**。本周重新验证已纠正此判断。

## 总体评价

- **通过项**：7/7
- **不通过项**：0/7
- **质量门槛判定**：检查 2（格式正确性）✅ 通过；检查 3（字段完整性）✅ 通过

### 建议：通过

Phase 1 输出质量良好，所有 6 项检查均通过，无需修正，可进入 Phase 2。
