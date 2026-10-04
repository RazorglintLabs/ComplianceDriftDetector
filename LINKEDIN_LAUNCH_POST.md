# LinkedIn Launch Post — ComplianceDriftDetector v0.1.1

---

## Post

Your policy says every production deployment requires approval.

Your operating evidence says:
"Mostly."

That gap is where drift becomes visible.

Policies stay written down while workflows, access patterns, and operating practices change over time.

ComplianceDriftDetector was built for one narrow job: compare structured policy claims against supplied behavior evidence across dated checkpoints and show where alignment is holding, drifting, violated, or missing mapped evidence.

We released v0.1.1 — a self-service local kit that generates readable drift reports plus tamper-evident JSON artifacts.

No cloud service required.
No production credentials required.
No customer PII or secrets required by the workflow.
No AI or blackbox scoring.

Download the ZIP, run it locally, open the HTML report.

It classifies policy claims as:

ALIGNED — supplied evidence meets the configured alignment threshold
DRIFTING — latest alignment is below the alignment threshold but above the violation threshold
VIOLATED — latest alignment is below the violation threshold
UNDECLARED — no mapped evidence was supplied for that claim

It also surfaces specially marked undeclared behavior references that have no matching policy claim.

This is not a compliance certificate.
It does not make you SOC 2, ISO 27001, or EU AI Act compliant.
It does not automatically parse raw policy documents or infer compliance from raw logs.

It does one narrower thing:

It measures how supplied structured evidence compares with declared policy across checkpoints.

Download the local kit. Run it on your machine. If you want updates, support, or commercial/client-facing use, choose a license.

Starter — $49/mo, 7-day free trial
Team — $149/mo
Consultant — $299/mo

If you are a CISO, compliance lead, engineering lead, or AI governance lead and want to see what checkpoint-based drift analysis looks like on sample or anonymized data, DM me "drift".

---

`#compliance` `#governance` `#driftdetection` `#SOC2` `#ISO27001` `#EUAIAct` `#tamperevident` `#infosec`

---

## First Comment

Self-service release:
https://github.com/RazorglintLabs/ComplianceDriftDetector/releases/tag/v0.1.1-self-service

Subscribe:
- Starter ($49/mo, 7-day trial): https://buy.stripe.com/cNi5kxghbd3CbdKfKn1ZS08
- Team ($149/mo): https://buy.stripe.com/fZubIVe934x61DadCf1ZS07
- Consultant ($299/mo): https://buy.stripe.com/14AdR39SNgfOepW8hV1ZS06

License tiers and policies are in the repo README.
