# ESA 加权相控阵阵因子算法接口规格

> **算法 ID**：ALG-SENSORS-ESA-WEIGHTED-ARRAY-FACTOR  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-esa-weighted-array-factor-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 以纯函数计算带幅度权重与有限相位位数的线性功率阵因子。
- 复刻 AFSIM 的频率回退、相位表达式、向零量化和总阵元数归一化。
- 不生成位置/权重，不计算阵元方向图、直射增益或外围扫描损失。
- 无共享状态，可重入、线程安全。

## 2. 单位与坐标系

| 量 | 类型 | 单位/坐标系 | 有效范围 |
| --- | --- | --- | --- |
| `frequency_hz` | `double` | Hz | 有限；`>0` 为物理频率，`<=0` 请求源码匹配回退 |
| `element_spacing_x/y_m` | `double` | m | 回退所用轴必须有限且 `>0` |
| `steering_azimuth/elevation_rad` | `double` | rad，ESA 本地角 | 有限 |
| `look_azimuth/elevation_rad` | `double` | rad，ESA 本地角 | 有限 |
| `position_m` | 三元组 | m，ESA 局部 XYZ | 每项有限 |
| `weight` | `double` | 1，幅度 | 有限 |
| `phase_quantization_bits` | `int` | bit | 安全接口 `0..30` |

观察角应是 AFSIM `ComputeGain` 接收的总图样角；公共 `GetGain` 会先把目标相对角与 EBS 角相加。

## 3. 中性数据类型

```cpp
enum class EsaArrayFactorStatus
{
    ok,
    matched_spacing_fallback,
    invalid_dimensions,
    invalid_spacing,
    invalid_quantization_bits,
    non_finite_input,
    non_finite_output
};

struct EsaArrayElement
{
    std::array<double, 3> position_m{};
    double weight{1.0};
};

enum class ZPhasePolicy
{
    source_compatible,
    geometrically_consistent
};

struct EsaArrayFactorInput
{
    std::size_t element_count_x{};
    std::size_t element_count_y{};
    double element_spacing_x_m{};
    double element_spacing_y_m{};
    double frequency_hz{};
    double steering_azimuth_rad{};
    double steering_elevation_rad{};
    double look_azimuth_rad{};
    double look_elevation_rad{};
    int phase_quantization_bits{};
    ZPhasePolicy z_phase_policy{ZPhasePolicy::source_compatible};
    std::vector<EsaArrayElement> elements;
};

struct EsaArrayFactorOutput
{
    double wavelength_m{};
    double real_sum{};
    double imaginary_sum{};
    double linear_power_factor{};
    EsaArrayFactorStatus status{EsaArrayFactorStatus::ok};
};
```

## 4. 核心接口

```cpp
Result<EsaArrayFactorOutput>
compute_esa_weighted_array_factor(const EsaArrayFactorInput& input);
```

| 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- |
| 数量匹配且第 2 节门禁通过 | 成功时波长、复数和与功率有限 | 无 | $O(N_xN_y)$ 时间，$O(1)$ 额外空间 |

`geometrically_consistent` 是显式修正模式，不可用于声称逐行为 AFSIM 兼容的验证。

## 5. 状态生命周期

算法无状态。阵元位置、权重和相位位数由初始化适配层产生；运行期每次频率、观察角或转向角变化均重新计算。不得跨频率缓存波长或相位。

## 6. 错误与边界

| 条件 | 状态 | 输出策略 |
| --- | --- | --- |
| `Nx==0`、`Ny==0` 或元素长度不等于乘积 | `invalid_dimensions` | 无输出 |
| 频率回退所需间距非正/非有限 | `invalid_spacing` | 无输出 |
| 位数不在 `0..30` | `invalid_quantization_bits` | 无输出 |
| 位置、权重或角非有限 | `non_finite_input` | 无输出 |
| 最终字段非有限 | `non_finite_output` | 无输出 |
| `frequency<=0` 且回退有效 | `matched_spacing_fallback` | 返回兼容结果并标记非物理频率来源 |

权重可全零，此时结果合法为 0；这是与孔径效率接口不同的边界。

## 7. AFSIM 到中性接口映射

| AFSIM 状态/API | 中性字段 | 转换 | 源码证据 |
| --- | --- | --- | --- |
| `aFrequency` | `frequency_hz` | Hz 直接复制 | `WsfESA_AntennaPattern.cpp:440-455` |
| `mNX/mNY` | 两个 count | 正整数转换 | `.cpp:446-447` |
| `mdX/mdY` | 两个 spacing | m 直接复制 | `.cpp:448-449` |
| `mElements[].mLocation` | `position_m` | XYZ 直接复制 | `.cpp:477-489` |
| `mElements[].mWeight` | `weight` | 直接复制 | `.cpp:491-492` |
| `mPhaseNumBits` | `phase_quantization_bits` | 直接复制 | `.cpp:484` |
| `aEBS_*`, `aAz/ElAngle` | steering/look | rad 直接复制 | `.cpp:480-489` |

## 8. 依赖替换

| AFSIM 依赖 | 中性方案 | 风险 |
| --- | --- | --- |
| `UtVec3d` | `std::array<double,3>` | 坐标约定需固定 |
| `UtMath::cLIGHT_SPEED` | 精确 `299792458.0` | 无 |
| `UtMath::cTWO_PI` | `2*std::numbers::pi` | 无 |
| `ComputeQuantizationError` | 与 Taylor 接口共用向零量化 | 负相位语义 |

## 9. 最小调用示例

```cpp
const EsaArrayFactorInput input{
    .element_count_x = 2,
    .element_count_y = 1,
    .element_spacing_x_m = 0.05,
    .element_spacing_y_m = 0.0,
    .frequency_hz = 2997924580.0,
    .steering_azimuth_rad = 0.0,
    .steering_elevation_rad = 0.0,
    .look_azimuth_rad = std::numbers::pi / 6.0,
    .look_elevation_rad = 0.0,
    .phase_quantization_bits = 0,
    .elements = {
        {{{-0.025, 0.0, 0.0}}, 1.0},
        {{{ 0.025, 0.0, 0.0}}, 1.0}
    }
};

const auto result = compute_esa_weighted_array_factor(input);
// result.value.linear_power_factor ≈ 0.5
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差 |
| --- | --- | --- | --- |
| 波束中心 | 第 9 节观察角改 0 | `1` | `1e-15` |
| 偏轴 | 第 9 节 | `0.5000000000000002` | `1e-14` |
| 锥削 | 波束中心、权重 `[1,0.5]` | `0.5625` | 精确 |
| 匹配转向 | look/steering 均 30°、bits=0 | `1` | `1e-15` |
| 2 bit 转向 | 上例 bits=2 | `0.5000000000000002` | `1e-14` |
| 回退 | `frequency=0`、2×1、`dx=0.05` | 波长 `0.1`，状态 fallback | 精确 |
| 门禁 | 维数不匹配、回退间距 0、NaN | 对应错误状态 | 精确 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 阻塞 |
| --- | --- | --- | --- | --- |
| ESA-AF-001 | 非平面阵列 Z 项的 `cos(el)`/`sin(el)` 差异是否缺陷 | 决定派生阵列迁移公式 | 派生类、模型参考与黄金场景 | yes |
| ESA-AF-002 | 二维非等间距的 `lambda=dx+dy` 回退是否正式契约 | 零频率调用兼容性 | 用户手册/场景 | yes |
| ESA-AF-003 | 相位量化是否应改为最近级或环形量化 | 物理改进模式 | 需求与回归数据 | no |
