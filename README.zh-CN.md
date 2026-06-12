# agent-failure-packet

语言： [English](./README.md) | 中文

把失败的 AI agent 执行过程生成可脱敏、可分享的调试包。

## 状态

`P1` - packet builder 设计已准备进入 v0.1.0 规划。

## 目的

把混乱的失败 agent run 转成适合 issue、PR 和 incident review 使用的安全证据。

## 第一生产化表面

本地 packet builder：接受 agent runtime export，并输出脱敏后的可分享 bundle。

第一可执行表面已在 [Packet Builder Design](./docs/superpowers/specs/2026-06-13-packet-builder-design.md) 中定义。

## 必要证据

- 时间线
- 工具调用
- 错误
- 脱敏摘要
- 环境摘要

## 非目标

- 不做完整 tracing 平台
- 不做 hosted observability backend
- 不分享原始 prompt 或 log

## OPT 运行模型

本项目通过 [ops/opt-overlay.md](./ops/opt-overlay.md) 引用共享 One Person Team 工作流。项目自己的约束放在 [ops/constraints](./ops/constraints)，可演进 skill 放在 [ops/skills](./ops/skills)。

## 暂缺输入

需要用户或真实世界数据补充的内容记录在 `../x-one-skipped-inputs.md`，不阻塞基础建设。

## 文档

- [产品基础](./docs/product-foundation.md)
- [Packet Builder Design](./docs/superpowers/specs/2026-06-13-packet-builder-design.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [生产约束](./ops/constraints/production.md)
- [主入口约束](./ops/constraints/main-entry.md)
- [Skill 演进](./ops/skills/evolution.md)
