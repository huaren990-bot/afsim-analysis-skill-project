---
name: cpp-proj-report
description: Phase 7: 综合报告生成 — 汇总前 6 阶段产出，生成 afsim-architecture.md、x-level-capabilities.md、module-dependency.md 三份最终报告。
metadata:
  phase: 7
  requires-codegraph: false
  produces: afsim-architecture.md, x-level-capabilities.md, module-dependency.md
---

# Phase 7: 综合报告与架构文档生成

## 目标

汇总前 6 个阶段的所有产出，生成面向人类读者的三份最终报告：
- **afsim-architecture.md**：总体架构报告
- **x-level-capabilities.md**：四层功能层次文档
- **module-dependency.md**：模块依赖说明

本阶段**不执行新的源码分析**，只做信息汇总、交叉验证、格式化和排版。

## 输入

- Phase 1-6 全部产出文件（共约 15+ 个文件）
- 特别关键的是：
  - `project-boundary/project-boundary.json`
  - `source-index/symbol-index.jsonl`
  - `source-index/function-index.jsonl`
  - `source-index/dependency-index.jsonl`
  - `architecture/lifecycle.md`
  - `architecture/dataflow.md`
  - `architecture/extension-points.md`
  - `architecture/module-overview.md`

## 执行步骤

### Step 1: 汇总全部索引数据

1. 读取所有 JSONL 索引文件，载入内存。**每个文件仅读取 1 次**，后续所有引用都复用该次读取的内容。
2. 确认各索引之间的交叉引用（qualified_name、path）是一致的。
3. 如发现不一致，记录但不在本阶段修改（应由上游阶段修复）。

**⚠️ 防重复工具调用**：
- 维护 `已读文件集合`，同一 JSONL 文件在本 Phase 内绝不读第 2 次。
- 跨 Step 引用时（如 Step 3 需要 function-index.jsonl），复用 Step 1 已读的内容，不重新打开。
- 若读取某个文件失败，在对应报告章节标注"数据源不可用"并继续，不重试。

### Step 2: 生成 afsim-architecture.md

参照模板 `skill/cpp-project-analyzer/templates/template_architecture.md` 的结构：

```markdown
# AFSIM 仿真框架架构文档

> **状态**：已完成
> **日期**：<当前日期>
> **分析范围**：<从 project-boundary.json 提取>
> **分析深度**：<从 project-boundary.json 提取>
> **基线文档**：<Phase 1-6 产出>

## 0. 文档说明
## 1. 目录结构总览
## 2. 模块总览
## 3. 仿真生命周期
## 4. 数据流
## 5. 配置流
## 6. 扩展点
## 7. 关键符号
## 8. 未知项
## 9. 源码证据
```

对各章节要求：
- **目录结构总览**：从 project-boundary.json 提取，含中文说明。
- **模块总览**：从 module-overview.md 汇总，按系统/子系统/模块三级组织。
- **仿真生命周期**：从 lifecycle.md 提取要点，含 Mermaid 图和关联表。
- **数据流**：从 dataflow.md 提取要点，含 Mermaid 图。
- **配置流**：从 dataflow.md 提取配置流向，含 Mermaid 图。
- **扩展点**：从 extension-points.md 汇总。
- **关键符号**：从 symbol-index.jsonl 提取最重要的 30 个符号。
- **未知项**：汇总所有阶段尚为 unknown 的问题。
- **源码证据**：列出所有产出文件及其统计数据。

### Step 3: 生成 x-level-capabilities.md

参照模板 `skill/cpp-project-analyzer/templates/template_x-level-capabilities.md` 的结构。

**必须按四层展开**：

1. **System-level**：列出所有系统级功能，每个系统级功能下列出其 Module-level 子功能。
2. **Module-level**：每个模块级功能下列出其 Class-level 子功能。
3. **Class-level**：每个类级功能下列出其 Method-level 子功能。
4. **Method-level**：每个方法级功能包含其 `qualified_name`、`brief`、`lifecycle_role`、`algorithm_hint`。

**关键要求**：
- 文档标题为 `# AFSIM 仿真框架架构文档`，不可擅自修改。
- 方法级功能表格中的 `qualified_name` 必须使用个体名（如 `WsfP6DOF_Mover::Initialize`），不可写成抽象群组（如"生命周期方法"）。
- 每个功能层级必须包含"功能对应条目"段落，明确写出对应 function-index.jsonl 中 level=xxx 的条目 qualified_name。
- 表格列必须与模板完全一致。

### Step 4: 生成 module-dependency.md

参照模板 `skill/cpp-project-analyzer/templates/template_module-dependency.md` 的结构。

包含：
1. **构建依赖**：Mermaid 图 + 依赖关系表
2. **架构级依赖（继承/组合/调用）**：Mermaid 图 + 依赖关系表
3. **子系统间依赖**：Mermaid 图 + 依赖关系表
4. **关键全局常量依赖**：常量表
5. **依赖强度说明**

**关键要求**：
- Mermaid 图中的每一条边可追溯到 dependency-index.jsonl 或源码位置。
- 依赖强度分类：`build` → strong, 继承/组合 → strong/medium, 调用→ medium/weak。

### Step 5: 生成最终验证报告

汇总 Phase 1-6 所有验证报告的结论，生成 `verification/phase7-final-verify-report.md`：
- 各阶段验证通过/不通过统计
- 仍存在的 known-issues
- 整体质量评分

## 输出文件

- `architecture/afsim-architecture.md`
- `architecture/x-level-capabilities.md`
- `architecture/module-dependency.md`
- `verification/phase7-final-verify-report.md`

## 质量门槛

1. afsim-architecture.md 包含模板要求的全部章节（0-9）。
2. x-level-capabilities.md 包含四层功能，标题为 `# AFSIM 仿真框架架构文档`。
3. x-level-capabilities.md 的方法级功能表格中，每个 `qualified_name` 可在 function-index.jsonl 中查到。
4. module-dependency.md 中每一条 Mermaid 边可追溯到 dependency-index.jsonl。
5. 三份报告中的模块名、符号名、函数名统一一致，无歧义。
6. 所有 `.md` 文件中英文标识均有中文翻译说明。
7. 不得使用省略号省略内容；条目超过 30 条时新建独立文件完整列出。
