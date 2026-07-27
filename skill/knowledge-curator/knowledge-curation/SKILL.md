---
name: afsim-knowledge-curator
description: 增量整理和审计 AFSIM 分析知识库，把源码结构、业务能力、算法卡片、需求证据、FU、迁移设计、实现与测试连接成可机器查询的追溯图和人读知识地图，并检测重复、断链、冲突、过期证据和覆盖缺口。用于阶段收尾、知识库更新、全量分析进度盘点或追溯审计；不替代源码分析、算法提取或需求判断。
---

# AFSIM 知识沉淀与追溯

优先增量更新既有资产，不复制整篇报告形成第二事实源。机器账本保存稳定关系，人读文档提供导航和摘要。

## 开始前读取

读取 [references/traceability-contract.md](references/traceability-contract.md)，确认节点、边、状态和稳定 ID。

## 输入

按存在情况读取：

- `workspace/source-index/` 与 `docs/architecture/`
- `workspace/algorithm-extraction/`、`docs/algorithms/`、`docs/extracted-algorithms/`
- `workspace/requirements/` 与 `docs/requirements/`
- `workspace/migration/`、`docs/migration/` 和迁移源码/测试
- `docs/verification/`、`docs/records/` 和用户审查意见

## 工作流

### 1. 盘点资产

枚举当前范围内的机器产物和人读产物，记录类型、稳定 ID、路径、版本/日期、验证状态和来源。使用路径与稳定 ID 去重，不用标题相似度静默合并。

### 2. 校验后再入库

只把已通过相应验证门禁的结论标为 `verified`。草稿、推断、unknown、not_run 和失败产物可以入库，但必须保留原状态，不能在汇总时提升可信度。

### 3. 建立追溯图

至少连接：

```text
source symbol/function
  -> AFSIM capability/flow
  -> algorithm
  -> requirement
  -> FU
  -> migration function
  -> implementation
  -> test evidence
```

每条边必须有关系类型、来源路径和状态。缺失的中间节点生成 gap，不用虚构节点补齐。

### 4. 检测问题

主动检查：

- 相同 ID 指向不同内容。
- 相同产物被不同 ID 重复登记。
- Markdown、JSONL、源码和测试之间的断链。
- 路径或行号已不存在。
- 上游文件更新时间/版本晚于下游，但下游未复验。
- `verified` 结论只引用 index-derived 证据。
- Compendium 数量、候选覆盖账本和实际卡片不一致。
- 需求/FU 已确认但迁移或测试仍为旧版本。

冲突不得自动选“最新文件”解决；列出候选、证据和建议处理方式。

### 5. 增量更新机器账本

生成或更新：

- `workspace/knowledge/artifact-index.jsonl`
- `workspace/knowledge/traceability.jsonl`
- `workspace/knowledge/gaps.jsonl`
- `workspace/knowledge/coverage-summary.json`

按稳定键 upsert，保持确定性排序。未在本轮范围内看到的历史条目不删除；若明确失效，标为 `stale` 或 `superseded` 并指向替代项。

### 6. 更新人读导航

生成或更新：

- `docs/architecture/knowledge-map.md`
- `docs/requirements/requirement-to-afsim-trace.md`（只做跨需求聚合导航，链接到各需求的详细矩阵）
- `docs/migration/migration-summary.md`

知识地图至少展示分析范围、模块/能力入口、算法覆盖、需求与迁移进度、验证状态、关键 gap 和下一批建议。避免复制卡片或报告全文。

### 7. 记录本轮

写入 `docs/records/<date>-knowledge-curation-<scope>.md`，记录输入范围、新增/更新/冲突/过期/断链数量、输出、未决问题和建议下一步。记录可审查依据，不记录隐藏推理过程。

## 完成门禁

- 所有机器账本逐行可解析，稳定键唯一。
- 人读链接均存在，机器路径可解析。
- verified 节点和边有验证报告或 source-cited 证据。
- unknown、stale、superseded、failed、not_run 未被汇总成 completed。
- 覆盖统计能从账本重算。
- 重跑相同输入不产生重复节点、边或记录。
