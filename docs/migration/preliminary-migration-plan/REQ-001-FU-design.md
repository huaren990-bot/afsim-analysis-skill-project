# 功能单元实现规格 — Function Unit Migration Design

>**需求编号**：REQ-001  
>**需求名称**：使用六自由度模型计算无人机的姿态和轨迹  
>**文档状态**：待确认  
>**生成时间**：2026-06-18 14:30  
>**最后确认时间**：—  
>**设计者**：AI + 待人工确认  
>**关联文件**：  
>- `workspace/requirements/gap-specs.jsonl` — 原子功能规格输入
>- `docs/algorithms/flight-dynamics-jet-engine-card.md` — FU-001 喷气发动机推力模型算法卡片
>- `docs/algorithms/flight-dynamics-propulsion-fuel-card.md` — FU-001 推进系统与燃油管理算法卡片
>- `docs/algorithms/flight-dynamics-rigidbody-aero-coefficient-card.md` — FU-002 气动系数模型算法卡片
>- `docs/algorithms/flight-dynamics-rigid-body-integrator-card.md` — FU-003 六自由度积分器算法卡片
>- `docs/algorithms/flight-dynamics-pointmass-sas-card.md` — FU-004 姿态控制系统算法卡片
>- `docs/requirements/confirmed_requirement_doc/function-mapping-matrix.md` — 需求功能映射矩阵
>- `docs/requirements/confirmed_requirement_doc/requirement-to-afsim-trace.md` — 需求追溯矩阵
>- `docs/requirements/confirmed_requirement_doc/requirement-gap-analysis.md` — 需求缺口分析

---

## 全局设计约定

以下约定适用于本迁移计划中的所有功能单元（FU），各 FU 章节不再重复说明。

### 目标系统环境
| 项目 | 约定 |
|------|------|
| **语言标准** | C++17 |
| **数学库** | Eigen 3.x（向量/矩阵/四元数） |
| **构建系统** | CMake 3.14+ |
| **目标平台** | Windows / Linux 跨平台 |
| **代码目录** | `tests/migration_src/REQ_001/` |

### 全局类型映射
| AFSIM 类型 | 目标系统类型 | 头文件 |
|------------|-------------|--------|
| `double` | `double` | — |
| `int64_t` | `int64_t` | `<cstdint>` |
| `bool` | `bool` | — |
| `UtVec3dX` | `Eigen::Vector3d` | `<Eigen/Dense>` |
| `UtQuaternion` | `Eigen::Quaterniond` | `<Eigen/Geometry>` |
| `UtDCM` | `Eigen::Matrix3d` | `<Eigen/Geometry>` |
| `UtTable::Table` | 自定义 `InterpTable3D` / `InterpTable2D` | `interp_table.h` |
| `UtTable::Curve` | `std::function<double(double)>` 或自定义 `InterpCurve1D` | `interp_curve.h` |
| `std::vector<T>` | `std::vector<T>` | `<vector>` |
| `std::unordered_map<K,V>` | `std::unordered_map<K,V>` | `<unordered_map>` |

### 全局单位约定
| 物理量 | AFSIM 单位 | 目标系统单位 | 转换关系 |
|--------|-----------|-------------|----------|
| 位置 | ft | m | 1 ft = 0.3048 m |
| 速度 | ft/s | m/s | 1 ft/s = 0.3048 m/s |
| 质量 | lbm (pound-mass) | kg | 1 lbm = 0.453592 kg |
| 力 / 推力 | lbf (pound-force) | N | 1 lbf = 4.44822 N |
| 力矩 | ft-lbf | N·m | 1 ft-lbf = 1.35582 N·m |
| 角度 | rad | rad | 一致 |
| 角速率 | rad/s | rad/s | 一致 |
| 转动惯量 | slug-ft² | kg·m² | 1 slug-ft² = 1.35582 kg·m² |
| 动压 | lb/ft² | Pa (N/m²) | 1 lb/ft² = 47.8803 Pa |
| 重力加速度 | 9.80665 m/s² | 9.80665 m/s² | 一致 |

> **单位策略**：内部计算全部使用 SI 单位制，接口输入输出使用 SI 单位。在关键公式注释中标注原始 AFSIM Imperial 值以保持可追溯性。

---

## FU-001：推进系统与燃油管理（source: afsim）

| 属性 | 内容 |
|------|------|
| **关联需求** | REQ-001 |
| **优先级** | 中 |
| **来源类型** | `afsim` |
| **设计版本** | v1.0 draft |
| **设计日期** | 2026-06-18 |
| **功能描述** | 根据发动机燃油流量输入和当前飞行状态（速度、高度）计算发动机推力，并更新燃油消耗量。需实现喷气发动机推力模型（含 Idle/Mil/AB 三层查表 + spool dynamics 转速加减速动特性）和燃油管理系统（含燃油消耗率限制、多油箱燃油传输比例协调、CG 位置线性插值）。 |
| **AFSIM 源位置** | `wsf_six_dof/source/WsfSixDOF_JetEngine.hpp:31-168 (JetEngine)` / `WsfSixDOF_JetEngine.cpp:428-864 (CalculateThrust)` / `WsfSixDOF_PropulsionSystem.hpp:34-237 (PropulsionSystem)` / `WsfSixDOF_FuelTank.hpp:34-232 (FuelTank)` |
| **源码行数** | JetEngine::CalculateThrust ~436行 + PropulsionSystem::Update ~170行 + FuelTank 各方法 ~400行，合计约 1000+ 行 |
| **迁移策略** | Clean-room 重实现（仅参考功能描述和算法卡片，不直接复制代码） |
| **风险评估** | 中 |

---

### 1. 功能概述

该功能单元负责两个紧密耦合的子功能：(1) **喷气发动机推力模型**——根据油门指令、飞行高度和马赫数，通过三层推力查表（Idle/Mil/AB）和油门 spool dynamics（转速加减速动特性）计算发动机推力和燃油消耗率；(2) **燃油管理系统**——管理油箱燃油消耗、多油箱间燃油传输、CG 位置线性插值和总质量属性汇总。

在仿真流程中，该 FU 位于积分器的力/力矩聚合阶段（`CalculateFM` → `CalculatePropulsionFM` → `JetEngine::CalculateThrust` + `FuelTank::UpdateFuelBurn`），为积分器提供推进力输入和更新后的燃油质量。

迁移必要性：目标系统为空系统，无任何推进或燃油管理代码，需从零构建。

### 2. 参考来源与算法依据

#### 2.1 AFSIM 参考实现

| 属性 | 值 |
|------|----|
| 源函数 | `JetEngine::CalculateThrust` / `PropulsionSystem::Update` / `FuelTank::UpdateFuelBurn` |
| 源文件 | `wsf_six_dof/source/WsfSixDOF_JetEngine.cpp:428-864` / `WsfSixDOF_PropulsionSystem.cpp:78-249` / `WsfSixDOF_FuelTank.cpp:390-431` |
| 源码行数 | JetEngine ~436行 + PropulsionSystem ~170行 + FuelTank ~400行 |
| 依赖的 AFSIM 类型/宏 | `UtTable::Table`（2D查表）、`UtTable::Curve`（1D曲线）、`UtVec3dX`（三维矢量）、`UtCloneablePtr`（深拷贝智能指针）、`ForceAndMomentsObject` |
| 依赖的全局变量/常量 | `cM_PER_FT`(0.3048)、`cEPSILON_SIMTIME_SEC`(极小时间阈值) |
| 使用的第三方库 | 无（仅 AFSIM 内部数学库） |

#### 2.2 核心算法摘要

**JetEngine::CalculateThrust**（436行）核心流程：

1. **油门指令确定**：优先使用直接设定的油门杆位置（`mThrottleLeverPosition`, 0=Idle/1=Mil/2=全AB），否则由父对象 Mil+AB 油门合成
2. **Spool Dynamics**：有效油门渐进跟随指令油门，`δ_eff(t+Δt) = δ_eff(t) + clamp(δ_cmd - δ_eff(t), -δ̇_down·Δt, +δ̇_up·Δt)`；Mil段和AB段使用不同的加减速率（spin-up/spin-down rate，可为标量或1D曲线查表）
3. **油门分解**：`δ_mil = min(δ_eff, 1.0)`, `δ_ab = max(0, δ_eff - 1.0)`
4. **三层推力查表**（简单曲线模式或改进2D表模式 Mach×Alt）：
   - `T_idle = f_idle(h)`, `T_mil_inc = f_mil(h) - f_idle(h)`, `T_ab_inc = f_ab(h) - f_mil(h)`
   - `T_total = T_idle + δ_mil·T_mil_inc + δ_ab·T_ab_inc`
5. **燃油消耗**（增量化 TSFC）：`m_fuel = (T_idle·SFC_idle_pps + δ_mil·T_mil_inc·SFC_mil_eff_pps + δ_ab·T_ab_inc·SFC_ab_eff_pps) × Δt`
6. **熄火保护**：缺油/断油时 `T_eff = -D_dead`（死机进气口阻力），`D_dead = A_drag × q̄`；flame-out时按燃油供给比例缩比推力并叠加部分死机阻力

**FuelTank 燃油管理**核心流程：

- **CG 线性插值**：`r_cg = r_empty + (m_current/m_max) × (r_full - r_empty)`
- **燃油消耗速率限制**：`ṁ_actual = min(ṁ_request, ṁ_max_flow×Δt, m_remaining)`
- **多油箱传输比例协调**：供给超过目标接收能力时等比压缩，`f = |m_max_receive| / |Σ m_provided|`
- **总质量属性汇总**：`m_total = Σ m_i`, `r_cg_total = Σ(m_i·r_i)/Σ m_i`

### 3. 耦合度与依赖分析

