---
name: cpp-project-analyzer
description: 当用户需要对 C++ 项目进行全面源码分析、架构认知、模块理解、符号索引、依赖关系梳理、生命周期追踪，或需要协调多个分析阶段 Agent 完成端到端细粒度源码认知时，使用本 skill。基于 CodeGraph MCP 工具实现从粗到细的 7 阶段分析流水线。
metadata:
  short-description: C++ 项目多阶段细粒度分析总控，基于 CodeGraph 从粗到细 7 阶段流水线
  pipeline-phases: 7
  requires-codegraph: true
---

# C++ 项目多阶段细粒度分析总控 Skill

## 核心定位

本 skill 是 C++ 项目分析的**总控入口**（Orchestrator）。它不直接执行源码分析，而是：

1. 接收用户的分析请求，确定分析边界和深度。
2. 按 **7 阶段流水线** 依次调度各阶段 Agent，每阶段完成后立即触发对应验证 Agent。
3. 确保每一阶段的输出产物符合模板规范和质量门槛，不合格则退回重做。
4. 在各阶段之间传递上下文（上游输出 = 下游输入），保障信息不丢失。
5. 汇总最终产物，向用户交付完整的分析报告。

## ⚠️ 防止重复工具调用协议（必须严格遵守）

本 skill 的 API 后端会检测并拒绝重复的工具调用（同一工具、相同参数、连续多轮）。为避免触发 `Repetitive tool calls detected` 错误，所有 Agent **必须**遵守以下规则：

### 规则 1: 工具调用去重（Dedup Before Call）

每个 Agent 在内部维护一个 `已调用集合`（概念上是一个 Set），键为 `<tool_name>::<args_hash>`。每次调用工具前：

1. 检查该调用是否已在集合中。
2. 若已存在 → **跳过该调用**，直接使用上次缓存的结果。
3. 若不存在 → 执行调用，将键加入集合。

### 规则 2: 失败不重试（No-Retry on Failure）

当工具调用返回以下结果时，**禁止**使用相同参数重试：

- 空结果 / 无匹配（如 `codegraph_explore` 返回空、`codegraph_node` 找不到符号）
- 错误信息（如 file not found、symbol not indexed）
- 超时或网络错误

正确做法：
1. 记录该调用失败（在 notes 中标记 `"<tool> failed for <target>: <reason>"`）。
2. 尝试**不同的参数**（如换一个查询词、换一个文件路径）或**不同的工具**（如从 codegraph 回退到 grep/read）。
3. 若仍无法获取，标记为 `evidence_level: "unknown"` 并继续。

### 规则 3: 批量优先（Batch Over Per-Item）

**禁止**以下模式：

```
for each symbol in symbol_list:
    codegraph_node(symbol)      ← 可能重复调用
```

**改为**按文件分组批量处理：

```
group symbols by file_path
for each file_path:
    read file_path once         ← 单次读取
    extract all symbols from the file content
```

同理，`codegraph_explore` 应按模块/子系统批量提问（一次涵盖多个符号），而非逐符号查询。

### 规则 4: 阶段重试时 prompt 必须变化

当验证不通过需要重做时，总控**不可**用完全相同的 prompt 重新启动分析 Agent。必须：

1. 在 prompt 中**内联**验证报告的具体不通过项。
2. 明确指出"上一轮已尝试过 X，本次应改为 Y"。
3. 限制重做次数为 2 次，超过则标记 known-issue 并继续。

### 规则 5: 验证抽样去重

验证 Agent 抽样读取源文件时：

1. 维护一个 `已读文件集合`。
2. 抽样时跳过已读文件，确保每个文件最多读取 1 次。
3. 若需多次引用同一文件，复用首次读取的内容。

### 规则 6: 进度保护（Progress Guard）

如果 Agent 发现自己连续 3 次工具调用都无法推进进度（返回空/错误/重复），必须：

1. **停止当前循环**。
2. 总结已获得的成果。
3. 将未完成的项标记为 `unknown`。
4. 输出当前产物并结束。

## 设计原则

