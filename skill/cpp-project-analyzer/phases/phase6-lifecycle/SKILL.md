---
name: cpp-proj-lifecycle
description: Phase 6: 生命周期与数据流分析 — 追踪仿真/应用生命周期、数据流路径、配置流路径、扩展点识别。产出 lifecycle.md、dataflow.md、extension-points.md。
metadata:
  phase: 6
  requires-codegraph: true
  produces: lifecycle.md, dataflow.md, extension-points.md
---

# Phase 6: 生命周期与数据流分析

## 目标

在前序阶段索引基础上，构建项目的**动态行为视图**：
- 应用/仿真生命周期（从启动到关闭的全流程）
- 数据流路径（数据在模块间如何流转）
- 配置流路径（配置从文件到运行时的加载链路）
- 扩展点机制（框架在哪些位置允许外部扩展）

## 输入

- `project-boundary/project-boundary.json`（Phase 1 产出）
- `source-index/file-index.jsonl`（Phase 2 产出）
- `source-index/symbol-index.jsonl`（Phase 3 精细化版）
- `source-index/function-index.jsonl`（Phase 4 产出）
- `source-index/function-body-summary.jsonl`（Phase 4 产出）
- `source-index/dependency-index.jsonl`（Phase 5 产出）

## 执行步骤

### Step 1: 生命周期追踪

1. **定位程序入口点**：
   - 优先从 function-index.jsonl 中筛选 `lifecycle_role=entry` 的方法（**无需调用 codegraph**）。
   - 仅当 function-index 中无 entry 标记时，使用 codegraph_explore 追溯（**整个 Phase 仅 1 次**）：
     ```
     codegraph_explore "main function entry point - what does it call, how does it initialize"
     ```
   - 若 codegraph_explore 返回空或错误，**不重试**，改为：
     - `rg "int\s+main\s*\(" <extract_root> --include='*.cpp' -n` 一次性找到 main 函数位置。
     - 读取该 main 所在文件 1 次，从函数体推断调用链。

2. **划分生命周期阶段**。标准阶段：
   | 阶段 | lifecycle_role | 说明 |
   |------|---------------|------|
   | entry | `entry` | 程序入口、命令行解析、版本检查 |
   | scenario_load | `scenario_load` | 场景文件解析、配置加载、环境初始化 |
   | object_create | `object_create` | 对象创建、注册、连接、初始化 |
   | simulation_loop | `simulation_loop` | 主循环、时间推进、帧步进 |
   | model_update | `model_update` | 物理模型更新、状态更新 |
   | event_handling | `event_handling` | 事件分发、响应 |
   | output | `output` | 结果写入、日志、可视化 |
   | shutdown | `shutdown` | 资源释放、清理 |

3. **对每个阶段**，**优先从 function-index.jsonl 中筛选**对应 `lifecycle_role` 的方法，构建调用序列。
   - **禁止**对每个阶段都调用 codegraph_explore — 这会产生重复调用。
   - 仅当 function-index 信息不足以构建某阶段的调用序列时，才针对该阶段发起 1 次补充查询（且必须使用与 Step 1.1 不同的查询词）。

4. **绘制生命周期 Mermaid 图**：用 flowchart 展示阶段流转和关键函数的调用关系。

5. **生成生命周期关联表**：每个阶段列出入口函数、关键类、配置来源、主要状态对象、证据位置。
6. **生成可验证调用链**：调用链每一步必须包含：
   - 调用方函数与位置（`file:line` 或 function-index 唯一键）。
   - 被调用方函数与位置。
   - 调用关系证据（来自 `calls`、dependency `relation=call`、或源码行）。
   - 中文说明：这一步在生命周期中完成什么状态变化。
   不能只写 `A() → B()`；位置错误或证据缺失时必须标记 `inferred` 并说明原因。

### Step 2: 数据流分析

1. **识别关键数据对象**：
   - 从 symbol-index.jsonl 中筛选核心数据类（如 Platform、Track、Event、Message、Signature）。
   - 从 dependency-index.jsonl 中提取这些数据对象的生产者和消费者。

2. **追踪数据流路径**（⚠️ **禁止逐数据类型调用 codegraph_explore**）：
   - **优先**从已有的 dependency-index.jsonl + function-index.jsonl 推断数据流（`calls` 字段 + `reads`/`writes` 字段 + composition 关系），**无需发起新工具调用**。
   - 仅当索引信息不足以识别 ≥5 个数据对象时，使用**单次**批量查询：
     ```
     codegraph_explore "all data objects (Platform Track Event Message Signature) flow creation consumption"
     ```
     整个 Phase 最多 1 次，不可对每个数据类型分别查询。
   - 若 codegraph_explore 返回空或错误，**不重试**，直接基于索引生成数据流分析，不足的标记 `evidence_level: "inferred"`。
   - 按 `state_source -> state_owner -> update_function -> consumers -> outputs` 模式描述。

3. **绘制数据流 Mermaid 图**：用 flowchart/graph 展示数据在各模块/子系统间的流转。
4. **建立图表映射表**：每个关键数据对象必须映射到 Mermaid 节点 ID，并说明该节点代表的源码对象/类/文件。
5. **解释每条数据流链路**：每条路径必须有一段中文说明，按 `state_source -> state_owner -> update_function -> consumers -> outputs` 展开，说明数据从哪里产生、由谁持有、在哪个函数更新、被谁消费、最终输出到哪里。不能只给一行箭头。

