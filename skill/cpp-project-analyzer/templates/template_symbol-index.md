# symbol-index.jsonl

## 要求

一行一个符号。覆盖所有 class、struct、enum、typedef、using、macro、variable 定义（剔除前向声明和 `*_EXPORT` 宏）。

## 模板


为每种 `kind` 单独给出**通用字段 + 专用字段**的完整 JSON 模板。

---

## 0. 通用字段定义（所有模板共享）


| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `schema_version` | `int` | ✅ | 固定为 `1`，用于未来格式演进时做兼容判断。 |
| `id` | `string` | ✅ | 全局唯一标识符。建议用 `文件路径:起始行:起始列` 或生成 UUID，用于跨符号引用。 |
| `kind` | `string` | ✅ | 符号类型枚举，取值固定为：<br>`namespace` / `class` / `struct` / `enum` / `enum_class` / `function` / `method` / `constructor` / `destructor` / `typedef` / `using` / `macro` / `variable` / `unknown`。 |
| `name` | `string` | ✅ | 符号的**非限定名**（即最简名称）。例如 `myFunction`、`MyClass`、`MAX_SIZE`。 |
| `qualified_name` | `string` | ✅ | **完全限定名**，包含所有外层命名空间/类。若无法确定或为顶层符号，则直接等于 `name`。例如 `std::vector<int>::size_type`。 |
| `owner` | `string` \| `null` | ✅ | 直接所属容器的完全限定名（命名空间或类）。若为全局作用域（顶层），则为 `null`。例如 `MyNamespace::MyClass`。 |
| `path` | `string` | ✅ | 该符号**定义所在**源文件的相对路径（相对于项目根目录）。如 `src/core/manager.cpp`。 |
| `line_start` | `int` \| `null` | ✅ | 符号定义在源文件中的**起始行号**（1‑based）。若无法获取则为 `null`（例如宏可能跨多行，可只取首行）。 |
| `line_end` | `int` \| `null` | ✅ | 符号定义在源文件中的**结束行号**（1‑based）。若无法获取则为 `null`。 |
| `declaration_path` | `string` \| `null` | ✅ | **声明文件**路径（如 `.h` / `.hpp`）。若该符号无独立声明（如宏、局部变量），或与定义在同一文件，则为 `null`。 |
| `definition_path` | `string` \| `null` | ✅ | **实现文件**路径（如 `.c` / `.cpp`）。若该符号无独立实现（如纯头文件中的内联函数、模板类），或与声明在同一文件，则为 `null`。 |
| `brief` | `string` \| `null` | ❌ | AI 或源码注释提取的**一句话职责摘要**（如 `“负责计算空气动力系数”`）。无则为 `null`。 |
| `responsibility` | `string` \| `null` | ❌ | 更详细的**职责描述**（如 `“根据当前迎角和马赫数查表，并考虑缩减频率修正”`）。无则为 `null`。 |
| `evidence_level` | `string` \| `null` | ❌ | **证据等级**，表示上述职责描述的可信度。建议取值 `high`（源码注释完整）、`medium`（有命名/上下文支撑）、`low`（纯 AI 推断）、`null`（未评估）。 |
| `notes` | `string[]` | ❌ | 补充说明数组，用于记录特殊约束、警告、待办事项等。默认空数组 `[]`。 |
| `used_by` | `string[]` | ❌ | 反向引用数组，记录“有哪些其他符号使用了当前符号”。存储那些符号的 `id` 或 `qualified_name`。默认空数组 `[]`。 |


```json
{
  "schema_version": 1,
  "id": "string (unique)",
  "kind": "string (见各模板)",
  "name": "string",
  "qualified_name": "string",
  "owner": "string | null",
  "path": "string",
  "line_start": "int | null",
  "line_end": "int | null",
  "declaration_path": "string | null",
  "definition_path": "string | null",
  "brief": "string | null",
  "responsibility": "string | null",
  "evidence_level": "string | null",  // "high" | "medium" | "low"
  "notes": "string[]",
  "used_by": "string[]"  // 存放引用该符号的 ID 或 qualified_name
}
```

---

## 1. `namespace`

**专用字段**：无

```json
{
  "schema_version": 1,
  "id": "ns:std",
  "kind": "namespace",
  "name": "std",
  "qualified_name": "std",
  "owner": null,
  "path": "include/namespace_std.cpp",
  "line_start": 1,
  "line_end": 100,
  "declaration_path": null,
  "definition_path": null,
  "brief": "C++ 标准库命名空间",
  "responsibility": "包含所有标准库组件",
  "evidence_level": "high",
  "notes": [],
  "used_by": []
}
```

