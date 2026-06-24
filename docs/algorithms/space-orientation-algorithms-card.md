# 算法卡片 -- 航天器空间姿态定向模型

> **状态**：draft
> **日期**：2026-06-24
> **索引证据**：function-index.jsonl (wsf_space, wsf::space::Orientation, wsf::space::OrientationNadirECI_Velocity, wsf::space::OrientationSolarNadir, wsf::space::OrientationNadirSolar, wsf::space::OrientationNadirECEF_Velocity, wsf::space::OrientationECI_VelocityNadir, wsf::space::OrientationECI_VelocitySolar, wsf::space::OrientationEntitySolar, wsf::space::OrientationEntityNadir, wsf::space::OrientationEntityOrbitPlane, wsf::space::OrientationPointOrbitPlane, wsf::space::OrientationNone)
> **关联文档**：space-integrating-propagator-card.md, space-de-ephemeris-card.md
> **关联源文件**：`WsfSpaceOrientation.hpp`、`WsfSpaceOrientation.cpp`

### 基础资料

- **算法名称**：Spacecraft Attitude Orientation Algorithm Suite（航天器空间姿态定向算法集）
- **算法所属模块**：wsf_space
- **算法功能**：提供航天器在轨飞行期间 11 种姿态定向模式的计算。所有模式基于统一的几何框架：给定指向轴方向矢量和约束轴方向矢量，通过叉积构造正交右手系的方向余弦矩阵（DCM），再由体轴系矢量提取 IEEE 1278.1-1995 DIS 标准的欧拉角（偏航角 Psi、俯仰角 Theta、滚动角 Phi）。指向源包括天底（Nadir）、太阳（Solar）、ECI 速度、ECEF 速度、目标实体（Entity/驻留空间目标 RSO）和地理点（GeoPoint）；约束源包括天底、太阳、ECI 速度、ECEF 速度和轨道面。

### 算法流程

整个姿态定向算法的总体流程如下：

```mermaid
flowchart TD
    A["开始: 某姿态模式的 Calculate()"] --> B["1. 获取指向轴矢量\n(根据模式调用 Nadir/Solar/VelocityECI/\nVelocityECEF/TargetVector)"]
    B --> C["2. 获取约束轴矢量\n(根据模式调用 Nadir/Solar/VelocityECI/\nVelocityECEF/OrbitPlaneConstraint)"]
    C --> D{"3. 是否实体/地理点指向模式?"}
    D -->|是| E["3.1. 调用 TargetVector()\n获取指向目标单位矢量"]
    D -->|否| F["3.2. 直接使用\nNadir/Solar/VelocityECI 等矢量"]
    E --> G["4. CalculateAligned(aPoint, aConstraint, psi, theta, phi)"]
    F --> G
    G --> H{"5. mDefaultX_Aligned?"}
    H -->|true (X轴指向)| I["5.1. CalculateX_Aligned:\nX=指向矢量, Z=约束矢量\n构建方向余弦"]
    H -->|false (Z轴指向)| J["5.2. CalculateZ_Aligned:\nZ=指向矢量, X=约束矢量\n构建方向余弦"]
    I --> K["6. CalculatePCS_DirectionCosines:\nX=normalize(指向) → Y=normalize(Z_const × X) → Z=X × Y"]
    J --> K
    K --> L["7. CalculateFromBodyFrame:\ntheta=-asin(xE[2])\npsi=atan2(xE[1],xE[0])\nphi=atan2(yE[2],zE[2])"]
    L --> M["输出: aPsi, aTheta, aPhi"]
    M --> N["结束"]
```

其中，第一步为根据定向模式类型获取指向轴参考矢量（在ECI坐标系中）；第二步为获取约束轴参考矢量（同样在ECI坐标系中）；第三步判断是否为需要查询目标的模式（Entity/GeoPoint），如果是则需要通过仿真框架查找目标平台或地理点的位置并计算指向矢量；第四步调用 `CalculateAligned` 核心调度函数；第五步根据 `mDefaultX_Aligned` 标志选择 X 轴对齐或 Z 轴对齐分支；第六步为核心几何运算 `CalculatePCS_DirectionCosines`，通过归一化和叉积构建正交右手坐标系；第七步从构建的体轴系方向余弦矩阵中提取 IEEE 1278.1-1995 DIS 标准的欧拉角。

### 算法变量和常量映射表

#### 1. 输入变量(input)

