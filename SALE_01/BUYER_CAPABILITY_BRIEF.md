# Compliance Drift Detector — software/IP acquisition brief
**Razorglint Labs / TCOG Collective LLC** · October 15, 2026 · non-confidential

## The capability
Written controls can say one thing while the structured evidence collected at different checkpoints says another. Compliance Drift Detector compares **operator-supplied structured policy claims** to **operator-supplied, pre-classified behavior observations**. It measures per-checkpoint alignment, highlights earlier threshold breaches, and distinguishes a recovered control from one that never drifted.

The outcome is an inspectable local report, not an automated compliance opinion.

## What is included in the present product
- Deterministic Python stdlib-only scanner, documented CSV intake and bundled examples.
- Current claim states: **ALIGNED / DRIFTING / VIOLATED / UNDECLARED** (no evidence).
- Separately counted **undeclared behavior findings** for unmatched `UNDECLARED-*` references.
- Buyer-facing history status, including **RECOVERED** when earlier below-threshold evidence precedes current alignment.
- JSON / Markdown / HTML reports; SHA-256 report seal and evidence hashes; independent consistency verifier for supported JSON artifacts.
- Local Tkinter review UI, Windows launchers, CLI and unit/regression suites.
- Bundled synthetic scenarios for deployment approval, privileged access and AI output logging.

## Why consider source/IP acquisition?
A platform, audit consultancy or specialist integrator with existing workflows could evaluate this as a compact **offline deterministic analysis component**, alongside its own data collection, governance, storage and user controls. It is not offered as a substitute for a mature GRC platform.

## Honest current boundary
- Inputs must already be structured and the `compliant` field supplied. No raw-log classification, natural-language policy parsing or live connectors.
- Claim-level numeric `threshold` is metadata only; present classification uses global thresholds.
- Batch / checkpoint analysis, not real-time continuous monitoring or preventive enforcement.
- No production-scale validation, multi-tenant service, built-in auth or longitudinal database.
- Report checksums test artifact consistency and detect certain changes; they do not prove who collected the source data, validate source truth, or provide authenticity against an adversary who recomputes hashes.
- No compliance certification, regulatory determination or guaranteed audit acceptance.
- The public repository has previously been offered under proprietary evaluation permissions. Any existing distribution/licensing rights must be disclosed and reviewed before exclusivity claims.

## Proposed transaction perimeter
Potential outright assignment of **CDD-specific transferable source and IP**, documentation, tests, example packs and verification tools, with exact items and retained third-party/prior-license rights specified in the agreement. TCOG Collective LLC, Prestige Forge / Prestige-Reforged, Viventia, SAR, VEAC, other Razorglint IP, unrelated brands/domains and future developments **are excluded**. Any transition services are separately scoped.

**Interested in evaluating the fit?** Ask for a non-confidential demo and an exact-build proof sheet. Deeper diligence and source-transfer terms follow qualified interest and, if appropriate, an NDA.

Contact: razorglint.ops@protonmail.com
Repository: https://github.com/RazorglintLabs/ComplianceDriftDetector