- **从粗到细**：项目结构 → 模块职责 → 符号清单 → 函数细节 → 依赖关系 → 生命周期 → 综合验证
- **每阶段自带验证**：每个分析 Agent 执行完后，立即启动验证 Agent 检查输出质量。验证不通过则分析 Agent 修正后重新验证。
- **输入输出明确**：每个阶段都有严格定义的输入文件（依赖上游产出）和输出文件（供下游消费）。
- **CodeGraph 优先**：所有代码查询优先使用 CodeGraph MCP 工具（`codegraph_explore`、`codegraph_node`、`codegraph_search`），仅在 CodeGraph 未覆盖时回退到 grep/read。
- **中文面向新手**：所有生成的 .md 报告面向母语为中文、无项目背景知识的程序员。具体要求如下：
  - **章节标题与表格表头**：必须使用中文（如“检查结果汇总”而非“Check Results Summary”）。
  - **描述性文字与评价**：必须使用中文撰写（如“总体评价”“结果：✅ 通过”而非“Overall Assessment”“Result: PASS”）。
  - **技术术语处理**：关键 C++ 术语（如 class、struct、namespace、typedef）保留英文以确保精确性，但可附带中文标注（如“class（类）”“struct（结构体）”）。首次出现时标注，后续可省略中文标注。
  - **代码标识符**：类名、函数名、变量名、文件路径等代码标识符保持原文，不做翻译。
  - **JSONL 数据文件中的描述字段**：`brief`、`notes`、`responsibility` 等面向人类的字段内容应使用中文撰写。
  - **验证报告**：章节、表格、结论全部使用中文。
- **绝不重复调用**：任何工具调用都必须推进认知，重复调用是严重违规。

## CodeGraph 配置与优先策略

### 索引位置

```
/Users/hjt/afsim/afsim-analysis-skill-project/source_root/afsim-2_9/.codegraph
```

### 工具调用优先级（必须严格遵守）

对于所有代码查询类任务，按以下优先级选择工具：

| 优先级 | 工具 | 适用场景 | 说明 |
|--------|------|----------|------|
| **1 (最高)** | `codegraph_explore` | 理解代码结构、调用关系、符号含义 | 一次调用可回答多个相关问题，返回源码+调用路径 |
| **2** | `codegraph_node` | 获取特定符号的源码、调用者列表、读取整个文件 | 精确查询单个符号或文件 |
| **3** | `codegraph_search` | 搜索符号名、函数名、类名 | 基于索引的符号搜索 |
| **4 (回退)** | `rg` / `grep` | CodeGraph 未覆盖的文件或模式匹配 | 文本搜索，无语义理解 |
| **5 (最后)** | `Read` | 读取完整文件内容 | 仅在需要完整文件时使用 |

### CodeGraph 使用模式

#### 模式 1: 批量探索（推荐）

```
codegraph_explore("模块 X 的核心类和它们之间的关系")
codegraph_explore("类 Y 的所有成员函数和继承关系")
```

一次调用涵盖多个符号，避免逐符号查询。

#### 模式 2: 精确查询

```
codegraph_node("Class::Method")  // 获取特定方法的源码和调用者
codegraph_node("/path/to/file.h")  // 读取整个文件（带行号）
```

#### 模式 3: 符号搜索

```
codegraph_search("Factory")  // 搜索所有含 "Factory" 的符号
```

### 回退策略

当 CodeGraph 查询返回空或错误时：

1. **不要重试相同查询** — 记录为 `evidence_level: "unknown"` 或标记 `notes: ["codegraph failed for X"]`
2. **尝试不同查询词** — 换用类名、函数名、模块名等不同关键词
3. **回退到文本搜索** — 使用 `rg` 或 `grep` 进行模式匹配
4. **最后才读文件** — 使用 `Read` 工具读取完整文件

### 各阶段 CodeGraph 使用建议

| 阶段 | CodeGraph 使用程度 | 说明 |
|------|-------------------|------|
| Phase 1 | 低 | 主要用 shell 扫描目录结构，可用 `codegraph_explore` 快速了解项目架构 |
| Phase 2 | 中 | 用 `codegraph_explore` 理解模块职责和核心类 |
| Phase 3 | 高 | 用 `codegraph_node` 获取符号详细信息（签名、继承、成员） |
| Phase 4 | 高 | 用 `codegraph_node` 获取函数源码、参数、调用链 |
| Phase 5 | 高 | 用 `codegraph_explore` 分析跨模块依赖和调用关系 |
| Phase 6 | 高 | 用 `codegraph_explore` 追踪生命周期和数据流 |
| Phase 7 | 低 | 主要汇总已有产出，CodeGraph 用于补充验证 |

### Agent Prompt 中的 CodeGraph 提醒

每个分析 Agent 的 prompt 中必须包含以下提醒：

```
## CodeGraph 优先（必须遵守）
1. 所有代码查询优先使用 CodeGraph 工具（codegraph_explore、codegraph_node、codegraph_search）。
2. 仅当 CodeGraph 返回空或错误时，才回退到 rg/grep/Read。
3. CodeGraph 查询失败后，不要重试相同查询，改用不同关键词或回退到文本搜索。
4. 批量探索：一次 codegraph_explore 调用涵盖多个相关符号，避免逐符号查询。
5. CodeGraph 索引位置：/Users/hjt/afsim/afsim-analysis-skill-project/source_root/afsim-2_9/.codegraph
```


