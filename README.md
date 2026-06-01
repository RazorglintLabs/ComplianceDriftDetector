# Compliance Drift Detector

**One painful thing:** Your stated policies and your actual system behavior diverge silently over time — and nobody notices until the audit.

**One proof path:** Compare policy declarations against system behavior evidence at every checkpoint — hash-anchor both sides, measure the delta.

**One outcome:** A tamper-evident drift report showing exactly which policy claims are aligned, drifting, violated, or undeclared — with cryptographic proof of when drift started.

---

## The Pain

You wrote a policy that says: "All deployments require approval."  
Six months later, 23% of deployments have no approval record.

Nobody noticed because:
- The policy doc hasn't been opened since it was signed
- The CI/CD system evolved without checking the policy
- The audit is annual — drift accumulated silently for 11 months

This is **compliance drift**. It's the #1 reason companies fail audits they thought they'd pass.

## What This Does

Compliance Drift Detector ingests:

| Input | What it is |
|-------|-----------|
| Policy declarations | What you claim your system does |
| System behavior logs | What your system actually does |
| Configuration snapshots | System state at points in time |
| Checkpoint timestamps | When evidence was captured |

And produces:

| Output | Meaning |
|--------|---------|
| `ALIGNED` | Policy matches behavior — evidence confirms compliance |
| `DRIFTING` | Behavior is diverging from policy — trend detected |
| `VIOLATED` | Clear evidence that behavior contradicts policy |
| `UNDECLARED` | System behavior has no corresponding policy |

## How It Works (No Blackbox)

1. **Parse** — Extract policy claims as testable assertions
2. **Observe** — Extract system behavior as measurable facts
3. **Match** — Map each policy claim to relevant behavior evidence
4. **Measure** — Calculate alignment score per claim per checkpoint
5. **Trend** — Detect drift direction over multiple checkpoints
6. **Classify** — Assign drift state based on alignment trajectory
7. **Seal** — Hash the entire analysis for tamper evidence

Every threshold is configurable and visible. Every measurement rule is in source. No hidden scoring.

## Run Locally in 60 Seconds

**No cloud. No credentials. No data leaves your machine.**

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

No data leaves your machine. No internet connection required.

## Run the Demo

```bash
python software/run_demo.py
```

Produces:
- `output/drift_report.json` — machine-readable drift analysis
- `output/drift_report.md` — human-readable report
- `output/drift_report.html` — browser-viewable executive report
- `output/drift_evidence.json` — full evidence with hashes

## Verify Any Output

```bash
python software/verify.py
```

Returns PASS or FAIL. No ambiguity.

## Requirements

- Python 3.11+
- Zero external dependencies (stdlib only)

## Architecture

```
policy declarations + system behavior + config snapshots + timestamps
                              ↓
                    [ Policy Parser ] ←── extracts testable claims
                              ↓
                    [ Behavior Observer ] ←── extracts measurable facts
                              ↓
                    [ Alignment Engine ] ←── maps claims to evidence
                              ↓
                    [ Drift Classifier ] ←── trends + thresholds (visible)
                              ↓
   drift_report.json + drift_report.md + drift_evidence.json
```

## The Key Insight

Most compliance tools ask: "Are you compliant today?"

This tool asks: **"Are you drifting away from compliance — and can you prove when it started?"**

That's the difference between a point-in-time checkbox and continuous governance evidence.

## License

Proprietary — RazorGlint Labs. All rights reserved.
