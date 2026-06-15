---
name: cpp-proj-modules
description: Phase 2: C++项目模块级粗粒度分析 — 逐模块使用 codegraph_explore，建立文件索引(file-index.jsonl)、符号粗索引(symbol-index.jsonl)、模块概览文档。产出 3 个文件。
metadata:
  phase: 2
  requires-codegraph: true
  produces: file-index.jsonl, symbol-index.jsonl (coarse), module-overview.md
---

# Phase 2: 模块级粗粒度分析

## 目标

在 Phase 1 骨架视图基础上，使用 **CodeGraph MCP 工具**逐模块进行粗粒度源码分析：
- 生成全量文件索引（含 includes 解析）
- 生成符号粗索引（class/struct/enum 级别）
- 生成模块概览文档

本阶段达到"知道每个文件干什么、每个模块有哪些核心类"的程度。

## 输入

- `project-boundary/project-boundary.json`（Phase 1 产出）
- `project-boundary/file-classification.jsonl`（Phase 1 产出）

## 执行步骤

### Step 1: 读取 Phase 1 产出

1. 读取 `project-boundary.json`，获取模块清单和分析边界。
2. 读取 `file-classification.jsonl`，获取全量文件列表。
3. 确认目标模块列表（按 `analysis_depth` 决定覆盖范围）。

### Step 2: 逐模块 codegraph_explore（批量 + 去重）

按以下顺序使用 CodeGraph，**遵守批量优先与去重原则**：

1. **模块级探索**（每模块仅 1 次调用）：
   ```
   codegraph_explore "<module_name> module overview - main classes, key files, core responsibilities"
   ```
   获取该模块的核心类、关键文件、主体职责。
   - **每模块只调用 1 次**，不可对同一模块使用不同查询词重复探索。
   - 若返回空结果，回退到读取模块根目录下的 `CMakeLists.txt` + 列举 `*.hpp` 文件，不再重试 codegraph_explore。

2. **子目录探索**（仅在模块有 ≥2 个明显子目录时执行，每子目录仅 1 次）：
   ```
   codegraph_explore "<module_name>/<subdirectory> - what classes and files, what does this subsystem do"
   ```
   - 若模块仅有 1 个平铺目录，**跳过此步**，不要对单目录反复探索。

3. **代表性头文件读取**（每子目录最多 1 个代表性头文件）：
   ```
   codegraph_node "<file_path>"
   ```
   - 维护一个 `已读文件集合`，**同一 file_path 绝不读第 2 次**。
   - 若 codegraph_node 返回空或错误，**不要重试**，改用 `Read` 工具读取文件前 100 行作为降级方案。

### Step 3: 生成 file-index.jsonl

在 Phase 1 的 `file-classification.jsonl` 基础上扩展，为每个文件增加：

- `key_symbols`：从 codegraph_explore 结果中提取该文件定义的主要符号。
- `functions`：该文件中包含的方法级功能名称。
- `includes`：**必须解析** `#include` 指令。**按文件批量读取**（每文件至多 1 次 read 或 codegraph_node），提取所有 `#include "..."` 和 `#include <...>` 路径。
  - 对于文件数超过 50 的模块，使用 shell 命令 `rg "^#include" <module_dir> --type cpp --type-add 'hpp:*.hpp' -n` **一次性**获取全模块的 include 行，而非逐文件读取。
- `brief`：从 codegraph 结果中总结一句话职责描述。

### Step 4: 生成 symbol-index.jsonl（粗版）

对每个模块，提取其核心符号：

- `class`/`struct`：类名、限定名、继承关系、文件位置。
- `enum`/`enum_class`：枚举名、所属类、文件位置。
- `typedef`/`using`：类型别名、原类型、文件位置。
- `namespace`：命名空间名称、文件位置。

通过 codegraph_explore 批量获取继承关系（**不要逐类查询**）：

```
# 一次性问整个模块的继承图
codegraph_explore "<module_name> all classes inheritance hierarchy"
```

- 单次查询涵盖模块内所有类。
- 若查询结果未覆盖某个类，**不要单独为该再类调用一次 codegraph_explore**，而是直接读取该类的头文件（仅读一次）提取基类。
- 维护一个 `已查询集合`，保证同一个查询词绝不发两次。

### Step 5: 生成 module-overview.md

按以下结构撰写模块概览文档：

```markdown
# 模块概览文档

## 模块清单

| # | 模块名 | 路径 | 文件数 | 核心职责 |
|---|--------|------|--------|----------|
| 1 | xxx    | xxx  | xxx    | xxx      |

## 各模块详情

### 模块 1: xxx

#### 子系统结构

| 子系统 | 路径 | 文件数 | 核心职责 |
|--------|------|--------|----------|

#### 核心类

| 类名 | 文件 | 基类 | 职责 |
|------|------|------|------|

#### 关键依赖

| 依赖模块 | 依赖类型 | 说明 |
|----------|----------|------|

### 模块 2: xxx
...
```

## 输出文件

- `source-index/file-index.jsonl`
- `source-index/symbol-index.jsonl`（粗版，Phase 3 将精细化）
- `architecture/module-overview.md`

## 质量门槛

1. `file-index.jsonl` 覆盖所有 `source` 和 `header` 类型文件。
2. `source`/`header` 文件的 `includes` 数组**已解析填充**，不可全部为 `[]`。
3. `symbol-index.jsonl` 覆盖所有模块的核心类（每个模块至少 5 个符号）。
4. `symbol-index.jsonl` 每行可被 JSON parser 解析。
5. `module-overview.md` 覆盖所有模块，每个模块含核心类清单。
6. 符号的 `kind` 为 `class`/`struct` 时必须包含 `base_symbols` 信息。
7. 不含前向声明（`class X;` 形式）条目。

## 并行化策略

如果模块数量超过 5 个，建议按模块拆分并行执行：
- 每个模块分配一个独立的 codegraph_explore 调用
- 最后合并各模块的索引文件
