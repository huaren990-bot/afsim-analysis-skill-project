# 喷气发动机推力模型 -- 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-jet-engine-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────┐
│                    Engine（引擎基类）                      │
│  发动机通用接口：推力查询、燃油箱绑定、启停控制、可见性标志    │
├──────────────────────────────────────────────────────────┤
│  + GetThrust_lbs() → double                              │
│  + CalculateThrust(dT, alt, dynPress, statPress, ...)     │
│  + UpdateThrust(dT, alt, dynPress, statPress, ...)       │
│  + CheckCurrentFuelTank() → bool                         │
│  + SetFuelTank(name) → bool                              │
│  + Ignite(time) / Shutdown(time)                         │
│  + EngineOperating() / AfterburnerOn() / Contrailing()   │
└──────────────┬───────────────────────────────────────────┘
               │ 继承
               ▼
┌──────────────────────────────────────────────────────────┐
│                    JetEngine（喷气发动机）                  │
│  含 Spool Dynamics + 三层推力查表 + TSFC 燃油消耗          │
├──────────────────────────────────────────────────────────┤
│  + ProcessInput(input) → bool  -- 读取 "jet" 配置块       │
│  + Initialize(simTime) → bool -- 计算有效 TSFC            │
│  - CalculateThrust(dT, alt, dynPress, mach,              │
│      force, fuelRate, fuelBurned, updateData)            │
│  + GetMaximumPotentialThrust_lbs(alt, mach, ...)          │
│  + GetMinimumPotentialThrust_lbs(alt, mach, ...)          │
│  + SetThrottlePosition(pos) / GetThrottlePosition()       │
│  + InjectFuel(on_off) -- 供油开关                         │
└──────────────┬───────────────────────────────────────────┘
               │ 使用
               ▼
┌──────────────────────────────────────────────────────────┐
│                    FuelTank（燃油箱）                      │
│  燃油燃烧/填充/传输的速率限制与 CG 插值                     │
├──────────────────────────────────────────────────────────┤
│  + UpdateFuelBurn(dT, burnRequest, actual, mass, cg)      │
│  + CalculateFuelBurn(dT, burnRequest, actual, mass, cg)   │
│  + GetCurrentFuelQuantity_lbs() → double                 │
│  + FuelFlowPathIntact(propSystem) → bool                 │
└──────────────────────────────────────────────────────────┘
               │ 向上调用
               ▼
┌──────────────────────────────────────────────────────────┐
│                 ThrustProducerObject（推力产生器父对象）     │
│  提供死机阻力面积、油门合成接口                              │
├──────────────────────────────────────────────────────────┤
│  + getThrottleMilSetting() → 0~1                        │
│  + getThrottleAbSetting() → 0~1                          │
│  + getInoperatingDragArea_ft2() → double                 │
│  + getParentPropulsionSystem() → PropulsionSystem*       │
└──────────────────────────────────────────────────────────┘
```

## 2. 核心接口定义

### 2.1 EngineConfig（喷气发动机配置参数）

```cpp
// 描述喷气发动机的全部静态配置参数
// 派生自 Engine 基类的具体类型：JetEngine
struct JetEngineConfig {
    // === 推力表（9 种表格式，优先级：简单曲线 > MachAlt 2D > AltMach 2D）===

    // 简单曲线模式：推力 = f(海拔高度 ft)
    // mIdleThrustTable：Idle 慢车工况推力基准 (lb)
    // mMilThrustTable：Mil  军推工况推力基准 (lb)
    // mABThrustTable：AB   全加力推力基准 (lb)，nullptr 时无加力
    double (*idle_thrust_table)(double alt_ft);  // 1D 拟合曲线
    double (*mil_thrust_table)(double alt_ft);
    double (*ab_thrust_table)(double alt_ft);

    // 改进 2D 表模式 MachAlt：推力 = f(马赫数 mach, 海拔高度 m)
    // mIdleThrustMachAltTable：Idle 推力 2D 表 (lb)，索引顺序 (mach, alt_m)
    // mMilThrustMachAltTable：Mil  推力 2D 表 (lb)
    // mABThrustMachAltTable：AB   推力 2D 表 (lb)
    double (*idle_thrust_mach_alt_table)(double mach, double alt_m);
    double (*mil_thrust_mach_alt_table)(double mach, double alt_m);
    double (*ab_thrust_mach_alt_table)(double mach, double alt_m);

