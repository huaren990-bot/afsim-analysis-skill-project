---
name: requirement-spec-generator
description: 本 skill 负责将模糊的功能需求文档转化为一份高度结构化、仅需人工勾选与简单选项的待确认需求规范文档。它结合已有 AFSIM 认知（索引、架构、算法卡片）来细化功能点，并为每一条细化需求提供“是否必需”“是否简化”“优先级”等选项，人工只需做选择题，大幅降低需求澄清成本。
---

# 需求规范生成 Skill

## 执行步骤

0. 预处理：
  - 确认本次需求编号、用户提供的功能需求文档，若不明确则人工确认。
  - 确认目标系统功能索引路径，若不明确则人工确认。
  - 确认 AFSIM 源码功能索引路径，若不明确则人工确认。

1. 加载上下文：
  - 读取 AFSIM 架构报告（docs/architecture/afsim-architecture.md）
  - 读取算法卡片概览（docs/algorithms/CompendiumofAlgorithms.md）
  - 加载 AFSIM 源码功能索引摘要（workspace/source-index/function-index.jsonl 中高等级函数）
  - 若已有目标系统功能索引，也一并加载。

2. 解析用户模糊的功能需求文档：
  - 读取用户提供的功能需求文档（不知道是哪个找人工确认）
  - 提取文档结构和关键领域词
  - 解析用户自然语言，将模糊表述拆解为可验证的功能陈述。

3. 将需求拆分为算法流水线
  1. AFSIM 能力匹配：对于每一条细化需求，在 AFSIM 索引中通过语义搜索找到最相关的函数或类。
    - 若找到匹配：评估匹配函数的接口、依赖、输入输出是否与需求吻合。
    - 记录候选函数的证据（路径、函数名、行号、功能摘要）。
    - **若未找到匹配**：标记为 🆕 AFSIM 无参考实现，该需求的算法流程需从领域文献或算法教材中寻找设计依据，不可依赖 AFSIM 源码。

  2. 目标系统能力对比：在目标系统功能索引中搜索对应功能。
    - 判定覆盖度：
        - ✅ 完全满足（功能完全匹配，接口兼容）
        - ⚠️ 部分满足（有类似功能但需要修改接口或补充参数）
        - ❌ 缺失（无相关实现，但 AFSIM 有参考实现）
        - 🆕 缺失（AFSIM无参考）（无相关实现，且 AFSIM 中也无对应功能）
        - ❓ 无法判断（索引或描述不足，需人工补充）
    - 判定非功能需求：
        - 多线程支持：根据算法复杂度、实时性要求和目标系统架构评估是否需要多线程支持。
        - 性能要求：评估算法的时间复杂度和性能需求，判断是否需要优化或并行化。
        - 可移植性：评估是否依赖特定平台或库，是否需要适配层。
        - 其他非功能需求：如内存限制、性能要求等。
  
  3. 为除了”✅ 完全满足”之外的需求设计算法简化方案，生成结构化需求草稿，将所有的Y/N选项留给人工确认。

4. 等待人工确认：
  - 将生成的结构化需求草稿（docs/requirements/<requirement_index>/1_<requirement_index>-requirement-<name>.md）交给人工确认。
  - 人工确认内容包括：
    - 是否需要简化
    - 是否选择简化方案
    - 优先级排序
    - 非功能需求的确认
    - 其他修改要求
  - 人工确认无需再修改后，生成最终的需求规范文档（docs/requirements/<requirement_index>/2_<requirement_index>-requirement-<name>.md），最终的需求规范文档中只保留人工选择的方案即可。
    
4. 过程留痕：把每一步的决策依据和执行计划生成文档进行记录归档，放在目录docs/records里面，以便人工追溯。

## 输入

- AFSIM：
  - 架构文档（docs/algorithms/*.md）
  - 算法文档（docs/algorithms/*.md）
  - 系统索引（workspace/source-index/*.jsonl）
- 自有系统：（如果有的话，没有按照空系统处理）
  - 架构文档（docs/algorithms/*.md）
  - 算法文档（docs/algorithms/*.md）
  - 系统索引（workspace/source-index/*.jsonl）
- 用户功能需求文档（docs/requirements/<requirement_index>/0_<name>.md）
- 其他网络文献

## 输出

### `docs/requirements/<requirement_index>/1_<requirement_index>-requirement-<name>.md` / `docs/requirements/<requirement_index>/2_<requirement_index>-requirement-<name>.md`

需求规范文档。要求和格式应当严格遵循模板`skill/requirement-mapper/template_list/template_requirement-specification.md`
