# 光学路径球形地球高度接口规格

> **算法 ID**：ALG-SENSORS-OPTICAL-CURVED-EARTH-PATH-HEIGHT  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-optical-curved-earth-path-height-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：计算球面弦路径任一点的 MSL 高度；不负责路径积分。
- 调用时机：每个光学传播积分采样点。
- 可重入/线程安全：纯函数。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `sample_range_m/total_slant_range_m` | `double` | m | 平台→目标 LOS | `0<=sample<=total`, total>0 | current |
| `target_height_m/platform_height_m` | `double` | m | MSL | finite | current |
| `earth_radius_m` | `double` | m | 球心 | `>0` | config |

## 3. 中性数据类型

```cpp
struct CurvedPathHeightInput { double sample_range_m{}, total_slant_range_m{}, target_height_m{}, platform_height_m{}, earth_radius_m{}; };
struct CurvedPathHeightOutput { double height_m{}; };
```

## 4. 核心接口

```cpp
CurvedPathHeightOutput compute_curved_path_height(const CurvedPathHeightInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `compute_curved_path_height` | 有效球面三角形 | 有限 MSL 高度 | 无 | $O(1)$ |

## 5. 状态生命周期

无持久状态。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 总距/地球半径非正 | 入口 | `invalid_argument` | 修正配置 |
| 根号负或采样越界 | 公式/入口 | `invalid_geometry` | 提供一致 LOS |

## 7. AFSIM 到中性接口映射

| AFSIM 项 | 中性项 | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| 四个 `a*` 参数 | 四个输入字段 | 直接复制 | none | `WsfOpticalPath.cpp:176-193` |
| `UtSphericalEarth::cEARTH_RADIUS` | `earth_radius_m` | 显式化 | 框架常量 | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `UtSphericalEarth` | 常量 | 替换 | 配置参数 | 地球模型差异 |

## 9. 最小调用示例

```cpp
auto out = compute_curved_path_height({5000,10000,0,1000,6371000});
// 中文：返回约 498.0577569035813 m。
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节 | `498.0577569035813` | `1e-9` | 超差 |
| 边界 | sample=0 | platform height | `1e-9` | 超差 |
| 退化 | total=0 | `invalid_geometry` | 不除零 | 未报错 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| OPT-H-001 | 是否需要椭球地球替代 | 精度 | 目标场景要求 | no |
