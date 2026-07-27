# AFSIM 算法汇总模板

# AFSIM 算法汇总

> **范围**：<全局或模块范围>
> **索引版本/摘要**：<version/hash/date>
> **候选账本**：`workspace/algorithm-extraction/algorithm-candidates.jsonl`
> **覆盖账本**：`workspace/algorithm-extraction/algorithm-coverage.jsonl`
> **更新日期**：YYYY-MM-DD

## 1. 覆盖摘要

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected | 完成状态 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `<module/domain>` | 0 | 0 | 0 | 0 | 0 | complete/incomplete |

数字必须从候选与覆盖账本计算。只有 pending/selected 为 0 且验证通过时才标 complete。

## 2. 算法目录

### <领域>

#### ALG-<DOMAIN>-<SLUG>：<中文名称>

- **英文名称**：……
- **AFSIM 模块**：……
- **功能**：……
- **生命周期**：……
- **核心源码证据**：`qualified_name`，`path:start-end`
- **算法卡片**：[链接](<domain>-<algorithm>-card.md)
- **接口规格**：[链接](../extracted-algorithms/<algorithm>/<domain>-<algorithm>-interface-spec.md)
- **验证状态**：draft / verified / needs-review

每个通过算法恰好一个主条目。不同模块实现同一数学算法时，可共享分类但分别列出实现证据。

## 3. 模块视图

| 模块 | 算法 ID | 算法 | 角色 | 验证 |
| --- | --- | --- | --- | --- |
| `<module>` | ALG-... | <名称> | <业务/数值角色> | <status> |

## 4. 可移植性

| 算法 ID | 可移植性 | 框架耦合 | 单位/坐标系适配 | clean-room/许可证注意 |
| --- | --- | --- | --- | --- |
| ALG-... | 高/中/低 | <说明> | <说明> | <说明> |

## 5. 未闭环范围

| candidate_id/范围 | 状态 | 原因 | 所需证据 | 下一步 |
| --- | --- | --- | --- | --- |
| `<id>` | deferred/pending | <原因> | <证据> | <动作> |
