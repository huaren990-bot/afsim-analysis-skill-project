# Phase 2 完成记录：batch47 父级 residual 与重叠单元闭环

> **完成日期**：2026-07-15
> **阶段**：Phase 2 / 7
> **状态**：已完成并通过增量验证

## 分析范围

| 最小目录单元 | source/header 数 | 核心符号 | 结论 |
|------|------:|------|------|
| `afsim-2_9/swdev/src/tools/geodata` | 5 | `geodata_test_main`、`DtedTile_ReadCell_test`、`GeotiffTileManager_SpatialPartitioning_test`、`FloatGridTile_ReadCell_test`、`GeotiffTile_ReadCell_test` | geodata 父级 residual：覆盖构建入口与 DTED/GeoTIFF/FloatGrid 单元测试，不重复 source/ 地形瓦片与投影实现。 |
| `afsim-2_9/swdev/src/tools/vespatk` | 6 | `vtk_write_vcproj_user`、`swdev_install_resources`、`install_maps`、`install_models`、`swdev_extract_resources` | vespatk 父级 residual：覆盖 shader header 与资源/安装辅助入口，不重复 source/ VESPA viewer 与资源管理核心。 |
| `afsim-2_9/swdev/src/tools/util_script` | 2 | `UtScriptData_StringIntEquivalenceInMap_test`、`TestScriptAccessible`、`TestScriptClass`、`UtScriptDataPack_PackAndUnpack_test`、`project_util_script` | util_script 父级 residual：覆盖顶层构建与 UtScriptData/UtScriptDataPack 回归测试，不重复 source/ parser、类型系统和 VM。 |
| `afsim-2_9/swdev/src/tools/utilqt` | 2 | `UtQtCodeTimerObserver`、`UtQtCodeTimer`、`UtQtCodeTimer::Initialize`、`UtQtCodeTimerObserver::Update`、`UtQtCodeTimerObserver::ReportChildren` | utilqt 父级 residual：覆盖 Qt code timer GUI 观察器和旧 `.pro` 工程入口，不重复 source/ 通用控件库。 |
| `afsim-2_9/swdev/src/core/wsf_cyber` | 3 | `project_wsf_cyber`、`add_event_pipe_schema`、`CyberEffect_grammar`、`CyberAttack_grammar`、`wsf_cyber_extension` | wsf_cyber 父级 residual：覆盖 CMake、grammar、event pipe schema、doc 与测试资产，不重复 source/ cyber attack/effect/trigger 实现。 |
| `afsim-2_9/swdev/src/wizard/plugins` | 22 | `WizDemoBrowser_plugin`、`WizCRDImporter_plugin`、`CRDImporter_main`、`SimulationManager::Plugin::Plugin`、`WizScenarioAnalyzer_plugin` | Wizard 插件集合父级 residual：覆盖插件清单、wizard_plugin.cmake、CRDImporter lib/exec/test 等包装层，不重复各插件 source/ 业务实现。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_coverage` | 37 | `project_wsf_coverage`、`add_wsf_doc_input`、`wsf_coverage_extension`、`coverage_root_grammar`、`WSF_LAT_LON_GRID_grammar` | wsf_coverage 父级 residual：覆盖顶层 CMake、coverage grammar、doc、test 与 test_mission 资产，不重复 source/ coverage/grid/measure 实现。 |
| `afsim-2_9/swdev/src/tools/utilosg/source` | 0 | `无新增符号，闭环确认` | utilosg/source 闭环确认：该源码目录已由 batch40 的 parent `tools/utilosg` 覆盖，本轮只关闭重叠 pending 单元。 |

## 执行方式

| 子阶段 | 方式 | 说明 |
|------|------|------|
| CodeGraph 批量探索 | 主 agent + 子 agent 并行读取证据 | 先用 CodeGraph 批量探索批次范围；对 residual/资源/测试/grammar 等 CodeGraph 弱项，回落到目录内 `rg` 与文件清单。 |
| 子 agent 分片 | 6 个 explorer | batch47-batch52 分别读取互不重叠目录，只输出证据摘要，不写共享文件。 |
| 主 agent 合并 | 主 agent | 更新 JSONL、模块总览、批次记录和验证报告；父级 residual 不覆盖已完成子目录归属。 |

## 关键发现

| 单元 | 后续业务逻辑入口 |
|------|------|
| `afsim-2_9/swdev/src/tools/geodata` | `CMakeLists.txt -> add_subdirectory(source) -> test/main.cpp -> gtest cases -> DtedTile/GeotiffTile/FloatGridTile`，用于验证地理数据读取链。 |
| `afsim-2_9/swdev/src/tools/vespatk` | CMake helper 安装/提取 resources、maps、models、shaders，运行时由 `VaResourceManager`/viewer 链消费。 |
| `afsim-2_9/swdev/src/tools/util_script` | `CMakeLists.txt -> gtest -> UtScriptData/UtScriptDataPack`，验证脚本数据对象、排序、constructors 和 pack/unpack。 |
| `afsim-2_9/swdev/src/tools/utilqt` | `UtQtCodeTimer::Initialize -> QTimer::timeout -> UtCodeTimer::Update -> UtQtCodeTimerObserver::Update/ReportChildren`。 |
| `afsim-2_9/swdev/src/core/wsf_cyber` | `wsf_cmake_extension.cmake -> grammar/wsf_cyber.ag -> scenario input -> source extension/managers -> event pipe schema`。 |
| `afsim-2_9/swdev/src/wizard/plugins` | `wizard_plugin.cmake -> WIZARD_PLUGIN_NAME/source path -> plugin target -> plugin constructor registers actions/docks/preferences`。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_coverage` | `wsf_cmake_extension.cmake -> grammar/wsf_coverage.ag -> scenario input -> source SimulationExtension -> grid/coverage/measure/output`。 |
| `afsim-2_9/swdev/src/tools/utilosg/source` | 已归属链仍为 `UtoShapeFactory/UtoTerrainFactory -> UtoResourceDB -> UtoViewer`；本轮不重新分摊子树。 |

