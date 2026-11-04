# Team A Updated Database Documentation

## 1. Overview

Team A is responsible for the course catalog, prerequisites, course offerings, and degree requirement data for our CMSC 447 project.

We use PostgreSQL to store course information retrieved from the Johns Hopkins University (JHU) SIS API. The database is also hosted on Supabase, so other teams can access the data for their parts of the project.

This document summarizes what we completed in Sprint 1, the updates made during Sprint 2, and what we plan to work on in Sprint 3 in the database.

## 2. Sprint 1 Summary

During Sprint 1, we created the original database structure with 7 tables:

1. `schools`
2. `departments`
3. `courses`
4. `terms`
5. `offerings`
6. `prerequisite_groups`
7. `prerequisites`

These tables store course information, academic terms, course offerings, and prerequisite relationships.

We also worked on importing course information from the JHU SIS API into our local PostgreSQL database.

For prerequisites, we created two tables to support AND/OR conditions and nested prerequisite groups. This allows us to represent more complicated prerequisite requirements, such as `(Course A AND Course B) OR Course C`.

After setting up the local database, we migrated the 7 tables and their data to Supabase.

At the time of the original Sprint 1 documentation (October 9), the database contained:

- 13 schools
- 26 departments
- 566 courses
- 8 terms
- 889 offerings
- 57 prerequisite groups
- 119 prerequisites

These numbers are from the original Sprint 1 snapshot, not the current database totals.

For more information about the original database setup, tables, prerequisite examples, and Supabase migration, please refer to:

- `database_setup.md` — Local PostgreSQL setup and data import
- `supabase_setup.md` — Supabase setup, prerequisite structure, and database access

The following sections focus on the changes made during Sprint 2.

## 3. Sprint 2 Updates

### 3.1 Degree Requirement Schema

During Sprint 2, we added 4 new tables to support degree requirements. We started with the Johns Hopkins Computer Science B.S. program, but the same database structure can also be used for other majors, such as Mathematics and Physics.

The new tables are connected to our existing `departments` and `courses` tables, so we can reuse the course information we already imported instead of storing the same data again.

**New Tables**

1. `degree_programs`

   Stores information about each degree program, such as the program name, degree type, department, catalog year, and total credits required.

2. `degree_requirement_groups`

   Organizes degree requirements into categories, such as CS Core, Mathematics, Basic Sciences, and Electives. It also supports nested groups using `parent_group_id`.

3. `degree_requirements`

   Stores the requirements students need to complete, such as a minimum number of courses or credits.

4. `degree_requirement_courses`

   Connects degree requirements to the courses in our existing `courses` table. A requirement can include multiple eligible courses, and a course can be connected to multiple requirements.

**How It Works**

The system starts with a degree program, finds its requirement groups, checks the requirements in each group, and then finds the courses that can satisfy those requirements.

For example:

`Computer Science B.S. → Mathematics → Minimum 16 credits → Eligible courses`

If a student has completed 13 eligible mathematics credits, the system can determine that the student still needs 3 more credits.

Some degree requirements may also involve different course combinations, similar to the AND/OR prerequisite structure we created during Sprint 1.

**Implementation**

All 4 tables were created and tested in our local PostgreSQL database before being migrated to Supabase.

We also verified the table relationships and foreign key constraints to make sure the new tables connect correctly to the existing database.

The implementation and migration were completed during Sprint 2.

### 3.2 CS B.S. Sample Data

After creating the 4 new tables, we imported sample degree requirement data for the Johns Hopkins Computer Science B.S. program to test how the tables work together.

We added a total of 33 records:

| Table | Records |
|---|---:|
| `degree_programs` | 1 |
| `degree_requirement_groups` | 12 |
| `degree_requirements` | 10 |
| `degree_requirement_courses` | 10 |
| **Total** | **33** |

The sample data includes the Computer Science B.S. program, requirement groups, and course mappings.

For example, the program can have different requirement groups, such as CS Core, Mathematics, Basic Sciences, and Electives. Each group can contain requirements that specify how many courses or credits a student needs to complete.

The `degree_requirement_courses` table connects these requirements to the courses already stored in our database.

**Testing and Verification**

After importing the sample data, we checked the relationships between the 4 new tables and the existing tables.

The sample data was also migrated to Supabase.

**Note:** These records are sample data used to test the database structure. They do not represent the complete graduation requirements for the Computer Science B.S. program. More requirements can be added later.

### 3.3 Course Description Updates

During Sprint 2, we also worked on adding course descriptions from the JHU SIS API to our existing `courses` table.

We imported a total of **473 course descriptions** into Supabase from the following departments:

- EN Computer Science
- AS Mathematics
- AS Physics & Astronomy

The descriptions provide more information about what each course covers. We updated the existing `course_description` column instead of creating a new table.

**Note:** Not all courses in our database have descriptions yet. Some descriptions may be missing from the JHU SIS API, and additional descriptions can be imported later if needed.

### 3.4 Database Verification and Security

After implementing the new degree requirement tables and importing the sample data, we performed several checks to make sure the database was working correctly.

**Database Verification**

- Verified the relationships between the new tables and existing tables.
- All foreign key and database integrity checks passed.
- Synchronized the ID sequences for all 4 new tables to prevent conflicts when inserting new records.
- Confirmed that the new tables and sample data were successfully migrated to Supabase.

## 4. Current Database Status

At the end of Sprint 2, our database contains 11 tables: the original 7 tables from Sprint 1 and the 4 new degree requirement tables added during Sprint 2.

The database is available in Supabase.

**Completed Work**

- Created and migrated all 11 tables to Supabase.
- Imported course information and offerings from multiple JHU departments.
- Added 33 sample records for the Computer Science B.S. degree requirements.
- Imported 473 course descriptions.
- Verified the database relationships and foreign key constraints.
- Synchronized the ID sequences for the 4 new tables.

**Remaining Items**

- Update minimum-grade values to follow the team's agreed A, B, C, D, F system.
- Add or update course and degree requirement data if needed.

**Note:** The database contains partial JHU course and degree requirement data. It is ready for continued development and integration, but it does not yet include all courses or complete degree requirements.

## 5. Sprint 3 Plan

During Sprint 3, we plan to focus on improving the existing database, adding user management, reviewing the remaining requirements, and supporting integration with Teams B and C.

**1. Create User Table**

We plan to add a new table to store user information and support 4 types of users:

- **Student (Normal):** Students who follow the regular degree requirements.
- **Student (Transfer):** Students who have transferred credits from another institution and may have different completed course records.
- **Admin:** Users who can manage and update course information, degree requirements, and other database records.
- **Advisor/Counselor:** Users who can review student progress and help students plan their courses.

**2. Update Minimum-Grade Values**

- Review the existing minimum-grade values in the prerequisite data.
- Update the values to follow the team's agreed grading system: A, B, C, D, and F.
- Verify that the updated values work correctly with prerequisite evaluation.

**3. Review Degree Requirement Data**

- Review the existing Computer Science B.S. sample data.
- Add or update degree requirements if needed for testing.
- Consider adding sample requirements for Mathematics and Physics if the other teams need them.

**4. Final Testing and Documentation**

- Test the database after any updates.
- Check for missing or invalid data that may affect the application.
- Update the documentation to reflect any final changes made during Sprint 3.

**Note:** The original course catalog and degree requirement tables were completed during Sprint 2. Sprint 3 will focus on adding user management, improving existing data, supporting integration, and testing.
