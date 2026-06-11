# 算法卡片 -- wsf_six_dof 推进系统与燃油管理模型

> **状态**：draft
> **日期**：2026-06-11
> **索引证据**：function-index.jsonl (wsf_six_dof::PropulsionSystem, wsf_six_dof::FuelTank), source/WsfSixDOF_PropulsionSystem.hpp/.cpp, source/WsfSixDOF_FuelTank.hpp/.cpp
> **关联文档**：flight-dynamics-jet-engine-card.md, flight-dynamics-rigid-body-integrator-card.md

### 基础资料

- **算法名称**：Propulsion System and Fuel Management Model（推进系统与燃油管理模型）
- **算法所属模块**：wsf_six_dof（点质/刚体六自由度飞行器运动学插件 -- 新模块）
- **算法功能**：管理多发动机推进系统中的燃油分配、消耗和油箱间传输。每帧更新时：遍历所有发动机的燃油消耗请求，通过相关燃油箱的 `UpdateFuelBurn` 消耗燃料；同时处理预定义的油箱间燃油传输（Fuel Transfer），按传输速率限制和比例因子协调多源到多目标的传输流程；最后汇总所有燃油箱质量属性（含 CG 位置线性插值）供总质量计算使用。

### 算法流程

整个算法流程图如下：

```mermaid
flowchart TD
    A["开始 PropulsionSystem::Update"] --> step1["1. 计算时间步长 dT，检查冻结标志"]
    step1 --> step2{"2. 燃油冻结？"}
    step2 -->|"是"| skip["跳过所有燃油操作"]
    step2 -->|"否"| step3["3. 移除无效传输路径"]
    step3 --> step4["4. 构建目标油箱→源油箱列表映射"]
    step4 --> step5["5. 对每个目标油箱计算最大接收能力"]
    step5 --> step6["6. 对每个源油箱计算最大提供能力"]
    step6 --> step7["7. 计算供给/需求比例因子 fraction"]
    step7 --> step8{"8. fraction > 0?"}
    step8 -->|"是"| step9["9. 按比例从各源油箱移出，加入目标油箱"]
    step8 -->|"否"| step10["10. 无实际传输"]
    step9 --> step11["11. 保存本帧时间戳"]
    step11 --> F["结束"]
```

其中，第一步计算 `dT_sec = aSimTime - mLastSimTime`；第二步检查 `GetParentVehicle()->GetFreezeFlags()->fuelBurn`，若冻结则直接返回（不处理传输但在引擎 UpdateThrust 中不改变油量）；第三步通过 `RemoveInvalidFuelTransfers` 清理因油箱分离（如抛弃副油箱）而失效的传输链路；第四步将所有传输按目标油箱分组构建 `TankMatching` 列表（一个目标可能对应多个源）；第五步使用目标油箱的 `GetMaxFuelTransferRate_pps() * dT_sec` 得到最大接收量，再受限于 `GetFuelCapacity - GetCurrentFuelQuantity`（油箱满度限制）；第六步使用源油箱的 `CalculateFuelTransfer(dT, -request, ...)` 计算最大可提供量；第七步计算 `fraction = totalXfer / maxTgtXfer`，若 fraction <= 1 则 fraction=1（全量传输），否则 fraction=1/fraction（等比压缩）；第九步通过源 `UpdateFuelTransfer(dT, -fraction*provided, ...)` 和 目标 `UpdateFuelTransfer(dT, +fraction*provided, ...)` 完成实际传输。

**燃油箱 FuelTank::Update 子流程**：

```mermaid
flowchart TD
    A2["FuelTank::Update"] --> s1["1. 限幅当前油量至 [0, maxQty]"]
    s1 --> s2["2. 提交临时速率 → 永久速率"]
    s2 --> s3["3. 清零临时速率"]
    s3 --> s4["4. 保存本帧时间戳"]
    s4 --> F2["结束"]
```

**燃油箱 CG 位置计算子流程（CalcCgLocation_ft）**：

```mermaid
flowchart TD
    A3["CalcCgLocation_ft"] --> c1["1. fraction = currentQty / maxQty"]
    c1 --> c2["2. scaledVec = fraction × (fullCg - emptyCg)"]
    c2 --> c3["3. return emptyCg + scaledVec"]
    c3 --> F3["结束"]
```

### 算法变量和常量

