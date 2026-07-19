# Phase3 batch03：core/wsf 高复用头文件符号补齐记录

> **日期**：2026-07-15  
> **阶段**：Phase 3 / 符号级细粒度分析  
> **范围**：`afsim-2_9/swdev/src/core/wsf` 中 external links、advanced behavior tree、comm、dis、event pipe、script、terrain、xio_sim 相关头文件  
> **证据方式**：按文件分组调用 CodeGraph file node；同一文件只读取一次

## 批次输入

| 文件 | Phase2 pending 数 |
|---|---:|
| `afsim-2_9/swdev/src/core/wsf/source/WsfExternalLinks.hpp` | 17 |
| `afsim-2_9/swdev/src/core/wsf/source/WsfAdvancedBehaviorTreeNode.hpp` | 17 |
| `afsim-2_9/swdev/src/core/wsf/source/comm/WsfCommNetworkManager.hpp` | 15 |
| `afsim-2_9/swdev/src/core/wsf/source/dis/WsfDisPlatform.hpp` | 15 |
| `afsim-2_9/swdev/src/core/wsf/source/comm/WsfCommProtocolOSPF.hpp` | 13 |
| `afsim-2_9/swdev/src/core/wsf/source/event_pipe/WsfEventPipeInterface.hpp` | 12 |
| `afsim-2_9/swdev/src/core/wsf/source/WsfTerrain.hpp` | 11 |
| `afsim-2_9/swdev/src/core/wsf/source/comm/WsfCommGraph.hpp` | 11 |
| `afsim-2_9/swdev/src/core/wsf/source/comm/WsfCommReservedAddressing.hpp` | 11 |
| `afsim-2_9/swdev/src/core/wsf/source/script/WsfScriptObserver.hpp` | 11 |
| `afsim-2_9/swdev/src/core/wsf/source/xio_sim/WsfXIO_AutoDisMapping.hpp` | 11 |
| `afsim-2_9/swdev/src/core/wsf/source/xio_sim/WsfXIO_PlatformInfoService.hpp` | 10 |

## 批次结果

| 指标 | 数量 |
|---|---:|
| 输入文件 | 12 |
| 输入 Phase2 pending | 154 |
| 新增精细符号 | 153 |
| 新增枚举条目 | 7 |
| 已记录跳过 | 1 |
| 目标文件剩余 pending | 0 |

## 跳过项

| 标识 | kind | 路径 | 跳过原因 |
|---|---|---|---|
| `WsfXIO_DisMessagePkt&)` | typedef | `afsim-2_9/swdev/src/core/wsf/source/xio_sim/WsfXIO_AutoDisMapping.hpp` | Phase2 残留的非法 C++ 符号名片段，不能作为有效 qualified name 生成精细符号 |

## 全局状态

| 指标 | 当前值 |
|---|---:|
| `symbol-index.jsonl` | 83,160 |
| `enum-index.jsonl` | 824 |
| `macro-index.jsonl` | 9,371 |
| Phase2 粗符号分母 | 12,108 |
| 已闭环 | 4,607 |
| 仍待处理 | 7,501 |
| 追溯覆盖率 | 38.05% |
| `core/wsf` 剩余 pending | 457 |

## 验证结论

batch03 目标文件已闭环，导出宏伪符号污染为 0，macro-index 违规宏为 0。Phase3 尚未全量完成，下一批建议继续处理 `core/wsf` 剩余 457 条 pending，再切换到 `core/wsf_l16`、`tools/wkf` 等大块目录。
