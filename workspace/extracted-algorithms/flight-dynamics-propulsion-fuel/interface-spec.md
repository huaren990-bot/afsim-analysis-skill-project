# 推进系统与燃油管理模型 -- 接口规格

> **日期:** 2026-06-11
> **状态:** draft
> **对应算法卡:** flight-dynamics-propulsion-fuel-card.md

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────┐
│                 PropulsionSystem（推进系统）                │
│  多油箱管理 + 油箱间传输协调 + 质量属性汇总                  │
├──────────────────────────────────────────────────────────┤
│  + Initialize(simTime) → bool                            │
│  + Update(simTime) -- 每帧主入口                          │
│  + GetMassProperties() → MassProperties                  │
│  + AddFuelTank(tank) / RemoveFuelTankByName(name)        │
│  + AddFuelTransfer(name, src, tgt) / RemoveFuelTransfer  │
│  + AddFuelQuantity_lbs(qty) / FillAllTanks(percent)      │
│  + GetFuelTanks() / GetFuelTank(name)                    │
│  - RemoveInvalidFuelTransfers() -- 清理失效传输链路       │
│  - 传输协调: 分组→计算最大接收/提供→比例因子→执行传输      │
└──────────┬───────────────────────────────────────────────┘
           │ 管理多个
           ▼
┌──────────────────────────────────────────────────────────┐
│                    FuelTank（燃油箱）                      │
│  燃油容量 + CG 线性插值 + 3 种速率的燃烧/填充/传输操作      │
├──────────────────────────────────────────────────────────┤
│  + ProcessInput(input) → bool                            │
│  + Initialize(simTime) → bool                            │
│  + Update(simTime) -- 每帧将临时速率提交为永久速率          │
│  + CalculateFuelBurn(dT, request, actual, newMass, cg)    │
│  + UpdateFuelBurn(dT, request, actual, newMass, cg)      │
│  + CalculateFuelFill(dT, request, actual, newMass, cg)   │
│  + UpdateFuelFill(dT, request, actual, newMass, cg)      │
│  + CalculateFuelTransfer(dT, request, actual, newMass, cg)│
│  + UpdateFuelTransfer(dT, request, actual, newMass, cg)  │
│  + FuelFlowPathIntact(propSystem) → bool                 │
│  - CalcCgLocation_ft(qty) → Vec3 -- CG 线性插值           │
└──────────────────────────────────────────────────────────┘
           │ 被调用方
           ▼
┌──────────────────────────────────────────────────────────┐
│                  Engine（发动机基类）                      │
│  每帧通过 UpdateFuelBurn 消耗燃油                          │
├──────────────────────────────────────────────────────────┤
│  + UpdateThrust(dT, alt, dynPress, ...)                  │
│    → CalculateThrust() → mCurrentFuelTank->UpdateFuelBurn │
│  + CheckCurrentFuelTank() → bool                         │
└──────────────────────────────────────────────────────────┘
```

## 2. 核心接口定义

### 2.1 FuelTankConfig（燃油箱配置参数）

```cpp
// 描述燃油箱的全部静态配置参数
struct FuelTankConfig {
    // 最大燃油供给速率（发动机从油箱抽取燃油的最大速率）
    // 单位：lb/s
    double max_flow_rate_pps;

    // 最大燃油填充速率（外部加油时油箱接受燃油的最大速率）
    // 单位：lb/s
    double max_fill_rate_pps;

    // 最大燃油传输速率（油箱间燃油传输的最大速率）
    // 单位：lb/s
    double max_transfer_rate_pps;

    // 油箱最大容量
    // 单位：lb
    double max_quantity_lbs;

    // 满油箱时的燃油质心位置（相对父对象坐标系）
    // 通常为油箱几何中心
    // 单位：ft
    Vec3 full_cg_location_ft;

    // 空油箱时的燃油质心位置（相对父对象坐标系）
    // 通常为油箱底部
    // 单位：ft
    Vec3 empty_cg_location_ft;
};
```

### 2.2 FuelTankState（燃油箱跨帧状态）

```cpp
// 描述燃油箱每帧更新后的持久化状态
// "临时速率 → 永久速率" 两阶段提交机制：
//   本帧内可能多次调用 UpdateFuelBurn/Fill/Transfer
//   每次调用将实际速率累加到 mTemp* 临时速率
//   本帧末尾的 Update() 将临时速率提交为永久速率并清零临时变量
struct FuelTankState {
    // === 当前燃油 ===
    double current_quantity_lbs;     // 当前燃油质量 (lb) -- 核心状态
    Vec3   current_cg_location_ft;   // 当前燃油质心位置 (ft)，由 CalcCgLocation_ft 计算

