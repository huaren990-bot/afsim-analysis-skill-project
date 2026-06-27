# 需求映射过程记录 — REQ-002

> **日期**：2026-06-26
> **执行 Skill**：requirement-mapping
> **输入文档**：docs/requirements/REQ_002/2_REQ-002-requirement-formation-move-along-path.md（已确认）
> **目标系统**：空系统

---

## 1. 输入加载

| 资产 | 路径 | 状态 |
|------|------|------|
| 确认需求规范 | docs/requirements/REQ_002/2_REQ-002-requirement-formation-move-along-path.md | ✅ |
| AFSIM 功能索引 | workspace/source-index/function-index.jsonl | ✅ |
| AFSIM 架构报告 (core) | docs/architecture/core/afsim-architecture.md | ✅ |
| AFSIM 架构报告 (plugins) | docs/architecture/wsf_plugins/afsim-architecture.md | ✅ |
| 算法卡片汇总 | docs/algorithms/CompendiumofAlgorithms.md | ✅ |
| 9 张独立算法卡片 | docs/algorithms/flight-dynamics-*.md | ✅ |

## 2. FU 划分决策

| FU ID | 名称 | 简化状态 | AFSIM 证据 |
|-------|------|---------|-----------|
| FU-001 | 航路段映射（仅向前搜索） | 简2 | FormUp 阶段航路跟踪逻辑 |
| FU-002 | 航线推进（风速修正） | 无 | KeepStation ECS 坐标系 |
| FU-003 | 剩余航线裁剪 | 无 | 无独立 AFSIM 函数 |
| FU-004 | 推进系统（三简化方案） | 简1+2+3 | jet-engine + propulsion-fuel cards |
| FU-005 | 气动模型（仅气动力） | 简2 | rigidbody-aero-coefficient card |
| FU-006 | 六自由度积分器（Heun+四元数） | 无 | rigid-body-integrator card |
| FU-007 | SAS 姿态控制（三通道） | 无 | pointmass-sas card |
| FU-008 | 航线机动集成调度 | 无 | WsfPlatform::Update |

## 3. 状态判定

- 全部 8 个 FU 状态：❌ 缺失（AFSIM 有参考）
- 无 🆕 缺失（AFSIM无参考）——所有 FU 均有 AFSIM 算法卡片对应
- 迁移方式：全部 cleanroom（目标系统为空系统）

## 4. 生成文件

| 文件 | 路径 |
|------|------|
| 需求追溯矩阵 | docs/requirements/confirmed_requirement_doc/REQ-002-requirement-to-afsim-trace.md |
| 功能映射矩阵 | docs/requirements/confirmed_requirement_doc/REQ-002-function-mapping-matrix.md |
| 缺口分析报告 | docs/requirements/confirmed_requirement_doc/REQ-002-requirement-gap-analysis.md |
| 结构化缺口规格 | workspace/requirements/REQ-002-gap-specs.jsonl |
| 过程记录 | docs/records/2026-06-26-requirement-mapping-record-REQ-002.md |

## 5. 补充参数缺口（待人工提供）

| FU | 缺失参数 | 数量 |
|----|---------|------|
| FU-004 | T_max(h)、ṁ_const、油箱容量+初始油量 | 3~5 |
| FU-005 | S_ref、l_ref、大气密度模型 | 2~3 |
| FU-007 | K_p/K_i/K_d、τ、限幅值 | 9+ |