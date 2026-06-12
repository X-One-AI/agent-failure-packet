# Production Constraints

- This is not a demo repository. Every shipped behavior must be usable in a real review workflow.
- Do not claim runtime protection, sandboxing, or complete security coverage unless the implementation truly provides it.
- Redaction is mandatory before sharing evidence, packets, reports, or examples.
- The first product surface must stay local-first: no uploads, network calls, hosted storage, or PR comments by default.
- The default redaction policy may be extended by users but must not be disabled.
- Packet outputs must include limitations so users do not treat regex redaction as complete security coverage.
- Prefer deterministic local behavior before introducing hosted services.
- Keep failure modes explicit and documented.
- Every rule, score, label, or scenario must have evidence or a limitation note.
