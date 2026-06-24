---
name: cpp-proj-lifecycle-verify
description: Phase 6 验证: 检查 lifecycle.md、dataflow.md、extension-points.md 的覆盖完整性、Mermaid 可追溯性。
metadata:
  phase: 6
  role: verifier
  verifies: cpp-proj-lifecycle
---

# Phase 6 验证: 生命周期与数据流分析

## 目标

验证 Phase 6 分析 Agent (`cpp-proj-lifecycle`) 的产出质量。

## 验证对象

- `docs/architecture/lifecycle.md`
- `docs/architecture/dataflow.md`
- `docs/architecture/extension-points.md`

## 验证步骤

### 检查 1: 生命周期阶段覆盖率

1. lifecycle.md 应覆盖以下 8 个阶段：entry, scenario_load, object_create, simulation_loop, model_update, event_handling, output, shutdown。
2. 对每个阶段，检查是否包含：
   - 入口函数（至少 1 个）
   - 关键类（至少 2 个）
   - 配置来源
   - 主要状态对象
   - 证据位置

### 检查 2: 生命周期调用链可追溯性

1. 从 lifecycle.md 中提取所有提到的函数调用（`xxx() → yyy()` 格式）。
2. 随机抽样 10 条调用，在 function-index.jsonl 中查找对应条目。
3. 追溯率 ≥ 80%。
4. 检查每条调用是否同时包含调用方位置、被调用方位置、证据来源和中文说明；仅有 `A() → B()` 的条目判定为过简。

### 检查 3: 数据流关键对象覆盖率

1. 统计 dataflow.md 中识别的关键数据对象数 K。
2. K ≥ 5。
3. 每个数据对象是否包含：类型、生产者、消费者、生命周期阶段。

### 检查 4: 数据流路径完整性

1. 对每个数据流路径，检查是否按 `state_source → state_owner → update_function → consumers → outputs` 模式描述。
2. 每个环节是否有可追溯的源码位置。
3. 检查关键数据对象是否存在 Mermaid 节点映射表，且节点 ID 与图中一致。
4. 检查每条数据流链路是否有逐步中文解释，说明数据来源、持有者、更新函数、消费者和输出影响。

### 检查 5: 扩展点覆盖率

1. 统计 extension-points.md 中识别的扩展机制数 E。
2. E ≥ 3。
3. 每种扩展机制是否包含：名称、关键接口/基类、注册位置、至少一个使用示例。
4. 检查文档开头是否解释扩展点分析的作用。
5. 检查每种扩展机制是否包含用途说明和运行时影响。

### 检查 6: 扩展点与 dependency-index 交叉验证

1. 从 dependency-index.jsonl 中筛选 `relation=registration` 的条目。
2. extension-points.md 是否覆盖了这些注册依赖的主要模式。

### 检查 7: Mermaid 图语法检查

1. 验证所有 Mermaid 代码块语法正确（至少 tag 闭合正确）。
2. 检查 Mermaid 图中是否有孤立节点（无边连接）。

### 检查 8: 配置流说明质量

1. 检查配置流章节是否解释“配置文件如何转化为运行时对象属性/注册/行为”。
2. 每条配置流必须包含配置来源、解析函数、目标对象、影响的运行时行为和证据位置。
3. 只有图或只有表格、没有中文解释的配置流判定为不通过。

## 输出

生成验证报告 `docs/verification/phase6-verify-report.md`。

## 质量门槛

1. lifecycle.md 覆盖 8 个阶段（缺一不可），每个阶段含关键函数。
2. dataflow.md 含 ≥ 5 个关键数据对象。
3. extension-points.md 含 ≥ 3 种扩展机制。
4. 调用链追溯率 ≥ 80%。
5. 调用链、数据流、配置流、扩展点均必须有中文解释和源码证据位置。
