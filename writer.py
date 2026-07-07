"""Output helpers for parsed listing data."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from models import OCTGListing


CSV_FIELDS = [
    "company_name",
    "pipe_grade",
    "diameter",
    "wall_thickness",
    "length",
    "quantity",
    "price",
    "location",
    "contact_email",
    "source_url",
]


def write_listings_csv(listings: Iterable[OCTGListing], path: str) -> Path:
    """Write normalized listing rows to a local CSV file."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for listing in listings:
            writer.writerow(listing.model_dump(mode="json"))

    return output_path
