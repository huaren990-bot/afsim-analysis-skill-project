# FU-design-generation 操作留痕 — REQ-002

> **日期**：2026-06-30
> **操作类型**：FU-design 初始生成（SKILL: migration-planner）
> **需求编号**：REQ-002
> **需求名称**：编队沿航线飞行机动模型设计

## 操作描述

执行 `skill/migration-builder/FU-design-generation/SKILL.md` 中的工作流程步骤 1-3（加载输入→生成 FU 迁移计划→汇编计划文档），为 REQ-002 "编队沿航线飞行机动模型设计" 生成初始 FU-design 文档。

## 输出文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| FU-design 文档 | `docs/migration/REQ-002/REQ-002-FU-design.md` | 含 9 个 FU 的完整迁移设计方案，v0.1 草稿 |
| 迁移日志 | `workspace/migration/REQ-002/REQ-002-migration-function.jsonl` | 记录本次生成事件 |
| 操作留痕 | `docs/records/2026-06-30-FU-design-generation-record-REQ-002.md` | 本文件 |

## 决策依据

### 全局设计决策
1. **目标环境**：C++17 + Eigen 3.x + CMake 3.14+，跨平台（Windows/Linux）
2. **单位策略**：内部计算全部 SI 单位制，接口输入输出使用 SI。关键公式注释标注 AFSIM Imperial 原始值
3. **代码目录**：`tests/migration_src/REQ_002/`，遵循 REQ-001 的目录约定
4. **类型映射**：UtVec3dX→Eigen::Vector3d，UtQuaternion→Eigen::Quaterniond，自定义 Point/Posture/CMRBasicBAC 结构体

### 各 FU 设计决策

| FU | 迁移策略 | 函数分解 | 算法卡片引用 | 关键设计决策 |
|----|---------|---------|-------------|-------------|
| FU-001 | Clean-room 简化版 | `mapRouteSegment()` + `computeLegProgress()` | station-keeping-card | O(1) 向前搜索，分离段定位与进度计算 |
| FU-002 | Clean-room 完整版 | `advanceAlongPath()` + `computeHeadingCommand()` | station-keeping-card | ECS坐标系位移+风速修正，分离航向角计算 |
| FU-003 | Clean-room 基础 | `trimRemainingPath()` | 无（基本数组操作） | 纯函数，无状态，保底终点 |
| FU-004 | Clean-room 简化版（最简层级） | `calculateThrust()` | jet-engine-card + propulsion-fuel-card | 简1+简2+简3 组合：线性推力+恒定燃油率+单油箱 |
| FU-005 | Clean-room 简化版 | `calculateAeroForces()` | rigidbody-aero-coefficient-card + pointmass-aero-card | 仅气动力3分量，力矩全零→SAS提供 |
| FU-006 | Clean-room 完整版 | `updateAutopilot()` | autopilot-pid-card | 完整20PID四通道，BTT/YTT嵌套回路+增益调度+anti-windup |
| FU-007 | Clean-room 完整版 | `computeStabilityAugmentation()` | pointmass-sas-card | 控制-稳定解耦架构（非PID），控制项一阶跟踪+稳定项二阶临界阻尼/一阶滞后 |
| FU-008 | Clean-room 完整版 | `integrate()` | rigid-body-integrator-card + pointmass-integrator-card | Heun预测-校正+四元数+欧拉方程含ω×Iω交叉耦合项 |
| FU-009 | Clean-room 调度层 | `runState()` + `reportError()` | core-architecture §6 | 顺序调度PATH-01→KINEMATICS-02→步长自适应输出 |

### 算法卡片引用
- station-keeping-card: FU-001, FU-002
- jet-engine-card: FU-004
- propulsion-fuel-card: FU-004
- rigidbody-aero-coefficient-card: FU-005
- pointmass-aero-card: FU-005
- autopilot-pid-card: FU-006
- pointmass-sas-card: FU-007
- rigid-body-integrator-card: FU-008
- pointmass-integrator-card: FU-008

### 函数分解原则
按照 SKILL.md 指引——按可复用性、可测试性、对主流程可读性的影响将每个 FU 拆分为 1-2 个函数：
- **可测试性**：独立计算函数（如 `computeLegProgress()`、`computeHeadingCommand()`）可单独单元测试
- **可复用性**：`computeHeadingCommand()` 可在其他需要方位角计算的场景中复用
- **可读性**：每个函数功能单一明确，避免单函数过长

## 待确认项

- [ ] 所有 9 个 FU 的设计确认勾选框
- [ ] FU-001: Point 的 _lon/_lat 单位确认（当前为 m 而非度）
- [ ] FU-002: V_wind 是否需要扩展为二维矢量支持侧风
- [ ] FU-004: T_max(h) 曲线数据、ṁ_const、Max_Fuel_Capacity 参数值
- [ ] FU-005: S_ref、l_ref 参数值；CL/CD/CY 气动系数表
- [ ] FU-006: 60+ PID 增益参数（建议使用 AFSIM 默认值）
- [ ] FU-007: ω_n_base、τ 系列时间常数、限幅值参数
- [ ] FU-008: m、I_xx/I_yy/I_zz/I_xz 常量值
- [ ] FU-009: boost::any 是否替换为 std::any/std::variant

## 下一步

人工审阅 `docs/migration/REQ-002/REQ-002-FU-design.md`，逐 FU 确认设计或提供修改要求，进入 SKILL.md 步骤 4（人工确认迭代）。
