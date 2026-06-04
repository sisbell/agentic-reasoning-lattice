# Review of ASN-0091

## REVISE

### Issue 1: Mis-citation in clause (iv) subspace-preservation discharge
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges" table, clause (iv) row**: "every affected-range position `v` has the cut subspace `S` (by CS3), and R-PPERM/R-SPERM map it to a position of the form `c₀ + (offset)`..."
**Problem**: CS3 constrains the *cuts* `cᵢ` (`subspace(cᵢ) = S`), not arbitrary positions in the affected range. The fact that an affected-range position carries subspace `S` follows from `R-PRE(iv)` / the RegionPartition definition (the regions α, μ, β are subsets of `V_S(d)`), not from CS3. The cited premise does not establish the asserted fact.
**Required**: Replace "(by CS3)" with the correct ground — that affected-range positions lie in `V_S(d)` by R-PRE(iv), hence have subspace `S` by definition of `V_S(d)`.

### Issue 2: Vacuously-conditioned prose hedges a case CS3 already fixes
**ASN-0091, "Subspace Frame (REARRANGE_K-specific)"**: "When the cut subspace is the content subspace, the link subspace is wholly preserved..."
**Problem**: CS3 fixes `S = 1 = s_C` for every REARRANGE_K invocation, so the cut subspace is *always* the content subspace. The conditional "When the cut subspace is the content subspace" presents a perpetually-true antecedent as if the cut subspace could be otherwise, which the operation's precondition excludes. This is the imagined-case hedging pattern the anti-bloat review targets.
**Required**: State the consequence unconditionally (the link subspace is wholly preserved because REARRANGE_K's cuts are always content-subspace by CS3), or drop the hedge.

### Issue 3: Constant "Status" column carries no information
**ASN-0091, both "Claims Introduced" tables**: every row's final column reads "introduced".
**Problem**: A column whose value is identical across all rows of the document conveys nothing — it is structural-slot noise. The same applies to the multi-clause justification embedded in the RA-frame "Provenance" cell ("...which follows structurally since neither K.μ⁻ nor K.μ⁺ touches the document registry..."), which places a real derivation inside a summary table rather than in the prose discharge.
**Required**: Drop the uniform "Status" column; move the RA-frame `dom(Σ'.M)`-preservation justification into the body where RA-frame is discharged, leaving the table cell a pointer.

## OUT_OF_SCOPE

### Topic 1: Same-source fragmentation reconstitution
The first Open Question (whether two fragments of a span transcluded from the same source jointly reconstitute the original) is correctly deferred — RE-trans honestly flags this limitation rather than overclaiming. Belongs in a future ASN.

### Topic 2: Link-subspace rearrangement semantics
The second Open Question (rearrangement on the link subspace) is genuinely new territory; CS3 confines REARRANGE_K to the content subspace, so link-subspace reordering is a separate operation.

VERDICT: REVISE
