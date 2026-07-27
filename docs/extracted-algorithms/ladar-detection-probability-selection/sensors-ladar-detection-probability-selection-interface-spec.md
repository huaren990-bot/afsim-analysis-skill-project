# LADAR 探测概率选择与噪声功率换算接口规格

> **算法 ID**：ALG-SENSORS-LADAR-DETECTION-PROBABILITY-SELECTION  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-ladar-detection-probability-selection-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：从光子计数输出 S/N、噪声功率和选定的探测概率。
- 调用时机：接收机已生成一次脉冲的 `DetectionData` 后。
- 包含/不包含：包含查表优先于 Gaussian；不含光子计数、探测状态和查表内部插值。
- 可重入/线程安全：纯计算，查表回调的线程安全由提供者负责。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `signal_count/noise_count` | `double` | 光子计数 | - | 噪声 `>0` | current |
| `wavelength_m` | `double` | m | LOS 光谱 | `>0` | current |
| `pulse_width_s` | `double` | s | - | `>0` | current |
| `threshold_snr` | `double` | 1 | - | finite | config |
| `noise_power_w` | `double` | W | - | `>=0` | output |

## 3. 中性数据类型

```cpp
using PdLookup = std::function<double(double snr)>;
struct DetectionSelectionInput { double signal_count{}; double noise_count{}; double wavelength_m{}; double pulse_width_s{}; double threshold_snr{}; PdLookup lookup{}; };
enum class PdModel { lookup, gaussian };
struct DetectionSelectionOutput { double snr{}; double noise_power_w{}; double probability{}; PdModel model{}; };
```

## 4. 核心接口

```cpp
DetectionSelectionOutput select_detection_probability(const DetectionSelectionInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `select_detection_probability` | 计数、波长、脉宽有效 | 输出三值和所用模型 | 无 | $O(1)$，加查表代价 |

## 5. 状态生命周期

无持久状态。AFSIM 的结果对象字段由调用者接收输出后写入；查表所有权在调用者。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 噪声、波长或脉宽非正 | 入口 | `invalid_argument` | 校正输入 |
| `lookup` 存在 | 选择处 | 仅调用 lookup | 确保输出范围 |
| lookup 返回非 [0,1] | 出口 | `numeric_error` | 修正查表 |

## 7. AFSIM 到中性接口映射

| AFSIM 项 | 中性项 | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `dd.mSignalCount/mNoiseCount` | 两计数字段 | 直接复制 | DetectionData 其他字段 | `WsfLADAR_Sensor.cpp:601-627` |
| `aXmtr.GetWavelength/GetPulseWidth` | 波长/脉宽 | 直接复制 | 发射机对象 | 同上 |
| `mDetectionProbabilityPtr` | `PdLookup` | 查表回调 | 插值策略外置 | 同上 |
| `aResult` 三字段 | 输出 | 调用者写回 | 结果类状态 | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `UtMath` 常量 | $h,c$ | 替换 | SI 常量 | 低 |
| AFSIM 查表 | Pd 查表 | 替换 | 回调/验证表 | 范围外语义 |
| Gaussian Pd | 回退 | 保留 | 相邻接口 | 一致性 |

## 9. 最小调用示例

```cpp
DetectionSelectionInput in{20.0, 10.0, 1e-6, 1e-8, 1.0, {}};
auto out = select_detection_probability(in);
// 中文：out.snr 为 2，out.noise_power_w 约 1.986445857148929e-10，使用 gaussian。
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节 | SNR=2, $P_N=1.986445857148929e-10$, Pd=.8413513380564247 | `1e-12` | 超差 |
| 边界 | lookup(2)=.7 | `.7`, model=lookup | 精确 | 错用 Gaussian |
| 退化 | noise=0 | `invalid_argument` | 不除零 | 未报错 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| LADAR-PD-001 | AFSIM `Lookup` 的插值与夹取语义 | 表模型兼容 | 查表类源码 | yes |