### Step 3: 配置流分析（批量 grep，不重复查询）

1. **定位配置入口**（使用**单次**批量 grep）：
   ```bash
   rg "(ProcessInput|LoadConfig|ParseScenario|ReadXML|UtInput|json::parse|tinyxml)" <extract_root> --include='*.cpp' --include='*.hpp' -n
   ```
   整个 Step 仅执行 1 次 grep，不可对每个模式分别查询。

2. **追踪配置加载链**：
   - 基于 grep 结果 + function-index.jsonl 的 `calls` 字段，按 `config_file -> parser -> factory_or_registry -> object_property -> runtime_behavior` 模式描述。
   - 不发起新的 codegraph 调用。

3. **绘制配置流 Mermaid 图**。
4. 在配置流章节开头加入中文说明，解释配置流分析的用途：帮助读者理解场景/配置文件如何转化为运行时对象属性、工厂注册和仿真行为。每条配置流必须列出配置来源、解析函数、目标对象、影响的运行时行为和证据位置。

### Step 4: 扩展点识别（基于已有索引）

扩展点章节开头必须说明本分析的作用：识别插件、工厂、注册表、事件订阅、策略/Policy 等扩展边界，帮助判断外部能力如何接入系统、哪些接口可稳定复用、哪些注册路径会改变运行时行为。

1. **从 dependency-index.jsonl 中筛选 `relation=registration` 的条目**（无需调用工具）。

2. **从源码中识别扩展机制**（使用**单次**批量 grep）：
   ```bash
   rg "(ComponentFactory|ObjectFactory|PluginManager|LoadLibrary|Extension|ExtensionPoint|Strategy|Policy|Observer|EventPipe|Subscribe)" <extract_root> --include='*.hpp' --include='*.cpp' -n
   ```
   整个 Step 仅执行 1 次 grep。

3. **对每个扩展点**，记录：
   - 扩展机制名称
   - 关键接口/基类
   - 注册位置
   - 使用示例（从 grep 结果中匹配至少一个注册实例）
   - 用途说明：该扩展点让外部代码能扩展什么能力、通常由谁调用、运行时影响是什么。

4. **防重复保护**：
   - 若某扩展机制在 grep 中无匹配，标记为 `evidence_level: "unknown"`，不重试也不发起 codegraph_explore。
   - 不针对单个扩展点单独发起 grep 或 codegraph 查询。

## 输出文件

- `docs/architecture/lifecycle.md`
- `docs/architecture/dataflow.md`
- `docs/architecture/extension-points.md`

## lifecycle.md 结构

```markdown
# 应用/仿真生命周期分析

## 生命周期总览

```mermaid
flowchart TD
  Start["按实际生命周期阶段填写"]
```

## 各阶段详情

### 阶段 1: xxx ({lifecycle_role})

| 属性 | 值 |
|------|-----|
| 入口函数 | xxx |
| 关键类 | xxx, yyy |
| 配置来源 | xxx |
| 主要状态对象 | xxx |
| 证据位置 | file:line |

**调用链**：
1. `xxx()` (`file:line`) → `yyy()` (`file:line`)：中文说明调用目的；证据：function-index calls / dependency-index call / 源码行。

### 阶段 2: xxx

继续按同一结构完整列出后续生命周期阶段。
```

## dataflow.md 结构

```markdown
# 数据流分析

## 关键数据对象

| 数据对象 | 类型 | 生产者 | 消费者 | 生命周期 |
|----------|------|--------|--------|----------|

## 数据流路径

### 数据流 1: xxx

```mermaid
flowchart TD
  DataSource["按实际数据源填写"]
```

**节点映射**：

| Mermaid 节点 | 数据对象 | 中文说明 | 源码证据 |
|--------------|----------|----------|----------|

**链路说明**：state_source → state_owner → update_function → consumers → outputs

**逐步解释**：
1. `source` 产生数据：按源码证据说明来源。
2. `owner` 持有/缓存数据：按源码证据说明持有者。
3. `update_function` 更新数据：按 function-index 说明更新函数。
4. `consumers` 消费数据：按 dependency/function 索引说明消费者。
5. `outputs` 输出或影响行为：说明输出位置或运行时影响。
```

## 质量门槛

1. lifecycle.md 覆盖所有 8 个生命周期阶段，每个阶段至少含 3 个关键函数。
2. dataflow.md 至少识别 5 个关键数据对象，每个有完整的流路径描述。
3. extension-points.md 至少识别 3 种扩展机制，每种有源码实例。
4. 所有 Mermaid 图中的节点可追溯到 function-index.jsonl 或 symbol-index.jsonl。
5. 无法确认的阶段/数据流/扩展点标记为 `unknown` 并说明原因。
6. lifecycle.md 的调用链必须有调用方/被调用方位置、证据来源和中文说明。
7. dataflow.md 的关键数据对象必须与 Mermaid 节点一一映射，每条数据流链路必须有逐步解释。
8. 配置流和扩展点章节必须包含用途说明，不能只给表格。
