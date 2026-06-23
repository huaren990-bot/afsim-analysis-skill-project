# AFSIM 仿真框架功能层次文档

> **状态**：已完成
> **日期**：2026-06-22
> **分析范围**：AFSIM 2.9 全量源码
> **分析深度**：full（7 阶段完整流水线）
> **关联文档**：function-index.jsonl, symbol-index.jsonl, afsim-architecture.md

---

## 0. 文档说明

**总体概述**：本文档按四层体系（System→Module→Class→Method）组织 AFSIM 仿真框架的全部功能，
每层功能均可追溯到 function-index.jsonl 中的对应条目。

**功能划分**：

| 层级 | 英文 | 定义 | 对应索引 |
|------|------|------|----------|
| **系统级** | System-level | 跨框架/域/插件层，组合多个模块完成的端到端业务能力 | function-index level=System-level |
| **模块级** | Module-level | 在单一子系统/模块内通过策略模式实现多变体的功能 | function-index level=Module-level |
| **类级** | Class-level | 单个类（class）封装的职责集合 | function-index level=Class-level |
| **方法级** | Method-level | 单个函数/方法的具体算法实现 | function-index level=Method-level |

---

## 1. 系统级功能总览

| # | 系统级功能 | 核心职责 |
|---|-----------|----------|
| 1 | 仿真生命周期管理 | AFSIM 仿真的完整生命周期管理：场景加载→对象创建→仿真循环→模型更新→事件处理→结果输出→资源清理 |
| 2 | 物理模型与动力学计算 | 涵盖飞行器六自由度/质点动力学、轨道预报、传感器物理模型、环境建模等数值计算密集型功能 |
| 3 | 数据链通信与战术网络 | 涵盖 Link16、IADS C2、MIL-STD 等战术数据链和通信协议的消息处理与网络仿真功能 |
| 4 | 场景解析与配置管理 | 场景文件解析、语法检查、配置生成、对象注册等仿真初始化前处理功能 |
| 5 | 可视化与用户界面 | 涵盖 2D/3D 可视化、地图渲染、数据显示、结果回放等图形用户界面功能 |

**功能对应条目**：见 function-index.jsonl 中 `level=System-level` 的 5 个条目。

---

## 1. 仿真生命周期管理

1. **系统功能概述**：AFSIM 仿真的完整生命周期管理：场景加载→对象创建→仿真循环→模型更新→事件处理→结果输出→资源清理
2. **功能对应条目**：见 function-index.jsonl 中 `level=System-level` 的条目 `qualified_name=system::simulation_lifecycle`
3. **模块级功能细览**：该系统功能包含 0 个模块级功能：

| 系统级功能 | 模块级功能 (Module-level) | 核心职责 |
|-----------|--------------------------|----------|

---

## 2. 物理模型与动力学计算

1. **系统功能概述**：涵盖飞行器六自由度/质点动力学、轨道预报、传感器物理模型、环境建模等数值计算密集型功能
2. **功能对应条目**：见 function-index.jsonl 中 `level=System-level` 的条目 `qualified_name=system::physics_dynamics`
3. **模块级功能细览**：该系统功能包含 4 个模块级功能：

| 系统级功能 | 模块级功能 (Module-level) | 核心职责 |
|-----------|--------------------------|----------|
| 物理模型与动力学计算 | wsf_space模块 | 太空仿真的轨道预报和星座管理功能集合 |
| 物理模型与动力学计算 | wsf_p6dof模块 | 质点六自由度动力学模型功能集合 |
| 物理模型与动力学计算 | wsf_six_dof模块 | 六自由度飞行器动力学仿真功能集合 |
| 物理模型与动力学计算 | wsf_sosm模块 | 小型轨道卫星模型功能集合 |

### 2.1 wsf_space

1. **模块功能概述**：太空仿真的轨道预报和星座管理功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_space`
3. **类级功能细览**：该模块级功能包含 116 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_space | State | Struct defined in UtRouteCalculator |
| wsf_space | SharedData | SharedData 的功能集合 |
| wsf_space | Object | Object 的功能集合 |
| wsf_space | Data | Struct defined in WsfRelativeManeuver |
| wsf_space | MyMat3d | MyMat3d 的功能集合 |

#### 2.1.1 State

1. **类功能概述**：Struct defined in UtRouteCalculator
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::State`
3. **方法级功能细览**：该类级功能包含 55 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| State | Set | State::Set | unknown | state_update | method: UtVec3d:: Set(mLocationWCS, 0.0) |
| State | Set | State::Set | unknown | state_update | method: UtVec3d:: Set(mLLA, 0.0) |
| State | ~State | State::~State | shutdown | unknown | destructor: virtual ~State() |
| State | State | State::State | unknown | unknown | constructor: State(WsfStringId aStateId) |
| State | State | State::State | unknown | unknown | constructor: State() |

#### 2.1.2 SharedData

