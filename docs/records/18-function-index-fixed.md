# function-index.jsonl 修复记录

**修复日期**：2026-06-24
**原文件备份**：`SaveFile/function-index-backup-20260624.jsonl`
**最终状态**：44484 行，39685 条 Method-level（原 50402 行，累计删除 5,918 条误标）

---

## 修复总览

| 修复类别 | 数量 | 严重度 | 操作 |
|----------|------|--------|------|
| 误标条目删除 | 5,918 | 🔴 严重 | 删除 |
| `return_type` 含 `static` 前缀 | ~1,296 | 🟡 中等 | 去除 `static ` 前缀 |
| 构造/析构函数 `return_type` 非空 | ~3,538 | 🔵 轻微 | 设为空字符串 |
| 行号范围修正 | ~16,000+ | 🟡 中等 | 精确定位到方法声明行 |

---

## 1. 误标删除明细（5,918条，分6轮）

### 第1轮：成员变量/初始化列表（13条）
- `mMover`, `mPlatform`, `mSensorName` — 成员变量被标为方法
- `yLabel` ×4 — 构造函数初始化列表 `, yLabel("y")`
- `boundaryCondition` ×4 — 初始化列表 `, boundaryCondition(0.0)`

### 第2轮：静态成员常量（18条）
- `cUPDATER_NAME` 系列：`Speed`, `Flow`, `Min`, `Max` ×12（`RvP6DOFData`, `RvSixDOF_Data`, `WkP6DOF_Data`, `WkSixDOF_Data`）
- `FromDegrees`, `FromRadians` ×2 — `static constexpr Angle`
- `max` ×4 — `static const ... cInvalidIndex = std::numeric_limits::max()`

### 第3轮：成员变量方法调用 / brace 初始化 / 花括号污染（~654条）
- `mEndMC{}` → `max`, `mVar.Set()` → `Set`, `mObservedSubjects.push_back()` → `push_back`
- return_type 含 `{` `}` 的被污染条目 ~640

### 第4轮：初始化列表 + 成员变量残余（26条）
- `speed(0.0)` ×3, `: QLineEdit(parent)` ×2, `: Buffer(b)`, `: UtException(...)`
- `mExecuteFn`, `mValue`, `mFunction`, `mCommName` ×2, `mServiceID` ×2, `mPlatformIndex`, `mLowestModeIndex`, `m_DestroyFunction`, `m_vBlendColor`, `m_stringrep`
- `_WSysID` ×2

### 第5轮：宏/代码语句误标（3,187条）
- `UT_DECLARE_SCRIPT_METHOD(...)` ×56 — 脚本注册宏被标为方法
- `WSF_REGISTER_EXTENSION(...)` ×2
- `throw ...` 语句, `emit ...` 信号, `std::move(...)`, `std::find(...)`, `QComboBox::showPopup()`, `notify(WARN)` 等

### 第6轮：代码语句误标（2,011条）
- `obj.method()` 链式调用、`auto x = ...`、`return ...`、`this->method()`
- `static_assert(...)`, `assert(...)`, `UtCallbackListN<void(...)>`
- 成员变量赋值 `= AeroTable2d(...)`, `= AeroTable4d(...)`, `= UtVec3dX(...)`

---

## 2. return_type 修复

### 2.1 static 前缀去除（~1,296条）
全文件批量处理，去除 `return_type` 字段中的 `static ` 存储类说明符。

### 2.2 构造/析构函数清空（~3,538条）
C++ 构造/析构函数无返回类型，`return_type` 设为空字符串。含两轮：批量修复（~2,258）+ 严格审计补修（~1,280）。

---

## 3. 行号范围修正（~16,000+条）

| 阶段 | 触发条件 | 修复方式 | 数量 |
|------|---------|---------|------|
| 批量处理 | `line_end - line_start > 20` | 正则匹配源文件方法声明行 | ~7,737 |
| 严格审计 | `line_start ≤ 10` + 源文件验证不通过 | 逐条验证重定位 | ~4,783 |
| 全量全面修复 | 上述所有 + span≤5 的短条目 | 统一扫描修复 | ~9,291 |

---

## 4. 检查方法演进

| 阶段 | 方法 | 发现的问题 |
|------|------|-----------|
| 初始检查 | mXxx前缀、static前缀、span>20、ctor/dtor | **严重不足**：Eclipse条目行号指向文件头未发现、return_type含变量名未发现 |
| 严格审计 | +return_type花括号、brief初始化列表模式、源文件行号验证 | 新发现~680条误标、~4,783条行号错误 |
| 全量修复 | 全文件static/ctor/line统一处理 | ~12,500条修复 |
| 去重分析 | qualified_name去重扫描 | 新发现~5,200条宏/代码语句误标 |

---

## 5. 修复后验证

```
文件行数: 44484（原 50402）
Method-level: 39685 条
Unique qualified_name: 36201（2,502 组为合法C++重载）

✅ member variable mislabels: 0
✅ static in return_type: 0
✅ line range > 20: 0
✅ constructor/destructor return_type: 0
✅ bad return_type (,/:): 0
✅ bad brief (method: ,): 0
✅ bad qualified_name: 0
✅ schema_version != 1: 0
```
