# SAR 1 m² 目标自由空间校准算法接口规格

> **算法 ID**：ALG-SENSORS-SAR-ONE-M2-CALIBRATION  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-sar-one-m2-calibration-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：在 1 m² 目标检测距离和接收机噪声之间互算，并返回当前检测距离。
- 调用时机：SAR 模式初始化校准。
- 包含/不包含：包含自由空间双程雷达方程；不包含日志和真实地杂波。
- 可重入/线程安全：纯计算部分可重入；写回噪声由调用者决定。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `transmit_power_w` | `double` | W | - | finite, `>0` | config |
| `frequency_hz` | `double` | Hz | - | finite, `>0` | config |
| `tx_peak_gain` | `double` | 1 | boresight | finite, `>0` | config |
| `rx_peak_gain` | `double` | 1 | boresight | finite, `>0` | config |
| `tx_internal_loss` | `double` | 1 | - | finite, `>0` | config |
| `rx_internal_loss` | `double` | 1 | - | finite, `>0` | config |
| `pulse_compression_ratio` | `double` | 1 | - | finite, `>0` | config |
| `integration_gain` | `double` | 1 | - | finite, `>0` | config |
| `adjustment_factor` | `double` | 1 | - | finite, `>0` | config |
| `detection_threshold` | `double` | 1 | S/N | finite, `>0` | config |
| `noise_power_w` | `double` | W | - | finite, `>0` | state |
| `one_m2_detect_range_m` | `double` | m | free-space range | finite, `>=0` | config |

## 3. 中性数据类型

```cpp
struct SarOneM2CalibrationInput
{
    double transmit_power_w{};
    double frequency_hz{};
    double tx_peak_gain{};
    double rx_peak_gain{};
    double tx_internal_loss{1.0};
    double rx_internal_loss{1.0};
    double pulse_compression_ratio{1.0};
    double integration_gain{1.0};
    double adjustment_factor{1.0};
    double detection_threshold{};
    double noise_power_w{};
    double one_m2_detect_range_m{};
};

enum class SarOneM2CalibrationStatus
{
    ok,
    calibrated_noise_from_range,
    invalid_input,
    non_finite_output
};

struct SarOneM2CalibrationOutput
{
    double wavelength_m{};
    double calibrated_noise_power_w{};
    double detection_range_m{};
    bool should_write_noise_power{};
    SarOneM2CalibrationStatus status{SarOneM2CalibrationStatus::ok};
};
```

## 4. 核心接口

```cpp
SarOneM2CalibrationOutput calibrate_sar_one_m2(const SarOneM2CalibrationInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `calibrate_sar_one_m2` | 所有功率、增益、损耗和阈值为正 | 返回检测距离；必要时返回应写回噪声 | 无直接副作用 | $O(1)$ |

## 5. 状态生命周期

中性接口不直接修改接收机。若 `should_write_noise_power=true`，适配层把 `calibrated_noise_power_w` 写入接收机噪声功率；之后 CNR 和探测阈值使用新噪声。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `one_m2_detect_range_m > 0` | 入口 | 反算噪声并标记写回 | 执行或拒绝副作用 |
| 任一分母参数 `<=0` | 入口 | `invalid_input` | 修正配置 |
| 输出非有限 | 出口 | `non_finite_output` | 失败处理 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `xmtr.GetPower()` | `transmit_power_w` | 直接复制 | average power 日志不迁移 | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2789` |
| `xmtr.GetFrequency()` | `frequency_hz` | 直接复制 | none | `WsfSAR_Sensor.cpp:2711` |
| `GetPeakAntennaGain()` | peak gains | 直接复制 | 角度方向图外置 | `WsfSAR_Sensor.cpp:2789-2803` |
| `GetInternalLoss()` | internal losses | 直接复制 | none | `WsfSAR_Sensor.cpp:2789-2803` |
| `mOneM2DetectRange` | `one_m2_detect_range_m` | 直接复制 | none | `WsfSAR_Sensor.cpp:2782-2815` |
| `rcvr.SetNoisePower` | `should_write_noise_power` | 由适配层执行 | 直接副作用外置 | `WsfSAR_Sensor.cpp:2814-2815` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfEM_Xmtr/Rcvr` | 参数和状态 | 替换 | 显式配置 | 参数语义 |
| `ut::log` | 打印校准数据 | 移除 | 调用者日志 | 无 |

## 9. 最小调用示例

```cpp
SarOneM2CalibrationInput input{};
input.transmit_power_w = 1000.0;
input.frequency_hz = 9.993081933333333e9;
input.tx_peak_gain = 100.0;
input.rx_peak_gain = 100.0;
input.tx_internal_loss = 2.0;
input.rx_internal_loss = 2.0;
input.pulse_compression_ratio = 10.0;
input.integration_gain = 2.0;
input.adjustment_factor = 0.5;
input.detection_threshold = 13.0;
input.noise_power_w = 1.0e-12;

// 中文：等效 wavelength 为 0.03 m 时，期望 detection_range_m 约为 966.3899246148366。
auto output = calibrate_sar_one_m2(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节样例 | `966.3899246148366` | `1e-9` | 超差 |
| 反算噪声 | `one_m2_range=5000` | `1.3954990860519005e-15` W | `1e-24` | 超差 |
| invalid | `threshold<=0` | `invalid_input` | 状态 | 未拒绝 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| SAR-CAL-001 | `GetPower()` 与 `GetAveragePower()` 在校准中的区分 | 迁移参数命名 | 发射机文档 | no |
