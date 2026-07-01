---
name: FU-design-generation-verify
description: 功能单元迁移设计验证: 检查 <requirement_index>-FU-design.md 和 migration-function.jsonl 的输出质量、完整性、模板合规性。
metadata:
  phase: FU-design-generation
  role: verifier
  verifies: afsim-migration-builder
---

# FU-design-generation 验证: 迁移设计文档质量检查

## 目标

验证 FU-design-generation Skill (`SKILL.md`) 的产出质量，确保输出文档完整、格式正确、模板合规、与输入一致。

## 验证对象

- `docs/migration/<requirement_index>/<req_index>-FU-design.md`
- `workspace/migration/<requirement_index>/<requirement_index>-migration-function.jsonl`
- `docs/records/` 操作留痕文件

## 验证步骤

### 检查 0: FU-design.md 文件存在性与基本完整性

1. 文件存在于 `docs/migration/<requirement_index>/` 目录下。
2. 文件非空且行数 > 100。
3. 所有 mermaid 代码块语法正确（````mermaid` ... ```` 闭合完整，无孤立开标签）。
4. 文件以"修订记录"表格结尾。

### 检查 1: 文档头部完整性

逐项检查必填字段：

| # | 字段 | 检查方式 |
|---|------|---------|
| 1 | `需求编号` | 直接读取，非空 |
| 2 | `需求名称` | 直接读取，非空 |
| 3 | `文档状态` | 合法值：草稿 / 待确认 / 已确认 |
| 4 | `生成时间` | 日期格式合法 |
| 5 | `设计者` | 非空 |
| 6 | `关联文件` | 非空列表，至少含 gap-specs.jsonl 和算法卡片 |

### 检查 2: 全局设计约定章节完整性

1. `### 目标系统环境` 表格存在且含：语言标准、数学库、构建系统、目标平台、代码目录。
2. `### 全局类型映射` 表格存在且含至少 3 行映射（`double`、`UtVec3dX`、`UtQuaternion` 等）。
3. `### 全局单位约定` 表格存在且含：位置、速度、质量、力、力矩等至少 5 行映射。

### 检查 3: 实现流程章节完整性

1. `## 实现流程` 大章节存在。
2. 包含至少 1 个 mermaid `sequenceDiagram`（展示 FU 间数据流）。
3. 包含接口信息表（流程步骤→函数→所属FU→输入来源→输出去向）。

### 检查 4: FU 章节完整性与模板合规性

对照 `workspace/requirements/gap-specs.jsonl`+`docs/requirements/<requirement_index>/3_<requirement_index>-requirement-gap-analysis.md` 中的每个 FU，检查是否存在对应章节且结构完整：

1. `## FU-{XXX}：{名称}` 章节标题存在。
2. FU 属性表含必填字段：关联需求、优先级、来源类型、设计版本、设计日期、迁移策略、风险评估。
3. 子章节齐全（按模板顺序）：
   - `### 功能概述`：存在且与`requirement-gap-analysis`文档中一致。
   - `### 算法流程`：含 `#### 算法流程图如下：` + mermaid `flowchart` + `#### 关键算法` + 公式（LaTeX `$...$`）+ 引用链接。
   - `### 接口详细定义（API）`：含函数签名 + 输入参数详细表 + 配置参数详细表 + 依赖 + 设计确认勾选框
   - `### 接口详细定义（API）`：输入参数详细表 + 配置参数详细表涵盖`requirement-gap-analysis`中的所有参数
   - `### 接口详细定义（API）`：依赖涵盖`requirement-gap-analysis`中的所有库和头文件
   - `### 耦合度评估`：含 框架/数据/控制/外部 四维度+ 综合等级 + 剥离策略。
   - `### 内部状态与生命周期`：含状态变量表格 + reset/拷贝说明。
   - `### 错误处理策略`：含异常场景表格（至少 3 行）。
   - `### 风险与未决问题`：含至少 1 条技术风险。
   - `**修改要求**`：留出人工修改要求填写部分。


### 检查 5: migration-function.jsonl 格式与字段完整性

1. 文件存在且非空。
2. 逐行解析 JSON，无解析错误。
3. 每条记录含必填字段：`event`、`req_index`、`req_name`、`file`、`fu_count`、`fu_list`、`status`、`generated_at`。
4. `file` 字段路径与实际文件路径一致。
5. `fu_count` 与 `fu_list` 数组长度一致。
6. `fu_list` 中的 FU 名称与 FU-design.md 中的章节标题匹配。

### 检查 6: 操作留痕完整性

1. `docs/records/` 目录下存在与 FU-design-generation 相关的操作留痕文件。
2. 留痕文件含：日期、操作描述、输出文件清单。
3. 留痕中的文件路径与实际输出一致。

## 输出

生成验证报告 `docs/verification/FU-design-generation-verify-report.md`，包含：

```markdown
# FU-design-generation 验证报告

> **日期**：YYYY-MM-DD
> **验证对象**：<req_index>-FU-design.md, migration-function.jsonl, 操作留痕

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 0 | 文件存在性与基本完整性 | ✅/❌ | ... |
| 1 | 文档头部完整性 | ✅/❌ | ... |
| 2 | 全局设计约定完整性 | ✅/❌ | ... |
| 3 | 实现流程章节完整性 | ✅/❌ | ... |
| 4 | FU 章节完整性与模板合规性 | ✅/❌ | ... |
| 5 | migration-function.jsonl 完整性 | ✅/❌ | ... |
| 6 | 操作留痕完整性 | ✅/❌ | ... |

## 不通过项详情

（逐项说明不通过的原因和建议修复方法）

## 总体评价

- 通过项：N/7
- 不通过项：M/7
- 建议：通过 / 修正后重新验证 / 人工介入
```

## 质量门槛

1. 7 项检查中至少 5 项通过。
2. 检查 4（FU 章节完整性）和检查 5（migration-function.jsonl）必须通过。
3. 如有不通过项，明确写出修复指引。
