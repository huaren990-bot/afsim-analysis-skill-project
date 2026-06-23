---
name: migration-planner
description: AFSIM 功能迁移的计划制定者与迭代协调者。它负责将上游需求映射阶段产生的每个原子功能单元（FU）转化为详细的、可逐项确认的迁移计划，并驱动与人工的多轮交互，直至所有计划获得人工“Y”确认，形成可执行基线。
---

# 迁移计划生成与迭代确认 Skill

## 输入
- `workspace/requirements/gap-specs.jsonl`：原子功能规格，每个 FU 包含需求 ID、描述、AFSIM 源位置、目标状态等。
- `docs/requirements/function-mapping-matrix.md`：需求映射矩阵（辅助理解全局）。
- AFSIM 源码索引（`workspace/source-index/function-index.jsonl` 等）及架构报告。
- 目标系统公共接口定义（如已有的头文件路径）。

## 工作流程（步骤）
1. **加载输入与上下文**
   - 读取全部缺口规格，提取所有待迁移 FU。
   - 加载 AFSIM 索引与架构报告，建立快速查找能力。

2. **为每个 FU 生成初步迁移计划**
   - 对每个 FU：
     - **若 `migration_approach == “novel”`（AFSIM 无参考）**：
       - 查阅设计依据来源：领域文献、算法教材、数学公式或网络资源。
       - 耦合分析：无 AFSIM 专有依赖，仅评估第三方库和标准 C++ 依赖。
       - 迁移策略：`novel`（全新设计——AFSIM 无参考，从领域文献/算法教材中寻找设计依据）。
       - 接口方案：无 AFSIM 源接口，改为”定义目标接口”——从需求描述和核心算法公式推导接口签名。
       - 关键设计决策：记录核心算法选择、数据结构设计、边界条件处理等关键决策点。
     - **若 AFSIM 有参考实现**：
       - 获取 AFSIM 源函数完整代码（通过工具或读取源码）。
       - 运行耦合分析：列出所有外部依赖，标注为 `标准C++`、`第三方库`、`AFSIM专有` 三类。
       - 选择迁移策略：`直接适配`（仅需替换少量接口/依赖）、`局部重写`（需要修改部分逻辑但保留核心算法）、`Clean-room重实现`（仅参考功能描述重写，不直接使用代码）。
       - 生成接口适配方案：源接口 → 目标接口映射，列出需要转换的类型、新增的参数。
       - 确定关键修改点：需移除/替换/保留的代码块、宏、全局变量。
     - 拟定测试策略与风险评估。
     - 附加人工确认选项：`[ ] Y（通过）` `[ ] N（需修改）`，并提供”修改要求”填写区。

3. **汇编计划文档**
   - 将所有 FU 的计划按照合并写入 `docs/migration/preliminary-migration-plan/<requirement_index>-FU-design.md`。
   - 文档头部包含需求索引编号、生成时间、状态（草稿/待确认）。
   - 每个 FU 独立章节，末尾附 Y/N 选项。

4. **人工确认迭代**
   - 提示人工审阅计划文档，对每个 FU 勾选 Y 或 N，若选 N 需写明具体要求。
   - 读取人工反馈，仅修改标记为 N 的 FU 计划（保持 Y 的部分不变）。
   - 重新生成修改后的 FU 章节，并保留历史修改记录（在文档底部添加修订表）。
   - 循环直至所有 FU 均为 Y。
   - 将文档标记为“已确认可执行计划”，添加确认时间和人工签字（电子记录）。

5. **输出最终计划并记录日志**
   - 保存确认版 `docs/migration/preliminary-migration-plan/<req_index>-FU-design-confirmed.md`。
   - 更新迁移日志 `workspace/migration/migration-log.jsonl`，记录该需求计划的确认时间、版本。

6.**操作留痕**
   - 每次修改 FU 计划时，记录修改内容、修改原因、修改时间，形成完整的迭代历史。
   - 把每一步的决策依据和执行计划生成文档进行记录归档，放在目录docs/records里面，以便人工追溯。

## 输出文件
- `docs/migration/preliminary-migration-plan/<requirement_index>-FU-design.md`：功能迁移计划文档，包含每个 FU 的详细迁移方案和人工确认状态。
  - 确认后为最终执行计划。
  - 按模板 `skill\afsim-migration-builder\template_list\template_FU-migration.md` 格式输出。
  - 所有需要用户确认的条目，均标亮（红色）显示，并提供修改要求填写区。
- `docs/records/`：操作留痕文件，记录每次修改的内容、原因、时间等，形成完整的迭代历史。
- `workspace/migration/migration-log.jsonl`：迁移日志，记录每个需求的计划生成和确认历史。


