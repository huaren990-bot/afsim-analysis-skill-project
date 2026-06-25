/*
 * ============================================================================
 * 文件名称: {REQ_xxx}.h / {REQ_xxx}.cpp
 * 功能描述: {简要描述本文件实现的功能}
 * 迁移来源: AFSIM 项目 {源文件路径}（若为 novel FU，则为"设计依据: {文献引用}"）
 * 源函数: {Class::method}（若为 novel FU，则为"无（AFSIM 无参考，全新设计）"）
 * 迁移日期: {YYYY-MM-DD}
 * 修改说明:
 *   - {说明1} 
 *   - {说明2}
 * 原始版权声明: {保留原许可证信息，若适用}
 * ============================================================================
 */

/**
 *  ============================================================================
 * @file REQ_xxx.h
 * @brief 需求 REQ-XXX 迁移模块接口声明。{简要描述本文件实现的功能}
 *
 * 包含的原子功能：
 * - FU-001: <功能名> (来源: AFSIM src/.../xxx.cpp:line)
 * - FU-xxx: <功能名> (设计依据: [文献引用] — novel，AFSIM 无参考)
 * ============================================================================
 */

#ifndef REQ_XXX_H
#define REQ_XXX_H

#include <target_system_common.h>   // 目标系统公共类型
#include <Eigen/Dense>              // 第三方依赖

// 如果需要，定义模块专有结构体
struct ModuleSpecificParams {
    double gravity = 9.80665;
    // ... 其他参数
};

/**
 * @brief FU-001: <功能描述>
 * @param state 当前刚体状态（位置、速度、姿态、角速度）
 * @param forces 合外力与力矩
 * @param dt 时间步长
 * @param params 配置参数（质量、惯量等）
 * @return 更新后的状态
 */
RigidBodyState REQ_xxx_integrate_step(const RigidBodyState& state,
                                      const Wrench& forces,
                                      double dt,
                                      const ModuleSpecificParams& params);

// 其他 FU 函数声明...

#endif // REQ_XXX_H