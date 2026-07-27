# SAR 地杂波噪声比算法接口规格

> **算法 ID**：ALG-SENSORS-SAR-CLUTTER-TO-NOISE-RATIO  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-sar-clutter-to-noise-ratio-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：计算 ground patch RCS、接收功率后处理链和最终线性 CNR。
- 调用时机：SAR 性能预测、spot SAR 实际成像结束。
- 包含/不包含：包含源码默认 backscatter 和脉冲积分；不实现 AFSIM 双程 RF 传播。
- 可重入/线程安全：纯标量层可重入；RF oracle 由调用者保证线程安全。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `frequency_hz` | `double` | Hz | - | finite, `>0` | current |
| `scan_angle_rad` | `double` | rad | antenna/LOS | finite | current |
| `grazing_angle_rad` | `double` | rad | local tangent | finite | current |
| `slant_range_m` | `double` | m | PCS x to WCS | finite, `>=0` | current |
| `resolution_m` | `double` | m | image cell | finite, `>0` | current |
| `prf_hz` | `double` | Hz | - | finite, `>0` | current |
| `dwell_time_s` | `double` | s | - | finite, `>=0` | current |
| `received_two_way_power_w` | `double` | W | RF oracle output | finite, `>=0` | current |
| `noise_power_w` | `double` | W | receiver | finite, `>0` | current |

## 3. 中性数据类型

```cpp
struct SarCnrInput
{
    double frequency_hz{};
    double scan_angle_rad{};
    double grazing_angle_rad{};
    double slant_range_m{};
    double resolution_m{};
    double prf_hz{};
    double dwell_time_s{};
    double configured_backscatter{};
    double pulse_compression_ratio{1.0};
    double integration_gain{1.0};
    double adjustment_factor{1.0};
    double received_two_way_power_w{};
    double noise_power_w{};
};

enum class SarCnrStatus
{
    ok,
    antenna_back_face,
    used_default_backscatter,
    invalid_input,
    non_finite_output
};

struct SarCnrOutput
{
    double wavelength_m{};
    double backscatter_linear{};
    double ground_patch_rcs_m2{};
    int pulses_integrated{};
    double adjusted_received_power_w{};
    double cnr_linear{};
    SarCnrStatus status{SarCnrStatus::ok};
};
```

## 4. 核心接口

```cpp
SarCnrOutput compute_sar_cnr_from_received_power(const SarCnrInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_sar_cnr_from_received_power` | 输入有限；RF 功率已由适配层算出 | 输出 CNR 和中间 RCS/脉冲数 | 无 | $O(1)$ |

## 5. 状态生命周期

算法无持久状态。AFSIM 的 `mTempPlatform`、`WsfSensorResult` 和 beam positions 属于适配层；中性接口只接收 RF oracle 的输出功率。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `scan_angle_rad >= pi/2` | 入口 | `cnr_linear=1e-37` | 标记不可成像 |
| `configured_backscatter <= 0` | backscatter 选择 | 使用源码默认经验式 | 记录状态 |
| `dwell_time_s * prf_hz < 1` | 脉冲积分 | `pulses_integrated=1` | 判断是否物理可接受 |
| `noise_power_w <= 0` | 入口 | `invalid_input` | 修正接收机配置 |
| 非有限输出 | 出口 | `non_finite_output` | 失败处理 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `mXmtrPtr->GetFrequency()` | `frequency_hz` | 直接复制 | none | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2073` |
| `mBackscatterCoefficient` | `configured_backscatter` | 直接复制 | none | `WsfSAR_Sensor.cpp:2077-2083` |
| `aResolution` | `resolution_m` | 直接复制 | cell 形状简化 | `WsfSAR_Sensor.cpp:2085` |
| `ComputeRF_TwoWayPower(rcs)` | `received_two_way_power_w` | RF oracle | AFSIM 天线细节外置 | `WsfSAR_Sensor.cpp:2112-2113` |
| `GetNoisePower()` | `noise_power_w` | 直接复制 | none | `WsfSAR_Sensor.cpp:2128` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfSensorResult` | RF 双程功率 | 替换 | 外部 oracle | 最大兼容风险 |
| `WsfPlatform` 临时目标 | ground patch 几何 | 替换 | 显式 RF 几何输入 | 姿态差异 |
| `UtMath` | dB、光速 | 替换 | 标准数学 | 低 |

## 9. 最小调用示例

```cpp
SarCnrInput input{};
input.frequency_hz = 10.0e9;
input.scan_angle_rad = 0.0;
input.grazing_angle_rad = std::numbers::pi / 6.0;
input.resolution_m = 3.0;
input.prf_hz = 900.0;
input.dwell_time_s = 2.3;
input.configured_backscatter = 0.1;
input.pulse_compression_ratio = 10.0;
input.integration_gain = 2.0;
input.adjustment_factor = 0.5;
input.received_two_way_power_w = 1.0e-9;
input.noise_power_w = 1.0e-12;

// 中文：期望 cnr_linear 约为 20700000。
auto output = compute_sar_cnr_from_received_power(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节样例 | `20700000.000000004` | 相对 `1e-12` | 超差 |
| 默认 backscatter | 10 GHz 且配置 `<=0` | `0.031655620273391985` | `1e-15` | 超差 |
| 背面 | `scan=pi/2` | `1e-37` | 精确 | 不等 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| SAR-CNR-001 | 默认 backscatter 经验式的适用范围 | 跨地表/频段可信度 | Skolnik 引文或 AFSIM 文档 | yes |
| SAR-CNR-002 | RF oracle 是否必须逐位兼容 `WsfSensorResult` | clean-room 验证难度 | 黄金场景 | yes |
