from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_FILENAME = ".agent-failure-packet.yml"
CONFIG_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class PacketConfig:
    profile: str = "incident"
    redaction_policy: Path | None = None


def default_config_text(profile: str = "incident") -> str:
    return (
        f"schema_version: {CONFIG_SCHEMA_VERSION}\n"
        f"profile: {profile}\n"
        "# redaction_policy: .agent-failure-packet-redaction.yml\n"
    )


def discover_config(start: Path | None = None) -> Path | None:
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for directory in (current, *current.parents):
        candidate = directory / CONFIG_FILENAME
        if candidate.exists():
            return candidate
    return None


def load_config(path: Path | None = None) -> PacketConfig:
    config_path = path or discover_config()
    if config_path is None:
        return PacketConfig()
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    schema_version = data.get("schema_version", CONFIG_SCHEMA_VERSION)
    if schema_version != CONFIG_SCHEMA_VERSION:
        raise ValueError(f"Unsupported config schema_version: {schema_version}")
    profile = str(data.get("profile", "incident"))
    if profile not in {"incident", "issue"}:
        raise ValueError(f"Unsupported profile: {profile}")
    policy = data.get("redaction_policy")
    policy_path = (config_path.parent / str(policy)).resolve() if policy else None
    return PacketConfig(profile=profile, redaction_policy=policy_path)
