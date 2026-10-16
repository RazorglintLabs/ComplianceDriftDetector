# CDD — three-minute licensing and OEM demonstration
**Scope:** demonstrate bounded, repeatable functions on synthetic input; do not imply enterprise readiness.

## Before recording
1. Use the qualified candidate commit and record full SHA and test results.
2. Check Python 3.11+ and run `python -m pytest -q`; preserve actual output.
3. Close unrelated programs. Do not open real customer data, credentials, billing or private repos.
4. Start with `START_UI.bat` on Windows, or `python software/ui_app_sale01.py`.
5. Use the bundled **deployment_approval** example. Confirm the resulting claim counts before recording.

## 0:00–0:30 — Problem
“Policies say what should happen. The difficult question is whether supplied operating evidence continues to match them as time passes. CDD checks that specific gap at dated checkpoints.”

## 0:30–1:15 — Run
In the UI: New Scan → bundled deployment-approval example → Run Scan. Show current claim states and the **separate** undeclared-behavior count. Do not confuse missing evidence (`UNDECLARED` claim) with a behavior without policy.

## 1:15–2:00 — Demonstrate recovery, not just latest status
Open the CI-pipeline policy claim. Show the supplied checkpoints **100% → 50% → 100%**. The current state is **ALIGNED**, but the history is **RECOVERED** and the first threshold breach was **2026-01-02**. Raw first-to-last trend remains `stable`; full-history status clarifies it without altering engine results.

## 2:00–2:35 — Export and verify
Show JSON, Markdown and HTML output. Verify `output/drift_report.json` and `output/drift_evidence.json` using `python software/verify.py <path>`. Explain: report seal covers metadata and summary; evidence export hashes bind exported items and aggregates. Neither independently authenticates source truth.

## 2:35–3:00 — Licensing / OEM fit
“CDD is a bounded local component with defined inputs, explainable outputs and independent artifact checks. Razorglint retains the core IP and is offering scoped licenses, OEM embedding or a paid evaluation — not an outright sale. It is not a hosted GRC suite or a certification.”

## Post-demo licensing partner questions
- **Does it read arbitrary policy PDFs/logs?** No, the inputs are structured and pre-classified.
- **Does it continuously monitor production?** No, it analyzes supplied dated checkpoints.
- **Are hashes signatures?** No, these are unkeyed SHA-256 digests; they detect certain changes, not independent origin authenticity.
- **Does it grant exclusive rights or source ownership?** No. Default is non-exclusive scoped licensing with Razorglint retaining IP; any special rights require separate negotiated written terms.
- **What if we want integration?** Discuss a separate bounded statement of work.
