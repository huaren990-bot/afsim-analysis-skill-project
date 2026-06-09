# 08 — 认知分析计划 v3（基于 2026-06-09 版提示词）

**日期**：2026-06-09
**状态**：待执行
**依据**：`tools/prompts/afsim-source-cognition 系统提示词.md`（2026-06-09 修订版）

---

## 提示词版本差异

| 维度 | v1 版 | v3 版（当前） |
|------|-------|--------------|
| 边界确认 | 一句话 | **P0-P4 分级表格**，明确 4 级优先级 |
| 覆盖范围 | 首轮仅 P0 (wsf/source) | **P0-P4 全部**，约 17,190 文件 |
| 文件分类 | 无 | 7 种：source/build/config/test/example/doc/generated |
| 索引 schema | 无版本号 | `schema_version: "1"`，字段大幅扩展 |
| function-index | 按函数名索引 | **四层级联**（System→Module→Class→Method） |
| 架构文档 | 4-5 章 | **8 章** + x-level-capabilities.md |
| 生命周期 | 无 | 7 阶段（entry→load→create→loop→update→output→shutdown） |
| 依赖类型 | 2 种 | **12 种**（include/build/inheritance/composition/call/read/write/registration/configuration/runtime/test/unknown） |
| 语言要求 | 无 | **中文优先**，英文后附中文翻译，路径可点击 |
| 目录说明格式 | 自由 | 参考 `docs/architecture/directroy_structure.md` 树形格式 |

## P0-P4 边界定义（来自提示词第 1 步）

| 级别 | 目录 | 文件数（约） |
|------|------|-------------|
| P0 | `src/core/`（wsf/wsf_mil/wsf_space/wsf_nx/wsf_parser/wsf_util/wsf_ripr/wsf_cyber/wsf_l16/wsf_mtt/wsf_mil_parser/wsf_grammar_check/wsf_weapon_server/sensor_plot_lib） | ~3,500 |
| P1 | `src/mover_creator/`、`src/weapon_tools/`、`src/wsf_plugins/` | ~10,135 |
| P2 | `src/warlock/`、`src/tools/` | ~3,101 |
| P3 | `src/wizard/`、`src/sensor_plot/`、`src/mystic/`、`src/mission/`、`src/evt_reader/`、`src/engage/` | ~1,399 |
| P4 | `dependencies/`、`src/cmake/`、`src/doc/` 等 | ~55+ |
| **合计** | | **~17,190** |

## 产出文件清单（8 个）

1. `docs/records/01-scope-boundary.md` — 边界确认记录
2. `docs/architecture/afsim-architecture.md` — 架构文档（8 章）
3. `docs/architecture/module-dependency.md` — 模块依赖表
4. `docs/architecture/x-level-capabilities.md` — 四层功能说明
5. `workspace/source-index/file-index.jsonl` — 文件索引
6. `workspace/source-index/symbol-index.jsonl` — 符号索引
7. `workspace/source-index/function-index.jsonl` — 功能索引（四层级联）
8. `workspace/source-index/dependency-index.jsonl` — 依赖索引

## 分析流程（9 步）

1. **确认边界** — 记录 P0-P4 范围和排除项
2. **发现文件** — `rg --files` 扫描，按 7 种类型分类
3. **参数提取** — 默认值、初始值、枚举值、宏常量
4. **索引记录** — 写入 4 个 JSONL 文件
5. **生命周期** — 识别 7 阶段：entry→scenario_load→object_create→simulation_loop→model_update→output→shutdown
6. **数据流/控制流** — 状态传递链路、配置传递链路
7. **架构草稿** — 生成 3 个 markdown 文档
8. **校对循环** — 提交问题给开发人员，迭代修正
9. **最终定稿** — 标记为最终版本

## 实施策略

由于 P0-P4 共 ~17,190 文件，采用**逐级推进**策略：

1. **P0 骨架**：先完成 P0（core/）的目录结构解析和关键文件深度分析
2. **P0 索引**：建立 P0 的完整 file-index + symbol-index + dependency-index
3. **功能追踪**：在 P0 基础上选取 5-6 个系统级功能，追踪到 P1（plugins）层的具体实现
4. **P1-P4 概览**：对 P1-P4 进行文件分类和目录级说明，关键路径深度分析
5. **汇总定稿**：基于所有层级认知完成全部 8 个产出文件

## 验证方法

1. `schema_version` 全部为 `"1"`
2. 所有英文标识符附中文翻译
3. 所有文件路径使用 markdown 链接语法，可点击打开
4. function-index 中四层功能的 `next-level` 级联完整闭合
5. x-level-capabilities 中功能可映射回 afsim-architecture 的子系统/模块
6. P0-P4 每个目录在 afsim-architecture.md「目录结构含义」章节中均有条目
