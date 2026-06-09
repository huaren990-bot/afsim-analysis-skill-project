# 01 — 分析边界确认

**日期**：2026-06-09
**依据**：`tools/prompts/afsim-source-cognition 系统提示词.md` 第 1 步

---

## 源码根目录

```
afsim-analysis-skill-project/afsim_2.9.0_src_linux/
```

## P0-P4 边界定义

| 级别 | 目录 | 文件数（估计） | 简要说明 |
|------|------|---------------|----------|
| **P0** | `src/core/` | ~3,500 | 核心仿真框架：wsf/wsf_mil/wsf_space/wsf_nx/wsf_parser/wsf_util/wsf_ripr/wsf_cyber/wsf_l16/wsf_mtt/wsf_mil_parser/wsf_grammar_check/wsf_weapon_server/sensor_plot_lib |
| **P1** | `src/mover_creator/`、`src/weapon_tools/`、`src/wsf_plugins/` | ~10,135 | 运动体创建工具 + 武器分析工具 + 23 个功能插件 |
| **P2** | `src/warlock/`、`src/tools/` | ~3,101 | 实时仿真控制器 + 16 个辅助工具集 |
| **P3** | `src/wizard/`、`src/sensor_plot/`、`src/mystic/`、`src/mission/`、`src/evt_reader/`、`src/engage/` | ~1,399 | GUI 工具 + 可视化 + 可执行入口 + 交战分析 |
| **P4** | `dependencies/`、`src/cmake/`、`src/doc/` | ~55 | 第三方依赖、构建系统配置、全局文档 |

**策略**：所有步骤覆盖 P0-P4 全部级别。首轮以 P0 深度分析为起点，P1-P4 进行文件分类和目录级说明。

## 排除范围

- `.git/` 目录
- 编译产物（`.o`、`.a`、`.so`、`moc_*`、`ui_*` 等自动生成文件）
- `test*/` 和 `*_test*/` 目录中的纯测试数据（测试源码仍需分类为 `test`）

## 分析深度

| 层级 | 深度 |
|------|------|
| P0 | 文件级：每个 .hpp/.cpp 分类 + 符号提取 + 参数默认值记录 |
| P1 | 目录级：每个子目录一句话说明 + 关键文件深度分析 |
| P2 | 目录级：每个工具目录一句话说明 |
| P3 | 目录级：每个子目录一句话说明 |
| P4 | 列表级：目录名和用途摘要 |

## 历史材料

本轮为全新分析，无继承的历史材料。之前的索引文件（`workspace/source-index/*.jsonl`）和架构文档（`docs/architecture/*.md`）为旧版 schema，本轮需完全重写。
