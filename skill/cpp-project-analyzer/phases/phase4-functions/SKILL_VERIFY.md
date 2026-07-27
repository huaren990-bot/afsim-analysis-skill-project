---
name: cpp-proj-functions-verify
description: "Phase 4 验证: 检查 function-index.jsonl 四层完整性、参数覆盖、qualified_name 唯一性、function-body-summary.jsonl 质量。"
metadata:
  phase: 4
  role: verifier
  verifies: cpp-proj-functions
---

# Phase 4 验证: 函数/方法级深度提取

## 目标

验证 Phase 4 分析 Agent (`cpp-proj-functions`) 的产出质量。

## 验证对象

- `source-index/function-index.jsonl`
- `source-index/function-body-summary.jsonl`

## 验证步骤

### 检查 1: 四层条目完整性

1. 统计各层级条目数：
   - System-level 条目数 S
   - Module-level 条目数 M
   - Class-level 条目数 C
   - Method-level 条目数 F
2. **必须** S > 0 且 M > 0 且 C > 0 且 F > 0（四层缺一不可）。
3. S ≥ 3（至少应有 3 个系统级功能）。

### 检查 2: 层级追溯完整性

1. 对每个 System-level 条目，检查其 `sub_functions` 中的每个 qualified_name 是否在 Module-level 中存在。
2. 对每个 Module-level 条目，检查其 `sub_functions` 中的每个 qualified_name 是否在 Class-level 中存在。
3. 对每个 Class-level 条目，检查其 `sub_functions` 中的每个 qualified_name 是否在 Method-level 中存在。
4. 记录追溯断裂的条目（子功能指向不存在的 qualified_name）。

### 检查 3: 必填字段非空检查

1. 所有 System/Module/Class 级条目的 `brief` 非空（不带空格且长度 > 10 字符）。
2. 随机抽样 50 个 Method-level 条目，检查：
   - `parameters` 数组非空（至少含 1 个参数带有 `name` + `type`）。
   - `return_type` 非 "unknown"（至少 80% 的抽样条目）。
   - `lifecycle_role` 非 "unknown"（至少 50% 的抽样条目）。

### 检查 4: qualified_name 唯一性

1. 提取所有条目的 `qualified_name`。
2. 检查是否有重复。如有重复，列出重复的 qualified_name 及出现次数。

### 检查 5: function-body-summary.jsonl 配对率

1. 统计 function-index.jsonl 中 Method-level 条目数 F。
2. 统计 function-body-summary.jsonl 条目数 B。
3. 配对率 = B / F，必须 ≥ 0.70 (70%)。

### 检查 6: algorithm_hint 分布合理性

1. 统计各 algorithm_hint 值的分布。
2. 如果 `unknown` 占比超过 30%，标记为"分类不够精细"。

### 检查 7: parameters 抽样验证

抽样 5 个 Method-level 条目，读取源文件验证：

- **防重复**：按函数所在的 `definition_path`（或 `declaration_path`）分组，每个文件最多读 1 次。若抽样命中同文件的多个函数，合并到一次读取中验证。
- **已读跳过**：维护 `已读文件集合`，抽样时跳过已读文件，选择下一个未读的条目。
- **失败不重试**：若读取文件失败，在报告中标注"无法验证此项"，不重试该文件。

1. 参数列表完整（无遗漏参数）。
2. `default_value` 与源码一致。
3. `type` 与源码一致。

### 检查 8: lifecycle_role 分布合理性

1. 统计各 `lifecycle_role` 值的分布比例。
2. 合理分布参考：
   - `utility` 不应超过 60%（否则说明分类过于笼统）。
   - `model_update` 或 `simulation_loop` 至少有一个 > 0（除非项目不是仿真系统）。
   - `unknown` 不应超过 50%（与检查 3 的 50% 阈值一致，但此处关注全局分布）。
3. 如果 `utility` 占比 > 60%，标记为"分类过于笼统，建议细化"。
4. 如果全部 Method-level 条目都是同一种 `lifecycle_role`，标记为"分类缺失多样性"。

### 检查 9: computation_density 与 algorithm_hint 交叉验证

1. 从 function-body-summary.jsonl 中筛选 `computation_density=high` 的条目。
2. 检查这些条目在 function-index.jsonl 中对应的 `algorithm_hint` 是否为 `math`、`state_update` 或 `integration`。
3. 如果 `computation_density=high` 但 `algorithm_hint=none` 或 `algorithm_hint=io`，标记为"交叉不一致"。

### 检查 10: functions_to_extract 覆盖闭环

1. 从 Phase 3 `symbol-index.jsonl` 中筛选 `kind=function/method/constructor/destructor`，并补充头文件 inline、模板函数、operator、匿名 namespace/static 函数候选。
2. 从 `function-index.jsonl` 中提取 Method-level 条目。
3. 计算候选覆盖率，必须 ≥ 90%。
4. 对未覆盖候选，检查是否记录跳过原因：`declaration_only`、`implicit_special_member`、`macro_generated_unexpanded`、`template_uninstantiated`、`parse_failed`。
5. 未覆盖且无原因的条目判定为遗漏。

### 检查 11: 重载与签名唯一性

1. 检查 Method-level 中是否存在相同 `qualified_name` 但不同 `signature` 的重载。
2. 若存在，`qualified_name` 或唯一键必须能区分签名；否则判定为静默覆盖风险。
3. 检查 `function-body-summary.jsonl` 与 `function-index.jsonl` 的配对是否使用同一唯一键，避免只按短名误配。

### 检查 12: 函数真实性与导出宏过滤

1. 扫描 `function-index.jsonl` 中所有 Method-level 条目，检查 `qualified_name`、`function_name`、`owner` 是否匹配 `.*(_EXPORT|_IMPORT|_API|_LIB_EXPORT)(::.*)?$`。
2. 检查每个 Method-level 条目的 `signature` 是否含 `(` 与 `)`，且不是变量声明、宏替换体或成员变量描述。
3. 特别检查 `POST_PROCESSOR_LIB_EXPORT::max` 这类导出宏伪成员名，必须不存在。
4. 对从候选中过滤掉的项，检查是否在 notes/context-handoff/验证报告中记录 `export_macro_pseudo_symbol` 或 `variable_not_function` 等跳过原因。

## 输出

生成验证报告 `docs/verification/phase4-verify-report.md`。

## 质量门槛

1. 四层条目全部存在。
2. 层级追溯无断裂（100% 子功能可追溯）。
3. System/Module/Class 级 brief 100% 非空。
4. qualified_name 全文件唯一。
5. function-body-summary.jsonl 配对率 ≥ 70%。
6. 参数抽样验证通过率 ≥ 80%（5 个中至少 4 个一致）。
7. `lifecycle_role` 分布合理：`utility` ≤ 60%，`unknown` ≤ 50%，至少有 2 种不同值。
8. `computation_density=high` 与 `algorithm_hint` 交叉不一致率 ≤ 10%。
9. functions_to_extract 覆盖率 ≥ 90%，未覆盖项均有跳过原因。
10. 重载函数和函数体摘要配对不存在静默覆盖风险。
11. Method-level 条目无导出宏伪函数、变量伪函数，且签名可验证。
