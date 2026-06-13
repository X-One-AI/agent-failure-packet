# Homebrew Packaging

`agent-failure-packet` is distributed through the X-One tap.

## User Install

```bash
brew tap x-one-ai/tap
brew trust --formula x-one-ai/tap/agent-failure-packet
brew install x-one-ai/tap/agent-failure-packet
agent-failure-packet --version
```

## Tap Repository

```text
X-One-AI/homebrew-tap
```

Formula path:

```text
Formula/agent-failure-packet.rb
```

## Formula Requirements

- Install the Python CLI as `agent-failure-packet`.
- Use the released `xone-agent-failure-packet` source distribution.
- Vendor Python dependencies as Homebrew resources.
- Run `agent-failure-packet --version` in the formula test.

## Current Target

```text
xone-agent-failure-packet==0.4.1
```
