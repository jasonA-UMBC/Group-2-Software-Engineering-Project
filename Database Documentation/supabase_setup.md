# Supabase Database Description (Oct 9, 2026)

## 1. About the Database

We transferred Team A's PostgreSQL database from the local computer to the Supabase project created by Team B.

Note:   The database is not fully completed yet, but it contains enough data for developing.

## 2. What I Did so far in Supabase

I used the SQL Editor in Supabase to create the seven tables using our `schema.sql` file.

Then, I exported the data from my local and imported them into Supabase: Course Prerequisites project.

Tables imported:

1. schools
2. departments
3. courses
4. terms
5. offerings
6. prerequisite_groups
7. prerequisites

## 3. Current Data in Supabase

| Table | Records |
|---|---:|
| schools | 13 |
| departments | 26 |
| courses | 566 |
| terms | 8 |
| offerings | 889 |
| prerequisite_groups | 57 |
| prerequisites | 119 |

Total: 1,678 records.

## 4. How Team B Can Use the Database

1. Team B can access the database through the Supabase: Course Prerequisites project.

The tables are under the `public` schema.

2. Team B can use Table Editor to view the records or SQL Editor to query the data.

3. Team B can also use the Supabase API to retrieve the data from the application. The application will need the Supabase Project URL and publishable key. These can be found in the Supabase project settings.

## 5. Prerequisites Explaination

I created two tables for prerequisite information:

- `prerequisite_groups`
- `prerequisites`

These tables work together to represent prerequisite requirements for a course.

### prerequisite_groups

This stores the groups used to organize prerequisite conditions.

| Column | Description |
|---|---|
| prerequisite_group_id | Unique ID for each group |
| course_id | The course that has the prerequisite requirement |
| group_operator | AND or OR |
| parent_group_id | Used to connect nested prerequisite groups |

The `group_operator` determines how the requirements in the group should be evaluated.
    - AND
    - OR

The `parent_group_id` allows one prerequisite group to be inside another group.

### prerequisites

This stores the individual prerequisite courses.

| Column | Description |
|---|---|
| prerequisite_id | Unique ID for each prerequisite record |
| prerequisite_group_id | The group this prerequisite belongs to |
| prerequisite_course_id | The required course |
| negative_prerequisite | Indicates a course that must not have been completed |
| min_grade | Minimum required grade, if specified |
| concurrent_allowed | Indicates whether concurrent enrollment is allowed |

The `prerequisite_course_id` references `courses.course_id`, so the required course can be found in the "courses" table.

### Example 1: A AND B

Course D requires Course A and Course B.

The prerequisite group uses AND.

Both A and B must be completed before the student is eligible for D.

### Example 2: A OR B

Course D requires either Course A or Course B.

The prerequisite group uses OR.

Only needs to satisfy one of the two requirements.

### Example 3: (A AND B) OR C

Course D requires: (A AND B) OR C

This means a student must complete both Course A and Course B, or complete Course C, to satisfy the prerequisites for Course D.

To represent this, we can use nested prerequisite groups.

- The main group uses OR.
- The child group uses AND and contains Course A and Course B.
- Course C belongs to the main OR group.
- The `parent_group_id` connects the child AND group to the main OR group.

I think this covers what we discussed with Team B on Thursday, October 8, 2026.

## 6. Example: Retrieve Prerequisite Information

To find the prerequisite groups for a course:

```sql
SELECT *
FROM public.prerequisite_groups
WHERE course_id = 1;
```

To see the required courses inside a prerequisite group:

```sql
SELECT
    p.prerequisite_id,
    c.course_identifier,
    c.course_title,
    p.min_grade,
    p.negative_prerequisite,
    p.concurrent_allowed
FROM public.prerequisites p
JOIN public.courses c
    ON p.prerequisite_course_id = c.course_id
WHERE p.prerequisite_group_id = 1;
```

Note:   Replace the IDs with the course or group you want to check.

These queries retrieve the stored prerequisite information. To determine whether a student is eligible, the application also needs to evaluate the AND/OR rules and the student's completed courses.

## 7. Row Level Security (RLS)

I enabled Row Level Security for all seven tables.

I also added SELECT policies for the `anon` and `authenticated` roles so the application can retrieve the data.

Note:   The policies I added only allow SELECT operations. They do not provide additional insert, update, or delete permissions.

        The current SELECT policies allow public reading through the Supabase API. 

## 8. Notes

- The database this version contains partial JHU course data .
- Some course information and prerequisite may still be missing.
- The data can be updated later as more courses and prerequisites are added.