# 延航线机动行为设计需求

> **时间**:2026.06.24
> **编号**:REQ-002
## 需求描述

- **使用对象**：无人机/飞机
- **涉及组件**：机动
- **原有设计**：-
- **目标设计**：
  - 1. 飞机沿着设定的期望航线（坐标数组）执行机动
  - 2. 使用六自由度模型计算姿态、位置和剩余油量

- **补充要求**：
  - 1. 默认飞机从起飞到降落的机动中，飞机的形态没有变化，大小、材质、外观、除了燃油的其他质量等物理属性都不会有变化。


## 参考理论

    无

## 数据类型说明
```c++
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
```


## 输入

- **需求输入**：
  - 期望航线`(vector<Point> path)`
  - 上个步长内的路径`vector<Point>`
  - 上个步长内的姿态`vector<Posture>`
  - 上个步长内的速度`vector<double>`
  - 上个步长内的油量`vector<double>`

## 输出

- **需求输出**：
  - 剩余的期望航线`vector<Point>`
  - 下个步长内的路径`vector<Point>`：当步长大于1s时，路径为每秒飞机位置的数组；当步长小于1s时，路径只存下一帧的飞机位置。
  - 下个步长内的姿态`vector<Posture>`：同上。
  - 下个步长内的速度`vector<double>`：同上。
  - 下个步长内的油量`vector<double>`：同上。

## 其他参数
  - 仿真步长`double`
  - 当前时间戳`double`
  - 耗油量`double`
  - 风速`dboule`
  - 速度`double`
  - 最大速度`double`
  - 地球参数



