"""Regression tests for the standalone verifier."""

import json

from software.compliance_drift_detector import ComplianceDriftDetector
from software.report_renderer import render_json_report
from software.verify import verify_drift_evidence, verify_drift_report


def _detector_with_evidence(count: int = 1) -> ComplianceDriftDetector:
    det = ComplianceDriftDetector()
    det.load_policies([
        {
            "claim_id": "POL-001",
            "description": "All deploys require approval",
            "testable_assertion": "deploy.approved == true",
        }
    ])
    det.load_behavior([
        {
            "evidence_id": f"EV-{i:03d}",
            "timestamp": f"2026-01-{(i % 28) + 1:02d}T12:00:00Z",
            "claim_ref": "POL-001",
            "observed_value": "approved",
            "compliant": True,
        }
        for i in range(count)
    ])
    return det


def test_valid_report_verifies_report_seal():
    det = _detector_with_evidence(3)
    report = det.detect_drift()
    data = json.loads(render_json_report(report))

    valid, message = verify_drift_report(data)

    assert valid is True
    assert "report seal PASS" in message


def test_tampered_report_hash_fails():
    det = _detector_with_evidence(3)
    report = det.detect_drift()
    data = json.loads(render_json_report(report))
    data["report_hash"] = "0" * 64

    valid, message = verify_drift_report(data)

    assert valid is False
    assert "Report hash mismatch" in message


def test_valid_large_evidence_export_verifies_every_item():
    det = _detector_with_evidence(150)
    data = det.export_evidence()

    valid, message = verify_drift_evidence(data)

    assert valid is True
    assert "150 evidence items" in message
    assert "all item + aggregate hashes PASS" in message


def test_tamper_after_first_100_evidence_items_fails():
    det = _detector_with_evidence(150)
    data = det.export_evidence()
    data["behavior_evidence"][149]["evidence_hash"] = "0" * 64

    valid, message = verify_drift_evidence(data)

    assert valid is False
    assert "EV-149" in message


def test_tampered_aggregate_behavior_hash_fails():
    det = _detector_with_evidence(5)
    data = det.export_evidence()
    data["verification"]["behavior_hash"] = "0" * 64

    valid, message = verify_drift_evidence(data)

    assert valid is False
    assert "Aggregate behavior hash mismatch" in message
