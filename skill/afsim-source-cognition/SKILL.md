---
name: afsim-source-cognition
description: 当用户需要快速学习 AFSIM 源码、理解目录结构、模块职责、核心类、函数索引、调用链、数据流、仿真生命周期或生成 AFSIM 架构认知报告时，使用本 skill。
---

# AFSIM 源码认知 Skill

本 skill 负责让大模型快速建立对 AFSIM 的源码级认知。它的输出应服务于后续算法提取、需求映射和迁移生成。

## 输入

- AFSIM 源码目录。
- 用户提供的基准说明文档。
- 已有索引或历史架构报告。

## 执行步骤

1. 扫描源码目录，识别顶层模块、构建文件、配置文件、测试目录和示例目录。
2. 生成文件级索引：路径、文件类型、模块归属、主要职责。
3. 生成符号级索引：类、函数、枚举、关键数据结构、入口点。
4. 识别仿真生命周期：初始化、场景加载、实体创建、模型更新、事件处理、输出和结束。
5. 识别核心数据流：状态如何进入模型、如何更新、如何被其他模块读取。
6. 识别扩展机制：插件、工厂、注册表、抽象接口、脚本配置。
7. 产出架构认知报告，并标记未知项。

## 输出

- `workspace/source-index/file-index.jsonl`
- `workspace/source-index/symbol-index.jsonl`
- `workspace/source-index/function-index.jsonl`
- `workspace/source-index/dependency-index.jsonl`
- `docs/architecture/afsim-architecture.md`
- `docs/architecture/module-dependency.md`

## 质量要求

- 每个模块职责必须有源码路径依据。
- 不把文件名相似当作功能等价证据。
- 对未阅读或无法确认的模块标记“待确认”。
- 架构图可以用 Mermaid，但必须能追溯到源码。
