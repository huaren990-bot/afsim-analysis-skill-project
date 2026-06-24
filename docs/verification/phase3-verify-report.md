# Phase 3 v2 验证报告：独立验证修复版

> **完成日期**：2026-06-17
> **阶段**：Phase 3 / 7
> **版本**：v2（针对独立验证报告 10 个问题的修复版）

## 验证对象

- `source-index/symbol-index.jsonl`（精细化版，含 69,159 个独立成员条目）
- `source-index/macro-index.jsonl`（9,381 个宏定义）
- `source-index/enum-index.jsonl`（814 个枚举）

## 10 个问题修复状态

| # | 问题 | 优先级 | 状态 | 详情 |
|---|------|--------|------|------|
| 1 | 符号索引粒度缺少成员独立条目 | High | ✅ 已修复 | 新增 method:39,820, constructor:3,805, destructor:1,978, variable:23,556 |
| 2 | 6 个模板必填字段为空 | High | ✅ 已修复 | access_modifier:83.2%, is_virtual:54.9%, is_static:83.2%, is_const:83.2%, definition_path:55.6%, initial_value:2.9% |
| 3 | member_variables 准确性低 | Medium | ✅ 已修复 | 嵌套类成员隔离；零成员类为 0 个 |
| 4 | 构造/析构函数遗漏 | Medium | ✅ 已修复 | constructor:3,805, destructor:1,978 独立条目 |
| 5 | 多行宏 replacement 丢失 | High | ✅ 已修复 | replacement 为空 function_like 宏：从 37→2 个 |
| 6 | 宏名含数字误判为 function-like | Medium | ✅ 已修复 | aero2: has_params=False; 96个末尾数字宏中的80个是合法function-like宏 |
| 7 | 模板字段/枚举值不合规 | High | ✅ 已修复 | macro_type 统一为 constant/expression/function_like；enum values.brief:100%；字段名已修正 |
| 8 | qualified_name 大量重复 | Medium | ✅ 已修复 | 通过命名空间前缀去重 |
| 9 | signature 偶发错误 | Low | ⚠️ known-issue | WSF_PARSER_EXPORT/WsfParseError 为 Phase 1/2 数据问题（0.0024%） |
| 10 | 枚举行号偏移 | Low | ✅ 已修复 | 括号匹配计算 end_line |

## 核心统计数据

| 指标 | Phase 2 粗版 | Phase 3 v2 |
|------|:-----------:|:-----------:|
| 总符号数 | 13,936 | **83,095** |
| class 含 signature | ~70% | **99.9%** |
| class 含 base_symbols | ~22% | **63.4%** |
| 成员函数独立条目 | 0 | **45,603** |
| 成员变量独立条目 | 0 | **23,556** |
| 宏定义 | 0 | **9,381** |
| 枚举（含完整 values） | 0 | **814（809 含 values）** |

## 字段覆盖率（symbol-index）

| 字段 | 非空数 | 比例 |
|------|--------|------|
| signature | 78,952 | 95.0% |
| access_modifier | 69,159 | 83.2% |
| is_virtual | 45,603 | 54.9% |
| is_static | 69,159 | 83.2% |
| is_const | 69,159 | 83.2% |
| definition_path | 46,213 | 55.6% |
| initial_value | 2,429 | 2.9% |
| base_symbols | 3,766 | 4.5% |

## Kind 分布

| Kind | 数量 |
|------|------|
| method | 39,820 |
| variable | 23,556 |
| class | 4,653 |
| namespace | 4,138 |
| constructor | 3,805 |
| destructor | 1,978 |
| using | 1,824 |
| struct | 1,288 |
| typedef | 1,219 |
| enum | 814 |

## 模板合规性

### macro-index
- 所有 12 个模板必填字段 100% 覆盖
- macro_type 值域：constant (8,718) / expression (415) / function_like (248)
- 无 EXPORT 宏或 include guard 泄漏

### enum-index
- 所有 13 个模板必填字段 100% 覆盖
- 5,181 个枚举值 100% 含 brief 字段
- 2 个枚举 values 为空（Phase, UtStringEnumId）

## known-issue

1. **#9 signature 偶发错误**（2/83,095 = 0.0024%）：`WSF_PARSER_EXPORT`（应为 WsfPProxyDiff）和 `WsfParseError` 的 signature 指向错误，均来自 Phase 2 粗版索引的原始数据问题。
2. **enum_class 0 条目**：代码库中不存在严格的 `enum class` 语法（大部分 C++14 enum class 在 AFSIM 中以 `enum` 形式被识别）。
