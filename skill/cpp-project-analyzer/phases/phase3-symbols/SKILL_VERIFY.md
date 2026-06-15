---
name: cpp-proj-symbols-verify
description: Phase 3 验证: 检查 symbol-index.jsonl 精细化质量、macro-index.jsonl 过滤正确性、enum-index.jsonl 枚举值完整性。
metadata:
  phase: 3
  role: verifier
  verifies: cpp-proj-symbols
---

# Phase 3 验证: 符号级细粒度分析

## 目标

验证 Phase 3 分析 Agent (`cpp-proj-symbols`) 的产出质量。

## 验证对象

- `source-index/symbol-index.jsonl`（精细化版）
- `source-index/macro-index.jsonl`
- `source-index/enum-index.jsonl`

## 验证步骤

### 检查 1: symbol-index.jsonl 精细化率

1. 统计 `kind=class/struct` 的条目数 C。
2. 统计其中 `signature` 非 `null` 且 `base_symbols` 数组非空的条目数 C_fine。
3. 精细化率 = C_fine / C，必须 ≥ 0.85。

### 检查 2: symbol-index.jsonl 访问修饰符覆盖率

1. 统计 `kind=method/constructor/destructor` 的条目数 M。
2. 统计其中 `access_modifier` 非 `null` 的条目数 M_acc。
3. 覆盖率 = M_acc / M，必须 ≥ 0.80。

### 检查 3: macro-index.jsonl 过滤正确性

1. 遍历 macro-index.jsonl 所有条目，检查是否存在 `macro_name` 匹配 `*_EXPORT` 或 `*_HPP` 或 `*_H_` 模式。
2. 如有，记录为"过滤不完整"。

### 检查 4: macro-index.jsonl 抽样验证

抽样 10 个宏定义，读取源文件验证：

- **防重复**：按宏所在的 `file_path` 分组，每个文件最多读 1 次。若抽样命中同文件的多个宏，合并到一次读取中验证。
- **已读跳过**：维护 `已读文件集合`，抽样时跳过已读文件，选择下一个未读的。
- **失败不重试**：若读取文件失败，在报告中标注"无法验证"，不重试该文件。

1. `replacement` 文本与实际源码一致。
2. `has_parameters` 判断正确。
3. `macro_type` 分类合理。

### 检查 5: enum-index.jsonl 完整性

1. 从 symbol-index.jsonl 中统计 `kind=enum/enum_class` 的条目数 E。
2. enum-index.jsonl 中条目数应 ≥ E（允许更多，因细粒度扫描可能发现新枚举）。
3. 抽样 5 个枚举，读取源文件验证 `values` 数组完整（无遗漏枚举值）。
   - **防重复**：按枚举所在的 `declaration_path` 分组，每个文件最多读 1 次。
   - 抽样命中已读文件时跳过，选择下一个未读的枚举。
   - 读取失败时标注"无法验证"，不重试。

### 检查 6: Phase 2 → Phase 3 追溯性

1. 读取 Phase 2 的粗版 symbol-index.jsonl，提取所有 `qualified_name`。
2. 在 Phase 3 精细化版 symbol-index.jsonl 中逐一查找。
3. 覆盖率必须 = 100%（所有 Phase 2 条目在 Phase 3 中都有对应条目）。

## 输出

生成验证报告 `verification/phase3-verify-report.md`。

## 质量门槛

1. class/struct 精细化率 ≥ 85%。
2. 访问修饰符覆盖率 ≥ 80%。
3. macro-index.jsonl 无 EXPORT 宏和 include guards。
4. enum-index.jsonl 每个枚举含 values 数组。
5. Phase 2 → Phase 3 追溯覆盖率 = 100%。
6. 三个 JSONL 文件每行可通过 JSON 解析。
