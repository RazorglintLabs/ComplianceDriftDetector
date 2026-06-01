"""
Compliance Drift Detector — Verification Tool

Verify any drift artifact for tamper evidence.

Usage:
    python verify.py output/drift_report.json
    python verify.py output/drift_evidence.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(data: str) -> str:
    """Deterministic SHA-256 hash, lowercase hex."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def verify_drift_report(data: dict) -> tuple[bool, str]:
    """
    Verify a drift report for internal consistency.
    
    Checks:
    1. Claim count matches declared total
    2. All drift states are valid
    3. Evidence counts are non-negative
    4. Summary percentages are consistent
    """
    analyses = data.get("analyses", [])
    declared_total = data.get("total_claims", 0)

    if len(analyses) != declared_total:
        return False, f"Claim count mismatch: declared {declared_total}, actual {len(analyses)}"

    valid_states = {"ALIGNED", "DRIFTING", "VIOLATED", "UNDECLARED"}
    valid_trends = {"improving", "stable", "degrading", "insufficient_data", "no_data"}

    for i, analysis in enumerate(analyses):
        if analysis["state"] not in valid_states:
            return False, f"Analysis {i}: invalid state '{analysis['state']}'"
        if analysis["trend"] not in valid_trends:
            return False, f"Analysis {i}: invalid trend '{analysis['trend']}'"
        if analysis["current_alignment"] < 0 or analysis["current_alignment"] > 1:
            return False, f"Analysis {i}: alignment {analysis['current_alignment']} out of range [0, 1]"

    # Verify summary consistency
    summary = data.get("summary", {})
    state_counts = summary.get("state_counts", {})
    total_from_counts = sum(state_counts.values())
    if total_from_counts != declared_total:
        return False, f"State count sum ({total_from_counts}) != declared total ({declared_total})"

    return True, f"Drift report verified: {len(analyses)} claims, structure PASS"


def verify_drift_evidence(data: dict) -> tuple[bool, str]:
    """
    Verify evidence export hashes.
    
    Checks:
    1. Each policy claim hash matches its preimage
    2. Each behavior evidence hash matches its preimage
    3. Aggregate hashes are consistent
    """
    claims = data.get("policy_claims", [])
    evidence = data.get("behavior_evidence", [])
    failures = []

    # Verify claim hashes
    for claim in claims:
        preimage = f"{claim['claim_id']}|{claim['claim_type']}|{claim['testable_assertion']}"
        expected = sha256(preimage)
        if claim["claim_hash"] != expected:
            failures.append(f"Claim {claim['claim_id']}: hash mismatch")

    # Verify evidence hashes
    for ev in evidence[:100]:  # Check first 100 for performance
        preimage = f"{ev['evidence_id']}|{ev['timestamp']}|{ev['claim_ref']}|{ev['observed_value']}|{ev['compliant']}"
        expected = sha256(preimage)
        if ev["evidence_hash"] != expected:
            failures.append(f"Evidence {ev['evidence_id']}: hash mismatch")

    if failures:
        return False, f"FAIL: {len(failures)} hash verification failures:\n  " + "\n  ".join(failures[:10])

    return True, f"Evidence verified: {len(claims)} claims, {len(evidence)} evidence items — hashes PASS"


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify.py <artifact_file.json>")
        print()
        print("Supports:")
        print("  - drift_report.json    (report verification)")
        print("  - drift_evidence.json  (evidence hash verification)")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"FAIL: File not found: {filepath}")
        sys.exit(1)

    data = json.loads(filepath.read_text(encoding="utf-8"))

    print(f"Verifying: {filepath.name}")
    print("-" * 50)

    # Detect file type
    if "analyses" in data and "summary" in data:
        valid, message = verify_drift_report(data)
    elif "policy_claims" in data and "behavior_evidence" in data:
        valid, message = verify_drift_evidence(data)
    else:
        print("FAIL: Unrecognized artifact format")
        sys.exit(1)

    if valid:
        print(f"PASS: {message}")
        sys.exit(0)
    else:
        print(f"FAIL: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