---

## 2. `class` / `struct` / `union`

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `template_parameters` | `string[]` \| `null` | 模板形参列表，如 `["typename T", "int N"]` |
| `base_symbols` | `string[]` | 直接基类的完全限定名列表 |
| `access_modifier` | `"public"` \| `"protected"` \| `"private"` \| `null` | 自身作为成员时的访问性（顶层为 `null`） |
| `members` | `MemberSummary[]` | 所有直接成员的摘要（变量 + 方法 + 类型别名等） |

其中 `MemberSummary` 结构：
```json
{
  "id": "string",           // 指向该成员完整条目的 ID
  "name": "string",         // 成员名
  "kind": "string",         // variable | method | typedef | ...
  "type": "string | null",  // 变量类型 或 方法返回类型
  "access": "public | protected | private"
}
```

**完整模板**：
```json
{
  "schema_version": 1,
  "id": "class:MyNamespace::MyClass",
  "kind": "class",
  "name": "MyClass",
  "qualified_name": "MyNamespace::MyClass",
  "owner": "MyNamespace",
  "path": "src/core/MyClass.h",
  "line_start": 10,
  "line_end": 45,
  "declaration_path": "src/core/MyClass.h",
  "definition_path": null,
  "brief": "空气动力计算核心类",
  "responsibility": "封装气动系数查表与缩减频率修正",
  "evidence_level": "medium",
  "notes": ["模板参数 T 为浮点类型"],
  "used_by": ["function:main"],
  "template_parameters": ["typename T"],
  "base_symbols": ["BaseObject"],
  "access_modifier": null,
  "members": [
    { "id": "var:MyClass::m_alpha", "name": "m_alpha", "kind": "variable", "type": "double", "access": "private" },
    { "id": "method:MyClass::compute", "name": "compute", "kind": "method", "type": "void", "access": "public" }
  ]
}
```

---

## 3. `enum` / `enum_class`

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `enumerators` | `{ name: string, initial_value?: string }[]` | 枚举值列表 |
| `is_scoped` | `bool` | 是否为 `enum class`（可从 `kind` 推断，但显式标出） |

**完整模板**：
```json
{
  "schema_version": 1,
  "id": "enum:MyNamespace::Color",
  "kind": "enum_class",
  "name": "Color",
  "qualified_name": "MyNamespace::Color",
  "owner": "MyNamespace",
  "path": "src/core/Color.h",
  "line_start": 5,
  "line_end": 10,
  "declaration_path": "src/core/Color.h",
  "definition_path": null,
  "brief": "颜色枚举",
  "responsibility": "定义红绿蓝三原色",
  "evidence_level": "high",
  "notes": [],
  "used_by": ["class:MyNamespace::Painter"],
  "enumerators": [
    { "name": "RED", "initial_value": "0" },
    { "name": "GREEN", "initial_value": "1" },
    { "name": "BLUE", "initial_value": "2" }
  ],
  "is_scoped": true
}
```

---

## 4. `function`（独立函数，非成员）

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `signature` | `string` | 完整函数签名（含 `const`、`noexcept` 等） |
| `return_type` | `string` | 返回类型（完全限定名） |
| `parameters` | `{ name: string, type: string }[]` | 参数列表（可为空） |
| `is_static` | `bool` | 固定为 `false`（独立函数不可能是静态） |
| `is_const` | `bool` | 固定为 `false`（独立函数不可能是 `const`） |
| `is_virtual` | `bool` | 固定为 `false`（独立函数不可能是虚） |
| `access_modifier` | `null` | 固定为 `null` |

**完整模板**：
```json
{
  "schema_version": 1,
  "id": "function:calculateAero",
  "kind": "function",
  "name": "calculateAero",
  "qualified_name": "calculateAero",
  "owner": null,
  "path": "src/aero/calculator.cpp",
  "line_start": 20,
  "line_end": 55,
  "declaration_path": "src/aero/calculator.h",
  "definition_path": "src/aero/calculator.cpp",
  "brief": "计算空气动力和力矩",
  "responsibility": "根据输入状态量查表计算总气动力与力矩",
  "evidence_level": "high",
  "notes": ["线程安全"],
  "used_by": ["function:main"],
  "signature": "AeroResult calculateAero(double alpha, double beta, double mach)",
  "return_type": "AeroResult",
  "parameters": [
    { "name": "alpha", "type": "double" },
    { "name": "beta", "type": "double" },
    { "name": "mach", "type": "double" }
  ],
  "is_static": false,
  "is_const": false,
  "is_virtual": false,
  "access_modifier": null
}
```