    // === 当前永久速率（上一帧结束时提交，用于外部查询）===
    double current_fuel_flow_pps;     // 当前供油速率 (lb/s)，正=流出
    double current_fill_rate_pps;     // 当前加油速率 (lb/s)，正=流入
    double current_transfer_rate_pps; // 当前传输速率 (lb/s)，正=接收，负=移出

    // === 本帧临时速率（本帧内累积，Update() 末尾提交并清零）===
    double temp_fuel_flow_pps;        // 临时供油速率
    double temp_fill_rate_pps;        // 临时加油速率
    double temp_transfer_rate_pps;    // 临时传输速率

    // === 质心参数（静态，初始化时确定）===
    Vec3 empty_cg_location_ft;        // 空箱 CG
    Vec3 full_cg_location_ft;         // 满箱 CG
    Vec3 cg_empty_to_full_vector;     // = fullCg - emptyCg (ft)

    // === 时间戳 ===
    int64_t last_sim_time_nanosec;    // 上一帧仿真时间 (ns)
};
```

### 2.3 FuelBurnResult（燃油燃烧/填充/传输操作结果）

```cpp
// FuelTank 燃油操作的统一返回结构
// 适用于 Calculate/Update 的三种操作：Burn（燃烧）、Fill（填充）、Transfer（传输）
struct FuelOperationResult {
    // 操作是否完全满足请求
    // true：请求的燃油量全部可用（剩余油量充足、速率未超限）
    // false：燃油不足（油箱见底、速率超限被截断、或容量已满）
    bool able_to_provide;

    // 实际操作的燃油质量
    // Burn：实际燃烧量 (lb)，正数
    // Fill/Transfer：实际填充/传输量 (lb)，正=接收，负=移出
    double fuel_actually_provided_lbs;

    // 操作完成后的新燃油质量 (lb)
    double new_fuel_mass_lbs;

    // 操作完成后的新燃油 CG 位置 (ft)
    Vec3 new_cg_location_ft;
};
```

### 2.4 FuelTank（燃油箱主接口类）

```cpp
// 燃油箱类：燃油容器，管理燃烧、填充、传输三种操作
// 内部使用 CG 线性插值（空箱 CG 到满箱 CG 按燃油充满度线性插值）
class FuelTank {
public:
    // ===================== 生命周期 =====================
    FuelTank();
    ~FuelTank();
    FuelTank* Clone() const;  // 深拷贝

    // 读取场景配置（max_quantity, flow_rate, cg locations 等）
    bool ProcessInput(UtInput& input);

    // 初始化：计算 mCgEmptyToFullVector = mFullCgLocation - mEmptyCgLocation
    bool Initialize(int64_t sim_time_nanosec);

    // 每帧更新：将本帧累积的临时速率（temp）提交为永久速率（current），清零临时变量
    // 注意：其他 update 函数（UpdateFuelBurn/Fill/Transfer）应在 Update 之前调用
    void Update(int64_t sim_time_nanosec);

    // ===================== 燃油燃烧（发动机消耗）=====================

    // 计算燃油燃烧（不改变状态）
    // 参数:
    //   dT_sec: 时间步长 (s)
    //   burn_request_lbs: 请求燃烧的燃油质量 (lb)
    //   out actually_provided: 实际可燃烧量 (lb)
    //   out new_mass: 燃烧后的新燃油质量 (lb)
    //   out new_cg: 燃烧后的新 CG 位置 (ft)
    // 返回: true=完全满足请求，false=不足
    bool CalculateFuelBurn(
        double dT_sec,
        double burn_request_lbs,
        double& actually_provided_lbs, // [out]
        double& new_fuel_mass_lbs,     // [out]
        Vec3&   new_cg_location_ft     // [out]
    );

