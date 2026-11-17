"""Generate deterministic synthetic phone and payment-shaped test data."""

import csv
from pathlib import Path
import random

CARD_COLUMNS = (
    "Card Number",
    "Cardholder name",
    "Expiry date",
    "CVV",
    "Amount",
    "Currency",
)


def _write_csv(path: Path, columns: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def generate_datasets(output_dir: Path) -> tuple[Path, Path, Path]:
    """Write 100 phone rows, 1,000 fake payment rows, and 2,000 augmented rows."""
    output_dir.mkdir(parents=True, exist_ok=True)
    randomizer = random.Random(2026)
    phone_models = ["Nova", "Orbit", "Pixel", "Summit", "Wave"]
    countries = ["India", "Canada", "Japan", "United Kingdom", "United States"]
    cameras = ["12 MP", "48 MP", "50 MP", "64 MP", "Dual 50 MP"]
    offers = ["No offer", "5% off", "10% off", "15% off"]
    phone_rows = [
        {
            "Year of launch": randomizer.randint(2018, 2026),
            "Model": f"{randomizer.choice(phone_models)} {index:03d}",
            "Price": round(randomizer.uniform(99, 1499), 2),
            "Country": randomizer.choice(countries),
            "Camera configuration": randomizer.choice(cameras),
            "Discount offer": randomizer.choice(offers),
        }
        for index in range(1, 101)
    ]
    phone_path = output_dir / "synthetic_mobile_phones.csv"
    _write_csv(
        phone_path,
        (
            "Year of launch",
            "Model",
            "Price",
            "Country",
            "Camera configuration",
            "Discount offer",
        ),
        phone_rows,
    )

    cards = [
        {
            "Card Number": f"TEST-CARD-{index:06d}",
            "Cardholder name": f"Test User {index:04d}",
            "Expiry date": f"{index % 12 + 1:02d}/{2030 + index % 6}",
            "CVV": "NOT-A-CVV",
            "Amount": round(randomizer.uniform(1, 500), 2),
            "Currency": randomizer.choice(("USD", "EUR", "GBP", "INR")),
        }
        for index in range(1, 1001)
    ]
    card_path = output_dir / "synthetic_card_data.csv"
    _write_csv(card_path, CARD_COLUMNS, cards)

    augmented = [dict(row) for row in cards]
    for index, row in enumerate(cards, start=1):
        augmented_row = dict(row)
        augmented_row["Card Number"] = f"TEST-AUGMENTED-{index:06d}"
        augmented_row["Cardholder name"] = f"Augmented Test User {index:04d}"
        augmented_row["Amount"] = round(float(row["Amount"]) * randomizer.uniform(0.8, 1.2), 2)
        augmented.append(augmented_row)

    augmented_path = output_dir / "augmented_synthetic_card_data.csv"
    _write_csv(augmented_path, CARD_COLUMNS, augmented)
    return phone_path, card_path, augmented_path


if __name__ == "__main__":
    paths = generate_datasets(Path(__file__).parent)
    for path in paths:
        print(f"Created {path.name}")