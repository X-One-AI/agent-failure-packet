# agent-failure-packet Packet Builder Design

## Status

Proposed for v0.1.0 implementation planning.

## Product Decision

`agent-failure-packet` should not become a tracing dashboard or hosted observability tool. Its first production surface is a deterministic local packet builder that converts a failed AI agent run export into a redacted, shareable evidence bundle for issues, PRs, support tickets, and incident review.

## Problem

Failed agent runs are hard to share safely. Raw transcripts often mix prompts, tool arguments, environment details, command output, stack traces, and possible secrets. Reviewers need enough evidence to debug what happened without receiving raw private context.

## Users

- Developers using coding agents or MCP tools.
- Maintainers receiving agent failure reports.
- Platform, DevTools, Security, and AI infrastructure teams.
- Incident reviewers who need concise evidence instead of raw logs.

## Goals

- Build a local CLI that accepts a versioned JSON run export.
- Normalize the export into a stable packet schema.
- Redact secret-like values before rendering or writing packets.
- Emit Markdown and JSON outputs.
- Include a timeline, tool calls, errors, redaction summary, and environment summary.
- Keep the main entry point small enough for repeated use.

## Non-Goals

- No hosted backend in v0.1.0.
- No real-time tracing, spans, dashboards, or storage service.
- No automatic upload to GitHub, Slack, Linear, or support systems.
- No claim that redaction is complete security coverage.
- No runtime-specific adapter until real exports are available.

## Input Contract

The first input contract is `agent-failure-packet.run.v1`, a generic JSON export with these top-level fields:

- `schema_version`: must equal `agent-failure-packet.run.v1`.
- `run`: object with `id`, `started_at`, `ended_at`, `status`, and optional `agent`.
- `environment`: object with safe metadata such as `os`, `runtime`, `repo`, and `branch`.
- `events`: ordered list of objects with `timestamp`, `kind`, `message`, and optional `tool_call`, `error`, or `metadata`.

Unknown fields are preserved only in JSON output after redaction. Markdown output stays intentionally compact.

## Output Contract

The packet JSON uses `agent-failure-packet.packet.v1` and contains:

- `schema_version`
- `source_schema_version`
- `summary`
- `timeline`
- `tool_calls`
- `errors`
- `environment`
- `redactions`
- `limitations`

Markdown output contains:

1. Failure summary
2. Timeline
3. Tool calls
4. Errors
5. Environment summary
6. Redaction summary
7. Reviewer checklist
8. Limitations

## Architecture

```text
JSON export -> parse -> validate -> normalize -> redact -> packet model -> render Markdown/JSON
```

Modules for v0.1.0:

- `schema`: validate supported input and output schema versions.
- `normalizer`: convert run export events into packet model sections.
- `redaction`: redact secret-like values from every rendered and serialized field.
- `renderers`: render Markdown and JSON.
- `cli`: expose `agent-failure-packet build`.

## CLI Shape

```bash
agent-failure-packet build --input failed-run.json --format markdown --output failure-packet.md
agent-failure-packet build --input failed-run.json --format json --output failure-packet.json
agent-failure-packet build --input failed-run.json --redaction-policy .agent-failure-packet.yml
```

The default behavior writes Markdown to stdout when `--output` is not provided.

## Redaction Policy

Default redaction must cover:

- API keys, tokens, secrets, passwords, bearer tokens, and common `sk-...` values.
- Assignment patterns such as `API_KEY=value`.
- HTTP authorization headers.
- URL credentials.

The v0.1.0 policy file may add custom literal values and regex patterns. It must not disable default redaction.

## Security Gate

Decision: revise if implementation cannot prove output redaction through tests.

Required controls:

- Redaction is applied before Markdown or JSON serialization.
- Tests include positive secret cases and placeholder non-secret cases.
- Fixtures must not contain real private data.
- Packet output must include explicit limitations.
- CLI must not upload, phone home, or read paths other than the provided input and optional policy file.

Residual risk:

- Regex redaction can miss organization-specific secrets until users add policy patterns.
- Raw input files remain the user's responsibility.

## QA Plan

Requirement-to-test mapping:

- R1 input schema validation -> invalid schema and missing required field tests.
- R2 redaction before output -> Markdown and JSON secret absence tests.
- R3 timeline/tool/error normalization -> fixture snapshot or structural tests.
- R4 policy extension -> custom literal and regex redaction tests.
- R5 CLI ergonomics -> stdout, output file, JSON format, and error exit tests.
- R6 docs alignment -> README, Chinese README, product foundation, and examples consistency tests.

E2E path:

1. Build a packet from `tests/fixtures/runs/generic-failure-v1.json`.
2. Assert Markdown contains summary, timeline, tool calls, errors, redaction summary, checklist, and limitations.
3. Assert no known secret literal appears in Markdown or JSON.
4. Assert CLI exits non-zero with a helpful message for unsupported schema versions.

## Implementation Batches

1. Package scaffold: `pyproject.toml`, package module, CLI version command, docs checks.
2. Packet model and schema validation with fixtures.
3. Redaction engine and policy loading.
4. Markdown and JSON renderers.
5. CLI build command and error handling.
6. README examples, bilingual docs, changelog, packaging, release artifact verification.

## Acceptance Criteria

- `python3 -m pytest tests -q` passes.
- `agent-failure-packet --version` works after editable install.
- `agent-failure-packet build` produces Markdown and JSON from a fixture.
- Outputs redact fixture secrets and report redaction counts.
- README and README.zh-CN show aligned install and usage paths.
- CI runs on push and pull request.
- The release can ship as a wheel and sdist.

## Open Inputs Recorded Elsewhere

The following should not block v0.1.0:

- First real runtime-specific export format.
- Real failed agent runs.
- Organization-specific redaction rules.
- Whether users prefer issue, support ticket, or incident-review templates.

