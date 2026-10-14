from email.utils import quote

import requests
import os
import re

BASE_URL = "https://sis.jhu.edu/api" 
API_KEY = os.getenv("API_KEY")

"""
get_class_by_code: Fetches a list of offerings for a course number, optionally filtered by term.
inputs: class_code (str): The course number to fetch offerings for.
        term (str, optional): The term to filter offerings by. Defaults to None.
        
outputs: A JSON list of course records.
"""
def get_class_by_code(class_code, term=None):
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

"""
get_departments: Fetches a list of departments for a given school.
inputs: school_name (str): The name of the school to fetch departments for.

outputs: A JSON list of department records.
"""
def get_departments(school_name):
    path = f"/classes/codes/departments/{quote(school_name)}"
    response = requests.get(
        f"{BASE_URL}{path}",
        params={"key": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

"""
parse_class: Fetches the requested information for a given class code.
inputs: class_code (str): The course number to fetch offerings for.
        info (str): The specific information to retrieve from the course record.
        
        outputs: The requested information for the given class code."""

def parse_class(class_code, info):
    results = get_class_by_code(class_code, "Fall 2026")

    return results[0][info]

