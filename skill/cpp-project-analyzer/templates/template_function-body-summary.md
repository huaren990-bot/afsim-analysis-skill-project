# function-body-summary.jsonl

## 要求

一行一个函数体的摘要。每个函数体的关键算法步骤用中文描述，帮助下游算法提取 Agent 快速定位数值计算密集区域。

## 必填字段

- `schema_version`：固定为 `1`。
- `qualified_name`：函数限定名，必须与 function-index.jsonl 中的 qualified_name 一致。
- `path`：函数定义所在相对路径。
- `line_start`、`line_end`：函数体行号范围。
- `body_line_count`：函数体行数。
- `control_flow_summary`：控制流摘要（中文）。描述主要分支、循环结构。
- `key_variables`：关键变量数组，每个含：
  - `name`：变量名。
  - `type`：数据类型。
  - `role`：`input` | `output` | `intermediate` | `state` | `constant`。
  - `brief`：变量用途（中文）。
- `computation_density`：`high` | `medium` | `low` — 数值计算的密集程度。
  - `high`：包含大量数学运算、矩阵运算、迭代求解、物理模型计算。
  - `medium`：包含一些数学运算但以逻辑控制为主。
  - `low`：主要是 getter/setter、简单赋值、接口转发。
- `math_operations`：涉及的数学运算类型数组。可选值：`matrix_multiply`、`matrix_inverse`、`vector_math`、`integration`、`interpolation`、`optimization`、`root_finding`、`trigonometry`、`statistics`、`coordinate_transform`、`random_sampling`、`linear_solve`、`none`。
- `calls_summary`：调用的关键函数列表（qualified_name 数组）。
- `algorithm_pattern`：可识别的算法模式。如 `KalmanFilter`、`RungeKutta`、`NewtonRaphson`、`MonteCarlo`、`PID_Control`、`StateMachine`、`unknown`。
- `evidence_level`：证据等级。
