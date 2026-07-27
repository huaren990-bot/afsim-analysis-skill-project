# SAR 方位分辨率驻留时间算法接口规格

> **算法 ID**：ALG-SENSORS-SAR-DWELL-TIME  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-sar-dwell-time-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 纯函数计算 SAR 指定方位分辨率所需驻留时间。
- 同时暴露物理/几何状态和 AFSIM 2.9 兼容返回值，避免调用者把哨兵当作有效时间。
- 不构造几何、不计算 PRF/CNR，也不自动应用任务调度层最大驻留时间。
- 无共享状态，可重入、线程安全。

## 2. 单位与坐标系

| 量 | 类型 | 单位/坐标系 | 有效范围 |
| --- | --- | --- | --- |
| `frequency_hz` | `double` | Hz | 有限且 `>0` |
| `doppler_broadening_factor` | `double` | 1 | 有限且 `>=1` |
| `slant_range_m` | `double` | m | 有限且 `>=0` |
| `velocity_magnitude_mps` | `double` | m/s，NED 三维速度模 | 有限且 `>=0` |
| `azimuth_resolution_m` | `double` | m | 有限且 `>0` |
| `squint_angle_rad` | `double` | rad，水平投影夹角 | 有限 |
| `grazing_angle_rad` | `double` | rad，LOS/目标切平面 | 有限 |
| `scan_angle_rad` | `double` | rad，天线法线/LOS | 有限 |
| `configured_maximum_dwell_s` | `double` | s | 有限且 `>0` |

## 3. 中性数据类型

```cpp
struct SarDwellTimeInput
{
    double frequency_hz{};
    double doppler_broadening_factor{1.0};
    double slant_range_m{};
    double velocity_magnitude_mps{};
    double azimuth_resolution_m{};
    double squint_angle_rad{};
    double grazing_angle_rad{};
    double scan_angle_rad{};
    double configured_maximum_dwell_s{999.0};
};

enum class SarDwellStatus
{
    ok,
    capped_at_source_limit,
    antenna_back_face,
    degenerate_geometry,
    invalid_input,
    non_finite_output
};

struct SarDwellTimeOutput
{
    double wavelength_m{};
    double denominator_m2_per_s{};
    double uncapped_dwell_s{};
    double source_compatible_dwell_s{};
    double caller_clamped_dwell_s{};
    SarDwellStatus status{SarDwellStatus::ok};
};

template<class T>
struct Result
{
    T value{};
    SarDwellStatus error{SarDwellStatus::ok};
};
```

`caller_clamped_dwell_s=min(source_compatible_dwell_s, configured_maximum_dwell_s)` 对应 `AttemptToDetect`；性能预测若需复刻源码，应使用未做这层裁剪的 `source_compatible_dwell_s`。

## 4. 核心接口

```cpp
// 中文：计算公式、源码兼容值和调度层裁剪值，不访问传感器对象。
Result<SarDwellTimeOutput>
compute_sar_resolution_dwell_time(const SarDwellTimeInput& input);
```

| 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- |
| 所有输入有限且满足第 2 节范围 | 成功时三个时间字段有限且非负 | 无 | $O(1)$ |

## 5. 状态生命周期

算法无状态。几何由调用者在同一仿真时刻生成；适配层不得缓存跨时刻的速度、角度或斜距。模式配置可缓存，但频率变化后必须重新计算。

## 6. 错误与边界

| 条件 | `status` | 源码兼容时间 | 调用者裁剪时间 |
| --- | --- | ---: | ---: |
| 合法且结果 `<1000` | `ok` | 公式值 | `min(公式值, cfg max)` |
| 合法且结果 `>=1000` | `capped_at_source_limit` | 1000 | `min(1000, cfg max)` |
| `scan>=π/2` | `antenna_back_face` | `max(cfg max+1,1000)` | `cfg max` |
| 分母 `<=0` | `degenerate_geometry` | 1000 | `min(1000,cfg max)` |
| 输入非法 | `invalid_input` | 不提供 | 不提供 |
| 中间/输出非有限 | `non_finite_output` | 不提供 | 不提供 |

安全调用者应根据 `status` 拒绝 `antenna_back_face` 和 `degenerate_geometry`，而不是调度一个哨兵时长。

## 7. AFSIM 到中性接口映射

| AFSIM 状态/API | 中性字段 | 转换 | 源码证据 |
| --- | --- | --- | --- |
| `mXmtrPtr->GetFrequency()` | `frequency_hz` | 直接复制 | `WsfSAR_Sensor.cpp:2152` |
| `mKa` | `doppler_broadening_factor` | 直接复制 | `WsfSAR_Sensor.cpp:2153` |
| `Geometry` 五个字段 | 对应 range/speed/angles | 直接复制，角为 rad | `WsfSAR_Sensor.hpp:118-147` |
| `aResolution` | `azimuth_resolution_m` | 直接复制 | `WsfSAR_Sensor.cpp:2155` |
| `mMaximumDwellTime` | 配置最大值 | 直接复制 | `WsfSAR_Sensor.cpp:2135` |
| `AttemptToDetect` 二次 `min` | `caller_clamped_dwell_s` | 外层裁剪 | `WsfSAR_Sensor.cpp:191-193` |

## 8. 依赖替换

| 依赖 | 处理 | 中性方案 | 风险 |
| --- | --- | --- | --- |
| 发射机对象 | 移除 | 显式 Hz | 单位 |
| SAR `Geometry` | 替换 | 中性标量字段 | 角定义必须一致 |
| `UtMath` | 替换 | 精确光速和标准 $\pi$ | 无实质风险 |
| 模式成员 | 移除 | 显式配置 | 生命周期由调用者管理 |

## 9. 最小调用示例

```cpp
const SarDwellTimeInput input{
    .frequency_hz = 10.0e9,
    .doppler_broadening_factor = 1.0,
    .slant_range_m = 10000.0,
    .velocity_magnitude_mps = 200.0,
    .azimuth_resolution_m = 1.0,
    .squint_angle_rad = std::numbers::pi / 6.0,
    .grazing_angle_rad = std::numbers::pi / 4.0,
    .scan_angle_rad = 0.0,
    .configured_maximum_dwell_s = 999.0
};

// 中文：源码兼容驻留时间期望约 2.119852800003833 s。
const auto result = compute_sar_resolution_dwell_time(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差 |
| --- | --- | --- | --- |
| 正常 | 第 9 节样例 | `2.119852800003833` s | 绝对误差 `1e-12` |
| 退化 | 斜视角 0 | status=`degenerate_geometry`，兼容值 1000 | 精确 |
| 硬上限 | 极小正斜视角 | status=`capped_at_source_limit`，兼容值 1000 | 精确 |
| 背面 | 扫描 `π/2`、cfg max=1200 | status=`antenna_back_face`，兼容值 1201，外层值 1200 | 精确 |
| 输入门禁 | 0 Hz、负范围、0 分辨率、NaN | `invalid_input` | 不计算 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 阻塞 |
| --- | --- | --- | --- | --- |
| SAR-DWELL-001 | `PredictPerformance` 是否应和探测路径一样应用配置最大值 | 两条调用链结果不一致 | 需求/黄金场景 | yes |
| SAR-DWELL-002 | 垂直速度是否应计入名为 ground speed 的量 | 高爬升/俯冲结果 | 模型参考 2 或测试 | yes |
| SAR-DWELL-003 | 反向扫描哨兵是否为公共契约 | API 兼容策略 | 调用者检查逻辑 | no |
