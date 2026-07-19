# Phase 2 batch47 增量验证报告

> **验证日期**：2026-07-15
> **验证对象**：Phase 2 最小目录单元增量产物
> **结论**：通过

## 检查结果汇总

| 检查项 | 结果 | 证据 |
|------|------|------|
| 目录边界 | 通过 | 本批 8 个最小目录单元均按独立 `analysis_unit` 写入工作清单；residual 单元不覆盖已完成子目录。 |
| source/header 计数 | 通过 | 本批合计 77 个 source/header；`vx.json` 未计入。 |
| 代表性符号 | 通过 | 本批新增 35 条代表性符号；闭环单元允许 0 新增。 |
| 导出宏过滤 | 通过 | 未把 `*_EXPORT`、`*_IMPORT`、`*_API`、`*_LIB_EXPORT` 作为符号写入。 |
| Markdown 产物位置 | 通过 | 批次记录与验证报告均位于 `docs/` 下。 |

## 单元复核

| 最小目录单元 | 计数 | 状态 | 主要风险 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/tools/geodata` | 5 | 通过 | 测试是否进入常规 CTest/CI 未确认；业务逻辑仍应以已完成的 `tools/geodata/source` 为主。 |
| `afsim-2_9/swdev/src/tools/vespatk` | 6 | 通过 | 资源包、shader 和安装路径依赖运行环境；CodeGraph 无法验证 shader 兼容性。 |
| `afsim-2_9/swdev/src/tools/util_script` | 2 | 通过 | 测试覆盖不到完整 parser/executor/initializer list 语义；核心逻辑仍以 `tools/util_script/source` 为主。 |
| `afsim-2_9/swdev/src/tools/utilqt` | 2 | 通过 | 依赖 Qt application 生命周期；缺少覆盖测试。 |
| `afsim-2_9/swdev/src/core/wsf_cyber` | 3 | 通过 | `add_subdirectory(test)` 被注释，测试安装与常规执行关系未确认。 |
| `afsim-2_9/swdev/src/wizard/plugins` | 22 | 通过 | doc-only 插件与 `NO_EXPORT.md` 插件的导出策略需人工确认；父级不替代子插件 source/ 结论。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_coverage` | 37 | 通过 | 顶层 test 子目录注释，`install_tests(test_mission)` 只确认安装不确认 CI 执行。 |
| `afsim-2_9/swdev/src/tools/utilosg/source` | 0 | 通过 | 闭环结论是归属关闭，不代表新增质量验证。 |

## 结论

batch47 已完成。该批可作为后续业务逻辑分析入口；涉及测试是否执行、生成代码、动态库 ABI、网络/消息所有权等问题需在函数级或运行配置阶段继续确认。
