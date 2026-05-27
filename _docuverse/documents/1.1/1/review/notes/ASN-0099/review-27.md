# Review of ASN-0099

## REVISE

### Issue 1: Citation error for L12a
**ASN-0099, A1 derivation in "Arrangement Independence" section**: "L12 (LinkImmutability, ASN-0093) supplies per-link value preservation conditional on `a ∈ dom(L)`, and L12a (LinkStoreMonotonicity, ASN-0093) supplies `dom(L) ⊆ dom(L')`"
**Problem**: L12a (LinkStoreMonotonicity) is defined in ASN-0043, not ASN-0093. The foundation claims list for ASN-0093 contains L12 (LinkImmutability), L14 (StoreDisjointness), L-fin, L0, L1, L1a, L1b, L1c, L3 — but not L12a. The L12a lemma is in ASN-0043. ASN-0093's L12 statement `(A Σ → Σ' : (A a : a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a)))` already implies the monotonicity clause via its address-persistence half, so a separate L12a reference is functionally redundant when citing ASN-0093.
**Required**: Either correct the citation to "(ASN-0043)" for L12a, or eliminate the L12a citation entirely and rely solely on L12's persistence clause from ASN-0093 (which supplies the monotonicity needed for the subsequent argument that "neither pins down equality `Σ'.L = Σ.L` directly").

### Issue 2: F10's general nesting structure derivation is compressed for non-trivial cases
**ASN-0099, F10 "Verifying F10 across a version extension" paragraph closing sentence**: "the general claim — that any version's link block nests strictly between its parent's and the parent's sibling's — is the iterated application of the same case analysis to each pairwise comparison, with no additional derivation needed beyond the pairwise machinery above."
**Problem**: The pairwise machinery covers (siblings via T1 case (i), versions via T1 case (ii)) over three specific document configurations. The general claim quantifies over arbitrary document trees with mixed branching (version-of-version, sibling-of-version, multi-account chains). "Iterated application" is asserted but not derived — in particular, the transitivity argument that chains the C(n,2) pairwise inequalities into a total order on n link blocks is not exhibited. Since T1 is already a strict total order on T, the iteration reduces to T1's own trichotomy plus the pairwise lemma that anchor ordering tracks document ordering — but this reduction is not stated.
**Required**: Add one sentence noting that the link-address ordering inherits from T1's total order on T (restriction of a strict total order to any subset is again a strict total order), with the pairwise machinery establishing that each restriction respects document hierarchy. This closes the "iteration" claim by anchoring it in T1's foundational properties rather than leaving it as informal extrapolation from a three-document case.

## OUT_OF_SCOPE

### Topic 1: Closed-world reading axiomatization
**Why out of scope**: A1's discharge at K.μ⁺, K.μ⁻, K.ρ rests on a "closed-world reading" of the substrate effect-clause convention that the substrate ASNs (ASN-0047, ASN-0093) do not explicitly axiomatize. The ASN is honest about this being an interpretive convention grounded in Nelson's design intent and Gregory's implementation evidence. Lifting this convention to a substrate-level axiom belongs in a future foundation revision, not in this ASN. The current handling — explicit framing as a load-bearing interpretive choice with explicit grounding — is acceptable specification practice.

VERDICT: REVISE
