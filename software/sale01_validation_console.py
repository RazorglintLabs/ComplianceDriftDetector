"""Buyer-safe local validation console for Compliance Drift Detector Sale 01.

Runs the real pytest suite while presenting only high-level validation categories.
No detector internals or individual test names are printed.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


WIDTH = 72
ROOT = Path(__file__).resolve().parent.parent


def _line(char: str = "=") -> str:
    return char * WIDTH


def _git_short_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def main() -> int:
    print(_line())
    print("COMPLIANCE DRIFT DETECTOR — SALE 01 VALIDATION")
    print(_line())
    print(f"Build: {_git_short_sha()}")
    print("Mode : Local deterministic validation")
    print()
    print("VALIDATION SCOPE")
    print("  [01] Deterministic scoring and claim-state classification")
    print("  [02] Drift trend and history/recovery semantics")
    print("  [03] Structured CSV intake and input validation")
    print("  [04] Self-service scan and template integration")
    print("  [05] Human-readable report generation")
    print("  [06] Report seal and evidence integrity verification")
    print("  [07] Tamper detection for generated artifacts")
    print("  [08] Buyer-facing UI and report semantics")
    print()
    print(_line("-"))
    print("Running full automated regression suite...")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    match = re.search(r"(?P<count>\d+) passed in (?P<time>[0-9.]+)s", combined)

    print(_line("-"))
    if result.returncode == 0 and match:
        print(f"AUTOMATED CHECKS : {match.group('count')}/{match.group('count')} PASS")
        print(f"SUITE RESULT     : 100% PASS ({match.group('time')}s)")
        print()
        print("VALIDATION PASS")
        print("All automated Sale 01 checks completed successfully.")
        print("Local deterministic validation. No customer data is uploaded.")
        print("This validates tested software behavior; it is not regulatory certification.")
        print(_line())
        return 0

    print("AUTOMATED CHECKS : FAIL")
    print()
    print("VALIDATION FAIL")
    print("One or more automated checks did not complete successfully.")
    print("Run 'python -m pytest -q' locally for diagnostic detail.")
    print(_line())
    return result.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