    // 改进 2D 表模式 AltMach：推力 = f(海拔高度 m, 马赫数 mach)
    // 索引顺序 (alt_m, mach)，与上面对偶
    double (*idle_thrust_alt_mach_table)(double alt_m, double mach);
    double (*mil_thrust_alt_mach_table)(double alt_m, double mach);
    double (*ab_thrust_alt_mach_table)(double alt_m, double mach);

    // === 推力比油耗 TSFC（Thrust-Specific Fuel Consumption）===
    // mTSFC_Idle_pph：慢车工况名义 TSFC (lb 燃油 / lb 推力 / 小时)
    // mTSFC_Mil_pph：军推工况名义 TSFC (lb/lb/hr)
    // mTSFC_AB_pph：加力工况名义 TSFC (lb/lb/hr)
    double tsfc_idle_pph;  // lb/lb/hr
    double tsfc_mil_pph;
    double tsfc_ab_pph;

    // === 额定推力（设计点推力，用于增量化 TSFC 计算）===
    // mRatedThrustIdle_lbs：设计点慢车推力 (lb)
    // mRatedThrustMil_lbs：设计点军推推力 (lb)
    // mRatedThrustAB_lbs：设计点加力推力 (lb)
    double rated_thrust_idle_lbs;  // lb
    double rated_thrust_mil_lbs;
    double rated_thrust_ab_lbs;

    // === Spool Dynamics 加减速率（油门转速动特性参数）===
    // 可为标量值 (1/s) 或 1D 曲线（查表参数为当前有效油门位置）
    // mSpinUpMil_per_sec：慢车→军推时的最大油门加速率 (1/s)
    // mSpinDownMil_per_sec：军推→慢车时的最大油门减速率 (1/s)
    // mSpinUpAB_per_sec：军推→加力时的最大油门加速率 (1/s)
    // mSpinDownAB_per_sec：加力→军推时的最大油门减速率 (1/s)
    double spin_up_mil_per_sec;    // 1/s，或查表
    double spin_down_mil_per_sec;  // 1/s，或查表
    double spin_up_ab_per_sec;
    double spin_down_ab_per_sec;

    // Spin rate 1D 曲线：查表参数 = 当前有效油门位置
    double (*spin_up_mil_table)(double throttle);
    double (*spin_down_mil_table)(double throttle);
    double (*spin_up_ab_table)(double throttle);
    double (*spin_down_ab_table)(double throttle);

    // === 视觉/尾迹参数 ===
    bool   engine_may_smoke;          // 是否允许冒烟
    double engine_smokes_above_level; // 冒烟门限（有效油门超过此值且非 AB 时冒烟），默认 1.0
};
```

### 2.2 JetEngineState（喷气发动机跨帧状态）

```cpp
// 描述喷气发动机每帧更新后的持久化状态
struct JetEngineState {
    // === 油门状态 ===
    double throttle_lever_position;     // 直接设定的油门杆位（0=Idle, 1=Mil, 2=全AB），可由脚本设定
    bool   throttle_lever_position_set; // 标记是否已通过 SetThrottlePosition 直接设定

    // === Spool Dynamics 状态 ===
    double last_throttle_lever_position; // 上一帧的有效油门位置 δ_eff(t)（spool dynamics 初始值）

    // === 发动机运转标志 ===
    bool   inject_fuel;          // 供油开关：true=正常供油，false=断油（熄火/停机）
    double engine_percent_rpm;   // 简化转速百分比 (= 100 * throttleMil)
    double nozzle_position;      // 简化喷口位置指示 (= throttleAB)

    // === 推力与燃油状态（跨帧保存）===
    double current_thrust_lbs;       // 当前推力值 (lb)，供 GetThrust_lbs() 查询
    double current_fuel_burn_rate_pph; // 当前燃油消耗率 (lb/hr)

