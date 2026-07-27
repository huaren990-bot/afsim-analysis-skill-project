---
name: requirement-mapping-verify
description: 验证 requirement-mapping 的需求缺口报告、功能映射矩阵、AFSIM 追溯矩阵和 gap-specs JSONL 是否覆盖完整、证据真实、ID/状态一致且可供迁移规划使用。用于需求映射验收和修复后复验，不生成新的需求或 FU。
---

# 需求映射验证

## 输入

- 人工确认的 `2_<req-id>-requirement-<slug>.md`
- `3_<req-id>-requirement-gap-analysis.md`
- `3_<req-id>-function-mapping-matrix.md`
- `3_<req-id>-requirement-to-afsim-trace.md`
- `workspace/requirements/<req-id>/<req-id>-gap-specs.jsonl`
- AFSIM evidence JSONL、完整算法卡片、索引和真实源码
- 目标系统证据或 `empty_system` 假设

## 验证步骤

### 1. 结构和解析

- 逐行解析 gap-specs，报告无效 JSON、重复 `fu_id` 和缺失必填字段。
- 核对四类输出路径、版本、req-id 和模板结构。
- 不以固定行数判断文档质量。

### 2. 需求覆盖

- 从确认版需求枚举全部原子 REQ ID。
- 核对每个 ID 在映射矩阵和追溯矩阵中恰好出现一次主记录。
- 核对 gap 报告中的状态、优先级和验收标准与确认版一致。

### 3. AFSIM 证据

对每个 `full`/`partial` AFSIM 覆盖或 `missing_with_afsim_reference` 状态：

- `qualified_name` 在 function-index 中存在。
- `path:line_start-line_end` 能打开真实源码并支持所述行为。
- 同名函数已按模块消歧。
- 引用算法时已打开完整卡片，且卡片与源码不冲突。

仅有 Compendium 摘要、函数名或索引 brief 时失败。

### 4. 目标系统证据

- `satisfied`/`partial` 必须有目标源码、接口或测试证据。
- 按空系统处理时必须显式记录假设，不得伪造“不存在”的检索证据。
- 需求证据、AFSIM 证据与目标证据分栏或分字段保存。

### 5. 状态与迁移方式

核对统一状态与建议方式：

- `satisfied` 通常不生成 FU。
- `partial` 可为 `direct_adaptation` 或 `partial_rewrite`。
- `missing_with_afsim_reference` 可为 `cleanroom` 或经许可证确认的适配方式。
- `missing_without_afsim_reference` 为 `novel`。
- `unknown` 不得进入已确认迁移实施。

### 6. FU 完整性

每个 FU 必须有稳定 ID、关联需求、验收标准、完整接口、单位/坐标系、状态、副作用、数据流、证据、耦合度、风险和优先级。文档与 JSONL 必须一致。

### 7. 管线检查

- 区分外部输入、上游 FU、持久状态、最终输出和诊断输出。
- 只把真正无来源的中间输入或无用途的中间输出报告为断链。
- 核对边上的类型、单位、坐标系和采样时刻。
- 核对初始化、更新、重置和终止。

### 8. 交叉一致性

核对所有产物中的 REQ ID、FU ID、名称、状态、AFSIM 源位置、目标证据、迁移方式和优先级。任何相互矛盾均为阻断项。

## 通过门禁

以下任一情况存在时不得通过：

- JSONL 无法完整解析。
- 确认需求遗漏或重复。
- 非 unknown 状态没有证据。
- AFSIM 路径/行号不存在或不支持结论。
- FU 文档与 JSONL 不一致。
- 数据流存在未解释断链。

## 输出

写入 `docs/verification/requirement-mapping-<req-id>-verify-report.md`，包含范围、输入摘要、逐项结果、缺陷严重程度、文件/FU/REQ 定位、最小修复建议和结论：`通过`、`修复后复验` 或 `上游阻塞`。
