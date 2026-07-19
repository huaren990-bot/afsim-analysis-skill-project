# Phase 2 完成记录：batch43 utilqt Qt 基础设施与 util_script 脚本运行时

> **完成日期**：2026-07-14
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/tools/utilqt/source` | 105 | `UtQtRaiseWidget`, `UtQtDockArea`, `UtQtDockControl`, `UtQtAbstractTableModel`, `UtQtGLWidgetBase` | utilqt 工具端 Qt 基础设施库：提供通用控件、dock 管理、model/view、OpenGL 绘图、渐变配置、XML 读写和网络/进程辅助能力。 |
| `afsim-2_9/swdev/src/tools/util_script/source` | 107 | `UtScript`, `UtScriptParser`, `UtScriptLanguage::Parser::func_def`, `UtScriptExecutor::Execute`, `UtScriptClass` | util_script 内嵌脚本系统：覆盖脚本类型系统、parser/scanner、字节码、VM 执行器、作用域、调试器和 AFSIM 常用对象绑定。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先执行批量 CodeGraph 查询；对通用符号噪声，按完整路径回落到目录内源码扫描确认。 |
| 目录内批量扫描 | 主 agent | 按目录边界扫描 class/function/registration/ProcessInput/输出入口，排除 `vx.json` 和导出宏伪符号。 |
| 合并与验证 | 主 agent | 更新 JSONL、模块总览、批次记录和批次验证报告。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `afsim-2_9/swdev/src/tools/utilqt/source` | GUI 基础链：业务 QWidget -> `UtQtDockControl` -> `UtQtDockArea::AddControl/UpdateLayout`；绘图链：派生 `UtQtGLWidgetBase` -> `initializeGL/resizeGL/paintGL` -> `Draw/QtDraw`；配置链：`UtQtXmlReader::Open/SetInput` -> token/attribute/text。 |
| `afsim-2_9/swdev/src/tools/util_script/source` | 脚本链：`UtScriptContext::Parse` -> `UtScriptParser::ParseP` -> `UtScriptLanguage::Scanner/Parser::func_def` -> `UtScriptScope/Registry` 注册脚本；执行链：`UtScriptContext::Execute` -> `UtScriptExecutor::Execute` -> debug/no-debug VM opcode loop。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch43-verify-report.md` |

## 已知问题

| 单元 | 风险与待确认项 |
|------|------|
| `afsim-2_9/swdev/src/tools/utilqt/source` | dock 逻辑依赖平台 workaround，OpenGL fixed-function API 对 Qt/GL 升级敏感，`file(GLOB)` 影响构建可追踪性。 |
| `afsim-2_9/swdev/src/tools/util_script/source` | Parser/Scanner 为生成代码，VM 由 include 模板生成 debug/no-debug 两套执行体；`UtScriptData` 指针/浅拷贝/managed-elsewhere 生命周期是高风险点。 |

## 下游就绪

本批新增 2 个最小目录单元、212 个 source/header 和 10 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
