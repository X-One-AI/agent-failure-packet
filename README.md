# agent-failure-packet

Languages: English | [中文](./README.zh-CN.md)

Create redacted, shareable debug packets from failed AI agent runs.

## Status

`P1` - v0.1.0 local packet builder.

## Purpose

Turn messy failed agent runs into safe evidence for issues, PRs, and incident review.

## First Production Surface

Local packet builder that accepts runtime exports and emits a redacted bundle.

The first executable surface is specified in [Packet Builder Design](./docs/superpowers/specs/2026-06-13-packet-builder-design.md).

## Install

From this repository:

```bash
python3 -m pip install -e .
agent-failure-packet --version
```

## Usage

Build a Markdown packet from a generic run export:

```bash
agent-failure-packet build --input tests/fixtures/runs/generic-failure-v1.json
agent-failure-packet build --input failed-run.json --format markdown --output failure-packet.md
agent-failure-packet build --input failed-run.json --format json --output failure-packet.json
agent-failure-packet build --input failed-run.json --redaction-policy .agent-failure-packet.yml
```

Input files use `schema_version: agent-failure-packet.run.v1`. JSON outputs use `schema_version: agent-failure-packet.packet.v1`.

Example custom redaction policy:

```yaml
literals:
  - internal-customer-id
regexes:
  - INTERNAL-[0-9]+
```

The default redaction policy cannot be disabled. The tool is local-first: it does not upload packet data, call a hosted service, or post comments.

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

## Docs

- [Product Foundation](./docs/product-foundation.md)
- [Packet Builder Design](./docs/superpowers/specs/2026-06-13-packet-builder-design.md)
- [Changelog](./CHANGELOG.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [Production Constraints](./ops/constraints/production.md)
- [Main Entry Constraints](./ops/constraints/main-entry.md)
- [Skill Evolution](./ops/skills/evolution.md)
