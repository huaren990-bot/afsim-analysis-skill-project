# 需求追溯矩阵 — requirement-to-afsim-trace.md

> 使用说明：本模板用于生成 `docs/requirements/requirement-to-afsim-trace.md`。  
> 每条需求一行，记录需求 ID、需求描述、关联的 AFSIM 实现函数及生成的功能单元（FU）。  
> 请根据缺口分析结果，逐条填写以下表格，替换 `{...}` 占位内容。


| 需求 ID | 功能单元 ID | 需求描述 | AFSIM源函数<br>（类::方法） | AFSIM文件路径:行号 | 备注 |
|---------|-------------|----------|----------------------------|-------------------|------|
| REQ-XXX | FU-XXX | **功能模块名称**<br>· 子功能描述：详细说明该功能的具体内容 | `ClassName::methodName` | `path/to/file.hpp` | 🔑 核心 关键特性说明<br>子项或补充信息<br>⚠ 特殊情况/注意事项<br>🆕 全新设计 AFSIM无参考，设计依据：[文献引用] |


**填写要求**：
- 若一条需求对应多个 AFSIM 函数，可合并为多行或使用逗号分隔，并在备注中说明分工。
- 若某需求在 AFSIM 中找不到直接实现，AFSIM 源函数及路径列填写”无”，FU ID 仍须分配，并备注需 Clean-room 重实现。
- 若某需求在 AFSIM 中完全无对应功能（🆕 缺失-AFSIM无参考），AFSIM 源函数及路径列填写”无”，备注中使用 `<span style=”background-color: #f9e79f; padding:2px 6px; border-radius:4px; font-size:12px;”>🆕 全新设计</span>` 标签，并注明替代设计依据来源（如 [文献引用]）。
- 所有 AFSIM 文件路径应相对于 `source_root/` 根目录。