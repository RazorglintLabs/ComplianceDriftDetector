"""
ComplianceDriftDetector — Test Suite

Tests all core engine paths: alignment scoring, trend detection,
drift classification, undeclared behavior detection, report sealing,
and evidence export.
"""

import json
import pytest
from software.compliance_drift_detector import (
    AlignmentEngine,
    BehaviorEvidence,
    CheckpointMeasurement,
    ComplianceDriftDetector,
    DriftReport,
    DriftState,
    PolicyClaim,
    PolicyClaimType,
    UndeclaredBehavior,
    hash_behavior,
    hash_policy,
    sha256,
)


# --- Fixtures ---

def make_claim(claim_id="POL-001", description="Test claim", assertion="X must be Y"):
    return PolicyClaim(
        claim_id=claim_id,
        policy_source="test",
        claim_type=PolicyClaimType.REQUIREMENT.value,
        description=description,
        testable_assertion=assertion,
    )


def make_evidence(evidence_id, claim_ref, compliant, timestamp="2026-01-01T00:00:00Z"):
    return BehaviorEvidence(
        evidence_id=evidence_id,
        timestamp=timestamp,
        source="test",
        claim_ref=claim_ref,
        observed_value="true" if compliant else "false",
        compliant=compliant,
    )


# --- sha256 ---

class TestSha256:
    def test_deterministic(self):
        assert sha256("hello") == sha256("hello")

    def test_different_inputs(self):
        assert sha256("a") != sha256("b")

    def test_lowercase_hex(self):
        result = sha256("test")
        assert result == result.lower()
        assert len(result) == 64


# --- hash_policy / hash_behavior ---

class TestHashing:
    def test_hash_policy_deterministic(self):
        claims = [make_claim("A"), make_claim("B")]
        assert hash_policy(claims) == hash_policy(claims)

    def test_hash_behavior_deterministic(self):
        ev = [make_evidence("E1", "A", True), make_evidence("E2", "A", False)]
        assert hash_behavior(ev) == hash_behavior(ev)

    def test_hash_policy_changes_on_different_claims(self):
        a = hash_policy([make_claim("A")])
        b = hash_policy([make_claim("B")])
        assert a != b


# --- AlignmentEngine ---

