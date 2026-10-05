"""
render_html_report.py — Static HTML drift report renderer

Produces a single self-contained HTML file with:
- Executive summary
- Drift state table
- Per-claim analysis
- Verification hash section
- Explicit claim boundaries

No JavaScript required. No external resources.
"""

from __future__ import annotations

from compliance_drift_detector import DriftReport, DriftState

try:
    from ui_semantics import history_status
except ImportError:  # package-style test/import path
    from software.ui_semantics import history_status


STATE_COLORS = {
    "ALIGNED": "#2d8a4e",
    "DRIFTING": "#d4910a",
    "VIOLATED": "#c9363e",
    "UNDECLARED": "#6e7781",
}


def _escape(text: str) -> str:
    """HTML-escape text."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_html_report(report: DriftReport) -> str:
    """Render a complete static HTML drift report."""
    verdict = report.summary.get("verdict", "UNKNOWN")
    state_counts = report.summary.get("state_counts", {})
    aligned_pct = report.summary.get("aligned_percentage", 0)
    thresholds = report.summary.get("thresholds", {})
    alignment_threshold = thresholds.get("alignment", 0.95)

    verdict_color = {
        "FULLY_ALIGNED": "#2d8a4e",
        "DRIFT_DETECTED": "#d4910a",
        "VIOLATION_DETECTED": "#c9363e",
        "UNDECLARED_BEHAVIORS": "#6e7781",
        "NO_POLICIES": "#6e7781",
    }.get(verdict, "#6e7781")

    analysis_rows = ""
    for a in report.analyses:
        color = STATE_COLORS.get(a.state.value, "#6e7781")
        history = history_status(a, alignment_threshold=alignment_threshold)
        first_breach = a.first_drift_time or "—"
        analysis_rows += f"""        <tr>
            <td><code>{_escape(a.claim_id)}</code></td>
            <td>{_escape(a.claim_description)}</td>
            <td style="color:{color};font-weight:bold">{a.state.value}</td>
            <td>{a.current_alignment:.0%}</td>
            <td><strong>{_escape(history)}</strong></td>
            <td>{_escape(first_breach)}</td>
            <td>{_escape(a.reason)}</td>
        </tr>\n"""

    undeclared_rows = ""
    for u in report.undeclared_behaviors:
        undeclared_rows += f"""        <tr>
            <td><code>{_escape(u.behavior_pattern)}</code></td>
            <td>{u.occurrence_count}</td>
            <td>{_escape(u.first_seen)}</td>
            <td>{_escape(u.last_seen)}</td>
        </tr>\n"""

    undeclared_section = ""
    if report.undeclared_behaviors:
        undeclared_section = f"""
    <h2>Undeclared Behaviors</h2>
    <p>Supplied behavior references marked <code>UNDECLARED-</code> with no matching policy claim. These are separate findings, not policy-claim states:</p>
    <table>
        <tr><th>Pattern</th><th>Count</th><th>First Seen</th><th>Last Seen</th></tr>
{undeclared_rows}
    </table>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Compliance Drift Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1180px; margin: 2rem auto; padding: 0 1rem; color: #1f2328; line-height: 1.6; }}
