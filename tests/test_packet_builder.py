import json
import subprocess
import sys
from pathlib import Path

import pytest

from agent_failure_packet.builder import build_packet
from agent_failure_packet.cli import main
from agent_failure_packet.renderers import render_markdown


FIXTURE = Path("tests/fixtures/runs/generic-failure-v1.json")
SECRET_VALUES = (
    "sk-live-secret-value",
    "Bearer test-secret-token",
    "user:pass@example.test",
    "password=hunter2",
)


def test_build_packet_normalizes_failed_run_and_redacts_sensitive_values():
    packet = build_packet(FIXTURE)

    assert packet["schema_version"] == "agent-failure-packet.packet.v1"
    assert packet["source_schema_version"] == "agent-failure-packet.run.v1"
    assert packet["summary"]["run_id"] == "run_123"
    assert packet["summary"]["status"] == "failed"
    assert packet["summary"]["agent"] == "codex"
    assert len(packet["timeline"]) == 3
    assert packet["tool_calls"][0]["name"] == "shell"
    assert packet["tool_calls"][0]["exit_code"] == 1
    assert packet["errors"][0]["type"] == "CommandError"
    assert packet["redactions"]["count"] >= 4
    assert packet["limitations"]

    serialized = json.dumps(packet, sort_keys=True)
    for secret in SECRET_VALUES:
        assert secret not in serialized


def test_render_markdown_contains_reviewable_sections_without_secrets():
    markdown = render_markdown(build_packet(FIXTURE))

    assert "# Agent Failure Packet" in markdown
    assert "## Timeline" in markdown
    assert "## Tool Calls" in markdown
    assert "## Errors" in markdown
    assert "## Redaction Summary" in markdown
    assert "## Reviewer Checklist" in markdown
    assert "## Limitations" in markdown
    assert "[REDACTED:" in markdown
    for secret in SECRET_VALUES:
        assert secret not in markdown


def test_cli_build_writes_json_and_markdown(tmp_path):
    json_output = tmp_path / "packet.json"
    markdown_output = tmp_path / "packet.md"

    json_exit = main(["build", "--input", str(FIXTURE), "--format", "json", "--output", str(json_output)])
    markdown_exit = main(["build", "--input", str(FIXTURE), "--format", "markdown", "--output", str(markdown_output)])

    assert json_exit == 0
    assert markdown_exit == 0
    assert json.loads(json_output.read_text(encoding="utf-8"))["schema_version"] == "agent-failure-packet.packet.v1"
    assert "# Agent Failure Packet" in markdown_output.read_text(encoding="utf-8")


def test_cli_build_prints_markdown_to_stdout(capsys):
    exit_code = main(["build", "--input", str(FIXTURE)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "# Agent Failure Packet" in captured.out


def test_unsupported_schema_returns_helpful_error(tmp_path, capsys):
    bad_input = tmp_path / "bad.json"
    bad_input.write_text(json.dumps({"schema_version": "unknown", "run": {}, "environment": {}, "events": []}), encoding="utf-8")

    exit_code = main(["build", "--input", str(bad_input)])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Unsupported schema_version" in captured.err


def test_custom_redaction_policy_redacts_literal_and_regex(tmp_path):
    input_path = tmp_path / "run.json"
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    data["events"].append(
        {
            "timestamp": "2026-06-13T00:02:45Z",
            "kind": "message",
            "message": "Customer id acme-private and ticket INTERNAL-12345",
        }
    )
    input_path.write_text(json.dumps(data), encoding="utf-8")
    policy = tmp_path / ".agent-failure-packet.yml"
    policy.write_text(
        "literals:\n  - acme-private\nregexes:\n  - INTERNAL-[0-9]+\n",
        encoding="utf-8",
    )

    packet = build_packet(input_path, policy_path=policy)
    serialized = json.dumps(packet, sort_keys=True)

    assert "acme-private" not in serialized
    assert "INTERNAL-12345" not in serialized
    assert packet["redactions"]["count"] >= 6


def test_package_module_entrypoint_outputs_version():
    result = subprocess.run(
        [sys.executable, "-m", "agent_failure_packet", "--version"],
        check=True,
        env={"PYTHONPATH": "src"},
        text=True,
        stdout=subprocess.PIPE,
    )

    assert result.stdout.strip() == "agent-failure-packet 0.1.0"
