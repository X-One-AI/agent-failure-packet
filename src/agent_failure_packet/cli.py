from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agent_failure_packet import __version__
from agent_failure_packet.builder import build_packet
from agent_failure_packet.config import CONFIG_FILENAME, default_config_text, load_config
from agent_failure_packet.renderers import render_json, render_markdown
from agent_failure_packet.schema import PacketInputError, validate_run_export
import json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent-failure-packet")
    parser.add_argument("--version", action="store_true", help="show version and exit")
    subparsers = parser.add_subparsers(dest="command")
    init = subparsers.add_parser("init", help="write a local configuration file")
    init.add_argument("--profile", choices=("incident", "issue"), default="incident")
    init.add_argument("--output", default=CONFIG_FILENAME)
    build = subparsers.add_parser("build", help="build a redacted failure packet")
    build.add_argument("--input", required=True, help="path to agent-failure-packet.run.v1 JSON")
    build.add_argument("--format", choices=("markdown", "json"), default="markdown")
    build.add_argument("--profile", choices=("incident", "issue"), help="Markdown output profile")
    build.add_argument("--output", help="output path; defaults to stdout")
    build.add_argument("--redaction-policy", help="optional YAML file with literals and regexes")
    validate = subparsers.add_parser("validate", help="validate a run export")
    validate.add_argument("--input", required=True, help="path to agent-failure-packet.run.v1 JSON")

    args = parser.parse_args(argv)
    if args.version:
        print(f"agent-failure-packet {__version__}")
        return 0
    if args.command == "init":
        output = Path(args.output)
        output.write_text(default_config_text(profile=args.profile), encoding="utf-8")
        print(f"Wrote {output}")
        return 0
    if args.command == "validate":
        try:
            data = json.loads(Path(args.input).read_text(encoding="utf-8"))
            validate_run_export(data)
        except (OSError, ValueError, PacketInputError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(f"schema_version={data['schema_version']} events={len(data['events'])}")
        return 0
    if args.command != "build":
        parser.print_help(sys.stderr)
        return 2

    try:
        config = load_config()
        profile = args.profile or config.profile
        policy_path = Path(args.redaction_policy) if args.redaction_policy else config.redaction_policy
        packet = build_packet(Path(args.input), policy_path=policy_path)
    except (OSError, ValueError, PacketInputError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    output = render_json(packet) if args.format == "json" else render_markdown(packet, profile=profile)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


def entrypoint() -> None:
    raise SystemExit(main())