## 7 阶段流水线总览

```
Phase 1: 边界确认与项目结构发现
  ├── 输入: 用户指定的源码根目录、分析范围
  ├── 分析: 目录树扫描、构建系统识别、文件分类
  ├── 输出: project-boundary.json, file-classification.jsonl
  └── 验证: Phase 1 Verifier 检查输出完整性与合理性

Phase 2: 模块级粗粒度分析
  ├── 输入: Phase 1 产出
  ├── 分析: 每个模块的职责、子目录结构、核心类列举
  ├── 输出: file-index.jsonl (全量), symbol-index.jsonl (粗), module-overview.md
  └── 验证: Phase 2 Verifier 检查索引覆盖率、模板合规性

Phase 3: 符号级细粒度分析
  ├── 输入: Phase 2 产出
  ├── 分析: 逐符号提取签名、继承关系、成员变量、枚举值、宏常量
  ├── 输出: symbol-index.jsonl (精), macro-index.jsonl, enum-index.jsonl
  └── 验证: Phase 3 Verifier 检查符号去重、枚举值完整性、宏过滤正确性

Phase 4: 函数/方法级深度提取
  ├── 输入: Phase 3 产出
  ├── 分析: 逐函数提取参数(含默认值)、返回类型、调用链、生命周期角色、算法提示
  ├── 输出: function-index.jsonl (四层), function-body-summary.jsonl
  └── 验证: Phase 4 Verifier 检查四层完整性、参数覆盖、qualified_name 唯一性

Phase 5: 跨模块依赖关系分析
  ├── 输入: Phase 2+3+4 产出
  ├── 分析: 构建依赖、继承依赖、组合依赖、调用依赖、注册依赖、include 依赖
  ├── 输出: dependency-index.jsonl, dependency-graph.md
  └── 验证: Phase 5 Verifier 检查依赖覆盖率(≥200条)、六种relation全覆盖

Phase 6: 生命周期与数据流分析
  ├── 输入: Phase 2+4+5 产出
  ├── 分析: 仿真/应用生命周期、数据流路径、配置流路径、扩展点识别
  ├── 输出: lifecycle.md, dataflow.md, extension-points.md
  └── 验证: Phase 6 Verifier 检查生命周期阶段完整性、数据流可追溯性

Phase 7: 综合验证与架构文档生成
  ├── 输入: Phase 1-6 全部产出
  ├── 分析: 汇总生成架构文档、功能层次文档、模块依赖文档
  ├── 输出: afsim-architecture.md, x-level-capabilities.md, module-dependency.md, final-verification-report.md
  └── 验证: Phase 7 Verifier 进行全量交叉一致性检查
```

## 各阶段 Agent 与 Skill 映射

| 阶段 | 分析 Skill | 验证 Skill | 职责 |
|------|-----------|-----------|------|
| Phase 1 | `cpp-proj-boundary` | `cpp-proj-boundary-verify` | 边界确认、目录扫描、文件分类 |
| Phase 2 | `cpp-proj-modules` | `cpp-proj-modules-verify` | 模块粗粒度分析、文件索引 |
| Phase 3 | `cpp-proj-symbols` | `cpp-proj-symbols-verify` | 符号细粒度分析 |
| Phase 4 | `cpp-proj-functions` | `cpp-proj-functions-verify` | 函数/方法深度提取 |
| Phase 5 | `cpp-proj-dependencies` | `cpp-proj-dependencies-verify` | 跨模块依赖分析 |
| Phase 6 | `cpp-proj-lifecycle` | `cpp-proj-lifecycle-verify` | 生命周期与数据流 |
| Phase 7 | `cpp-proj-report` | `cpp-proj-final-verify` | 综合报告与全量验证 |

## 输入要求

开始分析前确认以下输入：

- `source_root`：源码根目录的绝对路径。
- `extract_root`：本次需要解析的根目录（通常在 `source_root` 之下）。
- `analysis_scope`：本轮纳入的目录、模块、文件类型或用户指定主题。如未指定则默认覆盖 `extract_root` 下所有 C++ 源文件。
- `exclude_paths`：排除目录列表。默认排除 `.git`、以 `.` 开头的隐藏文件、`build/`、`3rd_party/`、`node_modules/`、`*.so`、`*.dll`、`*.a`、`*.osgb`。
- `analysis_depth`：`full`（全部 7 阶段）、`module`（Phase 1-3）、`overview`（Phase 1-2）。
- `baseline_docs`：用户提供的已有文档、设计说明、历史分析报告路径列表。

## 标准工作流

### Step 0: 确认边界

