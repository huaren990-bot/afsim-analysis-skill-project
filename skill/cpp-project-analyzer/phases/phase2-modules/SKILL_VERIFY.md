---
name: cpp-proj-modules-verify
description: "Phase 2 验证: 检查 file-index.jsonl、symbol-index.jsonl、module-overview.md 的覆盖率、模板合规性和交叉一致性。"
metadata:
  phase: 2
  role: verifier
  verifies: cpp-proj-modules
---

# Phase 2 验证: 模块级分析

## 目标

验证 Phase 2 分析 Agent (`cpp-proj-modules`) 的产出质量。

## 验证对象

- `source-index/file-index.jsonl`
- `source-index/symbol-index.jsonl`
- `docs/architecture/module-overview.md`

## 验证步骤

### 检查 1: file-index.jsonl 覆盖率

1. 读取 Phase 1 的 `file-classification.jsonl`，获取所有 `source` 和 `header` 类型文件数量 S。
2. 读取 `file-index.jsonl`，统计其中 `file_type` 为 `source`/`header` 的条目数 F。
3. 覆盖率 = F / S，必须 ≥ 0.95 (95%)。
4. 列出未被覆盖的 `source`/`header` 文件清单。

### 检查 2: file-index.jsonl includes 解析率

1. 从 `file-index.jsonl` 中筛选 `file_type` 为 `source`/`header` 的条目。
2. 统计其中 `includes` 数组非空的条目数 I。
3. includes 解析率 = I / F，必须 ≥ 0.80 (80%)。
4. 抽样 10 个 `includes` 为空的条目，检查源码文件是否确实无 `#include`。
   - **防重复**：维护一个 `已读文件集合`，抽样时跳过已读文件。每个文件最多读 1 次。
   - 若抽样命中已读文件，换下一个未读文件。
   - 若读文件失败（如路径不存在），在报告中标注"无法验证"并继续，不重试。

### 检查 3: file-index.jsonl 字段完整性

抽样 5% 的条目（最少 50 条），**仅基于 JSONL 文件本身分析，不读源码**，检查：
1. 每条含全部必填字段。
2. `key_symbols` 非空（至少含 1 个）。
3. `brief` 非空、非 "unknown"。

### 检查 4: symbol-index.jsonl 覆盖率

1. 对每个模块，从 module-overview.md 中提取核心类清单。
2. 在 symbol-index.jsonl 中逐一查找这些核心类，记录未找到的类。

### 检查 5: symbol-index.jsonl 去重与一致性

1. 检查是否存在 `symbol_name` + `path` 完全相同的重复条目。
2. 检查是否包含前向声明条目（`kind=class` 且无 `base_symbols`、`line_start`、`line_end` 且 `brief` 为空）。
3. 检查是否包含 `*_EXPORT` 宏条目（`kind=macro` 且 `symbol_name` 含 `_EXPORT`）。

### 检查 6: module-overview.md 覆盖完整性

1. 检查 module-overview.md 是否覆盖 Phase 1 中所有模块。
2. 检查每个模块是否包含子系统结构、核心类、关键依赖三个子章节。
3. 检查核心类表格是否可追溯到 symbol-index.jsonl。
4. 检查开头是否有中文概览段，且写明系统数、子系统数、模块总数、source/header 文件数。
5. 检查文档是否明确说明“系统/子系统/模块”的区分依据，且与 `project-boundary.json.module_hierarchy` 一致。
6. 检查模块清单表是否包含 Phase 1 所有模块；若正文为摘要表，必须有完整清单链接或附录。
7. 检查每个模块清单行是否包含中文说明和详情跳转锚点。
8. 检查是否至少包含一张 Mermaid 模块关系图；大型项目应按系统/子系统拆图，而不是只给一张过小总图。

### 检查 7: files_to_index 闭环

1. 从 Phase 1 的 `file-classification.jsonl` 中筛选所有 `source` 和 `header` 文件，作为 `files_to_index`。
2. 从 `file-index.jsonl` 中提取所有 `path`。
3. 计算覆盖率，必须 ≥ 95%。
4. 对缺失文件，检查是否在 `notes`、context-handoff 或验证报告中记录明确原因。
5. 若缺失文件没有原因，判定为遗漏。

### 检查 8: symbols_to_refine 可用性

1. 检查 `symbol-index.jsonl` 中每个正式符号是否有 `qualified_name`、`kind`、`path` 或 `declaration_path`。
2. 检查是否包含头文件 inline 函数、自由函数、匿名 namespace/static 函数候选的记录或跳过说明。
3. 若大量符号缺少路径（>5%），判定为 Phase 3 不可可靠精细化。

## 输出

生成验证报告 `docs/verification/phase2-verify-report.md`。

## 质量门槛

1. file-index.jsonl 覆盖率 ≥ 95%。
2. includes 解析率 ≥ 80%。
3. symbol-index.jsonl 无前向声明、无 EXPORT 宏、无重复条目。
4. module-overview.md 覆盖所有模块且包含核心类清单。
5. 检查 4 中核心类未命中率 ≤ 20%。
6. files_to_index 覆盖率 ≥ 95%，未覆盖项均有原因。
7. symbols_to_refine 条目具备可追溯路径，缺路径率 ≤ 5%。
8. module-overview.md 必须有概览说明、层级定义、完整模块清单入口、详情跳转和模块关系图。
