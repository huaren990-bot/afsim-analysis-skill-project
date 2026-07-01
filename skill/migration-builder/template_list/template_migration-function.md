# 结构化缺口规格模板 — <requirement_index>-migration-function.jsonl

> 使用说明：本模板描述 `workspace/migration/<requirement_index>/<requirement_index>-migration-function.jsonl` 中每行 JSON 对象的结构。  
> 生成时请严格遵循此模式，每行一个 JSON 对象，不可跨行。  
> 所有字段为必填，除非标注为可选。

## JSON 行模式 (Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "fu_id": { "type": "string", "description": "功能单元唯一标识，如 FU-001" },
    "function_name": { "type": "string", "description": "函数名称（代码中的标识符）" },
    "display_name": { "type": "string", "description": "函数中文/友好名称" },
    "description": { "type": "string", "description": "函数功能概述（一到两句话）" },
    "signature": { "type": "string", "description": "完整 C++ 函数签名（含参数和返回类型）" },

    "source_location": {
      "type": "object",
      "properties": {
        "exists_in_afsim": { "type": "boolean", "description": "AFSIM 中是否有参考实现" },
        "class_name": { "type": "string", "description": "所属类名（若无则空）" },
        "method_name": { "type": "string", "description": "方法名（与函数名一致或不同），与function-index.jsonl中的qualified_name保持一致" },
        "file": { "type": "string", "description": "源文件相对路径（AFSIM 或目标），与file-index.jsonl中的path保持一致" },
        "line_start": { "type": ["integer", "null"], "description": "起始行号" },
        "line_end": { "type": ["integer", "null"], "description": "结束行号" }
      },
      "required": ["exists_in_afsim"]
    },

    "interface": {
      "type": "object",
      "properties": {
        "parameters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string" },
              "pass_by": { "type": "string", "enum": ["value", "ref", "const ref", "pointer"] },
              "direction": { "type": "string", "enum": ["in", "out", "inout"] },
              "unit": { "type": "string", "description": "物理单位（如 m, s, rad, N）" },
              "constraints": { "type": "string", "description": "取值范围或约束条件" },
              "description": { "type": "string" }
            },
            "required": ["name", "type", "direction"]
          }
        },
        "return": {
          "type": "object",
          "properties": {
            "type": { "type": "string" },
            "unit": { "type": "string" },
            "description": { "type": "string" }
          },
          "required": ["type"]
        }
      },
      "required": ["parameters", "return"]
    },

    "side_effects": {
      "type": "object",
      "properties": {
        "modified_members": { "type": "array", "items": { "type": "string" } },
        "modified_globals": { "type": "array", "items": { "type": "string" } },
        "io_operations": { "type": "array", "items": { "type": "string" } },
        "exceptions": { "type": "array", "items": { "type": "string" } }
      },
      "default": { "modified_members": [], "modified_globals": [], "io_operations": [], "exceptions": [] }
    },

    "dependencies": {
      "type": "object",
      "properties": {
        "called_functions": { "type": "array", "items": { "type": "string" } },
        "data_tables": { "type": "array", "items": { "type": "string" } },
        "global_constants": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string" },
              "source": { "type": "string" },
              "description": { "type": "string" }
            }
          }
        },
        "types": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "definition": { "type": "string" },
              "source": { "type": "string" }
            }
          }
        }
      },
      "default": { "called_functions": [], "data_tables": [], "global_constants": [], "types": [] }
    },
    
    "notes": { "type": "array", "items": { "type": "string" }, "description": "补充说明（警告、注意事项）" }

  },
  "required": ["fu_id", "function_name", "display_name", "description", "source_location", "interface"]
}
```

## 示例行

```json
{
  "fu_id": "FU-001",
  "function_name": "mapRouteSegment",
  "display_name": "航路段映射（仅向前搜索）",
  "description": "确定飞机在航线中的位置——所在航路段序号和段内归一化进度。仅向前搜索，O(1) 复杂度。",
  "signature": "std::pair<int, double> mapRouteSegment(const std::vector<Point>& path, const Point& cur_pos, double dt, double V);",

  "source_location": {
    "exists_in_afsim": true,
    "class_name": "wsf::six_dof::PointMassControlActuator",
    "method_name": "wsf::six_dof::PointMassControlActuator::Initialize",
    "file": "afsim-2_9/swdev/src/wsf_plugins/wsf_six_dof/source/WsfPointMassSixDOF_ControlActuator.hpp",
    "line_start": 40,
    "line_end": 40
  },

  "interface": {
    "parameters": [
      {
        "name": "path",
        "type": "const std::vector<Point>&",
        "pass_by": "const ref",
        "direction": "in",
        "unit": "m (经纬高)",
        "constraints": "size ≥ 2",
        "description": "期望航线航路点数组"
      },
      {
        "name": "cur_pos",
        "type": "const Point&",
        "pass_by": "const ref",
        "direction": "in",
        "unit": "m",
        "constraints": "有效地理坐标",
        "description": "飞机当前位置"
      },
      {
        "name": "dt",
        "type": "double",
        "pass_by": "value",
        "direction": "in",
        "unit": "s",
        "constraints": "(0, 1.0]",
        "description": "仿真步长"
      },
      {
        "name": "V",
        "type": "double",
        "pass_by": "value",
        "direction": "in",
        "unit": "m/s",
        "constraints": "[0, ∞)",
        "description": "飞机当前速度"
      }
    ],
    "return": {
      "type": "std::pair<int, double>",
      "unit": "N/A",
      "description": "first=current_leg_index (int), second=leg_progress (double ∈ [0,1])"
    }
  },

  "side_effects": {
    "modified_members": [
      "prev_leg_index_ (内部状态，记录上一帧航段索引，用于 O(1) 搜索)"
    ],
    "modified_globals": [],
    "io_operations": [],
    "exceptions": ["无异常抛出，错误时返回默认值 (0, 0.0)"]
  },

  "dependencies": {
    "called_functions": [],
    "data_tables": [],
    "global_constants": [],
    "types": [
      {
        "name": "Point",
        "definition": "struct Point { double _lon; double _lat; double _alt; }",
        "source": "types.h"
      }
    ]
  },

  "notes": [
    "Point 经纬高单位均为米，已确认。",
    "小范围平面近似足够，大跨度时需启用曲率模式（通过 use_curvature 标志）。"
  ]
}
```


### 编码规则

- 输出文件必须为 UTF-8 编码，不含 BOM。
- 每行必须是一个完整的合法 JSON 对象，不能有多余的换行符或空格。
- 字段值中如有双引号，需按 JSON 标准转义。
- 数组为空时写作 []，对象为空时写作 {}。