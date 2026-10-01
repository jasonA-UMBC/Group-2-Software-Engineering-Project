CREATE TABLE SCHOOLS (
    school_id SERIAL PRIMARY KEY,
    school_name VARCHAR(300) UNIQUE 
);

CREATE TABLE DEPARTMENTS (
    department_id SERIAL PRIMARY KEY,
    school_id INTEGER FOREIGN KEY,
    department_name VARCHAR(500)

    FOREIGN KEY (school_id)
        REFERENCES SCHOOLS(school_id)

    UNIQUE (school_id, department_name)
);

CREATE TABLE COURSES (
    course_id SERIAL PRIMARY KEY,
    department_id INTEGER FOREIGN KEY,
    course_identifier VARCHAR(200),
    course_prefix VARCHAR(10),
    course_title VARCHAR(200),
    course_description TEXT,
    credits DECIMAL(4, 2),
    course_level VARCHAR(100),
    is_repeatable BOOLEAN

    FOREIGN KEY (department_id)
        REFERENCES DEPARTMENTS(department_id)
);

CREATE TABLE TERMS (
    term_id SERIAL PRIMARY KEY,
    term_name VARCHAR(20),
    start_date VARCHAR(20),
    end_date VARCHAR(20)
);

CREATE TABLE OFFERINGS (
    offering_id SERIAL PRIMARY KEY,
    course_id SERIAL FOREIGN KEY,
    term_id SERIAL FOREIGN KEY
    course_section VARCHAR(10),
    max_seats INTEGER,
    open_seats INTEGER,
    seat_available INTEGER,
    instruction_mode VARCHAR(50),
    course_location VARCHAR(100),
    building VARCHAR(100)

    FOREIGN KEY (course_id)
        REFERENCES COURSES(course_id)
    
    FOREIGN KEY (term_id)
        REFERENCES TERMS(term_id)
);

CREATE TABLE PREREQUISITE_GROUPS (
    prerequisite_group_id SERIAL PRIMARY KEY,
    course_id SERIAL FOREIGN KEY,
    group_operator VARCHAR(3)

    FOREIGN KEY (course_id)
        REFERENCES COURSES(course_id)
);

CREATE TABLE PREREQUISITEs (
    prerequisite_id SERIAL PRIMARY KEY,
    prerequisite_group_id SERIAL FOREIGN KEY,
    negative_prerequisite BOOLEAN

    FOREIGN KEY (prerequisite_group_id)
        REFERENCES PREREQUISITE_GROUPS(prerequisite_group_id)
);
