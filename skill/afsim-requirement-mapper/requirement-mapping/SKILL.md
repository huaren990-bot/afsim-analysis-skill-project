---
name: requirement-mapping
description: 当用户需要把自有项目需求、规范文档、接口定义或现有源码与 AFSIM 功能能力进行对照，生成需求缺口、功能映射和候选 AFSIM 模块清单时，使用本 skill。
---



# AFSIM 需求映射 Skill

本 skill 负责把“用户想要什么”和“AFSIM 已经有什么”连接起来，为后续功能迁移和算法复用提供明确目标。基于人工确认后的需求规范文档（即经过勾选和简化的版本），将每条确认后的需求映射到 AFSIM 源码中的具体功能函数，并判断目标系统当前的能力状态，最终生成需求缺口报告和功能映射矩阵，指导后续的代码迁移工作。本 skill 并不直接阅读源码，而是依赖上游 Agent 已经生成的结构化索引和自有内核的功能摘要（如果没有自有内核功能摘要可以忽略）。

## 输入

- 用户确认的需求规范文档，位置在`docs/requirements/structured_requirement_confirm/`，不明确需要找人工确认。
- 自有项目源码或接口说明。(如果没有自有项目，可以按照空系统处理，即所有需求都视为缺失)
- AFSIM 架构报告和函数索引。
- 已有算法卡片。

## 执行步骤

1. 加载输入：

- 读取人工确认后的需求规范文档（docs/requirements/requirement-spec-confirmed.md）
- 加载 AFSIM 源码索引（function-index, symbol-index）
- 加载目标系统功能索引（由人工或之前分析提供）
- 加载 AFSIM 架构报告和算法卡片作为补充

2. 解析确认后需求：

- 提取所有被需要简化和不需要简化的需求条目。
- 对于被简化的条目，使用精简后的描述；对于保持详细的，使用细化功能点。

3. 对**每个**部分满足或缺失的需求，生成一个原子功能单元（FU），例如模型计算、状态更新、传感器观测、事件处理、结果输出包含：
    - FU ID，关联需求 ID
    - 功能描述（基于确认的需求描述）
    - 期望接口签名（输入、输出、类型）
    - AFSIM 参考实现（源函数位置，若找到）
    - 建议迁移方式（直接适配/局部重写/Clean-room）
    - 优先级（沿用人工确认的优先级）

5. 对**每条需求**给出状态：已满足、部分满足、缺失、未知。

6. 生成需求追溯矩阵（REQ -> AFSIM 源 -> FU）和功能映射矩阵（需求 -> AFSIM 功能 -> 目标系统功能），并输出缺口分析报告。

7. 过程留痕：把每一步的决策依据和执行计划生成文档进行记录归档，放在目录docs/records里面，以便人工追溯。

## 输出

- `docs/requirements/confirmed_requirement_doc/requirement-gap-analysis.md` — 完整缺口报告
- `docs/requirements/confirmed_requirement_doc/function-mapping-matrix.md` — 功能映射矩阵
- `docs/requirements/confirmed_requirement_doc/requirement-to-afsim-trace.md` — 需求到AFSIM的追溯矩阵
- `workspace/requirements/gap-specs.jsonl` — 结构化缺口规格（供下游迁移 Skill 使用）

## 质量要求

- 每条需求必须保留原文或来源。
- 每个状态判断必须给出证据。
- 不把 AFSIM 候选能力直接等同于可迁移能力，迁移可行性由 `afsim-migration-builder` 评估。





