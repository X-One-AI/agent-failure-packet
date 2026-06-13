# Publishing

`agent-failure-packet` uses GitHub Actions and PyPI Trusted Publishing.

Python distribution package:

```text
xone-agent-failure-packet
```

Installed CLI:

```text
agent-failure-packet
```

## Current Index Status

As of 2026-06-13, public API checks show:

- PyPI: `xone-agent-failure-packet` is not published yet.
- TestPyPI: `xone-agent-failure-packet` is not published yet.

## GitHub Environments

Create these GitHub environments:

- `testpypi`
- `pypi`

The `pypi` environment should require manual approval.

## Trusted Publisher Settings

```text
Project: xone-agent-failure-packet
Owner: X-One-AI
Repository: agent-failure-packet
Workflow: publish.yml
Environment: testpypi or pypi
```

## Publish Order

1. Merge and verify a green CI run on `main`.
2. Confirm the release tag exists, for example `v0.4.0`.
3. Run `Publish Python Package` with `repository = testpypi`.
4. Verify a clean TestPyPI install.
5. Run `Publish Python Package` with `repository = pypi` from a release tag after approval.
6. Verify a clean PyPI install.

## TestPyPI Install Check

```bash
python -m venv /tmp/agent-failure-packet-testpypi
/tmp/agent-failure-packet-testpypi/bin/python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  xone-agent-failure-packet
/tmp/agent-failure-packet-testpypi/bin/agent-failure-packet --version
```

## PyPI Install Check

```bash
python -m venv /tmp/agent-failure-packet-pypi
/tmp/agent-failure-packet-pypi/bin/python -m pip install xone-agent-failure-packet
/tmp/agent-failure-packet-pypi/bin/agent-failure-packet --version
```

## GitHub Release Install Path

```bash
python3 -m pip install https://github.com/X-One-AI/agent-failure-packet/releases/download/v0.4.0/xone_agent_failure_packet-0.4.0-py3-none-any.whl
agent-failure-packet --version
```
