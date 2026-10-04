# Compliance Drift Quick Scan

**One policy-to-system drift analysis. Local, deterministic, tamper-evident artifacts.**

---

## Pricing

| Tier | Price | Scope |
|------|-------|-------|
| **Starter License** | $49/mo | Self-service local kit, updates, templates, limited async support |
| **Team License** | $149/mo | Internal team use, 1 assisted report interpretation/month |
| **Consultant License** | $299/mo | Client-facing advisory, 2 interpretations/month, Razorglint attribution required |

- Starter — [$49/mo, 7-day free trial](https://buy.stripe.com/cNi5kxghbd3CbdKfKn1ZS08)
- Team — [$149/mo](https://buy.stripe.com/fZubIVe934x61DadCf1ZS07)
- Consultant — [$299/mo](https://buy.stripe.com/14AdR39SNgfOepW8hV1ZS06)

---

## Who This Is For

- Compliance leads who want structured evidence of policy-behavior drift
- CISOs preparing for SOC 2, ISO 27001, or other readiness reviews
- Engineering leaders comparing stated controls with supplied operating evidence
- AI governance leads tracking whether documented controls still match supplied evidence

If your organization has written policies but lacks checkpoint-based alignment evidence, this is the problem the detector is designed to measure.

---

## What You Provide

1. **Policy claims** — 1–10 structured, testable assertions (for example: "All deployments require approval")
2. **Behavior evidence** — dated, anonymized observations mapped to those claims
3. **Compliance flag** — a supplied true/false value for each evidence record
4. **Time window** — the dated checkpoints you want compared

No production credentials, customer PII, or secrets are required by the workflow.

The current release does **not** automatically parse natural-language policies or infer compliance from raw logs.

---

## What It Produces

| Deliverable | Format |
|-------------|--------|
| Drift report | Markdown + JSON + HTML |
| Per-claim analysis | Score, trend, drift state (ALIGNED / DRIFTING / VIOLATED / UNDECLARED) |
| Undeclared behavior findings | Unmatched `UNDECLARED-` behavior references |
| Evidence export | Complete policy/evidence set with per-item and aggregate hashes |
| Verification tool | PASS/FAIL checks for supported JSON artifacts |

---

## What The Output Shows

- Whether supplied evidence meets the configured alignment threshold for each claim
- Which claims are drifting and in which direction across supplied checkpoints
- The earliest supplied checkpoint where alignment falls below the configured threshold
- Whether undeclared behavior references are present
- Whether supported JSON artifacts pass the included consistency/hash checks

## What It Does NOT Establish

- It is **not** a compliance certification
- It does **not** make an organization compliant with any standard or regulation
- It does **not** guarantee detection of all policy violations
- It does **not** replace a formal audit or accredited assessment
- It does **not** validate the truth, completeness, or provenance of supplied source data
- It does **not** assess policy quality; it measures alignment against supplied structured claims/evidence

---

## Claim Boundaries

| We Say | We Don't Say |
|--------|--------------|
| "Drift detection" | "Compliance assurance" |
| "Evidence for audit preparation" | "Replaces auditors" |
| "Tamper-evident" | "Tamper-proof" |
| "Readiness evidence" | "Certification" |
| "Deterministic analysis" | "AI-powered" |
| "Checkpoint-based" | "Real-time" |
| "Supplied behavior evidence" | "Automatically observed production behavior" |

---

## How It Works

```text
You provide:  structured policy claims + behavior evidence
                          ↓
Tool runs:    checkpoint measurement + visible threshold classification
                          ↓
Tool writes:  drift report + evidence export
                          ↓
You verify:   report seal/consistency + all exported item/aggregate hashes
```

---

## Monthly Licenses

Download the local kit. Run it on your machine. If you want updates, support, or commercial/client-facing use, choose a license.

See `LICENSE_TIERS.md` for full details.

## Policies

- [Terms of Service](TERMS_OF_SERVICE.md)
- [Privacy Policy](PRIVACY_POLICY.md)
- [Refund and Cancellation Policy](REFUND_AND_CANCELLATION_POLICY.md)
- [Notice](NOTICE.md)

## Next Step

Use the self-service templates in the repository or request the intake checklist for an assisted review.
