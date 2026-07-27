# 光学长方体投影面积接口规格

> **算法 ID**：ALG-SENSORS-OPTICAL-BOX-PROJECTED-AREA  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-optical-box-projected-area-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：无显式签名时计算长方体光学投影面积。
- 调用时机：签名选择器确认平台三维尺寸均正后。
- 不包含：签名查找、默认对象创建和 scale factor。
- 可重入/线程安全：纯函数。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `length_m/width_m/height_m` | `double` | m | 平台体轴 | `>0` | current |
| `azimuth_rad/elevation_rad` | `double` | rad | 与平台体轴一致 | finite | current |
| `projected_area_m2` | `double` | m² | 视线正交面 | `>=0` | output |

## 3. 中性数据类型

```cpp
struct BoxProjectionInput { double length_m{}, width_m{}, height_m{}, azimuth_rad{}, elevation_rad{}; };
struct BoxProjectionOutput { double projected_area_m2{}; };
```

## 4. 核心接口

```cpp
BoxProjectionOutput compute_box_projected_area(const BoxProjectionInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `compute_box_projected_area` | 正尺寸、有限角 | 非负面积 | 无 | $O(1)$ |

## 5. 状态生命周期

无内部状态。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 任一尺寸非正 | 入口 | `not_applicable` | 使用签名/默认路径 |
| 角度非有限 | 入口 | `invalid_argument` | 修正姿态 |

## 7. AFSIM 到中性接口映射

| AFSIM 项 | 中性项 | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `GetLength/Width/Height` | 三尺寸字段 | 直接复制 | 平台对象 | `WsfOpticalSignature.cpp:166-222` |
| `aAzimuth/aElevation` | 两角字段 | 直接复制 | 角语义外置 | 同上 |
| `sig` | `projected_area_m2` | 仅默认分支 | scale factor 外置 | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfPlatform` | 几何 | 替换 | 值结构 | 体轴约定 |

## 9. 最小调用示例

```cpp
auto out = compute_box_projected_area({4,2,1,0,0});
// 中文：正前视投影面积为 2 m²。
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 4,2,1,0,0 | 2 m² | `1e-15` | 超差 |
| 边界 | az=pi/2 | 4 m² | `1e-15` | 超差 |
| 退化 | height=0 | `not_applicable` | 不计算 | 未拒绝 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| OPT-BOX-001 | 平台轴和角的精确约定 | 互操作 | 平台坐标文档 | yes |
