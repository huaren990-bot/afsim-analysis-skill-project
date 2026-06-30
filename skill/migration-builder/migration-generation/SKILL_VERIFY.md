---
name: migration-generation-verify
description: 迁移程序生成验证: 检查 <req_index>-SDD.md 和 REQ_xxx.h、REQ_xxx.cpp、test_demo.cpp、<req_index>/README.md 的输出质量、完整性、模板合规性。
metadata:
  phase: migration-generation
  role: verifier
  verifies: afsim-migration-builder
---

# migration-generation 验证: 迁移设计程序质量检查

## 目标

验证 migration-generation Skill (`SKILL.md`) 的产出质量，确保输出文档完整、格式正确、模板合规、代码质量合格、与输入一致。

## 验证对象

- `docs/migration/<req_index>/<req_index>-SDD.md`
- `tests/migration_src/<req_index>/REQ_xxx.h`
- `tests/migration_src/<req_index>/REQ_xxx.cpp`
- `tests/migration_src/<req_index>/test_demo.cpp`
- `tests/migration_src/<req_index>/README.md`
- `workspace/migration/<req_index>/<req_index>-migration-log.jsonl`
- `docs/records/` 操作留痕文件

## 验证步骤

### 检查 0: SDD.md 文件存在性与基本完整性

1. 文件存在于 `docs/migration/<req_index>/` 目录下。
2. 文件非空且行数 > 80。
3. 所有 mermaid 代码块语法正确（````mermaid` ... ```` 闭合完整，无孤立开标签），每个标签内容均使用双引号包裹。
4. 文件以"附录"或"修改记录"章节结尾。
5. 文件严格遵守模板目录结构。

### 检查 1: 代码文件存在性与基本完整性

| # | 文件 | 检查方式 |
|---|------|---------|
| 1 | `REQ_xxx.h` | 存在、非空、行数 > 30，含头文件保护宏（`#ifndef`/`#define`/`#endif` 或 `#pragma once`） |
| 2 | `REQ_xxx.cpp` | 存在、非空、行数 > 80，含 `#include "REQ_xxx.h"` |
| 3 | `test_demo.cpp` | 存在、非空、行数 > 100，含 `main()` 函数 |
| 4 | `README.md` | 存在、非空、行数 > 15 |

### 检查 2: SDD.md 文档头部与章节完整性

逐项检查必填字段：

| # | 字段/章节 | 检查方式 |
|---|----------|---------|
| 1 | `文档版本` | 直接读取，格式为 `x.y`，非空 |
| 2 | `日期` | 日期格式合法（YYYY-MM-DD） |
| 3 | `作者` | 非空 |
| 4 | `关联需求` | 非空，格式 REQ-XXX |
| 5 | `关联迁移计划` | 非空，指向 `docs/migration/<req_index>/<req_index>-FU-design.md` |
| 6 | `### 1. 目的` | 章节存在且非空 |
| 7 | `### 2. 范围` | 章节存在，列出包含的 FU 及简要功能 |
| 8 | `### 3. 参考文档` | 章节存在，含需求规范、迁移计划、AFSIM 源文件路径（novel FU 替换为文献引用） |
| 9 | `## 测试策略` | 章节存在，含单元测试、集成测试、验证方法 |
| 10 | `## 限制与假设` | 章节存在且非空 |
| 11 | `## 人工确认` | 章节存在，含确认状态表格（需求ID / 确认状态 / 确认人 / 日期） |
| 12 | `## 附录` | 章节存在，含变量映射表和修改记录 |

### 检查 3: SDD.md 功能组件章节模板合规性

对照 `skill/afsim-migration-builder/template_list/template_sdd.md`，检查每个 FU 的功能组件章节：

1. `#### 1.FU-{xxx}:{名称}` 子章节标题存在。
2. `##### 1.1. 功能定位` 小节存在且非空。
3. `##### 1.2. 外部接口` 小节存在，含表格：
   | 序号 | 接口类型 | 参数类型 | 参数 | 参数描述 |
4. `##### 1.3. 运行逻辑` 小节存在，含 mermaid `flowchart` 代码块。
5. `##### 1.4. 数学公式` 小节存在，至少 1 个 LaTeX `$...$` 公式，并且每个公式后必须有公式中数学符号的中文解释说明，如"$x$表示速度"。
6. 对于 novel FU：公式来源标注为领域文献/算法教材引用，而非 AFSIM 源码。

### 检查 4: REQ_xxx.h 模板合规性与代码质量

对照 `skill/afsim-migration-builder/template_list/template_REQ_xxx.h`：

1. 头文件保护宏正确（`#ifndef` / `#define` / `#endif` 配对完整，或 `#pragma once`）。
2. 每个函数声明前有完整的 Doxygen 风格注释（`@brief`、`@param`、`@return` 等）。
3. 每个函数注释中含 FU ID 标识（如 `FU-XXX`）。
4. 每个函数注释中含实现来源：AFSIM 源文件路径 + 行号，或 novel FU 的设计依据文献引用。
5. `<requirement_index>-FU-design.md` 中所有已确认的 FU 接口均在头文件中声明。
6. 必要的 `#include` 和命名空间声明完整。

### 检查 5: REQ_xxx.cpp 模板合规性与代码质量

对照 `skill/afsim-migration-builder/template_list/template_REQ_xxx.cpp`：

