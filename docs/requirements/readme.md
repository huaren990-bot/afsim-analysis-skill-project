[用户] 模糊需求描述文档`external_requirement_doc/`
    ↓
[requirement-spec-generator] 
    → 读取 AFSIM 认知资产
    → 生成待确认需求规范文档（含复选框/选项）`structured_requirement_doc/`
    ↓
[人工] 勾选必须/可选、选择简化/详细、确认优先级`structured_requirement_confirm/`
    ↓
[gap-analyzer]
    → 读取确认后规范
    → 映射到 AFSIM 功能 + 对比目标系统
    → 生成缺口报告 + 映射矩阵`structured_requirement_doc/`
    ↓
[下游] 代码迁移 Agent