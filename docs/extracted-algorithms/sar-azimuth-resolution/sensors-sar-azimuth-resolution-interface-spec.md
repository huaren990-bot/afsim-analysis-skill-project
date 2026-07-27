# SAR 驻留时间反算方位分辨率算法接口规格

> **算法 ID**：ALG-SENSORS-SAR-AZIMUTH-RESOLUTION  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-sar-azimuth-resolution-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：由 SAR 几何、频率、Doppler 展宽因子和驻留时间计算方位分辨率。
- 调用时机：成像开始预测、成像结束实际驻留时间回算、性能评估。
- 包含/不包含：包含源码哨兵与旧角分辨率路径；不计算几何、驻留时间、CNR 或距离向分辨率。
- 可重入/线程安全：无共享状态，可重入。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `frequency_hz` | `double` | Hz | - | finite, `>0` | current |
| `doppler_broadening_factor` | `double` | 1 | - | finite, `>=1` | current |
| `slant_range_m` | `double` | m | WCS 派生 | finite, `>=0` | current |
| `velocity_magnitude_mps` | `double` | m/s | NED 矢量模 | finite, `>=0` | current |
| `dwell_time_s` | `double` | s | - | finite, `>0` | current |
| `squint_angle_rad` | `double` | rad | NED 水平投影 | finite | current |
| `grazing_angle_rad` | `double` | rad | 地面局部切平面 | finite | current |
| `scan_angle_rad` | `double` | rad | 天线坐标相关 | finite | current |
| `legacy_angular_resolution_rad` | `double` | rad | - | finite, `>=0` | config |

内部统一单位为 SI；角度均为 rad。

## 3. 中性数据类型

```cpp
struct SarAzimuthResolutionInput
{
    double frequency_hz{};
    double doppler_broadening_factor{1.0};
    double slant_range_m{};
    double velocity_magnitude_mps{};
    double dwell_time_s{};
    double squint_angle_rad{};
    double grazing_angle_rad{};
    double scan_angle_rad{};
    double legacy_angular_resolution_rad{};
};

enum class SarAzimuthResolutionStatus
{
    ok,
    legacy_angular_resolution,
    antenna_back_face,
    degenerate_geometry,
    invalid_input,
    non_finite_output
};

struct SarAzimuthResolutionOutput
{
    double wavelength_m{};
    double denominator_m2{};
    double resolution_m{};
    SarAzimuthResolutionStatus status{SarAzimuthResolutionStatus::ok};
};
```

## 4. 核心接口

```cpp
SarAzimuthResolutionOutput
compute_sar_azimuth_resolution(const SarAzimuthResolutionInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_sar_azimuth_resolution` | 输入有限并满足第 2 节 | 成功时输出有限分辨率或源码兼容哨兵 | 无 | $O(1)$ |

## 5. 状态生命周期

本算法无内部持久状态。调用者可把 `resolution_m` 写入模式当前分辨率或传感器达成分辨率；接口不负责缓存。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `legacy_angular_resolution_rad > 0` | 入口 | 返回 `legacy * slant_range` | 标记旧配置 |
| `scan_angle_rad > pi/2` | 入口 | 返回 1000 m，状态 `antenna_back_face` | 拒绝或降级成像 |
| 分母 `<=0` | 公式后 | 返回 1000 m，状态 `degenerate_geometry` | 不当作真实分辨率 |
| 非法频率/驻留/NaN | 入口 | `invalid_input` | 修正输入 |
| 输出非有限 | 出口 | `non_finite_output` | 失败处理 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `mXmtrPtr->GetFrequency()` | `frequency_hz` | 直接复制 | none | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2222` |
| `mKa` | `doppler_broadening_factor` | 直接复制 | none | `WsfSAR_Sensor.cpp:2223` |
| `aGeometry` | 几何标量 | 按字段复制 | 生成过程外置 | `WsfSAR_Sensor.hpp:118-147` |
| `aDwellTime` | `dwell_time_s` | 直接复制 | none | `WsfSAR_Sensor.cpp:2192` |
| `mAngularResolution` | `legacy_angular_resolution_rad` | 直接复制 | 弃用警告外置 | `WsfSAR_Sensor.cpp:2195-2199` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfEM_Xmtr` | 提供频率 | 移除 | 标量 Hz | 单位错误 |
| `Geometry` | 几何聚合 | 替换 | 显式字段 | 角定义漂移 |
| `UtMath` | 光速和 $\pi$ | 替换 | `std::numbers` + 精确光速 | 低 |

## 9. 最小调用示例

```cpp
SarAzimuthResolutionInput input{};
input.frequency_hz = 10.0e9;
input.doppler_broadening_factor = 1.2;
input.slant_range_m = 10000.0;
input.velocity_magnitude_mps = 200.0;
input.dwell_time_s = 5.0;
input.squint_angle_rad = std::numbers::pi / 6.0;
input.grazing_angle_rad = std::numbers::pi / 4.0;
input.scan_angle_rad = 0.0;

// 中文：期望 resolution_m 约为 0.5087646720009198。
auto output = compute_sar_azimuth_resolution(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节样例 | `0.5087646720009198` | `1e-12` | 超差 |
| 旧路径 | `legacy=0.001`、`R=12000` | 12 m | 精确 | 不等 |
| 退化 | 斜视角 0 | 1000 m + `degenerate_geometry` | 精确 | 状态错误 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| SAR-AZ-001 | 与驻留时间算法对 `scan==pi/2` 的门禁差异是否有意 | 边界兼容 | 需求或回归场景 | no |
