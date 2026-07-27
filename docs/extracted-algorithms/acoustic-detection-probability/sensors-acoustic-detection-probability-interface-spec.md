# 声学探测概率高斯近似算法接口规格

> **算法 ID**：ALG-SENSORS-ACOUSTIC-DETECTION-PROBABILITY  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-acoustic-detection-probability-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：将接收声级相对有效噪声和门限的裕量映射为探测概率。
- 调用时机：上层选定要评估的频带后。
- 包含/不包含：包含源码高斯 CDF 近似；不包含频带选择、布尔检测或随机抽样。
- 可重入/线程安全：纯函数，可重入且线程安全。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `signal_db` | `double` | dB | 无 | 有限；兼容源码时需 $>0$ 才计算 | 当前频带 |
| `noise_db` | `double` | dB | 无 | 有限 | 当前频带 |
| `threshold_db` | `double` | dB | 无 | 有限 | 当前配置 |
| `probability` | `double` | 1 | 无 | 目标 $[0,1]$ | 本次计算 |

三个 dB 量必须采用相同参考值。算法只用差值，但源码的 `signal_db <= 0` 早退依赖绝对数值。

## 3. 中性数据类型

```cpp
// 中文：三个输入均是采用相同参考值的 dB 数值。
struct AcousticDetectionProbabilityInput
{
    double signal_db{};       // 中文：接收信号声级
    double noise_db{};        // 中文：有效背景/听阈声级
    double threshold_db{};    // 中文：Pd=0.5 对应的 SNR 门限
};

struct AcousticDetectionProbabilityOutput
{
    double probability{};     // 中文：无量纲探测概率
    double beta{};            // 中文：S-N-threshold，便于诊断和验证
};

enum class AcousticProbabilityError
{
    none,
    non_finite_input,
    probability_out_of_range
};

template<class T>
struct Result
{
    T value{};
    AcousticProbabilityError error{AcousticProbabilityError::none};
};
```

算法无持久状态；多项式系数是模型定义，不作为运行时可调配置。

## 4. 核心接口

```cpp
// 中文：忠实执行 AFSIM 分支，包括 signal_db <= 0 时返回零。
Result<AcousticDetectionProbabilityOutput>
compute_acoustic_detection_probability(
    const AcousticDetectionProbabilityInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_acoustic_detection_probability` | 三个输入有限且使用同一 dB 参考 | 成功时 $0\le P_d\le1$ | 无 | $O(1)$；一次 `exp` |

## 5. 状态生命周期

| 状态 | 初值 | 读取时机 | 更新时机 | 重置规则 | 序列化/复制 |
| --- | --- | --- | --- | --- | --- |
| 无 | — | — | — | 无需重置 | 无需序列化 |

上层的“最大 SNR 频带”和累计 `mPd` 不属于本接口状态。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 任一输入 NaN/Inf | 函数入口 | 返回 `non_finite_input` | 修复上游声级计算 |
| `signal_db <= 0` | 输入分支 | 成功返回 `probability=0` | 明确是否需要源码兼容语义 |
| $|\beta|\le10^{-5}$ | 核心分支 | 成功返回 `0.5` | 回归测试边界 |
| 近似值越出 $[0,1]$ | 结果验证 | 返回 `probability_out_of_range` | 不静默钳制，记录输入 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `receivedPressureDB` | `signal_db` | 直接传入 | 所属频带 | `WsfAcousticSensor.cpp:504-505,528` |
| `max(filteredBackgroundDB, thresholdDB)` | `noise_db` | 取两者较大值后传入 | 背景与听阈各自值 | `WsfAcousticSensor.cpp:507-515,528-530` |
| `mDetectionThreshold` | `threshold_db` | 直接传入 | 配置来源文本 | `WsfAcousticSensor.cpp:375-379,530` |
| `aResult.mPd` | `probability` | 调用者保存返回值 | AFSIM 结果对象状态 | `WsfAcousticSensor.cpp:522-531` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfSensorResult` | 保存概率和最大 SNR | 移除 | 显式返回结构 | 上层必须自行选择频带 |
| `WsfEM_Rcvr` / 输入解析 | 配置门限 | 替换 | 调用者传 `threshold_db` | 确保配置单位一致 |
| `std::exp` | 正态密度 | 保留等价能力 | 目标语言数学库 | 极端输入下溢属预期 |

## 9. 最小调用示例

```cpp
AcousticDetectionProbabilityInput input{
    .signal_db = 50.0,       // 中文：接收信号声级
    .noise_db = 40.0,        // 中文：有效背景/听阈声级
    .threshold_db = 9.0      // 中文：相对 50% 点有 +1 dB 裕量
};

// 中文：期望 probability 约为 0.8413513380564247，beta 为 1。
const auto result = compute_acoustic_detection_probability(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正半轴 | `50,40,9` | `0.8413513380564247` | 绝对误差 $\le10^{-12}$ | 超差 |
| 零点 | `50,40,10` | `0.5` | 精确相等 | 非 0.5 |
| 负半轴 | `50,40,11` | `0.1586486619435753` | 绝对误差 $\le10^{-12}$ | 超差 |
| 对称性 | $\beta=+1,-1$ | 两个概率和为 1 | 误差 $\le10^{-12}$ | 不满足 |
| 早退 | `signal_db=0` | `0` | 精确相等 | 非零 |
| 异常 | NaN/Inf | `non_finite_input` | 不返回概率 | 进入公式 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| Q-001 | 目标系统是否必须保留 `signal_db <= 0` 早退 | 负 dB 声级兼容性 | 迁移需求和基准场景 | yes |
| Q-002 | dB 裕量对应标准差单位的标定依据 | 概率统计解释 | MDC B1368 或项目标定数据 | no |
