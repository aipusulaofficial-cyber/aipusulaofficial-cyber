import unittest
import urllib.error

from matrix_core import refresh_matrix, render_markdown, summarize_runs


class HealthMatrixContractTests(unittest.TestCase):
    def test_latest_attempt_per_workflow_wins_even_if_runs_are_unordered(self):
        runs = [
            {"name": "ci", "status": "completed", "conclusion": "success", "id": 2,
             "updated_at": "2026-09-29T12:00:00Z"},
            {"name": "ci", "status": "completed", "conclusion": "failure", "id": 1,
             "updated_at": "2026-09-29T11:00:00Z"},
        ]
        status, conclusion, workflows = summarize_runs(runs)
        self.assertEqual((status, conclusion), ("completed", "success"))
        self.assertEqual(workflows["ci"]["run_id"], 2)

    def test_repository_mapping_and_private_access_are_not_false_green(self):
        def fake_get(path):
            if path.startswith("private/"):
                raise urllib.error.HTTPError("https://example.invalid", 404, "not found", {}, None)
            if path.endswith("/git/ref/heads/main"):
                return {"object": {"sha": "newsha"}}
            return {"workflow_runs": [{
                "name": "ci", "status": "completed", "conclusion": "success",
                "id": 123, "updated_at": "2026-09-29T12:00:00Z",
            }]}

        rows = refresh_matrix(
            [{"repository": "public"}, {"repository": "private"}], fake_get
        )
        self.assertEqual(rows[0]["sha"], "newsha")
        self.assertEqual(rows[0]["conclusion"], "success")
        self.assertEqual(rows[1]["status"], "unavailable")
        self.assertIsNone(rows[1]["sha"])
        self.assertIn("private", render_markdown(rows))

    def test_empty_workflow_evidence_is_not_green(self):
        self.assertEqual(summarize_runs([])[:2], ("not_run", "not_run"))


if __name__ == "__main__":
    unittest.main()
