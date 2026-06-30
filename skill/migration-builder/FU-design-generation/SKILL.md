---
name: migration-planner
description: AFSIM 功能迁移的计划制定者与迭代协调者。它负责将上游需求映射阶段产生的每个原子功能单元（FU）转化为详细的、可逐项确认的迁移计划，并驱动与人工的多轮交互，直至所有计划获得人工“Y”确认，形成可执行基线。
---

# 迁移计划生成与迭代确认 Skill

## 输入
- 需求侧：
   - `docs/requirements/<requirement_index>/3_<requirement_index>-requirement-gap-analysis.md` — 完整缺口报告
   - `docs/requirements/<requirement_index>/3_<requirement_index>-function-mapping-matrix.md` — 功能映射矩阵
   - `docs/requirements/<requirement_index>/3_<requirement_index>-requirement-to-afsim-trace.md` — 需求到AFSIM的追溯矩阵
   - `workspace/requirements/<requirement_index>/<requirement_index>-gap-specs.jsonl` — 结构化缺口规格
- AFSIM侧：
   - `docs/architecture/afsim-architecture.md` — AFSIM 架构报告
   - `docs/algorithms/CompendiumofAlgorithms.md` — 算法卡片概览
   - `workspace/source-index/function-index.jsonl` — AFSIM 源码功能索引
- 目标系统侧：
   - `docs/migration/<requirement_index>/target-interfaces.md` — 目标系统公共接口定义（如有）。

## 工作流程（步骤）
1. **加载输入与上下文**
   - 读取全部缺口规格，提取所有待迁移 FU。
   - 加载 AFSIM 索引与架构报告，建立快速查找能力。

2. **为每个 FU 生成初步迁移计划**
   - 对每个 FU：
      - 读取 FU 的缺口规格和缺口报告，获取 `fu_id`、`name` 和 FU 功能描述。
      - 按照是否可复用？是否可单独测试？是否降低了主流程的可读性？ 把一个 FU 拆成多个函数。
      - 检查 AFSIM 是否有参考实现：
         - 若 `migration_approach == “novel”`（AFSIM 无参考）：
            - 查阅设计依据来源：领域文献、算法教材、数学公式或网络资源。
            - 耦合分析：无 AFSIM 专有依赖，仅评估第三方库和标准 C++ 依赖。
            - 迁移策略：`novel`（全新设计——AFSIM 无参考，从领域文献/算法教材中寻找设计依据）。
            - 接口方案：无 AFSIM 源接口，改为”定义目标接口”——从需求描述和核心算法公式推导接口签名。
            - 关键设计决策：记录核心算法选择、数据结构设计、边界条件处理等关键决策点。
         - 若 AFSIM 有参考实现：
            - 通过`workspace\source-index`中的`function-index.jsonl`等索引文件快速定位 AFSIM 源函数。
            - 运行耦合分析：列出所有外部依赖，标注为 `标准C++`、`第三方库`、`AFSIM专有` 三类。
            - 选择迁移策略：`直接适配`（仅需替换少量接口/依赖）、`局部重写`（需要修改部分逻辑但保留核心算法）、`Clean-room重实现`（仅参考功能描述重写，不直接使用代码）。
            - 生成接口适配方案：源接口 → 目标接口映射，列出需要转换的类型、新增的参数。
            - 确定关键修改点：需移除/替换/保留的代码块、宏、全局变量。
     - 拟定测试策略与风险评估。
     - 附加人工确认选项：提供”修改要求”填写区。

3. **汇编计划文档**
   - 将所有 FU 的计划按照合并写入 `docs/migration/<requirement_index>/<requirement_index>-FU-design.md`。
   - 文档头部包含需求索引编号、生成时间、状态（草稿/待确认）。

4. **人工确认迭代**
   - 提示人工审阅计划文档，对每个函数内容进行确认后进行勾选。
   - 读取人工反馈，包括`接口详细定义`和`修改要求`。
   - 重新生成修改后的 FU 章节，并保留历史修改记录（在文档底部添加修订表）。
   - 循环直至所有 函数设计确认 均被勾选。
   - 将文档标记为“已确认可执行计划”，添加确认时间和人工签字（电子记录）。

5. **输出最终计划并记录日志**
   - 保存确认版 `docs/migration/<requirement_index>/<requirement_index>-FU-design-confirmed.md`。
   - 更新迁移日志 `workspace/migration/<requirement_index>/<requirement_index>-migration-log.jsonl`，记录该需求计划的确认时间、版本。

6.**操作留痕**
   - 每次修改 FU 计划时，记录修改内容、修改原因、修改时间，形成完整的迭代历史。
   - 把每一步的决策依据和执行计划生成文档进行记录归档，放在目录docs/records里面，以便人工追溯。

## 输出文件
- `docs/migration/<requirement_index>/<requirement_index>-FU-design.md`：功能迁移计划文档，包含每个 FU 的详细迁移方案和人工确认状态。
  - 确认后为最终执行计划。
  - 按模板 `skill\afsim-migration-builder\template_list\template_FU-migration.md` 格式输出。
  - 所有需要用户确认的条目，均标亮（红色）显示，并提供修改要求填写区。
- `docs/records/`：操作留痕文件，记录每次修改的内容、原因、时间等，形成完整的迭代历史。
- `workspace/migration/<requirement_index>/<requirement_index>-migration-log.jsonl`：迁移日志，记录每个需求的计划生成和确认历史。


