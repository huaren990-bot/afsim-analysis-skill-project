---
name: requirement-mapping
description: 当用户需要把自有项目需求、规范文档、接口定义或现有源码与 AFSIM 功能能力进行对照，生成需求缺口、功能映射和候选 AFSIM 模块清单时，使用本 skill。
---



# AFSIM 需求映射 Skill

本 skill 负责把“用户想要什么”和“AFSIM 已经有什么”连接起来，为后续功能迁移和算法复用提供明确目标。对比自有仿真器内核的现有功能列表，输出标准化缺口规格，指导后续的代码迁移工作。本 skill 并不直接阅读源码，而是依赖上游 Agent 已经生成的结构化索引和自有内核的功能摘要（如果没有自有内核功能摘要可以忽略）。

## 输入

- 用户需求文档()。
- 自有项目源码或接口说明。
- AFSIM 架构报告和函数索引。
- 已有算法卡片。

## 执行步骤

1. 从需求文档中抽取功能点、性能约束、输入输出、场景条件和验收标准。
2. 从自有项目中识别已有能力、缺失能力和接口边界。
3. 将需求拆成原子能力，例如模型计算、状态更新、传感器观测、事件处理、结果输出。
4. 在 AFSIM 索引和算法卡片中查找候选能力。
5. 对每条需求给出状态：已满足、部分满足、缺失、未知。
6. 为缺失项推荐候选 AFSIM 模块和下一步分析任务。

## 输出

- `docs/requirements/requirement-gap-analysis.md`
- `docs/requirements/missing-features-spec.md`
- `docs/requirements/requirement-to-afsim-trace.md`

## 判断标准

- “已满足”：自有项目已有明确实现，且符合需求关键条件。
- “部分满足”：已有相近能力，但接口、精度、场景或约束不完整。
- “缺失”：未发现可用实现，需要新增或迁移。
- “未知”：缺少源码、需求或测试依据，不能确认。

## 质量要求

- 每条需求必须保留原文或来源。
- 每个状态判断必须给出证据。
- 不把 AFSIM 候选能力直接等同于可迁移能力，迁移可行性由 `afsim-migration-builder` 评估。


2. 产出 Skill：gap-analyzer — 需求缺口分析与映射
角色

gap-analyzer 基于人工确认后的需求规范文档（即经过勾选和简化的版本），将每条确认后的需求映射到 AFSIM 源码中的具体功能函数，并判断目标系统当前的能力状态，最终生成需求缺口报告和功能映射矩阵。
工作流程

    加载输入：

        读取人工确认后的需求规范文档（docs/requirements/requirement-spec-confirmed.md）

        加载 AFSIM 源码索引（function-index, symbol-index）

        加载目标系统功能索引（由人工或之前分析提供）

        加载 AFSIM 架构报告和算法卡片作为补充。

    解析确认后需求：

        提取所有被勾选为“必须”的需求条目。

        对于被简化的条目，使用精简后的描述；对于保持详细的，使用细化功能点。

    AFSIM 能力匹配：

        对于每一条细化需求，在 AFSIM 索引中通过语义搜索找到最相关的函数或类。

        评估匹配函数的接口、依赖、输入输出是否与需求吻合。

        记录候选函数的证据（路径、函数名、行号、功能摘要）。

    目标系统能力对比：

        在目标系统功能索引中搜索对应功能。

        判定覆盖度：

            ✅ 完全满足（功能完全匹配，接口兼容）

            ⚠️ 部分满足（有类似功能但需要修改接口或补充参数）

            ❌ 缺失（无相关实现）

            ❓ 无法判断（索引或描述不足，需人工补充）

    生成缺口与映射矩阵：

        对每个部分满足或缺失的需求，生成一个原子功能单元（FU），包含：

            FU ID，关联需求 ID

            功能描述（基于确认的需求描述）

            期望接口签名（输入、输出、类型）

            AFSIM 参考实现（源函数位置，若找到）

            建议迁移方式（直接适配/局部重写/Clean-room）

            优先级（沿用人工确认的优先级）

        生成需求追溯矩阵（REQ -> AFSIM 源 -> FU -> 目标系统状态）

        生成可视化关联图（Mermaid 流程图或矩阵表）

    输出文件：

        docs/requirements/requirement-gap-analysis.md — 完整缺口报告

        docs/requirements/function-mapping-matrix.md — 功能映射矩阵

        workspace/requirements/gap-specs.jsonl — 结构化缺口规格（供下游迁移 Skill 使用）

输出示例
json

// workspace/requirements/gap-specs.jsonl 中的一条记录
{
  "fu_id": "FU-003",
  "req_id": "REQ-001",
  "requirement_text": "六自由度刚体运动模型（四元数）",
  "afs_source": {
    "function_name": "integrate_step",
    "location": "src/kinematics/RigidBodyDynamics.cpp:45-89",
    "class_name": "RigidBodyDynamics"
  },
  "target_status": "缺失",
  "expected_signature": {
    "inputs": ["state: RigidBodyState", "forces: Wrench", "dt: double"],
    "outputs": ["new_state: RigidBodyState"]
  },
  "migration_suggestion": "直接适配（移除AFSIM日志，替换状态结构体）",
  "priority": "高"
}

工具列表

    read_file(path) — 读取确认需求规范、索引文件

    search_afs_functions(query, top_k) — 语义搜索 AFSIM 功能

    search_target_functions(query, top_k) — 搜索目标系统功能索引

    write_file(path, content) — 输出报告

    append_to_file(path, json_line) — 追加缺口规格 JSONL

校验 Skill

对应的检验 Skill 验证：

    所有确认后需求是否均已在矩阵中出现；

    每个缺口 FU 是否都有 AFSIM 证据或标注“未找到”；

    迁移建议与耦合评估是否合理（后续可由迁移 Agent 深度评估）。