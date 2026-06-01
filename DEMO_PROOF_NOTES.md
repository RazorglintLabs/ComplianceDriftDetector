# Demo Proof Notes — ComplianceDriftDetector v0.1.0-demo

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
| Dependencies | Zero (stdlib-only) |

---

## Test Results

```
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

Running `python software/run_demo.py` produces:

| File | Purpose |
|------|---------|
| `software/output/drift_report.json` | Machine-readable drift report (sealed) |
| `software/output/drift_report.md` | Human-readable markdown report |
| `software/output/drift_evidence.json` | Full evidence export with per-item hashes |
| `software/output/input_data.json` | Input data for reproducibility |

### Demo Scenario

- **5 policy claims** monitored over **30 simulated days**
- **314 evidence points** generated
- All 4 drift states demonstrated:

| Policy | Outcome | State |
|--------|---------|-------|
| POL-001: Deployments require approval | Degrades from 100% to ~70% | DRIFTING |
| POL-002: No persistent admin access | Violated from day 15 | VIOLATED |
| POL-003: PII logging >= 99% | Stays above 99.1% | ALIGNED |
| POL-004: Incident response <= 4 hours | Creeps from 1.5h to 4.5h | VIOLATED |
| POL-005: AI output logging | 100% throughout | ALIGNED |
| (undeclared) | Automated rollbacks detected | UNDECLARED |

---

## What The Demo Proves

- The engine ingests policy claims and behavior evidence
- It groups evidence into daily checkpoints and measures alignment
- It classifies drift state using visible, configurable thresholds
- It detects trend direction (improving / stable / degrading)
- It identifies undeclared system behaviors
- It seals reports with SHA-256 for tamper evidence
- The standalone verifier (`verify.py`) confirms artifact integrity
- Same inputs produce same outputs (deterministic)
- Zero external dependencies (stdlib-only)

## What The Demo Does NOT Prove

- Production scalability (demo uses in-memory processing)
- Real-world policy coverage (demo uses synthetic data)
- Integration with live monitoring systems
- Multi-tenant operation
- Authentication or access control
- Long-term storage or database persistence
- Regulatory compliance of any kind