---

## 5. `method`（成员函数）

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `signature` | `string` | 完整函数签名 |
| `return_type` | `string` | 返回类型 |
| `parameters` | `{ name: string, type: string }[]` | 参数列表 |
| `is_static` | `bool` | 是否静态方法 |
| `is_const` | `bool` | 是否 `const` 方法 |
| `is_virtual` | `bool` | 是否虚函数 |
| `override` | `bool` \| `null` | 是否 `override`（C++11） |
| `access_modifier` | `"public"` \| `"protected"` \| `"private"` | 访问性（必填） |

**完整模板**：
```json
{
  "schema_version": 1,
  "id": "method:MyClass::compute",
  "kind": "method",
  "name": "compute",
  "qualified_name": "MyClass::compute",
  "owner": "MyClass",
  "path": "src/core/MyClass.cpp",
  "line_start": 30,
  "line_end": 42,
  "declaration_path": "src/core/MyClass.h",
  "definition_path": "src/core/MyClass.cpp",
  "brief": "执行核心计算",
  "responsibility": "根据当前状态更新内部结果",
  "evidence_level": "medium",
  "notes": [],
  "used_by": ["function:main"],
  "signature": "void compute(double dt) const",
  "return_type": "void",
  "parameters": [{ "name": "dt", "type": "double" }],
  "is_static": false,
  "is_const": true,
  "is_virtual": false,
  "override": null,
  "access_modifier": "public"
}
```

---

## 6. `constructor`（构造函数）

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `signature` | `string` | 构造函数签名（如 `MyClass(int, double)`） |
| `parameters` | `{ name: string, type: string }[]` | 参数列表 |
| `access_modifier` | `"public"` \| `"protected"` \| `"private"` | 访问性 |
| `is_virtual` | `bool` | 构造函数不能为虚，固定为 `false` |
| `is_explicit` | `bool` \| `null` | 是否 `explicit`（单参构造函数） |
| `is_default` | `bool` \| `null` | 是否为默认构造函数（无参） |
| `is_copy` | `bool` \| `null` | 是否为拷贝构造函数 |
| `is_move` | `bool` \| `null` | 是否为移动构造函数 |

**完整模板**：
```json
{
  "schema_version": 1,
  "id": "constructor:MyClass::MyClass",
  "kind": "constructor",
  "name": "MyClass",
  "qualified_name": "MyClass::MyClass",
  "owner": "MyClass",
  "path": "src/core/MyClass.cpp",
  "line_start": 5,
  "line_end": 12,
  "declaration_path": "src/core/MyClass.h",
  "definition_path": "src/core/MyClass.cpp",
  "brief": "默认构造函数",
  "responsibility": "初始化成员变量为默认值",
  "evidence_level": "high",
  "notes": [],
  "used_by": ["function:main"],
  "signature": "MyClass()",
  "parameters": [],
  "access_modifier": "public",
  "is_virtual": false,
  "is_explicit": false,
  "is_default": true,
  "is_copy": false,
  "is_move": false
}
```

---

## 7. `destructor`（析构函数）

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `signature` | `string` | 析构函数签名（如 `~MyClass()`） |
| `access_modifier` | `"public"` \| `"protected"` \| `"private"` | 访问性 |
| `is_virtual` | `bool` | 是否虚析构 |

**完整模板**：
```json
{
  "schema_version": 1,
  "id": "destructor:MyClass::~MyClass",
  "kind": "destructor",
  "name": "~MyClass",
  "qualified_name": "MyClass::~MyClass",
  "owner": "MyClass",
  "path": "src/core/MyClass.cpp",
  "line_start": 15,
  "line_end": 18,
  "declaration_path": "src/core/MyClass.h",
  "definition_path": "src/core/MyClass.cpp",
  "brief": "释放动态资源",
  "responsibility": "释放 m_buffer 指向的内存",
  "evidence_level": "high",
  "notes": [],
  "used_by": [],
  "signature": "~MyClass()",
  "access_modifier": "public",
  "is_virtual": true
}
```

---

