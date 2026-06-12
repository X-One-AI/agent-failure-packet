from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


_DEFAULT_PATTERNS = (
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*=\s*([^\s,;]+)"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)(https?://)[^/\s:@]+:[^/\s@]+@"),
    re.compile(r"(?i)([?&](?:token|api[_-]?key|secret|password)=)[^&#\s]+"),
)

_PLACEHOLDERS = {
    "<api-key>",
    "<token>",
    "<your-api-key>",
    "<your-token>",
    "your-api-key",
    "your-token",
    "changeme",
    "example",
    "placeholder",
}


@dataclass(frozen=True)
class RedactionResult:
    value: Any
    count: int


def load_policy(path: Path | None) -> tuple[tuple[str, ...], tuple[re.Pattern[str], ...]]:
    if path is None:
        return (), ()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    literals = tuple(str(item) for item in data.get("literals", []) if str(item))
    regexes = tuple(re.compile(str(pattern)) for pattern in data.get("regexes", []) if str(pattern))
    return literals, regexes


def redact_value(value: Any, policy_path: Path | None = None) -> RedactionResult:
    literals, regexes = load_policy(policy_path)
    return _redact_any(value, literals, regexes)


def _redact_any(value: Any, literals: tuple[str, ...], regexes: tuple[re.Pattern[str], ...]) -> RedactionResult:
    if isinstance(value, str):
        return _redact_string(value, literals, regexes)
    if isinstance(value, list):
        redacted = []
        count = 0
        for item in value:
            result = _redact_any(item, literals, regexes)
            redacted.append(result.value)
            count += result.count
        return RedactionResult(redacted, count)
    if isinstance(value, dict):
        redacted_dict = {}
        count = 0
        for key, item in value.items():
            result = _redact_any(item, literals, regexes)
            redacted_dict[key] = result.value
            count += result.count
        return RedactionResult(redacted_dict, count)
    return RedactionResult(value, 0)


def _redact_string(value: str, literals: tuple[str, ...], regexes: tuple[re.Pattern[str], ...]) -> RedactionResult:
    text = value
    count = 0

    def replace_assignment(match: re.Match[str]) -> str:
        nonlocal count
        raw_value = match.group(2).strip().strip("\"'`,.;")
        if raw_value.lower() in _PLACEHOLDERS:
            return match.group(0)
        count += 1
        return f"{match.group(1)}=[REDACTED:secret]"

    text = _DEFAULT_PATTERNS[0].sub(replace_assignment, text)
    for pattern in _DEFAULT_PATTERNS[1:]:
        if pattern.pattern.startswith("(?i)([?&]"):
            text, additions = pattern.subn(r"\1[REDACTED:secret]", text)
        else:
            text, additions = pattern.subn("[REDACTED:secret]", text)
        count += additions
    for literal in literals:
        if literal in text:
            text = text.replace(literal, "[REDACTED:custom]")
            count += value.count(literal)
    for pattern in regexes:
        text, additions = pattern.subn("[REDACTED:custom]", text)
        count += additions
    return RedactionResult(text, count)
