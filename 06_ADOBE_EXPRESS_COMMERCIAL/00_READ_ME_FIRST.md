# Compliance Drift Detector — Adobe Express Commercial Pack

Purpose: create one clean buyer-facing 16:9 commercial from already-approved CDD Sale 01 material, then add the final voice track last.

## Build target
- Canvas: 1920 × 1080, 16:9
- Target runtime: 52 seconds
- Editing style: restrained B2B product film, not social-media hypercut
- Motion: slow push-ins, gentle pans, short fades only
- Voice: add after the visual skeleton is locked
- Music: optional, low and subordinate to narration

## Import order
Adobe should receive the final cleaned PNGs using the filenames below. Import them in numeric order:

1. `SCENE_01_NEW_SCAN.png`
2. `SCENE_02_SCAN_RESULTS.png`
3. `SCENE_03_HTML_REPORT_OVERVIEW.png`
4. `SCENE_04_HTML_REPORT_DETAIL.png`
5. `SCENE_05_VERIFY_REPORT_PASS.png`
6. `SCENE_06_VERIFY_EVIDENCE_PASS.png`
7. `SCENE_07_FULL_SUITE_VALIDATION.png`

Two scenes are built directly in Adobe and do not require PNG assets:
- `SCENE_00_OPENING_CARD`
- `SCENE_08_END_CARD`

## Scene order
Follow `01_TIMELINE.csv` exactly for the first cut. It is intentionally simple so the narration can be added without having to rebuild timing.

## Asset rules
- Use only cleaned captures with browser/taskbar chrome removed where possible.
- Keep every source image at 1920 × 1080 where practical.
- Do not crop away status labels, PASS results, report headings, or validation boundaries.
- Do not expose source code, test names, private implementation details, secrets, tokens, or customer data.
- The validation console is safe for buyer/demo use by design and should be used instead of raw pytest output.

## Product-claim boundary
The commercial may say CDD compares structured policy claims with supplied behavior evidence, detects drift/violations/undeclared behavior, exports reports/evidence, and independently verifies generated artifact integrity.

Do not present CDD as regulatory certification, an accredited audit, or proof that supplied source data is truthful or complete.

## First-cut rule
Build the full visual timeline first. Do not spend time on advanced transitions, music, captions, or voice until the silent 52-second sequence feels clean end-to-end.
