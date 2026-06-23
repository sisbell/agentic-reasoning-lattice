"""Unit tests for cone_cascade_anchor_addrs — the cone review's
cascade-anchor read-scope.

A cone review anchors its cascade signal on EVERY claim it read: the
apex, its transitive same-ASN cone deps, and the cross-ASN foundation
claims. This is the note model's "anchor on what you read" principle —
so a modification anywhere in the cone (including the apex being edited
by another apex's revise) re-fires this apex in a single pass, instead
of one-hop layered propagation that halts at unchanged layers.

These tests pin that scope (apex + same-ASN deps + cross-ASN deps, with
order-preserving dedup) so a refactor can't silently narrow it back to
the apex's one-hop citations — the original livelock-adjacent bug.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.agents.producers.cone_review import cone_cascade_anchor_addrs
from lib.backend.addressing import Address


def _a(s: str) -> Address:
    return Address(s)


class ConeCascadeAnchorScope(unittest.TestCase):
    def test_apex_plus_same_asn_deps_plus_cross_asn(self):
        apex = _a("1.3.0.1.0.61")
        dep1 = _a("1.3.0.1.0.40")
        dep2 = _a("1.3.0.1.0.37")
        fnd = _a("1.3.0.1.0.900")  # cross-ASN foundation claim
        cone_addrs = [apex, dep1, dep2]
        label_index = {"WF": fnd, "OTHER": _a("1.3.0.1.0.999")}
        out = cone_cascade_anchor_addrs(cone_addrs, ["WF"], label_index)
        # apex first, then same-ASN deps, then the resolved cross-ASN dep.
        self.assertEqual(out, [apex, dep1, dep2, fnd])

    def test_apex_included_so_external_edits_invalidate(self):
        """The apex itself is in the anchor — that's what makes an apex
        re-fire when ANOTHER apex's revise edits it (its own clean review
        streak wouldn't otherwise detect the change)."""
        apex = _a("1.3.0.1.0.61")
        out = cone_cascade_anchor_addrs([apex], [], {})
        self.assertIn(apex, out)

    def test_order_preserving_dedup(self):
        apex = _a("1.3.0.1.0.61")
        dep1 = _a("1.3.0.1.0.40")
        # dep1 also reachable as a cross-ASN label → must appear once.
        out = cone_cascade_anchor_addrs(
            [apex, dep1, apex], ["DUP"], {"DUP": dep1},
        )
        self.assertEqual(out, [apex, dep1])

    def test_unresolvable_cross_asn_labels_skipped(self):
        apex = _a("1.3.0.1.0.61")
        out = cone_cascade_anchor_addrs([apex], ["MISSING"], {})
        self.assertEqual(out, [apex])

    def test_empty_cone_is_empty_anchor(self):
        self.assertEqual(cone_cascade_anchor_addrs([], [], {}), [])


if __name__ == "__main__":
    unittest.main()
