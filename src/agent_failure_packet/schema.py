from __future__ import annotations

RUN_SCHEMA_VERSION = "agent-failure-packet.run.v1"
PACKET_SCHEMA_VERSION = "agent-failure-packet.packet.v1"


class PacketInputError(ValueError):
    pass


def validate_run_export(data: dict) -> None:
    schema_version = data.get("schema_version")
    if schema_version != RUN_SCHEMA_VERSION:
        raise PacketInputError(f"Unsupported schema_version: {schema_version}")
    for key in ("run", "environment", "events"):
        if key not in data:
            raise PacketInputError(f"Missing required field: {key}")
    if not isinstance(data["run"], dict):
        raise PacketInputError("Field 'run' must be an object")
    if not isinstance(data["environment"], dict):
        raise PacketInputError("Field 'environment' must be an object")
    if not isinstance(data["events"], list):
        raise PacketInputError("Field 'events' must be a list")
