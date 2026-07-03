#!/usr/bin/env python3
"""Comprehensive validation of function-index.jsonl (excluding algorithm_hint)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import re
from collections import Counter, defaultdict

FUNC_INDEX = "workspace/source-index/function-index.jsonl"

with open(FUNC_INDEX, "r", encoding="utf-8") as f:
    entries = [json.loads(line) for line in f if line.strip()]

# ── Split by level ──
system_level = [e for e in entries if e.get("level") == "System-level"]
module_level = [e for e in entries if e.get("level") == "Module-level"]
class_level  = [e for e in entries if e.get("level") == "Class-level"]
method_level = [e for e in entries if e.get("level") == "Method-level"]
print(f"Total entries: {len(entries)}")
print(f"  System-level : {len(system_level)}")
print(f"  Module-level : {len(module_level)}")
print(f"  Class-level  : {len(class_level)}")
print(f"  Method-level : {len(method_level)}")

issues = []

def issue(sev, cat, qname, detail):
    issues.append({"severity": sev, "category": cat, "qualified_name": qname, "detail": detail})

# ══════════════════════════════════════════════════════════
# CHECK 0: schema_version
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 0: schema_version ━━━")
bad_schema = [e for e in entries if str(e.get("schema_version")) != "1"]
if bad_schema:
    print(f"  {len(bad_schema)} entries with schema_version != 1")
    for e in bad_schema[:5]:
        print(f"    {e['qualified_name']}: schema_version={e.get('schema_version')}")
        issue("ERR", "schema_version", e["qualified_name"], f"schema_version={e.get('schema_version')}")
else:
    print("  ✅ All schema_version == 1")

# ══════════════════════════════════════════════════════════
# CHECK 1: qualified_name uniqueness & validity
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 1: qualified_name ━━━")
qnames = [e.get("qualified_name", "") for e in entries]
qname_counts = Counter(qnames)
dupes = {k: v for k, v in qname_counts.items() if v > 1}
if dupes:
    print(f"  {len(dupes)} duplicate qualified_names (total {sum(dupes.values())} entries):")
    for qn, cnt in sorted(dupes.items(), key=lambda x: -x[1])[:10]:
        print(f"    {qn}: {cnt}x")
        issue("ERR", "duplicate_qname", qn, f"appears {cnt} times")
else:
    print("  ✅ All qualified_names unique")

empty_qnames = [e for e in entries if not e.get("qualified_name", "").strip()]
if empty_qnames:
    issue("ERR", "empty_qname", "N/A", f"{len(empty_qnames)} entries with empty qualified_name")

# Bad qname patterns from prior fix record
bad_qname = 0
for e in entries:
    qn = e.get("qualified_name", "")
    # Check for known bad patterns: obj.method() mislabeled
    if any(p in qn for p in ["->", "(", ")", "throw ", "emit ", "std::", "return ", "= "]):
        bad_qname += 1
if bad_qname:
    print(f"  ⚠ {bad_qname} entries with suspicious qualified_name patterns")
    issue("WARN", "suspicious_qname", "N/A", f"{bad_qname} entries with suspicious qualified_name")
else:
    print("  ✅ No suspicious qualified_name patterns")

# ══════════════════════════════════════════════════════════
# CHECK 2: Method-level required fields
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 2: Method-level required fields ━━━")

method_req_fields = {
    "function_name": "str",
    "qualified_name": "str",
    "level": "str",
    "brief": "str",
    "path": "str",
    "return_type": "str",
    "parameters": "list",
    "calls": "list",
    "reads": "list",
    "writes": "list",
    "lifecycle_role": "str",
    "dependencies": "list",
    "is_virtual": "bool",
    "is_override": "bool",
    "is_const": "bool",
    "is_static": "bool",
    "access_modifier": "str_or_null",
    "embedding": "null_or_other",
    "evidence_level": "str",
    "notes": "list",
}

field_missing = Counter()
field_bad_type = Counter()
for e in method_level:
    for fname, ftype in method_req_fields.items():
        val = e.get(fname)
        if val is None:
            field_missing[fname] += 1
        elif ftype == "list":
            if not isinstance(val, list):
                field_bad_type[fname] += 1
        elif ftype == "bool":
            if not isinstance(val, bool):
                field_bad_type[fname] += 1

if field_missing:
    print("  Missing fields:")
    for k, v in field_missing.most_common():
        print(f"    {k}: {v}")
        issue("ERR", "missing_field", f"Method-level::{k}", f"{v} entries missing {k}")
else:
    print("  ✅ No missing required fields")

if field_bad_type:
    print("  Wrong type fields:")
    for k, v in field_bad_type.most_common():
        print(f"    {k}: {v}")
        issue("ERR", "bad_field_type", f"Method-level::{k}", f"{v} entries with wrong type for {k}")

# ══════════════════════════════════════════════════════════
# CHECK 3: return_type quality
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 3: return_type quality ━━━")
# static prefix
static_rt = [e for e in method_level if e.get("return_type","").lstrip().startswith("static ")]
if static_rt:
    print(f"  ⚠ {len(static_rt)} entries with 'static ' in return_type")
    issue("WARN", "static_in_return_type", "N/A", f"{len(static_rt)} entries")
else:
    print("  ✅ No 'static ' in return_type")

# constructor/destructor with non-empty return_type
ctor_rt = [e for e in method_level if e.get("function_name","") == e.get("qualified_name","").split("::")[-1] or
           e.get("function_name","").startswith("~")]
ctor_bad = [e for e in ctor_rt if e.get("return_type","").strip() not in ("", "unknown")]
if ctor_bad:
    print(f"  ⚠ {len(ctor_bad)} constructors/destructors with non-empty return_type")
    issue("WARN", "ctor_return_type", "N/A", f"{len(ctor_bad)} ctors/dtors with non-empty return_type")
else:
    print("  ✅ Constructor/destructor return_type OK")

# bad chars in return_type
rt_bad = [e for e in method_level if any(c in e.get("return_type","") for c in ["{", "}", "(", ":", ",", ";"])]
if rt_bad:
    print(f"  ⚠ {len(rt_bad)} entries with suspicious chars in return_type")
    issue("WARN", "bad_return_type_chars", "N/A", f"{len(rt_bad)} entries with bad chars in return_type")
else:
    print("  ✅ No suspicious chars in return_type")

# ══════════════════════════════════════════════════════════
# CHECK 4: brief quality
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 4: brief quality ━━━")
# Empty brief
empty_brief = [e for e in entries if not e.get("brief","").strip()]
if empty_brief:
    print(f"  ⚠ {len(empty_brief)} entries with empty brief")
    issue("WARN", "empty_brief", "N/A", f"{len(empty_brief)} entries with empty brief")
else:
    print("  ✅ No empty briefs")

# method: pattern (from prior fix)
bad_brief_method = [e for e in method_level if re.match(r'^method:\s', e.get("brief",""))]
if bad_brief_method:
    print(f"  ⚠ {len(bad_brief_method)} entries with 'method: ' brief pattern")
    issue("WARN", "brief_method_prefix", "N/A", f"{len(bad_brief_method)} entries")
else:
    print("  ✅ No 'method: ' brief pattern")

# member variable mislabel (brief looks like a member var)
var_brief = [e for e in method_level if re.match(r'^member variable|^m[A-Z]\w*:|^variable', e.get("brief",""))]
if var_brief:
    print(f"  ⚠ {len(var_brief)} entries with brief suggesting member variable")
    issue("WARN", "member_var_mislabel", "N/A", f"{len(var_brief)} entries with variable-like brief")
else:
    print("  ✅ No variable-like briefs")

# ══════════════════════════════════════════════════════════
# CHECK 5: line_start / line_end
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 5: line_start / line_end ━━━")
no_lines = [e for e in method_level if not e.get("line_start") or not e.get("line_end")]
if no_lines:
    print(f"  ⚠ {len(no_lines)} entries with null/missing line_start or line_end")
    issue("WARN", "missing_line_range", "N/A", f"{len(no_lines)} entries")
else:
    print("  ✅ All entries have line ranges")

# span > 20 (from prior fix)
wide_span = [e for e in method_level if e.get("line_start") and e.get("line_end") and
             (e["line_end"] - e["line_start"] > 20)]
if wide_span:
    print(f"  ⚠ {len(wide_span)} entries with line span > 20")
    # Sample
    for e in wide_span[:5]:
        print(f"    {e['qualified_name']}: L{e['line_start']}-L{e['line_end']} (span={e['line_end']-e['line_start']})")
    issue("WARN", "wide_line_span", "N/A", f"{len(wide_span)} entries with span > 20")
else:
    print("  ✅ All line spans ≤ 20")

# line_end < line_start
reversed_lines = [e for e in method_level if e.get("line_start") and e.get("line_end") and
                  e["line_end"] < e["line_start"]]
if reversed_lines:
    print(f"  ⚠ {len(reversed_lines)} entries with line_end < line_start")
    issue("ERR", "reversed_line_range", "N/A", f"{len(reversed_lines)} entries")
else:
    print("  ✅ No reversed line ranges")

# ══════════════════════════════════════════════════════════
# CHECK 5b: line_start too small (≤2) — likely wrong
# ══════════════════════════════════════════════════════════
small_line = [e for e in method_level if e.get("line_start") and e["line_start"] <= 2]
if small_line:
    print(f"  ⚠ {len(small_line)} entries with line_start <= 2 (likely wrong)")
    issue("WARN", "suspicious_line_start", "N/A", f"{len(small_line)} entries with line_start <= 2")
else:
    print("  ✅ No entries with line_start <= 2")

# ══════════════════════════════════════════════════════════
# CHECK 6: lifecycle_role values
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 6: lifecycle_role ━━━")
valid_lr = {"entry", "scenario_load", "object_create", "simulation_loop", "model_update",
            "event_handling", "output", "shutdown", "utility", "unknown"}
lr_counts = Counter(e.get("lifecycle_role","") for e in method_level)
bad_lr = {k: v for k, v in lr_counts.items() if k not in valid_lr}
if bad_lr:
    print(f"  ⚠ Invalid lifecycle_role values:")
    for k, v in bad_lr.items():
        print(f"    '{k}': {v}")
        issue("WARN", "invalid_lifecycle_role", "N/A", f"'{k}'={v}")
else:
    print("  ✅ All lifecycle_role values valid")
print(f"  Distribution:")
for k, v in lr_counts.most_common():
    print(f"    {k:25s}: {v:6d}")

# ══════════════════════════════════════════════════════════
# CHECK 7: parameters structure
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 7: parameters structure ━━━")
bad_params = []
for e in method_level:
    params = e.get("parameters", [])
    if not isinstance(params, list):
        bad_params.append(("not_list", e["qualified_name"]))
        continue
    for p in params:
        if not isinstance(p, dict):
            bad_params.append(("not_dict", e["qualified_name"]))
            continue
        for k in ["name", "type", "desc", "input_output", "default_value", "valid_range"]:
            if k not in p:
                bad_params.append((f"missing_{k}", e["qualified_name"]))
if bad_params:
    print(f"  ⚠ {len(bad_params)} parameter structure issues (first 10):")
    for t, qn in bad_params[:10]:
        print(f"    {qn}: {t}")
    issue("WARN", "bad_parameters", "N/A", f"{len(bad_params)} parameter structure issues")
else:
    print("  ✅ All parameters well-formed")

# ══════════════════════════════════════════════════════════
# CHECK 8: Class-level required fields
# ══════════════════════════════════════════════════════════
print(f"\n━━━ CHECK 8: Class-level fields ({len(class_level)} entries) ━━━")

# function_name should be short (last :: segment)
bad_fn = [e for e in class_level if "::" in e.get("function_name","")]
if bad_fn:
    print(f"  ⚠ {len(bad_fn)} Class-level entries with long function_name (contains '::')")
    issue("WARN", "class_long_function_name", "N/A", f"{len(bad_fn)} entries")
else:
    print("  ✅ All Class-level function_names are short")

# brief non-empty
empty_class_brief = [e for e in class_level if not e.get("brief","").strip()]
if empty_class_brief:
    print(f"  ⚠ {len(empty_class_brief)} with empty brief")
    issue("WARN", "class_empty_brief", "N/A", f"{len(empty_class_brief)} entries")
else:
    print("  ✅ All Class-level briefs non-empty")

# sub_functions non-empty
empty_sub = [e for e in class_level if not e.get("sub_functions")]
if empty_sub:
    print(f"  ⚠ {len(empty_sub)} with empty sub_functions (candidates for deletion)")
    issue("WARN", "class_empty_sub_functions", "N/A", f"{len(empty_sub)} entries")
else:
    print("  ✅ All Class-level sub_functions non-empty")

# path filled
no_class_path = [e for e in class_level if not e.get("path")]
if no_class_path:
    print(f"  ⚠ {len(no_class_path)} without path")
    issue("WARN", "class_no_path", "N/A", f"{len(no_class_path)} entries")
else:
    print("  ✅ All Class-level paths filled")

# evidence_level non-empty
no_cl_ev = [e for e in class_level if not e.get("evidence_level")]
if no_cl_ev:
    print(f"  ⚠ {len(no_cl_ev)} without evidence_level")
else:
    print("  ✅ All evidence levels present")

# ══════════════════════════════════════════════════════════
# CHECK 9: System/Module-level fields
# ══════════════════════════════════════════════════════════
sm_level = system_level + module_level
print(f"\n━━━ CHECK 9: System/Module-level ({len(sm_level)} entries) ━━━")
empty_sm_brief = [e for e in sm_level if not e.get("brief","").strip()]
if empty_sm_brief:
    print(f"  ⚠ {len(empty_sm_brief)} with empty brief")
    issue("WARN", "sys_empty_brief", "N/A", f"{len(empty_sm_brief)} entries")
else:
    print("  ✅ All System/Module briefs non-empty")

empty_sm_sub = [e for e in sm_level if not e.get("sub_functions")]
if empty_sm_sub:
    print(f"  ⚠ {len(empty_sm_sub)} with empty sub_functions")
    issue("WARN", "sys_empty_sub_functions", "N/A", f"{len(empty_sm_sub)} entries")
else:
    print("  ✅ All System/Module sub_functions non-empty")

# ══════════════════════════════════════════════════════════
# CHECK 10: Dead references (sub_functions pointing to non-existent entries)
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 10: Dead references ━━━")
all_qnames_set = set(qnames)
dead_refs = Counter()
dead_by_parent = defaultdict(list)
for e in entries:
    subs = e.get("sub_functions", [])
    for sub in subs:
        if sub not in all_qnames_set:
            dead_refs[sub] += 1
            dead_by_parent[e["qualified_name"]].append(sub)

if dead_refs:
    print(f"  ⚠ {len(dead_refs)} dead references ({sum(dead_refs.values())} total)")
    print(f"  Parents with dead refs: {len(dead_by_parent)}")
    for parent, dead in sorted(dead_by_parent.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"    {parent}: {len(dead)} dead refs")
    issue("WARN", "dead_references", "N/A",
          f"{len(dead_refs)} dead refs from {len(dead_by_parent)} parents")
else:
    print("  ✅ All sub_functions references valid")

# ══════════════════════════════════════════════════════════
# CHECK 11: Duplicate sub_functions arrays
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 11: Duplicate sub_functions ━━━")
dup_subs = 0
for e in entries:
    subs = e.get("sub_functions", [])
    if len(subs) != len(set(subs)):
        dup_subs += 1
if dup_subs:
    print(f"  ⚠ {dup_subs} entries with duplicate sub_functions entries")
    issue("WARN", "duplicate_sub_functions", "N/A", f"{dup_subs} entries")
else:
    print("  ✅ No duplicate sub_functions")

# ══════════════════════════════════════════════════════════
# CHECK 12: evidence_level values
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 12: evidence_level ━━━")
valid_el = {"source-cited", "document-cited", "index-derived", "inferred", "unknown"}
el_counts = Counter(e.get("evidence_level","") for e in entries)
bad_el = {k: v for k, v in el_counts.items() if k not in valid_el}
if bad_el:
    print(f"  ⚠ Invalid evidence_level values:")
    for k, v in bad_el.items():
        print(f"    '{k}': {v}")
        issue("WARN", "invalid_evidence_level", "N/A", f"'{k}'={v}")
else:
    print("  ✅ All evidence_level values valid")
print(f"  Distribution:")
for k, v in el_counts.most_common():
    print(f"    {k:25s}: {v:6d}")

# ══════════════════════════════════════════════════════════
# CHECK 13: access_modifier (Method-level only)
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 13: access_modifier ━━━")
valid_am = {"public", "protected", "private", "null", None}
am_counts = Counter(str(e.get("access_modifier","")) for e in method_level)
bad_am = {k: v for k, v in am_counts.items() if k not in {"public", "protected", "private", "None"}}
if bad_am:
    print(f"  ⚠ Unexpected access_modifier values:")
    for k, v in bad_am.items():
        print(f"    '{k}': {v}")
else:
    print("  ✅ All access_modifier values valid")
print(f"  Distribution: public={am_counts.get('public',0)} protected={am_counts.get('protected',0)} "
      f"private={am_counts.get('private',0)} None/other={am_counts.get('None',0)}")

# ══════════════════════════════════════════════════════════
# CHECK 14: notes is always a list
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 14: notes field ━━━")
bad_notes = [e for e in entries if not isinstance(e.get("notes"), list)]
if bad_notes:
    print(f"  ⚠ {len(bad_notes)} entries with non-list notes")
    issue("ERR", "notes_not_list", "N/A", f"{len(bad_notes)} entries")
else:
    print("  ✅ All notes are lists")

# ══════════════════════════════════════════════════════════
# CHECK 15: calls consistency (calls entries vs dependencies)
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 15: calls field consistency ━━━")
empty_calls_deps = 0
for e in method_level:
    calls = e.get("calls", [])
    deps = e.get("dependencies", [])
    if isinstance(calls, list) and len(calls) > 0 and isinstance(deps, list) and len(deps) == 0:
        empty_calls_deps += 1
if empty_calls_deps:
    print(f"  ⚠ {empty_calls_deps} entries with non-empty calls but empty dependencies")
    # This is actually common and expected — calls is statically visible, deps may be broader
else:
    print("  ✅ calls/dependencies field consistency OK")

# ══════════════════════════════════════════════════════════
# CHECK 16: function_name patterns - internal consistency
# ══════════════════════════════════════════════════════════
print("\n━━━ CHECK 16: function_name vs qualified_name consistency ━━━")
name_mismatch = 0
for e in method_level:
    fn = e.get("function_name","")
    qn = e.get("qualified_name","")
    if qn and fn and "::" in qn:
        if not qn.endswith("::" + fn):
            name_mismatch += 1
if name_mismatch:
    print(f"  ⚠ {name_mismatch} entries where function_name != last segment of qualified_name")
    # Sample
    for e in method_level:
        fn = e.get("function_name","")
        qn = e.get("qualified_name","")
        if qn and fn and "::" in qn and not qn.endswith("::" + fn):
            if name_mismatch <= 10 or len(fn) > 20:  # long ones are likely templates
                print(f"    {qn}  →  function_name='{fn}'")
            if name_mismatch > 10:
                break
    issue("WARN", "fn_qn_mismatch", "N/A", f"{name_mismatch} entries with fn/qn mismatch")
else:
    print("  ✅ All function_names match qualified_name suffix")

# ══════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("VALIDATION SUMMARY")
print(f"{'='*60}")

errors = [i for i in issues if i["severity"] == "ERR"]
warnings = [i for i in issues if i["severity"] == "WARN"]

print(f"\n  ❌ ERRORS   : {len(errors)}")
for i in errors:
    print(f"     [{i['category']}] {i['detail']}")

print(f"\n  ⚠ WARNINGS : {len(warnings)}")
for i in warnings:
    print(f"     [{i['category']}] {i['detail']}")

if not errors and not warnings:
    print("  ✅ function-index.jsonl passed all checks clean!")
elif not errors:
    print("\n  → No errors, only warnings. File is functionally clean.")

# Print counts per category
print(f"\n  Issue categories:")
cat_counts = Counter(i["category"] for i in issues)
for cat, cnt in cat_counts.most_common():
    print(f"    {cat:35s}: {cnt}")