| # | 中文名称(Name) | 代码标识(Symbol) | 数学符号(Math-sym) | 数据类型(Type) | 含义(Meaning) | 单位(Units) | 所属函数(Method) |
|---|---|---|---|---|---|---|---|
| 1 | 偏航角输出引用 | `aPsi` | $\psi$ | `double&` | 输出参数，ECI参考偏航角 | rad | `wsf::space::OrientationNadirECI_Velocity::Calculate`, `wsf::space::OrientationSolarNadir::Calculate`, `wsf::space::OrientationNadirSolar::Calculate`, `wsf::space::OrientationNadirECEF_Velocity::Calculate`, `wsf::space::OrientationECI_VelocityNadir::Calculate`, `wsf::space::OrientationECI_VelocitySolar::Calculate`, `wsf::space::OrientationEntitySolar::Calculate`, `wsf::space::OrientationEntityNadir::Calculate`, `wsf::space::OrientationEntityOrbitPlane::Calculate`, `wsf::space::OrientationPointOrbitPlane::Calculate` |
| 2 | 俯仰角输出引用 | `aTheta` | $\theta$ | `double&` | 输出参数，ECI参考俯仰角 | rad | 同上 |
| 3 | 滚动角输出引用 | `aPhi` | $\phi$ | `double&` | 输出参数，ECI参考滚动角 | rad | 同上 |
| 4 | 指向轴方向矢量 | `aPointingAxisOrientationECI` | $\mathbf{v}_{\text{point}}$ | `const UtVec3d&` | PCS主轴指向方向，ECI坐标 | 无量纲单位矢量 | `wsf::space::Orientation::CalculateAligned` |
| 5 | 约束轴方向矢量 | `aConstraintAxisOrientationECI` | $\mathbf{v}_{\text{constraint}}$ | `const UtVec3d&` | 约束轴方向，ECI坐标 | 无量纲单位矢量 | `wsf::space::Orientation::CalculateAligned` |
| 6 | X轴指向矢量(ECI) | `aX_AxisOrientationECI` | $\mathbf{x}_{\text{ECI}}$ | `const UtVec3d&` | X轴在ECI中的指向矢量 | 无量纲（内部归一化） | `wsf::space::Orientation::CalculateX_Aligned`, `wsf::space::Orientation::CalculatePCS_DirectionCosines`, `wsf::space::Orientation::CalculateGeneral` |
| 7 | Z轴约束矢量(ECI) | `aZ_AxisConstraintECI` | $\mathbf{z}_{\text{ECI}}$ | `const UtVec3d&` | Z轴在ECI中的约束矢量 | 无量纲（内部归一化） | `wsf::space::Orientation::CalculateX_Aligned`, `wsf::space::Orientation::CalculatePCS_DirectionCosines`, `wsf::space::Orientation::CalculateGeneral` |
| 8 | Z轴指向矢量(ECI) | `aZ_AxisOrientationECI` | $\mathbf{z}_{\text{ECI}}$ | `const UtVec3d&` | Z轴在ECI中的指向矢量 | 无量纲（内部归一化） | `wsf::space::Orientation::CalculateZ_Aligned` |
| 9 | X轴约束矢量(ECI) | `aX_AxisConstraintECI` | $\mathbf{x}_{\text{ECI}}$ | `const UtVec3d&` | X轴在ECI中的约束矢量 | 无量纲（内部归一化） | `wsf::space::Orientation::CalculateZ_Aligned` |
| 10 | ECS偏航角 | `aYawECS` | $\psi_{\text{ECS}}$ | `double` | 铰接部件PCS相对ECS的偏航角 | rad | `wsf::space::Orientation::CalculateGeneral` |
| 11 | ECS俯仰角 | `aPitchECS` | $\theta_{\text{ECS}}$ | `double` | 铰接部件PCS相对ECS的俯仰角 | rad | `wsf::space::Orientation::CalculateGeneral` |
| 12 | ECS滚动角 | `aRollECS` | $\phi_{\text{ECS}}$ | `double` | 铰接部件PCS相对ECS的滚动角 | rad | `wsf::space::Orientation::CalculateGeneral` |
| 13 | 姿态类型名称 | `aOrientation` | - | `const std::string&` | 工厂方法中指定要创建的姿态类型字符串 | 字符串 | `wsf::space::Orientation::Factory` |

#### 2. 输出变量(output)

| # | 中文名称(Name) | 代码标识(Symbol) | 数学符号(Math-sym) | 数据类型(Type) | 含义(Meaning) | 单位(Units) | 所属函数(Method) |
|---|---|---|---|---|---|---|---|
| 1 | 计算后的偏航角 | `aPsi` | $\psi$ | `double&` | ECI参考偏航角输出 | rad | 同输入变量表第1行所列全部Calculate函数 |
| 2 | 计算后的俯仰角 | `aTheta` | $\theta$ | `double&` | ECI参考俯仰角输出 | rad | 同上 |
| 3 | 计算后的滚动角 | `aPhi` | $\phi$ | `double&` | ECI参考滚动角输出 | rad | 同上 |
| 4 | 计算成功标志 | `retval` (bool) | - | `bool` | true表示定向计算成功，false表示失败（例如目标不存在） | 无 | 同上 |
| 5 | X方向余弦 | `aX_DC` | $\mathbf{\hat{x}}_{P}$ | `UtVec3d&` | PCS X轴在ECI中的方向余弦 | 无量纲 | `wsf::space::Orientation::CalculatePCS_DirectionCosines` |
| 6 | Y方向余弦 | `aY_DC` | $\mathbf{\hat{y}}_{P}$ | `UtVec3d&` | PCS Y轴在ECI中的方向余弦 | 无量纲 | 同上 |
| 7 | Z方向余弦 | `aZ_DC` | $\mathbf{\hat{z}}_{P}$ | `UtVec3d&` | PCS Z轴在ECI中的方向余弦 | 无量纲 | 同上 |
| 8 | 工厂返回的姿态对象 | `orientationPtr` | - | `std::unique_ptr<Orientation>` | 创建的姿态定向对象，若类型不识别则为nullptr | 无 | `wsf::space::Orientation::Factory` |

#### 3. 状态变量(state variables)

| # | 中文名称(Name) | 代码标识(Symbol) | 数学符号(Math-sym) | 数据类型(Type) | 含义(Meaning) | 单位(Units) | 所属函数(Method) | 初始值(Initial-val) | 更新时机(Update-tim) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 默认X轴对齐标志 | `mDefaultX_Aligned` | - | `bool` | 为true时X轴为指向轴(约束Z轴)；为false时Z轴为指向轴(约束X轴) | 无 | `wsf::space::Orientation::CalculateAligned` | 由子类构造函数决定（X-aligned子类为true，Z-aligned子类为false） | 构造时设置，运行时可通过`SetDefaultX_Aligned`修改 |
| 2 | 姿态控制器指针 | `mControllerPtr` | - | `const WsfAttitudeController*` | 指向所属平台的姿态控制器，提供访问平台状态的接口 | 无 | `wsf::space::Orientation::Nadir`, `wsf::space::Orientation::Solar`, `wsf::space::Orientation::VelocityECI`, `wsf::space::Orientation::VelocityECEF`, `wsf::space::Orientation::OrbitPlaneConstraint`, `wsf::space::OrientationEntity::TargetVector`, `wsf::space::OrientationGeoPoint::TargetVector` | `nullptr` | 初始化阶段由 `SetAttitudeController` 设置 |
| 3 | 错误消息已发出标志 | `mIssueErrorMessage` | - | `mutable bool` | 为true时允许输出警告日志，设为false后仅首次错误输出警告 | 无 | `wsf::space::Orientation::HandleException` | `true` | 首次遇到异常时置为false（仅警告一次） |
| 4 | 目标实体名称 | `mEntityName` | - | `std::string` | 姿态指向的目标平台（RSO）名称 | 无 | `wsf::space::OrientationEntity::TargetVector` | 空字符串 | 脚本输入处理（`ProcessInput`）或通过 `SetEntityName` 设置 |
| 5 | 目标航迹标识 | `mTrackId` | - | `WsfTrackId` | 姿态指向的航迹ID（替代实体名指向） | 无 | `wsf::space::OrientationEntity::TargetVector` | 默认构造值 | 通过 `SetTrackId` 设置 |
| 6 | 定向至航迹标志 | `mOrientToTrack` | - | `bool` | 为true时使用航迹位置而非实体位置作为指向参考 | 无 | `wsf::space::OrientationEntity::TargetVector` | `false` | `SetTrackId`调用时置true，`SetEntityName`调用时置false |
| 7 | 地理点名称 | `mGeoPointName` | - | `std::string` | 姿态指向的地理点组件名称 | 无 | `wsf::space::OrientationGeoPoint::TargetVector` | 空字符串 | 脚本输入处理（`ProcessInput`）或通过 `SetGeoPointName` 设置 |
| 8 | 地理点对象指针 | `mGeoPointPtr` | - | `mutable std::unique_ptr<WsfGeoPoint>` | 地理点对象的缓存副本，惰性初始化 | 无 | `wsf::space::OrientationGeoPoint::TargetVector` | `nullptr` | 首次调用 `TargetVector` 时从平台查找并克隆，或通过 `SetGeoPoint` 预设置 |

