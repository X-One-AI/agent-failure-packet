from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agent_failure_packet.builder import build_packet
from agent_failure_packet.renderers import render_json, render_markdown
from agent_failure_packet.schema import PacketInputError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="run-action.py")
    parser.add_argument("--input", required=True)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--profile", choices=("incident", "issue"), default="incident")
    parser.add_argument("--output", default="agent-failure-packet.md")
    parser.add_argument("--redaction-policy")
    args = parser.parse_args(argv)

    output_path = Path(args.output)
    try:
        packet = build_packet(Path(args.input), policy_path=Path(args.redaction_policy) if args.redaction_policy else None)
    except (OSError, ValueError, PacketInputError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    output = render_json(packet) if args.format == "json" else render_markdown(packet, profile=args.profile)
    output_path.write_text(output, encoding="utf-8")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        Path(summary_path).write_text(render_markdown(packet, profile="issue"), encoding="utf-8")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        summary = {
            "schema_version": packet["schema_version"],
            "run_id": packet["summary"]["run_id"],
            "status": packet["summary"]["status"],
            "agent": packet["summary"]["agent"],
            "redactions": packet["redactions"]["count"],
        }
        with Path(github_output).open("a", encoding="utf-8") as handle:
            handle.write(f"packet-path={output_path}\n")
            handle.write(f"summary-json={json.dumps(summary, sort_keys=True)}\n")

    print(f"Agent failure packet written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
