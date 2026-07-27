---
name: algorithm-verification
description: 验证 algorithm-extraction 生成的 AFSIM 候选清单、覆盖账本、算法卡片、接口规格和 Compendium 是否完整、一致且具有真实源码证据。用于算法提取批次验收、全量覆盖审计或修复后复验；不执行新的算法提取。
---

# AFSIM 算法提取验证

只验证已有产物，不补写缺失算法。逐项给出可复现证据和修复建议。

## 验证输入

- `workspace/algorithm-extraction/algorithm-candidates.jsonl`
- `workspace/algorithm-extraction/algorithm-coverage.jsonl`
- 当前批次清单（若为批次验收）
- `docs/algorithms/*-card.md`
- `docs/algorithms/CompendiumofAlgorithms.md`
- `docs/extracted-algorithms/*/*-interface-spec.md`
- `workspace/source-index/function-index.jsonl`
- `workspace/source-index/function-body-summary.jsonl`
- AFSIM 真实源码
- `references/upstream-contract.md`
- `references/output-contract.md`
- `skill/algorithm-extractor/template_list/` 下的三个模板

## 验证步骤

### 1. 输入与范围

1. 逐行解析候选与覆盖 JSONL，报告文件行数、无效 JSON 行和重复 `candidate_id`。
2. 明确分母：全局候选或当前批次候选。不得用算法卡片数代替候选覆盖分母。
3. 对候选状态分组统计。完成范围中存在 `pending` 或 `selected` 即失败。

### 2. 源码可追溯性

对所有 `extracted` 候选和至少 10%（不少于 5 条）的 `rejected`/`deferred` 候选抽样：

1. 用 `path`、`line_start`、`line_end` 打开真实源码。
2. 用 `candidate_id` 连接 function 与 body summary。
3. 核对 `qualified_name`、函数体范围、模块、algorithm hint 和决策理由。
4. 检查同名函数是否用模块和完整路径消歧。

任何不存在的源码路径、越界行号或引用不存在的 `function` 字段均为严重缺陷。

### 3. 卡片完整性

逐张卡片核对模板，并重点检查：

- 稳定算法 ID、算法边界、模块和领域。
- 入口、核心调用链、生命周期和源码位置。
- 输入、输出、参数、状态、常量、副作用、单位与坐标系。
- 离散公式、伪代码、变量映射和经验系数来源。
- 框架依赖、边界条件、数值风险、可移植性。
- 正常、边界、退化/异常三类验证计划。

章节标题存在但内容为 `TBD`、省略号、占位文本或无法验证的泛泛描述，按缺失处理。

### 4. 公式与变量

1. 每个数学符号必须映射到代码变量、配置量或明确的推导中间量。
2. Method 必须精确匹配当前 `function-index.jsonl` 的 `qualified_name`。
3. 单位和坐标系无法由源码证明时必须标为推断或未知。
4. 检查是否把离散更新误写成连续模型、把框架状态误当算法输入、把经验常量臆测为理论常量。

### 5. 算法粒度

检查一张卡片是否混合了可独立测试的不同机制，例如积分器与控制器、不同大气模型、Lambert 与初轨确定。发现混合时失败并给出拆分边界。

### 6. 接口规格

每个通过的算法必须有且只有一个主接口规格。核对：

- 算法 ID 与卡片一致。
- 输入输出、状态、单位、坐标系和错误处理与卡片一致。
- AFSIM 类型映射与框架替换方案明确。
- 示例不声称未实现代码已经可用。

### 7. Compendium 与覆盖账本

1. 每张通过卡片在 Compendium 中恰好出现一次。
2. Compendium 中每条主条目能链接到存在的卡片和接口规格。
3. 覆盖账本中每个 `extracted` 候选至少关联一个存在的算法 ID。
4. 每个 `rejected`/`deferred` 候选有具体 `decision_reason`。
5. Compendium 统计与实际条目一致。

## 严重程度

- **阻断**：JSONL 无法解析、完成范围未闭环、源码证据不存在、算法 ID 无法追溯。
- **严重**：核心公式/变量映射/接口规格缺失、卡片混合多个算法、卡片与源码行为矛盾。
- **一般**：非核心章节不完整、链接或统计错误、说明不足。
- **轻微**：不影响语义的格式或措辞问题。

存在阻断或严重缺陷时不得通过。不得用“多数检查通过”掩盖硬性失败。

## 输出

写入 `docs/verification/algorithm-extraction-<scope>-verify-report.md`，包含：

1. 范围与输入摘要。
2. 候选状态和覆盖率统计。
3. 检查项结果与证据。
4. 按严重程度排序的缺陷清单。
5. 每项缺陷的文件、算法 ID/候选 ID、问题和最小修复建议。
6. 结论：`通过`、`修复后复验` 或 `上游阻塞`。

记录验证方法和可审查证据，不记录隐藏推理过程。
