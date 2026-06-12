# agent-failure-packet

语言： [English](./README.md) | 中文

把失败的 AI agent 执行过程生成可脱敏、可分享的调试包。

## 状态

`P1` - v0.3.0 本地 packet builder，支持配置和兼容性检查。

## 目的

把混乱的失败 agent run 转成适合 issue、PR 和 incident review 使用的安全证据。

## 第一生产化表面

本地 packet builder：接受 agent runtime export，并输出脱敏后的可分享 bundle。

第一可执行表面已在 [Packet Builder Design](./docs/superpowers/specs/2026-06-13-packet-builder-design.md) 中定义。

## 安装

在本仓库中运行：

```bash
python3 -m pip install -e .
agent-failure-packet --version
```

## 使用

从 generic run export 生成 Markdown packet：

```bash
agent-failure-packet init --profile issue
agent-failure-packet validate --input failed-run.json
agent-failure-packet build --input tests/fixtures/runs/generic-failure-v1.json
agent-failure-packet build --input failed-run.json --format markdown --output failure-packet.md
agent-failure-packet build --input failed-run.json --format json --output failure-packet.json
agent-failure-packet build --input failed-run.json --profile issue --output issue-packet.md
agent-failure-packet build --input failed-run.json --redaction-policy .agent-failure-packet.yml
```

输入文件使用 `schema_version: agent-failure-packet.run.v1`。JSON 输出使用 `schema_version: agent-failure-packet.packet.v1`。

`agent-failure-packet build` 会从当前目录或上级目录自动发现 `.agent-failure-packet.yml`：

```yaml
schema_version: 1
profile: issue
# redaction_policy: .agent-failure-packet-redaction.yml
```

Markdown profiles：

- `incident`：完整 packet，包含时间线、工具调用、错误、环境、脱敏摘要、checklist 和限制说明。
- `issue`：适合 GitHub issue 或 support ticket 的紧凑 packet；省略更深的工具调用和环境章节。

Fixture corpus：

- `generic-failure-v1.json`
- `codex-cli-failure-v1.json`
- `github-copilot-agent-failure-v1.json`

自定义脱敏策略示例：

```yaml
literals:
  - internal-customer-id
regexes:
  - INTERNAL-[0-9]+
```

默认脱敏策略不能关闭。本工具是 local-first：不会上传 packet 数据，不调用 hosted service，也不会自动发布 comment。

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
- 不承诺覆盖所有组织特有 secret 的完整安全能力

## OPT 运行模型

本项目通过 [ops/opt-overlay.md](./ops/opt-overlay.md) 引用共享 One Person Team 工作流。项目自己的约束放在 [ops/constraints](./ops/constraints)，可演进 skill 放在 [ops/skills](./ops/skills)。

## 暂缺输入

需要用户或真实世界数据补充的内容记录在 `../x-one-skipped-inputs.md`，不阻塞基础建设。

## 文档

- [产品基础](./docs/product-foundation.md)
- [Packet Builder Design](./docs/superpowers/specs/2026-06-13-packet-builder-design.md)
- [Changelog](./CHANGELOG.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [生产约束](./ops/constraints/production.md)
- [主入口约束](./ops/constraints/main-entry.md)
- [Skill 演进](./ops/skills/evolution.md)
