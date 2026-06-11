# Review of ASN-0119

## REVISE

### Issue 1: π presented as "defined by" an equation that does not determine it
**ASN-0119, "The transposition as a permutation"**: "ASN-0084 proves these define a total function whose induced map π : dom(M(d)) → dom(M(d)), defined by M'(d)(π(v)) = M(d)(v), is a bijection..."
**Problem**: The equation `M'(d)(π(v)) = M(d)(v)` does not define π. When `M(d)` is not injective — and the ASN itself exhibits exactly this in "The two streams," where every position of the affected interval maps to one I-address and the cut-point π ≠ id yet `M'(d) = M(d)` — the equation is satisfied by many bijections (in that instance, by the identity as well as the cut-point π). ASN-0084 is careful on this point: R-PPERM/R-SPERM define π as "the specific bijection determined by the cut sequence K and the region partition," with the equation as a correctness property. ASN-0119's wording inverts definition and property. The slip matters downstream: RA8a's inversion `M'(d)(u) = M(d)(π⁻¹(u))` and the worked π tables are correct only because π is the specific cut-point bijection, not an arbitrary solution of the equation.
**Required**: Replace "defined by" with "satisfying," and state that π is the cut-point-induced bijection of R-PPERM/R-SPERM (the claims-table entry for RA2 already has this right; the body and RA1's phrasing should match it).

### Issue 2: Worked examples and RA8b silently assume the I-addresses are pairwise distinct
**ASN-0119, "A worked transposition" and "Atomicity"**: "write a_k = M(d)([s_C, k]) for the I-address of the k-th byte" … "concretely M_mid([s_C,4]) = a₂, while M([s_C,4]) = a₄ and M'([s_C,4]) = a₅, so M_mid(d) ≠ M(d) ∧ M_mid(d) ≠ M'(d)."
**Problem**: Nothing in the setup asserts that a₁, …, a₅ (resp. a₁, …, a₆) are pairwise distinct. Under shared content (S5, which the ASN invokes elsewhere), `a₂ = a₄` is a legal pre-state, and then the displayed RA8b inequalities fail. The same unstated assumption underwrites the footprint computations ("its footprint is {[s_C,3]}" requires that no other position maps to a₃) and the within-region example's footprint `{ord 3, ord 5}`. The ASN proved the degenerate shared-content case is reachable, so the example's implicit distinctness is not free.
**Required**: One sentence fixing the scenario: the five (six) bytes are produced by distinct allocation events, hence a₁, …, a₅ pairwise distinct (S4 / GlobalUniqueness). RA8b's exhibited inequalities then follow as written.

### Issue 3: Universally quantified obligations discharged for the rearranged document only
**ASN-0119, transition-invariants paragraph**: "J1★ … fires for an I-address that lies in { M'(d)(v) : subspace(v) = s_C } but not in { M(d)(u) : subspace(u) = s_C }. By the content-subspace-range invariance just displayed those two sets coincide…" and "P4★ … is preserved by the same invariance: Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'."
**Problem**: J1★ quantifies over every `d ∈ E'_doc`, and `Contains_C` ranges over every document; the displayed invariance covers only the rearranged document `d`. The `d' ≠ d` case is closed by the cross-document frame (R-FRAME (b) / RA9), but the discharge never says so — `Contains_C(Σ') = Contains_C(Σ)` is asserted as if the per-`d` invariance alone gave it. The same pattern runs through the per-state preservation arguments (S2, S3★, the set-invariance package, S8★ are all argued at the rearranged `d` only, with the other-documents case left implicit).
**Required**: One explicit closure sentence: for every `d' ≠ d`, `M'(d') = M(d')` (RA9), so every per-document invariant and both range-based couplings are inherited verbatim at `d'`; the displayed arguments then cover the only document whose arrangement changes.

### Issue 4: Undefined subtraction on cut positions and V-positions
**ASN-0119, "The intervening content"**: "(ord(c₀) + w_β) − ord(c₁) = w_β − w_α = (c₃ − c₂) − (c₁ − c₀)"; **"Links"**: "The region's net translation π(v₀) − v₀ is the signed quantity…"
**Problem**: `c₃ − c₂` and `π(v₀) − v₀` subtract tumblers. The note's adopted conventions define `v + k` (ordinal shift) but no subtraction on V-position pairs; tumbler `⊖` yields a tumbler, not an integer, and signed differences are not tumbler operations at all. The first two expressions in the displayed chain are correctly written in ordinal arithmetic; the third silently switches type. ASN-0084 itself routes interval widths through `ord(·)` (TruncatedSubtraction).
**Required**: Write `(ord(c₃) − ord(c₂)) − (ord(c₁) − ord(c₀))` and `ord(π(v₀)) − ord(v₀)`, consistent with the note's own convention that widths are ordinal differences.

### Issue 5: The K.μ~-coincidence claim is asserted without assembling its discharge
**ASN-0119, "The two streams"**: "…coinciding with an admissible K.μ~ whenever the net effect is non-trivial (M'(d) ≠ M(d))."
**Problem**: Admissibility of K.μ~ requires five clauses: (i) the post-state shape package, (ii) non-trivial net effect, (iii) length preservation of π, (iv) subspace preservation, (v) link-subspace fixity. The negative direction (the value-degenerate instance no K.μ~ realizes) gets a careful witness, but the positive direction — that REARRANGE's π satisfies (i), (iii), (iv), (v) — is never connected to this claim. The materials all exist later in the note (the invariant-preservation section for (i), the depth-2 closed form for (iii), RA2a for (iv), R-NS for (v)), but "X coincides with an admissible K.μ~" is a multi-clause claim presented as a given. The asymmetry is the tell: one direction proved, the other asserted.
**Required**: Either add a parenthetical assembling the discharge (pointing (i)/(iii)/(iv)/(v) at the later derivations), or cut the coincidence analysis to the one fact the note actually uses — REARRANGE is absent from ASN-0047's atomic vocabulary and is therefore added by fiat — and let the degenerate-instance witness stand alone as the reason reduction to K.μ~ is unavailable.

## OUT_OF_SCOPE

### Topic 1: Weakest precondition for footprint run-structure preservation
**Why out of scope**: RA7c is explicitly marked sufficient-not-necessary, the worked cases exercise both sides of the boundary (a seam that heals contiguity and seams that break it), and the exact characterisation for footprints spanning two or more regions is properly deferred by the ASN's fourth open question. This is new territory, not a gap in the present claims.

### Topic 2: Concurrent rearrangements and serialization
**Why out of scope**: The atomicity section establishes single-operation semantics against one coordinate frame; commutation conditions for two unserialized rearrangements are correctly parked in the open questions.

### Topic 3: Observability of the intermediate state via RETRIEVE
**Why out of scope**: RA8b's formal content is carried entirely by the exhibited arrangement inequalities `M_mid(d) ≠ M(d) ∧ M_mid(d) ≠ M'(d)`; the RETRIEVE sentence is illustrative color for an operation (content delivery) that is explicitly outside this ASN's scope, and should not be expanded into a claim here.

VERDICT: REVISE
