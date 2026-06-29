---
name: cpp-proj-final-verify
description: Phase 7 验证: 全量交叉一致性检查 — 验证四份最终产物与全部索引文件之间的一致性，产出最终验证报告。
metadata:
  phase: 7
  role: verifier
  verifies: cpp-proj-report
---

# Phase 7 验证: 综合报告全量交叉一致性检查

## 目标

对 Phase 7 生成的四份最终产物进行**全量交叉一致性验证**，确保：
- 报告中的每一条断言可追溯到索引文件
- 各报告之间用词一致
- 模板合规
- `business-logic-readiness.md` 能直接支撑下一步 AFSIM 业务逻辑分析

## 验证对象

- `docs/architecture/afsim-architecture.md`
- `docs/architecture/x-level-capabilities.md`
- `docs/architecture/module-dependency.md`
- `docs/architecture/business-logic-readiness.md`
- 以及 Phase 1-6 的全部索引文件（用于交叉验证）

## 验证步骤

### 检查 1: afsim-architecture.md 章节完整性

逐章检查 afsim-architecture.md 是否包含模板要求的全部章节：

| # | 章节 | 检查方式 |
|---|------|---------|
| 0 | 文档说明 | 含总体概述、业务价值、编程语言 |
| 1 | 目录结构总览 | 含目录树 + 中文说明 |
| 2 | 模块总览 | 含模块表 + Mermaid 图 + 详情跳转 |
| 3 | 仿真生命周期 | 含 Mermaid 图 + 关联表 |
| 4 | 数据流 | 含 Mermaid 图 |
| 5 | 配置流 | 含 Mermaid 图 |
| 6 | 扩展点 | 含扩展机制表 + 作用说明 |
| 7 | 关键符号 | 含总体性陈述 + 代表性符号表 + 完整清单入口 |
| 8 | 未知项 | 含未知问题清单 + 建议人工确认问题 |
| 9 | 源码证据 | 含证据统计表 |
| 10 | 下一步业务逻辑分析入口 | 含业务逻辑承接文档摘要和下一步分析入口 |

附加检查：
1. 必须包含总框架 Mermaid 图。
2. 目录结构不得使用省略号；若有摘要，必须有完整目录链接。
3. 数据流章节必须包含关键数据对象与 Mermaid 节点映射表。
4. 配置流章节必须说明配置流用途和运行时影响。
5. 下一步业务逻辑分析入口必须指向 `business-logic-readiness.md`，并摘要列出业务域候选、流程入口和规则候选。

### 检查 2: x-level-capabilities.md 结构合规性

1. 标题必须为 `# AFSIM 仿真框架架构文档`。
2. 表格列与模板 `template_x-level-capabilities.md` 完全一致。
3. 包含 System-level → Module-level → Class-level 三层详述，并对 Method-level 提供代表性样例或完整索引链接。
4. 每个功能层级包含"功能对应条目"段落。
5. 方法级功能表格中不使用抽象群组名。
6. 检查是否只纳入仿真模型相关功能；若包含 training/demo/test/doc 工具功能，必须说明用户显式纳入，否则判定为范围污染。
7. 检查是否有“功能总览”章节，概述功能数量和主要能力域。

### 检查 3: x-level-capabilities.md ↔ function-index.jsonl 交叉验证

1. 提取 x-level-capabilities.md 中所有 Method-level 的 `qualified_name`。
2. 在 function-index.jsonl 中逐一查找，统计未命中数。
3. 未命中率必须 ≤ 5%。

### 检查 4: module-dependency.md ↔ dependency-index.jsonl 交叉验证

1. 提取 module-dependency.md 中 Mermaid 图的所有边。
2. 在 dependency-index.jsonl 中逐一查找对应条目。
3. 边追溯率必须 ≥ 80%。
4. 检查 Mermaid 语法可渲染，节点 ID 安全，中文/路径位于 label 中。
5. 检查子系统名称是否与 afsim-architecture.md、module-overview.md 一致。
6. 检查所有子系统均有依赖说明；无依赖或未展示时必须说明原因。
7. 检查核心依赖是否包含 Phase 1 排除路径（如 training/demo），若有且无用户授权则判定为范围污染。
8. 检查 `strong`/`medium`/`weak` 是否解释清楚，并与依赖强度章节一致。
9. 检查关键全局常量表列顺序是否为“常量、值、说明、定义位置、完整清单/选择理由”，且说明不是重复常量名。

### 检查 5: 四份最终产物用词一致性

1. 提取四份最终产物中的所有模块名，检查是否统一。
2. 提取四份最终产物中的所有符号名，检查是否统一。
3. 检查是否有同一概念在不同报告中用不同中文词描述的情况。

### 检查 6: 英文标识中文翻译覆盖率

