# LADAR 目标太阳反射谱辐照度接口规格

> **算法 ID**：ALG-SENSORS-LADAR-TARGET-SOLAR-IRRADIANCE  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-ladar-target-solar-irradiance-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：计算 $SA\rho T/R^2$ 的太阳反射接收谱辐照度。
- 调用时机：主动探测中、接收机噪声模型之前。
- 不包含：主动激光回波、两程传输或光子计数转换。
- 可重入/线程安全：无状态、可重入。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `background_spectral_irradiance` | `double` | code-compatible，源码下游注释 W/(m²·m) | - | finite | current |
| `target_area_m2` | `double` | m² | 目标投影面 | `>=0` | current |
| `reflectivity_per_sr` | `double` | 1/sr（源码用法） | - | `>=0` | current |
| `range_m` | `double` | m | LOS | `>0` | current |
| `transmittance` | `double` | 1 | LOS | normally [0,1] | current |

## 3. 中性数据类型

```cpp
struct SolarIrradianceInput { double background_spectral_irradiance{}; double target_area_m2{}; double reflectivity_per_sr{}; double range_m{}; double transmittance{}; };
struct SolarIrradianceOutput { double receiver_spectral_irradiance{}; };
```

## 4. 核心接口

```cpp
SolarIrradianceOutput compute_target_solar_irradiance(const SolarIrradianceInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `compute_target_solar_irradiance` | `range_m>0`、输入有限 | 返回有限输出 | 无 | $O(1)$ |

## 5. 状态生命周期

无内部状态。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 零/负距离 | 入口 | `invalid_argument` | 提供 LOS 距离 |
| 非法反射率或传输 | 入口 | 拒绝或明确宽松模式 | 提供物理量 |
| 面积为零 | 公式 | 返回 0 | 可接受退化 |

## 7. AFSIM 到中性接口映射

| AFSIM 项 | 中性项 | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `mBackgroundSpectralIrradiance` | `background_spectral_irradiance` | 直接复制 | 产生链 | `WsfLADAR_Sensor.cpp:259-281` |
| `aTargetArea/aTargetReflectivity` | 面积/反射率 | 直接复制 | none | 同上 |
| `aRange/aTransmittance` | 距离/传输 | 直接复制 | none | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| LADAR 模式状态 | 背景值 | 移除 | 显式输入 | 单位 |

## 9. 最小调用示例

```cpp
SolarIrradianceInput in{1000.0, 2.0, .4, 100.0, .8};
auto out = compute_target_solar_irradiance(in); // 中文：结果为 0.064。
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节 | `.064` | `1e-15` | 超差 |
| 边界 | `area=0` | 0 | 精确 | 不等 |
| 退化 | `range=0` | `invalid_argument` | 不除零 | 未报错 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| LADAR-SOLAR-001 | 反射率的精确辐射度定义 | 物理互操作 | 配置文档 | no |
