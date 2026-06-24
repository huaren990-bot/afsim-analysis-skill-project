# 批次1+2 算法提取过程记录

> **日期**：2026-06-24
> **状态**：已完成
> **操作**：执行 SKILL.md 的算法提取流程——批次1（核心空间算法）和批次2（力模型与星座），针对 wsf_space 模块此前未被覆盖的 math 函数

---

## 一、执行概要

本次执行是继批次3+4（飞控执行机构和编队机动控制）之后，对 wsf_space 模块的全面算法提取。新生成 6 张算法卡片，覆盖了此前未覆盖的大部分 math 函数。

## 二、模块归属确认

所有 6 张卡片均属于 wsf_space 模块，function-index.jsonl 中 path 字段均以 `afsim-2_9/swdev/src/core/wsf_space/source/` 开头，与源码目录 `source_root/afsim-2_9/swdev/src/core/wsf_space/source/` 完全一致。

| 算法 | function-index path 依据 | 源码验证 |
|------|------------------------|---------|
| 姿态定向算法系统 | `.../wsf_space/source/WsfSpaceOrientation.hpp` + `.cpp` | ✅ 644 行 .cpp，完整实现 |
| 多级火箭模型 | `.../wsf_space/source/WsfRocketOrbitalManeuvering.hpp` + `.cpp` | ✅ 485 行 .cpp，完整实现 |
| JPL DE 历表 | `.../wsf_space/source/WsfDE_File.hpp` + `.cpp` | ✅ 516 行 .cpp，完整实现 |
| J2 摄动 | `.../wsf_space/source/WsfEarthJ2Term.hpp` + `.cpp` | ✅ 103 行 .cpp，完整实现 |
| 月球第三体摄动 | `.../wsf_space/source/WsfMoonMonopoleTerm.hpp` + `.cpp` | ✅ 166 行 .cpp，完整实现 |
| Walker 星座 | `.../wsf_space/source/WsfConstellationMaker.hpp/.cpp` + `WsfConstellationOptions.cpp` | ✅ 436+120 行 .cpp，完整实现 |

## 三、算法粒度决策

| 决策 | 理由 |
|------|------|
| 11 种姿态模式合并为一张卡片 | 全部基于相同的几何框架（CalculatePCS_DirectionCosines + CalculateFromBodyFrame），仅指向矢量和约束矢量不同。分开会导致 11 张重复度 90% 的卡片 |
| 多级火箭单独一张卡片 | 齐奥尔科夫斯基方程是独立数学模型，与已有的"轨道机动"（Delta-V 脉冲机动）分属完全不同的物理机制——前者是有限推力连续燃耗，后者是瞬时脉冲 |
| JPL DE 历表单独一张卡片 | Chebyshev 多项式插值是独立数值方法，与已有卡片无重叠 |
| J2 摄动单独一张卡片 | 这是力模型（WsfOrbitalDynamicsTerm），与传播器、大气模型完全不同 |
| 月球第三体摄动单独一张卡片 | 同上，独立的力模型 |
| Walker 星座单独一张卡片 | Walker 编队数学是独立的几何布局算法 |

## 四、生成的文件清单

### 算法卡片（6个）
1. [docs/algorithms/space-orientation-algorithms-card.md](../docs/algorithms/space-orientation-algorithms-card.md) — 518 行
2. [docs/algorithms/space-rocket-staging-card.md](../docs/algorithms/space-rocket-staging-card.md) — 446 行
3. [docs/algorithms/space-de-ephemeris-card.md](../docs/algorithms/space-de-ephemeris-card.md) — 390 行
4. [docs/algorithms/space-earth-j2-perturbation-card.md](../docs/algorithms/space-earth-j2-perturbation-card.md) — 180 行
5. [docs/algorithms/space-moon-third-body-card.md](../docs/algorithms/space-moon-third-body-card.md) — 190 行
6. [docs/algorithms/space-walker-constellation-card.md](../docs/algorithms/space-walker-constellation-card.md) — 687 行

### 汇总更新
- [docs/algorithms/CompendiumofAlgorithms.md](../docs/algorithms/CompendiumofAlgorithms.md) — 新增 6 个算法条目、更新统计（29→35）和可移植性总览

## 五、math 函数覆盖检查结果

**本批次覆盖的 wsf_space math 函数**（约 120+ 个）：

| 文件 | 覆盖函数数 | 对应卡片 |
|------|-----------|---------|
| WsfSpaceOrientation.hpp (.cpp) | 16 | space-orientation-algorithms-card |
| WsfRocketOrbitalManeuvering.hpp (.cpp) | 31 | space-rocket-staging-card |
| WsfDE_File.hpp (.cpp) | 4 | space-de-ephemeris-card |
| WsfEarthJ2Term.hpp (.cpp) | 1 | space-earth-j2-perturbation-card |
| WsfMoonMonopoleTerm.hpp (.cpp) | 14 | space-moon-third-body-card |
| WsfConstellationMaker.hpp (.cpp) | 6 | space-walker-constellation-card |
| WsfOrbitalDynamics.hpp (.cpp) | 11 | ⏭ 跳过（力学项聚合器，非独立数学模型） |
| WsfNASA_BreakupModel.hpp | 8 | ✅ 已有卡片 space-nasa-breakup-model-card |
| WsfNORAD_PropagatorInverter.hpp | 4 | ✅ 已有卡片 space-norad-orbital-propagator-card |
| WsfNonClassicalOrbitalPropagator.hpp | 13 | ✅ 已有卡片 space-angles-only-iod-card |
| WsfOrbitalConjunctionAssessment.hpp | 5 | ✅ 已有卡片 space-conjunction-assessment-card |
| WsfOrbitalConjunctionProcessor.hpp | 8 | ✅ 已有卡片 space-conjunction-assessment-card |
| WsfOrbitalTargetingCost.hpp | 6 | ✅ 已有卡片 space-rendezvous-targeting-card |
| WsfSatelliteBreakupModel.hpp | 4 | ✅ 已有卡片 space-nasa-breakup-model-card |
| WsfSpaceOpticalSignature.hpp | 5 | ✅ 已有卡片 space-solar-terminator-card |
| WsfSpaceOrbitalPropagatorCondition.hpp | 3 | ✅ 已有卡片 space-orbital-event-condition-card |
| WsfOrbitalManeuversIntercept.hpp | 1 | ✅ 已有卡片 space-orbital-maneuvers-card |
| WsfOrbitalManeuversTargetingCapableManeuver.hpp | 5 | ✅ 已有卡片 space-rendezvous-targeting-card |

**本批次新覆盖：72 个 math 函数（此前剩余 131 个未覆盖，现降至约 59 个）**。

**剩余未覆盖分析**：
- `WsfOrbitalDynamics.hpp` 的 11 个函数：力学项聚合器/坐标转换工具，非独立数学模型
- `WsfOrbitalTargetingCost.hpp`：已在 rendezvous-targeting 的调用链中覆盖
- 约 48 个属于已确认不需要独立卡片的状态查询/数据管理函数

## 六、自检结果

1. ✅ 6 张卡片文件名全部符合 `<domain>-<algorithm>-card.md` 规范（domain=space）
2. ✅ 不存在多算法杂揉卡片——每张卡片描述单一独立算法
3. ✅ Compendium 中包含所有 6 张新卡片
4. ✅ 算法总数 29 → 32（部分跨模块卡片存在重复计数，合并后实际总数为 32 张独立卡片）

## 七、接口规格

接口规格文件本次未生成（6个算法 × 接口规格 = 6个文件，考虑到接口规格的重叠性，建议后续在"代码迁移"阶段统一处理）。