| 评估维度 | 说明 |
|----------|------|
| 框架耦合 | 中 — JetEngine 继承自 `Engine` 基类（`ThrustProducerObject` 子类），PropulsionSystem 依赖 `Mover` 的 freeze 标志和父对象接口。剥离时可定义等效抽象接口。 |
| 数据耦合 | 中 — 依赖 `KinematicState`（速度/高度/马赫数）、`MassProperties`（质量特性）、`FuelTank` 对象（油箱状态）。迁移时替换为自定义数据结构。 |
| 控制耦合 | 低 — 推力计算为纯函数（给定输入→输出），不依赖全局状态机。仅油门 spool dynamics 需帧间状态（上一帧有效油门）。 |
| 外部依赖 | 低 — 仅依赖 `UtTable::Table/Curve` 查表引擎（可替换为自定义插值），无数据库/网络/硬件依赖。 |

**综合等级**：中  
**剥离策略**：将 JetEngine 和 FuelTank 拆分为独立类，定义清晰的输入/输出接口；使用标准 C++ 和 Eigen 替代 AFSIM 矢量类型；查表引擎替换为基于 `std::vector` + 线性插值的自定义实现。

### 4. 实现方案

#### 4.1 接口转换

| 原 AFSIM 接口 | 目标系统接口 | 转换说明 |
|---------------|--------------|----------|
| `JetEngine::CalculateThrust(dT_sec, alt_ft, dynPress_lbsqft, mach, out thrust_lbs, out fuelBurnRate_pps, out fuelBurned_lbs, updateData)` | `JetEngine::calculateThrust(double dt, double altitude, double dyn_pressure, double mach, ThrustOutput& out)` | 单位 Imperial→SI；输出合并为结构体 |
| `FuelTank::UpdateFuelBurn(dT_sec, burnRequest_lbs, out actualBurned, out newMass, out newCg)` | `FuelTank::updateFuelBurn(double dt, double burn_request, FuelBurnResult& out)` | 单位 lb→kg；多返回值→结构体 |
| `FuelTank::CalcCgLocation_ft(currentFuelQty_lbs)` | `FuelTank::calcCgLocation(double current_fuel_kg)` | 单位 ft→m, lb→kg |
| `PropulsionSystem::Update(simTime_nanosec)` | `PropulsionSystem::update(double dt)` | 直接使用秒为单位步长 |
| `PropulsionSystem::GetMassProperties()` | `PropulsionSystem::getMassProperties()` | 返回 SI 单位质量属性 |

- **源接口**（AFSIM）：
  ```cpp
  void CalculateThrust(double aDeltaT_sec, double aAlt_ft, double aDynPress_lbsqft,
                       double aMach, double& aForceAndMoment, double& aFuelBurnRate_pps,
                       double& aFuelBurned_lbs, bool aUpdateData);
  ```
- **目标接口**：
  ```cpp
  ThrustOutput calculateThrust(double dt, double altitude_m, double dyn_pressure_pa,
                               double mach, bool update_state = true);
  // ThrustOutput { double thrust_N; double fuel_burn_rate_kgs; double fuel_burned_kg; }
  ```

#### 4.2 需移除的 AFSIM 专属代码

- [ ] `UtTable::Table` / `UtTable::Curve` 查表引擎 → 替换为自定义 `InterpTable1D` / `InterpTable2D`
- [ ] `ForceAndMomentsObject` 力/力矩容器 → 替换为 `Eigen::Vector3d` 直接计算
- [ ] `UtCloneablePtr<T>` 深拷贝智能指针 → 替换为 `std::unique_ptr<T>`
- [ ] `UtInput` / `UtInputBlock` 配置解析 → 替换为 JSON 配置文件读取
- [ ] `UtMath::cM_PER_FT` / `cLB_PER_NT` 等单位常数 → 直接在公式中使用 SI 转换因子
- [ ] `ut::log::error()` 日志 → 替换为 `std::cerr` 或自定义日志宏

#### 4.3 需保留并修改的部分

- [ ] **Spool Dynamics 算法核心**：速率限制一阶滞后公式完整保留，仅变量名和单位转换
- [ ] **三层推力查表逻辑**：Idle/Mil/AB 查表+增量叠加架构保留；优先实现简单1D曲线模式（推力 vs 高度），2D表模式作为可选扩展
- [ ] **TSFC 增量化燃油消耗公式**：保留有效 TSFC 反算逻辑（从额定推力和名义 TSFC 计算增量 TSFC）
- [ ] **熄火保护逻辑**：缺油/断油/燃油路径中断的判定链保留
- [ ] **CG 线性插值公式**：一行核心公式直接移植
- [ ] **多油箱传输比例协调算法**：供给/需求计算和等比压缩逻辑保留

#### 4.4 新增辅助代码

- [ ] `InterpCurve1D` 类：1D 线性插值曲线（替代 `UtTable::Curve`）
- [ ] `InterpTable2D` 类：2D 双线性插值表（替代 `UtTable::Table`）
- [ ] `ThrustTableSet` 结构体：封装 Idle/Mil/AB 三张推力表 + TSFC 参数
- [ ] `FuelTankConfig` 结构体：封装油箱容量/速率/CG 配置参数
- [ ] `SpoolDynamicsConfig` 结构体：封装 Mil/AB 加减速率参数

### 5. 接口详细定义（API）

#### 5.1 函数：`JetEngine::calculateThrust`

| 项目 | 说明 |
|------|------|
| **签名** | `ThrustOutput calculateThrust(double dt, double altitude_m, double dyn_pressure_pa, double mach, bool update_state = true);` |
| **输入** | 详见下表 |
| **输出** | `ThrustOutput` 结构体：`thrust_N`（推力, N）、`fuel_burn_rate_kgs`（燃油消耗率, kg/s）、`fuel_burned_kg`（本步消耗燃油, kg）、`engine_operating`（发动机是否运转）、`afterburner_on`（加力是否开启） |
| **前置条件** | `dt > 0`，`altitude_m ≥ 0`，`dyn_pressure_pa ≥ 0`，`mach ≥ 0` |
| **后置条件** | 若 `update_state=true`，内部状态（有效油门、RPM指示）已更新 |
| **复杂度** | O(1) × 查表次数（简单模式3次1D查表+4次spin rate查表 ≈ 7次插值）；2D表模式约 9-11次2D查表 |

**输入参数详细表**：

| 参数名 | 类型 | 有效范围/约束 | 说明 |
|--------|------|---------------|------|
| `dt` | `double` | (0, 1.0] s | 仿真步长 |
| `altitude_m` | `double` | [0, 50000] m | MSL 海拔高度 |
| `dyn_pressure_pa` | `double` | [0, ∞) Pa | 自由流动压 q̄ = 0.5·ρ·V² |
| `mach` | `double` | [0, 10] | 飞行马赫数 |
| `update_state` | `bool` | — | 是否更新内部状态变量 |

#### 5.2 函数：`FuelTank::updateFuelBurn`

| 项目 | 说明 |
|------|------|
| **签名** | `FuelBurnResult updateFuelBurn(double dt, double burn_request_kg);` |
| **输入** | `dt`（仿真步长, s）、`burn_request_kg`（请求燃烧燃油质量, kg） |
| **输出** | `FuelBurnResult`：`able_to_provide`（bool）、`actual_burned_kg`（实际燃烧量, kg）、`new_mass_kg`（新油量, kg）、`new_cg_m`（新 CG 位置, Eigen::Vector3d） |
| **前置条件** | `dt > 0`, `burn_request_kg ≥ 0`, `m_max_flow_rate_kgps ≥ 0` |
| **后置条件** | `m_current_quantity_kg ≥ 0`（永不小于零） |
| **复杂度** | O(1) |

#### 5.3 函数：`PropulsionSystem::update`

| 项目 | 说明 |
|------|------|
| **签名** | `void update(double dt);` |
| **输入** | `dt`（仿真步长, s） |
| **输出** | 无（修改内部燃油箱状态：执行燃油传输、清理无效传输路径） |
| **前置条件** | `dt > 0` |
| **后置条件** | 所有燃油传输路径已处理，传输速率已更新 |
| **复杂度** | O(T·S)，T=传输链路数，S=每链路源油箱数 |

### 6. 数据类型映射表

| AFSIM 类型 | 目标系统类型 | 头文件/定义位置 | 备注 | 转换代码示例 |
|------------|-------------|----------------|------|-------------|
| `double` (lb) | `double` (kg) | — | 质量: ×0.453592 | `kg = lb * 0.453592` |
| `double` (lbf) | `double` (N) | — | 力: ×4.44822 | `N = lbf * 4.44822` |
| `double` (ft) | `double` (m) | — | 长度: ×0.3048 | `m = ft * 0.3048` |
| `double` (ft/s) | `double` (m/s) | — | 速度: ×0.3048 | `mps = fps * 0.3048` |
| `double` (lb/ft²) | `double` (Pa) | — | 动压: ×47.8803 | `pa = lbsqft * 47.8803` |
| `double` (lb/s) | `double` (kg/s) | — | 质量流率: ×0.453592 | `kgps = pps * 0.453592` |
| `UtVec3dX` | `Eigen::Vector3d` | `<Eigen/Dense>` | 三维矢量（如CG位置） | `Eigen::Vector3d(v[0], v[1], v[2])` |
| `UtTable::Curve*` | `InterpCurve1D` | `interp_curve.h` | 1D 查表曲线 | 自定义类 |
| `UtTable::Table*` | `InterpTable2D` | `interp_table.h` | 2D 查表 | 自定义类 |
| `std::unordered_map<string, CloneablePtr<FuelTank>>` | `std::unordered_map<std::string, std::unique_ptr<FuelTank>>` | `<unordered_map>`, `<memory>` | 油箱名称映射 | `std::make_unique<FuelTank>(...)` |

### 7. 内部状态与生命周期

