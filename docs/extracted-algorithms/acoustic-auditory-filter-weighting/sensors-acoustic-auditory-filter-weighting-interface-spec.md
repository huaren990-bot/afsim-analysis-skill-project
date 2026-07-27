# 三分之一倍频程听觉加权接口规格

> **算法 ID**：ALG-SENSORS-ACOUSTIC-AUDITORY-FILTER-WEIGHTING  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-acoustic-auditory-filter-weighting-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：对 24 个标准中心频带中的一个执行固定局部加权求和。
- 调用时机：上层分别计算目标频带量和背景频带量时。
- 包含/不包含：包含权重与 Doppler 后的采样频率；不包含谱插值实现和 dB 转换。
- 可重入/线程安全：权重不可变且采样器线程安全时可重入。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `band_index` | `int` | 1 | 无 | 0–23 | 当前频带 |
| `frequency_hz` | `double` | Hz | 无 | 采样器支持范围 | 当前查询 |
| `doppler_multiplier` | `double` | 1 | 无 | 目标模式时有限且 $>0$ | 当前交互 |
| `sample` | `double` | 代码线性声级 | 无 | 有限且 $\ge0$ | 当前谱状态 |
| `weighted_level` | `double` | 同 `sample` | 无 | 成功时有限且 $>0$ | 本次计算 |

## 3. 中性数据类型

```cpp
enum class SpectrumKind
{
    target,
    background
};

struct AuditoryFilterInput
{
    int band_index{};
    SpectrumKind kind{SpectrumKind::background};
    double doppler_multiplier{1.0};
};

struct AuditoryFilterOutput
{
    double weighted_level{};
    int sample_count{};
};

// 中文：调用者实现频率插值；返回线性声级量而不是 dB。
using SpectrumSampler = std::function<Result<double>(double frequency_hz)>;

enum class AuditoryFilterError
{
    none,
    band_out_of_range,
    invalid_doppler,
    sampler_failure,
    non_finite_sample,
    non_positive_output
};

template<class T>
struct Result
{
    T value{};
    AuditoryFilterError error{AuditoryFilterError::none};
};
```

权重矩阵和中心频率数组是算法版本 `1.0` 的不可变常量，完整值见算法卡。

## 4. 核心接口

```cpp
// 中文：执行一个频带的局部加权；不执行 log10。
Result<AuditoryFilterOutput>
apply_auditory_filter_weighting(const AuditoryFilterInput& input,
                                const SpectrumSampler& sampler);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `apply_auditory_filter_weighting` | 索引合法、采样器有效；目标模式倍率正 | 成功时输出正且有限 | 调用采样器 1–5 次 | $O(1)$ |

## 5. 状态生命周期

| 状态 | 初值 | 读取时机 | 更新时机 | 重置规则 | 序列化/复制 |
| --- | --- | --- | --- | --- | --- |
| 无算法状态 | — | — | — | 无需重置 | 无需序列化 |
| 谱状态 | 调用者定义 | 每次采样 | 算法不更新 | 调用者负责 | 由调用者负责 |

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 索引越界 | 入口 | `band_out_of_range` | 仅传 0–23 |
| 目标倍率 $\le0$ 或非有限 | 入口 | `invalid_doppler` | 先完成 Doppler 检查 |
| 采样器失败 | 循环 | `sampler_failure` | 提供覆盖查询频率的谱 |
| 样本非有限/负 | 循环 | `non_finite_sample` | 修复谱表 |
| 加权和 $\le0$ | 结果 | `non_positive_output` | 不执行下游 `log10` |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `aIndex` | `band_index` | 直接复制 | 无 | `WsfAcousticSensor.cpp:584-610` |
| `aFlag == 1` | `SpectrumKind::target` | 其他值统一映射背景 | 原始整数 | `WsfAcousticSensor.cpp:613-622` |
| `aDoppler` | `doppler_multiplier` | 直接复制 | 无 | `WsfAcousticSensor.cpp:615` |
| `WsfAcousticSignature::GetValue` | `SpectrumSampler` | 目标谱适配器 | 平台/状态 ID | `WsfAcousticSensor.cpp:615-617` |
| `mBackgroundNoise.GetNoisePressure` | `SpectrumSampler` | 背景谱适配器 | 背景状态 ID | `WsfAcousticSensor.cpp:618-622` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfAcousticSignature` | 目标签名查询 | 替换 | 采样回调 | 外推策略差异 |
| `WsfStandardAcousticSignature` | 背景插值 | 替换 | 同一回调 | 插值器需另行对齐 |
| 权重/频率常量 | 算法参数 | 保留 | 只读数组 | 版本和来源 |

## 9. 最小调用示例

```cpp
AuditoryFilterInput input{
    .band_index = 5,
    .kind = SpectrumKind::target,
    .doppler_multiplier = 1.0
};

// 中文：测试采样器对任意合法频率返回 1。
SpectrumSampler sampler = [](double) { return Result<double>{1.0}; };

// 中文：期望 weighted_level = 1.53096，sample_count = 5。
const auto result = apply_auditory_filter_weighting(input, sampler);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 5 点窗 | `band=5`，常数谱 1 | `1.53096`，5 次采样 | 绝对误差 $\le10^{-12}$ | 超差 |
| 低端 | `band=0`，常数谱 1 | `2.5`，3 次采样 | 绝对误差 $\le10^{-12}$ | 超差 |
| 高端 | `band=23`，常数谱 1 | `1.0`，3 次采样 | 精确相等 | 非 1 |
| Doppler | 目标模式、倍率 2 | 每个查询频率是对应中心频率两倍 | 逐项精确 | 查询未偏移 |
| 异常 | 越界、非法倍率、采样失败 | 对应错误码 | 无部分结果 | 返回成功 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| Q-001 | $j=1,2$ 不取低频邻居是否为有意 | 与“对称 5 点窗”差异 | Ref 3 或黄金输出 | no，兼容实现保留 |
| Q-002 | 线性声级量的正式物理单位 | 接口命名和跨系统换算 | 签名输入文档/单位测试 | yes |
