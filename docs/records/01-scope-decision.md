# 01 — 范围决策记录

**日期**：2026-06-08
**状态**：已确认
**决策者**：afsim-source-cognition agent + 开发人员

---

## 问题背景

需要根据 `tools/prompts/afsim-source-cognition 系统提示词.md` 的要求，对 AFSIM 2.9.0 仿真框架的 C++ 源代码进行全面分析，产出结构化索引文件和架构文档。

## 代码库规模

| 统计项 | 数值 |
|--------|------|
| 源码根目录 | `afsim_2.9.0_src_linux/` |
| C++ 源文件总数 | 17,190 |
| 主要模块数 | 15+ |

### 各模块文件分布

| 模块 | 文件数 | 说明 |
|------|--------|------|
| core/wsf/source (顶层) | 380 | 核心框架类 |
| core/wsf/source/comm | 108 | 通信子系统 |
| core/wsf/source/dis | 120 | DIS 分布式仿真协议 |
| core/wsf/source/mover | 101 | 运动模型 |
| core/wsf/source/observer | 32 | 观察者模式 |
| core/wsf/source/processor | 40 | 处理器 |
| core/wsf/source/script | 108 | 脚本系统 |
| core/wsf/source/sensor | 73 | 传感器系统 |
| core/wsf/source/traffic | 13 | 交通/流量 |
| core/wsf/source/xio | 55 | 外部 IO |
| core/wsf/source/ext | 16 | 扩展接口 |
| core/wsf/source/event_pipe | 15 | 事件管道 |
| core/wsf/source/xio_sim | 52 | 仿真 IO |
| core/wsf_mil/source | 213 | 军事域扩展 |
| core/wsf_space/source | 171 | 空间域扩展 |
| core/wsf_nx/source | 34 | 下一代框架 |
| core/wsf_parser | 81 | 语法解析器 |
| core/wsf_util | 9 | 工具库 |
| wsf_plugins | 9,884 | 各类插件 |
| tools | 2,485 | 辅助工具 |
| wizard | 1,061 | 向导/UI 工具 |
| warlock | 616 | Warlock 组件 |
| mystic | 291 | Mystic 组件 |
| mover_creator | 225 | 运动体创建工具 |
| 其他 | ~220 | engage, weapon_tools 等 |

## 决策过程

### 决策 1：优先分析核心框架

**选项**：
- A) 全量分析 17,190 文件 — 不可行，单次会话无法完成
- B) 所有核心模块（~1,039 文件）— 规模仍很大
- C) 仅核心框架 wsf/source（~1,113 文件）— ✅ 选择此项

**理由**：
1. `wsf/source/` 是 AFSIM 的心脏 — 包含 Application、Simulation、Platform、Track、Sensor、EM、Mover 等所有基础抽象
2. 其他模块（wsf_mil、wsf_space、wsf_plugins）都建立在核心框架之上，理解核心后才能理解它们
3. 985 个文件中的 wsf_plugins 大部分是自动生成代码和测试数据，优先级低
4. 先完成 P0 核心，产出有价值的成果后，再逐步扩展到 P1-P3

### 决策 2：文件级完整分析

**选项**：
- A) 架构级概览 — 只看关键类
- B) 文件级完整分析 — ✅ 选择此项

**理由**：
1. 提示词明确要求记录参数默认值、成员变量初始值、枚举值等细节
2. 这些细节对下游功能分析和代码迁移至关重要
3. 每个文件的分析记录可被下游 Agent 检索

### 决策 3：分批并行分析

**理由**：
1. 1,113 个文件无法串行处理
2. 按子系统分批，每批 30-80 个文件
3. 同批内文件在子系统内聚，依赖关系密集，适合并行

## 优先级定义

| 优先级 | 范围 | 文件数 | 理由 |
|--------|------|--------|------|
| P0 | wsf/source 全部 | ~1,113 | 仿真引擎基石，所有其他模块依赖它 |
| P1 | wsf_mil + wsf_space | ~384 | 军事和空间域是最重要的应用域 |
| P2 | wsf_nx + wsf_parser + wsf_util | ~124 | 基础设施 |
| P3 | wsf_plugins（精选） | 按需 | 特定应用场景 |
