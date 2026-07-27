# OTH 电离层传播特性算法接口规格

> **算法 ID**：ALG-SENSORS-OTH-IONOSPHERIC-CHARACTERISTICS  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-oth-ionospheric-characteristics-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：以显式标量输入复现 OTH 电离层频率和球形地球单跳范围计算。
- 包含太阳几何、简化电子密度、临界/最低可用频率、入射角和距离；不查询平台、修改天线或写日志。
- 相同输入得到相同输出；纯函数可重入、线程安全。
- 默认兼容 AFSIM 2.9 常量，但以状态码显式暴露源码中的非有限结果条件。

## 2. 单位与坐标系

| 量 | 类型 | 单位/坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- |
| `radar_latitude_deg` | `double` | deg，LLA 纬度 | `[-90,90]` | 本次重算 |
| `day_of_year` | `int` | day | `[1,365]` | 源码不支持 366 |
| `local_solar_hour` | `int` | h | `[1,24]` | 调用者负责经度/UTC 换算 |
| `peak_electron_density_per_m3` | `double` | m⁻³（推断） | 有限且 `>0` | 配置状态 |
| `peak_height_m` / `reflection_height_m` | `double` | m | 有限且 `>0` | 配置状态 |
| `electron_temperature_k` | `double` | K（推断） | 有限且 `>0` | 配置状态 |
| `radar_frequency_hz` | `double` | Hz | 有限且 `>0` | 当前模式 |
| 角输出 | `double` | rad；入射角另有 deg | 见输出状态 | 本次重算 |
| 范围输出 | `double` | m，球面弧长 | 有限且 `>=0` | 本次重算 |

## 3. 中性数据类型

```cpp
struct OthIonosphereInput
{
    double radar_latitude_deg{};
    int day_of_year{};
    int local_solar_hour{};
    double peak_electron_density_per_m3{};
    double peak_height_m{};
    double reflection_height_m{};
    double electron_temperature_k{};
    double radar_frequency_hz{};
    double spherical_earth_radius_m{6366707.0194937075};
};

enum class OthIonosphereStatus
{
    ok,
    invalid_input,
    night_side_model_undefined,
    propagation_frequency_too_low,
    minimum_range_domain_error,
    non_finite_output
};

struct OthIonosphereOutput
{
    double solar_hour_angle_rad{};
    double solar_declination_rad{};
    double solar_zenith_angle_rad{};
    double reflection_electron_density_per_m3{};
    double critical_frequency_hz{};
    double minimum_usable_frequency_hz{};
    double maximum_incidence_angle_deg{};
    double minimum_range_m{};
    double maximum_range_m{};
    bool propagation_supported{};
    bool minimum_range_valid{};
};

template<class T>
struct Result
{
    T value{};
    OthIonosphereStatus status{OthIonosphereStatus::ok};
};
```

`reflection_electron_density_per_m3` 是源码局部量 `nE` 的诊断性暴露；AFSIM 当前成员 `mComputedElectronicDensity` 未在该函数中赋值。

## 4. 核心接口

```cpp
// 中文：计算 OTH 电离层和单跳距离；不访问 AFSIM 对象。
Result<OthIonosphereOutput>
compute_oth_ionospheric_characteristics(const OthIonosphereInput& input);
```

| 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- |
| 输入有限并满足第 2 节范围 | `ok` 时所有标量有限，且 `minimum_range_valid=true` | 无 | $O(1)$ |

## 5. 状态生命周期

接口本身无状态。AFSIM 适配层可在配置、频率或雷达位置变化时调用，并在成功后把输出写回波束缓存；是否清除“dirty”标志由适配层决定。

## 6. 错误与边界

| 条件 | 状态 | 输出策略 |
| --- | --- | --- |
| NaN/Inf、范围或正值约束失败 | `invalid_input` | 不进入公式 |
| $\cos\chi\le0$ | `night_side_model_undefined` | 不复刻 `DBL_MAX` 的不稳定乘积 |
| $f_r\le1.03f_c$ | `propagation_frequency_too_low` | 保留频率输出，`propagation_supported=false`，入射角 0，最小范围无效 |
| $A\sin b/B\notin[-1,1]$ | `minimum_range_domain_error` | 保留频率、入射角和最大范围，最小范围无效 |
| 其余输出非有限 | `non_finite_output` | 调用者不得用于天线限制 |