1. 读取用户指定的 `source_root`、`extract_root`、`analysis_scope`、`exclude_paths`。
2. 检查是否存在 `.codegraph/` 目录，确认 CodeGraph 已初始化。
   - 标准路径：`<source_root>/afsim-2_9/.codegraph/`
   - 若存在 → 在所有后续阶段中启用 CodeGraph 优先策略。
   - 若缺失 → 提示用户运行 `codegraph index` 初始化索引，或降级为纯 grep/read 模式。
3. 若缺失关键输入参数，主动询问用户。
4. 确定 `analysis_depth`，控制执行到哪个阶段停止。

### Step 1-7: 逐阶段执行

对每个阶段：

1. **启动分析 Agent**：传入上游阶段的全部输出文件路径作为输入。**必须在 prompt 尾部附加防重复调用提醒**（见下方模板）。
2. **等待分析完成**：确认分析 Agent 已将输出写入指定路径。
3. **启动验证 Agent**：传入分析 Agent 的输出文件路径 + 本阶段 Skill 定义的质量门槛。同样附加防重复调用提醒。
4. **检查验证结果**：
   - 全部通过 → 进入下一阶段。
   - 存在不通过项 → **提取具体不通过项列表**，将其内联到新的 prompt 中，明确写出"上一轮问题：X，本轮需修正：Y"，重新启动分析 Agent（最多重试 2 次）。**绝不可用相同 prompt 重试**。
   - 重试 2 次仍不通过 → 记录为 `known-issue`，向用户报告后继续。

### 最后一个阶段完成后

1. 汇总所有阶段的输出文件清单。
2. 汇总所有验证报告。
3. 向用户交付摘要：分析范围、产出文件、关键发现、仍为 unknown 的项、质量门禁通过情况。

### 每阶段完成后自动记录（必须执行）

每个阶段（含验证）完成后，总控 Agent **必须**自动将本次执行结果记录到 `docs/records/` 目录。此步骤不可跳过。

#### 记录文件命名

```
docs/records/<序号>-phase<N>-<阶段名称>.md
```

序号递增，基于 `docs/records/` 中已有文件的最大序号 +1。例如已有 `13-phase1-boundary-analysis.md`，则 Phase 2 记录为 `14-phase2-modules-analysis.md`。

#### 记录内容模板

```markdown
# Phase <N> 完成记录：<阶段中文名称>

> **完成日期**：YYYY-MM-DD
> **阶段**：Phase <N> / 7
> **状态**：✅ 已完成并通过验证 / ⚠️ 已完成（存在 known-issue）

## 分析范围

| 参数 | 值 |
|------|-----|
| source_root | ... |
| extract_roots | ... |
| exclude_paths | ... |
| analysis_depth | ... |

## 执行方式

| 子阶段 | Agent 数 | 职责 |
|--------|----------|------|
| Phase <N>A: ... | N | ... |
| Phase <N>B: ... | N | ... |

**总耗时**：约 X 分钟
**总 Agent 数**：N
**总工具调用**：N 次

## 产出文件

| 文件 | 路径 | 大小 |
|------|------|------|
| ... | workspace/... | ... |

## 关键统计数据

（根据各阶段产出填写核心指标，如文件数、符号数、函数数、依赖数等）

## 验证结果

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | ... | ✅/❌ | ... |

## 已知问题与备注

（列出 known-issue、重试次数、降级项等）

## 下游就绪

（说明本阶段产出如何供下游消费）
```

#### 自动记录执行步骤

1. 运行 `ls docs/records/` 确定当前最大序号。
2. 收集本阶段执行数据：Agent 数量、工具调用次数、耗时、产出文件列表和大小。
3. 从验证报告中提取检查结果汇总表。
4. 按模板写入 `docs/records/<序号>-phase<N>-<name>.md`。
5. 在总控日志中确认记录已写入。

## 输出文件规范

所有输出文件放置在用户当前工作区下的workspace文件夹下，按以下目录组织：

