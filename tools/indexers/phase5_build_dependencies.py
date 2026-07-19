#!/usr/bin/env python3
"""Build Phase5 dependency index and graph documents."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable


SOURCE_ROOT_PREFIX = "afsim-2_9/swdev/src/"
RELATIONS = {"build", "inheritance", "composition", "include", "call", "registration"}
PRIMITIVE_TYPES = {
    "bool",
    "char",
    "double",
    "float",
    "int",
    "long",
    "short",
    "size_t",
    "std::size_t",
    "std::string",
    "string",
    "unsigned",
    "void",
}
REGISTRATION_PATTERN = re.compile(
    r"\b(AddComponent|RegisterComponent|ComponentFactory|AddExtension|RegisterExtension|Subscribe|ListenTo|EventPipe|PluginManager::Load|AddFactory|RegisterScriptClasses|AddMessage)\b"
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def load_boundary(root: Path) -> dict[str, Any]:
    path = root / "workspace/project-boundary/project-boundary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("analysis_boundaries") or data


def is_excluded(path: str, excluded: list[str]) -> bool:
    normalized = path.replace("\\", "/")
    parts = normalized.split("/")
    if any(part.startswith(".") for part in parts):
        return True
    return any(normalized == item or normalized.startswith(item.rstrip("/") + "/") for item in excluded)


def normalize_module(path: str) -> str:
    normalized = path.replace("\\", "/")
    if SOURCE_ROOT_PREFIX not in normalized:
        return normalized.split("/")[0] if normalized else "unknown"
    rest = normalized.split(SOURCE_ROOT_PREFIX, 1)[1]
    parts = [part for part in rest.split("/") if part]
    if not parts:
        return "unknown"
    if parts[0] in {"core", "wsf_plugins", "tools"} and len(parts) > 1:
        return f"{parts[0]}/{parts[1]}"
    return parts[0]


def safe_id(text: str) -> str:
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    return "n_" + digest


def clean_token(token: str) -> str:
    return token.strip().strip('"').strip("'").strip()


def dependency_id(row: dict[str, Any]) -> str:
    raw = "|".join(str(row.get(key, "")) for key in ("source", "target", "relation", "path", "line_start", "symbol"))
    return "dep_" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def make_row(
    source: str,
    target: str,
    relation: str,
    context: str,
    path: str | None,
    line_start: int | None,
    evidence: str,
    strength: str,
    symbol: str | None = None,
    evidence_level: str = "source-cited",
    notes: list[str] | None = None,
    source_module: str | None = None,
    target_module: str | None = None,
) -> dict[str, Any]:
    row = {
        "schema_version": "1",
        "source": source,
        "target": target,
        "relation": relation,
        "context": context,
        "path": path,
        "line_start": line_start,
        "line_end": line_start,
        "symbol": symbol,
        "evidence": evidence[:500],
        "evidence_level": evidence_level,
        "strength": strength,
        "source_module": source_module or (normalize_module(path) if path else normalize_module(source)),
        "target_module": target_module or normalize_module(target),
        "notes": notes or [],
    }
    row["dependency_id"] = dependency_id(row)
    return row


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    result: list[dict[str, Any]] = []
    for row in rows:
        key = (row["source"], row["target"], row["relation"], row.get("path"), row.get("line_start"), row.get("symbol"))
        if key in seen:
            continue
        seen.add(key)
        result.append(row)
    return result


def strip_cmake_comments(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def parse_cmake_blocks(text: str, command: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    pattern = re.compile(r"\b" + re.escape(command) + r"\s*\(", re.IGNORECASE)
    for match in pattern.finditer(text):
        depth = 0
        idx = match.end() - 1
        while idx < len(text):
            char = text[idx]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    result.append((line_number_for_offset(text, match.start()), text[match.end() : idx]))
                    break
            idx += 1
    return result


def build_dependencies(root: Path, excluded: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cmake_root = root / "source_root/afsim-2_9/swdev/src"
    skip_tokens = {"PUBLIC", "PRIVATE", "INTERFACE", "debug", "optimized", "general"}
    for path in sorted(cmake_root.rglob("CMakeLists.txt")):
        rel = str(path.relative_to(root / "source_root")).replace("\\", "/")
        if is_excluded(rel, excluded):
            continue
        text = strip_cmake_comments(path.read_text(errors="ignore"))
        for line_start, body in parse_cmake_blocks(text, "target_link_libraries"):
            tokens = [clean_token(token) for token in re.split(r"[\s\r\n]+", body) if clean_token(token)]
            if len(tokens) < 2:
                continue
            source = tokens[0]
            for target in tokens[1:]:
                if target in skip_tokens or target.startswith("$<") or not target:
                    continue
                rows.append(
                    make_row(
                        source=source,
                        target=target,
                        relation="build",
                        context=f"CMake 目标 {source} 链接 {target}",
                        path=rel,
                        line_start=line_start,
                        evidence=f"target_link_libraries({source} ... {target} ...)",
                        strength="strong",
                        symbol=source,
                        source_module=normalize_module(rel),
                        target_module=target,
                    )
                )
    return rows


def inheritance_dependencies(symbols: list[dict[str, Any]], excluded: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for symbol in symbols:
        path = symbol.get("path") or ""
        if is_excluded(path, excluded):
            continue
        if symbol.get("kind") not in {"class", "struct"}:
            continue
        for base in symbol.get("base_symbols") or []:
            if not base or re.search(r"_EXPORT$|_IMPORT$|_API$|_LIB_EXPORT$", str(base)):
                continue
            rows.append(
                make_row(
                    source=symbol.get("qualified_name") or symbol.get("symbol_name"),
                    target=str(base),
                    relation="inheritance",
                    context=f"{symbol.get('qualified_name')} 继承 {base}",
                    path=path,
                    line_start=symbol.get("line_start"),
                    evidence=symbol.get("signature") or f"base_symbols: {base}",
                    strength="strong",
                    symbol=symbol.get("qualified_name"),
                    source_module=normalize_module(path),
                    target_module="class:" + str(base),
                )
            )
    return rows


def clean_type(type_text: str) -> str:
    text = re.sub(r"\b(const|volatile|mutable|static|mutable)\b", "", type_text)
    text = text.replace("&", " ").replace("*", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def target_from_member(member: str) -> tuple[str, str] | None:
    text = re.sub(r"\s*\[[^\]]+\]\s*$", "", member).strip()
    text = text.split("=", 1)[0].strip()
    if "(" in text and ")" in text:
        return None
    template_match = re.search(r"\b(?:std::)?(unique_ptr|shared_ptr|weak_ptr|CloneablePtr)\s*<\s*([^,>]+)", text)
    if template_match:
        wrapper = template_match.group(1)
        target = clean_type(template_match.group(2))
        strength = "medium" if wrapper != "weak_ptr" else "weak"
        return target, strength
    if "*" in text:
        before_pointer = text.split("*", 1)[0]
        target = clean_type(before_pointer.split()[-1] if before_pointer.split() else before_pointer)
        return (target, "medium") if target and target not in PRIMITIVE_TYPES else None
    tokens = text.split()
    if len(tokens) < 2:
        return None
    target = clean_type(" ".join(tokens[:-1]))
    if not target or target in PRIMITIVE_TYPES:
        return None
    if target.startswith(("std::", "Q")) and "<" not in target:
        return None
    if not re.search(r"[A-Z]", target):
        return None
    return target, "strong"


def composition_dependencies(symbols: list[dict[str, Any]], excluded: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for symbol in symbols:
        path = symbol.get("path") or ""
        if is_excluded(path, excluded):
            continue
        if symbol.get("kind") not in {"class", "struct"}:
            continue
        source = symbol.get("qualified_name") or symbol.get("symbol_name")
        for member in symbol.get("member_variables") or []:
            parsed = target_from_member(str(member))
            if not parsed:
                continue
            target, strength = parsed
            if target == source or target in PRIMITIVE_TYPES:
                continue
            rows.append(
                make_row(
                    source=source,
                    target=target,
                    relation="composition",
                    context=f"{source} 通过成员变量持有 {target}",
                    path=path,
                    line_start=symbol.get("line_start"),
                    evidence=str(member),
                    strength=strength,
                    symbol=source,
                    source_module=normalize_module(path),
                    target_module="class:" + target,
                )
            )
    return rows


def include_dependencies(files: list[dict[str, Any]], excluded: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_basename: dict[str, list[str]] = collections.defaultdict(list)
    all_paths = [row.get("path") for row in files if row.get("path") and not is_excluded(row["path"], excluded)]
    for path in all_paths:
        by_basename[Path(path).name].append(path)

    for row in files:
        source_path = row.get("path") or ""
        if is_excluded(source_path, excluded):
            continue
        source_module = normalize_module(source_path)
        source_dir = str(Path(source_path).parent).replace("\\", "/")
        for include in row.get("includes") or []:
            include = str(include).strip("<>\"")
            candidates = by_basename.get(Path(include).name, [])
            if not candidates:
                continue
            same_module = [item for item in candidates if normalize_module(item) == source_module]
            same_dir = [item for item in candidates if str(Path(item).parent).replace("\\", "/") == source_dir]
            target = (same_dir or same_module or candidates)[0]
            if source_path == target or is_excluded(target, excluded):
                continue
            rows.append(
                make_row(
                    source=source_path,
                    target=target,
                    relation="include",
                    context=f"{source_path} include {include}",
                    path=source_path,
                    line_start=None,
                    evidence=f'#include "{include}"',
                    strength="strong",
                    symbol=None,
                    source_module=source_module,
                    target_module=normalize_module(target),
                )
            )
    return rows


def call_dependencies(functions: list[dict[str, Any]], excluded: list[str]) -> list[dict[str, Any]]:
    methods = [row for row in functions if row.get("level") == "Method-level" and not is_excluded(row.get("path", ""), excluded)]
    by_name: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    by_canonical: dict[str, dict[str, Any]] = {}
    for row in methods:
        by_name[row.get("function_name") or ""].append(row)
        by_canonical[row.get("canonical_qualified_name") or row["qualified_name"]] = row

    rows: list[dict[str, Any]] = []
    for row in methods:
        calls = list(dict.fromkeys((row.get("calls") or []) + (row.get("dependencies") or [])))[:20]
        source = row["qualified_name"]
        source_module = row.get("module") or normalize_module(row.get("path", ""))
        for call in calls:
            call_name = str(call)
            target_row = by_canonical.get(call_name)
            if not target_row:
                matches = by_name.get(call_name) or []
                target_row = matches[0] if matches else None
            target = (
                target_row["qualified_name"]
                if target_row
                else ("external-call:" + call_name)
            )
            target_module = (target_row.get("module") if target_row else "external") or "external"
            rows.append(
                make_row(
                    source=source,
                    target=target,
                    relation="call",
                    context=f"{source} 调用 {call_name}",
                    path=row.get("path"),
                    line_start=row.get("line_start"),
                    evidence=f"calls: {call_name}",
                    strength="medium" if target_row else "weak",
                    symbol=source,
                    source_module=source_module,
                    target_module=target_module,
                    notes=[] if target_row else ["未在 Method-level 中解析到被调用函数定义，按外部/库调用记录。"],
                )
            )
    return rows


def registration_dependencies(root: Path, excluded: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    src_root = root / "source_root/afsim-2_9/swdev/src"
    suffixes = {".cpp", ".cc", ".cxx", ".C", ".hpp", ".h", ".hh", ".hxx", ".ipp", ".inl", ".tpp"}
    for path in sorted(src_root.rglob("*")):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        rel = str(path.relative_to(root / "source_root")).replace("\\", "/")
        if is_excluded(rel, excluded):
            continue
        for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            match = REGISTRATION_PATTERN.search(line)
            if not match:
                continue
            token = match.group(1)
            rows.append(
                make_row(
                    source=rel,
                    target=token,
                    relation="registration",
                    context=f"{rel} 使用 {token} 注册/订阅扩展点",
                    path=rel,
                    line_start=line_no,
                    evidence=line.strip(),
                    strength="weak",
                    symbol=token,
                    source_module=normalize_module(rel),
                    target_module="registration:" + token,
                )
            )
    return rows


def select_edges(rows: list[dict[str, Any]], relation_filter: set[str], limit: int) -> list[dict[str, Any]]:
    filtered = [row for row in rows if row["relation"] in relation_filter and row["source_module"] != row["target_module"]]
    filtered.sort(key=lambda row: ({"strong": 0, "medium": 1, "weak": 2}.get(row["strength"], 9), row["relation"], row["source_module"], row["target_module"]))
    result: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str, str]] = set()
    for row in filtered:
        key = (row["source_module"], row["target_module"], row["relation"])
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        result.append(row)
        if len(result) >= limit:
            break
    return result


def mermaid_block(rows: list[dict[str, Any]], title: str) -> tuple[str, list[dict[str, Any]]]:
    lines = ["```mermaid", "graph TD"]
    node_labels: dict[str, str] = {}
    for row in rows:
        src = safe_id(row["source_module"])
        tgt = safe_id(row["target_module"])
        node_labels[src] = row["source_module"]
        node_labels[tgt] = row["target_module"]
    for node_id, label in sorted(node_labels.items()):
        lines.append(f'  {node_id}["{label}"]')
    for row in rows:
        src = safe_id(row["source_module"])
        tgt = safe_id(row["target_module"])
        label = f"{row['relation']} {row['dependency_id']}"
        lines.append(f'  {src} -->|"{label}"| {tgt}')
    lines.append("```")
    return "\n".join(lines), rows


def write_dependency_docs(root: Path, rows: list[dict[str, Any]], excluded: list[str]) -> None:
    docs = root / "docs/architecture"
    docs.mkdir(parents=True, exist_ok=True)
    counts = collections.Counter(row["relation"] for row in rows)
    modules = sorted({row["source_module"] for row in rows} | {row["target_module"] for row in rows if not row["target_module"].startswith(("class:", "external", "registration:"))})
    involved = {row["source_module"] for row in rows} | {row["target_module"] for row in rows}
    isolated = [module for module in modules if module not in involved]

    build_edges = select_edges(rows, {"build"}, 30)
    arch_edges = select_edges(rows, {"inheritance", "composition", "call"}, 40)
    subsystem_edges = select_edges(rows, RELATIONS, 45)
    registration_edges = select_edges(rows, {"registration"}, 20)
    trace_rows = build_edges + arch_edges + subsystem_edges + registration_edges

    build_graph, _ = mermaid_block(build_edges, "构建依赖")
    arch_graph, _ = mermaid_block(arch_edges, "架构依赖")
    subsystem_graph, _ = mermaid_block(subsystem_edges, "子系统依赖")
    registration_graph, _ = mermaid_block(registration_edges, "注册依赖")

    trace_table = "\n".join(
        f"| `{row['source_module']} -> {row['target_module']}` | `{row['dependency_id']}` | `{row['relation']}` | `{row.get('path')}` | {row['evidence'].replace('|', '/')} |"
        for row in trace_rows
    )
    relation_table = "\n".join(f"| `{rel}` | {counts[rel]:,} |" for rel in sorted(counts))
    excluded_table = "\n".join(f"| `{path}` | Phase1 建议排除架构依赖核心图 |" for path in excluded)
    isolated_table = "\n".join(f"| `{module}` | 当前依赖索引无核心边或仅作为外部/类型名出现 |" for module in isolated) or "| 无 | 所有索引模块均有依赖记录 |"

    graph_doc = f"""# Phase5 依赖关系图