1. 输入 (input)：

   | 英文标识符 (Symbol)        | 中文名称 (Name) | 数据类型 (Type)    | 含义 (Meaning)           | 单位 (Units) | 所属函数 (Method) |
   | --------------------- | ----------- | -------------- | ---------------------- | ---------- | ------------- |
   | `aSimTime_nanosec`    | 当前仿真时间      | `int64_t`      | 当前帧的仿真时间戳              | ns         | Update        |
   | `mLastSimTime_nanosec` | 上次仿真时间      | `int64_t`      | 上一帧的仿真时间戳              | ns         | Update        |
   | `mFuelTransferList`   | 燃油传输列表      | `vector<FuelTransfer>` | 预定义的油箱间传输源/目标/名称       | —          | Update        |
   | `mFuelTankMap`        | 燃油箱映射表      | `unordered_map` | 所有燃油箱的名称→对象映射          | —          | Update        |

2. 输出 (output)：

   | 英文标识符 (Symbol)      | 中文名称 (Name) | 数据类型 (Type)  | 含义 (Meaning)                        | 单位 (Units) | 所属函数 (Method)   |
   | ------------------- | ----------- | ------------ | ----------------------------------- | ---------- | --------------- |
   | `GetMassProperties` | 推进系统质量属性    | `MassProperties` | 所有燃油箱的质量+CG 汇总（mCurrentQuantity_lbs + CG 位置） | lb, ft     | GetMassProperties |

3. 常量 (constant)：

   | 英文标识符 (Symbol)              | 中文名称 (Name)     | 数据类型 (Type) | 含义 (Meaning)                        | 单位 (Units) | 所属函数 (Method)       |
   | --------------------------- | --------------- | ----------- | ----------------------------------- | ---------- | ------------------- |
   | `mMaxFlowRate_pps` (FuelTank) | 最大燃油供给速率       | `double`    | 发动机从油箱抽取燃油的最大速率                    | lb/s       | FuelTank::ProcessInput |
   | `mMaxFillRate_pps` (FuelTank) | 最大燃油填充速率       | `double`    | 外部加油时油箱接受燃油的最大速率                   | lb/s       | FuelTank::ProcessInput |
   | `mMaxTransferRate_pps` (FuelTank) | 最大燃油传输速率      | `double`    | 油箱间燃油传输的最大速率                       | lb/s       | FuelTank::ProcessInput |
   | `mMaxQuantity_lbs` (FuelTank) | 油箱最大容量          | `double`    | 油箱满容量时的燃油质量                        | lb         | FuelTank::ProcessInput |
   | `mFullCgLocation_ft` (FuelTank) | 满油箱 CG 位置      | `UtVec3dX`  | 油箱满时燃油的质心位置（通常为油箱中心）               | ft         | FuelTank::ProcessInput |
   | `mEmptyCgLocation_ft` (FuelTank) | 空油箱 CG 位置      | `UtVec3dX`  | 油箱空时燃油的质心位置（通常为油箱底部）               | ft         | FuelTank::ProcessInput |
   | `mCgEmptyToFullVector` (FuelTank) | 空到满 CG 矢量      | `UtVec3dX`  | = mFullCgLocation_ft - mEmptyCgLocation_ft | ft         | FuelTank::CalcCgLocation_ft |

### 关键数学公式

1. **燃油箱 CG 位置线性插值**：
   CG 位置在空油箱 CG 和满油箱 CG 之间按燃油充满度线性插值：
   $$\mathbf{r}_{cg} = \mathbf{r}_{empty} + \frac{m_{current}}{m_{max}} \cdot (\mathbf{r}_{full} - \mathbf{r}_{empty})$$
   其中：
   - $\mathbf{r}_{cg}$ 为当前燃油 CG 位置矢量（ft）。
   - $\mathbf{r}_{empty}$ 为空油箱 CG 位置（通常为底部）。
   - $\mathbf{r}_{full}$ 为满油箱 CG 位置（通常为中心）。
   - $m_{current}$ 为当前燃油质量（lb）。
   - $m_{max}$ 为油箱最大容量（lb）。
   - 分数 $m_{current}/m_{max}$ 是燃油充满度。

2. **燃油消耗速率限制**：
   发动机请求的燃油燃烧速率必须受限于油箱的最大供给速率：
   $$\dot{m}_{actual} = \min\left(\dot{m}_{request}, \dot{m}_{max\_flow} \cdot \Delta t, m_{remaining}\right)$$
   其中 $\dot{m}_{request}$ 为发动机请求消耗量，$\dot{m}_{max\_flow}$ 为油箱最大供给速率（lb/s），$\Delta t$ 为时间步长（s），$m_{remaining}$ 为油箱当前剩余燃油。

