"""Unit tests for claim_derivation.find_in_source.

The resolver takes the source note text and an LLM-extracted body, and
returns the matched substring of the source — or None on failure. Two
match strategies, in order: exact byte-substring, then
whitespace-normalized. Strict by design — fuzzy matching is silent
acceptance of unexplained drift.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.claim_derivation.find_in_source import find_in_source


class ExactMatchTests(unittest.TestCase):
    def test_exact_substring_returns_unchanged(self):
        src = "before\n\n**T0 (Foo).** body content here.\n\nafter"
        probe = "**T0 (Foo).** body content here."
        self.assertEqual(find_in_source(src, probe), probe)

    def test_full_text_matches(self):
        src = "the entire content"
        self.assertEqual(find_in_source(src, src), src)

    def test_empty_inputs_return_none(self):
        self.assertIsNone(find_in_source("", "x"))
        self.assertIsNone(find_in_source("x", ""))
        self.assertIsNone(find_in_source("", ""))


class WhitespaceNormalizedTests(unittest.TestCase):
    def test_extra_spaces_in_probe_match(self):
        src = "**T0 (Foo).** content here\nspanning lines"
        probe = "**T0 (Foo).** content here spanning lines"
        result = find_in_source(src, probe)
        self.assertIsNotNone(result)
        # Result is the source's bytes, with the original newline
        self.assertIn("content here\nspanning lines", result)

    def test_collapsed_runs_in_probe_match_split_in_source(self):
        src = "alpha    beta\n\n\ngamma"
        probe = "alpha beta gamma"
        result = find_in_source(src, probe)
        self.assertEqual(result, src)

    def test_probe_with_collapsed_internal_whitespace(self):
        src = "**T0 (Description).**\n\n  T0 posits the carrier set."
        probe = "**T0 (Description).** T0 posits the carrier set."
        result = find_in_source(src, probe)
        self.assertIsNotNone(result)
        # Source's bytes preserve the actual newlines and indentation
        self.assertIn("\n\n  T0 posits", result)


class FailureTests(unittest.TestCase):
    def test_content_not_in_source_returns_none(self):
        src = "the source note text"
        probe = "completely unrelated content"
        self.assertIsNone(find_in_source(src, probe))

    def test_partial_match_with_extra_unrelated_words_fails(self):
        src = "alpha beta gamma"
        probe = "alpha beta gamma delta"  # delta is not in source
        self.assertIsNone(find_in_source(src, probe))


class SourceBytesPreservedTests(unittest.TestCase):
    """When the resolver finds a match via whitespace normalization, the
    bytes returned must be the source's original bytes, not the probe's."""

    def test_returns_source_bytes_not_probe_bytes(self):
        src = "claim:\n\n  indented body  \n\nrest"
        probe = "claim: indented body"  # no indentation, normalized spaces
        result = find_in_source(src, probe)
        self.assertIsNotNone(result)
        # Return must contain the source's exact whitespace, not the probe's
        self.assertIn("\n\n  indented body", result)
        # And must be a substring of the source
        self.assertIn(result, src)


if __name__ == "__main__":
    unittest.main()
