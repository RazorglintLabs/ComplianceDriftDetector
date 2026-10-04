# Compliance Drift Detector

**The problem:** Written policy and observed system behavior can diverge over time, and the gap may remain invisible until a review, audit, incident, or internal investigation.

**The evidence path:** Compare structured policy claims against supplied behavior evidence at dated checkpoints, measure alignment, surface drift, and hash-anchor the resulting artifacts.

**The outcome:** A local drift report showing which policy claims are aligned, drifting, violated, or missing evidence — plus undeclared behavior findings, checkpoint history, and independently verifiable hash artifacts.

---

## What This Does

Compliance Drift Detector ingests structured policy claims and structured behavior evidence.

| Input | What it is |
|-------|-----------|
| Policy claims | Testable assertions describing what policy says should happen |
| Behavior evidence | Dated observations mapped to a policy claim |
| `compliant` value | A supplied true/false classification for each evidence record |
| Checkpoint timestamps | Dates used to group evidence into longitudinal checkpoints |

It produces:

| Output | Meaning |
|--------|---------|
| `ALIGNED` | Latest supplied evidence meets the configured alignment threshold |
| `DRIFTING` | Latest alignment is below the alignment threshold but above the violation threshold |
| `VIOLATED` | Latest alignment is below the configured violation threshold |
| `UNDECLARED` | No mapped evidence was supplied for that policy claim |

Evidence rows whose `claim_ref` begins with `UNDECLARED-` and does not match a policy claim are also surfaced separately as **undeclared behaviors**.

### Important input boundary

The current release does **not** infer compliance from raw logs and does **not** parse natural-language policy documents into claims automatically. Policy assertions and evidence classification are supplied as structured input. The engine then performs deterministic checkpoint measurement, trend detection, classification, reporting, and verification.

## How It Works

1. **Load claims** — Read structured policy claims from CSV or Python data
2. **Load evidence** — Read structured behavior evidence mapped to claim IDs
3. **Checkpoint** — Group evidence by date from supplied timestamps
4. **Measure** — Calculate per-claim alignment as compliant evidence / total mapped evidence
5. **Trend** — Compare checkpoint alignment over time using a visible sensitivity threshold
6. **Classify** — Assign ALIGNED / DRIFTING / VIOLATED / UNDECLARED using visible thresholds
7. **Seal** — Hash-anchor report metadata, policy inputs, behavior inputs, and exported evidence items

Every classification threshold is configurable and visible in source. No ML or LLM scoring is involved.

## Run Locally in 60 Seconds

**No cloud service is required. No credentials are required. The scanner makes no network calls.**

```bash
# 1. Add your CSVs to input/
#    (or skip this step to run the built-in demo)

# 2. Run
python software/run_scan.py

# 3. Open output/drift_report.html in your browser
```

See [SELF_SERVICE_QUICKSTART.md](SELF_SERVICE_QUICKSTART.md) for the full walkthrough.

**Windows users:** Double-click `START_HERE.bat`.

## Self-Service Mode

| Step | What You Do |
|------|-------------|
| 1 | Put `policy_claims.csv` + `behavior_evidence.csv` in `input/` |
| 2 | Run `python software/run_scan.py` |
| 3 | Open `output/drift_report.html` |

Template CSVs: `input_templates/`  
Example packs: `examples/template_packs/` (deployment, access, AI logging)

The local scanner does not upload your data or require an internet connection.

## Local Desktop UI

The Sale 01 desktop UI is a thin local shell over the same CSV loaders, deterministic engine, report renderers, and verifier.

```bash
python software/ui_app.py
```

**Windows users:** Double-click `START_UI.bat`.

The four-screen flow is intentionally small:

1. **New Scan** — choose policy and behavior CSV files
2. **Results** — review ALIGNED / DRIFTING / VIOLATED / UNDECLARED status
3. **Evidence Detail** — inspect checkpoint measurements and hashes
4. **Export & Verify** — open generated reports and verify supported JSON artifacts

The UI does not replace or reinterpret the engine. The CLI remains independently runnable.

Frozen design reference: [UI_DESIGN_REFERENCE.md](UI_DESIGN_REFERENCE.md)  
Editable Figma source: https://www.figma.com/design/0xFZtfAvEbZ0Qenz0rLcMM

## Run the Demo

```bash
python software/run_demo.py
```

Produces:
- `output/drift_report.json` — machine-readable drift analysis
- `output/drift_report.md` — human-readable report
- `output/drift_report.html` — browser-viewable report
- `output/drift_evidence.json` — complete exported evidence set with hashes

## Verify Supported JSON Artifacts

```bash
python software/verify.py output/drift_report.json
python software/verify.py output/drift_evidence.json
```

The verifier checks:
- report structure, state-count consistency, aligned-percentage consistency, and the report metadata/summary seal;
- every exported policy-claim hash;
- every exported behavior-evidence hash;
- aggregate policy and behavior hashes.

It returns PASS or FAIL. Verification establishes artifact consistency and tamper evidence; it does **not** establish that the supplied source data is true, complete, regulatory-compliant, or independently collected from production systems.

## Requirements

- Python 3.11+
- Core scanner/verifier: zero external Python package dependencies (stdlib only)
- Desktop UI: Tkinter; included with standard Windows/macOS Python distributions. Some minimal Linux installations may require the system Tk package.

## Architecture

```text
structured policy_claims.csv + behavior_evidence.csv
                         ↓
              [ CSV input loaders ]
                         ↓
             [ daily checkpoints ]
                         ↓
              [ AlignmentEngine ]
                         ↓
       [ trend + threshold classifier ]
                         ↓
 JSON / Markdown / HTML report + evidence export
                         ↕
          [ verifier ]   [ optional local UI ]
```

## The Key Insight

Point-in-time reviews can miss what changed between checkpoints.

This tool asks: **"Does the supplied operating evidence still align with declared policy, and what is the earliest supplied checkpoint where divergence becomes visible?"**

That is a narrower, testable question than claiming compliance or certification.

## License / Use

Copyright © 2026 Razorglint Labs / TCOG Collective LLC. All rights reserved.

This repository is published for evaluation and buyer demonstration. No open-source license is granted. See `NOTICE.md`.

Commercial use, resale, hosted-service use, redistribution, or modified redistribution requires written permission from Razorglint Labs / TCOG Collective LLC.

## Monthly Licenses

| Tier | Price | Best For |
|---|---:|---|
| Starter | $49/mo | Solo/internal evaluation |
| Team | $149/mo | Internal compliance/security teams |
| Consultant | $299/mo | vCISOs, SOC 2/ISO/GRC consultants |

- Starter — [$49/mo, 7-day free trial](https://buy.stripe.com/cNi5kxghbd3CbdKfKn1ZS08)
- Team — [$149/mo](https://buy.stripe.com/fZubIVe934x61DadCf1ZS07)
- Consultant — [$299/mo](https://buy.stripe.com/14AdR39SNgfOepW8hV1ZS06)

Download the local kit. Run it on your machine. If you want updates, support, or commercial/client-facing use, choose a license.

No production credentials, customer PII, or secrets are required by the product workflow.

See `LICENSE_TIERS.md` for full details.

## Policies

- [Terms of Service](TERMS_OF_SERVICE.md)
- [Privacy Policy](PRIVACY_POLICY.md)
- [Refund and Cancellation Policy](REFUND_AND_CANCELLATION_POLICY.md)
- [Notice](NOTICE.md)
