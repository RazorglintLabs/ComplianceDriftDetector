"""Build a reproducible, bounded CDD licensing-evaluation ZIP from a clean commit.

This is a proprietary evaluation snapshot, NOT an assignment of IP.
The archive deliberately excludes internal sale strategy, Git metadata, untracked
customer inputs and generated output reports. Requires Python stdlib + git.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"
ARCHIVE_PREFIX = "ComplianceDriftDetector/"
ZIP_DATE = (2026, 10, 16, 0, 0, 0)
ROOT_FILES = {
    "README.md", "NOTICE.md", "CLAIM_BOUNDARIES.md",
    "SELF_SERVICE_QUICKSTART.md", "LICENSE_TIERS.md",
    "TERMS_OF_SERVICE.md", "PRIVACY_POLICY.md",
    "REFUND_AND_CANCELLATION_POLICY.md",
    "START_HERE.bat", "START_UI.bat",
    "RUN_SALE_01_VALIDATION.bat", "pyproject.toml",
}
SCOPE_NOTE = """Compliance Drift Detector — proprietary local evaluation kit

Copyright (c) 2026 Razorglint Labs / TCOG Collective LLC.
All rights reserved. No open-source license or IP assignment is granted.
The rights available to an evaluator are governed by NOTICE.md and applicable
written agreements. OEM, embedding, redistribution, sublicensing, source/IP
transfer and exclusivity are NOT granted by this archive.

This archive includes only the explicitly inventoried source/demo materials.
It excludes private sales strategy, unreleased systems, Git history, customer
data, untracked inputs and generated output. This is not a production SaaS
distribution or regulatory-compliance certification.

This engine compares supplied structured claims with supplied, pre-classified
behavior evidence. It does not collect live logs or verify source truth.
Hashes are artifact-consistency checks, not authenticated provenance.
"""


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def included(name: str) -> bool:
    p = Path(name)
    if name in ROOT_FILES:
        return True
    if not p.parts:
        return False
    if p.parts[0] in {"software", "tests"}:
        return name.endswith(".py")
    if len(p.parts) >= 2 and p.parts[0] == "input_templates":
        return p.suffix in {".md", ".csv"}
    if len(p.parts) >= 3 and p.parts[:2] == ("examples", "template_packs"):
        return p.suffix in {".md", ".csv"}
    return False


def zip_entry(name: str, data: bytes) -> tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(ARCHIVE_PREFIX + name, date_time=ZIP_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o644 << 16
    return info, data


def main() -> int:
    if subprocess.run(["git", "diff", "--quiet", "HEAD", "--"],
                      cwd=ROOT).returncode:
        print("FAIL: tracked worktree differs from HEAD; build from a clean commit", file=sys.stderr)
        return 2
    commit = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).decode("utf-8").split("\0")
    names = sorted(n for n in tracked if n and included(n))
    if not names or not any(n.startswith("software/") for n in names):
        print("FAIL: no qualified source files found", file=sys.stderr)
        return 2
    files: list[dict[str, str | int]] = []
    entries: list[tuple[zipfile.ZipInfo, bytes]] = []
    for name in names:
        data = (ROOT / name).read_bytes()
        files.append({"path": name, "sha256": hashlib.sha256(data).hexdigest(),
                      "bytes": len(data)})
        entries.append(zip_entry(name, data))
    entries.append(zip_entry("PACKAGE_SCOPE.txt", SCOPE_NOTE.encode("utf-8")))
    manifest = {
        "product": "ComplianceDriftDetector",
        "transaction": "RETAIN_IP_LICENSE_EVALUATION_ONLY",
        "commit": commit,
        "tree": tree,
        "hash_algorithm": "SHA-256",
        "files": files,
        "exclusions": ["untracked input", "output", "Git history",
                       "internal sales strategy", "unrelated Razorglint IP"],
    }
    entries.append(zip_entry("PACKAGE_MANIFEST.json", (
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")))
    OUTPUT.mkdir(exist_ok=True)
    target = OUTPUT / f"CDD_LICENSE_EVAL_{commit[:12]}.zip"
    with zipfile.ZipFile(target, "w") as out:
        for info, data in sorted(entries, key=lambda x: x[0].filename):
            out.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED,
                         compresslevel=9)
    with zipfile.ZipFile(target) as chk:
        if chk.testzip() is not None:
            raise RuntimeError("Archive CRC verification failed")
        record = json.loads(chk.read(ARCHIVE_PREFIX + "PACKAGE_MANIFEST.json"))
        assert record["commit"] == commit
        for entry in record["files"]:
            content = chk.read(ARCHIVE_PREFIX + entry["path"])
            assert hashlib.sha256(content).hexdigest() == entry["sha256"]
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    sha_path = target.with_suffix(target.suffix + ".sha256")
    sha_path.write_text(f"{digest}  {target.name}\n", encoding="utf-8")
    print(f"BUILD COMMIT: {commit}")
    print(f"GIT TREE: {tree}")
    print(f"PACKAGE: {target.name}")
    print(f"SHA-256: {digest}")
    print(f"TRACKED FILES: {len(files)}; ZIP BYTES: {target.stat().st_size}")
    print(f"VERIFIED: ZIP CRC + {len(files)} embedded file hashes")
    print("IP POSTURE: RETAINED; NON-EXCLUSIVE EVALUATION / SEPARATE LICENSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
