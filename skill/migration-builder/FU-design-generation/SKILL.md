---
name: migration-planner
description: 将 requirement-mapping 生成并验证的 AFSIM 功能缺口 FU 转化为可逐函数审查的迁移设计，完成源码证据复核、耦合与许可证评估、目标接口映射、状态生命周期、错误处理、测试策略和人工确认，产出确认版 FU 设计与 migration-function JSONL。用于迁移实施前设计；不生成最终代码。
---

# AFSIM 功能迁移设计

只规划已确认需求和已验证 FU。AFSIM 参考实现用于理解和设计，不默认获得复制源码的许可。

## 输入门禁

必须读取：

- `docs/requirements/<req-id>/3_<req-id>-requirement-gap-analysis.md`
- `docs/requirements/<req-id>/3_<req-id>-function-mapping-matrix.md`
- `docs/requirements/<req-id>/3_<req-id>-requirement-to-afsim-trace.md`
- `workspace/requirements/<req-id>/<req-id>-gap-specs.jsonl`
- requirement-mapping 验证报告
- 目标系统接口、编码规范、构建方式和落盘目录；缺失时列为阻塞或明确假设

按需读取完整算法卡片、接口规格、AFSIM 索引和真实源码。若 requirement-mapping 未通过，不进入确认版设计。

## 工作流

### 1. 校验 FU 基线

逐行解析 gap-specs，核对 FU/REQ ID、验收标准、接口、单位、坐标系、数据流、AFSIM 证据和迁移方式。任何 `unknown`、断链或相互矛盾先退回上游。

### 2. 复核 AFSIM 证据

对 `missing_with_afsim_reference` 或 `partial` FU：

- 打开 `qualified_name` 对应的真实源码。
- 核对路径、行号、输入输出、状态读写、生命周期和依赖。
- 列出标准 C++、第三方库、AFSIM 框架、平台/构建依赖。
- 检查许可证或用户给出的使用边界。

未验证或许可证不明确时，计划采用 `cleanroom`：只基于可审查行为、公式、接口和测试 oracle 重实现，不复制实现表达。

对 `missing_without_afsim_reference` FU，AFSIM 源位置必须为空，设计依据使用用户提供或后续验证的领域资料；不得伪造 AFSIM 类/函数。

### 3. 把 FU 分解为函数

按单一职责、独立测试、状态所有权和可读性分解。每个函数定义：

- 稳定 `function_id`、`fu_id`、名称和职责。
- 完整签名、输入输出、单位、坐标系、约束和错误语义。
- 读写状态、副作用、线程安全与生命周期。
- 输入来源和输出消费者。
- AFSIM 参考或非 AFSIM 设计依据。
- 依赖、替换方案和边界条件。
- 验收测试与 oracle。

不要把一个 FU 机械等同于一个函数，也不要把仅为日志/包装的步骤拆成无价值函数。

### 4. 选择迁移策略

- `direct_adaptation`：许可证允许、耦合低、接口变化小。
- `partial_rewrite`：保留可用结构，替换框架/类型/状态管理。
- `cleanroom`：参考行为与算法规格独立重实现。
- `novel`：记录范围内没有 AFSIM 参考，根据经验证的外部设计依据全新设计。

记录选择原因、被否决方案和风险。不可仅按 gap-specs 的建议字段自动决定。

### 5. 设计测试

每个函数至少定义正常、边界、退化/异常测试；数值算法增加基准值、容差、守恒量/单调性/范围等 oracle。端到端 FU 测试覆盖数据流、状态初始化/重置和目标系统接入点。

### 6. 生成设计

读取 `skill/migration-builder/template_list/template_FU-migration.md`，生成：

- `docs/migration/<req-id>/<req-id>-FU-design.md`
- `workspace/migration/<req-id>/<req-id>-migration-function.jsonl`

JSONL 每行一个拟实现函数，不是一次执行的摘要事件。按
`skill/migration-builder/template_list/template_migration-function.md` 生成。

`source_location` 规则：

- `exists_in_afsim == true`：`candidate_id`、`qualified_name`、`class_name`、`method_name`、`file`、`line_start`、`line_end` 必须来自已验证 AFSIM 证据。
- `exists_in_afsim == false`：上述 AFSIM 定位字段为空字符串或 `null`，并填写 `design_basis` 与 `search_scope`。

### 7. 人工确认

待确认版只突出真正需要选择的接口、单位、依赖、策略和未决问题。根据反馈修订并保留修订记录。全部阻塞项关闭后生成：

- `docs/migration/<req-id>/<req-id>-FU-design-confirmed.md`

确认版删除空白填写区和未选方案，保留已批准决策、确认来源、日期和版本。同步更新 JSONL 的 `approval.status`、版本和接口，确保文档与机器规格一致。

### 8. 验证和留痕

按 `SKILL_VERIFY.md` 验证，写入
`docs/verification/migration-plan-<req-id>-verify-report.md`。在
`docs/records/<date>-migration-plan-<req-id>.md` 记录输入版本、设计决策、证据、反馈、产物和未决风险。

## 完成门禁

- 所有 FU 与函数均能追溯到需求和验收标准。
- AFSIM 定位字段与 `exists_in_afsim` 逻辑一致。
- 文档与 JSONL 的签名、单位、状态、依赖和策略一致。
- 数据流、生命周期、错误处理和测试 oracle 完整。
- 所有实施阻塞项已关闭并有人工确认记录。
- 不记录隐藏推理过程。
