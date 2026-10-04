# Pain Statement

## The 30-Second Version

**Who feels this:** Compliance officers, engineering leaders, CISOs, and governance teams with written policies that are supposed to govern system behavior — but limited evidence about whether operating reality still matches those claims over time.

**The pain:** A policy can say one thing while operating evidence gradually shows another. If nobody compares the two across checkpoints, the gap may remain hidden until an audit, internal review, incident, or investigation.

**What this gives you:** Checkpoint-based drift measurement between structured policy claims and supplied behavior evidence. Each claim is scored against mapped evidence, trends are visible over time, and the earliest supplied checkpoint below the configured alignment threshold is surfaced.

**The artifact:** A local drift report plus evidence export showing which claims are aligned, drifting, violated, or missing mapped evidence, together with undeclared behavior findings and SHA-256 hashes for tamper evidence.

## Why This Matters

Many governance and assurance programs need evidence that controls remain effective over a period rather than only at one point in time. ComplianceDriftDetector is designed to support that narrower evidence question without claiming certification or regulatory approval.

Potential use cases include:
- audit preparation and control-review workflows;
- internal policy-to-behavior reviews;
- longitudinal evidence checks between formal assessments;
- AI governance or software-control reviews where teams already have structured claims and evidence.

The tool itself does not determine whether a framework, auditor, regulator, insurer, or customer will accept the resulting evidence.

## The Market Gap

| Existing category | The narrower gap this tool targets |
|-------------------|------------------------------------|
| Policy management tools | Comparing structured policy claims with supplied operating evidence |
| Compliance checklists | Longitudinal drift measurement across dated checkpoints |
| Configuration scanners | Mapping evidence to declared policy claims rather than only configuration state |
| Audit reports | Repeatable local evidence generation between reviews |

Compliance Drift Detector is intended to sit between "we have policies" and "we have supplied evidence showing how current behavior compares with those policies."

## Important Boundary

The current release does **not** parse raw policy documents automatically and does **not** infer compliance from raw logs. The operator supplies structured policy assertions, mapped behavior evidence, and a `compliant` value for each evidence record. The engine then measures and classifies those inputs deterministically.

## What Buyers Should Understand

This is not a replacement for a GRC platform, SIEM, auditor, or control-testing program.

Its value is narrower: it provides a small local engine and buyer-facing UI for repeatable checkpoint comparison, trend classification, artifact generation, and verification of supported JSON outputs.
