# AFSIM 算法中性接口规格模板

# <算法中文名称>接口规格

> **算法 ID**：ALG-<DOMAIN>-<SLUG>
> **版本/状态**：1.0 / draft
> **对应卡片**：`docs/algorithms/<domain>-<algorithm>-card.md`
> **性质**：接口规格，不代表已有实现

## 1. 目标与边界

- 接口职责：……
- 调用时机：……
- 包含/不包含：……
- 可重入/线程安全：……

## 2. 单位与坐标系

| 量 | 类型 | 单位 | 坐标系 | 有效范围 | 时间语义 |
| --- | --- | --- | --- | --- | --- |
| `<name>` | `<type>` | <unit> | <frame> | <range> | current/previous/rate |

内部统一单位与边界转换规则：……

## 3. 中性数据类型

```cpp
// 中文：算法输入；所有字段注明单位、坐标系和有效范围。
struct AlgorithmInput
{
    double value{}; // 中文：示例输入，单位 <unit>，坐标系 <frame>
};

// 中文：算法持久状态；由调用者持有并显式初始化/重置。
struct AlgorithmState
{
    double value{}; // 中文：示例状态，初值与更新时机见第 5 节
};

// 中文：算法配置；运行期间是否可变必须明确。
struct AlgorithmConfig
{
    double parameter{}; // 中文：参数含义、单位、范围和来源
};

// 中文：算法输出；不隐藏副作用。
struct AlgorithmOutput
{
    double value{}; // 中文：示例输出，单位 <unit>，坐标系 <frame>
};
```

不要保留与算法无关的 AFSIM 基类、工厂或日志类型。

## 4. 核心接口

```cpp
// 中文：初始化状态；失败策略见第 6 节。
AlgorithmState initialize(const AlgorithmInput& input,
                          const AlgorithmConfig& config);

// 中文：执行一个离散更新步；dt 单位为秒且必须满足约束。
AlgorithmOutput step(const AlgorithmInput& input,
                     double dt,
                     const AlgorithmConfig& config,
                     AlgorithmState& state);

// 中文：将状态恢复到可重复的初始条件。
void reset(AlgorithmState& state);
```

| API | 前置条件 | 后置条件 | 副作用 | 复杂度/实时性 |
| --- | --- | --- | --- | --- |
| `step` | <条件> | <条件> | 更新 `state` | <预算> |

## 5. 状态生命周期

| 状态 | 初值 | 读取时机 | 更新时机 | 重置规则 | 序列化/复制 |
| --- | --- | --- | --- | --- | --- |
| `<state>` | <value> | <timing> | <timing> | <rule> | <rule> |

## 6. 错误与边界

| 条件 | 检测位置 | API 行为 | 调用者责任 |
| --- | --- | --- | --- |
| 非法 `dt` | `step` 入口 | error/exception/status | <责任> |
| NaN/Inf | <位置> | <行为> | <责任> |
| 退化几何/矩阵 | <位置> | <行为> | <责任> |

## 7. AFSIM 到中性接口映射

| AFSIM 类型/状态/API | 中性类型/API | 转换 | 丢失信息 | 源码证据 |
| --- | --- | --- | --- | --- |
| `<AFSIM item>` | `<neutral item>` | <规则> | <none/list> | `path:start-end` |

## 8. 依赖替换

| AFSIM/第三方依赖 | 作用 | 保留/替换/移除 | 中性方案 | 风险 |
| --- | --- | --- | --- | --- |
| `<dependency>` | <作用> | <decision> | <方案> | <风险> |

## 9. 最小调用示例

```cpp
AlgorithmConfig config{/* 中文：填入已验证参数 */};
AlgorithmInput input{/* 中文：填入 SI 单位输入 */};
AlgorithmState state = initialize(input, config);

// 中文：以固定步长执行，并用独立 oracle 检查输出。
const AlgorithmOutput output = step(input, 0.01, config, state);
```

示例中的每个字段和步骤用中文说明；不要调用未在本规格声明的 API。

## 10. 验证契约

| 测试 | 输入 | Oracle | 容差/不变量 | 失败判据 |
| --- | --- | --- | --- | --- |
| 正常 | <fixture> | <expected> | <tolerance> | <condition> |
| 边界 | <fixture> | <expected> | <range> | <condition> |
| 序列/退化 | <fixture> | <expected> | <invariant> | <condition> |

## 11. 未决问题

| ID | 问题 | 影响 | 所需证据 | 是否阻塞实现 |
| --- | --- | --- | --- | --- |
| Q-001 | <问题> | <影响> | <证据> | yes/no |
