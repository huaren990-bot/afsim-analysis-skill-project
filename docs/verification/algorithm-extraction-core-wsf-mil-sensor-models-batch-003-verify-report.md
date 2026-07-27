# `core/wsf_mil` 传感器物理模型第三批算法提取验证报告

> 日期：2026-07-23  
> 批次：`batch-003-core-wsf-mil-sensor-models`  
> 结论：**通过**

## 1. 范围与输入

本报告只验收第三批 7 条候选记录对应的 3 个物理算法：

1. `ALG-SENSORS-OTH-IONOSPHERIC-CHARACTERISTICS`
2. `ALG-SENSORS-OPTICAL-GLIMPSE-ANGULAR-CDF`
3. `ALG-SENSORS-SAR-DWELL-TIME`

验证输入：

| 文件 | SHA-256 |
| --- | --- |
| `workspace/source-index/function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `workspace/source-index/function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `workspace/algorithm-extraction/algorithm-candidates.jsonl` | `0b8bbc01060997ce6d0f550aa6f569724e932d2b8432b88e26aa71645c90729a` |
| `workspace/algorithm-extraction/algorithm-coverage.jsonl` | `adf0002e3c20767d49328f10c25f7510e71953c95ea30450bd142b46f1bed9e3` |
| `workspace/algorithm-extraction/batches/batch-003-core-wsf-mil-sensor-models.jsonl` | `75094fa723e25edd6b3c7545a7514c401c690fc62d142eb8769b61d012b07cb8` |

真实源码根为 `source_root/afsim-2_9`。本批核对的核心文件是
`WsfOTH_RadarSensor.cpp`、`WsfOpticalSensor.cpp`、`WsfSAR_Sensor.cpp`，
并补查相应头文件、调用者和 `UtRandom.hpp`。

## 2. 候选状态与覆盖率

全局分母保持 8,137 条候选：

| 状态 | 数量 |
| --- | ---: |
| extracted | 19 |
| rejected | 2 |
| deferred | 0 |
| selected | 0 |
| pending | 8,116 |

全局闭环率为 `21 / 8137 = 0.2581%`，不构成模块或 AFSIM 全量完成声明。

本批分母为 7 条候选：

| 物理算法 | 候选记录 | extracted | 说明 |
| --- | ---: | ---: | --- |
| OTH 电离层传播特性 | 3 | 3 | 同一真实嵌套类函数的三个索引所有者别名 |
| 光学角分离 CDF | 3 | 3 | 同一真实嵌套类函数的三个索引所有者别名 |
| SAR 驻留时间 | 1 | 1 | 索引遗漏 `SAR_Mode` 嵌套层 |
| 合计 | 7 | 7 | 3 个物理算法 |

本批闭环率 100%，没有 `pending`、`selected`、`rejected` 或 `deferred`。

## 3. 检查结果

| 检查项 | 结果 | 可复现证据 |
| --- | --- | --- |
| JSONL 解析与唯一性 | 通过 | candidates/coverage 各 8,137 条唯一 ID；batch-003 为 7 条唯一 ID |
| 批次状态闭环 | 通过 | 7 条均为 `extracted` 且 verification=`passed` |
| function/body 连接 | 通过 | 逐条按 `candidate_id + qualified_name + path + line range` 精确匹配 |
| 真实源码位置 | 通过 | 3 个源码路径存在，7 条行号均在文件范围内 |
| 嵌套类消歧 | 通过 | 卡片明确记录索引名称与真实 C++ 定义的差异 |
| 卡片完整性 | 通过 | 3 张卡均具备连续 1–10 节，无占位标记或省略文本 |
| 接口完整性 | 通过 | 3 份规格均具备连续 1–11 节，并声明不代表已有实现 |
| 数据与单位 | 通过 | 所有输入/输出映射到代码；无法由类型系统证明的 OTH 单位标为物理推断 |
| 随机性语义 | 通过 | `UtRandom.hpp:169-172` 证明本地 RNG 默认种子为 1；跨标准库风险已保留 |
| 调用者语义 | 通过 | SAR 核心硬上限和 `AttemptToDetect` 二次配置裁剪分别记录 |
| 产物链接 | 通过 | 新卡片、接口及全部 19 条历史/当前 extracted 产物路径存在 |
| Compendium | 通过 | 3 个新算法主条目各 1 次；传感器分类 8 项，总计 40 项 |
| Python 脚本语法 | 通过 | 两个算法账本脚本 `py_compile` 成功 |

## 4. 数值与边界复验

| 算法 | 独立输入 | 结果 | 判据 |
| --- | --- | --- | --- |
| OTH 电离层 | 纬度 30°、第 172 日 12 时、默认电离层、6 MHz | $n_e=322057190755.68854$ m⁻³（推断单位）；$f_c=5096157.443154109$ Hz；$f_{\min}=5249042.166448732$ Hz | 标量复算通过 |
| OTH 单跳范围 | 同上 | $i_{\max}=58.14208128741023°$；$R_{\min}=376367.0394286476$ m；$R_{\max}=3834484.6233969247$ m | 标量复算通过 |
| OTH 定义域 | 同上改为 20 MHz | 最小距离 `asin` 参数 `1.012556465356911`，确认为越界 | 风险分支通过 |
| OTH 夜侧 | 纬度 30°、第 172 日 24 时 | `cos(zenith)<=0` | 安全接口错误分支已定义 |
| 光学角 CDF | 0° 方位、0°..0° 俯仰、$N=7$ | `hist[0]=7`，其余 0；`cdf[0]=0`，其余 1 | 确定性退化 oracle 通过 |
| SAR 驻留时间 | 10 GHz、10 km、200 m/s、1 m、斜视 30°、擦地 45° | `2.119852800003833` s | 绝对误差 `<1e-15` |

数值 oracle 使用独立 JavaScript 标量实现，不调用 AFSIM 函数。光学正常随机样例以结构不变量验收，不把特定标准库的 `uniform_real_distribution` 输出误当作跨平台黄金值。

## 5. 缺陷清单

本批文档、账本和链接未发现阻断、严重、一般或轻微缺陷。

以下为已准确保留的上游模型风险，不属于本批产物缺陷：

1. OTH 夜侧把天顶角正割设为 `DBL_MAX`，随后进入溢出/下溢组合。
2. OTH 在载频不足或部分高频条件下，最小距离 `asin` 参数可超过 1。
3. OTH 电子温度与密度输入是裸数，正式单位需外部文档确认。
4. 光学 RNG 固定种子 1，但实数均匀分布的逐位输出依赖 C++ 标准库实现。
5. 光学角点积只保护大于等于 1 的上界，没有保护小于 -1 的舍入越界。
6. SAR 反向扫描分支绕过 1000 s 内部上限，并以“时间值”承载错误哨兵。
7. SAR 探测路径会再按配置上限裁剪，性能预测路径不会。

这些风险会阻塞不加适配的直接迁移，但不阻塞“源码行为、边界与未知已被准确提取”的验收。

## 6. 结论

第三批 7 条候选已全部闭环为 3 个独立算法。算法卡、接口规格、覆盖账本、真实源码、索引、Compendium 和独立数值验证一致，批次验收通过。全局仍有 8,116 条候选待处理。
