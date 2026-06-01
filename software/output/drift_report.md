# Compliance Drift Report

**Generated:** 2026-05-19T10:33:22.712493Z
**Policy Hash:** `a2841f8fafe0e19e...`
**Behavior Hash:** `c70a4a567617e791...`
**Report Hash:** `572fd7a952a8da2f...`
**Claims Analyzed:** 5
**Evidence Points:** 314

---

## Overall Verdict

**VIOLATION_DETECTED**

- Policy alignment: **40.0%** of claims fully aligned
- Total claims: **5**
- Undeclared behaviors: **1**

### Thresholds (visible — no hidden scoring)

- Alignment threshold: **95%** (above = ALIGNED)
- Violation threshold: **70%** (below = VIOLATED)
- Drift sensitivity: **5%** (minimum trend delta)

### State Distribution

| State | Count | Meaning |
|-------|-------|---------|
| ALIGNED | 2 | Policy matches behavior — evidence confirms |
| DRIFTING | 1 | Behavior diverging from policy — trend detected |
| VIOLATED | 2 | Clear evidence contradicts policy |

---

## Policy Claim Analysis

### Claim 1: `POL-001` — [DRIFTING]

- **Description:** All production deployments require explicit approval
- **State:** DRIFTING
- **Current Alignment:** 80.0%
- **Trend:** degrading
- **Reason:** Alignment at 80.0% — below threshold (95.0%) but above violation level (70.0%). Trend: degrading.
- **First drift detected:** 2026-05-09
- **Checkpoints:** 30 measurements

  | Date | Alignment | Evidence |
  |------|-----------|----------|
  | 2026-05-14 | 80.0% | 5 items |
  | 2026-05-15 | 80.0% | 5 items |
  | 2026-05-16 | 80.0% | 5 items |
  | 2026-05-17 | 80.0% | 5 items |
  | 2026-05-18 | 80.0% | 5 items |

### Claim 2: `POL-002` — [VIOLATED]

- **Description:** No service account shall have persistent admin access
- **State:** VIOLATED
- **Current Alignment:** 0.0%
- **Trend:** degrading
- **Reason:** Alignment at 0.0% — below violation threshold (70.0%). 15 violation checkpoint(s) recorded.
- **First drift detected:** 2026-05-04
- **Violation checkpoints:** 15
- **Checkpoints:** 30 measurements

  | Date | Alignment | Evidence |
  |------|-----------|----------|
  | 2026-05-14 | 0.0% | 1 items |
  | 2026-05-15 | 0.0% | 1 items |
  | 2026-05-16 | 0.0% | 1 items |
  | 2026-05-17 | 0.0% | 1 items |
  | 2026-05-18 | 0.0% | 1 items |

### Claim 3: `POL-003` — [ALIGNED]

- **Description:** PII access logging must cover >= 99% of access events
- **State:** ALIGNED
- **Current Alignment:** 100.0%
- **Trend:** stable
- **Reason:** Alignment at 100.0% (threshold: 95.0%)
- **Checkpoints:** 30 measurements

  | Date | Alignment | Evidence |
  |------|-----------|----------|
  | 2026-05-14 | 100.0% | 1 items |
  | 2026-05-15 | 100.0% | 1 items |
  | 2026-05-16 | 100.0% | 1 items |
  | 2026-05-17 | 100.0% | 1 items |
  | 2026-05-18 | 100.0% | 1 items |

### Claim 4: `POL-004` — [VIOLATED]

- **Description:** All security incidents must have response within 4 hours
- **State:** VIOLATED
- **Current Alignment:** 0.0%
- **Trend:** degrading
- **Reason:** Alignment at 0.0% — below violation threshold (70.0%). 3 violation checkpoint(s) recorded.
- **First drift detected:** 2026-05-10
- **Violation checkpoints:** 3
- **Checkpoints:** 10 measurements

  | Date | Alignment | Evidence |
  |------|-----------|----------|
  | 2026-05-04 | 100.0% | 1 items |
  | 2026-05-07 | 100.0% | 1 items |
  | 2026-05-10 | 0.0% | 1 items |
  | 2026-05-13 | 0.0% | 1 items |
  | 2026-05-16 | 0.0% | 1 items |

### Claim 5: `POL-005` — [ALIGNED]

- **Description:** AI model outputs must be logged before delivery to end users
- **State:** ALIGNED
- **Current Alignment:** 100.0%
- **Trend:** stable
- **Reason:** Alignment at 100.0% (threshold: 95.0%)
- **Checkpoints:** 30 measurements

  | Date | Alignment | Evidence |
  |------|-----------|----------|
  | 2026-05-14 | 100.0% | 3 items |
  | 2026-05-15 | 100.0% | 3 items |
  | 2026-05-16 | 100.0% | 3 items |
  | 2026-05-17 | 100.0% | 3 items |
  | 2026-05-18 | 100.0% | 3 items |

---

## Undeclared Behaviors

System behaviors detected with no corresponding policy claim:

| Pattern | Occurrences | First Seen | Last Seen |
|---------|-------------|------------|-----------|
| UNDECLARED-auto-rollback | 4 | 2026-04-26 | 2026-05-17 |

*These behaviors may represent ungoverned operations or policy gaps.*

---

## Verification

This report is tamper-evident. To verify:

1. Re-run the detector with the same policies and evidence
2. Compare `report_hash` — must match exactly
3. Verify evidence hashes with `verify.py`

Policy hash and behavior hash anchor both sides.
Any modification to policies, evidence, or thresholds produces a different report hash.

---

*Compliance Drift Detector — RazorGlint Labs*
