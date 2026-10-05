# Compliance Drift Detector — Sale 01 UI Semantics Fix

**Date:** 2026-10-05  
**Scope:** Buyer-facing desktop presentation only  
**Branch:** `fix/sale01-ui-semantics`

## Trigger

During the owner walkthrough of the wired desktop UI, two presentation ambiguities were found:

1. The Results screen replaced the policy-claim `UNDECLARED` count with the count of unmatched `UNDECLARED-*` behaviour findings. Those are different concepts and must not share one number.
2. The engine's `trend` field is a first-to-last direction. A checkpoint sequence such as `100% -> 50% -> 100%` therefore returns `stable`, even though the full history contains a breach and recovery. Presenting that raw trend alone beside an earlier breach looked contradictory.

## Correction

The Sale 01 UI now:

- keeps the four policy-claim states (`ALIGNED`, `DRIFTING`, `VIOLATED`, `UNDECLARED`) as claim counts only;
- shows unmatched undeclared behaviour findings in a separate panel;
- labels state and alignment explicitly as **current** values;
- labels `first_drift_time` as **First threshold breach**;
- derives a buyer-facing **History status** from the full checkpoint sequence;
- shows `RECOVERED` when the latest checkpoint is aligned after an earlier threshold breach;
- preserves the engine's raw first-to-last `trend` and shows it separately in Evidence Detail.

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
- claim boundaries.

The correction is intentionally a presentation-semantics layer over the already-qualified deterministic engine.

## Regression targets

Tests cover:

- policy `UNDECLARED` counts cannot be overwritten by undeclared-behaviour findings;
- `100% -> 50% -> 100%` displays `RECOVERED` rather than `STABLE` as the full-history status;
- fully aligned histories preserve `STABLE`;
- active degradation preserves `DEGRADING`;
- empty histories display `NO DATA`.

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
- raw first-to-last trend remains `stable` in Evidence Detail.
