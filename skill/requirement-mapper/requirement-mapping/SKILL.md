---
name: requirement-mapping
description: 将人工确认的需求规范与已验证的 AFSIM 参考实现、算法卡片以及目标系统能力进行逐条对照，生成需求覆盖结论、原子功能单元 FU、缺口报告、映射/追溯矩阵和机器可读 gap-specs。用于目标系统能力缺口分析和迁移前范围定义；不用于澄清未确认需求、仅凭索引猜测 AFSIM 功能或直接生成实现代码。
---

# AFSIM 需求映射

把“需求事实”“AFSIM 参考能力”“目标系统现状”作为三条独立证据链。相似函数名不等于覆盖，AFSIM 有实现也不等于可直接迁移。

## 输入门禁

必须有：

- `docs/requirements/<req-id>/2_<req-id>-requirement-<slug>.md`
- 需求原始来源
- AFSIM 参考实现文档或可用于现场验证的索引与源码
- 目标系统源码、索引或明确声明“按空系统处理”

可选但推荐：

- `workspace/requirements/<req-id>/<req-id>-afsim-evidence.jsonl`
- 完整算法卡片与接口规格
- 目标系统架构、接口和测试

若需求未确认，先使用 `requirement-spec-generator`。若 AFSIM 候选只有索引摘要，先使用 `requirement-reference-implementation` 或在本流程中完成源码验证。

## 工作流

### 1. 建立需求基线

枚举全部确认的原子需求 ID，记录来源、验收标准、优先级、输入输出、单位、坐标系、状态和非功能约束。后续所有产物必须覆盖同一 ID 集合。

### 2. 验证 AFSIM 侧

对每条需求：

1. 读取已验证证据 JSONL。
2. 打开命中的完整算法卡片和接口规格。
3. 抽查真实源码，确认 qualified name、路径、行号、接口、状态读写和生命周期。
4. 将候选标为 `verified`、`rejected` 或 `unknown`。

Compendium 与函数索引只能定位，不能单独支撑 `full`/`partial` 结论。

### 3. 验证目标系统侧

用目标源码、接口或测试证明当前能力。未提供目标系统时，显式记录 `target_assumption: empty_system`，不要把“未提供证据”写成“已证明不存在”。

### 4. 判定覆盖状态

使用统一状态：

- `satisfied`：目标系统满足需求及验收标准。
- `partial`：目标系统部分满足。
- `missing_with_afsim_reference`：目标系统缺失，AFSIM 有已验证参考。
- `missing_without_afsim_reference`：目标系统缺失，记录范围内未找到 AFSIM 参考。
- `unknown`：任一关键证据不足。

分别记录需求证据、AFSIM 证据、目标系统证据和差异，不把三者混写成一句结论。

### 5. 生成原子 FU

仅为 `partial`、`missing_with_afsim_reference` 和 `missing_without_afsim_reference` 生成 FU。FU 必须可独立实现或测试，并包含：

- 稳定 `fu_id` 与关联 `req_ids`。
- 功能描述与验收标准。
- 完整接口：类型、单位、坐标系、约束、错误处理和副作用。
- 上游输入来源、下游输出消费者、状态生命周期。
- 已验证 AFSIM 参考或明确的无参考检索范围。
- 目标系统差异、耦合度、风险和优先级。
- 建议方式：`direct_adaptation`、`partial_rewrite`、`cleanroom` 或 `novel`。

`novel` 只能用于记录范围内无 AFSIM 参考的缺口；需要外部文献时记录待检索项，不伪造引用。

### 6. 检查管线完整性

把 FU 排成数据流并检查：

- 中间输入来自外部边界、上游 FU 或明确状态。
- 中间输出被下游 FU、系统状态或最终验收使用。
- 类型、单位、坐标系和时间语义在边上匹配。
- 初始化、循环更新、事件触发、重置和终止完整。

外部输入、最终输出、诊断输出和持久状态应标注边界类型，不误报为孤儿参数。

### 7. 生成产物

按现有模板生成：

- `docs/requirements/<req-id>/3_<req-id>-requirement-gap-analysis.md`
- `docs/requirements/<req-id>/3_<req-id>-function-mapping-matrix.md`
- `docs/requirements/<req-id>/3_<req-id>-requirement-to-afsim-trace.md`
- `workspace/requirements/<req-id>/<req-id>-gap-specs.jsonl`

模板目录为 `skill/requirement-mapper/tamplate_list/`。保留该历史目录名，不在输出中创建第二套 `template_list`。

gap-specs 每行一个 FU，除模板字段外必须包含 `coverage_status`、`acceptance_criteria`、`dataflow` 和结构化 `evidence`。AFSIM 无参考时，`afs_reference` 的函数、类、路径和行号留空，并记录检索范围。

### 8. 验证和留痕

按 `SKILL_VERIFY.md` 验证，输出到 `docs/verification/requirement-mapping-<req-id>-verify-report.md`。在 `docs/records/<date>-requirement-mapping-<req-id>.md` 记录输入版本、证据边界、状态统计、FU 统计、未决问题和产物。

## 硬性门禁

- 四类产物中的 REQ/FU ID、状态和证据一致。
- 每条非 `unknown` 状态都有当前证据。
- 每个 AFSIM 源引用能定位真实源码。
- 每个 FU 可独立验收，数据流边界明确。
- 不记录隐藏推理过程。
