"""Unit tests for sweep_progress workspace progress tracking."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.claim_convergence import sweep_progress
from lib.claim_convergence.sweep_progress import (
    clear_progress, make_params, matches_params,
    progress_path, read_progress, write_progress,
)


class SweepProgressTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.workspace = Path(self.tmp.name) / "_workspace"
        self.patcher = mock.patch.object(
            sweep_progress, "WORKSPACE_DIR", self.workspace,
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_progress_path_under_workspace(self):
        path = progress_path("ASN-0034")
        self.assertEqual(
            path,
            self.workspace / "cone-sweep" / "ASN-0034" / "progress.json",
        )

    def test_read_returns_none_for_missing_file(self):
        self.assertIsNone(read_progress("ASN-0034"))

    def test_write_then_read_roundtrip(self):
        data = {
            "started_at": "2026-04-29T18:00:00Z",
            "min_deps": 4,
            "all": False,
            "completed": ["NAT-addbound", "T4"],
        }
        write_progress("ASN-0034", data)
        self.assertEqual(read_progress("ASN-0034"), data)

    def test_write_atomic_no_tmp_left_behind(self):
        write_progress("ASN-0034", {"min_deps": 4, "all": False, "completed": []})
        path = progress_path("ASN-0034")
        siblings = list(path.parent.iterdir())
        self.assertEqual(siblings, [path])  # no .tmp survivor

    def test_clear_removes_file_and_empty_parent(self):
        write_progress("ASN-0034", {"min_deps": 4, "all": False, "completed": []})
        clear_progress("ASN-0034")
        self.assertFalse(progress_path("ASN-0034").exists())
        # Parent dir cleaned up too if empty
        self.assertFalse(progress_path("ASN-0034").parent.exists())

    def test_clear_when_missing_is_safe(self):
        clear_progress("ASN-0034")  # no file, no parent — should not raise

    def test_read_returns_none_for_corrupted_json(self):
        path = progress_path("ASN-0034")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not valid json")
        self.assertIsNone(read_progress("ASN-0034"))


class MatchesParamsTests(unittest.TestCase):
    def test_none_saved_does_not_match(self):
        self.assertFalse(matches_params(None, make_params(min_deps=4, all_mode=False)))

    def test_same_params_match(self):
        saved = make_params(min_deps=4, all_mode=False)
        current = make_params(min_deps=4, all_mode=False)
        self.assertTrue(matches_params(saved, current))

    def test_different_min_deps_does_not_match(self):
        saved = make_params(min_deps=4, all_mode=False)
        current = make_params(min_deps=3, all_mode=False)
        self.assertFalse(matches_params(saved, current))

    def test_different_all_mode_does_not_match(self):
        saved = make_params(min_deps=4, all_mode=False)
        current = make_params(min_deps=4, all_mode=True)
        self.assertFalse(matches_params(saved, current))

    def test_extra_fields_in_saved_are_ignored(self):
        saved = {
            **make_params(min_deps=4, all_mode=False),
            "started_at": "2026-04-29T18:00:00Z",
            "completed": ["A", "B"],
        }
        current = make_params(min_deps=4, all_mode=False)
        self.assertTrue(matches_params(saved, current))


if __name__ == "__main__":
    unittest.main()
