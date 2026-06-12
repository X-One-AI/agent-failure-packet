# agent-failure-packet

语言： [English](./README.md) | 中文

把失败的 AI agent 执行过程生成可脱敏、可分享的调试包。

## 状态

`P1` - reserved production foundation。

## 目的

Turn messy failed agent runs into safe evidence for issues, PRs, and incident review.

## 第一生产化表面

Local packet builder that accepts runtime exports and emits a redacted bundle.

## 必要证据

- timeline
- tool calls
- errors
- redaction summary
- environment summary

## 非目标

- not a full tracing platform
- not a hosted observability backend
- not raw prompt/log sharing

## OPT 运行模型

本项目通过 [ops/opt-overlay.md](./ops/opt-overlay.md) 引用共享 One Person Team 工作流。项目自己的约束放在 [ops/constraints](./ops/constraints)，可演进 skill 放在 [ops/skills](./ops/skills)。

## 暂缺输入

需要用户或真实世界数据补充的内容记录在 `../x-one-skipped-inputs.md`，不阻塞基础建设。

## 文档

- [产品基础](./docs/product-foundation.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [生产约束](./ops/constraints/production.md)
- [主入口约束](./ops/constraints/main-entry.md)
- [Skill 演进](./ops/skills/evolution.md)
