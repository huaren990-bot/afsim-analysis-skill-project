---
name: afsim-migration-builder
description: 当用户需要把 AFSIM 中的算法、模型或功能迁移到自有项目，生成接口适配、重写方案、代码原型、测试计划、风险评估或迁移记录时，使用本 skill。
---

# AFSIM 迁移生成 Skill

本 skill 负责把 AFSIM 中已经定位和理解的能力转化为自有项目可用的迁移方案或实现草稿。

## 输入

- 需求缺口报告。
- 算法卡片。
- AFSIM 候选源码位置。
- 自有项目接口、代码风格和构建方式。

## 执行步骤

1. 明确目标项目接入点：目录、类、接口、数据结构、测试位置。
2. 评估 AFSIM 候选实现的耦合度：框架服务、全局状态、配置系统、事件系统、外部库。
3. 选择迁移方式：直接适配、局部重写、clean-room 重实现、只迁移公式和接口。
4. 生成接口适配说明：输入、输出、单位、生命周期、错误处理。
5. 生成迁移记录：选择理由、依赖替换、许可证说明、风险和验证计划。
6. 在用户明确需要代码时，再生成小范围、可测试的实现草稿。

## 输出

- `docs/migration/<feature>-migration-plan.md`
- `docs/migration/<feature>-migration-record.md`
- `workspace/own-kernel-adapters/<feature>/interface-adapter.md`
- `workspace/own-kernel-adapters/<feature>/prototype.*`
- `tests/<feature>/`

## 迁移方式选择

| 情况 | 推荐方式 |
| --- | --- |
| 算法独立、依赖少、许可证允许 | 直接适配或小范围重写 |
| 算法清晰但框架耦合强 | 提取公式和伪代码后重写 |
| 许可证不明确 | clean-room 规格说明和重新实现 |
| 自有项目接口不明确 | 先生成接口假设和问题清单 |

## 生成代码前检查

- 是否有明确需求 ID。
- 是否有 AFSIM 源码证据。
- 是否有目标项目接入点。
- 是否有输入输出和单位说明。
- 是否有测试计划。
- 是否处理许可证和版权声明。



---

## 3. 迁移程序生成 Skill

**文件路径**：`skill/afsim-migration-builder/skills/migration-code-generation.md`

```markdown
# migration-code-generation — 迁移程序生成 Skill

## 角色
你是一个 **迁移代码实现专家**，在软件设计说明（SDD）获得人工确认后，负责将设计转化为符合目标系统规范、包含完整中文注释的 C++ 迁移代码，并编写相应的测试调用说明。

## 前置条件
- `docs/migration/software-design-description.md` 已通过人工确认（状态为 `confirmed`）。
- AFSIM 源码及目标系统头文件可访问。

## 输入
- 已确认的 SDD 文档
- AFSIM 源文件（通过 `get_afs_source` 获取）
- 目标系统编码规范及已有接口定义（若有）

## 工作步骤
1. **加载 SDD**：读取确认后的软件设计说明，提取待实现的 FU 列表。
2. **逐 FU 生成迁移代码**：
   - 根据 SDD 中的适配方案和接口定义，生成目标系统的 C++ 源文件和头文件。
   - 从 AFSIM 源码中拷贝核心算法部分，按照 SDD 中的“需移除/保留/修改”清单进行处理：
     - 移除 AFSIM 特定宏、日志、全局配置引用。
     - 替换数据类型为目标系统类型（依据映射表）。
     - 添加必要的适配层函数（如状态结构体转换）。
   - 所有代码必须包含**中文注释**，说明每个函数/关键步骤的作用、参数含义、修改来源。
   - 保留原始版权声明（若有许可证要求），并添加“迁移自 AFSIM ...”的说明。
3. **生成测试调用说明**：
   - 按照 `template_test_and_verification.md` 为每个 FU 生成测试验证文档，包含：
     - 编译依赖、头文件包含
     - 测试用例构造方法（输入数据准备）
     - 调用示例代码
     - 预期输出和验证方式（如与 AFSIM 原输出对比、数值容差等）
4. **保存产物**：
   - 建立迁移代码保存目录 `tests/migration_src/<requirement_index>/`。
   - 迁移代码保存至 `src/migration/{module}/{function_name}.h` 和 `.cpp`。
   - 测试说明文档保存至 `docs/migration/test-plan-FU-XXX.md` 或汇总至 `docs/migration/test-and-verification.md`。
   - 更新 `workspace/migration/<requirement_index>-migration-log.jsonl`，记录代码生成状态为 “implemented”。

5. **过程留痕**：把每一步的决策依据和执行计划生成文档进行记录归档，放在目录 `docs/records` 里面，以便人工追溯。

## 输出
- `src/migration/` 下的 C++ 头文件和源文件（带中文注释）
- `docs/migration/test-and-verification.md` 或各 FU 测试说明
- 更新的迁移日志

## 代码规范
- 文件头部必须包含注释块，说明来源、修改点、日期。
- 每个公共函数前必须有中文注释，说明功能、参数、返回值、注意事项。
- 关键算法步骤使用中文行注释。
- 遵循目标系统的命名约定和代码风格。

## 工具
- `read_file(path)` — 读取 SDD、源码索引
- `get_afs_source(function_id)` — 获取 AFSIM 源函数代码
- `write_file(path, content)` — 写入迁移代码和文档
- `run_syntax_check(code)` — 对生成的代码进行语法检查（需编译环境支持）
- `append_migration_log(entry)` — 追加日志