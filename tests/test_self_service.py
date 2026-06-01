"""
Tests for the self-service CSV scan layer.

Covers: CSV parsing, column validation, template pack smoke tests,
HTML report generation, and run_scan integration.
"""

import csv
import sys
from pathlib import Path

import pytest

from run_scan import load_csv, load_policies, load_evidence, parse_bool, REQUIRED_POLICY_COLUMNS, REQUIRED_EVIDENCE_COLUMNS
from render_html_report import render_html_report
from compliance_drift_detector import ComplianceDriftDetector


# --- parse_bool ---

class TestParseBool:
    def test_true_values(self):
        for v in ("true", "True", "TRUE", "1", "yes", "Yes", "YES"):
            assert parse_bool(v) is True

    def test_false_values(self):
        for v in ("false", "False", "0", "no", "No", "", "anything"):
            assert parse_bool(v) is False

    def test_whitespace(self):
        assert parse_bool("  true  ") is True
        assert parse_bool("  false  ") is False


# --- CSV Loading ---

class TestLoadCsv:
    def _write_csv(self, tmp: Path, header: list[str], rows: list[list[str]]):
        with open(tmp, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)

    def test_valid_csv(self, tmp_path):
        p = tmp_path / "test.csv"
        self._write_csv(p, ["claim_id", "description", "testable_assertion"], [["A", "B", "C"]])
        result = load_csv(p, REQUIRED_POLICY_COLUMNS)
        assert len(result) == 1
        assert result[0]["claim_id"] == "A"

    def test_missing_column_exits(self, tmp_path):
        p = tmp_path / "test.csv"
        self._write_csv(p, ["claim_id", "description"], [["A", "B"]])
        with pytest.raises(SystemExit):
            load_csv(p, REQUIRED_POLICY_COLUMNS)

    def test_file_not_found_exits(self, tmp_path):
        p = tmp_path / "nonexistent.csv"
        with pytest.raises(SystemExit):
            load_csv(p, REQUIRED_POLICY_COLUMNS)

    def test_empty_csv_exits(self, tmp_path):
        p = tmp_path / "empty.csv"
        p.write_text("")
        with pytest.raises(SystemExit):
            load_csv(p, REQUIRED_POLICY_COLUMNS)

    def test_extra_columns_ok(self, tmp_path):
        p = tmp_path / "test.csv"
        self._write_csv(p, ["claim_id", "description", "testable_assertion", "extra"], [["A", "B", "C", "D"]])
        result = load_csv(p, REQUIRED_POLICY_COLUMNS)
        assert len(result) == 1


# --- Policy Loading ---

class TestLoadPolicies:
    def _write_policy_csv(self, path: Path, rows: list[dict]):
        fields = ["claim_id", "description", "testable_assertion", "claim_type", "threshold"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def test_basic_load(self, tmp_path):
        p = tmp_path / "pol.csv"
        self._write_policy_csv(p, [{"claim_id": "P1", "description": "Test", "testable_assertion": "x==y", "claim_type": "", "threshold": ""}])
        result = load_policies(p)
        assert result[0]["claim_id"] == "P1"
        assert result[0]["claim_type"] == "REQUIREMENT"

    def test_threshold_parsing(self, tmp_path):
        p = tmp_path / "pol.csv"
        self._write_policy_csv(p, [{"claim_id": "P1", "description": "T", "testable_assertion": "x", "claim_type": "THRESHOLD", "threshold": "0.95"}])
        result = load_policies(p)
        assert result[0]["threshold"] == 0.95


# --- Evidence Loading ---

class TestLoadEvidence:
    def _write_evidence_csv(self, path: Path, rows: list[dict]):
        fields = ["evidence_id", "timestamp", "claim_ref", "observed_value", "compliant", "source"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def test_basic_load(self, tmp_path):
        p = tmp_path / "ev.csv"
        self._write_evidence_csv(p, [{"evidence_id": "E1", "timestamp": "2026-01-01T00:00:00Z", "claim_ref": "P1", "observed_value": "ok", "compliant": "true", "source": "test"}])
        result = load_evidence(p)
        assert result[0]["compliant"] is True

    def test_false_compliant(self, tmp_path):
        p = tmp_path / "ev.csv"
        self._write_evidence_csv(p, [{"evidence_id": "E1", "timestamp": "2026-01-01T00:00:00Z", "claim_ref": "P1", "observed_value": "bad", "compliant": "false", "source": "test"}])
        result = load_evidence(p)
        assert result[0]["compliant"] is False


# --- Template Pack Smoke Tests ---

TEMPLATE_PACKS = [
    "deployment_approval",
    "privileged_access",
    "ai_output_logging",
]

class TestTemplatePacks:
    @pytest.mark.parametrize("pack", TEMPLATE_PACKS)
    def test_pack_loads_and_runs(self, pack):
        root = Path(__file__).parent.parent
        pack_dir = root / "examples" / "template_packs" / pack
        policy_path = pack_dir / "policy_claims.csv"
        evidence_path = pack_dir / "behavior_evidence.csv"

        assert policy_path.exists(), f"Missing {policy_path}"
        assert evidence_path.exists(), f"Missing {evidence_path}"

        policies = load_policies(policy_path)
        evidence = load_evidence(evidence_path)

        assert len(policies) > 0
        assert len(evidence) > 0

        # Run through detector
        det = ComplianceDriftDetector()
        det.load_policies(policies)
        det.load_behavior(evidence)
        report = det.detect_drift()

        assert report.total_claims == len(policies)
        assert report.total_evidence == len(evidence)
        assert report.report_hash != ""
        assert report.summary["verdict"] in ("FULLY_ALIGNED", "DRIFT_DETECTED", "VIOLATION_DETECTED", "UNDECLARED_BEHAVIORS")


# --- HTML Report ---

class TestHtmlReport:
    def test_produces_valid_html(self):
        det = ComplianceDriftDetector()
        det.load_policies([{"claim_id": "P1", "description": "Test", "testable_assertion": "x"}])
        det.load_behavior([{"evidence_id": "E1", "timestamp": "2026-01-01T00:00:00Z", "claim_ref": "P1", "observed_value": "ok", "compliant": True}])
        report = det.detect_drift()

        html = render_html_report(report)
        assert "<!DOCTYPE html>" in html
        assert "Compliance Drift Report" in html
        assert "ALIGNED" in html
        assert report.report_hash in html

    def test_html_contains_boundary_language(self):
        det = ComplianceDriftDetector()
        det.load_policies([{"claim_id": "P1", "description": "Test", "testable_assertion": "x"}])
        det.load_behavior([{"evidence_id": "E1", "timestamp": "2026-01-01T00:00:00Z", "claim_ref": "P1", "observed_value": "ok", "compliant": True}])
        report = det.detect_drift()

        html = render_html_report(report)
        assert "not</strong> a compliance certification" in html
        assert "audit preparation" in html
        assert "No data left your machine" in html

    def test_html_escapes_dangerous_input(self):
        det = ComplianceDriftDetector()
        det.load_policies([{"claim_id": "P1", "description": "<script>alert('xss')</script>", "testable_assertion": "x"}])
        det.load_behavior([{"evidence_id": "E1", "timestamp": "2026-01-01T00:00:00Z", "claim_ref": "P1", "observed_value": "ok", "compliant": True}])
        report = det.detect_drift()

        html = render_html_report(report)
        assert "<script>" not in html
        assert "&lt;script&gt;" in html