class TestAlignmentEngine:
    def setup_method(self):
        self.engine = AlignmentEngine(
            alignment_threshold=0.95,
            violation_threshold=0.70,
            drift_sensitivity=0.05,
        )

    def test_perfect_alignment(self):
        claim = make_claim()
        evidence = [make_evidence(f"E{i}", "POL-001", True) for i in range(10)]
        m = self.engine.measure_checkpoint(claim, evidence, "2026-01-01")
        assert m.alignment_score == 1.0
        assert m.compliant_count == 10

    def test_zero_alignment(self):
        claim = make_claim()
        evidence = [make_evidence(f"E{i}", "POL-001", False) for i in range(5)]
        m = self.engine.measure_checkpoint(claim, evidence, "2026-01-01")
        assert m.alignment_score == 0.0

    def test_partial_alignment(self):
        claim = make_claim()
        evidence = [
            make_evidence("E1", "POL-001", True),
            make_evidence("E2", "POL-001", True),
            make_evidence("E3", "POL-001", False),
            make_evidence("E4", "POL-001", True),
        ]
        m = self.engine.measure_checkpoint(claim, evidence, "2026-01-01")
        assert m.alignment_score == 0.75

    def test_no_evidence_scores_zero(self):
        claim = make_claim()
        m = self.engine.measure_checkpoint(claim, [], "2026-01-01")
        assert m.alignment_score == 0.0
        assert m.evidence_count == 0

    def test_ignores_unrelated_evidence(self):
        claim = make_claim("POL-001")
        evidence = [make_evidence("E1", "POL-999", True)]
        m = self.engine.measure_checkpoint(claim, evidence, "2026-01-01")
        assert m.evidence_count == 0

    # --- Trend Detection ---

    def test_trend_degrading(self):
        cps = [
            CheckpointMeasurement("2026-01-01", "A", 5, 5, 1.0, "h1"),
            CheckpointMeasurement("2026-01-02", "A", 5, 3, 0.6, "h2"),
        ]
        assert self.engine.detect_trend(cps) == "degrading"

    def test_trend_improving(self):
        cps = [
            CheckpointMeasurement("2026-01-01", "A", 5, 3, 0.6, "h1"),
            CheckpointMeasurement("2026-01-02", "A", 5, 5, 1.0, "h2"),
        ]
        assert self.engine.detect_trend(cps) == "improving"

    def test_trend_stable(self):
        cps = [
            CheckpointMeasurement("2026-01-01", "A", 5, 5, 0.95, "h1"),
            CheckpointMeasurement("2026-01-02", "A", 5, 5, 0.96, "h2"),
        ]
        assert self.engine.detect_trend(cps) == "stable"

    def test_trend_insufficient_data(self):
        cps = [CheckpointMeasurement("2026-01-01", "A", 5, 5, 1.0, "h1")]
        assert self.engine.detect_trend(cps) == "insufficient_data"

    # --- Classification ---

    def test_classify_aligned(self):
        claim = make_claim()
        cps = [CheckpointMeasurement("2026-01-01", "POL-001", 10, 10, 1.0, "h")]
        result = self.engine.classify_drift(claim, cps)
        assert result.state == DriftState.ALIGNED

    def test_classify_drifting(self):
        claim = make_claim()
        cps = [CheckpointMeasurement("2026-01-01", "POL-001", 10, 8, 0.8, "h")]
        result = self.engine.classify_drift(claim, cps)
        assert result.state == DriftState.DRIFTING

    def test_classify_violated(self):
        claim = make_claim()
        cps = [CheckpointMeasurement("2026-01-01", "POL-001", 10, 5, 0.5, "h")]
        result = self.engine.classify_drift(claim, cps)
        assert result.state == DriftState.VIOLATED

    def test_classify_no_evidence(self):
        claim = make_claim()
        result = self.engine.classify_drift(claim, [])
        assert result.state == DriftState.UNDECLARED


# --- ComplianceDriftDetector (Integration) ---

