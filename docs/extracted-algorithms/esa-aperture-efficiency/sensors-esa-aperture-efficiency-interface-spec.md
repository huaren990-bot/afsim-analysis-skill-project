# ESA 幅度权重孔径效率算法接口规格

> **算法 ID**：ALG-SENSORS-ESA-APERTURE-EFFICIENCY  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-esa-aperture-efficiency-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 以纯函数计算 X、Y 和二维阵元的幅度权重孔径效率。
- 显式区分安全错误状态与 AFSIM 全零权重产生 NaN 的兼容行为。
- 不生成权重、不选择失效元素、不计算增益或阵因子。
- 无共享状态，可重入、线程安全。

## 2. 单位与有效范围

| 字段 | 类型 | 单位 | 安全接口约束 |
| --- | --- | --- | --- |
| `element_count_x/y` | `size_t` | 1 | `>=1` |
| `x_weights/y_weights` | `vector<double>` | 幅度比 | 长度分别等于 Nx/Ny，值有限 |
| `element_weights` | `vector<double>` | 幅度比 | 行优先，长度等于 Nx*Ny，值有限 |

正常非零向量的效率为无量纲数，数学范围为 `(0,1]`。

## 3. 中性数据类型

```cpp
enum class ApertureEfficiencyStatus
{
    ok,
    invalid_dimensions,
    non_finite_input,
    all_zero_x_weights,
    all_zero_y_weights,
    all_zero_element_weights,
    non_finite_output
};

struct EsaApertureEfficiencyInput
{
    std::size_t element_count_x{};
    std::size_t element_count_y{};
    std::vector<double> x_weights;
    std::vector<double> y_weights;
    std::vector<double> element_weights;
};

struct EsaApertureEfficiencyOutput
{
    double x_efficiency{};
    double y_efficiency{};
    double total_efficiency{};
};

template<class T>
struct Result
{
    T value{};
    ApertureEfficiencyStatus status{ApertureEfficiencyStatus::ok};
};
```

## 4. 核心接口

```cpp
Result<EsaApertureEfficiencyOutput>
compute_esa_aperture_efficiency(const EsaApertureEfficiencyInput& input);
```

| 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- |
| 数量、长度和有限性门禁通过 | `ok` 时三项均有限且位于 `(0,1]` | 无 | $O(N_xN_y)$ 时间，$O(1)$ 额外空间 |

实现应使用缩放和或稳定归约，避免直接平方极端幅度导致溢出；对正常量级必须与源码公式等价。

## 5. 状态生命周期

算法无状态。AFSIM 适配层在分布加权和随机失效完成后调用，将三项输出写入对象。若权重或失效掩码改变，三项必须同步重算；不能只更新总效率。

## 6. 错误与边界

| 条件 | 状态 | AFSIM 2.9 行为 | 安全输出 |
| --- | --- | --- | --- |
| 数量为 0 或长度不匹配 | `invalid_dimensions` | 除零或越界 | 无输出 |
| 任一输入非有限 | `non_finite_input` | 传播非有限值 | 无输出 |
| X 权重全零 | `all_zero_x_weights` | $\eta_x$ 为 NaN | 无输出 |
| Y 权重全零 | `all_zero_y_weights` | $\eta_y$ 为 NaN | 无输出 |
| 二维权重全零 | `all_zero_element_weights` | 总效率为 NaN | 无输出 |
| 计算后非有限 | `non_finite_output` | 传播到增益链 | 无输出 |

若兼容层需要逐位复刻，应在错误结果旁单独提供 `source_compatible_nan` 标志，不应把 NaN 包装成成功。

## 7. AFSIM 到中性接口映射

| AFSIM 状态/API | 中性字段 | 转换 | 源码证据 |
| --- | --- | --- | --- |
| `mNX/mNY` | 两个 count | 正整数转 `size_t` | `WsfESA_AntennaPattern.cpp:611-613` |
| `mWeightVecX/Y` | 两个轴向量 | 直接复制 | `.cpp:618-633` |
| `mElements[].mWeight` | `element_weights` | 行优先复制 | `.cpp:638-644` |
| `mApertureEffX/Y` | 轴输出 | 写回适配层 | `.cpp:623,633` |
| `mApertureEff` | 总输出 | 写回并作为函数返回 | `.cpp:646-648` |

必须在 `ComputeFailedModulesWeights` 之后采集二维元素权重，但轴向量保持分布算法输出。

## 8. 依赖替换

| AFSIM 依赖 | 中性方案 | 风险 |
| --- | --- | --- |
| `ElementVec` | `std::vector<double>` | 行主序长度 |
| `sqrt(w*w)` | `std::abs(w)` | 对有限值语义等价且更稳健 |
| 成员缓存 | 返回值结构 | 适配层负责同步写回 |

## 9. 最小调用示例

```cpp
const EsaApertureEfficiencyInput input{
    .element_count_x = 2,
    .element_count_y = 1,
    .x_weights = {1.0, 0.5},
    .y_weights = {1.0},
    .element_weights = {1.0, 0.5}
};

const auto result = compute_esa_aperture_efficiency(input);
// x_efficiency == total_efficiency == 0.9，y_efficiency == 1
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差 |
| --- | --- | --- | --- |
| 均匀 | `[1,1,1,1]` | `1` | 精确 |
| 锥削 | 第 9 节 | X/total=`0.9`，Y=`1` | `1e-15` |
| 半失效 | element=`[1,0,1,0]` | total=`0.5` | 精确 |
| Taylor | 卡片 5 单元未量化向量 | `0.8579882159275146` | `1e-12` |
| 量化 Taylor | `[0.25,0.75,1,0.75,0.25]` | `0.8` | 精确 |
| 全失效 | element=`[0,0]` | `all_zero_element_weights` | 精确 |
| 门禁 | 长度不匹配、NaN、N=0 | 对应错误状态 | 精确 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 阻塞 |
| --- | --- | --- | --- | --- |
| ESA-EFF-001 | 100% 失效时最终增益应为 0 还是模式不可用 | 替换 NaN 的业务语义 | 需求/黄金场景 | yes |
| ESA-EFF-002 | 轴效率是否应纳入失效空间分布 | 波束宽度对部分失效的响应 | 模型参考与测试 | yes |
| ESA-EFF-003 | 负幅度权重是否为受支持输入 | 决定是否允许符号权重 | 配置与派生类证据 | no |
