# Phase3 batch05：core/wsf 顶层头文件符号补齐记录

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/core/wsf/source/*.hpp` 中 batch01-batch03 后剩余顶层头文件  
> **证据方式**：按文件分组调用 CodeGraph file node；同一文件只读取一次

## 结果汇总

| 指标 | 数量 |
|---|---:|
| 输入文件 | 18 |
| 输入 pending | 73 |
| 新增精细符号 | 73 |
| 新增枚举条目 | 9 |
| 已记录跳过 | 0 |
| 目标范围剩余 pending | 0 |

## 质量修复

本批新增枚举中有 6 个枚举值行带 `//!<` 注释，初次解析时 values 为空。已用去注释源码重新解析并补齐 values，未向最终 `enum-index.jsonl` 引入新增空枚举。

