# CDD — three-minute technical walkthrough

*Public synthetic demo. Do not imply it used real enterprise data.*

1. **0:00–0:30 · Problem.** A control can look healthy today despite earlier evidence of a breach.
2. **0:30–1:15 · Input.** In the Windows EXE select **Load example**, then **Run Compliance Drift Scan**. Show **3 claims / 13 evidence records** and explain that `compliant` labels were supplied with the synthetic data.
3. **1:15–2:00 · Recovery.** Inspect **No deployment without passing CI pipeline**: the current state is **ALIGNED**, current alignment **100%**, but its **History status = RECOVERED** after an earlier **2026-01-02** below-threshold checkpoint. The history is not rewritten to present the control as permanently healthy.
4. **2:00–2:40 · Verification.** Open **Export & Verify**. Select **Verify report** and **Verify evidence** separately. Both should say PASS for the v2 JSON artifacts. Show the browser HTML executive report; explain that this HTML document is a readable rendering, not itself a signed document.
5. **2:40–3:00 · Fit.** CDD could be evaluated as a small offline evidence-history component for internal reviews or a separately scoped OEM license. It does not automatically parse policies, collect live logs, prove source truth or certify compliance.

**Transaction:** Razorglint Labs / TCOG Collective LLC retains the IP. The demo is a licensing conversation, **not** an acquisition or assignment offer.

For exact qualified build SHA and live artifact details see [release status](RELEASE_STATUS.md).