    // 燃油燃烧 + 状态更新
    // 更新 mCurrentQuantity_lbs 和 mCurrentCgLocation_ft
    // 累积临时速率 mTempCurrentFuelFlow_pps += actually_provided / dT
    bool UpdateFuelBurn(
        double dT_sec,
        double burn_request_lbs,
        double& actually_provided_lbs, // [out]
        double& new_fuel_mass_lbs,     // [out]
        Vec3&   new_cg_location_ft     // [out]
    );

    // ===================== 燃油填充（外部加油）=====================

    // 计算燃油填充（不改变状态）
    bool CalculateFuelFill(
        double dT_sec,
        double fill_request_lbs,       // 请求填充量 (lb)
        double& actually_provided_lbs, // [out] 实际填充量
        double& new_fuel_mass_lbs,     // [out]
        Vec3&   new_cg_location_ft     // [out]
    );

    // 燃油填充 + 状态更新
    bool UpdateFuelFill(
        double dT_sec,
        double fill_request_lbs,
        double& actually_provided_lbs, // [out]
        double& new_fuel_mass_lbs,     // [out]
        Vec3&   new_cg_location_ft     // [out]
    );

    // ===================== 燃油传输（油箱到油箱）=====================

    // 计算燃油传输（不改变状态）
    // aFuelAddRequest_lbs: 正=接收燃油，负=移出燃油
    bool CalculateFuelTransfer(
        double dT_sec,
        double fuel_add_request_lbs,   // 正=接收/负=移出 (lb)
        double& actually_provided_lbs, // [out] 实际传输量
        double& new_fuel_mass_lbs,     // [out]
        Vec3&   new_cg_location_ft     // [out]
    );

    // 燃油传输 + 状态更新
    bool UpdateFuelTransfer(
        double dT_sec,
        double fuel_add_request_lbs,   // 正=接收/负=移出 (lb)
        double& actually_provided_lbs, // [out]
        double& new_fuel_mass_lbs,     // [out]
        Vec3&   new_cg_location_ft     // [out]
    );

    // ===================== 燃油量查询 =====================

    // 当前燃油质量 (lb)
    double GetCurrentFuelQuantity_lbs() const;

    // 油箱最大容量 (lb)
    double GetFuelCapacity_lbs() const;

    // 燃油充满度百分比 (0~100)
    double GetPercentFull() const;

    // 燃油充满度分数 (0~1) = currentQty / maxQty
    double GetFuelFraction() const;

    // 设置/获取最大燃油量
    void SetMaxFuelQuantity(double qty_lbs);

    // 设置当前燃油量（同时更新 CG 位置）
    void SetCurrentFuelQuantity(double qty_lbs);

    // ===================== 各种速率查询 =====================

    // 当前供油速率（发动机消耗）
    double GetFuelFlow_pps() const;
    double GetFuelFlow_pph() const;

    // 当前加油速率
    double GetFuelFillRate_pps() const;
    double GetFuelFillRate_pph() const;

    // 当前传输速率
    double GetFuelTransferRate_pps() const;
    double GetFuelTransferRate_pph() const;

    // 最大传输速率
    double GetMaxFuelTransferRate_pps() const;

    // ===================== CG 质心查询与设置 =====================

    // 获取当前 CG 位置（相对父对象）
    Vec3 GetCurrentCgLocation_ft() const;

    // 获取满箱 CG 位置
    Vec3 GetFullCgLocation_ft() const;

    // 获取空箱 CG 位置
    Vec3 GetEmptyCgLocation_ft() const;

    // 设置满箱 CG（同时更新 mCgEmptyToFullVector = mFullCg - mEmptyCg）
    void SetFullCgLocation_ft(const Vec3& cg_ft);

    // 设置空箱 CG（同时更新 mCgEmptyToFullVector）
    void SetEmptyCgLocation_ft(const Vec3& cg_ft);

    // ===================== 传输速率设置 =====================

    // 设置最大供油速率 (lb/s)，通常用于测试
    void SetMaxFlowRate_pps(double max_flow_rate_pps);

    // ===================== 推进系统绑定 =====================

    void SetPropulsionSystem(PropulsionSystem* parent);

