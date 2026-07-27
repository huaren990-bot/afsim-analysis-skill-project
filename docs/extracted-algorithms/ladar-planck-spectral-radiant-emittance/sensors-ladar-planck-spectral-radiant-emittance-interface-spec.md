# LADAR 普朗克谱辐射出射度接口规格

> **算法 ID**：ALG-SENSORS-LADAR-PLANCK-SPECTRAL-RADIANT-EMITTANCE  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-ladar-planck-spectral-radiant-emittance-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：计算每 µm 的黑体谱辐射出射度；不做背景状态更新或波段积分。
- 调用时机：LADAR 模式初始化或任意纯函数调用。
- 可重入/线程安全：无状态、可重入。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `temperature_k` | `double` | K | - | finite, `>0` | current |
| `wavelength_um` | `double` | µm | - | finite, `>0` | current |
| `emittance_w_per_cm2_um` | `double` | W/(cm²·µm) | - | finite, `>=0` | output |

内部使用 µm 和 K；不隐式做面积或波段单位转换。

## 3. 中性数据类型

```cpp
struct PlanckSpectralInput { double temperature_k{}; double wavelength_um{}; };
struct PlanckSpectralOutput { double emittance_w_per_cm2_um{}; };
```

## 4. 核心接口

```cpp
PlanckSpectralOutput compute_planck_spectral_emittance(const PlanckSpectralInput& input);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度 |
| --- | --- | --- | --- | --- |
| `compute_planck_spectral_emittance` | 两输入正且有限 | 返回有限非负值或错误 | 无 | $O(1)$ |

## 5. 状态生命周期

无持久状态、初始化或重置要求。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 非正/非有限输入 | 入口 | `invalid_argument` | 提供 K、µm 正数 |
| 指数溢出 | 公式 | 返回受控极限 0 或 `numeric_error` | 记录策略 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `aTemperature` | `temperature_k` | 直接复制 | none | `WsfLADAR_Sensor.cpp:205-232` |
| `aWavelength` | `wavelength_um` | 直接复制 | none | 同上 |
| `return` | `emittance_w_per_cm2_um` | 直接复制 | none | 同上 |

## 8. 依赖替换

| 依赖 | 作用 | 决策 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `expm1` | 稳定指数差 | 保留 | 标准数学库 | 低 |

## 9. 最小调用示例

```cpp
PlanckSpectralInput in{300.0, 10.0}; // 中文：300 K 黑体在 10 µm。
auto out = compute_planck_spectral_emittance(in); // 中文：约 0.003117725468277123。
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 300 K, 10 µm | `.003117725468277123` | `1e-15` | 超差 |
| 边界 | 300 K, 1 µm | 有限、非负 | 有限性 | 非有限 |
| 退化 | 0 K | `invalid_argument` | 不执行除法 | 未报错 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| LADAR-PLANCK-001 | 下游面积单位换算位置 | 集成单位 | 接收机/配置文档 | no |
