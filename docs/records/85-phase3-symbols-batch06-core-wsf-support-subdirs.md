# Phase3 batch06：core/wsf 支撑子目录符号补齐记录

> **日期**：2026-07-15  
> **范围**：observer、mover、script、dis、event_pipe、processor、ext、xio  
> **证据方式**：按文件分组调用 CodeGraph file node；同一文件只读取一次

## 结果汇总

| 指标 | 数量 |
|---|---:|
| 输入文件 | 22 |
| 输入 pending | 83 |
| 新增精细符号 | 83 |
| 新增枚举条目 | 7 |
| 已记录跳过 | 0 |
| 目标范围剩余 pending | 0 |

## 范围说明

本批覆盖观察者回调、机动路线、脚本上下文、DIS 接口、事件管道、方向查找处理器扩展和 XIO 基础接口等支撑符号，为后续函数级分析提供目录级闭环基础。