#### 4. 常量(constant)

| # | 中文名称(Name) | 代码标识(Symbol) | 数学符号(Math-sym) | 数据类型(Type) | 含义(Meaning) | 单位(Units) | 所属函数(Method) |
|---|---|---|---|---|---|---|---|
| 1 | 无姿态模式类型名 | `OrientationNone::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"none"`，标识无姿态定向模式 | 无 | `wsf::space::OrientationNone::GetTypeName` |
| 2 | 天底指向/ECI速度约束类型名 | `OrientationNadirECI_Velocity::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"nadir_with_eci_velocity_constraint"` | 无 | `wsf::space::OrientationNadirECI_Velocity::GetTypeName` |
| 3 | 太阳指向/天底约束类型名 | `OrientationSolarNadir::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"solar_with_nadir_constraint"` | 无 | `wsf::space::OrientationSolarNadir::GetTypeName` |
| 4 | 天底指向/太阳约束类型名 | `OrientationNadirSolar::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"nadir_with_solar_constraint"` | 无 | `wsf::space::OrientationNadirSolar::GetTypeName` |
| 5 | 天底指向/ECEF速度约束类型名 | `OrientationNadirECEF_Velocity::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"nadir_with_ecef_velocity_constraint"` | 无 | `wsf::space::OrientationNadirECEF_Velocity::GetTypeName` |
| 6 | ECI速度指向/天底约束类型名 | `OrientationECI_VelocityNadir::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"eci_velocity_with_nadir_constraint"` | 无 | `wsf::space::OrientationECI_VelocityNadir::GetTypeName` |
| 7 | ECI速度指向/太阳约束类型名 | `OrientationECI_VelocitySolar::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"eci_velocity_with_solar_constraint"` | 无 | `wsf::space::OrientationECI_VelocitySolar::GetTypeName` |
| 8 | 实体指向/太阳约束类型名 | `OrientationEntitySolar::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"entity_with_solar_constraint"` | 无 | `wsf::space::OrientationEntitySolar::GetTypeName` |
| 9 | 实体指向/天底约束类型名 | `OrientationEntityNadir::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"entity_with_nadir_constraint"` | 无 | `wsf::space::OrientationEntityNadir::GetTypeName` |
| 10 | 实体指向/轨道面约束类型名 | `OrientationEntityOrbitPlane::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"entity_with_orbit_plane_constraint"` | 无 | `wsf::space::OrientationEntityOrbitPlane::GetTypeName` |
| 11 | 地理点指向/轨道面约束类型名 | `OrientationPointOrbitPlane::GetTypeName()` | - | `static constexpr const char*` | 返回字符串 `"point_with_orbit_plane_constraint"` | 无 | `wsf::space::OrientationPointOrbitPlane::GetTypeName` |

### 关键数学公式

1. **PCS方向余弦构建（正交右手系构造）**：
   该公式直接对应 `CalculatePCS_DirectionCosines` 的数学逻辑。给定ECI空间中PCS X轴的期望指向 $\mathbf{x}_{\text{ECI}}$ 和Z轴约束方向 $\mathbf{z}_{\text{constraint}}$，构建正交归一化的右手坐标系：

   $$\mathbf{\hat{x}}_P = \frac{\mathbf{x}_{\text{ECI}}}{|\mathbf{x}_{\text{ECI}}|}$$

   $$\mathbf{\hat{y}}_P = \frac{\mathbf{\hat{z}}_{\text{constraint}} \times \mathbf{\hat{x}}_P}{|\mathbf{\hat{z}}_{\text{constraint}} \times \mathbf{\hat{x}}_P|}$$

   $$\mathbf{\hat{z}}_P = \mathbf{\hat{x}}_P \times \mathbf{\hat{y}}_P$$

   其中：
   - $\mathbf{\hat{x}}_P$ 为PCS X轴在ECI中的单位方向余弦矢量，指向期望的指向方向。
   - $\mathbf{\hat{y}}_P$ 由约束轴与X轴的叉积得到，确保Y轴同时垂直于X轴和约束轴（即Y轴的方位使得Z轴位于X轴和约束轴所在平面内）。
   - $\mathbf{\hat{z}}_P$ 由X轴与Y轴的叉积得到，保证右手系正交性。注意最终 $\mathbf{\hat{z}}_P$ 位于 $\mathbf{\hat{x}}_P$ 和原始 $\mathbf{z}_{\text{constraint}}$ 所在平面内，但不一定与 $\mathbf{z}_{\text{constraint}}$ 同向。

2. **体轴系方向余弦到欧拉角的转换（IEEE 1278.1-1995 DIS 约定）**：
   该公式直接对应 `CalculateFromBodyFrame` 的数学逻辑。给定正交右手系体轴矢量 $\mathbf{x}_E, \mathbf{y}_E, \mathbf{z}_E$（均在ECI中表达），按DIS标准提取3-2-1旋转序列（Z-Y-X，即偏航-俯仰-滚动）的欧拉角：

   $$\theta = -\arcsin(x_E[2])$$

   $$\psi = \text{atan2}(x_E[1], x_E[0])$$

   $$\phi = \text{atan2}(y_E[2], z_E[2])$$

   其中：
   - $\theta$（theta/俯仰角）由X轴矢量的Z分量的反正弦取负得到。$x_E[2] = \sin(-\theta) = -\sin\theta$。
   - $\psi$（psi/偏航角）由X轴矢量在XY平面投影的atan2得到。
   - $\phi$（phi/滚动角）由Y轴矢量Z分量与Z轴矢量Z分量的atan2得到，对应绕X轴的旋转后的姿态。
   - atan2(y, x) 返回四象限反正切值，取值范围 $(-\pi, \pi]$。

