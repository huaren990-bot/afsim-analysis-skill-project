---
name: afsim-knowledge-curator
description: 当用户需要整理、更新、归档 AFSIM 分析知识库，包括架构报告、算法卡片、需求追溯矩阵、迁移记录、决策记录和后续任务清单时，使用本 skill。
---

# AFSIM 知识沉淀 Skill

本 skill 负责把多轮 AFSIM 分析结果整理为可复用知识库，避免每次从零理解。

## 输入

- 已生成的源码索引。
- 架构报告。
- 算法卡片。
- 需求缺口报告。
- 迁移记录。
- 用户审查意见。

## 执行步骤

1. 检查已有文档，优先更新而不是重复生成。
2. 合并重复结论，保留最新证据和审查意见。
3. 生成或更新追溯矩阵：需求 -> AFSIM 源码 -> 算法卡片 -> 迁移方案 -> 测试。
4. 记录本轮输入、产出、决策、未决问题和后续任务。
5. 标记过期索引、未知模块和需要人工确认的风险。

## 输出

- `docs/records/YYYY-MM-DD-<topic>.md`
- `docs/requirements/requirement-to-afsim-trace.md`
- `docs/migration/migration-summary.md`
- `docs/architecture/knowledge-map.md`

## 质量要求

- 文档之间的链接必须保持一致。
- 不记录隐藏推理过程。
- 对已确认、推断、未知三类结论明确标记。
- 保留用户审查意见和修改依据。
