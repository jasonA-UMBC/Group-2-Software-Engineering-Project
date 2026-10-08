from email.utils import quote

import requests
import os
import re

BASE_URL = "https://sis.jhu.edu/api" 
API_KEY = os.getenv("API_KEY")

def main():
    #print(check_eligibility(["AS110107"], "AS110202"))

    print(parse_class("AS110107", "Title"))

    #for c in results:
        #restrictions = parse_restrictions(c.get("SectionRegRestrictions"))
        #prereq = restrictions.get("Prerequisite", "None")
        #print(c["Title"], prereq)


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
    
    for c in class_list:
        if c == ["SectionRegRestrictions"]:
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

def parse_class(class_code, info):
    """Return the requested information for a given class code."""
    results = get_class_by_code(class_code, "Fall 2026")

    return results[0][info]

if __name__ == "__main__":
    main()

""" The entire printout of a class object for AS110107 in Fall 2026 is as follows: 
{'TermStartDate': '8/31/2026 12:00:00 AM', 'SchoolName': 'Krieger School of Arts and Sciences', 
 'CoursePrefix': 'AS', 'Term': 'Fall 2026', 'Term_IDR': 'Fall 2026', 'OfferingName': 'AS.110.107', 
 'SectionName': '01', 'Title': 'Calculus II (For Biological and Social Science)', 
 'Credits': '4.00', 'Department': 'AS Mathematics', 'Level': 'Lower Level Undergraduate', 
 'Status': 'Closed', 'DOW': '23', 'DOWSort': '01^10:00:00', 'TimeOfDay': 'Other', 'SubDepartment': '', 
 'SectionRegRestrictions': '', 'SeatsAvailable': '3/30', 'MaxSeats': '30', 'OpenSeats': '3', 
 'Waitlisted': '0', 'IsWritingIntensive': 'No', 'AllDepartments': 'AS Mathematics', 
 'Instructors': 'L. Doan', 'InstructorsFullName': 'Doan, Lam', 'Location': 'Homewood Campus', 
 'Building': 'Hodson, Krieger', 'HasBio': None, 'Meetings': 'MWF 10:00AM - 10:50AM, T 3:00PM - 3:50PM', 
 'Areas': 'Q, Science and Data, Writing and Communication', 'InstructionMethod': 'In-person, In-person', 'SectionCoRequisites': '', 
 'SectionCoReqNotes': '', 'SSS_SectionsID': '868570', 'Term_JSS': 'Fall 2026', 'Repeatable': 'N', 'SectionDetails': None}
 """