3. **燃油传输协调比例因子**：
   当多个源油箱向同一目标油箱传输时，若总供给量超过目标接收能力，按比例压缩：
   $$f = \begin{cases} 1.0 & \text{if } |\sum m_{provided}| \leq |m_{max\_receive}| \\ \frac{|m_{max\_receive}|}{|\sum m_{provided}|} & \text{otherwise} \end{cases}$$
   每个源油箱实际传输量 = $f \times m_{provided\_by\_source}$。

4. **推进系统总质量属性汇总**：
   所有燃油箱的质量属性累加：
   $$m_{total} = \sum_i m_{tank\_i}, \quad \mathbf{r}_{cg\_total} = \frac{\sum_i m_{tank\_i} \cdot \mathbf{r}_{tank\_i}}{\sum_i m_{tank\_i}}$$
   其中 $m_{tank\_i}$ 表示第 i 个油箱的当前燃油质量（lb），$\mathbf{r}_{tank\_i}$ 表示其 CG 位置。

5. **百分比加油算法**：
   当添加的燃油不足以填满所有油箱时（`AddFuelQuantity_lbs`），按统一百分比填充：
   $$P = 100 \times \frac{m_{current\_total} + m_{to\_add}}{m_{max\_total}}$$
   每个油箱的目标油量 $= m_{max\_i} \times P / 100$，实际加油量 $= m_{target\_i} - m_{current\_i}$。

### 算法伪代码

```
// === 推进系统燃油管理模型 ===
// 整体目标：管理多油箱燃油消耗和油箱间传输，汇总质量属性供飞行器质心计算

// --- PropulsionSystem::Update：每帧调用 ---
function PropulsionSystem_Update(simTime_nanosec):
    dT_nanosec = simTime_nanosec - mLastSimTime_nanosec           // 时间步长 (ns)
    if dT_nanosec < 0 then return                                 // 负时间步，直接返回

    dT_sec = dT_nanosec * 1e-9                                    // 转为秒

    if parentVehicle.freezeFlags.fuelBurn:                         // 冻结标志检查
        mLastSimTime_nanosec = simTime_nanosec
        return                                                    // 燃油冻结，不处理传输

    RemoveInvalidFuelTransfers()                                   // 清理无效传输路径（如抛弃的油箱）

    // 按目标油箱分组构建 tankMatching 列表
    tankMatchingList = []
    for each transfer in mFuelTransferList:
        if transfer.targetTank already in tankMatchingList:
            add transfer.sourceTank to existing match
        else:
            create new TankMatching with targetTank + sourceTank

    // 对每个目标油箱处理传输
    for each match in tankMatchingList:
        targetTank = match.targetTank

        // 目标油箱最大接收量 = 传输速率 × dT，受满度限制
        maxTargetTransfer_lbs = targetTank.maxTransferRate_pps * dT_sec
        targetSpaceAvailable_lbs = targetTank.capacity_lbs - targetTank.currentFuel_lbs
        if maxTargetTransfer_lbs < 0 then maxTargetTransfer_lbs = 0   // 负值截断
        if targetSpaceAvailable_lbs < maxTargetTransfer_lbs:
            maxTargetTransfer_lbs = targetSpaceAvailable_lbs           // 受满度限制

        // 遍历源油箱，累积各自最大可提供量
        totalAvailable_lbs = 0.0
        for each tankData in match.sourceTankList:
            sourceTank = tankData.sourceTank
            sourceMaxTransfer = sourceTank.maxTransferRate_pps * dT_sec

            // 计算源油箱可提供量（负号表示移出）
            (canProvide, actualProvided, newMass, newCg) =
                sourceTank.CalculateFuelTransfer(dT_sec, -sourceMaxTransfer, ...)
            tankData.fuelActuallyProvided_lbs = actualProvided          // 记录每个源的提供量
            totalAvailable_lbs = totalAvailable_lbs + actualProvided    // 累积总供给

        // 计算比例因子
        if |maxTargetTransfer_lbs| > EPSILON:
            fraction = |totalAvailable_lbs| / |maxTargetTransfer_lbs|
            if fraction <= 1.0: fraction = 1.0                          // 供给不超需求，全量
            else: fraction = 1.0 / fraction                             // 等比压缩
        else:
            fraction = 0.0                                              // 目标无法接收

        // 按比例完成传输
        if fraction > EPSILON:
            for each tankData in match.sourceTankList:
                sourceTank = tankData.sourceTank
                transferAmount = -tankData.fuelActuallyProvided_lbs * fraction
                sourceTank.UpdateFuelTransfer(dT_sec, transferAmount, ...)  // 源减少
                targetTank.UpdateFuelTransfer(dT_sec, -transferAmount, ...) // 目标增加

    mLastSimTime_nanosec = simTime_nanosec                               // 保存时间戳

// --- FuelTank::CalcCgLocation_ft：CG 位置线性插值 ---
function FuelTank_CalcCgLocation_ft(currentFuelQty_lbs):
    fraction = currentFuelQty_lbs / maxQty_lbs                       // 燃油充满度 [0, 1]
    scaledVector = fraction * (fullCg_ft - emptyCg_ft)              // 按比例缩放空→满矢量
    return emptyCg_ft + scaledVector                                 // 空CG + 偏移 = 当前CG

// --- FuelTank::UpdateFuelBurn：燃油燃烧状态更新 ---
function FuelTank_UpdateFuelBurn(dT_sec, burnRequest_lbs):
    if dT_sec < EPSILON: return currentState                         // 极小时间步，不更新

    ableToProvide = CalculateFuelBurn(dT_sec, burnRequest_lbs,
                                      out actuallyBurned, out newMass, out newCg)
    // 累积临时流量速率（本帧内可能多次调用）
    mTempCurrentFuelFlow_pps = mTempCurrentFuelFlow_pps + actuallyBurned / dT_sec

    if not parentVehicle.freezeFlags.fuelBurn:                       // 未冻结才改状态
        mCurrentQuantity_lbs = max(0.0, newMass)                     // 更新油量（≥0）
        mCurrentCgLocation_ft = newCg                                // 更新CG位置

    return ableToProvide

// --- FuelTank::CalculateFuelBurn：燃油燃烧计算（不改变状态）---
function FuelTank_CalculateFuelBurn(dT_sec, burnRequest_lbs):
    requestedFlowRate_pps = burnRequest_lbs / dT_sec

    if requestedFlowRate > maxFlowRate_pps:                          // 超过供给速率上限
        limitedBurn = maxFlowRate_pps * dT_sec                       // 限制燃烧量
        burnAmount = min(burnRequest, limitedBurn)                   // 取小值
        remainingAfterBurn = currentFuel - burnAmount
        if remainingAfterBurn < 0:
            burnAmount = burnRequest + remainingAfterBurn            // 油箱见底，仅烧剩余量
    else:
        remainingAfterBurn = currentFuel - burnRequest
        if remainingAfterBurn > 0 and burnRequest >= 0:
            fullyAchieved = true
            burnAmount = burnRequest                                 // 完全满足请求
        else:
            burnAmount = burnRequest + remainingAfterBurn            // 油箱不足

    newMass = currentFuel - burnAmount
    newCg = CalcCgLocation_ft(newMass)                               // 更新CG插值
    return (fullyAchieved, burnAmount, newMass, newCg)
```

