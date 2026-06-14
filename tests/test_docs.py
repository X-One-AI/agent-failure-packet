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
    action = Path("action.yml").read_text(encoding="utf-8")

    assert "agent-failure-packet build" in english
    assert "GitHub Action" in english
    assert "--profile issue" in english
    assert "agent-failure-packet init" in english
    assert "agent-failure-packet validate" in english
    assert "v0.4.1" in english
    assert "README.zh-CN.md" in english
    assert "agent-failure-packet build" in chinese
    assert "GitHub Action" in chinese
    assert "--profile issue" in chinese
    assert "agent-failure-packet init" in chinese
    assert "agent-failure-packet validate" in chinese
    assert "v0.4.1" in chinese
    assert "README.md" in chinese
    assert "agent-failure-packet.run.v1" in design
    assert "agent-failure-packet.packet.v1" in design
    assert "local-first and deterministic" in foundation
    assert "schema compatibility checks" in foundation
    assert "default redaction policy" in production
    assert "fixture corpus evidence" in production
    assert "snapshot coverage" in production
    assert "python3 -m pytest tests -q" in ci
    assert "python3 scripts/run-action.py" in action
    assert 'version = "0.4.1"' in pyproject
    assert "include README.zh-CN.md" in manifest
    assert "include action.yml" in manifest
    assert "include scripts/run-action.py" in manifest
    assert "recursive-include tests/fixtures *.json" in manifest
    assert "recursive-include tests/fixtures *.md" in manifest
    assert "## 0.4.1" in changelog
    assert "GitHub Action" in changelog


def test_issue_handoff_workflow_document_is_actionable():
    workflow = Path("docs/issue-handoff-workflow.md").read_text(encoding="utf-8")

    assert "10-minute issue handoff path" in workflow
    assert "Validate the export before building" in workflow
    assert "Attach the compact issue packet" in workflow
    assert "Redaction review" in workflow
    assert "Product gate" in workflow


def test_pr_ci_failure_handoff_document_is_actionable():
    workflow = Path("docs/pr-ci-failure-handoff.md").read_text(encoding="utf-8")

    assert "create-failure-packet" in workflow
    assert "PR/CI failure" in workflow
    assert "redaction review" in workflow
    assert "issue packet" in workflow
    assert "does not read GitHub PRs automatically" in workflow
    assert "do not paste raw logs" in workflow
