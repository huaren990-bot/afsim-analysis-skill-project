# migration-generation 操作留痕 — REQ-002

> **日期**：2026-07-01
> **操作类型**：迁移代码生成（SKILL: migration-implementer）
> **需求编号**：REQ-002
> **需求名称**：编队沿航线飞行机动模型设计

## 操作描述

执行 `skill/migration-builder/migration-generation/SKILL.md` 全部 7 个步骤，基于已确认的 FU-design v1.0 和 migration-function.jsonl（12 条记录），为 REQ-002 生成完整的 SDD、头文件、实现文件、测试 Demo、README 和 CMakeLists。

## 输出文件清单

| 文件 | 路径 | 行数 | 说明 |
|------|------|------|------|
| SDD | `docs/migration/REQ-002/REQ-002-SDD.md` | 587 | 9 个 FU 的软件设计说明 |
| 头文件 | `tests/migration_src/REQ_002/REQ_002.h` | 455 | 类型定义 + 12 函数声明 + 主类 |
| 实现文件 | `tests/migration_src/REQ_002/REQ_002.cpp` | 830 | 12 函数 Clean-room 实现 |
| 测试 Demo | `tests/migration_src/REQ_002/REQ_002_test.cpp` | 204 | 3 集成测试用例 |
| README | `tests/migration_src/REQ_002/README.md` | 86 | 编译/依赖/运行说明 |
| CMakeLists | `tests/migration_src/REQ_002/CMakeLists.txt` | 31 | CMake 构建配置 |
| 操作留痕 | `docs/records/2026-07-01-migration-generation-record-REQ-002.md` | 本文件 | — |

## 决策依据

### 全局设计决策
1. **代码目录**：`tests/migration_src/REQ_002/`，与 REQ-001 并列
2. **单位策略**：全部 SI 单位，含 Imperial→SI 转换常量。FU-006 内部保留 Imperial
3. **Clean-room**：所有实现标注 AFSIM 源引用但不复制源码
4. **构建系统**：CMake 3.14+，C++17，Eigen 3.x

### 各 FU 实现决策

| FU | 实现策略 | 简化程度 | 关键决策 |
|----|---------|---------|---------|
| FU-001 | O(1) 向前搜索 + 段内投影 | 简化版 | 静态 prev_leg_index 缓存；首次遍历全段 |
| FU-002 | 三维风矢量投影 + 跨段推进 + 线性插值 | 完整版 | 小跨度平面 atan2；风投影 clamp 防止大幅跳变 |
| FU-003 | 最近点裁剪 + 保底逻辑 | 基础 | 纯函数；保底至少返回 1 个航路点 |
| FU-004 | InterpCurve1D 查表 + 恒定燃油率 | 简化版 | 推力曲线数据为全局静态；默认常量 50 kN 兜底 |
| FU-005 | ISA 简化大气 + 常量气动系数 | 简化版 | 首版用常量 CL/CD/CY；力矩全零 |
| FU-006 | 20 PID + 增益调度 + anti-windup | 完整版 | 默认增益占位；动压下界 clamp 50 Pa；4 通道级联 |
| FU-007 | 控制-稳定解耦（一阶跟踪+二阶阻尼+一阶滞后） | 完整版 | SAS 参数全局静态；质量比率影响限幅 |
| FU-008 | Heun 预测-校正 + 欧拉方程 ω×Iω | 完整版 | FM1=FM0 简化；角速度限幅 100 rev/s；四元数归一化 |
| FU-009 | 顺序调度 PATH-01→KINEMATICS-02 | 调度层 | 全局静态状态；单线程 |

### 测试策略
- TC-001（正常）：100 步全管线仿真，验证燃油递减、速度有界
- TC-002（边界）：dt=0、空航线、零速度、零燃油、超大步长
- TC-003（异常）：退化四元数、负燃油、mass=0

### 与 migration-function.jsonl 的一致性
- 12 个函数全部在 .h 中声明，.cpp 中实现
- 函数签名与 migration-function.jsonl 一致
- AFSIM 源引用标注在注释中
