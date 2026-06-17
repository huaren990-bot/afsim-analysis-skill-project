# Phase 3 完成记录：符号级细粒度分析

> **完成日期**：2026-06-17
> **阶段**：Phase 3 / 7
> **状态**：⚠️ 已完成（存在 known-issue）

## 分析范围

| 参数 | 值 |
|------|-----|
| source_root | /Users/hjt/afsim/afsim-analysis-skill-project/source_root |
| extract_roots | afsim-2_9, src |
| exclude_paths | .git, build, 3rd_party, node_modules |
| analysis_depth | full |

## 执行方式

| 子阶段 | 方式 | 职责 |
|--------|------|------|
| Phase 3A: 符号精细化 | Python 脚本（phase3_process.py） | 按文件读取（3722个文件），提取类/结构体成员、方法、继承关系、枚举值 |
| Phase 3B: 宏提取 | grep批量扫描 | 一次性 grep 全量 #define，过滤 EXPORT/guard，提取 9106 个宏 |
| Phase 3C: 枚举索引 | 复用已读文件 | 从已读取的 3722 个文件中提取 814 个枚举的完整值列表 |

**总耗时**：约 15 分钟
**工具调用**：3722 次文件读取（每个文件1次），2 次 grep 扫描（afsim-2_9 + src）

## 产出文件

| 文件 | 路径 | 大小 |
|------|------|------|
| symbol-index.jsonl（精细化版） | workspace/source-index/symbol-index.jsonl | 23.4 MB |
| macro-index.jsonl | workspace/source-index/macro-index.jsonl | 3.0 MB |
| enum-index.jsonl | workspace/source-index/enum-index.jsonl | 631 KB |

## 关键统计数据

| 指标 | Phase 2（粗版） | Phase 3（精细化） |
|------|-----------------|-------------------|
| 总符号数 | 13,936 | 13,936 |
| class/struct 含 signature | ~70% | 99.9% |
| class/struct 含 base_symbols | ~21.6% | 63.4% |
| class/struct 含 member_functions | 0 | 4,859（81.8%） |
| class/struct 含 member_variables | 0 | 3,989（67.1%） |
| 成员函数总数（含access/virtual/static/const） | 0 | 46,084 |
| 成员变量总数（含type/access/initial_value） | 0 | 23,556 |
| 宏 | 0 | 9,106 |
| 枚举（含完整values） | 0 | 814（812 含 values） |

## 验证结果

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | class/struct 精细化率 ≥ 85% | ⚠️ known-issue | 63.4% — 代码库特征 |
| 2 | 成员函数访问修饰符 ≥ 80% | ✅ | 100.0% |
| 3 | 宏过滤 无EXPORT/guard | ✅ | EXPORT: 0, guard: 0 |
| 4 | 宏抽样验证 | ✅ | 抽样10个，0个问题 |
| 5 | enum-index 完整性 | ✅ | 814条目，812含values |
| 6 | Phase2→Phase3 100% 追溯 | ✅ | 13936/13936 |

## 已知问题与备注

1. **base_symbols 覆盖率 63.4%**：经 80 个样本抽样验证（0 漏检），确认是代码库真实特征。AFSIM 中 92.5% 的 struct 无基类继承，约 21% 的 class 也无基类。class 的 base_symbols 覆盖率为 78.9%。
2. **2 个枚举 values 为空**（Phase、UtStringEnumId）。
3. 继承检测迭代了 3 轮：修复了多行声明、命名空间前缀（如 `rv::PlatformAngleUpdater`）、`std::exception` 小写基类等问题。

## 下游就绪

Phase 4（函数/方法级深度提取）可使用：
- `symbol-index.jsonl` — 含 46,084 个成员函数的签名、参数、访问修饰符、virtual/static/const 属性
- `macro-index.jsonl` — 9,106 个宏定义
- `enum-index.jsonl` — 814 个枚举的完整值列表
