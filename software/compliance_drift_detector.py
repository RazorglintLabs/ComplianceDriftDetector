"""
Compliance Drift Detector — Core Engine

Compares policy declarations against system behavior evidence.
Detects drift over time. Produces tamper-evident drift reports.

No external dependencies. No blackbox. Every rule visible.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional


class DriftState(Enum):
    """Drift classification for a policy claim."""
    ALIGNED = "ALIGNED"
    DRIFTING = "DRIFTING"
    VIOLATED = "VIOLATED"
    UNDECLARED = "UNDECLARED"


class PolicyClaimType(Enum):
    """Types of policy claims."""
    REQUIREMENT = "REQUIREMENT"      # "All X must Y"
    PROHIBITION = "PROHIBITION"      # "No X shall Y"
    THRESHOLD = "THRESHOLD"          # "X must be >= Y"
    PROCESS = "PROCESS"              # "Every X follows process Y"
    CONTROL = "CONTROL"              # "Control X is active"


@dataclass(frozen=True)
class PolicyClaim:
    """A single testable policy claim."""
    claim_id: str
    policy_source: str
    claim_type: str
    description: str
    testable_assertion: str
    threshold: Optional[float] = None
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class BehaviorEvidence:
    """A single piece of system behavior evidence."""
    evidence_id: str
    timestamp: str
    source: str
    claim_ref: str  # which claim this relates to
    observed_value: str
    compliant: bool
    metadata: dict = field(default_factory=dict)


@dataclass
class CheckpointMeasurement:
    """Alignment measurement at a single checkpoint."""
    checkpoint_time: str
    claim_id: str
    evidence_count: int
    compliant_count: int
    alignment_score: float  # 0.0 to 1.0
    evidence_hash: str


@dataclass
class DriftAnalysis:
    """Complete drift analysis for a single policy claim."""
    claim_id: str
    claim_description: str
    state: DriftState
    reason: str
    current_alignment: float
    trend: str  # "improving", "stable", "degrading"
    checkpoints: list[CheckpointMeasurement] = field(default_factory=list)
    first_drift_time: Optional[str] = None
    violation_count: int = 0


@dataclass
class UndeclaredBehavior:
    """System behavior with no corresponding policy claim."""
    behavior_pattern: str
    occurrence_count: int
    first_seen: str
    last_seen: str
    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class DriftReport:
    """Complete drift detection report."""
    generated_at: str
    policy_hash: str
    behavior_hash: str
    total_claims: int
    total_evidence: int
    analyses: list[DriftAnalysis] = field(default_factory=list)
    undeclared_behaviors: list[UndeclaredBehavior] = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    report_hash: str = ""


def sha256(data: str) -> str:
    """Deterministic SHA-256 hash, lowercase hex."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def hash_policy(claims: list[PolicyClaim]) -> str:
    """Hash all policy claims deterministically."""
    content = json.dumps(
        [{"id": c.claim_id, "type": c.claim_type, "assertion": c.testable_assertion} for c in claims],
        sort_keys=True
    )
    return sha256(content)


def hash_behavior(evidence: list[BehaviorEvidence]) -> str:
    """Hash all behavior evidence deterministically."""
    content = json.dumps(
        [{"id": e.evidence_id, "ts": e.timestamp, "claim": e.claim_ref, "val": e.observed_value} for e in evidence],
        sort_keys=True
    )
    return sha256(content)


