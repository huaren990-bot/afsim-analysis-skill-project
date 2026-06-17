# 需求追溯矩阵 — requirement-to-afsim-trace.md

> **日期**：2026-06-16
> **来源需求规范**：`docs/requirements/structured_requirement_confirm/REQ-001-requirement-six-dof-UAV.md`
> **说明**：本矩阵展示每条需求与 AFSIM 源码实现函数及生成的功能单元（FU）之间的追溯关系。
<table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <thead>
    <tr style="background-color: #2c3e50; color: white; text-align: left;">
      <th style="padding: 10px; border: 1px solid #ddd; width: 8%;">需求 ID</th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 8%;">功能单元<br><span style="font-weight:normal; font-size:12px; color:#bbb;">FU ID</span></th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 28%;">需求描述</th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 15%;">AFSIM 源函数<br><span style="font-weight:normal; font-size:12px; color:#bbb;">（类::方法）</span></th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 12%;">AFSIM 文件路径:行号</th>
      <th style="padding: 10px; border: 1px solid #ddd; width: 29%;">备注</th>
    </tr>
  </thead>
  <tbody>
    <!-- 行 1: FU-001 -->
    <tr style="background-color: #f9f9f9;">
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #e8f4f8; font-weight: bold;">REQ-001</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #fff3cd; font-weight: bold;">FU-001</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        <b>六自由度模型计算无人机姿态和轨迹</b><br>
        <span style="font-size:13px; color:#333;">· 推进系统与燃油管理：根据燃油流量和飞行状态计算推力并更新燃油量</span>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:13px;">
        <code>PointMassPropulsionSystem::updateThrust</code><br>
        <code>PointMassPropulsionSystem::updateFuel</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:12px;">
        <code>wsf_six_dof/source/<br>WsfPointMassSixDOF_PropulsionSystem.hpp</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-size:13px;">
        <span style="background-color: #dff0d8; padding:2px 6px; border-radius:4px; font-size:12px;">🔑 核心</span> 喷气发动机推力模型<br>
        <span style="color:#666; font-size:12px;">含三层查表 Idle/Mil/AB + spool dynamics</span><br>
        <span style="color:#666; font-size:12px;">多油箱传输 + CG 插值</span><br>
        <span style="color:#c0392b; font-size:12px; background-color:#fdd; padding:0 4px;">⚠ Clean-room 重实现</span>
      </td>
    </tr>
    <!-- 行 2: FU-002 -->
    <tr style="background-color: #ffffff;">
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #e8f4f8; font-weight: bold;">REQ-001</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #fff3cd; font-weight: bold;">FU-002</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        <span style="font-size:13px; color:#333;">· 气动模型：根据飞行状态计算气动六分量（升力/阻力/侧力/滚转/俯仰/偏航力矩）</span>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:13px;">
        <code>RigidBodyAeroCoreObject::calculateAero</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:12px;">
        <code>wsf_six_dof/source/<br>WsfRigidBodySixDOF_AeroCoreObject.hpp</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-size:13px;">
        <span style="background-color: #dff0d8; padding:2px 6px; border-radius:4px; font-size:12px;">🔑 核心</span> RigidBody 稳定性导数气动系数模型<br>
        <span style="color:#666; font-size:12px;">高维查表 Ma×α×β×p×q×r</span><br>
        <span style="color:#666; font-size:12px;">动压 × 参考面积/长度缩放</span><br>
        <span style="color:#c0392b; font-size:12px; background-color:#fdd; padding:0 4px;">⚠ Clean-room 重实现</span>
      </td>
    </tr>
    <!-- 行 3: FU-003 -->
    <tr style="background-color: #f9f9f9;">
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #e8f4f8; font-weight: bold;">REQ-001</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #fff3cd; font-weight: bold;">FU-003</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        <span style="font-size:13px; color:#333;">· 六自由度积分器：使用 Heun 预测-校正法进行时间推进，更新位置/速度/姿态/角速度</span>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:13px;">
        <code>RigidBodySixDOF_Mover::integrate</code><br>
        <span style="font-size:12px; color:#888;">（刚体 Heun 积分器）</span>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:12px;">
        <code>wsf_six_dof/source/<br>WsfRigidBodySixDOF_Mover.hpp</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-size:13px;">
        <span style="background-color: #dff0d8; padding:2px 6px; border-radius:4px; font-size:12px;">🔑 核心</span> 刚体六自由度 Heun 积分器<br>
        <span style="color:#666; font-size:12px;">预测-校正法 + 四元数姿态积分</span><br>
        <span style="color:#666; font-size:12px;">欧拉转动方程含转动惯量张量</span><br>
        <span style="color:#c0392b; font-size:12px; background-color:#fdd; padding:0 4px;">⚠ Clean-room 重实现</span>
      </td>
    </tr>
    <!-- 行 4: FU-004 -->
    <tr style="background-color: #ffffff;">
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #e8f4f8; font-weight: bold;">REQ-001</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; background-color: #fff3cd; font-weight: bold;">FU-004</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        <span style="font-size:13px; color:#333;">· 姿态控制系统 SAS：控制-稳定解耦，将控制指令转化为角加速度</span>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:13px;">
        <code>PointMassSAS::computeAngularAcceleration</code><br>
        <span style="font-size:12px; color:#888;">（PointMass 稳定增稳系统）</span>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-family: 'Courier New', monospace; font-size:12px;">
        <code>wsf_six_dof/source/<br>WsfPointMassSixDOF_FlightControlSystem.hpp</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; font-size:13px;">
        <span style="background-color: #dff0d8; padding:2px 6px; border-radius:4px; font-size:12px;">🔑 核心</span> 三通道控制-稳定解耦 SAS<br>
        <span style="color:#666; font-size:12px;">一阶指令跟踪 + 二阶临界阻尼稳定项</span><br>
        <span style="color:#666; font-size:12px;">各通道独立限幅</span><br>
        <span style="color:#c0392b; font-size:12px; background-color:#fdd; padding:0 4px;">⚠ Clean-room 重实现</span>
      </td>
    </tr>
  </tbody>
</table>

