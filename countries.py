"""
Country codes and names for filtering
"""

COUNTRIES = {
    "america": {
        "US": "United States",
        "CA": "Canada",
        "MX": "Mexico",
        "BR": "Brazil",
        "AR": "Argentina",
        "CL": "Chile",
        "CO": "Colombia",
    },
    "europe": {
        "GB": "United Kingdom",
        "DE": "Germany",
        "FR": "France",
        "ES": "Spain",
        "IT": "Italy",
        "NL": "Netherlands",
        "BE": "Belgium",
        "PT": "Portugal",
        "SE": "Sweden",
        "NO": "Norway",
        "DK": "Denmark",
        "FI": "Finland",
        "PL": "Poland",
        "CZ": "Czech Republic",
        "AT": "Austria",
        "CH": "Switzerland",
        "IE": "Ireland",
    },
    "asia": {
        "SG": "Singapore",
        "MY": "Malaysia",
        "TH": "Thailand",
        "PH": "Philippines",
        "ID": "Indonesia",
        "VN": "Vietnam",
        "IN": "India",
        "CN": "China",
        "JP": "Japan",
        "KR": "South Korea",
        "TW": "Taiwan",
        "HK": "Hong Kong",
        "AE": "UAE",
        "SA": "Saudi Arabia",
    }
}

def get_countries_by_region(region: str):
    """Get all countries for a specific region"""
    return COUNTRIES.get(region, {})

def get_all_countries():
    """Get all countries flattened"""
    all_countries = {}
    for region_countries in COUNTRIES.values():
        all_countries.update(region_countries)
    return all_countries
