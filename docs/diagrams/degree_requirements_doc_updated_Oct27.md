# Degree Requirements – ER Diagram Update Oct 27

We added four tables to the ER diagram for degree requirements. We will start with the JHU Computer Science B.S. program and later use the same tables for Mathematics and Physics. The existing course catalog tables will stay the same.

## New Tables

### 1. DEGREE_PROGRAMS – Which major/program?
Stores information about each degree program, including department, program name, degree type, catalog year, and total credits required.

For example, one department can offer Computer Science B.S. and B.A. programs, and they may have different requirements.

- PK: degree_program_id
- FK: department_id -> DEPARTMENTS

### 2. DEGREE_REQUIREMENT_GROUPS – Which category?
Stores categories for each degree program, such as CS Core, Mathematics, Basic Sciences, and CS Electives.

For example, if degree_program_id = 1 is Computer Science B.S., we can have:

- Group 1: CS Core, degree_program_id = 1
- Group 2: Mathematics, degree_program_id = 1
- Group 3: Basic Sciences, degree_program_id = 1
- Group 4: CS Electives, degree_program_id = 1

- PK: requirement_group_id
- FK: degree_program_id -> DEGREE_PROGRAMS
- FK: parent_group_id -> DEGREE_REQUIREMENT_GROUPS (same table, can be NULL)

The parent_group_id is used when we have nested requirements. For example, suppose CS Foundations can be satisfied by Course A OR (Course B AND Course C):

    Group 1: OR (parent_group_id = NULL)
       - Course A
       - Group 2: AND (parent_group_id = 1)
           - Course B
           - Course C

Group 2 belongs to Group 1. The group_operator tells us whether the requirements are combined using AND or OR. We still need to define this behavior in the evaluator. This is only an example, not an actual JHU rule.

### 3. DEGREE_REQUIREMENTS – What must be completed?
Stores the actual requirement for each category.

- PK: degree_requirement_id
- FK: requirement_group_id -> DEGREE_REQUIREMENT_GROUPS

Examples of requirement_type:

- CREDIT_MINIMUM: Complete at least 16 mathematics credits.
- COURSE_COUNT: Complete at least 3 approved electives.
- REQUIRED_COURSE: Complete a specific required course.

For example, the Mathematics group can have requirement_type = CREDIT_MINIMUM and minimum_credits = 16. If a student completed 13 eligible credits, they would still need 3 more credits.

### 4. DEGREE_REQUIREMENT_COURSES – Which courses count?
Connects degree requirements to eligible courses in our existing COURSES table.

- PK: requirement_course_id
- FK: degree_requirement_id -> DEGREE_REQUIREMENTS
- FK: course_id -> COURSES

For example, requirement 10 says to complete at least 12 credits of approved upper-level CS electives. We can link Course A, Course B, and Course C to requirement 10. Each course is worth 4 credits.

This means those courses are eligible for the requirement. It does not mean a student must take all three if other approved courses are available. The requirement checks the total eligible credits.

One requirement can have many eligible courses, and one course can be linked to more than one requirement. This is why we use the junction table.

## Complete Example

Computer Science B.S. (degree_program_id = 1)
-> Mathematics (requirement_group_id = 2)
-> Complete at least 16 mathematics credits (degree_requirement_id = 10)
-> DEGREE_REQUIREMENT_COURSES links requirement 10 to approved math courses in COURSES.

The system would check the student's completed eligible courses and add up the credits. Student course history and grades would need to come from the appropriate team/component; these four tables only store degree rules.

## ER Diagram Relationships

The existing tables still connect as before. The new relationships are:

10. A department can offer multiple degree programs, and each degree program belongs to one department.
11. One degree program can have multiple requirement groups.
12. Requirement groups can contain smaller groups using parent_group_id (self-reference).
13. One requirement group can have multiple degree requirements.
14. One degree requirement can link to multiple eligible courses.
15. One course can be linked to multiple degree requirements through DEGREE_REQUIREMENT_COURSES.
