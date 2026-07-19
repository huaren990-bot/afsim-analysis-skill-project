# Phase3 batch08：core/wsf_l16 Link-16 符号补齐记录

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/core/wsf_l16/source`  
> **证据方式**：按文件分组调用 CodeGraph file node；同一文件只读取一次

## 结果汇总

| 指标 | 数量 |
|---|---:|
| 输入文件 | 74 |
| 输入 pending | 1,279 |
| 新增精细符号 | 1,229 |
| 新增枚举条目 | 92 |
| 已记录跳过 | 50 |
| 目标范围剩余 pending | 0 |

## 跳过项分类

| 分类 | 数量 | 示例 | 处理原因 |
|---|---:|---|---|
| 非法 C++ 符号片段 | 8 | `spare<43>`、`STATUS/QUALITY`、`(TRUE=SENSOR)` | 不是有效 qualified name，不能生成 typedef 条目 |
| 注释词或说明文本误识别 | 42 | `NORTH`、`TARGET`、`MINUTE`、`CONTROLLER` | 源码中无对应 typedef 声明，多来自字段注释或模板说明 |

## 处理说明

本批覆盖 Link-16 message、field、accessor、interface、part、factory、script bridge 等符号。`FieldTypes.hpp`、`Message11_0.hpp`、`Message11_1.hpp`、`MessagesPreDef.hpp` 等高密度头文件均按文件级 CodeGraph 证据处理。

所有新增 enum 均解析出 values；batch08 没有引入新的空 values 枚举。处理完成后，`core/wsf_l16` 范围在 `workspace/source-index/symbols-to-refine-phase3.jsonl` 中已无 `pending`。
