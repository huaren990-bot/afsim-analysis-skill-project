# SAR 距离向地距分辨率算法接口规格

> **算法 ID**：ALG-SENSORS-SAR-GROUND-RANGE-RESOLUTION  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-sar-ground-range-resolution-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：计算 SAR 距离向地距分辨率。
- 调用时机：SAR 成像性能预测和实际成像结束。
- 包含/不包含：包含旧角分辨率、脉宽/带宽和擦地角投影；不计算方位分辨率。
- 可重入/线程安全：纯函数，无共享状态。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `requested_resolution_m` | `double` | m | image | finite, `>=0` | config |
| `legacy_angular_resolution_rad` | `double` | rad | sensor | finite, `>=0` | config |
| `slant_range_m` | `double` | m | LOS | finite, `>=0` | current |
| `pulse_width_s` | `double` | s | - | finite | current |
| `receiver_bandwidth_hz` | `double` | Hz | - | finite | current |
| `pulse_compression_ratio` | `double` | 1 | - | finite | current |
| `grazing_angle_rad` | `double` | rad | local tangent | finite | current |

## 3. 中性数据类型

```cpp
struct SarGroundRangeResolutionInput
{
    double requested_resolution_m{};
    double legacy_angular_resolution_rad{};
    double slant_range_m{};
    double pulse_width_s{};
    double receiver_bandwidth_hz{};
    double pulse_compression_ratio{1.0};
    double grazing_angle_rad{};
};

enum class SarGroundRangeResolutionStatus
{
    ok,
    legacy_angular_resolution,
    bandwidth_pulse_width,
    fallback_resolution,
    invalid_input,
    non_finite_output
};

struct SarGroundRangeResolutionOutput
{
    double pulse_width_used_s{};
    double slant_resolution_m{};
    double ground_resolution_m{};
    SarGroundRangeResolutionStatus status{SarGroundRangeResolutionStatus::ok};
};
```

## 4. 核心接口

```cpp
SarGroundRangeResolutionOutput
compute_sar_ground_range_resolution(const SarGroundRangeResolutionInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_sar_ground_range_resolution` | 输入有限 | 返回有限分辨率或错误状态 | 无 | $O(1)$ |

## 5. 状态生命周期

算法无状态。调用者负责把输出写入当前/达成地距分辨率字段。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `legacy_angular_resolution_rad > 0` | 入口 | 使用旧路径 | 标记旧配置 |
| 脉宽不可用但带宽有效 | 预处理 | 使用 `1/bandwidth` | 确认带宽单位 |
| 脉宽和带宽都不可用 | 预处理 | 使用 requested fallback | 判断是否可接受 |
| 非有限输入 | 入口 | `invalid_input` | 修正配置 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `mResolution` | `requested_resolution_m` | 直接复制 | none | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2237` |
| `mAngularResolution` | `legacy_angular_resolution_rad` | 直接复制 | 弃用警告外置 | `WsfSAR_Sensor.cpp:2238-2242` |
| `mXmtrPtr->GetPulseWidth()` | `pulse_width_s` | 直接复制 | none | `WsfSAR_Sensor.cpp:2245-2249` |
| `mRcvrPtr->GetBandwidth()` | `receiver_bandwidth_hz` | 直接复制 | none | `WsfSAR_Sensor.cpp:2250-2252` |
| `aGeometry.mGrazingAngle` | `grazing_angle_rad` | 直接复制 | none | `WsfSAR_Sensor.cpp:2259` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| 发射机/接收机对象 | 参数来源 | 移除 | 显式标量 | 单位 |
| `Geometry` | 几何来源 | 替换 | 显式字段 | 角定义 |

## 9. 最小调用示例

```cpp
SarGroundRangeResolutionInput input{};
input.pulse_width_s = 1.0e-6;
input.pulse_compression_ratio = 10.0;
input.grazing_angle_rad = std::numbers::pi / 6.0;

// 中文：期望 ground_resolution_m 约为 17.308525632731957。
auto output = compute_sar_ground_range_resolution(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节样例 | `17.308525632731957` | `1e-12` | 超差 |
| 旧路径 | `legacy=0.001,R=12000,grazing=45deg` | `16.97056274847714` | `1e-12` | 超差 |
| fallback | 无脉宽无带宽 | 使用 requested 分辨率投影 | 精确 | 状态错误 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| SAR-GRR-001 | fallback 的 `mResolution` 是否应视为距离向目标值 | API 语义 | 场景配置说明 | no |
