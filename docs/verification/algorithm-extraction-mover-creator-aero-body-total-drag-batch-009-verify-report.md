# AFSIM 算法提取验证报告：mover_creator aero body total drag batch 009

## 1. 范围与输入摘要

验证 batch 009 的两个候选、一个卡片、一个接口规格、Compendium 及覆盖账本，真实源码为 `source_root/afsim-2_9`。

## 2. 覆盖统计

| 范围 | 候选数 | extracted | rejected | deferred | pending/selected | 结论 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 全局 | 8141 | 42 | 6 | 0 | 8093 | 持续提取中 |
| batch 009 | 2 | 2 | 0 | 0 | 0 | 通过 |

## 3. 源码与产物核对

两候选均指向 `afsim-2_9/swdev/src/mover_creator/source/AeroBody.cpp:293-319`；其完整 Method、模块和算法 ID 与卡片、接口规格、批次和覆盖账本一致。卡片第 1–10 节和接口规格第 1–11 节完整，含正常/边界/退化 oracle。

## 4. Compendium 与缺陷

`ALG-AERODYNAMICS-BODY-TOTAL-DRAG-COEFFICIENT` 在 Compendium 中恰好一条，链接存在；统计合计为 59。无阻断、严重或一般缺陷。

## 5. 结论

结论：通过。
