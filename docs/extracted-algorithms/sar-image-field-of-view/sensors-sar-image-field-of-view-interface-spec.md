# SAR 图像尺寸视场反算算法接口规格

> **算法 ID**：ALG-SENSORS-SAR-IMAGE-FIELD-OF-VIEW  
> **版本/状态**：1.0 / verified  
> **对应卡片**：`docs/algorithms/sensors-sar-image-field-of-view-card.md`  
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：由 cue、图像宽高、斜距和俯角计算天线方位/俯仰 FOV。
- 调用时机：SAR `ComputeGeometry` 中，在几何主量计算后更新天线 FOV。
- 包含/不包含：包含源码三角反算；不实现 terrain mask 递归，可用回调提供调整后的图像中心。
- 可重入/线程安全：纯计算接口可重入；terrain/cue 回调由调用者保证。

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `sensor_wcs_m` | `Vec3` | m | WCS | finite | current |
| `cue_wcs_m` | `Vec3` | m | WCS | finite if location cue | current |
| `slant_range_m` | `double` | m | PCS x axis | finite, `>=0` | current |
| `image_width_m` | `double` | m | image plane | finite, `>0` | config |
| `image_height_m` | `double` | m | image plane | finite, `>0` | config |
| `depression_angle_rad` | `double` | rad | NED positive down | finite | current |
| `los_ned_m` | `Vec3` | m | NED | finite | derived |

## 3. 中性数据类型

```cpp
struct Vec3
{
    double x{};
    double y{};
    double z{};
};

enum class SarCueType
{
    none,
    location,
    angle
};

struct SarImageFovInput
{
    SarCueType cue_type{SarCueType::none};
    Vec3 sensor_wcs_m{};
    Vec3 cue_wcs_m{};
    Vec3 angle_cue_direction_wcs{}; // 中文：angle cue 时为 PCS x 按 slant range 转到 WCS 的向量。
    Vec3 los_ned_m{};
    double slant_range_m{};
    double image_width_m{};
    double image_height_m{};
    double depression_angle_rad{};
};

enum class SarImageFovStatus
{
    ok,
    unchanged_no_cue,
    unchanged_no_image_size,
    invalid_cue,
    degenerate_range,
    invalid_input,
    non_finite_output
};

struct SarImageFovOutput
{
    Vec3 image_center_wcs_m{};
    double azimuth_min_rad{};
    double azimuth_max_rad{};
    double elevation_min_rad{};
    double elevation_max_rad{};
    SarImageFovStatus status{SarImageFovStatus::ok};
};
```

## 4. 核心接口

```cpp
using ImageCenterAdjuster = Vec3 (*)(Vec3 sensor_wcs_m, Vec3 cue_wcs_m);

SarImageFovOutput
compute_sar_image_field_of_view(const SarImageFovInput& input,
                                ImageCenterAdjuster adjust_image_center);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `compute_sar_image_field_of_view` | 输入有限；必要时提供中心调整器 | 返回 FOV，不直接修改天线 | 无 | $O(1)$ 加调整器成本 |

## 5. 状态生命周期

算法自身无状态。AFSIM 适配层把 `image_center_wcs_m` 写入 `mImageCenterWCS`，把 FOV 输出写入 `WsfEM_Antenna`。未 cue 或未配置宽高时应保持调用者原状态不变。

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| `cue_type == none` | 入口 | `unchanged_no_cue` | 保留旧 FOV |
| 宽高任一 `<=0` | 入口 | `unchanged_no_image_size` | 补完整图像尺寸 |
| cue 类型未知 | 入口 | `invalid_cue` | 修正 cue |
| slant range 退化 | 方位角计算 | 仍给源码兼容角并标状态 | 判断是否允许 |
| NaN/Inf | 入口/出口 | `invalid_input` 或 `non_finite_output` | 失败处理 |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `GetCueType()` | `cue_type` | enum 映射 | none | `afsim-2_9/swdev/src/core/wsf_mil/source/sensor/WsfSAR_Sensor.cpp:2630-2649` |
| `GetLocationWCS` | `sensor_wcs_m` | 直接复制 | none | `WsfSAR_Sensor.cpp:2638-2640` |
| `GetCuedLocationWCS` | `cue_wcs_m` | 直接复制 | none | `WsfSAR_Sensor.cpp:2644-2647` |
| `ConvertPCSVectorToWCS` | `angle_cue_direction_wcs` | 适配层转换 | 传感器姿态外置 | `WsfSAR_Sensor.cpp:2650-2653` |
| `ComputeImageCenter` | `adjust_image_center` | 回调 | terrain 细节外置 | `WsfSAR_Sensor.cpp:2656-2658` |
| `SetAzimuthFieldOfView` / `SetElevationFieldOfView` | output FOV | 适配层写回 | none | `WsfSAR_Sensor.cpp:2665-2686` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `WsfSensor` | cue 与坐标转换 | 替换 | 显式 cue + 方向向量 | cue 语义 |
| `WsfPlatform` | WCS/NED 转换 | 替换 | 适配层给 `los_ned_m` | 坐标轴方向 |
| `WsfEM_Antenna` | 状态写回 | 移除 | 返回 FOV | 生命周期 |
| terrain interface | 遮挡修正 | 替换 | `ImageCenterAdjuster` | 可重复性 |

## 9. 最小调用示例

```cpp
SarImageFovInput input{};
input.cue_type = SarCueType::location;
input.sensor_wcs_m = {0.0, 0.0, 0.0};
input.cue_wcs_m = {8660.254037844386, 0.0, 5000.0};
input.los_ned_m = {8660.254037844386, 0.0, 5000.0};
input.slant_range_m = 10000.0;
input.image_width_m = 2000.0;
input.image_height_m = 1000.0;
input.depression_angle_rad = std::numbers::pi / 6.0;

// 中文：无地形修正时直接返回 cue 作为图像中心。
auto identity_adjuster = [](Vec3, Vec3 cue) { return cue; };
auto output = compute_sar_image_field_of_view(input, identity_adjuster);
```

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | 第 9 节样例 | `az_max=0.09966865249116202`、`el_max=0.023957812945459123`、`el_min=-0.026125582775832656` | `1e-12` | 超差 |
| 未 cue | `cue_type=none` | 状态 `unchanged_no_cue` | 不写输出 | 状态错误 |
| 退化 | `slant=0` 且宽高正 | 方位半角不超过 $\pi/2$ | 限幅 | 非有限 |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| SAR-FOV-001 | `ComputeImageCenter` 是否应独立提取为地形遮挡中心搜索算法 | FOV 黄金结果依赖 terrain | 后续批次审查 | no |
