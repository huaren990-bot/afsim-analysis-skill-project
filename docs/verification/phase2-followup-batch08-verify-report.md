# Phase 2 follow-up batch08 验证报告

> **日期**：2026-07-04
> **批次范围**：6 个 WKF/Wizard 小型最小目录单元
> **执行方式**：3 个子 agent 并行采集证据，主 agent 复核 CodeGraph/source 并统一合并 JSONL 与文档。

## 1. 批次范围

| # | 最小目录单元 | source/header 数 | 子系统 |
|---|--------------|------------------|--------|
| 1 | `afsim-2_9/swdev/src/tools/wkf/plugins/Visibility/source` | 2 | `tools/wkf` |
| 2 | `afsim-2_9/swdev/src/wizard/main/source` | 2 | `wizard/main` |
| 3 | `afsim-2_9/swdev/src/wizard/plugins/MapAnnotation/source` | 2 | `wizard/plugins` |
| 4 | `afsim-2_9/swdev/src/wizard/plugins/MysticLauncher/source` | 2 | `wizard/plugins` |
| 5 | `afsim-2_9/swdev/src/wizard/plugins/SIMDIS/source` | 2 | `wizard/plugins` |
| 6 | `afsim-2_9/swdev/src/wizard/plugins/UnitConversion/source` | 2 | `wizard/plugins` |

## 2. 验证摘要

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Phase1/File-index 覆盖闭环 | 通过 | `file-index.jsonl` 保持 43,586 行。 |
| batch08 工作清单状态 | 通过 | 6 个目标单元均标记为 `done_batch08`，总完成单元数为 28/237。 |
| batch08 文件索引 | 通过 | 12 个 source/header 条目均补充 `analysis_unit`、`system`、`subsystem`、`key_symbols`、`functions` 和中文 `brief`。 |
| batch08 粗符号索引 | 通过 | `symbol-index-phase2.jsonl` 共 14,286 行；本批目标路径下共有 101 条粗符号。 |
| 导出宏伪符号 | 通过 | 本批目标路径中 `*_EXPORT` 作为 `symbol_name` 的条目为 0；`WKF_PLUGIN_DEFINE_SYMBOLS` 仅作为插件注册宏调用记录。 |
| JSONL 可解析 | 通过 | `file-index.jsonl`、`symbol-index-phase2.jsonl`、`phase2-analysis-unit-worklist.jsonl` 均可逐行解析。 |
| 文档产物位置 | 通过 | 新增/更新 Markdown 均位于 `docs/`；`workspace` 下 Markdown 数为 0。 |

## 3. 按目录验证

| 最小目录单元 | 文件条目 | 粗符号条目 | 关键修正 |
|--------------|----------|------------|----------|
| `Visibility/source` | 2 | 10 | 补入 Visibility dock、viewer 菜单、平台可见性过滤器、ShowAll/HideSelected/HideUnselected。 |
| `wizard/main/source` | 2 | 5 | 补入 `main`、`wizard_main` 声明、Windows `WinMain`、`wideToMulti` 和 NVIDIA Optimus 导出变量。 |
| `MapAnnotation/source` | 2 | 53 | 补入 proxy watcher、POI/decoration/range ring parse/change、文本 replacement helper、地图菜单和属性面板反写链路。 |
| `MysticLauncher/source` | 2 | 10 | 补入 `WSF_PIPE` 文件检测器、文件右键动作、Mystic 进程启动和错误弹窗。 |
| `SIMDIS/source` | 2 | 16 | 补入 SIMDIS 配置、模型目录扫描、`.asi` 启动、编辑器模型/颜色替换和 settings 持久化。 |
| `UnitConversion/source` | 2 | 7 | 补入 editor context menu、parse/proxy unit type、标准单位中转和文本替换。 |

## 4. 子 agent 交叉确认

| 子 agent 范围 | 结论 |
|---------------|------|
| `Visibility/source`、`wizard/main/source` | 与主 agent CodeGraph 证据一致；补充 visibility filter 生命周期、scenario 空指针和 Windows 命令行编码复核点。 |
| `MapAnnotation/source` | 与主 agent CodeGraph 证据一致；补充 proxy path 边界、版本比较 `2.10` 风险和重复 entity name 业务限制。 |
| `MysticLauncher/source`、`SIMDIS/source`、`UnitConversion/source` | 与主 agent CodeGraph 证据一致；补充 QProcess 生命周期、SIMDIS 模型扫描/颜色编码和单位转换格式复核点。 |

## 5. 保留风险

| 风险 | 处理 |
|------|------|
| `Visibility` 注册平台可见性过滤器但未见注销路径，`HideUnselected` 未检查 standard scenario 空指针。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| `MapAnnotation::DisableFeatures` 用截取到小数后一位的方式比较版本，`2.10` 可能被误判为 `2.1`。 | 记录为 needs_review；这是 Wizard annotation 兼容性逻辑的后续重点。 |
| `MapAnnotation` 多处依赖 proxy path 形状、index node 存在和 token 查找成功。 | 记录为 needs_review，后续分析 Wizard 文本编辑一致性时集中验证。 |
| `MysticLauncher` 进程对象、`mFileInfo` 共享状态和错误输出读取长度存在边界。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| `SIMDIS` 模型扫描、颜色编码顺序和菜单 disconnect 范围需要结合外部格式确认。 | 记录为 needs_review，不在 Phase2 修改源码。 |
| `UnitConversion` 对数值文本格式和输出精度的假设较窄。 | 记录为 needs_review，不在 Phase2 修改源码。 |

## 6. 结论

batch08 通过。该批次补强了 Wizard/WKF 工具链入口，尤其是 `MapAnnotation` 的 WSF proxy、WKF map annotation 和 Wizard editor 双向同步链路。产物可支撑后续从 Wizard 工具行为分析 AFSIM 场景文本编辑、地图对象生成、外部工具启动和单位转换业务逻辑。
