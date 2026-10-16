# Compliance Drift Detector

**Local-first, deterministic evidence-history analysis for structured policy controls.**

[Windows quickstart](WINDOWS_EXE_QUICKSTART.md) · [Python/CLI quickstart](SELF_SERVICE_QUICKSTART.md) · [Capability boundaries](CLAIM_BOUNDARIES.md) · [Build and release status](docs/RELEASE_STATUS.md) · [Licensing](LICENSE_TIERS.md)

> **Windows v0.2 technical preview accepted — 16 October 2026.** The Windows x64 portable EXE passed a native owner walkthrough, and the build pipeline passed **76 regression tests** on Windows/Linux with Python 3.11/3.12. Current portable binaries are **unsigned** and intended for controlled evaluation, not unattended enterprise rollout. The last public tagged GitHub Release remains an older v0.1.x source/self-service kit; use the [release status](docs/RELEASE_STATUS.md) to identify the verified v0.2 build rather than assuming the latest tagged release is current.

## What it does

CDD measures how **operator-supplied, pre-classified** observations align with **operator-supplied structured** policy claims across dated checkpoints. It makes recovery from an earlier below-threshold checkpoint visible even when a control is currently healthy.

| Output | Interpretation |
| --- | --- |
| **ALIGNED** | Latest supplied evidence meets the global alignment threshold |
| **DRIFTING** | Latest alignment is below alignment threshold but not below violation threshold |
| **VIOLATED** | Latest alignment is below the violation threshold |
| **UNDECLARED (no evidence)** | No mapped evidence was supplied for this policy claim |
| **Undeclared behavior finding** | Unmatched `UNDECLARED-*` evidence reference; counted **separately**, not as a policy state |
| **RECOVERED history** | Currently aligned after an earlier below-alignment-threshold checkpoint |

The built-in **synthetic deployment-approval example** demonstrates three claims, 13 evidence records, two current violations and one recovered control. Results are generated from example inputs; they are **not an assessment of any real organization's compliance**.

## Windows — portable executable

1. Obtain the current Windows evaluation ZIP from the approved distribution channel / [verified build record](docs/RELEASE_STATUS.md). Older tagged releases are not the current EXE.
2. Extract the ZIP and run **`ComplianceDriftDetector.exe`**. No Python, terminal, or `.bat` files are required.
3. Select **Load example → Run Compliance Drift Scan**.
4. Review current classifications and checkpoint history, then open **Export & Verify**.
5. Verify **report** and **evidence** separately and open the HTML report if needed.

Reports are written locally to `%LOCALAPPDATA%\RazorglintLabs\ComplianceDriftDetector\output`. Bundled synthetic examples are unpacked temporarily by the one-file executable. The local scan does not upload inputs or require a cloud account.

**Unsigned preview:** Windows SmartScreen may say **Unknown publisher**. Check provenance and SHA-256 against the release receipt and follow your organization's security policy. Do **not** disable security controls to run the app. [Windows setup, verification and limitations](WINDOWS_EXE_QUICKSTART.md).

## Python / integration

Requires Python **3.11+**. Scanner/reporting/verifier use the Python standard library; the optional desktop UI uses Tkinter. `pytest` is only needed for tests.

```bash
python software/run_demo.py
python software/verify.py output/drift_report.json
python software/verify.py output/drift_evidence.json
python -m pytest -q
```

For CSV intake and the source UI, see the [CLI quickstart](SELF_SERVICE_QUICKSTART.md) and [input schema](input_templates/README_INPUT_FORMAT.md). The Windows EXE's `Export & Verify` screen performs supported verification without Python.

## Outputs & integrity boundary

CDD produces `drift_report.html`, `drift_report.md`, `drift_report.json`, and `drift_evidence.json`.

**Version 2 JSON** report sealing covers detailed claim analyses, checkpoint history, unmatched undeclared findings, metadata and summaries. **Version 2 evidence** sealing binds the complete exported JSON package in addition to individual and aggregate hashes. The verifier explicitly identifies **legacy v1** files as limited when their older coverage applies.

**Important:** These SHA-256 hashes verify self-consistency and detect certain changes. They are **not digital signatures**, authenticated source provenance, or protection against someone who changes data and recomputes its hashes. The HTML/Markdown renders themselves are not independently cryptographically signed. For verification use the JSON artifacts.

## Scope and limitations

- CDD does **not** classify raw logs, inspect arbitrary policy PDFs, collect live production telemetry, or enforce controls.
- The operator supplies `compliant` flags. Claim-level numeric `threshold` fields are **metadata only**; scoring uses global alignment/violation thresholds.
- It is **batch/checkpoint-based**, not a continuous, multi-tenant hosted GRC or certification platform.
- It cannot establish the truth, completeness, lawful acquisition, or authenticity of the source records.
- A passing report verifier does **not** mean compliance with SOC 2, ISO 27001, the EU AI Act, or any regulation.

[Detailed claim boundaries](CLAIM_BOUNDARIES.md).

## Qualification and release

Source checks run on **Ubuntu and Windows / Python 3.11 and 3.12**, including regression tests, synthetic demo and independent verification. The **Windows x64 build** additionally compiles and executes the frozen EXE from a separate directory and tests tamper rejection. See the [release status and exact CI receipts](docs/RELEASE_STATUS.md).

Production-wide software signing, a built-in paid-license entitlement mechanism, and enterprise deployment assurance are **not represented as complete**.

## Licensing and contact

© 2026 **Razorglint Labs / TCOG Collective LLC**. **Proprietary; no open-source license granted.** This public source snapshot may be evaluated only within the rights described in [NOTICE.md](NOTICE.md) and applicable written agreements. Public visibility is not permission to redistribute, sublicense, offer it as SaaS, or transfer the IP.

**We retain core CDD IP** and offer scoped subscriptions, paid evaluations and separately negotiated OEM/embedded licensing. See [license tiers](LICENSE_TIERS.md), [Terms](TERMS_OF_SERVICE.md), [Privacy](PRIVACY_POLICY.md), and [Refund policy](REFUND_AND_CANCELLATION_POLICY.md). OEM/enterprise integrations, support and redistribution rights require a separate agreement.

**Included human assistance is capped for new subscriptions:** Starter **2 requests / 1 interpretation / 20 minutes**, Team **4 / 1 / 45 minutes**, Consultant **6 / 2 / 90 minutes**, all per **paid billing month**. Interpretations count within both the request and time caps. All support is asynchronous, best-effort and not an SLA. See [Support Scope](docs/SUPPORT_SCOPE.md); this must be disclosed in the checkout agreement and does not retroactively reduce existing customers' rights.

**Commercial and security contact:** [razorglint.ops@protonmail.com](mailto:razorglint.ops@protonmail.com).

For vulnerability disclosures, see [SECURITY.md](SECURITY.md).
