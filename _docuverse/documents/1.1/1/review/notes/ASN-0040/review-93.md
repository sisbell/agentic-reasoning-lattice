# Review of ASN-0040

The technical core is sound. I checked the inductive invariants (B1, B10, B_fin), the disjointness argument (B7), and the uniqueness/extent proofs (B8, B9) case-by-case; the case splits are exhaustive and the postconditions are genuinely established. The trace and the two B7 illustrations supply real concrete witnesses. My findings are confined to the anti-bloat patterns the `review-mode.anti-bloat` classifier asks me to surface, plus one structural-clarity item.

## REVISE

### Issue 1: Proof-hygiene editorializing in Bop freshness
**ASN-0040, Bop (Proof of well-definedness and correctness, Freshness)**: "We show a ∉ s.B *without appeal to contiguity*" and "the maximum is well-defined by NextAddress's totality argument (§NextAddress)."
**Problem**: This is reviser drift of the kind the classifier names — prose that justifies the proof's *independence from B1* (a non-circularity hygiene note) rather than advancing the freshness claim. The internal back-pointer "(§NextAddress)" re-justifies a fact already established at its definition site. The precise reader must skip the editorial aside to follow the actual two-branch argument, which stands on its own.
**Required**: Delete "without appeal to contiguity" and the "(§NextAddress)" back-pointer. State the two branches (children = ∅; children ≠ ∅) and conclude a ∉ s.B. If non-circularity between Bop and B1 needs recording at all, it belongs once in the dependency table, not inline.

### Issue 2: B7 mixes proof modes, addressing a length case its own assumption excludes
**ASN-0040, B7 (Proof), *Length split***: "Suppose, for contradiction, some x ∈ S(p, d) ∩ S(p', d')… Equal tumblers have equal length (T3), so #p + d = #p' + d'. *Length split.* If #p + d ≠ #p' + d', no shared element exists (T3)…"
**Problem**: The proof opens by assuming a shared `x` exists, which *already forces* #p + d = #p' + d' one sentence earlier. The "Length split" paragraph then reasons about the #p + d ≠ #p' + d' branch — a case the standing assumption has excluded. This is the "paragraph imagines a case the precondition already excludes" pattern: the unequal-length branch is dead inside the by-contradiction frame, and the reader must reconcile two incompatible proof modes (assume-x-exists vs. direct case analysis on lengths).
**Required**: Pick one structure. Either drop the "suppose x exists" wrapper and prove disjointness directly by cases on lengths (unequal → T3; equal → parent-length subcases), or keep the contradiction and simply note that x's existence forces equal length, then proceed to the two parent-length subcases. Do not do both.

## OUT_OF_SCOPE

### Topic 1: Uniqueness across forked (non-co-reachable) version branches
**Why out of scope**: B8 deliberately restricts to *co-reachable* acts (those on a single transition path s_init →* s) and proves uniqueness only there. Distinct baptisms on diverging branches of the version DAG are a separate guarantee requiring branch-merge reasoning beyond this ASN's growth law; the restriction is stated honestly and is not an error here.

VERDICT: REVISE
