# AFSIM 算法提取验证报告：core/wsf_mil optical geometry/attenuation batch 008

## 1. 范围与输入摘要

验证 `batch-008-core-wsf-mil-optical-geometry-attenuation.jsonl` 中 5 个候选、3 张算法卡、3 份接口规格、Compendium 和覆盖账本；真实源码根为 `source_root/afsim-2_9`。

## 2. 候选状态和覆盖率统计

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected | 结论 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 全局候选账本 | 8141 | 40 | 6 | 0 | 8095 | 持续提取中 |
| batch 008 | 5 | 5 | 0 | 0 | 0 | 通过 |

候选与覆盖 JSONL 均为 8141 个唯一 ID；本批 5 行均为 `extracted`、有产物路径且 `verification=passed`。

## 3. 源码可追溯性

| 候选 | 源码位置 | 检查 | 结论 |
| --- | --- | --- | --- |
| `b9dcf250b3cf3878`、`bf1c93bdd53ab1f4`、`8822387113318a75` | `WsfOpticalPath.cpp:176-193` | 同一 `Height#1312e6167f` 实现、行号有效 | 通过 |
| `83f6af3c75d7a558` | `WsfOpticalSignature.cpp:166-222` | 默认分支投影公式与卡片边界一致 | 通过 |
| `1f3fa01844d1e14c` | `WsfOpticalAttenuation.cpp:298-363` | 分层、密度平均、指数累乘均已映射 | 通过 |

## 4. 卡片完整性

3 张卡片均具备第 1–10 节，含公式、变量映射、伪代码、源码证据和正常/边界/退化验证；3 份接口规格均具备第 1–11 节，说明 AFSIM 映射、依赖和错误处理。

## 5. Compendium 与覆盖账本

- 3 个新增算法 ID 在 Compendium 各出现一次，链接文件存在。
- `ALG-SENSORS-*` 主条目为 26；统计表为传感器/声学 26、合计 58。
- 三个路径高度别名共享同一算法 ID，避免重复算法条目，覆盖账本仍逐候选闭环。

## 6. 缺陷清单

无阻断、严重或一般缺陷。残余问题已在接口未决项中记录，不影响源码兼容的数学提取。

## 7. 结论

结论：通过。
