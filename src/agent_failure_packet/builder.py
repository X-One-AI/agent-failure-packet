from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_failure_packet.redaction import redact_value
from agent_failure_packet.schema import PACKET_SCHEMA_VERSION, RUN_SCHEMA_VERSION, validate_run_export


def build_packet(input_path: Path, policy_path: Path | None = None) -> dict[str, Any]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    validate_run_export(data)

    run = data["run"]
    events = data["events"]
    packet = {
        "schema_version": PACKET_SCHEMA_VERSION,
        "source_schema_version": RUN_SCHEMA_VERSION,
        "summary": {
            "run_id": run.get("id", "unknown"),
            "status": run.get("status", "unknown"),
            "agent": run.get("agent", "unknown"),
            "started_at": run.get("started_at"),
            "ended_at": run.get("ended_at"),
            "event_count": len(events),
        },
        "timeline": [_timeline_event(event) for event in events],
        "tool_calls": [_tool_call(event) for event in events if event.get("tool_call")],
        "errors": [_error(event) for event in events if event.get("error") or event.get("kind") == "error"],
        "environment": data["environment"],
        "redactions": {"count": 0, "policy": "default+custom" if policy_path else "default"},
        "limitations": [
            "Regex redaction reduces accidental exposure but is not complete security coverage.",
            "Raw input files remain the user's responsibility.",
            "Runtime-specific interpretation is limited to the generic run.v1 contract.",
        ],
    }
    result = redact_value(packet, policy_path=policy_path)
    redacted_packet = result.value
    redacted_packet["redactions"]["count"] = result.count
    return redacted_packet


def _timeline_event(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp": event.get("timestamp"),
        "kind": event.get("kind", "event"),
        "message": event.get("message", ""),
    }


def _tool_call(event: dict[str, Any]) -> dict[str, Any]:
    tool_call = event.get("tool_call", {})
    return {
        "timestamp": event.get("timestamp"),
        "name": tool_call.get("name", "unknown"),
        "arguments": tool_call.get("arguments", {}),
        "exit_code": tool_call.get("exit_code"),
        "message": event.get("message", ""),
    }


def _error(event: dict[str, Any]) -> dict[str, Any]:
    error = event.get("error", {})
    return {
        "timestamp": event.get("timestamp"),
        "type": error.get("type", "Error"),
        "message": error.get("message", event.get("message", "")),
        "event_message": event.get("message", ""),
    }
