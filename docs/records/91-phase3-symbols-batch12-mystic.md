# Phase3 Batch12: Mystic 符号精细化

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/mystic/`  
> **阶段**：Phase3 / symbol refinement

## 处理摘要

| 指标 | 数量 |
|---|---:|
| 输入 pending | 337 |
| 覆盖文件 | 117 |
| CodeGraph 文件读取成功 | 117 |
| 新增 `symbol-index.jsonl` 条目 | 335 |
| 新增 `enum-index.jsonl` 条目 | 7 |
| 标记跳过 | 2 |
| 范围剩余 pending | 0 |

## 处理方式

本批次按文件分组读取 CodeGraph，每个文件只读取一次。解析范围覆盖 Mystic 执行入口、结果可视化插件、`rv` 支撑库、自由函数、方法、构造函数、插件注册宏调用、class、struct、namespace、using、typedef 和 enum。解析成功的 Phase2 粗符号标记为 `done_batch12`，无法在源码中定位真实 C++ 声明或定义形态的候选标记为 `skipped_unresolved_phase2_symbol_batch12`。

其中 `main(int,char**)` 已归一到源码中的 `int main(int aArgc, char* aArgv[]) try` 定义，并作为 `done_batch12` 写入精细符号索引。

## 跳过项

| 符号 | kind | 路径 | 原因 |
|---|---|---|---|
| `rv::TrackDb` | function | `afsim-2_9/swdev/src/mystic/lib/source/RvTrackDb.cpp` | Phase2 将类型/构造相关名称误归类为 function，源码中无匹配自由函数定义 |
| `rv::ResultMessageArray` | function | `afsim-2_9/swdev/src/mystic/lib/source/RvResultMessageArray.hpp` | Phase2 将类型名误归类为 function，源码中无匹配自由函数定义 |

## 产物变更

| 文件 | 变更 |
|---|---|
| `workspace/source-index/symbol-index.jsonl` | 追加 335 条 `phase3:batch12` 精细符号 |
| `workspace/source-index/enum-index.jsonl` | 追加 7 条 `phase3:batch12` 枚举 |
| `workspace/source-index/symbols-to-refine-phase3.jsonl` | 335 条标记为 `done_batch12`，2 条标记为 `skipped_unresolved_phase2_symbol_batch12` |
