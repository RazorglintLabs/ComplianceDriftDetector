# Input Format Reference

## policy_claims.csv

| Column | Required | Description |
|--------|----------|-------------|
| `claim_id` | YES | Unique identifier (e.g., POL-001) |
| `description` | YES | Human-readable policy statement |
| `testable_assertion` | YES | Machine-readable assertion |
| `claim_type` | NO | REQUIREMENT, PROHIBITION, THRESHOLD, PROCESS, CONTROL (default: REQUIREMENT) |
| `threshold` | NO | Numeric threshold for THRESHOLD-type claims |

## behavior_evidence.csv

| Column | Required | Description |
|--------|----------|-------------|
| `evidence_id` | YES | Unique identifier (e.g., EV-001) |
| `timestamp` | YES | ISO 8601 timestamp (e.g., 2026-01-15T10:30:00Z) |
| `claim_ref` | YES | Which policy claim this relates to (must match a claim_id) |
| `observed_value` | YES | What was actually observed |
| `compliant` | YES | `true` or `false` — did this observation comply with the claim? |
| `source` | NO | Where this evidence came from (default: UNKNOWN) |

## Rules

- CSV must include a header row
- `compliant` accepts: `true`, `True`, `TRUE`, `1`, `yes` → compliant; anything else → non-compliant
- Timestamps must be sortable (ISO 8601 recommended)
- Use `UNDECLARED-*` prefix in `claim_ref` for behaviors with no governing policy
- No secrets, credentials, or PII in any field