    // === 引擎可见性标志（每帧 CalculateThrust 中更新）===
    bool engine_operating;     // 发动机是否正在运转并燃烧燃油
    bool afterburner_present;  // 是否存在加力燃烧室（初始化时确定，全程不变）
    bool afterburner_on;       // 加力燃烧室是否正在工作（AB 分量 > 0）
    bool contrailing;          // 是否在凝结尾迹高度层
    bool engine_smoking;       // 是否有限冒烟（非持久烟迹）
    bool producing_smoke_trail;// 是否产生持久烟迹（涡喷涡扇固定为 false）
    bool engine_damage_smoke_activated; // 外部迫冒烟（如战斗损伤）

    // === 定时器 ===
    bool    shutdown_in_progress;       // 是否正在执行停机流程
    int64_t shutdown_fraction_nanosec;  // 停机发生时刻在本帧内的偏移 (ns)
    int64_t ignite_time_in_frame_nanosec; // 点火时刻在本帧内的偏移 (ns)

    // === 燃油箱绑定 ===
    // mCurrentFuelTank：指向当前供油油箱的指针（nullptr 表示无油箱或已分离）
    FuelTank* current_fuel_tank_ptr;
};
```

### 2.3 ThrustCalculationResult（推力计算结果，单帧临时输出）

```cpp
// CalculateThrust 函数单次调用的输出结果
// 区分"更新状态"(updateData=true)和"仅计算不改变状态"(updateData=false)两种调用模式
struct ThrustCalculationResult {
    // 有效推力：正值为推力；熄火时为负值（死机进气口阻力）
    // 单位：lb（磅）
    double effective_thrust_lbs;

    // 燃油消耗速率（本帧平均水平）
    // 单位：lb/s（磅每秒）
    double fuel_burn_rate_pps;

    // 本帧实际燃烧的燃油质量
    // 单位：lb（磅）
    double fuel_burned_lbs;

    // 以下为只在 updateData=true 时更新的状态变量
    bool data_updated;  // 标记本次调用是否触发了状态更新
};
```

### 2.4 JetEngine（喷气发动机主接口类）

```cpp
// 喷气发动机推力模型，含完整 Spool Dynamics + 三层推力查表 + TSFC 燃油消耗 + 熄火保护
// 继承自 Engine（发动机基类），通过 ThrustProducerObject 与推进系统耦合
class JetEngine {
public:
    // ===================== 生命周期 =====================

    // 构造：绑定到父推力产生器对象（ThrustProducerObject）
    explicit JetEngine(ThrustProducerObject* parent_thrust_producer);

    // 读取场景文件中的 "jet" 配置块，解析所有推力表、TSFC、spin rate 等参数
    // 返回 false 表示配置有误，引擎不可用
    bool ProcessInput(UtInput& input, TypeManager* type_manager);

    // 初始化：计算有效 TSFC（增量 TSFC，从额定推力和名义 TSFC 反算）
    // 同时调用 DetermineIfAfterburnerIsPresent() 确定是否有加力燃烧室
    bool Initialize(int64_t sim_time_nanosec);

    // 克隆（深拷贝）引擎对象
    JetEngine* Clone() const;

    // ===================== 推力计算（核心算法接口）=====================

    // 推力计算（不改变发动机状态）
    // 参数:
    //   dT_sec:          时间步长 (s)
    //   alt_ft:          MSL 海拔高度 (ft)
    //   dynPress_lbsqft: 自由流动压 q_bar (lb/ft²)
    //   statPress_lbssqft: 静压 (lb/ft²)
    //   speed_fps:       真空速 (ft/s)
    //   mach:            飞行马赫数（无量纲）
    //   alpha_rad, beta_rad: 攻角/侧滑角 (rad)
    //   out force_lbs:        输出推力 (lb)，正=推力，负=熄机阻力
    //   out fuel_burn_rate_pps: 输出燃油消耗速率 (lb/s)
    //   out fuel_burned_lbs:   输出本帧燃烧燃油质量 (lb)
    void CalculateThrust(
        double dT_sec,
        double alt_ft,
        double dynPress_lbsqft,
        double statPress_lbssqft,
        double speed_fps,
        double mach,
        double alpha_rad,
        double beta_rad,
        double& force_lbs,           // [out] 推力 (lb)
        double& fuel_burn_rate_pps,  // [out] 燃油消耗速率 (lb/s)
        double& fuel_burned_lbs      // [out] 本帧燃油消耗量 (lb)
    );

