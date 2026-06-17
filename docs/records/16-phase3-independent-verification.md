# Phase 3 独立验证记录：改进项清单

> **验证日期**：2026-06-17
> **阶段**：Phase 3 / 7
> **验证方式**：6 个并行 Agent 独立验证（统计 3 + 抽样 3），覆盖 SKILL_VERIFY.md 全部 6 项检查 + 模板合规性检查
> **验证对象**：symbol-index.jsonl、macro-index.jsonl、enum-index.jsonl

## 验证总览

| # | 检查项 | 原验证结果 | 独立验证结果 | 需要改进 |
|---|--------|-----------|-------------|---------|
| 1 | class/struct 精细化率 ≥ 85% | ⚠️ known-issue 63.4% | 确认 63.34% | ✅ 见问题 #1 |
| 2 | 访问修饰符覆盖率 ≥ 80% | ✅ 100% | ❌ 不可计算（分母为 0） | ✅ 见问题 #2 |
| 3 | 宏过滤无 EXPORT/guard | ✅ 通过 | 确认 0 条泄漏 | — |
| 4 | 宏抽样验证 | ✅ 10/10 通过 | 5/10 一致，4/10 replacement 缺失，1/10 严重错误 | ✅ 见问题 #5、#6 |
| 5 | enum-index 完整性 | ✅ 通过 | values 完整但模板字段缺失 | ✅ 见问题 #7 |
| 6 | Phase2→Phase3 追溯 100% | ✅ 通过 | 确认 13936/13936 | — |
| — | 模板合规性 | 未检查 | 严重不合规 | ✅ 见问题 #2、#3、#4、#7、#8 |

---

## 需要改进的问题清单

### 问题 #1 [High] symbol-index 索引粒度停留在"声明级"，缺少成员级独立条目

**现象**：symbol-index.jsonl 的 `kind` 字段仅含 6 种值（class/namespace/using/struct/typedef/enum），**完全没有** `function`、`method`、`constructor`、`destructor`、`variable`、`macro`、`enum_class` 类型的独立条目。

**影响**：
- 模板定义了 14 种 kind 值，实际只使用了 6 种（43%）
- 检查 2（访问修饰符覆盖率）因分母为 0 而无法计算
- Phase 4（函数级深度提取）无法基于 symbol-index 的成员函数条目展开
- 成员信息被嵌套在 `member_functions`/`member_variables` 数组字段中（模板外额外字段），而非作为独立条目存在

**建议**：明确 Phase 3 的设计决策——是将成员函数/变量作为独立条目（符合模板），还是继续嵌套在 class/struct 条目中（当前做法）。如果选择嵌套方案，需同步更新模板和 SKILL_VERIFY.md 的检查逻辑。

---

### 问题 #2 [High] symbol-index 6 个模板必填字段完全为空

| 字段 | 非空率 | 说明 |
|------|--------|------|
| `definition_path` | 0% | 声明与实现分离时未识别实现文件 |
| `initial_value` | 0% | 变量/枚举初始值未提取 |
| `access_modifier` | 0% | 因无 method 条目而无法填充 |
| `is_virtual` | 0% | 同上 |
| `is_static` | 0% | 同上 |
| `is_const` | 0% | 同上 |

**建议**：`definition_path` 可通过 grep `.cpp` 文件中的方法实现来补充；其余 5 个字段依赖问题 #1 的解决（需先有 method 条目）。

---

### 问题 #3 [Medium] symbol-index member_variables 准确性低（抽样 40%）

**现象**（15 个样本中 9 个有问题）：
- **漏检**：VisualEffectsPrefData（索引 0 vs 实际 4 个成员）、PlatformState（1 vs 3）、Intersection（1 vs 3）、SurfaceWaveRadarSensorErrorModel（1 vs 5）
- **幻觉/误检**：NewtonRaphson（索引 14 vs 实际 0，纯静态模板类被凭空造出 14 个成员）、WsfEmitterTypeReporting（索引 16 vs 实际 6，嵌套 struct 的成员被错误归入外层类）

**建议**：修复 phase3_process.py 的成员变量提取逻辑——(1) 嵌套类型的成员不应计入外层类；(2) 模板类的静态成员不应被误识别为实例成员。

---

### 问题 #4 [Medium] symbol-index member_functions 系统性遗漏构造/析构函数（抽样 53%）

**现象**：多个条目少计了 constructor/destructor/operator=，可能是解析器对特殊成员函数的处理不完整。
- ActivatePilotCommand：构造函数未计入
- WsfDisDraw：5 个实际方法只记录了 4 个
- WeightedRouteEdge：有 1 个构造函数但索引记录为 0

**建议**：在 phase3_process.py 中补充对 `ClassName(...)` 构造函数、`~ClassName()` 析构函数、`operator=` 等特殊成员函数的识别规则。

---

### 问题 #5 [High] macro-index 多行函数宏 replacement 丢失（抽样 40%）

