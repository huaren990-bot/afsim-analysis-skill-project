# Phase 2 follow-up batch04 验证报告

> **日期**：2026-06-25
> **批次范围**：4 个最小目录单元
> **执行方式**：子 agent 逐目录采集证据，主 agent 复核 CodeGraph/source 并统一合并 JSONL 与文档。

## 1. 批次范围

| # | 最小目录单元 | source/header 数 | 子系统 |
|---|--------------|------------------|--------|
| 1 | `afsim-2_9/swdev/src/wsf_plugins/wsf_simdis/source` | 2 | `wsf_plugins/wsf_simdis` |
| 2 | `afsim-2_9/swdev/src/wsf_plugins/wsf_scenario_analyzer_iads_c2/source` | 2 | `wsf_plugins/wsf_scenario_analyzer_iads_c2` |
| 3 | `afsim-2_9/swdev/src/mystic/plugins/ResultAcesDisplay/source` | 2 | `mystic/plugins` |
| 4 | `afsim-2_9/swdev/src/mystic/plugins/ResultAirCombatVisualization/source` | 2 | `mystic/plugins` |

## 2. 验证摘要

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Phase1/File-index 覆盖闭环 | 通过 | Phase1 `file-classification.jsonl` 43,586 行；`file-index.jsonl` 43,586 行；source/header 均为 17,342。 |
| batch04 工作清单状态 | 通过 | 4 个目标单元均标记为 `done_batch04`，总完成单元数为 7/237。 |
| batch04 文件索引 | 通过 | 8 个 source/header 条目均补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions` 和中文 `brief`。 |
| batch04 粗符号索引 | 通过 | 本批目标路径下共有 114 条粗符号，覆盖 class、function、method、constructor、namespace、macro_invocation。 |
| 导出宏伪符号 | 通过 | 本批目标路径中 `*_EXPORT` 作为 `symbol_name` 的条目为 0。 |
| 文档产物位置 | 通过 | 新增/更新 Markdown 均位于 `docs/`；`workspace` 下 Markdown 数为 0。 |
| 已删除 Phase1 临时文件 | 通过 | `docs/records/22-phase1-directory-tree-rebuild.md` 和 `docs/architecture/phase1-directory-tree-rebuild-verify.md` 未被重新生成。 |

## 3. 按目录验证

| 最小目录单元 | 文件条目 | 粗符号条目 | 关键修正 |
|--------------|----------|------------|----------|
| `wsf_simdis/source` | 2 | 22 | 补入 `wsf::simdis::ScenarioExtension`、`wsf::simdis::Interface`、插件 C ABI 入口和 SIMDIS 事件输出方法；修正 `wsf::simdis` 限定名。 |
| `wsf_scenario_analyzer_iads_c2/source` | 2 | 64 | 补入 IADS C2 检查 helper、26 个公开 `check*` 包装函数、脚本桥接类、应用扩展和插件入口。 |
| `ResultAcesDisplay/source` | 2 | 17 | 修正 `RvAcesDisplay::Plugin` 基类，补入 `WKF_PLUGIN_DEFINE_SYMBOLS` 和 ACES Display 数据填充方法。 |
| `ResultAirCombatVisualization/source` | 2 | 11 | 修正 `RvAirCombatVisualization::Plugin` 基类，补入匿名 helper、插件注册宏和空战可视化数据/overlay 方法。 |

## 4. 保留风险

| 风险 | 处理 |
|------|------|
| `ScenarioAnalyzerIADSC2RegisterScriptTypes` 只有头文件声明，未在本轮证据中发现定义。 | 未写入正式粗符号索引；记录在 file-index notes 与模块概览中，后续 Phase3/Phase4 可继续追踪。 |
| `RvAcesDisplay::Plugin::Plugin::PlatformAddedRead` 源码限定名疑似多出一层 `Plugin::`。 | 粗索引按稳定语义记录为 `RvAcesDisplay::Plugin::PlatformAddedRead`，并在文档中保留源码事实。 |
| 全局历史 `symbol-index-phase2.jsonl` 仍存在非 batch04 的 EXPORT 噪声。 | 本批未扩大清理范围；batch04 目标路径已验证无新增导出宏伪符号。 |

## 5. 结论

batch04 通过。该批次验证了“多个最小目录单元 + 子 agent 并行证据采集 + 主 agent 串行合并”的流程可行：4 个小目录在一个批次内完成，且每个目录都有独立边界、文件、符号、关系和风险记录。