    // 检查燃油流动路径是否完整
    // 验证油箱仍连接到推进系统（未被抛弃/阀门切断）
    bool FuelFlowPathIntact(const PropulsionSystem* system_drawing_fuel);

private:
    // CG 位置线性插值：
    //   fraction = current_fuel_qty / max_qty
    //   return empty_cg + fraction * (full_cg - empty_cg)
    Vec3 CalcCgLocation_ft(double current_fuel_quantity_lbs);
};
```

### 2.5 PropulsionSystem（推进系统主接口类）

```cpp
// 推进系统：管理多油箱燃油分配、油箱间传输、质量属性汇总
class PropulsionSystem {
public:
    // ===================== 生命周期 =====================
    PropulsionSystem();

    // 初始化（由子类实现具体逻辑）
    virtual bool Initialize(int64_t sim_time_nanosec) = 0;

    // 每帧更新：处理燃油传输 + 保存时间戳
    // 1. 计算 dT
    // 2. 检查燃油冻结标志，若冻结则跳过传输
    // 3. RemoveInvalidFuelTransfers() 清理失效链路
    // 4. 遍历 mFuelTransferList，按目标油箱分组
    // 5. 计算比例因子，按比例执行传输
    virtual void Update(int64_t sim_time_nanosec);

    void SetLastSimTime(int64_t last_sim_time_nanosec);

    // ===================== 燃油箱管理 =====================

    // 获取所有燃油箱的名称→对象映射
    const std::unordered_map<std::string, FuelTank*>& GetFuelTanks() const;

    // 按名称获取燃油箱
    FuelTank* GetFuelTank(const std::string& name) const;

    // 获取燃油箱数量
    size_t GetNumFuelTanks() const;

    // 添加燃油箱
    bool AddFuelTank(std::unique_ptr<FuelTank> fuel_tank);

    // 按名称移除燃油箱（如抛弃副油箱）
    bool RemoveFuelTankByName(const std::string& name);

    // ===================== 燃油传输管理 =====================

    // 添加传输链路（通常在配置解析时调用，不立即连接）
    bool AddFuelTransfer(
        const std::string& transfer_name,
        const std::string& source_tank_name,
        const std::string& target_tank_name
    );

    // 添加传输链路并立即连接（脚本动态调用时使用）
    bool AddFuelTransferAndConnect(
        const std::string& transfer_name,
        const std::string& source_tank_name,
        const std::string& target_tank_name
    );

    // 按名称移除传输链路
    bool RemoveFuelTransfer(const std::string& transfer_name);

    // ===================== 燃油量修改 =====================

    // 修改指定油箱的燃油量
    bool ModifyFuelQuantity(const std::string& tank_name, double qty_lbs);

    // 获取总容量
    double GetInternalFuelTankCapacity_lbs() const;

    // 获取当前总燃油量
    double GetCurrentInternalFuelTankQuantity_lbs() const;

    // 百分比加油（按统一百分比填满所有油箱）
    double AddFuelQuantity_lbs(double fuel_to_add_lbs);

    // 将所有油箱填充到指定百分比
    double FillAllTanks(double percent_full);

    // 清空所有油箱
    void EmptyAllTanks();

    // ===================== 质量属性汇总 =====================

    // 汇总所有燃油箱的质量属性（总质量 + 加权 CG 位置）
    const MassProperties GetMassProperties() const;

    // ===================== 推力产生器管理（子类实现）=====================

    // 按名称获取推力产生器（引擎）
    virtual ThrustProducerObject* GetThrustProducerObjectByName(const std::string& name) const = 0;

    // 按索引获取推力产生器
    virtual ThrustProducerObject* GetThrustProducerByIndex(size_t index) const = 0;

    // 设置所有引擎的油门杆位置
    virtual void SetThrottleLeverPosition(double position) = 0;

    // 获取推力产生器数量
    virtual size_t GetNumThrustProducers() const = 0;

    // 点火/停机所有引擎
    virtual void Ignite(int64_t time) = 0;
    virtual void Shutdown(int64_t time = 0) = 0;

    // 设置引擎供油油箱
    virtual bool SetFuelFeed(std::string& engine_name, std::string tank_name) = 0;
    virtual bool SetFuelFeed(std::string tank_name) = 0;

    // ===================== 状态查询 =====================

    // 是否有引擎正在产生推力
    virtual bool IsProducingThrust() const = 0;

