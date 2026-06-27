# 09 — 算法提取首轮记录（运动学积分器）

**日期**：2026-06-10
**状态**：首轮完成（3 张算法卡片 + 2 份支撑文件）
**对应阶段**：阶段 2 — 算法提取
**使用的 Skill**：`algorithm-extractor`

---

## 分析范围

`wsf_plugins/wsf_p6dof/` 和 `wsf_plugins/wsf_six_dof/` 中运动学积分相关核心源文件，共阅读 8 个关键文件。

## 产出清单

### docs/algorithms/（人可读算法卡片）

| 文件 | 内容 | 行数 |
|------|------|------|
| `p6dof-heun-integrator-card.md` | P6DOF Heun 修正欧拉积分器 — 完整的预测-校正框架、四元数姿态积分、力/力矩限幅、WGS84/球面地球双模型 | ~230 行 |
| `p6dof-aero-coefficient-model-card.md` | P6DOF 稳定性导数气动模型 — 20+ 条高维查表、升力/阻力/侧力/力矩六分量、简化频率计算 | ~260 行 |
| `pointmass-integration-sas-card.md` | PointMass 六自由度积分器 + 稳定增稳系统 — 控制-稳定项解耦的二阶增稳模型、一阶滚转滞后、数值限幅 | ~250 行 |

### workspace/extracted-algorithms/（机器可读支撑文件）

| 文件 | 内容 |
|------|------|
| `kinematics-integration/pseudocode.md` | 7 段结构化伪代码：Heun 积分、力/力矩评估、平动/转动推进、四元数积分、气动状态、PointMass 增稳、稳定性导数 |
| `kinematics-integration/interface-spec.md` | SI 单位接口定义：`IntegrationResult`、`HeunIntegrator`、`IForceSource` 等核心结构体和调用示例 |

## 关键发现

1. **P6DOF 与 PointMass 共用 Heun 预测-校正框架**，区别在于：P6DOF 直接计算力/力矩力矩+欧拉方程求角加速度；PointMass 将旋转加速度分解为"控制项 + 稳定项"，不显式依赖转动惯量矩阵。

2. **四元数姿态积分已替代旧的 DCM 连乘方法**，每步后做四元数归一化是关键。

3. **单位混用严重**：P6DOF 代码中 lb/ft/slug 与 m/mps 并存，SI 版本需要完全统一。

4. **PointMass 的稳定增稳系统 (SAS)** 是一个巧妙的设计：
   - 俯仰/偏航用二阶弹簧-阻尼系统（临界阻尼）驱动 α/β→0
   - 滚转用一阶滞后平滑
   - 配合数值安全限幅保证任意时间步长下不发散

5. **气动系数模型有 20+ 条高维查表**，代码中标记了 6 条 deprecated legacy 导数（单变量 α-only），新实现的应使用 α-β-Mach 三变量表。

## 可移植性评估

| 算法 | 分数 | 关键因素 |
|------|------|----------|
| Heun 积分器框架 | Medium | 核心方法标准，但框架耦合重 |
| 稳定性导数气动模型 | High/Low | 数学标准，但数据表为各飞行器特有 |
| PointMass SAS | Medium-High | 控制-稳定解耦设计可用公式重实现 |

## 未覆盖内容

- `PropagateTranslationWGSEarth` / `PropagateTranslationSphericalEarth` 中 `UtEntity` WGS84 坐标变换的具体实现（依赖 `UtEntity` 闭源类）
- `P6DofVehicle::CalculatePropulsionFM()` 发动机详细模型
- `P6DofLandingGear` 起落架接触力模型
- maneuvers/ 和 formations/ 子目录下的机动/编队库（文件量大，按需求另行分析）
- `wsf_argo8/` ARGO8 外部导弹模型集成

## 下一步建议

1. 如需继续算法提取：传感器融合跟踪(Kalman/AlphaBeta) 或 IADS C2 武器-目标配对是合适候选
2. 如需进入阶段 3（需求映射）：提供自有项目需求文档或接口定义
3. 如需进入阶段 4（迁移生成）：选择 1-2 个移植性高的算法生成代码原型
