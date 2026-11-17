from buggy_code import add_numbers, greet, is_eligible_for_discount


def test_greet_prints_name(capsys) -> None:
    greet("Asha")

    assert capsys.readouterr().out == "Hello, Asha\n"


def test_add_numbers_uses_arithmetic(monkeypatch, capsys) -> None:
    inputs = iter(("10", "20"))
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))

    add_numbers()

    assert "The sum of 10 and 20 is 30" in capsys.readouterr().out


def test_age_60_qualifies_for_discount() -> None:
    assert is_eligible_for_discount(60) is True


def test_age_below_60_does_not_qualify() -> None:
    assert is_eligible_for_discount(59) is False