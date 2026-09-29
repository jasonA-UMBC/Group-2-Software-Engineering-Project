# Database Research

## 1. Database Requirements

### Course catalog
The database needs to store:
- Course identifier ex. EN.601.112
- Course title
- Course description
- Credits
- Department
- Course level 

*note: we can discuss more if we want to add/remove something.

Also, the system should support CRUD:
- Create a course
- Retrieve course info
- Update course info
- Delete a course

### Prerequisites
The database needs to store prereq relationships between courses.
So it must support:
- A single prereq
- Multiple prereq using AND ex. CMSC341 AND STAT355
- Alternative prereq using OR ex. CMSC462 OR DATA601
- Combination of AND and OR ex. (CMSC341 AND STAT355) OR DATA300

This helps the system to evaluate whether a student has completed the required courses.

### Course Offerings
The database needs to store info about when courses are offered.

For example:
- Course
- Term
- Section
- Offering status

*note: It needs to be checked in the JHU public course search API for which data available.

### Degree Requirements
The database needs to support degree requirement info.

For example:
- Degree/program
- Required courses
- Elective requirements
- Groups of courses that can satisfy a requirement

*note: still need more research for this info

### Course Catalog Validation
The database needs to support validation of catalog.

For example,
- Course identifiers should be valid and unique
- A prereq should refer to an existing course
- Required attributes should not be empty
- No duplicate course recourds
- No invalid prereq relationships

### Catalog API Support
Possible service interfaces:
- get_course(course_id)
- get_offerings(course_id)
- is_eligible(course, completed_courses)
- evaluate_prerequisites(course, completed_courses)

*note: further discuss with team B

## 2. Schema (Draft 1)

*note: PK = Primary key
       FK = Foreign key: an attribute in one table that references PK   
                         of another table

### Table 1: COURSES
-course_id           --> PK
-course_identifier   --> UNIQUE
-course_title
-course_description
-credits
-department_id       --> FK
-level

### Table 2: DEPARTMENTS
-department_id       --> PK
-school_id           --> FK
-department_name

### Table 3: SCHOOLS
-school_id           --> PK
-school_name

### Table 4: OFFERINGS
-offering_id         --> PK
-course_id           --> FK
-term
-section
-status

### Table 5: PREREQUISITES
*note: still planning

### Table 6: DEGREE_REQUIREMENTS
*note: still planning
