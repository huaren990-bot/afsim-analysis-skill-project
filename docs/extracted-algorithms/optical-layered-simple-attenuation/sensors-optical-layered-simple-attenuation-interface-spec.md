# 光学分层简单大气透过率接口规格

> **算法 ID**：ALG-SENSORS-OPTICAL-LAYERED-SIMPLE-ATTENUATION  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-optical-layered-simple-attenuation-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：以 1000 m 层、平均相对密度计算简单平地大气透过率。
- 调用时机：光学相互作用选择 simple attenuation 时。
- 不包含：外层 adjustment factor、compact 模型、地球曲率。
- 可重入/线程安全：密度回调线程安全时可重入。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `altitude1_m/altitude2_m` | `double` | m | MSL | finite | current |
| `ground_range_m` | `double` | m | 平地水平 | `>=0` | current |
| `attenuation_per_m` | `double` | 1/m | 海平面 | `>=0` | config |
| `density(z)` | callback | 同一密度单位 | MSL | density(0)>0 | current |

## 3. 中性数据类型

```cpp
using DensityAtAltitude = std::function<double(double altitude_m)>;
struct SimpleAttenuationInput { double altitude1_m{}, altitude2_m{}, ground_range_m{}, attenuation_per_m{}; DensityAtAltitude density; };
struct SimpleAttenuationOutput { double transmittance{}; };
```

## 4. 核心接口

```cpp
SimpleAttenuationOutput compute_layered_simple_attenuation(const SimpleAttenuationInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `compute_layered_simple_attenuation` | 密度有效、范围/消光非负 | 返回有限透过率 | 无 | $O(\lceil\Delta z/1000\rceil)$ |

## 5. 状态生命周期

无状态；密度回调由调用者拥有并可缓存。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `density(0)<=0` | 初始化 | `invalid_density` | 提供基准密度 |
| 负地距/消光 | 入口 | `invalid_argument` | 修正配置 |
| 高度负 | 预处理 | 与源码一致截为 0 | 接受该近似 |

## 7. AFSIM 到中性接口映射

| AFSIM 项 | 中性项 | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `aAltitude1/aAltitude2/aGroundRange` | 三几何字段 | 直接复制 | none | `WsfOpticalAttenuation.cpp:298-363` |
| `mSimpleAttenuation` | `attenuation_per_m` | 直接复制 | 配置对象 | 同上 |
| `mAtmosphere.Density` | `density` | 回调 | 大气模型类型 | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `UtAtmosphere` | 密度 | 替换 | 回调/表 | 单位与线程安全 |
| `exp/sqrt` | 数学 | 保留 | 标准库 | 低 |

## 9. 最小调用示例

```cpp
SimpleAttenuationInput in{0,2000,1000,.001,[](double){ return 1.0; }};
auto out = compute_layered_simple_attenuation(in);
// 中文：常密度结果约为 0.10687792566038574。
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节 | `.10687792566038574` | `1e-12` | 超差 |
| 边界 | 0,0,1000,.001,ρ=1 | $e^{-1}$ | `1e-12` | 超差 |
| 退化 | density(0)=0 | `invalid_density` | 不除零 | 未报错 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| OPT-ATT-001 | 1000 m 层厚是否应配置化 | 精度/兼容 | 需求 | no |
