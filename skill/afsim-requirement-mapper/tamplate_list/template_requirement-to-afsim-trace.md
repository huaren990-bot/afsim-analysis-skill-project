# 需求追溯矩阵 — requirement-to-afsim-trace.md

> 使用说明：本模板用于生成 `docs/requirements/requirement-to-afsim-trace.md`。  
> 每条需求一行，记录需求 ID、需求描述、关联的 AFSIM 实现函数及生成的功能单元（FU）。  
> 请根据缺口分析结果，逐条填写以下表格，替换 `{...}` 占位内容。


<table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <thead>
    <tr style="background-color: #2c3e50; color: white; text-align: left;">
      <th style="padding: 10px; border: 1px solid #ddd; width: 8%;">需求 ID</th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 8%;">功能单元 ID</span></th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 28%;">需求描述</th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 15%;">AFSIM源函数<br><span style="font-weight:normal; font-size:12px; color:#bbb;">（类::方法）</span></th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 12%;">AFSIM文件路径:行号</th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 29%;">备注</th>
    </tr>
  </thead>
  <tbody>
    <!-- 示例行 1（可根据需要复制或删除） -->
    <tr style="background-color: #f9f9f9;">
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #e8f4f8; font-weight: bold;">REQ-XXX</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #fff3cd; font-weight: bold;">FU-XXX</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        <b>功能模块名称</b><br>
        <span style="font-size:13px; color:#333;">· 子功能描述：详细说明该功能的具体内容</span>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:13px;">
        <code>ClassName::methodName</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:12px;">
        <code>path/to/file.hpp</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-size:13px;">
        <span style="background-color: #dff0d8; padding:2px 6px; border-radius:4px; font-size:12px;">🔑 核心</span> 关键特性说明<br>
        <span style="color:#666; font-size:12px;">子项或补充信息</span><br>
        <span style="color:#c0392b; font-size:12px; background-color:#fdd; padding:0 4px;">⚠ 特殊情况/注意事项</span>
      </td>
    </tr>
    <!-- 可在此继续添加更多行 -->
  </tbody>
</table>


**填写要求**：
- 若一条需求对应多个 AFSIM 函数，可合并为多行或使用逗号分隔，并在备注中说明分工。
- 若某需求在 AFSIM 中找不到直接实现，AFSIM 源函数及路径列填写“无”，FU ID 仍须分配，并备注需 Clean-room 重实现。
- 所有 AFSIM 文件路径应相对于 `source_root/` 根目录。