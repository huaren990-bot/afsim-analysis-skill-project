# 均匀大气声吸收算法接口规格

> **算法 ID**：ALG-SENSORS-ACOUSTIC-ATMOSPHERIC-ABSORPTION  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-acoustic-atmospheric-absorption-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：用一组已采样的大气状态和频率计算 dB/100 m 声吸收率。
- 调用时机：声传播模型处理一个频带时；总距离衰减由调用者换算。
- 包含/不包含：包含分子弛豫和经典吸收；不包含大气采样、路径积分、几何扩散、地面效应和 Doppler。
- 可重入/线程安全：纯函数，无共享状态时可重入且线程安全。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `temperature_k` | `double` | K | 无 | 有限且 $>0$ | 当前路径代表值 |
| `relative_humidity` | `double` | 1 | 无 | $[0,1]$ | 当前路径代表值 |
| `pressure_pa` | `double` | Pa | 无 | 有限且 $>0$ | 当前路径代表值 |
| `sea_level_pressure_pa` | `double` | Pa | 无 | 有限且 $>0$ | 同一大气模型参考值 |
| `frequency_hz` | `double` | Hz | 无 | 有限且 $>0$；AFSIM 使用 50–10000 Hz 频带 | 当前频带 |
| `attenuation_db_per_100m` | `double` | dB/100 m | 无 | 有限且通常 $\ge0$ | 本次计算 |

内部统一使用 SI 输入。相对湿度必须是比例值，例如 50% 传入 `0.5`。

## 3. 中性数据类型

```cpp
// 中文：算法输入；大气状态由调用者在代表高度处采样。
struct AcousticAtmosphericAbsorptionInput
{
    double temperature_k{};            // 中文：绝对温度，K，必须 > 0
    double relative_humidity{};        // 中文：相对湿度比例，[0, 1]
    double pressure_pa{};              // 中文：代表高度压力，Pa，必须 > 0
    double sea_level_pressure_pa{};    // 中文：同一模型海平面压力，Pa，必须 > 0
    double frequency_hz{};             // 中文：声频率，Hz，必须 > 0
};

// 中文：算法输出；距离尚未计入。
struct AcousticAtmosphericAbsorptionOutput
{
    double attenuation_db_per_100m{};  // 中文：每 100 m 声压级损失
};

enum class AcousticAbsorptionError
{
    none,
    non_finite_input,
    non_positive_temperature,
    invalid_humidity,
    non_positive_pressure,
    non_positive_frequency,
    non_finite_output
};

template<class T>
struct Result
{
    T value{};
    AcousticAbsorptionError error{AcousticAbsorptionError::none};
};
```

算法无 `State` 与运行时配置；经验系数属于受版本控制的模型定义。

## 4. 核心接口

```cpp
// 中文：计算单位 100 m 的大气声吸收率，不读取全局环境或修改状态。
Result<AcousticAtmosphericAbsorptionOutput>
compute_acoustic_atmospheric_absorption(
    const AcousticAtmosphericAbsorptionInput& input);

// 中文：把单位 100 m 的结果换算为指定非负距离上的总 dB 衰减。
Result<double> scale_absorption_to_range(
    double attenuation_db_per_100m,
    double range_m);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_acoustic_atmospheric_absorption` | 所有输入有限并满足第 2 节范围 | 成功时输出有限 | 无 | $O(1)$；若干 `exp/pow/log10/sqrt` |
| `scale_absorption_to_range` | 吸收率有限，`range_m >= 0` | 返回 `attenuation * range_m * 0.01` | 无 | $O(1)$ |

## 5. 状态生命周期

| 状态 | 初值 | 读取时机 | 更新时机 | 重置规则 | 序列化/复制 |
| --- | --- | --- | --- | --- | --- |
| 无 | — | — | — | 无需重置 | 无需序列化 |

大气沿程变化由调用者处理：可对路径分段采样并累加每段 dB 损失，不应在本纯函数中隐藏环境状态。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| NaN/Inf | 函数入口 | 返回 `non_finite_input` | 修复环境采样 |
| $T\le0$ | 函数入口 | 返回 `non_positive_temperature` | 使用 K |
| $H_r\notin[0,1]$ | 函数入口 | 返回 `invalid_humidity` | 百分数先除以 100 |
| 压力 $\le0$ | 函数入口 | 返回 `non_positive_pressure` | 限定大气模型有效高度 |
| $f\le0$ | 函数入口 | 返回 `non_positive_frequency` | 传入正频率 |
| 输出 NaN/Inf | 核心公式后 | 返回 `non_finite_output` | 记录输入并停止传播计算 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `0.5*(mRcvrLoc.mAlt+mTgtLoc.mAlt)` | 调用者采样高度 | 两端高度取平均，m | 沿程分层信息 | `WsfAcousticSensor.cpp:650-657` |
| `mAtmosphere.Temperature(alt)` | `temperature_k` | 直接传 K | 大气类型标识 | `WsfAcousticSensor.cpp:653` |
| `mAtmosphere.RelativeHumidity(alt)` | `relative_humidity` | 无量纲比例 | 湿度剖面 | `WsfAcousticSensor.cpp:654` |
| `mAtmosphere.Pressure(alt/0)` | 两个压力字段 | 直接传 Pa | 完整压力剖面 | `WsfAcousticSensor.cpp:655-657` |
| `AtmosphericAttenuation(aResult, aFreq)` | `compute_acoustic_atmospheric_absorption` | 展开框架对象 | 无 | `WsfAcousticSensor.cpp:648-675` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfSensorResult` | 提供位置和距离 | 移除 | 显式标量输入；距离单独缩放 | 调用者须统一单位 |
| `UtAtmosphere` | 环境采样 | 替换 | 由上层环境服务采样后传值 | 采样高度选择影响结果 |
| `std::cmath` | 数学函数 | 保留等价能力 | 目标语言标准数学库 | 浮点库差异 |

## 9. 最小调用示例

```cpp
AcousticAtmosphericAbsorptionInput input{
    .temperature_k = 288.15,          // 中文：标准海平面温度
    .relative_humidity = 0.5,         // 中文：50% 相对湿度
    .pressure_pa = 101330.0,          // 中文：代表高度压力
    .sea_level_pressure_pa = 101330.0,
    .frequency_hz = 1000.0
};

// 中文：期望约为 0.29636178637145016 dB/100 m。
const auto result = compute_acoustic_atmospheric_absorption(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 288.15 K、0.5、压力比 1、1000 Hz | `0.29636178637145016` dB/100 m | 绝对误差 $\le10^{-12}$ | 超差或非有限 |
| 边界 | 湿度 0，其余合法 | 独立公式实现 | 有限且非负 | NaN/Inf/负值 |
| 距离换算 | 正常 oracle、1000 m | `2.9636178637145016` dB | 绝对误差 $\le10^{-11}$ | 单位换算错误 |
| 退化 | 0 Hz、0 K、0 Pa、NaN | 对应错误码 | 不返回数值结果 | 进入核心公式 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| Q-001 | ESDU #78002 与代码经验系数是否逐项一致 | 模型来源可追溯性 | 合法取得的原文与版本信息 | no |
| Q-002 | 新系统是否要求沿程分层积分 | 精度和接口上层设计 | 目标系统精度需求 | no |
