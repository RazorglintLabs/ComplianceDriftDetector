# Pilot Intake Checklist — Compliance Drift Quick Scan

---

## What You Provide

### 1. Structured Policy Claims (Required)

The self-service release expects policy claims in `policy_claims.csv` using the repository template.

Required fields include:
- `claim_id`
- `description`
- `testable_assertion`

Optional fields include claim type and threshold metadata.

Example claims:

| Example Claim | Type |
|---------------|------|
| "All production deployments require manager approval" | PROCESS |
| "No persistent admin access beyond 24 hours" | PROHIBITION |
| "AI model outputs are logged with >= 99% coverage" | THRESHOLD |
| "Incident response starts within 4 hours of detection" | THRESHOLD |
| "All code changes pass automated security scan" | REQUIREMENT |

The current release does **not** parse natural-language policy documents automatically. An assisted review may help normalize claims into the CSV format if that service is explicitly agreed.

### 2. Structured Behavior Evidence (Required)

The self-service release expects `behavior_evidence.csv` using the repository template.

Each evidence row includes:
- `evidence_id`
- `timestamp`
- `claim_ref`
- `observed_value`
- `compliant` (`true` / `false`)
- optional `source`

The `compliant` value is supplied by the operator. The current release does **not** infer compliance from raw logs.

Examples of source material that an operator may normalize into evidence rows include deployment records, access records, logging measurements, workflow outputs, or configuration observations.

### 3. Time Window

Evidence can cover one or more dated checkpoints. A single checkpoint can be classified, but trend output will be `insufficient_data`. Multiple dated checkpoints are needed to show improving / stable / degrading direction.

---

## What You Do NOT Provide

| Never Send | Why |
|-----------|-----|
| Production credentials | Not required |
| API keys or tokens | Not required |
| Customer PII | Remove before any assisted review |
| Unredacted names/emails | Anonymize when identity is not required for the claim |
| Source code | Not required by the standard workflow |
| Full database dumps | Not required |
| Secrets or certificates | Never required |

---

## Anonymization Guide

Before sending material for an assisted review:

1. Replace real names with roles where identity is not relevant.
2. Replace sensitive system names with neutral identifiers where possible.
3. Preserve timestamps when time ordering matters.
4. Preserve the boolean/numeric values needed for the selected claim.
5. Remove IP addresses and unrelated identifiers unless they are necessary for the claim being evaluated.
6. Remove any field that is not required for the scoped analysis.

**Rule:** minimize the data to the narrow evidence needed for the selected claim.

---

## Scope Boundary

| In Scope | Out of Scope |
|----------|-------------|
| Structured policy-behavior alignment measurement | Penetration testing |
| Checkpoint trend analysis | Vulnerability scanning |
| Surfacing unmatched `UNDECLARED-` behavior references | General anomaly discovery |
| Tamper-evident report/evidence artifacts | Architecture assessment |
| Exportable evidence for review workflows | Remediation implementation |

The tool measures supplied structured evidence. It does not fix drift, establish overall security posture, certify compliance, or validate the truth/completeness of the source data.

---

## Assisted Review Workflow

If an assisted review is separately agreed:

1. Scope the claims and accepted input format.
2. Confirm that submitted material is appropriately minimized/redacted.
3. Normalize accepted material into the supported structured format where agreed.
4. Run the local detector and verifier.
5. Return the agreed report/evidence artifacts and interpretation.

Any delivery timeline or support commitment should be agreed in writing for that engagement; this checklist does not create a fixed service-level commitment.

---

## Self-Service Path

For the current product workflow, start with:

- `SELF_SERVICE_QUICKSTART.md`
- `input_templates/policy_claims.csv`
- `input_templates/behavior_evidence.csv`
- `examples/template_packs/`
