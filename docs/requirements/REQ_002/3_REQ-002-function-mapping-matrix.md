# 功能映射矩阵 — REQ-002-function-mapping-matrix.md

> **来源需求规范**：[`2_REQ-002-requirement-formation-move-along-path.md`](../../requirements/REQ_002/2_REQ-002-requirement-formation-move-along-path.md)
> **日期**：2026-06-26
> **需求编号**：REQ-002
> **说明**：本矩阵展示每条需求对应的 AFSIM 功能和目标系统当前的能力状态，是需求覆盖度分析的汇总视图。

本功能映射矩阵中的所有功能需求均源于 `2_REQ-002-requirement-formation-move-along-path.md` 需求规范文档，文档共提出功能需求 **8 个**，各功能需求的映射关系如下：

| 需求 ID | 需求描述 | AFSIM 对应功能 | 目标系统当前功能 | 状态 | 匹配证据 / 差异说明 |
|---------|----------|----------------|------------------|------|---------------------|
| REQ-002-PATH-01 | 航路段映射：确定飞机在航线中位置，仅向前搜索 | wsf_six_dof/wsf_p6dof `maneuver/` 航路管理模块；FormUp 航路跟踪逻辑 | 无 | ❌ | 证据：function-index.jsonl 中 `module::wsf_six_dof` 含机动/编队子目录。<br>差异：AFSIM 航路管理为完整实现，本需求已简化为仅向前搜索（O(1)）；cleanroom 实现简化版 |
| REQ-002-PATH-01 | 航线推进：沿航路段推进参考点，含风速修正和期望航向 | wsf_six_dof/wsf_p6dof `formation/` 模块；KeepStation ECS 坐标系 P+D+DD 控制 | 无 | ❌ | 证据：function-index.jsonl 中 `module::wsf_six_dof` 含 ECS 坐标系编队控制。<br>差异：需提取风速修正和航向计算逻辑，去除编队多机协同部分 |
| REQ-002-PATH-01 | 剩余航线裁剪：移除已飞越航点 | 无——基本数组操作 | 无 | ❌ | 证据：function-index.jsonl 中无独立对应函数，基本数组遍历操作。<br>差异：cleanroom 直接实现，无 AFSIM 参考 |
| REQ-002-KINEMATICS-02 | 推进系统（简化版）：线性推力 T=δ×Tmax(h)、恒定燃油率、单油箱 | `JetEngine::CalculateThrust` + `PropulsionSystem::Update` + `FuelTank::UpdateFuelBurn`，位于 wsf_six_dof 插件模块 | 无 | ❌ | 证据：function-index.jsonl 中 `module::wsf_six_dof` 含推进子系统；算法卡片 jet-engine-card 和 propulsion-fuel-card 提供完整公式。<br>差异：AFSIM 为完整三层查表+spool dynamics+多油箱管理；本需求已按最简层级简化（简1+简2+简3）。需补充 4 个参数 |
| REQ-002-KINEMATICS-02 | 气动模型（简化版）：仅计算气动力 3 分量，力矩由 SAS 提供 | `RigidBodyAeroCoreObject::calculateAero`，位于 wsf_six_dof 插件模块 | 无 | ❌ | 证据：function-index.jsonl 中 `module::wsf_six_dof` 含 RigidBody 气动子系统。<br>差异：AFSIM 为完整 6 分量高维查表气动模型；本需求仅需 3 个气动力分量（无力矩）。需补充 S_ref、l_ref 参数 |
| REQ-002-KINEMATICS-02 | 六自由度积分器：Heun 二阶 RK + 四元数姿态 + 欧拉转动方程 | `RigidBodySixDOF_Mover::integrate` + `PointMassMover`，位于 wsf_six_dof 插件模块 | 无 | ❌ | 证据：function-index.jsonl 中 `module::wsf_six_dof` 含积分器功能；算法卡片 rigid-body-integrator-card 提供完整 Heun 预测-校正公式。<br>差异：无简化，cleanroom 按完整刚体积分器实现。m 和 I 为飞行全程常量（补充约束） |
| REQ-002-KINEMATICS-02 | SAS 姿态控制：三通道控制-稳定解耦，各通道独立限幅 | `PointMassFlightControlSystem::computeAngularAcceleration`，位于 wsf_six_dof 插件模块 | 无 | ❌ | 证据：function-index.jsonl 中 `module::wsf_six_dof` 含 SAS 子系统；算法卡片 pointmass-sas-card 提供完整控制-稳定解耦架构。<br>差异：无简化，cleanroom 完整实现。需补充 15 个 PID 和限幅参数 |
| REQ-002-INTEGRATION-03 | 航线机动集成层：顺序调度 + 步长自适应输出 | `WsfPlatform::Update` → `WsfMover::Update`，位于 wsf 核心模块 | 无 | ❌ | 证据：function-index.jsonl 中 `module::wsf` 含仿真引擎模块；架构 core-architecture.md §6 提供仿真生命周期框架。<br>差异：纯调度逻辑，依赖 FU-001~FU-007 全部完成后集成 |

**状态图例**：✅ 完全满足 / ⚠️ 部分满足 / ❌ 缺失（AFSIM有参考） / 🆕 缺失（AFSIM无参考） / ❓ 无法判断