h1 {{ border-bottom: 2px solid #d1d9e0; padding-bottom: 0.5rem; }}
h2 {{ color: #25292e; margin-top: 2rem; }}
table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
th, td {{ border: 1px solid #d1d9e0; padding: 0.5rem 0.75rem; text-align: left; font-size: 0.9rem; vertical-align: top; }}
th {{ background: #f6f8fa; font-weight: 600; }}
tr:nth-child(even) {{ background: #f6f8fa; }}
code {{ background: #eff1f3; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.85rem; }}
.verdict {{ display: inline-block; padding: 0.4rem 1rem; border-radius: 4px; color: white; font-weight: bold; font-size: 1.1rem; }}
.summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }}
.summary-card {{ background: #f6f8fa; border: 1px solid #d1d9e0; border-radius: 6px; padding: 1rem; text-align: center; }}
.summary-card .number {{ font-size: 1.8rem; font-weight: bold; }}
.summary-card .label {{ font-size: 0.8rem; color: #6e7781; text-transform: uppercase; }}
.hash {{ font-family: monospace; font-size: 0.75rem; word-break: break-all; color: #6e7781; }}
.note {{ color: #57606a; font-size: 0.85rem; }}
.boundary {{ background: #fff8c5; border: 1px solid #d4a72c; border-radius: 6px; padding: 1rem; margin: 1rem 0; }}
.boundary h3 {{ margin-top: 0; }}
</style>
</head>
<body>

<h1>Compliance Drift Report</h1>

<p><span class="verdict" style="background:{verdict_color}">{verdict}</span></p>
<p>Generated: <code>{_escape(report.generated_at)}</code></p>

<div class="summary-grid">
    <div class="summary-card"><div class="number">{report.total_claims}</div><div class="label">Policy Claims</div></div>
    <div class="summary-card"><div class="number">{report.total_evidence}</div><div class="label">Evidence Records</div></div>
    <div class="summary-card"><div class="number">{aligned_pct:.0f}%</div><div class="label">Currently Aligned</div></div>
    <div class="summary-card"><div class="number">{state_counts.get('VIOLATED', 0)}</div><div class="label">Violated Claims</div></div>
</div>

<h2>Drift Analysis</h2>
<table>
    <tr><th>Claim</th><th>Description</th><th>Current State</th><th>Current Alignment</th><th>History Status</th><th>First Threshold Breach</th><th>Reason</th></tr>
{analysis_rows}
</table>
<p class="note"><strong>History Status</strong> summarizes the full supplied checkpoint sequence. For example, <strong>RECOVERED</strong> means the latest checkpoint is aligned after an earlier threshold breach. The machine-readable JSON retains the detector's raw first-to-last trend field.</p>
{undeclared_section}

<h2>Thresholds Used</h2>
<table>
    <tr><th>Parameter</th><th>Value</th><th>Meaning</th></tr>
    <tr><td>Alignment threshold</td><td>{thresholds.get('alignment', 0.95):.0%}</td><td>Current score at or above this = ALIGNED</td></tr>
    <tr><td>Violation threshold</td><td>{thresholds.get('violation', 0.70):.0%}</td><td>Current score below this = VIOLATED</td></tr>
    <tr><td>Drift sensitivity</td><td>{thresholds.get('drift_sensitivity', 0.05):.0%}</td><td>Minimum first-to-last score change used by the detector's raw trend field</td></tr>
</table>

<h2>Verification</h2>
<p>The report hash seals generated metadata, input hashes, totals, and summary values. The evidence export contains per-item and aggregate hashes.</p>
<table>
    <tr><td>Report hash</td><td class="hash">{_escape(report.report_hash)}</td></tr>
    <tr><td>Policy hash</td><td class="hash">{_escape(report.policy_hash)}</td></tr>
    <tr><td>Behavior hash</td><td class="hash">{_escape(report.behavior_hash)}</td></tr>
</table>
<p>Verify report JSON with: <code>python software/verify.py output/drift_report.json</code></p>
<p>Verify exported evidence with: <code>python software/verify.py output/drift_evidence.json</code></p>

<div class="boundary">
<h3>What This Report Shows</h3>
<ul>
    <li>How supplied behavior evidence compares with structured policy claims at dated checkpoints</li>
    <li>Which claims currently meet or fall below the configured alignment and violation thresholds</li>
    <li>Full-sequence history status, including recovery after an earlier threshold breach</li>
    <li>The earliest supplied checkpoint where alignment falls below the configured alignment threshold</li>
</ul>
<h3>What This Report Does NOT Establish</h3>
<ul>
    <li>This is <strong>not</strong> a compliance certification</li>
    <li>This does <strong>not</strong> establish compliance with any standard or regulation</li>
    <li>This does <strong>not</strong> validate the truth, completeness, or provenance of supplied source data</li>
    <li>This does <strong>not</strong> replace a formal audit or accredited assessment</li>
    <li>The current release does <strong>not</strong> infer compliance from raw logs or parse policy documents automatically</li>
</ul>
</div>

<p style="color:#6e7781;font-size:0.8rem;margin-top:3rem;border-top:1px solid #d1d9e0;padding-top:1rem;">
ComplianceDriftDetector — Checkpoint-based policy-behavior drift detection over supplied structured evidence.<br>
Local deterministic analysis. No AI or blackbox scoring.
</p>

</body>
</html>"""
    return html
