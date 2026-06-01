# ComplianceDriftDetector — Claim Boundaries

## Purpose

This document defines what ComplianceDriftDetector IS and IS NOT allowed to claim.
Every public statement, README sentence, and buyer communication must stay within these boundaries.

---

## Allowed Claims

| # | Claim | Evidence |
|---|-------|----------|
| 1 | "Detects drift between stated policy and observed system behavior" | Core engine classifies ALIGNED / DRIFTING / VIOLATED / UNDECLARED |
| 2 | "Produces tamper-evident drift reports" | SHA-256 sealed reports with deterministic hashing |
| 3 | "Zero external dependencies" | stdlib-only: hashlib, json, dataclasses, datetime, enum, pathlib |
| 4 | "Deterministic — same inputs produce same outputs" | Frozen dataclasses, sorted JSON, documented preimage format |
| 5 | "All scoring rules visible in source" | AlignmentEngine thresholds are configurable and rendered in output |
| 6 | "No blackbox scoring" | Classification logic is 3 thresholds, all shown in report |
| 7 | "Independently verifiable" | verify.py recalculates hashes from artifacts — PASS/FAIL |
| 8 | "Continuous monitoring between audit points" | Checkpoint-based measurement over time windows |
| 9 | "Identifies undeclared system behaviors" | Evidence with no matching policy claim is surfaced |
| 10 | "27 automated tests, all PASS" | pytest suite covers all engine paths |

## Forbidden Claims

| # | Forbidden | Why | Safe Alternative |
|---|-----------|-----|------------------|
| 1 | "Compliant" | We detect drift, not certify compliance | "Monitors policy-behavior alignment" |
| 2 | "Certified" | No certification authority involved | "Produces evidence for certification processes" |
| 3 | "Prevents violations" | Detection only, not enforcement | "Detects violations when they occur" |
| 4 | "Real-time monitoring" | Batch checkpoint analysis | "Continuous checkpoint-based monitoring" |
| 5 | "Replaces audits" | Supplements, not replaces | "Provides continuous evidence between audits" |
| 6 | "Guaranteed" | No guarantees on detection completeness | "Systematic measurement against declared policy" |
| 7 | "AI-powered" | No ML, no LLM, no AI — deterministic rules only | "Deterministic rule-based analysis" |
| 8 | "Tamper-proof" | Hash sealing is tamper-evident, not tamper-proof | "Tamper-evident" |
| 9 | "Enterprise-ready" | No auth, no multi-tenancy, no HA | "Production-grade proof logic" |
| 10 | "SOC 2 compliant" / "ISO 27001 compliant" | Not certified against these standards | "Produces evidence mappable to SOC 2 / ISO 27001 controls" |

## Vocabulary Discipline

| Use | Don't Use |
|-----|-----------|
| "Drift detection" | "Compliance assurance" |
| "Policy-behavior gap measurement" | "Compliance verification" |
| "Tamper-evident" | "Tamper-proof" |
| "Evidence for auditors" | "Replaces auditors" |
| "Readiness evidence" | "Certification" |
| "Checkpoint-based" | "Real-time" |
| "Deterministic" | "Intelligent" / "Smart" |

## Boundary Tests

Before any public claim, ask:

1. Can we prove it with a test run? If no → forbidden.
2. Does it imply a guarantee we can't back? If yes → forbidden.
3. Does it claim authority we don't have? If yes → forbidden.
4. Would a hostile auditor find it misleading? If yes → reword.
5. Is there a narrower true statement? If yes → use that instead.