```
<workspace>/
├── project-boundary/
│   ├── project-boundary.json        # Phase 1 产出
│   └── file-classification.jsonl    # Phase 1 产出
├── source-index/
│   ├── file-index.jsonl             # Phase 2 产出
│   ├── symbol-index.jsonl           # Phase 3 产出（精细版）
│   ├── macro-index.jsonl            # Phase 3 产出
│   ├── enum-index.jsonl             # Phase 3 产出
│   ├── function-index.jsonl         # Phase 4 产出
│   ├── function-body-summary.jsonl  # Phase 4 产出
│   └── dependency-index.jsonl       # Phase 5 产出
├── architecture/
│   ├── module-overview.md           # Phase 2 产出
│   ├── dependency-graph.md          # Phase 5 产出
│   ├── lifecycle.md                 # Phase 6 产出
│   ├── dataflow.md                  # Phase 6 产出
│   ├── extension-points.md          # Phase 6 产出
│   ├── afsim-architecture.md        # Phase 7 产出
│   ├── x-level-capabilities.md      # Phase 7 产出
│   └── module-dependency.md         # Phase 7 产出
└── verification/
    ├── phase1-verify-report.md      # Phase 1 验证报告
    ├── phase2-verify-report.md      # Phase 2 验证报告
    ├── phase3-verify-report.md      # Phase 3 验证报告
    ├── phase4-verify-report.md      # Phase 4 验证报告
    ├── phase5-verify-report.md      # Phase 5 验证报告
    ├── phase6-verify-report.md      # Phase 6 验证报告
    └── phase7-final-verify-report.md # Phase 7 全量验证报告
```

## 证据等级

各阶段分析产出的每一条结论必须标注证据等级：

- `source-cited`：由源码路径、符号和行号直接支持。
- `document-cited`：由用户文档、设计文档或历史报告支持。
- `index-derived`：由上一阶段生成的索引汇总得到。
- `inferred`：由相邻证据推断，但源码未直接说明（必须说明推断依据）。
- `unknown`：证据不足。

## 阶段间上下文传递协议

每个阶段启动时，必须先读取模板 `templates/template_context-handoff.md`，填写完整后传递给下游 Agent。

分析 Agent 启动时，必须在其 prompt 中明确列出：

```
本阶段输入文件：
  - xxx.jsonl （来自 Phase N，路径：...）
  - yyy.md   （来自 Phase M，路径：...）

本阶段输出要求：
  - 输出文件 1：路径、格式、模板参考
  - 输出文件 2：路径、格式、模板参考·

本阶段质量门槛：
  - 检查项 1
  - 检查项 2
  ...
```

验证 Agent 启动时，必须在其 prompt 中明确列出：

```
本阶段验证对象：
  - 分析 Agent 输出文件 1（路径：...）
  - 分析 Agent 输出文件 2（路径：...）

验证依据：
  - 本阶段 Skill 定义的质量门槛
  - 对应模板文件（如有）

验证输出：
  - verification/phaseN-verify-report.md
```

## 错误处理与重试策略

1. **分析 Agent 执行失败**：记录错误信息，检查输入文件是否完整，重新启动一次。若再次失败，向用户报告并询问是否跳过该阶段。
2. **验证 Agent 发现不通过项**：将验证报告完整传递给分析 Agent，要求逐项修复。最多重试 2 次。
3. **CodeGraph 查询无结果**：回退到 `grep -r` 或 `rg` 进行文本搜索，并在结论中标记 `inferred`（非 CodeGraph 直接证据）。
4. **输出 JSONL 格式错误**：验证 Agent 逐行解析 JSONL，记录无法解析的行号和错误原因，退回分析 Agent 修正。

## 阶段间并行化建议

- Phase 2 可按模块并行：每个模块分配一个分析 Agent，最后合并索引。
- Phase 3 可按文件/模块并行：每个 Agent 负责一个模块的符号提取。
- Phase 4 可按模块并行：每个 Agent 负责一个模块的函数提取。
- Phase 5-7 需要全量数据，不可并行，但验证 Agent 可与下一阶段的分析 Agent 部分重叠。

## 需要读取的参考文件

- `skill/cpp-project-analyzer/templates/` — 各阶段输出模板（11 个模板）。
- `skill/cpp-project-analyzer/phases/phase*/SKILL.md` — 各阶段 Skill 详细说明。
- `skill/cpp-project-analyzer/phases/phase*/SKILL_VERIFY.md` — 各阶段验证 Skill 详细说明。

## Agent 调度指令

本 skill 使用 Claude Code 的 `Agent` 工具调度各阶段 Agent。调度模板如下：

### 分析 Agent 调度模板

