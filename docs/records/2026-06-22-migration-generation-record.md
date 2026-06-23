# migration-generation 操作留痕 — 2026-06-22

> **日期**：2026-06-22
> **操作**：执行 migration-generation/SKILL.md，将已确认的 FU 迁移设计转化为 SDD + C++ 代码实现
> **状态**：已完成，待人工审阅代码

---

## 一、输入文件

| 文件 | 说明 |
|------|------|
| docs/migration/preliminary-migration-plan/REQ-001-FU-design-confirmed.md | 已确认迁移计划 (v0.3 confirmed) |
| docs/algorithms/flight-dynamics-jet-engine-card.md | FU-001 算法卡片 |
| docs/algorithms/flight-dynamics-propulsion-fuel-card.md | FU-001 算法卡片 |
| docs/algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md | FU-002 算法卡片 |
| docs/algorithms/flight-dynamics-rigid-body-integrator-card.md | FU-003 算法卡片 |
| docs/algorithms/flight-dynamics-pointmass-sas-card.md | FU-004 算法卡片 |
| skill/afsim-migration-builder/template_list/template_sdd.md | SDD 模板 |
| skill/afsim-migration-builder/template_list/template_REQ_xxx.h | 头文件模板 |
| skill/afsim-migration-builder/template_list/template_REQ_xxx.cpp | 实现文件模板 |
| skill/afsim-migration-builder/template_list/template_test_demo.cpp | 测试模板 |
| skill/afsim-migration-builder/template_list/template_README.md | README 模板 |

## 二、输出文件清单

| # | 文件 | 行数 | 说明 |
|---|------|------|------|
| 1 | docs/migration/software-design-specification/REQ-001-SDD.md | 292 | 软件设计说明 |
| 2 | tests/migration_src/REQ_001/REQ_001.h | 494 | 头文件：类型定义+接口声明 |
| 3 | tests/migration_src/REQ_001/REQ_001.cpp | 777 | 实现文件：4个FU全部实现 |
| 4 | tests/migration_src/REQ_001/test_demo.cpp | 427 | 测试Demo：4个测试用例 |
| 5 | tests/migration_src/REQ_001/README.md | 88 | 快速入门 |

## 三、实现决策记录

### FU-001: 推进系统与燃油管理
- Spool dynamics: `clamp(δ_cmd - δ_last, -down×dt, +up×dt)` 实现速率限制一阶滞后
- 推力查表: InterpCurve1D 存储 `f(altitude)` 曲线
- TSFC 燃油: 增量化计算（仅用增量部分×有效TSFC × dt）
- AB: 通过 `m_afterburner_present_` 开关控制
- 多线程: `std::lock_guard<std::mutex>` 保护所有状态读写

### FU-002: 气动模型
- 简化频率: `k = rate/(2×max(V,1.0)) × 参考长度`
- 系数叠加: 静态3D表 + 动态导数×简化频率 (空表→0.0)
- 有量纲化: `F = q̄ × S_ref × C × R²`, `M = q̄ × S_ref × l_ref × C`
- 构型切换: `setConfiguration(AeroConfig)` + enviro + 构型增量表集
- InterpTableND 支持2D/3D线性插值

### FU-003: 六自由度积分器
- Heun法: 预测T0→重算T1→平均FM_avg→从初始态校正
- 平动: 二次积分 `r_new = r + v×dt + ½a×dt²`
- 转动: 欧拉方程 `ω̇_i = M_i/I_ii` + 四元数积分 + normalize
- 限幅: `|F| ≤ m×1000g`, `|M_i| ≤ I_ii×62832`
- 轨迹采集: `std::vector<RigidBodyState>` 环形缓冲 (max 100000)
- 起落架: LandingGearProvider 初期返回零力/力矩

### FU-004: 姿态控制系统SAS
- 控制项: `(ω_cmd - ω_current) / dt` 各轴独立限幅
- 俯仰/偏航: 二阶临界阻尼 ζ=1 (最快无过冲)
- 滚转: 一阶滞后低通滤波
- 交叉耦合: `α_pitch' += k_y_pitch × α_yaw`, `α_yaw' += k_z_yaw × α_pitch`
- 多线程: SAS 参数通过 mutex 保护

### 全局设计决策
- 数学库: Eigen 3.x (Vector3d/Quaterniond/Matrix3d)
- 插值引擎: InterpCurve1D (1D线性), InterpTableND (2D/3D线性)
- 单位转换: 内部全部SI, 注释标注AFSIM Imperial原值
- 接口模式: IForceProvider 抽象接口注入 (替代AFSIM ForceAndMomentsObject)
- 多线程: 所有运行时状态受 std::mutex 保护, 禁止拷贝含mutex的对象

## 四、与 AFSIM 源码的差异对照

| AFSIM 类型/函数 | 目标系统 | 修改说明 |
|----------------|---------|---------|
| UtVec3dX | Eigen::Vector3d | 算子重载兼容 |
| UtQuaternion | Eigen::Quaterniond | w,x,y,z 顺序一致 |
| UtDCM | Eigen::Matrix3d | bodyToWCS() 方法返回 |
| UtTable::Table | InterpTableND | 简化为2D/3D线性插值 |
| UtTable::Curve | InterpCurve1D | 简化为1D线性插值 |
| KinematicState | RigidBodyState | 新增 alpha/beta/mach/altitude 辅助字段 |
| ForceAndMomentsObject | IForceProvider | 抽象接口依赖注入 |
| JetEngine::CalculateThrust | calculateThrust() | SI单位, 新增 mutex |
| FuelTank::UpdateFuelBurn | updateFuelBurn() | SI单位, CG插值抽取 |
| RigidBodyAeroCoreObject | RigidBodyAeroModel | 合并基类+子类为单一类 |
| RigidBodyIntegrator::Update | integrate() | 新增轨迹采集+起落架 |
| CalculateStabilityAugmentation | computeAngularAcceleration() | 新增交叉耦合补偿 |

## 五、下一步

1. 人工审阅代码：REQ_001.h / REQ_001.cpp / test_demo.cpp / REQ-001-SDD.md
2. 编译测试：`g++ -std=c++17 -I. test_demo.cpp REQ_001.cpp -o test_demo`
3. 运行验证：`./test_demo`
4. 确认后执行 `SKILL_VERIFY.md` 进行10项质量检查
