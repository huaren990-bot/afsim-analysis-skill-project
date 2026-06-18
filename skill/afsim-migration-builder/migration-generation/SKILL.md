---
name: migration-implementer
description: >
  负责将已确认的迁移计划转化为符合工程规范的软件设计说明（SDD）和可编译运行的代码实现。
  严格遵循模板生成 SDD，并按需求粒度为每个 REQ 生成一个头文件、一个实现文件、
  一个测试 demo 和一个快速入门 README。
---

# 迁移实现 Skill

本 Skill 负责把 AFSIM 中已经定位和理解的能力转化为目标系统可用的软件设计说明与实现代码。
在生成任何代码之前，须确认迁移计划已获人工批准，并严格遵循“先设计、后实现、附带测试”的顺序。

## 一、输入

| 输入项 | 路径/来源 | 说明 |
|--------|-----------|------|
| 确认后的迁移计划 | `docs/migration/<req_index>-FU-design.md` | 必须为已确认版本（所有 FU 均为 Y） |
| 软件设计说明模板 | `docs/templates/template_sdd.md` | 定义 SDD 的章节结构 |
| 需求缺口报告 | `docs/requirements/requirement-gap-analysis.md` | 提供需求的完整上下文 |
| 算法卡片 | `docs/algorithms/` | 对应 FU 的算法公式、伪代码、变量映射 |
| AFSIM 候选源码 | `workspace/source-index/` + `source_root/` | 通过索引定位，获取原始代码片段 |
| 目标系统接口定义 | 目标系统公共头文件 | 类型定义（状态结构体、数学库等） |

## 二、核心原则

1. **计划先行**：所有 FU 的迁移计划必须已获人工确认（Y），才可进入实现阶段。
2. **设计先于编码**：先产出 SDD，再生成代码，确保接口和逻辑经过文档化推敲。
3. **追溯性**：每个函数实现必须用注释标注对应的 FU ID 和实现来源（AFSIM 源位置 或 对于 novel FU，设计依据文献引用）。
4. **合规优先**：许可证不明确的代码，仅生成 Clean-room 风格的算法规格和重写建议，不直接复制源码。
5. **可测试**：所有迁移代码必须附带可编译运行的 `test_demo.cpp`。

## 三、执行步骤

### 步骤 1：加载所有输入
- 读取迁移计划，解析出所有已确认的 FU 列表、适配方案、接口映射。
- 读取 SDD 模板，明确章节结构。
- 通过索引获取对应的 AFSIM 源码片段。
- 加载目标系统公共类型定义，确保类型映射准确。

### 步骤 2：明确目标系统接入点
- 确认迁移代码存放目录：`tests/migration_src/<req_index>/`
- 确认目标系统的目录结构、类命名规范、接口风格、构建方式。
- 列出需要引用的目标系统头文件和第三方库。

### 步骤 3：评估耦合度并选择迁移方式

| 情况 | 推荐方式 |
|------|----------|
| 算法独立、依赖少、许可证允许 | 直接适配或小范围重写 |
| 算法清晰但框架耦合强 | 提取公式和伪代码后重写 |
| 许可证不明确 | Clean-room 规格说明和重新实现 |
| 目标系统接口不明确 | 先生成接口假设和问题清单，提交人工确认 |
| AFSIM 无参考实现（novel） | 从领域文献/算法教材中提取公式和伪代码，全新设计实现 |

### 步骤 4：生成软件设计说明（SDD）
- 以需求（REQ）为范围撰写一份软件设计说明`<req_index>-SDD.md`，按模板 `skill\afsim-migration-builder\template_list\template_sdd.md` 格式输出。
- 内容覆盖：概述、引用文档、设计细节（含每个 FU 的算法描述、数据流）、接口定义（输入、输出、单位、生命周期、错误处理）、依赖关系、测试策略、限制与假设。

### 步骤 5：生成代码文件
- **头文件**：生成`REQ_xxx.h`，要求包括所有 FU 的接口声明；每个函数前用注释标注 FU ID 和实现来源（AFSIM 源位置 或 novel FU 的设计依据文献引用）；包含完整的 Doxygen 风格注释。按模板 `skill/afsim-migration-builder/template_list/template_REQ_xxx.h` 格式输出。
- **实现文件**：生成`REQ_xxx.cpp`，要求包括所有 FU 的实现代码；按 FU 分段，每段以 `/* === FU-xxx: 描述 === */` 开头；对于 AFSIM 有参考的 FU，保留原始版权注释（若许可允许）；对于 novel FU，标注设计依据；详细注释所有修改点。按模板 `skill/afsim-migration-builder/template_list/template_REQ_xxx.cpp` 格式输出。
- **测试 Demo**：生成 `test_demo.cpp`，可直接编译运行的演示程序，包含 `main()`；注释中说明编译命令、运行方法和预期输出；覆盖主要使用场景。按模板 `skill/afsim-migration-builder/template_list/template_test_demo.cpp` 格式输出。
  - main() 为最简单示例场景，展示核心功能的输入输出，统一调用测试用例函数。
  - 设计至少 3 个测试用例，覆盖正常情况、边界情况和异常情况，每个以 `/* --- TC-xxx: 描述 --- */` 开头，每个测试用例对应一个函数，都放在 `test_demo.cpp` 中。

### 步骤 6：生成 README
- 在代码目录下生成 `README.md`，仅包含：编译命令、依赖列表、运行 demo 的步骤和预期输出。按模板 `skill/afsim-migration-builder/template_list/template_README.md` 格式输出。
- 不涉及设计细节，与 SDD 分工明确。

### 步骤 7：输出与记录
- 写入所有文件。
- 更新迁移日志 `workspace/migration/migration-log.jsonl`，记录生成的文件路径和版本。

## 四、生成代码前检查清单

在生成代码之前，必须确认以下条件全部满足：

- [ ] 有明确的 REQ ID 和 FU ID。
- [ ] 有实现依据：AFSIM 源码证据（文件路径+行号）**或** 对于 novel FU，有设计依据（文献引用/算法教材）。
- [ ] 目标系统接入点已明确（目录、命名空间、类型）。
- [ ] 输入输出、单位、生命周期、错误处理已定义。
- [ ] 测试计划已拟定。
- [ ] 许可证和版权声明已处理（保留原始声明或确认 Clean-room）。

## 五、输出文件

| 产物 | 路径 | 说明 |
|------|------|------|
| 软件设计说明 | `docs/migration/<req_index>-SDD.md` | 依据 `template_sdd.md` 模板撰写 |
| 头文件 | `tests/migration_src/<req_index>/REQ_xxx.h` | 接口声明，含 FU 追溯注释 |
| 实现文件 | `tests/migration_src/<req_index>/REQ_xxx.cpp` | 核心实现，按 FU 分段注释 |
| 测试 Demo | `tests/migration_src/<req_index>/test_demo.cpp` | 完整可运行示例 |
| 使用说明 | `tests/migration_src/<req_index>/README.md` | 编译、依赖、运行说明 |