| 状态变量 | 类型 | 默认值 | 生命周期 | 线程安全 | 备注 |
|----------|------|--------|----------|----------|------|
| `m_last_throttle_` | `double` | 0.0 | 对象级 | 否 | 上一帧有效油门 [0, 2]，spool dynamics 初值 |
| `m_current_thrust_N_` | `double` | 0.0 | 对象级 | 否 | 当前推力值（极小dt时返回此值） |
| `m_engine_percent_rpm_` | `double` | 0.0 | 对象级 | 否 | 发动机转速百分比 = 100.0 × δ_mil |
| `m_afterburner_present_` | `bool` | false | 对象级（不变） | 否 | 是否配置加力燃烧室 |
| `m_throttle_lever_position_` | `double` | 0.0 | 对象级 | 否 | 直接设定的油门杆位置 |
| `m_throttle_position_set_` | `bool` | false | 对象级 | 否 | 标记直设油门是否有效 |
| `m_inject_fuel_` | `bool` | true | 对象级 | 否 | 供油开关 |
| `m_current_fuel_tank_` | `FuelTank*` | nullptr | 对象级 | 否 | 当前供油油箱指针 |
| `m_current_quantity_kg_` | `double` | 0.0 | 对象级 | 否 | 油箱当前燃油质量 |
| `m_max_quantity_kg_` | `double` | 0.0 | 对象级（不变） | 否 | 油箱最大容量 |
| `m_cg_empty_m_` | `Eigen::Vector3d` | (0,0,0) | 对象级（不变） | 否 | 空油箱 CG 位置 |
| `m_cg_full_m_` | `Eigen::Vector3d` | (0,0,0) | 对象级（不变） | 否 | 满油箱 CG 位置 |
| `m_max_flow_rate_kgps_` | `double` | 0.0 | 对象级（不变） | 否 | 最大供油速率 |
| `m_max_transfer_rate_kgps_` | `double` | 0.0 | 对象级（不变） | 否 | 最大传输速率 |

- **是否需要 `reset()` 函数**：是 — 将有效油门、当前推力、RPM、燃油量等运行时状态重置为初始值
- **拷贝/移动行为**：允许深拷贝（引擎和油箱对象可复制）；移动语义支持
- **初始化要求**：构造后必须调用 `loadConfig()` 加载推力表、TSFC、油箱参数等配置；首次调用 `calculateThrust()` 前需设置初始油门位置

### 8. 错误处理策略

| 异常场景 | 检测条件 | 处理方式 | 返回/错误码 |
|----------|----------|----------|-------------|
| 非法输入（dt ≤ 0） | 函数入口 if 判断 | 返回当前推力，燃油消耗=0 | `{current_thrust, 0, 0}` |
| 查表输入越界（高度/马赫） | 插值引擎检测 | 边界钳位（clamp to range），打印警告 | 边界值 |
| 油箱容量 ≤ 0 | 构造时检查 | 抛出 `std::invalid_argument` | — |
| 燃油不足（油箱不够烧） | `remainingAfterBurn < 0` | `burnAmount = burnRequest + remainingAfterBurn`（仅烧剩余量） | `able_to_provide = false` |
| 燃油路径中断（油箱被抛弃） | 检查 `FuelFlowPathIntact()` | 置空油箱指针，进入 deadEngine | 推力 = -deadEngineDrag |
| 主动断油（`m_inject_fuel_ == false`） | 每帧检查 | 进入 deadEngine 状态 | 推力 = 0 + 进气口阻力 |
| 质量比率异常（m/m_base > 1） | 每帧检查 | 不触发错误，仅限幅变迟钝 | 正常返回 |

### 9. 风险与未决问题

- **技术风险**：Spool dynamics 的加减速率参数（spin-up/spin-down rate）为发动机型号特有数据，AFSIM 默认值可能不适用于目标无人机型号——需通过发动机手册或系统辨识获取准确参数
- **技术风险**：三层推力表（Idle/Mil/AB）和 TSFC 数据为发动机制造商机密数据，AFSIM 默认数据表仅供开发测试，需最终用户替换为真实数据
- **合规风险**：低 — 核心算法（速率限制一阶滞后 + 线性插值查表）为公开工程方法，不涉及专利
- **待确认**：是否需要支持 AB（加力燃烧室）？若无 AB 需求的无人机型号可简化掉 AB 段逻辑

### 10. 人工确认

请逐项勾选确认：

- [ ] 耦合评估合理
- [ ] 接口适配方案可行
- [ ] 数据类型映射正确
- [ ] 内部状态管理设计合理
- [ ] 错误处理策略完整
- [ ] 测试策略与用例充分

**修改要求**（若有）：  
______________________________________________  

**确认人**：__________  
**确认日期**：__________  


---

## FU-002：气动模型（source: afsim）

| 属性 | 内容 |
|------|------|
| **关联需求** | REQ-001 |
| **优先级** | 中 |
| **来源类型** | `afsim` |
| **设计版本** | v1.0 draft |
| **设计日期** | 2026-06-18 |
| **功能描述** | 根据无人机当前飞行状态（马赫数、攻角、侧滑角、角速率）计算气动六分量（升力、阻力、侧力、滚转力矩、俯仰力矩、偏航力矩）。需实现 RigidBody 稳定性导数气动系数模型，支持高维查表（Ma×α×β×p×q×r 6维插值）、静态3D表项与动态阻尼增量线性叠加、动压×参考面积×参考长度缩放。 |
| **AFSIM 源位置** | `wsf_six_dof/source/WsfRigidBodySixDOF_AeroCoreObject.hpp:27-181 (RigidBodyAeroCoreObject)` / `WsfRigidBodySixDOF_AeroCoreObject.cpp:747-951 (CalculateCoreAeroFM)` / `WsfSixDOF_AeroCoreObject.hpp:34-78 (AeroCoreObject 基类)` |
| **源码行数** | CalculateCoreAeroFM ~200行 + ProcessCommonInput ~350行 + 14个查表函数各~10行，合计约 700 行 |
| **迁移策略** | Clean-room 重实现（仅参考功能描述和算法卡片，不直接复制代码） |
| **风险评估** | 中 |

---

### 1. 功能概述

该功能单元根据飞行器的瞬时飞行状态（马赫数、攻角 α、侧滑角 β、角速率 p/q/r、攻角变化率 α̇、侧滑角变化率 β̇），通过稳定性导数法计算六分量气动力和力矩。核心机制是"简化频率（Reduced Frequency）"无量纲化——将角速率和变化率除以 2V 得到无量纲频率，按参考长度（弦长或翼展）缩放后乘以对应的动态导数，再与静态 3D 表项（α×β×Mach）线性叠加，最后乘以动压、参考面积和参考长度得到有量纲力/力矩。

在仿真流程中，该 FU 位于积分器的力/力矩聚合阶段（`CalculateFM` → `CalculateAeroBodyForceAndMoments` → `RigidBodyAeroCoreObject::CalculateCoreAeroFM`），为积分器提供气动力和气动力矩。

迁移必要性：目标系统为空系统，无任何气动模型代码。

### 2. 参考来源与算法依据

#### 2.1 AFSIM 参考实现

| 属性 | 值 |
|------|----|
| 源函数 | `RigidBodyAeroCoreObject::CalculateCoreAeroFM` |
| 源文件 | `wsf_six_dof/source/WsfRigidBodySixDOF_AeroCoreObject.cpp:747-951` |
| 源码行数 | ~200 行（核心计算函数） |
| 依赖的 AFSIM 类型/宏 | `UtTable::Table`（3D查表）`UtTable::Curve`（1D曲线）`UtVec3dX`（矢量）`AeroCoreObject`（基类，持有CL/Cd/CY静态3D表） |
| 依赖的全局变量/常量 | 无全局状态；翼面几何参数（`mWingChord_ft`, `mWingSpan_ft`, `mWingArea_sqft`）为配置常量 |
| 使用的第三方库 | 无 |

#### 2.2 核心算法摘要

**简化频率（Reduced Frequency）无量纲化**：
```
V_safe = max(V, 1.0)  // 防止除零
k_q = q / (2·V_safe), k_r = r / (2·V_safe), k_p = p / (2·V_safe)
k_α̇ = α̇ / (2·V_safe), k_β̇ = β̇ / (2·V_safe)
// 按参考长度缩放各分量独立简化频率（俯仰用弦长c，偏航/滚转用翼展b）
```

**升力系数**（静态 + 动态）：
```
C_L_total = C_L(α, β, M) + C_Lq(α, M)·k_Lq + C_Lα̇(α, M)·k_La
L = q̄ · S_ref · C_L_total · R²
```

**阻力系数**（仅静态，无动态项）：
```
C_d = C_d(α, β, M)
D = q̄ · S_ref · C_d · R²
```

**侧力系数**（静态 + 动态）：
```
C_Y_total = C_Y(α, β, M) + C_Yr(β, M)·k_Yr + C_Yβ̇(β, M)·k_Yb
Y = q̄ · S_ref · C_Y_total · R²
```

**俯仰力矩系数**（含交叉导数）：
```
C_m_total = C_m(α, β, M) + C_mq(M)·k_mq + C_mp(M)·k_mp + C_mα̇(M)·k_ma
M_y = q̄ · S_ref · c_ref · C_m_total
```

**偏航力矩系数**：
```
C_n_total = C_n(α, β, M) + C_nr(M)·k_nr + C_np(M)·k_np + C_nβ̇(M)·k_nb
M_z = q̄ · S_ref · b · C_n_total
```

**滚转力矩系数**（最全面，含 6 项叠加）：
```
C_l_total = C_l(α, β, M) + C_lp(M)·k_lp + C_lr(M)·k_lr + C_lq(M)·k_lq + C_lα̇(M)·k_la + C_lβ̇(M)·k_lb
M_x = q̄ · S_ref · b · C_l_total
```

### 3. 耦合度与依赖分析

