# CDD release status — 16 October 2026

**Current acceptance:** Windows x64 **v0.2 controlled-evaluation preview**. Native EXE, deterministic reporting and v2 integrity checks accepted by owner. **Unsigned.** Technical acceptance does not mean paid entitlement, cryptographic publisher signing, legal clearance, or enterprise certification.

## Exact accepted Windows binary

| Field | Verified value |
| --- | --- |
| Source commit used to build the accepted EXE | `662f84caa2ed372abde6a83245c58b466e52ce94` |
| Windows build job | [GitHub Actions 38893213993](https://github.com/RazorglintLabs/ComplianceDriftDetector/actions/runs/38893213993) — SUCCESS |
| Cross-platform qualification | [GitHub Actions 38893214199](https://github.com/RazorglintLabs/ComplianceDriftDetector/actions/runs/38893214199) — SUCCESS |
| Full test suite | **76 passed** (Windows/Linux, Python 3.11/3.12 qualification) |
| Native EXE smoke | PASS: included samples, recovered history, report and evidence verifiers, deliberate data mutation rejection |
| ZIP | `CDD_Windows_Portable_662f84caa2ed.zip` |
| ZIP SHA-256 | `8e92c16e4b651cc289af0a986c60f39860bfc476791976b5b4c71fa1c9be9b6c` |
| EXE SHA-256 | `acedbf1095ac22494bcec82dc76274c22e3e3d57f193bcc8599020459d9e5807` |
| Native walkthrough | Owner acceptance 2026-10-16, including corrected export panel and visible Open HTML / Open output folder controls |

[Owner acceptance and distribution distinctions — issue #12](https://github.com/RazorglintLabs/ComplianceDriftDetector/issues/12).

**Distribution distinction:** The current publicly tagged GitHub Release remains an earlier **v0.1.x** kit; **do not describe that release as the accepted v0.2 binary**. The v0.2 ZIP comes from the qualified build artifact or a controlled approved distribution. GitHub Actions artifacts can expire or require permissions; availability should be checked at delivery. The version number in the source package may be changed by a documentation/metadata-only follow-up commit; always distinguish the accepted binary's exact source commit from the current documentation HEAD.

## Acceptance scope

- Operator-supplied structured policy claims and classified observations only.
- Synthetic built-in sample: three claims, thirteen evidence records, 1 aligned / 2 violated, 1 unmatched undeclared-behavior finding, a recovered historical checkpoint.
- Version 2 JSON report full-content consistency check: PASS.
- Version 2 evidence package full-content consistency check: PASS.
- Old version 1 artifact verification intentionally reports reduced coverage.
- GUI visible at owner's Windows display / smart-TV layout. Portable build is not digitally code-signed.

## Distinct gates not yet complete

- Publisher identity verification and code-signing/timestamping for broad customer distribution.
- Subscription entitlement/delivery and permitted-use enforcement: not built into the EXE.
- Final third-party license/IP provenance review and customer contract diligence.
- Fully scoped enterprise/OEM integration terms and support commitments.
- New tagged GitHub Release containing the accepted signed binary: **not yet published**.

**Launch scope:** Non-confidential outreach and demos now; qualified **controlled** evaluator access under clear proprietary terms. Don't call it a signed general-availability enterprise release.

## Maintainer note

Routine documentation cleanup can move `main` forward without modifying the accepted binary. If a newer Windows EXE is shipped, require a fresh exact-commit artifact and hash receipt. Avoid claiming that an old ZIP was built from the latest documentation commit.
