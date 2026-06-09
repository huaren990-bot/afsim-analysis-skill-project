# AFSIM Analysis Skill Project

本项目用于构建一套面向 **AFSIM 的多 agent 协作体系**。

目标是能通过该项目实现快速完成对 AFSIM 的**认知学习**、**源码索引**、**架构理解**、**算法提取**、**需求映射**和**功能迁移**，并最终生成可以快速用在自有项目中的算法说明、接口规范、代码原型和测试计划。

将**知识提取 -> 需求映射 -> 代码迁移**路线落成可执行、可扩展、可追溯的目录结构。

以下方案从**架构设计、Agent 分工、数据流、文档与规范**四个层面给出可落地的路线图。

---

## 一、总体思路：以“知识提取→需求映射→代码迁移”为主干

整个项目可以分为 7 个阶段，每个阶段都有对应的 Agent 和输出文档：

1. **源码索引与静态分析准备**

2. **架构与功能提取（理解 AFSIM）**：从目录、模块、类、函数、调用链、数据流和仿真生命周期建立整体认知；通过源码索引和架构报告找到 AFSIM 中与目标需求相关的模块和实现。

3. **数学公式与算法解析**：将源码中的数学公式、数值计算、模型逻辑和控制流程转化为算法卡片、伪代码和接口说明。

4. **需求分析与功能缺口推断**：把用户需求或自有项目源码作为基准，输出缺口分析、迁移方案、适配接口和验证计划。

5. **AFSIM 源码定位与适配方案生成**

6. **代码迁移与集成到自有内核**

7. **验证、文档生成与闭环记录**：每次分析都沉淀为知识库，后续任务复用已有索引、报告和决策记录。

---

## 二、Agent 体系设计（1个总体Agent + 5 个专职 Agent）

基于大模型（如 GPT-4/Claude 3.5 级别）搭建 Agent，每个 Agent 有明确的角色、输入、输出和可调用的工具。

| Agent 名称                                | 作用                                                   | 主要产物                                 |
| --------------------------------------- | ---------------------------------------------------- | ------------------------------------ |
| `afsim-analyst`                         | 总控入口，判断任务类型并协调其他 skill                               | 阶段计划、路由决策、综合报告                       |
| `afsim-source-cognition`(源码分析 Agent)    | 快速学习 AFSIM 源码，总结架构，提取函数、类、数据流                        | 源码索引、架构报告、模块依赖                       |
| `afsim-algorithm-extractor`(数学解析 Agent) | 识别并解释源码中的算法、公式、变量映射，转化为标准数学表示和伪代码                    | 算法卡片、伪代码、接口规格                        |
| `afsim-requirement-mapper`(需求分析 Agent)  | 阅读规范需求文档，推断自有仿真器缺少的功能，生成待补充功能列表                      | 需求缺口报告、功能映射矩阵                        |
| `afsim-migration-builder`(代码迁移 Agent)   | 在 AFSIM 源码中定位所需功能，进行代码切片、简化、适配，生成迁移方案、适配接口、代码原型和测试计划 | 迁移记录、适配方案、测试计划                       |
| `afsim-knowledge-curator`(知识记录 Agent)   | 整理知识库、追溯矩阵、决策记录和后续任务，全程记录每一步的输入、思考链、决策、输出，生成阶段性文档    | 知识地图、追溯矩阵、过程记录、文档模板、Markdown 生成、版本快照 |

---

## 三、分阶段实施步骤与规范

### 项目结构

```text
afsim-analysis-skill-project/
├── README.md
├── skill/
│   ├── afsim-analyst/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── baseline-workflow.md
│   │   │   ├── output-contracts.md
│   │   │   ├── skill-routing.md
│   │   │   └── traceability-rules.md
│   │   ├── scripts/
│   │   └── assets/
│   ├── afsim-source-cognition/
│   │   └── SKILL.md
│   ├── afsim-algorithm-extractor/
│   │   └── SKILL.md
│   ├── afsim-requirement-mapper/
│   │   └── SKILL.md
│   ├── afsim-migration-builder/
│   │   └── SKILL.md
│   └── afsim-knowledge-curator/
│       └── SKILL.md
├── docs/
│   ├── architecture/   # 架构总结、API说明
│   ├── algorithms/
│   ├── requirements/
│   ├── migration/
│   ├── records/
│   └── templates/
│       ├── architecture-report.md
│       ├── algorithm-card.md
│       ├── migration-record.md
│       └── requirement-gap.md
├── workspace/
│   ├── source-index/    # 索引说明
│   ├── analysis-cache/
│   ├── extracted-algorithms/
│   └── own-kernel-adapters/
├── tools/
│   ├── prompts/
│   ├── indexers/
│   ├── validators/
│   └── orchestrators/
├── examples/
│   ├── requests/
│   └── outputs/
└── tests/
```

