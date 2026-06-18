# 结构化缺口规格模板 — gap-specs.jsonl

> 使用说明：本模板描述 `workspace/requirements/gap-specs.jsonl` 中每行 JSON 对象的结构。  
> 生成时请严格遵循此模式，每行一个 JSON 对象，不可跨行。  
> 所有字段为必填，除非标注为可选。

## JSON 行模式 (Schema)

```json
{
  "fu_id": "FU-XXX",
  "req_ids": ["REQ-001", "REQ-002"],
  "name": "功能单元名称",
  "description": "该功能单元的详细描述，说明要解决的问题和实现目标。",
  "expected_signature": {
    "inputs": [
      {
        "name": "参数名",
        "type": "C++类型",
        "desc": "参数说明"
      }
    ],
    "outputs": [
      {
        "name": "返回值或输出参数名",
        "type": "类型",
        "desc": "说明"
      }
    ],
    "side_effects": ["修改的全局状态或成员变量说明，若无则为空数组"]
  },
  "afs_reference": {
    "function_name": "AFSIM源函数名（若 target_status 为 not_in_afsim，填空字符串）",
    "location": "文件路径:行号范围（若 target_status 为 not_in_afsim，填空字符串）",
    "class_name": "所属类（若为全局函数则为空字符串；若 target_status 为 not_in_afsim，填空字符串）",
    "dependency_summary": "依赖的关键 AFSIM 类型/宏/全局变量，用逗号分隔（若 target_status 为 not_in_afsim，填空字符串）"
  },
  "target_status": "missing / partial / not_in_afsim",
  "migration_approach": "direct_adaptation / partial_rewrite / cleanroom / novel",
  "coupling_assessment": "low / medium / high",
  "priority": "high / medium / low",
  "risks": ["风险1", "风险2"],
  "notes": "补充说明（可选）。对于 novel 迁移方式，需注明替代设计依据来源",
  "generated_at": "YYYY-MM-DD"
}
```

## 示例行

### 示例 1：AFSIM 有参考实现（cleanroom）
```json
{"fu_id":"FU-001","req_ids":["REQ-012"],"name":"六自由度刚体积分器","description":"使用RK4积分位置和四元数姿态更新","expected_signature":{"inputs":[{"name":"state","type":"RigidBodyState","desc":"当前刚体状态"},{"name":"forces","type":"Wrench","desc":"合外力与力矩"},{"name":"dt","type":"double","desc":"积分步长"}],"outputs":[{"name":"new_state","type":"RigidBodyState","desc":"更新后的状态"}],"side_effects":["归一化四元数"]},"afs_reference":{"function_name":"integrate_step","location":"src/kinematics/RigidBodyDynamics.cpp:45-89","class_name":"RigidBodyDynamics","dependency_summary":"Eigen, Quaternion, G_GRAVITY"},"target_status":"missing","migration_approach":"cleanroom","coupling_assessment":"low","priority":"high","risks":["姿态四元数归一化需验证多次迭代后的精度"],"notes":"目标系统已使用Eigen，接口适配工作量小","generated_at":"2026-06-15"}
```

### 示例 2：AFSIM 无参考实现（novel）
```json
{"fu_id":"FU-005","req_ids":["REQ-020"],"name":"新型传感器融合算法","description":"实现多源异构传感器数据的自适应加权融合，输出统一目标航迹","expected_signature":{"inputs":[{"name":"sensor_data_list","type":"vector<SensorData>","desc":"多源传感器数据列表"},{"name":"weights","type":"vector<double>","desc":"自适应融合权重"}],"outputs":[{"name":"fused_track","type":"Track","desc":"融合后的目标航迹"}],"side_effects":[]},"afs_reference":{"function_name":"","location":"","class_name":"","dependency_summary":""},"target_status":"not_in_afsim","migration_approach":"novel","coupling_assessment":"high","priority":"medium","risks":["无 AFSIM 参考实现，需从零设计算法架构","融合权重自适应调整的收敛性需理论验证"],"notes":"设计依据：[Bar-Shalom 2004] Estimation with Applications to Tracking and Navigation; AFSIM 索引搜索范围：core/function-index.jsonl + wsf_plugins/function-index.jsonl，未找到匹配函数","generated_at":"2026-06-16"}
```

### 编码规则

- 输出文件必须为 UTF-8 编码，不含 BOM。
- 每行必须是一个完整的合法 JSON 对象，不能有多余的换行符或空格。
- 字段值中如有双引号，需按 JSON 标准转义。
- 数组为空时写作 []，对象为空时写作 {}。