    // 推力计算 + 状态更新
    // 参数同上，但额外更新发动机内部状态（有效油门、RPM、推力、燃油速率等）
    void UpdateThrust(
        double dT_sec,
        double alt_ft,
        double dynPress_lbsqft,
        double statPress_lbssqft,
        double speed_fps,
        double mach,
        double alpha_rad,
        double beta_rad,
        double& force_lbs,           // [out]
        double& fuel_burn_rate_pps,  // [out]
        double& fuel_burned_lbs      // [out]
    );

    // ===================== 最大/最小潜在推力查询 =====================

    // 获取最大潜在推力（全加力，如 AB 不可用则降级查 Mil 表）
    double GetMaximumPotentialThrust_lbs(
        double alt_ft,
        double dynPress_lbsqft,
        double statPress_lbssqft,
        double speed_fps,
        double mach,
        double alpha_rad,
        double beta_rad
    );

    // 获取最小潜在推力（Idle 慢车）
    double GetMinimumPotentialThrust_lbs(
        double alt_ft,
        double dynPress_lbsqft,
        double statPress_lbssqft,
        double speed_fps,
        double mach,
        double alpha_rad,
        double beta_rad
    );

    // ===================== 油门控制 =====================

    // 设置油门杆位置（直接设定，优先级高于父对象油门合成）
    // aThrottleLeverPosition: 0=慢车, 1=军推, 2=全加力（含 AB 时）
    void SetThrottlePosition(double throttle_lever_position);

    // 获取当前油门位置
    double GetThrottlePosition() const;

    // 供油开关控制
    // aInjectFuel=true: 正常供油（启动/恢复）
    // aInjectFuel=false: 断油（熄火/停机），推力 spool down 至零
    void InjectFuel(bool inject_fuel);

    // ===================== 引擎启停 =====================

    // 点火/启动引擎
    void Ignite(int64_t ignite_time_in_frame_nanosec);

    // 停机
    void Shutdown(int64_t terminate_time_nanosec = 0);

    // ===================== 状态查询 =====================

    // 获取当前推力值 (lb)。注：此值为上次 CalculateThrust/UpdateThrust 结束时保存的值
    double GetThrust_lbs() const;  // 继承自 Engine，返回 mCurrentThrust_lbs

    // 获取当前燃油消耗率 (lb/hr)
    double GetFuelBurnRate_pph() const;

    // 获取简化引擎转速百分比 (%RPM = 100 * throttleMil)
    double GetEnginePercentRPM() const;

    // 获取简化喷口位置 (0~1 = throttleAB)
    double GetNozzlePosition() const;

    // ===================== 燃油箱绑定 =====================

    // 设置引擎供油油箱（按名称查找）
    bool SetFuelTank(const std::string& fuel_tank_name);

    // 检查当前燃油箱路径是否完整
    // 返回 false 时 mCurrentFuelTank 被置空，引擎进入 dead state
    bool CheckCurrentFuelTank();

    // ===================== 引擎可见性标志 =====================
    bool EngineOperating() const;      // 引擎正在运转
    bool AfterburnerOn() const;        // AB 正在工作
    bool Contrailing() const;          // 产生凝结尾迹
    bool EngineSmoking() const;        // 有限冒烟
    bool ProducingSmokeTrail() const;  // 产生持久烟迹
    bool AfterburnerIsPresent() const; // 加力燃烧室存在
    void MakeEngineSmoke(bool smoking);// 外部设定引擎冒烟

private:
    // ===================== 内部算法（受保护） =====================

    // 推力计算核心（436 行完整实现）
    // 内部流程：油门指令确定 → spin-up/down 查表 → Spool Dynamics（有效油门跟随）
    // → 油门分解(Mil/AB) → Idle/Mil/AB 推力三层查表 → 燃油消耗(TSFC) → 熄火判定 → 死机阻力
    void CalculateThrust(
        double dT_sec, double alt_ft, double dynPress_lbsqft,
        double statPress_lbssqft, double speed_fps, double mach,
        double alpha_rad, double beta_rad,
        double& force_lbs, double& fuel_burn_rate_pps,
        double& fuel_burned_lbs,
        bool update_data  // true=更新状态变量, false=仅计算
    );

