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

3. 生成结构化需求草稿。

## 输入

- AFSIM 架构报告（docs/architecture/afsim-architecture.md）
- 算法卡片概览（docs/algorithms/CompendiumofAlgorithms.md）
- 功能索引（workspace/source-index/function-index.jsonl）
- 用户功能需求文档。

## 输出

- AFSIM 架构报告（docs/architecture/afsim-architecture.md）
- 算法卡片概览（docs/algorithms/CompendiumofAlgorithms.md）
- 功能索引（workspace/source-index/function-index.jsonl）
- 用户功能需求文档。

## 需求项 REQ-001
- **原始需求**：“飞行器要能进行高精度的六自由度仿真”
- **细化功能描述**：
  1. 使用四元数或旋转矩阵进行姿态表示，避免万向节锁
  2. 支持变步长龙格库塔积分（RK4 或更高）
  3. 刚体质量、惯量张量可配置
- **是否必须？** ☐ 必须  ☐ 可选  
- **是否需要简化？** ☐ 保持详细  ☐ 简化为“标准6DOF刚体模型”  
- **优先级建议**：高  
- **AFSIM 关联证据**：`RigidBodyDynamics::integrate_step`（src/kinematics/）  
- **备注/疑问**：是否需要考虑旋转地球（科里奥利力）？（如果用户未提及，默认否）
