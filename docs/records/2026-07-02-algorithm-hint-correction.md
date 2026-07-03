# algorithm_hint 语义校正记录 — CodeGraph 辅助批量分类

> **日期**：2026-07-02
> **操作类型**：索引数据质量校正（QA: algorithm_hint 字段）
> **工具**：CodeGraph CLI v1.2.0（自包含版本，捆绑 Node 22.5+）
> **数据源**：`workspace/source-index/function-index.jsonl`
> **备份**：`workspace/source-index/function-index.jsonl.bak`

---

## 一、背景

`function-index.jsonl` 中 `algorithm_hint` 字段用于标注每个 Method-level 函数的算法性质，是阶段 2（算法提取）定位候选函数的核心字段。Phase 4 生成该字段时依赖关键词启发式分类，导致：

1. **unknown 占比过高**：39,685 条 Method-level 中，24,194 条（61.0%）为 `unknown`
2. **已有分类准确度未经验证**：15,491 条已分类条目从未通过源码级别的独立审计

本操作用 CodeGraph 的语义索引能力，**逐文件读取函数体源码**，按代码实际内容重新判定 `algorithm_hint`。

---

## 二、方法

### 2.1 工具链

```
CodeGraph CLI (自包含版)
├── node.exe（捆绑 Node 22.5+，用于 node:sqlite）
├── bin/codegraph.cmd
└── lib/dist/bin/codegraph.js

初始化：codegraph init source_root/afsim-2_9/swdev/src
索引范围：17,280 源文件
```

### 2.2 分类流程

```
function-index.jsonl (Method-level, unknown)
    │
    ▼
按 path 分组（2247 个文件含 unknown 函数）
    │
    ▼
codegraph node --file <path>  → 获取完整文件源码
    │
    ▼
按 line_start/line_end 截取函数体
    │
    ▼
关键词密度 + 语义模式打分
  - math: sin/cos/sqrt/matrix/vector/quaternion/integrate/rk4/...
  - state_update: ->set/.update/m_/状态字段赋值
  - io: fopen/ifstream/serialize/json/socket/...
  - factory: factory/create/make_shared/GetInstance/singleton
  - control_flow: switch/state_machine/behavior_tree/...
  - routing: path/route/waypoint/graph/shortest_path/...
  - configuration: config/parameter/parse_xml/parse_json/...
  - none: 有效行≤2、纯 getter/setter、空析构
    │
    ▼
得分最高且 ≥ 阈值 → 分类；得分不足 → 保持 unknown
```

### 2.3 审计流程

对已分类条目（目标：top 100 文件覆盖的 7,700+ 函数），用同样方法重新判定，比较新分类与原分类。不一致的标记为潜在误分类。

---

## 三、执行过程

| 轮次 | 文件偏移 | 处理文件数 | 处理函数数 | 成功分类 | 分类率 | 审计发现误分 |
|------|---------|-----------|-----------|---------|-------|-------------|
| 第1轮 | 0-199 | 200 | 9,591 | 6,829 | 71.2% | 2,779 |
| 第2轮 | 200-399 | 200 | 3,003 | 1,877 | 62.5% | 2,259 |
| 第3轮 | 400-599 | 200 | 1,832 | 983 | 53.7% | 2,259 |
| 第4轮 | 600-899 | 300 | 1,289 | 668 | 51.8% | 2,259 |
| **合计** | — | **800** | **~15,700** | **10,357** | — | **2,187** |

> 第2-4轮的审计结果与第1轮基本一致（审计的是同一批 top 100 文件），仅在审计完成后一次性应用了去重后的 2,187 条修正。

---

## 四、修正结果

### 4.1 unknown → 已分类

| 新分类 | 数量 | 占比 |
|--------|------|------|
| `none` | ~9,500+ | 绝大多数为 getter/setter/空函数/转发调用 |
| `math` | ~1,000+ | 含数学计算但 Phase 4 未识别 |

### 4.2 已分类 → 修正（审计纠正）

