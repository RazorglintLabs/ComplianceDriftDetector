"""Build audit-friendly proprietary portable ZIP after executing frozen EXE smoke."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import zipfile
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DATE = (2026, 10, 16, 0, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    exe = DIST / "ComplianceDriftDetector.exe"
    smoke = DIST / "WINDOWS_EXE_SMOKE.json"
    if not exe.is_file() or not smoke.is_file():
        raise RuntimeError("Missing compiled EXE or test receipt")
    smoke_result = json.loads(smoke.read_text(encoding="utf-8"))
    if smoke_result.get("result") != "PASS":
        raise RuntimeError("Frozen EXE smoke was not PASS")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip()
    exe_hash = sha256(exe.read_bytes())
    provenance = {
        "owner": "TCOG Collective LLC / Razorglint Labs",
        "license_mode": "PROPRIETARY_RETAINED_IP_EVALUATION",
        "product": "ComplianceDriftDetector",
        "platform": "Windows x64",
        "source_commit": commit,
        "source_tree": tree,
        "build_ci_run": os.getenv("GITHUB_RUN_ID", "local-unqualified"),
        "python": sys.version,
        "pyinstaller": version("pyinstaller"),
        "executable": "ComplianceDriftDetector.exe",
        "executable_sha256": exe_hash,
        "smoke": smoke_result,
        "source_ip_transferred": False,
        "code_signed": False,
        "limits": ["Unsigned: Windows SmartScreen/reputation warning possible",
                   "No native GUI interaction verified in CI",
                   "No regulatory certification or production assurance"],
    }
    files = {
        "ComplianceDriftDetector.exe": exe.read_bytes(),
        "README_WINDOWS.txt": (ROOT / "WINDOWS_EXE_QUICKSTART.md").read_bytes(),
        "NOTICE.md": (ROOT / "NOTICE.md").read_bytes(),
        "CLAIM_BOUNDARIES.md": (ROOT / "CLAIM_BOUNDARIES.md").read_bytes(),
        "BUILD_PROVENANCE.json": (json.dumps(provenance, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        "WINDOWS_EXE_SMOKE.json": smoke.read_bytes(),
    }
    lines = ["SHA-256     FILE"]
    for filename, data in sorted(files.items()):
        lines.append(f"{sha256(data)}  {filename}")
    files["SHA256SUMS.txt"] = ("\n".join(lines) + "\n").encode("utf-8")
    target = DIST / f"CDD_Windows_Portable_{commit[:12]}.zip"
    with zipfile.ZipFile(target, "w") as z:
        for filename, data in sorted(files.items()):
            info = zipfile.ZipInfo("CDD_Windows/" + filename, DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o644 << 16
            z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for name, data in files.items():
            assert z.read("CDD_Windows/" + name) == data
    outer = sha256(target.read_bytes())
    checksum = DIST / (target.name + ".sha256")
    checksum.write_text(f"{outer}  {target.name}\n", encoding="ascii")
    print("PACKAGE:", target)
    print("ZIP SHA256:", outer)
    print("EXE SHA256:", exe_hash)
    print("SOURCE COMMIT:", commit)
    print("GIT TREE:", tree)
    print("NATIVE SMOKE:", smoke_result["result"])
    print("NOTE: UNSIGNED PORTABLE EXE; HUMAN GUI ACCEPTANCE STILL REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
