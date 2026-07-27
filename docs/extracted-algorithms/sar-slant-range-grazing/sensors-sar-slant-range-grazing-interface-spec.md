# SAR 曲率地球斜距与擦地角算法接口规格

> **算法 ID**：ALG-SENSORS-SAR-SLANT-RANGE-GRAZING  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-sar-slant-range-grazing-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：由高度、俯角和有效地球半径计算斜距与擦地角。
- 调用时机：SAR 几何更新。
- 包含/不包含：包含地平线夹取；不处理地形、椭球和折射。
- 可重入/线程安全：纯函数。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `altitude_m` | `double` | m | spherical earth radial | finite | current |
| `depression_angle_rad` | `double` | rad | positive down | finite | current |
| `earth_radius_m` | `double` | m | spherical earth | finite, `>0` | config |

## 3. 中性数据类型

```cpp
struct SarSlantRangeInput
{
    double altitude_m{};
    double depression_angle_rad{};
    double earth_radius_m{};
};

enum class SarSlantRangeStatus
{
    ok,
    negative_altitude,
    nadir,
    horizon_clamped,
    invalid_input,
    non_finite_output
};

struct SarSlantRangeOutput
{
    double slant_range_m{};
    double grazing_angle_rad{};
    double horizon_depression_angle_rad{};
    SarSlantRangeStatus status{SarSlantRangeStatus::ok};
};
```

## 4. 核心接口

```cpp
SarSlantRangeOutput compute_sar_slant_range_grazing(const SarSlantRangeInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_sar_slant_range_grazing` | 输入有限，半径大于 0 | 返回有限斜距和擦地角 | 无 | $O(1)$ |

## 5. 状态生命周期

算法无状态。输出通常写入 `Geometry::mSlantRange` 和 `Geometry::mGrazingAngle`，在每次几何更新时覆盖。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `altitude_m < 0` | 入口 | range=0, grazing=0 | 标记退化 |
| `depression >= pi/2` | 入口 | range=altitude, grazing=pi/2 | 保留源码兼容 |
| `depression <= horizon` | 几何分支 | 返回 horizon tangent range | 判断是否可成像 |
| 定义域错误 | 计算前 | `invalid_input` | 修正输入 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `aAltitude` | `altitude_m` | 直接复制 | none | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2273` |
| `aDepressionAngle` | `depression_angle_rad` | 直接复制 | none | `WsfSAR_Sensor.cpp:2273` |
| `UtSphericalEarth::cEARTH_RADIUS * multiplier` | `earth_radius_m` | 适配层相乘 | multiplier 来源外置 | `WsfSAR_Sensor.cpp:2289` |
| `aGrazingAngle` | `grazing_angle_rad` | 输出字段 | reference 参数改为值返回 | `WsfSAR_Sensor.cpp:2325-2335` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `UtSphericalEarth` | 半径常量 | 替换 | 显式半径 | 常量差异 |
| `WsfEM_Xmtr` | 半径倍数 | 移除 | 显式半径 | 配置来源 |

## 9. 最小调用示例

```cpp
SarSlantRangeInput input{};
input.altitude_m = 10000.0;
input.depression_angle_rad = std::numbers::pi / 6.0;
input.earth_radius_m = 6371000.0;

// 中文：期望 slant_range_m 约为 20047.311502652294。
auto output = compute_sar_slant_range_grazing(input);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节样例 | range `20047.311502652294`, grazing `0.5208736927970348` | `1e-9` | 超差 |
| nadir | `dep=pi/2` | range=altitude, grazing=pi/2 | 精确 | 状态错误 |
| negative | `alt<0` | range=0, grazing=0 | 精确 | 状态错误 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| SAR-SLANT-001 | 有效地球半径倍数默认值来源 | 复现实验 | 发射机配置文档 | no |
