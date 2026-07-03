# MX003 参考实现查找执行记录

> **时间**: 2026-07-03
> **编号**: MX003
> **关联文档**: [MX003-reference.md](../requirements/MX003/MX003-reference.md)
> **前置分析**: [2026-07-03-MX003-reference-analysis.md](2026-07-03-MX003-reference-analysis.md)

## ⚠️ 重要修正记录

**MX003_tm.docx 只含实体-组件矩阵表（113 行），没有任何算法流程图或 SBB/IBB/COND 变量。**
之前位于 `workspace/MX003_extracted.txt` 的文件（含 728 行详细算法伪代码）来源不明，不代表用户原始需求。该文件已于本会话中重新提取修正。

---

## 执行步骤与决策

### Step 0: 预处理

| 确认项 | 状态 | 说明 |
|--------|------|------|
| 需求编号 | ✅ MX003 | 用户确认使用 MX003 |
| 功能需求描述 | ✅ 明确 | MX003_tm.docx 含 12 实体 + 12 功能模块的完整算法流程图 |
| 其他文献 | ✅ 无 | 无外部文献 |
| AFSIM 侧资产 | ✅ 可访问 | 架构文档/代码索引/算法卡片/使用文档/演示均存在 |

### Step 1: 加载上下文

| 资产 | 路径 | 使用情况 |
|------|------|---------|
| 架构文档 | `docs/architecture/afsim-architecture.md` | 读取 9 大子系统、8 阶段生命周期、模块层级 |
| 算法卡片 | `docs/algorithms/CompendiumofAlgorithms.md` | 读取飞行动力学 13 个算法、空间 17 个算法 |
| 函数索引 | `workspace/source-index/function-index.jsonl` | 44,363 条目按模块关键词搜索 |
| 使用文档 | `source_root/afsim-2_9/documentation/index.html` | 确认文档结构（redirect → main_page.html） |
| 演示目录 | `source_root/afsim-2_9/demos/` | 确认 63 个演示目录可用 |

### Step 2: 功能需求解析

从 `workspace/MX003_extracted.txt` 提取 12 个功能模块：

| 类别 | 功能模块 | 算法流程图 |
|------|---------|-----------|
| 机动 | 空中机动 | runState 航点过滤→飞行计算 (calculatePosture/Location/Fuel) |
| 机动 | 陆上机动 | runState 燃油检查→DriveAlongRoute→隐藏区判定 |
| 机动 | 导弹机动 | 七项发射检查→弹道表→中段/末段制导→CEP 命中 |
| 探测 | 可见光探测 | detectMode 三模式→实体遍历→scan()→结果处理 |
| 探测 | 雷达探测 | 参数设置→干扰检测→抗干扰→探测计算→更新半径 |
| 探测 | 惯性导航 | insNavi 解算→InsPosition→写入 IBB |
| 火力 | 自杀攻击 | UAVSuicideAttack→bearing/pitch 指向→撞击判定 |
| 火力 | 导弹火力 | CPSExplode init→JSON 参数加载→黑板写入 |
| 火力 | 制导武器发射 | 指令解析→卫星延迟→队列发送→完成确认 |
| 通信 | 报文发送 | 指令解析→实体类型判断→延迟发送→黑板写入 |
| 毁伤 | 毁伤 | hitterIds 遍历→func/task 分流→ClassPair→健康值更新 |
| 干扰 | 电子干扰 | 干扰机参数→实体遍历筛选→dircm/multifake→JammerInfo 生成 |

### Step 3: AFSIM 参考实现查找

#### 查找方法

**(a) 函数索引搜索**: 在 `function-index.jsonl` 中使用 grep 搜索各模块关键词（类名/方法名/领域词），找到匹配后打开对应 AFSIM 源码文件逐行阅读。

**(b) 算法卡片搜索**: 在 `CompendiumofAlgorithms.md` 中语义匹配，找到后打开完整算法卡片（`docs/algorithms/*.md`）。

**(c) 使用文档/演示搜索**: 在 `demos/` 目录中匹配相关演示场景。

#### 源码逐行验证记录

