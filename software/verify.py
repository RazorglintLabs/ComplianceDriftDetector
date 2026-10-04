"""
Compliance Drift Detector — Verification Tool

Verify supported drift artifacts for internal consistency and tamper evidence.

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
    Verify a drift report for internal consistency and report-seal integrity.

    Checks:
    1. Claim count matches declared total
    2. Drift states, trends, and alignment values are valid
    3. Summary state counts and aligned percentage match analyses
    4. The report hash matches the sealed report metadata/summary payload
    """
    try:
        analyses = data.get("analyses", [])
        declared_total = data.get("total_claims", 0)
        total_evidence = data.get("total_evidence", 0)

        if not isinstance(declared_total, int) or declared_total < 0:
            return False, f"Invalid total_claims: {declared_total!r}"
        if not isinstance(total_evidence, int) or total_evidence < 0:
            return False, f"Invalid total_evidence: {total_evidence!r}"
        if len(analyses) != declared_total:
            return False, f"Claim count mismatch: declared {declared_total}, actual {len(analyses)}"

        valid_states = {"ALIGNED", "DRIFTING", "VIOLATED", "UNDECLARED"}
        valid_trends = {"improving", "stable", "degrading", "insufficient_data", "no_data"}
        computed_state_counts: dict[str, int] = {}

        for i, analysis in enumerate(analyses):
            state = analysis["state"]
            trend = analysis["trend"]
            alignment = analysis["current_alignment"]

            if state not in valid_states:
                return False, f"Analysis {i}: invalid state '{state}'"
            if trend not in valid_trends:
                return False, f"Analysis {i}: invalid trend '{trend}'"
            if not isinstance(alignment, (int, float)) or alignment < 0 or alignment > 1:
                return False, f"Analysis {i}: alignment {alignment!r} out of range [0, 1]"

            computed_state_counts[state] = computed_state_counts.get(state, 0) + 1

        summary = data.get("summary", {})
        state_counts = summary.get("state_counts", {})
        if state_counts != computed_state_counts:
            return False, f"State counts mismatch: summary {state_counts}, analyses {computed_state_counts}"

        expected_aligned_pct = round(
            (computed_state_counts.get("ALIGNED", 0) / declared_total * 100) if declared_total else 0,
            1,
        )
        actual_aligned_pct = summary.get("aligned_percentage", 0)
        if actual_aligned_pct != expected_aligned_pct:
            return False, (
                f"Aligned percentage mismatch: summary {actual_aligned_pct}, "
                f"expected {expected_aligned_pct}"
            )

        seal_payload = {
            "generated_at": data["generated_at"],
            "policy_hash": data["policy_hash"],
            "behavior_hash": data["behavior_hash"],
            "total_claims": declared_total,
            "total_evidence": total_evidence,
            "summary": summary,
        }
        expected_report_hash = sha256(json.dumps(seal_payload, sort_keys=True))
        actual_report_hash = data.get("report_hash", "")
        if actual_report_hash != expected_report_hash:
            return False, "Report hash mismatch"

    except (KeyError, TypeError, ValueError) as exc:
        return False, f"Malformed drift report: {exc}"

    return True, f"Drift report verified: {len(analyses)} claims, structure + report seal PASS"


def verify_drift_evidence(data: dict) -> tuple[bool, str]:
    """
    Verify the complete evidence export.

    Checks:
    1. Every policy claim hash matches its preimage
    2. Every behavior evidence hash matches its preimage
    3. Aggregate policy and behavior hashes match the exported verification block
    """
    claims = data.get("policy_claims", [])
    evidence = data.get("behavior_evidence", [])
    verification = data.get("verification", {})
    failures: list[str] = []

    try:
        for claim in claims:
            preimage = f"{claim['claim_id']}|{claim['claim_type']}|{claim['testable_assertion']}"
            expected = sha256(preimage)
            if claim.get("claim_hash") != expected:
                failures.append(f"Claim {claim.get('claim_id', '<unknown>')}: hash mismatch")

        for ev in evidence:
            preimage = (
                f"{ev['evidence_id']}|{ev['timestamp']}|{ev['claim_ref']}|"
                f"{ev['observed_value']}|{ev['compliant']}"
            )
            expected = sha256(preimage)
            if ev.get("evidence_hash") != expected:
                failures.append(f"Evidence {ev.get('evidence_id', '<unknown>')}: hash mismatch")

        policy_content = json.dumps(
            [
                {
                    "id": claim["claim_id"],
                    "type": claim["claim_type"],
                    "assertion": claim["testable_assertion"],
                }
                for claim in claims
            ],
            sort_keys=True,
        )
        expected_policy_hash = sha256(policy_content)
        if verification.get("policy_hash") != expected_policy_hash:
            failures.append("Aggregate policy hash mismatch")

        behavior_content = json.dumps(
            [
                {
                    "id": ev["evidence_id"],
                    "ts": ev["timestamp"],
                    "claim": ev["claim_ref"],
                    "val": ev["observed_value"],
                }
                for ev in evidence
            ],
            sort_keys=True,
        )
        expected_behavior_hash = sha256(behavior_content)
        if verification.get("behavior_hash") != expected_behavior_hash:
            failures.append("Aggregate behavior hash mismatch")

        if verification.get("hash_algorithm") not in (None, "SHA-256"):
            failures.append(f"Unexpected hash algorithm: {verification.get('hash_algorithm')}")

    except (KeyError, TypeError, ValueError) as exc:
        return False, f"Malformed evidence export: {exc}"

    if failures:
        return False, f"{len(failures)} verification failure(s):\n  " + "\n  ".join(failures[:10])

    return True, (
        f"Evidence verified: {len(claims)} claims, {len(evidence)} evidence items — "
        "all item + aggregate hashes PASS"
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify.py <artifact_file.json>")
        print()
        print("Supports:")
        print("  - drift_report.json    (structure + report-seal verification)")
        print("  - drift_evidence.json  (complete item + aggregate hash verification)")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"FAIL: File not found: {filepath}")
        sys.exit(1)

    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: Could not read valid JSON: {exc}")
        sys.exit(1)

    print(f"Verifying: {filepath.name}")
    print("-" * 50)

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

    print(f"FAIL: {message}")
    sys.exit(1)


if __name__ == "__main__":
    main()
