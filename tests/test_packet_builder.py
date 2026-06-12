import json
import subprocess
import sys
from pathlib import Path

import pytest

from agent_failure_packet.builder import build_packet
from agent_failure_packet.cli import main
from agent_failure_packet.renderers import render_markdown


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests/fixtures/runs/generic-failure-v1.json"
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


def test_issue_profile_is_compact_and_incident_profile_keeps_deeper_sections():
    packet = build_packet(Path("tests/fixtures/runs/codex-cli-failure-v1.json"))

    issue_markdown = render_markdown(packet, profile="issue")
    incident_markdown = render_markdown(packet, profile="incident")

    assert "## Tool Calls" not in issue_markdown
    assert "## Errors" in issue_markdown
    assert "## Tool Calls" in incident_markdown
    assert "## Environment Summary" in incident_markdown
    assert "query-secret-token" not in incident_markdown
    assert "Bearer codex-secret-token" not in incident_markdown
    assert "<your-api-key>" in incident_markdown


def test_runtime_fixture_corpus_documents_supported_real_world_shapes():
    fixture_dir = Path("tests/fixtures/runs")
    fixture_names = {path.name for path in fixture_dir.glob("*.json")}

    assert "generic-failure-v1.json" in fixture_names
    assert "codex-cli-failure-v1.json" in fixture_names
    assert "github-copilot-agent-failure-v1.json" in fixture_names
    for fixture in fixture_dir.glob("*.json"):
        packet = build_packet(fixture)
        assert packet["schema_version"] == "agent-failure-packet.packet.v1"
        assert packet["timeline"], fixture.name


def test_cli_build_writes_json_and_markdown(tmp_path):
    json_output = tmp_path / "packet.json"
    markdown_output = tmp_path / "packet.md"

    json_exit = main(["build", "--input", str(FIXTURE), "--format", "json", "--output", str(json_output)])
    markdown_exit = main(["build", "--input", str(FIXTURE), "--format", "markdown", "--output", str(markdown_output)])

    assert json_exit == 0
    assert markdown_exit == 0
    assert json.loads(json_output.read_text(encoding="utf-8"))["schema_version"] == "agent-failure-packet.packet.v1"
    assert "# Agent Failure Packet" in markdown_output.read_text(encoding="utf-8")


def test_cli_build_supports_output_profiles(tmp_path):
    output = tmp_path / "issue.md"

    exit_code = main(
        [
            "build",
            "--input",
            "tests/fixtures/runs/codex-cli-failure-v1.json",
            "--profile",
            "issue",
            "--output",
            str(output),
        ]
    )

    text = output.read_text(encoding="utf-8")
    assert exit_code == 0
    assert "## Errors" in text
    assert "## Tool Calls" not in text
    assert "query-secret-token" not in text


def test_cli_init_writes_default_config_and_build_auto_discovers_it(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    input_path = tmp_path / "run.json"
    input_path.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")

    init_exit = main(["init", "--profile", "issue"])
    output = tmp_path / "packet.md"
    build_exit = main(["build", "--input", str(input_path), "--output", str(output)])

    config = (tmp_path / ".agent-failure-packet.yml").read_text(encoding="utf-8")
    text = output.read_text(encoding="utf-8")
    assert init_exit == 0
    assert build_exit == 0
    assert "schema_version: 1" in config
    assert "profile: issue" in config
    assert "## Errors" in text
    assert "## Tool Calls" not in text


def test_cli_validate_checks_input_schema_and_outputs_summary(capsys):
    exit_code = main(["validate", "--input", str(FIXTURE)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "schema_version=agent-failure-packet.run.v1" in captured.out
    assert "events=3" in captured.out


def test_incident_markdown_snapshot_stays_stable():
    expected = (REPO_ROOT / "tests/fixtures/snapshots/incident-generic.md").read_text(encoding="utf-8")

    assert render_markdown(build_packet(FIXTURE), profile="incident") == expected


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

    assert result.stdout.strip() == "agent-failure-packet 0.4.0"
