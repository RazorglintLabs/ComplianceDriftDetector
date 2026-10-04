# Demo Proof Notes — ComplianceDriftDetector v0.1.0-demo

> **Historical release receipt.** This file records the original `v0.1.0-demo` state from 2026-06-01. It is not the current Sale 01 qualification receipt and should not be used as the current test count.

---

## Release Record

| Field | Value |
|-------|-------|
| Tag | `v0.1.0-demo` |
| Release URL | https://github.com/RazorglintLabs/ComplianceDriftDetector/releases/tag/v0.1.0-demo |
| Commit | `78d7f0a` |
| Date | 2026-06-01 |
| Tests | 27/27 PASS |
| Test time | 0.07s |
| Python | 3.12.10 |
| Dependencies | Zero external Python packages (stdlib-only core) |

---

## Historical Test Results

```text
tests/test_drift_detector.py::TestSha256::test_deterministic PASSED
tests/test_drift_detector.py::TestSha256::test_different_inputs PASSED
tests/test_drift_detector.py::TestSha256::test_lowercase_hex PASSED
tests/test_drift_detector.py::TestHashing::test_hash_policy_deterministic PASSED
tests/test_drift_detector.py::TestHashing::test_hash_behavior_deterministic PASSED
tests/test_drift_detector.py::TestHashing::test_hash_policy_changes_on_different_claims PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_perfect_alignment PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_zero_alignment PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_partial_alignment PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_no_evidence_scores_zero PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_ignores_unrelated_evidence PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_trend_degrading PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_trend_improving PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_trend_stable PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_trend_insufficient_data PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_classify_aligned PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_classify_drifting PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_classify_violated PASSED
tests/test_drift_detector.py::TestAlignmentEngine::test_classify_no_evidence PASSED
tests/test_drift_detector.py::TestComplianceDriftDetector::test_empty_policies PASSED
tests/test_drift_detector.py::TestComplianceDriftDetector::test_fully_aligned PASSED
tests/test_drift_detector.py::TestComplianceDriftDetector::test_violation_detected PASSED
tests/test_drift_detector.py::TestComplianceDriftDetector::test_undeclared_behaviors PASSED
tests/test_drift_detector.py::TestComplianceDriftDetector::test_report_hash_is_sealed PASSED
tests/test_drift_detector.py::TestComplianceDriftDetector::test_report_hash_deterministic PASSED
tests/test_drift_detector.py::TestComplianceDriftDetector::test_multi_day_drift_detection PASSED
tests/test_drift_detector.py::TestComplianceDriftDetector::test_export_evidence PASSED

27 passed in 0.07s
```

---

## Demo Outputs

Running `python software/run_demo.py` writes to the repository-root `output/` directory:

| File | Purpose |
|------|---------|
| `output/drift_report.json` | Machine-readable drift report |
| `output/drift_report.md` | Human-readable markdown report |
| `output/drift_report.html` | Browser-readable report |
| `output/drift_evidence.json` | Full evidence export with per-item hashes |
| `output/input_data.json` | Synthetic demo input summary for reproducibility |

### Demo Scenario

- **5 policy claims** over **30 simulated days**
- **314 synthetic evidence points** generated
- All 4 claim states / undeclared behavior concepts demonstrated:

| Policy | Outcome | State |
|--------|---------|-------|
| POL-001: Deployments require approval | Degrades from 100% to ~70% | DRIFTING |
| POL-002: No persistent admin access | Violated from day 15 | VIOLATED |
| POL-003: PII logging >= 99% | Stays above 99.1% | ALIGNED |
| POL-004: Incident response <= 4 hours | Creeps from 1.5h to 4.5h | VIOLATED |
| POL-005: AI output logging | 100% throughout | ALIGNED |
| (undeclared behavior finding) | Automated rollback reference has no matching policy | UNDECLARED finding |

---

## What The Historical Demo Demonstrates

- The engine ingests structured policy claims and structured behavior evidence
- It groups evidence into daily checkpoints and measures alignment
- It classifies claim state using visible thresholds
- It detects first-to-last trend direction (improving / stable / degrading)
- It surfaces specially marked undeclared behavior references
- It emits report/input hashes and an evidence export with per-item hashes
- The verifier can check supported JSON artifact consistency
- For the same ordered structured inputs and thresholds, semantic classification and input hashes are deterministic
- The core engine uses zero external Python packages

## What The Historical Demo Does NOT Establish

- Production scalability (demo uses in-memory processing)
- Real-world policy coverage (demo uses synthetic data)
- Truth, completeness, or provenance of supplied source evidence
- Automatic policy parsing or compliance inference from raw logs
- Integration with live monitoring systems
- Multi-tenant operation
- Authentication or access control
- Long-term storage or database persistence
- Regulatory compliance, certification, or audit acceptance of any kind
