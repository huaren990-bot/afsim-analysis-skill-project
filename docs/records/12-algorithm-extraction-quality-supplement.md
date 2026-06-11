# 12 — 阶段 2 算法提取全面质量补全记录

**日期**：2026-06-12
**状态**：完成
**关联 Skill**：`afsim-algorithm-extractor`、`afsim-source-cognition`
**触发来源**：对阶段 2 全部产出进行系统性质量检查后，发现 4 类结构性缺失

---

## 背景

在阶段 2（算法提取）产出 23 张算法卡片 + 8 份接口规格后，通过逐项对照 `skill/afsim-analyst/references/output-contracts.md` 和 `skill/afsim-algorithm-extractor/template_list/template_algorithm-card.md` 中的要求，发现以下系统性质量问题：

1. **所有 23 张卡片系统性缺失 4 个必填章节**：内部状态（Internal State）、变量映射表（Variable Mapping）、边界条件（Edge Cases）、提取策略（Extraction Strategy）
2. **2 张卡片内容严重不足**：space-orbital-event-condition（119行）和 space-piecewise-exponential-atmosphere（106行），缺失伪代码、入口点、验证计划
3. **16 个算法缺失接口规格文件**：workspace/extracted-algorithms/ 下仅 8 个目录有 interface-spec.md
4. **wsf_plugins 依赖索引结构不均衡**：210 条中 inheritance 仅 13 条（symbol-index 中有 8,962 条可用继承信息）

---

## 执行计划（4 阶段并行）

```
Phase A: 重写 2 张简陋卡片（各基于源码全量重写）
   ↓
Phase B: 为 23 张卡片补全 4 个章节（分 6 批次并行，每批 4 张）
Phase C: 为 16 个算法生成接口规格（分 4 批次并行）
Phase C-alt: 增强 wsf_plugins dependency-index
```

---

## Phase A — 重写扩充 2 张简陋卡片

### 产出

| 卡片 | 修改前行数 | 修改后行数 | 新增内容 |
|------|-----------|-----------|---------|
| space-orbital-event-condition-card.md | 119 | **509** | 完整伪代码（11 阶段 ~80 行）、6 层入口调用链、24 行源码位置表（含 Lines 和 Evidence level）、5 项框架依赖、5 项测试方案、4 个新增章节。修正了原卡片中 4 个不存在的条件类（TrueAnomalyCondition 等），基于源码确认为 12 个真实条件子类。 |
| space-piecewise-exponential-atmosphere-card.md | 106 | **342** | 完整伪代码（6 步骤）、4 条入口调用链、12 行源码位置表（含 Lines 和 Evidence level）、8 项框架依赖、5 项测试方案、4 个新增章节。确认 Vallado Table 8-4 (p.567) 为分段表数据来源。 |

### 关键决策

- 两张卡片均从 `source_root/afsim-2_9/swdev/src/core/wsf_space/source/` 读取了全部相关 `.hpp`/`.cpp` 源码
- orbital-event-condition 补充了 12 个条件子类的完整 Objective 函数说明
- piecewise-exponential-atmosphere 确认了 28 段分段表的静态常量性质

---

## Phase B — 为全部 23 张卡片补全 4 个缺失章节

### 执行策略

分 6 批并行处理：

| 批次 | 卡片 |
|------|------|
| 1 | rigid-body-integrator, p6dof-heun-integrator, autopilot-pid, aero-coefficient-model |
| 2 | pointmass-integrator, pointmass-sas, pointmass-aero, rigidbody-aero-coefficient |
| 3 | jet-engine, propulsion-fuel, norad-orbital-propagator, integrating-propagator |
| 4 | lambert-solver, angles-only-iod, orbital-maneuvers, rendezvous-targeting |
| 5 | nasa-breakup-model, jacchia-roberts-atmosphere, libration-point, conjunction-assessment |
| 6 | solar-terminator |

### 新增章节标准

| 章节 | 要求 | 示例 |
|------|------|------|
| **内部状态** | 表格记录跨帧持久化变量（变量名、类型、初始值、物理含义、更新时机） | 自动驾驶PID卡片记录了 PID 层 13 个成员变量 + CommonController 层 20 个 PID 实例 |
| **变量映射表** | `代码变量 \| 数学符号 \| 含义` 三列，覆盖所有关键公式中的变量 | 每张卡片 15-50 行不等 |
| **边界条件** | 数值稳定性保护、无效输入处理、限幅阈值、回退行为 | 每张卡片 6-12 条 |
| **提取策略** | 源文件清单、提取方法、函数识别来源、还原方式 | 标注 function-index.jsonl 中定位方式 |

### 关键发现

- 所有内容均基于源码 `.hpp` 文件中的成员变量声明确认，非凭空编造
- function-index.jsonl 中部分模板函数（如 RungeKutta 的 `TakeStep`）未被收录，需在提取策略中标注"向上映射到公开函数"
- 同一算法在不同 module（如 wsf_p6dof vs wsf_six_dof 同名类）的内部状态差异显著