3. **ECEF速度到ECI坐标系的转换**：
   该公式对应 `VelocityECEF` 的数学逻辑。将地固系（WCS）速度通过地球自转角旋转到惯性系（ECI）：

   $$v_{\text{ECI},x} = \cos\phi \cdot v_{\text{ECEF},x} - \sin\phi \cdot v_{\text{ECEF},y}$$

   $$v_{\text{ECI},y} = \sin\phi \cdot v_{\text{ECEF},x} + \cos\phi \cdot v_{\text{ECEF},y}$$

   $$v_{\text{ECI},z} = v_{\text{ECEF},z}$$

   其中：
   - $\phi$ 为 `earthAngle`，当前时间的地球自转角（绕Z轴正向的旋转角）。
   - 此转换仅进行旋转（不添加科里奥利力或向心加速度项），将WCS中测量的速度矢量表达在ECI中。
   - $v_{\text{ECEF}}$ 由 `mControllerPtr->GetMover()->GetPlatform()->GetVelocityWCS()` 获取。

4. **轨道面约束矢量计算**：
   该公式对应 `OrbitPlaneConstraint` 的数学逻辑。计算位于轨道平面内且垂直于指定对齐矢量的约束方向：

   $$\mathbf{n} = \mathbf{r} \times \mathbf{v}$$

   $$\mathbf{c} = \begin{cases} \mathbf{n} \times \mathbf{a}_{\text{align}} & \text{若 } |\mathbf{n} \times \mathbf{a}_{\text{align}}|^2 \neq 0 \\ \mathbf{v} & \text{若 } |\mathbf{n} \times \mathbf{a}_{\text{align}}|^2 = 0 \text{ (退化情况)} \end{cases}$$

   $$\mathbf{\hat{c}} = \frac{\mathbf{c}}{|\mathbf{c}|}$$

   其中：
   - $\mathbf{r}$ 为平台在ECI中的位置矢量。
   - $\mathbf{v}$ 为平台在ECI中的速度矢量。
   - $\mathbf{n} = \mathbf{r} \times \mathbf{v}$ 为轨道面法向矢量（轨道角动量方向）。
   - $\mathbf{a}_{\text{align}}$ 为外部指定的对齐矢量（如指向目标的方向）。
   - $\mathbf{\hat{c}}$ 为输出约束矢量，位于轨道面内且垂直于 $\mathbf{a}_{\text{align}}$。
   - 退化情况：当 $\mathbf{a}_{\text{align}}$ 平行于轨道面法向时，$\mathbf{n} \times \mathbf{a}_{\text{align}} = \mathbf{0}$，此时直接用速度矢量作为约束方向。

5. **通用铰接部件定向模型**：
   该公式对应 `CalculateGeneral` 的数学逻辑。处理带有铰接部件（如可转动天线、传感器）的航天器姿态。首先通过部件在ECS中的偏航/俯仰/滚动角构建ECS到PCS的旋转矩阵，再与PCS目标定向矩阵相乘得到ECS到ECI的总体变换矩阵：

   $$\mathbf{T}_{\text{ECS}\rightarrow\text{PCS}} = \text{ComputeRotationalTransform}(\psi_{\text{ECS}}, \theta_{\text{ECS}}, \phi_{\text{ECS}})$$

   $$\mathbf{T}_{\text{PCS}\rightarrow\text{ECI}} = \begin{bmatrix}
   \mathbf{\hat{x}}_P[0] & \mathbf{\hat{y}}_P[0] & \mathbf{\hat{z}}_P[0] \\
   \mathbf{\hat{x}}_P[1] & \mathbf{\hat{y}}_P[1] & \mathbf{\hat{z}}_P[1] \\
   \mathbf{\hat{x}}_P[2] & \mathbf{\hat{y}}_P[2] & \mathbf{\hat{z}}_P[2]
   \end{bmatrix}$$

   $$\mathbf{T}_{\text{ECS}\rightarrow\text{ECI}} = \mathbf{T}_{\text{PCS}\rightarrow\text{ECI}} \times \mathbf{T}_{\text{ECS}\rightarrow\text{PCS}}$$

   其中 $\mathbf{T}_{\text{PCS}\rightarrow\text{ECI}}$ 由 `CalculatePCS_DirectionCosines` 从目标PCS指向和约束矢量构建。最终从 $\mathbf{T}_{\text{ECS}\rightarrow\text{ECI}}$ 的各列提取体轴矢量，通过 `CalculateFromBodyFrame` 提取欧拉角。

### 算法伪代码

