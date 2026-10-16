"""Prove frozen EXE loads bundled samples without writing into its extraction dir."""
import sys
from pathlib import Path
from software.desktop_paths import resource_root, reports_dir


def test_source_paths_match_repo(monkeypatch):
    monkeypatch.delattr(sys, "frozen", raising=False)
    assert (resource_root() / "examples" / "template_packs" / "deployment_approval" / "policy_claims.csv").is_file()
    assert reports_dir() == resource_root() / "output"


def test_frozen_resources_and_writable_output_are_distinct(monkeypatch, tmp_path):
    unpack = tmp_path / "unpacked"
    unpack.mkdir()
    writable = tmp_path / "appdata"
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(unpack), raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(writable))
    assert resource_root() == unpack
    assert reports_dir() == writable / "RazorglintLabs" / "ComplianceDriftDetector" / "output"
    assert not str(reports_dir()).startswith(str(unpack))


def test_local_appdata_fallback(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path / "fakehome"))
    assert reports_dir() == tmp_path / "fakehome" / "AppData" / "Local" / "RazorglintLabs" / "ComplianceDriftDetector" / "output"