## 8. `typedef` / `using`（类型别名）

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `aliased_type` | `string` | 被别名指向的原始类型（完全限定名） |
| `template_parameters` | `string[]` \| `null` | **仅 `using` 支持**模板别名时填写，`typedef` 为 `null` |
| `access_modifier` | `"public"` \| `"protected"` \| `"private"` \| `null` | 若为类成员则必填，否则为 `null` |

**完整模板（`using`）**：
```json
{
  "schema_version": 1,
  "id": "using:MyClass::Ptr",
  "kind": "using",
  "name": "Ptr",
  "qualified_name": "MyClass::Ptr",
  "owner": "MyClass",
  "path": "src/core/MyClass.h",
  "line_start": 8,
  "line_end": 8,
  "declaration_path": "src/core/MyClass.h",
  "definition_path": null,
  "brief": "智能指针别名",
  "responsibility": "简化 shared_ptr<MyClass> 的书写",
  "evidence_level": "high",
  "notes": [],
  "used_by": ["method:MyClass::create"],
  "aliased_type": "std::shared_ptr<MyClass>",
  "template_parameters": null,
  "access_modifier": "public"
}
```

---

## 9. `macro`（宏）

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `replacement_text` | `string` | 宏替换体（如 `x + y` 或 `42`） |
| `is_function_like` | `bool` | 是否带参数的宏（函数式宏） |
| `parameters` | `string[]` \| `null` | 若为函数式宏，记录参数名列表（如 `["x", "y"]`） |
| `initial_value` | `string` \| `null` | 与 `replacement_text` 相同，也可理解为常数值（保留兼容性） |

**完整模板**：
```json
{
  "schema_version": 1,
  "id": "macro:MAX_SIZE",
  "kind": "macro",
  "name": "MAX_SIZE",
  "qualified_name": "MAX_SIZE",
  "owner": null,
  "path": "src/config/defines.h",
  "line_start": 3,
  "line_end": 3,
  "declaration_path": null,
  "definition_path": null,
  "brief": "最大缓冲区大小",
  "responsibility": "定义 1024 作为默认上限",
  "evidence_level": "medium",
  "notes": ["硬编码值，未来可能改为配置项"],
  "used_by": ["variable:buffer"],
  "replacement_text": "1024",
  "is_function_like": false,
  "parameters": null,
  "initial_value": "1024"
}
```

---

## 10. `variable`（变量，含静态成员变量）

**专用字段**：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `type` | `string` | 变量类型（完全限定名） |
| `initial_value` | `string` \| `null` | 初始化表达式（如 `42`、`"hello"`、`nullptr`） |
| `is_const` | `bool` | 是否 `const` |
| `is_static` | `bool` | 是否静态（若为静态成员则为 `true`） |
| `access_modifier` | `"public"` \| `"protected"` \| `"private"` \| `null` | 若为类成员则必填，否则为 `null` |

**完整模板（全局变量）**：
```json
{
  "schema_version": 1,
  "id": "variable:g_debugLevel",
  "kind": "variable",
  "name": "g_debugLevel",
  "qualified_name": "g_debugLevel",
  "owner": null,
  "path": "src/main.cpp",
  "line_start": 15,
  "line_end": 15,
  "declaration_path": null,
  "definition_path": "src/main.cpp",
  "brief": "全局调试级别",
  "responsibility": "控制日志输出详细程度，0=静默，3=最详细",
  "evidence_level": "medium",
  "notes": ["仅在 Debug 构建中有效"],
  "used_by": ["function:logMessage"],
  "type": "int",
  "initial_value": "0",
  "is_const": false,
  "is_static": false,
  "access_modifier": null
}
```

**完整模板（静态成员变量）**：
```json
{
  "schema_version": 1,
  "id": "variable:MyClass::s_instance",
  "kind": "variable",
  "name": "s_instance",
  "qualified_name": "MyClass::s_instance",
  "owner": "MyClass",
  "path": "src/core/MyClass.cpp",
  "line_start": 25,
  "line_end": 25,
  "declaration_path": "src/core/MyClass.h",
  "definition_path": "src/core/MyClass.cpp",
  "brief": "单例实例指针",
  "responsibility": "持有 MyClass 的唯一实例",
  "evidence_level": "high",
  "notes": [],
  "used_by": ["method:MyClass::getInstance"],
  "type": "MyClass*",
  "initial_value": "nullptr",
  "is_const": false,
  "is_static": true,
  "access_modifier": "private"
}
```

