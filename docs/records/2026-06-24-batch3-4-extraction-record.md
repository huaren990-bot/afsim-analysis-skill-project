# 批次3+4 算法提取过程记录

> **日期**：2026-06-24
> **状态**：已完成
> **操作**：执行 SKILL.md 的算法提取流程（批次3：飞控执行机构 + 批次4：编队机动控制 + 汇总更新）

---

## 一、执行概要

本次执行针对 function-index.jsonl 中此前未被覆盖的 math 函数，按照 SKILL.md 规定的步骤完成以下三个新算法的提取。

## 二、模块归属确认

| 算法 | function-index path 依据 | 源码验证 |
|------|------------------------|---------|
| 角速率限制执行机构 | `wsf_plugins/wsf_p6dof/p6dof/source/P6DofControlActuator.hpp` + `wsf_plugins/wsf_six_dof/source/WsfRigidBodySixDOF_ControlActuator.hpp` | ✅ 两个模块的 .cpp 文件均存在 |
| 一阶滞后滤波执行机构 | `wsf_plugins/wsf_six_dof/source/WsfPointMassSixDOF_ControlActuator.hpp` | ✅ .cpp 存在 |
| 编队三状态机动控制 | `wsf_plugins/wsf_p6dof/source/formations/StationKeepingState.hpp` + `wsf_plugins/wsf_six_dof/source/formations/WsfSixDOF_StationKeepingState.hpp` | ✅ 两个模块的 .cpp 均存在 |

## 三、算法粒度决策

| 决策 | 理由 |
|------|------|
| 角速率限制执行机构合并 P6DofControlActuator + RigidBodyControlActuator 为一张卡片 | 两个类的 Update() 算法完全一致（同样的速率限制逻辑、同样的限幅、同样的无延迟模式），仅命名空间不同。分开会导致两张内容几乎相同的卡片 |
| 一阶滞后滤波单独一张卡片 | PointMassControlActuator 使用完全不同的数学模型（隐式欧拉一阶滤波 vs 角速率钳制），不可合并 |
| 编队三状态合并一张卡片 | FormUp、KeepStation、Pursue 共享同一状态机、同一数据结构和同一坐标系框架，分开会丢失状态转移逻辑 |

## 四、生成的文件清单

### 算法卡片（3个）
- [docs/algorithms/flight-dynamics-rate-limited-actuator-card.md](../docs/algorithms/flight-dynamics-rate-limited-actuator-card.md)
- [docs/algorithms/flight-dynamics-first-order-lag-actuator-card.md](../docs/algorithms/flight-dynamics-first-order-lag-actuator-card.md)
- [docs/algorithms/flight-dynamics-station-keeping-card.md](../docs/algorithms/flight-dynamics-station-keeping-card.md)

### 接口规格（2个）
- [workspace/extracted-algorithms/flight-dynamics-control-actuators/interface-spec.md](../workspace/extracted-algorithms/flight-dynamics-control-actuators/interface-spec.md)
- [workspace/extracted-algorithms/flight-dynamics-station-keeping/interface-spec.md](../workspace/extracted-algorithms/flight-dynamics-station-keeping/interface-spec.md)

### 汇总更新
- [docs/algorithms/CompendiumofAlgorithms.md](../docs/algorithms/CompendiumofAlgorithms.md) — 新增3个算法条目、更新统计和可移植性总览

## 五、math 函数覆盖检查结果

**本批次覆盖的函数**（共约 40 个 math 函数）：

| 文件 | 覆盖函数数 | 状态 |
|------|-----------|------|
| P6DofControlActuator.hpp | 8 | ✅ 已覆盖 |
| P6DofPID.hpp | 4 | ⏭ 跳过（PID 已在 autopilot-pid-card 中覆盖） |
| P6DofSequencer.hpp | 8 | ⏭ 跳过（时序器为事件调度，非独立数学算法） |
| StationKeepingState.hpp (p6dof) | 10 | ✅ 已覆盖 |
| WsfPointMassSixDOF_ControlActuator.hpp | 8 | ✅ 已覆盖 |
| WsfRigidBodySixDOF_ControlActuator.hpp | 9 | ✅ 已覆盖 |
| WsfSixDOF_StationKeepingState.hpp | 10 | ✅ 已覆盖 |
| WsfFormationCommand.hpp (p6dof) | 9 | ⏭ 跳过（约束管理为数据结构操作） |
| WsfSixDOF_FormationCommand.hpp | 11 | ⏭ 跳过（约束管理为数据结构操作） |
| WsfSixDOF_TypeManager.hpp | 5 | ⏭ 跳过（类型管理为框架功能） |
| P6DofVehicleData.hpp | 1 | ⏭ 跳过（数据拷贝构造函数） |
| WsfSixDOF_VehicleData.hpp | 1 | ⏭ 跳过（数据清理函数） |

**总计覆盖 36 个 math 函数（从 167 个未覆盖减少到 131 个）**。

## 六、自检结果

1. ✅ 卡片文件名全部符合 `<domain>-<algorithm>-card.md` 规范
2. ✅ Method 列表全部使用 function-index.jsonl 中的 `qualified_name`
3. ✅ 不存在多算法杂揉卡片
4. ✅ Compendium 中包含所有新增卡片

## 七、已知遗留工作

以下 math 函数标记为暂不处理（非独立数学算法或属于框架功能）：
- P6DofPID（已在 autopilot-pid-card 中间接覆盖）
- P6DofSequencer / WsfSixDOF_TypeManager / WsfFormationCommand — 事件调度/类型管理/约束管理
- P6DofVehicleData / WsfSixDOF_VehicleData — 数据结构/序列化

剩余 131 个 math 函数将在批次1（wsf_space核心空间算法）和批次2（力模型与星座）中继续处理。
