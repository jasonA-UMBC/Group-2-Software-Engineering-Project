"""
test_api_prereqs.py
Tests for the prereq API (branch: api-endpoint).

Put this file next to api-class.py and api-simulator.py, then run:
    pip install flask pytest
    pytest test_api_prereqs.py -v

Part 1: Are the API pulls valid?  (status codes, JSON shape, routes)
Part 2: Are the prereqs "fair"?   (three cases + sanity rules)
"""
import importlib.util
import pathlib
import re

import pytest

HERE = pathlib.Path(__file__).parent


def _load(filename, modname):
    """api-class.py has a hyphen, so a normal `import` won't work."""
    spec = importlib.util.spec_from_file_location(modname, HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


api_class = _load("api-class.py", "api_class")
api_sim = _load("api-simulator.py", "api_sim")

# JHU-style code: 2 letters + 3 digits (+ optional .section)
COURSE_RE = re.compile(r"^[A-Z]{2}\d{3}(\.\d{3})?$")


@pytest.fixture(params=["class", "sim"])
def client(request):
    app = api_class.app if request.param == "class" else api_sim.app
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def sim_client():
    api_sim.app.config["TESTING"] = True
    return api_sim.app.test_client()


@pytest.fixture
def class_client():
    api_class.app.config["TESTING"] = True
    return api_class.app.test_client()


# ---------------------------------------------------------------------------
# PART 1: API pulls are valid
# ---------------------------------------------------------------------------
class TestApiValidity:
    def test_home_returns_hello_world(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert r.get_json() == {"data": "hello world"}

    def test_prereq_route_returns_json_200(self, client):
        r = client.get("/prereqs/AS101")
        assert r.status_code == 200
        assert r.is_json

    def test_prereq_response_keyed_by_requested_code(self, client):
        body = client.get("/prereqs/AS101").get_json()
        assert list(body.keys()) == ["AS101"]
        assert isinstance(body["AS101"], list)

    def test_prereq_entries_are_strings(self, client):
        for item in client.get("/prereqs/AS101").get_json()["AS101"]:
            assert isinstance(item, str)

    def test_post_not_allowed(self, client):
        assert client.post("/prereqs/AS101").status_code == 405

    def test_unknown_route_404(self, client):
        assert client.get("/nope").status_code == 404

    def test_square_route(self, class_client):
        r = class_client.get("/home/7")
        assert r.status_code == 200
        assert r.get_json() == {"data": 49}

    def test_square_rejects_non_integer(self, class_client):
        assert class_client.get("/home/abc").status_code == 404


# ---------------------------------------------------------------------------
# PART 2: Prereq fairness -- THREE CASES
# ---------------------------------------------------------------------------
class TestPrereqFairness:
    # ---- Case 1: valid course, prereqs come back and are sane ------------
    @pytest.mark.parametrize("code", api_sim.course_code_data)
    def test_case1_valid_course_has_fair_prereqs(self, sim_client, code):
        prereqs = sim_client.get(f"/prereqs/{code}").get_json()[code]
        assert code not in prereqs, "course cannot be its own prereq"
        assert len(prereqs) == len(set(prereqs)), "no duplicate prereqs"
        assert len(prereqs) <= 5
        assert all(p in api_sim.course_code_data for p in prereqs), \
            "every prereq must itself be a real course"

    # ---- Case 2: course with NO prereqs -> empty list, not an error ------
    def test_case2_no_prereqs_is_empty_list_not_error(self, sim_client, monkeypatch):
        monkeypatch.setattr(api_sim.random, "randint", lambda a, b: 0)
        body = sim_client.get("/prereqs/AS101").get_json()
        assert body == {"AS101": []}

    # ---- Case 3: invalid / unknown course -> clear error, no fake prereqs
    @pytest.mark.parametrize("bad", ["ZZ000", "hello", "AS10", "as101"])
    def test_case3_unknown_course_reports_error(self, sim_client, bad):
        data = sim_client.get(f"/prereqs/{bad}").get_json()[bad]
        assert data == ["ERROR: COURSE CODE NOT FOUND"]

    # ---- Extra fairness rules --------------------------------------------
    def test_simulator_no_self_prereq_over_many_runs(self, sim_client):
        for _ in range(200):
            for code in api_sim.course_code_data:
                assert code not in sim_client.get(f"/prereqs/{code}").get_json()[code]

    def test_class_api_prereqs_are_separate_codes(self, class_client):
        """
        KNOWN BUG in api-class.py: find_all_prereqs returns
        ['PH102.000, PH104.000'] -- ONE string with a comma, not two codes.
        This test fails until it is ['PH102.000', 'PH104.000'].
        """
        data = class_client.get("/prereqs/PH201").get_json()["PH201"]
        for p in data:
            assert "," not in p, f"prereqs merged into one string: {p!r}"
            assert COURSE_RE.match(p), f"bad course code format: {p!r}"

    def test_class_api_no_self_or_duplicate_prereq(self, class_client):
        data = class_client.get("/prereqs/PH102.000").get_json()["PH102.000"]
        flat = [x.strip() for p in data for x in p.split(",")]
        assert "PH102.000" not in flat
        assert len(flat) == len(set(flat))


# ---------------------------------------------------------------------------
# PART 3: Schema-based fairness (database-research branch)
# Pure-Python model of prerequisite_groups / prerequisites so you can check
# AND/OR logic and circular chains without needing the Postgres DB.
# Swap FakeDB for real psycopg queries once find_all_prereqs hits the DB.
# ---------------------------------------------------------------------------
def satisfied(group, completed):
    """group = {'op': 'AND'|'OR', 'items': [course | nested group]}"""
    results = [
        satisfied(i, completed) if isinstance(i, dict) else i in completed
        for i in group["items"]
    ]
    return all(results) if group["op"] == "AND" else any(results)


def has_cycle(graph):
    """graph = {course: [prereq courses]}"""
    seen, stack = set(), set()

    def visit(n):
        if n in stack:
            return True
        if n in seen:
            return False
        seen.add(n)
        stack.add(n)
        if any(visit(m) for m in graph.get(n, [])):
            return True
        stack.discard(n)
        return False

    return any(visit(n) for n in graph)


class TestSchemaLogic:
    def test_and_group_needs_all(self):
        g = {"op": "AND", "items": ["EN.601.220", "EN.601.226"]}
        assert satisfied(g, {"EN.601.220", "EN.601.226"})
        assert not satisfied(g, {"EN.601.220"})

    def test_or_group_needs_one(self):
        g = {"op": "OR", "items": ["EN.601.220", "EN.601.226"]}
        assert satisfied(g, {"EN.601.226"})
        assert not satisfied(g, set())

    def test_nested_groups(self):
        g = {"op": "AND", "items": ["A", {"op": "OR", "items": ["B", "C"]}]}
        assert satisfied(g, {"A", "C"})
        assert not satisfied(g, {"B", "C"})

    def test_no_circular_prereqs_valid_catalog(self):
        assert not has_cycle({"C": ["B"], "B": ["A"], "A": []})

    def test_circular_prereqs_detected(self):
        assert has_cycle({"A": ["B"], "B": ["C"], "C": ["A"]})

    def test_self_prereq_detected(self):
        assert has_cycle({"A": ["A"]})