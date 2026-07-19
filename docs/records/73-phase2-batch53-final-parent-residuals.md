# Phase2 batch53：最终父目录 residual 闭环

> 日期：2026-07-15  
> 方法：CodeGraph 优先定位代表入口，结合源码路径抽样与既有 Phase2 工作清单；本批只统计 C/C++ 源/头，显式排除 `vx.json`。

## 范围

| 最小目录单元 | source/header 数 | 代表入口 | Phase2 结论 |
|---|---:|---|---|
| `afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof` | 1 | P6DofTypeManager::ProcessInput, P6DofTypeManager::ProcessInput, P6DofTypeManager::ProcessInput, P6DofTypeManager::ProcessInput, P6DofTypeManager::ProcessInput | P6DOF 插件父目录 residual，仅保留顶层/测试闭环；真正运动模型在 p6dof/source 与 wsf_p6dof/source。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof` | 1 | test_six_dof_utils | SixDOF 插件父目录 residual，闭合顶层构建入口；动力学、发动机和推进系统在 source 子目录。 |
| `afsim-2_9/swdev/src/tools/wkf` | 2 | wkf::DataContainer, wkf::DataContainer, wkf::DataContainer, wkf::DataContainer, wkf::DataContainer | WKF 父目录 residual，闭合 common/core 等已拆分单元之外的顶层入口。 |
| `afsim-2_9/swdev/src/core/wsf_mil` | 3 | main, test_wsfopticalpath, test_wsftrackclassifier | 军事感知/特征父目录 residual；source 子目录承载贝叶斯、光学、声学与聚类实现。 |
| `afsim-2_9/swdev/src/core/wsf` | 12 | WsfUnitTestCommands, test_wsfapplication, test_wsfclocksource, test_wsfdatetime, test_wsfdefaultkinematicstateextrapolation | WSF 核心父目录 residual，闭合主 source、parser、space 等子单元之外的残留入口。 |
| `afsim-2_9/swdev/src/core/wsf_parser` | 19 | ParseSourceProvider, WsfParser::ParseFiles, WsfParser::ParseFiles, WsfParser::ParseFiles, WsfParser::ParseFiles | WSF 解析器父目录 residual，负责解析动作、脚本扫描和 parse-source 周边入口。 |
| `afsim-2_9/swdev/src/core/wsf_space` | 25 | SpaceTestService, EXPECT_THROW, main, test_wsfdeltavorbitalmaneuver, test_wsfjacchiarobertsatmosphere | 空间/轨道父目录 residual；source 子目录承载轨道传播器和大气扩展。 |
| `afsim-2_9/swdev/src/tools/util` | 63 | UtCodeTimer, UtCodeTimerNode, main, test_tbllookup, test_utalgorithm | 通用工具父目录 residual；source 子目录承载日志、字符串、异常和历史映射。 |
| `afsim-2_9/swdev/src/wizard/usmtf` | 72 | UserDefinedSet, main, test_acmid, test_aco, test_aerial_refueling | USMTF Wizard 父目录 residual；source 子目录承载字段、消息、时间点与枚举校验。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_iads_c2_lib` | 95 | VclInterceptCalculator::CanIntercept, VclInterceptCalculator::CanIntercept, VclInterceptCalculator::CanIntercept, VclInterceptCalculator::CanIntercept, VclInterceptCalculator::CanIntercept | IADS C2 库父目录 residual，补齐脚本可覆写处理器、事件输出与场景扩展边界。 |

## 关键判断

- 本批按最小目录单元闭环；父目录 residual 不覆盖已完成子目录。
- `symbol-index-phase2.jsonl` 补充/保留 44 个代表入口，用于下一步从模块边界进入业务逻辑调用链。
- `file-index.jsonl` 对本批 C/C++ 文件增加 batch 标记和模块摘要；非 C/C++ 文件不参与 source/header 计数。

## 业务逻辑分析提示

- `afsim-2_9/swdev/src/wsf_plugins/wsf_p6dof`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/tools/wkf`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/core/wsf_mil`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/core/wsf`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/core/wsf_parser`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/core/wsf_space`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/tools/util`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/wizard/usmtf`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/wsf_plugins/wsf_iads_c2_lib`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。

## 产物

- Worklist 状态：`done_batch53`
- 验证报告：`docs/verification/phase2-followup-batch53-verify-report.md`
