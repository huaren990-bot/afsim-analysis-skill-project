# FU 设计生成操作留痕 — 2026-06-18（v0.3 迭代更新）

> **日期**：2026-06-18 17:00（初版生成）→ 2026-06-22 09:21（v0.3 迭代）
> **操作**：根据更新后的 SKILL.md 和 template_FU-migration.md 重新生成 FU 设计文档，并根据人工审阅反馈进行 v0.3 迭代
> **状态**：v0.3 已确认

---

## 一、模板变更说明（v0.1 → v0.2）

| 变更类型 | 内容 |
|----------|------|
| **新增** | 全局「实现流程」章节（mermaid sequence diagram + 接口信息表） |
| **新增** | 每 FU「算法流程图」（mermaid flowchart）+ 「关键算法」公式（带引用链接） |
| **新增** | API 定义中的「补充参数详细表」 |
| **新增** | 耦合度章节中的「依赖」小节（头文件/库/参考源） |
| **移除** | `source: afsim` / `source: novel` 双模板区分 → 统一模板 |
| **移除** | 「数据类型映射表」整个小节（合并到全局章节） |
| **移除** | 「实现方案」整个小节（接口转换/移除/保留/新增 4 子节） |
| **移除** | 「参考来源与算法依据」详细表格 → 简化为算法流程中的引用链接 |
| **移除** | FU header 中的 `AFSIM 源位置`、`源码行数`、`迁移策略`、`风险评估` 字段 → 简化到「来源类型」和「依赖」中 |
| **重组** | 每 FU 小节顺序：功能概述 → 算法流程 → API → 耦合度 → 状态 → 错误处理 → 风险 |
| **路径变更** | 输出目录：`docs/migration/` → `docs/migration/preliminary-migration-plan/` |

## 二、SKILL.md 路径变更

| 变更点 | 旧值 | 新值 |
|--------|------|------|
| 主输出路径 | `docs/migration/<req>-FU-design.md` | `docs/migration/preliminary-migration-plan/<req>-FU-design.md` |
| 确认版路径 | 同一文件状态变更 | `docs/migration/preliminary-migration-plan/<req>-FU-design-confirmed.md` |

## 三、输出文件清单

| 文件 | 路径 | 状态 |
|------|------|------|
| FU 迁移设计文档 | `docs/migration/preliminary-migration-plan/REQ-001-FU-design.md` | ✅ 已更新 (v0.2) |
| 旧版文档 | `docs/migration/REQ-001-FU-design.md` | ❌ 已删除 |
| 迁移日志 | `workspace/migration/migration-function.jsonl` | ✅ 已更新 |
| 操作留痕（本文件） | `docs/records/2026-06-18-FU-design-generation-record.md` | ✅ 已更新 |

## 四、v0.3 迭代（2026-06-22）—— 人工审阅反馈

### 反馈汇总

| FU | 修改要求 | 处理结果 |
|-----|----------|----------|
| FU-001 | 多线程安全 + 支持AB | ✅ 全状态变量加 m_mutex_；AB 已确认支持 |
| FU-002 | 多模态气动构型切换 | ✅ 新增 `setConfiguration()` + `AeroConfig` 枚举 + 增量表集 |
| FU-003 | 多线程安全 + 姿态轨迹采集 + 起落架 | ✅ 全状态加锁；新增 `collectTrajectory()` + 环形缓冲；新增起落架力源 |
| FU-004 | 俯仰/偏航交叉耦合 + 多线程安全 | ✅ 新增交叉耦合公式 + `k_y_pitch`/`k_z_yaw` 系数；全状态加锁 |

### 新增 API

| FU | 新增函数 | 说明 |
|-----|----------|------|
| FU-002 | `setConfiguration(AeroConfig)` | 多模态构型切换 |
| FU-003 | `collectTrajectory(RigidBodyState)` | 飞行轨迹采集 |

### 全局变更

- 所有 FU 的状态变量 **线程安全** 列已从"否"更新为"是"
- 所有 FU 新增 `std::mutex` 成员用于多线程保护
- 含 mutex 的类 **禁止拷贝，支持移动**
- 所有"待确认"风险项已全部转为"已确认"
- 人工确认 checkbox 全部标记 [x]，待最终确认

## 五、下一步

1. 人工审阅 `docs/migration/preliminary-migration-plan/REQ-001-FU-design.md`
2. 对每个 FU 在第 9 节（人工确认）勾选 Y/N
3. 确认后进入 `migration-generation/SKILL.md`（代码实现 + SDD）


## 六、v0.3 最终确认（2026-06-22）

| 项目 | 内容 |
|------|------|
| **确认版本** | v0.3 confirmed |
| **确认日期** | 2026-06-22 |
| **确认文件** | `docs/migration/preliminary-migration-plan/REQ-001-FU-design-confirmed.md` |
| **状态** | 已确认可执行计划 |
| **下一步** | 执行 `migration-generation/SKILL.md` 进入代码实现阶段 |

### 确认的 4 个 FU 设计要点

| FU | 关键确认项 |
|-----|-----------|
| FU-001 | 多线程安全(m_mutex_) + AB支持(m_afterburner_present_) |
| FU-002 | 多模态构型切换(setConfiguration + AeroConfig枚举) + 多线程安全 |
| FU-003 | 多线程安全(m_state_mutex_) + 姿态轨迹采集(collectTrajectory) + 起落架初期实现 |
| FU-004 | 俯仰/偏航交叉耦合补偿(k_y_pitch/k_z_yaw) + 多线程安全 |
