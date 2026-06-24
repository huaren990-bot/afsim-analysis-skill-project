# Phase 5 完成记录：跨模块依赖关系分析

> **完成日期**：2026-06-22
> **阶段**：Phase 5 / 7
> **状态**：✅ 全部检查通过

## 分析范围

| 参数 | 值 |
|------|-----|
| source_root | /Users/hjt/afsim/afsim-analysis-skill-project/source_root |
| extract_roots | afsim-2_9, src |
| input | Phase 3 symbol-index (83,095 符号) + Phase 4 function-index (50,402 条目) |

## 产出文件

| 文件 | 路径 | 条目数 |
|------|------|--------|
| dependency-index.jsonl | workspace/source-index/dependency-index.jsonl | 52,996 |
| dependency-graph.md | workspace/architecture/dependency-graph.md | Mermaid 图 + 统计表 |

## 依赖分布

| Relation | 条目数 | 说明 |
|----------|--------|------|
| call | 28,095 | 函数调用关系 |
| composition | 10,402 | 成员变量组合关系 |
| include | 8,736 | 头文件包含关系 |
| inheritance | 3,908 | 类继承关系 |
| registration | 1,557 | 组件/类型注册 |
| build | 298 | CMake 构建依赖 |
| **总计** | **52,996** | 6 种 relation 全覆盖 |

## Strength 分布

| Strength | 条目数 | 占比 |
|----------|--------|------|
| medium | 31,843 | 60.1% |
| strong | 19,596 | 37.0% |
| weak | 1,557 | 2.9% |

## 质量检查

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 条目数 ≥ 200 | ✅ 52,996 |
| 2 | 6 种 relation 全覆盖 | ✅ 每种 ≥ 5 条 |
| 3 | strength null ≤ 5% | ✅ 0% |
| 4 | 跨模块覆盖 | ✅ 7,355 个模块/前缀 |
| — | JSON 解析成功率 | ✅ 100% |
| — | evidence 具体率 | ✅ 20/20 (100%) |

## 下游就绪

Phase 6（生命周期与数据流分析）可使用本阶段的 dependency-index 追踪跨模块数据流和生命周期依赖。
