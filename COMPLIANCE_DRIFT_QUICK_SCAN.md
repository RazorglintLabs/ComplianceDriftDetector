# Compliance Drift Quick Scan

**One policy-to-system drift analysis. Tamper-evident report. Delivered in 48 hours.**

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

- Compliance leads who suspect their systems have drifted from stated policy
- CISOs preparing for SOC 2 Type II, ISO 27001, or EU AI Act readiness audits
- Engineering VPs who need proof that policy controls are actually enforced
- AI governance leads tracking whether AI system controls match documentation

If your organization has written policies but no checkpoint-based evidence they're followed — this is for you.

---

## What You Send Us

1. **Policy excerpt** — 1–10 testable policy statements (e.g., "All deployments require approval," "No persistent admin access," "AI outputs are logged")
2. **Behavior sample** — Anonymized system behavior evidence (e.g., deployment logs, access records, config snapshots, workflow outputs)
3. **Time window** — How many days/weeks of behavior data to analyze

We provide a secure intake form. No production credentials, no customer PII, no secrets required.

---

## What We Deliver

| Deliverable | Format |
|-------------|--------|
| Drift report | Markdown + JSON (tamper-evident, SHA-256 sealed) |
| Per-claim alignment analysis | Score, trend, drift state (ALIGNED / DRIFTING / VIOLATED) |
| Undeclared behavior detection | System behaviors with no matching policy |
| Evidence export | Hash-verified evidence set for independent validation |
| Verification tool | Standalone script to re-verify all outputs |

**Delivery:** 48 hours from intake acceptance.

---

## What This Proves

- Whether your stated policies match your observed system behavior
- Which specific claims are drifting and in which direction
- How alignment has changed over the sampled time window
- Whether undeclared behaviors exist (activity with no governing policy)
- That the analysis is tamper-evident and independently verifiable

## What This Does NOT Prove

- This is **not** a compliance certification
- This does **not** make you SOC 2 / ISO 27001 / EU AI Act compliant
- This does **not** guarantee detection of all policy violations
- This does **not** replace a formal audit by an accredited body
- This does **not** assess policy quality — only policy-behavior alignment

---

## Claim Boundaries

| We Say | We Don't Say |
|--------|--------------|
| "Drift detection" | "Compliance assurance" |
| "Evidence for auditors" | "Replaces auditors" |
| "Tamper-evident" | "Tamper-proof" |
| "Readiness evidence" | "Certification" |
| "Deterministic analysis" | "AI-powered" |
| "Monitors alignment" | "Guarantees compliance" |

---

## How It Works

```
You provide:  Policy claims + behavior evidence (anonymized)
                          ↓
We run:       ComplianceDriftDetector engine (deterministic, no AI, no blackbox)
                          ↓
We deliver:   Sealed drift report + evidence export + verification tool
                          ↓
You verify:   Run verify.py on any artifact — PASS or FAIL
```

---

## Monthly Licenses

Download the local kit. Run it on your machine. If you want updates, support, or commercial/client-facing use, choose a license.

See `LICENSE_TIERS.md` for full details.

No secrets, credentials, customer PII, or production access required.

## Policies

- [Terms of Service](TERMS_OF_SERVICE.md)
- [Privacy Policy](PRIVACY_POLICY.md)
- [Refund and Cancellation Policy](REFUND_AND_CANCELLATION_POLICY.md)
- [Notice](NOTICE.md)

## Next Step

Reply with "interested" or reach out directly. We'll send the intake checklist and scope the review within 24 hours.
