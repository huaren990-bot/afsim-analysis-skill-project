# 需求规范模板

用于待确认版 `1_<req-id>-requirement-<slug>.md` 与确认版
`2_<req-id>-requirement-<slug>.md`。待确认版保留选择项；确认版只保留已选结论和批准假设。

# <需求名称>需求规范

> **需求集 ID**：REQ-XXX
> **版本**：0.1
> **状态**：待确认 / 已确认
> **来源**：`<path>#<section-or-lines>`
> **生成日期**：YYYY-MM-DD
> **确认记录**：<确认人或用户消息、日期>

## 1. 目标与范围

### 1.1 目标

<说明系统要解决的问题，不写具体 AFSIM 实现方案。>

### 1.2 范围内

- <能力>

### 1.3 范围外

- <明确排除项>

## 2. 系统边界与术语

| 术语/量 | 定义 | 类型 | 单位 | 坐标系 | 时间语义 | 来源 |
| --- | --- | --- | --- | --- | --- | --- |
| `<name>` | <含义> | `<type>` | <unit/unknown> | <frame/none/unknown> | <current/previous/rate> | `<source_ref>` |

## 3. 功能流水线

```mermaid
flowchart LR
    IN["外部输入"] --> R1["REQ-XXX-FUNC-01"]
    R1 --> R2["REQ-XXX-FUNC-02"]
    R2 --> OUT["最终输出"]
```

| 步骤 | 原子需求 ID | 输入来源 | 输出去向 | 状态读写 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 1 | REQ-XXX-FUNC-01 | external:`<name>` | REQ-XXX-FUNC-02:`<name>` | `<state>` | <说明> |

## 4. 原子功能需求

### REQ-XXX-FUNC-01：<短名称>

- **来源**：`<path>#<section-or-lines>` / 用户消息
- **状态**：confirmed / assumed / unknown / conflict
- **优先级**：high / medium / low
- **需求陈述**：系统应……
- **触发条件**：……
- **前置条件**：……
- **正常行为**：
  1. ……
- **替代/异常行为**：
  1. ……
- **输入**：

| 名称 | 类型 | 单位 | 坐标系 | 约束 | 来源 |
| --- | --- | --- | --- | --- | --- |
| `<name>` | `<type>` | <unit> | <frame> | <range> | external / state / REQ-ID |

- **输出**：

| 名称 | 类型 | 单位 | 坐标系 | 约束 | 消费者 |
| --- | --- | --- | --- | --- | --- |
| `<name>` | `<type>` | <unit> | <frame> | <range> | final / state / REQ-ID |

- **状态与副作用**：……
- **验收标准**：
  1. Given … When … Then …
  2. 边界条件……
- **AFSIM 候选提示（非需求）**：`<candidate or none>`，证据等级 `<index-derived/source-cited>`。

> 复制本节直至覆盖全部原子需求。

## 5. 非功能需求

| ID | 类别 | 可验证约束 | 测量/验收方法 | 状态 | 来源 |
| --- | --- | --- | --- | --- | --- |
| REQ-XXX-NFR-01 | 性能 | <如每步耗时上限> | <基准环境与方法> | confirmed/unknown | `<source_ref>` |

## 6. 假设、未知与冲突

| ID | 类型 | 内容 | 对接口/行为的影响 | 需要的确认 | 是否阻塞确认版 |
| --- | --- | --- | --- | --- | --- |
| Q-001 | unknown | <问题> | <影响> | <最小确认问题> | yes/no |

## 7. 追溯与变更

| 原子需求 ID | 原始来源 | 上一版本 | 本版变化 | 原因 |
| --- | --- | --- | --- | --- |
| REQ-XXX-FUNC-01 | `<source_ref>` | — | 初始建立 | — |

## 8. 确认

| 检查项 | 结果 |
| --- | --- |
| 原始需求均有来源 | Y/N |
| 原子需求均可验收 | Y/N |
| 单位、坐标系、时间语义已确认或标 unknown | Y/N |
| 阻塞问题已关闭 | Y/N |
| 同意进入 AFSIM 能力映射 | Y/N |