| 评估维度 | 说明 |
|----------|------|
| 框架耦合 | 中 — 继承自 `AeroCoreObject` 基类（持有 CL/Cd/CY 三张静态 3D 表）。子类额外管理 14 张动态导数表。迁移时可合并为单一扁平类。 |
| 数据耦合 | 中 — 依赖 20+ 张气动数据表（6张静态3D表 + 6张动态2D表 + 8张动态1D曲线）和翼面几何参数（弦长/翼展/面积）。数据表为飞行器特有数据。 |
| 控制耦合 | 低 — `CalculateCoreAeroFM` 为纯函数（14个查表函数均无副作用），不修改任何成员变量。配置加载与运行时计算分离。 |
| 外部依赖 | 低 — 仅依赖 `UtTable::Table/Curve` 查表引擎，替换为自定义多维插值即可。 |

**综合等级**：中  
**剥离策略**：将 `AeroCoreObject` 基类和 `RigidBodyAeroCoreObject` 子类合并为单一的 `RigidBodyAeroModel` 类；用自定义多维插值引擎替代 `UtTable::Table/Curve`；保留简化频率无量纲化公式和系数叠加架构；支持两种面积模式（翼面模式 / 显式参考面积模式）。

### 4. 实现方案

#### 4.1 接口转换

| 原 AFSIM 接口 | 目标系统接口 | 转换说明 |
|---------------|--------------|----------|
| `CalculateCoreAeroFM(q_bar_lbsqft, mach, V_fps, α_rad, β_rad, α̇_rps, β̇_rps, ω_vec, radiusFactor, out moment_ftlbs, out lift_lbs, out drag_lbs, out sideForce_lbs)` | `AeroOutput calculateAero(const AeroInput& input)` | 所有参数打包为结构体；输出结构体；单位 SI |

- **源接口**（AFSIM）：
  ```cpp
  void CalculateCoreAeroFM(double aDynPress_lbsqft, double aMach, double aSpeed_fps,
                           double aAlpha_rad, double aBeta_rad, double aAlphaDot_rps,
                           double aBetaDot_rps, const UtVec3dX& aAngularRates_rps,
                           double aRadiusSizeFactor, UtVec3dX& aMoment_ftlbs,
                           double& aLift_lbs, double& aDrag_lbs, double& aSideForce_lbs);
  ```
- **目标接口**：
  ```cpp
  struct AeroInput {
      double dyn_pressure_pa;      // 动压 q̄ (Pa)
      double mach;                 // 马赫数
      double speed_mps;            // 真空速 (m/s)
      double alpha_rad;            // 攻角 (rad)
      double beta_rad;             // 侧滑角 (rad)
      double alpha_dot_rps;        // 攻角变化率 (rad/s)
      double beta_dot_rps;         // 侧滑角变化率 (rad/s)
      Eigen::Vector3d angular_rates_rps; // 体轴角速率 [p, q, r]
      double radius_factor;        // 几何尺度因子
  };
  struct AeroOutput {
      Eigen::Vector3d force_N;     // 气动力 [lift, drag, side] (N)
      Eigen::Vector3d moment_Nm;   // 气动力矩 [roll, pitch, yaw] (N·m)
  };
  AeroOutput calculateAero(const AeroInput& input);
  ```

#### 4.2 需移除的 AFSIM 专属代码

- [ ] `UtTable::Table` 3D插值引擎 → 自定义 `InterpTable3D`（α×β×Mach 三维线性插值）
- [ ] `UtTable::Curve` 1D曲线 → 自定义 `InterpCurve1D`（Mach 一维线性插值）
- [ ] `AeroCoreObject` 基类（CL/Cd/CY 静态表分离）→ 合并到 `RigidBodyAeroModel` 类
- [ ] `ForceAndRotationObject` 旋转参数容器 → 直接使用 `Eigen::Vector3d`
- [ ] `UtInput` 配置解析 → JSON 配置文件
- [ ] `SubModesList` 多模态气动配置 → 可选保留为配置切换机制

#### 4.3 需保留并修改的部分

- [ ] **简化频率（Reduced Frequency）公式**：完整保留 `k = rate/(2·max(V,1.0))` 无量纲化，再乘以参考长度缩放
- [ ] **六分量系数叠加架构**：CL/Cd/CY/Cm/Cn/Cl 各自由静态项 + 动态导数×简化频率叠加
- [ ] **面积模式分支**：翼面面积（wingArea×wingChord/wingSpan）vs 显式参考面积（refArea×refLength）
- [ ] **空表保护**：所有查表前检查 nullptr → 查表为空返回 0.0 系数
- [ ] **面积缩放因子 R²**：`radiusFactor * radiusFactor` 用于非翼面飞行器

#### 4.4 新增辅助代码

- [ ] `InterpTable3D` 类：三维线性插值（α×β×Mach）
- [ ] `InterpTable2D` 类：二维双线性插值（α×Mach 或 β×Mach）
- [ ] `AeroTableSet` 结构体：封装 20+ 张气动数据表的指针集合
- [ ] `WingGeometry` 结构体：封装弦长/翼展/面积/参考面积/参考长度

### 5. 接口详细定义（API）

#### 5.1 函数：`RigidBodyAeroModel::calculateAero`

| 项目 | 说明 |
|------|------|
| **签名** | `AeroOutput calculateAero(const AeroInput& input) const;` |
| **输入** | `AeroInput` 结构体（dyn_pressure, mach, speed, alpha, beta, alpha_dot, beta_dot, angular_rates, radius_factor） |
| **输出** | `AeroOutput` 结构体：`force_N`（气动力矢量 [L,D,Y], N）、`moment_Nm`（气动力矩矢量 [Mx,My,Mz], N·m） |
| **前置条件** | `input.speed_mps > 0`（内部取 `max(speed, 1.0)` 防除零）；所有表已加载（空表返回 0） |
| **后置条件** | 无副作用（const 方法，不修改任何内部状态） |
| **复杂度** | O(T) × 查表次数，T = 表维数（3D 表约 6 次 trilinear + 2D 表约 6 次 bilinear + 1D 曲线约 8 次 linear ≈ 总计 O(20×插值)） |

**输入参数详细表**：

| 参数名 | 类型 | 有效范围/约束 | 说明 |
|--------|------|---------------|------|
| `dyn_pressure_pa` | `double` | [0, ∞) Pa | 自由流动压 |
| `mach` | `double` | [0, 10] | 飞行马赫数 |
| `speed_mps` | `double` | (0, ∞) m/s | 真空速（内部下限保护 1.0） |
| `alpha_rad` | `double` | [-π, π] rad | 攻角 |
| `beta_rad` | `double` | [-π/2, π/2] rad | 侧滑角 |
| `alpha_dot_rps` | `double` | 任意 | 攻角变化率 |
| `beta_dot_rps` | `double` | 任意 | 侧滑角变化率 |
| `angular_rates_rps` | `Eigen::Vector3d` | 任意 | [p, q, r] 体轴角速率 |
| `radius_factor` | `double` | (0, ∞) | 几何尺度因子，默认 1.0 |

### 6. 数据类型映射表

| AFSIM 类型 | 目标系统类型 | 头文件/定义位置 | 备注 | 转换代码示例 |
|------------|-------------|----------------|------|-------------|
| `UtTable::Table` (3D) | `InterpTable3D` | `interp_table.h` | 三维 (α,β,Mach) 线性插值 | 自定义类 |
| `UtTable::Table` (2D) | `InterpTable2D` | `interp_table.h` | 二维 (α,Mach) 双线性插值 | 自定义类 |
| `UtTable::Curve` (1D) | `InterpCurve1D` | `interp_curve.h` | 一维线性插值 | 自定义类 |
| `double` (lb) | `double` (N) | — | 力: ×4.44822 | `N = lb * 4.44822` |
| `double` (ft-lbf) | `double` (N·m) | — | 力矩: ×1.35582 | `Nm = ftlb * 1.35582` |
| `double` (lb/ft²) | `double` (Pa) | — | 动压: ×47.8803 | — |
| `double` (ft) | `double` (m) | — | 长度: ×0.3048 | — |
| `double` (ft/s) | `double` (m/s) | — | 速度: ×0.3048 | — |
| `double` (ft²) | `double` (m²) | — | 面积: ×0.092903 | — |
| `UtVec3dX` | `Eigen::Vector3d` | `<Eigen/Dense>` | 矢量 | `Eigen::Vector3d(x,y,z)` |

### 7. 内部状态与生命周期

`RigidBodyAeroModel` 的计算函数 `calculateAero()` 为纯函数（const 方法），所有状态来自初始化阶段加载的配置参数和查表指针。

| 状态变量 | 类型 | 默认值 | 生命周期 | 线程安全 | 备注 |
|----------|------|--------|----------|----------|------|
| `m_wing_chord_m_` | `double` | 0.0 | 对象级（不变） | 是 | 平均气动弦长 MAC |
| `m_wing_span_m_` | `double` | 0.0 | 对象级（不变） | 是 | 翼展 |
| `m_wing_area_m2_` | `double` | 0.0 | 对象级（不变） | 是 | 机翼参考面积 |
| `m_ref_area_m2_` | `double` | 0.0 | 对象级（不变） | 是 | 显式参考面积 |
| `m_ref_length_m_` | `double` | 0.0 | 对象级（不变） | 是 | `sqrt(refArea)` |
| `m_use_ref_area_` | `bool` | false | 对象级（不变） | 是 | 显式参考面积开关 |
| `m_use_reduced_frequency_` | `bool` | true | 对象级（不变） | 是 | 简化频率开关 |
| `m_aero_center_m_` | `Eigen::Vector3d` | (0,0,0) | 对象级（不变） | 是 | 气动中心位置 |
| `m_table_cl_3d_` | `InterpTable3D*` | nullptr | 对象级（不变） | 是 | 升力系数静态 3D 表 |
| `m_table_cd_3d_` | `InterpTable3D*` | nullptr | 对象级（不变） | 是 | 阻力系数静态 3D 表 |
| `m_table_cy_3d_` | `InterpTable3D*` | nullptr | 对象级（不变） | 是 | 侧力系数静态 3D 表 |
| `m_table_cm_3d_` | `InterpTable3D*` | nullptr | 对象级（不变） | 是 | 俯仰力矩系数静态 3D 表 |
| `m_table_cn_3d_` | `InterpTable3D*` | nullptr | 对象级（不变） | 是 | 偏航力矩系数静态 3D 表 |
| `m_table_cl_3d_` | `InterpTable3D*` | nullptr | 对象级（不变） | 是 | 滚转力矩系数静态 3D 表 |
| `m_table_clq_2d_` ~ 等 6 张 2D 导数表 | `InterpTable2D*` | nullptr | 对象级（不变） | 是 | 动态导数 2D 表 |
| `m_curve_cmq_1d_` ~ 等 8 条 1D 曲线 | `InterpCurve1D*` | nullptr | 对象级（不变） | 是 | 动态导数 1D 曲线 |

