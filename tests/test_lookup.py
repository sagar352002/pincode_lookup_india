from pincode_lookup_india import PincodeLookup
from pincode_lookup_india.lookup import lookup_by_pincode


def test_lookup_by_pincode_returns_matching_rows():
    result = lookup_by_pincode("504273")

    assert result
    assert result[0]["pincode"] == "504273"
    assert result[0]["statename"] == "TELANGANA"


def test_lookup_returns_professional_summary_for_pincode():
    lookup = PincodeLookup()
    result = lookup.lookup_by_pincode("504273")

    assert result[0]["pincode"] == "504273"
    assert result[0]["district"] == "KUMURAM BHEEM ASIFABAD"
    assert result[0]["state"] == "TELANGANA"


def test_lookup_by_unknown_pincode_returns_empty_list():
    assert lookup_by_pincode("000000") == []


def test_package_exports_pincode_lookup_class():
    lookup = PincodeLookup()
    assert lookup.lookup_by_pincode("504273")[0]["pincode"] == "504273"


def test_district_lookup_returns_all_pincodes_for_district():
    lookup = PincodeLookup()
    result = lookup.lookup_by_district("KUMURAM BHEEM ASIFABAD")

    assert isinstance(result, list)
    assert len(result) > 1
    assert all(item["district"] == "KUMURAM BHEEM ASIFABAD" for item in result)


def test_combined_lookup_helpers_work():
    lookup = PincodeLookup()

    assert lookup.lookup_by_pincode_with_state("504273")[0]["state"] == "TELANGANA"
    assert lookup.lookup_by_district_with_state("KUMURAM BHEEM ASIFABAD")[0]["state"] == "TELANGANA"
    assert lookup.lookup_by_pincode_with_district("504273")[0]["district"] == "KUMURAM BHEEM ASIFABAD"
