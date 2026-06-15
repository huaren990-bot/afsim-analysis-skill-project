---
name: cpp-proj-dependencies-verify
description: Phase 5 验证: 检查 dependency-index.jsonl 的覆盖率（≥200条）、relation 种类（≥6种）、dependency-graph.md 的可追溯性。
metadata:
  phase: 5
  role: verifier
  verifies: cpp-proj-dependencies
---

# Phase 5 验证: 跨模块依赖关系分析

## 目标

验证 Phase 5 分析 Agent (`cpp-proj-dependencies`) 的产出质量。

## 验证对象

- `source-index/dependency-index.jsonl`
- `architecture/dependency-graph.md`

## 验证步骤

### 检查 1: 条目数量达标

1. 统计 dependency-index.jsonl 总条目数 D。
2. D ≥ 200：✅ 通过。
3. 100 ≤ D < 200：⚠️ 部分通过，标记为"条目偏少"。
4. D < 100：❌ 不通过。

### 检查 2: relation 种类覆盖

1. 统计 dependency-index.jsonl 中各 relation 值的分布。
2. 必须覆盖：`build`、`inheritance`、`composition`、`include`、`call`、`registration`（6 种缺一不可）。
3. 每种 relation 的条目数 ≥ 5。

### 检查 3: strength 字段覆盖率

1. 统计 `strength` 字段为 `null` 或缺失的条目数。
2. 缺失率必须 ≤ 5%。

### 检查 4: 跨模块覆盖均衡性

1. 统计各模块在 dependency 中作为 `source` 或 `target` 出现的次数。
2. 是否存在某个模块完全没有依赖记录？如有，标记为"模块遗漏"。

### 检查 5: dependency-graph.md Mermaid 可追溯性

1. 提取 dependency-graph.md 中 Mermaid 图的所有边（A --> B 或 A -->|label| B）。
2. 随机抽样 10 条边，在 dependency-index.jsonl 中查找对应的条目。
3. 追溯率必须 ≥ 0.80（10 条中至少 8 条可追溯）。

### 检查 6: 格式正确性

1. 逐行解析 JSON，记录无法解析的行号。
2. 解析成功率必须 = 100%。

### 检查 7: evidence 字段质量

1. 随机抽样 20 条，检查 `evidence` 字段是否具体（不是空字符串或 "unknown"）。
2. 具体率必须 ≥ 0.80（20 条中至少 16 条有具体 evidence）。

### 检查 8: inheritance 与 symbol-index 交叉验证

1. 从 dependency-index.jsonl 中提取所有 `relation=inheritance` 的条目。
2. 在 symbol-index.jsonl 中验证：子类的 `base_symbols` 应包含基类。
3. 不一致的条目记录为"交叉验证失败"。

## 输出

生成验证报告 `verification/phase5-verify-report.md`。

## 质量门槛

1. 总条目数 ≥ 200。
2. 覆盖 6 种 relation，每种 ≥ 5 条。
3. strength 缺失率 ≤ 5%。
4. JSON 解析成功率 = 100%。
5. dependency-graph.md 边追溯率 ≥ 80%。
6. inheritance 交叉验证不一致率 ≤ 10%。