### 源码使用说明

#### 入口和调用链

```
// 从积分器主循环 → 推进系统更新 → 燃油箱更新 → 汇总质量属性
WsfSixDOF_Integrator::CalculateFM()                                        // 积分器每帧调用
  → PropulsionSystem::Update(aSimTime_nanosec)                             // 推进系统燃油管理更新
    → 计算 dT → 检查 freeze 标志
    → RemoveInvalidFuelTransfers()                                         // 清理无效传输
    → 遍历 mFuelTransferList → 构建 tankMatching 分组
    → 对每个目标：
      → tgtTank->GetMaxFuelTransferRate_pps() * dT_sec                    // 计算最大接收量
      → tgtTank->CalculateFuelTransfer(dT_sec, fuelAddRequest, ...)        // 目标接收能力计算
      → 对每个源：
        → srcTank->CalculateFuelTransfer(dT_sec, -fuelAddRequest, ...)   // 源提供能力计算
      → 计算 fraction 比例因子
      → 对每个源：
        → srcTank->UpdateFuelTransfer(dT_sec, -fraction*amount, ...)      // 源移出
        → tgtTank->UpdateFuelTransfer(dT_sec, +fraction*amount, ...)      // 目标接收
    → mLastSimTime_nanosec = aSimTime_nanosec                              // 保存时间
  → 各发动机 Engine::UpdateThrust() → FuelTank::UpdateFuelBurn()           // 燃油消耗
  → PropulsionSystem::GetMassProperties()                                   // 汇总质量属性
    → 对每个燃油箱调用 GetMassProperties()                                  // 各油箱质量+CG
```

#### 源码位置

