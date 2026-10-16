# Security and responsible disclosure

This repository contains proprietary code published for evaluation. CDD is a **local batch-analysis tool**, not a security monitoring agent or regulatory certification service.

If you discover a suspected security flaw, privately contact **razorglint.ops@protonmail.com** with a concise description, affected CDD version, minimal reproduction and the impact. **Do not include secrets, customer records, real production logs, credentials or confidential third-party data.** Avoid public disclosure of actively exploitable issues while they are being reviewed.

Supported local behavior: structured CSV inputs, deterministic threshold classification, locally written reports and **unkeyed SHA-256 artifact consistency checks**. Hashes are not source authenticity signatures; a party able to edit and re-hash the package can construct a new internally consistent export. The current portable Windows EXE is **unsigned**; check its published build checksums and follow enterprise execution policy.

This is a reporting contact, not a guaranteed security response SLA or bounty program.
