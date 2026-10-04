# ComplianceDriftDetector — Claim Boundaries

## Purpose

This document defines what ComplianceDriftDetector IS and IS NOT allowed to claim.
Every public statement, README sentence, and buyer communication must stay within these boundaries.

---

## Allowed Claims

| # | Claim | Evidence |
|---|-------|----------|
| 1 | "Detects drift between stated policy claims and supplied behavior evidence" | Core engine classifies ALIGNED / DRIFTING / VIOLATED / UNDECLARED from structured inputs |
| 2 | "Produces tamper-evident report metadata and hash-anchored evidence exports" | SHA-256 report seal, per-item evidence hashes, aggregate policy/behavior hashes |
| 3 | "Core scanner/verifier use zero external Python packages" | stdlib-only core; optional desktop UI uses Tkinter |
| 4 | "Deterministic classification for the same structured inputs and thresholds" | Visible threshold logic and repeatable checkpoint measurement |
| 5 | "All scoring rules visible in source" | AlignmentEngine thresholds are configurable and rendered in output |
| 6 | "No blackbox scoring" | Classification logic is threshold-based and visible in source |
| 7 | "Supported JSON artifacts are independently verifiable" | verify.py checks report seal/consistency plus all exported item and aggregate hashes |
| 8 | "Checkpoint-based evidence between audit points" | Evidence is grouped into dated checkpoints and compared longitudinally |
| 9 | "Surfaces undeclared behavior references" | Unmatched evidence references prefixed `UNDECLARED-` are reported separately |
| 10 | "Current qualified test suite passes in the sealed sale build" | Fresh qualification receipt records the exact candidate and test result |

## Required Input Boundary

The current release does **not** infer compliance from raw logs and does **not** parse natural-language policy documents automatically.

Policy claims are supplied as structured assertions. Behavior evidence is supplied with a mapped `claim_ref` and a `compliant` boolean. The engine measures and classifies those supplied inputs deterministically.

## Forbidden Claims

| # | Forbidden | Why | Safe Alternative |
|---|-----------|-----|------------------|
| 1 | "Compliant" | We detect drift; we do not certify compliance | "Measures policy-behavior alignment in supplied evidence" |
| 2 | "Certified" | No certification authority involved | "Produces evidence that can support certification preparation" |
| 3 | "Prevents violations" | Detection only, not enforcement | "Classifies supplied evidence against visible thresholds" |
| 4 | "Real-time monitoring" | Batch checkpoint analysis | "Checkpoint-based longitudinal drift analysis" |
| 5 | "Replaces audits" | Supplements, not replaces | "Provides evidence between audit points" |
| 6 | "Guaranteed detection" | Completeness depends on supplied claims/evidence | "Systematic measurement of supplied structured evidence" |
| 7 | "AI-powered" | No ML, no LLM, no AI | "Deterministic rule-based analysis" |
| 8 | "Tamper-proof" | Hashing is tamper-evident, not tamper-proof | "Tamper-evident" |
| 9 | "Enterprise-ready" | No auth, multi-tenancy, HA, or hosted control plane | "Standalone local engine with buyer-facing UI" |
| 10 | "SOC 2 compliant" / "ISO 27001 compliant" / "EU AI Act compliant" | The tool is not an accredited assessment body | "Can produce evidence useful in readiness or audit-preparation workflows" |
| 11 | "Automatically understands raw logs/policies" | Inputs are structured by the user/operator | "Consumes structured policy claims and behavior evidence" |

## Vocabulary Discipline

| Use | Don't Use |
|-----|-----------|
| "Drift detection" | "Compliance assurance" |
| "Policy-behavior gap measurement" | "Compliance verification" |
| "Tamper-evident" | "Tamper-proof" |
| "Evidence for audit preparation" | "Replaces auditors" |
| "Readiness evidence" | "Certification" |
| "Checkpoint-based" | "Real-time" |
| "Deterministic" | "Intelligent" / "Smart" |
| "Supplied behavior evidence" | "Automatically observed production behavior" |
| "Earliest supplied checkpoint showing divergence" | "Proof of when drift started" |

## Boundary Tests

Before any public claim, ask:

1. Can we demonstrate it with the current code and a test run? If no → forbidden.
2. Does it imply a guarantee we cannot back? If yes → forbidden.
3. Does it claim authority we do not have? If yes → forbidden.
4. Does it imply automated data collection or interpretation that the current release does not perform? If yes → reword.
5. Would a hostile auditor or buyer find it misleading? If yes → reword.
6. Is there a narrower true statement? If yes → use that instead.
