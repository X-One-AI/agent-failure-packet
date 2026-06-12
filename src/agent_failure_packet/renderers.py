from __future__ import annotations

import json
from typing import Any


def render_json(packet: dict[str, Any]) -> str:
    return json.dumps(packet, indent=2, sort_keys=True) + "\n"


def render_markdown(packet: dict[str, Any]) -> str:
    summary = packet["summary"]
    lines = [
        "# Agent Failure Packet",
        "",
        "## Failure Summary",
        "",
        f"- Run ID: `{summary['run_id']}`",
        f"- Status: `{summary['status']}`",
        f"- Agent: `{summary['agent']}`",
        f"- Started: `{summary.get('started_at') or 'unknown'}`",
        f"- Ended: `{summary.get('ended_at') or 'unknown'}`",
        f"- Events: `{summary['event_count']}`",
        "",
        "## Timeline",
        "",
    ]
    for event in packet["timeline"]:
        lines.append(f"- `{event.get('timestamp') or 'unknown'}` `{event['kind']}`: {event['message']}")
    lines.extend(["", "## Tool Calls", ""])
    if packet["tool_calls"]:
        for call in packet["tool_calls"]:
            lines.append(f"- `{call.get('timestamp') or 'unknown'}` `{call['name']}` exit `{call.get('exit_code')}`: {call['message']}")
    else:
        lines.append("- None recorded.")
    lines.extend(["", "## Errors", ""])
    if packet["errors"]:
        for error in packet["errors"]:
            lines.append(f"- `{error.get('timestamp') or 'unknown'}` `{error['type']}`: {error['message']}")
    else:
        lines.append("- None recorded.")
    lines.extend(["", "## Environment Summary", ""])
    for key, value in sorted(packet["environment"].items()):
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Redaction Summary",
            "",
            f"- Redactions applied: `{packet['redactions']['count']}`",
            f"- Policy: `{packet['redactions']['policy']}`",
            "",
            "## Reviewer Checklist",
            "",
            "- [ ] Confirm the failure scope is understood.",
            "- [ ] Review tool calls and exit codes.",
            "- [ ] Confirm no raw secrets are present before sharing.",
            "- [ ] Attach relevant tests or reproduction steps.",
            "",
            "## Limitations",
            "",
        ]
    )
    for limitation in packet["limitations"]:
        lines.append(f"- {limitation}")
    return "\n".join(lines) + "\n"
