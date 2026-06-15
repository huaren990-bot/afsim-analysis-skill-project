# 算法提取质量检测报告

> **检测日期**：2026-06-15
> **检测范围**：23 张算法卡片 + 23 份接口规格（跨 23 个子目录）
> **检测 Skill**：algorithm-verification

## 1. 检测概要

| 指标 | 数值 |
|------|------|
| 算法卡片总数 | 23 |
| 接口规格总数 | 23 |
| 索引模块数（function-index.jsonl） | 2（core + wsf_plugins） |
| math 标记函数数 | ~82（core 模块） |
| 完全合规卡片数 | 11 |
| 严重缺陷数 | 8 |
| 一般缺陷数 | 10 |
| 轻微缺陷数 | 4 |

## 2. 检测清单与结果

### 2.1 模板合规性 — 必填章节

| 卡片 | 基础资料 | 流程图 | 变量表 | 数学公式 | 伪代码 | 入口链 | 源码位置 | 框架依赖 | 边界条件 | 测试计划 | 可移植性 | 内部状态 | 变量映射 | 提取策略 | 综合 |
|------|---------|--------|--------|---------|--------|--------|---------|---------|---------|---------|---------|---------|---------|---------|------|
| flight-dynamics-aero-coefficient-model-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-autopilot-pid-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-jet-engine-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-p6dof-heun-integrator-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-pointmass-aero-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-pointmass-integrator-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-pointmass-sas-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-propulsion-fuel-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-rigidbody-aero-coefficient-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| flight-dynamics-rigid-body-integrator-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| space-angles-only-iod-card.md | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL |
| space-conjunction-assessment-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| space-integrating-propagator-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| space-jacchia-roberts-atmosphere-card.md | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS | FAIL | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL |
| space-lambert-solver-card.md | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL |
| space-libration-point-card.md | PASS | FAIL | PASS | PASS | FAIL | FAIL | PASS | FAIL | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL |
| space-nasa-breakup-model-card.md | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS | FAIL | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL |
| space-norad-orbital-propagator-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| space-orbital-event-condition-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| space-orbital-maneuvers-card.md | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS | FAIL | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL |
| space-piecewise-exponential-atmosphere-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| space-rendezvous-targeting-card.md | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL |
| space-solar-terminator-card.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

### 2.2 表格列头规范

| 检查项 | 结果 |
|--------|------|
| 所有卡片包含「所属函数(Method)」列 | PASS |
| 状态变量表列头（含初始值/更新时机） | N/A（大部分卡片无此表，有者均符合） |
| 列头与模板完全一致 | PASS |

### 2.3 命名规范与模块归属

| 检查项 | 结果 |
|--------|------|
| 卡片文件命名遵循 domain-algorithm-card.md | PASS |
| domain 来自已知清单（flight-dynamics/space） | PASS |
| 文件名与 Compendium 交叉对照 | PASS |
| 算法所属模块标注正确（wsf_p6dof:2, wsf_six_dof:8, wsf_space:13） | PASS |
| 算法粒度合理（无杂揉） | PASS |

### 2.4 接口规格完整性

| 检查项 | 结果 |
|--------|------|
| 接口规格文件总数 | 23 份 |
| 接口规格与卡片一一对应 | FAIL（3 处映射不一致） |

**映射不一致详情**：

| 卡片 | 目录 | 问题 |
|------|------|------|
| space-angles-only-iod-card.md | 不存在 | 无对应目录 |
| space-nasa-breakup-model-card.md | 不存在 | 无对应目录（space-breakup-model 存在但名称不匹配） |
| space-norad-orbital-propagator-card.md | space-norad-propagator/ | 卡片名有 orbital，目录名省略 |

另有 `kinematics-integration/` 和 `space-atmosphere-model/` 两个目录无对应卡片（可能为历史遗留或聚合目录）。

### 2.5 汇总文档一致性

| 检查项 | 结果 |
|--------|------|
| 算法条目（23）与卡片总数一致 | PASS |
| 所有链接指向存在文件 | PASS |
| 算法统计表 = 2+8+13=23 | PASS |
| 可移植性总览涵盖全部 23 张卡 | PASS |

