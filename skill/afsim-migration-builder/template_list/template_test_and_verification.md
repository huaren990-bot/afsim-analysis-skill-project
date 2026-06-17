# 测试调用与验证说明 — {FU-XXX} {功能单元名称}

## 1. 编译与环境要求
- **编译器**：支持 C++17，如 GCC 9.0+ / Clang 10+
- **依赖库**：
  - Eigen 3.3+ （头文件即可）
  - {其他依赖}
- **头文件搜索路径**：添加 `src/migration/{module}` 和 Eigen 路径
- **链接**：不需要额外库（仅头文件）

## 2. 测试用例构造
### 2.1 输入数据准备
以下示例构造一个典型刚体状态和力输入（SI 单位）：
```cpp
// 包含迁移模块头文件
#include "rigid_body_integrator.h"

// 构造初始状态
RigidBodyState state;
state.position = Eigen::Vector3d(0.0, 0.0, 0.0);        // 初始位置
state.velocity = Eigen::Vector3d(100.0, 0.0, 0.0);      // 初速度 100 m/s 沿 X
state.orientation = Eigen::Quaterniond::Identity();      // 单位四元数
state.angular_velocity = Eigen::Vector3d(0.0, 0.0, 0.0); // 无初始旋转

// 构造外力与力矩
Wrench forces;
forces.force = Eigen::Vector3d(0.0, 0.0, -9.80665 * 1000.0); // 重力 N, 质量1000kg
forces.torque = Eigen::Vector3d(0.0, 0.0, 0.0);

double dt = 0.001; // 1ms 步长
```

### 2.2 调用示例
```c++
RigidBodyState new_state = integrate_rigid_body(state, forces, dt);
```
## 3.预期输出与验证方法

### 3.1 基本物理验证

- 位置：由于重力向下，Z 轴位置应减小；X 轴由于初速度且无阻力应保持匀速，因此 X 位置近似 100 * t。
- 速度：X 分量保持不变，Z 分量应线性增加（vy = g*t）。
- 姿态：无外力矩时四元数应保持为单位四元数（误差 < 1e-12）。

### 3.2 数值验证（与 AFSIM 原版对比）
如有条件，在相同输入下调用 AFSIM 原始函数，比较输出：

- 允许的绝对误差：位置 < 1e-9 米，速度 < 1e-12 米/秒。
- 可使用 assert 或 GTest 进行自动检查。

### 3.3 边界条件测试
- 零时间步长：传入 dt=0 应返回原状态不变。
- 极大质量：当质量趋于无穷时，加速度应为 0。
- 非正规化四元数输入：函数内部应重新归一化。

## 4. 编译与运行指令（示例）
```bash
g++ -std=c++17 -I src/migration/kinematics -I /usr/include/eigen3 \
    test_rigid_body.cpp -o test_rigid_body
./test_rigid_body
```
## 5. 故障排查
- 如遇到编译错误 “Eigen not found”，请检查 Eigen 安装路径。
- 如结果出现 NaN，检查输入是否有非数或除法零。
- 姿态漂移过大，请确认角速度单位是弧度/秒。

## 6. 测试报告
| 测试项 |	状态 |	备注 |
|-------|-------|-------|
| 基本物理验证 |	☐ 通过 / ☐ 失败 | - |	
| 数值对比（与 AFSIM） |	☐ 通过 / ☐ 未执行 |-|	
| 边界测试  | ☐ 通过 / ☐ 失败	| - |
| 异常处理测试  |	☐ 通过 / ☐ 未覆盖	| - |
>**测试人员**：__________ 
>**日期**：__________


