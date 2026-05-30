# Review of ASN-0058

I worked through every proof — M0 through M16, the M-int interval lemma, the canonical-decomposition uniqueness argument (M12/M12a/M12b), and the content-reference resolution chain (C0–C2). The mathematics is sound: the split/merge duality, the maximal-run partition, the origin-invariance lemma, and the width-preservation count all check out, including the boundary cases (n=1 in M0, k=0 via OrdinalShiftBase throughout, empty arrangement in M2, restriction boundaries in C1a). The two worked examples correctly exercise the key postconditions.

I found one extraneous reference that the active anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: M2 appends an unused decomposition-uniqueness pointer that conflates two distinct "uniqueness" notions
**ASN-0058, M2 (DecompositionExistence), final paragraph**: "its *existence* half ... is B1 (Coverage), and its *uniqueness* half ... is B2 (Disjointness); uniqueness of the maximal-run decomposition is S8(c)."
**Problem**: M2's proof obligation is *existence* of some block decomposition — it produces the maximal-run family and discharges B1, B2, B3. The appended clause "uniqueness of the maximal-run decomposition is S8(c)" plays no role in establishing existence; it is an extraneous reference dropped into a structural slot. Worse, it sits one semicolon away from the legitimate "uniqueness half ... is B2," where "uniqueness" means *positional* uniqueness (each V-position in at most one extent). S8(c) is *decomposition* uniqueness — an entirely different statement, belonging to M3/M12, not M2. Putting the two "uniquenesses" in the same sentence invites a reader to conflate them.
**Required**: Delete the trailing clause "; uniqueness of the maximal-run decomposition is S8(c)." M2 should close at "its uniqueness half ... is B2 (Disjointness)." If decomposition uniqueness is worth a pointer, it already lives where it belongs (M3, M12).

## OUT_OF_SCOPE

None. The Open Questions section correctly defers I-space-discontinuity structure, the refinement lattice, block-count bounds, and depth relationships to future work rather than asserting them as claims.

VERDICT: REVISE
