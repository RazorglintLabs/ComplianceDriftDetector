"""
render_html_report.py — Static HTML drift report renderer

Produces a single self-contained HTML file with:
- Executive summary
- Drift state table
- Per-claim analysis
- Verification hash section
- What this proves / does not prove

No JavaScript required. No external resources.
"""

from __future__ import annotations

from compliance_drift_detector import DriftReport, DriftState


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

    verdict_color = {
        "FULLY_ALIGNED": "#2d8a4e",
        "DRIFT_DETECTED": "#d4910a",
        "VIOLATION_DETECTED": "#c9363e",
        "UNDECLARED_BEHAVIORS": "#6e7781",
        "NO_POLICIES": "#6e7781",
    }.get(verdict, "#6e7781")

    # Build analysis rows
    analysis_rows = ""
    for a in report.analyses:
        color = STATE_COLORS.get(a.state.value, "#6e7781")
        analysis_rows += f"""        <tr>
            <td><code>{_escape(a.claim_id)}</code></td>
            <td>{_escape(a.claim_description)}</td>
            <td style="color:{color};font-weight:bold">{a.state.value}</td>
            <td>{a.current_alignment:.0%}</td>
            <td>{_escape(a.trend)}</td>
            <td>{_escape(a.reason)}</td>
        </tr>\n"""

    # Build undeclared rows
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
    <p>System behaviors detected with no governing policy claim:</p>
    <table>
        <tr><th>Pattern</th><th>Count</th><th>First Seen</th><th>Last Seen</th></tr>
{undeclared_rows}
    </table>"""

    thresholds = report.summary.get("thresholds", {})

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Compliance Drift Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; color: #1f2328; line-height: 1.6; }}
h1 {{ border-bottom: 2px solid #d1d9e0; padding-bottom: 0.5rem; }}
h2 {{ color: #25292e; margin-top: 2rem; }}
table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
th, td {{ border: 1px solid #d1d9e0; padding: 0.5rem 0.75rem; text-align: left; font-size: 0.9rem; }}
th {{ background: #f6f8fa; font-weight: 600; }}
tr:nth-child(even) {{ background: #f6f8fa; }}
code {{ background: #eff1f3; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.85rem; }}
.verdict {{ display: inline-block; padding: 0.4rem 1rem; border-radius: 4px; color: white; font-weight: bold; font-size: 1.1rem; }}
.summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }}
.summary-card {{ background: #f6f8fa; border: 1px solid #d1d9e0; border-radius: 6px; padding: 1rem; text-align: center; }}
.summary-card .number {{ font-size: 1.8rem; font-weight: bold; }}
.summary-card .label {{ font-size: 0.8rem; color: #6e7781; text-transform: uppercase; }}
.hash {{ font-family: monospace; font-size: 0.75rem; word-break: break-all; color: #6e7781; }}
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
    <div class="summary-card"><div class="number">{aligned_pct:.0f}%</div><div class="label">Aligned</div></div>
    <div class="summary-card"><div class="number">{state_counts.get('VIOLATED', 0)}</div><div class="label">Violations</div></div>
</div>

<h2>Drift Analysis</h2>
<table>
    <tr><th>Claim</th><th>Description</th><th>State</th><th>Alignment</th><th>Trend</th><th>Reason</th></tr>
{analysis_rows}
</table>
{undeclared_section}

<h2>Thresholds Used</h2>
<table>
    <tr><th>Parameter</th><th>Value</th><th>Meaning</th></tr>
    <tr><td>Alignment threshold</td><td>{thresholds.get('alignment', 0.95):.0%}</td><td>Score above this = ALIGNED</td></tr>
    <tr><td>Violation threshold</td><td>{thresholds.get('violation', 0.70):.0%}</td><td>Score below this = VIOLATED</td></tr>
    <tr><td>Drift sensitivity</td><td>{thresholds.get('drift_sensitivity', 0.05):.0%}</td><td>Minimum change to detect trend</td></tr>
</table>

<h2>Verification</h2>
<p>This report is tamper-evident. Any modification breaks the hash chain.</p>
<table>
    <tr><td>Report hash</td><td class="hash">{_escape(report.report_hash)}</td></tr>
    <tr><td>Policy hash</td><td class="hash">{_escape(report.policy_hash)}</td></tr>
    <tr><td>Behavior hash</td><td class="hash">{_escape(report.behavior_hash)}</td></tr>
</table>
<p>Verify with: <code>python software/verify.py</code></p>

<div class="boundary">
<h3>What This Report Proves</h3>
<ul>
    <li>Whether stated policies match observed system behavior at each checkpoint</li>
    <li>Which claims are drifting and in which direction</li>
    <li>That the analysis is tamper-evident and independently verifiable</li>
</ul>
<h3>What This Report Does NOT Prove</h3>
<ul>
    <li>This is <strong>not</strong> a compliance certification</li>
    <li>This does <strong>not</strong> make you compliant with any standard</li>
    <li>This does <strong>not</strong> replace a formal audit by an accredited body</li>
    <li>This produces evidence for audit preparation — not regulatory approval</li>
</ul>
</div>

<p style="color:#6e7781;font-size:0.8rem;margin-top:3rem;border-top:1px solid #d1d9e0;padding-top:1rem;">
ComplianceDriftDetector — Checkpoint-based policy-behavior drift detection.<br>
No data left your machine. Deterministic analysis. No AI. No blackbox.
</p>

</body>
</html>"""
    return html