```
Agent({
  description: "Phase <N>: <阶段名称>",
  prompt: "
    你是一个 C++ 源码分析 Agent。你的任务是执行 Phase <N>：<阶段名称>。

    请严格按照以下 Skill 定义执行：
    - 读取 Skill 文件：skill/cpp-project-analyzer/phases/phase<N>-<name>/SKILL.md
    - 读取模板文件：skill/cpp-project-analyzer/templates/template_<xxx>.md

    输入文件：
    - <上游产出文件 1>
    - <上游产出文件 2>

    输出文件：
    - <本阶段产出文件 1>
    - <本阶段产出文件 2>

    分析边界：
    - source_root: <路径>
    - extract_roots: <路径列表>
    - exclude_paths: <排除列表>

    ## ⚠️ 防重复工具调用（必须遵守）
    1. 每次调用工具前，确认本会话中尚未用相同参数调用过该工具。若已调用过，直接使用上次结果，绝不重复调用。
    2. 若某次工具调用返回空结果或错误，**不要用相同参数重试**。改为：(a) 换一个查询词，(b) 换一个工具（codegraph ↔ grep ↔ read），或 (c) 记录为 unknown 并继续。
    3. 处理多个符号/文件时，**按文件分组批量处理**：一次性读取文件，从中提取所有符号信息。禁止对每个符号单独调用 codegraph_node。
    4. 每轮对话至少要推进一个新的认知点。如果连续 3 次工具调用都未带来新信息，立即停止当前循环，总结已有成果并输出产物。

    执行完毕后，确认所有输出文件已写入。
  ",
  model: "sonnet"  // Phase 1-2 用 sonnet；Phase 3-4 用 opus
})
```

### 分析 Agent 重试调度模板（验证不通过时使用）

```
Agent({
  description: "Phase <N> Retry #<K>: <阶段名称>",
  prompt: "
    你是一个 C++ 源码分析 Agent。这是 Phase <N> 的第 <K> 次重试。

    ## 上一轮验证发现的问题（必须逐项修复）
    <粘贴验证报告中 ❌ 的每一项，含具体行号/qualified_name/问题描述>

    ## 修复策略要求
    - 针对问题 1：<具体修复指导>
    - 针对问题 2：<具体修复指导>
    - 不要重做已经通过验证的部分，只修复不通过项。

    请读取 Skill 文件并按上一轮相同输入执行，但**必须修正上述问题**：
    - Skill：skill/cpp-project-analyzer/phases/phase<N>-<name>/SKILL.md
    - 输入文件：<同上一轮>
    - 输出文件：<同上一轮，覆盖写入>

    ## ⚠️ 防重复工具调用（必须遵守）
    <同上 4 条规则>

    特别注意：上一轮 Agent 可能已经对以下工具调用失败过，本轮必须使用不同策略：
    <列出上一轮失败的工具调用和替代策略>
  ",
  model: "sonnet"
})
```

### 验证 Agent 调度模板

```
Agent({
  description: "Phase <N> Verify",
  prompt: "
    你是一个质量验证 Agent。你的任务是验证 Phase <N> 分析 Agent 的产出质量。

    请严格按照以下验证 Skill 执行：
    - 读取验证 Skill：skill/cpp-project-analyzer/phases/phase<N>-<name>/SKILL_VERIFY.md

    验证对象：
    - <分析产出文件 1>
    - <分析产出文件 2>

    对照模板：
    - skill/cpp-project-analyzer/templates/template_<xxx>.md

    输出：verification/phase<N>-verify-report.md

    对每个检查项给出 ✅ 或 ❌ 判定，并说明理由。

    ## ⚠️ 防重复工具调用（必须遵守）
    1. 抽样验证时，维护一个"已读文件集合"。每个源文件最多读取 1 次。若抽样命中已读文件，跳过并选择下一个。
    2. 若某个 codegraph 查询返回空或错误，**不要重试**，直接在报告中标注"无法验证此项"。
    3. 统计类检查（如条目计数、字段非空率）直接基于 JSONL 文件内容分析，**无需重复读取源文件**。
  "
})
```

### 模型选择策略

| 阶段 | 推荐模型 | 原因 |
|------|---------|------|
| Phase 1 | sonnet | 目录扫描，不需要深度推理 |
| Phase 2 | sonnet | 模块概览，粗粒度 |
| Phase 3 | opus | 符号精细化，需要理解 C++ 语法 |
| Phase 4 | opus | 函数深度提取，需要理解算法逻辑 |
| Phase 5 | sonnet | 依赖提取，结构化分析 |
| Phase 6 | opus | 生命周期追踪，需要跨文件推理 |
| Phase 7 | sonnet | 报告汇总，不需要源码分析 |
| 所有验证 | sonnet | 格式/规则检查为主 |

## Workflow 自动化脚本

以下是使用 Workflow 工具自动化执行全部 7 阶段的脚本模板。总控 Agent 可以直接调用：