> 状态：已生成
> 完整清单：`workspace/source-index/dependency-index.jsonl`
> 模块明细：`docs/architecture/module-dependency.md`
> 验证报告：`docs/verification/phase5-verify-report.md`

## 0. 分析边界

以下路径按 Phase1 边界排除出核心架构依赖索引和 Mermaid 图：

| 路径 | 原因 |
|---|---|
{excluded_table}

图中只展示摘要边。筛选标准为：优先跨模块、优先 `strong` 强度、每组 `source_module + target_module + relation` 只展示一条代表证据。完整依赖清单以 `workspace/source-index/dependency-index.jsonl` 为准。

## 1. 依赖关系分布

| relation | 条目数 |
|---|---:|
{relation_table}

## 2. 构建依赖图

{build_graph}

## 3. 架构级依赖图

覆盖 `inheritance`、`composition`、`call` 三类关系的跨模块摘要。

{arch_graph}

## 4. 子系统间依赖图

{subsystem_graph}

## 5. 注册/扩展点依赖图

注册依赖用于识别插件、工厂、事件订阅和扩展点接入路径，帮助判断运行时能力如何接入系统。

{registration_graph}

## 6. 孤立或未展示模块说明

| 模块 | 说明 |
|---|---|
{isolated_table}

## 7. Mermaid 边追溯矩阵