```
// ============================================================
// 航天器姿态定向算法 —— 核心计算链
// 输入：姿态控制器指针 mControllerPtr（提供平台位置、速度和时间访问）
// 输出：欧拉角 (psi, theta, phi)，单位 rad
// 各子类的 Calculate() 为入口点，调用链如下
// ============================================================

// ---------- 辅助矢量计算（protected 方法） ----------

function Nadir(): UtVec3d                      // 计算天底矢量 (ECI)
    nadir = platform.GetLocationECI()          // 平台到地心的位置矢量 (m)
    nadir.Multiply(-1.0)                       // 取反得地心到天底方向（指向地心）
    return nadir                               // 返回天底单位方向 (ECI)

function Solar(): UtVec3d                      // 计算太阳方向矢量 (ECI)
    solarVec = UtSun::GetSunLocationECI(currentTime) // 从星历获取太阳ECI位置
    return solarVec                             // 返回太阳方向 (ECI)

function VelocityECI(): UtVec3d                // 获取平台 ECI 速度矢量
    velocityECI = platform.GetVelocityECI()    // 直接获取平台ECI速度 (m/s)
    return velocityECI                          // 返回ECI速度矢量

function VelocityECEF(): UtVec3d               // 获取 WCS 速度并转为 ECI 表达
    velocityECEF = platform.GetVelocityWCS()   // 获取平台地固系速度 (m/s)
    earthAngle = propagator.GetCurrentTime().GetEarthAngle() // 当前地球自转角 (rad)
    sinPhi = sin(earthAngle); cosPhi = cos(earthAngle)       // 旋转矩阵元素
    // 绕Z轴旋转 WCS→ECI（仅旋转，不含科里奥利/向心加速度）
    velocityECI[0] = cosPhi * velocityECEF[0] - sinPhi * velocityECEF[1]
    velocityECI[1] = sinPhi * velocityECEF[0] + cosPhi * velocityECEF[1]
    velocityECI[2] = velocityECEF[2]
    return velocityECI                          // 返回ECI表达的地固系速度

function OrbitPlaneConstraint(alignVector): UtVec3d  // 轨道面内约束矢量
    r = platform.GetLocationECI()              // 平台ECI位置矢量 (m)
    v = platform.GetVelocityECI()              // 平台ECI速度矢量 (m/s)
    r_x_v = CrossProduct(r, v)                 // 轨道面法向 = r × v
    constraint = CrossProduct(r_x_v, alignVector) // 轨道面内且垂直于alignVector
    if constraint.MagnitudeSquared() == 0.0:
        constraint = v                         // 退化处理：用速度矢量替代
    constraint.Normalize()                     // 归一化为单位矢量
    return constraint

// ---------- 核心几何运算（public static 方法） ----------

function CalculatePCS_DirectionCosines(xAxisECI, zConstraintECI, out xDC, out yDC, out zDC):
    // 构建PCS在ECI中的正交右手方向余弦
    xDC = normalize(xAxisECI)                  // X轴：指向期望方向
    zDC = normalize(zConstraintECI)            // Z轴约束：归一化
    yDC = CrossProduct(zDC, xDC)               // Y轴：Z_const × X = 垂直于两者
    yDC.Normalize()                             // 归一化Y轴
    zDC = CrossProduct(xDC, yDC)               // Z轴：X × Y = 严格正交右手系
    // 输出: xDC, yDC, zDC 构成ECI中PCS的正交方向余弦

function CalculateFromBodyFrame(xE, yE, zE, out psi, out theta, out phi):
    // 从体轴方向余弦提取IEEE 1278.1-1995 DIS标准欧拉角
    theta = -asin(xE[2])                       // 俯仰角：X轴Z分量的反正弦
    psi = atan2(xE[1], xE[0])                  // 偏航角：X轴在XY平面的方位角
    phi = atan2(yE[2], zE[2])                  // 滚动角：由Y轴Z分量和Z轴Z分量确定

function CalculateX_Aligned(xAxisECI, zConstraintECI, out psi, out theta, out phi):
    // X轴对齐模式：X轴指向目标，Z轴由约束矢量确定
    CalculatePCS_DirectionCosines(xAxisECI, zConstraintECI, xP, yP, zP)
    CalculateFromBodyFrame(xP, yP, zP, psi, theta, phi)

function CalculateZ_Aligned(zAxisECI, xConstraintECI, out psi, out theta, out phi):
    // Z轴对齐模式：Z轴指向目标，X轴由约束矢量确定
    CalculatePCS_DirectionCosines(zAxisECI, xConstraintECI, xP, yP, zP)
    // 交换X和Z轴方向，并翻转Y轴以适应Z轴对齐
    zPCopy = zP
    zP = xP                                     // 原来计算的Z→新的Z（原指向方向先作为X构建）
    xP = zPCopy                                 // 原来计算的X→新的X
    yP = -yP                                    // Y轴取反保持右手系
    CalculateFromBodyFrame(xP, yP, zP, psi, theta, phi)

function CalculateAligned(pointAxisECI, constraintAxisECI, out psi, out theta, out phi):
    // 调度函数：根据mDefaultX_Aligned标志选择X轴或Z轴对齐
    if mDefaultX_Aligned == true:
        CalculateX_Aligned(pointAxisECI, constraintAxisECI, psi, theta, phi)
    else:
        CalculateZ_Aligned(pointAxisECI, constraintAxisECI, psi, theta, phi)

function CalculateGeneral(yawECS, pitchECS, rollECS, xAxisECI, zConstraintECI,
                          out psi, out theta, out phi):
    // 通用铰接部件定向：ECS→PCS→ECI复合变换
    Tecs_pcs = ComputeRotationalTransform(yawECS, pitchECS, rollECS) // ECS到PCS旋转矩阵
    CalculatePCS_DirectionCosines(xAxisECI, zConstraintECI, xP, yP, zP)
    Tpcs_eci = [[xP[0], yP[0], zP[0]],          // PCS到ECI方向余弦矩阵
                [xP[1], yP[1], zP[1]],
                [xP[2], yP[2], zP[2]]]
    Tecs_eci = Multiply(Tpcs_eci, Tecs_pcs)      // ECS到ECI = PCS_to_ECI × ECS_to_PCS
    // 从组合矩阵提取列向量作为体轴
    for i = 0 to 2:
        xP[i] = Tecs_eci[i][0]; yP[i] = Tecs_eci[i][1]; zP[i] = Tecs_eci[i][2]
    CalculateFromBodyFrame(xP, yP, zP, psi, theta, phi)

// ---------- 各定向模式的 Calculate() 入口 ----------

function OrientationNone::Calculate(psi, theta, phi):  // 无定向模式
    return false                                 // 不计算任何定向，直接返回失败

function OrientationNadirECI_Velocity::Calculate(psi, theta, phi): // 天底指向/ECI速度约束
    CalculateAligned(Nadir(), VelocityECI(), psi, theta, phi) // Z→天底, X(ECI速度)
    return true

function OrientationNadirECEF_Velocity::Calculate(psi, theta, phi): // 天底指向/ECEF速度约束
    CalculateAligned(Nadir(), VelocityECEF(), psi, theta, phi) // Z→天底, X(ECEF速度)
    return true

function OrientationSolarNadir::Calculate(psi, theta, phi):  // 太阳指向/天底约束
    CalculateAligned(Solar(), Nadir(), psi, theta, phi) // Z→太阳, X(天底)
    return true

function OrientationNadirSolar::Calculate(psi, theta, phi):  // 天底指向/太阳约束
    CalculateAligned(Nadir(), Solar(), psi, theta, phi) // Z→天底, X(太阳)
    return true

function OrientationECI_VelocityNadir::Calculate(psi, theta, phi): // ECI速度指向/天底约束
    CalculateAligned(VelocityECI(), Nadir(), psi, theta, phi) // X→ECI速度, Z(天底)
    return true

function OrientationECI_VelocitySolar::Calculate(psi, theta, phi): // ECI速度指向/太阳约束
    CalculateAligned(VelocityECI(), Solar(), psi, theta, phi) // X→ECI速度, Z(太阳)
    return true

function OrientationEntitySolar::Calculate(psi, theta, phi):  // 实体指向/太阳约束
    try:
        CalculateAligned(TargetVector(), Solar(), psi, theta, phi) // X→目标, Z(太阳)
        return true
    catch UtException:
        HandleException(exception)               // 警告一次并记录
        return false

function OrientationEntityNadir::Calculate(psi, theta, phi):  // 实体指向/天底约束
    try:
        CalculateAligned(TargetVector(), Nadir(), psi, theta, phi) // X→目标, Z(天底)
        return true
    catch UtException:
        HandleException(exception)
        return false

function OrientationEntityOrbitPlane::Calculate(psi, theta, phi): // 实体指向/轨道面约束
    try:
        targetVec = TargetVector()
    catch UtException:
        HandleException(exception)
        return false
    CalculateAligned(targetVec, OrbitPlaneConstraint(targetVec), psi, theta, phi)
    // X→目标, Z(轨道面内约束)
    return true

function OrientationPointOrbitPlane::Calculate(psi, theta, phi): // 地理点指向/轨道面约束
    try:
        targetVec = TargetVector()
    catch UtException:
        HandleException(exception)
        return false
    CalculateAligned(targetVec, OrbitPlaneConstraint(targetVec), psi, theta, phi)
    // X→地理点, Z(轨道面内约束)
    return true

// ---------- 辅助：实体目标矢量 ----------
function OrientationEntity::TargetVector(): UtVec3d  // 获取实体目标方向 (ECI)
    platformPtr = mControllerPtr.GetMover().GetPlatform()
    if mOrientToTrack == true:                   // 使用航迹指向模式
        trackPtr = platformPtr.GetMasterTrackList().FindTrack(mTrackId)
        if trackPtr == nullptr: throw TrackNotFoundException
        if not trackPtr.LocationValid(): throw TrackLocationInvalidException
        trackPtr.GetExtrapolatedLocationWCS(simTime, rsoLocWCS)
        platformPtr.ConvertWCSToECI(rsoLocWCS, rsoLocECI) // WCS→ECI转换
    else:                                        // 使用实体名指向模式
        rsoPtr = simulation.GetPlatformByName(mEntityName)
        if rsoPtr == nullptr: throw EntityNotFoundException
        rsoPtr.GetLocationECI(rsoLocECI)
    myLocECI = platformPtr.GetLocationECI()
    targetVec = (rsoLocECI - myLocECI).Normalize() // 单位指向矢量 (ECI)
    return targetVec

function OrientationGeoPoint::TargetVector(): UtVec3d  // 获取地理点目标方向 (ECI)
    platformPtr = mControllerPtr.GetMover().GetPlatform()
    if mGeoPointPtr == nullptr:                  // 惰性初始化
        geoPointPtr = platformPtr.GetComponent<WsfGeoPoint>(mGeoPointName)
        if geoPointPtr == nullptr: throw GeoPointNotFoundException
        mGeoPointPtr = Clone(geoPointPtr)
    mGeoPointPtr.GetLocationWCS(targetLocWCS)
    platformPtr.ConvertWCSToECI(targetLocWCS, targetLocECI) // WCS→ECI转换
    myLocECI = platformPtr.GetLocationECI()
    targetVec = (targetLocECI - myLocECI).Normalize() // 单位指向矢量 (ECI)
    return targetVec
```