**现象**：所有使用 `\` 续行的多行函数宏，其 `replacement` 字段均为空字符串。受影响样本：`FORMAT_TIME_STRING`、`WSF_P6DOF_OBSERVER_CALLBACK_DEFINE`、`DEFINE_CONTINUATIONS10`、`UT_SCRIPT_STATIC_VARIADIC_METHOD`。

**影响**：`has_parameters` 和 `macro_type` 判断正确，但 replacement 丢失导致无法了解宏的实际功能。在全部 9106 个宏中，function_like 类型（272 个）可能大量存在 replacement 为空的情况。

**建议**：修改 grep 解析逻辑，对 `#define` 行以 `\` 结尾的宏，继续读取后续续行直到遇到不以 `\` 结尾的行，将完整的多行 body 拼接到 replacement 中。

---

### 问题 #6 [Medium] macro-index 名称含数字的 object-like 宏被误判为 function-like

**现象**：`#define aero2 (2)` 被解析器误识别——名称末尾的数字 `2` 被当作参数列表，导致 `has_parameters=true`、`parameters=['2']`、`macro_type=function_like`、`replacement` 为空。

**建议**：修复正则表达式，确保 `(params)` 紧跟在宏名称后面（无空格），而非匹配名称内部的数字。

---

### 问题 #7 [High] macro-index 和 enum-index 模板字段名/枚举值不合规

#### macro-index.jsonl

| 问题 | 详情 |
|------|------|
| `macro_type` 枚举不合规 | 95.3%（8680/9106）使用了模板外的值：`integer`(8608)、`string`(55)、`boolean`(7)、`float`(6)、`hex_integer`(2)、`numeric`(2)，应统一映射为 `constant` |
| 字段名偏差 | `line_start` → 实际为 `line`；`parameter_names` → 实际为 `parameters` |
| 3 个必填字段缺失 | `estimated_type`(0%)、`brief`(0%)、`used_in_files`(0%) |
| 一致性问题 | 31 条 `has_parameters=true` 但 `parameters=[]`；35 条 `replacement` 为空 |

#### enum-index.jsonl

| 问题 | 详情 |
|------|------|
| values 子字段 schema 不匹配 | 实际为 `{name, value, explicit, comment}`，模板要求 `{name, value, brief}`。`brief` 完全缺失 |
| 3 个必填字段缺失 | `owner`(0%)、`brief`(0%)、`used_in_files`(0%) |
| `underlying_type` 填充率极低 | 仅 2.5%（20/814），且存在疑似截断值 `std`（可能为 `std::uint32_t`） |
| 无 `enum_class` 条目 | 814 条全部为 `enum`，若代码库中存在 `enum class` 则存在分类遗漏 |

**建议**：
- 统一 macro_type 的值域到模板规范，或扩展模板以容纳细粒度分类
- 修正字段名差异（`line` → `line_start`，`parameters` → `parameter_names`）
- enum-index 的 values 子元素添加 `brief` 字段（可从 `comment` 字段映射）
- 检查代码库中是否存在 `enum class` 语法，补充 `enum_class` 分类

---

### 问题 #8 [Medium] symbol-index qualified_name 大量重复（非 namespace 类）

**现象**：排除 namespace 后，889 个名字对应 3,465 条记录存在重复。典型案例：`Plugin`(143 次)、`SimInterface`(46 次)、`FieldType2`(39 次)。

**建议**：检查这些重复项是否因缺少命名空间前缀导致。若同一名称在不同命名空间下存在，`qualified_name` 应包含完整命名空间路径以确保唯一性。

---

### 问题 #9 [Low] symbol-index signature 偶发严重错误（抽样 2/15）

- `WSF_PARSER_EXPORT`：qualified_name 取了导出宏名而非真正的 struct 名 `WsfPProxyDiff`
- `Intersection`：signature 指向了前一个 struct 结尾的 `};` 和 using 声明，完全不是该 struct 的签名

**建议**：修复 phase3_process.py 中对 `*_EXPORT` 前缀的 class/struct 声明的解析逻辑。

---

### 问题 #10 [Low] enum-index line_start/line_end 偶发偏移

**现象**：抽样 10 个枚举中 1 个（AEWEnum）行号偏移约 11 行（索引 265-274，实际 276-285），疑似多枚举密集文件中解析器行号定位逻辑有误。

---

## 改进优先级建议

| 优先级 | 问题 | 工作量 |
|--------|------|--------|
| **P0** | #1 索引粒度决策（声明级 vs 成员级） | 设计决策 |
| **P0** | #7 模板字段名/枚举值合规性 | 脚本修改 |
| **P1** | #5 多行宏 replacement 提取 | 脚本修改 |
| **P1** | #3 member_variables 准确性 | 脚本修改 |
| **P1** | #4 构造/析构函数识别 | 脚本修改 |
| **P2** | #2 必填字段补充 | 依赖 #1 |
| **P2** | #6 宏名含数字的解析 bug | 正则修复 |
| **P2** | #8 qualified_name 去重 | 脚本修改 |
| **P3** | #9 signature 错误 | 边缘 case 修复 |
| **P3** | #10 行号偏移 | 边缘 case 修复 |
