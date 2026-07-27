# gap-specs.jsonl 契约

输出路径：
`workspace/requirements/<req-id>/<req-id>-gap-specs.jsonl`

每行一个 FU，UTF-8、无 BOM、合法 JSON 对象。字段不得依赖 Markdown 才能解释。

## 必需结构

```json
{
  "schema_version": "2.0",
  "fu_id": "FU-001",
  "req_ids": ["REQ-XXX-FUNC-01"],
  "name": "功能单元名称",
  "description": "可独立实现和测试的功能",
  "coverage_status": "missing_with_afsim_reference",
  "acceptance_criteria": ["Given ... When ... Then ..."],
  "expected_signature": {
    "inputs": [
      {
        "name": "input",
        "type": "double",
        "unit": "m/s",
        "frame": "NED",
        "constraints": ">= 0",
        "description": "输入说明"
      }
    ],
    "outputs": [
      {
        "name": "output",
        "type": "double",
        "unit": "m",
        "frame": "NED",
        "constraints": "finite",
        "description": "输出说明"
      }
    ],
    "state": [],
    "side_effects": [],
    "errors": []
  },
  "dataflow": {
    "input_sources": [{"name": "input", "source": "external:input"}],
    "output_consumers": [{"name": "output", "consumer": "final:output"}]
  },
  "afs_reference": {
    "coverage": "partial",
    "candidate_id": "stable-id",
    "qualified_name": "Namespace::Class::Method#digest",
    "class_name": "Namespace::Class",
    "path": "relative/path.cpp",
    "line_start": 10,
    "line_end": 40,
    "dependency_summary": "依赖摘要",
    "search_scope": []
  },
  "target_evidence": {
    "assumption": "",
    "references": []
  },
  "migration_approach": "cleanroom",
  "coupling_assessment": "medium",
  "priority": "high",
  "risks": ["风险"],
  "notes": [],
  "generated_at": "YYYY-MM-DD"
}
```

## 枚举

- `coverage_status`：`partial`、`missing_with_afsim_reference`、`missing_without_afsim_reference`
- `afs_reference.coverage`：`full`、`partial`、`none`、`unknown`
- `migration_approach`：`direct_adaptation`、`partial_rewrite`、`cleanroom`、`novel`
- `coupling_assessment`：`low`、`medium`、`high`、`unknown`
- `priority`：`high`、`medium`、`low`

## 无 AFSIM 参考

当 `afs_reference.coverage == "none"`：

- `candidate_id`、`qualified_name`、`class_name`、`path` 为空字符串。
- `line_start`、`line_end` 为 `null`。
- `search_scope` 非空，记录实际检查的索引、模块、关键词、文档和 demo 范围。
- `migration_approach` 为 `novel`。

不得用模块目录或算法卡片标题冒充 verified 源函数位置。
