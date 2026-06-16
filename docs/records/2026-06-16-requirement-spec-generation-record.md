# 需求规范生成过程记录

> **日期**：2026-06-16
> **执行 Skill**：requirement-spec-generator
> **输入文档**：docs/requirements/external_requirements_doc/six_dof_UAV.md
> **输出文档**：docs/requirements/structured_requirement_doc/REQ-001-requirement-six-dof-UAV.md

---

## 1. 上下文加载

### 1.1 已加载资产

| 资产 | 路径 | 加载状态 | 关键内容 |
|------|------|----------|----------|
| AFSIM 核心架构报告 | docs/architecture/core/afsim-architecture.md | ✅ 完整 | WSF 仿真生命周期、WsfPlatform/Mover 模型、14 个核心类 |
| AFSIM 插件架构报告 | docs/architecture/wsf_plugins/afsim-architecture.md | ✅ 完整 | wsf_six_dof 模块（849 源文件）、PointMass/RigidBody 双模型架构 |
| 算法卡片汇总 | docs/algorithms/CompendiumofAlgorithms.md | ✅ 完整 | 23 个算法，wsf_six_dof 模块 8 个算法 |
| 功能索引 (core) | workspace/source-index/core/function-index.jsonl | ✅ 相关条目 | 燃油消耗率计算函数（CalcConsumptionRate、AddAltitudeEntry 等） |
| 功能索引 (plugins) | workspace/source-index/wsf_plugins/function-index.jsonl | ✅ 相关条目 | 运动学系统高层级功能分解（System/Module/Class 三级） |
| 输出模板 | skill/afsim-requirement-mapper/tamplate_list/template_requirement-specification.md | ✅ 完整 | 章节结构、表格表头、简化方案格式 |

### 1.2 缺失资产

| 资产 | 预期路径 | 实际路径 | 处理方式 |
|------|----------|----------|----------|
| 架构报告 | docs/architecture/afsim-architecture.md | docs/architecture/core/afsim-architecture.md + docs/architecture/wsf_plugins/afsim-architecture.md | 分别加载两份子目录文档 |
| 功能索引 | workspace/source-index/function-index.jsonl | workspace/source-index/core/function-index.jsonl + workspace/source-index/wsf_plugins/function-index.jsonl | 分别搜索两份索引 |

---

## 2. 需求解析

### 2.1 模糊需求分析

原需求文档 `six_dof_UAV.md` 仅包含一个需求：

> **REQ-001**：使用六自由度模型计算无人机的姿态和轨迹

**关键特征**：
- 使用对象：无人机/飞机
- 涉及组件：机动（Mover）
- 无原有设计参考
- 输入变量 14 个，输出变量 11 个
- 变量覆盖了完整的六自由度状态（位置、速度、姿态角、角速度）+ 燃油

### 2.2 AFSIM 算法映射

需求映射到 AFSIM `wsf_six_dof` 插件模块，该模块包含 849 个源文件，提供 PointMass（点质）和 RigidBody（刚体）双重模型。

| 算法流程序号 | 算法名称 | AFSIM 对应算法 | 可移植性 | 映射依据 |
|-------------|---------|---------------|---------|---------|
| 1 | 推进系统与燃油管理 | 推进系统与燃油管理模型 + 喷气发动机推力模型 | 高/中 | 燃油消耗率计算、多油箱传输、CG 插值 |
| 2 | 气动模型 | RigidBody 稳定性导数气动系数模型 + PointMass 气动力与旋转限幅模型 | 中/高 | 气动六分量计算、稳定性导数查表 |
| 3 | 六自由度积分器 | 刚体六自由度 Heun 积分器 + PointMass 六自由度 Heun 积分器 | 中/中高 | Heun 预测-校正法 + 四元数姿态积分 |
| 4 | 姿态控制系统 | PointMass 稳定增稳系统（SAS） | 中/高 | 控制-稳定解耦、三通道独立限幅 |

### 2.3 流程设计决策

**决策 1：将需求拆分为 4 个流程而非更多**
- 自动驾驶仪 PID 控制（算法 8）和喷气发动机推力模型（算法 7）被合并到推进系统和 SAS 流程中
- 原因：原需求仅强调"机动"计算，不涉及航路规划和目标跟踪，自动驾驶仪作为可选扩展保留

**决策 2：每个流程提供 2 个简化方案**
- 方案 1 通常是最激进的简化（如刚体→点质、多表→常数）
- 方案 2 通常是中等简化（如 Heun→欧拉、完整SAS→限幅）
- 简化方案均标注了复杂度变化（如 O(n²)→O(n)）

**决策 3：变量命名采用中文+数学符号双语标注**
- 满足模板要求"所有变量都用中文名"
- 同时提供数学符号便于开发人员实现

---

## 3. 输出文档结构验证

对照模板 checklist：

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 头部元信息（模糊需求文档、日期、编号） | ✅ | 已填写 |
| 需求映射表 | ✅ | REQ-001 → REQ-001-SIXDOF-01 |
| 需求实现流程表（含输入/输出/其他变量/常量/功能/是否需要简化） | ✅ | 4 行流程，所有列完整 |
| 输入变量使用中文名 | ✅ | 全部变量使用中文名+数学符号标注 |
| 输出变量列出 | ✅ | 11 个输出变量全部列出 |
| 每个算法有简化方案 | ✅ | 每个算法 2 个简化方案，含公式和复杂度对比 |
| Y/N 选项留给人工确认 | ✅ | 所有"是否需要简化"和"是否选择此方案"均为 Y/N |
| 参考文献 | ✅ | 8 条引用指向算法卡片和汇总文档 |
| 无省略号 | ✅ | 流程表完整列出，无省略 |
| 中文注释全覆盖 | ✅ | 所有章节均有中文说明 |

---

## 4. 待人工确认清单

| # | 确认项 | 位置 | 类型 |
|---|--------|------|------|
| 1 | 推进系统与燃油管理是否需要简化 | 流程表 #1 | Y/N |
| 2 | 气动模型是否需要简化 | 流程表 #2 | Y/N |
| 3 | 六自由度积分器是否需要简化 | 流程表 #3 | Y/N |
| 4 | 姿态控制系统是否需要简化 | 流程表 #4 | Y/N |
| 5-12 | 各简化方案选择 | 8 个简化方案 | Y/N |
| 13 | 是否需添加自动驾驶仪 PID 流程 | 扩展 | Y/N |

---

## 5. 执行摘要

- **输入**：1 个模糊需求（REQ-001）
- **输出**：1 个规范需求（REQ-001-SIXDOF-01），拆分为 4 个算法流程
- **简化方案**：8 个（每个算法 2 个方案）
- **引用 AFSIM 资产**：2 份架构报告 + 1 份算法汇总 + 2 份功能索引 + 8 张算法卡片
- **人工确认项**：12 个 Y/N 选项