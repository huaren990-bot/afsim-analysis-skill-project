```c++
class FormationMoveAlongPath
{
    public:
    /**
    初始化：在仿真开始时初始化
    pPhyComp 组件指针
    params 参数集容器指针
    p 初始化参数
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
}

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

(*params)["V_wind"]=para.getPara("V_wind", 0.0);
(*params)["V_max"]...
(*params)["V_wind"]...
(*params)["m_const"]...
(*params)["Max_Fuel_Capacity"]...
(*params)["S_ref"]...
(*params)["l_ref"]...


```