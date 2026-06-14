# Agent Failure Packet Issue Handoff Workflow

This workflow turns a failed AI agent run into a redacted packet that can be shared in a GitHub issue, support thread, or incident review without attaching raw logs.

## 10-minute issue handoff path

1. Export the failed run into `agent-failure-packet.run.v1` JSON.
2. Validate the export before building:

   ```bash
   agent-failure-packet validate --input failed-run.json
   ```

3. Build the compact issue profile:

   ```bash
   agent-failure-packet build --input failed-run.json --profile issue --output failure-packet.md
   ```

4. Run a Redaction review before sharing the packet.
5. Attach the compact issue packet to the issue or support request.
6. Keep the raw export local unless the maintainer explicitly asks for a sanitized fixture.

## Redaction review

Before sharing, check:

- no raw API keys, bearer tokens, passwords, or private URLs remain;
- customer names, repository names, and internal hostnames are removed or replaced when needed;
- custom literals or regexes are added to `.agent-failure-packet.yml` when the default policy is not enough;
- the redaction summary shows that redaction ran before rendering.

## Product gate

This workflow is production-ready only when:

- a developer can create a shareable issue packet in 10 minutes;
- `agent-failure-packet validate` catches incompatible exports before packet generation;
- fixture corpus entries represent real runtime-shaped failures;
- packet output is covered by redaction tests and Markdown snapshot tests;
- real-user or public-sample feedback is recorded before adapter behavior changes.
