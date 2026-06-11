# 11 — afsim-algorithm-extractor Skill 完善记录

**日期**：2026-06-11
**状态**：完成
**关联 Skill**：`afsim-algorithm-extractor`
**触发来源**：第二轮 wsf_space + wsf_six_dof + wsf_p6dof 算法提取过程中发现系统性质量问题

---

## 背景

在完成第一轮 8 张 wsf_space 算法卡片后，经过审查发现以下系统性质量问题：
1. 部分卡片存在算法杂揉（多算法混在一张卡片中）
2. 部分算法被遗漏（wsf_six_dof 模块的刚体积分器、气动、推进、飞控等）
3. 卡片命名不统一（混用模块名前缀和算法名前缀）
4. 模块归属错误（wsf_six_dof 算法被标注为 wsf_p6dof）
5. 变量表格中"所属函数 (Method)"列使用了非 function-index 中的函数名

上述问题在修正过程中又发现了更深层的遗漏（wsf_six_dof 5 个高优先级子系统、wsf_space 2 个遗漏算法），总计经历了 3 轮修正才达到完整覆盖。

为避免下次使用本 skill 时重复出现同类问题，对 `skill/afsim-algorithm-extractor/SKILL.md` 进行了系统性完善。

---

## SKILL.md 新增章节明细

### 1. 「算法识别与分类准则」（新增一级章节，位于"核心能力与限制"之后）

#### 1.1 模块归属验证
- 从 function-index.jsonl 的 `path` 字段确认模块名
- 对照 `source_root/src/<模块>/` 验证
- 注意 `wsf_p6dof` 和 `wsf_six_dof` 同名类混淆
- 附已知模块清单（core/wsf_plugins 两个索引目录下的 3 个模块）

#### 1.2 算法粒度准则（一张卡片 = 一个算法）
- 4 条拆分准则：
  1. 数值积分方法 ⊥ 控制算法
  2. 边界值问题 ⊥ 初轨确定
  3. 不同物理机制的模型
  4. 经典机动 ⊥ 最优瞄准
- 4 个反面示例（禁止出现的杂揉）

#### 1.3 算法命名规范
- `<domain>-<algorithm>-card.md` 格式规范
- 已知 domain 清单（`flight-dynamics`、`space`）

#### 1.4 算法完整性检查（三步法）
1. math 标记全覆盖
2. 源文件扫描
3. 模块间对等检查

### 2. 执行步骤补充（在原有 7 步基础上增强）

| 步骤 | 原有内容 | 新增内容 |
|------|---------|---------|
| 步骤 1 | 接收 function-index | + 确认模块归属（从 path 字段）+ 优先处理 math 标记 |
| 步骤 4 | 构建符号映射 | + Method 列必须使用 function-index.jsonl 函数名，私有方法需向上映射 |
| 步骤 5 | 撰写算法卡片 | + 检查算法粒度 + 检查命名规范 |
| 步骤 6 | 汇总 | + 按模块/领域双维度组织 + 统计 math 覆盖 |
| 步骤 7 | 过程留痕 | + 记录模块归属确认依据、粒度决策、math 覆盖结果 |
| **步骤 8** | **（新增）** | **自检：Method 列检查、命名规范检查、杂揉检查、compendium 遗漏检查** |

### 3. 「常见错误与预防」（新增一级章节，位于"执行步骤"之后）

| 编号 | 错误名称 | 表现 | 根因 | 预防 |
|------|---------|------|------|------|
| 1 | 模块归属错误 | wsf_six_dof 算法标为 wsf_p6dof | 同名类混淆 | 始终从 function-index path 确认 |
| 2 | 算法杂揉 | 多算法打包在一张卡片 | 源码中共用外层类 | "独立教材"判断标准 |
| 3 | 算法遗漏 | 只提取积分器漏掉气动等 | 只关注传播函数 | 三步完整性检查 |
| 4 | Method 列非索引名 | 使用 SGP4_init, TakeStep 等 | 直接使用 C++ 私有方法名 | 与 function-index 交叉核对 |
| 5 | 命名不一致 | p6dof- vs pointmass- 混用 | 未统一 domain 前缀 | 先定 domain 再定 algorithm |
| 6 | 遗漏 Method 列 | 简单卡片缺少表格 | 对模板理解不一致 | 六列完整性检查 |

---

## 实际修正历程（本轮算法提取）

| 轮次 | 问题 | 操作 | 卡片数变化 |
|------|------|------|-----------|
| 初始 | — | 创建 8 张 wsf_space 卡片 | 8（+3 已有飞行动力 = 11） |
| 第 1 轮 | Method 列不规范 | 修正 8 张卡片的 Method 列 | 11 |
| 第 2 轮 | 缺少刚体积分器 + 命名不规范 | 新建刚体卡片 + 重命名 3 张飞行动力卡片 | 12 |
| 第 3 轮 | 4 张杂揉 + 7 个遗漏 | 拆分 4 张 + 新增 7 张（wsf_six_dof×5 + wsf_space×2） | 23 |

最终产出：23 张算法卡片、7 份接口规格、1 份汇总文档、11 份过程记录。

---

## 关联文件

- `skill/afsim-algorithm-extractor/SKILL.md` — 完善后的 skill 文档（57 行 → 168 行）
- `docs/records/10-wsf-space-algorithm-extraction.md` — 本轮空间算法提取记录
- `docs/records/09-algorithm-extraction-kickoff.md` — 首轮算法提取记录
- `docs/algorithms/CompendiumofAlgorithms.md` — 23 张卡片的汇总文档