| Mermaid 边 | dependency-index 条目 | relation | 证据路径 | 证据 |
|---|---|---|---|---|
{trace_table}
"""
    (docs / "dependency-graph.md").write_text(graph_doc, encoding="utf-8")

    top_module_pairs = collections.Counter((row["source_module"], row["target_module"], row["relation"]) for row in rows)
    pair_rows = "\n".join(
        f"| `{src}` | `{tgt}` | `{rel}` | {count:,} |"
        for (src, tgt, rel), count in top_module_pairs.most_common(120)
    )
    module_doc = f"""# AFSIM 模块依赖关系说明

> 状态：已生成
> 索引证据：`workspace/source-index/dependency-index.jsonl`
> 关联图：`docs/architecture/dependency-graph.md`

## 0. 文档说明

本文档按模块聚合 Phase5 依赖关系。正文展示出现频次最高的模块对；完整逐条依赖见 `workspace/source-index/dependency-index.jsonl`。

## 1. 分析边界

| 路径 | 处理方式 |
|---|---|
{excluded_table}

## 2. 模块依赖摘要

| 源模块 | 目标模块 | relation | 条目数 |
|---|---|---|---:|
{pair_rows}

## 3. 依赖强度说明

| 强度 | 含义 | 典型关系 |
|---|---|---|
| `strong` | 缺失通常导致编译、链接或核心运行路径失败 | build、inheritance、include、值类型 composition |
| `medium` | 运行时通常需要，但可能有默认值、空指针、策略替代或延迟绑定 | 指针 composition、关键 call |
| `weak` | 松耦合或场景性依赖，通常通过注册、配置、事件或可选功能触发 | registration、外部库调用 |

