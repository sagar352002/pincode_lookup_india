from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional


DATA_FILE = Path(__file__).resolve().parent / "data" / "india_pincode.csv"


class PincodeLookup:
    """Offline Indian pincode lookup with simple text search support."""

    def __init__(self, csv_path: Optional[Path | str] = None):
        """Load records from the packaged CSV by default."""
        path = Path(csv_path) if csv_path is not None else DATA_FILE
        self.records = self._load_records(path)

    def _load_records(self, csv_path: Path | str) -> List[Dict[str, str]]:
        records: List[Dict[str, str]] = []
        with Path(csv_path).open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                normalized = self._normalize_row(row)
                if normalized:
                    records.append(normalized)
        return records

    def _normalize_row(self, row: Dict[str, str]) -> Dict[str, str]:
        pincode = str(row.get("pincode", "")).strip()
        district = str(row.get("district", "")).strip()
        state = str(row.get("statename") or row.get("state") or "").strip()

        if not pincode:
            return {}

        return {
            "pincode": pincode,
            "district": district,
            "state": state,
            "statename": state,
            "_district": district.lower(),
            "_state": state.lower(),
        }

    def lookup_by_pincode(self, pincode: str) -> List[Dict[str, str]]:
        """Return the full location details for a given pincode."""
        target = str(pincode).strip()
        matches = [row for row in self.records if row.get("pincode") == target]
        return [
            {
                "pincode": row["pincode"],
                "district": row["district"],
                "state": row["state"],
            }
            for row in matches
        ]

    def lookup_by_pincode_with_district(self, pincode: str) -> List[Dict[str, str]]:
        """Return pincode and district for a given pincode search."""
        return [
            {"pincode": row["pincode"], "district": row["district"]}
            for row in self.lookup_by_pincode(pincode)
        ]

    def lookup_by_pincode_with_state(self, pincode: str) -> List[Dict[str, str]]:
        """Return pincode and state for a given pincode search."""
        return [
            {"pincode": row["pincode"], "state": row["state"]}
            for row in self.lookup_by_pincode(pincode)
        ]

    def lookup_by_district(self, district: str) -> List[Dict[str, str]]:
        """Return all pincodes for the matching district in a clean format."""
        target = str(district).strip().lower()
        matches = [row for row in self.records if row.get("_district") == target]
        return [
            {
                "district": row["district"],
                "pincode": row["pincode"],
                "state": row["state"],
            }
            for row in matches
        ]

    def lookup_by_district_with_state(self, district: str) -> List[Dict[str, str]]:
        """Return district and state for a given district search."""
        return [
            {"district": row["district"], "state": row["state"]}
            for row in self.lookup_by_district(district)
        ]

    def lookup_by_state(self, state: str) -> List[Dict[str, str]]:
        """Return all districts and pincodes for the given state in a structured format."""
        target = str(state).strip().lower()
        matches = [row for row in self.records if row.get("_state") == target]
        return [
            {
                "district": row["district"],
                "pincode": row["pincode"],
                "state": row["state"],
            }
            for row in matches
        ]

    def search(self, value: str) -> List[Dict[str, str]]:
        """Automatically detect whether the input is a pincode, district or state."""
        value = str(value).strip()
        if value.isdigit():
            return self.lookup_by_pincode(value)

        district_result = self.lookup_by_district(value)
        if district_result:
            return district_result

        return self.lookup_by_state(value)


__all__ = ["PincodeLookup"]