    // 引擎可见性批量查询
    virtual bool AnEngineIsOperating(bool test_subobjects = false) const = 0;
    virtual bool AnEngineIsSmoking(bool test_subobjects = false) const = 0;
    virtual bool AnEngineHasAfterburnerOn(bool test_subobjects = false) const = 0;
    virtual bool AnEngineIsContrailing(bool test_subobjects = false) const = 0;
    virtual bool AnEngineIsEmittingSmokeTrail(bool test_subobjects = false) const = 0;

    // 是否有加力燃烧室
    virtual bool AfterburnerIsPresent() const = 0;

    // 推力矢量控制
    virtual void EnableThrustVectoring(bool enable) = 0;
    bool ThrustVectoringEnabled() const;

    // 强制引擎冒烟
    virtual void MakeAnEngineSmoke(int engine_index) = 0;

private:
    // 内部数据结构
    struct FuelTransfer {
        std::string name;
        std::string source_tank_name;
        std::string target_tank_name;
        FuelTank*   source_tank;
        FuelTank*   target_tank;
    };

    struct FuelTankData {
        FuelTank* source_tank;
        double    fuel_actually_provided_lbs;
    };

    struct TankMatching {
        FuelTank*                    target_tank;
        std::vector<FuelTankData>   source_tank_list;
    };

    // 清理无效传输链路（因油箱被移除而导致源/目标悬空）
    void RemoveInvalidFuelTransfers();
};
```

## 3. 典型调用模式

```cpp
// ============================================================
// 1. 初始化阶段：配置油箱和传输链路
// ============================================================

// 创建推进系统
PropulsionSystem* prop_system = createSpecificPropulsionSystem();

// 创建油箱 1（主油箱）
auto tank1 = std::make_unique<FuelTank>();
tank1->SetMaxFuelQuantity(10000.0);  // 10000 lb 容量
tank1->SetCurrentFuelQuantity(8000.0); // 初始 80% 燃油
tank1->SetFullCgLocation_ft({0.0, 0.0, 1.0});  // 满 CG = 油箱中心
tank1->SetEmptyCgLocation_ft({0.0, 0.0, 0.0}); // 空 CG = 油箱底部
// 注：SetFullCg/SetEmptyCg 会自动计算 mCgEmptyToFullVector = {0, 0, 1}

// 创建油箱 2（副油箱）
auto tank2 = std::make_unique<FuelTank>();
tank2->SetMaxFuelQuantity(2000.0);
tank2->SetCurrentFuelQuantity(2000.0); // 满油
tank2->SetFullCgLocation_ft({0.0, 0.0, -1.0});
tank2->SetEmptyCgLocation_ft({0.0, 0.0, -0.5});

// 将油箱添加到推进系统
prop_system->AddFuelTank(std::move(tank1));
prop_system->AddFuelTank(std::move(tank2));

// 定义传输链路：副油箱 → 主油箱（自动传输）
prop_system->AddFuelTransfer("xfer_to_main", "tank2", "tank1");

// 引擎绑定主油箱作为供油源
prop_system->SetFuelFeed("engine1", "tank1");

// ============================================================
// 2. 仿真循环：每帧推进
// ============================================================
while (simulating) {
    int64_t sim_time_ns = getCurrentSimTimeNs();

    // 2.1 推进系统燃油传输（先执行传输，再执行引擎燃油消耗）
    prop_system->Update(sim_time_ns);

    // 2.2 各引擎更新（内部调用 FuelTank::UpdateFuelBurn）
    for (auto& engine : engines) {
        engine.UpdateThrust(dT, alt, dynPress, ...);
        // 内部流程:
        //   engine.CalculateThrust(...)
        //   → mCurrentFuelTank->UpdateFuelBurn(dT, fuelRequest, actual, newMass, newCg)
    }

    // 2.3 各油箱的每帧提交（将临时速率转为永久速率，清零临时变量）
    for (auto& [name, tank] : prop_system->GetFuelTanks()) {
        tank->Update(sim_time_ns);
    }

    // 2.4 汇总推进系统质量属性（供飞行器总质量/总质心计算）
    MassProperties prop_mass = prop_system->GetMassProperties();
    vehicle.setPropulsionMass(prop_mass);
    // 内部: 所有油箱的 mass = mCurrentQuantity_lbs, cg = mCurrentCgLocation_ft
    //       总质量 = Σ mass_i, 总CG = Σ(mass_i * cg_i) / Σ mass_i

    // 2.5 查询燃油状态（HUD/仪表用）
    double total_fuel = prop_system->GetCurrentInternalFuelTankQuantity_lbs();
    double max_fuel   = prop_system->GetInternalFuelTankCapacity_lbs();
    hud.setFuelGauge(total_fuel / max_fuel);  // 0~1

    sim_time_s += dT;
}
// ============================================================
// 3. CG 位置查询示例
// ============================================================

