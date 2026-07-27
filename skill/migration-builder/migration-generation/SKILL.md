---
name: migration-implementer
description: 将已验证并人工确认的 AFSIM FU 迁移设计实现为软件设计说明、可构建的 C++ 代码、自动化测试、CMake 配置和使用说明，并通过编译、测试、数值/行为 oracle 与追溯检查证明结果。用于确认版迁移计划的工程实现；不用于需求澄清、未批准设计或许可证不明确时复制 AFSIM 源码。
---

# AFSIM 迁移实现

严格执行“确认设计 → SDD → 实现 → 构建 → 测试 → 证据回写”。编译成功不等于逻辑正确。

## 输入门禁

- `docs/migration/<req-id>/<req-id>-FU-design-confirmed.md`
- `workspace/migration/<req-id>/<req-id>-migration-function.jsonl`
- migration-planner 验证报告
- 目标系统源码、接口、编码规范、构建系统和测试框架
- 经批准的 AFSIM 证据或非 AFSIM 设计依据

逐行确认 `approval.status == "approved"`，并核对文档与 JSONL 的版本、函数签名和单位。存在未批准函数、unknown 证据或阻塞问题时停止。

## 核心规则

- 许可证允许前不复制 AFSIM 实现表达；默认采用 clean-room 重实现。
- 每个函数实现必须追溯到 FU、REQ、设计版本和来源证据。
- 所有内部计算与接口单位遵循确认版设计；转换集中且可测试。
- 不声称运行、通过或等价，除非本轮实际执行并保存结果。
- 不用空测试、固定 PASS 文本或无断言 demo 代替验证。

## 工作流

### 1. 确认接入点

解析目标系统的目录、命名空间、类型、错误处理、线程模型、构建与测试约定。默认原型目录为 `tests/migration_src/<req-id>/`；用户指定真实接入目录时使用目标项目约定。

### 2. 生成 SDD

读取 `skill/migration-builder/template_list/template_sdd.md`，生成
`docs/migration/<req-id>/<req-id>-SDD.md`。至少包含：

- 范围、FU/REQ 追溯、组件和接口。
- 数据流、状态生命周期、线程/所有权。
- 数学公式、单位、坐标系和边界。
- AFSIM 差异、clean-room 边界或 novel 设计依据。
- 错误处理、测试 oracle、限制与假设。

### 3. 实现代码

按目标项目风格生成头文件和实现文件。每个公共 API 写清输入、输出、单位、约束、错误和线程安全；每个核心函数标注 FU/REQ 与设计来源。

不要保留模板占位符、虚构头文件、未实现分支或无解释常量。若目标依赖不可用，提供最小中性适配层并明确其临时性质。

### 4. 生成自动化测试

至少覆盖：

- 正常路径与代表性数值。
- 边界、零值、极限值和无效输入。
- 状态初始化、连续多步更新和重置。
- 单位/坐标系转换。
- 解析解、黄金数据、独立实现、守恒量、单调性或合理范围中的至少一种行为 oracle。

测试必须包含断言和失败退出码。Demo 可用于展示，但不能替代自动化测试。

### 5. 构建与运行

生成或接入 CMake 配置，执行：

1. 配置构建。
2. 编译所有目标。
3. 运行测试。
4. 启用项目可用的警告、格式、静态分析和 sanitizer。
5. 审查输出中的 NaN/Inf、恒定不变量、未使用结果和异常范围。

失败时先定位根因，修复后重跑相关测试与回归测试。环境缺失导致无法执行时，将状态标为 `not_run` 并列出确切命令和阻塞项。

### 6. 交叉一致性

核对 JSONL 中所有函数均在代码声明、实现和测试中出现；签名、单位、默认值、错误语义与 SDD 一致。反向核对代码中没有未设计的公共 API。

### 7. 输出

默认生成：

- `docs/migration/<req-id>/<req-id>-SDD.md`
- `tests/migration_src/<req-id>/<requirement-name>.h`
- `tests/migration_src/<req-id>/<requirement-name>.cpp`
- `tests/migration_src/<req-id>/<requirement-name>_test.cpp`
- `tests/migration_src/<req-id>/CMakeLists.txt`
- `tests/migration_src/<req-id>/README.md`
- `docs/verification/migration-implementation-<req-id>-verify-report.md`
- `docs/records/<date>-migration-implementation-<req-id>.md`

若写入真实目标项目，使用其目录和命名约定，并在记录中映射上述逻辑产物。

## 完成门禁

- SDD、设计 JSONL、代码和测试相互一致。
- 实际编译成功且所有测试通过，或明确标为未运行而非通过。
- 关键行为有独立 oracle，不只检查程序未崩溃。
- 无未处理模板占位、未解释警告或 silent fallback。
- 许可证和 clean-room 边界可审查。
- 不记录隐藏推理过程。
