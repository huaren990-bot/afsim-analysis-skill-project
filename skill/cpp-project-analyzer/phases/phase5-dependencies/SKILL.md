---
name: cpp-proj-dependencies
description: "Phase 5: 跨模块依赖关系分析 — 生成 dependency-index.jsonl（≥200条，覆盖6种relation）和 dependency-graph.md（含Mermaid图）。"
metadata:
  phase: 5
  requires-codegraph: true
  produces: dependency-index.jsonl, dependency-graph.md
---

# Phase 5: 跨模块依赖关系分析

## 目标

在前序阶段的文件/符号/函数索引基础上，系统性地提取和分类项目中所有的依赖关系：
- **build**：CMake target_link_libraries 依赖
- **inheritance**：类继承关系
- **composition**：成员变量组合关系（unique_ptr/shared_ptr/值类型成员）
- **call**：函数调用关系
- **include**：头文件包含关系
- **registration**：工厂注册、插件注册、事件订阅

本阶段输出是整个分析流水线中**交叉引用密度最高**的产物。

## 输入

- `project-boundary/project-boundary.json`（Phase 1 产出）
- `source-index/file-index.jsonl`（Phase 2 产出）
- `source-index/symbol-index.jsonl`（Phase 3 精细化版）
- `source-index/function-index.jsonl`（Phase 4 产出）
- `source-index/function-body-summary.jsonl`（Phase 4 产出）

## 执行步骤

### Step 0: 应用分析边界

依赖提取前必须读取 `project-boundary.json.analysis_boundaries`：

1. 将 `recommended_exclude_paths_for_architecture`、用户明确排除路径、第三方库目录、文档/资源目录加入排除集合。
2. `training`、`demo`、示例和教程目录不得进入架构级依赖、子系统依赖或最终 Mermaid 图，除非用户明确把它们纳入分析范围。
3. 若 dependency 候选的 `source` 或 `target` 位于排除集合，只能记录为 `out_of_scope_reference` notes，不写入核心 `dependency-index.jsonl`。
4. 在 `dependency-graph.md` 开头写明排除路径和原因，避免读者误以为这些路径“没有依赖”。

### Step 1: 提取 build 依赖

1. 扫描所有 `CMakeLists.txt` 文件。
2. 提取 `target_link_libraries` 声明。
3. 对每条 build 依赖，记录：
   - `source`：依赖发起方模块
   - `target`：被依赖模块
   - `relation`: `build`
   - `evidence`：CMakeLists.txt 中的具体语句

### Step 2: 提取 inheritance 依赖

1. 从 symbol-index.jsonl 中筛选 `kind=class/struct` 且 `base_symbols` 非空的条目。
2. 对每条继承关系，记录：
   - `source`：子类 qualified_name
   - `target`：基类 qualified_name
   - `relation`: `inheritance`
   - `evidence`：源码中的继承声明（如 `class X : public Y`）

### Step 3: 提取 composition 依赖（批量查询，禁止逐类）

**⚠️ 关键规则：按模块批量查询，禁止对每个类单独调用 codegraph_explore。**

1. **按模块批量查询成员变量**：
   ```
   # 每模块只问一次，涵盖模块内所有核心类
   codegraph_explore "<module_name> all classes member variables composition unique_ptr shared_ptr"
   ```
   同一模块只调用 1 次。若返回空或信息不足，**不要为单个类重试**，改为：
   - 复用 Phase 3 已读过的文件内容（symbol-index.jsonl 的 signature 字段通常包含成员变量信息）。
   - 或使用 `rg "(unique_ptr|shared_ptr|CloneablePtr|std::vector)" <module_dir>` 一次性批量 grep。

2. **识别以下模式的组合关系**（基于已获得的源码信息）：
   - `std::unique_ptr<T>` → 独占所有权
   - `std::shared_ptr<T>` → 共享所有权
   - `ut::CloneablePtr<T>` → 克隆指针（AFSIM 专用）
   - 值类型成员 → 强组合
   - 裸指针成员 → 弱组合（标记为 `strength: weak`）

3. 对每条组合关系，记录 `source`（持有者类）、`target`（被持有类）。

4. **防重复保护**：
   - 同一模块的 codegraph_explore 仅调用 1 次。
   - 同一 grep 模式在同一目录仅执行 1 次。
   - 若 codegraph_explore 失败，降级到 grep + 已读文件内容，不重试 codegraph。

### Step 4: 提取 call 依赖

