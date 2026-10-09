-- CMSC 447 Team A - Course Catalog PostgreSQL Schema
-- Reconstructed from the current pgAdmin schema-only export (2026-10-09).

CREATE TABLE public.schools (
    school_id SERIAL PRIMARY KEY,
    school_name VARCHAR(300) UNIQUE
);

CREATE TABLE public.departments (
    department_id SERIAL PRIMARY KEY,
    school_id INTEGER REFERENCES public.schools(school_id),
    department_name VARCHAR(500),
    UNIQUE (school_id, department_name)
);

CREATE TABLE public.courses (
    course_id SERIAL PRIMARY KEY,
    department_id INTEGER REFERENCES public.departments(department_id),
    course_identifier VARCHAR(50) UNIQUE,
    course_prefix VARCHAR(10),
    course_title VARCHAR(250),
    course_description TEXT,
    credits NUMERIC(4,2),
    course_level VARCHAR(100),
    is_repeatable BOOLEAN
);

CREATE TABLE public.terms (
    term_id SERIAL PRIMARY KEY,
    term_name VARCHAR(20),
    start_date DATE,
    end_date DATE,
    CONSTRAINT unique_term_name UNIQUE (term_name)
);

CREATE TABLE public.offerings (
    offering_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES public.courses(course_id),
    term_id INTEGER REFERENCES public.terms(term_id),
    course_section VARCHAR(20),
    max_seats INTEGER,
    open_seats INTEGER,
    instruction_method VARCHAR(50),
    course_location VARCHAR(100),
    status VARCHAR(50),
    waitlisted INTEGER,
    meetings VARCHAR(200),
    CONSTRAINT unique_course_term_section UNIQUE (course_id, term_id, course_section)
);

CREATE TABLE public.prerequisite_groups (
    prerequisite_group_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES public.courses(course_id),
    group_operator VARCHAR(3) CHECK (group_operator IN ('AND', 'OR')),
    parent_group_id INTEGER REFERENCES public.prerequisite_groups(prerequisite_group_id)
);

CREATE TABLE public.prerequisites (
    prerequisite_id SERIAL PRIMARY KEY,
    prerequisite_group_id INTEGER REFERENCES public.prerequisite_groups(prerequisite_group_id),
    prerequisite_course_id INTEGER REFERENCES public.courses(course_id),
    negative_prerequisite BOOLEAN DEFAULT FALSE,
    min_grade VARCHAR(2),
    concurrent_allowed BOOLEAN DEFAULT FALSE
);