class AlignmentEngine:
    """
    Measures alignment between policy claims and behavior evidence.
    
    Rules (all visible):
    - Alignment score = compliant_evidence / total_evidence for that claim
    - Score 1.0 = ALIGNED (100% of evidence confirms compliance)
    - Score >= threshold = ALIGNED (configurable, default 0.95)
    - Score < threshold but >= violation_threshold = DRIFTING
    - Score < violation_threshold = VIOLATED
    - Behavior with no matching claim = UNDECLARED
    """

    def __init__(
        self,
        alignment_threshold: float = 0.95,
        violation_threshold: float = 0.70,
        drift_sensitivity: float = 0.05,
    ):
        """
        Args:
            alignment_threshold: Score above this = ALIGNED (default 95%)
            violation_threshold: Score below this = VIOLATED (default 70%)
            drift_sensitivity: Minimum score change to detect trend (default 5%)
        """
        self.alignment_threshold = alignment_threshold
        self.violation_threshold = violation_threshold
        self.drift_sensitivity = drift_sensitivity

    def measure_checkpoint(
        self,
        claim: PolicyClaim,
        evidence: list[BehaviorEvidence],
        checkpoint_time: str,
    ) -> CheckpointMeasurement:
        """Measure alignment for a claim at a single checkpoint."""
        relevant = [e for e in evidence if e.claim_ref == claim.claim_id]
        total = len(relevant)
        compliant = sum(1 for e in relevant if e.compliant)

        score = compliant / total if total > 0 else 0.0

        # Hash the evidence for this measurement
        evidence_content = json.dumps(
            [{"id": e.evidence_id, "compliant": e.compliant} for e in relevant],
            sort_keys=True
        )

        return CheckpointMeasurement(
            checkpoint_time=checkpoint_time,
            claim_id=claim.claim_id,
            evidence_count=total,
            compliant_count=compliant,
            alignment_score=round(score, 4),
            evidence_hash=sha256(evidence_content),
        )

    def detect_trend(self, checkpoints: list[CheckpointMeasurement]) -> str:
        """
        Detect alignment trend over checkpoints.
        
        Uses simple linear direction:
        - If last score > first score + sensitivity: "improving"
        - If last score < first score - sensitivity: "degrading"
        - Otherwise: "stable"
        """
        if len(checkpoints) < 2:
            return "insufficient_data"

        first_score = checkpoints[0].alignment_score
        last_score = checkpoints[-1].alignment_score
        delta = last_score - first_score

        if delta > self.drift_sensitivity:
            return "improving"
        elif delta < -self.drift_sensitivity:
            return "degrading"
        else:
            return "stable"

    def classify_drift(
        self,
        claim: PolicyClaim,
        checkpoints: list[CheckpointMeasurement],
    ) -> DriftAnalysis:
        """
        Classify drift state for a policy claim based on checkpoint measurements.
        """
        if not checkpoints:
            return DriftAnalysis(
                claim_id=claim.claim_id,
                claim_description=claim.description,
                state=DriftState.UNDECLARED,
                reason="No evidence found for this claim",
                current_alignment=0.0,
                trend="no_data",
            )

        current = checkpoints[-1]
        trend = self.detect_trend(checkpoints)

        # Find first drift point
        first_drift_time = None
        violation_count = 0

        for cp in checkpoints:
            if cp.alignment_score < self.alignment_threshold:
                if first_drift_time is None:
                    first_drift_time = cp.checkpoint_time
            if cp.alignment_score < self.violation_threshold:
                violation_count += 1

        # Classify current state
        if current.alignment_score >= self.alignment_threshold:
            state = DriftState.ALIGNED
            reason = f"Alignment at {current.alignment_score:.1%} (threshold: {self.alignment_threshold:.1%})"
        elif current.alignment_score >= self.violation_threshold:
            state = DriftState.DRIFTING
            reason = (
                f"Alignment at {current.alignment_score:.1%} — below threshold "
                f"({self.alignment_threshold:.1%}) but above violation level "
                f"({self.violation_threshold:.1%}). Trend: {trend}."
            )
        else:
            state = DriftState.VIOLATED
            reason = (
                f"Alignment at {current.alignment_score:.1%} — below violation threshold "
                f"({self.violation_threshold:.1%}). {violation_count} violation checkpoint(s) recorded."
            )

        return DriftAnalysis(
            claim_id=claim.claim_id,
            claim_description=claim.description,
            state=state,
            reason=reason,
            current_alignment=current.alignment_score,
            trend=trend,
            checkpoints=checkpoints,
            first_drift_time=first_drift_time,
            violation_count=violation_count,
        )


