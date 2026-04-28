"""Unit tests for note-convergence review parsing."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.note_convergence.review import extract_note_findings


SAMPLE_REVIEW = """# Review of ASN-0009

VERDICT: REVISE

## REVISE

### Issue 1: foo
Body of issue 1.
Multiple lines.

### Issue 2: bar
Body of issue 2.

## OUT_OF_SCOPE

### Issue 3: baz
Body of issue 3.

## RESOLVED

### Old issue
This was resolved last cycle.
"""


class ExtractNoteFindingsTests(unittest.TestCase):
    def test_separates_revise_and_oos(self):
        findings = extract_note_findings(SAMPLE_REVIEW)
        self.assertEqual(len(findings), 3)
        self.assertEqual([f[1] for f in findings],
                         ["REVISE", "REVISE", "OUT_OF_SCOPE"])

    def test_extracts_titles(self):
        findings = extract_note_findings(SAMPLE_REVIEW)
        self.assertEqual([f[0] for f in findings],
                         ["Issue 1: foo", "Issue 2: bar", "Issue 3: baz"])

    def test_skips_resolved_section(self):
        findings = extract_note_findings(SAMPLE_REVIEW)
        for title, _, _ in findings:
            self.assertNotEqual(title, "Old issue")

    def test_body_preserved(self):
        findings = extract_note_findings(SAMPLE_REVIEW)
        first = findings[0]
        self.assertIn("Body of issue 1", first[2])
        self.assertIn("Multiple lines", first[2])
        self.assertTrue(first[2].startswith("### Issue 1: foo"))

    def test_no_findings_when_no_sections(self):
        text = "# Review of ASN-0001\nVERDICT: CONVERGED\n"
        self.assertEqual(extract_note_findings(text), [])

    def test_only_revise(self):
        text = (
            "# Review of ASN-0001\n"
            "VERDICT: REVISE\n"
            "## REVISE\n\n"
            "### Solo\nBody\n"
        )
        findings = extract_note_findings(text)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0][1], "REVISE")


if __name__ == "__main__":
    unittest.main()
