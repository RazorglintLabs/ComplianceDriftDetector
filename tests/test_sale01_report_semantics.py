"""Regression tests for Sale 01 exported report presentation semantics."""

from software.compliance_drift_detector import ComplianceDriftDetector
from software.render_html_report import render_html_report
from software.report_renderer import render_markdown_report


def recovered_report():
    det = ComplianceDriftDetector()
    det.load_policies([
        {
            "claim_id": "POL-RECOVER-001",
            "description": "Recovered control",
            "testable_assertion": "x == true",
        }
    ])
    det.load_behavior([
        {
            "evidence_id": "E1",
            "timestamp": "2026-01-01T10:00:00Z",
            "claim_ref": "POL-RECOVER-001",
            "observed_value": "ok",
            "compliant": True,
        },
        {
            "evidence_id": "E2",
            "timestamp": "2026-01-02T10:00:00Z",
            "claim_ref": "POL-RECOVER-001",
            "observed_value": "bad",
            "compliant": False,
        },
        {
            "evidence_id": "E3",
            "timestamp": "2026-01-03T10:00:00Z",
            "claim_ref": "POL-RECOVER-001",
            "observed_value": "ok",
            "compliant": True,
        },
    ])
    return det.detect_drift()


def test_html_report_labels_recovered_history_explicitly():
    html = render_html_report(recovered_report())
    assert "Current State" in html
    assert "Current Alignment" in html
    assert "History Status" in html
    assert "RECOVERED" in html
    assert "First Threshold Breach" in html
    assert "2026-01-02" in html
    assert "Violated Claims" in html


def test_markdown_report_separates_history_from_raw_trend():
    markdown = render_markdown_report(recovered_report())
    assert "**Current State:** ALIGNED" in markdown
    assert "**Current Alignment:** 100.0%" in markdown
    assert "**History Status:** RECOVERED" in markdown
    assert "**First-to-last Trend (raw engine direction):** stable" in markdown
    assert "**First Threshold Breach:** 2026-01-02" in markdown


def test_json_schema_remains_unchanged_by_presentation_fix():
    report = recovered_report()
    assert report.analyses[0].trend == "stable"
    assert report.analyses[0].first_drift_time == "2026-01-02"
