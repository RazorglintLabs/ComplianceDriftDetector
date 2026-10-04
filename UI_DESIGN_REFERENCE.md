# Compliance Drift Detector — Frozen Sale 01 UI Reference

**Status:** Frozen for Sale 01  
**Purpose:** Buyer-facing local desktop interaction layer over the existing deterministic engine.  
**Design authority:** Figma file `ComplianceDriftDetector — Sale UI`  
**Figma:** https://www.figma.com/design/0xFZtfAvEbZ0Qenz0rLcMM

---

## Boundary

The UI is a thin presentation and interaction shell.

It does **not** replace, reinterpret, or duplicate the detector's classification logic. The existing Python engine, report renderers, and verifier remain the source of truth.

The local desktop implementation is `software/ui_app.py`.

Run it with:

```bash
python software/ui_app.py
```

On Windows, double-click:

```text
START_UI.bat
```

The CLI remains independently runnable with `python software/run_scan.py`.

---

## Frozen flow

1. **New Scan**
   - choose `policy_claims.csv`
   - choose `behavior_evidence.csv`
   - optionally load the bundled deployment-approval example
   - run the deterministic scan

2. **Results**
   - show `ALIGNED`, `DRIFTING`, `VIOLATED`, and `UNDECLARED` counts
   - list policy results with alignment, trend, and earliest observed drift checkpoint
   - open a result for evidence detail

3. **Evidence Detail**
   - show state, alignment, reason, trend, earliest observed drift checkpoint, and violation-checkpoint count
   - show the checkpoint trail with evidence counts and evidence hashes

4. **Export & Verify**
   - expose the existing HTML / Markdown / JSON / evidence outputs
   - open the generated HTML report or output folder
   - independently verify `drift_report.json`
   - independently verify `drift_evidence.json`

---

## Frozen visual language

The final Sale 01 design uses the first screen as the color authority.

| Role | Color |
|---|---|
| Main background | `#252629` |
| Header | `#23272F` |
| Primary panel | `#282C34` |
| Secondary panel | `#252A31` |
| Warm ivory text | `#E2D3B7` |
| Muted text | `#B8AC99` |
| Restrained warm border | `#C8A66A` |
| Verification / primary green | `#176B4F` |
| Aligned | `#2E7D5B` |
| Drifting | `#A96E18` |
| Violated | `#934A4A` |
| Undeclared | `#675D83` |

No glow, blur, glass, animation, or decorative effect is required. The interface should remain restrained, dark, legible, and immediately understandable.

---

## Product-language rules

Keep these phrases visible where appropriate:

- `LOCAL-FIRST • No data uploaded`
- `Runs locally • No cloud • Deterministic engine • Independent verifier`
- `Checkpoint-based analysis only. This tool detects policy-behaviour drift; it does not certify compliance.`
- `Verification checks artifact integrity. It does not certify regulatory compliance or audit acceptance.`

Do not describe the UI as real-time monitoring, continuous live monitoring, compliance certification, regulatory approval, or an enterprise SaaS platform.

---

## Stop rule

For Sale 01, the UI is complete when the four-screen flow remains easy to understand and operates through the existing engine and verifier.

Do not add accounts, RBAC, billing, cloud storage, integrations, AI assistants, dashboards, multi-tenancy, or other SaaS surface area unless a buyer separately requests and funds it.
