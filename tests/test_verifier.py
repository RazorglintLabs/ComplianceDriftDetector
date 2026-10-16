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



def test_v2_seal_rejects_changes_to_displayed_reason_and_checkpoint():
    det = _detector_with_evidence(3)
    data = json.loads(render_json_report(det.detect_drift()))
    assert data["report_seal_version"] == 2
    for mutate in [
        lambda r: r["analyses"][0].__setitem__("reason", "This was never checked"),
        lambda r: r["analyses"][0]["checkpoints"][0].__setitem__("evidence_hash", "fake-checkpoint"),
        lambda r: r["analyses"][0].__setitem__("claim_description", "Changed policy wording"),
        lambda r: r["analyses"][0].__setitem__("first_drift_time", "2026-10-16"),
        lambda r: r["analyses"][0].__setitem__("trend", "improving"),
    ]:
        copy = json.loads(json.dumps(data))
        mutate(copy)
        passed, message = verify_drift_report(copy)
        assert not passed, message


def test_v2_seal_rejects_undeclared_finding_mutation():
    det = _detector_with_evidence(1)
    det.load_behavior([{
        "evidence_id": "UNDECL-1",
        "timestamp": "2026-02-01T00:00:00Z",
        "claim_ref": "UNDECLARED-ACCESS",
        "observed_value": "unknown",
        "compliant": False,
    }])
    data = json.loads(render_json_report(det.detect_drift()))
    assert data["undeclared_behaviors"]
    data["undeclared_behaviors"][0]["pattern"] = "REPLACED"
    passed, message = verify_drift_report(data)
    assert not passed, message


def test_v2_missing_version_does_not_silently_retain_full_hash():
    data = json.loads(render_json_report(_detector_with_evidence(1).detect_drift()))
    del data["report_seal_version"]
    valid, _ = verify_drift_report(data)
    assert not valid


def test_legacy_v1_report_is_labeled_limited():
    from software.verify import sha256
    det = _detector_with_evidence(2)
    data = json.loads(render_json_report(det.detect_drift()))
    del data["report_seal_version"]
    legacy = {
        k: data[k] for k in ("generated_at", "policy_hash",
                             "behavior_hash", "total_claims",
                             "total_evidence", "summary")
    }
    data["report_hash"] = sha256(json.dumps(legacy, sort_keys=True))
    passed, message = verify_drift_report(data)
    assert passed
    assert "LIMITED summary-only" in message
    assert "NOT sealed" in message


def test_no_policies_gets_consistent_v2_seal():
    empty_report = ComplianceDriftDetector().detect_drift()
    data = json.loads(render_json_report(empty_report))
    passed, message = verify_drift_report(data)
    assert passed, message
    assert data["report_seal_version"] == 2
