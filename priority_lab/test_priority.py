import pytest

from priority_score import calculate_priority_score


@pytest.mark.parametrize(
    ("severity", "expected_score"),
    [("critical", 70), ("warning", 40), ("info", 20)],
)
def test_score_for_each_severity_is_an_int(
    severity: str,
    expected_score: int,
) -> None:
    score = calculate_priority_score(severity, 125, 100)

    assert isinstance(score, int)
    assert score == expected_score


def test_unknown_severity_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Unsupported severity"):
        calculate_priority_score("emergency", 100, 90)


def test_zero_threshold_raises_value_error() -> None:
    with pytest.raises(ValueError, match="threshold must not be zero"):
        calculate_priority_score("critical", 50, 0)


def test_metric_below_threshold_gets_no_bonus() -> None:
    assert calculate_priority_score("warning", -20, 10) == 30