### 源码使用说明

#### 入口和调用链

外部调用入口：平台的姿态控制器（`WsfInstantAttitudeController::UpdateOrientation` 或类似的 `WsfAttitudeController` 子类）在每个仿真帧调用当前定向模式的 `Calculate(psi, theta, phi)`。

```
外部: WsfInstantAttitudeController::UpdateOrientation()
  → Orientation 子类::Calculate(psi, theta, phi)   // 入口1：各模式计算定向
      → CalculateAligned(point, constraint, psi, theta, phi)  // 调度X/Z轴对齐
          → [if mDefaultX_Aligned] CalculateX_Aligned(xAxis, zConstraint, psi, theta, phi)
          → [else] CalculateZ_Aligned(zAxis, xConstraint, psi, theta, phi)
              → CalculatePCS_DirectionCosines(x, z, xDC, yDC, zDC)  // 构建正交方向余弦
              → CalculateFromBodyFrame(xP, yP, zP, psi, theta, phi)  // 提取欧拉角
      ← 或直接返回 (OrientationNone → false)
      ← 或 try/catch 失败处理 (Entity/GeoPoint 子类 → HandleException → false)

外部初始化: Orientation::Factory(typeName)
  → 根据类型名字符串创建对应的 Orientation 子类 unique_ptr
  → 返回 nullptr 若类型名不识别
```

调用链中每一步的说明：
- **Calculate() 入口**：各子类的虚函数，由姿态控制器每帧调用，提供输出引用参数接收三个欧拉角。
- **CalculateAligned()**：基类的 const 成员函数，根据 `mDefaultX_Aligned` 标志分派到 X 轴或 Z 轴对齐分支。
- **CalculateX_Aligned() / CalculateZ_Aligned()**：静态方法，调用 `CalculatePCS_DirectionCosines` 构建正交方向余弦，再调用 `CalculateFromBodyFrame` 提取欧拉角。
- **CalculatePCS_DirectionCosines()**：静态方法，核心几何运算——通过两次归一化和两次叉积构建正交右手系方向余弦。
- **CalculateFromBodyFrame()**：匿名命名空间中的自由函数，从方向余弦矩阵中提取DIS标准欧拉角。
- **Nadir/Solar/VelocityECI/VelocityECEF/OrbitPlaneConstraint**：基类protected方法，获取各参考矢量。
- **TargetVector()**：Entity子类和GeoPoint子类的protected方法，查找目标并计算指向矢量。
- **HandleException()**：基类protected方法，在首次异常时输出一次警告日志并抑制后续重复警告。

