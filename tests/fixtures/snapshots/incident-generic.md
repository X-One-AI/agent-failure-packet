# Agent Failure Packet

## Failure Summary

- Run ID: `run_123`
- Status: `failed`
- Agent: `codex`
- Started: `2026-06-13T00:00:00Z`
- Ended: `2026-06-13T00:03:00Z`
- Events: `3`

## Timeline

- `2026-06-13T00:00:15Z` `message`: Started task with API_KEY=[REDACTED:secret]
- `2026-06-13T00:01:00Z` `tool_call`: Running tests
- `2026-06-13T00:02:30Z` `error`: Tests failed while calling [REDACTED:secret]example.test/path

## Tool Calls

- `2026-06-13T00:01:00Z` `shell` exit `1`: Running tests

## Errors

- `2026-06-13T00:02:30Z` `CommandError`: 2 failed, password=[REDACTED:secret]

## Environment Summary

- branch: `feat/example`
- os: `macOS`
- repo: `X-One-AI/example`
- runtime: `python3.12`

## Redaction Summary

- Redactions applied: `5`
- Policy: `default`

## Reviewer Checklist

- [ ] Confirm the failure scope is understood.
- [ ] Review tool calls and exit codes.
- [ ] Confirm no raw secrets are present before sharing.
- [ ] Attach relevant tests or reproduction steps.

## Limitations

- Regex redaction reduces accidental exposure but is not complete security coverage.
- Raw input files remain the user's responsibility.
- Runtime-specific interpretation is limited to the generic run.v1 contract.