class TestComplianceDriftDetector:
    def test_empty_policies(self):
        det = ComplianceDriftDetector()
        report = det.detect_drift()
        assert report.total_claims == 0
        assert report.summary["verdict"] == "NO_POLICIES"

    def test_fully_aligned(self):
        det = ComplianceDriftDetector()
        det.load_policies([{
            "claim_id": "POL-001",
            "description": "All deploys require approval",
            "testable_assertion": "deploy.approved == true",
        }])
        det.load_behavior([{
            "evidence_id": f"EV-{i}",
            "timestamp": f"2026-01-01T{i:02d}:00:00Z",
            "claim_ref": "POL-001",
            "observed_value": "approved",
            "compliant": True,
        } for i in range(10)])

        report = det.detect_drift()
        assert report.summary["verdict"] == "FULLY_ALIGNED"
        assert report.analyses[0].state == DriftState.ALIGNED

    def test_violation_detected(self):
        det = ComplianceDriftDetector()
        det.load_policies([{
            "claim_id": "POL-001",
            "description": "No admin access",
            "testable_assertion": "admin.sessions == 0",
        }])
        det.load_behavior([{
            "evidence_id": f"EV-{i}",
            "timestamp": f"2026-01-01T{i:02d}:00:00Z",
            "claim_ref": "POL-001",
            "observed_value": "admin_active",
            "compliant": False,
        } for i in range(10)])

        report = det.detect_drift()
        assert report.summary["verdict"] == "VIOLATION_DETECTED"
        assert report.analyses[0].state == DriftState.VIOLATED

    def test_undeclared_behaviors(self):
        det = ComplianceDriftDetector()
        det.load_policies([{
            "claim_id": "POL-001",
            "description": "Test",
            "testable_assertion": "x == y",
        }])
        det.load_behavior([
            {
                "evidence_id": "EV-1",
                "timestamp": "2026-01-01T00:00:00Z",
                "claim_ref": "POL-001",
                "observed_value": "ok",
                "compliant": True,
            },
            {
                "evidence_id": "EV-2",
                "timestamp": "2026-01-01T01:00:00Z",
                "claim_ref": "UNDECLARED-ROLLBACK",
                "observed_value": "automated rollback detected",
                "compliant": True,
            },
        ])

        report = det.detect_drift()
        assert len(report.undeclared_behaviors) == 1
        assert report.undeclared_behaviors[0].behavior_pattern == "UNDECLARED-ROLLBACK"

    def test_report_hash_is_sealed(self):
        det = ComplianceDriftDetector()
        det.load_policies([{
            "claim_id": "POL-001",
            "description": "Test",
            "testable_assertion": "x",
        }])
        det.load_behavior([{
            "evidence_id": "EV-1",
            "timestamp": "2026-01-01T00:00:00Z",
            "claim_ref": "POL-001",
            "observed_value": "ok",
            "compliant": True,
        }])

        report = det.detect_drift()
        assert report.report_hash != ""
        assert len(report.report_hash) == 64

    def test_report_hash_deterministic(self):
        """Same inputs on same detector produce same hashes (excluding timestamp)."""
        det = ComplianceDriftDetector()
        det.load_policies([{
            "claim_id": "POL-001",
            "description": "Test",
            "testable_assertion": "x",
        }])
        det.load_behavior([{
            "evidence_id": "EV-1",
            "timestamp": "2026-01-01T00:00:00Z",
            "claim_ref": "POL-001",
            "observed_value": "ok",
            "compliant": True,
        }])
        # Policy and behavior hashes are deterministic
        assert det.detect_drift().policy_hash == det.detect_drift().policy_hash
        assert det.detect_drift().behavior_hash == det.detect_drift().behavior_hash

    def test_multi_day_drift_detection(self):
        """Multi-checkpoint scenario detecting degradation over time."""
        det = ComplianceDriftDetector()
        det.load_policies([{
            "claim_id": "POL-001",
            "description": "Deploys require approval",
            "testable_assertion": "deploy.approved == true",
        }])
        # Day 1: 100% compliant, Day 2: 50% compliant
        evidence = [
            {"evidence_id": "E1", "timestamp": "2026-01-01T10:00:00Z", "claim_ref": "POL-001", "observed_value": "ok", "compliant": True},
            {"evidence_id": "E2", "timestamp": "2026-01-01T11:00:00Z", "claim_ref": "POL-001", "observed_value": "ok", "compliant": True},
            {"evidence_id": "E3", "timestamp": "2026-01-02T10:00:00Z", "claim_ref": "POL-001", "observed_value": "no", "compliant": False},
            {"evidence_id": "E4", "timestamp": "2026-01-02T11:00:00Z", "claim_ref": "POL-001", "observed_value": "ok", "compliant": True},
        ]
        det.load_behavior(evidence)

        report = det.detect_drift()
        analysis = report.analyses[0]
        assert analysis.trend == "degrading"
        assert analysis.current_alignment == 0.5
        assert analysis.state == DriftState.VIOLATED

    def test_export_evidence(self):
        det = ComplianceDriftDetector()
        det.load_policies([{
            "claim_id": "POL-001",
            "description": "Test",
            "testable_assertion": "x",
        }])
        det.load_behavior([{
            "evidence_id": "EV-1",
            "timestamp": "2026-01-01T00:00:00Z",
            "claim_ref": "POL-001",
            "observed_value": "ok",
            "compliant": True,
        }])
        export = det.export_evidence()
        assert "behavior_evidence" in export
        assert "verification" in export
        assert len(export["behavior_evidence"]) == 1