- **是否需要 `reset()` 函数**：否 — 无运行时可变状态
- **拷贝/移动行为**：深拷贝（需拷贝所有查表对象）；或使用 `std::shared_ptr` 共享表数据
- **初始化要求**：构造后必须调用 `loadConfig()` 加载气动数据表和几何参数

### 8. 错误处理策略

| 异常场景 | 检测条件 | 处理方式 | 返回/错误码 |
|----------|----------|----------|-------------|
| 速度为零（除零保护） | `speed_mps < 1.0` | 内部取 `max(speed, 1.0)` 作为分母 | 有效简化频率值 |
| 查表为空（未配置导数） | 指针 == nullptr | 对应系数项返回 0.0（不贡献力/力矩增量） | 部分零输出 |
| 查表输入越界（α/β/Mach） | 插值引擎检测 | 边界钳位（clamp to nearest） | 边界值 |
| 翼面几何参数为 0 | 初始化检查 | 若 `wing_area <= 0` 且 `ref_area <= 0`，打印严重警告 | 所有力/力矩 = 0 |
| 非翼面飞行器无参考面积 | `m_use_ref_area_ == false` 且 `wing_area == 0` | 启用参考面积模式 | 正常（参考面积模式） |
| 配置解析失败 | 初始化阶段 | 抛出 `std::runtime_error` 或返回 false | 构造失败 |

### 9. 风险与未决问题

- **技术风险**：20+ 张气动数据表为飞行器特有数据（通常来自风洞试验或 CFD），AFSIM 默认数据表仅供开发测试——需用户提供目标飞行器的真实气动数据
- **技术风险**：3D 和 2D 插值的精度影响气动力的准确性；对于高超声速区域（Mach > 5），线性插值可能不够精确，需评估是否采用 Akima 或 Cubic Spline 插值
- **技术风险**：简化频率公式 `k = rate/(2V)` 在极低速下（V ≈ 0）产生大值；虽已做 `max(V, 1.0)` 保护，但低速段气动模型物理意义减弱
- **待确认**：是否需要支持多模态气动构型切换（如襟翼位置、外挂构型）？初期可跳过，后续扩展

### 10. 人工确认

请逐项勾选确认：

- [ ] 耦合评估合理
- [ ] 接口适配方案可行
- [ ] 数据类型映射正确
- [ ] 内部状态管理设计合理
- [ ] 错误处理策略完整
- [ ] 测试策略与用例充分

**修改要求**（若有）：  
______________________________________________  

**确认人**：__________  
**确认日期**：__________  


---

## FU-003：六自由度积分器（source: afsim）

| 属性 | 内容 |
|------|------|
| **关联需求** | REQ-001 |
| **优先级** | 高 |
| **来源类型** | `afsim` |
| **设计版本** | v1.0 draft |
| **设计日期** | 2026-06-18 |
| **功能描述** | 使用 Heun 预测-校正法（二阶Runge-Kutta）对无人机进行六自由度时间推进。将合外力（推力+气动力+重力）和合外力矩转化为线加速度和角加速度，通过四元数姿态积分和欧拉转动方程（含完整转动惯量张量 I_xx/I_yy/I_zz/I_xz）更新飞行状态（位置、速度、姿态四元数、角速度）。 |
| **AFSIM 源位置** | `wsf_six_dof/source/WsfRigidBodySixDOF_Integrator.hpp:25-76 (RigidBodyIntegrator)` / `WsfRigidBodySixDOF_Integrator.cpp:44-141 (Update)` / `WsfSixDOF_Integrator.hpp:30-52 (Integrator 基类)` / `WsfSixDOF_Integrator.cpp:31-161 (PropagateTranslation/PropagateRotation)` |
| **源码行数** | Update ~100行 + CalculateFM ~150行 + PropagateUsingFM ~100行 + PropagateTranslation ~70行 + PropagateRotation ~55行，合计约 475 行 |
| **迁移策略** | Clean-room 重实现（仅参考功能描述和算法卡片，不直接复制代码） |
| **风险评估** | 中 |

---

### 1. 功能概述

该功能单元是整个六自由度仿真的核心。它采用 Heun 预测-校正法（显式二阶 Runge-Kutta）在每帧内执行两次力/力矩评估和两次状态推进，取平均力/力矩完成最终状态更新。积分器同时处理平动（牛顿第二定律 → 位置/速度更新）和转动（欧拉转动方程 → 角速率更新 + 四元数姿态积分 → 姿态更新），并包含力/力矩限幅（防止加速度尖峰发散）和四元数归一化（防止长时间积分漂移）等数值保护。

该 FU 是仿真主循环的核心：仿真引擎每帧 → `RigidBodyMover::Update()` → `RigidBodyIntegrator::Update()` → Heun 法流程 → 输出更新后的完整运动学状态。

迁移必要性：目标系统为空系统，无任何运动学积分代码。FU-003 是最高优先级，因为它是整个仿真流水线的核心——其他 FU（推进、气动、SAS）的输出都需要通过积分器进行时间推进。

### 2. 参考来源与算法依据

#### 2.1 AFSIM 参考实现

| 属性 | 值 |
|------|----|
| 源函数 | `RigidBodyIntegrator::Update` / `CalculateFM` / `PropagateUsingFM` / `UpdateUsingFM` / `PropagateRotation` |
| 源文件 | `wsf_six_dof/source/WsfRigidBodySixDOF_Integrator.cpp:44-448` / `WsfSixDOF_Integrator.cpp:20-161` |
| 源码行数 | 约 475 行（5个核心方法） |
| 依赖的 AFSIM 类型/宏 | `KinematicState`（运动学状态容器）、`MassProperties`（质量特性）、`ForceAndMomentsObject`（F&M容器）、`UtVec3dX`、`UtQuaternion`、`UtDCM`、`FreezeFlags`、`UtMath::cGravitationAccel_mps2` |
| 依赖的全局变量/常量 | `cMaxG=1000`（力限幅）、`cMaxOmegaDot_rps≈62832`（力矩限幅）、`cGravitationAccel_mps2=9.80665` |
| 使用的第三方库 | 无 |

#### 2.2 核心算法摘要

**Heun 预测-校正法完整流程**（12步）：

1. **计算当前质量特性**：因燃油消耗，质心位置可能变化
2. **保存初始状态快照**：`initialState = *kinematicState`（深拷贝）
3. **预测步 T0**：`FM_T0 = CalculateFM(initialState, t0)` —— 计算 T0 时刻力/力矩
4. **推进步 T0**：`PropagateUsingFM(tempState, FM_T0)` —— 用 T0 的 F&M 推进到中间态
5. **预测步 T1**：`FM_T1 = CalculateFM(tempState, t1)` —— 在中间态重新计算力/力矩
6. **推进步 T1**：`PropagateUsingFM(tempState, FM_T1)` —— 用 T1 的 F&M 再次推进
7. **平均 F&M**：`FM_avg = (FM_T0 + FM_T1) / 2` —— 两点导数的算术平均
8. **起落架摩擦检查**：若起落架摩擦保持静止，跳过状态更新（初期迁移可省略起落架）
9. **最终校正步**：`UpdateUsingFM(initialState, FM_avg)` —— 用平均 F&M 和旧初始状态完成最终推进
10. **测试模式**：移除攻角（可选，迁移时可省略）
11. **更新气动状态**：计算 α̇, β̇ 等气动导数
12. **计算二次参数**：辅助输出参数

**平动推进**（`PropagateTranslation`）：
```
a_body = F_total_body / m × g₀                               // 体轴加速度 (m/s²)
a_WCS = R_body2WCS × a_body                                   // 体轴→世界坐标系
v_new = v_old + a_WCS × dt                                    // 速度更新
r_new = r_old + v_old×dt + 0.5×a_WCS×dt²                     // 位置更新（匀加速）
```

**转动推进**（`PropagateRotation`）：
```
ṗ = M_x / I_xx, q̇ = M_y / I_yy, ṙ = M_z / I_zz                 // 欧拉转动方程（对角惯量）
ω_new = ω_old + ω̇ × dt                                        // 角速率欧拉步进
q_att = QuatFromDCM(R)                                        // DCM→姿态四元数
q_rate = SetRate(q_att, ω)                                    // 角速率→速率四元数
q_att_new = q_att + q_rate × dt                               // 四元数推进
q_att_new ← Normalize(q_att_new)                              // 四元数归一化（关键步骤）
R_new = DCMFromQuat(q_att_new)                                // 四元数→新 DCM
```

**力/力矩限幅**（数值保护）：
```
|F| ≤ m × 1000g     // 最大过载 1000g
|M_i| ≤ I_ii × 62832 rad/s²  // 最大角加速度 100 rev/s²
```
限幅方式：若超过上限，等比例缩放力/力矩矢量。

**简单偏航阻尼器**（可选）：
```
r_new = β / dt   （仅当离地且启用时）
```
初期迁移可省略此功能。

### 3. 耦合度与依赖分析

