"""Regression tests for Sale 01 buyer-facing UI semantics."""

from types import SimpleNamespace

from software.ui_semantics import history_status, result_counts


def cp(score: float):
    return SimpleNamespace(alignment_score=score)


def analysis(scores, trend="stable"):
    return SimpleNamespace(checkpoints=[cp(score) for score in scores], trend=trend)


def test_undeclared_behaviors_do_not_overwrite_claim_state_count():
    report = SimpleNamespace(
        summary={
            "state_counts": {
                "ALIGNED": 1,
                "DRIFTING": 0,
                "VIOLATED": 2,
                "UNDECLARED": 1,
            }
        },
        undeclared_behaviors=[SimpleNamespace(), SimpleNamespace()],
    )

    claim_counts, undeclared_behavior_count = result_counts(report)

    assert claim_counts == {
        "ALIGNED": 1,
        "DRIFTING": 0,
        "VIOLATED": 2,
        "UNDECLARED": 1,
    }
    assert undeclared_behavior_count == 2


def test_recovered_history_is_not_presented_as_stable():
    item = analysis([1.0, 0.5, 1.0], trend="stable")
    assert history_status(item, alignment_threshold=0.95) == "RECOVERED"


def test_all_aligned_history_preserves_engine_trend():
    item = analysis([1.0, 0.98, 1.0], trend="stable")
    assert history_status(item, alignment_threshold=0.95) == "STABLE"


def test_active_degradation_preserves_engine_trend():
    item = analysis([1.0, 0.5], trend="degrading")
    assert history_status(item, alignment_threshold=0.95) == "DEGRADING"


def test_no_checkpoint_history_is_explicit():
    item = analysis([], trend="no_data")
    assert history_status(item, alignment_threshold=0.95) == "NO DATA"
