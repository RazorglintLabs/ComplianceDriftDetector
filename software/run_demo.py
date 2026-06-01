"""
Compliance Drift Detector — Demo Runner

Generates realistic sample data demonstrating all drift states.
Run this to see the detector in action with zero setup.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from compliance_drift_detector import ComplianceDriftDetector, PolicyClaimType
from report_renderer import render_markdown_report, render_json_report
from render_html_report import render_html_report


def generate_sample_policies() -> list[dict]:
    """
    Generate realistic policy claims.
    
    5 claims covering common governance scenarios.
    """
    return [
        {
            "claim_id": "POL-001",
            "policy_source": "Deployment Policy v3.2",
            "claim_type": PolicyClaimType.REQUIREMENT.value,
            "description": "All production deployments require explicit approval",
            "testable_assertion": "Every deployment event has a corresponding approval record",
            "metadata": {"owner": "engineering-vp", "last_reviewed": "2026-01-15"},
        },
        {
            "claim_id": "POL-002",
            "policy_source": "Access Control Policy v2.1",
            "claim_type": PolicyClaimType.PROHIBITION.value,
            "description": "No service account shall have persistent admin access",
            "testable_assertion": "Service accounts with admin role have TTL <= 24 hours",
            "metadata": {"owner": "ciso", "last_reviewed": "2026-02-01"},
        },
        {
            "claim_id": "POL-003",
            "policy_source": "Data Handling Policy v4.0",
            "claim_type": PolicyClaimType.THRESHOLD.value,
            "description": "PII access logging must cover >= 99% of access events",
            "testable_assertion": "PII access events with audit log entry / total PII access events >= 0.99",
            "threshold": 0.99,
            "metadata": {"owner": "dpo", "last_reviewed": "2026-03-01"},
        },
        {
            "claim_id": "POL-004",
            "policy_source": "Incident Response Policy v1.8",
            "claim_type": PolicyClaimType.PROCESS.value,
            "description": "All security incidents must have response within 4 hours",
            "testable_assertion": "Time from incident detection to first response <= 4 hours",
            "metadata": {"owner": "security-lead", "last_reviewed": "2026-01-20"},
        },
        {
            "claim_id": "POL-005",
            "policy_source": "AI Governance Policy v1.0",
            "claim_type": PolicyClaimType.CONTROL.value,
            "description": "AI model outputs must be logged before delivery to end users",
            "testable_assertion": "Every model inference has a log entry with timestamp before response delivery",
            "metadata": {"owner": "ai-ethics-board", "last_reviewed": "2026-04-01"},
        },
    ]


def generate_sample_evidence() -> list[dict]:
    """
    Generate realistic behavior evidence over 30 days.
    
    Demonstrates:
    - POL-001: Starts aligned, drifts (approval rate drops)
    - POL-002: Violated (persistent admin found)
    - POL-003: Aligned (>99% coverage maintained)
    - POL-004: Drifting (response times creeping up)
    - POL-005: Aligned throughout
    + Undeclared behavior: automated rollbacks with no policy
    """
    base_date = datetime(2026, 4, 19)
    evidence = []
    ev_counter = 0

    for day in range(30):
        current_date = base_date + timedelta(days=day)
        date_str = current_date.isoformat() + "Z"

        # === POL-001: Deployment approvals — starts at 100%, drifts to 70% ===
        deployments_per_day = 5
        # Approval rate degrades over time
        if day < 10:
            approval_rate = 1.0  # 100% first 10 days
        elif day < 20:
            approval_rate = 0.85  # 85% middle 10 days
        else:
            approval_rate = 0.70  # 70% last 10 days

        for i in range(deployments_per_day):
            ev_counter += 1
            compliant = (i / deployments_per_day) < approval_rate
            evidence.append({
                "evidence_id": f"EV-{ev_counter:05d}",
                "timestamp": date_str,
                "source": "ci-cd-pipeline",
                "claim_ref": "POL-001",
                "observed_value": f"deployment_{day}_{i}_{'approved' if compliant else 'unapproved'}",
                "compliant": compliant,
                "metadata": {"deployment_id": f"DEP-{day:03d}-{i}"},
            })

        # === POL-002: Service account admin — violated from day 15 ===
        ev_counter += 1
        if day < 15:
            evidence.append({
                "evidence_id": f"EV-{ev_counter:05d}",
                "timestamp": date_str,
                "source": "iam-scanner",
                "claim_ref": "POL-002",
                "observed_value": "service_accounts_admin_ttl_12h",
                "compliant": True,
            })
        else:
            evidence.append({
                "evidence_id": f"EV-{ev_counter:05d}",
                "timestamp": date_str,
                "source": "iam-scanner",
                "claim_ref": "POL-002",
                "observed_value": "svc-backup-agent_admin_persistent_no_ttl",
                "compliant": False,
                "metadata": {"account": "svc-backup-agent", "ttl": "NONE"},
            })

        # === POL-003: PII logging — consistently above 99% ===
        ev_counter += 1
        # Slight variation but always compliant
        evidence.append({
            "evidence_id": f"EV-{ev_counter:05d}",
            "timestamp": date_str,
            "source": "audit-log-monitor",
            "claim_ref": "POL-003",
            "observed_value": f"pii_coverage_{99.1 + (day % 5) * 0.1:.1f}%",
            "compliant": True,
            "metadata": {"coverage_pct": 99.1 + (day % 5) * 0.1},
        })

        # === POL-004: Incident response — starts fast, creeps up ===
        if day % 3 == 0:  # Incident every 3 days
            ev_counter += 1
            if day < 12:
                response_hours = 1.5 + (day * 0.1)
                compliant = True
            elif day < 24:
                response_hours = 3.0 + (day - 12) * 0.15
                compliant = response_hours <= 4.0
            else:
                response_hours = 4.5 + (day - 24) * 0.3
                compliant = False

            evidence.append({
                "evidence_id": f"EV-{ev_counter:05d}",
                "timestamp": date_str,
                "source": "incident-tracker",
                "claim_ref": "POL-004",
                "observed_value": f"response_time_{response_hours:.1f}h",
                "compliant": compliant,
                "metadata": {"response_hours": response_hours},
            })

        # === POL-005: AI output logging — consistently compliant ===
        for i in range(3):  # 3 model inferences per day
            ev_counter += 1
            evidence.append({
                "evidence_id": f"EV-{ev_counter:05d}",
                "timestamp": date_str,
                "source": "model-serving-layer",
                "claim_ref": "POL-005",
                "observed_value": f"inference_{day}_{i}_logged_before_delivery",
                "compliant": True,
            })

        # === UNDECLARED: Automated rollbacks (no policy covers this) ===
        if day % 7 == 0 and day > 0:
            ev_counter += 1
            evidence.append({
                "evidence_id": f"EV-{ev_counter:05d}",
                "timestamp": date_str,
                "source": "deployment-automation",
                "claim_ref": "UNDECLARED-auto-rollback",
                "observed_value": f"automatic_rollback_triggered_no_human_approval",
                "compliant": False,  # Can't be compliant — no policy exists
                "metadata": {"trigger": "health_check_failure", "human_notified": False},
            })

    return evidence


def main():
    """Run the demo and produce all artifacts."""
    print("=" * 60)
    print("  COMPLIANCE DRIFT DETECTOR - Demo Run")
    print("=" * 60)
    print()

    # Generate sample data
    print("[1/5] Generating sample policies and behavior evidence...")
    policies = generate_sample_policies()
    evidence = generate_sample_evidence()
    print(f"      -> {len(policies)} policy claims")
    print(f"      -> {len(evidence)} evidence points over 30 days")
    print()

    # Initialize detector
    print("[2/5] Initializing detector (align=95%, violate=70%, sensitivity=5%)...")
    detector = ComplianceDriftDetector(
        alignment_threshold=0.95,
        violation_threshold=0.70,
        drift_sensitivity=0.05,
    )
    print()

    # Load data
    print("[3/5] Loading policies and behavior evidence...")
    detector.load_policies(policies)
    detector.load_behavior(evidence)
    print()

    # Detect drift
    print("[4/5] Analyzing drift...")
    report = detector.detect_drift()
    print(f"      -> {len(report.analyses)} claims analyzed")
    print(f"      -> {len(report.undeclared_behaviors)} undeclared behaviors found")
    print(f"      -> Verdict: {report.summary['verdict']}")
    print()

    # Export evidence
    evidence_export = detector.export_evidence()

    # Write output
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("[5/5] Writing artifacts...")

    # Drift report JSON
    report_json_path = output_dir / "drift_report.json"
    report_json_path.write_text(render_json_report(report), encoding="utf-8")
    print(f"      -> {report_json_path.name}")

    # Drift report markdown
    report_md_path = output_dir / "drift_report.md"
    report_md_path.write_text(render_markdown_report(report), encoding="utf-8")
    print(f"      -> {report_md_path.name}")

    # Drift report HTML
    report_html_path = output_dir / "drift_report.html"
    report_html_path.write_text(render_html_report(report), encoding="utf-8")
    print(f"      -> {report_html_path.name}")

    # Evidence export
    evidence_path = output_dir / "drift_evidence.json"
    evidence_path.write_text(json.dumps(evidence_export, indent=2), encoding="utf-8")
    print(f"      -> {evidence_path.name}")

    # Input data (for reproducibility)
    input_path = output_dir / "input_data.json"
    input_path.write_text(json.dumps({"policies": policies, "evidence_count": len(evidence)}, indent=2), encoding="utf-8")
    print(f"      -> {input_path.name}")

    print()
    print("=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print()
    print(f"  Verdict:           {report.summary['verdict']}")
    print(f"  Aligned:           {report.summary['aligned_percentage']}%")
    print(f"  Report Hash:       {report.report_hash[:32]}...")
    print()
    print("  Claim breakdown:")
    for analysis in report.analyses:
        print(f"    [{analysis.claim_id}] {analysis.state.value:12s} | {analysis.current_alignment:.0%} | {analysis.trend}")
        print(f"                     {analysis.claim_description[:60]}")
    print()
    if report.undeclared_behaviors:
        print("  Undeclared behaviors:")
        for ub in report.undeclared_behaviors:
            print(f"    - {ub.behavior_pattern} ({ub.occurrence_count} occurrences)")
    print()
    print("  All artifacts written to: output/")
    print("  Verify with: python software/verify.py output/drift_report.json")
    print()


if __name__ == "__main__":
    main()