| 评估维度 | 说明 |
|----------|------|
| 框架耦合 | 中-高 — 与多个 AFSIM 基础设施类耦合：`KinematicState`（运动学状态）、`MassProperties`（质量特性）、`ForceAndMomentsObject`（力/力矩容器含参考点自动转换）、`Mover/RigidBodyMover`（运动器抽象基类）、`RigidBodyLandingGear`（起落架）。迁移时需全部替换。 |
| 数据耦合 | 高 — 依赖气动模型（`CalculateAeroBodyForceAndMoments`）、推进模型（`CalculatePropulsionFM`）、起落架模型（`CalculateLandingGearFM`）三个外部子系统提供力/力矩。迁移时通过接口注入。 |
| 控制耦合 | 中 — 依赖仿真引擎的主循环调用 `Update()`，内部通过 `CalculateFM` 聚合各子系统力/力矩。不依赖全局状态机。 |
| 外部依赖 | 低 — 仅依赖数学库（向量/矩阵/四元数运算），无数据库/网络/硬件。 |

**综合等级**：中-高  
**剥离策略**：定义清晰的 `IForceProvider` 抽象接口（气动/推进/起落架均实现此接口），积分器通过依赖注入获取各力源；`KinematicState` 替换为 `RigidBodyState` 结构体；`ForceAndMomentsObject` 的参考点自动转换逻辑需完整重实现（`operator+=` 隐式力矩转换）。

### 4. 实现方案

#### 4.1 接口转换

| 原 AFSIM 接口 | 目标系统接口 | 转换说明 |
|---------------|--------------|----------|
| `RigidBodyIntegrator::Update(simTime_ns, dt_sec)` | `void integrate(double dt, RigidBodyState& state, const MassProperties& mass, IForceProvider& aero, IForceProvider& propulsion, IForceProvider& gravity)` | 时间戳用秒；状态通过引用传入/更新；力源通过接口注入 |
| `CalculateFM(state, simTime, dt, out FM_RP, out FM_CM)` | `ForceMoments calculateFM(const RigidBodyState& state, double dt)` | 聚合气动+推进+重力 |
| `PropagateUsingFM(state, mass, dt, FM_RP, FM_CM)` | `void propagateUsingFM(RigidBodyState& state, const MassProperties& mass, double dt, const ForceMoments& fm)` | 限幅+平动+转动 |
| `PropagateTranslation(state, bodyAccel, dt)` | `void propagateTranslation(RigidBodyState& state, const Eigen::Vector3d& body_accel, double dt)` | 平动推进 |
| `PropagateRotation(state, omegaDot, dt)` | `void propagateRotation(RigidBodyState& state, const Eigen::Vector3d& omega_dot, double dt)` | 转动推进+四元数归一化 |

- **源接口**（AFSIM）：
  ```cpp
  void Update(int64_t aSimTime_nanosec, double aDeltaT_sec);
  ```
- **目标接口**：
  ```cpp
  void integrate(double dt, RigidBodyState& state,
                 const MassProperties& mass,
                 IForceProvider& aero_provider,
                 IForceProvider& propulsion_provider,
                 IForceProvider& gravity_provider);
  ```

#### 4.2 需移除的 AFSIM 专属代码

- [ ] `KinematicState` 运动学状态容器 → 替换为 `RigidBodyState` 结构体
- [ ] `MassProperties`（含 lbm/slug-ft² 单位）→ 替换为 SI 单位 `MassProperties`
- [ ] `ForceAndMomentsObject` 的 `operator+=` 隐式参考点转换 → 显式参考点→质心力矩转换函数
- [ ] `Mover` / `RigidBodyMover` 运动器基类 → 移除，积分器直接操作 `RigidBodyState`
- [ ] `FreezeFlags` 冻结标志 → 可选保留为简单位掩码
- [ ] `RigidBodyLandingGear` 起落架 → 初期省略，后续扩展
- [ ] `ut::log::error()` 日志 → `std::cerr`
- [ ] `utils::cEPSILON_SIMTIME_SEC` → 自定义 `constexpr double kEpsilon = 1e-12`

#### 4.3 需保留并修改的部分

- [ ] **Heun 预测-校正主控流程**：12步流程完整保留（保存初始态→预测T0→推进T0→预测T1→推进T1→平均FM→校正步→辅助更新），省略起落架步骤
- [ ] **平动推进公式**：F/m·g₀ → a_body, DCM旋转 → a_WCS, 匀加速位置更新
- [ ] **转动推进公式**：欧拉转动方程（对角惯量）→ ω̇, ω更新, 四元数姿态积分+归一化
- [ ] **力/力矩限幅**：过载限制 1000g + 角加速度限制 100 rev/s²
- [ ] **参考点→质心力矩转换**：`M_CM = M_RP + (r_RP - r_CM) × F_RP`
- [ ] **四元数归一化**：每次转动推进后执行

#### 4.4 新增辅助代码

- [ ] `RigidBodyState` 结构体：位置/速度/姿态四元数/角速率/气动状态（α,β,Mach,α̇,β̇）
- [ ] `MassProperties` 结构体（SI单位）：质量(kg)/质心偏移(m)/转动惯量(kg·m²)
- [ ] `ForceMoments` 结构体：力矢量(N)+力矩矢量(N·m)+参考点(m)，含参考点→质心转换方法
- [ ] `IForceProvider` 抽象接口：`ForceMoments calculateForce(const RigidBodyState&, double dt) = 0`
- [ ] `RigidBodyIntegrator` 类：封装 Heun 法全流程

### 5. 接口详细定义（API）

#### 5.1 结构体：`RigidBodyState`

```cpp
struct RigidBodyState {
    Eigen::Vector3d    position_m;         // WCS 位置 [x, y, z] (m)
    Eigen::Vector3d    velocity_mps;       // WCS 速度 [Vx, Vy, Vz] (m/s)
    Eigen::Quaterniond attitude_quat;      // 姿态四元数 (body→WCS)
    Eigen::Vector3d    angular_velocity_rps; // 体轴角速率 [p, q, r] (rad/s)
    // 气动状态（辅助）
    double alpha_rad = 0.0;   // 攻角
    double beta_rad  = 0.0;   // 侧滑角
    double mach      = 0.0;   // 马赫数
    double alpha_dot_rps = 0.0;
    double beta_dot_rps  = 0.0;
};
```

#### 5.2 函数：`RigidBodyIntegrator::integrate`

| 项目 | 说明 |
|------|------|
| **签名** | `void integrate(double dt, RigidBodyState& state, const MassProperties& mass, IForceProvider& aero, IForceProvider& propulsion, IForceProvider& gravity);` |
| **输入** | `dt`（步长,s）、`state`（当前状态, 引用被更新）、`mass`（质量特性）、`aero/propulsion/gravity`（力源接口） |
| **输出** | `state` 被更新为新时刻的运动学状态（位置/速度/姿态/角速率）；四元数已归一化 |
| **前置条件** | `dt > 0`, `mass.mass_kg > 0`, 三个力源非空 |
| **后置条件** | `state.attitude_quat.norm() ≈ 1.0`（误差 < 1e-12） |
| **复杂度** | O(1) + 2次力源评估（气动+推进+重力各2次） |

#### 5.3 函数：`RigidBodyIntegrator::propagateTranslation`

| 项目 | 说明 |
|------|------|
| **签名** | `static void propagateTranslation(RigidBodyState& state, const Eigen::Vector3d& body_accel_mps2, const Eigen::Matrix3d& dcm, double dt);` |
| **输入** | `body_accel_mps2`（体轴加速度）、`dcm`（body→WCS 方向余弦矩阵）、`dt`（步长） |
| **输出** | 更新 `state.position_m` 和 `state.velocity_mps` |
| **前置条件** | `dt > 0` |
| **复杂度** | O(1) |

#### 5.4 函数：`RigidBodyIntegrator::propagateRotation`

| 项目 | 说明 |
|------|------|
| **签名** | `static void propagateRotation(RigidBodyState& state, const Eigen::Vector3d& omega_dot_rps2, const Eigen::Vector3d& inertia_diag, double dt);` |
| **输入** | `omega_dot_rps2`（角加速度矢量 [ṗ,q̇,ṙ]）、`inertia_diag`（转动惯量对角线 [Ixx,Iyy,Izz]）、`dt` |
| **输出** | 更新 `state.angular_velocity_rps` 和 `state.attitude_quat` |
| **前置条件** | `dt > 0`, 惯量对角线 > 0 |
| **后置条件** | 四元数已归一化 |
| **复杂度** | O(1) |

### 6. 数据类型映射表

| AFSIM 类型 | 目标系统类型 | 头文件/定义位置 | 备注 |
|------------|-------------|----------------|------|
| `KinematicState` | `RigidBodyState` | `rigid_body_state.h` | 自定义结构体 |
| `MassProperties` | `MassProperties` (SI) | `mass_properties.h` | 自定义结构体 |
| `ForceAndMomentsObject` | `ForceMoments` | `force_moments.h` | 自定义结构体，含参考点→质心转换 |
| `UtVec3dX` | `Eigen::Vector3d` | `<Eigen/Dense>` | — |
| `UtQuaternion` | `Eigen::Quaterniond` | `<Eigen/Geometry>` | 顺序 (w,x,y,z) |
| `UtDCM` | `Eigen::Matrix3d` | `<Eigen/Geometry>` | — |
| `double` (lbf) | `double` (N) | — | ×4.44822 |
| `double` (ft-lbf) | `double` (N·m) | — | ×1.35582 |
| `double` (lbm) | `double` (kg) | — | ×0.453592 |
| `double` (slug-ft²) | `double` (kg·m²) | — | ×1.35582 |
| `cMaxG = 1000.0` | `kMaxG = 1000.0` | `integrator_constants.h` | 不变 |
| `cMaxOmegaDot_rps ≈ 62831.85` | `kMaxOmegaDot = 62831.85` | `integrator_constants.h` | 不变 |
| `cGravitationAccel_mps2 = 9.80665` | `kGravity = 9.80665` | `integrator_constants.h` | 不变 |

