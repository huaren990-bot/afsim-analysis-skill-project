# x-level-capabilities.md 模板

## 要求

四层功能层次文档。必须按 System-level → Module-level → Class-level → Method-level 四层展开。
所有功能必须可追溯到 function-index.jsonl 中的对应条目。
本文档只纳入仿真模型相关功能；training/demo/test/doc/tooling 等边界外功能不得进入正文，除非用户明确要求。

## 结构

```markdown
# [项目名称] 仿真框架功能层次文档

> **状态**：
> **日期**：
> **分析范围**：
> **分析深度**：
> **关联文档**：

---

## 0. 文档说明

**总体概述**：

**功能划分**：功能按四层体系组织：

| 层级 | 英文 | 定义 | 边界范围 | 对应索引 |
|------|------|------|----------|----------|
| **系统级** | System-level | 跨框架/域/插件层，组合多个模块完成的端到端业务能力 | 跨目录、跨子系统 | function-index level=System-level |
| **模块级** | Module-level | 在单一子系统/模块内，通过策略模式实现多变体的功能 | 同一目录或相邻目录 | function-index level=Module-level |
| **类级** | Class-level | 单个类（class）封装的职责集合 | 单个 .hpp + .cpp | function-index level=Class-level |
| **方法级** | Method-level | 单个函数/方法的具体算法实现 | 单个文件内的函数 | function-index level=Method-level |

---

## 1. 系统级功能总览

**功能总览**：说明本次识别的 System-level、Module-level、Class-level、Method-level 条目数量，概述主要仿真模型能力域，并说明完整 Method-level 清单位置。

| # | 系统级功能 | 核心职责 |
|---|-----------|----------|
| 1 | xxx（中文名称） | yyy |
| 2 | xxx（中文名称） | yyy |

---

## 2. xxx系统功能（中文名称）

1. **xxx系统功能概述**：
2. **功能对应条目**：见 function-index.jsonl 中 `level=System-level` 的条目 `qualified_name=xxx`
3. **模块级功能细览**：xxx系统功能共包含yyyy个模块级功能：

| 系统级功能 | 模块级功能 | 核心职责 |
|-----------|-----------|----------|
| xxx       | xxx（中文名称） | yyy |

### 2.1 xxx模块级功能（中文名称）

1. **xxx模块功能概述**：
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=xxx`
3. **类级功能细览**：xxx模块级功能共包含yyyy个类级功能：

| 模块级功能 | 类级功能 | 核心职责 |
|-----------|---------|----------|
| xxx       | xxx（中文名称） | yyy |

#### 2.1.1 xxx类级功能（中文名称）

1. **xxx类功能概述**：
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=xxx`
3. **方法级功能摘要**：xxx类级功能共包含 yyyy 个方法级功能。若数量超过 30 个，正文只列代表性方法和统计，不展开完整方法级清单；完整数据见 `source-index/function-index.jsonl` 或附录。

| 类级功能 | 方法级功能 | qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|---------|-----------|----------------|----------------|----------------|----------|
| xxx     | xxx       | Class::Method  | model_update   | math           | yyy      |

### 2.2 xxx模块级功能（中文名称）

继续按同一结构完整列出后续模块级功能；不得使用省略号代替内容。

---

## 3. yyy系统功能（中文名称）

继续按同一结构完整列出后续系统级功能；不得使用省略号代替内容。

---

## 附录：方法级功能完整清单

（当方法级功能超过 30 个时，优先提供完整索引位置和统计；如用户要求在 Markdown 展示，则在此附录中完整列出所有仿真模型相关方法级功能，不在正文中使用省略号）

| qualified_name | lifecycle_role | algorithm_hint | 核心职责 |
|----------------|----------------|----------------|----------|
```

## 填写规则

1. 文档标题必须为 `# [项目名称] 仿真框架功能层次文档`，不可擅自修改。
2. 必须包含四层级：System-level → Module-level → Class-level → Method-level。
3. 每个功能层级必须包含"功能对应条目"段落，明确写出对应 function-index.jsonl 中 `level=xxx` 的条目 `qualified_name`。
4. 方法级功能表格中必须使用个体的 `qualified_name`（如 `WsfP6DOF_Mover::Initialize`），不可写成抽象群组（如"生命周期方法"）。
5. 表格列必须与模板完全一致，不可增删列、不可修改表头文字。
6. 不能使用省略号省略内容；方法级条目超过 30 条时，正文摘要化并给出完整 `function-index.jsonl` 或附录链接。
7. 所有英文标识首次出现时必须附带中文翻译。
8. 每个方法级功能的 `qualified_name` 必须可在 function-index.jsonl 中查到。
9. 必须包含“功能总览”章节，说明功能数量和主要能力域。
10. 只包含仿真模型相关功能；边界外功能必须过滤或说明用户显式纳入。
