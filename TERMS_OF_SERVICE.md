# Terms of Service

Effective date: June 1, 2026

These Terms govern access to and use of ComplianceDriftDetector products, downloads, subscriptions, assisted reviews, reports, templates, and related materials provided by Razorglint Labs / TCOG Collective LLC.

## 1. What ComplianceDriftDetector Is

ComplianceDriftDetector is a deterministic checkpoint-based drift-detection tool. It compares structured policy claims against supplied structured behavior evidence and produces readable reports plus tamper-evident JSON artifacts.

The current release expects the operator to supply the policy assertions, evidence mapping, and `compliant` values. It does not automatically parse raw policy documents or infer compliance from raw logs.

It is not a compliance certification tool, legal service, audit service, regulatory approval service, source-data validation service, or guarantee of compliance.

## 2. Licenses

A valid subscription grants the customer a limited, revocable, non-exclusive license to use the software according to the selected tier.

Starter License: internal evaluation and internal review use.

Team License: internal team use for compliance, security, engineering, and audit-preparation workflows.

Consultant License: client-facing advisory use by consultants, vCISOs, SOC 2 consultants, ISO consultants, and GRC advisors.

Unless separately agreed in writing, customers may not resell, repackage, sublicense, host as a service, remove attribution, or claim ownership of the software, templates, detection logic, documentation, or methodology.

## 3. Reports

Reports generated from a customer's own input data belong to that customer.

The software, templates, detection logic, documentation, verification structure, and methodology remain the property of Razorglint Labs / TCOG Collective LLC.

## 4. Customer Data

Customers must not submit production credentials, secrets, API keys, customer PII, full database dumps, confidential third-party data, or anything they are not authorized to process.

Customers are responsible for anonymizing and redacting input data before using assisted review services.

## 5. Assisted Reviews, Support and Monthly Limits

Assisted reviews explain **existing CDD outputs**; they are not independent evidence validation, audit certification, legal advice, regulatory approval, or a formal compliance assessment.

**For new self-service subscriptions whose checkout or accepted agreement discloses these terms**, the monthly **combined** human-service limits are:

| Tier | Focused email requests per paid billing month | Included written interpretations (part of those requests) | Maximum combined staff working time per paid billing month |
| --- | ---: | ---: | ---: |
| Starter | 2 | 1 | 20 minutes |
| Team | 4 | 1 | 45 minutes |
| Consultant | 6 | 2 | 90 minutes |

**Report interpretations are counted against both the request and time cap**, not added on top. Limits apply per subscription account (including consultant engagements with multiple clients), not separately for each staff member, report or end client. A request addresses one focused topic; each written interpretation covers one focused question on one redacted report excerpt containing at most 10 policy claims or five pages.

Included support is **best-effort asynchronous email** during ordinary business days; there is **no guaranteed response or resolution time, availability SLA or emergency/on-call support**. Team “priority support” refers to queue order ahead of Starter as capacity permits, not a guaranteed deadline. No live calls, remote assistance, bespoke implementation, client data preparation, policy drafting or ongoing consulting is included.

Unused requests, interpretation slots and time do **not** roll over. If a limit is reached, further work is not included and is not charged automatically; any additional services require separate written quotation and approval. Staff effort spent reproducing an issue, examining redacted material and writing responses counts toward the monthly limit, which the provider will communicate when reached.

When a Starter 7-day free trial is offered, **it includes self-service use and documentation only**; human-service allowances start with the first successfully paid month unless separately agreed. Security issue reports may always be submitted under [SECURITY.md](SECURITY.md), without establishing unlimited technical support.

The precise request definitions, allowed inputs, exclusions and caps are detailed in [CDD Support Scope](docs/SUPPORT_SCOPE.md). **Existing subscriptions are not unilaterally reduced by publishing these limits**; prior accepted terms, required notice/consent, and any specific written agreement govern. Any mandatory consumer rights remain unaffected.

## 6. Availability and Updates

Active subscriptions provide access to **updates that are actually published** during the applicable license period; no specific monthly engineering, feature or template release cadence is guaranteed **for new purchases**. Features, templates, and documentation may change over time.

## 7. Payment and Subscription

Subscription fees are billed monthly through Stripe. Customers may cancel according to Stripe's subscription cancellation flow or by contacting support.

Access to updates, support, and license rights may end when a subscription is cancelled or payment fails.

## 8. No Warranty

The software and services are provided "as is." Razorglint Labs / TCOG Collective LLC does not guarantee detection of all policy violations, source-data completeness, audit acceptance, regulatory compliance, or uninterrupted operation.

## 9. Limitation of Liability

To the maximum extent permitted by law, Razorglint Labs / TCOG Collective LLC is not liable for indirect, incidental, consequential, special, or punitive damages arising from use of the software or services.

## 10. Contact

Support: razorglint.ops@protonmail.com
