@echo off
echo ============================================================
echo   ComplianceDriftDetector — Local Drift Scan
echo   No data leaves your machine.
echo ============================================================
echo.

if exist "input\policy_claims.csv" (
    echo   Found input/ files. Running scan...
    echo.
    python software\run_scan.py
) else (
    echo   No input/ directory with CSV files found.
    echo.
    echo   To scan your own data:
    echo     1. Create an input\ folder
    echo     2. Copy policy_claims.csv and behavior_evidence.csv into it
    echo     3. Run this file again
    echo.
    echo   See input_templates\ for the required format.
    echo   See examples\template_packs\ for ready-to-use examples.
    echo.
    echo   Running demo scenario instead...
    echo.
    python software\run_scan.py
)

echo.
pause
