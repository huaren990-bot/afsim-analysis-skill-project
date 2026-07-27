# SAR 非模糊距离 PRF 选择算法接口规格

> **算法 ID**：ALG-SENSORS-SAR-PRF-UNAMBIGUOUS-RANGE  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-sar-prf-unambiguous-range-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：按斜距计算非模糊距离 PRF。
- 调用时机：SAR 自动 PRF 性能预测。
- 包含/不包含：包含 0.9 普通裕度和 constraint plotting 分支；不计算 Doppler 最小 PRF。
- 可重入/线程安全：纯函数。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `slant_range_m` | `double` | m | LOS | finite, `>=0` | current |
| `constraint_plotting` | `bool` | - | - | true/false | current |

## 3. 中性数据类型

```cpp
struct SarPrfInput
{
    double slant_range_m{};
    bool constraint_plotting{};
};

enum class SarPrfStatus
{
    ok,
    constraint_boundary,
    invalid_input,
    non_finite_output
};

struct SarPrfOutput
{
    double prf_hz{};
    SarPrfStatus status{SarPrfStatus::ok};
};
```

## 4. 核心接口

```cpp
SarPrfOutput compute_sar_prf_unambiguous_range(const SarPrfInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_sar_prf_unambiguous_range` | `slant_range_m>=0` | 输出有限正 PRF | 无 | $O(1)$ |

## 5. 状态生命周期

算法无状态。调用者可把 `prf_hz` 写入发射机脉冲重复频率。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `constraint_plotting=true` | 入口 | 不乘 0.9，状态 `constraint_boundary` | 仅用于约束图 |
| `slant_range_m<0` | 入口 | `invalid_input` | 修正几何 |
| 输出非有限 | 出口 | `non_finite_output` | 失败处理 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `aGeometry.mSlantRange` | `slant_range_m` | 直接复制 | none | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2172-2178` |
| `mSAR_ConstraintPlotting` | `constraint_plotting` | 直接复制 | none | `WsfSAR_Sensor.cpp:2168-2173` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `Geometry` | 斜距来源 | 替换 | 显式字段 | 低 |
| `WsfSAR_Sensor` | constraint flag | 替换 | 显式布尔 | 低 |

## 9. 最小调用示例

```cpp
SarPrfInput input{};
input.slant_range_m = 10000.0;
input.constraint_plotting = false;

// 中文：期望 prf_hz 约为 13489.986110694465。
auto output = compute_sar_prf_unambiguous_range(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | `R=10000`, false | `13489.986110694465` | `1e-9` | 超差 |
| constraint | `R=10000`, true | `14988.873456327183` | `1e-9` | 超差 |
| invalid | `R<0` | `invalid_input` | 状态 | 未拒绝 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| SAR-PRF-001 | 分母 `+1 m` 的建模意图 | 极短斜距差异 | 需求或历史提交 | no |