1. 从 function-index.jsonl 中提取每个 Method-level 条目的 `calls` 数组。
2. 将调用关系展开为 dependency 条目：
   - `source`：调用方 qualified_name
   - `target`：被调用方 qualified_name
   - `relation`: `call`
3. 从 function-body-summary.jsonl 中提取 `calls_summary`，补充额外调用关系。

### Step 5: 提取 include 依赖

1. 从 file-index.jsonl 中提取所有 `includes` 数组。
2. 将 include 关系展开为模块间依赖：
   - `source`：包含方文件路径
   - `target`：被包含文件路径
   - `relation`: `include`

### Step 6: 提取 registration 依赖（批量 grep 优先）

**⚠️ 关键规则：先用 shell 批量 grep，不足时再用一次 codegraph_explore 补充。禁止对每种注册模式反复查询。**

1. **优先使用 shell 批量 grep**（一次命令覆盖所有注册模式）：
   ```bash
   rg "(AddComponent|RegisterComponent|ComponentFactory|AddExtension|RegisterExtension|Subscribe|ListenTo|EventPipe|PluginManager::Load)" <extract_root> -n --include='*.cpp' --include='*.hpp'
   ```

2. **仅当 grep 结果不足时**，使用**单次** codegraph_explore 补充：
   ```
   codegraph_explore "<module_name> factory registration plugin component event subscription"
   ```
   整个项目只调用 1 次，不可对每种注册模式分别查询。

3. **防重复保护**：
   - grep 命令整个 Step 只执行 1 次。
   - codegraph_explore 整个 Step 最多 1 次。
   - 若两者都返回空，将 registration 关系标记为 `evidence_level: "unknown"`，不重试。

### Step 7: 生成 dependency-graph.md

1. 使用 Mermaid 语法绘制构建依赖图。
2. 使用 Mermaid 语法绘制架构级依赖图（继承+组合+调用）。
3. 使用 Mermaid 语法绘制子系统间依赖图。
4. 在同一文件中用表格列出所有高价值依赖（按 `strength` 排序）。
5. 如果依赖数量过多，不得只写“Top 20”并结束；必须：
   - 说明筛选标准（如按 relation/strength/跨模块程度抽样）。
   - 列出未展示模块和未展示原因。
   - 给出完整依赖清单位置：`source-index/dependency-index.jsonl`，以及最终报告中的 `docs/architecture/module-dependency.md` 链接。
6. 对零边或孤立模块，单独列出“无核心依赖记录/被边界排除/索引不足”的原因；不得让图中没有边的模块与实际依赖状态混淆。
7. Mermaid 图必须能渲染：节点 ID 使用安全标识，中文和路径放在 label 中；大图按系统/子系统拆分，避免类继承图缩成不可读小图。

## 输出文件

- `source-index/dependency-index.jsonl`
- `docs/architecture/dependency-graph.md`

推荐使用项目脚本生成 Phase5 产物：

```bash
python3 tools/indexers/phase5_build_dependencies.py --root <project_root>
```

该脚本会读取 Phase1 边界与 Phase2-4 索引，生成 `dependency-index.jsonl`、`phase5-dependency-summary.json`、`docs/architecture/dependency-graph.md`、`docs/architecture/module-dependency.md` 与 `docs/verification/phase5-verify-report.md`。脚本必须保留 `raw` 证据字段和 `dependency_id`，确保 Mermaid 摘要边可回溯到 JSONL 全量清单。

## 质量门槛

1. **条目数不少于 200**。
2. **覆盖至少 6 种 relation**：`build`、`inheritance`、`composition`、`include`、`call`、`registration`。
3. 每种 relation 的条目数不少于 5。
4. `strength` 字段必须填写（`strong`/`medium`/`weak`）。
5. dependency-graph.md 中的每一条 Mermaid 边可追溯到 dependency-index.jsonl 中的条目。
6. 每行可被 JSON parser 解析。
7. 核心依赖不得包含 Phase 1 已排除路径（如 training/demo/docs/resources），除非用户显式纳入。
8. dependency-graph.md 必须说明筛选/拆图策略、完整依赖清单位置、孤立模块原因，并链接 `docs/architecture/module-dependency.md`。

## 依赖强度判断标准

| 强度 | 含义 | 典型 relation |
|------|------|-------------|
| **strong** | 缺少则编译失败 | build, inheritance, include, 值类型 composition |
| **medium** | 运行时通常需要，有默认/null 替代 | 指针 composition, call（虚函数调用） |
| **weak** | 松耦合，特定场景使用 | registration, configuration, test |
