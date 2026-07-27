# 气动体总阻力系数接口规格

> **算法 ID**：ALG-AERODYNAMICS-BODY-TOTAL-DRAG-COEFFICIENT  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/aerodynamics-body-total-drag-coefficient-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：汇总姿态、诱导、摩擦和外形阻力系数。
- 调用时机：气动力求解；不实现子系数模型。
- 可重入/线程安全：子模型回调线程安全时可重入。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `alpha_rad/beta_rad` | `double` | rad | 机体气动角 | finite | current |
| `mach` | `double` | 1 | - | `>=0` | current |
| 系数与面积比 | `double` | 1 | - | finite；截面积 `>0` | current |

## 3. 中性数据类型

```cpp
struct BodyDragGeometry { double surface_area{}, cross_section_area{}, drag_multiplier{1}; };
struct BodyDragModel { std::function<double(double,double)> lift, side; std::function<double(double)> skin_friction, shape_drag; };
struct BodyDragInput { double alpha_rad{}, beta_rad{}, mach{}; BodyDragGeometry geometry; BodyDragModel model; };
struct BodyDragOutput { double drag_coefficient{}; };
```

## 4. 核心接口

```cpp
BodyDragOutput compute_body_drag_coefficient(const BodyDragInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- |
| `compute_body_drag_coefficient` | 有效几何与回调 | 有限 $C_D$ | 无 | $O(1)$ + 回调 |

## 5. 状态生命周期

无算法持久状态；几何与子模型配置由调用者持有。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 截面积非正 | 入口 | `invalid_geometry` | 提供参考面积 |
| 回调缺失/非有限 | 入口/调用后 | `invalid_model` | 配置子模型 |
| Mach 负或角非有限 | 入口 | `invalid_argument` | 修正状态 |

## 7. AFSIM 到中性接口映射

| AFSIM 项 | 中性项 | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `aAlpha_rad/aBeta_rad/aMach` | 三标量 | 直接复制 | none | `AeroBody.cpp:293-319` |
| 面积和倍率成员 | `BodyDragGeometry` | 直接复制 | 类所有权 | 同上 |
| 四个 `Calc*Coefficient` | `BodyDragModel` | 回调 | 辅助实现 | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `AeroBody` | 数据/子模型 | 替换 | 值与回调 | 配置一致性 |
| `UtMath::cPI` | 常量 | 替换 | 标准 π | 低 |

## 9. 最小调用示例

```cpp
// 中文：回调返回已验证的子系数；零姿态时结果约为 0.26677184039195917。
BodyDragInput in{0,0,0.8,{10,1,1.2},{[](double,double){return .5;},[](double,double){return .2;},[](double){return .003;},[](double){return .1;}}};
auto out = compute_body_drag_coefficient(in);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节 | `.26677184039195917` | `1e-12` | 超差 |
| 边界 | beta=pi/2 | 姿态项=2 | `1e-12` | 超差 |
| 退化 | cross_area=0 | `invalid_geometry` | 不除零 | 未报错 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| AERO-CD-001 | 阻力倍率配置来源 | 标定 | 设计器输入链 | no |
