"""Unit tests for path-construction helpers in lib.shared.paths."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import claim_doc_path


class ClaimDocPathTests(unittest.TestCase):
    def test_returns_canonical_lattice_relative_string(self):
        self.assertEqual(
            claim_doc_path("ASN-0034", "T0"),
            "_docuverse/documents/claim/ASN-0034/T0.md",
        )

    def test_dotted_label(self):
        # Labels with dots survive intact (e.g., Σ.M(d)).
        self.assertEqual(
            claim_doc_path("ASN-0036", "Σ.M(d)"),
            "_docuverse/documents/claim/ASN-0036/Σ.M(d).md",
        )

    def test_does_not_check_file_exists(self):
        # Pure construction — caller may use this to address a claim that
        # has not been written yet (new-claim creation flow).
        path_str = claim_doc_path("ASN-9999", "DoesNotExist")
        self.assertEqual(
            path_str,
            "_docuverse/documents/claim/ASN-9999/DoesNotExist.md",
        )

    def test_returns_str_not_path(self):
        # Substrate links store path strings; the helper returns a str
        # directly so callers don't have to remember to coerce.
        self.assertIsInstance(claim_doc_path("ASN-0034", "T0"), str)


if __name__ == "__main__":
    unittest.main()
