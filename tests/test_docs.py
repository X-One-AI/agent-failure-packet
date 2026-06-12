from pathlib import Path


def test_docs_and_package_metadata_stay_aligned():
    english = Path("README.md").read_text(encoding="utf-8")
    chinese = Path("README.zh-CN.md").read_text(encoding="utf-8")
    foundation = Path("docs/product-foundation.md").read_text(encoding="utf-8")
    design = Path("docs/superpowers/specs/2026-06-13-packet-builder-design.md").read_text(encoding="utf-8")
    production = Path("ops/constraints/production.md").read_text(encoding="utf-8")
    ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    manifest = Path("MANIFEST.in").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")

    assert "agent-failure-packet build" in english
    assert "--profile issue" in english
    assert "v0.2.0" in english
    assert "README.zh-CN.md" in english
    assert "agent-failure-packet build" in chinese
    assert "--profile issue" in chinese
    assert "v0.2.0" in chinese
    assert "README.md" in chinese
    assert "agent-failure-packet.run.v1" in design
    assert "agent-failure-packet.packet.v1" in design
    assert "local-first and deterministic" in foundation
    assert "default redaction policy" in production
    assert "fixture corpus evidence" in production
    assert "python3 -m pytest tests -q" in ci
    assert 'version = "0.2.0"' in pyproject
    assert "include README.zh-CN.md" in manifest
    assert "recursive-include tests/fixtures *.json" in manifest
    assert "## 0.2.0" in changelog
    assert "runtime fixture corpus" in changelog
