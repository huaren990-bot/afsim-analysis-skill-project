# Phase3 batch07：core/wsf sensor、xio_sim 与 test 符号补齐记录

> **日期**：2026-07-15  
> **范围**：sensor、xio_sim、test  
> **证据方式**：按文件分组调用 CodeGraph file node；同一文件只读取一次

## 结果汇总

| 指标 | 数量 |
|---|---:|
| 输入文件 | 23 |
| 输入 pending | 59 |
| 新增精细符号 | 54 |
| 新增枚举条目 | 1 |
| 已记录跳过 | 5 |
| 目标范围剩余 pending | 0 |

## 跳过项

| 标识 | 路径 | 跳过原因 |
|---|---|---|
| `WsfUnitTestCommands` | `afsim-2_9/swdev/src/core/wsf/test/WsfUnitTestCommands.cpp` | gtest 源文件名被 Phase2 误归类为 class，源码中无 class 声明 |
| `test_wsfapplication` | `afsim-2_9/swdev/src/core/wsf/test/test_wsfapplication.cpp` | gtest 源文件名被 Phase2 误归类为 class，源码中无 class 声明 |
| `test_wsfclocksource` | `afsim-2_9/swdev/src/core/wsf/test/test_wsfclocksource.cpp` | gtest 源文件名被 Phase2 误归类为 class，源码中无 class 声明 |
| `test_wsfdatetime` | `afsim-2_9/swdev/src/core/wsf/test/test_wsfdatetime.cpp` | gtest 源文件名被 Phase2 误归类为 class，源码中无 class 声明 |
| `test_wsfdefaultkinematicstateextrapolation` | `afsim-2_9/swdev/src/core/wsf/test/test_wsfdefaultkinematicstateextrapolation.cpp` | gtest 源文件名被 Phase2 误归类为 class，源码中无 class 声明 |

## 结论

batch07 完成后，`afsim-2_9/swdev/src/core/wsf` 范围内 Phase3 pending 为 0。
