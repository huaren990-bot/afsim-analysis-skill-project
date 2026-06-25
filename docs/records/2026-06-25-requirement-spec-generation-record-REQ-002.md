# 需求规范生成过程记录

> **日期**：2026-06-25
> **执行 Skill**：requirement-spec-generator
> **输入文档**：docs/requirements/REQ_002/0_formation_move_along_path.md
> **输出文档**：docs/requirements/structured_requirement_doc/REQ-002-requirement-formation-move-along-path.md

---

## 1. 上下文加载

### 1.1 已加载资产

| 资产 | 路径 | 加载状态 | 关键内容 |
|------|------|----------|----------|
| AFSIM 核心架构报告 | docs/architecture/core/afsim-architecture.md | ✅ | WSF 仿真生命周期、WsfPlatform 编队管理 |
| AFSIM 插件架构报告 | docs/architecture/wsf_plugins/afsim-architecture.md | ✅ | wsf_six_dof maneuver/formation 子目录、wsf_p6dof 编队动作库 |
| 算法卡片汇总 | docs/algorithms/CompendiumofAlgorithms.md | ✅ | 编队汇合/位置保持/追击三状态机动控制算法 |
| 功能索引 (plugins) | workspace/source-index/wsf_plugins/function-index.jsonl | ✅ | 编队/机动相关模块级条目 |
| REQ-001 规范文档 | docs/requirements/REQ_002/0_formation_move_along_path.md | ✅ | 单机六自由度作为子流程复用 |

---

## 2. 需求解析

### 2.1 模糊需求分析

原需求文档 `0_formation_move_along_path.md` 提出 3 个目标设计：

1. **飞机编队沿着设定的期望航线（坐标数组）执行机动**
2. **用单个飞机模型代替整个编队模型进行机动计算**
3. **使用六自由度模型计算姿态、位置和剩余油量**

### 2.2 需求分解决策

| 决策 | 内容 | 依据 |
|------|------|------|
| 拆分为 5 个规范需求 | 航线推进 / 逐机六自由度 / 姿态合成 / 速度油量 / 集成层 | 算法粒度分离、复用 REQ-001 |
| REQ-002-FORMATION-02 复用 REQ-001 | 单机六自由度算法已在 REQ-001 中规范定义 | 避免重复，引用 REQ-001 文档 |
| 集成层（FORMATION-05）独立 | 纯调度逻辑，数据分发与收集 | 明确集成点便于下游实现 |
| 数据类型（Point/Posture）不重新定义 | 沿用需求文档中的 C++ 结构体 | 避免冗余定义 |

### 2.3 AFSIM 算法映射

| 规范需求 | AFSIM 参考 | 状态 | 匹配度 |
|---------|-----------|------|--------|
| FORMAT-01 航路段映射 | wsf_six_dof/wsf_p6dof maneuver/ 航路管理 | ❌（自有缺失） | 中 — AFSIM 有航路管理但需提取 |
| FORMAT-01 航线推进 | 编队三状态机动控制 KeepStation（ECS 坐标系） | ❌（自有缺失） | 中 — AFSIM 编队飞行逻辑可参考 |
| FORMAT-02 单机六自由度 | 同 REQ-001-SIXDOF-01 全量算法 | ❌（自有缺失） | 高 — 完全复用 REQ-001 |
| FORMAT-03 姿态合成 | 无独立 AFSIM 算法，Observer/EventPipe 机制 | ❌（自有缺失） | 低 — 纯数据搬运 |
| FORMAT-04 速度油量 | 无独立 AFSIM 算法 | ❌（自有缺失） | 低 — 纯数据搬运 |
| FORMAT-05 编队集成 | WsfPlatform::Update → Mover 驱动 | ❌（自有缺失） | 中 — AFSIM 框架级调度 |

### 2.4 非功能需求判定

| 规范需求 | 多线程 | 判定依据 |
|---------|--------|---------|
| FORMAT-01 | ❌ 不需要 | 航线推进为单编队内串行逻辑 |
| FORMAT-02 | ✅ 需要 | 多机独立计算，天然数据并行 |
| FORMAT-03 | ✅ 需要 | 同 02 |
| FORMAT-04 | ✅ 需要 | 同 02 |
| FORMAT-05 | ✅ 需要（共享状态） | 集成层分发/收集含共享缓冲区 |

---

## 3. 简化方案设计

| 规范需求 | 算法数 | 简化方案数 | 覆盖范围 |
|---------|--------|-----------|---------|
| FORMAT-01 | 3（航路段映射/航线推进/剩余航线裁剪） | 6 个方案 | 精确投影→最近点、全搜索→向前搜索、风速修正简化、弧线简化 |
| FORMAT-02 | 4（目标位置/推进/气动/积分器） | 4 个编队特有方案 | ECS→航向旋转、固定队形、统一参数、尾流忽略 |
| FORMAT-03 | 2（姿态汇总/步长自适应） | 2 个方案 | 单帧输出、线性插值 |
| FORMAT-04 | 3（速度汇总/油量汇总/步长自适应） | 同 03 | — |
| FORMAT-05 | 1（集成调度） | 2 个方案 | 串行单线程、跳过队形检查 |

---

## 4. 待人工确认清单

| # | 确认项 | 类型 | 影响范围 |
|---|--------|------|---------|
| 1 | 5 个规范需求的拆分粒度是否合理 | 结构决策 | 全部下游文档 |
| FORMAT-01 | 航路段映射是否需要简化（Y/N，含 2 子方案） | Y/N | 航线推进算法复杂度 |
| FORMAT-01 | 航线推进是否需要简化（Y/N，含 2 子方案） | Y/N | 推进精度 |
| FORMAT-02 | 目标位置计算是否需要简化（Y/N，含 2 子方案） | Y/N | 编队坐标系精度 |
| FORMAT-02 | 单机六自由度是否需要简化（Y/N） | Y/N | 复用 REQ-001 决策 |
| FORMAT-02 | 编队特有简化（统一参数/尾流忽略）是否采用 | Y/N | 仿真实时性 |
| FORMAT-03/04 | 步长自适应是否需要简化 | Y/N | 输出精度 |
| FORMAT-05 | 集成层是否需要多线程 | Y/N | 运行时架构 |
| 全局 | 非功能需求中的性能上限是否合理 | 数值 | 硬件选型 |