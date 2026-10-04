# Self-Service Quickstart

**Run a compliance drift scan locally in about 60 seconds. No cloud service, account, or production credentials required.**

---

## What You Need

- Python 3.11+ installed
- Structured policy claims in CSV format
- Structured behavior evidence in CSV format

The current release expects each behavior-evidence row to include a supplied `compliant` true/false value. It does **not** infer compliance from raw logs or parse natural-language policy documents automatically.

No pip install, API key, or account is required for the core scanner.

---

## Step 1: Download or Clone

```bash
git clone https://github.com/RazorglintLabs/ComplianceDriftDetector.git
cd ComplianceDriftDetector
```

Or download the ZIP from GitHub and extract it.

---

## Step 2: Add Your Data

Create an `input/` folder and add two CSV files:

### `input/policy_claims.csv`

```csv
claim_id,description,testable_assertion,claim_type,threshold
POL-001,All deployments require approval,deploy.approved == true,REQUIREMENT,
POL-002,No admin access beyond 24h,admin.hours <= 24,THRESHOLD,24
```

### `input/behavior_evidence.csv`

```csv
evidence_id,timestamp,claim_ref,observed_value,compliant,source
EV-001,2026-01-01T10:00:00Z,POL-001,approved,true,deploy_log
EV-002,2026-01-02T14:00:00Z,POL-001,no approval,false,deploy_log
```

See `input_templates/` for blank templates. See `examples/template_packs/` for ready-to-use scenarios.

---

## Step 3: Run

**Windows (double-click):**
```text
START_HERE.bat
```

**Any platform (command line):**
```bash
python software/run_scan.py
```

The scanner makes no network calls and writes output locally under `output/`.

---

## Step 4: Read Your Report

Reports appear in `output/`:

| File | For |
|------|-----|
| `drift_report.html` | Browser-readable summary with drift table |
| `drift_report.md` | Markdown report |
| `drift_report.json` | Machine-readable drift report |
| `drift_evidence.json` | Complete exported policy/evidence set with hashes |

---

## Step 5: Verify Supported JSON Artifacts

```bash
python software/verify.py output/drift_report.json
python software/verify.py output/drift_evidence.json
```

The report verifier checks structure, state-count/alignment consistency, and the run-specific report seal. The evidence verifier checks every exported claim/evidence item hash plus the aggregate policy and behavior hashes.

PASS means the supported artifact is internally consistent with those checks. It does **not** establish that the source data is true, complete, independently collected, or compliant with a regulation or standard.

---

## No Input Files? No Problem.

If you run without an `input/` directory, the tool runs a built-in demo scenario with 5 policies and 314 synthetic evidence points. Use it to inspect the workflow before adding your own data.

---

## What This Does

- Measures alignment between structured policy claims and supplied behavior evidence
- Groups evidence into dated checkpoints
- Classifies each claim as ALIGNED, DRIFTING, VIOLATED, or UNDECLARED using visible thresholds
- Tracks trend direction across supplied checkpoints
- Exports report metadata and evidence hashes for tamper-evident verification

## What This Does NOT Do

- Does not certify compliance with any standard or regulation
- Does not infer compliance from raw logs
- Does not automatically parse policy documents into claims
- Does not upload input data or require an internet connection for scanning
- Does not use AI, ML, or non-deterministic scoring
- Does not replace formal audits or accredited assessments

---

## Template Packs

Ready-to-use example scenarios:

| Pack | Scenario |
|------|----------|
| `examples/template_packs/deployment_approval/` | Deployment governance drift |
| `examples/template_packs/privileged_access/` | Admin access policy drift |
| `examples/template_packs/ai_output_logging/` | AI system logging-control drift |

Copy any pack's CSVs into `input/` and run.
