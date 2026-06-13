# Changelog

## 0.4.1

Distribution release.

- Add package publishing workflow and distribution documentation.
- Prepare a release tag that includes the PyPI/TestPyPI publishing workflow.

## 0.4.0

GitHub Action release.

- Add a read-only composite GitHub Action for building failure packets in CI.
- Add `scripts/run-action.py` to write packets, step summaries, and downstream outputs.
- Expose `packet-path` and `summary-json` Action outputs.
- Keep Action behavior local and non-commenting by default.

## 0.3.0

Configuration and compatibility release.

- Add `agent-failure-packet init` for local project configuration.
- Add config auto-discovery from `.agent-failure-packet.yml`.
- Add `agent-failure-packet validate` for run export schema checks.
- Add Markdown snapshot coverage to detect accidental packet structure drift.

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
