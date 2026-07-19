# Phase2 batch56：核心辅助库与 DIS/Space/MIL source 闭环

> 日期：2026-07-15  
> 方法：CodeGraph 优先定位代表入口，结合源码路径抽样与既有 Phase2 工作清单；本批只统计 C/C++ 源/头，显式排除 `vx.json`。

## 范围

| 最小目录单元 | source/header 数 | 代表入口 | Phase2 结论 |
|---|---:|---|---|
| `afsim-2_9/swdev/src/core/wsf_space/source` | 304 | WsfNonClassicalOrbitalPropagator, OrbitalPropagator, OrbitalMissionContext, OrbitalMissionVerificationContext, WsfJ2_PerturbationOrbitalPropagator | WSF 空间与轨道传播实现，覆盖积分传播器、机动、轨道类型和大气仿真扩展。 |
| `afsim-2_9/swdev/src/tools/util/source` | 341 | UtHistoryMap, UtLogStream, MessageStream, UtStringUtil, Parse | 跨模块通用工具实现，覆盖历史映射、日志流、字符串解析、异常记录和实体工具。 |
| `afsim-2_9/swdev/src/core/wsf_mil/source` | 429 | WsfPlatformClusterObject, WsfBayesClassification, ColumnPair, WsfBayesClassifier, WsfBayesClassifier | 军事环境感知与特征模型，覆盖贝叶斯分类、光学路径、声学/光学特征和聚类。 |
| `afsim-2_9/swdev/src/tools/dis/source` | 433 | DisIff, DisIff, DisIffAtcNavaids, DisIffAtcNavaidsParams, DisIffAtcNavaidsParams | DIS 协议数据结构与 PDU 读写，覆盖实体类型、IFF、AIS、坐标和动作响应。 |

## 关键判断

- 本批按最小目录单元闭环；父目录 residual 不覆盖已完成子目录。
- `symbol-index-phase2.jsonl` 补充/保留 20 个代表入口，用于下一步从模块边界进入业务逻辑调用链。
- `file-index.jsonl` 对本批 C/C++ 文件增加 batch 标记和模块摘要；非 C/C++ 文件不参与 source/header 计数。

## 业务逻辑分析提示

- `afsim-2_9/swdev/src/core/wsf_space/source`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/tools/util/source`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/core/wsf_mil/source`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/tools/dis/source`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。

## 产物

- Worklist 状态：`done_batch56`
- 验证报告：`docs/verification/phase2-followup-batch56-verify-report.md`
