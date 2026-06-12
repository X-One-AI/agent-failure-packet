# agent-failure-packet Product Foundation

## Intake

- Priority: P1
- Status: v0.3.0 local packet builder with config auto-discovery and schema compatibility checks
- Positioning: Create redacted, shareable debug packets from failed AI agent runs.
- Primary route: Product -> Architecture -> Expert/Security -> QA -> Implementation -> Completion readiness

## PRD

### Problem

Turn messy failed agent runs into safe evidence for issues, PRs, and incident review.

### Users

- Developers adopting AI agents or MCP tools
- Platform, DevTools, Security, and AI infrastructure teams
- Maintainers who need reviewable evidence rather than vague AI automation claims

### Goals

- timeline
- tool calls
- errors
- redaction summary
- environment summary

### Non-Goals

- not a full tracing platform
- not a hosted observability backend
- not raw prompt/log sharing

### Acceptance Criteria

- The project can explain its place in Safe Agent Operations in one sentence.
- The first production surface is local-first or review-first, not a hosted dashboard by default.
- Reports, packets, indexes, or labs must be redaction-safe by design.
- Every risky claim links to evidence, rule logic, or an explicit limitation.
- The first packet builder design is documented in `docs/superpowers/specs/2026-06-13-packet-builder-design.md`.
- `agent-failure-packet build` produces redacted Markdown and JSON packets from `agent-failure-packet.run.v1` inputs.
- Markdown profiles support compact issue sharing and fuller incident review.
- `agent-failure-packet validate` checks run export schema compatibility before packet generation.
- `.agent-failure-packet.yml` keeps team defaults out of crowded command lines.

## Architecture Brief

### Boundaries

- Keep shared workflow knowledge in OPT; keep project-specific decisions in this repository.
- Keep the main entrypoint small and explicit.
- Prefer file-based artifacts over hidden services for the first production surface.

### Data Flow

```text
input evidence -> normalize -> redact -> evaluate -> render reviewable artifact
```

### Risks

- Overclaiming safety guarantees.
- Creating generic tooling that weakens the Agentic DevSecOps signal.
- Accepting real secrets or private user data into fixtures.
- Allowing packet output to leak raw secrets because redaction was applied after rendering.

## QA Plan

- Unit-test redaction and normalization before rule or report expansion.
- Add positive and negative fixtures for every behavior boundary.
- Verify generated artifacts do not include raw secrets.
- Keep bilingual README guidance aligned.

## Implementation Plan

1. Keep the first executable surface local-first and deterministic.
2. Use the generic `agent-failure-packet.run.v1` JSON input contract until real runtime exports justify adapters.
3. Build Markdown and JSON packet outputs before any hosted or comment-posting workflow.
4. Prove redaction through positive and negative fixtures before release.
5. Maintain runtime-shaped fixture corpus entries before adding runtime-specific adapters.
6. Keep compatibility checks and snapshot tests in CI before each release.
7. Use feature branches named `feat/<scope>` or `docs/<scope>`.
8. Use Conventional/Angular commits such as `feat: add packet schema` or `docs: clarify deferred scope`.
9. Never push directly to `main`; open a pull request from the feature branch.

## Skipped Inputs

- first runtime export format
- real failed runs
- redaction policy details
