from email.utils import quote

import requests
import os
import re

BASE_URL = "https://sis.jhu.edu/api" 
API_KEY = os.getenv("API_KEY")

def main():
    #print(check_eligibility(["AS110107"], "AS110202"))

    results = get_class_by_code("PH120604", "Fall 2026")

    for c in results:
        restrictions = parse_restrictions(c.get("SectionRegRestrictions"))
        prereq = restrictions.get("Prerequisite", "None")
        print(c["Title"], prereq)


def get_class_by_code(class_code, term=None):
    """Return a list of offerings for a course number (optionally in one term)."""
    path = f"/classes/{quote(class_code)}"
    if term:
        path += f"/{quote(term)}" 

    response = requests.get(
        BASE_URL + path,
        params={"key": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()  # JSON list of course records

def check_eligibility(class_list, class_code):
    """Return True if the student is eligible to register for the class, False otherwise."""
    """Currently non functional"""
    result = get_class_by_code(class_code, "Fall 2026")


    if result[0]["SectionRegRestrictions"] == None:
        return True
    
    for c in class_list:
        if c == result[0]["SectionRegRestrictions"]:
            return True
    return False
    
def parse_restrictions(text):
    """Split a SectionRegRestrictions string into its labeled parts."""
    if not text:
        return {}

    # Split on known labels, keeping the labels themselves
    labels = ["Prerequisite", "Enrollment restrictions", "Consent Note"]
    pattern = r"(" + "|".join(labels) + r"):\s*"

    parts = re.split(pattern, text)
    # parts looks like ['', 'Prerequisite', '120.600 ', 'Enrollment restrictions', '...', 'Consent Note', '...']

    result = {}
    for i in range(1, len(parts) - 1, 2):
        label = parts[i].strip()
        value = parts[i + 1].strip()
        result[label] = value

    return result

def get_departments(school_name):
    """Return a list of departments for a given school."""
    path = f"/classes/codes/departments/{quote(school_name)}"
    response = requests.get(
        f"{BASE_URL}{path}",
        params={"key": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    main()