# PR/CI Failure Handoff

Use this workflow when `agent-pr-evidence` returns the `create-failure-packet` handoff decision for a PR/CI failure or an agent run failure.

## Boundary

- `agent-failure-packet` does not read GitHub PRs automatically.
- It does not post comments, close issues, retry CI, or change repository settings.
- It turns already-collected evidence into a redacted issue packet or support packet.
- Maintainers: do not paste raw logs into public issues or shared channels.

## Required Inputs

- The `agent-pr-evidence` Markdown or JSON report.
- The failed command name.
- A short redacted failure excerpt.
- The expected behavior.
- The observed behavior.
- The last known passing state when available.

## Flow

1. Confirm the report decision is `create-failure-packet`.
2. Copy only the minimal failure excerpt into the packet draft.
3. Run a redaction review for tokens, credentials, private paths, customer data, and internal hostnames.
4. Add reproduction steps that a maintainer can run locally.
5. Attach the resulting issue packet to the PR, issue, or incident record.

## Packet Checklist

- Decision: `create-failure-packet`
- Evidence source: test log, CI log excerpt, or agent run transcript excerpt
- Redaction review: completed before sharing
- Owner: named reviewer or maintainer
- Next action: retry, fix, rollback, or accept with rationale

## Stop Conditions

- If there is no failure evidence, ask for test evidence instead of creating a packet.
- If the failure excerpt contains secrets, redact before creating the issue packet.
- If the failure can affect production users, escalate to the incident process.
