# agent-failure-packet

Languages: English | [中文](./README.zh-CN.md)

Create redacted, shareable debug packets from failed AI agent runs.

## Status

`P1` - reserved production foundation.

## Purpose

Turn messy failed agent runs into safe evidence for issues, PRs, and incident review.

## First Production Surface

Local packet builder that accepts runtime exports and emits a redacted bundle.

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

## OPT Operating Model

This project references the shared One Person Team workflow through [ops/opt-overlay.md](./ops/opt-overlay.md). Project-specific constraints live under [ops/constraints](./ops/constraints), and evolvable local skills live under [ops/skills](./ops/skills).

## Blocked Inputs

Inputs that require user or real-world data are recorded in `../x-one-skipped-inputs.md` and should not block foundation work.

## Docs

- [Product Foundation](./docs/product-foundation.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [Production Constraints](./ops/constraints/production.md)
- [Main Entry Constraints](./ops/constraints/main-entry.md)
- [Skill Evolution](./ops/skills/evolution.md)
