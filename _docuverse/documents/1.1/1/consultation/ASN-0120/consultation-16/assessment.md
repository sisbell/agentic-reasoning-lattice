# Channel Assignment — ASN-0120 review-16

**Date:** 2026-06-11 04:08

## Issue 1: Fact (a) of ML9 asserts a false inclusion at the boundary case `d' = d`
Reason: The fix is a proof-reordering: restate Fact (a) over the post-state store and discharge the `{a}` delta with the subspace argument (`subspace_I(a) = s_L ≠ s_C`) that the ASN already contains in Fact (b). All needed facts (ML0 freshness, S3★ at `Σ'`, L0) are already cited; no design intent or implementation evidence is required.

## Issue 2: Coverage equality of merged vs. unit decompositions is miscited to LP-Fin Corollary
Reason: The review itself supplies the correct derivation (chain-sibling adjacency via TA5-SigValid, then ASN-0053 S3/S5 interval merge by induction over the run), and all ingredients are substrate lemmas the ASN already references. The fix is replacing a citation with that derivation — internal.

## Issue 3: The first-link V-position depth is undetermined and misattributed
Reason: The ASN must commit to how `m` is fixed in the first-link case — a convention, an operation argument, or explicit nondeterminism — and that choice cannot be derived from the ASN's own content. Gregory can say what udanax-green actually does for a document's first link, which determines whether a fixed convention is evidence-backed; Nelson can say whether the design constrains link placement within the home document or leaves it as implementation freedom.
Nelson question: Does Nelson's design attach any meaning to where in its home document a link sits in the V-stream (e.g., a required structure or ordering for link positions), or is the placement of the first link an implementation-free choice?
Gregory question: When CREATELINK adds the first link to a document with an empty link subspace, what exact V-position (tumbler depth and components, e.g. under `docISA.0.2`) does udanax-green assign it, and is that depth fixed or derived from anything?

## Issue 4: Meta-prose accretion (anti-bloat)
Reason: Purely editorial — deduplicating the store-membership disclaimer, deleting the corrective aside and forward assurance, and trimming the claims-table rows requires only the ASN's own text. No external channel needed.
