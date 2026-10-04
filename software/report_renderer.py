"""
Compliance Drift Detector — Report Renderer

Produces human-readable drift reports.
"""

from __future__ import annotations

import json
from compliance_drift_detector import DriftReport, DriftState


def render_markdown_report(report: DriftReport) -> str:
    """Render human-readable markdown drift report."""
    lines = [
        "# Compliance Drift Report",
        "",
        f"**Generated:** {report.generated_at}",
        f"**Policy Hash:** `{report.policy_hash[:16]}...`",
        f"**Behavior Hash:** `{report.behavior_hash[:16]}...`",
        f"**Report Hash:** `{report.report_hash[:16]}...`",
        f"**Claims Analyzed:** {report.total_claims}",
        f"**Evidence Points:** {report.total_evidence}",
        "",
        "---",
        "",
        "## Overall Verdict",
        "",
        f"**{report.summary.get('verdict', 'UNKNOWN')}**",
        "",
        f"- Policy alignment: **{report.summary.get('aligned_percentage', 0)}%** of claims fully aligned",
        f"- Total claims: **{report.total_claims}**",
        f"- Undeclared behaviors: **{report.summary.get('undeclared_behavior_count', 0)}**",
        "",
    ]

    thresholds = report.summary.get("thresholds", {})
    if thresholds:
        lines.append("### Thresholds (visible — no hidden scoring)")
        lines.append("")
        lines.append(f"- Alignment threshold: **{thresholds.get('alignment', 0.95):.0%}** (at or above = ALIGNED)")
        lines.append(f"- Violation threshold: **{thresholds.get('violation', 0.70):.0%}** (below = VIOLATED)")
        lines.append(f"- Drift sensitivity: **{thresholds.get('drift_sensitivity', 0.05):.0%}** (minimum first-to-last trend delta)")
        lines.append("")

    state_counts = report.summary.get("state_counts", {})
    if state_counts:
        lines.append("### State Distribution")
        lines.append("")
        lines.append("| State | Count | Meaning |")
        lines.append("|-------|-------|---------|")
        meanings = {
            "ALIGNED": "Latest supplied evidence meets the alignment threshold",
            "DRIFTING": "Latest alignment is below the alignment threshold but above the violation threshold",
            "VIOLATED": "Latest alignment is below the violation threshold",
            "UNDECLARED": "No mapped evidence was supplied for this claim",
        }
        for state, count in sorted(state_counts.items()):
            lines.append(f"| {state} | {count} | {meanings.get(state, '')} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Policy Claim Analysis")
    lines.append("")

    for i, analysis in enumerate(report.analyses, 1):
        state_icon = {
            DriftState.ALIGNED: "[ALIGNED]",
            DriftState.DRIFTING: "[DRIFTING]",
            DriftState.VIOLATED: "[VIOLATED]",
            DriftState.UNDECLARED: "[UNDECLARED]",
        }.get(analysis.state, "[?]")

        lines.append(f"### Claim {i}: `{analysis.claim_id}` — {state_icon}")
        lines.append("")
        lines.append(f"- **Description:** {analysis.claim_description}")
        lines.append(f"- **State:** {analysis.state.value}")
        lines.append(f"- **Current Alignment:** {analysis.current_alignment:.1%}")
        lines.append(f"- **Trend:** {analysis.trend}")
        lines.append(f"- **Reason:** {analysis.reason}")

        if analysis.first_drift_time:
            lines.append(f"- **Earliest supplied checkpoint below alignment threshold:** {analysis.first_drift_time}")
        if analysis.violation_count > 0:
            lines.append(f"- **Violation checkpoints:** {analysis.violation_count}")

        if analysis.checkpoints:
            lines.append(f"- **Checkpoints:** {len(analysis.checkpoints)} measurements")
            lines.append("")
            lines.append("  | Date | Alignment | Evidence |")
            lines.append("  |------|-----------|----------|")
            for cp in analysis.checkpoints[-5:]:
                lines.append(f"  | {cp.checkpoint_time} | {cp.alignment_score:.1%} | {cp.evidence_count} items |")
        lines.append("")

    if report.undeclared_behaviors:
        lines.append("---")
        lines.append("")
        lines.append("## Undeclared Behaviors")
        lines.append("")
        lines.append("Supplied behavior references marked `UNDECLARED-` with no corresponding policy claim:")
        lines.append("")
        lines.append("| Pattern | Occurrences | First Seen | Last Seen |")
        lines.append("|---------|-------------|------------|-----------|")
        for ub in report.undeclared_behaviors:
            lines.append(f"| {ub.behavior_pattern} | {ub.occurrence_count} | {ub.first_seen[:10]} | {ub.last_seen[:10]} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Verification")
    lines.append("")
    lines.append("Supported JSON artifacts can be checked with the included verifier:")
    lines.append("")
    lines.append("```bash")
    lines.append("python software/verify.py output/drift_report.json")
    lines.append("python software/verify.py output/drift_evidence.json")
    lines.append("```")
    lines.append("")
    lines.append("- `drift_report.json`: checks structure, state-count/alignment consistency, and the run-specific report seal.")
    lines.append("- `drift_evidence.json`: checks every exported item hash plus aggregate policy/behavior hashes.")
    lines.append("- `policy_hash` and `behavior_hash` are deterministic for the same ordered structured inputs.")
    lines.append("- `report_hash` is run-specific because `generated_at` is part of its sealed payload; a later re-run is expected to have a different report hash.")
    lines.append("")
    lines.append("Verification establishes artifact consistency and tamper evidence. It does not validate the truth, completeness, or provenance of the supplied source data.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Compliance Drift Detector — Razorglint Labs*")
    lines.append("")

    return "\n".join(lines)


def render_json_report(report: DriftReport) -> str:
    """Render machine-readable JSON report."""
    output = {
        "generated_at": report.generated_at,
        "policy_hash": report.policy_hash,
        "behavior_hash": report.behavior_hash,
        "report_hash": report.report_hash,
        "total_claims": report.total_claims,
        "total_evidence": report.total_evidence,
        "summary": report.summary,
        "analyses": [
            {
                "claim_id": a.claim_id,
                "claim_description": a.claim_description,
                "state": a.state.value,
                "reason": a.reason,
                "current_alignment": a.current_alignment,
                "trend": a.trend,
                "first_drift_time": a.first_drift_time,
                "violation_count": a.violation_count,
                "checkpoint_count": len(a.checkpoints),
                "checkpoints": [
                    {
                        "time": cp.checkpoint_time,
                        "alignment": cp.alignment_score,
                        "evidence_count": cp.evidence_count,
                        "compliant_count": cp.compliant_count,
                        "evidence_hash": cp.evidence_hash,
                    }
                    for cp in a.checkpoints
                ],
            }
            for a in report.analyses
        ],
        "undeclared_behaviors": [
            {
                "pattern": ub.behavior_pattern,
                "occurrences": ub.occurrence_count,
                "first_seen": ub.first_seen,
                "last_seen": ub.last_seen,
            }
            for ub in report.undeclared_behaviors
        ],
    }
    return json.dumps(output, indent=2)