### 阶段 1：AFSIM 源码结构化分析

**Agent：`afsim-source-cognition`(源码分析 Agent)**

**输入：** AFSIM 源码目录

**过程：**

1. **代码切分**：用 AST 工具将源码切分为函数级、类级片段，保留文件路径和行号。

2. **摘要生成**：让大模型为每个代码单元生成功能摘要、输入输出说明、依赖关系。

3. **架构归纳**：由大模型阅读主要模块的摘要，绘制组件图、数据流图（可用 Mermaid）。

4. **人工校验**：开发人员校对架构图与关键模块理解，修正后存入 `/docs/architecture/`。

**输出：**

- ```
  workspace/source-index/
  ├── file-index.jsonl        # 文件级索引
  ├── symbol-index.jsonl      # 符号索引（类、枚举、全局变量等）
  ├── function-index.jsonl    # 函数/方法索引
  └── dependency-index.jsonl  # 模块依赖关系索引
  
  docs/architecture/
  ├── afsim-architecture.md   # 总体架构文档（含 Mermaid 图）
  └── module-dependency.md    # 模块依赖关系
  ```

**记录要求：** 文档 Agent 记录每个总结所依据的代码片段、模型思考过程（通过 Chain-of-Thought 提示生成）。

### 2. 算法与功能提取

使用 `afsim-algorithm-extractor` 对关键模块进行算法抽取。重点区分：

- 数学和算法核心
- AFSIM 框架封装
- 配置、场景和运行时依赖
- 可直接迁移部分
- 应重新实现部分

输出保存到 `docs/algorithms/` 和 `workspace/extracted-algorithms/`。

### 3. 自有项目需求映射

使用 `afsim-requirement-mapper` 读取自有项目需求文档、接口定义或源码，形成需求到 AFSIM 能力的映射。每条需求分类为：

- 已满足
- 部分满足
- 缺失
- 未知

输出保存到 `docs/requirements/`。

### 4. 功能迁移与适配生成

使用 `afsim-migration-builder` 选择可迁移算法和功能，生成：

- 候选 AFSIM 源码位置
- 选择理由
- 耦合度评估
- 接口适配方案
- 许可证和版权风险
- 测试计划
- 必要时生成代码原型

输出保存到 `docs/migration/` 和 `workspace/own-kernel-adapters/`。

### 5. 知识沉淀

使用 `afsim-knowledge-curator` 汇总每轮分析结果，更新：

- `docs/records/`
- `docs/architecture/knowledge-map.md`
- `docs/requirements/requirement-to-afsim-trace.md`
- `docs/migration/migration-summary.md`

## 目录职责

`skill/` 保存可被大模型直接使用的 skill。每个 skill 只放执行规则和必要引用，保持精简。

`docs/` 保存人工可读、可审查的分析结果。架构、算法、需求、迁移和过程记录分开，方便长期维护。

`workspace/` 保存机器生成或中间产物，例如源码索引、分析缓存、算法切片和适配草稿。

`tools/` 保存后续可实现的索引器、验证器、编排脚本和 prompt 模板。

`examples/` 保存典型请求和标准输出样例，用于检验 skill 是否稳定。

`tests/` 保存脚本测试、结构检查和提取算法的最小验证用例。

## 输出规范

所有正式输出都应满足以下要求：

1. 结论必须有证据来源，例如源码路径、符号名、行号、需求编号或用户文档位置。
2. 算法提取必须包含输入、输出、状态依赖、数学形式、伪代码、变量映射和验证计划。
3. 迁移方案必须说明为什么选择该源码片段，以及哪些依赖需要保留、替换或删除。
4. 生成代码前必须明确目标项目接口、单位、生命周期、错误处理和测试策略。
5. 许可证不明确时，只生成 clean-room 风格的算法规格和重写建议。
6. 文档记录可审查的依据、假设、决策和结论，不记录隐藏推理过程。

## 推荐落地顺序

1. 先完善 `tools/indexers/`，实现 C/C++ 源码扫描和 JSONL 索引输出。
2. 用 `afsim-source-cognition` 生成第一版 AFSIM 架构报告。
3. 选择一个小功能，用 `afsim-algorithm-extractor` 生成算法卡片。
4. 输入一个自有项目需求，用 `afsim-requirement-mapper` 做缺口分析。
5. 用 `afsim-migration-builder` 生成迁移方案和最小代码原型。
6. 用 `afsim-knowledge-curator` 更新追溯矩阵和知识地图。

## 未来扩展

- 增加 tree-sitter 或 clang AST 索引器。
- 增加公式热点检测脚本。
- 增加报告证据校验器。
- 增加从算法卡片生成 C++/Python 原型的脚本。
- 增加针对自有项目构建系统的迁移适配模板。
