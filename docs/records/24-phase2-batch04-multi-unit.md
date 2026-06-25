# Phase 2 batch04 多最小目录单元处理记录

> **日期**：2026-06-25
> **目标**：按 `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` 继续 Phase2，使用子 agent 并行分析多个最小目录单元。

## 1. 本批范围

| # | 最小目录单元 | 系统 | 子系统 | 文件数 |
|---|--------------|------|--------|--------|
| 1 | `afsim-2_9/swdev/src/wsf_plugins/wsf_simdis/source` | `plugin_modules` | `wsf_plugins/wsf_simdis` | 2 |
| 2 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer_iads_c2/source` | `plugin_modules` | `wsf_plugins/wsf_scenario_analyzer_iads_c2` | 2 |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultAcesDisplay/source` | `applications` | `mystic/plugins` | 2 |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultAirCombatVisualization/source` | `applications` | `mystic/plugins` | 2 |

## 2. 执行方式

| 角色 | 工作 |
|------|------|
| 子 agent | 分别负责一个最小目录单元，只读取 CodeGraph/source，输出文件职责、关键符号、注册/跨模块证据和风险项。 |
| 主 agent | 复核关键源码行号，串行合并 `file-index.jsonl`、`symbol-index-phase2.jsonl`、模块概览、计划和验证报告。 |

## 3. 修改产物

| 产物 | 处理 |
|------|------|
| `workspace/source-index/file-index.jsonl` | 精修 8 个 source/header 条目，补充 `analysis_unit`、`system`、`subsystem`、关键符号、函数和中文职责。 |
| `workspace/source-index/symbol-index-phase2.jsonl` | 替换 7 条目标路径旧粗符号，新增本批 114 条可追溯符号。 |
| `workspace/source-index/phase2-analysis-unit-worklist.jsonl` | 4 个目标单元标记为 `done_batch04`，总完成数达到 7。 |
| `docs/architecture/module-overview-v2-incremental.md` | 追加第 4-7 节，分别描述 4 个最小目录单元。 |
| `skill/cpp-project-analyzer/phases/phase2-modules/phase2-minimal-unit-plan.md` | 更新完成数、当前完成批次和 batch05 候选。 |
| `docs/verification/phase2-followup-batch04-verify-report.md` | 新增本批验证报告。 |

## 4. 关键发现

| 目录 | 发现 |
|------|------|
| `wsf_simdis/source` | 旧索引遗漏 `wsf::simdis::ScenarioExtension`、`wsf::simdis::Interface` 和 C ABI 插件入口。 |
| `wsf_scenario_analyzer_iads_c2/source` | 旧索引未覆盖 IADS C2 检查套件；本批补入 helper、公开检查函数、脚本类、扩展类和插件入口。 |
| `ResultAcesDisplay/source` | 旧索引缺少 `RvAcesDisplay::Plugin` 基类和方法级符号；源码中 `PlatformAddedRead` 限定名存在疑似额外 `Plugin::`。 |
| `ResultAirCombatVisualization/source` | 旧索引缺少 `rv::Plugin` 基类、匿名 helper、插件注册宏和核心数据填充方法。 |

## 5. 验证结果

| 指标 | 值 |
|------|-----|
| Phase1 文件行数 | 43,586 |
| file-index 行数 | 43,586 |
| source/header 覆盖一致 | 是，均为 17,342 |
| symbol-index-phase2 行数 | 14,055 |
| batch04 文件条目 | 8 |
| batch04 粗符号条目 | 114 |
| batch04 导出宏伪符号 | 0 |
| 已完成最小目录单元 | 7 / 237 |
| `workspace` 下 Markdown | 0 |

## 6. 后续建议

batch05 可继续按多目录批次推进，优先考虑当前 plan 中列出的 3-6 个小目录。`core/wsf_util` 和 six-dof 相关目录在开始前应先确认是否存在跨目录耦合；如证据复杂，拆成独立批次。
