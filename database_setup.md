# Database Setup

## 1. About the Database

I used PostgreSQL to store course information from the Johns Hopkins University (JHU) SIS API: https://sis.jhu.edu/api/help. 

The database includes schools, departments, courses, terms, offerings, and prerequisite rules.

Note: The database is not fully completed yet, but it has enough data.

## 2. Requirements

- PostgreSQL
- pgAdmin 4
- Python 3

The Python libraries are listed in `requirements.txt`.

run the command: `pip install -r database/requirements.txt`

## 3. Create the Database

1. Open pgAdmin 4.
2. Connect to the PostgreSQL server.
3. Right-click Databases and select Create → Database.
4. Name the database `course_catalog_db`.
5. Click Save.

## 4. Set Up the Tables and Data

1. Open `course_catalog_db` in pgAdmin.
2. Open the Query Tool.
3. Open `schema.sql` from the database folder.
4. Run the SQL commands.

This will create the tables and relationships, but it will not import any course data.

## 5. Database Tables

The database currently has seven tables:

| Table | Description |
|---|---|
| schools | Stores school names |
| departments | Stores departments under each school |
| courses | Stores course information, such as course identifiers, titles, descriptions, and credits |
| terms | Stores academic term information |
| offerings | Stores course sections, schedules, and availability |
| prerequisite_groups | Stores groups for prerequisite rules, including AND/OR conditions |
| prerequisites | Stores the required courses and prerequisite conditions |

The tables are connected using PK and FK.

## 6. Current Data

This is the amount of data I have imported so far:

| Table | Records |
|---|---:|
| schools | 13 |
| departments | 26 |
| courses | 566 |
| terms | 8 |
| offerings | 889 |
| prerequisite_groups | 57 |
| prerequisites | 119 |

Note: It may change as I continue importing the data.

## 7. Python Scripts

I used some of Jason's JHU SIS API functions to retrieve course information. I also worked on importing the data into PostgreSQL.

**insert_courses.py**

This script retrieves course information from the JHU SIS API and inserts it into the courses table.

Note:   1. Before running the script, the department must already exist in the database.
        2. If a course already exists, the script only updates its is_repeatable value. It does not update the other course information.
        3. The school and department can be changed in the Python file to retrieve data from another department.

## 8. Environment Variables

For Python scripts that connect to PostgreSQL or the JHU API, you may need to create a `.env` file.

The file stores information such as:

API_KEY=your_jhu_api_key
DB_NAME=course_catalog_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

Note:   1. Make sure the variable names match the Python scripts.
        2. Do not upload `.env` file to GitHub because it contains private information.