兼容适配层若必须逐项复刻源码，可在上述两个距离错误分支写入 IEEE NaN；安全接口不得静默把 `asin` 参数钳制到 1，因为那会改变模型行为。

## 7. AFSIM 到中性接口映射

| AFSIM 状态/API | 中性字段 | 转换 | 源码证据 |
| --- | --- | --- | --- |
| `GetLocationLLA(radarLat, radarLon, radarAlt)` | `radar_latitude_deg` | 仅取纬度 | `WsfOTH_RadarSensor.cpp:1002-1009` |
| `mSolarCharacteristics` | 日、小时 | 直接复制 | `WsfOTH_RadarSensor.cpp:1013-1027` |
| `mIonosphericCharacteristics` 四个配置量 | 密度、高度、温度 | 高度保持 m；密度/温度单位为物理推断 | `WsfOTH_RadarSensor.cpp:1029-1047` |
| `mXmtrPtr->GetFrequency()` | `radar_frequency_hz` | 直接复制 | `WsfOTH_RadarSensor.cpp:1051` |
| `UtSphericalEarth::cEARTH_RADIUS` | `spherical_earth_radius_m` | 默认常量 | `UtSphericalEarth.hpp:40` |

## 8. 依赖替换

| 依赖 | 处理 | 中性方案 | 风险 |
| --- | --- | --- | --- |
| 平台/发射机 | 移除 | 调用者传纬度和 Hz | 适配层单位错误 |
| `UtSphericalEarth` | 替换 | 显式半径，默认保持 AFSIM 值 | 更换半径会改变范围 |
| 日志 | 替换 | 状态码和外层诊断 | 调用者须记录失败 |
| 数学库 | 保留等价能力 | `sin/cos/asin/acos/exp/sqrt` | 极端值跨平台差异 |

## 9. 最小调用示例

```cpp
const OthIonosphereInput input{
    .radar_latitude_deg = 30.0,
    .day_of_year = 172,
    .local_solar_hour = 12,
    .peak_electron_density_per_m3 = 4.0e11,
    .peak_height_m = 250000.0,
    .reflection_height_m = 300000.0,
    .electron_temperature_k = 1540.0,
    .radar_frequency_hz = 6.0e6
};

// 中文：期望临界频率约 5.096157443 MHz，最小范围约 376.367 km。
const auto result = compute_oth_ionospheric_characteristics(input);
```

## 10. 验证契约

| 测试 | Oracle/不变量 | 容差 |
| --- | --- | --- |
| 正常样例 | `critical=5096157.443154109` Hz、`minimum_usable=5249042.166448732` Hz | 相对误差 `1e-12` |
| 正常样例 | `incidence=58.14208128741023` deg、`min=376367.0394286476` m、`max=3834484.6233969247` m | 相对误差 `1e-12` |
| 低频 | 频率等于最低可用频率 | 精确返回 `propagation_frequency_too_low` |
| 夜侧 | 30°、第 172 日、24 时 | `night_side_model_undefined` |
| 范围定义域 | 同正常样例但 20 MHz，`asin` 参数 `1.012556465356911` | `minimum_range_domain_error` |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 阻塞 |
| --- | --- | --- | --- | --- |
| OTH-001 | 电子温度和密度配置的正式单位 | 接口单位确认 | AFSIM 用户输入文档/模型参考 | yes，阻塞无条件迁移 |
| OTH-002 | 夜侧期望物理模型 | 夜间传播结果 | 模型设计说明或黄金场景 | yes |
| OTH-003 | 最小距离 `asin` 越界是否为已知缺陷 | 高频范围输出 | AFSIM 回归结果/维护记录 | yes |
| OTH-004 | `minimum usable frequency` 命名是否有领域特定含义 | API 命名 | OTH 模型参考资料 | no |
