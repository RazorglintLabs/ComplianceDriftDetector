# Compliance Drift Detector — Sale 01 Presentation Semantics Fix

**Date:** 2026-10-05  
**Scope:** Buyer-facing desktop and human-readable report presentation only  
**Branch:** `fix/sale01-ui-semantics`

## Trigger

During the owner walkthrough of the wired desktop UI, two presentation ambiguities were found:

1. The Results screen replaced the policy-claim `UNDECLARED` count with the count of unmatched `UNDECLARED-*` behaviour findings. Those are different concepts and must not share one number.
2. The engine's `trend` field is a first-to-last direction. A checkpoint sequence such as `100% -> 50% -> 100%` therefore returns `stable`, even though the full history contains a breach and recovery. Presenting that raw trend alone beside an earlier breach looked contradictory.

Owner validation of the corrected desktop UI then exposed the same second ambiguity in the generated HTML report: the recovered claim still showed the raw `stable` trend without a full-history recovery label. The human-readable export surfaces therefore needed the same semantic clarification.

## Correction

The Sale 01 presentation layer now:

- keeps the four policy-claim states (`ALIGNED`, `DRIFTING`, `VIOLATED`, `UNDECLARED`) as claim counts only;
- shows unmatched undeclared behaviour findings separately;
- labels state and alignment explicitly as **current** values;
- labels `first_drift_time` as **First Threshold Breach**;
- derives a buyer-facing **History Status** from the full checkpoint sequence;
- shows `RECOVERED` when the latest checkpoint is aligned after an earlier threshold breach;
- preserves the engine's raw first-to-last `trend` and labels it explicitly where surfaced;
- applies the same distinction to the desktop UI, HTML report, and Markdown report;
- renames the HTML summary card from generic `Violations` to **Violated Claims**.

## Boundaries

This correction does **not** change:

- policy/evidence ingestion;
- alignment scores;
- drift classifications;
- checkpoint generation;
- report sealing;
- evidence hashing;
- verifier behavior;
- JSON schema;
- machine-readable `trend` values;
- claim boundaries.

The correction is intentionally a presentation-semantics layer over the already-qualified deterministic engine.

## Regression targets

Tests cover:

- policy `UNDECLARED` counts cannot be overwritten by undeclared-behaviour findings;
- `100% -> 50% -> 100%` displays `RECOVERED` rather than `STABLE` as the full-history status;
- fully aligned histories preserve `STABLE`;
- active degradation preserves `DEGRADING`;
- empty histories display `NO DATA`;
- HTML exports show current state/alignment, history status, and first threshold breach;
- Markdown exports separate full-history status from the raw first-to-last engine trend;
- the underlying engine still returns raw `trend="stable"` and the original `first_drift_time` for the recovered test case.

## Expected bundled-example facing

For the deployment-approval example, the Results screen should show:

- `1` ALIGNED claim;
- `0` DRIFTING claims;
- `2` VIOLATED claims;
- `0` UNDECLARED/no-evidence claims;
- **1 undeclared behaviour finding** separately.

The CI-pipeline claim should show:

- Current state: `ALIGNED`;
- Current alignment: `100%`;
- History status: `RECOVERED`;
- First threshold breach: `2026-01-02`;
- raw first-to-last trend remains `stable` and is explicitly identified as such where shown.

The HTML report should likewise show `RECOVERED` for this claim rather than exposing `stable` as the only historical descriptor.
