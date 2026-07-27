# 需求缺口分析模板

# <需求名称>需求缺口分析

> **需求集 ID**：REQ-XXX
> **需求基线**：`2_REQ-XXX-requirement-<slug>.md`
> **分析日期**：YYYY-MM-DD
> **状态**：draft / verified

## 1. 分析边界

- AFSIM 索引与源码版本：……
- 目标系统证据或假设：……
- 已读取算法卡片：……
- 未覆盖范围：……

## 2. 覆盖汇总

| 综合状态 | 数量 | 原子需求 ID |
| --- | ---: | --- |
| satisfied | 0 | — |
| partial | 0 | — |
| missing_with_afsim_reference | 0 | — |
| missing_without_afsim_reference | 0 | — |
| unknown | 0 | — |

## 3. 逐需求结论

| 原子需求 ID | 验收目标 | 综合状态 | AFSIM 证据 | 目标系统证据 | 缺口 FU | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-XXX-FUNC-01 | <摘要> | <status> | `path:start-end` | `<path>` / empty_system | FU-001 | high |

## 4. FU 详细规格

### FU-001：<名称>

- **关联需求**：REQ-XXX-FUNC-01
- **建议方式**：direct_adaptation / partial_rewrite / cleanroom / novel
- **功能与验收标准**：……
- **输入/输出契约**：……
- **单位、坐标系、时间语义**：……
- **状态与副作用**：……
- **上游输入来源**：external / state / FU-XXX
- **下游输出去向**：final / state / FU-XXX
- **AFSIM 已验证参考**：`qualified_name`，`path:start-end`；无参考时记录检索范围
- **目标系统差异**：……
- **耦合度与风险**：……

## 5. FU 数据流

```mermaid
flowchart LR
    IN["external:input"] --> FU1["FU-001"]
    FU1 --> OUT["final:output"]
```

| 数据边 | 类型 | 单位 | 坐标系 | 生产者 | 消费者 | 结果 |
| --- | --- | --- | --- | --- | --- | --- |
| `<name>` | `<type>` | <unit> | <frame> | external | FU-001 | pass/fail |

## 6. 风险与未决问题

| ID | 问题 | 影响 | 处理建议 | 是否阻塞迁移 |
| --- | --- | --- | --- | --- |
| Q-001 | <问题> | <影响> | <建议> | yes/no |

## 7. 产物与验证

- 功能映射矩阵：……
- AFSIM 追溯矩阵：……
- gap-specs：……
- 验证报告：……
