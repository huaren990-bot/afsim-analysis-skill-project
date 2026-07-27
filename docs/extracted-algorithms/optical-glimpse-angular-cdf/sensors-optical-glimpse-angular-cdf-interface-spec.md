# 光学掠视角分离 Monte Carlo CDF 接口规格

> **算法 ID**：ALG-SENSORS-OPTICAL-GLIMPSE-ANGULAR-CDF  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-optical-glimpse-angular-cdf-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 生成两个独立球面视场点之间角分离的 1° 分箱 CDF。
- 不计算对比度阈值或最终探测概率。
- 支持 `afsim_2_9_compat` 与 `portable_double` 两种累计精度策略。
- RNG 状态必须由接口显式规定；不依赖全局仿真随机状态。

## 2. 单位与坐标系

| 量 | 类型 | 单位/坐标系 | 有效范围 |
| --- | --- | --- | --- |
| `azimuth_fov_deg` | `double` | deg，局部视场方位 | `[0,360]` |
| `minimum_elevation_deg` | `double` | deg，局部俯仰 | `[-90,90]` |
| `maximum_elevation_deg` | `double` | deg，局部俯仰 | `[minimum,90]` |
| `sample_count` | `uint32_t` | 次 | `[1,INT_MAX]` |
| `seed` | `uint32_t` | — | 兼容默认 1 |
| `cdf[j]` | `double` | 概率 | $j$ 对应 $j°$ 边界，期望 `[0,1]` 附近 |

视场只定义局部角度矩形，不依赖 WCS/NED/ECI。

## 3. 中性数据类型

```cpp
enum class AngularCdfPrecision
{
    afsim_2_9_compat,  // 中文：每箱除以 float(sample_count) 后累加到 double
    portable_double   // 中文：全部使用 double，并可在末点归一到 1
};

struct OpticalAngularCdfInput
{
    double azimuth_fov_deg{};
    double minimum_elevation_deg{};
    double maximum_elevation_deg{};
    std::uint32_t sample_count{1000};
    std::uint32_t seed{1};
    AngularCdfPrecision precision{AngularCdfPrecision::afsim_2_9_compat};
};

enum class OpticalAngularCdfError
{
    none,
    non_finite_input,
    invalid_angle_range,
    invalid_sample_count,
    dot_product_domain_error,
    counter_overflow,
    non_finite_output
};

struct OpticalAngularCdfOutput
{
    std::array<std::uint32_t, 180> histogram{};
    std::array<double, 181> cdf{};
};

template<class T>
struct Result
{
    T value{};
    OpticalAngularCdfError error{OpticalAngularCdfError::none};
};
```

## 4. 核心接口

```cpp
// 中文：用明确的 mt19937 兼容随机策略生成角分离 CDF。
Result<OpticalAngularCdfOutput>
build_optical_glimpse_angular_cdf(const OpticalAngularCdfInput& input);

// 中文：用于跨语言逐位可复验；调用者提供每次抽样所需的 U[0,1) 值。
Result<OpticalAngularCdfOutput>
build_optical_glimpse_angular_cdf_from_u01(
    const OpticalAngularCdfInput& input,
    Uniform01Source& random_source);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `build_*` | 角范围合法、样本数合法 | 直方图和为 $N$，CDF 单调 | 仅局部 RNG | 时间 $O(N)$，空间 $O(1)$ |
| `build_*_from_u01` | 每样本可取得 4 个 $U[0,1)$ 值 | 同上 | 消耗 `4N` 个随机值 | 时间 $O(N)$ |

## 5. 状态生命周期

核心函数无持久状态。AFSIM 适配层在模式初始化时保存 `cdf`；输入视场变化后必须重建。固定种子意味着相同输入重建时应得到相同分布。

## 6. 错误与边界

| 条件 | 行为 |
| --- | --- |
| 角度非有限或超范围 | `non_finite_input` / `invalid_angle_range` |
| `sample_count==0` 或超过 `INT_MAX` | `invalid_sample_count` |
| 点积在 `[-1-\epsilon,1+\epsilon]` 外 | `dot_product_domain_error` |
| 点积仅因舍入轻微越界 | 安全模式钳制到 `[-1,1]` 并记录诊断；兼容模式仅保护上界 |
| 计数器将溢出 | `counter_overflow` |
| 输出出现 NaN/Inf | `non_finite_output` |

## 7. AFSIM 到中性接口映射

| AFSIM 状态/API | 中性字段/API | 转换 | 源码证据 |
| --- | --- | --- | --- |
| `mAzimuthFOV` | `azimuth_fov_deg` | 源码内部已存 deg | `WsfOpticalSensor.cpp:632` |
| `mMinElevation/mMaxElevation` | 两个 elevation 字段 | 源码内部已存 deg | `WsfOpticalSensor.cpp:634-636` |
| `mNumIterations` | `sample_count` | 正整数 | `WsfOpticalSensor.cpp:642` |
| `ut::Random()` | `seed=1` + `mt19937` | 构造时固定种子 | `UtRandom.hpp:169-172` |
| `mProbabilityDistribution` | `output.cdf` | 181 节点复制 | `WsfOpticalSensor.cpp:691-696` |

## 8. 依赖替换

| 依赖 | 保留/替换 | 中性方案 | 风险 |
| --- | --- | --- | --- |
| `ut::Random` | 替换 | `mt19937` 兼容器或 U01 注入 | 标准库实数映射差异 |
| `std::uniform_real_distribution` | 兼容时保留同实现 | 跨语言时版本化 U01 映射 | 逐位不一致 |
| 动态 `vector` | 替换 | 固定 `array<181>` | 无 |
| 数学函数 | 保留 | 标准等价实现 | 末位舍入 |

## 9. 最小调用示例

```cpp
const OpticalAngularCdfInput input{
    .azimuth_fov_deg = 5.0,
    .minimum_elevation_deg = 0.0,
    .maximum_elevation_deg = 5.0,
    .sample_count = 1000,
    .seed = 1
};

// 中文：结果应有 181 个单调节点，直方图计数总和为 1000。
const auto result = build_optical_glimpse_angular_cdf(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle/不变量 | 失败判据 |
| --- | --- | --- | --- |
| 正常 | 默认配置 | `sum(histogram)=1000`、`cdf[0]=0`、单调、`cdf[180]≈1` | 任一不变量失败 |
| 重复性 | 同一标准库、同一输入调用两次 | 直方图和 CDF 逐位一致 | 任一节点不同 |
| 确定性退化 | 0° 方位，俯仰 0°..0°，$N=7$ | `hist[0]=7`，其余 0；`cdf[0]=0`，其余 1 | 任一元素不同 |
| 输入门禁 | 非法角范围、0 次、NaN | 对应错误码 | 进入抽样循环 |
| 注入流 | 固定 4N 个 U01 测试向量 | 与独立实现逐项一致 | 直方图或 CDF 不同 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 阻塞 |
| --- | --- | --- | --- | --- |
| OPT-CDF-001 | 目标系统是否要求与当前 C++ 标准库逐位兼容 | RNG 接口选择 | 部署编译器/标准库基线 | yes |
| OPT-CDF-002 | 是否允许把累计从 float 改为 double | 末位统计差异 | 黄金探测概率容差 | no |
| OPT-CDF-003 | 下游是否可能请求 180° 插值 | 数组越界风险 | 场景配置范围和回归数据 | yes，阻塞直接复用插值器 |
