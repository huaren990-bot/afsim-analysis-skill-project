---
name: cpp-proj-modules-verify
description: Phase 2 验证: 检查 file-index.jsonl、symbol-index.jsonl、module-overview.md 的覆盖率、模板合规性和交叉一致性。
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
- `architecture/module-overview.md`

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

## 输出

生成验证报告 `verification/phase2-verify-report.md`。

## 质量门槛

1. file-index.jsonl 覆盖率 ≥ 95%。
2. includes 解析率 ≥ 80%。
3. symbol-index.jsonl 无前向声明、无 EXPORT 宏、无重复条目。
4. module-overview.md 覆盖所有模块且包含核心类清单。
5. 检查 4 中核心类未命中率 ≤ 20%。
