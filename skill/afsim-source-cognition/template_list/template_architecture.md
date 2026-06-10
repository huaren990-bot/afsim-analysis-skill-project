# AFSIM 仿真框架架构文档

> **状态**：
> **日期**：
> **分析范围**：
> **分析深度**：
> **基线文档**：

---
## 0.文档说明
**总体概述**：

**业务价值**：

**编程语言**：

---
## 1. 目录结构总览
```
xxx #介绍
  └── xxx #介绍
        ├── xxx #介绍
        │     ├── xxx #介绍
        │     ├── xxx #介绍
        │     └── xxx #介绍
        ├── xxx #介绍
        │     ├── xxx #介绍
        │     └── xxx #介绍
...
```
---

## 2. xxx总览

| 系统 |  子系统 | 模块 | 源文件数 | 核心职责 |
|------|------|------|----------|----------|


```mermaid

```
其中，xxx表示xxx，yyy表示yyy...

### 2.1 xxx系统（项目xxx系统路径）
1.**xxx系统概述**：

#### 2.1.1 xxx子系统（项目xxx子系统路径）

1.**子系统概述**：
2.**目录结构细览**：xxx子系统共包含yyyy个源文件，组织为以下子目录结构：
| 子目录 | 文件数 | 所属模块 | 核心职责 |
|--------|--------|--------|----------|

##### 2.1.1.1 xxxx模块（项目xxxx模块路径）
1.**模块概述**：
2.**模块类细览**：xxxx模块共包含yyyy个类：
| 类 | 文件 | 职责 |
|----|------|------|

### 2.2 xxx系统（项目xxx系统路径）
1.**xxx系统概述**：

#### 2.2.1 xxx子系统（项目xxx子系统路径）

1.**子系统概述**：
2.**目录结构细览**：xxx子系统共包含yyyy个源文件，组织为以下子目录结构：
| 子目录 | 文件数 | 所属模块 | 核心职责 |
|--------|--------|--------|----------|

##### 2.2.1.1 xxxx模块（项目xxxx模块路径）
1.**模块概述**：
2.**模块类细览**：xxxx模块共包含yyyy个类：
| 类 | 文件 | 职责 |
|----|------|------|

...

---

## 3. 仿真生命周期

依据文档xxx 第xxx节及 xxx 源码：

```mermaid

```
其中，xxx表示xxx，yyy表示yyy...(用语言说明生命周期)

### 3.1 生命周期各阶段关联

| 阶段 | 入口函数/关键类 | 配置来源 | 主要状态对象 | 证据位置 |
|------|----------------|----------|-------------|----------|


---

## 7. 数据流

```mermaid

```
其中，xxx表示xxx，yyy表示yyy...(用语言说明数据流)

---

## 8. 配置流

```mermaid

```
其中，xxx表示xxx，yyy表示yyy...(用语言说明控制流)

---

## 9. 扩展点

| 扩展机制 | 关键接口 | 位置 | 说明 |
|----------|----------|------|------|


---

## 10. 关键符号

| 符号 | 类型 | 角色 | 源位置 |
|------|------|------|--------|


---

## 11. 未知项

| # | 问题 | 原因 | 严重度 |
|----|------|------|--------|
| 1 | xxx | yyy | 低 |


---

## 12. 源码证据

| 证据类型 | 位置 | 数量 | 验证状态 |
|----------|------|------|----------|
| 源码根目录 | `source_root/afsim-2_9/swdev/src/core/` | 4,997 源文件 | ✅ |
| 文件索引 | `workspace/source-index/file-index.jsonl` | 4,997 行，2,413 文件含 include 数组 | ✅ JSON 全通过 |
| 符号索引 | `workspace/source-index/symbol-index.jsonl` | 3,255 去重符号（class/struct/enum/typedef/using） | ✅ 行号源码验证 |
| 函数索引 | `workspace/source-index/function-index.jsonl` | 4,099 函数/方法（24.4%生命周期已分类） | ✅ 枚举合规 |
| 依赖索引 | `workspace/source-index/dependency-index.jsonl` | 1,113 依赖（继承1014+组合50+调用16+构建14+include10+注册9） | ✅ 源码行号引用 |
| 构建系统 | core/ 下 25 个 CMakeLists.txt | 14 条模块间 target_link_libraries 依赖 | ✅ |
| 源码验证 | WsfSimulation.hpp, WsfPlatform.hpp, WsfComponent.hpp, WsfComponentFactory.hpp, WsfExtension.hpp, WsfPluginManager.hpp | 7 个核心头文件完整阅读 | ✅ source-cited |
| 基线文档 | `docs/baseline/WsfSimulation_Design_Document.md` (111KB) + `WsfSimulation_Core_Design_Document.md` (66KB) | 2 份基线设计文档 | ✅ document-cited |
