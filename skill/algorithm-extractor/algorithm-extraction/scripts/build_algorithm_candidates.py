#!/usr/bin/env python3
"""Build a resumable AFSIM algorithm-candidate manifest from analyzer JSONL."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


NAME_SIGNAL = re.compile(
    r"(integrat|propagat|calculat|compute|solve|interpolat|filter|guid|control|"
    r"estimate|transform|convert|dynamics|kinematic|aero|atmos|gravity|orbit|"
    r"track|predict|update|model|evaluate)",
    re.IGNORECASE,
)

MANUAL_FIELDS = ("status", "algorithm_ids", "decision_reason", "review_notes")


def read_jsonl(file_path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with file_path.open("r", encoding="utf-8-sig") as stream:
        for line_number, raw_line in enumerate(stream, 1):
            if not raw_line.strip():
                continue
            try:
                item = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{file_path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"{file_path}:{line_number}: expected a JSON object")
            yield line_number, item


def body_key(item: dict[str, Any]) -> str:
    candidate_id = str(item.get("candidate_id") or "")
    if candidate_id:
        return f"id:{candidate_id}"
    return "loc:{qualified}|{path}|{line}".format(
        qualified=item.get("qualified_name") or "",
        path=item.get("path") or "",
        line=item.get("line_start") or "",
    )


def derive_module(index_path: str) -> str:
    parts = [part for part in Path(index_path).parts if part not in ("", ".")]
    if "src" in parts:
        start = parts.index("src") + 1
        remaining = parts[start:]
        if len(remaining) >= 2:
            return "/".join(remaining[:2])
        if remaining:
            return remaining[0]
    return "unknown"


def resolve_source(source_root: Path | None, index_path: str) -> bool:
    if source_root is None or not index_path:
        return False
    source_root = source_root.resolve()
    relative = Path(index_path)
    options = [source_root / relative, source_root.parent / relative]
    if relative.parts and relative.parts[0] == source_root.name:
        options.append(source_root.joinpath(*relative.parts[1:]))
    if source_root.name == "source_root":
        options.extend(child / relative for child in source_root.iterdir() if child.is_dir())
        for child in source_root.iterdir():
            if child.is_dir() and relative.parts and relative.parts[0] == child.name:
                options.append(child.joinpath(*relative.parts[1:]))
    return any(option.is_file() for option in options)


def score_candidate(
    function: dict[str, Any], body: dict[str, Any], include_control_flow: bool
) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    hint = function.get("algorithm_hint") or body.get("algorithm_pattern") or "none"
    hint_scores = {"math": 100, "state_update": 70, "control_flow": 35}
    score += hint_scores.get(hint, 0)
    if hint in hint_scores:
        reasons.append(f"algorithm_hint={hint}")

    density = body.get("computation_density") or "unknown"
    density_scores = {"high": 30, "medium": 15, "low": 0}
    score += density_scores.get(density, 0)
    if density in ("high", "medium"):
        reasons.append(f"computation_density={density}")

    operations = [
        str(value)
        for value in (body.get("math_operations") or [])
        if str(value).lower() not in ("", "none", "unknown")
    ]
    if operations:
        score += min(20, 5 * len(operations))
        reasons.append("math_operations=" + ",".join(operations[:4]))

    qualified_name = str(function.get("qualified_name") or "")
    if NAME_SIGNAL.search(qualified_name):
        score += 10
        reasons.append("algorithmic_name_signal")

    if hint == "control_flow" and not include_control_flow:
        score = 0
    return score, reasons


def load_existing(output_path: Path) -> dict[str, dict[str, Any]]:
    if not output_path.is_file():
        return {}
    existing: dict[str, dict[str, Any]] = {}
    for _, item in read_jsonl(output_path):
        key = str(item.get("candidate_id") or body_key(item))
        existing[key] = item
    return existing


def atomic_write_jsonl(output_path: Path, items: list[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.", suffix=".tmp", dir=output_path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            for item in items:
                stream.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")))
                stream.write("\n")
        os.replace(temporary_name, output_path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--function-index", type=Path, required=True)
    parser.add_argument("--body-summary", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--include-control-flow",
        action="store_true",
        help="Include control-flow candidates in addition to math and state_update.",
    )
    parser.add_argument(
        "--include-candidate-id",
        action="append",
        default=[],
        help=(
            "Explicitly include one upstream candidate_id even when its algorithm hint "
            "is outside the default filter. Repeat for multiple IDs."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bodies = {body_key(item): item for _, item in read_jsonl(args.body_summary)}
    existing = load_existing(args.output)
    accepted_hints = {"math", "state_update"}
    if args.include_control_flow:
        accepted_hints.add("control_flow")
    explicitly_included = set(args.include_candidate_id)

    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    for _, function in read_jsonl(args.function_index):
        if function.get("level") != "Method-level" or not function.get("path"):
            continue
        key = body_key(function)
        if key in seen:
            continue
        seen.add(key)
        body = bodies.get(key, {})
        candidate_id = str(function.get("candidate_id") or key)
        prior = existing.get(candidate_id) or existing.get(key)
        hint = function.get("algorithm_hint") or body.get("algorithm_pattern") or "none"
        preserve_reviewed = bool(
            prior and prior.get("status") in {"selected", "extracted", "rejected", "deferred"}
        )
        explicitly_selected = candidate_id in explicitly_included
        if hint not in accepted_hints and not explicitly_selected and not preserve_reviewed:
            continue
        score, reasons = score_candidate(function, body, args.include_control_flow)
        if explicitly_selected:
            reasons.append("explicit_candidate_id")
        if preserve_reviewed and hint not in accepted_hints:
            reasons.append("preserved_reviewed_candidate")
        if score <= 0 and not explicitly_selected and not preserve_reviewed:
            continue
        score = max(score, 1)

        item: dict[str, Any] = {
            "schema_version": "1.0",
            "candidate_id": candidate_id,
            "qualified_name": function.get("qualified_name") or "",
            "canonical_qualified_name": function.get("canonical_qualified_name") or "",
            "function_name": function.get("function_name") or "",
            "module": derive_module(str(function.get("path") or "")),
            "path": function.get("path") or "",
            "line_start": function.get("line_start"),
            "line_end": function.get("line_end"),
            "algorithm_hint": hint,
            "algorithm_pattern": body.get("algorithm_pattern") or hint,
            "computation_density": body.get("computation_density") or "unknown",
            "lifecycle_role": function.get("lifecycle_role") or "unknown",
            "priority_score": score,
            "selection_reasons": reasons,
            "source_resolved": resolve_source(args.source_root, str(function.get("path") or "")),
            "status": "pending",
            "algorithm_ids": [],
            "decision_reason": "",
            "review_notes": [],
        }
        if prior:
            for field in MANUAL_FIELDS:
                if field in prior:
                    item[field] = prior[field]
        candidates.append(item)

    candidates.sort(
        key=lambda item: (
            -int(item["priority_score"]),
            str(item["module"]),
            str(item["qualified_name"]),
            str(item["candidate_id"]),
        )
    )
    atomic_write_jsonl(args.output, candidates)

    hint_counts = Counter(str(item["algorithm_hint"]) for item in candidates)
    unresolved = sum(not bool(item["source_resolved"]) for item in candidates)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "candidate_count": len(candidates),
                "by_hint": dict(sorted(hint_counts.items())),
                "unresolved_source_count": unresolved,
                "preserved_existing_count": sum(
                    1 for item in candidates if item["candidate_id"] in existing
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
