#!/usr/bin/env python3
"""Batch classify algorithm_hint using CodeGraph file-level source extraction.

Strategy: group unknown functions by file, read each file once via
`codegraph node --file`, then classify all functions in that file at once.
"""

import json
import subprocess
import os
import sys
from collections import Counter
from pathlib import Path

CODEGRAPH_NODE = os.path.expandvars(
    r"$HOME/codegraph-bundle/codegraph-win32-x64/node.exe"
)
CODEGRAPH_JS = os.path.expandvars(
    r"$HOME/codegraph-bundle/codegraph-win32-x64/lib/dist/bin/codegraph.js"
)
CG_WORKDIR = os.path.abspath(
    "E:/All_About_The_Code/VS Code repository/work_surrogatemodels/afsim-analysis-skill-project/source_root/afsim-2_9/swdev/src"
)
PROJ_ROOT = "E:/All_About_The_Code/VS Code repository/work_surrogatemodels/afsim-analysis-skill-project"

FUNC_INDEX = os.path.join(PROJ_ROOT, "workspace/source-index/function-index.jsonl")
OUTPUT_FIXES = os.path.join(PROJ_ROOT, "workspace/source-index/algorithm_hint_fixes.jsonl")
OUTPUT_AUDIT = os.path.join(PROJ_ROOT, "workspace/source-index/algorithm_hint_audit.jsonl")


