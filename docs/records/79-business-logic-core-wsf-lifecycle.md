# 业务逻辑分析批次记录：core/wsf 主生命周期

> **完成日期**：2026-07-15  
> **阶段**：业务逻辑分析入口 / Phase2 后续  
> **状态**：已完成并通过本批验证

## 分析范围

| 参数 | 值 |
|---|---|
| source_root | `/Users/hjt/afsim/afsim-analysis-skill-project/source_root/afsim-2_9` |
| extract_roots | `afsim-2_9/swdev/src/core/wsf/source` |
| exclude_paths | `.git`、隐藏目录、边界外 demo/training/documentation/resources、`vx.json` |
| analysis_depth | 业务逻辑入口增量，不替代全量 Phase3/4 函数索引 |

## 执行方式

| 子阶段 | 工具 | 职责 |
|---|---|---|
| 证据定位 | CodeGraph | 批量定位 `WsfStandardApplication`、`WsfScenario`、`WsfSimulation`、`WsfFrameStepSimulation` 主链路 |
| 源码校验 | CodeGraph node/explore | 获取 `AdvanceFrame`、`Initialize`、`AddInputPlatforms` 精确源码位置 |
| 产物合并 | 主 agent | 写入业务流程 JSONL、承接文档、生命周期补丁和验证报告 |

## 产出文件

| 文件 | 路径 | 用途 |
|---|---|---|
| 核心流程清单 | `workspace/business-logic/core-wsf-lifecycle-flows.jsonl` | 机器可读业务流程入口 |
| 业务承接文档 | `docs/architecture/business-logic-readiness.md` | 下一步业务逻辑分析入口 |
| 生命周期补丁 | `docs/architecture/lifecycle.md` | 增补核心 WSF 主链路证据 |
| 验证报告 | `docs/verification/business-logic-core-wsf-lifecycle-verify.md` | 本批质量门禁 |

## 关键统计数据

| 指标 | 值 |
|---|---:|
| 业务流程入口 | 3 |
| 业务域候选 | 4 |
| 规则/决策点候选 | 5 |
| 数据/配置映射 | 5 |
| 扩展机制入口 | 3 |

## 下游就绪

本批已经把 `core/wsf/source` 主生命周期拆成可继续追踪的入口。下一批建议从 `WsfPlatform::Update` 开始，向 mover、part、processor、sensor 和 event 子类继续展开。