### 2.6 常见错误专项检测

| # | 错误类型 | 结果 |
|---|---------|------|
| 1 | 模块归属错误 | PASS |
| 2 | 算法杂揉 | PASS |
| 3 | 算法遗漏（math函数未覆盖） | 需人工复核（~82个math函数，详见附录） |
| 4 | Method列使用非索引函数名 | PASS |
| 5 | 命名规范不一致 | FAIL（3处接口目录名不匹配） |
| 6 | 遗漏"所属函数"列 | PASS |

## 3. 不通过项详情与修复指引

### 3.1 [严重] 算法伪代码缺失（× 7）

以下 7 张空间类算法卡片缺少 `### 算法伪代码` 章节：

1. space-angles-only-iod-card.md
2. space-jacchia-roberts-atmosphere-card.md
3. space-lambert-solver-card.md
4. space-libration-point-card.md
5. space-nasa-breakup-model-card.md
6. space-orbital-maneuvers-card.md
7. space-rendezvous-targeting-card.md

**问题描述**：上述卡片使用了替代布局——将「源码位置」和「可移植性评分」提升为顶级章节（`###`），省略了 `算法伪代码`、`入口和调用链`、`测试和验证计划`。所有 11 张飞行动力学卡片和其余 5 张空间卡片正确遵循模板结构。

**修复指引**（参考 `skill/afsim-algorithm-extractor/template_list/template_algorithm-card.md`）：
1. 在 `### 关键数学公式` 之后插入 `### 算法伪代码` 章节（伪代码块，每 3-5 行一句中文注释）
2. 插入 `### 源码使用说明` 章节，将现有 `### 源码位置` 和 `### 可移植性评分` 降级移入
3. 补全 `#### 入口和调用链`、`#### 框架依赖`、`#### 测试和验证计划`

### 3.2 [严重] 流程图缺失（× 1）

`space-libration-point-card.md` 缺少 `### 算法流程` 中的 mermaid 流程图和中文流程说明。

**修复指引**（参考 `template_algorithm-card.md` 的 `### 算法流程` 章节）：
- 添加 mermaid 流程图展示拉格朗日点计算主流程（输入参数 → Gamma 系数迭代 → L1-L5 位置计算 → Halo 轨道近似 → 输出）
- 附中文流程说明

### 3.3 [一般] 接口规格目录名不匹配（× 3）

- `space-norad-orbital-propagator` 卡片 → `space-norad-propagator` 目录：`orbital` 一词缺失
- `space-nasa-breakup-model` 卡片 → 无目录（存在 `space-breakup-model` 但缺少 `nasa-` 前缀）
- `space-angles-only-iod` 卡片 → 无目录

**修复指引**：统一命名规则。建议：重命名 `space-norad-propagator` → `space-norad-orbital-propagator`；重命名 `space-breakup-model` → `space-nasa-breakup-model`；创建 `space-angles-only-iod/` 目录。

### 3.4 [一般] 框架依赖缺失（× 4）

| space-jacchia-roberts-atmosphere-card.md | 缺 `#### 框架依赖` |
| space-libration-point-card.md | 缺 `#### 框架依赖` |
| space-nasa-breakup-model-card.md | 缺 `#### 框架依赖` |
| space-orbital-maneuvers-card.md | 缺 `#### 框架依赖` |

**修复指引**：添加框架依赖表，列出对 AFSIM 类的依赖（如 WsfPlatform、UtVec3d 等）及替代方案。

### 3.5 [一般] 测试和验证计划缺失（× 7）

与 3.1 节相同 7 张卡片缺少 `#### 测试和验证计划`。

**修复指引**：每卡至少列出 3 项测试（输入/预期输出/参考基准）。

### 3.6 [一般] 入口和调用链缺失（× 7）

与 3.1 节相同 7 张卡片缺少 `#### 入口和调用链`。

**修复指引**（参考 `template_algorithm-card.md`）：列出调用链，每行附中文注释。

## 4. 统计汇总

