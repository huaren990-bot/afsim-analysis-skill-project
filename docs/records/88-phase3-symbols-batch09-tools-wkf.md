# Phase3 batch09：tools/wkf 符号补齐记录

> **日期**：2026-07-15  
> **范围**：`afsim-2_9/swdev/src/tools/wkf`  
> **证据方式**：按文件分组调用 CodeGraph file node；同一文件只读取一次

## 结果汇总

| 指标 | 数量 |
|---|---:|
| 输入文件 | 312 |
| 输入 pending | 1,001 |
| 新增精细符号 | 993 |
| 新增枚举条目 | 43 |
| 已闭环补齐 | 994 |
| 已记录跳过 | 7 |
| 目标范围剩余 pending | 0 |

## 跳过项分类

| 分类 | 数量 | 示例 | 处理原因 |
|---|---:|---|---|
| 类型引用误归类为 function | 5 | `wkf::DataContainer` | Phase2 把 ACES display 数据容器相关类型引用识别为 function，源码中无对应函数声明 |
| 文件名前缀误归类为 class | 2 | `WkfVisualEffectsDisplayInterface`、`WkfEventMarkerDisplayInterface` | 真实 class 名分别为 `VisualEffectsDisplayInterface`、`EventMarkerDisplayInterface`，源码中无带 `Wkf` 前缀的 class 声明 |

## 范围说明

本批覆盖 WKF 的 core、common、air_combat、comm_vis、wsfg 和 plugins 子树，主要包括 GUI 框架、插件注册、偏好对象、数据容器、显示覆盖、轨迹/区域/可视化工具和空间任务配置组件。

batch09 没有引入新的空 values 枚举。处理完成后，`tools/wkf` 范围在 `workspace/source-index/symbols-to-refine-phase3.jsonl` 中已无 `pending`。
