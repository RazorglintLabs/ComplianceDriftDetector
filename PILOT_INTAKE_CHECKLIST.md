# Pilot Intake Checklist — Compliance Drift Quick Scan

---

## What You Provide

### 1. Policy Claims (Required)

Testable policy statements your organization enforces. Examples:

| Example Claim | Type |
|---------------|------|
| "All production deployments require manager approval" | PROCESS |
| "No persistent admin access beyond 24 hours" | PROHIBITION |
| "AI model outputs are logged with >= 99% coverage" | THRESHOLD |
| "Incident response starts within 4 hours of detection" | THRESHOLD |
| "All code changes pass automated security scan" | REQUIREMENT |

**Format:** Plain text, bullet list, or table. 1–3 claims for intro scan, up to 10 for expanded.

### 2. Behavior Evidence (Required)

Anonymized system behavior data showing what actually happened. Examples:

| Evidence Type | What To Send |
|---------------|-------------|
| Deployment logs | Timestamps, approval status (approved/unapproved), deployer role |
| Access records | Session durations, privilege levels, access type |
| Monitoring logs | Coverage percentages, logging gaps, timestamps |
| Workflow outputs | Response times, completion status, gate results |
| Config snapshots | Control states at different points in time |

**Format:** JSON, CSV, or structured text. One row per observation.

### 3. Time Window (Required)

How many days/weeks of data to analyze. Minimum: 7 days. Recommended: 14–30 days.

---

## What You Do NOT Provide

| Never Send | Why |
|-----------|-----|
| Production credentials | Not needed — we analyze behavior data, not live systems |
| API keys or tokens | Not needed |
| Customer PII | Remove before sending — we need behavior patterns, not identities |
| Unredacted names/emails | Anonymize with roles (e.g., "deployer_A", "admin_B") |
| Source code | Not needed |
| Full database dumps | Not needed — send relevant log excerpts only |
| Secrets or certificates | Never |

---

## Anonymization Guide

Before sending behavior data:

1. Replace real names with roles: `"john.smith"` → `"deployer_A"`
2. Replace real system names if sensitive: `"prod-db-01"` → `"system_A"`
3. Keep timestamps intact (we need time ordering)
4. Keep boolean/numeric values intact (we need compliance signal)
5. Remove IP addresses unless relevant to the policy claim
6. Remove any field you're uncomfortable sharing

**Rule:** If removing a field doesn't break the compliance signal, remove it.

---

## Scope Boundary

| In Scope | Out of Scope |
|----------|-------------|
| Policy-behavior alignment measurement | Penetration testing |
| Drift trend analysis over time | Vulnerability scanning |
| Undeclared behavior detection | Code review |
| Tamper-evident report generation | Architecture assessment |
| Evidence export for auditors | Remediation implementation |

We measure drift. We don't fix it, and we don't assess your overall security posture.

---

## Delivery

| Step | Timeline |
|------|----------|
| You send intake materials | Day 0 |
| We confirm scope and acceptance | Within 24 hours |
| We run analysis and deliver report | Within 48 hours of acceptance |
| You receive: drift report (MD + JSON) + evidence export + verifier | Day 2–3 |

---

## Ready?

Send your policy claims and anonymized behavior data to begin. We'll confirm scope and timeline within 24 hours.
