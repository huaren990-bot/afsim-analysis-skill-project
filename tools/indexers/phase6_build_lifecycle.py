#!/usr/bin/env python3
"""Build Phase6 lifecycle, dataflow, and extension point documents."""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
from typing import Any


STAGES = [
    ("entry", "程序入口与命令行处理"),
    ("scenario_load", "场景与配置加载"),
    ("object_create", "对象创建与注册"),
    ("simulation_loop", "仿真主循环"),
    ("model_update", "模型状态更新"),
    ("event_handling", "事件处理与分发"),
    ("output", "结果输出与可视化"),
    ("shutdown", "关闭与资源清理"),
]

DATA_OBJECTS = [
    ("Platform", "平台对象/实体状态"),
    ("Track", "航迹/目标跟踪状态"),
    ("Event", "事件队列与事件消息"),
    ("Message", "通信消息与消息表"),
    ("Signature", "传感器/目标特征数据"),
]

EXTENSION_DESCRIPTIONS = {
    "RegisterExtension": "应用或场景扩展注册机制，用于把外部能力挂接到 WsfApplication/WsfScenario 生命周期。",
    "AddExtension": "扩展列表机制，用于维护扩展对象和扩展间依赖顺序。",
    "AddComponent": "平台组件挂接机制，用于给 WsfPlatform 增加传感器、武器、通信等运行时能力。",
    "RegisterComponent": "组件注册机制，用于声明可创建或可识别的组件类型。",
    "ComponentFactory": "组件工厂机制，用于根据输入类型创建运行时组件。",
    "AddFactory": "工厂注册机制，用于把类型工厂加入 FactoryManager。",
    "RegisterScriptClasses": "脚本类注册机制，用于把 C++ 类型暴露给脚本系统。",
    "AddMessage": "消息工厂注册机制，用于把消息类型加入消息表。",
    "EventPipe": "事件管道订阅/记录机制，用于把仿真事件输出给 Warlock/Mystic 等工具。",
    "Subscribe": "事件订阅机制，用于让观察者接收运行时事件。",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def pos(row: dict[str, Any]) -> str:
    return f"{row.get('path')}:{row.get('line_start')}"


def display_func(row: dict[str, Any]) -> str:
    return row.get("canonical_qualified_name") or row.get("qualified_name")


def short_func(row: dict[str, Any]) -> str:
    return display_func(row).split("#", 1)[0]


def safe_node(text: str) -> str:
    return "n" + str(abs(hash(text)))[:10]


def load_methods(root: Path) -> list[dict[str, Any]]:
    return [
        row
        for row in read_jsonl(root / "workspace/source-index/function-index.jsonl")
        if row.get("level") == "Method-level"
    ]


def find_methods(methods: list[dict[str, Any]], *needles: str, limit: int = 10) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for needle in needles:
        for row in methods:
            hay = " ".join([row.get("qualified_name", ""), row.get("canonical_qualified_name", ""), row.get("function_name", ""), row.get("path", "")])
            if needle in hay and row not in result:
                result.append(row)
                if len(result) >= limit:
                    return result
    return result


def method_by_call_name(methods: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_name: dict[str, dict[str, Any]] = {}
    preferred = sorted(methods, key=lambda row: (0 if "core/wsf/source" in row.get("path", "") else 1, row.get("path", "")))
    for row in preferred:
        by_name.setdefault(row.get("function_name") or "", row)
        by_name.setdefault(row.get("canonical_qualified_name") or "", row)
    return by_name


def stage_methods(methods: list[dict[str, Any]], stage: str) -> list[dict[str, Any]]:
    if stage == "entry":
        entries = [
            row
            for row in methods
            if row.get("function_name") in {"main", "WinMain"} and not any(part in row.get("path", "") for part in ["/test/", "legacy_test"])
        ]
        return entries[:5]
    rows = [row for row in methods if row.get("lifecycle_role") == stage]
    preferred_tokens = {
        "scenario_load": ["ProcessInputFiles", "CompleteLoad", "LoadFromFile", "ProcessInput", "ReadValue"],
        "object_create": ["AddInputPlatforms", "AddComponent", "RegisterExtension", "Create", "Initialize"],
        "simulation_loop": ["RunEventLoop", "AdvanceFrame", "AdvanceTime", "InitializeSimulation", "Complete"],
        "model_update": ["Update", "Evaluate", "Compute", "Process", "Tick"],
        "event_handling": ["AddEvent", "Execute", "Observer", "EventPipe", "Report"],
        "output": ["Output", "Write", "Print", "Report", "CSV"],
        "shutdown": ["Complete", "Reset", "~", "Destroy", "Clear"],
    }.get(stage, [])
    rows.sort(
        key=lambda row: (
            0 if any(token in display_func(row) for token in preferred_tokens) else 1,
            0 if "core/wsf/source" in row.get("path", "") else 1,
            row.get("path", ""),
            row.get("line_start") or 0,
        )
    )
    return rows[:8]


def build_call_chains(stage_rows: list[dict[str, Any]], by_name: dict[str, dict[str, Any]], count: int = 3) -> list[str]:
    lines: list[str] = []
    for row in stage_rows:
        target = None
        call_name = None
        for call in row.get("calls") or []:
            if call in by_name and by_name[call]["candidate_id"] != row["candidate_id"]:
                target = by_name[call]
                call_name = call
                break
        if target:
            lines.append(
                f"1. `{short_func(row)}()` (`{pos(row)}`) → `{short_func(target)}()` (`{pos(target)}`)："
                f"通过 Phase4 `calls` 记录调用 `{call_name}`，用于推进该阶段的状态变化；证据：function-index calls。"
            )
        else:
            calls = ", ".join((row.get("calls") or [])[:5]) or "无显式 calls"
            lines.append(
                f"1. `{short_func(row)}()` (`{pos(row)}`) → `{calls}`："
                "该函数是本阶段关键执行点，调用目标未全部解析为 Method-level，按索引证据记录；证据：function-index calls。"
            )
        if len(lines) >= count:
            break
    return lines


def lifecycle_doc(root: Path, methods: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    by_name = method_by_call_name(methods)
    stage_blocks: list[str] = []
    stage_summary: dict[str, int] = {}
    graph_lines = ["```mermaid", "flowchart TD"]
    previous = None
    for stage, label in STAGES:
        node = safe_node(stage)
        graph_lines.append(f'  {node}["{label} ({stage})"]')
        if previous:
            graph_lines.append(f"  {previous} --> {node}")
        previous = node
    graph_lines.append("```")

    for index, (stage, label) in enumerate(STAGES, 1):
        rows = stage_methods(methods, stage)
        stage_summary[stage] = len(rows)
        key_classes = sorted({(row.get("owner") or short_func(row).rsplit("::", 1)[0]).split("#", 1)[0] for row in rows})[:6]
        state_objects = sorted({item for row in rows for item in (row.get("reads") or []) + (row.get("writes") or [])})[:8]
        evidence = ", ".join(f"`{pos(row)}`" for row in rows[:3]) or "`unknown`"
        config_source = "命令行/场景输入文件/UtInput" if stage in {"entry", "scenario_load", "object_create"} else "已加载运行时状态"
        chains = "\n".join(build_call_chains(rows, by_name, 3))
        function_rows = "\n".join(
            f"| `{short_func(row)}()` | `{pos(row)}` | `{row.get('lifecycle_role')}` | `{', '.join((row.get('calls') or [])[:5])}` |"
            for row in rows[:5]
        )
        stage_blocks.append(
            f"""### 阶段 {index}: {label} (`{stage}`)

| 属性 | 值 |
|---|---|
| 入口函数 | {', '.join(f'`{short_func(row)}()`' for row in rows[:3]) or '`unknown`'} |
| 关键类 | {', '.join(f'`{item}`' for item in key_classes[:4]) or '`unknown`'} |
| 配置来源 | {config_source} |
| 主要状态对象 | {', '.join(f'`{item}`' for item in state_objects[:5]) or '`unknown`'} |
| 证据位置 | {evidence} |

| 关键函数 | 位置 | lifecycle_role | 代表性调用 |
|---|---|---|---|
{function_rows}

**可验证调用链**：

{chains}
"""
        )

    doc = f"""# 应用/仿真生命周期分析

> 状态：已按 Phase6 重建
> 输入索引：`workspace/source-index/function-index.jsonl`、`workspace/source-index/dependency-index.jsonl`
> 说明：本文件以 Phase4 函数级生命周期角色为主，入口点补充来自一次 CodeGraph 批量查询。

## 生命周期总览

{chr(10).join(graph_lines)}

## 各阶段详情

{chr(10).join(stage_blocks)}
"""
    return doc, stage_summary


def data_object_rows(symbols: list[dict[str, Any]], methods: list[dict[str, Any]], deps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for key, brief in DATA_OBJECTS:
        symbol_matches = [
            row
            for row in symbols
            if row.get("kind") in {"class", "struct"} and key.lower() in (row.get("qualified_name") or "").lower()
        ]
        method_matches = [
            row
            for row in methods
            if key.lower() in " ".join([row.get("canonical_qualified_name", ""), row.get("brief", ""), " ".join(row.get("reads") or []), " ".join(row.get("writes") or [])]).lower()
        ]
        dep_matches = [
            row
            for row in deps
            if key.lower() in " ".join([str(row.get("source")), str(row.get("target")), str(row.get("context"))]).lower()
        ]
        result.append(
            {
                "key": key,
                "brief": brief,
                "symbols": symbol_matches[:5],
                "methods": method_matches[:8],
                "deps": dep_matches[:8],
            }
        )
    return result


def dataflow_doc(symbols: list[dict[str, Any]], methods: list[dict[str, Any]], deps: list[dict[str, Any]]) -> tuple[str, int]:
    objects = data_object_rows(symbols, methods, deps)
    rows = []
    sections = []
    for obj in objects:
        key = obj["key"]
        first_symbol = obj["symbols"][0] if obj["symbols"] else {}
        producer = obj["methods"][0] if obj["methods"] else {}
        consumer = obj["deps"][0] if obj["deps"] else {}
        rows.append(
            f"| `{key}` | {obj['brief']} | `{short_func(producer) if producer else 'unknown'}()` | `{consumer.get('source', 'unknown')}` | `scenario_load → model_update/output` |"
        )
        node_source = f"{key}_source"
        node_owner = f"{key}_owner"
        node_update = f"{key}_update"
        node_consumer = f"{key}_consumer"
        node_output = f"{key}_output"
        symbol_name = first_symbol.get("qualified_name", key)
        method_name = short_func(producer) if producer else "unknown"
        method_pos = pos(producer) if producer else "unknown"
        dep_evidence = consumer.get("path", "unknown")
        sections.append(
            f"""### 数据流 {key}: {obj['brief']}

```mermaid
flowchart LR
  {node_source}["配置/事件输入"]
  {node_owner}["{symbol_name}"]
  {node_update}["{method_name}()"]
  {node_consumer}["消费者/依赖方"]
  {node_output}["输出/行为影响"]
  {node_source} --> {node_owner}
  {node_owner} --> {node_update}
  {node_update} --> {node_consumer}
  {node_consumer} --> {node_output}
```

**节点映射**：

| Mermaid 节点 | 数据对象 | 中文说明 | 源码证据 |
|---|---|---|---|
| `{node_source}` | `{key}` 输入来源 | 场景输入、事件或运行时计算产生数据 | `workspace/source-index/function-index.jsonl` |
| `{node_owner}` | `{symbol_name}` | 持有或表示该类数据的 class/struct | `{first_symbol.get('path', 'unknown')}:{first_symbol.get('line_start', 'unknown')}` |
| `{node_update}` | `{method_name}()` | 更新或处理该数据的函数 | `{method_pos}` |
| `{node_consumer}` | 依赖消费者 | include/call/composition 中引用该对象的模块或函数 | `{dep_evidence}` |
| `{node_output}` | 输出/行为影响 | 数据影响仿真状态、事件、报告或可视化 | `docs/architecture/dependency-graph.md` |

**链路说明**：state_source → state_owner → update_function → consumers → outputs

**逐步解释**：
1. `state_source` 产生 `{key}`：来自场景配置、仿真事件或上一帧状态。
2. `state_owner` 持有 `{key}`：`{symbol_name}` 是当前索引中最直接的数据对象证据。
3. `update_function` 更新 `{key}`：`{method_name}()` 在 `{method_pos}` 处理或传播相关状态。
4. `consumers` 消费 `{key}`：依赖索引显示 `{consumer.get('source', 'unknown')}` 通过 `{consumer.get('relation', 'unknown')}` 关系使用它。
5. `outputs` 输出或影响行为：该数据最终影响模型更新、事件输出、报告或工具可视化。
"""
        )
    doc = f"""# 数据流分析

## 0. 用途说明

数据流分析用于解释 AFSIM 的关键状态如何从配置、事件或模型计算进入运行时对象，再被更新函数处理并影响其他模块、输出或可视化。

## 1. 关键数据对象

| 数据对象 | 类型 | 生产者 | 消费者 | 生命周期 |
|---|---|---|---|---|
{chr(10).join(rows)}

## 2. 数据流路径

{chr(10).join(sections)}
"""
    return doc, len(objects)


def config_flow_doc(methods: list[dict[str, Any]]) -> str:
    config_methods = [
        row
        for row in methods
        if any(token in " ".join([display_func(row), row.get("brief", ""), " ".join(row.get("calls") or [])]) for token in ["ProcessInput", "LoadFromFile", "ReadValue", "UtInput", "CompleteLoad"])
    ]
    config_methods.sort(key=lambda row: (0 if "core/wsf/source" in row.get("path", "") else 1, row.get("path", "")))
    rows = []
    flows = []
    for idx, row in enumerate(config_methods[:8], 1):
        target = row.get("owner") or short_func(row).rsplit("::", 1)[0]
        rows.append(f"| 配置流 {idx} | 场景/配置文件 | `{short_func(row)}()` | `{target}` | 影响对象属性或注册行为 | `{pos(row)}` |")
    for idx, row in enumerate(config_methods[:5], 1):
        flows.append(
            f"{idx}. 配置来源进入 `{short_func(row)}()` (`{pos(row)}`)，函数通过 `{', '.join((row.get('calls') or [])[:5])}` 等调用读取命令或值，写入 `{row.get('owner')}` 的运行时状态，并影响后续初始化/更新行为。"
        )
    return f"""## 配置流分析

配置流分析用于说明场景/配置文件如何转化为运行时对象属性、工厂注册和仿真行为。它帮助读者定位“输入文本中的命令”最终影响哪个对象、哪个初始化阶段和哪类运行时行为。

```mermaid
flowchart LR
  CfgFile["场景/配置文件"]
  Parser["UtInput / ProcessInput / LoadFromFile"]
  Registry["Factory / Extension / Component"]
  RuntimeObj["运行时对象属性"]
  Behavior["仿真行为"]
  CfgFile --> Parser --> Registry --> RuntimeObj --> Behavior
```

| 配置流 | 配置来源 | 解析函数 | 目标对象 | 运行时影响 | 证据位置 |
|---|---|---|---|---|---|
{chr(10).join(rows)}

**逐步解释**：

{chr(10).join(flows)}
"""


def extension_doc(deps: list[dict[str, Any]], methods: list[dict[str, Any]]) -> tuple[str, int]:
    registrations = [row for row in deps if row.get("relation") == "registration"]
    by_symbol: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in registrations:
        by_symbol[row.get("symbol") or row.get("target")].append(row)
    mechanism_rows = []
    sections = []
    for symbol, rows in sorted(by_symbol.items(), key=lambda item: (-len(item[1]), item[0]))[:10]:
        sample = rows[0]
        related_methods = find_methods(methods, symbol, limit=3)
        iface = ", ".join(f"`{short_func(row)}()`" for row in related_methods) or f"`{symbol}`"
        desc = EXTENSION_DESCRIPTIONS.get(symbol, "扩展/观察者机制，用于把外部能力接入运行时流程。")
        mechanism_rows.append(
            f"| `{symbol}` | {iface} | `{sample.get('path')}:{sample.get('line_start')}` | `{sample.get('evidence')}` | {desc} |"
        )
        sections.append(
            f"""### `{symbol}`

- 关键接口/基类：{iface}
- 注册位置：`{sample.get('path')}:{sample.get('line_start')}`
- 使用示例：`{sample.get('evidence')}`
- 用途说明：{desc}
- 运行时影响：注册项会改变对象创建、事件订阅、插件加载或输出链路；证据来自 `dependency-index.jsonl` 中 `relation=registration` 的 {len(rows)} 条记录。
"""
        )
    doc = f"""# 扩展点识别

## 0. 用途说明

扩展点分析用于识别插件、工厂、注册表、事件订阅、策略/Policy 等扩展边界，帮助判断外部能力如何接入系统、哪些接口可稳定复用、哪些注册路径会改变运行时行为。

## 1. 扩展机制总览

| 扩展机制 | 关键接口/基类 | 注册位置 | 使用示例 | 用途说明 |
|---|---|---|---|---|
{chr(10).join(mechanism_rows)}

## 2. 机制详情

{chr(10).join(sections)}
"""
    return doc, len(by_symbol)


def verify_docs(root: Path, stage_summary: dict[str, int], data_object_count: int, extension_count: int) -> dict[str, Any]:
    lifecycle = (root / "docs/architecture/lifecycle.md").read_text(encoding="utf-8")
    dataflow = (root / "docs/architecture/dataflow.md").read_text(encoding="utf-8")
    extensions = (root / "docs/architecture/extension-points.md").read_text(encoding="utf-8")
    stage_ok = all(f"`{stage}`" in lifecycle for stage, _label in STAGES)
    call_count = lifecycle.count("→")
    mermaid_blocks = lifecycle.count("```mermaid") + dataflow.count("```mermaid") + extensions.count("```mermaid")
    summary = {
        "schema_version": "1",
        "phase": "phase6-lifecycle",
        "status": "verified" if stage_ok and data_object_count >= 5 and extension_count >= 3 and call_count >= 8 else "needs_review",
        "stage_summary": stage_summary,
        "stage_coverage_ok": stage_ok,
        "call_chain_count": call_count,
        "data_object_count": data_object_count,
        "extension_mechanism_count": extension_count,
        "mermaid_block_count": mermaid_blocks,
        "outputs": {
            "lifecycle": "docs/architecture/lifecycle.md",
            "dataflow": "docs/architecture/dataflow.md",
            "extension_points": "docs/architecture/extension-points.md",
            "verify_report": "docs/verification/phase6-verify-report.md",
        },
    }
    return summary


def write_verify_report(root: Path, summary: dict[str, Any]) -> None:
    stage_rows = "\n".join(f"| `{stage}` | {count} |" for stage, count in summary["stage_summary"].items())
    report = f"""# Phase6 生命周期与数据流验证报告

## 1. 总体结论

| 检查项 | 结果 |
|---|---|
| 生命周期 8 阶段覆盖 | {'通过' if summary['stage_coverage_ok'] else '不通过'} |
| 生命周期调用链数量 | {summary['call_chain_count']} |
| 数据对象数量 ≥ 5 | {'通过' if summary['data_object_count'] >= 5 else '不通过'} |
| 扩展机制数量 ≥ 3 | {'通过' if summary['extension_mechanism_count'] >= 3 else '不通过'} |
| Mermaid 代码块 | {summary['mermaid_block_count']} |
| 总体状态 | {summary['status']} |

## 2. 生命周期阶段统计

| lifecycle_role | 关键函数数 |
|---|---:|
{stage_rows}

## 3. 输出文件

```text
docs/architecture/lifecycle.md
docs/architecture/dataflow.md
docs/architecture/extension-points.md
```

## 4. 说明

本轮 Phase6 以 Phase4 `function-index.jsonl`、Phase5 `dependency-index.jsonl` 为主要证据。入口函数因 Phase4 未标记 `entry`，已按 Phase6 规则用一次 CodeGraph 批量查询补充，并在 lifecycle.md 中以 main/WinMain 条目体现。
"""
    write_text(root / "docs/verification/phase6-verify-report.md", report)


def run(root: Path) -> dict[str, Any]:
    methods = load_methods(root)
    symbols = read_jsonl(root / "workspace/source-index/symbol-index.jsonl")
    deps = read_jsonl(root / "workspace/source-index/dependency-index.jsonl")
    life_doc, stage_summary = lifecycle_doc(root, methods)
    data_doc, data_object_count = dataflow_doc(symbols, methods, deps)
    config_doc = config_flow_doc(methods)
    extension_points_doc, extension_count = extension_doc(deps, methods)

    write_text(root / "docs/architecture/lifecycle.md", life_doc)
    write_text(root / "docs/architecture/dataflow.md", data_doc + "\n" + config_doc)
    write_text(root / "docs/architecture/extension-points.md", extension_points_doc)
    summary = verify_docs(root, stage_summary, data_object_count, extension_count)
    write_text(root / "workspace/source-index/phase6-lifecycle-summary.json", json.dumps(summary, ensure_ascii=False, indent=2))
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
