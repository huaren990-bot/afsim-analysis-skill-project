# Skill 路由规则

当用户提出 AFSIM 相关任务时，先判断任务目标，再选择最小必要 skill。

## 单任务路由

| 用户意图 | 首选 Skill | 主要输出 |
| --- | --- | --- |
| 快速了解 AFSIM 总体结构 | `afsim-source-cognition` | 架构报告、模块图、源码索引 |
| 理解某个模块或函数 | `afsim-source-cognition` | 模块说明、调用链、数据流 |
| 提取算法、公式、伪代码 | `afsim-algorithm-extractor` | 算法卡片、数学表达、伪代码 |
| 判断自有项目缺少什么 | `afsim-requirement-mapper` | 需求缺口矩阵 |
| 把 AFSIM 功能用到自有项目 | `afsim-migration-builder` | 迁移方案、接口适配、测试计划 |
| 整理已有分析结果 | `afsim-knowledge-curator` | 知识库更新、追溯矩阵、决策记录 |

## 组合任务路由

完整端到端任务按以下顺序执行：

1. `afsim-source-cognition`
2. `afsim-algorithm-extractor`
3. `afsim-requirement-mapper`
4. `afsim-migration-builder`
5. `afsim-knowledge-curator`

如果已有某阶段产物，优先复用并检查是否过期。

## 停止条件

在以下情况下停止生成代码，先补充分析：

- 未找到源码证据。
- 不清楚自有项目接口。
- 许可证状态不明确且用户要求直接复用代码。
- 算法输入、输出、单位或状态依赖不明确。