    // 判定是否存在加力燃烧室（mABThrustTable 或 mABThrustMachAltTable 非空）
    bool DetermineIfAfterburnerIsPresent();
};
```

### 2.5 Engine（发动机基类接口）

```cpp
// 所有发动机类型的抽象基类
// 定义了与推进系统的通用交互接口
class Engine {
public:
    virtual ~Engine() = default;

    // 配置解析与初始化
    virtual bool ProcessInput(UtInput& input, TypeManager* type_manager) = 0;
    virtual bool Initialize(int64_t sim_time_nanosec) = 0;

    // 克隆
    virtual Engine* Clone() const = 0;

    // 推力查询
    double GetThrust_lbs() const;
    virtual double GetMaximumPotentialThrust_lbs(...) = 0;
    virtual double GetMinimumPotentialThrust_lbs(...) = 0;

    // 推力计算（公共调用入口，内部 dispatch 到子类 CalculateThrust）
    void CalculateThrust(...); // updateData=false
    void UpdateThrust(...);    // updateData=true

    // 燃油箱管理
    bool CheckCurrentFuelTank();
    virtual bool SetFuelTank(const std::string& name);

    // 油门控制
    virtual double GetThrottlePosition() const = 0;
    virtual void SetThrottlePosition(double pos) = 0;

    // 启停
    virtual void Ignite(int64_t time) = 0;
    virtual void Shutdown(int64_t time = 0) = 0;

    // 燃油消耗率
    virtual double GetFuelBurnRate_pph() const = 0;

    // 可见性标志查询
    bool EngineOperating() const;
    bool AfterburnerOn() const;
    bool Contrailing() const;
    bool EngineSmoking() const;
    bool ProducingSmokeTrail() const;
    virtual bool AfterburnerIsPresent() const;
    void MakeEngineSmoke(bool smoking);
};
```

## 3. 典型调用模式

```cpp
// ============================================================
// 1. 初始化阶段：解析配置并初始化引擎
// ============================================================

// 创建引擎并绑定到推力产生器
JetEngine engine(thrust_producer_object);

// 解析场景文件中的 "jet" 配置块（推力表、TSFC、spin rate 等）
bool ok = engine.ProcessInput(input, type_manager);
if (!ok) {
    // 配置解析失败（如缺少必要推力表），引擎不可用
    return;
}

// 计算有效 TSFC + 确定是否有加力燃烧室
engine.Initialize(simulation_time_nanosec);

// 绑定燃油箱
engine.SetFuelTank("main_tank_1");

// 设定初始油门
engine.SetThrottlePosition(0.0);  // 从慢车开始
// ============================================================
// 2. 仿真循环：每帧调用推力更新
// ============================================================
while (simulating) {
    double dT   = 1.0 / 60.0;        // 60 Hz 物理步长 (s)
    double alt  = vehicle.getAltitude_ft();   // MSL 海拔 (ft)
    double dynQ = vehicle.getDynamicPressure_lbsqft(); // 动压 (lb/ft²)
    double statP = vehicle.getStaticPressure_lbssqft(); // 静压 (lb/ft²)
    double speed = vehicle.getSpeed_fps();  // 真空速 (ft/s)
    double mach  = vehicle.getMach();
    double alpha = vehicle.getAlpha_rad();
    double beta  = vehicle.getBeta_rad();

    double thrust_lbs, fuel_rate_pps, fuel_burned_lbs;

    // 情况 A：只计算不改变状态（用于力/力矩查询）
    engine.CalculateThrust(dT, alt, dynQ, statP, speed,
                           mach, alpha, beta,
                           thrust_lbs, fuel_rate_pps, fuel_burned_lbs);

    // 情况 B：计算并更新状态（正常每帧推进）
    engine.UpdateThrust(dT, alt, dynQ, statP, speed,
                        mach, alpha, beta,
                        thrust_lbs, fuel_rate_pps, fuel_burned_lbs);

    // 将推力应用于飞行器
    vehicle.applyThrust(thrust_lbs);

    // 查询发动机状态（日志/可视化用）
    if (engine.AfterburnerOn()) {
        render_ab_flame();           // 渲染加力火焰效果
    }
    if (engine.EngineSmoking()) {
        render_smoke();              // 渲染冒烟效果
    }

    sim_time += dT;
}
// ============================================================
// 3. 脚本控制：运行时修改油门和供油
// ============================================================

