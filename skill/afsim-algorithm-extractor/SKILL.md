---
name: afsim-algorithm-extractor
description: 当用户需要从 AFSIM 源码中提取算法、数学公式、动力学模型、传感器模型、制导控制逻辑、伪代码、变量映射或可移植实现方案时，使用本 skill。
---

# AFSIM 算法提取 Skill

本 skill 负责从 AFSIM 源码中抽取可理解、可验证、可迁移的算法和功能单元。

## 输入

- AFSIM 源码片段或源码目录。
- `workspace/source-index/` 中的索引。
- 用户指定的目标算法、模块或功能。
- 自有项目的目标接口，若用户已提供。

## 执行步骤

1. 定位候选源码：优先使用索引，再用符号名、注释、调用链和文件路径补充搜索。
2. 区分三类内容：算法核心、工程封装、框架依赖。
3. 抽取输入、输出、状态变量、单位、边界条件和错误处理。
4. 将关键数值计算转换为数学表达或清晰伪代码。
5. 建立代码变量到数学符号的映射表。
6. 评估可移植性：高、中、低，并说明原因。
7. 给出验证方案：单元测试、数值对比、场景回放或边界测试。

## 输出

- `docs/algorithms/<domain>-<algorithm>-card.md`
- `workspace/extracted-algorithms/<algorithm>/pseudocode.md`
- `workspace/extracted-algorithms/<algorithm>/interface-spec.md`
- 必要时生成 `workspace/extracted-algorithms/<algorithm>/prototype.*`

## 算法卡片必须包含

- 算法名称和领域。
- 源码位置。
- 入口函数和调用链。
- 输入、输出、状态依赖。
- 数学形式或伪代码。
- 变量映射。
- 框架依赖和可替换依赖。
- 可移植性评分。
- 测试和验证计划。

## 迁移前限制

如果许可证不明确，或算法与 AFSIM 框架高度耦合，应输出 clean-room 风格的算法说明，而不是直接复制源码实现。
