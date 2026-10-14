# Compliance Drift Detector — commercial licensing / OEM capability brief
**Razorglint Labs / TCOG Collective LLC** · October 15, 2026 · NON-CONFIDENTIAL
**Commercial posture: IP RETAINED. LICENSING / OEM / INTEGRATION PARTNERSHIPS. NOT OFFERED FOR SALE.**

## The problem
A documented control can appear healthy today even when earlier structured operating evidence shows that the process drifted or crossed a threshold. Existing point-in-time reporting can miss this historical context.

## The capability
**Compliance Drift Detector (CDD)** compares operator-supplied, structured policy claims with operator-supplied, **pre-classified** behavior observations across dated checkpoints. It computes deterministic alignment states (**ALIGNED, DRIFTING, VIOLATED, UNDECLARED**), distinguishes unmatched undeclared-behavior findings, highlights first threshold breaches and presents historical **RECOVERED** states.

The output is inspectable, local reporting — **not** an automatic compliance opinion.

## Available implementation
- Python 3.11+ stdlib-only scanner and independent JSON consistency verifier.
- Defined CSV intake, documentation, synthetic examples and Windows launchers.
- Local Tkinter desktop interface plus CLI.
- JSON / Markdown / HTML reports with SHA-256 seals and item/aggregate evidence hashes.
- Regression testing, including cross-platform qualification against the current candidate branch (not a production-certification claim).

## How we partner
Razorglint Labs **retains ownership** and seeks:
- Product/internal-use licenses and paid evaluations.
- Bounded team, consulting and multi-deployment licensing.
- **OEM / embedded technology licensing** into an existing platform, on negotiated terms.
- Clearly scoped integrations and commercial partnerships.

Existing published self-service license tiers include Starter **$49/month**, Team **$149/month** and Consultant **$299/month**. **OEM/enterprise source integration is custom-scoped and custom-quoted**; no blanket exclusivity, source rights, derivative rights or resale rights are implied. Actual customer/revenue status must be independently verified.

## Exact limits
- No automatic raw-log interpretation, natural-language policy ingestion, live production collectors, preventive enforcement, multi-tenant hosted service or compliance certification.
- The operator supplies `compliant` classification; claim-level numeric `threshold` remains descriptive metadata, while **global alignment thresholds** control scoring.
- Hash checks support artifact consistency/tamper evidence, **not authenticated original-source provenance**, and an adversary able to rewrite/re-hash an export can produce a new self-consistent file.
- Not yet proven at production scale. New integration, support and deployment responsibilities must be contractually defined.

## IP boundary
All CDD source/IP ownership remains with **TCOG Collective LLC / Razorglint Labs**, subject to documented rights. Prestige Forge / Prestige-Reforged, Viventia, SAR, VEAC and all other Razorglint IP are **excluded**. No assignment or acquisition of IP is being offered in this outreach.

**Contact:** razorglint.ops@protonmail.com
**Repository:** https://github.com/RazorglintLabs/ComplianceDriftDetector

*Next step: request a three-minute synthetic demo and a discussion of your intended deployment / OEM integration use case.*
