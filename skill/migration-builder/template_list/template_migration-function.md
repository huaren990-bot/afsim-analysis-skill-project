# migration-function.jsonl 契约

输出路径：
`workspace/migration/<req-id>/<req-id>-migration-function.jsonl`

每行一个拟实现函数，UTF-8、无 BOM、合法 JSON 对象。

```json
{
  "schema_version": "2.0",
  "function_id": "FUNC-001",
  "fu_id": "FU-001",
  "req_ids": ["REQ-XXX-FUNC-01"],
  "function_name": "computeValue",
  "display_name": "中文名称",
  "description": "单一职责说明",
  "signature": "Result computeValue(const Input& input)",
  "source_location": {
    "exists_in_afsim": true,
    "candidate_id": "stable-id",
    "qualified_name": "Namespace::Class::Method#digest",
    "class_name": "Namespace::Class",
    "method_name": "Method",
    "file": "relative/path.cpp",
    "line_start": 10,
    "line_end": 40
  },
  "design_basis": {
    "kind": "afsim_behavior_spec",
    "references": ["docs/algorithms/example-card.md"],
    "search_scope": []
  },
  "interface": {
    "parameters": [
      {
        "name": "input",
        "type": "const Input&",
        "direction": "in",
        "unit": "SI",
        "frame": "none",
        "constraints": "valid",
        "description": "输入说明"
      }
    ],
    "return": {
      "type": "Result",
      "unit": "SI",
      "frame": "none",
      "constraints": "finite",
      "description": "返回说明"
    },
    "errors": ["invalid_argument"]
  },
  "state": {
    "reads": [],
    "writes": [],
    "initialization": "none",
    "update_timing": "per_call",
    "reset": "none",
    "thread_safety": "reentrant"
  },
  "dataflow": {
    "input_sources": [{"name": "input", "source": "external:input"}],
    "output_consumers": [{"name": "return", "consumer": "final:output"}]
  },
  "dependencies": {
    "standard_library": [],
    "third_party": [],
    "target_system": [],
    "afsim_to_replace": []
  },
  "migration_approach": "cleanroom",
  "acceptance_criteria": ["Given ... When ... Then ..."],
  "tests": [
    {
      "kind": "normal",
      "input": "fixture",
      "oracle": "expected value",
      "tolerance": "1e-9"
    }
  ],
  "risks": [],
  "approval": {
    "status": "draft",
    "version": "0.1",
    "approved_by": "",
    "approved_at": null
  },
  "notes": []
}
```

## 来源规则

`exists_in_afsim == true` 时，`candidate_id`、`qualified_name`、`file` 和行号必须完整并能在当前源码复核。

`exists_in_afsim == false` 时：

- AFSIM 定位字符串为空，行号为 `null`。
- `design_basis.kind` 为 `domain_reference`、`requirement_derived` 或其他真实来源。
- novel 项的 `search_scope` 非空。

## 枚举

- `migration_approach`：`direct_adaptation`、`partial_rewrite`、`cleanroom`、`novel`
- `approval.status`：`draft`、`changes_requested`、`approved`
- `tests.kind`：`normal`、`boundary`、`degenerate`、`invalid`、`sequence`、`performance`

文档确认后同步更新签名、接口、测试和 approval；不得只改 Markdown。
