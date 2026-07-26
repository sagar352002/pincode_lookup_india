import pandas as pd

from pincode_lookup_india import PincodeLookup

lookup = PincodeLookup()


def show_results(title: str, results: list[dict]) -> None:
    print(f"\n{title}")
    if results:
        print(pd.DataFrame(results))
    else:
        print("No results found")


show_results("Generic search by pincode:", lookup.search("504273"))
show_results("Generic search by district:", lookup.search("KUMURAM BHEEM ASIFABAD"))
show_results("Generic search by state:", lookup.search("TELANGANA"))