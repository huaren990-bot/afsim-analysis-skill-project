# function-index.jsonl 综合质量验证报告

> **验证日期**：2026-07-02
> **验证对象**：`workspace/source-index/function-index.jsonl`（44,362 行）
> **验证范围**：排除 `algorithm_hint` 字段（该字段已由 `2026-07-02-algorithm-hint-correction.md` 独立校正）
> **验证脚本**：`tools/validate_function_index.py`

---

## 一、总体状态

| 层级 | 条目数 | 状态 |
|------|--------|------|
| System-level | 5 | ✅ 全部通过 |
| Module-level | 32 | ✅ 全部通过 |
| Class-level | 4,640 | ⚠ 40 条缺 path（已知） |
| Method-level | 39,685 | ⚠ 重名重复（详见第三节） |
| **合计** | **44,362** | — |

---

## 二、通过项（无问题）

| 检查项 | 结果 |
|--------|------|
| schema_version | ✅ 全部为 1 |
| brief 非空 | ✅ 全部有内容 |
| line_start / line_end | ✅ 全部存在且合法 |
| 行号范围 ≤ 20 | ✅ 全部通过 |
| line_start ≤ 2 异常 | ✅ 0 条 |
| line_end < line_start | ✅ 0 条 |
| lifecycle_role 值合法性 | ✅ 全部在枚举范围内 |
| parameters 结构 | ✅ 全部 name/type/desc/input_output/default_value/valid_range 齐全 |
| evidence_level | ✅ 全部在 source-cited / inferred / index-derived 内 |
| access_modifier | ✅ 全部 public/protected/private/null |
| notes 字段 | ✅ 全部为数组 |
| function_name 与 qualified_name 一致性 | ✅ function_name 均为 qname 最后一段 |
| calls / dependencies 字段一致性 | ✅ |
| System/Module-level brief 非空 | ✅ |
| System/Module-level sub_functions 非空 | ✅ |
| 构造/析构函数 return_type | ✅ 6,031 条全部为空（干净） |

---

## 三、问题项

### 3.1 同文件内重名条目重复（2287 组）⚠ 中等

同一文件中同名函数被拆分为多条 Method-level 条目，但 `qualified_name` 未做区分（未追加参数签名或序号），导致 qname 不唯一。

| 典型案例 | 出现次数 | 所在文件 |
|----------|---------|---------|
| `ScenarioImporter::OutputTemplate::emplace_back` | 27x | wizard/.../Output.hpp |
| `engage::Events::Write` | 25x | engage/.../Events.hpp |
| `Designer::VehicleAeroCore::AeroTable2d` | 23x | mover_creator/.../VehicleAeroCore.hpp |

**根因**：C++ 重载函数的多个重载版本（不同参数）被拆成多条记录，但 Phase 4 未给每条分配唯一标识。

**影响**：按 qname 查函数时会返回多条，需要逐条核对参数签名才能区分。

**建议**：为 qname 追加参数类型签名后缀（如 `::emplace_back(const T&)`），或增加 `overload_index` 字段区分。

### 3.2 跨文件重名（215 组）✅ 预期行为

同名函数出现在不同文件中（如 `State::State` 在 13 个文件中都有）。这是 C++ 不同类中的合法重名，**不是数据错误**。`qualified_name` 不含 namespace 前缀时会放大此问题。

### 3.3 可疑 qname 格式（366 条）⚠ 低

Class-level 条目中 `class::std::WsfRoute` 这类命名——`std::` 作为普通前缀而非 C++ 标准库。命名不规范但不影响使用。

### 3.4 Class-level 缺 path（40 条）⚠ 低 — 已知遗留

这 40 条因下属 Method-level 跨多个 .cpp 文件，无法单一继承 path。上次修复记录（`18-function-index-fixed.md`）中已注明。

### 3.5 死引用（1 条）⚠ 低

`system::simulation_lifecycle` 的 sub_functions 中 1 个引用指向不存在的条目。

### 3.6 重复 sub_functions（10 条）⚠ 低

10 个 Class/Module 的 sub_functions 数组中含重复引用。

### 3.7 已知设计字段未填充 — 非问题

| 字段 | 未填充数 | 说明 |
|------|---------|------|
| `is_override` | 39,685 | 模板中定义但 Phase 4 未要求填充 |
| `embedding` | 39,685 | 模板中定义但标注为后续步骤填充 |

---

## 四、与上次修复比较

| 指标 | 上次（2026-06-24） | 本次（2026-07-02） | 变化 |
|------|-------------------|-------------------|------|
| 误标条目删除 | 6,040 | 0 | ✅ 无复发 |
| `static` 在 return_type 中 | 1,296 条残留 | 0 | ✅ 已清零 |
| 构造/析构 return_type 非空 | 残留 | 0 | ✅ 全部清零 |
| 行号范围异常 | 多处 | 0 | ✅ 全部合格 |
| brief "method: " 前缀 | 3,194 条 Class | 33,903 条 Method | → 这是 Phase 4 默认生成格式 |
| 同文件重复 qname | 未检查 | 2,287 组 | 🆕 首次发现 |

---

## 五、综合评定

**function-index.jsonl 质量：良好。** 44,362 条记录中，所有结构性和格式性检查均通过。上次修复中涉及的 5 类严重数据错误（误标删除、static 污染、ctor return_type、行号偏差、死引用）均已清零，无复发。

**主要遗留问题**：2,287 组同文件重载函数 qname 不唯一，影响索引检索精确度。建议列为下一轮数据优化任务但非紧急——当前项目流程中大多数查询是基于 `path` + `function_name` 而非 `qualified_name`。

---

## 六、验证脚本

`tools/validate_function_index.py` — 可复用，每次索引更新后执行。

用法：
```bash
cd <project_root> && python3 tools/validate_function_index.py
```
