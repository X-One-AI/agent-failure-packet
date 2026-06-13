# agent-failure-packet

Languages: English | [中文](./README.zh-CN.md)

Create redacted, shareable debug packets from failed AI agent runs.

## Status

`P1` - v0.4.1 local packet builder and read-only GitHub Action.

## Purpose

Turn messy failed agent runs into safe evidence for issues, PRs, and incident review.

## First Production Surface

Local packet builder that accepts runtime exports and emits a redacted bundle.

The first executable surface is specified in [Packet Builder Design](./docs/superpowers/specs/2026-06-13-packet-builder-design.md).

## Install

From PyPI:

```bash
python3 -m pip install xone-agent-failure-packet
agent-failure-packet --version
```

From Homebrew:

```bash
brew install x-one-ai/tap/agent-failure-packet
agent-failure-packet --version
```

From this repository:

```bash
python3 -m pip install -e .
agent-failure-packet --version
```

## Usage

Build a Markdown packet from a generic run export:

```bash
agent-failure-packet init --profile issue
agent-failure-packet validate --input failed-run.json
agent-failure-packet build --input tests/fixtures/runs/generic-failure-v1.json
agent-failure-packet build --input failed-run.json --format markdown --output failure-packet.md
agent-failure-packet build --input failed-run.json --format json --output failure-packet.json
agent-failure-packet build --input failed-run.json --profile issue --output issue-packet.md
agent-failure-packet build --input failed-run.json --redaction-policy .agent-failure-packet.yml
```

Input files use `schema_version: agent-failure-packet.run.v1`. JSON outputs use `schema_version: agent-failure-packet.packet.v1`.

`agent-failure-packet build` auto-discovers `.agent-failure-packet.yml` from the current directory or its parents:

```yaml
schema_version: 1
profile: issue
# redaction_policy: .agent-failure-packet-redaction.yml
```

Markdown profiles:

- `incident`: full packet with timeline, tool calls, errors, environment, redaction summary, checklist, and limitations.
- `issue`: compact packet for GitHub issues or support tickets; omits deeper tool-call and environment sections.

Fixture corpus:

- `generic-failure-v1.json`
- `codex-cli-failure-v1.json`
- `github-copilot-agent-failure-v1.json`

Example custom redaction policy:

```yaml
literals:
  - internal-customer-id
regexes:
  - INTERNAL-[0-9]+
```

The default redaction policy cannot be disabled. The tool is local-first: it does not upload packet data, call a hosted service, or post comments.

## GitHub Action

Use the Action after checkout and point it at a failure export produced by your agent workflow:

```yaml
name: Agent Failure Packet

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  packet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: X-One-AI/agent-failure-packet@v0.4.1
        with:
          input: failed-run.json
          profile: issue
          output: agent-failure-packet.md
```

The Action writes a packet file, appends a compact packet to `GITHUB_STEP_SUMMARY`, and exposes `packet-path` and `summary-json` outputs. It is read-only and does not post PR comments.

## Required Evidence

- timeline
- tool calls
- errors
- redaction summary
- environment summary

## Non-Goals

- not a full tracing platform
- not a hosted observability backend
- not raw prompt/log sharing
- not complete security coverage for every organization-specific secret

## OPT Operating Model

This project references the shared One Person Team workflow through [ops/opt-overlay.md](./ops/opt-overlay.md). Project-specific constraints live under [ops/constraints](./ops/constraints), and evolvable local skills live under [ops/skills](./ops/skills).

## Blocked Inputs

Inputs that require user or real-world data are recorded in `../x-one-skipped-inputs.md` and should not block foundation work.

Real-user feedback should be classified as false-positive, false-negative, adapter-request, scenario-request, or catalog-update when it applies; portfolio-level handling is tracked in X-One portfolio health docs.

## Docs

- [Product Foundation](./docs/product-foundation.md)
- [Packet Builder Design](./docs/superpowers/specs/2026-06-13-packet-builder-design.md)
- [Changelog](./CHANGELOG.md)
- [Publishing](./docs/publishing.md)
- [Homebrew Packaging](./docs/homebrew.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [Production Constraints](./ops/constraints/production.md)
- [Main Entry Constraints](./ops/constraints/main-entry.md)
- [Skill Evolution](./ops/skills/evolution.md)
