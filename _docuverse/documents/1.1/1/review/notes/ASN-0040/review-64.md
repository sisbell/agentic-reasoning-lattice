# Review of ASN-0040

This ASN has clearly been through many revision cycles. The core mathematics is sound: the contiguous-prefix induction (B1), the high-water-mark reduction (B2), namespace disjointness (B7), and the necessity analysis in B6 are thorough, with genuine attention to edge cases (empty children, the singleton `[0]`, trailing-zero parents). My findings are concentrated in stale references and accumulated meta-prose, consistent with the anti-bloat classifier on this note.

## REVISE

### Issue 1: Dangling case reference in the worked trace
**ASN-0040, "A baptism traced" — Step 3**: "B7: S([1], 2) elements have length 3; S([1, 0, 1], 2) elements have length 5 — **Case 1 disjointness**."
**Problem**: B7's proof labels its cases *Length split*, *Equal-length parents*, and *Unequal-length parents* — there is no "Case 1." This is a reference to a case label that no longer exists (almost certainly relocated from a prior numbered-case version of B7). A reader cross-checking the trace against B7 cannot resolve "Case 1."
**Required**: Replace with the surviving label, e.g. "the *Length split* case of B7," or drop the case citation.

### Issue 2: The d=1 trailing-zero exception is explained in three places
**ASN-0040, S2 / "Remark (Namespace disjointness)" / B6 necessity sub-case (b)**: The same fact — that a trailing-zero parent at `d = 1` produces a *T4-valid* stream identical to a B6-valid `(p′, 2)` namespace, so B6(i) is retained for injectivity rather than T4 — is established once (S2), motivated again (the Remark), and then re-asserted as a carve-out in B6 necessity ("the d = 1 case is the S2 exception").
**Problem**: This is the flagged accretion pattern: multiple sections in different words deferring to the same point. S2 is the load-bearing lemma; the rest restates it. A precise reader must reconcile three statements of one carve-out.
**Required**: Keep S2 (the lemma) and the single-clause carve-out in B6 necessity. Fold the Remark's *content* (the `[1,0]`/`(p′,2)` worked instance) into S2 if it adds value; remove the duplicated narration.

### Issue 3: Design-rationale meta-prose in the S2 Remark
**ASN-0040, "Remark (Namespace disjointness)"**: "...Excluding trailing-zero parents at d = 1 (folded into B6 condition (i)) keeps the namespace map injective on B6-valid pairs. **This is a design motivation for retaining condition (i) where T4 does not force it, not a T4-necessity step.**"
**Problem**: This is prose explaining *why a constraint is needed* rather than advancing the argument — the anti-bloat pattern. The worked example (`p = [1,0]`, `c₁ = [1,0,1]`) is legitimate (a concrete instance), but the surrounding justification essay is the kind of defensive framing that compounds across cycles.
**Required**: Reduce to the operative fact: B6(i) is necessary for T4 except at the `d = 1` trailing-zero case (S2), where it is retained to keep the namespace map injective. One sentence, stated where B6(i) is defined.

### Issue 4: B0★ full induction for a trivial monotonicity lemma
**ASN-0040, B0★ (Multi-step Irrevocability)**: A six-line base/step induction to lift `s.B ⊆ s'.B` from single transitions to the reflexive-transitive closure.
**Problem**: This is the standard "monotone single-step relation extends to its transitive closure" fact; the full induction is boilerplate for a property used exactly once (B8 Case 1). The labeled corollary is fine; the spelled-out proof is filler.
**Required**: Compress to a one-line citation of monotonicity under transitive closure, or inline the fact at its sole use site in B8.

## OUT_OF_SCOPE

### Topic 1: Cross-branch baptism uniqueness
B8 restricts to *co-reachable* acts and notes cross-branch uniqueness is "unaddressed." This is correctly scoped, not a gap: two divergent histories can independently baptize the first child of `[1]` at depth 2 and both compute `[1,0,1]`, so cross-branch uniqueness is *false* and cannot be strengthened. The inline note is the right treatment — no action needed, and not a defect.

### Topic 2: Ghost/structural-position distinction (B3 and Open Questions)
B3's `Occupied` forward requirement correctly defers content storage to a future ASN; the "could-hold-content vs. cannot" refinement raised in Open Questions belongs there, not here.

VERDICT: REVISE
