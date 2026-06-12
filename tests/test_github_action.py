import json
import os
import subprocess
import sys
from pathlib import Path

import yaml


FIXTURE = Path("tests/fixtures/runs/generic-failure-v1.json")


def test_action_metadata_is_read_only_and_exposes_expected_inputs_outputs():
    text = Path("action.yml").read_text(encoding="utf-8")
    action = yaml.safe_load(text)

    assert action["runs"]["using"] == "composite"
    assert "input" in action["inputs"]
    assert "format" in action["inputs"]
    assert "profile" in action["inputs"]
    assert "output" in action["inputs"]
    assert "packet-path" in action["outputs"]
    assert "summary-json" in action["outputs"]
    run_commands = "\n".join(step.get("run", "") for step in action["runs"]["steps"])
    assert "python3 scripts/run-action.py" in run_commands
    assert "pull-requests: write" not in text


def test_action_runner_writes_packet_summary_and_outputs(tmp_path):
    summary_path = tmp_path / "summary.md"
    output_path = tmp_path / "outputs.txt"
    packet_path = tmp_path / "packet.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run-action.py",
            "--input",
            str(FIXTURE),
            "--format",
            "markdown",
            "--profile",
            "issue",
            "--output",
            str(packet_path),
        ],
        check=True,
        env=os.environ
        | {
            "GITHUB_STEP_SUMMARY": str(summary_path),
            "GITHUB_OUTPUT": str(output_path),
        },
        text=True,
        stdout=subprocess.PIPE,
    )

    packet_text = packet_path.read_text(encoding="utf-8")
    assert "Agent failure packet written" in result.stdout
    assert "# Agent Failure Packet" in packet_text
    assert "## Tool Calls" not in packet_text
    assert "# Agent Failure Packet" in summary_path.read_text(encoding="utf-8")
    outputs = output_path.read_text(encoding="utf-8")
    assert f"packet-path={packet_path}" in outputs
    summary_line = next(line for line in outputs.splitlines() if line.startswith("summary-json="))
    summary = json.loads(summary_line.removeprefix("summary-json="))
    assert summary["schema_version"] == "agent-failure-packet.packet.v1"
    assert summary["status"] == "failed"
