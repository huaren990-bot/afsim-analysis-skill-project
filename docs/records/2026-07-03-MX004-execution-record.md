# MX004 — 需求功能参考实现生成执行记录

> **时间**: 2026-07-03
> **编号**: MX004
> **来源文档**: `E:\mine\撑到几号算几号\afsim设计\MX004_tm.docx`
> **关联文档**: [MX004-reference.md](../requirements/MX004/MX004-reference.md)、[MX004-reference-evidence-summary.md](../requirements/MX004/MX004-reference-evidence-summary.md)

---

## Step 0: 预处理确认

| 确认项 | 状态 | 说明 |
|--------|------|------|
| 需求编号 | ✅ MX004 | 从 docx 文件名提取 |
| 功能需求描述 | ✅ 明确 | 实体-组件矩阵：11 个实体模型 × 12 个功能组件 |
| 可依据的其他文献 | ✅ 无额外文献 | 仅 docx 文件提供功能需求 |
| AFSIM 架构文档 | ✅ 就绪 | `docs/architecture/afsim-architecture.md`（17,342 源文件、107 模块、5,941 类、45,603 方法） |
| AFSIM 代码索引 | ✅ 就绪 | `workspace/source-index/function-index.jsonl`（44,363 条索引） |
| AFSIM 算法文档 | ✅ 就绪 | `docs/algorithms/CompendiumofAlgorithms.md`（32 张算法卡片） |
| AFSIM 演示参考 | ✅ 就绪 | `source_root/afsim-2_9/demos/`（6,304 文件、67+ 场景） |
| AFSIM 使用文档 | ✅ 就绪 | `source_root/afsim-2_9/documentation/`（5,075 文件） |

---

## Step 1: 加载 AFSIM 上下文

| 资源 | 路径 | 用途 |
|------|------|------|
| 架构总览 | `docs/architecture/afsim-architecture.md` | 了解 AFSIM 9 个子系统和 8 阶段仿真生命周期 |
| 算法卡片索引 | `docs/algorithms/CompendiumofAlgorithms.md` | 32 个算法（15 飞行动力学、19 太空轨道力学）快速导航 |
| 函数索引 | `workspace/source-index/function-index.jsonl` (44,363 行) | 按功能关键词搜索对应类和方法的索引 |
| 演示目录 | `source_root/afsim-2_9/demos/` | 验证 kinematic_mover、electronic_warfare、comm 等演示存在 |
| 使用文档 | `source_root/afsim-2_9/documentation/` | 总体概览，未逐页阅读（实体-组件矩阵需求简单明确） |

---

## Step 2: 需求解析

MX004 需求文档为 docx 表格格式，含 11 种仿真实体模型和 6 大类功能组件。

从矩阵中提取 12 个独立功能组件：

| # | 功能组件 | 类别 | 涉及实体 |
|---|---------|------|---------|
| 1 | 空中机动 | 机动 | AA无人机、BB无人机、电子战飞机 |
| 2 | 陆上机动 | 机动 | 指挥所、EE雷达车、运弹车、EE发射车、EE指挥车 |
| 3 | 导弹机动 | 机动 | EE弹、远箱火弹 |
| 4 | 可见光探测 | 探测 | AA无人机 |
| 5 | 雷达探测 | 探测 | BB无人机、电子战飞机、EE雷达车、运弹车、EE发射车、EE弹 |
| 6 | 惯性导航 | 探测 | 远箱火弹 |
| 7 | 自杀攻击 | 火力 | AA无人机、BB无人机 |
| 8 | 导弹火力 | 火力 | AA无人机、BB无人机、EE弹、远箱火弹 |
| 9 | 制导武器发射 | 火力 | EE发射车 |
| 10 | 报文发送 | 通信 | AA无人机、BB无人机、电子战飞机、指挥所、EE雷达车、EE发射车、EE指挥车 |
| 11 | 毁伤 | 毁伤 | 全部 11 个实体 |
| 12 | 电子干扰 | 干扰 | 电子战飞机 |

---

## Step 3: AFSIM 参考实现查找

### 查找方法

