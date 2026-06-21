"""Label-parsing regexes in claim-validate.py must handle the full claim
label vocabulary, not just ASCII S-numbers.

ASN-0053 uses ASCII labels (S0, S11d, WF, T4a). ASN-0036 uses Greek +
dotted-letter + parameterized labels (Σ.C, Σ.M(d)). The validator's
DECLARATION_RE and DEP_ENTRY_RE previously hardcoded an ASCII char class
([A-Za-z0-9()-]+(?:\\.[0-9]+)?), which silently failed on ASN-0036 —
declaration-label-mismatch on every claim and unparseable Depends bullets,
stalling the validate-gate. These tests lock in support for both.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SCRIPTS))

_spec = importlib.util.spec_from_file_location(
    "claim_validate", _SCRIPTS / "claim-validate.py",
)
cv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cv)


class DeclarationLabelParsing(unittest.TestCase):
    """DECLARATION_RE extracts the label from `**<label> (<Name>).**`."""

    CASES = [
        # ASCII
        ("**S0 (Convexity).**", "S0"),
        ("**S11d (GeneralDifferenceBound).**", "S11d"),
        ("**WF (WellFormedSpanFromEndpoints).**", "WF"),
        ("**T4a (SyntacticEquivalence).**", "T4a"),
        # Greek / dotted / parameterized (ASN-0036)
        ("**Σ.C (ContentStore).**", "Σ.C"),
        ("**Σ.M(d) (Arrangement).**", "Σ.M(d)"),
    ]

    def test_label_extraction(self):
        for text, want in self.CASES:
            m = cv.DECLARATION_RE.match(text)
            self.assertIsNotNone(m, f"no match: {text!r}")
            self.assertEqual(m.group(1), want, f"label from {text!r}")

    def test_name_is_captured(self):
        m = cv.DECLARATION_RE.match("**Σ.M(d) (Arrangement).**")
        self.assertEqual(m.group(2), "Arrangement")

    def test_prose_bold_without_name_paren_is_not_a_declaration(self):
        # A bold run with no ` (<Name>).` tail must not parse as a decl.
        self.assertIsNone(cv.DECLARATION_RE.match("**Case A:** the merge"))


class DepEntryLabelParsing(unittest.TestCase):
    """DEP_ENTRY_RE extracts the dependency label (first token) from a
    `  - <label> — <desc>` Depends bullet."""

    CASES = [
        ("  - S3 (SpanMerge, ASN-0053) — supplies the merge", "S3"),
        ("  - WR — width recovery", "WR"),
        ("  - Σ.C — supplies the store", "Σ.C"),
        ("  - Σ.M(d) — the arrangement", "Σ.M(d)"),
    ]

    def test_dep_label_extraction(self):
        for line, want in self.CASES:
            m = cv.DEP_ENTRY_RE.match(line)
            self.assertIsNotNone(m, f"no match: {line!r}")
            self.assertEqual(m.group(1), want, f"dep label from {line!r}")


if __name__ == "__main__":
    unittest.main()