---

## Phase C — 接口规格与依赖索引

### C1：16 个新接口规格

分 4 批并行生成，每批 4 个。输出至 `workspace/extracted-algorithms/<算法名>/interface-spec.md`。

每个接口规格包含 5 个标准章节：总体架构、核心接口定义（含中文注释的 C++ 声明）、典型调用模式（含中文注释的代码示例）、坐标系/单位约定、框架依赖解耦表。

新增的 16 个目录：

| # | 算法目录 |
|---|---------|
| 1 | flight-dynamics-rigid-body-integrator |
| 2 | flight-dynamics-p6dof-heun-integrator |
| 3 | flight-dynamics-autopilot-pid |
| 4 | flight-dynamics-aero-coefficient-model |
| 5 | flight-dynamics-rigidbody-aero-coefficient |
| 6 | flight-dynamics-pointmass-aero |
| 7 | flight-dynamics-pointmass-integrator |
| 8 | flight-dynamics-pointmass-sas |
| 9 | flight-dynamics-jet-engine |
| 10 | flight-dynamics-propulsion-fuel |
| 11 | space-orbital-event-condition |
| 12 | space-rendezvous-targeting |
| 13 | space-conjunction-assessment |
| 14 | space-solar-terminator |
| 15 | space-piecewise-exponential-atmosphere |
| 16 | space-jacchia-roberts-atmosphere |

最终覆盖率：24/24 目录全部包含接口规格文件。

### C2：wsf_plugins dependency-index 增强

从 `workspace/source-index/wsf_plugins/symbol-index.jsonl`（8,962 条含 `base_symbols` 的类）中提取**跨模块继承关系**，从关键 `.hpp` 文件提取 composition关系。

| 指标 | 修改前 | 修改后 | 变化 |
|------|--------|--------|------|
| inheritance | 13 | **208** | +195 |
| composition | 19 | **70** | +51 |
| include | 133 | 133 | — |
| build | 36 | 36 | — |
| registration | 8 | 8 | — |
| configuration | 1 | 1 | — |
| **总计** | **210** | **456** | **+246** |

---

## Phase D — 最终自检与汇总文档更新

### 验证结果

| 检查项 | 结果 |
|--------|------|
| 23 张卡片全部包含"内部状态"章节 | ✅ 通过 |
| 23 张卡片全部包含"变量映射表"章节 | ✅ 通过 |
| 23 张卡片全部包含"边界条件"章节 | ✅ 通过 |
| 23 张卡片全部包含"提取策略"章节 | ✅ 通过 |
| 24 个 workspace 目录全部包含 interface-spec.md | ✅ 通过 |
| dependency-index.jsonl ≥ 400 条 | ✅ 通过（456 条） |
| dependency-index.jsonl inheritance ≥ 200 | ✅ 通过（208 条） |
| dependency-index.jsonl composition ≥ 50 | ✅ 通过（70 条） |
| CompendiumofAlgorithms.md 统计算法数量与实际一致 | ✅ 已更正（24→23） |

---

## 最终产出统计

| 类别 | 修改前 | 修改后 |
|------|--------|--------|
| 算法卡片总数 | 23 | 23 |
| 卡片最短行数 | 106 | **180** |
| 卡片平均行数 | ~290 | **~405** |
| 最短卡片 | piecewise-exponential-atmosphere (106行) | lambert-solver (180行) |
| 最长卡片 | solar-terminator (466行, 现 707行) | solar-terminator (707行) |
| 4 个必填章节覆盖率 | 0/23 | **23/23** |
| 接口规格覆盖率 | 8/24 目录 | **24/24** 目录 |
| dependency-index 条目数 | 210 | **456** |

---

## 后续建议

1. **阶段 3（需求映射）**：当前 23 张算法卡片和 24 份接口规格已满足进入需求映射的质量要求，建议启动 `afsim-requirement-mapper`
2. **SKILL.md 再次完善**：本次补全中发现卡片模板与实际产出之间的结构偏差（模板中"内部状态"、"提取策略"等章节未被早期 agent 生成），建议在 SKILL.md 的输出章节中显式列出所有必填章节名称
3. **定期自检**：建议每次大规模算法提取后，执行与本次相同的系统性章节检查

---

## 关联文件

- `skill/afsim-algorithm-extractor/SKILL.md` — 算法提取 skill（168 行，已在上次完善中增强）
- `skill/afsim-analyst/references/output-contracts.md` — 输出合约（定义了 14 个必填章节）
- `docs/algorithms/` — 23 张算法卡片
- `docs/algorithms/CompendiumofAlgorithms.md` — 汇总文档（已更新计数）
- `workspace/extracted-algorithms/` — 24 个接口规格目录
- `workspace/source-index/wsf_plugins/dependency-index.jsonl` — 增强后的依赖索引（456 条）
- `docs/records/11-skill-improvement-from-algorithm-extraction.md` — 上次 skill 完善记录（本轮问题的上游预防措施）
