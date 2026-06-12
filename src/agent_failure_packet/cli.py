from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agent_failure_packet import __version__
from agent_failure_packet.builder import build_packet
from agent_failure_packet.renderers import render_json, render_markdown
from agent_failure_packet.schema import PacketInputError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent-failure-packet")
    parser.add_argument("--version", action="store_true", help="show version and exit")
    subparsers = parser.add_subparsers(dest="command")
    build = subparsers.add_parser("build", help="build a redacted failure packet")
    build.add_argument("--input", required=True, help="path to agent-failure-packet.run.v1 JSON")
    build.add_argument("--format", choices=("markdown", "json"), default="markdown")
    build.add_argument("--profile", choices=("incident", "issue"), default="incident", help="Markdown output profile")
    build.add_argument("--output", help="output path; defaults to stdout")
    build.add_argument("--redaction-policy", help="optional YAML file with literals and regexes")

    args = parser.parse_args(argv)
    if args.version:
        print(f"agent-failure-packet {__version__}")
        return 0
    if args.command != "build":
        parser.print_help(sys.stderr)
        return 2

    try:
        packet = build_packet(Path(args.input), policy_path=Path(args.redaction_policy) if args.redaction_policy else None)
    except (OSError, ValueError, PacketInputError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    output = render_json(packet) if args.format == "json" else render_markdown(packet, profile=args.profile)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


def entrypoint() -> None:
    raise SystemExit(main())
