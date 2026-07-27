# 2026-07-23 `core/wsf_mil` 传感器物理模型第三批算法提取记录

## 1. 目标与范围

在前两批 5 个被动声学算法完成后，继续按候选优先级提取 3 个独立传感器物理算法：

1. OTH 电离层传播特性；
2. 光学掠视角分离 Monte Carlo CDF；
3. SAR 方位分辨率驻留时间。

范围限定为：

- `WsfOTH_RadarSensor.cpp:1000-1089`
- `WsfOpticalSensor.cpp:625-697`
- `WsfSAR_Sensor.cpp:2133-2162`
- 为确认参数、随机数和调用边界而读取的头文件与调用者。

本记录不声明 `core/wsf_mil` 或 AFSIM 全量完成。

## 2. 输入

| 输入 | SHA-256 / 状态 |
| --- | --- |
| `workspace/source-index/function-index.jsonl` | `2fb5ee9dd066ace8fe22299a7440094ea7e06bf7e341bc47e2b61bec82c746fc` |
| `workspace/source-index/function-body-summary.jsonl` | `a979efc1629d797500fde2ddd0ae7cb3c57db2d6b2abed79e9ace41b3eed6113` |
| `workspace/algorithm-extraction/algorithm-candidates.jsonl` | 8,137 条 |
| AFSIM 源码 | `source_root/afsim-2_9` |
| 批次决策 | `batch-003-core-wsf-mil-sensor-models.jsonl`，7 条 |

按仓库 `AGENTS.md` 约束，三个核心函数均先通过 CodeGraph 获取源码和调用路径，再读取真实文件确认参数、默认值与边界。

## 3. 处理结果

| 指标 | 数量 |
| --- | ---: |
| 批次候选记录 | 7 |
| extracted | 7 |
| rejected/deferred | 0 |
| 提取的物理算法 | 3 |

候选多于算法的原因是：

- OTH 函数被索引为 `OTH_Beam`、`OTH_Mode` 和外层 `WsfOTH_RadarSensor` 三个所有者；
- 光学函数被索引为 `GlimpseProbability`、`OpticalMode` 和外层 `WsfOpticalSensor` 三个所有者；
- 真实源码分别只有一个嵌套类实现。

## 4. 产物

- 算法卡：
  - `docs/algorithms/sensors-oth-ionospheric-characteristics-card.md`
  - `docs/algorithms/sensors-optical-glimpse-angular-cdf-card.md`
  - `docs/algorithms/sensors-sar-dwell-time-card.md`
- 对应的 3 份中性接口规格；
- `workspace/algorithm-extraction/batches/batch-003-core-wsf-mil-sensor-models.jsonl`；
- 更新候选/覆盖账本；
- 更新 `docs/algorithms/CompendiumofAlgorithms.md`：
  - 当前候选流程验证算法由 5 项增至 8 项；
  - 加 32 项历史结果后汇编总数由 37 增至 40；
- 验证报告：
  `docs/verification/algorithm-extraction-core-wsf-mil-sensor-models-batch-003-verify-report.md`。

## 5. 关键提取决策

### 5.1 OTH 电离层

- 保留源码的太阳几何、Chapman 型电子密度和球形地球单跳范围为一个耦合算法。
- 明确电子密度 m⁻³、温度 K 是物理推断，不伪装成类型系统已证明的单位。
- 不把夜侧 `DBL_MAX` 链和 `asin` 越界美化为正常数值；中性接口以状态码暴露。

### 5.2 光学角分离 CDF

- 确认 `ut::Random` 的成员默认值为种子 1 和 `std::mt19937{1}`，每次函数调用都会重置。
- 不用某个标准库的随机样本序列作为跨平台黄金值。
- 接口同时提供显式 seed 与 U01 流注入边界，以支持兼容或跨语言复验。

### 5.3 SAR 驻留时间

- 区分核心公式的 1000 s 硬上限、反向扫描哨兵和 `AttemptToDetect` 的配置上限裁剪。
- `mGroundSpeed` 按真实生成逻辑解释为完整 NED 速度模，不按名称擅自改成水平速度。
- 中性输出同时给出未裁剪、源码兼容和调用者裁剪三层结果。

## 6. 覆盖状态

回写后全局状态：

| 状态 | 数量 |
| --- | ---: |
| extracted | 19 |
| rejected | 2 |
| pending | 8,116 |
| selected/deferred | 0 |

全局闭环率 `0.2581%`。第三批自身 7/7 闭环。

## 7. 验证

- candidates/coverage 各 8,137 条、ID 唯一、JSONL 可解析。
- 7 条批次记录逐条回连 function index、body summary 和真实源码。
- 3 张卡和 3 份接口分别满足 10 节与 11 节输出契约。
- 19 条累计 extracted 候选均存在卡片、接口和 `passed` 验证状态。
- Compendium 新算法各一个主条目，汇编总数 40。
- OTH、光学退化 CDF 和 SAR 数值/边界 oracle 通过。
- 两个 Python 账本脚本 `py_compile` 通过。

验收结论：通过。

## 8. 未决问题

| ID | 问题 | 影响 | 下一步 |
| --- | --- | --- | --- |
| SENSOR-003-001 | OTH 电子温度/密度正式单位 | 阻塞无条件迁移 | 核对用户手册或模型参考 |
| SENSOR-003-002 | OTH 夜侧模型和最小距离越界 | 可能产生 NaN/平台差异 | 建立黄金场景并确认修正策略 |
| SENSOR-003-003 | 光学随机数是否要求跨标准库逐位一致 | 决定 RNG 接口 | 固化部署编译器或规范 U01 映射 |
| SENSOR-003-004 | 光学下游 180° 插值边界 | 潜在越界 | 审计配置范围与调用数据 |
| SENSOR-003-005 | SAR 两条调用链的最大驻留时间语义 | 探测/预测结果不一致 | 用需求和回归场景确定契约 |
| SENSOR-003-006 | SAR 三维速度模是否为预期 | 高爬升/俯冲精度 | 核对参考公式与黄金数据 |
