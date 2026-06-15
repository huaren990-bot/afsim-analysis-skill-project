---
name: cpp-proj-symbols
description: Phase 3: C++项目符号级细粒度分析 — 精细化 symbol-index.jsonl、生成 macro-index.jsonl 和 enum-index.jsonl，提取完整签名、枚举值、宏定义。
metadata:
  phase: 3
  requires-codegraph: true
  produces: symbol-index.jsonl (fine), macro-index.jsonl, enum-index.jsonl
---

# Phase 3: 符号级细粒度分析

## 目标

在 Phase 2 粗符号索引基础上，使用 CodeGraph **深入每个符号**：
- 精细化 symbol-index.jsonl（填充完整字段）
- 独立生成 macro-index.jsonl（全量宏定义）
- 独立生成 enum-index.jsonl（全量枚举定义，含每个枚举值）

本阶段达到"知道每个符号的完整签名、继承链、访问控制、成员变量"的程度。

## 输入

- `project-boundary/project-boundary.json`（Phase 1 产出）
- `source-index/file-index.jsonl`（Phase 2 产出）
- `source-index/symbol-index.jsonl`（Phase 2 粗版）

## 执行步骤

### Step 1: 读取上游产物

1. 读取 Phase 2 的 `symbol-index.jsonl`（粗版），获取已有符号清单。
2. 读取 `file-index.jsonl`，获取文件到模块的映射。

### Step 2: 按文件分组批量精细化

**⚠️ 关键规则：禁止逐符号调用 codegraph_node。必须按文件分组，每文件仅读 1 次。**

先将 Phase 2 粗版 symbol-index.jsonl 中的符号按 `declaration_path`（或 `path`）分组到各个源文件，然后：

```
for each file_path in 文件分组.keys():
    读取 file_path 一次（codegraph_node 或 Read）
    从返回的源码中提取本文件内所有符号的细节
    若 codegraph_node 失败 → 改用 Read 工具
    若 Read 也失败 → 将这些符号标记为 evidence_level: "unknown" 并继续
    绝不重试相同的调用
```

具体到每种符号类型：

1. **class/struct 精细化**：
   - 优先使用：`codegraph_node "<file_path>"`（按文件而非按符号查询）
   - 备选（仅当 codegraph_node 返回空时）：`Read <file_path>`
   - 从返回的文件内容中一次性提取本文件内所有 class/struct 的：
     - 完整类声明（含 public/protected/private 分界）
     - 全部基类（直接+间接）
     - 成员变量（类型、访问修饰符、默认值）
     - 成员函数签名
     - 嵌套类型
   - **禁止**对同一 file_path 调用第二次 codegraph_node（即使是查询不同符号）。

2. **enum/enum_class 精细化**：
   - 复用 Step 2.1 已读过的文件内容（不要重新读）。
   - 仅当枚举所在文件尚未被读过时，才调用：
     ```
     Read <file_path>
     ```
   - 提取每个枚举值及其显式/隐式赋值。

3. **typedef/using 精细化**：
   - 使用**模块级** codegraph_explore（而非逐符号）：
     ```
     codegraph_explore "<module_name> typedef using type aliases"
     ```
   - 同一模块只问一次。

4. **variable 精细化**：
   - 从已读过的文件内容中提取全局变量/静态成员的初始值、类型和用途。
   - 不发起新的工具调用。

### Step 3: 独立生成 macro-index.jsonl（批量 grep 模式）

**⚠️ 关键规则：使用 shell 批量 grep，禁止逐宏读取源文件。**

1. **一次性 grep 获取全量宏定义**：
   ```bash
   rg "^#\s*define\s+\w+" <extract_root> --include='*.hpp' --include='*.h' --include='*.cpp' -n
   ```
   此命令一次性返回所有宏定义的行，无需逐文件读取。

2. **过滤排除**（基于宏名模式匹配，不需要读源码）：
   - `*_EXPORT` 模式（如 `WSF_MIL_EXPORT`、`WSF_EXPORT`）— 这是 DLL 导出宏
   - Include guards（`_HPP`、`_H_` 结尾的宏）
   - 空替换体宏（如 `#define FOO`）— 通常是 feature flag，可选保留

3. **对每个剩余宏**，从 grep 返回的**那一行文本**直接解析：
   - 宏名称、替换体文本
   - 是否有参数（通过 `#define NAME(x, y)` 模式识别）
   - 推断的替换体类型
   - 使用该宏的文件（如需，用第二次 grep `rg "\b<macro_name>\b" <extract_root>` 一次性获取所有使用点，而非逐文件搜索）

4. **防重复保护**：
   - 同一 macro_name 在多个文件中重复定义时，只保留第一条，其余记录在 notes 中。
   - grep 命令只执行 2 次（定义 + 使用），不可对同一宏多次 grep。

### Step 4: 独立生成 enum-index.jsonl（复用已读文件）

**⚠️ 关键规则：复用 Step 2 已读过的文件内容，不发起新的读取。**

1. 从 symbol-index.jsonl 中筛选 `kind=enum` 和 `kind=enum_class` 的条目。
2. 按枚举所在的 `declaration_path` 分组。
3. 对每个文件分组：
   - **优先复用** Step 2 中已经读取过的该文件内容（如已在内存/上下文中）。
   - 若 Step 2 未读过该文件，则**仅此时**读取一次（`Read <file_path>`）。
   - 从文件内容中一次性提取该文件内所有枚举的完整枚举值列表。
4. 记录：
   - 枚举名称、限定名
   - 底层类型（对于 `enum class`，查找 `: uint8_t` 等显式指定）
   - 所有枚举值（名称 + 显式赋值 + 含义说明）
5. **防重复保护**：
   - 同一 file_path 在本 Step 内只读 1 次（即使包含多个枚举）。
   - 若 Read 失败，将该文件内所有枚举标记为 `evidence_level: "unknown"`，不重试。

### Step 5: 生成精细化 symbol-index.jsonl

将 Step 2 的精细化结果写入 symbol-index.jsonl，覆盖 Phase 2 的粗版。

确保以下字段已填充（而非 `null`）：
- `signature`：class 含继承关系、method 含完整参数签名
- `base_symbols`：所有直接基类
- `access_modifier`：class 成员必须有
- `is_virtual`、`is_static`、`is_const`：成员函数必须有
- `declaration_path`、`definition_path`：声明与实现分离时分别记录

## 输出文件

- `source-index/symbol-index.jsonl`（覆盖 Phase 2 粗版，精细化）
- `source-index/macro-index.jsonl`
- `source-index/enum-index.jsonl`

## 质量门槛

1. `symbol-index.jsonl` 中 `kind=class/struct` 的条目 90% 以上含 `base_symbols` 和 `signature`。
2. `symbol-index.jsonl` 中 `kind=method/function` 的条目 80% 以上含完整 `signature`。
3. `macro-index.jsonl` 不含 `*_EXPORT` 导出宏和 include guards。
4. `enum-index.jsonl` 中每个枚举含完整的 `values` 数组。
5. 三个 JSONL 文件每行可被 JSON parser 解析。
6. Phase 2 粗版中的符号 100% 在精细化版本中有对应条目。

## 并行化策略

按模块并行：
- 每个模块分配一个 Agent，负责该模块下所有符号的精细化。
- 最后合并 macro-index.jsonl 和 enum-index.jsonl（需跨模块去重）。
