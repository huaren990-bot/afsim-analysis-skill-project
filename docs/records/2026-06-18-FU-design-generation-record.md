# FU 设计生成操作留痕 — 2026-06-18

> **日期**：2026-06-18 14:30
> **操作**：执行 `skill/afsim-migration-builder/FU-design-generation/SKILL.md`
> **状态**：已完成，待人工确认

---

## 一、输入来源

| 输入 | 路径 | 内容概要 |
|------|------|---------|
| 原子功能规格 | `workspace/requirements/gap-specs.jsonl` | 4 个 FU（FU-001 ~ FU-004），全部 `migration_approach: cleanroom` |
| 需求追溯矩阵 | `docs/requirements/confirmed_requirement_doc/requirement-to-afsim-trace.md` | 每个 FU → AFSIM 源函数→文件路径的完整追溯 |
| 需求缺口分析 | `docs/requirements/confirmed_requirement_doc/requirement-gap-analysis.md` | 优先级排序：FU-003(高) > FU-001/FU-002(中) > FU-004(低) |
| 已确认需求规范 | `docs/requirements/structured_requirement_confirm/REQ-001-requirement-six-dof-UAV.md` | 全部 8 个简化方案均标记为 N（不简化），全复杂度实现 |
| AFSIM 算法卡片（5 张） | `docs/algorithms/flight-dynamics-*-card.md` | 提供详细算法流程、伪代码、变量映射表、框架依赖分析、边界条件 |

## 二、生成内容概要

### 文档结构
生成的 `docs/migration/REQ-001-FU-design.md` 包含：
- 文档头部（需求编号、名称、状态、生成时间、关联文件列表）
- **全局设计约定**：目标系统环境（C++17/Eigen/CMake）、全局类型映射、全局单位约定（Imperial→SI 转换表）
- **4 个 FU 章节**，每个 FU 使用 `source: afsim` 模板，包含完整 10 个小节

### FU-001：推进系统与燃油管理（中优先级）
- **设计依据**：AFSIM `JetEngine::CalculateThrust` (436行) + `FuelTank` (400行)
- **核心算法**：Spool dynamics 速率限制一阶滞后 + 三层推力查表（Idle/Mil/AB）+ 增量化 TSFC 燃油消耗 + CG 线性插值
- **关键设计决策**：
  - 优先实现简单 1D 曲线模式（推力 vs 高度），2D 表模式作为可选扩展
  - `UtTable::Table/Curve` → `InterpTable2D` / `InterpCurve1D` 自定义插值
  - 单位 Imperial→SI 内部转换（lb→N, ft→m, lbm→kg）
- **待确认**：是否需要支持 AB（加力燃烧室）？

### FU-002：气动模型（中优先级）
- **设计依据**：AFSIM `RigidBodyAeroCoreObject::CalculateCoreAeroFM` (~200行)
- **核心算法**：简化频率无量纲化 + 稳定性导数法 + 20+ 张气动数据表查表 + 六分量系数叠加
- **关键设计决策**：
  - 将 `AeroCoreObject` 基类 + `RigidBodyAeroCoreObject` 子类合并为单一 `RigidBodyAeroModel` 类
  - 保留简化频率公式 `k = rate/(2·max(V,1.0))` 完整逻辑
  - 空表保护：未配置的导数表返回 0.0（不崩溃）
- **待确认**：是否需要多模态气动构型切换？

### FU-003：六自由度积分器（高优先级 — 核心）
- **设计依据**：AFSIM `RigidBodyIntegrator::Update` (~100行) + 4个辅助方法 (~375行)
- **核心算法**：Heun 预测-校正法（12步）+ 牛顿第二定律平动 + 欧拉转动方程 + 四元数姿态积分归一化
- **关键设计决策**：
  - 定义 `IForceProvider` 接口实现依赖注入（气动/推进/重力均实现此接口）
  - `ForceAndMomentsObject::operator+=` 隐式参考点转换 → 显式 `convertRPtoCM()` 函数
  - `KinematicState` → `RigidBodyState` 结构体（与所有 FU 共享）
  - 初期省略起落架摩擦检查和旋转地球效应
- **待确认**：初期是否完全省略起落架模型？

### FU-004：姿态控制系统 SAS（低优先级）
- **设计依据**：AFSIM `CalculateStabilityAugmentation` (~73行，内联在 PointMassIntegrator 中)
- **核心算法**：三通道控制-稳定解耦 + 一阶指令跟踪 + 俯仰/偏航二阶临界阻尼 + 滚转一阶滞后
- **关键设计决策**：
  - 定义 `IFlightControlSystem` 接口和 `SASParams` 结构体
  - 质量比率缩放（m/m_base）：质量越小→限幅越大→飞行器越敏捷
  - 偏航通道符号翻转保留
- **待确认**：PointMass SAS 应用到 RigidBody 模型是否需要交叉耦合补偿？

## 三、关键设计决策汇总

| 决策点 | 决策 | 影响 |
|--------|------|------|
| 单位制 | 内部全部 SI，输入输出 SI | 所有 FU 统一 |
| 数学库 | Eigen 3.x（Vector3d/Quaterniond/Matrix3d） | 所有 FU 共享 |
| 查表引擎 | 自研 `InterpTable1D/2D/3D` + 线性插值 | FU-001, FU-002 |
| 力源接口 | `IForceProvider` 抽象接口 + 依赖注入 | FU-003 与 FU-001/002 解耦 |
| 状态结构体 | `RigidBodyState` 统一结构体 | FU-003, FU-004 共享 |
| 起落架 | 初期省略（先做空中飞行测试） | 简化 FU-003 |
| 旋转地球效应 | 初期省略（短时飞行可忽略） | 简化 FU-003 |
| 多模态构型 | 初期省略（后续扩展） | 简化 FU-002 |

## 四、输出文件清单

| 文件 | 路径 | 状态 |
|------|------|------|
| FU 迁移设计文档 | `docs/migration/REQ-001-FU-design.md` | ✅ 已生成 |
| 迁移日志 | `workspace/migration/migration-log.jsonl` | ✅ 已生成 |
| 操作留痕（本文件） | `docs/records/2026-06-18-FU-design-generation-record.md` | ✅ 已生成 |

## 五、下一步操作

1. 人工审阅 `docs/migration/REQ-001-FU-design.md`
2. 对每个 FU 在第 10 节勾选 Y/N，若 N 需写明修改要求
3. 确认后进入下一阶段：`skill/afsim-migration-builder/migration-generation/SKILL.md`（代码实现 + SDD）
