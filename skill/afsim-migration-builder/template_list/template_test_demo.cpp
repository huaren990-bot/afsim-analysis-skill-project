/**
 * @file test_demo.cpp
 * @brief REQ-XXX 迁移功能演示与快速验证
 *
 * 编译命令（示例）：
 *   g++ -std=c++17 -I../include test_demo.cpp REQ_xxx.cpp -o test_demo
 * 运行：
 *   ./test_demo
 * 预期输出：
 *   最终位置: (x, y, z)
 *   姿态四元数: (w, x, y, z)
 */

#include "REQ_xxx.h"
#include <iostream>

int main() {
    // 1. 初始化
    RigidBodyState state = RigidBodyState::Identity();
    // ... 设置初始值

    // 2. 配置参数
    ModuleParams params;
    params.mass = 100.0;

    // 3. 调用
    state = REQ_xxx_integrate_step(state, forces, 0.01, params);

    // 4. 输出
    std::cout << "Position: " << state.position.transpose() << std::endl;
    return 0;
}