## 4. 完整清单入口

完整 JSONL 清单位于：

```text
workspace/source-index/dependency-index.jsonl
```
"""
    (docs / "module-dependency.md").write_text(module_doc, encoding="utf-8")


def validate_rows(rows: list[dict[str, Any]], excluded: list[str]) -> dict[str, Any]:
    relation_counts = collections.Counter(row["relation"] for row in rows)
    missing_relations = sorted(RELATIONS - set(relation_counts))
    low_relations = {rel: relation_counts[rel] for rel in RELATIONS if relation_counts[rel] < 5}
    missing_strength = sum(1 for row in rows if row.get("strength") not in {"strong", "medium", "weak"})
    boundary_hits = [
        row["dependency_id"]
        for row in rows
        if any(is_excluded(str(row.get(field) or ""), excluded) for field in ("source", "target", "path"))
    ]
    return {
        "row_count": len(rows),
        "relation_counts": dict(relation_counts),
        "missing_relations": missing_relations,
        "low_relations": low_relations,
        "missing_strength_count": missing_strength,
        "boundary_hit_count": len(boundary_hits),
        "boundary_hit_sample": boundary_hits[:20],
    }


def write_verify_report(root: Path, summary: dict[str, Any]) -> None:
    relation_rows = "\n".join(f"| `{rel}` | {count:,} |" for rel, count in sorted(summary["relation_counts"].items()))
    status = "通过" if not summary["missing_relations"] and not summary["low_relations"] and summary["row_count"] >= 200 and summary["boundary_hit_count"] == 0 else "需复核"
    report = f"""# Phase5 依赖关系验证报告