1. **类功能概述**：SharedData 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::SharedData`
3. **方法级功能细览**：该类级功能包含 83 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| SharedData | SharedData | SharedData::SharedData | unknown | unknown | constructor: SharedData() |
| SharedData | ~SharedData | SharedData::~SharedData | shutdown | unknown | destructor: ~SharedData() |
| SharedData | InitializeType | SharedData::InitializeType | object_create | math | method: bool InitializeType(WsfObject& aBase) |
| SharedData | IsA_ValidState | SharedData::IsA_ValidState | unknown | math | method: bool IsA_ValidState(WsfStringId aId) const |
| SharedData | ProcessInput | SharedData::ProcessInput | model_update | math | method: bool ProcessInput(UtInput& aInput, WsfObject& aBase) |

### 2.2 wsf_p6dof

1. **模块功能概述**：质点六自由度动力学模型功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_p6dof`
3. **类级功能细览**：该模块级功能包含 20 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_p6dof | Event | Event 的功能集合 |
| wsf_p6dof | Data | Struct defined in WsfRelativeManeuver |
| wsf_p6dof | WsfP6DOF_TypeManager | WsfP6DOF_TypeManager 的功能集合 |
| wsf_p6dof | wsf::p6dof::EventPipe | wsf::p6dof::EventPipe 的功能集合 |
| wsf_p6dof | wsf::p6dof::EventPipeInterface | wsf::p6dof::EventPipeInterface 的功能集合 |

#### 2.2.1 Event

1. **类功能概述**：Event 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::Event`
3. **方法级功能细览**：该类级功能包含 3 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| Event | Event | Event::Event | event_handling | unknown | constructor: Event(WsfFormationCommand* aCommandPtr, WsfSimu |
| Event | ~Event | Event::~Event | event_handling | unknown | destructor: ~Event() override |
| Event | Execute | Event::Execute | model_update | unknown | method: WsfEvent::EventDisposition Execute() override |

#### 2.2.2 Data

1. **类功能概述**：Struct defined in WsfRelativeManeuver
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::Data`
3. **方法级功能细览**：该类级功能包含 34 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| Data | Clone | Data::Clone | object_create | routing | method: MTT_Track::Data* Clone() const override |
| Data | ~Data | Data::~Data | shutdown | routing | destructor: ~Data() override |
| Data | ConvertFrom | Data::ConvertFrom | event_handling | routing | method: void ConvertFrom(const SupBlock& aBlock) override |
| Data | CopyFrom | Data::CopyFrom | unknown | routing | method: mHorizontalInfoMatrix. CopyFrom(aBlock.mDoubleBlock) |
| Data | CopyFrom | Data::CopyFrom | unknown | unknown | method: mFilterStates. CopyFrom(aBlock.mDoubleBlock + 36) |

### 2.3 wsf_six_dof

1. **模块功能概述**：六自由度飞行器动力学仿真功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_six_dof`
3. **类级功能细览**：该模块级功能包含 27 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_six_dof | wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData | Struct defined in WsfSixDOF_VehicleData |
| wsf_six_dof | wsf::six_dof::PointMassControlActuator | wsf::six_dof::PointMassControlActuator 的功能集合 |
| wsf_six_dof | wsf::six_dof::ObjectManager | wsf::six_dof::ObjectManager 的功能集合 |
| wsf_six_dof | wsf::six_dof::RigidBodyAeroMovableObject | wsf::six_dof::RigidBodyAeroMovableObject 的功能集合 |
| wsf_six_dof | wsf::six_dof::Environment | wsf::six_dof::Environment 的功能集合 |

#### 2.3.1 wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData

1. **类功能概述**：Struct defined in WsfSixDOF_VehicleData
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData`
3. **方法级功能细览**：该类级功能包含 4 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData | clearData | wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData::clearData | event_handling | math | method: void clearData() |
| wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData | max | wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData::max | event_handling | math | method: float MaxAccum         = std::numeric_limits<float>: |
| wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData | max | wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData::max | event_handling | math | method: float MaxErrorZero     = std::numeric_limits<float>: |
| wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData | min | wsf::six_dof::DataType::Appearance::Pid::Lateral::Vertical::Speed::Control::Nav::PidGainData::min | event_handling | math | method: float MinErrorZero     = std::numeric_limits<float>: |

#### 2.3.2 wsf::six_dof::PointMassControlActuator

1. **类功能概述**：wsf::six_dof::PointMassControlActuator 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::wsf::six_dof::PointMassControlActuator`
3. **方法级功能细览**：该类级功能包含 9 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| wsf::six_dof::PointMassControlActuator | PointMassControlActuator | wsf::six_dof::PointMassControlActuator::PointMassControlActuator | event_handling | math | constructor: explicit PointMassControlActuator(PointMassFlig |
| wsf::six_dof::PointMassControlActuator | ~PointMassControlActuator | wsf::six_dof::PointMassControlActuator::~PointMassControlActuator | event_handling | math | destructor: ~PointMassControlActuator() |
| wsf::six_dof::PointMassControlActuator | Clone | wsf::six_dof::PointMassControlActuator::Clone | object_create | math | method: PointMassControlActuator* Clone(PointMassFlightContr |
| wsf::six_dof::PointMassControlActuator | ProcessInput | wsf::six_dof::PointMassControlActuator::ProcessInput | event_handling | math | method: bool ProcessInput(UtInputBlock& aInputBlock) |
| wsf::six_dof::PointMassControlActuator | Initialize | wsf::six_dof::PointMassControlActuator::Initialize | object_create | math | method: bool Initialize(int64_t aSimTime_nanosec) |

---

## 3. 数据链通信与战术网络

1. **系统功能概述**：涵盖 Link16、IADS C2、MIL-STD 等战术数据链和通信协议的消息处理与网络仿真功能
2. **功能对应条目**：见 function-index.jsonl 中 `level=System-level` 的条目 `qualified_name=system::datalink_communication`
3. **模块级功能细览**：该系统功能包含 5 个模块级功能：

| 系统级功能 | 模块级功能 (Module-level) | 核心职责 |
|-----------|--------------------------|----------|
| 数据链通信与战术网络 | wsf_mil模块 | 模块 wsf_mil 的功能集合 |
| 数据链通信与战术网络 | wsf_mtt模块 | 模块 wsf_mtt 的功能集合 |
| 数据链通信与战术网络 | wsf_l16模块 | Link16 数据链消息处理和字段定义功能集合 |
| 数据链通信与战术网络 | wsf_mil_parser模块 | 模块 wsf_mil_parser 的功能集合 |
| 数据链通信与战术网络 | wsf_iads_c2_lib模块 | 模块 wsf_iads_c2_lib 的功能集合 |

### 3.1 wsf_mil

1. **模块功能概述**：模块 wsf_mil 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_mil`
3. **类级功能细览**：该模块级功能包含 438 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_mil | State | Struct defined in UtRouteCalculator |
| wsf_mil | BaseData | Struct defined in WsfFalseTarget |
| wsf_mil | Point | Struct defined in UtHeatMap |
| wsf_mil | Table | Table 的功能集合 |
| wsf_mil | SharedData | SharedData 的功能集合 |

