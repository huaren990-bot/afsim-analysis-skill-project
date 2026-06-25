# REQ-XXX 迁移模块快速入门

## 编译
确保已安装 Eigen3 和目标系统公共头文件路径正确。
```bash
cd tests/migration_src/<req_index>/
g++ -std=c++17 -I<path_to_target_includes> test_demo.cpp REQ_xxx.cpp -o test_demo
```

## 依赖
- Eigen3（线性代数）
- 目标系统类型定义：`RigidBodyState`, `Wrench`（位于 `src/common/` 或由目标系统提供）

## 运行 Demo
```bash
./test_demo
```
预期输出：
```
最终位置: ...
姿态四元数: ...
```

## 功能列表
- FU-001: 六自由度积分器
- FU-xxx: <功能名> 🆕（全新设计，AFSIM 无参考）