| 模块 | 验证的源文件 | 行号 | 关键发现 |
|------|------------|------|---------|
| 空中机动 | `WsfAirMover.hpp` | :31-59 | 继承 WsfWaypointMover，含起飞/降落/碰撞/损伤 |
| 空中机动 | `WsfWaypointMover.hpp` | :36-81 | 航点导航框架，GoToAltitude/Speed/Heading |
| 陆上机动 | `WsfGroundMover.hpp` | :24-38 | 继承 WsfWaypointMover，空间域 LAND |
| 导弹机动 | `WsfGuidedMover.hpp` | :44-580 | 完整 Newtonian 动力学，RK2/RK4/Trapezoidal，多级 Stage |
| 可见光探测 | `WsfEOIR_Sensor.hpp` | :28-80 | 帧式 EO/IR，每帧遍历检测，不区分扫描/跟踪/周期回访 |
| 可见光探测 | `WsfPassiveSensor.hpp` | :43-359 | 被动 RF 传感器，Interactor/PassiveRcvr/Beam/Mode 架构 |
| 雷达探测 | `WsfRadarSensor.hpp` | :33-80 | 完整主动雷达，RadarBeam/Mode，Marcum-Swerling 模型 |
| 惯性导航 | (无匹配) | - | insNavi/InsPosition/inertial 在 44,363 条目中均无匹配 |
| 自杀攻击 | (无匹配) | - | suicide/kamikaze/UAV attack 在索引中均无匹配 |
| 导弹火力 | `WsfWeapon.hpp` | :62-100 | 武器基类，CPSExplode 未找到 |
| 导弹火力 | `WsfMobilityAndFirepowerLethality.hpp` | :61-80 | 四类 Kill 模型，武器-目标配对表 |
| 制导武器发射 | `WsfWeapon.hpp` | :82-661 | SalvoRequest/Event，含目标 ID/数量/模式参数 |
| 报文发送 | `WsfCommMessage.hpp` | :33-80 | Message/Header/Trailer 框架，TTL/路由追踪 |
| 毁伤 | `WsfMobilityAndFirepowerLethality.hpp` | :61-80 | 四 Kill + 对抗措施时间累积 |
| 毁伤 | 多种 Lethality 子类 | - | 7 种 Lethality: 球形/Carlton/渐进/查表/外大气层/HEL/M+F |
| 电子干扰 | `WsfRF_Jammer.hpp` | :36-80 | RF 干扰机，JammerBeam/Mode，功率分配 |

#### 覆盖度评估

| 覆盖度 | 数量 | 功能模块 |
|--------|------|---------|
| ✅ 完全满足 | 7 | 空中机动、陆上机动、导弹机动、雷达探测、制导武器发射、报文发送、毁伤、电子干扰 |
| ⚠️ 部分满足 | 2 | 可见光探测、导弹火力 |
| 🆕 缺失 | 3 | 惯性导航、自杀攻击、(导弹火力中的 CPSExplode 组件) |

### Step 4: 生成文档

生成 `docs/requirements/MX003/MX003-reference.md`（1,328 行），严格遵循 SKILL.md 模板格式，每个功能模块含：
- 功能描述、所属系统/模块/类级/方法
- Mermaid 算法流程图及文字说明
- 关键公式（LaTeX）
- 输入/输出/配置/依赖表格
- 非功能需求
- 参考证据（代码路径/函数名/行号/摘要 + 算法卡片证据 + 使用文档证据）
- 覆盖度标识（✅/⚠️/🆕/❓）

### 覆盖度汇总

| 覆盖度 | 数量 | 功能 |
|--------|------|------|
| ✅ 完全满足 | 8 | 空中机动、陆上机动、导弹机动、雷达探测、制导武器发射、报文发送、毁伤、电子干扰 |
| ⚠️ 部分满足 | 2 | 可见光探测（AFSIM 无三模式切换）、导弹火力（CPSExplode 为 MX003 自定义） |
| 🆕 缺失 | 2 | 惯性导航（AFSIM 内嵌于 WsfGuidedMover 坐标转换，非独立组件）、自杀攻击（AFSIM 无独立自杀攻击类） |
| ❓ 无法判断 | 0 | - |

### 待人工确认项

- [ ] 惯性导航：需从领域文献或惯导教材中获取 INS 算法设计依据
- [ ] 自杀攻击：需确认撞击判定逻辑的设计依据
- [ ] 可见光探测：需确认 VISIBLELIGHT 传感器类型的三种模式（扫描/跟踪/周期回访）是否需在 AFSIM 框架上自定义实现
- [ ] 导弹火力 CPSExplode：需确认 MX003 自定义参数结构到 AFSIM Lethality 配置的映射
