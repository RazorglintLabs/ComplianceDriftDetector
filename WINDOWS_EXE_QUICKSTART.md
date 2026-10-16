# CDD for Windows — portable native .exe (no Python required)

**Commercial posture:** Razorglint Labs / TCOG Collective LLC retains the CDD core IP. Proprietary evaluation/contract-based license; the executable is **not** a transfer, OEM sublicense, certification or unrestricted redistribution permission.

## Start

1. Download the release ZIP from the exact qualified GitHub Actions artifact or an approved evaluation distribution (the older v0.1.x tagged release is not the current Windows EXE).
2. Extract it to a normal local directory. Do **not** run the executable while it is inside a ZIP.
3. Double-click **ComplianceDriftDetector.exe**. No `.bat`, Python, terminal, cloud account, or installer is required.
4. Press **Load example**, then **Run Compliance Drift Scan**. Select the recovered CI-pipeline claim if you want to inspect recovery.
5. Select **Export & Verify**, then **Verify report** and **Verify evidence**.
6. Open HTML or **Open output folder** to see your results.

The app keeps local outputs at:
`%LOCALAPPDATA%\\RazorglintLabs\\ComplianceDriftDetector\\output`

Your own CSV files can be chosen from anywhere you are authorized to access. Bundled examples are synthetic. CDD **does not transmit customer data**. It checks data already classified and provided by the operator; it does not read raw logs or certify regulatory compliance.

## Version verification

Verify the distributed EXE checksum against the accompanying `SHA256SUMS.txt` using Windows PowerShell:
`Get-FileHash .\\ComplianceDriftDetector.exe -Algorithm SHA256`

**Build provenance:** see `BUILD_PROVENANCE.json` in the extracted package. The package was assembled on a Windows GitHub Actions runner from an exact Git commit and smoke-tested as a compiled executable; the current v0.2 build received a native owner GUI walkthrough on October 16, 2026. Details and exact checksums: [release status](docs/RELEASE_STATUS.md).

**Windows reputation warning:** The current v0.2 technical preview is **unsigned**. Windows SmartScreen or antivirus tools may warn about an unfamiliar executable. Verify its origin/checksum and follow your organization's security policy; **do not disable antivirus or bypass corporate security controls**. A signed, professionally distributed installer requires a separate code-signing/reputation process.

## Important operational notes

- The first launch of a bundled one-file executable may take several seconds while it unpacks to a temporary folder.
- The app must be allowed to create files in your own local AppData directory.
- This native Windows package is not a hosted service, continuous production monitor or source-authentication solution.
- A SHA-256 report/evidence check establishes artifact consistency only; it does not independently prove that source records are truthful.
- Report outputs contain the supplied input content; don't paste secrets, personally identifying records or unauthorized third-party data into the tool.
- If you need a managed enterprise deployment, signed binary, OEM embedding or integration, contact `razorglint.ops@protonmail.com`.
