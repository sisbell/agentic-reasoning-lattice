# Review of ASN-0068

## REVISE

(none)

## OUT_OF_SCOPE

(none)

VERDICT: CONVERGED

The ASN's proofs are rigorous and complete. CV-MAX's existence and uniqueness arguments handle the walk construction with explicit case analysis (left region/right region in existence; δ = 0/δ > 0 in uniqueness, with WLOG handling negative δ). The lockstep argument uses last-component arithmetic via D-SEQ★, TS2, and T3 — all foundation-grounded. CV-PRED's inverse properties are derived from TS2 and the convention `v − 0 := v`; existence is tied to S8a's positive-component requirement.

The four worked examples exercise distinct configurations (cross-document contiguous transclusion, cross-document self-transclusion blocking merge, self-comparison with both diagonal and off-diagonal runs, differing depths). Each example traces the walks step-by-step and verifies the result against CV-MAX.

Boundary cases are handled: empty restrictions (CV-EMPTY), single-position runs (CV-ATOM), self-comparison (CV-SELF, CV-LINK-SELF), depth mismatches (Example 4), and CV-LINK-DEGEN. Cardinality is bounded via S8-fin and run→starting-pair injectivity. The link-subspace special cases are correctly grounded in CL-OWN + S7 (cross-document emptiness) and CL-UNIQ (self-comparison diagonal collapse).

Cross-references are confined to foundation ASNs (0034, 0036, 0047, 0053, 0058). CV-RO and CV-DETERM properly establish the operation as a pure observation outside the transition vocabulary. CV-SPAN-VIEW's injectivity is derived from OrdinalDisplacement's defining form and T3, with the set-level lift inheriting from per-run injectivity.