// 军推
engine.SetThrottlePosition(1.0);

// 全加力
engine.SetThrottlePosition(2.0);

// 断油熄火
engine.InjectFuel(false);

// 重新点火
engine.InjectFuel(true);
engine.Ignite(current_frame_time_nanosec);

// ============================================================
// 4. 查询推力包线（用于战术决策）
// ============================================================

// 当前高度/马赫数下的最大可用推力
double max_thrust = engine.GetMaximumPotentialThrust_lbs(
    alt, dynQ, statP, speed, mach, alpha, beta);

// 当前高度/马赫数下的最小推力 (Idle)
double min_thrust = engine.GetMinimumPotentialThrust_lbs(
    alt, dynQ, statP, speed, mach, alpha, beta);

// 判断是否有加力能力
if (engine.AfterburnerIsPresent()) {
    double ab_margin = max_thrust - min_thrust;  // 加力推力的包线范围
}
```

## 4. 坐标系/单位约定

| 量 | AFSIM 原始单位 | SI 等效 | 说明 |
|----|-------------|---------|------|
| 推力 | lb (磅力) | 1 lb = 4.448 N | 输出推力/阻力 |
| 海拔高度 | ft (英尺) | 1 ft = 0.3048 m | 推力表查表参数（alt 维度） |
| 海拔（2D 表）| m (米) | SI | AltMach/MachAlt 表的 alt 维度已做单位转换 |
| 动压 | lb/ft² (psf) | 1 psf = 47.88 Pa | 熄机阻力 D_dead = dragArea * q_bar |
| 静压 | lb/ft² (psf) | 同上 | 调用接口传入 |
| 速度 | ft/s | 1 ft/s = 0.3048 m/s | 真空速 |
| 马赫数 | 无量纲 | — | 改进 2D 表的查表维度 |
| 攻角/侧滑角 | rad | — | 调用接口传入 |
| 时间步长 | s | — | 仿真物理步长 |
| 燃油质量 | lb (磅) | 1 lb = 0.4536 kg | 油箱油量/消耗量 |
| 燃油消耗速率 | lb/s (pps), lb/hr (pph) | — | TSFC 单位 lb/lb/hr → 有效 TSFC 转为 lb/lb/s |
| 推力比油耗 | lb燃料/lb推力/hr | — | Idle/Mil/AB 各工况分别输入 |

> 注：AFSIM 原始代码使用美制 Imperial 单位（lb, ft, psf），移植到 SI 单位时应：
> - 推力：lb -> N (x4.448)
> - 高度：ft -> m (x0.3048)
> - 燃油：lb -> kg (x0.4536)
> - 动压：psf -> Pa (x47.88)

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|---------|----------|
| `UtTable::Curve` (1D 推力表, spin rate 表) | 查表引擎 | 自定义 1D 线性/样条插值器 |
| `UtTable::Table` (2D MachAlt/AltMach 表) | 查表引擎 | 自定义 2D 双线性/样条插值器 |
| `UtInput` / `UtInputBlock` | 配置解析器 | JSON/YAML/TOML 配置解析器 |
| `UtCloneablePtr<T>` | 深拷贝智能指针 | `std::unique_ptr<T>` + 自定义 Clone 工厂 |
| `UtMath::cLB_PER_NT` / `cFT_PER_M` / `cM_PER_FT` | 单位转换常数 | 硬编码或自定义 UnitConverter |
| `FuelTank` (wsf_six_dof::FuelTank) | 燃油箱类 | 自定义 FuelTank 类（提供 UpdateFuelBurn / FuelFlowPathIntact 接口） |
| `ThrustProducerObject` | 父对象 | 自定义推力产生器类（提供油门合成 + dead engine drag area 查询） |
| `Engine` (wsf_six_dof::Engine) | 发动机基类 | 自定义发动机抽象基类 |
| `PropulsionSystem` | 推进系统 | 自定义推进系统类（管理多引擎 + 多油箱，提供燃油箱查询和路径完整性检查） |
| `TypeManager` | 类型注册管理器 | 自定义配置工厂 |
| `Mover` / `KinematicState` | 飞行器状态查询 | 自定义飞行器接口（提供 alt, mach, dynPress 等状态查询） |
| `UtLog` | 日志 | 标准日志库或 printf |
