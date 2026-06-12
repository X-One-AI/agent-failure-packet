# Changelog

## 0.2.0

runtime fixture corpus and output profile release.

- Add Codex CLI and GitHub Copilot agent-style failure fixtures.
- Add Markdown output profiles: `incident` for full review and `issue` for compact sharing.
- Redact secret-like query parameters while preserving documented placeholder credentials.
- Expand fixture coverage for real-world agent failure shapes.

## 0.1.0

Initial local packet builder release.

- Add `agent-failure-packet build` for Markdown and JSON packet output.
- Add generic `agent-failure-packet.run.v1` input support.
- Add `agent-failure-packet.packet.v1` output packets.
- Add default and user-extended redaction before rendering.
- Add fixture-backed tests for schema validation, rendering, CLI behavior, and redaction.
