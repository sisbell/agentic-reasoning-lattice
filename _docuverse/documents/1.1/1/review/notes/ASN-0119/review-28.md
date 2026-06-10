# Review of ASN-0119

This is a careful, mathematically sound note. I verified both worked examples component-by-component (the π tables, the destination tilings, the range and extent checks, the four link-footprint cases, and the two-move atomicity composite) and they all hold. The invariant discharge against ASN-0047 is genuinely complete: every conjunct of ExtendedReachableStateInvariants, the three composite-boundary properties, and P3 are accounted for, with the value-dependent S8★ correctly singled out as needing R-BLK/R-CANON rather than verbatim inheritance. The boundary analysis (empty subspace, single position, empty exterior as a degenerate *branch* not a degenerate *input*) is exactly what is wanted. The substantive findings below are about over-accreted prose in one discharge and two minor scope/slot inconsistencies — not about correctness.

## REVISE

### Issue 1: The P4a discharge credits an ingredient it does not use and carries a redundant witness clause
**ASN-0119, "What is preserved: I-address correspondence" (the P4a sub-argument)**: "That witness Σ_k persists unchanged into the extended trace to Σ', witnessing (a, d) there as well; and the content-subspace-range invariance {M'(d)(v):s_C} = {M(d)(u):s_C} keeps Σ itself an admissible witness across the appended step. **P4a is thus discharged by the R frame *together with* content-subspace-range invariance and the persistence of the pre-state's trace witnesses along the prefix — not by frame alone.**"

**Problem**: The clean discharge uses exactly two facts: `R' = R`, and P4a holding at Σ (the inductive hypothesis). A valid trace to Σ' ending in the REARRANGE step has a prefix that is a valid trace to Σ; for any `(a,d) ∈ R' = R`, P4a@Σ supplies a witness `Σ_k` in that prefix, and `Σ_k` is an earlier trace state whose arrangement `M_k(d)` is untouched by appending the step — so the witness persists. Content-subspace-range invariance is never consulted: the witness uses `M_k(d)` (or, in the special case `Σ_k = Σ`, the *pre*-REARRANGE `M(d)`), never `M'(d)`. The "Σ itself an admissible witness" clause is therefore a redundant special case (already covered by `Σ_k`), and the summary sentence mis-attributes content-subspace-range invariance as a co-equal load-bearing ingredient for P4a — when in fact it is load-bearing only for J1★ and P4★. A reader verifying which invariants P4a actually rests on must untangle this.

**Required**: Reduce the P4a discharge to `R' = R` + (P4a@Σ applied to the prefix) ⟹ witness persists. Drop the "Σ itself an admissible witness" clause and remove content-subspace-range invariance from P4a's ingredient list (it belongs to J1★/P4★, where it is correctly invoked).

### Issue 2: RA7c's region enumeration is narrower than the R-COMM region list it relies on
**ASN-0119, "Links" (RA7c)**: "project(a, i, d, Σ) ⊆ one region **(exterior, α, μ, or β)** ⟹ π preserves the footprint's run structure"

**Problem**: The body's R-COMM citation lists the regions as "the non-S subspace ({v : subspace(v) ≠ S}), the subspace-S exterior, α, μ, or β" — five regions. RA7c's parenthetical lists only four, dropping the non-S (link) subspace. A link-to-link footprint confined to `s_L` is frozen pointwise, so its run structure is trivially preserved — the conclusion holds, but RA7c as enumerated does not cover it, and "exterior" is left ambiguous as to whether it subsumes the frozen non-S subspace. The claim under-states its own validity.

**Required**: Either align RA7c's enumeration with the R-COMM list (add the non-S subspace) or state explicitly that "exterior" here means the union of all frozen regions (subspace-S exterior plus non-S subspace).

### Issue 3: Meta-prose in the claims table
**ASN-0119, Claims Introduced (REARRANGE_K row)**: "Operation imported from ASN-0084: … ; **this note builds the system-level guarantees below on top of it**"

**Problem**: The trailing clause describes the document's structure rather than stating what REARRANGE_K is — essay content in a structural slot. The "imported (ASN-0084)" status column already conveys that this row is the imported base.

**Required**: Drop the clause; the row should state the operation and its postcondition source only.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at V-position depths greater than 2
**Why out of scope**: The note explicitly scopes to depth 2 ("We make no claim about other subspaces or other depths"), matching ASN-0084's depth-2 REARRANGE_K. A deeper transposition would require a deeper imported operation; this is future territory, not a gap in this note.

### Topic 2: The five Open Questions (cross-document boundary-hood, unserialized concurrent rearrangements, content-based discovery indexing under fragmentation, prior-arrangement recoverability, closed-form displacement boundary guards)
**Why out of scope**: Each is correctly posed as a forward question and touches material reserved for other operations (transclusion, version history, link discovery) or implementation-refinement layers.

VERDICT: REVISE