| 卡片 | 伪代码 | 流程图 | 入口链 | 框架依赖 | 测试计划 | 接口目录 | 综合 |
|------|--------|--------|--------|---------|---------|---------|------|
| flight-dynamics-aero-coefficient-model-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-autopilot-pid-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-jet-engine-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-p6dof-heun-integrator-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-pointmass-aero-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-pointmass-integrator-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-pointmass-sas-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-propulsion-fuel-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-rigidbody-aero-coefficient-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| flight-dynamics-rigid-body-integrator-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| space-angles-only-iod-card.md | 1 | 0 | 1 | 0 | 1 | 1 | FAIL |
| space-conjunction-assessment-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| space-integrating-propagator-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| space-jacchia-roberts-atmosphere-card.md | 1 | 0 | 1 | 1 | 1 | 0 | FAIL |
| space-lambert-solver-card.md | 1 | 0 | 1 | 0 | 1 | 0 | FAIL |
| space-libration-point-card.md | 1 | 1 | 1 | 1 | 1 | 0 | FAIL |
| space-nasa-breakup-model-card.md | 1 | 0 | 1 | 1 | 1 | 1 | FAIL |
| space-norad-orbital-propagator-card.md | 0 | 0 | 0 | 0 | 0 | 1 | FAIL |
| space-orbital-event-condition-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| space-orbital-maneuvers-card.md | 1 | 0 | 1 | 1 | 1 | 0 | FAIL |
| space-piecewise-exponential-atmosphere-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| space-rendezvous-targeting-card.md | 1 | 0 | 1 | 0 | 1 | 0 | FAIL |
| space-solar-terminator-card.md | 0 | 0 | 0 | 0 | 0 | 0 | PASS |

## 5. 未覆盖 math 函数清单

> **状态**：需人工复核

从 `workspace/source-index/core/function-index.jsonl` 中提取约 **82 个** math 函数，分发到 9 个模块：
wsf (~16), wsf_mil (~22), wsf_nx (~24), wsf_space (~8), sensor_plot_lib (3), wsf_cyber (2), wsf_l16 (3), wsf_parser (4), wsf_util (1)。

- wsf_space 的 8 个 math 函数基本被对应空间卡片覆盖
- wsf 路径查找/外推函数的覆盖需人工确认
- wsf_mil/wsf_nx 中大量电磁/传感器类 math 函数可能属于尚未提取的算法域
- 精确覆盖矩阵需逐函数核对

---

## 附录 A：检测方法说明

### A.1 使用的索引文件
- `workspace/source-index/core/function-index.jsonl`
- `workspace/source-index/wsf_plugins/function-index.jsonl`（无 math 标记函数）

### A.2 使用的模板文件
- `skill/afsim-algorithm-extractor/template_list/template_algorithm-card.md`
- `skill/afsim-algorithm-extractor/template_list/template_interface-spec.md`
- `skill/afsim-analyst/references/output-contracts.md`

### A.3 检测方法
- **章节存在性**：PowerShell 正则匹配 23 张卡片的全部 `###` 和 `####` 级标题
- **内容质量最低检**：伪代码行数>=20、边界条件条目>=3、数学公式条目>=3
- **命名对照**：逐一对比卡片文件名与 Compendium 链接引用
- **接口映射**：卡片 BaseName 与接口规格目录名集合差运算

### A.4 不确定项
- **math 函数全覆盖**：82 个函数中部分属传感器/通信域，需人工确认是否遗漏
- **接口规格内容质量**：本次聚焦映射关系和章节结构，未逐份深度审查接口定义准确性

### A.5 伪代码质量数据（抽样）

| 卡片 | 伪代码行数 | 注释行数 | 状态 |
|------|-----------|---------|------|
| flight-dynamics-autopilot-pid-card.md | 207 | ~70 | PASS |
| flight-dynamics-rigid-body-integrator-card.md | 203 | ~68 | PASS |
| space-conjunction-assessment-card.md | 209 | ~70 | PASS |
| space-solar-terminator-card.md | 204 | ~68 | PASS |
| flight-dynamics-p6dof-heun-integrator-card.md | 170 | ~57 | PASS |
| space-orbital-event-condition-card.md | 98 | ~33 | PASS |
| space-piecewise-exponential-atmosphere-card.md | 33 | ~11 | PASS（内容完整，算法简单） |