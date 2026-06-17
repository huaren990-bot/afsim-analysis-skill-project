# 需求映射过程记录

> **日期**：2026-06-17
> **执行 Skill**：requirement-mapping
> **输入文档**：docs/requirements/structured_requirement_confirm/REQ-001-requirement-six-dof-UAV.md
> **输出目录**：docs/requirements/confirmed_requirement_doc/

---

## 1. 上下文加载

### 1.1 已加载资产

| 资产 | 路径 | 关键内容 |
|------|------|----------|
| 确认后需求规范 | docs/requirements/structured_requirement_confirm/REQ-001-requirement-six-dof-UAV.md | 1 个需求，4 个流程，全部简化方案标记为 N |
| AFSIM 核心架构 | docs/architecture/core/afsim-architecture.md | WsfPlatform/Mover 模型、仿真生命周期 |
| AFSIM 插件架构 | docs/architecture/wsf_plugins/afsim-architecture.md | wsf_six_dof 模块 849 文件、PointMass/RigidBody 双架构 |
| 算法卡片汇总 | docs/algorithms/CompendiumofAlgorithms.md | 23 个算法，wsf_six_dof 8 个算法 |
| 功能索引 (core) | workspace/source-index/core/function-index.jsonl | 燃油消耗率相关函数 |
| 功能索引 (plugins) | workspace/source-index/wsf_plugins/function-index.jsonl | 运动学系统三级分解 |

### 1.2 目标系统状态

**无自有项目**，按空系统处理。所有需求均视为缺失（❌）。

---

## 2. 确认后需求解析

### 2.1 人工确认决策

| 流程 | 简化列 | 简化方案1 | 简化方案2 | 决策解读 |
|------|--------|----------|----------|----------|
| 推进系统与燃油管理 | N | N | N | 完整实现发动机推力模型 + 燃油管理 |
| 气动模型 | N | N | N | 完整实现 RigidBody 稳定性导数气动模型 |
| 六自由度积分器 | Y/N（待定） | N | N | 待最终确认，暂按刚体积分器处理 |
| 姿态控制系统 SAS | N | N | N | 完整实现三通道控制-稳定解耦 SAS |

### 2.2 功能单元划分

REQ-001 按 4 个算法流程拆分为 4 个功能单元（FU）：

| FU ID | 名称 | 优先级 | 理由 |
|-------|------|--------|------|
| FU-001 | 推进系统与燃油管理 | 中 | 为积分器提供推力，依赖外部数据表 |
| FU-002 | 气动模型 | 中 | 为积分器提供气动力/力矩，依赖外部数据表，风险最高 |
| FU-003 | 六自由度积分器 | 高 | 运动学仿真核心，其他模块输出均依赖它 |
| FU-004 | 姿态控制系统 SAS | 低 | 可先用直接角加速度替代，延后集成 |

---

## 3. 输出文件

| 文件 | 路径 | 行数/条目 | 状态 |
|------|------|----------|------|
| 需求追溯矩阵 | docs/requirements/confirmed_requirement_doc/requirement-to-afsim-trace.md | 4 行 | ✅ |
| 功能映射矩阵 | docs/requirements/confirmed_requirement_doc/function-mapping-matrix.md | 4 行 | ✅ |
| 缺口分析报告 | docs/requirements/confirmed_requirement_doc/requirement-gap-analysis.md | 6 章 | ✅ |
| 结构化缺口规格 | workspace/requirements/gap-specs.jsonl | 4 行 JSON | ✅ |

---

## 4. 质量验证

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 每条需求保留原文来源 | ✅ | 所有 FU 引用 REQ-001 和确认文档路径 |
| 每个状态判断有证据 | ✅ | 引用 AFSIM 算法卡片和架构报告 |
| 模板格式匹配 | ✅ | 4 个模板全部匹配 |
| JSONL 格式 | ✅ | 4 行合法 JSON，UTF-8 无 BOM |
| 迁移可行性标注 | ✅ | 全部 cleanroom（目标系统为空） |

---

## 5. 遗留问题（已全部解决）

| # | 问题 | 影响 | 决策 |
|---|------|------|------|
| ~~1~~ | ~~FU-003 简化状态待定~~ | ~~积分器选型~~ | ✅ 已确认不简化，使用完整刚体六自由度 Heun 积分器 |
| ~~2~~ | ~~气动数据表来源~~ | ~~FU-002 能否实现~~ | ✅ 已确认采用 AFSIM 默认数据表 |
| ~~3~~ | ~~转动惯量参数~~ | ~~FU-003 刚体转动方程~~ | ✅ 已确认采用 AFSIM 默认参数 |
| ~~4~~ | ~~发动机数据表~~ | ~~FU-001 推力模型~~ | ✅ 已确认采用 AFSIM 默认数据表 |

> **状态**：所有遗留问题已解决 ✅