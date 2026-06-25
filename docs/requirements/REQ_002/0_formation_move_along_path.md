# 编队延航线机动行为设计需求

> **时间**:2026.06.24
> **编号**:REQ-002
## 需求描述

- **使用对象**：无人机/飞机编队
- **涉及组件**：机动
- **原有设计**：-
- **目标设计**：
  - 1. 飞机编队沿着设定的期望航线（坐标数组）执行机动
  - 2. 用单个飞机模型代替整个编队模型进行机动计算
  - 3. 使用六自由度模型计算姿态、位置和剩余油量

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
  - 上个步长内的编队路径`vector<Point>`
  - 上个步长内的姿态`vector<Posture>`
  - 上个步长内的速度`vector<double>`
  - 上个步长内的油量`vector<double>`

## 输出

- **需求输出**：
  - 剩余的期望航线`vector<Point>`
  - 下个步长内的编队路径`vector<Point>`：当步长大于1s时，路径为每秒编队位置的数组；当步长小于1s时，路径只存下一帧的编队位置。
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




