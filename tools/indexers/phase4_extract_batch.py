#!/usr/bin/env python3
"""Extract Phase4 Method-level rows for one batch.

The extractor is intentionally file-batch oriented: it reads every candidate
source/header file at most once, then matches all functions against cached text.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
from typing import Any


KEYWORD_CALLS = {
    "alignof",
    "case",
    "catch",
    "const_cast",
    "decltype",
    "delete",
    "do",
    "dynamic_cast",
    "else",
    "for",
    "if",
    "new",
    "reinterpret_cast",
    "return",
    "sizeof",
    "static_cast",
    "switch",
    "throw",
    "try",
    "typeid",
    "while",
}

COMMON_NONSEMANTIC_CALLS = {
    "begin",
    "block",
    "empty",
    "end",
    "forward",
    "get",
    "make_shared",
    "make_unique",
    "move",
    "size",
}

HEADER_SUFFIXES = (".hpp", ".h", ".hh", ".hxx")
SOURCE_SUFFIXES = (".cpp", ".cc", ".cxx", ".C")
INLINE_SUFFIXES = (".inl", ".ipp", ".tpp")
_BASENAME_CACHE: dict[tuple[str, str], list[str]] = {}
_STEM_CACHE: dict[tuple[str, str], list[str]] = {}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def select_batch_candidates(root: Path, batch: dict[str, Any]) -> list[dict[str, Any]]:
    unit_ids = {unit["unit_id"] for unit in batch["units"]}
    candidates = read_jsonl(root / "workspace/source-index/functions-to-extract-phase4.jsonl")
    by_unit: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in candidates:
        by_unit[str(Path(row["path"]).parent)].append(row)

    selected: list[dict[str, Any]] = []
    target_split = 1200
    for unit, rows in by_unit.items():
        files: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        for row in rows:
            files[row["path"]].append(row)

        if len(rows) > target_split:
            current: list[dict[str, Any]] = []
            part = 1
            for _path, file_rows in sorted(files.items()):
                if current and len(current) + len(file_rows) > target_split:
                    if f"{unit}#part{part:02d}" in unit_ids:
                        selected.extend(current)
                    part += 1
                    current = []
                current.extend(file_rows)
            if current and f"{unit}#part{part:02d}" in unit_ids:
                selected.extend(current)
        elif unit in unit_ids:
            selected.extend(rows)

    return selected


def project_rel(path: str | None) -> str | None:
    return path.replace("\\", "/") if path else None


def existing_rel(root: Path, rel: str | None) -> str | None:
    if not rel:
        return None
    return rel if (root / "source_root" / rel).exists() else None


def sibling_candidates(rel: str | None) -> list[str]:
    if not rel:
        return []
    path = Path(rel)
    stem = path.with_suffix("")
    suffixes = HEADER_SUFFIXES + SOURCE_SUFFIXES + INLINE_SUFFIXES
    return [str(stem.with_suffix(suffix)).replace("\\", "/") for suffix in suffixes]


def basename_candidates(root: Path, rel: str | None) -> list[str]:
    if not rel:
        return []
    stem = Path(rel).stem
    cache_key = (str(root), stem)
    if cache_key in _BASENAME_CACHE:
        return _BASENAME_CACHE[cache_key]

    search_root = root / "source_root/afsim-2_9/swdev/src"
    suffixes = set(HEADER_SUFFIXES + SOURCE_SUFFIXES + INLINE_SUFFIXES)
    matches: list[str] = []
    if search_root.exists():
        for path in search_root.rglob(stem + ".*"):
            if path.suffix in suffixes:
                matches.append(str(path.relative_to(root / "source_root")).replace("\\", "/"))
    matches.sort(key=lambda p: (0 if Path(p).suffix in SOURCE_SUFFIXES else 1, len(p), p))
    _BASENAME_CACHE[cache_key] = matches
    return matches


def source_tree_stem_candidates(root: Path, stem: str | None) -> list[str]:
    """Find files whose basename equals a candidate implementation stem.

    Header names do not always match implementation class names in large C++
    projects, e.g. Bounds.hpp can declare TimeBounds while TimeBounds.cpp holds
    the definitions. This cache-backed search covers that class-name split.
    """

    if not stem or not re.fullmatch(r"[A-Za-z_]\w*", stem):
        return []
    if len(stem) <= 2 or stem in {"Data", "Info", "Base", "Impl", "Type", "Node", "Item", "Model", "Filter"}:
        return []

    cache_key = (str(root), stem)
    if cache_key in _STEM_CACHE:
        return _STEM_CACHE[cache_key]

    search_root = root / "source_root/afsim-2_9/swdev/src"
    suffixes = set(HEADER_SUFFIXES + SOURCE_SUFFIXES + INLINE_SUFFIXES)
    matches: list[str] = []
    if search_root.exists():
        for path in search_root.rglob(stem + ".*"):
            if path.suffix in suffixes:
                matches.append(str(path.relative_to(root / "source_root")).replace("\\", "/"))
    matches.sort(key=lambda p: (0 if Path(p).suffix in SOURCE_SUFFIXES else 1, len(p), p))
    _STEM_CACHE[cache_key] = matches
    return matches


def owner_search_stems(row: dict[str, Any]) -> list[str]:
    stems: list[str] = []
    for value in (row.get("owner"), row.get("qualified_name")):
        if not value:
            continue
        parts = [part for part in str(value).split("::") if part]
        if row.get("qualified_name") == value and len(parts) > 1:
            parts = parts[:-1]
        if parts:
            stems.append(parts[-1])
    return list(dict.fromkeys(stems))


def candidate_search_paths(root: Path, row: dict[str, Any]) -> list[str]:
    """Return ordered files to search for a function body.

    This is the main head-to-source enhancement:
    definition_path is still first, but declaration_path and same-stem
    header/inline/source siblings are searched before declaring no body.
    """

    ordered: list[str] = []
    for rel in (
        row.get("definition_path"),
        row.get("path"),
        row.get("declaration_path"),
    ):
        rel = project_rel(rel)
        if rel:
            ordered.append(rel)
        ordered.extend(sibling_candidates(rel))
        ordered.extend(basename_candidates(root, rel))

    for stem in owner_search_stems(row):
        ordered.extend(source_tree_stem_candidates(root, stem))

    seen: set[str] = set()
    result: list[str] = []
    for rel in ordered:
        if rel in seen:
            continue
        seen.add(rel)
        if existing_rel(root, rel):
            result.append(rel)
    return result


def split_params(param_text: str) -> list[str]:
    parts: list[str] = []
    current = ""
    depth = 0
    for char in param_text:
        if char in "(<[{":
            depth += 1
        elif char in ")>]}":
            depth = max(0, depth - 1)
        if char == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += char
    if current.strip():
        parts.append(current.strip())
    return parts


def parse_params(signature: str) -> list[dict[str, Any]]:
    if "(" not in signature or ")" not in signature:
        return []
    text = signature[signature.find("(") + 1 : signature.rfind(")")].strip()
    if not text or text == "void":
        return []

    params: list[dict[str, Any]] = []
    for raw_param in split_params(text):
        default_value = None
        param = raw_param
        if "=" in param:
            param, default_value = param.split("=", 1)
            param = param.strip()
            default_value = default_value.strip()

        tokens = param.replace("&", " & ").replace("*", " * ").split()
        name = tokens[-1] if tokens else ""
        if re.fullmatch(r"[A-Za-z_]\w*", name):
            param_type = param[: param.rfind(name)].strip()
        else:
            name = f"param{len(params) + 1}"
            param_type = param

        params.append(
            {
                "name": name,
                "type": param_type or "unknown",
                "default_value": default_value,
                "input_output": "input",
                "valid_range": "unknown",
            }
        )
    return params


def return_type(signature: str, function_name: str, kind: str) -> str:
    if kind in {"constructor", "destructor"} or function_name.startswith("~"):
        return ""
    before = signature.split("(", 1)[0].strip()
    if "operator" in before:
        return "operator"
    idx = before.rfind(function_name)
    if idx > 0:
        rt = before[:idx]
        rt = re.sub(r"\b(virtual|static|inline|explicit|constexpr|friend|extern)\b\s*", "", rt).strip()
        return rt or "unknown"
    return "unknown"


def matching_paren(text: str, open_idx: int) -> int:
    depth = 0
    in_string: str | None = None
    escaped = False
    in_line_comment = False
    in_block_comment = False
    idx = open_idx
    while idx < len(text):
        char = text[idx]
        nxt = text[idx + 1] if idx + 1 < len(text) else ""
        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            idx += 1
            continue
        if in_block_comment:
            if char == "*" and nxt == "/":
                in_block_comment = False
                idx += 2
                continue
            idx += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == in_string:
                in_string = None
            idx += 1
            continue
        if char == "/" and nxt == "/":
            in_line_comment = True
            idx += 2
            continue
        if char == "/" and nxt == "*":
            in_block_comment = True
            idx += 2
            continue
        if char in ("'", '"'):
            in_string = char
            idx += 1
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return idx
        idx += 1
    return -1


def matching_brace(text: str, open_idx: int) -> int:
    depth = 0
    in_string: str | None = None
    escaped = False
    in_line_comment = False
    in_block_comment = False
    idx = open_idx
    while idx < len(text):
        char = text[idx]
        nxt = text[idx + 1] if idx + 1 < len(text) else ""
        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            idx += 1
            continue
        if in_block_comment:
            if char == "*" and nxt == "/":
                in_block_comment = False
                idx += 2
                continue
            idx += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == in_string:
                in_string = None
            idx += 1
            continue
        if char == "/" and nxt == "/":
            in_line_comment = True
            idx += 2
            continue
        if char == "/" and nxt == "*":
            in_block_comment = True
            idx += 2
            continue
        if char in ("'", '"'):
            in_string = char
            idx += 1
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return idx
        idx += 1
    return -1


def owner_variants(owner: str | None) -> list[str]:
    if not owner:
        return []
    parts = owner.split("::")
    variants = [owner]
    if parts:
        variants.append(parts[-1])
    return list(dict.fromkeys(variants))


def function_patterns(row: dict[str, Any]) -> list[re.Pattern[str]]:
    name = row["function_name"]
    escaped_name = re.escape(name)
    patterns: list[str] = []
    operator_patterns: list[str] = []
    if name == "operator" or name.startswith("operator"):
        signature = row.get("signature") or ""
        if "operator()" in signature:
            operator_patterns.append(r"\boperator\s*\(\)\s*\(")
        if "operator[]" in signature:
            operator_patterns.append(r"\boperator\s*\[\]\s*\(")
        if not operator_patterns:
            operator_patterns.append(r"\boperator\s*[^\s(]*\s*\(")
    for owner in owner_variants(row.get("owner")):
        if operator_patterns:
            for operator_pattern in operator_patterns:
                patterns.append(r"\b" + re.escape(owner) + r"\s*::\s*" + operator_pattern.lstrip(r"\b"))
        else:
            patterns.append(r"\b" + re.escape(owner) + r"\s*::\s*" + escaped_name + r"\s*\(")
    if operator_patterns:
        patterns.extend(operator_patterns)
    else:
        patterns.append(r"\b" + escaped_name + r"\s*\(")
    return [re.compile(pattern) for pattern in dict.fromkeys(patterns)]


def skip_after_params(text: str, idx: int) -> int:
    while True:
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx + 1 < len(text) and text[idx] == "/" and text[idx + 1] == "/":
            idx += 2
            while idx < len(text) and text[idx] != "\n":
                idx += 1
            continue
        if idx + 1 < len(text) and text[idx] == "/" and text[idx + 1] == "*":
            idx += 2
            while idx + 1 < len(text) and not (text[idx] == "*" and text[idx + 1] == "/"):
                idx += 1
            idx = min(len(text), idx + 2)
            continue
        break
    advanced = True
    while advanced:
        advanced = False
        for keyword in ("const", "override", "final", "noexcept"):
            if text.startswith(keyword, idx) and (idx + len(keyword) == len(text) or not text[idx + len(keyword)].isalnum()):
                idx += len(keyword)
                advanced = True
                while True:
                    while idx < len(text) and text[idx].isspace():
                        idx += 1
                    if idx + 1 < len(text) and text[idx] == "/" and text[idx + 1] == "/":
                        idx += 2
                        while idx < len(text) and text[idx] != "\n":
                            idx += 1
                        continue
                    if idx + 1 < len(text) and text[idx] == "/" and text[idx + 1] == "*":
                        idx += 2
                        while idx + 1 < len(text) and not (text[idx] == "*" and text[idx + 1] == "/"):
                            idx += 1
                        idx = min(len(text), idx + 2)
                        continue
                    break
    return idx


def find_body_in_text(text: str, row: dict[str, Any]) -> tuple[int, int] | None:
    for pattern in function_patterns(row):
        for match in pattern.finditer(text):
            open_idx = text.find("(", match.end() - 1)
            if row["function_name"] == "operator" or row["function_name"].startswith("operator"):
                # For operator() and operator[] the first parens/brackets are
                # part of the operator name. The parameter list starts after it.
                if re.search(r"operator\s*\(\)\s*\($", match.group(0)):
                    open_idx = match.end() - 1
                elif re.search(r"operator\s*\[\]\s*\($", match.group(0)):
                    open_idx = match.end() - 1
            close_idx = matching_paren(text, open_idx)
            if close_idx < 0:
                continue

            idx = skip_after_params(text, close_idx + 1)
            if text.startswith("try", idx) and (idx + 3 == len(text) or not text[idx + 3].isalnum()):
                idx = skip_after_params(text, idx + 3)
            if idx < len(text) and text[idx] == ":":
                while idx < len(text) and text[idx] not in "{;":
                    idx += 1

            if idx < len(text) and text[idx] == "{":
                end = matching_brace(text, idx)
                if end >= 0:
                    return match.start(), end + 1
    return None


def line_no(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def token_set(*values: str) -> set[str]:
    raw = " ".join(values)
    split_camel = re.sub(r"([a-z])([A-Z])", r"\1 \2", raw)
    return set(re.findall(r"[a-z][a-z0-9_]*", split_camel.lower()))


def classify_lifecycle(name: str, calls: list[str], kind: str) -> str:
    tokens = token_set(name, " ".join(calls))
    if kind == "destructor" or name.startswith("~") or tokens & {"destroy", "shutdown", "cleanup", "terminate", "clear"}:
        return "shutdown"
    if tokens & {"main", "run", "advance", "step", "simulate", "simulation", "clock", "time"}:
        return "simulation_loop"
    if tokens & {"load", "parse", "input", "scenario", "configure", "config"}:
        return "scenario_load"
    if tokens & {"create", "factory", "clone", "initialize", "init", "register", "add"}:
        return "object_create"
    if tokens & {"update", "process", "execute", "compute", "calculate", "move", "propagate"}:
        return "model_update"
    if tokens & {"event", "notify", "message", "callback", "observer", "send", "receive"}:
        return "event_handling"
    if tokens & {"write", "print", "report", "output", "log", "serialize"}:
        return "output"
    if tokens & {"read", "set", "get", "find", "check", "validate"}:
        return "configuration"
    return "utility"


def classify_algorithm(body: str, name: str, path: str) -> str:
    text = " ".join([body[:2000], name, path]).lower()
    if any(word in text for word in ("ifstream", "ofstream", "fstream", "read", "write", "serialize", "file", "stream")):
        return "io"
    if any(word in text for word in ("parse", "input", "config", "scenario", "token")):
        return "configuration"
    if any(word in text for word in ("factory", "create", "register", "clone")):
        return "factory"
    if any(word in text for word in ("state", "mode", "switch", "case", "decision")):
        return "control_flow"
    if any(word in text for word in ("sqrt", "sin", "cos", "tan", "matrix", "vec", "integrat", "kalman", "monte", "rk4")):
        return "math"
    if len(re.findall(r"[+\-*/]=?|\bstd::(min|max|abs)\b", body)) > 20:
        return "math"
    if any(word in text for word in ("update", "position", "velocity", "acceleration", "state")):
        return "state_update"
    return "none"


def computation_density(body: str) -> str:
    ops = len(re.findall(r"[+\-*/]=?|\bfor\b|\bwhile\b|\bstd::|Matrix|Vec|Integrat|Kalman", body))
    lines = max(1, body.count("\n") + 1)
    ratio = ops / lines
    if ratio > 1.2 or ops > 80:
        return "high"
    if ratio > 0.35 or ops > 20:
        return "medium"
    return "low"


def extract_calls(body: str, current_name: str) -> list[str]:
    calls: set[str] = set()
    for match in re.finditer(r"\b([A-Za-z_]\w*)\s*\(", body):
        name = match.group(1)
        if name in KEYWORD_CALLS or name in COMMON_NONSEMANTIC_CALLS or name == current_name:
            continue
        calls.add(name)
    return sorted(calls)[:80]


def extract_one(row: dict[str, Any], rel: str, text: str) -> tuple[dict[str, Any], dict[str, Any]] | None:
    loc = find_body_in_text(text, row)
    if not loc:
        return None

    start, end = loc
    body = text[start:end]
    calls = extract_calls(body, row["function_name"])
    members = sorted(set(re.findall(r"\bm[A-Z]\w*\b", body)))[:80]
    writes = sorted(set(re.findall(r"\b(m[A-Z]\w*)\s*(?:=|\+=|-=|\*=|/=|\+\+|--)", body)))[:80]
    reads = [member for member in members if member not in writes]
    line_start = line_no(text, start)
    line_end = line_no(text, end)
    qualified_name = row["qualified_name"] + "#" + row["signature_digest"]

    notes = list(row.get("notes") or [])
    if row.get("source_qualified_name"):
        notes.append("Phase3 原始限定名已按 signature 修正: " + row["source_qualified_name"])
    if rel != row.get("path"):
        notes.append("函数体命中声明/同名头文件: " + rel)

    method = {
        "schema_version": "1",
        "candidate_id": row["candidate_id"],
        "function_name": row["function_name"],
        "qualified_name": qualified_name,
        "canonical_qualified_name": row["qualified_name"],
        "level": "Method-level",
        "brief": f"{row['kind']}: {row['signature']}",
        "path": rel,
        "line_start": line_start,
        "line_end": line_end,
        "return_type": return_type(row["signature"], row["function_name"], row["kind"]),
        "parameters": parse_params(row["signature"]),
        "calls": calls,
        "reads": reads,
        "writes": writes,
        "lifecycle_role": classify_lifecycle(row["function_name"], calls, row["kind"]),
        "algorithm_hint": classify_algorithm(body, row["function_name"], rel),
        "dependencies": calls,
        "is_virtual": "virtual" in row["signature"],
        "is_override": "override" in row["signature"],
        "is_const": bool(re.search(r"\)\s*const\b", row["signature"])),
        "is_static": "static" in row["signature"],
        "access_modifier": "unknown",
        "embedding": None,
        "evidence_level": "source-cited",
        "notes": notes,
    }

    body_summary = {
        "schema_version": "1",
        "candidate_id": row["candidate_id"],
        "qualified_name": qualified_name,
        "canonical_qualified_name": row["qualified_name"],
        "path": rel,
        "line_start": line_start,
        "line_end": line_end,
        "body_line_count": line_end - line_start + 1,
        "control_flow_summary": (
            "包含条件分支/循环，需在业务分析阶段结合调用方细化"
            if re.search(r"\b(if|for|while|switch)\b", body)
            else "线性执行或简单转发，无明显复杂控制流"
        ),
        "key_variables": [
            {"name": member, "type": "member", "role": "state", "brief": "成员状态变量"} for member in members[:20]
        ],
        "computation_density": computation_density(body),
        "math_operations": sorted(
            set(re.findall(r"\b(sqrt|sin|cos|tan|atan2|pow|Normalize|Dot|Cross|Matrix|Vec|Integrate|Kalman)\b", body))
        )[:30]
        or ["none"],
        "calls_summary": calls[:50],
        "algorithm_pattern": classify_algorithm(body, row["function_name"], rel),
        "evidence_level": "source-cited",
    }
    return method, body_summary


def skip_reason_for_unmatched(row: dict[str, Any]) -> str:
    """Classify unmatched candidates without hiding real declarations.

    Some Phase3 member-function candidates were seeded from broad signature
    scans and include local variable direct-initialization or expression
    fragments, such as `std::vector<size_t> after(...)` inside a method body.
    These are invalid function candidates and should not remain in the effective
    Phase4 denominator. Pure virtual/default/delete declarations are still real
    declarations, so they remain declaration_only.
    """

    signature = (row.get("signature") or "").strip()
    function_name = row.get("function_name") or ""
    if re.search(r"=\s*(?:0|default|delete)\b", signature):
        return "declaration_only"
    if re.search(r"(^|[;{}]\s*)throw\s+", signature):
        return "variable_not_function"
    if re.search(r"(^|[;{}]\s*)return\s+", signature):
        return "variable_not_function"
    if re.search(r"\btypeid\s*\(", signature):
        return "variable_not_function"
    if "<<" in signature and not function_name.startswith("operator"):
        return "variable_not_function"

    escaped_name = re.escape(function_name)
    variable_decl = re.match(
        r"^(?:}\s*)*(?:const\s+)?(?:typename\s+)?"
        r"(?:std::[A-Za-z_]\w*(?:::[A-Za-z_]\w*)?(?:<[^)]*>)?|"
        r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)?(?:<[^)]*>)?|"
        r"[A-Z_][A-Z_0-9]*)\s+"
        + escaped_name
        + r"\s*\(",
        signature,
    )
    if variable_decl and re.match(r"[a-z_]\w*$", function_name):
        return "variable_not_function"
    return "declaration_only"


def enforce_unique_method_names(method_rows: list[dict[str, Any]], body_rows: list[dict[str, Any]]) -> int:
    """Make qualified_name unique within a batch.

    Signature digest is usually enough for overloads, but large C++ projects can
    contain same short owner/name/signature in distinct anonymous/local classes or
    duplicated helper types. candidate_id is the stable final tie-breaker.
    """

    counts = collections.Counter(row["qualified_name"] for row in method_rows)
    body_by_id = {row["candidate_id"]: row for row in body_rows}
    fixed = 0
    for method in method_rows:
        if counts[method["qualified_name"]] <= 1:
            continue
        old_name = method["qualified_name"]
        new_name = f"{old_name}@{method['candidate_id'][:8]}"
        method["qualified_name"] = new_name
        method.setdefault("notes", []).append("同签名短限定名重复，追加 candidate_id 短后缀保证唯一性")
        if method["candidate_id"] in body_by_id:
            body_by_id[method["candidate_id"]]["qualified_name"] = new_name
        fixed += 1
    return fixed


def run_batch(root: Path, batch_id: str) -> dict[str, Any]:
    plan_path = root / "workspace/source-index/phase4-function-batch-plan.jsonl"
    plan = read_jsonl(plan_path)
    batch = next((item for item in plan if item["batch_id"] == batch_id), None)
    if not batch:
        raise SystemExit(f"batch not found: {batch_id}")

    selected = select_batch_candidates(root, batch)
    file_cache: dict[str, str] = {}
    for row in selected:
        for rel in candidate_search_paths(root, row):
            if rel not in file_cache:
                file_cache[rel] = (root / "source_root" / rel).read_text(errors="ignore")

    method_rows: list[dict[str, Any]] = []
    body_rows: list[dict[str, Any]] = []
    skip_rows: list[dict[str, Any]] = []
    matched_file_counts: collections.Counter[str] = collections.Counter()

    for row in selected:
        extracted = None
        for rel in candidate_search_paths(root, row):
            extracted = extract_one(row, rel, file_cache[rel])
            if extracted:
                matched_file_counts[rel] += 1
                break
        if extracted:
            method, body_summary = extracted
            method_rows.append(method)
            body_rows.append(body_summary)
        else:
            skip_reason = skip_reason_for_unmatched(row)
            skip_note = (
                "增强匹配后判定为变量/表达式误识别，按非函数候选记录"
                if skip_reason == "variable_not_function"
                else "增强匹配后仍未定位到函数体，按声明-only 记录"
            )
            skip_rows.append(
                {
                    **row,
                    "status": "skipped",
                    "skip_reason": skip_reason,
                    "notes": list(row.get("notes") or []) + [skip_note],
                }
            )

    duplicate_name_fix_count = enforce_unique_method_names(method_rows, body_rows)

    out_dir = root / "workspace/source-index/phase4-batches"
    out_dir.mkdir(parents=True, exist_ok=True)
    function_path = out_dir / f"{batch_id}-function-index.jsonl"
    body_path = out_dir / f"{batch_id}-function-body-summary.jsonl"
    skip_path = out_dir / f"{batch_id}-skips.jsonl"
    summary_path = out_dir / f"{batch_id}-summary.json"

    write_jsonl(function_path, method_rows)
    write_jsonl(body_path, body_rows)
    write_jsonl(skip_path, skip_rows)

    invalid_candidate_count = sum(1 for row in skip_rows if row["skip_reason"] == "variable_not_function")
    effective_candidate_count = max(0, len(selected) - invalid_candidate_count)
    raw_coverage = round(len(method_rows) / len(selected), 4) if selected else 0
    effective_coverage = round(len(method_rows) / effective_candidate_count, 4) if effective_candidate_count else 0

    summary = {
        "schema_version": "1",
        "batch_id": batch_id,
        "status": "completed",
        "input_candidate_count": len(selected),
        "effective_candidate_count": effective_candidate_count,
        "invalid_candidate_count": invalid_candidate_count,
        "read_file_count": len(file_cache),
        "method_done_count": len(method_rows),
        "body_summary_count": len(body_rows),
        "skip_count": len(skip_rows),
        "raw_coverage": raw_coverage,
        "coverage": effective_coverage,
        "skip_reasons": dict(collections.Counter(row["skip_reason"] for row in skip_rows)),
        "matched_files_not_in_original_path": sum(
            1 for row in method_rows if row["path"] != next(c["path"] for c in selected if c["candidate_id"] == row["candidate_id"])
        ),
        "duplicate_name_fix_count": duplicate_name_fix_count,
        "top_matched_files": dict(matched_file_counts.most_common(20)),
        "output_function_index": str(function_path.relative_to(root)),
        "output_body_summary": str(body_path.relative_to(root)),
        "output_skips": str(skip_path.relative_to(root)),
        "notes": [
            "增强匹配：同时搜索 definition_path、path、declaration_path、同名头文件和 inline 文件。",
            "补充匹配：从 owner/qualified_name 提取类名，搜索类名同 stem 的源/头/inline 文件，覆盖声明头文件与实现文件不同名的场景。",
            "每个候选搜索文件读取后复用缓存；同一文件不重复读取。",
            "qualified_name 追加 signature_digest 以避免重载静默覆盖；若仍重复则追加 candidate_id 短后缀。",
            "coverage 使用有效候选口径；raw_coverage 保留未剔除变量/表达式误报前的原始口径。",
        ],
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    for item in plan:
        if item["batch_id"] == batch_id:
            item.update(
                {
                    "status": "completed",
                    "method_done_count": len(method_rows),
                    "skip_count": len(skip_rows),
                    "coverage": summary["coverage"],
                    "read_file_count": len(file_cache),
                    "output_skips": str(skip_path.relative_to(root)),
                }
            )
    write_jsonl(plan_path, plan)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    summary = run_batch(root, args.batch_id)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
