#!/usr/bin/env python3
"""Merge Phase4 batch outputs into final four-level function artifacts."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def module_qualified_name(module: str) -> str:
    return "AFSIM::Module::" + module.replace("/", "::").replace("-", "_")


def class_qualified_name(module: str, owner: str) -> str:
    normalized_owner = owner.replace(" ", "")
    return module_qualified_name(module) + "::Class::" + normalized_owner


def leaf_name(qualified_name: str) -> str:
    return qualified_name.split("::")[-1] if qualified_name else "未知对象"


def top_items(counter: collections.Counter[str], limit: int = 6) -> list[str]:
    return [name for name, _count in counter.most_common(limit)]


def brief_from_counts(prefix: str, count: int, lifecycle: collections.Counter[str], algorithms: collections.Counter[str]) -> str:
    roles = "、".join(top_items(lifecycle, 4)) or "unknown"
    algos = "、".join(top_items(algorithms, 4)) or "unknown"
    return f"{prefix}，覆盖 {count} 个 Method-level 函数；主要生命周期角色：{roles}；主要算法类型：{algos}。"


def load_batch_rows(batch_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    methods: list[dict[str, Any]] = []
    bodies: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []
    for path in sorted(batch_dir.glob("phase4-batch??-function-index.jsonl")):
        methods.extend(read_jsonl(path))
    for path in sorted(batch_dir.glob("phase4-batch??-function-body-summary.jsonl")):
        bodies.extend(read_jsonl(path))
    for path in sorted(batch_dir.glob("phase4-batch??-skips.jsonl")):
        skips.extend(read_jsonl(path))
    return methods, bodies, skips


def dedupe_by_candidate(rows: list[dict[str, Any]], label: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    duplicates = 0
    for row in rows:
        candidate_id = row["candidate_id"]
        if candidate_id in seen:
            duplicates += 1
            continue
        seen.add(candidate_id)
        result.append(row)
    if duplicates:
        print(f"{label}: dropped duplicate candidate_id rows: {duplicates}")
    return result


def enrich_methods(methods: list[dict[str, Any]], candidates: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for method in methods:
        row = dict(method)
        candidate = candidates[row["candidate_id"]]
        row["module"] = candidate.get("module") or "unknown"
        row["owner"] = candidate.get("owner") or candidate.get("qualified_name", "").rsplit("::", 1)[0] or "free_functions"
        row["kind"] = candidate.get("kind") or "function"
        row["signature"] = candidate.get("signature") or row.get("brief", "")
        row["phase4_sequence"] = candidate.get("phase4_sequence")
        row["source_candidate_path"] = candidate.get("path")
        enriched.append(row)
    enriched.sort(key=lambda item: (item.get("phase4_sequence") is None, item.get("phase4_sequence") or 0, item["path"], item["line_start"]))
    return enriched


def enforce_global_unique(methods: list[dict[str, Any]], bodies: list[dict[str, Any]]) -> int:
    counts = collections.Counter(row["qualified_name"] for row in methods)
    body_by_id = {row["candidate_id"]: row for row in bodies}
    fixed = 0
    for method in methods:
        if counts[method["qualified_name"]] <= 1:
            continue
        old_name = method["qualified_name"]
        new_name = f"{old_name}@{method['candidate_id'][:8]}"
        method["qualified_name"] = new_name
        method.setdefault("notes", []).append("全局合并时发现重复 qualified_name，追加 candidate_id 短后缀保证唯一性")
        if method["candidate_id"] in body_by_id:
            body_by_id[method["candidate_id"]]["qualified_name"] = new_name
        fixed += 1
    return fixed


def build_class_rows(methods: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for method in methods:
        grouped[(method["module"], method["owner"])].append(method)

    class_rows: list[dict[str, Any]] = []
    for (module, owner), rows in sorted(grouped.items()):
        lifecycle = collections.Counter(row.get("lifecycle_role", "unknown") for row in rows)
        algorithms = collections.Counter(row.get("algorithm_hint", "unknown") for row in rows)
        qname = class_qualified_name(module, owner)
        class_rows.append(
            {
                "schema_version": "1",
                "level": "Class-level",
                "function_name": f"{leaf_name(owner)} 类功能聚合",
                "qualified_name": qname,
                "canonical_qualified_name": owner,
                "module": module,
                "owner": owner,
                "brief": brief_from_counts(f"汇总 {module} 模块中 {owner} 的函数职责", len(rows), lifecycle, algorithms),
                "sub_functions": [row["qualified_name"] for row in rows],
                "method_count": len(rows),
                "paths": sorted(set(row["path"] for row in rows))[:100],
                "lifecycle_roles": dict(lifecycle),
                "algorithm_hints": dict(algorithms),
                "evidence_level": "batch-merged",
                "notes": ["由 Phase4 Method-level 批次合并生成。"],
            }
        )
    return class_rows


def build_module_rows(class_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for class_row in class_rows:
        grouped[class_row["module"]].append(class_row)

    module_rows: list[dict[str, Any]] = []
    for module, rows in sorted(grouped.items()):
        lifecycle: collections.Counter[str] = collections.Counter()
        algorithms: collections.Counter[str] = collections.Counter()
        method_count = 0
        for row in rows:
            lifecycle.update(row.get("lifecycle_roles", {}))
            algorithms.update(row.get("algorithm_hints", {}))
            method_count += row.get("method_count", 0)
        module_rows.append(
            {
                "schema_version": "1",
                "level": "Module-level",
                "function_name": f"{module} 模块功能聚合",
                "qualified_name": module_qualified_name(module),
                "canonical_qualified_name": module,
                "module": module,
                "brief": brief_from_counts(f"汇总 {module} 模块的类级功能", method_count, lifecycle, algorithms),
                "sub_functions": [row["qualified_name"] for row in rows],
                "class_count": len(rows),
                "method_count": method_count,
                "lifecycle_roles": dict(lifecycle),
                "algorithm_hints": dict(algorithms),
                "evidence_level": "batch-merged",
                "notes": ["由 Phase4 Class-level 条目合并生成。"],
            }
        )
    return module_rows


def build_system_rows(module_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lifecycle: collections.Counter[str] = collections.Counter()
    algorithms: collections.Counter[str] = collections.Counter()
    method_count = 0
    class_count = 0
    for row in module_rows:
        lifecycle.update(row.get("lifecycle_roles", {}))
        algorithms.update(row.get("algorithm_hints", {}))
        method_count += row.get("method_count", 0)
        class_count += row.get("class_count", 0)
    return [
        {
            "schema_version": "1",
            "level": "System-level",
            "function_name": "AFSIM 函数级能力总览",
            "qualified_name": "AFSIM::System::FunctionInventory",
            "canonical_qualified_name": "AFSIM",
            "brief": brief_from_counts(
                f"汇总 AFSIM 全项目 {len(module_rows)} 个模块、{class_count} 个类级聚合的函数级能力",
                method_count,
                lifecycle,
                algorithms,
            ),
            "sub_functions": [row["qualified_name"] for row in module_rows],
            "module_count": len(module_rows),
            "class_count": class_count,
            "method_count": method_count,
            "lifecycle_roles": dict(lifecycle),
            "algorithm_hints": dict(algorithms),
            "evidence_level": "batch-merged",
            "notes": ["由 Phase4 Module-level 条目合并生成；作为后续业务逻辑分析入口。"],
        }
    ]


def validate(function_rows: list[dict[str, Any]], body_rows: list[dict[str, Any]], skips: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    by_level = collections.defaultdict(dict)
    for row in function_rows:
        qname = row["qualified_name"]
        if qname in by_level[row["level"]]:
            errors.append(f"duplicate qualified_name in {row['level']}: {qname}")
        by_level[row["level"]][qname] = row
        if row["level"] in {"System-level", "Module-level", "Class-level"} and not row.get("brief"):
            errors.append(f"empty brief: {qname}")

    lower_for = {
        "System-level": set(by_level["Module-level"]),
        "Module-level": set(by_level["Class-level"]),
        "Class-level": set(by_level["Method-level"]),
    }
    for row in function_rows:
        if row["level"] in lower_for:
            missing = [name for name in row.get("sub_functions", []) if name not in lower_for[row["level"]]]
            if missing:
                errors.append(f"{row['qualified_name']} has missing sub_functions: {missing[:3]}")

    method_ids = {row["candidate_id"] for row in by_level["Method-level"].values()}
    body_ids = {row["candidate_id"] for row in body_rows}
    if method_ids != body_ids:
        errors.append(f"method/body candidate_id mismatch: method={len(method_ids)} body={len(body_ids)}")

    skip_ids = {row["candidate_id"] for row in skips}
    if method_ids & skip_ids:
        errors.append(f"candidate appears in both method and skip: {len(method_ids & skip_ids)}")
    return errors


def run(root: Path) -> dict[str, Any]:
    source_index = root / "workspace/source-index"
    batch_dir = source_index / "phase4-batches"
    candidates = {row["candidate_id"]: row for row in read_jsonl(source_index / "functions-to-extract-phase4.jsonl")}
    methods_raw, bodies_raw, skips = load_batch_rows(batch_dir)
    methods = enrich_methods(dedupe_by_candidate(methods_raw, "methods"), candidates)
    bodies = dedupe_by_candidate(bodies_raw, "bodies")
    global_duplicate_fix_count = enforce_global_unique(methods, bodies)

    class_rows = build_class_rows(methods)
    module_rows = build_module_rows(class_rows)
    system_rows = build_system_rows(module_rows)
    function_rows = system_rows + module_rows + class_rows + methods

    errors = validate(function_rows, bodies, skips)
    if errors:
        raise SystemExit("Phase4 merge validation failed:\n" + "\n".join(errors[:20]))

    write_jsonl(source_index / "function-index.jsonl", function_rows)
    write_jsonl(source_index / "function-body-summary.jsonl", sorted(bodies, key=lambda row: methods_raw_index.get(row["candidate_id"], 10**12)))
    write_jsonl(source_index / "phase4-function-skips.jsonl", skips)

    summaries = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(batch_dir.glob("phase4-batch??-summary.json"))]
    input_count = sum(row["input_candidate_count"] for row in summaries)
    effective_count = sum(row.get("effective_candidate_count", row["input_candidate_count"]) for row in summaries)
    invalid_count = sum(row.get("invalid_candidate_count", 0) for row in summaries)
    summary = {
        "schema_version": "1",
        "phase": "phase4-functions",
        "status": "merged",
        "batch_count": len(summaries),
        "input_candidate_count": input_count,
        "effective_candidate_count": effective_count,
        "invalid_candidate_count": invalid_count,
        "method_done_count": len(methods),
        "body_summary_count": len(bodies),
        "skip_count": len(skips),
        "raw_coverage": round(len(methods) / input_count, 4) if input_count else 0,
        "coverage": round(len(methods) / effective_count, 4) if effective_count else 0,
        "system_level_count": len(system_rows),
        "module_level_count": len(module_rows),
        "class_level_count": len(class_rows),
        "method_level_count": len(methods),
        "function_index_count": len(function_rows),
        "global_duplicate_name_fix_count": global_duplicate_fix_count,
        "skip_reasons": dict(collections.Counter(row.get("skip_reason") for row in skips)),
        "outputs": {
            "function_index": "workspace/source-index/function-index.jsonl",
            "function_body_summary": "workspace/source-index/function-body-summary.jsonl",
            "skips": "workspace/source-index/phase4-function-skips.jsonl",
        },
    }
    (source_index / "phase4-merge-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


methods_raw_index: dict[str, int] = {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    global methods_raw_index
    methods_raw, _bodies_raw, _skips = load_batch_rows(root / "workspace/source-index/phase4-batches")
    methods_raw_index = {row["candidate_id"]: index for index, row in enumerate(methods_raw)}
    print(json.dumps(run(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