def run_codegraph_file(filepath):
    """Read an entire file with codegraph."""
    try:
        result = subprocess.run(
            [CODEGRAPH_NODE, CODEGRAPH_JS, "node", "--file", filepath],
            cwd=CG_WORKDIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        return None


def extract_function_body(file_content, func_name, line_start, line_end):
    """Extract the body of a specific function from file content."""
    if not file_content or not line_start or not line_end:
        return None

    lines = file_content.split("\n")
    if line_start < 1:
        line_start = 1
    if line_end > len(lines):
        line_end = len(lines)

    # Get function lines (1-based to 0-based)
    func_lines = lines[line_start - 1:line_end]
    return "\n".join(func_lines)


def classify_function(func_name, body):
    """Classify a function based on its source code body."""
    if not body or len(body.strip()) < 10:
        return None  # Can't determine

    body_lower = body.lower()
    lines = [l for l in body.split("\n") if l.strip() and not l.strip().startswith("//") and not l.strip().startswith("/*") and not l.strip().startswith("*")]

    # Effective lines (not just braces)
    effective = [l for l in lines if l.strip() not in ["{", "}", ";"]]

    # --- Math indicators ---
    math_funcs = ["sin(", "cos(", "tan(", "sqrt(", "pow(", "exp(", "log(", "log10(",
                  "fabs(", "fmod(", "atan2(", "asin(", "acos(", "sinh(", "cosh(", "tanh(",
                  "abs(", "fmin(", "fmax(", "floor(", "ceil(", "round("]
    math_ops = ["matrix", "vector", "cross(", "dot(", "norm(", "determinant", "transpose",
                "inverse", "quaternion", "euler", "rotation", "eigen", "jacobian",
                "integrate", "rk4", "runge", "interpolat", "extrapolat",
                "newton", "gradient", "hessian", "least_squares", "bisection",
                "gauss", "lu_decompos", "cholesky", "singular_value",
                "convolution", "fft", "ifft", "kalman", "pid_",
                "kinematic", "dynamics", "trajectory", "orbit", "propagat",
                "aero", "thrust", "drag", "lift", "gravity", "acceleration",
                "velocity", "attitude", "angular", "torque", "momentum",
                "latitud", "longitud", "altitud", "azimuth", "elevat",
                "geodetic", "ecef", "ned", "enu", "wgs84",
                "noise", "random", "gaussian", "monte_carlo", "distribution",
                "polynomial", "spline", "taylor", "fourier"]

    math_score = 0
    for kw in math_funcs:
        math_score += body_lower.count(kw)
    for kw in math_ops:
        if kw in body_lower:
            math_score += 3  # higher weight for concept keywords

    # Compound assignment with math ops
    for op in ["+=", "-=", "*=", "/="]:
        math_score += body_lower.count(op) * 0.5

    # --- Factory indicators ---
    factory_kws = ["factory", "create", "make_shared", "make_unique", "new ",
                   "getinstance", "singleton", "register_type", "register_class",
                   "clone(", "instantiate", "allocate"]
    factory_score = sum(1 for kw in factory_kws if kw in body_lower)

    # --- IO indicators ---
    io_kws = ["fopen", "fread", "fwrite", "fprintf", "fclose", "fscanf",
              "ifstream", "ofstream", "fstream", "iostream",
              "serialize", "deserialize", "marshal", "unmarshal",
              "json", "xml", "protobuf", "yaml",
              "socket", "recv", "send", "bind(", "connect(", "listen(",
              "read(", "write(", "seek(", "tell(",
              "log(", "logger", "logging", "print", "cout", "cin", "cerr",
              "encode", "decode", "base64", "hex_"]
    io_score = sum(1 for kw in io_kws if kw in body_lower)

    # --- Control flow indicators ---
    cf_kws = ["switch", "case ", "state_machine", "fsm", "behavior_tree",
              "decision", "dispatch", "transition", "finite_state",
              "if (", "else if", "foreach", "callback",
              "notify(", "emit(", "signal(", "trigger("]
    cf_score = sum(1 for kw in cf_kws if kw in body_lower)
    # Count switch cases as strong signal
    cf_score += body_lower.count("case ") * 2

    # --- State update indicators ---
    state_kws = ["->set", "->update", ".set_", "set_", "update_",
                 "m_", "_state", ".state", "status_", "mode_",
                 " = true", " = false", "enable", "disable",
                 "activate", "deactivate", "toggle",
                 "reset(", "clear(", "initialize("]
    state_score = sum(1 for kw in state_kws if kw in body_lower)
    # Check for member variable access patterns
    state_score += body_lower.count("->") * 0.5

    # --- Routing indicators ---
    routing_kws = ["path", "route", "waypoint", "graph", "dijkstra", "a_star",
                   "shortest_path", "adjacent", "neighbor", "edge", "vertex",
                   "floyd", "warshall", "bellman", "traverse"]
    routing_score = sum(1 for kw in routing_kws if kw in body_lower)

    # --- Configuration indicators ---
    config_kws = ["config", "parameter", "option", "setting", "property",
                  "parse_xml", "parse_json", "parse_yaml", "parse_ini",
                  "from_string", "from_file", "deserialize_config",
                  "set_parameter", "get_parameter", "set_option"]
    config_score = sum(1 for kw in config_kws if kw in body_lower)

    # --- Trivial check ---
    if len(effective) <= 3 and math_score < 1.5:
        # Check if it's truly trivial (getter/setter/empty)
        trivial_patterns = ["return ", " = ", "delete ", "free("]
        if any(p in body_lower for p in ["return m_", "return _", " = m_", " = _"]):
            return "none"
        if len(effective) <= 2:
            return "none"

    # --- Decision ---
    scores = {
        "math": math_score,
        "factory": factory_score,
        "io": io_score,
        "control_flow": cf_score,
        "state_update": state_score,
        "routing": routing_score,
        "configuration": config_score,
    }

    # Filter categories with meaningful scores
    candidates = [(cat, s) for cat, s in scores.items() if s >= 1.0]
    if not candidates:
        return None

    # Sort by score descending
    candidates.sort(key=lambda x: x[1], reverse=True)
    best_cat, best_score = candidates[0]

    # Only classify if we have a clear signal
    if best_score >= 2.0:
        # If math and state are both high but math is clearly dominant
        if best_cat == "math" and best_score >= 3.0:
            return "math"
        # If two categories tie closely, prefer the more specific one
        if len(candidates) >= 2 and candidates[1][1] > best_score * 0.7:
            return None  # Too ambiguous
        return best_cat

    return None


def main():
    os.chdir(PROJ_ROOT)

    # Load function index
    print("Loading function-index.jsonl...")
    with open(FUNC_INDEX, "r", encoding="utf-8") as f:
        entries = [json.loads(line) for line in f if line.strip()]

    method_level = [e for e in entries if e.get("level") == "Method-level"]
    unknowns = [e for e in method_level if e.get("algorithm_hint") == "unknown"]
    classified = [e for e in method_level if e.get("algorithm_hint") not in ("unknown",)]

    print(f"Total method-level: {len(method_level)}")
    print(f"Unknown: {len(unknowns)}")
    print(f"Classified (target for audit): {len(classified)}")

    # Group unknowns by file (remove path prefix if any)
    file_groups = {}
    for e in unknowns:
        fp = e.get("path", "")
        if not fp:
            continue
        if fp not in file_groups:
            file_groups[fp] = []
        file_groups[fp].append(e)

    print(f"Unique files with unknowns: {len(file_groups)}")

    # Process target files (prioritize files with most unknowns)
    start_offset = 600
    target_count = min(start_offset + 300, len(file_groups))  # 300 more files   # Skip first N files already processed in previous run
    target_count = min(start_offset + 200, len(file_groups))
    top_files = sorted(file_groups.items(), key=lambda x: len(x[1]), reverse=True)[start_offset:target_count]

    total_funcs = sum(len(grp) for _, grp in top_files)
    print(f"Processing top {len(top_files)} files covering {total_funcs} unknown functions\n")

    # --- Step 1: Classify unknowns ---
    print("=" * 60)
    print("STEP 1: Classifying unknown functions")
    print("=" * 60)

    fixes = []
    processed_files = 0
    processed_funcs = 0

    with open(OUTPUT_FIXES, "w", encoding="utf-8") as out_f:
        for i, (fp, funcs) in enumerate(top_files):
            processed_files += 1
            if (i + 1) % 20 == 0:
                print(f"  [{i+1}/{len(top_files)}] files, {processed_funcs} funcs processed, {len(fixes)} classified")

            # Resolve relative path to absolute for codegraph
            # Function index stores paths like "afsim-2_9/swdev/src/core/..."
            # CodeGraph works relative to swdev/src
            rel_path = fp
            prefix = "afsim-2_9/swdev/src/"
            if rel_path.startswith(prefix):
                rel_path = rel_path[len(prefix):]

            file_content = run_codegraph_file(rel_path)
            if not file_content:
                continue

            for func in funcs:
                processed_funcs += 1
                body = extract_function_body(
                    file_content,
                    func.get("function_name", ""),
                    func.get("line_start"),
                    func.get("line_end"),
                )
                if not body:
                    continue

                hint = classify_function(func.get("function_name", ""), body)
                if hint:
                    result = {
                        "qualified_name": func["qualified_name"],
                        "function_name": func.get("function_name", ""),
                        "path": func.get("path", ""),
                        "old_hint": "unknown",
                        "new_hint": hint,
                    }
                    fixes.append(result)
                    out_f.write(json.dumps(result, ensure_ascii=False) + "\n")
                    out_f.flush()

    print(f"\n  Processed {processed_files} files, {processed_funcs} functions")
    print(f"  Successfully classified: {len(fixes)}")

    # Distribution
    hint_dist = Counter(f["new_hint"] for f in fixes)
    print("\n  Classification distribution:")
    for k, v in hint_dist.most_common():
        print(f"    {k:20s}: {v:5d}")

    # --- Step 2: Audit existing classifications ---
    print(f"\n{'='*60}")
    print("STEP 2: Auditing existing classifications")
    print("=" * 60)

    import random
    random.seed(42)

    # Group classified functions by file too
    classified_by_file = {}
    for e in classified:
        fp = e.get("path", "")
        if not fp:
            continue
        if fp not in classified_by_file:
            classified_by_file[fp] = []
        classified_by_file[fp].append(e)

    # Prioritize files with most functions
    audit_files = sorted(classified_by_file.items(), key=lambda x: len(x[1]), reverse=True)[:100]
    audit_funcs_total = sum(len(grp) for _, grp in audit_files)
    print(f"Auditing {len(audit_files)} files covering ~{audit_funcs_total} classified functions\n")

    mistakes = []
    audited_count = 0

    with open(OUTPUT_AUDIT, "w", encoding="utf-8") as out_f:
        for i, (fp, funcs) in enumerate(audit_files):
            if (i + 1) % 20 == 0:
                print(f"  [{i+1}/{len(audit_files)}] files, {audited_count} funcs audited, {len(mistakes)} mistakes")

            prefix = "afsim-2_9/swdev/src/"
            rel_path = fp[len(prefix):] if fp.startswith(prefix) else fp

            file_content = run_codegraph_file(rel_path)
            if not file_content:
                continue

            for func in funcs:
                audited_count += 1
                body = extract_function_body(
                    file_content,
                    func.get("function_name", ""),
                    func.get("line_start"),
                    func.get("line_end"),
                )
                if not body:
                    continue

                suggested = classify_function(func.get("function_name", ""), body)
                current = func.get("algorithm_hint", "")

                if suggested and suggested != current:
                    mistake = {
                        "qualified_name": func["qualified_name"],
                        "function_name": func.get("function_name", ""),
                        "path": func.get("path", ""),
                        "current_hint": current,
                        "suggested_hint": suggested,
                    }
                    mistakes.append(mistake)
                    out_f.write(json.dumps(mistake, ensure_ascii=False) + "\n")
                    out_f.flush()

    print(f"\n  Audited: {audited_count} functions")
    print(f"  Potential misclassifications: {len(mistakes)}")

    if mistakes:
        mistake_dist = Counter(f"{m['current_hint']}->{m['suggested_hint']}" for m in mistakes)
        print("\n  Mistake distribution:")
        for k, v in mistake_dist.most_common(20):
            print(f"    {k:30s}: {v}")

    # --- Summary ---
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Unknowns processed    : {processed_funcs}")
    print(f"  Successfully classified: {len(fixes)}")
    print(f"  Classification rate   : {len(fixes)/processed_funcs*100:.1f}%" if processed_funcs > 0 else "  N/A")
    print(f"  Existing audited      : {audited_count}")
    print(f"  Potential misclass    : {len(mistakes)}")
    print(f"  Misclassification rate: {len(mistakes)/audited_count*100:.1f}%" if audited_count > 0 else "  N/A")
    print(f"\n  Fixes saved to : {OUTPUT_FIXES}")
    print(f"  Audit saved to : {OUTPUT_AUDIT}")

    # Apply fixes to function-index.jsonl
    if fixes:
        print(f"\nApplying {len(fixes)} fixes to function-index.jsonl...")
        fix_map = {f["qualified_name"]: f["new_hint"] for f in fixes}

        updated_count = 0
        for entry in entries:
            qname = entry.get("qualified_name", "")
            if qname in fix_map:
                entry["algorithm_hint"] = fix_map[qname]
                updated_count += 1

        # Write back
        backup_path = FUNC_INDEX + ".bak"
        import shutil
        shutil.copy2(FUNC_INDEX, backup_path)

        with open(FUNC_INDEX, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        print(f"  Updated {updated_count} entries")
        print(f"  Backup saved to: {backup_path}")


if __name__ == "__main__":
    main()
