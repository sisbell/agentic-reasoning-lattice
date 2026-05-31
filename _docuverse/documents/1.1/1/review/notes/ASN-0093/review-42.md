# Review of ASN-0093

## REVISE

### Issue 1: C1b/L1b subsequent-emit discharge justifies element-field depth by length alone

**ASN-0093, Discharge matrix, C1b row (K.α) and L1b row (K.λ)**: "subsequent-emit branch has `a = inc(a_prev, 0)`, where `#a = #a_prev` by length preservation (TA5(c)), so `#E(a) = #E(a_prev) ≥ 2` by the IH on `a_prev`."

**Problem**: `#E(a) = #E(a_prev)` does *not* follow from `#a = #a_prev` alone. Two equal-length tumblers can have different element-field depths if their zero positions differ (`#E` is measured from the position after the third separator). The step needs the zeros — and their positions — preserved, so that the element-field boundary is unchanged. That is supplied by TA5(b) (`k = 0` preserves every position except `sig`) together with the T4-validity placing `sig(a_prev) = #a_prev` in the element field — exactly the facts the C1 row invokes via B5a, but the C1b/L1b rows cite only TA5(c) (length + sig-increment), which is insufficient on its own.

**Required**: Cite TA5(b) (position preservation away from `sig`) and the zeros-preservation fact (B5a / TA5-SigValid placing `sig` at the terminal element-field position) so that the field boundary, hence `#E`, is shown invariant. The worked example (Step 8) already does this for `origin` via TA5(b); the matrix entry should carry the same justification rather than reducing it to "length preservation."

### Issue 2: L0 description states its provenance twice in one breath

**ASN-0093, Link store invariants, L0**: "The L-clause is from ASN-0043; the C-clause is added here as a substrate-level commitment — ASN-0043 carries only the L-clause, and the substrate pins both as joint preconditions of its sub-allocator discipline."

**Problem**: "The L-clause is from ASN-0043" and "ASN-0043 carries only the L-clause" assert the same provenance fact in different words within a single sentence — the second clause adds nothing the first did not establish. This is the kind of restated-provenance accretion the anti-bloat classifier targets.

**Required**: Collapse to one statement, e.g. "The L-clause is inherited from ASN-0043; the C-clause is a new substrate commitment, pinned as a joint precondition of the sub-allocator discipline."

### Issue 3: StoreT4Validity closes with a use-site pointer rather than content

**ASN-0093, StoreT4Validity corollary, final sentence**: "This corollary discharges the T4-validity precondition of T7 (SubspaceDisjointness, ASN-0034) wherever T7 is cited against `dom(C)` and `dom(L)`."

**Problem**: The sentence is a downstream use-site note appended to the corollary; it does not advance the corollary's claim, and the consuming sites (L14, FirstEmissionFreshness, SubsequentEmissionFreshness) already cite StoreT4Validity at their point of use. Per the forward-reference-accretion checks, this is consumer-enumeration prose in a result slot.

**Required**: Remove the trailing sentence; the corollary stands on its statement and proof, and the consumers reference it where needed.

## OUT_OF_SCOPE

### Topic 1: Element-field stratification beyond a single content/link ordinal
The Open Questions raise sub-allocator stratification for `s ≥ 3`. Coordinating a third subspace is new territory, correctly deferred — not an error here.

The substrate's proof obligations (the three primitives, the structural invariants, the freshness lemmas, cross-document disjointness, and the simultaneous induction) are otherwise complete and correctly discharged: the first-emit/subsequent-emit case split is exhaustive and mutually exclusive, the anchor construction's dependence on `s_C = 1` and `s_L = s_C + 1` is correctly localized to SubspaceConventionAxiom, and the worked example exercises both emission branches and both the prefix-comparable (`d ≺ d'`) and prefix-incomparable cross-document cases without redundancy.

VERDICT: REVISE