| File | Symbol | Lines | Evidence level | 中文说明 |
| ---- | ------ | ----- | -------------- | -------- |
| [WsfSixDOF_PropulsionSystem.hpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_PropulsionSystem.hpp) | `PropulsionSystem` (class) | 34-237 | source-cited | 推进系统类全量 -- 多油箱管理 + 传输协调 |
| [WsfSixDOF_PropulsionSystem.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_PropulsionSystem.cpp) | `Update()` | 78-249 | source-cited | 推进系统更新主函数 -- 170 行传输协调 |
| [WsfSixDOF_PropulsionSystem.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_PropulsionSystem.cpp) | `GetMassProperties()` | 499-516 | source-cited | 汇总所有油箱质量属性 |
| [WsfSixDOF_PropulsionSystem.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_PropulsionSystem.cpp) | `AddFuelQuantity_lbs()` | 435-469 | source-cited | 百分比统一加油算法 |
| [WsfSixDOF_PropulsionSystem.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_PropulsionSystem.cpp) | `FillAllTanks()` | 471-489 | source-cited | 所有油箱按百分比填充 |
| [WsfSixDOF_FuelTank.hpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_FuelTank.hpp) | `FuelTank` (class) | 34-232 | source-cited | 燃油箱类全量 -- 3 种速率 + CG 插值 |
| [WsfSixDOF_FuelTank.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_FuelTank.cpp) | `CalcCgLocation_ft()` | 857-864 | source-cited | CG 位置线性插值 -- 核心 8 行 |
| [WsfSixDOF_FuelTank.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_FuelTank.cpp) | `CalculateFuelBurn()` | 307-388 | source-cited | 燃油燃烧计算（不改变状态） -- 80 行速率/容量双重限制 |
| [WsfSixDOF_FuelTank.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_FuelTank.cpp) | `UpdateFuelBurn()` | 390-431 | source-cited | 燃油燃烧状态更新 |
| [WsfSixDOF_FuelTank.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_FuelTank.cpp) | `CalculateFuelTransfer()` | 560-715 | source-cited | 燃油传输计算（双向：正=接收，负=移出） -- 155 行 |
| [WsfSixDOF_FuelTank.cpp](source_root/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_FuelTank.cpp) | `SetFullCgLocation_ft()` / `SetEmptyCgLocation_ft()` | 828-840 | source-cited | 设置满/空 CG 并计算 mCgEmptyToFullVector |

#### 框架依赖

| AFSIM 原始依赖 | 依赖类型 | 替换方案 |
| ------------ | ---- | ---- |
| `UtVec3dX` | 三维矢量 | Eigen::Vector3d |
| `UtCloneablePtr` | 智能指针（深拷贝） | std::unique_ptr/std::shared_ptr |
| `UtMath::cLB_PER_KG / cFT_PER_M` | 单位转换常数 | 直接硬编码 |
| `std::unordered_map` | 哈希映射（油箱名 → 对象） | 标准库，直接可用 |
| `Mover / Object` | 父类耦合（freeze 标志检查） | 自定义等效接口 |
| `MassProperties` | 质量属性汇总类 | Eigen 或自定义类 |

#### 测试和验证计划

1. **空油箱燃烧测试**：油箱初始量为 0，请求燃烧 > 0，验证实际消耗为 0 且 `ableToProvide = false`。
2. **超速率燃烧限制测试**：请求燃烧速率 > mMaxFlowRate_pps，验证实际燃烧量不超过 `maxFlowRate * dT`。
3. **CG 线性插值测试**：设定 fullCg=(0,0,5) 和 emptyCg=(0,0,0)，50% 油量时验证 CG=(0,0,2.5)。
4. **油箱间传输测试**：源油箱容量 100lb、目标油箱容量 100lb，传输 50lb，验证源减量=目标增量=50lb 且不超过速率限制。
5. **多源等比压缩测试**：目标油箱仅能接收 10lb，2 个源油箱各提供 20lb，验证 fraction=0.5，每源实际移出 10lb。
6. **燃油冻结测试**：设置 freezeFlags.fuelBurn=true，验证燃油消耗和传输均不生效。
7. **质心汇总测试**：2 个油箱各 100lb，CG 分别为 (1,0,0) 和 (-1,0,0)，验证总质心在 (0,0,0)。
8. **百分比加油测试**：2 个油箱容量各 100lb（当前各 0lb），添加 100lb → 各油箱变为 50lb（50% 填充）。

### 内部状态

**PropulsionSystem（推进系统）层 -- 跨帧持久化成员变量：**

