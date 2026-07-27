---
name: fu-design-generation-verify
description: 验证 migration-planner 生成的 FU 迁移设计、确认版和 migration-function JSONL 是否与需求缺口一致、AFSIM 证据真实、接口/单位/状态/数据流完整并具有可执行测试方案。用于迁移计划验收和修复后复验，不生成代码。
---

# FU 迁移设计验证

## 输入

- 已验证 gap-specs 与需求映射报告
- `<req-id>-FU-design.md`
- 可选的 `<req-id>-FU-design-confirmed.md`
- `<req-id>-migration-function.jsonl`
- 当前 AFSIM 索引与真实源码
- 目标系统接口与构建约定
- 人工确认记录

## 检查

### 1. JSONL

- 逐行解析，每行对应一个拟实现函数。
- `function_id` 唯一，`fu_id` 均存在于 gap-specs。
- 必填字段含职责、签名、接口、状态/副作用、依赖、来源、测试、风险和 approval。
- 不接受把整个执行摘要写成唯一 JSON 行。

### 2. FU 与函数覆盖

- 每个需迁移 FU 至少映射一个函数。
- 每个函数追溯到 REQ、FU 和验收标准。
- 函数分解符合单一职责且可独立测试。
- 文档章节与 JSONL 的函数集合完全一致。

### 3. AFSIM 来源逻辑

若 `exists_in_afsim == true`：

- candidate、qualified name、class/method、file、line range 完整。
- 当前索引和真实源码可复核，并支持所述行为。

若 `exists_in_afsim == false`：

- AFSIM 类、方法、文件和行号为空。
- `design_basis` 非空；novel 项的 `search_scope` 非空。

任何真假标记与定位字段矛盾均为阻断缺陷。

### 4. 接口与数据流

- 类型、单位、坐标系、约束、所有权、错误语义和线程安全明确。
- 文档、JSONL、gap-specs 三者一致。
- 所有中间输入/输出有来源/消费者；系统边界和持久状态已标注。
- 初始化、更新、重置、复制/移动和终止策略完整。

### 5. 依赖与策略

- 依赖按标准库、第三方、AFSIM 框架、平台/构建分类。
- 每个 AFSIM 依赖有保留、替换或移除方案。
- migration approach 与许可证、耦合和证据相符。
- clean-room/novel 边界和设计依据可审查。

### 6. 测试可执行性

每个函数有正常、边界、退化/异常测试，并提供可判定 oracle、容差和必要测试数据。只写“与 AFSIM 对比”但没有输入、输出和容差不通过。

### 7. 确认版

确认版存在时：

- 所有阻塞问题已关闭。
- approval 为 approved，包含版本、确认来源和日期。
- 未选方案、空白填写区和占位符已移除。
- 确认版与 JSONL 完全一致。

## 通过门禁

不采用“通过多数检查即可通过”。JSONL 可解析、FU/函数覆盖、来源逻辑、接口一致性、数据流、测试 oracle 和确认状态全部为硬门禁。

## 输出

写入 `docs/verification/migration-plan-<req-id>-verify-report.md`，包含范围、逐项结果、缺陷严重程度、FU/function 定位、最小修复建议和结论：`通过`、`修复后复验` 或 `上游阻塞`。
