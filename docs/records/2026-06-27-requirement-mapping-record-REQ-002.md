# 需求映射过程记录 — REQ-002

> **日期**：2026-06-27
> **执行 Skill**：requirement-mapping
> **输入文档**：docs/requirements/REQ_002/2_REQ-002-requirement-formation-move-along-path.md（已确认）
> **目标系统**：空系统

---

## 1. 输入加载

| 资产 | 状态 |
|------|------|
| 确认需求规范 `2_` | ✅ |
| function-index.jsonl | ✅ |
| 架构报告 core + wsf_plugins | ✅ |
| 算法卡片 10 张（全部逐卡阅读） | ✅ |

## 2. 逐卡验证结果

| 卡片 | 验证结果 |
|------|---------|
| station-keeping-card | ✅ 三状态机动控制，FormUp 航路跟踪逻辑 |
| jet-engine-card | ✅ CalculateThrust，三层查表+spool dynamics+TSFC |
| propulsion-fuel-card | ✅ PropulsionSystem::Update，多油箱传输+CG插值 |
| rigidbody-aero-coefficient-card | ✅ RigidBodyAeroCoreObject，6维查表 |
| pointmass-aero-card | ✅ PointMassAeroCoreObject，旋转限幅+SAS频率基准 |
| autopilot-pid-card | ✅ CommonController::Update，**20 PID 嵌套回路 = PID控制核心** |
| pointmass-sas-card | ✅ CalculateStabilityAugmentation，**控制-稳定解耦 ≠ PID** |
| rigid-body-integrator-card | ✅ Heun 二阶 RK + 四元数 + 欧拉方程 |

> **关键验证**：autopilot-pid-card 和 pointmass-sas-card 的分工已确认——PID=制导决策，SAS=执行保护。无管道断链。

## 3. FU 划分

| FU ID | 名称 | 简化 | 卡片 |
|-------|------|------|------|
| FU-001 | 航路段映射 | 简2 | station-keeping |
| FU-002 | 航线推进（三维指令） | 无 | station-keeping |
| FU-003 | 剩余航线裁剪 | 无 | — |
| FU-004 | 推进系统（最简） | 简1+2+3 | jet-engine + propulsion-fuel |
| FU-005 | 气动模型（仅气动力） | 简2 | rigidbody-aero + pointmass-aero |
| FU-006 | Autopilot PID（完整20PID） | 无 | autopilot-pid |
| FU-007 | SAS（控制-稳定解耦） | 无 | pointmass-sas |
| FU-008 | 六自由度积分器 | 无 | rigid-body-integrator |
| FU-009 | 集成调度 | 无 | Platform/Mover |

## 4. 状态判定

全部 9 个 FU：❌ 缺失（AFSIM 有参考），迁移方式 cleanroom。

## 5. 生成文件

| 文件 | 路径 |
|------|------|
| 追溯矩阵 | `REQ_002/3_REQ-002-requirement-to-afsim-trace.md` |
| 映射矩阵 | `REQ_002/3_REQ-002-function-mapping-matrix.md` |
| 缺口分析 | `REQ_002/3_REQ-002-requirement-gap-analysis.md` |
| gap-specs | `workspace/requirements/REQ_002/REQ-002-gap-specs.jsonl` |