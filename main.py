from email.utils import quote

import requests
import os
import re

BASE_URL = "https://sis.jhu.edu/api" 
API_KEY = os.getenv("API_KEY")

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

def parse_class(class_code, info):
    """Return the requested information for a given class code."""
    results = get_class_by_code(class_code, "Fall 2026")

    return results[0][info]

