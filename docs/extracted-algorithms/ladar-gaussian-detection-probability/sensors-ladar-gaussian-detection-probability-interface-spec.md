# LADAR Gaussian 探测概率近似接口规格

> **算法 ID**：ALG-SENSORS-LADAR-GAUSSIAN-DETECTION-PROBABILITY  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-ladar-gaussian-detection-probability-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：实现源码的分段正态 CDF 概率近似。
- 调用时机：没有 Pd-S/N 查表的简单探测器。
- 不包含：查表模型、计数生成、探测状态门限。
- 可重入/线程安全：纯函数。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `signal_count/noise_count` | `double` | 光子计数 | - | finite | current |
| `threshold_snr` | `double` | 1 | - | finite | config |
| `probability` | `double` | 1 | - | [0,1] | output |

## 3. 中性数据类型

```cpp
struct GaussianPdInput { double signal_count{}; double noise_count{}; double threshold_snr{}; };
struct GaussianPdOutput { double probability{}; };
```

## 4. 核心接口

```cpp
GaussianPdOutput compute_gaussian_detection_probability(const GaussianPdInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `compute_gaussian_detection_probability` | 有限；若信号正则噪声正 | 输出 [0,1] | 无 | $O(1)$ |

## 5. 状态生命周期

无内部状态。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `signal_count<=0` | 入口 | 返回 0，源码兼容 | 无 |
| `noise_count<=0 && signal>0` | 入口 | `invalid_argument` | 提供有效噪声 |
| `abs(beta)<=1e-5` | 核心 | 返回 .5 | 保留源码带宽 |

## 7. AFSIM 到中性接口映射

| AFSIM 项 | 中性项 | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `aSignal/aNoise/aThreshold` | 三个输入字段 | 直接复制 | none | `WsfLADAR_Sensor.cpp:638-681` |
| `return pd` | `probability` | 直接复制 | none | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `exp` | 正态密度 | 保留 | 标准数学库 | 低 |

## 9. 最小调用示例

```cpp
auto out = compute_gaussian_detection_probability({20.0, 10.0, 1.0});
// 中文：概率约为 0.8413513380564247。
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 20,10,1 | `.8413513380564247` | `1e-12` | 超差 |
| 边界 | 10,10,1 | `.5` | 精确 | 不等 |
| 退化 | 0,10,1 | 0 | 精确 | 不等 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| LADAR-GPD-001 | 被忽略的第二 Q 项是否应供增强模型使用 | 模型保真度 | MDC B1368 原文 | no |