| 变量名 | 类型 | 初始值 | 物理含义 | 更新时机 |
|--------|------|--------|----------|----------|
| `mFuelTransferList` | `vector<unique_ptr<FuelTransfer>>` | 空 | 预定义的油箱间传输链路列表（源→目标对） | 初始化时由 ProcessInput 构建；`RemoveInvalidFuelTransfers()` 动态移除失效链路 |
| `mFuelTankMap` | `unordered_map<string, UtCloneablePtr<FuelTank>>` | 空 | 所有燃油箱的名称→对象映射表 | 初始化时添加/移除燃油箱；抛弃油箱后移除 |
| `mLastSimTime_nanosec` | `int64_t` | 0 | 上一帧的仿真时间（ns），用于计算 dT | 每帧 `Update()` 末尾赋值 |
| `mPropulsionSystemThrottleLeverPosition` | `double` | 0.0 | 推进系统级总油门杆位置（可覆盖各发动机） | 脚本调用设置 |
| `mThrottleLeverPositionSet` | `bool` | false | 标记是否已设定系统级油门 | 设定时置 true |
| `mEnableThrustVectoring` | `bool` | false | 是否启用推力矢量控制 | 初始化时配置 |

**FuelTank（燃油箱）层 -- 跨帧持久化成员变量：**

| 变量名 | 类型 | 初始值 | 物理含义 | 更新时机 |
|--------|------|--------|----------|----------|
| `mMaxFlowRate_pps` | `double` | 0.0 | 油箱向发动机供油的最大速率（lb/s） | 初始化时配置 |
| `mMaxFillRate_pps` | `double` | 0.0 | 外部加油时油箱接受燃油的最大速率（lb/s） | 初始化时配置 |
| `mMaxTransferRate_pps` | `double` | 0.0 | 油箱间燃油传输的最大速率（lb/s） | 初始化时配置 |
| `mMaxQuantity_lbs` | `double` | 0.0 | 油箱最大容量（lb） | 初始化时配置 |
| `mCurrentQuantity_lbs` | `double` | 0.0 | 当前燃油质量（lb）-- 核心状态 | 每帧 `CalculateFuelBurn`/`UpdateFuelBurn`/`Fill`/`Transfer` 更新 |
| `mCurrentFuelFlow_pps` | `double` | 0.0 | 当前向发动机供油的流出速率（lb/s） | 每帧 `Update()` 中由临时速率提交 |
| `mCurrentFillRate_pps` | `double` | 0.0 | 当前外部加油的流入速率（lb/s） | 每帧 `Update()` 中由临时速率提交 |
| `mCurrentTransferRate_pps` | `double` | 0.0 | 当前传输速率（正=接收，负=移出）（lb/s） | 每帧 `Update()` 中由临时速率提交 |
| `mTempCurrentFuelFlow_pps` | `double` | 0.0 | 本帧内累积的临时供油速率（可能多次调用 UpdateFuelBurn） | 每次 `UpdateFuelBurn` 调用时累加；`Update()` 末尾清零 |
| `mTempCurrentFillRate_pps` | `double` | 0.0 | 本帧内累积的临时加油速率 | 每次 `UpdateFuelFill` 调用时累加；`Update()` 末尾清零 |
| `mTempCurrentTransferRate_pps` | `double` | 0.0 | 本帧内累积的临时传输速率 | 每次 `UpdateFuelTransfer` 调用时累加；`Update()` 末尾清零 |
| `mCurrentCgLocation_ft` | `UtVec3dX` | (0,0,0) | 当前燃油质心位置（ft），相对于父对象 | 每次油量变化后调用 `CalcCgLocation_ft()` 更新 |
| `mFullCgLocation_ft` | `UtVec3dX` | 配置值 | 油箱满时燃油质心位置（ft），通常为油箱中心 | 初始化时配置 |
| `mEmptyCgLocation_ft` | `UtVec3dX` | 配置值 | 油箱空时燃油质心位置（ft），通常为油箱底部 | 初始化时配置 |
| `mCgEmptyToFullVector` | `UtVec3dX` | = fullCg - emptyCg | 空到满质心的偏移矢量（ft） | `SetFullCgLocation_ft`/`SetEmptyCgLocation_ft` 被调用时更新 |
| `mLastSimTime_nanosec` | `int64_t` | 0 | 上一帧仿真时间（ns） | 每帧 `Update()` 末尾赋值 |
| `mMassProperties` | `MassProperties` | 默认 | 燃油箱当前质量属性（含质量+CG） | `CalculateCurrentMassProperties()` 中更新 |

### 变量映射表

