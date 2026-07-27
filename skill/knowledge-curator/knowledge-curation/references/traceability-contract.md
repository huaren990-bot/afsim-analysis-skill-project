# AFSIM 知识追溯契约

## artifact-index.jsonl

每行一个资产：

```json
{
  "artifact_id": "ALG-FLIGHT-DYNAMICS-RK4",
  "artifact_type": "algorithm",
  "path": "docs/algorithms/example-card.md",
  "version": "1.0",
  "status": "verified",
  "verification": "docs/verification/example.md",
  "source_refs": ["candidate-id"],
  "updated_at": "YYYY-MM-DD"
}
```

稳定键为 `artifact_type + artifact_id`。允许多个路径时用 `related_paths`，不复制同一节点。

## traceability.jsonl

每行一条有向边：

```json
{
  "edge_id": "source:candidate-id->algorithm:ALG-ID",
  "from": {"type": "source_function", "id": "candidate-id"},
  "relation": "implements",
  "to": {"type": "algorithm", "id": "ALG-ID"},
  "evidence": ["workspace/algorithm-extraction/algorithm-coverage.jsonl"],
  "status": "verified"
}
```

稳定键为 `from.type + from.id + relation + to.type + to.id`。

推荐关系：

- `belongs_to`、`calls`、`reads`、`writes`
- `implements`、`describes`、`covers`
- `satisfies`、`partially_satisfies`、`has_gap`
- `decomposes_to`、`planned_as`、`implemented_by`
- `verified_by`、`supersedes`

## gaps.jsonl

每行一个可行动缺口：

```json
{
  "gap_id": "GAP-<stable-slug>",
  "kind": "missing_evidence",
  "subject": {"type": "algorithm", "id": "ALG-ID"},
  "description": "缺少真实源码行号",
  "severity": "blocking",
  "source": "docs/verification/example.md",
  "status": "open"
}
```

## 状态

统一使用：

- `draft`
- `verified`
- `unknown`
- `failed`
- `not_run`
- `stale`
- `superseded`

汇总完成度时只有 `verified` 计为完成。`superseded` 不计入当前分母，但必须保留历史边。

## 新鲜度

如果上游资产的版本、内容摘要或更新时间晚于依赖它的下游验证，则下游标为 `stale`，直到复验。只靠文件修改时间无法证明语义变化时，记录为待审计而非直接判错。
