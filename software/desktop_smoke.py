"""Exercise packaged detector + renderer + verifier without a GUI or pytest.

Invocation from the actual compiled Windows program:
    ComplianceDriftDetector.exe --smoke-test --smoke-report C:\\path\\smoke.json

This verifies packed CSV resources and report semantics, not a GUI click-through.
"""
from __future__ import annotations

import json
from pathlib import Path

from compliance_drift_detector import ComplianceDriftDetector
from desktop_paths import resource_root, reports_dir
from render_html_report import render_html_report
from report_renderer import render_json_report, render_markdown_report
from run_scan import load_evidence, load_policies
from ui_semantics import history_status, result_counts
from verify import verify_drift_evidence, verify_drift_report


def run_smoke() -> dict:
    sample = resource_root() / "examples" / "template_packs" / "deployment_approval"
    claims = load_policies(sample / "policy_claims.csv")
    observations = load_evidence(sample / "behavior_evidence.csv")
    detector = ComplianceDriftDetector()
    detector.load_policies(claims)
    detector.load_behavior(observations)
    report = detector.detect_drift()
    counts, unmatched = result_counts(report)
    assert counts == {"ALIGNED": 1, "DRIFTING": 0, "VIOLATED": 2, "UNDECLARED": 0}, counts
    assert unmatched == 1, unmatched
    ci = next(a for a in report.analyses if a.claim_id == "POL-DEPLOY-002")
    assert ci.state.value == "ALIGNED"
    assert history_status(ci, alignment_threshold=0.95) == "RECOVERED"
    assert ci.first_drift_time == "2026-01-02"
    rendered = json.loads(render_json_report(report))
    ok_report, reason_report = verify_drift_report(rendered)
    exported = detector.export_evidence()
    ok_evidence, reason_evidence = verify_drift_evidence(exported)
    assert ok_report, reason_report
    assert ok_evidence, reason_evidence
    assert "RECOVERED" in render_html_report(report)
    assert "RECOVERED" in render_markdown_report(report)
    # The entire v2 report (including detail) must be sealed, not just the summary.
    rendered["analyses"][0]["reason"] = "REWRITTEN-DETAILED-REASON"
    ok_changed_detail, _ = verify_drift_report(rendered)
    assert not ok_changed_detail, "Verifier accepted changed report detail"
    # Deliberate mutation: should be detected. Do not use real customer data.
    exported["behavior_evidence"][0]["observed_value"] = "TAMPERED-SMOKE"
    ok_tampered, _ = verify_drift_evidence(exported)
    assert not ok_tampered, "Verifier accepted changed evidence"
    return {
        "result": "PASS", "mode": "real-frozen-executable-smoke",
        "sample_claims": report.total_claims,
        "claim_states": counts, "undeclared_behavior_findings": unmatched,
        "ci_history": "RECOVERED", "report_verifier": "PASS",
        "evidence_verifier": "PASS", "tamper_negative_test": "PASS",
        "bundled_sample_available": True,
        "writable_report_directory": str(reports_dir()),
        "limitations": "No GUI clicks or native-install signing covered by this smoke test",
    }


def main(output_path: str) -> int:
    try:
        result = run_smoke()
    except Exception as exc:
        result = {"result": "FAIL", "error": str(exc), "mode": "real-frozen-executable-smoke"}
    try:
        path = Path(output_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except Exception:
        return 2
    return 0 if result["result"] == "PASS" else 1
