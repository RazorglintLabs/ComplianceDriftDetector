# Self-Service Quickstart

**Run a compliance drift scan locally in 60 seconds. No cloud. No credentials. No data leaves your machine.**

---

## What You Need

- Python 3.11+ installed
- Your policy claims in CSV format
- Your system behavior evidence in CSV format

That's it. No pip install. No API keys. No account.

---

## Step 1: Download or Clone

```
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
```
START_HERE.bat
```

**Any platform (command line):**
```
python software/run_scan.py
```

---

## Step 4: Read Your Report

Reports appear in `output/`:

| File | For |
|------|-----|
| `drift_report.html` | Open in browser — executive summary with drift table |
| `drift_report.md` | Markdown — paste into docs or share with team |
| `drift_report.json` | Machine-readable — feed into other tools |
| `drift_evidence.json` | Full evidence with per-item hashes |

---

## Step 5: Verify (Optional)

```
python software/verify.py
```

This recalculates all hashes and confirms nothing was modified. Returns PASS or FAIL.

---

## No Input Files? No Problem.

If you run without an `input/` directory, the tool runs a built-in 30-day demo scenario with 5 policies and 314 evidence points. Use it to see what output looks like before adding your own data.

---

## What This Does

- Measures alignment between your stated policies and your observed system behavior
- Classifies each claim: ALIGNED, DRIFTING, VIOLATED, or UNDECLARED
- Tracks trend direction over your time window
- Seals the report with SHA-256 hashes for tamper evidence

## What This Does NOT Do

- Does not certify compliance with any standard
- Does not send data anywhere — everything stays on your machine
- Does not require an internet connection
- Does not use AI, ML, or any non-deterministic logic
- Does not replace formal audits — it produces evidence for audit preparation

---

## Template Packs

Ready-to-use example scenarios:

| Pack | Scenario |
|------|----------|
| `examples/template_packs/deployment_approval/` | Deployment governance drift |
| `examples/template_packs/privileged_access/` | Admin access policy drift |
| `examples/template_packs/ai_output_logging/` | AI system monitoring drift |

Copy any pack's CSVs into `input/` and run.