### 7. 内部状态与生命周期

`RigidBodyIntegrator` 类本身不持有帧间持久化状态（`mVehicle` 指针除外）。所有中间变量（`initialState`, `tempState`, `FM_T0`, `FM_T1`, `FM_avg`）均为局部变量。

| 状态变量 | 类型 | 默认值 | 生命周期 | 线程安全 | 备注 |
|----------|------|--------|----------|----------|------|
| `m_aero_provider_` | `IForceProvider*` | nullptr | 对象级 | 否 | 气动模型接口 |
| `m_propulsion_provider_` | `IForceProvider*` | nullptr | 对象级 | 否 | 推进系统接口 |
| `m_gravity_provider_` | `IForceProvider*` | nullptr | 对象级 | 否 | 重力计算接口 |
| `m_enable_force_clamp_` | `bool` | true | 对象级 | 否 | 力/力矩限幅开关 |
| `m_enable_simple_yaw_damper_` | `bool` | false | 对象级 | 否 | 简单偏航阻尼器（可选） |

`RigidBodyState`（外部传入/更新）包含所有运动学状态：

| 状态变量 | 类型 | 默认值 | 物理含义 |
|----------|------|--------|----------|
| `position_m` | `Eigen::Vector3d` | (0,0,0) | WCS 位置 |
| `velocity_mps` | `Eigen::Vector3d` | (0,0,0) | WCS 速度 |
| `attitude_quat` | `Eigen::Quaterniond` | Identity | 姿态四元数 |
| `angular_velocity_rps` | `Eigen::Vector3d` | (0,0,0) | 体轴角速率 |

- **是否需要 `reset()` 函数**：是 — 通过外部重置 `RigidBodyState` 实现
- **拷贝/移动行为**：`RigidBodyState` 支持浅拷贝（Eigen 类型值语义）
- **初始化要求**：积分前需设置初始 `RigidBodyState`、`MassProperties` 和力源接口

### 8. 错误处理策略

| 异常场景 | 检测条件 | 处理方式 | 返回/错误码 |
|----------|----------|----------|-------------|
| 质量 ≤ 0 | `mass.mass_kg <= 0` | 跳过推进，直接返回（不更新状态） | 状态不变 |
| 转动惯量对角线 ≤ 0 | `I_xx/I_yy/I_zz <= 0` | 跳过转动推进，仅保留平动推进 | 部分更新 |
| 速度过大导致四元数发散 | `attitude_quat.norm() < 1e-6` | 重置为单位四元数，打印错误 | 重置姿态 |
| 力/力矩幅值异常（过大） | 限幅检查 | 等比例缩放到上限 | 限幅后力/力矩 |
| 四元数归一化漂移 | 每次转动推进后检查 | `attitude_quat.normalize()` | 归一化四元数 |
| 力源接口为空 | nullptr 检查 | 跳过对应力源（贡献零力/力矩） | 部分输出 |
| `dt ≤ 0` | 入口检查 | 直接返回，不更新状态 | 状态不变 |

### 9. 风险与未决问题

- **技术风险**：欧拉转动方程的对角惯量简化（忽略 I_xz 交叉项）在某些飞行器构型（如细长体导弹）下可能不够精确——后续可扩展为完整转动惯量张量求逆
- **技术风险**：Heun 法为二阶精度，对于高频振动（如气动弹性）可能不够——但六自由度刚体运动的主要频率远小于步长倒数，二阶精度足够
- **技术风险**：旋转地球效应（离心+科里奥利加速度）在初期迁移中省略——对于短距离/短时飞行仿真影响可忽略；若需要，后续在 `propagateTranslation` 中添加
- **待确认**：起落架模型是否需要在初期实现？若不需要（先做空中飞行测试），可完全省略起落架摩擦检查

### 10. 人工确认

请逐项勾选确认：

- [ ] 耦合评估合理
- [ ] 接口适配方案可行
- [ ] 数据类型映射正确
- [ ] 内部状态管理设计合理
- [ ] 错误处理策略完整
- [ ] 测试策略与用例充分

**修改要求**（若有）：  
______________________________________________  

**确认人**：__________  
**确认日期**：__________  


---

## FU-004：姿态控制系统 SAS（source: afsim）

| 属性 | 内容 |
|------|------|
| **关联需求** | REQ-001 |
| **优先级** | 低 |
| **来源类型** | `afsim` |
| **设计版本** | v1.0 draft |
| **设计日期** | 2026-06-18 |
| **功能描述** | 实现三通道（滚转/俯仰/偏航）控制-稳定解耦姿态控制系统。将自动驾驶仪输出的控制指令（升降舵/副翼/方向舵偏转）转化为角加速度输出，含控制项（一阶指令跟踪）、稳定项（俯仰/偏航二阶临界阻尼 + 一阶滚转滞后）和各通道独立限幅保护。 |
| **AFSIM 源位置** | `wsf_six_dof/source/WsfPointMassSixDOF_Integrator.cpp:270-343 (CalculateStabilityAugmentation)` / `WsfPointMassSixDOF_FlightControlSystem.hpp (PointMassFlightControlSystem)` |
| **源码行数** | CalculateStabilityAugmentation ~73 行（内联在 PointMassIntegrator::CalculateAcceleration 中） |
| **迁移策略** | Clean-room 重实现（仅参考功能描述和算法卡片，不直接复制代码） |
| **风险评估** | 低 |

---

### 1. 功能概述

该功能单元实现三通道（滚转/俯仰/偏航）控制-稳定解耦的姿态控制系统（Stability Augmentation System, SAS）。核心设计是将旋转角加速度分解为两个独立项：

1. **控制项（一阶指令跟踪）**：将飞控系统输出的期望体轴角速率指令通过一阶差分转化为角加速度，各轴独立限幅
2. **稳定增稳项**：模拟飞行器固有静稳定性和气动阻尼——俯仰/偏航通道使用二阶临界阻尼系统（ζ=1）将攻角/侧滑角驱回零，滚转通道使用一阶滞后平滑

两项叠加得到总旋转加速度，输出给积分器进行转动推进。SAS 还通过质量比率（m/m_base）缩放控制限幅和稳定化频率——质量越小（燃油消耗后），飞行器越敏捷。

在仿真流程中，该 FU 位于积分器的 `CalculateAcceleration` 阶段，在气动力/力矩计算之后，在转动推进之前。

迁移必要性：目标系统为空系统，无任何飞行控制系统代码。FU-004 优先级最低，因为初期测试可用直接角加速度输入替代 SAS。

### 2. 参考来源与算法依据

#### 2.1 AFSIM 参考实现

| 属性 | 值 |
|------|----|
| 源函数 | `PointMassIntegrator::CalculateStabilityAugmentation` |
| 源文件 | `wsf_six_dof/source/WsfPointMassSixDOF_Integrator.cpp:270-343` |
| 源码行数 | ~73 行（内联代码） |
| 依赖的 AFSIM 类型/宏 | `KinematicState`、`MassProperties`（含 baseMass）、`PointMassFlightControlSystem`（飞控系统，输出期望角速率）、`ForceAndRotationObject`（含旋转限幅和稳定化频率） |
| 依赖的全局变量/常量 | `cREFERENCE_GRAV_ACCEL_MPS2 = 9.80665`、`DEG_PER_RAD`（度↔弧度转换） |
| 使用的第三方库 | 无 |

#### 2.2 核心算法摘要

**总旋转加速度 = 控制项 + 稳定项**：
```
α_total = α_controls + α_stability
```

**控制项 — 一阶指令跟踪**：
```
ω_cmd_rps = flightControls->GetBodyRateCommands_dps() × DEG_TO_RAD
α_controls = (ω_cmd_rps - ω_current_rps) / moverDt
α_limit = α_limit_base / massFraction                        // 质量越小限幅越大
for i in {roll,pitch,yaw}: α_controls[i] = clamp(α_controls[i], ±|α_limit[i]|)
```

**质量比率**：
```
massFraction = m_current / m_base
```

**俯仰通道 — 二阶临界阻尼（ζ=1）→ 驱 α→0**：
```
ω_n_pitch = ω_n_pitch_base / massFraction
α_pitch_stab = -α × ω_n_pitch² - 2 × ω_n_pitch × α̇
```
恢复项 `-α·ω_n²` + 阻尼项 `-2·ω_n·α̇`。

**偏航通道 — 二阶临界阻尼（ζ=1）→ 驱 β→0**：
```
ω_n_yaw = ω_n_yaw_base / massFraction
α_yaw_stab = -β × ω_n_yaw² - 2 × ω_n_yaw × β̇
// 最终输出取反：-α_yaw_stab
```

**滚转通道 — 一阶滞后平滑 → 驱 p→0**：
```
weight = ω_n_roll × dt / (1 + ω_n_roll × dt)
p_expected = (1 - weight) × p
α_roll_stab = (p_expected - p) / dt
```
等效于低通滤波器时间常数 τ = 1/ω_n_roll。

**稳定性数值限幅**（防止大时间步长发散）：
```
α_roll_max  = |p / dt|
α_pitch_max = |2/dt² × (-α - α̇ × dt)|
α_yaw_max   = |2/dt² × (-β - β̇ × dt)|
```

### 3. 耦合度与依赖分析

| 评估维度 | 说明 |
|----------|------|
| 框架耦合 | 中 — 依赖 `PointMassFlightControlSystem`（飞控系统，提供期望角速率指令）和 `PointMassAeroCoreObject`（气动模型，提供旋转限幅和稳定化频率基准）。这两个依赖均可通过接口抽象。 |
| 数据耦合 | 低 — 仅需 `KinematicState` 的 α/β/α̇/β̇/p/q/r 和 `MassProperties` 的 m/m_base。数据量小且简单。 |
| 控制耦合 | 低 — SAS 为纯计算函数，不修改外部状态，不依赖全局状态机。 |
| 外部依赖 | 低 — 仅依赖基本数学运算和 `std::clamp`。 |

