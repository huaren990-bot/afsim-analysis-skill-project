---
name: afsim-migration-builder
description: 当用户需要把 AFSIM 中的算法、模型或功能迁移到自有项目，生成接口适配、重写方案、代码原型、测试计划、风险评估或迁移记录时，使用本 skill。
---

# AFSIM 迁移生成 Skill

本 skill 负责把 AFSIM 中已经定位和理解的能力转化为自有项目可用的迁移方案或实现草稿。

## 输入

- 需求缺口报告。
- 算法卡片。
- AFSIM 候选源码位置。
- 自有项目接口、代码风格和构建方式。

## 执行步骤

1. 明确目标项目接入点：目录、类、接口、数据结构、测试位置。
2. 评估 AFSIM 候选实现的耦合度：框架服务、全局状态、配置系统、事件系统、外部库。
3. 选择迁移方式：直接适配、局部重写、clean-room 重实现、只迁移公式和接口。
4. 生成接口适配说明：输入、输出、单位、生命周期、错误处理。
5. 生成迁移记录：选择理由、依赖替换、许可证说明、风险和验证计划。
6. 在用户明确需要代码时，再生成小范围、可测试的实现草稿。

## 输出

- `docs/migration/<feature>-migration-plan.md`
- `docs/migration/<feature>-migration-record.md`
- `workspace/own-kernel-adapters/<feature>/interface-adapter.md`
- `workspace/own-kernel-adapters/<feature>/prototype.*`
- `tests/<feature>/`

## 迁移方式选择

| 情况 | 推荐方式 |
| --- | --- |
| 算法独立、依赖少、许可证允许 | 直接适配或小范围重写 |
| 算法清晰但框架耦合强 | 提取公式和伪代码后重写 |
| 许可证不明确 | clean-room 规格说明和重新实现 |
| 自有项目接口不明确 | 先生成接口假设和问题清单 |

## 生成代码前检查

- 是否有明确需求 ID。
- 是否有 AFSIM 源码证据。
- 是否有目标项目接入点。
- 是否有输入输出和单位说明。
- 是否有测试计划。
- 是否处理许可证和版权声明。
