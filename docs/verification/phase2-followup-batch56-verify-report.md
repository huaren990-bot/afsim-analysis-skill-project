# Phase2 batch56 验证报告

| 检查项 | 结果 | 说明 |
|---|---|---|
| worklist 状态 | 通过 | 4 个单元均标记为 `done_batch56` |
| source/header 计数 | 通过 | 本批合计 1507 个 C/C++ 源/头；`vx.json` 未计入 |
| 代表符号 | 通过 | 20 个代表入口带源码路径 |
| 文档位置 | 通过 | Markdown 产物位于 `docs/` 下 |
| 父子目录覆盖 | 通过 | residual 父目录与 `source` 子目录分开记录，避免重复闭环 |

## 单元清单

| 单元 | 数量 | 报告 |
|---|---:|---|
| `afsim-2_9/swdev/src/core/wsf_space/source` | 304 | `docs/records/76-phase2-batch56-final-core-tools-protocols.md` |
| `afsim-2_9/swdev/src/tools/util/source` | 341 | `docs/records/76-phase2-batch56-final-core-tools-protocols.md` |
| `afsim-2_9/swdev/src/core/wsf_mil/source` | 429 | `docs/records/76-phase2-batch56-final-core-tools-protocols.md` |
| `afsim-2_9/swdev/src/tools/dis/source` | 433 | `docs/records/76-phase2-batch56-final-core-tools-protocols.md` |
