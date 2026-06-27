# 需求追溯矩阵 — REQ-002-requirement-to-afsim-trace.md

> **来源需求规范**：[`2_REQ-002-requirement-formation-move-along-path.md`](../../requirements/REQ_002/2_REQ-002-requirement-formation-move-along-path.md)
> **日期**：2026-06-26
> **需求编号**：REQ-002
> **说明**：本矩阵展示每条需求与 AFSIM 源码实现函数及生成的功能单元（FU）之间的追溯关系。

| 需求 ID | 功能单元 ID | 需求描述 | AFSIM源函数<br>（类::方法） | 备注 |
|---------|-------------|----------|----------------------------|------|
| REQ-002-PATH-01 | FU-001 | **航路段映射（简化版）**<br>· 仅向前搜索，确定飞机所处航路段和段内进度 | `module::wsf_six_dof`<br>六自由度飞行器动力学仿真功能集合，含机动/编队子目录 | 🔑 核心 简化为仅向前搜索（禁止回退），O(1)。FormUp 航路跟踪逻辑。卡片：[flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md) |
| REQ-002-PATH-01 | FU-002 | **航线推进（风速修正）**<br>· 沿航路段推进参考点，含风速修正和期望航向输出 | `module::wsf_six_dof`<br>六自由度飞行器动力学仿真功能集合，含 ECS 坐标系编队控制 | 🔑 核心 无简化。KeepStation ECS 坐标系 P+D+DD 偏差控制。卡片：[flight-dynamics-station-keeping-card.md](../../algorithms/flight-dynamics-station-keeping-card.md) |
| REQ-002-PATH-01 | FU-003 | **剩余航线裁剪**<br>· 从航线中移除已飞越航点，返回剩余航线 | `无`<br>基本数组操作，function-index.jsonl 中无独立对应函数 | 基本数组遍历操作，无算法复杂度。cleanroom 直接实现 |
| REQ-002-KINEMATICS-02 | FU-004 | **推进系统（线性推力+恒定燃油率+单油箱）**<br>· 推力：线性推力-油门；燃油：恒定消耗率；油箱：单油箱模型 | `module::wsf_six_dof`<br>六自由度飞行器动力学仿真功能集合，含 JetEngine + PropulsionSystem 推进子系统 | 🔑 核心 已简化：简1(线性推力 T=δ×Tmax(h))+简2(恒定燃油率 ṁ=const)+简3(单油箱)。卡片：[jet-engine-card](../../algorithms/flight-dynamics-jet-engine-card.md) + [propulsion-fuel-card](../../algorithms/flight-dynamics-propulsion-fuel-card.md) |
| REQ-002-KINEMATICS-02 | FU-005 | **气动模型（仅气动力）**<br>· 仅计算气动力 3 分量，力矩由 SAS 提供 | `module::wsf_six_dof`<br>六自由度飞行器动力学仿真功能集合，含 RigidBodyAeroCoreObject 气动子系统 | 已简化：仅输出 F_aero(Fx,Fy,Fz)，M_aero 全零。卡片：[rigidbody-aero-coefficient-card](../../algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md) |
| REQ-002-KINEMATICS-02 | FU-006 | **六自由度积分器（Heun+四元数+欧拉转动方程）**<br>· Heun 预测-校正法 + 四元数姿态积分 + 欧拉转动方程 | `module::wsf_six_dof`<br>六自由度飞行器动力学仿真功能集合，含 RigidBody/PointMass 积分器 | 🔑 核心 无简化。质量(m)和惯量(I)为飞行全程常量（补充约束）。卡片：[rigid-body-integrator-card](../../algorithms/flight-dynamics-rigid-body-integrator-card.md) |
| REQ-002-KINEMATICS-02 | FU-007 | **SAS 姿态控制（三通道控制-稳定解耦）**<br>· 控制项+稳定项+独立限幅，含期望航向角转化 | `module::wsf_six_dof`<br>六自由度飞行器动力学仿真功能集合，含 PointMassFlightControlSystem SAS 子系统 | 无简化。一阶指令跟踪 + 二阶临界阻尼稳定项 + 三通道独立限幅。卡片：[pointmass-sas-card](../../algorithms/flight-dynamics-pointmass-sas-card.md) |
| REQ-002-INTEGRATION-03 | FU-008 | **航线机动集成调度**<br>· 顺序调用 PATH-01→KINEMATICS-02→输出组装 | `module::wsf`<br>AFSIM 核心仿真引擎模块，含 WsfPlatform::Update + WsfMover::Update 仿真驱动框架 | 纯调度逻辑，无独立算法。步长自适应输出。架构：[core-architecture](../../architecture/core/afsim-architecture.md) §6 |