#### 3.1.1 State

1. **类功能概述**：Struct defined in UtRouteCalculator
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::State`
3. **方法级功能细览**：该类级功能包含 55 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| State | Set | State::Set | unknown | state_update | method: UtVec3d:: Set(mLocationWCS, 0.0) |
| State | Set | State::Set | unknown | state_update | method: UtVec3d:: Set(mLLA, 0.0) |
| State | ~State | State::~State | shutdown | unknown | destructor: virtual ~State() |
| State | State | State::State | unknown | unknown | constructor: State(WsfStringId aStateId) |
| State | State | State::State | unknown | unknown | constructor: State() |

#### 3.1.2 BaseData

1. **类功能概述**：Struct defined in WsfFalseTarget
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::BaseData`
3. **方法级功能细览**：该类级功能包含 9 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| BaseData | BaseData | BaseData::BaseData | unknown | unknown | constructor: BaseData() |
| BaseData | BaseData | BaseData::BaseData | unknown | unknown | constructor: BaseData(const BaseData& aSrc) |
| BaseData | ~BaseData | BaseData::~BaseData | shutdown | unknown | destructor: ~BaseData() override |
| BaseData | ProcessInput | BaseData::ProcessInput | model_update | unknown | method: virtual bool ProcessInput(WsfAntennaPattern& aPatter |
| BaseData | Initialize | BaseData::Initialize | object_create | unknown | method: virtual bool Initialize(WsfAntennaPattern& aAntennaP |

### 3.2 wsf_mtt

1. **模块功能概述**：模块 wsf_mtt 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_mtt`
3. **类级功能细览**：该模块级功能包含 20 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_mtt | Data | Struct defined in WsfRelativeManeuver |
| wsf_mtt | MTT_PerceivedCluster | MTT_PerceivedCluster 的功能集合 |
| wsf_mtt | MTT_Parameters | MTT_Parameters 的功能集合 |
| wsf_mtt | MTT_EmbryonicTrack | MTT_EmbryonicTrack 的功能集合 |
| wsf_mtt | WsfMTT_ReferencePoint | WsfMTT_ReferencePoint 的功能集合 |

#### 3.2.1 Data

1. **类功能概述**：Struct defined in WsfRelativeManeuver
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::Data`
3. **方法级功能细览**：该类级功能包含 34 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| Data | Clone | Data::Clone | object_create | routing | method: MTT_Track::Data* Clone() const override |
| Data | ~Data | Data::~Data | shutdown | routing | destructor: ~Data() override |
| Data | ConvertFrom | Data::ConvertFrom | event_handling | routing | method: void ConvertFrom(const SupBlock& aBlock) override |
| Data | CopyFrom | Data::CopyFrom | unknown | routing | method: mHorizontalInfoMatrix. CopyFrom(aBlock.mDoubleBlock) |
| Data | CopyFrom | Data::CopyFrom | unknown | unknown | method: mFilterStates. CopyFrom(aBlock.mDoubleBlock + 36) |

#### 3.2.2 MTT_PerceivedCluster

1. **类功能概述**：MTT_PerceivedCluster 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::MTT_PerceivedCluster`
3. **方法级功能细览**：该类级功能包含 6 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| MTT_PerceivedCluster | MTT_PerceivedCluster | MTT_PerceivedCluster::MTT_PerceivedCluster | unknown | unknown | constructor: MTT_PerceivedCluster() |
| MTT_PerceivedCluster | ~MTT_PerceivedCluster | MTT_PerceivedCluster::~MTT_PerceivedCluster | shutdown | unknown | destructor: virtual ~MTT_PerceivedCluster() |
| MTT_PerceivedCluster | SetCombinedTrack | MTT_PerceivedCluster::SetCombinedTrack | unknown | state_update | method: void SetCombinedTrack(const MTT_CombinedTrack& aComb |
| MTT_PerceivedCluster | SetMeasurement | MTT_PerceivedCluster::SetMeasurement | unknown | state_update | method: void SetMeasurement(const MTT_Measurement& aMeasurem |
| MTT_PerceivedCluster | CopyFrom | MTT_PerceivedCluster::CopyFrom | unknown | unknown | method: void CopyFrom(double aSimTime, WsfMTT_Interface* aMT |

### 3.3 wsf_l16

1. **模块功能概述**：Link16 数据链消息处理和字段定义功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_l16`
3. **类级功能细览**：该模块级功能包含 322 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_l16 | WsfL16::Messages::J9_0::Continuation1 | WsfL16::Messages::J9_0::Continuation1 的功能集合 |
| wsf_l16 | WsfL16::Messages::J9_0::Continuation2 | WsfL16::Messages::J9_0::Continuation2 的功能集合 |
| wsf_l16 | WsfL16::Messages::J9_0::Extension0 | WsfL16::Messages::J9_0::Extension0 的功能集合 |
| wsf_l16 | WsfL16::Messages::J9_0::Initial | WsfL16::Messages::J9_0::Initial 的功能集合 |
| wsf_l16 | WsfL16::WeaponsCoordinationPart | WsfL16::WeaponsCoordinationPart 的功能集合 |

#### 3.3.1 WsfL16::Messages::J9_0::Continuation1

1. **类功能概述**：WsfL16::Messages::J9_0::Continuation1 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::WsfL16::Messages::J9_0::Continuation1`
3. **方法级功能细览**：该类级功能包含 1 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| WsfL16::Messages::J9_0::Continuation1 | DEFINE_CONTINUATION | WsfL16::Messages::J9_0::Continuation1::DEFINE_CONTINUATION | event_handling | control_flow | method: DEFINE_CONTINUATION(9, 0, 1) |

#### 3.3.2 WsfL16::Messages::J9_0::Continuation2

1. **类功能概述**：WsfL16::Messages::J9_0::Continuation2 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::WsfL16::Messages::J9_0::Continuation2`
3. **方法级功能细览**：该类级功能包含 2 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| WsfL16::Messages::J9_0::Continuation2 | DEFINE_CONTINUATION | WsfL16::Messages::J9_0::Continuation2::DEFINE_CONTINUATION | event_handling | control_flow | method: DEFINE_CONTINUATION(9, 0, 2) |
| WsfL16::Messages::J9_0::Continuation2 | DEFINE_MEMBERS6 | WsfL16::Messages::J9_0::Continuation2::DEFINE_MEMBERS6 | event_handling | control_flow | method: DEFINE_MEMBERS6(Hour, Minute, Second, NumberOfMissil |

---

## 4. 场景解析与配置管理

1. **系统功能概述**：场景文件解析、语法检查、配置生成、对象注册等仿真初始化前处理功能
2. **功能对应条目**：见 function-index.jsonl 中 `level=System-level` 的条目 `qualified_name=system::scenario_configuration`
3. **模块级功能细览**：该系统功能包含 4 个模块级功能：

| 系统级功能 | 模块级功能 (Module-level) | 核心职责 |
|-----------|--------------------------|----------|
| 场景解析与配置管理 | wsf_parser模块 | AFSIM 场景文件解析器功能集合 |
| 场景解析与配置管理 | wsf_grammar_check模块 | 模块 wsf_grammar_check 的功能集合 |
| 场景解析与配置管理 | wsf_mil_parser模块 | 模块 wsf_mil_parser 的功能集合 |
| 场景解析与配置管理 | wsf_scenario_analyzer模块 | 模块 wsf_scenario_analyzer 的功能集合 |

### 4.1 wsf_parser

1. **模块功能概述**：AFSIM 场景文件解析器功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_parser`
3. **类级功能细览**：该模块级功能包含 58 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_parser | WsfPM_Fuel | WsfPM_Fuel 的功能集合 |
| wsf_parser | WsfPProxyStructType | WsfPProxyStructType 的功能集合 |
| wsf_parser | WsfPProxyHash | WsfPProxyHash 的功能集合 |
| wsf_parser | WsfPProxyStructHeader | Struct defined in WsfPProxyStructHeader |
| wsf_parser | WsfParseActionAddress | WsfParseActionAddress 的功能集合 |

#### 4.1.1 WsfPM_Fuel

1. **类功能概述**：WsfPM_Fuel 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::WsfPM_Fuel`
3. **方法级功能细览**：该类级功能包含 1 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| WsfPM_Fuel | WsfPM_Fuel | WsfPM_Fuel::WsfPM_Fuel | unknown | unknown | constructor: WsfPM_Fuel() |

#### 4.1.2 WsfPProxyStructType

1. **类功能概述**：WsfPProxyStructType 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::WsfPProxyStructType`
3. **方法级功能细览**：该类级功能包含 37 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| WsfPProxyStructType | ~WsfPProxyStructType | WsfPProxyStructType::~WsfPProxyStructType | shutdown | math | destructor: ~WsfPProxyStructType() override |
| WsfPProxyStructType | IsUnset | WsfPProxyStructType::IsUnset | unknown | math | method: bool IsUnset(void* aValuePtr) const override |
| WsfPProxyStructType | SetUnset | WsfPProxyStructType::SetUnset | unknown | math | method: void SetUnset(void* aValuePtr) const override |
| WsfPProxyStructType | IsInherited | WsfPProxyStructType::IsInherited | utility | math | method: bool IsInherited(void* aValuePtr) const override |
| WsfPProxyStructType | SetInherited | WsfPProxyStructType::SetInherited | unknown | math | method: void SetInherited(void* aValuePtr, bool aIsInherited |

### 4.2 wsf_grammar_check

1. **模块功能概述**：模块 wsf_grammar_check 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_grammar_check`
3. **类级功能细览**：该模块级功能包含 1 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_grammar_check | ParseSourceProvider | ParseSourceProvider 的功能集合 |

#### 4.2.1 ParseSourceProvider

1. **类功能概述**：ParseSourceProvider 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::ParseSourceProvider`
3. **方法级功能细览**：该类级功能包含 5 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| ParseSourceProvider | WsfGrammarCheckExtension | ParseSourceProvider::WsfGrammarCheckExtension | scenario_load | unknown | method: WsfGrammarCheckExtension() |
| ParseSourceProvider | ~WsfGrammarCheckExtension | ParseSourceProvider::~WsfGrammarCheckExtension | scenario_load | unknown | method: ~WsfGrammarCheckExtension() override |
| ParseSourceProvider | FileLoaded | ParseSourceProvider::FileLoaded | scenario_load | unknown | method: void FileLoaded(const std::string& aFileName) overri |
| ParseSourceProvider | InitializeGrammar | ParseSourceProvider::InitializeGrammar | scenario_load | unknown | method: void InitializeGrammar(std::istream& aGrammarText) |
| ParseSourceProvider | FileLoad | ParseSourceProvider::FileLoad | scenario_load | unknown | method: int FileLoad(const std::string& aGrammarText, const  |

### 4.3 wsf_mil_parser

1. **模块功能概述**：模块 wsf_mil_parser 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wsf_mil_parser`
3. **类级功能细览**：该模块级功能包含 1 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wsf_mil_parser | Mode | Mode 的功能集合 |

#### 4.3.1 Mode

1. **类功能概述**：Mode 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::Mode`
3. **方法级功能细览**：该类级功能包含 2 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| Mode | Mode | Mode::Mode | unknown | unknown | constructor: Mode() |
| Mode | transmitter | Mode::transmitter | unknown | unknown | method: WsfPM_Transmitter transmitter() const |

---

## 5. 可视化与用户界面

1. **系统功能概述**：涵盖 2D/3D 可视化、地图渲染、数据显示、结果回放等图形用户界面功能
2. **功能对应条目**：见 function-index.jsonl 中 `level=System-level` 的条目 `qualified_name=system::visualization_ui`
3. **模块级功能细览**：该系统功能包含 2 个模块级功能：

| 系统级功能 | 模块级功能 (Module-level) | 核心职责 |
|-----------|--------------------------|----------|
| 可视化与用户界面 | engage模块 | 交战规则与任务分配功能集合 |
| 可视化与用户界面 | wizard模块 | 模块 wizard 的功能集合 |

### 5.1 engage

1. **模块功能概述**：交战规则与任务分配功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::engage`
3. **类级功能细览**：该模块级功能包含 48 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| engage | engage::TargetConfig | engage::TargetConfig 的功能集合 |
| engage | engage::RoutePoint | Struct defined in TargetConfig |
| engage | engage::SimulationThread | engage::SimulationThread 的功能集合 |
| engage | engage::Simulation | engage::Simulation 的功能集合 |
| engage | engage::TaskOutput | engage::TaskOutput 的功能集合 |

#### 5.1.1 engage::TargetConfig

1. **类功能概述**：engage::TargetConfig 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::engage::TargetConfig`
3. **方法级功能细览**：该类级功能包含 25 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| engage::TargetConfig | TargetConfig | engage::TargetConfig::TargetConfig | event_handling | math | constructor: TargetConfig() |
| engage::TargetConfig | Complete | engage::TargetConfig::Complete | event_handling | math | method: bool Complete(bool aTargetGridUsed) |
| engage::TargetConfig | CreatePlatform | engage::TargetConfig::CreatePlatform | object_create | math | method: bool CreatePlatform(Simulation& aSimulation, const T |
| engage::TargetConfig | ProcessInput | engage::TargetConfig::ProcessInput | event_handling | math | method: bool ProcessInput(UtInput& aInput) |
| engage::TargetConfig | ProcessSiteGridInput | engage::TargetConfig::ProcessSiteGridInput | event_handling | math | method: bool ProcessSiteGridInput(UtInput& aInput) |

#### 5.1.2 engage::RoutePoint

1. **类功能概述**：Struct defined in TargetConfig
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::engage::RoutePoint`
3. **方法级功能细览**：该类级功能包含 4 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| engage::RoutePoint | RoutePoint | RoutePoint::RoutePoint | unknown | unknown | constructor: RoutePoint() |
| engage::RoutePoint | RoutePoint | RoutePoint::RoutePoint | unknown | unknown | constructor: RoutePoint(const WaypointAddr& aAddr, double aD |
| engage::RoutePoint | RouteIndex | RoutePoint::RouteIndex | unknown | unknown | method: int RouteIndex() const |
| engage::RoutePoint | WaypointIndex | RoutePoint::WaypointIndex | unknown | unknown | method: int WaypointIndex() const |

### 5.2 wizard

1. **模块功能概述**：模块 wizard 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Module-level` 的条目 `qualified_name=module::wizard`
3. **类级功能细览**：该模块级功能包含 585 个类级功能：

| 模块级功能 | 类级功能 (Class-level) | 核心职责 |
|-----------|----------------------|----------|
| wizard | ZoneEditor::Plugin | ZoneEditor::Plugin 的功能集合 |
| wizard | ZoneEditor::CreateZoneDialog | ZoneEditor::CreateZoneDialog 的功能集合 |
| wizard | ZoneEditor::DockWidget | ZoneEditor::DockWidget 的功能集合 |
| wizard | TypeBrowser::Plugin | TypeBrowser::Plugin 的功能集合 |
| wizard | wizard::TypeBrowser::Model | wizard::TypeBrowser::Model 的功能集合 |

#### 5.2.1 ZoneEditor::Plugin

1. **类功能概述**：ZoneEditor::Plugin 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::ZoneEditor::Plugin`
3. **方法级功能细览**：该类级功能包含 25 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| ZoneEditor::Plugin | Plugin | ZoneEditor::Plugin::Plugin | event_handling | unknown | constructor: Plugin(const QString& aName, const size_t aUniq |
| ZoneEditor::Plugin | ~Plugin | ZoneEditor::Plugin::~Plugin | event_handling | unknown | destructor: ~Plugin() override |
| ZoneEditor::Plugin | BuildViewerContextMenu | ZoneEditor::Plugin::BuildViewerContextMenu | object_create | factory | method: void BuildViewerContextMenu(QMenu* aMenuPtr, vespa:: |
| ZoneEditor::Plugin | BuildAttachmentContextMenu | ZoneEditor::Plugin::BuildAttachmentContextMenu | object_create | factory | method: void BuildAttachmentContextMenu(QMenu* aMenu, vespa: |
| ZoneEditor::Plugin | GetPreferencesWidgets | ZoneEditor::Plugin::GetPreferencesWidgets | event_handling | configuration | method: QList<wkf::PrefWidget*> GetPreferencesWidgets() cons |

#### 5.2.2 ZoneEditor::CreateZoneDialog

1. **类功能概述**：ZoneEditor::CreateZoneDialog 的功能集合
2. **功能对应条目**：见 function-index.jsonl 中 `level=Class-level` 的条目 `qualified_name=class::ZoneEditor::CreateZoneDialog`
3. **方法级功能细览**：该类级功能包含 22 个方法级功能：

| 类级功能 | 方法级功能 | qualified_name（限定名） | lifecycle_role（生命周期角色） | algorithm_hint（算法提示） | 核心职责 |
|---------|-----------|------------------------|-------------------------------|--------------------------|----------|
| ZoneEditor::CreateZoneDialog | ~CreateZoneDialog | ZoneEditor::CreateZoneDialog::~CreateZoneDialog | object_create | math | destructor: ~CreateZoneDialog() override |
| ZoneEditor::CreateZoneDialog | closeEvent | ZoneEditor::CreateZoneDialog::closeEvent | object_create | math | method: void closeEvent(QCloseEvent* aEventPtr) override |
| ZoneEditor::CreateZoneDialog | CreateZone | ZoneEditor::CreateZoneDialog::CreateZone | object_create | math | method: void CreateZone() |
| ZoneEditor::CreateZoneDialog | ZoneTypeChanged | ZoneEditor::CreateZoneDialog::ZoneTypeChanged | object_create | math | method: void ZoneTypeChanged(const QString& aText) |
| ZoneEditor::CreateZoneDialog | ShowGeometricCommands | ZoneEditor::CreateZoneDialog::ShowGeometricCommands | object_create | math | method: void ShowGeometricCommands(bool aShow) |

---


---

## 附录 A：方法级功能精选清单

> 从 45603 个方法级功能中选取调用复杂度最高的 100 个方法。

| qualified_name | lifecycle_role | algorithm_hint | calls | 核心职责 |
|----------------|----------------|----------------|-------|----------|
| wsf::TerrainInterface::ProcessRect | model_update | math | 50 | method: bool ProcessRect(UtInput& aInput) |
| wsf::Terrain::ProcessRect | model_update | math | 50 | method: bool ProcessRect(UtInput& aInput) |
| wsf::six_dof::NestedFeedbackLoop::value_or | model_update | math | 50 | method: int tickCount = middleLoopFactor. value_or(1) |
| wsf::six_dof::NestedFeedbackLoop::value_or | model_update | math | 50 | method: int middleLoopTickCount = middleLoopFactor. value_or |
| wsf::six_dof::NestedFeedbackLoop::value_or | model_update | math | 50 | method: int outerLoopTickCount  = outerLoopFactor. value_or( |
| Designer::Designer::GeometryMassProperties::GetCgX | unknown | control_flow | 50 | method: double GetCgX() |
| Designer::Designer::GeometryMassProperties::GetCgY | unknown | control_flow | 50 | method: double GetCgY() |
| Designer::Designer::GeometryMassProperties::GetCgZ | unknown | control_flow | 50 | method: double GetCgZ() |
| Designer::Designer::GeometryMassProperties::GetCg | unknown | control_flow | 50 | method: UtVec3dX GetCg() |
| Designer::Designer::GeometryMassProperties::GetFueledIxx | unknown | control_flow | 50 | method: double GetFueledIxx() |
| Designer::Designer::GeometryMassProperties::GetFueledIyy | unknown | control_flow | 50 | method: double GetFueledIyy() |
| Designer::Designer::GeometryMassProperties::GetFueledIzz | unknown | control_flow | 50 | method: double GetFueledIzz() |
| Designer::Designer::GeometryMassProperties::GetFueledCgX | unknown | control_flow | 50 | method: double GetFueledCgX() |
| Designer::Designer::GeometryMassProperties::GetFueledCgY | unknown | control_flow | 50 | method: double GetFueledCgY() |
| Designer::Designer::GeometryMassProperties::GetFueledCgZ | unknown | control_flow | 50 | method: double GetFueledCgZ() |
| Designer::GeometryGLFocusPoint::Draw | output | math | 50 | method: void Draw() |
| Designer::GeometryGLFocusPoint::GetX | unknown | math | 50 | method: double GetX() |
| Designer::GeometryGLFocusPoint::GetY | unknown | math | 50 | method: double GetY() |
| Designer::GeometryGLFocusPoint::GetZ | unknown | math | 50 | method: double GetZ() |
| Designer::GeometryGLWidget::AdjustViewingDistance | utility | math | 50 | method: void AdjustViewingDistance(bool aInitialize = false) |
| Designer::GeometryGLWidget::initializeGL | object_create | math | 50 | method: void initializeGL() override |
| Designer::GeometryGLWidget::ToggleAxis | unknown | math | 50 | method: void ToggleAxis() |
| Designer::GeometryGLWidget::ToggleSelectedObjectCG | unknown | math | 50 | method: void ToggleSelectedObjectCG() |
| Designer::GeometryGLWidget::ToggleShowEngines | unknown | math | 50 | method: void ToggleShowEngines() |
| Designer::GeometryGLWidget::ToggleThrustVectors | unknown | math | 50 | method: void ToggleThrustVectors() |
| Designer::GeometryGLWidget::TogglePointMasses | unknown | math | 50 | method: void TogglePointMasses() |
| Designer::GeometryGLWidget::ToggleFuelTanks | unknown | math | 50 | method: void ToggleFuelTanks() |
| Designer::GeometryGLWidget::ToggleVehicleCG | unknown | math | 50 | method: void ToggleVehicleCG() |
| Designer::GeometryGLWidget::ToggleLandingGear | unknown | math | 50 | method: void ToggleLandingGear() |
| Designer::GeometryGLWidget::ToggleSpeedBrakes | unknown | math | 50 | method: void ToggleSpeedBrakes() |
| Designer::GeometryGLWidget::ToggleShowWireframe | model_update | math | 50 | method: void ToggleShowWireframe() |
| Designer::GeometryGLWidget::ShowAxis | unknown | math | 50 | method: void ShowAxis(bool aShow) |
| Designer::GeometryGLWidget::ShowSelectedObjectCG | unknown | math | 50 | method: void ShowSelectedObjectCG(bool aShow) |
| Designer::GeometryGLWidget::Draw | output | math | 50 | method: void Draw() override |
| Designer::GeometryGLWidget::QtDraw | output | math | 50 | method: void QtDraw() override |
| Designer::GeometryGLWidget::Draw3dView | output | math | 50 | method: void Draw3dView() |
| Designer::GeometryGLWidget::Draw2dOverlay | output | math | 50 | method: void Draw2dOverlay() |
| Designer::GeometryGLWidget::Draw2dOverlayTopLeft | output | math | 50 | method: void Draw2dOverlayTopLeft() |
| Designer::GeometryGLWidget::Draw2dOverlayTopCenter | output | math | 50 | method: void Draw2dOverlayTopCenter() |
| Designer::GeometryGLWidget::Draw2dOverlayTopRight | output | math | 50 | method: void Draw2dOverlayTopRight() |
| Designer::GeometryGLWidget::Draw2dOverlayBottomLeft | output | math | 50 | method: void Draw2dOverlayBottomLeft() |
| Designer::GeometryWing::GetAspectRatio | unknown | math | 50 | method: double GetAspectRatio() override |
| Designer::GeometryWing::GetPlanformArea_ft2 | unknown | math | 50 | method: double GetPlanformArea_ft2() override |
| Designer::GeometryWing::GetAileronsPresent | event_handling | math | 50 | method: bool GetAileronsPresent() |
| Designer::GeometryWing::GetAileronsChordFractionStart | event_handling | math | 50 | method: double GetAileronsChordFractionStart() |
| Designer::GeometryWing::GetAileronsChordFractionEnd | event_handling | math | 50 | method: double GetAileronsChordFractionEnd() |
| Designer::GeometryWing::GetAileronsSpanFractionStart | event_handling | math | 50 | method: double GetAileronsSpanFractionStart() |
| Designer::GeometryWing::GetAileronsSpanFractionEnd | event_handling | math | 50 | method: double GetAileronsSpanFractionEnd() |
| Designer::GeometryWing::GetAileronsUseExponentialAngleMapping | event_handling | math | 50 | method: bool GetAileronsUseExponentialAngleMapping() |
| Designer::GeometryWing::GetAileronsControlSurfaceMinAngle_deg | event_handling | math | 50 | method: double GetAileronsControlSurfaceMinAngle_deg() |
| Designer::GeometryWing::GetAileronsControlSurfaceMaxAngle_deg | event_handling | math | 50 | method: double GetAileronsControlSurfaceMaxAngle_deg() |
| Designer::GeometryWing::GetAileronsActuatorMinRate_dps | event_handling | math | 50 | method: double GetAileronsActuatorMinRate_dps() |
| Designer::GeometryWing::GetAileronsActuatorMaxRate_dps | event_handling | math | 50 | method: double GetAileronsActuatorMaxRate_dps() |
| Designer::GeometryWing::GetAileronsActuatorMinAngle_deg | event_handling | math | 50 | method: double GetAileronsActuatorMinAngle_deg() |
| Designer::GeometryWing::GetAileronsActuatorMaxAngle_deg | event_handling | math | 50 | method: double GetAileronsActuatorMaxAngle_deg() |
| Designer::GeometryWing::GetDrageronsPresent | event_handling | math | 50 | method: bool GetDrageronsPresent() |
| Designer::GeometryWing::GetDrageronsChordFractionStart | event_handling | math | 50 | method: double GetDrageronsChordFractionStart() |
| Designer::GeometryWing::GetDrageronsChordFractionEnd | event_handling | math | 50 | method: double GetDrageronsChordFractionEnd() |
| Designer::GeometryWing::GetDrageronsSpanFractionStart | event_handling | math | 50 | method: double GetDrageronsSpanFractionStart() |
| Designer::GeometryWing::GetDrageronsSpanFractionEnd | event_handling | math | 50 | method: double GetDrageronsSpanFractionEnd() |
| Designer::GeometryWing::GetDrageronsUseExponentialAngleMapping | event_handling | math | 50 | method: bool GetDrageronsUseExponentialAngleMapping() |
| Designer::VehicleAero::AeroObjectNameIsUnique | unknown | math | 50 | method: bool AeroObjectNameIsUnique(const std::string& aName |
| Designer::VehicleAero::MakeNameUnique | unknown | math | 50 | method: std::string MakeNameUnique(const std::string& aBaseN |
| Designer::VehicleAero::EnableDisableTables | unknown | math | 50 | method: void EnableDisableTables(bool aGenerateP6DOFMover, b |
| Designer::VehicleAero::CalculateFullVehicleAerodynamics | model_update | math | 50 | method: void CalculateFullVehicleAerodynamics() |
| Designer::VehicleAero::SetVehicleAlphaBeta | unknown | math | 50 | method: void SetVehicleAlphaBeta(double aAlpha_deg, double a |
| WkP6DOF_Controller::HUD::~HUD | event_handling | math | 50 | destructor: ~HUD() override |
| WkP6DOF_Controller::HUD::Clone | object_create | math | 50 | method: HUD* Clone() const override |
| WkP6DOF_Controller::HUD::Initialize | object_create | math | 50 | method: bool Initialize() override |
| WkP6DOF_Controller::HUD::Update | model_update | math | 50 | method: void Update() override |
| WkP6DOF_Controller::HUD::SetupHudProjection | event_handling | math | 50 | method: void SetupHudProjection(float aFovY) |
| WkP6DOF_Controller::HUD::SetHudMode | event_handling | math | 50 | method: void SetHudMode(P6DOF_ControllerDataContainer::eHudM |
| WkP6DOF_Controller::RegionExtents::X1 | event_handling | math | 50 | method: double X1() const |
| WkP6DOF_Controller::RegionExtents::Y1 | event_handling | math | 50 | method: double Y1() const |
| WkP6DOF_Controller::RegionExtents::X2 | event_handling | math | 50 | method: double X2() const |
| WkP6DOF_Controller::RegionExtents::Y2 | event_handling | math | 50 | method: double Y2() const |
| RoadTrafficNetworkInput::BadValue | unknown | math | 44 | method: throw UtInput:: BadValue(aInput, "XWsfRoadTraffic th |
| Designer::GeometrySurface::GeometrySurface | unknown | math | 50 | constructor: explicit GeometrySurface(Vehicle* aVehicle) |
| Designer::GeometrySurface::~GeometrySurface | shutdown | math | 50 | destructor: virtual ~GeometrySurface() |
| Designer::GeometrySurface::MoveRefPoint | unknown | math | 50 | method: void MoveRefPoint(UtVec3dX aMoveDelta_ft) override |
| Designer::GeometrySurface::GetSpan_ft | unknown | math | 50 | method: double GetSpan_ft() |
| Designer::GeometrySurface::GetRootChord_ft | unknown | math | 50 | method: double GetRootChord_ft() |
| Designer::GeometrySurface::GetTipChord_ft | unknown | math | 50 | method: double GetTipChord_ft() |
| Designer::GeometrySurface::GetSweepAngle_deg | unknown | math | 50 | method: double GetSweepAngle_deg() |
| Designer::GeometrySurface::GetDihedralAngle_deg | unknown | math | 50 | method: double GetDihedralAngle_deg() |
| Designer::GeometrySurface::GetIncidenceAngle_deg | unknown | math | 50 | method: double GetIncidenceAngle_deg() |
| Designer::GeometrySurface::GetThicknessRatio | unknown | math | 50 | method: double GetThicknessRatio() |
| Designer::GeometrySurface::GetOswaldsEfficiency | unknown | math | 50 | method: double GetOswaldsEfficiency() |
| Designer::GeometrySurface::GetFinRefRadius_ft | unknown | math | 50 | method: double GetFinRefRadius_ft() |
| Designer::Designer::Vehicle::SetVehicleControlConfiguration | event_handling | math | 50 | method: void SetVehicleControlConfiguration(VehicleControlCo |
| Designer::Designer::Vehicle::GetVehicleControlConfiguration | event_handling | math | 50 | method: VehicleControlConfig GetVehicleControlConfiguration( |
| Designer::Designer::Vehicle::GetVehicleControlConfigurationString | event_handling | math | 50 | method: QString GetVehicleControlConfigurationString() const |
| Designer::Designer::Vehicle::IsAircraft | unknown | math | 50 | method: bool IsAircraft() |
| Designer::Designer::Vehicle::IsWeapon | event_handling | math | 50 | method: bool IsWeapon() |
| WsfImageProcessor::ReceiveMessage | model_update | math | 50 | method: bool ReceiveMessage(double aSimTime, const WsfMessag |
| ObjectTest::GetDraw | output | math | 50 | method: double GetDraw() const |
| ObjectTest::GetRequiredDetected | unknown | math | 50 | method: double GetRequiredDetected() const |
| wkf::RegionExtents::X1 | event_handling | math | 50 | method: double X1() const |
| wkf::RegionExtents::Y1 | event_handling | math | 50 | method: double Y1() const |
| wkf::RegionExtents::X2 | event_handling | math | 50 | method: double X2() const |