1. 扫描四份 .md 文件，提取所有英文标识（类名、函数名、模块名）。
2. 检查每个英文标识首次出现时是否有中文翻译说明。
3. 覆盖率应 ≥ 90%。

### 检查 7: 省略号违规检查

1. 搜索四份 .md 文件中的 `...`（省略号）和 `等`（中文省略）。
2. 如果省略号背后应展开的内容超过 30 项，检查是否已新建独立文件完整列出。

### 检查 7.5: 可处理未知项检查

1. 扫描四份最终产物中的 unknown/inferred/待确认项。
2. 每项必须包含问题描述、影响、当前证据、建议人工确认的问题、建议确认对象/文件。
3. 只有“未知”或“无法确定”而没有下一步确认问题的条目判定为不可处理。

### 检查 8: business-logic-readiness.md 承接可用性

1. 检查是否包含以下章节：业务域候选总览、端到端业务流程入口、业务规则/决策点候选、数据与配置映射、扩展点与业务能力接入、下一步分析优先级、未知项和人工确认问题。
2. 检查每条业务域、流程或规则候选是否至少关联一类证据：`module-overview.md`、`function-index.jsonl`、`dependency-index.jsonl`、`lifecycle.md`、`dataflow.md`、`extension-points.md` 或具体源文件位置。
3. 检查每条候选是否标注 `evidence_level`，且值为 `direct`、`cross_checked`、`inferred` 或 `unknown`。
4. 检查端到端流程是否覆盖“触发入口 → 配置/事件输入 → 关键处理链 → 状态对象 → 输出/副作用”。
5. 检查业务规则/决策点是否明确条件、所在函数/类、影响对象/输出和待确认问题。
6. 对没有证据却写成确定业务结论的条目判定为失败；允许写为“候选”或“待确认”。

### 检查 9: 全量索引文件 JSON 解析

1. 对所有 JSONL 索引文件执行逐行 JSON 解析。
2. 任何新增的解析错误都必须在最终报告中记录。

## 输出

生成 `docs/verification/phase7-final-verify-report.md`，包含：

```markdown
# Phase 7 最终验证报告

> **日期**：
> **验证范围**：Phase 1-7 全部产出

## 各阶段验证通过情况汇总

| 阶段 | 分析产出 | 验证结果 | 未解决问题数 |
|------|---------|---------|-------------|
| Phase 1 | <产物清单> | ✅/❌ | N |
| Phase 2 | <产物清单> | ✅/❌ | N |
| Phase 3 | <产物清单> | ✅/❌ | N |
| Phase 4 | <产物清单> | ✅/❌ | N |
| Phase 5 | <产物清单> | ✅/❌ | N |
| Phase 6 | <产物清单> | ✅/❌ | N |
| Phase 7 | <产物清单> | ✅/❌ | N |

## 交叉一致性检查

| 检查项 | 结果 | 详情 |
|--------|------|------|
| afsim-architecture.md 章节完整性 | ✅/❌ | <具体缺失或通过证据> |
| x-level-capabilities.md 结构合规 | ✅/❌ | <具体缺失或通过证据> |
| x-level-capabilities ↔ function-index 交叉验证 | 命中率: X% | <未命中清单位置> |
| module-dependency ↔ dependency-index 交叉验证 | 追溯率: X% | <未追溯边清单位置> |
| 四份最终产物用词一致性 | ✅/❌ | <冲突术语清单> |
| 英文标识中文翻译覆盖率 | X% | <缺少说明的标识清单> |
| 省略号违规检查 | ✅/❌ | <违规位置或通过证据> |
| 可处理未知项检查 | ✅/❌ | <不可处理未知项清单> |
| business-logic-readiness.md 承接可用性 | ✅/❌ | <缺失章节、无证据候选或不可执行下一步清单> |
| 全量JSON解析 | ✅/❌ | <解析错误行或通过证据> |

## Known Issues（仍未解决的问题）

| # | 来源 | 问题描述 | 严重度 | 建议 |
|---|------|---------|--------|------|
| 1 | Phase N | <问题描述> | 高/中/低 | <可执行建议> |

## 总体质量评分

- 总分：X/10
- 建议：可交付 / 需修复后交付 / 需人工介入
```

## 质量门槛

1. 9 项交叉一致性检查中至少 8 项通过。
2. x-level-capabilities ↔ function-index 未命中率 ≤ 5%。
3. module-dependency ↔ dependency-index 边追溯率 ≥ 80%。
4. 英文标识中文翻译覆盖率 ≥ 90%。
5. 全部 JSONL 文件可逐行解析。
6. 无边界外核心结论污染；未知项均可人工继续处理。
7. business-logic-readiness.md 承接可用性必须通过，否则 Phase 7 不可标记为可支撑下一步业务逻辑分析。
