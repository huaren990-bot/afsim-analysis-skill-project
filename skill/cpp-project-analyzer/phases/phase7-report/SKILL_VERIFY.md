---
name: cpp-proj-final-verify
description: Phase 7 验证: 全量交叉一致性检查 — 验证三份最终报告与全部索引文件之间的一致性，产出最终验证报告。
metadata:
  phase: 7
  role: verifier
  verifies: cpp-proj-report
---

# Phase 7 验证: 综合报告全量交叉一致性检查

## 目标

对 Phase 7 生成的三份最终报告进行**全量交叉一致性验证**，确保：
- 报告中的每一条断言可追溯到索引文件
- 各报告之间用词一致
- 模板合规

## 验证对象

- `architecture/afsim-architecture.md`
- `architecture/x-level-capabilities.md`
- `architecture/module-dependency.md`
- 以及 Phase 1-6 的全部索引文件（用于交叉验证）

## 验证步骤

### 检查 1: afsim-architecture.md 章节完整性

逐章检查 afsim-architecture.md 是否包含模板要求的全部章节：

| # | 章节 | 检查方式 |
|---|------|---------|
| 0 | 文档说明 | 含总体概述、业务价值、编程语言 |
| 1 | 目录结构总览 | 含目录树 + 中文说明 |
| 2 | 模块总览 | 含模块表 + Mermaid 图 |
| 3 | 仿真生命周期 | 含 Mermaid 图 + 关联表 |
| 4 | 数据流 | 含 Mermaid 图 |
| 5 | 配置流 | 含 Mermaid 图 |
| 6 | 扩展点 | 含扩展机制表 |
| 7 | 关键符号 | 含符号表 |
| 8 | 未知项 | 含未知问题清单 |
| 9 | 源码证据 | 含证据统计表 |

### 检查 2: x-level-capabilities.md 结构合规性

1. 标题必须为 `# AFSIM 仿真框架架构文档`。
2. 表格列与模板 `template_x-level-capabilities.md` 完全一致。
3. 包含四层级：System-level → Module-level → Class-level → Method-level。
4. 每个功能层级包含"功能对应条目"段落。
5. 方法级功能表格中不使用抽象群组名。

### 检查 3: x-level-capabilities.md ↔ function-index.jsonl 交叉验证

1. 提取 x-level-capabilities.md 中所有 Method-level 的 `qualified_name`。
2. 在 function-index.jsonl 中逐一查找，统计未命中数。
3. 未命中率必须 ≤ 5%。

### 检查 4: module-dependency.md ↔ dependency-index.jsonl 交叉验证

1. 提取 module-dependency.md 中 Mermaid 图的所有边。
2. 在 dependency-index.jsonl 中逐一查找对应条目。
3. 边追溯率必须 ≥ 80%。

### 检查 5: 三份报告用词一致性

1. 提取三份报告中的所有模块名，检查是否统一。
2. 提取三份报告中的所有符号名，检查是否统一。
3. 检查是否有同一概念在不同报告中用不同中文词描述的情况。

### 检查 6: 英文标识中文翻译覆盖率

1. 扫描三份 .md 文件，提取所有英文标识（类名、函数名、模块名）。
2. 检查每个英文标识首次出现时是否有中文翻译说明。
3. 覆盖率应 ≥ 90%。

### 检查 7: 省略号违规检查

1. 搜索三份 .md 文件中的 `...`（省略号）和 `等`（中文省略）。
2. 如果省略号背后应展开的内容超过 30 项，检查是否已新建独立文件完整列出。

### 检查 8: 全量索引文件 JSON 解析

1. 对所有 JSONL 索引文件执行逐行 JSON 解析。
2. 任何新增的解析错误都必须在最终报告中记录。

## 输出

生成 `verification/phase7-final-verify-report.md`，包含：

```markdown
# Phase 7 最终验证报告

> **日期**：
> **验证范围**：Phase 1-7 全部产出

## 各阶段验证通过情况汇总

| 阶段 | 分析产出 | 验证结果 | 未解决问题数 |
|------|---------|---------|-------------|
| Phase 1 | ... | ✅/❌ | N |
| Phase 2 | ... | ✅/❌ | N |
| Phase 3 | ... | ✅/❌ | N |
| Phase 4 | ... | ✅/❌ | N |
| Phase 5 | ... | ✅/❌ | N |
| Phase 6 | ... | ✅/❌ | N |
| Phase 7 | ... | ✅/❌ | N |

## 交叉一致性检查

| 检查项 | 结果 | 详情 |
|--------|------|------|
| afsim-architecture.md 章节完整性 | ✅/❌ | ... |
| x-level-capabilities.md 结构合规 | ✅/❌ | ... |
| x-level-capabilities ↔ function-index 交叉验证 | 命中率: X% | ... |
| module-dependency ↔ dependency-index 交叉验证 | 追溯率: X% | ... |
| 三份报告用词一致性 | ✅/❌ | ... |
| 英文标识中文翻译覆盖率 | X% | ... |
| 省略号违规检查 | ✅/❌ | ... |
| 全量JSON解析 | ✅/❌ | ... |

## Known Issues（仍未解决的问题）

| # | 来源 | 问题描述 | 严重度 | 建议 |
|---|------|---------|--------|------|
| 1 | Phase N | ... | 高/中/低 | ... |

## 总体质量评分

- 总分：X/10
- 建议：可交付 / 需修复后交付 / 需人工介入
```

## 质量门槛

1. 8 项交叉一致性检查中至少 7 项通过。
2. x-level-capabilities ↔ function-index 未命中率 ≤ 5%。
3. module-dependency ↔ dependency-index 边追溯率 ≥ 80%。
4. 英文标识中文翻译覆盖率 ≥ 90%。
5. 全部 JSONL 文件可逐行解析。