#### 源码位置

| 函数 | 源文件位置 (file:line) |
|------|----------------------|
| `Orientation::CalculatePCS_DirectionCosines` | `WsfSpaceOrientation.cpp:62-80` |
| `Orientation::CalculateX_Aligned` | `WsfSpaceOrientation.cpp:90-99` |
| `Orientation::CalculateZ_Aligned` | `WsfSpaceOrientation.cpp:109-123` |
| `Orientation::CalculateGeneral` | `WsfSpaceOrientation.cpp:139-166` |
| `Orientation::CalculateAligned` | `WsfSpaceOrientation.cpp:176-190` |
| `Orientation::Solar` | `WsfSpaceOrientation.cpp:193-198` |
| `Orientation::VelocityECI` | `WsfSpaceOrientation.cpp:201-206` |
| `Orientation::VelocityECEF` | `WsfSpaceOrientation.cpp:209-224` |
| `Orientation::Nadir` | `WsfSpaceOrientation.cpp:227-233` |
| `Orientation::Factory` | `WsfSpaceOrientation.cpp:239-288` |
| `Orientation::OrbitPlaneConstraint` | `WsfSpaceOrientation.cpp:293-309` |
| `Orientation::HandleException` | `WsfSpaceOrientation.cpp:312-322` |
| `Orientation::GetScriptClassName` | `WsfSpaceOrientation.cpp:46-49` |
| `CalculateFromBodyFrame` (匿名空间) | `WsfSpaceOrientation.cpp:33-38` |
| `OrientationEntity::OrientationEntity` | `WsfSpaceOrientation.cpp:324-327` |
| `OrientationEntity::ProcessInput` | `WsfSpaceOrientation.cpp:329-333` |
| `OrientationEntity::SetEntityName` | `WsfSpaceOrientation.cpp:335-339` |
| `OrientationEntity::SetTrackId` | `WsfSpaceOrientation.cpp:341-345` |
| `OrientationEntity::IsValid` | `WsfSpaceOrientation.cpp:347-358` |
| `OrientationEntity::GetTargetEntity` | `WsfSpaceOrientation.cpp:360-363` |
| `OrientationEntity::TargetVector` | `WsfSpaceOrientation.cpp:366-404` |
| `OrientationGeoPoint::ProcessInput` | `WsfSpaceOrientation.cpp:407-411` |
| `OrientationGeoPoint::IsValid` | `WsfSpaceOrientation.cpp:413-423` |
| `OrientationGeoPoint::SetGeoPoint` | `WsfSpaceOrientation.cpp:425-429` |
| `OrientationGeoPoint::TargetVector` | `WsfSpaceOrientation.cpp:432-460` |
| `OrientationEntitySolar::Calculate` | `WsfSpaceOrientation.cpp:462-474` |
| `OrientationEntityNadir::Calculate` | `WsfSpaceOrientation.cpp:582-594` |
| `OrientationEntityOrbitPlane::Calculate` | `WsfSpaceOrientation.cpp:615-629` |
| `OrientationPointOrbitPlane::Calculate` | `WsfSpaceOrientation.cpp:476-490` |
| `Orientation` 基类声明 | `WsfSpaceOrientation.hpp:79-160` |
| `OrientationNone` 声明 | `WsfSpaceOrientation.hpp:162-171` |
| `OrientationNadirECI_Velocity` 声明 | `WsfSpaceOrientation.hpp:173-186` |
| `OrientationSolarNadir` 声明 | `WsfSpaceOrientation.hpp:188-201` |
| `OrientationNadirSolar` 声明 | `WsfSpaceOrientation.hpp:203-216` |
| `OrientationNadirECEF_Velocity` 声明 | `WsfSpaceOrientation.hpp:218-231` |
| `OrientationECI_VelocityNadir` 声明 | `WsfSpaceOrientation.hpp:233-246` |
| `OrientationECI_VelocitySolar` 声明 | `WsfSpaceOrientation.hpp:248-261` |
| `OrientationEntity` 声明 | `WsfSpaceOrientation.hpp:263-310` |
| `OrientationEntitySolar` 声明 | `WsfSpaceOrientation.hpp:312-321` |
| `OrientationEntityNadir` 声明 | `WsfSpaceOrientation.hpp:323-332` |
| `OrientationEntityOrbitPlane` 声明 | `WsfSpaceOrientation.hpp:334-343` |
| `OrientationGeoPoint` 声明 | `WsfSpaceOrientation.hpp:345-369` |
| `OrientationPointOrbitPlane` 声明 | `WsfSpaceOrientation.hpp:371-381` |

#### 框架依赖

本算法集依赖于以下AFSIM框架组件：

**不可替换依赖（核心接口）**：
1. `WsfAttitudeController` -- 提供 `GetMover()` 接口，通过该接口访问平台和仿真环境。必须由平台初始化时调用 `Orientation::SetAttitudeController()` 注入。
2. `WsfPlatform` -- 提供位置（`GetLocationECI`）、速度（`GetVelocityECI`, `GetVelocityWCS`）、仿真时间（`GetSimTime`）、组件查找（`GetComponent`）和坐标转换（`ConvertWCSToECI`）功能。
3. `UtSun` -- 提供太阳在ECI坐标系中的位置计算（`GetSunLocationECI`），依赖于时间参数。
4. `WsfSpaceMoverBase`（通过 `GetMover()->GetPropagator()`）-- 提供当前仿真时间以获取地球自转角（`GetEarthAngle`）。
5. `UtEntity::ComputeRotationalTransform` -- 用于 `CalculateGeneral` 中将ECS偏航/俯仰/滚动角转换为旋转矩阵。

**可替换依赖**：
1. `UtMat3d::Multiply` -- 3x3矩阵乘法，用于 `CalculateGeneral` 中的矩阵组合。可使用任何等效的3x3矩阵乘法实现替换。
2. `UtVec3d`（`UtVec3.hpp`）-- 三维矢量类，提供归一化（`Normalize`）、叉积（`CrossProduct`）、模平方（`MagnitudeSquared`）、减法（`Subtract`）、标量乘法（`Multiply`）等基本矢量运算。可用任何支持相同基本矢量运算的线性代数库替换。
3. `WsfTrackList` / `WsfLocalTrack` -- 航迹系统仅在 `mOrientToTrack = true` 时使用。若不需要航迹指向功能，可安全移除。
4. `WsfGeoPoint` -- 地理点组件仅在 `OrientationPointOrbitPlane` 和 `OrientationGeoPoint` 类中使用。若不需要地理点指向功能，可安全移除。

