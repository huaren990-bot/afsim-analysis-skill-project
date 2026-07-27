# ESA Taylor 阵元幅度加权算法接口规格

> **算法 ID**：ALG-SENSORS-ESA-TAYLOR-DISTRIBUTION-WEIGHTS  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-esa-taylor-distribution-weights-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 以纯函数生成 X/Y 离散 Taylor 权重和源码兼容二维阵元权重。
- 同时暴露归一化未量化权重与量化结果，保留 AFSIM 的更新顺序。
- 不布局阵元、不选择失效阵元、不计算效率或阵因子。
- 无共享状态，可重入、线程安全。

## 2. 单位与有效范围

| 字段 | 类型 | 单位 | 安全接口约束 |
| --- | --- | --- | --- |
| `element_count_x/y` | `size_t` | 1 | `>=1` |
| `sidelobe_power_ratio_x/y` | `double` | 线性功率比 | 若对应 `n_bar>1`，有限且 `>=10^(15/10)`、`<=10^(55/10)` |
| `n_bar_x/y` | `int` | 1 | `>=1` 且建议 `<=element_count` |
| `amplitude_quantization_bits` | `int` | bit | `0..30`；上限为中性安全策略 |
| `initial_element_weights` | `vector<double>` | 1 | 长度 `Nx*Ny` 且有限 |

输入的 30 dB 副瓣水平应写成线性功率比 `1000`，不是 `30`。

## 3. 中性数据类型

```cpp
enum class TaylorWeightStatus
{
    ok,
    invalid_dimensions,
    invalid_sidelobe_ratio,
    invalid_n_bar,
    invalid_quantization_bits,
    non_finite_input,
    non_positive_normalizer,
    non_finite_output
};

struct TaylorAxisInput
{
    std::size_t element_count{};
    double sidelobe_power_ratio{};
    int n_bar{1};
};

struct EsaTaylorWeightsInput
{
    TaylorAxisInput x;
    TaylorAxisInput y;
    int amplitude_quantization_bits{};
    std::vector<double> initial_element_weights;
};

struct EsaTaylorWeightsOutput
{
    std::vector<double> normalized_x;
    std::vector<double> normalized_y;
    std::vector<double> quantized_x;
    std::vector<double> quantized_y;
    std::vector<double> source_compatible_element_weights;
};

template<class T>
struct Result
{
    T value{};
    TaylorWeightStatus status{TaylorWeightStatus::ok};
};
```

## 4. 核心接口

```cpp
Result<EsaTaylorWeightsOutput>
compute_esa_taylor_distribution_weights(const EsaTaylorWeightsInput& input);

// 中文：复刻 AFSIM 的 2^bits 等间隔、向零截断量化。
Result<double>
quantize_toward_zero(double value, int bits, double full_range);
```

| 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- |
| 第 2 节门禁通过 | 成功时所有向量尺寸匹配、值有限 | 无 | $O[N_x\bar n_x^2+N_y\bar n_y^2+N_xN_y]$ |

## 5. 状态生命周期

接口无状态。AFSIM 适配层在阵列尺寸确定后调用一次，将
`source_compatible_element_weights` 写入阵元，再由失效模型修改；任何尺寸、Taylor 参数或量化位数变化都必须重算。

## 6. 错误与边界

| 条件 | 状态 | 输出策略 |
| --- | --- | --- |
| 维数为 0 或元素数组长度错误 | `invalid_dimensions` | 无输出 |
| `n_bar<1` 或安全策略下 `n_bar>N` | `invalid_n_bar` | 无输出 |
| 活跃轴副瓣比越界/非正 | `invalid_sidelobe_ratio` | 无输出 |
| 位数不在 `0..30` | `invalid_quantization_bits` | 无输出 |
| 最大原始权重非有限或不大于 0 | `non_positive_normalizer` | 无输出 |
| 任一输出非有限 | `non_finite_output` | 无输出 |

兼容测试若必须复刻未校验的 `n_bar>N`，应使用单独的 `source_compatibility` 策略开关；生产接口默认拒绝。

## 7. AFSIM 到中性接口映射

| AFSIM 状态/API | 中性字段 | 转换 | 源码证据 |
| --- | --- | --- | --- |
| `mNX/mNY` | 两轴 `element_count` | 正整数转 `size_t` | `WsfESA_AntennaPattern.cpp:317-319` |
| `mTaylorData.mSidelobeLevelX/Y` | `sidelobe_power_ratio_*` | 直接复制线性比 | `.cpp:324,358,943-951` |
| `mN_BarX/Y` | `n_bar_*` | 直接复制 | `.cpp:322,356,953-960` |
| `mAmpNumBits` | `amplitude_quantization_bits` | 直接复制 | `.cpp:416` |
| `Element::mWeight` | `initial_element_weights` | 行优先复制 | `.hpp:49-60` |
| 两阶段写入 | 三类输出向量 | 保持先二维、后轴量化 | `.cpp:418-435` |

## 8. 依赖替换

| AFSIM 依赖 | 中性方案 | 风险 |
| --- | --- | --- |
| `UtMath::LinearToDB` | `10*log10(S)` | 必须保持功率比语义 |
| `UtMath::cPI` | `std::numbers::pi_v<double>` | 无 |
| 成员向量 | `std::vector<double>` | 行主序需固定 |
| `ComputeQuantizationError` | 显式向零量化函数 | 不得替换为 round/floor |

## 9. 最小调用示例

```cpp
const EsaTaylorWeightsInput input{
    .x = {.element_count = 5, .sidelobe_power_ratio = 1000.0, .n_bar = 3},
    .y = {.element_count = 1, .sidelobe_power_ratio = 1.0, .n_bar = 1},
    .amplitude_quantization_bits = 0,
    .initial_element_weights = std::vector<double>(5, 1.0)
};

const auto result = compute_esa_taylor_distribution_weights(input);
// result.value.normalized_x[0] == 0.3404043556738716（容差内）
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差 |
| --- | --- | --- | --- |
| 正常 | 第 9 节 | X 权重卡片第 8 节的 5 项向量 | `1e-12` |
| 3 bit | 正常例改 bits=3 | `[0.25,0.75,1,0.75,0.25]` | 精确 |
| 二维顺序 | X/Y 均为正常例、bits=3 | 角阵元兼容权重 0，不等于 0.0625 | 精确 |
| 量化符号 | `±0.73, bits=3, range=1` | `±0.625` | 精确 |
| 无 Taylor 展开 | `n_bar=1` | 轴向均匀权重 | 精确 |
| 门禁 | S=0、NaN、N=0、bits=31 | 对应错误状态 | 精确 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 阻塞 |
| --- | --- | --- | --- | --- |
| ESA-TAYLOR-001 | `n_bar` 的正式允许上限 | 决定安全接口门禁 | 用户手册/模型参考 | yes |
| ESA-TAYLOR-002 | 轴向量后量化与二维先量化的差异是否刻意 | 下游波束宽度与阵因子使用不同离散权重 | 黄金场景或维护记录 | yes |
| ESA-TAYLOR-003 | 大于 30 位量化是否有合法用例 | 决定跨语言整数策略 | 配置样本 | no |
