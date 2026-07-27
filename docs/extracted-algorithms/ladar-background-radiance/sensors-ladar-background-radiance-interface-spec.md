# LADAR 黑体背景谱辐照度初始化接口规格

> **算法 ID**：ALG-SENSORS-LADAR-BACKGROUND-RADIANCE  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-ladar-background-radiance-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：在正背景温度时更新背景谱量；否则保留调用者状态。
- 调用时机：模式初始化完成接收机波长配置后。
- 包含/不包含：包含 m→µm 与每 µm→每 m 数值换算；不推断面积单位。
- 可重入/线程安全：调用者持有状态；不同状态实例可重入。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `background_temperature_k` | `double` | K | - | finite | config |
| `receiver_wavelength_m` | `double` | m | - | finite, `>0` | config |
| `spectral_irradiance_code_units` | `double` | code-compatible；下游注释 W/(m²·m) | - | finite | state |

## 3. 中性数据类型

```cpp
struct BackgroundRadianceInput { double background_temperature_k{}; double receiver_wavelength_m{}; };
struct BackgroundRadianceState { double spectral_irradiance_code_units{}; };
enum class BackgroundRadianceStatus { updated, not_configured, invalid_input };
struct BackgroundRadianceOutput { BackgroundRadianceStatus status{}; };
```

## 4. 核心接口

```cpp
BackgroundRadianceOutput initialize_background_radiance(const BackgroundRadianceInput&, BackgroundRadianceState&);
void reset(BackgroundRadianceState& state);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `initialize_background_radiance` | 波长有效；温度可为非正 | 正温度时更新状态 | 写 `state` | $O(1)$ |

## 5. 状态生命周期

| 状态 | 初值 | 读取时机 | 更新时机 | 重置规则 | 复制 |
| --- | --- | --- | --- | --- | --- |
| `spectral_irradiance_code_units` | 配置值或 0 | 太阳噪声计算 | 初始化且 $T>0$ | 调用者决定 | 值复制 |

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 温度 `<=0` | 入口 | `not_configured`，不改状态 | 提供配置或保留旧值 |
| 波长非正 | 入口 | `invalid_input`，不改状态 | 修正接收机配置 |

## 7. AFSIM 到中性接口映射

| AFSIM 项 | 中性项 | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `mBackgroundTemperature` | `background_temperature_k` | 直接复制 | none | `WsfLADAR_Sensor.cpp:234-244` |
| `mRcvr.GetWavelength()` | `receiver_wavelength_m` | 直接复制 | 接收机对象 | 同上 |
| `mBackgroundSpectralIrradiance` | state 字段 | 条件写入 | 面积单位未证实 | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfEM_Rcvr` | 提供波长 | 替换 | 标量 m | 低 |
| 普朗克函数 | 计算谱量 | 保留 | 前述纯函数 | 单位 |

## 9. 最小调用示例

```cpp
BackgroundRadianceState state{};
auto result = initialize_background_radiance({300.0, 1e-5}, state);
// 中文：状态被更新为约 3117.7254682771227，result.status 为 updated。
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 300 K, 10 µm | 3117.7254682771227 | `1e-9` | 超差 |
| 边界 | 0 K, state=7 | state=7 | 精确 | 被改写 |
| 退化 | 300 K, 0 m | `invalid_input` | 不写状态 | 未报错 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| LADAR-BG-001 | 面积单位缺失转换 | 集成量纲 | 配置/接收机文档 | yes |