```javascript
export const meta = {
  name: 'cpp-project-analysis',
  description: 'C++ 项目 7 阶段细粒度分析流水线',
  phases: [
    { title: 'Phase 1: 边界确认' },
    { title: 'Phase 2: 模块分析' },
    { title: 'Phase 3: 符号分析' },
    { title: 'Phase 4: 函数分析' },
    { title: 'Phase 5: 依赖分析' },
    { title: 'Phase 6: 生命周期' },
    { title: 'Phase 7: 综合报告' },
  ],,
}

// 防重复调用提醒文本，嵌入每个 Agent 的 prompt 尾部
const ANTI_REPETITION_REMINDER = `
## ⚠️ 防重复工具调用（必须严格遵守，否则会触发 API 错误）
1. 每次调用工具前，确认本会话中尚未用相同参数调用过该工具。若已调用过，直接使用上次结果，绝不重复调用。
2. 若某次工具调用返回空结果或错误，**不要用相同参数重试**。改为：(a) 换一个查询词，(b) 换一个工具（codegraph ↔ grep ↔ read），或 (c) 记录为 unknown 并继续。
3. 处理多个符号/文件时，**按文件分组批量处理**：一次性读取文件，从中提取所有符号信息。禁止对每个符号单独调用 codegraph_node。
4. 每轮对话至少要推进一个新的认知点。如果连续 3 次工具调用都未带来新信息，立即停止当前循环，总结已有成果并输出产物。

## CodeGraph 优先（必须遵守）
1. 所有代码查询优先使用 CodeGraph 工具（codegraph_explore、codegraph_node、codegraph_search）。
2. 仅当 CodeGraph 返回空或错误时，才回退到 rg/grep/Read。
3. CodeGraph 查询失败后，不要重试相同查询，改用不同关键词或回退到文本搜索。
4. 批量探索：一次 codegraph_explore 调用涵盖多个相关符号，避免逐符号查询。
5. CodeGraph 索引位置：/Users/hjt/afsim/afsim-analysis-skill-project/source_root/afsim-2_9/.codegraph
`

const PHASES = [
  {
    id: 1,
    name: 'boundary',
    skill: 'phase1-boundary',
    verify: 'phase1-boundary',
    model: 'sonnet',
    inputs: [],
    outputs: ['project-boundary/project-boundary.json', 'project-boundary/file-classification.jsonl'],
  },
  {
    id: 2,
    name: 'modules',
    skill: 'phase2-modules',
    verify: 'phase2-modules',
    model: 'sonnet',
    inputs: ['project-boundary/project-boundary.json', 'project-boundary/file-classification.jsonl'],
    outputs: ['source-index/file-index.jsonl', 'source-index/symbol-index.jsonl', 'architecture/module-overview.md'],
  },
  {
    id: 3,
    name: 'symbols',
    skill: 'phase3-symbols',
    verify: 'phase3-symbols',
    model: 'opus',
    inputs: ['source-index/file-index.jsonl', 'source-index/symbol-index.jsonl'],
    outputs: ['source-index/symbol-index.jsonl', 'source-index/macro-index.jsonl', 'source-index/enum-index.jsonl'],
  },
  {
    id: 4,
    name: 'functions',
    skill: 'phase4-functions',
    verify: 'phase4-functions',
    model: 'opus',
    inputs: ['source-index/symbol-index.jsonl', 'source-index/macro-index.jsonl', 'source-index/enum-index.jsonl'],
    outputs: ['source-index/function-index.jsonl', 'source-index/function-body-summary.jsonl'],
  },
  {
    id: 5,
    name: 'dependencies',
    skill: 'phase5-dependencies',
    verify: 'phase5-dependencies',
    model: 'sonnet',
    inputs: ['source-index/file-index.jsonl', 'source-index/symbol-index.jsonl', 'source-index/function-index.jsonl'],
    outputs: ['source-index/dependency-index.jsonl', 'architecture/dependency-graph.md'],
  },
  {
    id: 6,
    name: 'lifecycle',
    skill: 'phase6-lifecycle',
    verify: 'phase6-lifecycle',
    model: 'opus',
    inputs: ['source-index/function-index.jsonl', 'source-index/dependency-index.jsonl', 'source-index/symbol-index.jsonl'],
    outputs: ['architecture/lifecycle.md', 'architecture/dataflow.md', 'architecture/extension-points.md'],
  },
  {
    id: 7,
    name: 'report',
    skill: 'phase7-report',
    verify: 'phase7-report',
    model: 'sonnet',
    inputs: ['source-index/file-index.jsonl', 'source-index/symbol-index.jsonl', 'source-index/function-index.jsonl', 'source-index/dependency-index.jsonl', 'architecture/lifecycle.md', 'architecture/dataflow.md'],
    outputs: ['architecture/afsim-architecture.md', 'architecture/x-level-capabilities.md', 'architecture/module-dependency.md'],
  },
]

// 用于记录失败的调用，以便在重试时提供不同的策略
const failedCallsByPhase = {}

for (const phase of PHASES) {
  log(`开始 Phase ${phase.id}: ${phase.name}`)

  // 分析 Agent — prompt 包含防重复调用提醒
  const analysisPrompt = `执行 Phase ${phase.id} 分析。
     读取 Skill: skill/cpp-project-analyzer/phases/${phase.skill}/SKILL.md
     输入文件: ${phase.inputs.length ? phase.inputs.join(', ') : '（无，本阶段为首阶段）'}
     输出文件: ${phase.outputs.join(', ')}
     分析边界: source_root=${args.source_root}, extract_roots=${args.extract_roots}
     ${ANTI_REPETITION_REMINDER}`

  const analysisResult = await agent(analysisPrompt, {
    phase: `Phase ${phase.id}: ${phase.name}`,
    model: phase.model,
  })

  // 验证 Agent — prompt 也包含防重复调用提醒
  const verifyPrompt = `验证 Phase ${phase.id} 产出质量。
     读取验证 Skill: skill/cpp-project-analyzer/phases/${phase.verify}/SKILL_VERIFY.md
     验证对象: ${phase.outputs.join(', ')}
     输出验证报告: verification/phase${phase.id}-verify-report.md
     ${ANTI_REPETITION_REMINDER}
     额外要求：抽样验证时每个源文件最多读取 1 次，命中已读文件则跳过。`

  const verifyResult = await agent(verifyPrompt, {
    phase: `Phase ${phase.id}: ${phase.name}`,
  })

  // 自动记录 — 每阶段完成后写入 docs/records/
  const recordPrompt = `自动记录 Phase ${phase.id} 完成情况。

