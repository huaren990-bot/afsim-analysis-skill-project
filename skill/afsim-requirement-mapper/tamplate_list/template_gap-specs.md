// workspace/requirements/gap-specs.jsonl 中的一条记录
{
  "fu_id": "FU-003",
  "req_id": "REQ-001",
  "requirement_text": "六自由度刚体运动模型（四元数）",
  "afs_source": {
    "function_name": "integrate_step",
    "location": "src/kinematics/RigidBodyDynamics.cpp:45-89",
    "class_name": "RigidBodyDynamics"
  },
  "target_status": "缺失",
  "expected_signature": {
    "inputs": ["state: RigidBodyState", "forces: Wrench", "dt: double"],
    "outputs": ["new_state: RigidBodyState"]
  },
  "migration_suggestion": "直接适配（移除AFSIM日志，替换状态结构体）",
  "priority": "高"
}