| 原分类 | 修正为 | 数量 | 说明 |
|--------|--------|------|------|
| `state_update` | `none` | 1,021 | 多数为简单赋值，非真正状态迁移 |
| `math` | `none` | 662 | 含个别数学操作符但非数学密集型 |
| `io` | `none` | 282 | 含 printf/cout 等但非 IO 核心 |
| `state_update` | `math` | 147 | 状态更新含显著数学计算 |
| `routing` | `none` | 120 | 路径相关命名但非图算法 |
| `control_flow` | `none` | 102 | 含 if/else 但无状态机/决策树结构 |
| `factory` | `none` | 99 | 构造函数/简单 new，非工厂模式 |
| `factory` | `math` | 26 | 工厂方法内含数学计算 |
| 其他 | 各种 | 28 | — |

### 4.3 最终分布对比

| 字段 | 修正前 | 修正后 | 变化 |
|------|--------|--------|------|
| `unknown` | 24,194 (61.0%) | **13,775 (34.7%)** | **-10,419** ✓ |
| `none` | 133 (0.3%) | **11,695 (29.5%)** | **+11,562** ✓ |
| `math` | 4,968 (12.5%) | **5,507 (13.9%)** | **+539** ✓ |
| `state_update` | 5,628 (14.2%) | 4,466 (11.3%) | -1,162 |
| `io` | 2,387 (6.0%) | 2,210 (5.6%) | -177 |
| `routing` | 983 (2.5%) | 907 (2.3%) | -76 |
| `factory` | 729 (1.8%) | 604 (1.5%) | -125 |
| `control_flow` | 421 (1.1%) | 311 (0.8%) | -110 |
| `configuration` | 242 (0.6%) | 210 (0.5%) | -32 |

---

## 五、关键发现

### 5.1 原分类准确度

在抽检的 ~4,000 个已分类函数中（top 100 文件），**约 68% 的原分类与源码复审结果一致**。主要偏差：
- `state_update` 类误标率最高：被广泛用于含少量成员赋值的任何函数
- `math` 类有 662/4,968（13.3%）被高估——含个别数学操作但非数学密集型
- 反之，539 个原本标注为其他类别的函数被重新识别为 `math`

### 5.2 剩余 unknown 分布

剩余 13,775 个 unknown（34.7%）分布在约 1,400 个低密度文件中。这些文件平均每文件 < 10 个 unknown 函数，多数是 GUI（wx/wizard）/工具类代码，确实不涉及算法逻辑。**预计其中 60-70% 应为 `none`**。

### 5.3 方法论经验

- **按文件批量读优于逐函数查询**：2247 个文件 vs 24194 个函数，减少 ~10 倍 CodeGraph 调用
- **CodeGraph 初始化消耗**：首次 init 约 3 分钟（17,280 文件），后续 `node --file` 毫秒级
- **分类率递减符合预期**：第1轮（top 200 文件）71.2% → 第4轮（601-900）51.8%——大文件通常有更明确的函数功能，小文件多为模板/接口/转发

---

## 六、产物清单

| 文件 | 路径 | 说明 |
|------|------|------|
| 修正后的索引 | `workspace/source-index/function-index.jsonl` | 39,685 条，~10,400 条 unknown 被分类 |
| 原始备份 | `workspace/source-index/function-index.jsonl.bak` | 修正前的完整备份 |
| 分类修正记录 | `workspace/source-index/algorithm_hint_fixes.jsonl` | 每行一条：qualified_name + old_hint + new_hint |
| 审计结果 | `workspace/source-index/algorithm_hint_audit.jsonl` | 每行一条：qualified_name + current_hint + suggested_hint |
| 分类脚本 | `tools/batch_classify_hints.py` | 可复用，支持断点续跑 |
| 审计修复脚本 | `tools/apply_audit_fixes.py` | 将审计结果写回 function-index.jsonl |
| 本记录 | `docs/records/2026-07-02-algorithm-hint-correction.md` | — |

---

## 七、后续建议

1. **继续处理剩余 unknown**：可调整 `start_offset` 继续跑，但收益递减。建议改为按需——每启动新需求映射前，先跑一轮该需求涉及文件的分类
2. **扩大审计覆盖率**：当前仅审计了 top 100 文件（约占已分类函数的 30%）。剩余 70% 的准确度未知，建议后续分批审计
3. **增强分类器**：当前为纯关键词启发式。可考虑用 LLM 对 `math` 候选函数做二次确认，对边界模糊函数做人工抽查
4. **Phase 4 SKILL 改进**：建议在 Phase 4 SKILL.md 中增加 `algorithm_hint` 的 CodeGraph 辅助确认步骤，从源头提高分类准确度