1. 每个 FU 实现以 `/* === FU-xxx: 描述 === */` 分段开头。
2. 关键代码逻辑有中文注释（核心算法步骤、边界条件处理、关键决策点）。
3. AFSIM 有参考的 FU：保留原始版权注释（若许可证允许）并标注源位置。
4. novel FU：实现开始处标注设计依据文献引用。
5. 所有与 AFSIM 源码有差异的修改点均有注释说明。
6. 函数签名与 `.h` 文件中的声明一致。

### 检查 6: test_demo.cpp 模板合规性与可运行性

对照 `skill/afsim-migration-builder/template_list/template_test_demo.cpp`：

1. 文件开头注释含编译命令（如 `g++ ...`）和运行方法。
2. 含 `main()` 函数，`main()` 统一调用各测试用例函数。
3. 至少 3 个测试用例函数：
   - 设计为正常情况测试。
   - 设计为边界情况测试。
   - 设计为异常情况测试。
4. 每个测试用例以 `/* --- TC-xxx: 描述 --- */` 开头。
5. 每个测试用例含详细注释和预期输出说明。
6. `main()` 为最简单示例场景，展示核心功能的输入输出。
7. 审查`test_demo.cpp`的逻辑正确性与输出合理性（仅编译通过+PASS标签 ≠ 逻辑正确）：
   1. 逐测试用例审查仿真/计算循环中的代码逻辑：
      - 检查是否存在"计算了但未使用"的变量（变量赋值后从未被后续表达式引用）
      - 检查循环体内所有依赖状态变量是否在每步迭代后更新（避免全循环使用不变的初始值）
   2. 运行并审查输出：
      - 根据输入参数和物理/业务常识预估合理输出区间，比对实际输出是否在该区间内
      - 关注不变量：应变化但始终不变的字段（如位置Z在重力下不降、速度在推力下不变）→ 逻辑缺陷信号
   3. 代码卫生检查：
      - 是否有语义无效的表达式（如零向量加法、乘以1、加0等）
      - 是否有未被调用的函数、未使用的#include、未使用的变量



### 检查 7: README.md 完整性

对照 `skill/afsim-migration-builder/template_list/template_README.md`：

1. 含编译命令（如 g++ 命令行、CMake 等）。
2. 含依赖列表（所需头文件、第三方库、目标系统组件）。
3. 含运行 demo 的步骤说明。
4. 含预期输出示例。
5. 与 SDD 分工明确：不涉及设计细节和算法推导。

### 检查 8: migration-log.jsonl 格式与字段完整性

1. 文件存在于 `workspace/migration/<req_index>/<req_index>-migration-log.jsonl` 且非空。
2. 逐行解析 JSON，无解析错误。
3. 每条记录含必填字段：`event`、`req_index`、`req_name`、`files`、`status`、`generated_at`。
4. `files` 字段为数组，至少包含：`<req_index>-SDD.md`、`REQ_xxx.h`、`REQ_xxx.cpp`、`test_demo.cpp`、`README.md`。
5. `files` 数组中各路径与各文件实际路径一致。
6. 文件的相对路径根目录正确（SDD 在 `docs/migration/<req_index>/`，代码在 `tests/migration_src/<req_index>/`）。

### 检查 9: 操作留痕完整性

1. `docs/records/` 目录下存在与 migration-generation 相关的操作留痕文件。
2. 留痕文件含：操作日期、操作描述、输出文件清单。
3. 留痕中的文件路径与实际输出文件路径一致。

## 输出

生成验证报告，保存到 `docs/verification/migration-generation-verify-report.md`，包含：

```markdown
# migration-generation 验证报告

> **日期**：YYYY-MM-DD
> **验证对象**：<req_index>-SDD.md, REQ_xxx.h, REQ_xxx.cpp, test_demo.cpp, README.md, migration-log.jsonl, 操作留痕

## 检查结果汇总

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 0 | SDD.md 文件存在性与基本完整性 | ✅/❌ | ... |
| 1 | 代码文件存在性与基本完整性 | ✅/❌ | ... |
| 2 | SDD.md 文档头部与章节完整性 | ✅/❌ | ... |
| 3 | SDD.md 功能组件章节模板合规性 | ✅/❌ | ... |
| 4 | REQ_xxx.h 模板合规性与代码质量 | ✅/❌ | ... |
| 5 | REQ_xxx.cpp 模板合规性与代码质量 | ✅/❌ | ... |
| 6 | test_demo.cpp 模板合规性与可运行性 | ✅/❌ | ... |
| 7 | README.md 完整性 | ✅/❌ | ... |
| 8 | migration-log.jsonl 格式与字段完整性 | ✅/❌ | ... |
| 9 | 操作留痕完整性 | ✅/❌ | ... |

## 不通过项详情

（逐项说明不通过的原因和建议修复方法）

## 总体评价

- 通过项：N/10
- 不通过项：M/10
- 建议：通过 / 修正后重新验证 / 人工介入
```

## 质量门槛

1. 10 项检查中至少 8 项通过。
2. 检查 4（REQ_xxx.h 质量）、检查 5（REQ_xxx.cpp 质量）、检查 6（test_demo.cpp）和检查 8（migration-log.jsonl）必须全部通过（共 4 项硬性门槛）。
3. 如有不通过项，明确写出修复指引。
