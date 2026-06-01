"""
run_scan.py — Self-service CSV-to-report scanner

Reads policy_claims.csv and behavior_evidence.csv from input/ directory,
runs ComplianceDriftDetector, writes reports to output/.

No external dependencies. No network calls. No data leaves your machine.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

# Add software/ to path for sibling imports
_software_dir = str(Path(__file__).parent)
if _software_dir not in sys.path:
    sys.path.insert(0, _software_dir)

# Add project root to path
_root_dir = str(Path(__file__).parent.parent)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from compliance_drift_detector import ComplianceDriftDetector
from report_renderer import render_markdown_report, render_json_report
from render_html_report import render_html_report


REQUIRED_POLICY_COLUMNS = {"claim_id", "description", "testable_assertion"}
REQUIRED_EVIDENCE_COLUMNS = {"evidence_id", "timestamp", "claim_ref", "observed_value", "compliant"}


def parse_bool(value: str) -> bool:
    """Parse a boolean from CSV value."""
    return value.strip().lower() in ("true", "1", "yes")


def load_csv(path: Path, required_columns: set[str]) -> list[dict]:
    """Load and validate a CSV file. Returns list of row dicts."""
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            print(f"ERROR: {path} appears to be empty or has no header row.")
            sys.exit(1)

        actual_columns = set(reader.fieldnames)
        missing = required_columns - actual_columns
        if missing:
            print(f"ERROR: {path} is missing required columns: {sorted(missing)}")
            print(f"  Required: {sorted(required_columns)}")
            print(f"  Found:    {sorted(actual_columns)}")
            sys.exit(1)

        rows = list(reader)

    if not rows:
        print(f"WARNING: {path} has a header but no data rows.")

    return rows


def load_policies(path: Path) -> list[dict]:
    """Load policy claims from CSV."""
    rows = load_csv(path, REQUIRED_POLICY_COLUMNS)
    policies = []
    for row in rows:
        pol = {
            "claim_id": row["claim_id"].strip(),
            "description": row["description"].strip(),
            "testable_assertion": row["testable_assertion"].strip(),
            "claim_type": row.get("claim_type", "REQUIREMENT").strip() or "REQUIREMENT",
        }
        threshold = row.get("threshold", "").strip()
        if threshold:
            try:
                pol["threshold"] = float(threshold)
            except ValueError:
                pass
        policies.append(pol)
    return policies


def load_evidence(path: Path) -> list[dict]:
    """Load behavior evidence from CSV."""
    rows = load_csv(path, REQUIRED_EVIDENCE_COLUMNS)
    evidence = []
    for row in rows:
        ev = {
            "evidence_id": row["evidence_id"].strip(),
            "timestamp": row["timestamp"].strip(),
            "claim_ref": row["claim_ref"].strip(),
            "observed_value": row["observed_value"].strip(),
            "compliant": parse_bool(row["compliant"]),
            "source": row.get("source", "UNKNOWN").strip() or "UNKNOWN",
        }
        evidence.append(ev)
    return evidence


def main():
    """Main entry point for self-service scan."""
    # Determine paths
    root = Path(__file__).parent.parent
    input_dir = root / "input"
    output_dir = root / "output"

    policy_path = input_dir / "policy_claims.csv"
    evidence_path = input_dir / "behavior_evidence.csv"

    # Check input directory exists
    if not input_dir.exists():
        print("=" * 60)
        print("  No input/ directory found.")
        print()
        print("  To run a scan:")
        print("    1. Create an input/ folder")
        print("    2. Add policy_claims.csv")
        print("    3. Add behavior_evidence.csv")
        print()
        print("  See input_templates/ for format reference.")
        print("  See examples/template_packs/ for ready-to-use examples.")
        print()
        print("  Running demo instead...")
        print("=" * 60)
        print()
        from software.run_demo import main as demo_main
        demo_main()
        return

    if not policy_path.exists() or not evidence_path.exists():
        print("=" * 60)
        print("  input/ directory found but missing required files:")
        if not policy_path.exists():
            print(f"    MISSING: {policy_path}")
        if not evidence_path.exists():
            print(f"    MISSING: {evidence_path}")
        print()
        print("  Both files are required. See input_templates/ for format.")
        print("=" * 60)
        sys.exit(1)

    # Load data
    print("Loading policy claims...")
    policies = load_policies(policy_path)
    print(f"  {len(policies)} policy claim(s) loaded.")

    print("Loading behavior evidence...")
    evidence = load_evidence(evidence_path)
    print(f"  {len(evidence)} evidence record(s) loaded.")

    # Run detector
    print("Running drift analysis...")
    detector = ComplianceDriftDetector()
    detector.load_policies(policies)
    detector.load_behavior(evidence)
    report = detector.detect_drift()

    # Write outputs
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "drift_report.json"
    md_path = output_dir / "drift_report.md"
    html_path = output_dir / "drift_report.html"
    evidence_path_out = output_dir / "drift_evidence.json"

    json_content = render_json_report(report)
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(json_content)

    md_content = render_markdown_report(report)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    html_content = render_html_report(report)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    evidence_export = detector.export_evidence()
    with open(evidence_path_out, "w", encoding="utf-8") as f:
        json.dump(evidence_export, f, indent=2)

    # Summary
    print()
    print("=" * 60)
    print("  SCAN COMPLETE")
    print("=" * 60)
    print()
    print(f"  Verdict: {report.summary['verdict']}")
    print(f"  Claims analyzed: {report.total_claims}")
    print(f"  Evidence records: {report.total_evidence}")
    print()
    for state, count in report.summary.get("state_counts", {}).items():
        print(f"    {state}: {count}")
    print()
    print("  Reports written to:")
    print(f"    {json_path}")
    print(f"    {md_path}")
    print(f"    {html_path}")
    print(f"    {evidence_path_out}")
    print()
    print("  Verify with: python software/verify.py")
    print()
    print("  No data left your machine.")
    print("=" * 60)


if __name__ == "__main__":
    main()
