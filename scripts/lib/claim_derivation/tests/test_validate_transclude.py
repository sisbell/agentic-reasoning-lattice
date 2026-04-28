"""Unit tests for claim_derivation.validate_transclude.

The validator confirms each claim body markdown is a byte-substring of
its source note (modulo trailing whitespace). Mechanical, no LLM.
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.claim_derivation.validate_transclude import (
    _is_claim_body, validate_transclude_substring,
)


class IsClaimBodyTests(unittest.TestCase):
    def test_plain_md_is_claim_body(self):
        self.assertTrue(_is_claim_body(Path("T0.md")))
        self.assertTrue(_is_claim_body(Path("ActionPoint.md")))

    def test_sidecars_are_not_claim_bodies(self):
        self.assertFalse(_is_claim_body(Path("T0.label.md")))
        self.assertFalse(_is_claim_body(Path("T0.name.md")))
        self.assertFalse(_is_claim_body(Path("T0.description.md")))

    def test_underscore_prefix_not_claim_body(self):
        self.assertFalse(_is_claim_body(Path("_preamble.md")))
        self.assertFalse(_is_claim_body(Path("_signature.md")))

    def test_non_md_not_claim_body(self):
        self.assertFalse(_is_claim_body(Path("T0.yaml")))
        self.assertFalse(_is_claim_body(Path("T0.json")))


class ValidateTransludeBase(unittest.TestCase):
    """Setup: temp dir mirroring the lattice layout, source note + claim
    docs that the validator will read."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

        # Mirror the lattice structure relative to LATTICE root.
        self.note_dir = self.root / "_docuverse" / "documents" / "note"
        self.claim_dir = self.root / "_docuverse" / "documents" / "claim" / "ASN-0001"
        self.note_dir.mkdir(parents=True)
        self.claim_dir.mkdir(parents=True)

        self.note_path = self.note_dir / "ASN-0001-test-note.md"
        self.note_text = (
            "# ASN-0001\n\n"
            "## Section 1\n\n"
            "**T0 (FirstClaim).** body content for T0\n"
            "spans multiple lines\n"
            "with proof and details.\n\n"
            "**T1 (SecondClaim).** body content for T1\n"
            "another paragraph here.\n"
        )
        self.note_path.write_text(self.note_text)

        # Patch CLAIM_DIR so the validator looks in our tmp.
        # find_asn references NOTE_DIR captured at common.py import time
        # (via `from lib.shared.paths import ... NOTE_DIR ...`), so we
        # patch the binding in common.py rather than paths.py.
        self._patches = [
            mock.patch(
                "lib.claim_derivation.validate_transclude.CLAIM_DIR",
                self.root / "_docuverse" / "documents" / "claim",
            ),
            mock.patch(
                "lib.shared.common.NOTE_DIR",
                self.note_dir,
            ),
        ]
        for p in self._patches:
            p.start()
        self.addCleanup(lambda: [p.stop() for p in self._patches])

    def _write_claim(self, label, body):
        (self.claim_dir / f"{label}.md").write_text(body)


class SuccessTests(ValidateTransludeBase):
    def test_byte_substring_passes(self):
        self._write_claim(
            "T0",
            "**T0 (FirstClaim).** body content for T0\n"
            "spans multiple lines\n"
            "with proof and details.",
        )
        ok, findings = validate_transclude_substring(1)
        self.assertTrue(ok)
        self.assertEqual(findings, [])

    def test_with_trailing_newline_passes(self):
        # transclude writes body.rstrip() + "\n" — file has trailing newline
        # that the source may not have. The validator should rstrip before
        # checking.
        self._write_claim(
            "T0",
            "**T0 (FirstClaim).** body content for T0\n"
            "spans multiple lines\n"
            "with proof and details.\n",
        )
        ok, findings = validate_transclude_substring(1)
        self.assertTrue(ok)

    def test_multiple_claims_all_pass(self):
        self._write_claim(
            "T0",
            "**T0 (FirstClaim).** body content for T0\n"
            "spans multiple lines\n"
            "with proof and details.",
        )
        self._write_claim(
            "T1",
            "**T1 (SecondClaim).** body content for T1\n"
            "another paragraph here.",
        )
        ok, findings = validate_transclude_substring(1)
        self.assertTrue(ok)


class FailureTests(ValidateTransludeBase):
    def test_arbitrary_edit_fails(self):
        self._write_claim(
            "T0",
            "**T0 (FirstClaim).** body content for T0 — EDITED\n"
            "spans multiple lines",
        )
        ok, findings = validate_transclude_substring(1)
        self.assertFalse(ok)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0][0], "T0.md")
        self.assertIn("not a byte-substring", findings[0][1])

    def test_empty_body_flagged(self):
        self._write_claim("T0", "")
        ok, findings = validate_transclude_substring(1)
        self.assertFalse(ok)
        self.assertIn("empty body", findings[0][1])

    def test_one_failure_among_passes(self):
        self._write_claim(
            "T0",
            "**T0 (FirstClaim).** body content for T0\n"
            "spans multiple lines",
        )
        self._write_claim("T1", "this content does not appear in source")
        ok, findings = validate_transclude_substring(1)
        self.assertFalse(ok)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0][0], "T1.md")


class SkipsNonBodyFiles(ValidateTransludeBase):
    def test_sidecars_not_checked(self):
        self._write_claim(
            "T0",
            "**T0 (FirstClaim).** body content for T0\n"
            "spans multiple lines\n"
            "with proof and details.",
        )
        # Sidecars contain content NOT in the source note — must be skipped
        (self.claim_dir / "T0.label.md").write_text("T0\n")
        (self.claim_dir / "T0.name.md").write_text("FirstClaim\n")
        (self.claim_dir / "T0.description.md").write_text(
            "Some description prose that is not in the source note.\n",
        )
        ok, findings = validate_transclude_substring(1)
        self.assertTrue(ok)

    def test_underscore_files_not_checked(self):
        self._write_claim(
            "T0",
            "**T0 (FirstClaim).** body content for T0\n"
            "spans multiple lines\n"
            "with proof and details.",
        )
        (self.claim_dir / "_preamble.md").write_text(
            "Standalone preamble text not in source.\n",
        )
        ok, findings = validate_transclude_substring(1)
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