**综合等级**：低  
**剥离策略**：定义 `IFlightControlSystem` 接口（提供期望角速率指令）和 `IAeroStabilityParams` 接口（提供旋转限幅和稳定化频率基准）；SAS 核心计算独立为 `StabilityAugmentationSystem` 类。

### 4. 实现方案

#### 4.1 接口转换

| 原 AFSIM 接口 | 目标系统接口 | 转换说明 |
|---------------|--------------|----------|
| `CalculateStabilityAugmentation(aState, massProperties, rotationalAccelLimits_rps2, stabilizingFrequency_rps, flightControls, ...)` | `Eigen::Vector3d computeAngularAcceleration(const RigidBodyState& state, const MassProperties& mass, const SASParams& params, const IFlightControlSystem* fcs)` | 参数打包；返回值简化 |

- **源接口**（AFSIM 内联）：
  ```cpp
  // 内联在 PointMassIntegrator::CalculateAcceleration() 中
  // 输入: aState, massProperties, rotationalAccelLimits_rps2,
  //       stabilizingFrequency_rps, flightControls
  // 输出: aRotationalAccel_mps2 (控制+稳定叠加)
  ```
- **目标接口**：
  ```cpp
  Eigen::Vector3d computeAngularAcceleration(
      const RigidBodyState& state,          // 飞行器状态
      const MassProperties& mass,           // 质量特性 (含 base_mass_kg)
      const SASParams& params,              // SAS 配置参数
      const IFlightControlSystem* fcs);     // 飞控系统接口 (可为nullptr→仅稳定项)
  ```

#### 4.2 需移除的 AFSIM 专属代码

- [ ] `KinematicState` → `RigidBodyState`（与 FU-003 共享）
- [ ] `MassProperties`（含 baseMass）→ `MassProperties` SI 版本
- [ ] `PointMassFlightControlSystem::GetBodyRateCommands_dps()` → `IFlightControlSystem` 接口
- [ ] `ForceAndRotationObject` 旋转参数容器 → `SASParams` 结构体
- [ ] `UtMath::Limit()` → `std::clamp()`
- [ ] `UtMath::cDEG_PER_RAD / cRAD_PER_DEG` → `M_PI / 180.0` / `180.0 / M_PI`

#### 4.3 需保留并修改的部分

- [ ] **控制+稳定解耦架构**：`α_total = α_controls + α_stability`
- [ ] **一阶指令跟踪公式**：`α_controls = (ω_cmd - ω_current) / dt`
- [ ] **俯仰/偏航二阶临界阻尼公式**：`-α·ω_n² - 2·ω_n·α̇`
- [ ] **滚转一阶滞后平滑公式**：`weight = ω_n·dt/(1+ω_n·dt)`
- [ ] **质量比率缩放**：`massFraction = m/m_base` → 控制限幅和稳定化频率
- [ ] **各通道独立限幅**：控制限幅（α_limit = α_limit_base/massFraction）+ 稳定项数值限幅
- [ ] **偏航符号翻转**：`-α_yaw_stab`

#### 4.4 新增辅助代码

- [ ] `SASParams` 结构体：三通道旋转限幅基准 + 三通道稳定化频率基准
- [ ] `IFlightControlSystem` 接口：`Eigen::Vector3d getBodyRateCommands_rps() const = 0`
- [ ] `StabilityAugmentationSystem` 类：封装三通道 SAS 计算

### 5. 接口详细定义（API）

#### 5.1 结构体：`SASParams`

```cpp
struct SASParams {
    // 旋转加速度限幅基准（来自气动模型）
    Eigen::Vector3d rotational_accel_limit_rps2 = {10.0, 10.0, 10.0}; // [roll, pitch, yaw]
    // 稳定化固有频率基准（来自气动模型）
    Eigen::Vector3d stabilizing_frequency_rps  = {1.0, 2.0, 2.0};   // [roll, pitch, yaw]
};
```

#### 5.2 函数：`StabilityAugmentationSystem::computeAngularAcceleration`

| 项目 | 说明 |
|------|------|
| **签名** | `Eigen::Vector3d computeAngularAcceleration(const RigidBodyState& state, const MassProperties& mass, const SASParams& params, const IFlightControlSystem* fcs, double mover_dt);` |
| **输入** | `state`（飞行器状态）、`mass`（含 base_mass_kg）、`params`（SAS 配置）、`fcs`（飞控接口，可为 nullptr）、`mover_dt`（运动器步长） |
| **输出** | `Eigen::Vector3d` — 总旋转角加速度 [α_roll, α_pitch, α_yaw] (rad/s²)，已限幅 |
| **前置条件** | `mover_dt > 0`, `mass.mass_kg > 0`, `mass.base_mass_kg > 0` |
| **后置条件** | 输出各分量 ≤ 各自限幅值 |
| **复杂度** | O(1) |

#### 5.3 函数：`StabilityAugmentationSystem::computeStabilityTerm`

| 项目 | 说明 |
|------|------|
| **签名** | `static Eigen::Vector3d computeStabilityTerm(const RigidBodyState& state, const SASParams& params, double mass_fraction, double mover_dt);` |
| **输入** | `state`（α/β/α̇/β̇/p）、`params`、`mass_fraction`（m/m_base）、`mover_dt` |
| **输出** | `Eigen::Vector3d` — 稳定增稳角加速度（限幅后） |
| **前置条件** | `mover_dt > 0` |
| **复杂度** | O(1) |

### 6. 数据类型映射表

| AFSIM 类型 | 目标系统类型 | 头文件/定义位置 | 备注 |
|------------|-------------|----------------|------|
| `KinematicState` | `RigidBodyState` | `rigid_body_state.h` | 与 FU-003 共享 |
| `MassProperties` (含 baseMass) | `MassProperties` | `mass_properties.h` | 新增 `base_mass_kg` 字段 |
| `ForceAndRotationObject` (旋转参数) | `SASParams` | `sas_params.h` | 自定义结构体 |
| `PointMassFlightControlSystem` | `IFlightControlSystem` | `flight_control_interface.h` | 抽象接口 |
| `double` (deg/s) | `double` (rad/s) | — | ×π/180 |
| `UtVec3dX` | `Eigen::Vector3d` | `<Eigen/Dense>` | — |

### 7. 内部状态与生命周期

SAS 算法本身不持有帧间持久化状态——所有输入来自飞行器状态或外部接口，通过计算函数直接输出。

| 状态变量 | 类型 | 默认值 | 生命周期 | 线程安全 | 备注 |
|----------|------|--------|----------|----------|------|
| `m_params_` | `SASParams` | 默认值 | 对象级 | 是 | SAS 配置参数 |
| `m_fcs_` | `IFlightControlSystem*` | nullptr | 对象级 | 否 | 飞控系统接口 |

`IFlightControlSystem` 接口的典型实现可能持有内部状态（操纵杆曲线等），但不属于 SAS 的职责范围。

- **是否需要 `reset()` 函数**：否 — 无运行时可变状态需要重置
- **拷贝/移动行为**：允许浅拷贝（仅配置参数和接口指针）
- **初始化要求**：构造后调用 `setParams()` 设置 SAS 配置；可选调用 `setFlightControlSystem()` 挂载飞控接口

### 8. 错误处理策略

| 异常场景 | 检测条件 | 处理方式 | 返回/错误码 |
|----------|----------|----------|-------------|
| 飞控系统为空（nullptr） | 函数入口检查 | 控制项 = 0（仅稳定项生效，模拟无飞行员输入的自然稳定性） | 仅稳定项输出 |
| 质量 ≤ 0 | `mass_kg <= 0` | 返回零角加速度 | `(0,0,0)` |
| 基准质量 ≤ 0 | `base_mass_kg <= 0` | `massFraction` 设为 1.0（不缩放） | 正常输出 |
| `moverDt ≤ 0` | 入口检查 | 返回零角加速度 | `(0,0,0)` |
| 控制指令超出合理范围 | 限幅检查 | `std::clamp()` 到限幅值 | 限幅后值 |
| 稳定项数值过大（大步长） | 稳定性数值限幅检查 | 限幅到 `|p|/dt` 或 `2/dt²×|-α-α̇×dt|` | 限幅后值 |
| 稳定化频率 ≤ 0 | 入口检查 | 对应通道稳定项 = 0 | 部分零 |
| 输入 NaN 传播 | 无显式检查 | NaN 会直接传播到输出（调用方负责验证输入） | NaN |

### 9. 风险与未决问题

- **技术风险**：稳定化固有频率基准（ω_n）取决于飞行器气动设计——基准值需通过风洞试验或 CFD 获取；AFSIM 默认值可能不适用于目标飞行器型号
- **技术风险**：SAS 设计的"控制-稳定解耦"架构是 PointMass 模型的简化方案，对于真实六自由度飞行器（如 FU-003 的刚体模型），SAS 需要额外的交叉耦合补偿——初期可沿用此简化方案
- **低风险**：所有公式为标准控制理论算法（一阶跟踪、二阶临界阻尼、一阶滞后），实现复杂度低
- **待确认**：SAS 是为 PointMass 模型设计的，应用到 RigidBody 模型（FU-003）时，是否需要在俯仰/偏航通道添加交叉耦合（如偏航引起滚转）——初期不添加，后续按需扩展

### 10. 人工确认

请逐项勾选确认：

- [ ] 耦合评估合理
- [ ] 接口适配方案可行
- [ ] 数据类型映射正确
- [ ] 内部状态管理设计合理
- [ ] 错误处理策略完整
- [ ] 测试策略与用例充分

**修改要求**（若有）：  
______________________________________________  

**确认人**：__________  
**确认日期**：__________  


---

## 修订记录

| 版本 | 日期 | 修改内容 | 修改原因 |
|------|------|----------|----------|
| v0.1 | 2026-06-18 | 初始版本，包含全部 4 个 FU 的迁移设计方案 | 首次生成 |
