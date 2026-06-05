# Review of ASN-0100

This ASN is heavily revised and substantially rigorous. The substrate decomposition, the three-region effect, the invariant verification, the projection-shift derivation (INS.proj), and the two wp computations are all carefully argued, and the boundary cases (j=0, append, empty document, re-insertion after clearance) are genuinely covered rather than hand-waved. The remaining issues are localized: duplicated proof obligations between the discovery and verification passes, and one imprecise component claim.

## REVISE

### Issue 1: S8a / S8-depth for Insertion positions is proven three times

**ASN-0100, §Effect Two vs. §Post-state V-position well-formedness vs. §Sequential structure (empty case)**: Effect Two already gives a TumblerAdd-based *proof*, not just an assertion: "TumblerAdd at action point m_C copies p's leading all-1 components and advances only the final, strictly positive component, so shift(p, k) inherits p's S8a (zero-freedom, depth ≥ 2, positivity)." The §Post-state section then re-derives the same conclusion in full with a k=0 / k≥1 split via "TumblerAdd's piecewise rule," and the empty-case sequential-structure bullet derives it a third time.

**Problem**: The note carries `review-mode.anti-bloat`, and this is the listed pattern "two paragraphs in the same document say the same thing in different words." A discovery section that embeds a proof later superseded by the canonical verification is accretion the precise reader must reconcile.

**Required**: In §Effect Two, state the placement effect (each Insertion position is `shift(p, k)`, with the run merging to block `(p, a_0, n)`) and defer S8a/S8-depth to the verification section. Keep the full proof once, in §Post-state V-position well-formedness.

### Issue 2: "leading … components … which are all 1" is imprecise

**ASN-0100, §Sequential text-subspace structure (S8a derivation)**: "TumblerAdd's piecewise rule … copies the leading m_C − 1 components from p, **which are all 1** (since p is a valid insertion position of the form `[s_C, 1, …, 1, p_m]` …)."

**Problem**: The leading components are `[s_C, 1, …, 1]` — position 1 is the subspace identifier `s_C`, not the literal `1`. The cited form `[s_C, 1, …, 1, p_m]` displays `s_C` as a distinct symbol, contradicting "all 1" unless one silently invokes `s_C = 1` (SubspaceConventionAxiom), which is not invoked here. Moreover S8a only needs the leading components to be *nonzero and positive*, not equal to 1 — the stronger claim is both unnecessary and not established by the surrounding argument.

**Required**: Replace "which are all 1" with "all of which are strictly positive (position 1 is `s_C ≥ 1`, the rest are `1`)," which is what S8a (zero-freedom, positivity) actually consumes.

## OUT_OF_SCOPE

(none — the note correctly bounds itself to content-subspace INSERT and lists link-subspace insertion, COPY, DELETE, REARRANGE, version derivation, and replication as out of scope without smuggling claims about them.)

VERDICT: REVISE
