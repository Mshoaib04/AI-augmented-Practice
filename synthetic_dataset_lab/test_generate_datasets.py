import csv

from generate_datasets import CARD_COLUMNS, generate_datasets


def _read_rows(path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def test_generator_creates_expected_dataset_sizes(tmp_path) -> None:
    phone_path, card_path, augmented_path = generate_datasets(tmp_path)

    phones = _read_rows(phone_path)
    cards = _read_rows(card_path)
    augmented = _read_rows(augmented_path)

    assert len(phones) == 100
    assert len(cards) == 1000
    assert len(augmented) == 2000
    assert tuple(cards[0]) == CARD_COLUMNS
    assert phones[0]["Model"]
    assert phones[0]["Country"]


def test_card_dataset_contains_only_unusable_test_values(tmp_path) -> None:
    _, card_path, augmented_path = generate_datasets(tmp_path)

    for row in _read_rows(card_path) + _read_rows(augmented_path):
        assert row["Card Number"].startswith("TEST-")
        assert row["CVV"] == "NOT-A-CVV"
        assert row["Cardholder name"].startswith(("Test User", "Augmented Test User"))