class ComplianceDriftDetector:
    """
    Main engine. Ingests policies and behavior, detects drift, produces report.
    """

    def __init__(
        self,
        alignment_threshold: float = 0.95,
        violation_threshold: float = 0.70,
        drift_sensitivity: float = 0.05,
    ):
        self.engine = AlignmentEngine(
            alignment_threshold=alignment_threshold,
            violation_threshold=violation_threshold,
            drift_sensitivity=drift_sensitivity,
        )
        self.claims: list[PolicyClaim] = []
        self.evidence: list[BehaviorEvidence] = []

    def load_policies(self, raw_policies: list[dict]) -> None:
        """Load policy declarations."""
        for pol in raw_policies:
            claim = PolicyClaim(
                claim_id=pol["claim_id"],
                policy_source=pol.get("policy_source", ""),
                claim_type=pol.get("claim_type", PolicyClaimType.REQUIREMENT.value),
                description=pol["description"],
                testable_assertion=pol["testable_assertion"],
                threshold=pol.get("threshold"),
                metadata=pol.get("metadata", {}),
            )
            self.claims.append(claim)

    def load_behavior(self, raw_evidence: list[dict]) -> None:
        """Load system behavior evidence."""
        for ev in raw_evidence:
            evidence = BehaviorEvidence(
                evidence_id=ev["evidence_id"],
                timestamp=ev["timestamp"],
                source=ev.get("source", "UNKNOWN"),
                claim_ref=ev["claim_ref"],
                observed_value=ev["observed_value"],
                compliant=ev["compliant"],
                metadata=ev.get("metadata", {}),
            )
            self.evidence.append(evidence)

    def _group_evidence_by_checkpoint(self) -> dict[str, list[BehaviorEvidence]]:
        """Group evidence by date (daily checkpoints)."""
        groups: dict[str, list[BehaviorEvidence]] = {}
        for ev in self.evidence:
            # Use date as checkpoint key
            date_key = ev.timestamp[:10]  # YYYY-MM-DD
            groups.setdefault(date_key, []).append(ev)
        return groups

    def _find_undeclared_behaviors(self) -> list[UndeclaredBehavior]:
        """Find behavior evidence that doesn't map to any policy claim."""
        claim_ids = {c.claim_id for c in self.claims}
        undeclared_refs: dict[str, list[BehaviorEvidence]] = {}

        for ev in self.evidence:
            if ev.claim_ref not in claim_ids and ev.claim_ref.startswith("UNDECLARED-"):
                undeclared_refs.setdefault(ev.claim_ref, []).append(ev)

        undeclared = []
        for ref, evidences in undeclared_refs.items():
            sorted_ev = sorted(evidences, key=lambda e: e.timestamp)
            undeclared.append(UndeclaredBehavior(
                behavior_pattern=ref,
                occurrence_count=len(evidences),
                first_seen=sorted_ev[0].timestamp,
                last_seen=sorted_ev[-1].timestamp,
                evidence_ids=[e.evidence_id for e in sorted_ev[:10]],
            ))

        return undeclared

    def detect_drift(self) -> DriftReport:
        """
        Main entry point. Analyzes all policies against behavior,
        detects drift, produces sealed report.
        """
        if not self.claims:
            return DriftReport(
                generated_at=datetime.utcnow().isoformat() + "Z",
                policy_hash=sha256("EMPTY"),
                behavior_hash=sha256("EMPTY"),
                total_claims=0,
                total_evidence=0,
                summary={"verdict": "NO_POLICIES"},
            )

        # Hash inputs
        policy_hash = hash_policy(self.claims)
        behavior_hash = hash_behavior(self.evidence)

        # Group evidence by checkpoint
        checkpoints_map = self._group_evidence_by_checkpoint()
        checkpoint_keys = sorted(checkpoints_map.keys())

        # Analyze each claim
        analyses: list[DriftAnalysis] = []

        for claim in self.claims:
            # Build checkpoints for this claim
            claim_checkpoints: list[CheckpointMeasurement] = []
            for cp_key in checkpoint_keys:
                cp_evidence = checkpoints_map[cp_key]
                measurement = self.engine.measure_checkpoint(claim, cp_evidence, cp_key)
                if measurement.evidence_count > 0:
                    claim_checkpoints.append(measurement)

            # Classify drift
            analysis = self.engine.classify_drift(claim, claim_checkpoints)
            analyses.append(analysis)

        # Find undeclared behaviors
        undeclared = self._find_undeclared_behaviors()

        # Build summary
        state_counts: dict[str, int] = {}
        for analysis in analyses:
            state_counts[analysis.state.value] = state_counts.get(analysis.state.value, 0) + 1

        total = len(analyses)
        aligned_pct = (state_counts.get("ALIGNED", 0) / total * 100) if total > 0 else 0

        if state_counts.get("VIOLATED", 0) > 0:
            verdict = "VIOLATION_DETECTED"
        elif state_counts.get("DRIFTING", 0) > 0:
            verdict = "DRIFT_DETECTED"
        elif undeclared:
            verdict = "UNDECLARED_BEHAVIORS"
        else:
            verdict = "FULLY_ALIGNED"

        summary = {
            "total_claims": total,
            "state_counts": state_counts,
            "aligned_percentage": round(aligned_pct, 1),
            "undeclared_behavior_count": len(undeclared),
            "verdict": verdict,
            "thresholds": {
                "alignment": self.engine.alignment_threshold,
                "violation": self.engine.violation_threshold,
                "drift_sensitivity": self.engine.drift_sensitivity,
            },
        }

        report = DriftReport(
            generated_at=datetime.utcnow().isoformat() + "Z",
            policy_hash=policy_hash,
            behavior_hash=behavior_hash,
            total_claims=total,
            total_evidence=len(self.evidence),
            analyses=analyses,
            undeclared_behaviors=undeclared,
            summary=summary,
        )

        # Seal the report
        seal_content = json.dumps({
            "generated_at": report.generated_at,
            "policy_hash": report.policy_hash,
            "behavior_hash": report.behavior_hash,
            "total_claims": report.total_claims,
            "total_evidence": report.total_evidence,
            "summary": report.summary,
        }, sort_keys=True)
        report.report_hash = sha256(seal_content)

        return report

    def export_evidence(self) -> dict:
        """Export full evidence set with hashes for independent verification."""
        return {
            "policy_claims": [
                {
                    "claim_id": c.claim_id,
                    "policy_source": c.policy_source,
                    "claim_type": c.claim_type,
                    "description": c.description,
                    "testable_assertion": c.testable_assertion,
                    "claim_hash": sha256(f"{c.claim_id}|{c.claim_type}|{c.testable_assertion}"),
                }
                for c in self.claims
            ],
            "behavior_evidence": [
                {
                    "evidence_id": e.evidence_id,
                    "timestamp": e.timestamp,
                    "source": e.source,
                    "claim_ref": e.claim_ref,
                    "observed_value": e.observed_value,
                    "compliant": e.compliant,
                    "evidence_hash": sha256(f"{e.evidence_id}|{e.timestamp}|{e.claim_ref}|{e.observed_value}|{e.compliant}"),
                }
                for e in self.evidence
            ],
            "verification": {
                "hash_algorithm": "SHA-256",
                "policy_hash": hash_policy(self.claims),
                "behavior_hash": hash_behavior(self.evidence),
            },
        }
