# Degree Requirements – ER Diagram Update Oct 26

## New Tables

### 1. DEGREE_PROGRAMS
Stores each degree program, such as Computer Science B.S., along with its department, degree type, and catalog year. One department can have multiple degree programs.

### 2. DEGREE_REQUIREMENT_GROUPS
Organizes requirements into categories like CS Core, Mathematics, Basic Sciences, and Electives. 

Note: A group can also have a parent group so we can organize more complicated requirements.

### 3. DEGREE_REQUIREMENTS
Stores the actual rule for a requirement, such as completing a required course, taking a certain number of courses, or earning a minimum number of credits.

For example, if the Mathematics requirement is 16 credits and a student has completed 13 eligible credits, the student still needs 3 credits.

### 4. DEGREE_REQUIREMENT_COURSES
Connects requirements to courses in our existing `COURSES` table. 

## How It Works
The system starts with a degree program, finds its requirement groups, checks the rules in each group, and looks up the courses that can satisfy those rules.

For example,

Computer Science B.S. -> Mathematics -> Minimum 16 credits -> Eligible courses

Note: Some requirements may have choices, such as (Course A AND Course B) OR Course C. This is similar to the AND/OR prerequisite logic we already implemented.

## ER Diagram Relationships
10. A department can offer multiple degree programs.
11. Each degree program belongs to one department.
12. A degree program can have multiple requirement groups.
13. Each requirement group belongs to one degree program.
14. Requirement groups can contain nested groups through a self-referencing foreign key.
15. Each requirement group can contain multiple degree requirements.
16. Degree requirements and courses have a many-to-many relationship through DEGREE_REQUIREMENT_COURSES.

**Note: The ER diagram is still a draft.