# MX004 — AFSIM Reference Implementation Evidence Summary

| # | MX004 功能 | AFSIM 参考 | 覆盖度 |
|---|-----------|-----------|--------|
| 1 | 空中机动 | `WsfAirMover` (wsf/source/mover/WsfAirMover.hpp) extends `WsfWaypointMover` → `WsfRouteMover` → `WsfMover`. 航路点飞行 + 起降/HAT计算/地面碰撞/毁伤评估. 关联算法: flight-dynamics-pointmass-integrator-card.md | ✅ |
| 2 | 陆上机动 | `WsfGroundMover` (wsf/source/mover/WsfGroundMover.hpp) extends `WsfWaypointMover` → `WsfRouteMover` → `WsfMover`. 地面航路点运动 + 地形跟随. | ✅ |
| 3 | 导弹机动 | `WsfGuidedMover` (wsf_mil/source/mover/WsfGuidedMover.hpp) extends `WsfGuidedMoverBase`. 制导飞行器运动 + RK2/RK4积分 + 多级推进 + TVC. 关联算法: flight-dynamics-pointmass-integrator-card.md, space-rocket-staging-card.md | ✅ |
| 4 | 可见光探测 | `WsfEOIR_Sensor` (wsf_mil/source/sensor/WsfEOIR_Sensor.hpp) with `EOIR_Mode`/`EOIR_ErrorModel`/`EOIR_SensorScheduler`. 无多模式自动切换机制 | ⚠️ |
| 5 | 雷达探测 | `WsfRadarSensor` (wsf/source/sensor/WsfRadarSensor.hpp) + `RadarBeam`/`RadarMode` + Marcum-Swerling 检测器 + 杂波模型. `WsfESM_Sensor`(无源). | ✅ |
| 6 | 惯性导航 | AFSIM 无独立 INS 组件. 需从外部领域文献设计. | 🆕 |
| 7 | 自杀攻击 | 可由 `WsfGuidedMover` + `WsfMobilityAndFirepowerLethality` + `WsfAirTargetFuse`/`WsfGroundTargetFuse` 组合实现. AFSIM 无专用"自杀无人机"类. | ⚠️ |
| 8 | 导弹火力 | `WsfWeaponComponent` + `WsfImplicitWeapon`/`WsfExplicitWeapon` + 多种杀伤模型 (`WsfSphericalLethality`, `WsfTabulatedLethality`, `WsfGraduatedLethality`, `WsfCarltonLethality`, `WsfMobilityAndFirepowerLethality`). `WsfWeaponTaskManager` + `WsfGuidanceComputer` + `WsfWeaponFuse`. | ✅ |
| 9 | 制导武器发射 | `WsfLaunchComputer` (基类) → `WsfAirToAirLaunchComputer`/`WsfSAM_LaunchComputer`/`WsfBallisticMissileLaunchComputer`/`WsfTabularLaunchComputer`. `WsfLaunchHandoffData`. | ✅ |
| 10 | 报文发送 | `WsfNetworkInterface` + `wsf::comm::Comm` (`WsfMessage` → `wsf::comm::Message` → ProtocolStack → JTIDS/LASER 物理层). `WsfAssetMessage`, `WsfTrackNotifyMessage`, `WsfStatusMessage`. Link16 J-series (J2-J31). | ✅ |
| 11 | 毁伤 | `WsfMobilityAndFirepowerLethality` (52 methods): M-kill/F-kill/M+F-kill/K-kill 四级 + CM 对抗评估. 另有 7 种杀伤模型可选. `WsfWeaponEffectsTypes` + `WsfExplicitWeaponEffects`. | ✅ |
| 12 | 电子干扰 | `WsfRF_Jammer` (JammerXmtr + JammerBeam + JammerMode: 多模式/多波束/多瞄准点 + 压制/欺骗/假目标等 10+ 技术). `WsfEW_Effect` 体系 (EA/EP). Demo: electronic_warfare/ (40+ 场景). | ✅ |

## 覆盖度统计

| 覆盖度 | 数量 | 占比 |
|--------|------|------|
| ✅ 完全覆盖 | 9 | 75% |
| ⚠️ 部分覆盖 | 2 | 17% |
| 🆕 缺失 | 1 | 8% |
| **总计** | **12** | **100%** |