## 产出文件

| 文件 | 路径 |
|------|------|
| file-index 增量 | `workspace/source-index/file-index.jsonl` |
| Phase2 粗符号索引 | `workspace/source-index/symbol-index-phase2.jsonl` |
| 工作清单 | `workspace/source-index/phase2-analysis-unit-worklist.jsonl` |
| 模块总览增量 | `docs/architecture/module-overview-v2-incremental.md` |
| 验证报告 | `docs/verification/phase2-followup-batch47-verify-report.md` |

## 已知问题

| 单元 | 风险与待确认项 |
|------|------|
| `afsim-2_9/swdev/src/tools/geodata` | 测试是否进入常规 CTest/CI 未确认；业务逻辑仍应以已完成的 `tools/geodata/source` 为主。 |
| `afsim-2_9/swdev/src/tools/vespatk` | 资源包、shader 和安装路径依赖运行环境；CodeGraph 无法验证 shader 兼容性。 |
| `afsim-2_9/swdev/src/tools/util_script` | 测试覆盖不到完整 parser/executor/initializer list 语义；核心逻辑仍以 `tools/util_script/source` 为主。 |
| `afsim-2_9/swdev/src/tools/utilqt` | 依赖 Qt application 生命周期；缺少覆盖测试。 |
| `afsim-2_9/swdev/src/core/wsf_cyber` | `add_subdirectory(test)` 被注释，测试安装与常规执行关系未确认。 |
| `afsim-2_9/swdev/src/wizard/plugins` | doc-only 插件与 `NO_EXPORT.md` 插件的导出策略需人工确认；父级不替代子插件 source/ 结论。 |
| `afsim-2_9/swdev/src/wsf_plugins/wsf_coverage` | 顶层 test 子目录注释，`install_tests(test_mission)` 只确认安装不确认 CI 执行。 |
| `afsim-2_9/swdev/src/tools/utilosg/source` | 闭环结论是归属关闭，不代表新增质量验证。 |

## 下游就绪

本批新增/闭环 8 个最小目录单元、77 个 source/header 和 35 个代表性符号，可继续支撑下一步 AFSIM 业务逻辑分析。
