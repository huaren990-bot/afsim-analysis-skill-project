# Phase2 batch55：Wizard/WKF/USMTF 工具 source 闭环

> 日期：2026-07-15  
> 方法：CodeGraph 优先定位代表入口，结合源码路径抽样与既有 Phase2 工作清单；本批只统计 C/C++ 源/头，显式排除 `vx.json`。

## 范围

| 最小目录单元 | source/header 数 | 代表入口 | Phase2 结论 |
|---|---:|---|---|
| `afsim-2_9/swdev/src/wizard/usmtf/source` | 182 | USMTF_Parser, Message, Field, Field, RangeValidator | USMTF 字段/消息/段结构解析与校验，面向 Wizard 输入合法性和格式约束。 |
| `afsim-2_9/swdev/src/mover_creator/source` | 225 | MoverCreatorWidget, ScriptGenerator, VehicleAero, VehicleAero, VehicleAeroCore | Mover Creator 图形工具，编辑气动、几何、发动机、脚本生成和车辆性能数据。 |
| `afsim-2_9/swdev/src/tools/wkf/common/source` | 247 | WkfVisualEffectsDisplayInterface, VisualEffectsDisplayInterface, WkfEventMarkerDisplayInterface, EventMarkerDisplayInterface, EventMarkerPluginBase | WKF 公共可视化/事件标记组件，提供视觉效果、轨迹效果和显示接口。 |
| `afsim-2_9/swdev/src/wizard/lib/source` | 248 | WsfEditor, WsfEditor, ParseResults, ParseResultsProxyData, ActionManager | Wizard 编辑器基础库，覆盖文本源读写、语法折叠、编辑器初始化和解析结果聚合。 |

## 关键判断

- 本批按最小目录单元闭环；父目录 residual 不覆盖已完成子目录。
- `symbol-index-phase2.jsonl` 补充/保留 20 个代表入口，用于下一步从模块边界进入业务逻辑调用链。
- `file-index.jsonl` 对本批 C/C++ 文件增加 batch 标记和模块摘要；非 C/C++ 文件不参与 source/header 计数。

## 业务逻辑分析提示

- `afsim-2_9/swdev/src/wizard/usmtf/source`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/mover_creator/source`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/tools/wkf/common/source`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。
- `afsim-2_9/swdev/src/wizard/lib/source`：Phase2 已建立模块边界；Phase3 可沿代表符号进入调用链和业务语义。

## 产物

- Worklist 状态：`done_batch55`
- 验证报告：`docs/verification/phase2-followup-batch55-verify-report.md`
