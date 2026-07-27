---
name: algorithm-extraction
description: 从 cpp-project-analyzer 已生成的 AFSIM C++ 索引和真实源码中，系统发现、聚类、还原并验证数学模型、数值算法、状态更新与控制算法，产出可追溯的算法卡片、接口规格、算法汇总和全量覆盖账本。用于“继续分析 AFSIM”“提取某模块/某功能算法”“把源码还原为公式与伪代码”“检查 AFSIM 算法是否提取完整”等任务；不用于仅做目录/符号索引、需求缺口分析或直接迁移代码。
---

# AFSIM 算法发现与提取

把 `cpp-project-analyzer` 的结构化结果当作定位入口，把真实 AFSIM 源码当作行为证据。禁止仅凭索引摘要、函数名或旧算法卡片断言算法行为。

## 开始前读取

1. 读取 [references/upstream-contract.md](references/upstream-contract.md)，确认索引字段、源码路径解析和证据等级。
2. 读取 [references/output-contract.md](references/output-contract.md)，确认候选、卡片、接口规格和覆盖账本的输出契约。
3. 生成卡片、接口规格或汇总前，分别读取：
   - `skill/algorithm-extractor/template_list/template_algorithm-card.md`
   - `skill/algorithm-extractor/template_list/template_interface-spec.md`
   - `skill/algorithm-extractor/template_list/template_CompendiumofAlgorithms.md`

## 输入门禁

确认以下输入存在且可解析：

- `workspace/source-index/function-index.jsonl`
- `workspace/source-index/function-body-summary.jsonl`
- `workspace/source-index/file-index.jsonl`
- `workspace/source-index/symbol-index.jsonl`
- `workspace/source-index/dependency-index.jsonl`
- AFSIM 源码根目录，默认在 `source_root/` 下解析，不假定固定版本目录名

抽样至少 3 条 Method-level 记录，验证 `path`、`line_start`、`line_end` 能定位到真实源码。若路径无法解析、索引 JSONL 损坏或关键行号明显越界，停止提取并输出上游阻塞项；不要猜测源码位置。

## 标准工作流

### 1. 建立可续跑候选清单

运行：

```bash
python3 skill/algorithm-extractor/algorithm-extraction/scripts/build_algorithm_candidates.py \
  --function-index workspace/source-index/function-index.jsonl \
  --body-summary workspace/source-index/function-body-summary.jsonl \
  --source-root source_root \
  --output workspace/algorithm-extraction/algorithm-candidates.jsonl
```

脚本默认纳入 `math` 与 `state_update`，并按计算密度、数学操作和名称信号排序。只有在任务明确包含业务控制流程时才加 `--include-control-flow`。

若真实源码证明某个被上游误标为 `none` 或 `control_flow` 的函数是算法，可重复使用
`--include-candidate-id <id>` 精确纳入；不得为纳入少量误分类函数而无差别扩大整个
`control_flow` 分母。经人工闭环的显式候选会在以后默认重跑时保留。

保留候选状态，不覆盖人工或历史处理结果：

- `pending`：尚未审查
- `selected`：已确认属于可独立描述的算法
- `extracted`：卡片与接口规格均已生成并验证
- `rejected`：不是算法，必须填写 `decision_reason`
- `deferred`：证据不足或超出本轮范围，必须填写 `decision_reason`

### 2. 确定范围并分批

按 `module`、业务域和调用关系分批，每批建议 20–50 个候选。为本轮生成
`workspace/algorithm-extraction/batches/<batch-id>.jsonl`，记录候选 ID、范围、状态和失败原因。

不得以“处理了若干代表函数”声称模块完成。完成度以覆盖账本为准。

### 3. 从候选函数聚类为算法

逐个读取候选的真实源码，并结合调用者、被调函数、状态读写和相邻实现判断算法边界：

- 一个算法可以跨多个函数，但必须共享同一数学目标、状态和输入输出契约。
- 同一函数包含可独立教授、独立测试的不同数学机制时，拆为多张卡片。
- 包装器、注册器、日志、序列化和纯配置解析通常标记为 `rejected`。
- 数值积分、滤波、制导、控制律、坐标变换、查表插值、物理模型和状态估计通常标记为 `selected`。