## 1. 总体结论

| 检查项 | 结果 |
|---|---|
| 总体状态 | {status} |
| dependency-index 条目数 ≥ 200 | {'通过' if summary['row_count'] >= 200 else '不通过'} |
| 覆盖 6 种 relation | {'通过' if not summary['missing_relations'] else '不通过'} |
| 每种 relation ≥ 5 | {'通过' if not summary['low_relations'] else '不通过'} |
| strength 字段覆盖 | {'通过' if summary['missing_strength_count'] == 0 else '不通过'} |
| 分析边界污染 | {'通过' if summary['boundary_hit_count'] == 0 else '不通过'} |

## 2. relation 分布

| relation | 条目数 |
|---|---:|
{relation_rows}

## 3. 输出文件

```text
workspace/source-index/dependency-index.jsonl
docs/architecture/dependency-graph.md
docs/architecture/module-dependency.md
```

## 4. 说明

Mermaid 图采用跨模块摘要展示，每条边在 `docs/architecture/dependency-graph.md` 的“Mermaid 边追溯矩阵”中记录 `dependency_id`，可回查 `workspace/source-index/dependency-index.jsonl`。
"""
    (root / "docs/verification/phase5-verify-report.md").write_text(report, encoding="utf-8")


def run(root: Path) -> dict[str, Any]:
    boundary = load_boundary(root)
    excluded = list(boundary.get("recommended_exclude_paths_for_architecture") or [])
    source_index = root / "workspace/source-index"
    files = read_jsonl(source_index / "file-index.jsonl")
    symbols = read_jsonl(source_index / "symbol-index.jsonl")
    functions = read_jsonl(source_index / "function-index.jsonl")

    rows: list[dict[str, Any]] = []
    rows.extend(build_dependencies(root, excluded))
    rows.extend(inheritance_dependencies(symbols, excluded))
    rows.extend(composition_dependencies(symbols, excluded))
    rows.extend(include_dependencies(files, excluded))
    rows.extend(call_dependencies(functions, excluded))
    rows.extend(registration_dependencies(root, excluded))
    rows = dedupe(rows)
    rows.sort(key=lambda row: (row["relation"], row["source_module"], row["target_module"], row["source"], row["target"]))

    write_jsonl(source_index / "dependency-index.jsonl", rows)
    write_dependency_docs(root, rows, excluded)
    summary = validate_rows(rows, excluded)
    summary.update(
        {
            "schema_version": "1",
            "phase": "phase5-dependencies",
            "status": "generated",
            "excluded_paths": excluded,
            "outputs": {
                "dependency_index": "workspace/source-index/dependency-index.jsonl",
                "dependency_graph": "docs/architecture/dependency-graph.md",
                "module_dependency": "docs/architecture/module-dependency.md",
                "verify_report": "docs/verification/phase5-verify-report.md",
            },
        }
    )
    (source_index / "phase5-dependency-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_verify_report(root, summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    print(json.dumps(run(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
