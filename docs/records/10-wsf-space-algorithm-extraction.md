# 10 — wsf_space 模块算法提取记录

**日期**：2026-06-11
**状态**：完成（初始 8 张卡片，后拆分为 12 张独立算法卡片 + 7 份接口规格 + 1 份汇总文档）
**对应阶段**：阶段 2 — 算法提取
**使用的 Skill**：`afsim-algorithm-extractor`

---

## 分析范围

`wsf_space` 模块的全部相关函数和类，从 `workspace/source-index/core/` 中的 4 个索引文件（function-index.jsonl, file-index.jsonl, symbol-index.jsonl, dependency-index.jsonl）驱动，结合实际 C++ 源码（`source_root/src/core/wsf_space/source/`）完成分析。

## 产出清单

### docs/algorithms/（算法卡片 × 12 — 已拆分杂揉卡片）

| 文件 | 内容 | 可移植性 |
|------|------|---------|
| `space-norad-orbital-propagator-card.md` | NORAD SGP4/SDP4 轨道传播器 — 5 种星历类型的完整数学推导（Kepler 方程、J2/J3/J4 摄动、大气阻力、日月引力） | 中 |
| `space-integrating-propagator-card.md` | 数值积分传播器 — Prince-Dormand 8(7)13M RK 方法、自适应步长控制、FSAL 优化 | 高 |
| `space-orbital-event-condition-card.md` | 轨道事件条件 — 二分搜索求根 + 14 种事件条件的 Objective 函数定义 | 高 |
| `space-lambert-solver-card.md` | Lambert 问题求解器 — f/g 级数展开（纯 Lambert 边界值问题） | 高 |
| `space-angles-only-iod-card.md` | 仅角度初始轨道确定 — Gauss 方法变体，从两次传感器角度测量迭代求解轨道 | 高 |
| `space-piecewise-exponential-atmosphere-card.md` | 分段指数大气密度模型 — 按高度分段的指数衰减 | 高 |
| `space-jacchia-roberts-atmosphere-card.md` | Jacchia-Roberts 大气密度模型 — 含 $F_{10.7}$、$K_p$ 修正的高层大气高保真模型 | 高 |
| `space-nasa-breakup-model-card.md` | NASA 碎片解体模型 — 幂律分布、A/M 分布、ΔV 分布、动量守恒修正 | 高 |
| `space-orbital-maneuvers-card.md` | 经典轨道机动模型 — ΔV 脉冲机动、要素变更、Hohmann 转移 | 高 |
| `space-rendezvous-targeting-card.md` | 轨道交会与拦截瞄准 — Lambert 驱动的最优转移轨道搜索 | 高 |
| `space-libration-point-card.md` | 拉格朗日点 — 限制性三体问题、Gamma 系数 Newton 求解、L1-L5 位置 | 高 |
| `space-conjunction-assessment-card.md` | 航天器交会评估 — 碰撞概率计算 | 高 |
| `space-solar-terminator-card.md` | 太阳光照终止线 — 地影判定 | 高 |

### workspace/extracted-algorithms/（接口规格 × 7）

| 目录 | 文件 | 内容 |
|------|------|------|
| `space-norad-propagator/` | `interface-spec.md` | TLE 数据结构、传播器类、核心数学函数接口 |
| `space-integrating-propagator/` | `interface-spec.md` | RK 积分器基类模板、PD78 系数定义、动力学项抽象接口 |
| `space-lambert-solver/` | `interface-spec.md` | Lambert f/g 函数、速度求解 |
| `space-angles-only-iod/` | `interface-spec.md` | 仅角度初轨确定、圆轨道几何解 |
| `space-atmosphere-model/` | `interface-spec.md` | 大气密度计算接口（分段指数 + Jacchia-Roberts）、阻力加速度 |
| `space-breakup-model/` | `interface-spec.md` | 碎片 Fragment 结构体、爆炸/碰撞解体接口 |
| `space-orbital-maneuvers/` | `interface-spec.md` | ΔV 机动、交会瞄准接口 |
| `space-libration-point/` | `interface-spec.md` | L1-L5 位置计算、Gamma 系数接口 |

### docs/algorithms/（汇总文档）

| 文件 | 内容 |
|------|------|
| `CompendiumofAlgorithms.md` | 全部 11 个算法的汇总目录（含已有的 3 张运动学卡片 + 本轮 8 张空间力学卡片）|

---

## 关键发现

1. **wsf_space 模块采用了高度模块化的架构**：
   - 传播器（Propagator）与积分器（Integrator）分离 — 可以独立替换数值方法
   - 动力学模型（Dynamics）与动力学项（DynamicsTerm）分离 — 力模型可插拔组合
   - 事件条件（Condition）与传播器解耦 — 使用二分搜索框架，对任意传播器通用

2. **NORAD 传播器实现了完整的 Spacetrack Report #3 标准**：
   - 5 种星历类型（SGP/SGP4/SGP8/SDP4/SDP8），自动按轨道周期选择
   - 深空模块（Deep_dpinit/dpsec/dpper）含 12h 共振轨道和地球同步轨道的特殊处理
   - 单位混用严重：内部 km、km/min、rad/min；输出转换为 SI（m、m/s）

3. **数值积分传播器使用 Prince-Dormand 8(7)13M 格式**：
   - 8 阶精度 + FSAL 优化（实际 12 次函数评估/步）
   - 自适应步长控制基于嵌入格式误差估计（接受/拒绝步 + 步长缩放）
   - 支持 $L_\infty$ 和 $L_2$ 两种误差范数

4. **NASA 碎片模型经验系数丰富**：
   - 碎片数分布、A/M 分布、ΔV 分布三套独立经验公式
   - 区分爆炸（6 倍 S 因子）与碰撞（0.1 × M^0.75）场景
   - 碰撞再细分为灾难性（完全碎裂）和非灾难性（仅撞击体碎裂）

## 未覆盖内容

- `wsf_space` 中 Kalman 滤波轨道确定的详细协方差传播公式
- Solar Terminator（太阳终结线）的完整几何计算
- Conjunction Analysis（交会分析）的碰撞概率积分
- Constellation（星座）Walker/自定义星座的覆盖分析
- 轨道瞄准优化（Orbital Targeting Cost）的多目标代价函数

## 与已有算法的对照

| 维度 | 已有算法（运动学） | 本轮算法（空间力学） |
|------|------------------|-------------------|
| 物理域 | 大气层内飞行器 6DOF | 轨道力学（二体/受摄） |
| 传播方法 | Heun 预测-校正 | SGP4/SDP4 解析 + RK8(7) 数值积分 |
| 力模型 | 气动+推进+起落架+重力 | 引力+J2+日月+大气阻力 |
| 事件 | 触地/起飞 | 近地点/远地点/节点/地影 |
| 碎片/机动 | — | 爆炸/碰撞碎片 + 轨道机动 |