| 代码变量 | 数学符号 | 含义 |
|----------|----------|------|
| `dT_sec` | $\Delta t$ | 仿真时间步长（s） |
| `mCurrentQuantity_lbs` | $m_{current}$ | 当前燃油质量（lb） |
| `mMaxQuantity_lbs` | $m_{max}$ | 油箱最大容量（lb） |
| `mCurrentCgLocation_ft` | $\mathbf{r}_{cg}$ | 当前 CG 位置矢量（ft） |
| `mEmptyCgLocation_ft` | $\mathbf{r}_{empty}$ | 空油箱 CG 位置（ft） |
| `mFullCgLocation_ft` | $\mathbf{r}_{full}$ | 满油箱 CG 位置（ft） |
| `mCgEmptyToFullVector` | $\mathbf{r}_{full} - \mathbf{r}_{empty}$ | 空到满 CG 偏移矢量（ft） |
| `fraction` (CG) | $m_{current} / m_{max}$ | 燃油充满度 [0, 1] |
| `aFuelBurnRequest_lbs` | $\dot{m}_{request} \cdot \Delta t$ | 请求燃烧的燃油质量（lb） |
| `mMaxFlowRate_pps` | $\dot{m}_{max\_flow}$ | 最大供油速率（lb/s） |
| `aFuelActuallyProvided_lbs` | $m_{actual}$ | 实际供给的燃油质量（lb） |
| `mMaxTransferRate_pps` | $\dot{m}_{max\_transfer}$ | 最大传输速率（lb/s） |
| `maxTargetTransfer_lbs` | $m_{max\_receive}$ | 目标油箱最大接收量（lb） |
| `totalAvailable_lbs` | $\sum m_{provided}$ | 所有源油箱可提供量之和（lb） |
| `fraction` (传输) | $f$ | 传输比例因子，$f \in [0, 1]$ |
| `mFuelTransferList[i].sourceTankName` | — | 传输源油箱名称 |
| `mFuelTransferList[i].targetTankName` | — | 传输目标油箱名称 |
| `mCurrentFuelFlow_pps` | $\dot{m}_{flow}$ | 当前供油速率（lb/s） |
| `mCurrentFillRate_pps` | $\dot{m}_{fill}$ | 当前加油速率（lb/s） |
| `mCurrentTransferRate_pps` | $\dot{m}_{transfer}$ | 当前传输速率（lb/s） |
| `mLastSimTime_nanosec` | $t_{last}$ | 上一帧仿真时间（ns） |
| `aSimTime_nanosec` | $t_{sim}$ | 当前帧仿真时间（ns） |
| `burnRequest_lbs` | $m_{burn\_request}$ | 请求燃烧的燃油质量（lb） |

### 边界条件

1. **负时间步保护**：`PropulsionSystem::Update()` 中计算 `dT_nanosec = aSimTime - mLastSimTime`，若 `dT_nanosec < 0` 则直接返回（跳过本帧所有燃油操作），避免因仿真时钟回退导致异常。

2. **极小时间步 / 零时间步保护**：在 `FuelTank::UpdateFuelBurn()`、`CalculateFuelBurn()`、`Transfer`、`Fill` 等函数中，当 `aDeltaT_sec < EPSILON` 时直接返回当前状态而不做任何修改，防止除零（速率 = 质量 / 时间）。

3. **燃油冻结标志**：当 `parentVehicle.freezeFlags.fuelBurn == true` 时，`PropulsionSystem::Update()` 仅保存时间戳后直接返回，不处理任何传输。引擎侧的 `UpdateThrust()` 也会检查此标志，冻结时不更新 `mCurrentQuantity_lbs`（不改变油量但可执行计算）。

4. **油量非负下限**：`UpdateFuelBurn()` 中油量更新为 `mCurrentQuantity_lbs = max(0.0, newMass)`，确保燃油质量永远不会为负数。同理在 `CalculateFuelBurn()` 中，如果 `remainingAfterBurn < 0`（油箱不够烧），`burnAmount = burnRequest + remainingAfterBurn`（仅烧掉剩余部分）。

5. **超速率燃烧限幅**：`CalculateFuelBurn()` 中限制实际燃烧量不超过 `mMaxFlowRate_pps * dT_sec`。若请求速率超过上限，`burnAmount` 被缩至速率限幅值。并且如果 `burnAmount` 超出当前剩余油量，最终 `burnAmount` 进一步缩至剩余量。