#### 边界条件

1. **约束/指向矢量平行或反平行**：当指向轴矢量与约束轴矢量平行或反平行时，`CalculatePCS_DirectionCosines` 中的叉积 $\mathbf{z}_{\text{constraint}} \times \mathbf{x}$ 将为零矢量。在这种情况下，`Normalize()` 的行为由 `UtVec3d` 实现决定（通常返回零矢量或触发断言）。调用方需确保指向矢量和约束矢量不平行——对于内置模式，这两个矢量来自不同的物理源（如天底与速度），在实际轨道运行中通常不会平行。

2. **轨道面约束退化**：`OrbitPlaneConstraint` 中当 `alignVector` 平行于轨道面法向时（即目标指向方向恰好沿轨道面法向），$\mathbf{n} \times \mathbf{a}_{\text{align}}$ 将为零矢量。此时算法以平台速度矢量 $\mathbf{v}$ 作为回退约束方向。$\mathbf{v}$ 始终在轨道面内，保证约束矢量始终有效。

3. **目标实体不存在**：在 `OrientationEntity::TargetVector()` 中，若指定的实体名称在仿真中不存在，将抛出 `EntityNotFoundException`。调用该异常后，实体定向子类的 `Calculate()` 捕获异常并通过 `HandleException` 输出一次警告日志，返回 `false`。

4. **目标航迹无效**：在航迹指向模式中（`mOrientToTrack = true`），若航迹ID未在航迹列表中注册，抛出 `TrackNotFoundException`；若航迹位置无效（未初始化或已过期），抛出 `TrackLocationInvalidException`。处理方式同上。

5. **地理点组件不存在**：`OrientationGeoPoint::TargetVector()` 中，若指定名称的地理点组件未在平台上注册，抛出 `GeoPointNotFoundException`。处理方式同上。

6. **姿态控制器未设置**：`mControllerPtr` 在初始化时为 `nullptr`（由 `SetAttitudeController` 设置）。在控制器未设置时，`IsValid()` 返回 `true`（无法验证目标存在性，假设有效用于预验证步骤）。但若实际调用 `Calculate()`，解引用空指针将导致未定义行为。正常使用中，平台初始化会在首次定向计算前调用 `SetAttitudeController`。

7. **仅警告一次错误**：`HandleException` 使用 `mIssueErrorMessage` 标志确保对给定定向对象的每个会话中仅输出一次警告日志。首次异常后将该标志置为 `false`，后续同类异常静默处理。这防止了持续无效状态（如目标平台被销毁）导致的日志洪泛。

#### 测试和验证计划

**最简单测试方案**：对每种定向模式进行单元测试。

1. **测试环境**：创建一个简单的仿真场景，包含一颗在圆形LEO轨道上的卫星平台，设置其 `WsfInstantAttitudeController` 的定向模式为待测模式。

2. **基本功能测试**（覆盖所有11种模式）：
   - `OrientationNone`：调用 `Calculate()`，验证返回 `false` 且角度不变。
   - 天底指向模式（NadirECI_Velocity, NadirECEF_Velocity, NadirSolar）：初始化卫星位置在(0, 0, 7000km) ECI，验证天底矢量指向地心方向（即与位置矢量反平行），Z轴对齐天底，X轴由对应约束确定。
   - ECI速度指向模式（ECI_VelocityNadir, ECI_VelocitySolar）：验证X轴指向速度方向，Z轴由约束确定。
   - 太阳指向模式（SolarNadir）：设置已知太阳位置，验证Z轴对齐太阳方向。
   - 实体指向模式（EntitySolar, EntityNadir, EntityOrbitPlane）：在同一仿真中放置第二颗卫星作为目标，验证X轴指向目标实体。
   - 地理点指向模式（PointOrbitPlane）：在卫星上定义一个WsfGeoPoint（如地面站坐标），验证X轴指向该地理点。

3. **边界条件测试**：
   - 测试目标实体不存在时的异常处理：创建一个指向不存在实体名称的姿态定向，验证 `Calculate()` 返回 `false` 且日志包含一次警告。
   - 测试退化轨道面约束：将卫星置于轨道面法向恰好指向目标的情况，验证回退到速度矢量约束。
   - 测试零速度情况：若卫星速度为零（理论上在轨道中不可能，但可用于测试），验证约束矢量计算的鲁棒性。

4. **验证指标**：
   - 输出角度在 $[-\pi, \pi]$（偏航/滚动）和 $[-\pi/2, \pi/2]$（俯仰）范围内。
   - 构建的方向余弦矩阵应为正交矩阵（各列为单位矢量且互相垂直，误差小于数值精度 $10^{-12}$）。
   - 指向轴实际指向（由计算出的欧拉角重建方向余弦矩阵的对应列）与输入的指向矢量夹角应小于 $10^{-10}$ 弧度。

#### 可移植性评分

**可移植性**：高

**原因**：
1. 核心数学运算（矢量归一化、叉积、点积、反正弦、反正切、三角函数）在所有平台和编译器上都是标准数学库的一部分，无平台特定依赖。
2. 算法本身是纯数学坐标变换，不涉及文件I/O、操作系统调用或硬件接口。所有外部依赖（平台位置/速度查询、太阳位置计算）都通过抽象接口获取，隔离良好。
3. 唯一需要关注的移植问题是 `Normalize()` 对零矢量的处理行为——在退化情况下约束矢量与指向矢量平行时可能产生零矢量。不同平台上 `UtVec3d::Normalize()` 的实现可能以不同方式处理零矢量（返回零矢量或触发断言），移植时需验证此行为并确保处理器一致。
4. ECEF到ECI的速度变换仅使用二维旋转矩阵（绕Z轴），不涉及地球极移、章动或岁差修正——此简化可能在需要高精度地球定向建模的应用中需要替换，但对于大多数航天仿真应用是足够的。
5. 航迹系统和地理点系统是AFSIM特有的框架组件，若移植到非AFSIM环境，这些实体/地理点指向模式需要替换为等效的目标跟踪和目标点定位实现。