为每个算法分配稳定 ID `ALG-<DOMAIN>-<SLUG>`。重跑时复用已有 ID，不按批次或日期重新编号。

### 4. 建立证据包

每个算法至少收集：

1. 入口与核心函数的 `candidate_id`、`qualified_name`、`path:line_start-line_end`。
2. 直接调用链、读取状态、写入状态和生命周期位置。
3. 真实源码中的核心计算片段及其语义摘要。
4. 相关配置、枚举、常量、单位和坐标系约定。
5. 可用时，再用官方文档、演示场景或既有卡片交叉验证。

索引只用于定位；源码是行为结论的最低证据。官方文档与演示可以补充意图和用法，但不能替代源码证明实现细节。

### 5. 还原算法

区分并显式记录：

- 算法核心、AFSIM 框架封装、I/O/日志、缓存和注册逻辑。
- 输入、输出、参数、内部状态、初值、更新时机、副作用。
- 单位、坐标系、符号约定、有效范围、边界条件和错误处理。
- 离散时间公式与连续时间公式；不要把实现中的离散更新误写成连续模型。
- 代码直接给定的经验系数、可从上下文证明的常量、无法证明来源的常量。

仅在证据充分时给出公式名称或经典算法归类。不能确认时标记“待人工复核”，并说明缺少哪一类证据。

### 6. 生成三类产物

每个算法生成：

- `docs/algorithms/<domain>-<algorithm>-card.md`
- `docs/extracted-algorithms/<algorithm>/<domain>-<algorithm>-interface-spec.md`

同步更新：

- `docs/algorithms/CompendiumofAlgorithms.md`
- `workspace/algorithm-extraction/algorithm-coverage.jsonl`

覆盖账本每行对应一个候选，至少包含 `candidate_id`、源码定位、状态、关联 `algorithm_ids`、决策理由和验证状态。一个候选被多个算法共享时允许列出多个 ID。

完成批次审查后，把决策写入批次 JSONL，并运行：

```bash
python3 skill/algorithm-extractor/algorithm-extraction/scripts/apply_algorithm_decisions.py \
  --manifest workspace/algorithm-extraction/algorithm-candidates.jsonl \
  --decisions workspace/algorithm-extraction/batches/<batch-id>.jsonl \
  --coverage workspace/algorithm-extraction/algorithm-coverage.jsonl
```

脚本会校验候选 ID 与状态约束，原子更新候选清单并重建全量覆盖账本。

### 7. 验证并闭环

按 `SKILL_VERIFY.md` 执行验证。硬性门禁：

- 所有本批候选均为 `extracted`、`rejected` 或 `deferred`，不得遗留无解释状态。
- 每张卡片的源码位置、Method、模块和行号可在当前索引与源码中复核。
- 每个公式符号都能映射到代码变量、配置量或明确的推导中间量。
- 卡片、接口规格、Compendium 和覆盖账本中的算法 ID、名称和路径一致。
- 每个算法至少有正常、边界和退化/异常三类验证方案。

验证失败时只修复失败项并重验，不重新生成已通过的批次。

### 8. 记录执行结果

在 `docs/records/<date>-algorithm-extraction-<scope>.md` 记录输入版本、范围、候选统计、提取/拒绝/延期数量、产物、验证结果和未决问题。记录可审查的证据与决策，不记录隐藏推理过程。

## 完成定义

只有同时满足以下条件才能声称范围完成：

1. 范围边界可枚举，并记录所用索引版本或文件摘要。
2. 范围内候选均已闭环。
3. 所有 `extracted` 候选可追溯到算法卡片与接口规格。
4. 所有 `rejected`/`deferred` 候选有具体理由。
5. 质检硬性门禁全部通过。

若目标是“全量 AFSIM 算法提取”，按模块持续执行，直到全局候选账本闭环；不要把已有少量模块或既有 32 张卡片视为全量。

## 停止条件

遇到以下情况停止当前项并报告阻塞，不得补写臆测内容：

- 源码缺失、许可证限制或路径无法解析。
- 索引与源码的符号、行号或函数体不一致。
- 单位、坐标系或状态来源无法由当前证据确定。
- 候选跨越的调用链超出用户明确范围。
