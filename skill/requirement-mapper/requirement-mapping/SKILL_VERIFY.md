---
name: requirement-mapping-verify
description: 检验requirement-mapping skill生成产物的质量。
---

# function-mapping-matrix
1. 表格是否符合模板格式、模板结构。
2. `需求ID`是否在需求规范文档中存在。
3. `需求描述`是否为中文描述。
4. `afsim对应功能`是否为AFSIM 函数或模块的功能中文描述
5. `目标系统当前功能`是否为目标系统当前功能的中文描述
6. `状态`是否符合状态图例
7. `匹配证据 / 差异说明`是否每行都列举了证据，说明了差异，证据和差异之间是否有`<br>`隔开
8. 所有确认后需求是否均已在矩阵中出现

# requirement-to-afsim-trace
1. 矩阵是否符合模板格式、模板结构
2. `需求ID`是否包含所有确认需求
3. `需求描述`是否有加粗的功能模块名称、是否有子功能描述
4. `AFSIM源函数`是否都能与function-index.jsonl中的函数对应上
5. `AFSIM源函数`是否有函数说明的`brife`字段
6. `备注`是否有参考文献

# requirement-gap-analysis
1. 报告是否符合模板格式、模板结构
2. 报告是否覆盖了确认后的所有需求
3. 管线完整性：每个 FU 的输入参数是否有上游 FU 提供，输出参数是否有下游 FU 消费，不存在"孤儿参数"（即输入变量无人产出、输出变量无人消费）。
4. 算法卡片一致性：每个 FU 的 AFSIM 参考描述是否与对应完整算法卡片正文（`docs/algorithms/flight-dynamics-*.md`）一致，不可仅凭 `CompendiumofAlgorithms.md` 的一句话摘要替代。

# 总体
1. 不同文档中是否FU ID统一
2. 不同文档中是否需求ID统一
3. 不同文档中是否覆盖状态统一
4. gap-specs.jsonl是否与文档内容相符
5. 算法卡片覆盖率：所有被引用的 AFSIM 算法卡片是否均已逐张打开阅读，不存在仅凭摘要引用的卡片。

# 输入
- `3_<requirement_index>-requirement-gap-analysis.md` — 完整缺口报告
- `3_<requirement_index>-function-mapping-matrix.md` — 功能映射矩阵
- `3_<requirement_index>-requirement-to-afsim-trace.md` — 需求到AFSIM的追溯矩阵
- `<requirement_index>-gap-specs.jsonl` — 结构化缺口规格（供下游迁移 Skill 使用）

# 输出
1. 生成检验报告，报告要求包括所有检验问题，以便其他skill问题修复，检验报告放入`docs\records`。