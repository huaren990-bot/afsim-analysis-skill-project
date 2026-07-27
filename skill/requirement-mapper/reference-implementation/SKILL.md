---
name: requirement-reference-implementation
description: 针对一个已明确的功能需求，在 AFSIM 架构报告、源码索引、算法卡片、真实源码、官方文档和演示场景中检索并验证参考实现，输出功能分解、端到端调用链、配置/状态/事件/数据流、算法与源码证据以及覆盖结论。用于“AFSIM 是否有某功能”“定位某能力如何实现”“生成 AFSIM 参考程序设计”；不用于目标系统缺口判断或直接迁移代码。
---

# AFSIM 参考实现分析

每次只分析用户指定的需求范围。不得读取其他需求的结论作为本需求事实；可复用公共 AFSIM 架构与源码索引。

## 输入

- 明确的需求描述和稳定需求 ID。
- `docs/architecture/*.md`
- `workspace/source-index/*.jsonl`
- `docs/algorithms/*.md`
- AFSIM 真实源码
- 可选：AFSIM 官方文档与演示场景

## 工作流

### 1. 固定检索问题

把需求拆成可验证的功能步骤，明确每步的输入、输出、状态、触发条件和完成条件。记录检索词，包括领域术语、可能的类/函数名、配置关键字和事件名。

### 2. 多入口检索

按以下顺序建立候选：

1. 从 `business-logic-readiness.md`、`x-level-capabilities.md` 和模块报告定位业务域。
2. 从 function、symbol、dependency、file 索引查找函数、类型和调用关系。
3. 从 Compendium 查找算法，再打开命中的完整算法卡片。
4. 从官方文档与 demo 查找配置方法、场景入口和预期行为。

索引和 Compendium 只产生候选，不是最终证据。

### 3. 逐候选源码验证

对每个候选打开真实源码，核对：

- `candidate_id`、`qualified_name`、模块和 `path:line_start-line_end`。
- 输入、输出、读写状态、副作用、错误处理和生命周期。
- 直接调用者、被调函数、继承/组合关系和注册入口。
- 配置项如何进入对象，事件如何触发，结果如何输出。
- 与需求步骤的语义差异。

记录 `verified`、`rejected` 或 `unknown`，并写明原因。不得命中第一个相似名称后停止；至少检查同模块同名/近义候选和关键调用链。

### 4. 重建端到端功能

按“配置/场景输入 → 对象创建与初始化 → 仿真循环/事件 → 状态更新 → 输出”组织参考实现。对每一步给出：

- 业务职责。
- 类与方法。
- 数据、单位和坐标系。
- 前后调用关系。
- 源码证据。
- 与需求的覆盖差异。

数学算法引用已验证算法卡片；卡片缺失或与源码不一致时，回到源码并标记算法提取缺口。

### 5. 给出覆盖结论

使用以下机器可判定状态：

- `full`：需求语义与端到端实现均有源码证据。
- `partial`：存在可复用机制，但接口、范围或行为不完整。
- `none`：在记录的检索边界内未找到参考实现。
- `unknown`：源码/索引/文档不足，无法判断。

`none` 只能表示“在已记录范围内未找到”，不能证明整个 AFSIM 永远不存在。

### 6. 输出

生成：

- `docs/requirements/<req-id>/<req-id>-afsim-reference.md`
- `workspace/requirements/<req-id>/<req-id>-afsim-evidence.jsonl`
- `docs/records/<date>-reference-implementation-<req-id>.md`

证据 JSONL 每行对应一个需求步骤与候选实现，至少包含：

```json
{
  "req_step_id": "REQ-002-FUNC-01",
  "coverage": "partial",
  "candidate_status": "verified",
  "candidate_id": "stable-id",
  "qualified_name": "Namespace::Class::Method#digest",
  "source": {"path": "relative/path.cpp", "line_start": 10, "line_end": 40},
  "role": "simulation_update",
  "differences": ["缺少目标需求中的风场修正"],
  "evidence_level": "source-cited"
}
```

人读文档至少包含需求分解、证据摘要、端到端流程图、输入输出/配置/状态/依赖、覆盖结论、差异和未决问题。

## 质量门禁

- 每个覆盖结论至少有一条源码证据或明确的未命中检索范围。
- 所有源码路径和行号可在当前工作区复核。
- 同名候选已消歧。
- 配置、初始化、更新和输出链路没有用“内部自动完成”等表述跳过。
- 公式、单位和坐标系只在证据支持时断言。
- 不记录隐藏推理过程。