// 当前 CG 由 CalcCgLocation_ft 实时计算：
//   fraction = currentQty / maxQty                    // 燃油充满度
//   cg = emptyCg + fraction * (fullCg - emptyCg)    // 线性插值
// 结果在每次 UpdateFuelBurn/Fill/Transfer 操作后自动更新

// 手动查询
FuelTank* tank = prop_system->GetFuelTank("tank1");
Vec3 cg = tank->GetCurrentCgLocation_ft();   // 当前燃油 CG (ft)
double fraction = tank->GetFuelFraction();    // 0.75 表示 75% 剩余
// ============================================================
// 4. 燃油传输场景
// ============================================================

// 4.1 比例因子计算（当多源向同一目标传输时自动协调）:
//    fraction = totalAvailable / maxTargetReceive
//    若 fraction <= 1: 全量传输
//    若 fraction > 1:  等比压缩（fraction = 1 / fraction）
//   若 fraction <= EPSILON (目标无法接收): fraction = 0

// 4.2 抛弃油箱示例
prop_system->RemoveFuelTankByName("tank2");
// RemoveInvalidFuelTransfers() 会在下一帧自动清理关联的传输链路

// ============================================================
// 5. 百分比加油
// ============================================================

// 添加 5000 lb 燃油，按百分比均匀分配
double actually_added = prop_system->AddFuelQuantity_lbs(5000.0);

// 所有油箱填充到 80%
double fuel_used = prop_system->FillAllTanks(80.0);
```

## 4. 坐标系/单位约定

| 量 | AFSIM 原始单位 | SI 等效 | 说明 |
|----|-------------|---------|------|
| 燃油质量 | lb (磅) | 1 lb = 0.4536 kg | 油箱容量、当前油量、燃烧/填充/传输量 |
| 燃油速率 | lb/s (pps), lb/hr (pph) | — | 供油/加油/传输速率 |
| 位置/CG | ft (英尺) | 1 ft = 0.3048 m | CG 位置坐标（相对父对象） |
| 时间步长 | s (秒) | — | 物理仿真步长 |
| 仿真时间 | ns (纳秒) | — | 内部使用 ns 精度存储时间戳，计算 dT 时转为秒 |

> 注：AFSIM 原始代码使用美制 Imperial 单位（lb, ft）。移植到 SI 单位时应：
> - 燃油质量：lb -> kg (x0.4536)
> - 燃油速率：lb/s -> kg/s, lb/hr -> kg/hr
> - CG 位置：ft -> m (x0.3048)

## 5. 框架依赖解耦表

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
|---------------|---------|----------|
| `UtVec3dX` | 3D 向量 | Eigen::Vector3d 或自定义 Vec3 |
| `UtCloneablePtr<T>` | 深拷贝智能指针 | `std::unique_ptr<T>` + 自定义 Clone |
| `MassProperties` (wsf_six_dof) | 质量属性类 | 自定义 MassProperties（质量 + CG + 惯量） |
| `Object` (wsf_six_dof) | 基类 | 自定义物体基类 |
| `Mover` (父 Vehicle) | 飞行器父对象 | 自定义飞行器接口（提供 freeze 标志查询） |
| `std::unordered_map` | 哈希表 | C++ 标准库，直接可用 |
| `std::vector`, `std::unique_ptr` | 容器/智能指针 | C++ 标准库，直接可用 |
| `UtLog` | 日志 | 标准日志库或 printf |
| `UtInput` / `UtInputBlock` | 配置解析 | JSON/YAML/TOML 解析器 |
| `Engine` (wsf_six_dof::Engine) | 引擎基类 | 自定义引擎接口（提供推力更新、燃油消耗回调） |
| `ThrustProducerObject` | 推力产生器 | 自定义推力产生器接口 |
