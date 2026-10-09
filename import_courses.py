import os
import requests
import psycopg
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("API_KEY")

# JHU school and department we want to import (can be changed)
school = "Whiting School of Engineering"
department = "EN Computer Science"

# JHU SIS API endpoint
url = f"https://sis.jhu.edu/api/classes/{school}/{department}"

params = {
    "key": api_key
}

# Request course data from JHU API
response = requests.get(url, params=params)

print("Status:", response.status_code)

# Stop the program if the API request failed
response.raise_for_status()

data = response.json()

print("Number of records:", len(data))

# Filter Computer Science records
# so filter the results using the Department field.
cs_records = []

for course in data:
    if course.get("Department") == department:
        cs_records.append(course)

print("Computer Science records:", len(cs_records))

# Connect to PostgreSQL
conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

print("\nConnected to PostgreSQL")

# Find the department_id for EN Computer Science
# We look up the department_id
cursor.execute(
    """
    SELECT department_id
    FROM departments
    WHERE department_name = %s
    """,
    (department,)
)

result = cursor.fetchone()

if result is None:
    print("Department not found in the database.")
    cursor.close()
    conn.close()
    exit()

department_id = result[0]

print("Computer Science department ID:", department_id)

# Insert courses
for course in cs_records:
    course_identifier = course.get("OfferingName")
    course_prefix = course.get("CoursePrefix")
    course_title = course.get("Title")
    course_credits = course.get("Credits")
    course_level = course.get("Level")
    repeatable = course.get("Repeatable")

    # Clean credit values from the JHU API
    # Some courses have no credit value:
    # "" -> NULL
    #
    # Some courses have a credit range:
    # "1.00 - 3.00" -> NULL
    if not course_credits:
        course_credits = None
    elif " - " in course_credits:
        course_credits = None

    # Clean Repeatable value
    # Any missing or unexpected value is stored as NULL.
    if repeatable == "Y":
        is_repeatable = True
    elif repeatable == "N":
        is_repeatable = False
    else:
        is_repeatable = None

    # Insert or update course
    cursor.execute(
        """
        INSERT INTO courses (
            department_id,
            course_identifier,
            course_prefix,
            course_title,
            credits,
            course_level,
            is_repeatable
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (course_identifier) DO UPDATE
        SET is_repeatable = COALESCE(
            EXCLUDED.is_repeatable,
            courses.is_repeatable
        )
        """,
        (
            department_id,
            course_identifier,
            course_prefix,
            course_title,
            course_credits,
            course_level,
            is_repeatable
        )
    )

# Save all inserted courses
conn.commit()

# Close the database connection
cursor.close()
conn.close()

print("Courses Inserted")