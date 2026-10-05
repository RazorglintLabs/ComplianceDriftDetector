"""Buyer-facing UI semantics for Compliance Drift Detector.

This module does not change detector classifications or verifier behavior.
It only derives presentation labels that make current state, historical
threshold breaches, and unmatched behavior findings explicit.
"""

from __future__ import annotations

from typing import Any


CLAIM_STATES = ("ALIGNED", "DRIFTING", "VIOLATED", "UNDECLARED")


def result_counts(report: Any) -> tuple[dict[str, int], int]:
    """Return policy-claim state counts and undeclared-behavior count separately."""
    raw_counts = report.summary.get("state_counts", {})
    claim_counts = {state: int(raw_counts.get(state, 0)) for state in CLAIM_STATES}
    undeclared_behavior_count = len(report.undeclared_behaviors)
    return claim_counts, undeclared_behavior_count


def history_status(
    analysis: Any,
    *,
    alignment_threshold: float = 0.95,
) -> str:
    """Derive a full-history display label without rewriting engine output.

    The engine's ``trend`` field is intentionally preserved as its raw
    first-to-last direction. This display status adds one missing distinction:
    when the latest checkpoint is aligned again after one or more earlier
    checkpoints fell below the alignment threshold, the history is RECOVERED,
    not merely STABLE.
    """
    checkpoints = list(getattr(analysis, "checkpoints", []) or [])
    if not checkpoints:
        return "NO DATA"

    latest_score = checkpoints[-1].alignment_score
    earlier_scores = [cp.alignment_score for cp in checkpoints[:-1]]

    if latest_score >= alignment_threshold and any(
        score < alignment_threshold for score in earlier_scores
    ):
        return "RECOVERED"

    raw_trend = str(getattr(analysis, "trend", "") or "").strip()
    if not raw_trend:
        return "UNKNOWN"
    return raw_trend.replace("_", " ").upper()