步骤：
1. 运行 ls docs/records/ 确定当前最大序号 N，新记录序号为 N+1。
2. 读取验证报告: verification/phase${phase.id}-verify-report.md，提取检查结果汇总表。
3. 读取本阶段产出文件列表，用 ls -lh 获取大小。
4. 按以下模板写入 docs/records/<序号>-phase${phase.id}-${phase.name}-analysis.md：

   # Phase ${phase.id} 完成记录：<阶段名称>
   > **完成日期**：（当天日期）
   > **阶段**：Phase ${phase.id} / 7
   > **状态**：✅ 已完成

   ## 分析范围
   （从 project-boundary.json 读取）

   ## 执行方式
   （记录本阶段的 Agent 协作方式）

   ## 产出文件
   （列出文件名、路径、大小）

   ## 关键统计数据
   （从产出文件中提取核心指标）

   ## 验证结果
   （从验证报告提取汇总表）

   ## 已知问题与备注
   ## 下游就绪

5. 确认记录文件已写入。`

  await agent(recordPrompt, {
    phase: `Phase ${phase.id}: ${phase.name}`,
    model: 'haiku',
    label: `record:phase${phase.id}`,
  })

  log(`Phase ${phase.id} 完成（含自动记录）`)
}

log('全部 7 阶段分析完成')
```

## 故障排除指南

### 常见问题与解决方案

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| CodeGraph 查询返回空结果 | `.codegraph/` 未初始化 | 运行 `codegraph index` 初始化索引，或回退到 `rg`/`grep` |
| JSONL 文件某行解析失败 | 行内包含未转义的换行符或引号 | 检查该行，确保 JSON object 在单行内闭合 |
| Phase 4 qualified_name 重复 | 同名函数在不同类中存在 | 使用 `Class::Method` 格式确保唯一 |
| Phase 5 依赖条目数不足 200 | 只提取了 build 依赖 | 补充 inheritance、composition、call、include、registration 五种关系 |
| Phase 6 生命周期阶段缺失 | 项目非仿真系统，无标准阶段 | 根据项目实际行为定义等价阶段 |
| 验证 Agent 反复不通过 | 分析 Agent 未正确理解模板 | 将模板文件内容直接嵌入分析 Agent prompt |
| Agent 执行超时 | 源码量过大 | 缩小 `analysis_scope`，或按模块拆分并行 |

### 回退策略

当某个阶段在重试 2 次后仍无法通过验证时：

1. **记录 known-issue**：在 context-handoff 文件中记录问题。
2. **标记降级输出**：在该阶段产出文件中标注 `evidence_level: "inferred"` 或 `"unknown"`。
3. **继续下游阶段**：不阻塞后续阶段，但下游阶段必须在 notes 中标注"上游数据不完整"。
4. **最终报告标注**：在 Phase 7 的 final-verify-report.md 中汇总所有 known-issues。

### 增量分析策略

当用户只对部分模块感兴趣时：

1. 在 `project-boundary.json` 中只列出目标模块。
2. Phase 2-4 只分析目标模块。
3. Phase 5 只提取目标模块相关的依赖。
4. Phase 6-7 基于缩减后的数据生成报告。
5. 在最终报告中标注"部分分析"。