6. **油箱满度截断**：在 `CalculateFuelTransfer()` 和 `CalculateFuelFill()` 中，目标油箱的最大接收量受 `mMaxQuantity_lbs - mCurrentQuantity_lbs` 限制（即油箱空余容量）。超过空余容量的接收量被截断。同理，计算源油箱移出量时受 `mCurrentQuantity_lbs` 限制（不可移出超过当前油量的燃油）。

7. **传输比例因子钳制**：
   - 当 `|∑ provided| ≤ |maxTargetTransfer|` 时：`fraction = 1.0`（全量传输）。
   - 当 `|∑ provided| > |maxTargetTransfer|` 时：`fraction = |maxTargetTransfer| / |∑ provided|`（等比压缩）。
   - 当 `|maxTargetTransfer| ≤ EPSILON` 时：`fraction = 0.0`（目标无法接收任何燃油）。
   - 当 `fraction ≤ EPSILON` 时：跳过实际传输步骤。

8. **无效传输路径清理**：`RemoveInvalidFuelTransfers()` 在每帧开始前遍历 `mFuelTransferList`，检查 `sourceTank` 和 `targetTank` 指针是否仍然有效（非 null 且在 `mFuelTankMap` 中存在）。如果油箱被抛弃（`RemoveFuelTankByName`），相关传输链路被移除，避免悬空指针访问。

9. **CG 位置空/满线性插值边界**：`CalcCgLocation_ft()` 中 `fraction = currentQty / maxQty` 的计算隐含了 `mMaxQuantity_lbs == 0` 时的除零风险（实际中 `maxQty` 应大于 EPSILON）。空油箱时 fraction = 0，CG = emptyCg；满油箱时 fraction = 1，CG = fullCg。建议移植时增加 `if (maxQty < EPSILON) return emptyCg` 的保护。

10. **百分比加油算法保护**：`AddFuelQuantity_lbs()` 中若总容量为 0（无油箱或有油箱但容量均为 0），百分比计算会导致除零。建议移植时增加保护：`if totalCapacity < EPSILON -> return 0`。

### 提取策略

- **源文件**：
  - `source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_PropulsionSystem.hpp`（PropulsionSystem 类声明，含 mFuelTankMap、mFuelTransferList 等）
  - `source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_PropulsionSystem.cpp`（Update、GetMassProperties、AddFuelQuantity_lbs、FillAllTanks 等实现）
  - `source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_FuelTank.hpp`（FuelTank 类声明，含 3 种速率 + CG 插值 + 各状态变量）
  - `source_root/afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfSixDOF_FuelTank.cpp`（CalcCgLocation_ft、CalculateFuelBurn/UpdateFuelBurn、CalculateFuelTransfer/UpdateFuelTransfer 等实现）
- **提取方法**：通过读取 `.hpp` 头文件获取所有成员变量的类型和默认初始值（注意 c++ 类内初始化语法 `= 0.0`）；通过阅读 `.cpp` 文件的 `Update()`、`CalculateFuelBurn()`、`UpdateFuelBurn()`、`CalculateFuelTransfer()` 等函数追踪每个变量的读写位置。
- **函数识别**：从 `workspace/source-index/wsf_plugins/function-index.jsonl` 中可搜索 `wsf_p6dof::` 命名空间的 `PropulsionSystem` 和 `FuelTank` 相关函数。`CalcCgLocation_ft`（位置 857-864，核心 8 行）、`CalculateFuelBurn`（307-388，80 行）、`Update`（每帧主入口）是核心算法函数。
- **还原方式**：数学公式来自源码中对 CG 线性插值和速率限制逻辑的直接提取。变量映射表覆盖公式中使用的全部关键符号。该算法的核心逻辑极其简单（线性插值+速率限制+比例分配），提取的重点在于正确追踪"临时速率→永久速率"的两阶段提交机制。

#### 可移植性评分

**可移植性**：高

**原因**：

1. 核心算法均为基本数学运算：线性插值（CG）、速率限制比较、比例分配，无任何领域特定黑盒。
2. CG 位置线性插值公式极其简单（`emptyCg + fraction * (fullCg - emptyCg)`），一行代码即可实现。
3. 传输比例因子算法是通用资源分配逻辑，仅含加减乘除和条件分支。
4. 主要复杂度在管理逻辑（传输分组、比例计算）而非数学计算，适合任何编程语言。
5. 唯一外部依赖为矢量运算类 `UtVec3dX`，可直接替换为 `Eigen::Vector3d`。
6. 单位体系为 Imperial（lb, ft），但 CG 插值和速率限制的单位转换对算法本身无影响。
7. 燃油箱质量属性汇总使用简单的质量加权平均，公式为标准物理原理。
