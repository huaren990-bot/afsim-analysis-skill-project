/*
 * ============================================================================
 * 文件名称: {function_name}.h / {function_name}.cpp
 * 功能描述: {简要描述本文件实现的功能}
 * 迁移来源: AFSIM 项目 {源文件路径}
 * 源函数: {Class::method}
 * 迁移日期: {YYYY-MM-DD}
 * 修改说明:
 *   - {说明1} 
 *   - {说明2}
 * 原始版权声明: {保留原许可证信息，若适用}
 * ============================================================================
 */

#ifndef {GUARD_MACRO}_H
#define {GUARD_MACRO}_H

#include <Eigen/Dense>      // 线性代数库
// 其他必要头文件...

/**
 * @brief {函数功能简述}
 * 
 * @param {参数名} {参数说明} （单位、坐标系等）
 * @param {参数名} {参数说明}
 * @return {返回值说明}
 * 
 * @note 注意说明:
 *       - {特殊事项}
 *       - {坐标系假设}
 * 
 * @warning {警告: 如线程安全、异常安全等}
 */
{return_type} {function_name}({parameter_list});

#endif // {GUARD_MACRO}_H


// ===== {function_name}.cpp =====

#include "{function_name}.h"
#include <cmath>  // 数学函数

/**
 * 内部辅助函数: {辅助功能描述}
 * 从 AFSIM 原始私有方法 {original_method} 改编
 * @param ...
 * @return ...
 */
static {return_type} helper_function({parameters}) {
    // 实现代码...
}

// ---------------------------------------------------------------------------
// 公共接口实现
// ---------------------------------------------------------------------------

{return_type} {function_name}({parameter_list}) {
    // 步骤1: {描述第一步操作，例如：提取输入状态}
    // 原 AFSIM 代码: {source_function} 第 {line} 行

    // 步骤2: {核心算法步骤}
    // 使用 {数值方法/公式}，参考 AFSIM 算法卡片 {card_id}

    // 步骤3: {后处理，如归一化、限幅}

    // 返回结果
    return result;
}