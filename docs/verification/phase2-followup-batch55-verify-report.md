# Phase2 batch55 验证报告

| 检查项 | 结果 | 说明 |
|---|---|---|
| worklist 状态 | 通过 | 4 个单元均标记为 `done_batch55` |
| source/header 计数 | 通过 | 本批合计 902 个 C/C++ 源/头；`vx.json` 未计入 |
| 代表符号 | 通过 | 20 个代表入口带源码路径 |
| 文档位置 | 通过 | Markdown 产物位于 `docs/` 下 |
| 父子目录覆盖 | 通过 | residual 父目录与 `source` 子目录分开记录，避免重复闭环 |

## 单元清单

| 单元 | 数量 | 报告 |
|---|---:|---|
| `afsim-2_9/swdev/src/wizard/usmtf/source` | 182 | `docs/records/75-phase2-batch55-final-wizard-wkf-usmtf.md` |
| `afsim-2_9/swdev/src/mover_creator/source` | 225 | `docs/records/75-phase2-batch55-final-wizard-wkf-usmtf.md` |
| `afsim-2_9/swdev/src/tools/wkf/common/source` | 247 | `docs/records/75-phase2-batch55-final-wizard-wkf-usmtf.md` |
| `afsim-2_9/swdev/src/wizard/lib/source` | 248 | `docs/records/75-phase2-batch55-final-wizard-wkf-usmtf.md` |
