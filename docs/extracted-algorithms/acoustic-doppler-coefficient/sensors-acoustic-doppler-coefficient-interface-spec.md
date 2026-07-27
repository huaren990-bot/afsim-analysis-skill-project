# 声学 Doppler 频率系数接口规格

> **算法 ID**：ALG-SENSORS-ACOUSTIC-DOPPLER-COEFFICIENT  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-acoustic-doppler-coefficient-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：根据同一坐标系中的收发位置、速度和声速计算频率倍率。
- 调用时机：上层查询 Doppler 偏移后的目标签名前。
- 包含/不包含：包含视线投影和源码超声速规则；不采样大气或声谱。
- 可重入/线程安全：纯函数，可重入且线程安全。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `receiver_position` | `Vec3` | m | 任一统一笛卡尔系 | 有限 | 同一时刻 |
| `receiver_velocity` | `Vec3` | m/s | 与位置同系 | 有限 | 同一时刻 |
| `source_position` | `Vec3` | m | 与接收机同系 | 有限 | 同一时刻 |
| `source_velocity` | `Vec3` | m/s | 与接收机同系 | 有限 | 同一时刻 |
| `sound_speed_mps` | `double` | m/s | 无 | 有限且 $>0$ | 路径代表值 |
| `frequency_multiplier` | `double` | 1 | 无 | 成功时有限且 $>0$ | 本次计算 |

## 3. 中性数据类型

```cpp
struct Vec3
{
    double x{};
    double y{};
    double z{};
};

struct AcousticDopplerInput
{
    Vec3 receiver_position_m{};
    Vec3 receiver_velocity_mps{};
    Vec3 source_position_m{};
    Vec3 source_velocity_mps{};
    double sound_speed_mps{};
};

struct AcousticDopplerOutput
{
    double frequency_multiplier{};
    double receiver_radial_speed_mps{};
    double source_radial_speed_mps{};
    bool coincident{};
};

enum class AcousticDopplerError
{
    none,
    non_finite_input,
    non_positive_sound_speed,
    supersonic_geometry,
    non_finite_output
};

template<class T>
struct Result
{
    T value{};
    AcousticDopplerError error{AcousticDopplerError::none};
};
```

算法无配置和持久状态。

## 4. 核心接口

```cpp
// 中文：返回 observed/static 频率倍率；超声速条件用错误码表示，不使用 -1 哨兵。
Result<AcousticDopplerOutput>
compute_acoustic_doppler_coefficient(const AcousticDopplerInput& input);

// 中文：按 AFSIM 调用者的实际行为将中心频率乘以倍率。
Result<double> shift_frequency(double static_frequency_hz,
                               double frequency_multiplier);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_acoustic_doppler_coefficient` | 输入有限，声速正 | 成功时倍率正且有限 | 无 | $O(1)$ |
| `shift_frequency` | 两参数正且有限 | 返回二者乘积 | 无 | $O(1)$ |

## 5. 状态生命周期

| 状态 | 初值 | 读取时机 | 更新时机 | 重置规则 | 序列化/复制 |
| --- | --- | --- | --- | --- | --- |
| 无 | — | — | — | 无需重置 | 无需序列化 |

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| NaN/Inf | 入口 | `non_finite_input` | 修复运动/大气状态 |
| 声速 $\le0$ | 入口 | `non_positive_sound_speed` | 使用合法声速 |
| $-v_r\ge c$ 或 $v_s\ge c$ | 投影后 | `supersonic_geometry` | 本次声学检测不可用 |
| 收发同位 | 归一化 | 成功，倍率 1、`coincident=true` | 决定是否接受中性结果 |
| 输出非有限/非正 | 比值后 | `non_finite_output` | 记录接近声速的输入 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `GetLocationWCS` | 两个位置向量 | 分量复制 | 平台身份 | `WsfAcousticSensor.cpp:989-1003` |
| `GetVelocityWCS` | 两个速度向量 | 分量复制 | 平台状态历史 | `WsfAcousticSensor.cpp:989-997` |
| `mAtmosphere.SonicVelocity` | `sound_speed_mps` | 在平均高度采样后传入 | 大气剖面 | `WsfAcousticSensor.cpp:985-987` |
| `ComputeDopplerTerm` | `compute_acoustic_doppler_coefficient` | `-1` 映射为错误码 | 无 | `WsfAcousticSensor.cpp:983-1026` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfSensorResult` / `WsfPlatform` | 运动状态访问 | 移除 | 显式向量输入 | 时刻必须一致 |
| `UtAtmosphere` | 声速 | 替换 | 上层采样 | 路径代表高度选择 |
| `UtVec3d` | 向量运算 | 替换 | 小型 `Vec3` 库 | 归一化容差 |

## 9. 最小调用示例

```cpp
AcousticDopplerInput input{
    .receiver_position_m = {0.0, 0.0, 0.0},
    .receiver_velocity_mps = {10.0, 0.0, 0.0},   // 中文：朝声源 10 m/s
    .source_position_m = {1000.0, 0.0, 0.0},
    .source_velocity_mps = {-20.0, 0.0, 0.0},    // 中文：朝接收机 20 m/s
    .sound_speed_mps = 340.0
};

// 中文：期望倍率 1.09375；1000 Hz 查询频率为 1093.75 Hz。
const auto result = compute_acoustic_doppler_coefficient(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常接近 | 第 9 节输入 | `1.09375` | 绝对误差 $\le10^{-12}$ | 超差 |
| 静止 | 两端速度 0 | `1.0` | 精确相等 | 非 1 |
| 同位 | 两端位置相同 | `1.0`，`coincident=true` | 精确相等 | 分母或 NaN |
| 超声速 | 声源朝接收机速度 340 m/s | `supersonic_geometry` | 不计算倍率 | 返回数值 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| Q-001 | 是否按调用者乘法还是函数注释除法迁移 | 频移方向 | AFSIM 场景黄金输出；当前兼容规范选乘法 | no |
| Q-002 | 接近声速时是否设置倍率上限 | 数值与声谱外推 | 目标需求 | no |
