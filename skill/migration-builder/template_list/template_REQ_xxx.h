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

#ifndef REQ_XXX_H
#define REQ_XXX_H

#include <target_system_common.h>   // 目标系统公共类型
#include <Eigen/Dense>              // 第三方依赖

// 如果需要，定义模块专有结构体
struct Point{
    double _lon; // 经度，单位m
    double _lat; // 纬度，单位m
    double _alt; // 高度，单位m
}

struct Posture{
    double _yaw; //航向角，单位度
    double _pitch; //俯仰角，单位度
    double _roll; //翻滚角，单位度
}

struct CMRBasicBAC{
    std::vector<Point> path; //期望航线
    std::vector<dobule> speed_profile; //期望速度
    std::vector<Point> track; //当前步长内的路径
    Posture posture; //当前姿态
    double speed; //当前速度
    double prev_fuel; //当前燃油质量
}


class FormationMoveAlongPath
{
    public:
    /**
     * @brief 初始化：在仿真开始时初始化
     * @param pPhyComp 组件指针
     * @param p 初始化参数
     * @param params 配置参数（质量、惯量等）
     */
    void init(CMRBasicBAC *pPhyComp, std::unordered_map<std::string, boost::any> *params, const CMRJsonPara &p);

    /**
    进入状态：在进入状态时被调用一次
    para 数据库参数
    */
    void enterState(const boost::any &para);

    /**
    状态运行：在状态保持时每个步长都调用一次
    */
    bool runState(double curTime, double deltaTime);

    /**
    异常情况上报
    */
    void reportError(double curTime, std::string report_string);
};
#endif // REQ_XXX_H