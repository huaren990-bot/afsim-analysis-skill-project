---
name: requirement-spec-generator
description: 本 skill 负责将模糊的功能需求文档转化为一份高度结构化、仅需人工勾选与简单选项的待确认需求规范文档。它结合已有 AFSIM 认知（索引、架构、算法卡片）来细化功能点，并为每一条细化需求提供“是否必需”“是否简化”“优先级”等选项，人工只需做选择题，大幅降低需求澄清成本。
---

# 需求规范生成 Skill

## 执行步骤

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
    - 评估匹配函数的接口、依赖、输入输出是否与需求吻合。
    - 记录候选函数的证据（路径、函数名、行号、功能摘要）。

  2. 目标系统能力对比：在目标系统功能索引中搜索对应功能。
    - 判定覆盖度：
        - ✅ 完全满足（功能完全匹配，接口兼容）
        - ⚠️ 部分满足（有类似功能但需要修改接口或补充参数）
        - ❌ 缺失（无相关实现）
        - ❓ 无法判断（索引或描述不足，需人工补充）
  
  3. 为除了“✅ 完全满足”之外的需求设计算法简化方案，生成结构化需求草稿，将所有的Y/N选项留给人工确认。

4. 过程留痕：把每一步的决策依据和执行计划生成文档进行记录归档，放在目录docs/records里面，以便人工追溯。

## 输入

- AFSIM：
  - 架构报告（docs/architecture/afsim-architecture.md）
  - 算法卡片概览（docs/algorithms/CompendiumofAlgorithms.md）
  - 功能索引（workspace/source-index/function-index.jsonl）
- 自有系统：（如果有的话，没有按照空系统处理）
  - 架构报告（docs/architecture/afsim-architecture.md）
  - 算法卡片概览（docs/algorithms/CompendiumofAlgorithms.md）
  - 功能索引（workspace/source-index/function-index.jsonl）
- 用户功能需求文档。
- 其他网络文献

## 输出

### `docs/requirements/structured_requirement_doc/<index>-requirement-<name>.md` 

需求规范文档。要求和格式应当严格遵循模板skill\afsim-requirement-mapper\tamplate_list\template_requirement-specification.md

