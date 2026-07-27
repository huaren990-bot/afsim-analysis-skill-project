# 声学地面效应与反射干涉接口规格

> **算法 ID**：ALG-SENSORS-ACOUSTIC-GROUND-EFFECT  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-acoustic-ground-effect-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：把框架几何/环境适配与可移植复数核心分开，计算源码兼容的地面效应值。
- 调用时机：声学频带传播损失合成阶段。
- 包含/不包含：核心包含复阻抗与干涉；几何适配器包含反射点估计；不决定返回量如何换算为 dB。
- 可重入/线程安全：核心纯函数；几何适配器取决于地形服务。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `incidence_angle_rad` | `double` | rad | 反射点局部 NED | 有限 | 当前几何 |
| `direct_range_m` | `double` | m | 标量 | $>0$ | 当前几何 |
| `reflected_range_m` | `double` | m | 标量 | $>0$ | 当前几何 |
| `ground_range_m` | `double` | m | 地表距离 | $\ge0$ | 当前几何 |
| `azimuth_phase_rad` | `double` | rad | 源码目标到接收机方位语义 | 有限 | 当前几何 |
| `frequency_hz` / `bandwidth_hz` | `double` | Hz | 无 | $>0$ | 当前频带 |
| `sound_speed_*` | `double` | m/s | 无 | $>0$ | 当前环境 |
| `reflection_density_kgpm3` | `double` | kg/m³ | 无 | $>0$ | 当前环境 |
| `legacy_ground_effect` | `double` | 未证明 | 无 | 有限 | 本次计算 |

## 3. 中性数据类型

```cpp
enum class SurfaceClass { barren, wetland, urban, other };

struct GroundEffectCoreInput
{
    double incidence_angle_rad{};
    double direct_range_m{};
    double reflected_range_m{};
    double ground_range_m{};
    double azimuth_phase_rad{};
    double frequency_hz{};
    double bandwidth_hz{};
    double midpoint_sound_speed_mps{};
    double reflection_sound_speed_mps{};
    double reflection_density_kgpm3{};
    SurfaceClass surface{SurfaceClass::other};
};

struct GroundEffectOutput
{
    double legacy_ground_effect{}; // 中文：忠实公式输出，单位未证明
    bool bypassed_high_incidence{};
};

enum class GroundEffectError
{
    none,
    non_finite_input,
    non_positive_environment,
    non_positive_range,
    singular_path_difference,
    non_finite_output
};

template<class T>
struct Result
{
    T value{};
    GroundEffectError error{GroundEffectError::none};
};
```

反射点几何另由上层适配器生成，核心接口不携带 AFSIM 对象。

## 4. 核心接口

```cpp
// 中文：执行 WsfAcousticSensor.cpp:761-911 的复数核心。
Result<GroundEffectOutput>
compute_legacy_acoustic_ground_effect(const GroundEffectCoreInput& input);

// 中文：可选稳定版本，仅把 sin(x)/x 重写为 sinc 等价式，不改变数学模型。
Result<GroundEffectOutput>
compute_stable_acoustic_ground_effect(const GroundEffectCoreInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_legacy_acoustic_ground_effect` | 输入有限、环境量和距离正 | 成功时输出有限 | 无 | $O(1)$，复指数/开方 |
| `compute_stable_acoustic_ground_effect` | 同上 | 路径差趋零时保持有限 | 无 | $O(1)$ |

在单位决策完成前，不提供把输出直接应用到 dB 声级的 API。

## 5. 状态生命周期

| 状态 | 初值 | 读取时机 | 更新时机 | 重置规则 | 序列化/复制 |
| --- | --- | --- | --- | --- | --- |
| 无核心状态 | — | — | — | 无需重置 | 无需序列化 |
| 地形/大气服务 | 上层配置 | 几何适配阶段 | 核心不更新 | 上层负责 | 不属于算法状态 |

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| NaN/Inf | 入口 | `non_finite_input` | 修复几何/环境 |
| 频率、声速、密度 $\le0$ | 入口 | `non_positive_environment` | 限定模型有效域 |
| 直达/反射距离 $\le0$ | 入口 | `non_positive_range` | 修复反射几何 |
| $R_d=R_r$ | 核心 | legacy 返回 `singular_path_difference`；stable 用极限 | 选择兼容/稳定模式 |
| $\theta>5°$ | 入口分支 | 成功返回 1.0 并置 bypass 标志 | 不自行解释为 dB |
| 输出非有限 | 结果 | `non_finite_output` | 记录全部输入 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `ComputeIncidenceAngle` | 几何适配器 | 输出角、反射距和 LLA 反射点；源码注释误称 WCS | AFSIM 对象身份 | `WsfAcousticSensor.cpp:921-977` |
| `mTgtToRcvr.mRange/mAz` | 直达距/相位项 | 直接复制 | 其余交互量 | `WsfAcousticSensor.cpp:901-907` |
| `GroundRange` | `ground_range_m` | 直接复制 | 地球模型 | `WsfAcousticSensor.cpp:785-790` |
| `SonicVelocity` / `Density` | 三个环境量 | 在对应高度采样 | 大气剖面 | `WsfAcousticSensor.cpp:788-850` |
| `LandCover` | `SurfaceClass` | 按四分支归并 | 更细地表类别 | `WsfAcousticSensor.cpp:816-846` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfSensorResult` | 交互几何 | 移除 | 标量输入 | 字段语义 |
| `UtEllipsoidalEarth` / `UtSphericalEarth` | 反射几何 | 替换 | 地理库与地形服务 | 源码几何疑点 |
| `UtAtmosphere` | 环境 | 替换 | 显式采样值 | 模型差异 |
| `std::complex` | 复数运算 | 保留等价能力 | 标准复数库 | 分支/开方约定 |

## 9. 最小调用示例

```cpp
GroundEffectCoreInput input{
    .incidence_angle_rad = 2.0 * pi / 180.0,
    .direct_range_m = 1000.0,
    .reflected_range_m = 1005.0,
    .ground_range_m = 1000.0,
    .azimuth_phase_rad = 0.3,
    .frequency_hz = 1000.0,
    .bandwidth_hz = 450.0,
    .midpoint_sound_speed_mps = 340.0,
    .reflection_sound_speed_mps = 340.0,
    .reflection_density_kgpm3 = 1.225,
    .surface = SurfaceClass::other
};

// 中文：按源码常量 gamma=1.401，期望 1.6262959722255057。
const auto result = compute_legacy_acoustic_ground_effect(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 完整核心 | 第 9 节输入 | `1.6262959722255057` | 绝对误差 $\le10^{-12}$ | 超差 |
| 高入射角 | 6°，其余合法 | `1.0`、bypass=true | 精确相等 | 继续复数计算 |
| 四类地表 | 固定几何，遍历分类 | 独立复数实现 | 每类误差 $\le10^{-12}$ | 参数映射错误 |
| 路径差退化 | $R_d=R_r$ | legacy 错误；stable 有限 | 无 NaN/Inf | 未处理 0/0 |
| 异常 | 非正环境量/距离 | 对应错误码 | 无部分输出 | 返回成功 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| Q-001 | 返回值应视为线性因子还是 dB | 与其他传播项合成 | Ref 1、AFSIM 黄金场景、维护者说明 | yes |
| Q-002 | `ComputeIncidenceAngle` 的变换实参是否正确，且 `aLoc` 注释为何称 WCS 而实际写 LLA | 全部反射几何和坐标适配 | 单元场景和预期反射点 | yes |
| Q-003 | `mAz` 作为干涉相位的理论含义 | 方位依赖 | Ref 1 | no |
