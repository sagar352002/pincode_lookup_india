"""Lookup helpers for Indian pincodes."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Dict


DATA_FILE = Path(__file__).resolve().parent / "data" / "india_pincode.csv"


def lookup_by_pincode(pincode: str) -> List[Dict[str, str]]:
    """Return matching records for a pincode."""
    if not pincode:
        return []

    matches: List[Dict[str, str]] = []
    with DATA_FILE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row.get("pincode") == str(pincode):
                matches.append(row)

    return matches
