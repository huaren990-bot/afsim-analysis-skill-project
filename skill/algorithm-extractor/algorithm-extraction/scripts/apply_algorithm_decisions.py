#!/usr/bin/env python3
"""Apply reviewed algorithm decisions and rebuild the full coverage ledger."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable


VALID_STATUS = {"pending", "selected", "extracted", "rejected", "deferred"}


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


def atomic_write_jsonl(output_path: Path, items: Iterable[dict[str, Any]]) -> None:
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
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--coverage", type=Path, required=True)
    return parser.parse_args()


def validate_decision(
    decision: dict[str, Any], decision_path: Path, line_number: int
) -> None:
    candidate_id = decision.get("candidate_id")
    status = decision.get("status")
    if not candidate_id:
        raise ValueError(f"{decision_path}:{line_number}: candidate_id is required")
    if status not in VALID_STATUS:
        raise ValueError(
            f"{decision_path}:{line_number}: status must be one of {sorted(VALID_STATUS)}"
        )
    algorithm_ids = decision.get("algorithm_ids") or []
    reason = str(decision.get("decision_reason") or "").strip()
    if status == "extracted" and not algorithm_ids:
        raise ValueError(
            f"{decision_path}:{line_number}: extracted candidates require algorithm_ids"
        )
    if status in {"rejected", "deferred"} and not reason:
        raise ValueError(
            f"{decision_path}:{line_number}: {status} candidates require decision_reason"
        )


def main() -> int:
    args = parse_args()
    manifest = [item for _, item in read_jsonl(args.manifest)]
    by_candidate_id = {
        str(item.get("candidate_id") or ""): item for item in manifest
    }
    if "" in by_candidate_id:
        raise ValueError(f"{args.manifest}: every candidate requires candidate_id")
    if len(by_candidate_id) != len(manifest):
        raise ValueError(f"{args.manifest}: duplicate candidate_id")

    decisions: dict[str, dict[str, Any]] = {}
    for line_number, decision in read_jsonl(args.decisions):
        validate_decision(decision, args.decisions, line_number)
        candidate_id = str(decision["candidate_id"])
        if candidate_id in decisions:
            raise ValueError(
                f"{args.decisions}:{line_number}: duplicate decision for {candidate_id}"
            )
        if candidate_id not in by_candidate_id:
            raise ValueError(
                f"{args.decisions}:{line_number}: unknown candidate_id {candidate_id}"
            )
        decisions[candidate_id] = decision

    existing_coverage: dict[str, dict[str, Any]] = {}
    if args.coverage.exists():
        for line_number, item in read_jsonl(args.coverage):
            candidate_id = str(item.get("candidate_id") or "")
            if not candidate_id:
                raise ValueError(
                    f"{args.coverage}:{line_number}: candidate_id is required"
                )
            if candidate_id in existing_coverage:
                raise ValueError(
                    f"{args.coverage}:{line_number}: duplicate candidate_id {candidate_id}"
                )
            existing_coverage[candidate_id] = item

    update_fields = (
        "status",
        "algorithm_ids",
        "decision_reason",
        "review_notes",
    )
    for candidate_id, decision in decisions.items():
        candidate = by_candidate_id[candidate_id]
        for field in update_fields:
            if field in decision:
                candidate[field] = decision[field]

    coverage: list[dict[str, Any]] = []
    for candidate in manifest:
        candidate_id = str(candidate["candidate_id"])
        decision = decisions.get(candidate_id, {})
        previous = existing_coverage.get(candidate_id, {})
        coverage.append(
            {
                "schema_version": "1.0",
                "candidate_id": candidate_id,
                "qualified_name": candidate.get("qualified_name") or "",
                "module": candidate.get("module") or "unknown",
                "source": {
                    "path": candidate.get("path") or "",
                    "line_start": candidate.get("line_start"),
                    "line_end": candidate.get("line_end"),
                },
                "status": candidate.get("status") or "pending",
                "algorithm_ids": candidate.get("algorithm_ids") or [],
                "decision_reason": candidate.get("decision_reason") or "",
                "artifacts": (
                    decision["artifacts"]
                    if "artifacts" in decision
                    else previous.get("artifacts") or {}
                ),
                "verification": (
                    decision["verification"]
                    if "verification" in decision
                    else previous.get("verification") or "not_run"
                ),
                "review_notes": candidate.get("review_notes") or [],
            }
        )

    atomic_write_jsonl(args.manifest, manifest)
    atomic_write_jsonl(args.coverage, coverage)
    status_counts = {
        status: sum(1 for item in manifest if item.get("status") == status)
        for status in sorted(VALID_STATUS)
    }
    print(
        json.dumps(
            {
                "manifest": str(args.manifest),
                "coverage": str(args.coverage),
                "decision_count": len(decisions),
                "candidate_count": len(manifest),
                "status_counts": status_counts,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
