# 人工检查报告
>时间：2026-06-23
>检查阶段：phase1-phase7

## 整体问题
1. markdown文件应当放置到`/docs`目录下，而不是`/workspace`目录下
2. 旧文件可以被覆盖/放入项目回收站
3. 所有文件中的英文标识均没有对应的说明，缺少添加中文说明/中文名称，那么如何理解该英文标识的含义？
4. 不知道extension-points扩展点分析的作用。

## afsim-architecture.md
1. 目录总览需要详细而完整，不能使用省略号
2. 缺少总框架图
3. 模块总览缺少模块图、详情跳转链接。
4. 数据流关键数据对象和数据流程图没有对应关系。
5. 配置流、扩展点两章节没有任何说明。
6. 未知项问题描述不清楚，应当寻求人工解决。
7. 关键符号过多导致无法全部列举，建议改为总体性陈述。

## dataflow.md
1. 没有任何数据流链路的解释和说明。

## dependency-graph.md
1. 类继承关系图太小
2. 模块间依赖关系图：既然展示前 20 个连接最密集的模块，为什么Designer等模块一条连接线都没有。
3. 模块依赖详情既然无法展示，就应当添加到module-dependency.md的文件链接。

## lifecycle.md
1. 调用链`位置`错误，`调用`写的太简略，无法验证正确性。

## module-dependency.md
1. 检查`mermaid`语法，存在错误无法渲染。
2. 依赖模块列中，"afsim-2_9/training/developer/core/labs/s"路径不存在，同时不应该依赖到training文件夹，这个文件夹没有做分析。
3. 架构级依赖：如果一个章节条目过多，改为总结性陈述，同时，告知所有条目可以去哪里查询到。
4. 持有类型的`strong`、`medium`、`weak`什么含义，如何解释，与第五节依赖强度是否相关？
5. 本文件中的子系统与afsim-architecture.md中的子系统不一致，产生冲突。
6. 只展示了一个子系统的依赖，从第二个子系统开始就没有内容了。
7. 关键全局常量依赖展示完整了吗？为什么展示这些？去哪里找完整的说明？
8. “关键全局常量依赖”表格`说明`列应当放在`定义位置`前，并且不能简单重复常量标识，起码解释含义吧。

## module-overview.md
1. 模块概览应当有段文字说明，总计多少模块，模块如下：（再展示表格），表格为模块清单，不应当缺少模块。
2. 模块级别如何区分的，为什么source、wsf_six_dof、test都是在一个路径？都属于一个层次的模块？
3. 子系统和模块需要区分开。

## x-level-capabilities.md
1. 要求只包含仿真模型的功能。
2. 方法级功能过多导致无法展示，那么就无需写方法级功能。
3. 添加一个功能总览章节，综述全部功能。

## **function-index.jsonl**
1. json条目存在问题。以最后一行为例："qualified_name": "POST_PROCESSOR_LIB_EXPORT::max"，这属于成员变量，不属于函数。

## **symbol-index**
1. symbol-index.jsonl是phase3生成的？为什么不补充到symbol-index-phase2.jsonl，而是分两个文件？
2. symbol-index.jsonl条目存在问题。以"qualified_name": "POST_PROCESSOR_LIB_EXPORT"为例，其signature、member_functions均不正确。








