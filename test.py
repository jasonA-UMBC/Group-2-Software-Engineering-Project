import unittest

COURSE_PREREQUISITES = {
    "Intro to Programming": [],
    "Data Structures": ["Intro to Programming"],
    "Algorithms": ["Data Structures"],
}


def query_prerequisites(course_name, courses=COURSE_PREREQUISITES):
    """Return the prerequisites for a course, or None if it isn't in the dictionary."""
 
    return courses.get(course_name)


def main():
    course_name = input("Enter a class name: ").strip()
    prerequisites = query_prerequisites(course_name)

    if prerequisites is None:
        print(f"Class not found: {course_name}")
    elif prerequisites:
        print(f"Prerequisites for {course_name}: {', '.join(prerequisites)}")
    else:
        print(f"{course_name} has no prerequisites.")


class TestQueryPrerequisites(unittest.TestCase):
    def test_returns_prerequisites(self):
        courses = {"Algorithms": ["Data Structures"]}
        self.assertEqual(query_prerequisites("Algorithms", courses), ["Data Structures"])

    def test_returns_empty_list_for_no_prerequisites(self):
        courses = {"Intro to Programming": []}
        self.assertEqual(query_prerequisites("Intro to Programming", courses), [])

    def test_returns_none_for_unknown_class(self):
        self.assertIsNone(query_prerequisites("Unknown Class", {}))


if __name__ == "__main__":
    unittest.main()