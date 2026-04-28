"""Unit tests for the signature plumbing.

Two units under test:
  - `_render_signature` in claim_derivation.transclude — converts
    enrich's signature list into a markdown bullet sidecar string
  - `aggregate_signature` in lib.shared.common — concatenates
    sidecars across an ASN's claims for the contract-review prompt
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.claim_derivation.transclude import _render_signature
from lib.shared.common import aggregate_signature


class RenderSignatureTests(unittest.TestCase):
    def test_empty_list_returns_none(self):
        self.assertIsNone(_render_signature([]))
        self.assertIsNone(_render_signature(None))

    def test_single_entry(self):
        out = _render_signature([
            {"symbol": "Σ.C", "meaning": "The content store"},
        ])
        self.assertEqual(out, "- `Σ.C` — The content store")

    def test_multiple_entries_join_with_newline(self):
        out = _render_signature([
            {"symbol": "T", "meaning": "carrier set"},
            {"symbol": "#a", "meaning": "length operator"},
        ])
        self.assertEqual(
            out,
            "- `T` — carrier set\n- `#a` — length operator",
        )

    def test_symbol_only_no_meaning(self):
        out = _render_signature([{"symbol": "⊕"}])
        self.assertEqual(out, "- `⊕`")

    def test_skips_entries_without_symbol(self):
        out = _render_signature([
            {"symbol": "T", "meaning": "carrier set"},
            {"meaning": "orphan with no symbol"},
            {"symbol": "", "meaning": "empty symbol"},
        ])
        self.assertEqual(out, "- `T` — carrier set")

    def test_all_invalid_returns_none(self):
        self.assertIsNone(_render_signature([
            {"meaning": "no symbol"},
            {"symbol": ""},
        ]))

    def test_non_dict_entries_skipped(self):
        out = _render_signature([
            "not-a-dict",
            {"symbol": "T", "meaning": "carrier set"},
        ])
        self.assertEqual(out, "- `T` — carrier set")

    def test_strips_whitespace_from_fields(self):
        out = _render_signature([
            {"symbol": "  T  ", "meaning": "  carrier set  "},
        ])
        self.assertEqual(out, "- `T` — carrier set")


class AggregateSignatureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.claim_dir = Path(self.tmp.name)

    def test_no_sidecars_returns_placeholder(self):
        # Empty claim dir
        self.assertEqual(
            aggregate_signature(self.claim_dir),
            "(no signature)",
        )

    def test_nonexistent_dir_returns_placeholder(self):
        self.assertEqual(
            aggregate_signature(Path("/nonexistent/path")),
            "(no signature)",
        )

    def test_single_sidecar(self):
        (self.claim_dir / "T0.signature.md").write_text(
            "- `T` — carrier set\n- `#a` — length operator\n",
        )
        out = aggregate_signature(self.claim_dir)
        self.assertIn("### T0", out)
        self.assertIn("- `T` — carrier set", out)
        self.assertIn("- `#a` — length operator", out)

    def test_multiple_sidecars_concatenate(self):
        (self.claim_dir / "T0.signature.md").write_text("- `T` — carrier")
        (self.claim_dir / "Sigma.C.signature.md").write_text("- `Σ.C` — store")
        out = aggregate_signature(self.claim_dir)
        # Both stems present
        self.assertIn("### T0", out)
        self.assertIn("### Sigma.C", out)

    def test_empty_sidecar_skipped(self):
        (self.claim_dir / "T0.signature.md").write_text("")
        (self.claim_dir / "T1.signature.md").write_text("- `T` — carrier")
        out = aggregate_signature(self.claim_dir)
        self.assertNotIn("### T0", out)
        self.assertIn("### T1", out)

    def test_only_signature_sidecars_picked_up(self):
        # Other sidecar kinds should not be aggregated
        (self.claim_dir / "T0.label.md").write_text("T0\n")
        (self.claim_dir / "T0.name.md").write_text("FirstClaim\n")
        (self.claim_dir / "T0.description.md").write_text("Description\n")
        # No signature sidecar
        self.assertEqual(
            aggregate_signature(self.claim_dir),
            "(no signature)",
        )


if __name__ == "__main__":
    unittest.main()
