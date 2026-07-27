# 需求到 AFSIM 追溯矩阵模板

# <需求名称>需求到 AFSIM 追溯矩阵

> **需求集 ID**：REQ-XXX
> **日期**：YYYY-MM-DD

| 原子需求 ID | FU ID | AFSIM 覆盖 | candidate_id | qualified_name | 源码证据 | 生命周期/角色 | 算法卡片 | 差异与备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-XXX-FUNC-01 | FU-001 | full/partial/none/unknown | `<id>` | `<qualified_name>` | `path:start-end` | `<role>` | `[ALG-ID](relative-link)` | <差异> |

规则：

- 路径必须与当前 `function-index.jsonl` 的 `path` 一致，并能在真实源码中复核。
- AFSIM 覆盖为 `none` 时，candidate、qualified name、源码证据和算法卡片留空，在备注中记录实际检索范围。
- AFSIM 覆盖为 `unknown` 时，说明缺少的索引、源码或语义证据。
- 一个需求对应多个候选时可多行列出，但只设一个主证据并说明其他候选角色。
