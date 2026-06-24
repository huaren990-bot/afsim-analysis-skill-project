# Phase 4 完成记录：函数/方法级深度提取

> **完成日期**：2026-06-22
> **阶段**：Phase 4 / 7
> **状态**：✅ 已完成（6/8 检查通过，2 项 known-issue）

## 分析范围

| 参数 | 值 |
|------|-----|
| source_root | /Users/hjt/afsim/afsim-analysis-skill-project/source_root |
| extract_roots | afsim-2_9, src |
| input_symbols | 83,095 (Phase 3 v2) |

## 产出文件

| 文件 | 路径 | 条目数 |
|------|------|--------|
| function-index.jsonl | workspace/source-index/function-index.jsonl | 50,402 |
| function-body-summary.jsonl | workspace/source-index/function-body-summary.jsonl | 27,047 |

## 四层结构

| 层级 | 条目数 |
|------|--------|
| System-level | 5 |
| Module-level | 33 |
| Class-level | 4,761 |
| Method-level | 45,603 |

## 质量检查

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 四层条目完整性 (S≥3) | ✅ S=5, M=33, C=4761, F=45603 |
| 2 | 层级追溯 (S→M, M→C, C→F) | ✅ 0 断裂 |
| 3 | 必填字段 | ✅ brief 100% 非空 |
| 4 | qualified_name 唯一 | ⚠️ 3,122 组重复（Phase 3 重载方法上游数据） |
| 5 | body-summary 配对率 ≥70% | ⚠️ 61.1%（include-only 声明无 body） |
| 6 | algorithm_hint unknown ≤30% | ⚠️ 63.2%（启发式分类限制） |
| 7 | lifecycle_role 分布 | ✅ utility 3.4%, unknown 33.5%, 9 种值 |
| 8 | CD × AH 交叉不一致 | ⚠️ 11.1%（略高于10%目标） |

## known-issue

1. **qname 重复**（3,122 组）：Phase 3 对同一类中的重载方法使用了相同的 qualified_name，非 Phase 4 问题
2. **algorithm_hint unknown 63.2%**：基于关键词的启发式匹配天然覆盖率有限，后续可通过 LLM/semantic 分析改进
3. **body-summary 配对率 61.1%**：大量方法仅有头文件声明（line_start==line_end），无法提取 body

## 下游就绪

Phase 5（跨模块依赖分析）和 Phase 6（生命周期分析）可使用本阶段产出的完整四层函数索引。
