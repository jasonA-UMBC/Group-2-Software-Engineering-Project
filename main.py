from email.utils import quote

import requests
import os

BASE_URL = "https://sis.jhu.edu/api" 
API_KEY = os.getenv("API_KEY")

def main():
    results = get_class_by_code("AS020", "Fall 2026")

    for c in results:
        print(c["OfferingName"], c["Title"], c["Term"], c["Status"], c["SeatsAvailable"])

def get_class_by_code(class_code, term=None):
    """Return a list of offerings for a course number (optionally in one term)."""
    path = f"/classes/{quote(class_code)}"
    if term:
        path += f"/{quote(term)}"  # e.g. "Fall 2026" -> "Fall%202026"

    response = requests.get(
        BASE_URL + path,
        params={"key": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()  # JSON list of course records

def check_eligibility(class_list, class_code):
    for class_info in class_list:
        if class_info['code'] == class_code:
            return class_info['is_eligible']
    return False

def get_schools():
    response = requests.get(
        f"{BASE_URL}/classes",
        params={"key": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    main()