1. **function-index.jsonl 搜索**：对每个功能组件的关键词（如 "AirMover"、"EOIR"、"Jammer"）在 44,363 行 JSONL 索引中 grep 搜索。
2. **CompendiumofAlgorithms.md 搜索**：检查 32 个算法卡片中与各功能组件相关的卡片。
3. **源码逐行验证**：对候选匹配函数，打开对应 `.hpp` 头文件阅读完整源码（共验证 7 个关键文件）：
   - `WsfAirMover.hpp` / `WsfGroundMover.hpp` / `WsfGuidedMover.hpp` (及基类)
   - `WsfEOIR_Sensor.hpp` / `WsfRadarSensor.hpp`
   - `WsfWeaponComponent.hpp` / `WsfMobilityAndFirepowerLethality.hpp` / `WsfRF_Jammer.hpp`
   - `WsfImplicitWeapon.hpp` / `WsfExplicitWeapon.hpp`
   - `WsfMessage.hpp` / `WsfNetworkInterface.hpp` / `WsfJTIDS_Terminal.hpp` 等
4. **演示/文档搜索**：检查 `demos/kinematic_mover/`、`demos/electronic_warfare/`、`demos/comm/` 等目录。

### 源码逐行验证记录

| 功能组件 | 验证源文件 | 关键发现 |
|---------|-----------|---------|
| 空中机动 | `wsf/source/mover/WsfAirMover.hpp` | 轻量级特化，继承 WsfWaypointMover，新增 HAT/起降/碰撞/毁伤评估 |
| 陆上机动 | `wsf/source/mover/WsfGroundMover.hpp` | 极简特化，主要区别是空间域返回 `WSF_SPATIAL_DOMAIN_LAND` |
| 导弹机动 | `wsf_mil/source/mover/WsfGuidedMover.hpp` | 完整 Newtonian 动力学模型，支持梯形/RK2/RK4 积分、多级推进、TVC、坐标帧切换 |
| 可见光探测 | `wsf_mil/source/sensor/WsfEOIR_Sensor.hpp` | 成像传感器（每帧检测所有物体），含 EOIR_Mode/ErrorModel/Scheduler，但无多模式自动切换 |
| 雷达探测 | `wsf/source/sensor/WsfRadarSensor.hpp` | 完整的雷达模型：RadarBeam + RadarMode + Marcum-Swerling 检测器 + 杂波衰减 |
| 导弹火力 | `wsf_mil/source/weapon/WsfImplicitWeapon.hpp`、`WsfExplicitWeapon.hpp` | 隐式武器（无飞行实体）+ 显式武器（创建独立飞行平台），完整的发射-制导-引爆-评估链路 |
| 毁伤 | `wsf_mil/source/weapon/WsfMobilityAndFirepowerLethality.hpp` (52 方法) | MFK 四级毁伤（无/M/F/M+F/K）+ 目标类型易损性表 + 对抗措施评估（方位/距离/时间约束） |
| 电子干扰 | `wsf_mil/source/weapon/WsfRF_Jammer.hpp` | 多模式/多波束/多瞄准点架构，噪声/脉冲/相干三功率类型，压制/欺骗/假目标 10+ 种 EA 技术 |
| 报文发送 | `wsf/source/WsfMessage.hpp`、`wsf/source/comm/WsfComm.hpp` | 消息基类 + 7 层 OSI 协议栈 + JTIDS TDMA 终端 + Link16 J-series |

### 覆盖度评估

| 覆盖度 | 数量 | 功能组件 |
|--------|------|---------|
| ✅ 完全覆盖 | 9 | 空中机动、陆上机动、导弹机动、雷达探测、导弹火力、制导武器发射、报文发送、毁伤、电子干扰 |
| ⚠️ 部分覆盖 | 2 | 可见光探测（缺多模式自动切换）、自杀攻击（无专用类，需组合实现） |
| 🆕 缺失 | 1 | 惯性导航（AFSIM 无独立 INS 组件，需从领域文献设计） |
| ❓ 无法判断 | 0 | — |

---

## Step 4: 文档生成

- **MX004-reference.md**：按 SKILL.md 模板生成，含 12 个功能组件的完整参考设计（每个组件含：功能描述、系统/模块/类级/方法层级、Mermaid 算法流程图、输入/输出/配置/依赖表格、非功能需求、参考证据）。
- **MX004-reference-evidence-summary.md**：紧凑单表格式的证据摘要。

---

## 待人工确认事项

- [ ] 检查 12 个功能组件分解是否完整无遗漏
- [ ] 确认可见光探测的 "部分覆盖" 判定是否可接受（是否需要在多模式切换方面补充外部设计）
- [ ] 确认自杀攻击的 "部分覆盖" 判定是否可接受（是否需要在自杀无人机专用类方面补充设计）
- [ ] 确认惯性导航的 "缺失" 判定，是否需要作为独立组件实现（或接受 mover 内置积分器满足需求）
- [ ] 审核各功能的算法流程图和公式是否正确
- [ ] 确认 AFSIM 源码路径引用是否准确
