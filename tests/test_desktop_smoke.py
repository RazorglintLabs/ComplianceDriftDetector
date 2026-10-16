"""Exercise the packaged path's non-GUI smoke logic from source."""
from software.desktop_smoke import run_smoke


def test_real_detector_and_export_from_bundled_example():
    result = run_smoke()
    assert result["result"] == "PASS"
    assert result["ci_history"] == "RECOVERED"
    assert result["report_verifier"] == "PASS"
    assert result["tamper_negative_test"] == "PASS"
