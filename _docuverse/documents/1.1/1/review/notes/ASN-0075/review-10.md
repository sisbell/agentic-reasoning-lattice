# Review of ASN-0075

## REVISE

### Issue 1: Notational typo in D-ACT Case 3 proof
**ASN-0075, D-ACT proof, Case 3 (Different origin)**: "T1 lexicographic comparison applied to d and d' (...) fixes some position p at which every emission of A_C(d) carries d's component and every emission of A_C(d') carries d's component, with both prefixes agreeing on positions before p."

**Problem**: The second instance of "d's component" should be "d′'s component" (the component of d′ at position p, i.e., d′_p). As written, both allocators carry the same component d_p at position p, which would mean their emissions agree at p — directly contradicting the divergence-based separation argument the case is trying to establish. The case relies on d_p ≠ d′_p at the divergence position p to conclude that every A_C(d) emission is T1-comparable (and strictly ordered) against every A_C(d′) emission.

**Required**: Replace the second "d's component" with "d′'s component" (or equivalent notation distinguishing d_p from d′_p). Without the fix, the central comparison step in Case 3 is incoherent in writing even though the intended argument is sound.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
