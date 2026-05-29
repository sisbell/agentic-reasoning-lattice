# Review of ASN-0040

## REVISE

### Issue 1: Bop's preservation paragraphs duplicate the dedicated invariant proofs

**ASN-0040, Bop "Proof of well-definedness and correctness"**: "**B1 preservation.** ... The registry-wide preservation across all namespaces ... is carried by §B1" and "**B10 preservation.** ... The registry-wide preservation is carried by §B10."

**Problem**: §B1, §B10, and §B_fin each carry full inductive proofs of preservation. Bop's "Monotonicity (B0) / B1 preservation / B10 preservation" paragraphs restate those conclusions and then defer downstream ("carried by §B1", "carried by §B10"). The Properties table already records "Bop correctness follows as corollary" of B1. The reader must skip past summary paragraphs that point elsewhere to find the actual argument — multiple paragraphs deferring to the same downstream location.

**Required**: Bop should carry only what is genuinely local — well-definedness and freshness. Drop the B0/B1/B10 preservation paragraphs (or reduce to a one-line "invariant preservation is established in §B1/§B10/§B_fin").

### Issue 2: Bop FRAME duplicates the Formal Contract Frame line with a within-document pointer

**ASN-0040, Bop**: "FRAME: s.B is modified as specified by POST; other components are left to the ASNs that introduce them (see the Formal Contract *Frame:* line)."

**Problem**: The Formal Contract *Frame:* line states the same content at length ("Only s.B is modified ... this ASN makes no commitment about other components"). The operation-spec FRAME and the contract Frame say the same thing, and the parenthetical "see the Formal Contract Frame line" is a redundant within-document pointer.

**Required**: State the frame once; remove the cross-pointer.

### Issue 3: hwm "Justification" anticipates and duplicates B2

**ASN-0040, hwm Justification**: "the next allocation target: since children occupy exactly the first m positions of S(p, d), the next unoccupied position is c_{m+1}."

**Problem**: This is exactly B2 (High Water Mark Sufficiency), which immediately follows with its own two-case proof. The hwm justification needs only the "sufficient statistic for the maximum" claim; deriving the *next* address pre-empts B2 and says the same thing twice in adjacent slots.

**Required**: Trim hwm's justification to the maximum-identification claim; let B2 carry the next-address derivation.

### Issue 4: B1 sub-case C and B6 necessity sub-case (b) duplicate the (p′, 2) validity check

**ASN-0040, §B1 sub-case C**: "We verify that p' satisfies T4 and (p', 2) satisfies B6. For T4: p₁ > 0 ... B6(iii): zeros(p') + (d' − 1) = zeros(p') + 1 ≤ 3."
**ASN-0040, §B6 necessity (b)**: "We verify (p', 2) is itself B6-valid: p' satisfies T4 ... zeros(p') + 1 = zeros(p) ≤ 3."

**Problem**: The same verification — that removing a sole trailing zero yields a T4-valid parent with (p′, 2) satisfying B6 — is performed in two different sections in nearly identical words. Two paragraphs saying the same thing.

**Required**: Establish the (p′, 2) validity once (it is most natural in B6, where the necessity argument originates) and have §B1 sub-case C cite it rather than re-derive it.

### Issue 5: B0a closes with a restated partition / exhaustiveness claim

**ASN-0040, B0a**: "Each `op ∈ Σ` is in exactly one class by its symbol: the baptismal class is the named family `{baptize(p, d) : B6(p, d)}`, and the s.B-frame class is its complement in Σ."

**Problem**: The opening sentence ("Σ partitions into two classes") plus the two bullets already define and name both classes. The closing sentence re-asserts partition exhaustiveness ("exactly one class") and re-names the two classes — an exhaustiveness restatement that adds no content.

**Required**: Delete the closing sentence; the partition and its complement are already fixed by the bullets.

### Issue 6: The allocated-set aside duplicates an Open Question

**ASN-0040, "Relationship to ASN-0034's allocated set"**: "This ASN neither assumes nor establishes `allocated(s) ⊆ s.B`; the activation discipline that would force it is left open (see Open Questions)."

**Problem**: The Open Questions list already contains "Under what activation discipline does `allocated(s) ⊆ s.B` hold...". The aside and the open question carry the same deferral; the aside's "(see Open Questions)" is the deferral pointer pattern.

**Required**: Keep the open question; reduce the aside to the single factual line that the inclusion is neither assumed nor established, without the forward pointer, or drop it.

## OUT_OF_SCOPE

### Topic 1: Parent-baptized prerequisite
The note explicitly defers "no parent-baptized prerequisite is imposed" to Tumbler Ownership. Correctly scoped — not an error here.

VERDICT: REVISE
