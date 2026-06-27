# 需求追溯矩阵 — requirement-to-afsim-trace.md

1. **使用说明**：本模板用于生成 `docs/requirements/requirement-to-afsim-trace.md`， 生成矩阵每条需求一行，记录需求 ID、需求描述、关联的 AFSIM 实现函数及生成的功能单元（FU）。  
  
2. **填写要求**：
   1. 请根据缺口分析结果，逐条填写以下表格，替换 `{...}` 占位内容。
   2. 本模板用于生成 `docs/requirements/requirement-gap-analysis.md`总结需求覆盖度情况，列出所有能力缺口，并按优先级排序，给出总体迁移建议。
   3. 若一条需求对应多个 AFSIM 函数，可合并为多行或使用逗号分隔，并在备注中说明分工。
   4. 若某需求在 AFSIM 中找不到直接实现，AFSIM 源函数及路径列填写”无”，FU ID 仍须分配，并备注需 Clean-room 重实现。
   5. 若某需求在 AFSIM 中完全无对应功能（🆕 缺失-AFSIM无参考），AFSIM 源函数及路径列填写”无”，备注中使用🆕**NOVAL，AFSIM无参考** 标签，并注明替代设计依据来源（如[文献引用](path/to/file.md)）。
   6. 所有 AFSIM 文件路径应相对于 `source_root/` 根目录。
   7. `function-index.jsonl`等所有索引均位于`workspace\source-index\`。

---

# 需求追溯矩阵模板

> **来源需求规范**：[`xxx.md`](path/to/file.md)
> **日期**：{YYYY-MM-DD}
> **需求编号**：{REQ-xxx}
> **说明**：本矩阵展示每条需求与 AFSIM 源码实现函数及生成的功能单元（FU）之间的追溯关系。


| 需求 ID | 功能单元 ID | 需求描述 | AFSIM源函数 | 备注 |
|---------|-------------|----------|----------------------------|-------------------|------|
| REQ-XXX | FU-XXX |  **功能模块名称**<br>· 子功能描述：详细说明该功能的具体内容 | {对应function-index.josnl中的"qualified_name"}<br>{对应function-index.josnl中的"brife"} | 🔑 核心 关键特性说明<br>子项或补充信息<br>⚠ 特殊情况/注意事项<br>🆕**NOVAL，AFSIM无参考** ，设计依据：[文献引用](path/to/file.md) |

