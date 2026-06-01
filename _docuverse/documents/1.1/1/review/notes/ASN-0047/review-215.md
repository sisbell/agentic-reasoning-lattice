# Review of ASN-0047

## REVISE

### Issue 1: S3★ × K.μ~ verification-matrix cell is a defensive essay in a structural slot

**ASN-0047, Class (a) verification matrix, row S3★, column K.μ~**: "S3★(Σ') holds by admissibility clause (i) (precondition-carried on the candidate π); the K.μ⁻+K.μ⁺ decomposition (Steps A/B) establishes only realizability of an admissible π and non-vacuity of the admissibility filter — the latter via the π_swap witness, whose S3★ is verified independently from its swap-within-dom_C structure (see *Decomposition of K.μ~*)"

**Problem**: The matrix preamble states "each cell summarises the load-bearing argument" and the reviser has previously endorsed the matrix as a navigational index. This cell instead recapitulates the entire circularity defense (precondition-carried vs. realizability vs. non-vacuity-via-witness) — three distinct clauses of meta-argument about *how the proof is structured* rather than naming the discharge. It is the only cell in the matrix that argues with itself. Every other cell names a discharge and (where needed) a section.

**Required**: Reduce to the form used by the rest of the matrix, e.g. "by admissibility (i) (carried on π); realisability and non-vacuity in §Decomposition of K.μ~." The defensive recapitulation belongs in (and is already present in) that section.

### Issue 2: The "frontier-maximality condition … not a separate precondition clause" editorializing is repeated four times

**ASN-0047**: the same defensive aside recurs at four sites:
- FrontierEquivalence: "…which is itself the frontier-maximality condition on `t`, not a separate precondition clause…"
- K.δ case (ii), k = 0 sub-case: "the operational frontier check — this guard is itself the frontier-maximality condition on `t`, by FrontierEquivalence; there is no separate maximality clause"
- §K.δ case (ii) discharge, k = 0: "The guard `inc(t, 0) ∉ E` is itself the frontier-maximality condition on `t`, by FrontierEquivalence."
- S7d discharge, k = 0: "Freshness is the caller-checked guard `inc(t, 0) ∉ E`, which is itself the frontier-maximality condition on `t` by FrontierEquivalence."

**Problem**: Each site legitimately needs "freshness discharged by FrontierEquivalence," but the editorial clause asserting that the guard is *not* a separate precondition clause is anti-bloat noise — it answers an objection ("isn't this a hidden extra precondition?") that the reader does not raise, repeated verbatim in four sections. This is the "two paragraphs say the same thing in different words" pattern compounded across the document.

**Required**: State the guard-vs-maximality identity once, at FrontierEquivalence (or in the K.δ k = 0 sub-case). The other sites should cite FrontierEquivalence for freshness without re-litigating "not a separate clause."

### Issue 3: P4a composite-boundary matrix cell mischaracterizes the property for stale entries

**ASN-0047, composite-boundary verification matrix, row P4a**: "J1'★ at boundary supplies content-subspace witness v with M'(d)(v) = a at the post-state Σ' itself"

**Problem**: P4a's own definition is a *trace*-existential — `(E Σ_k ∈ {Σ₀, ..., Σ_n} : (E v ∈ dom(M_k(d)) : …))` — explicitly because "provenance rides on the permanent I-address and survives deletion from the current arrangement." Valid composites do produce stale entries: the *Worked example: interior content replacement* leaves `(a₂, d) ∈ R'` with `a₂ ∉ ran(M'(d)|_{s_C})`, and the K.μ⁻ delete example leaves `(a₃, d)` stale. For these entries there is **no** content-subspace witness "at the post-state Σ' itself" — the witness lives in an earlier trace state. The cell asserts a Σ'-witness for what it presents as the P4a discharge, but a Σ'-witness exists only for the `R' \ R` slice; the dominant case (entries already in `R`, including all stale ones) is discharged in the prose by induction + P2, not by J1'★ at Σ'. As written, the cell contradicts the property it claims to discharge.

**Required**: The cell must reflect both routes — `R' \ R` (Σ'-witness via J1'★) and the `R` carry-forward (IH trace witness propagated by P2) — or at minimum not assert a Σ'-witness over all of `R`. The prose already has the correct two-case argument; the matrix should not state something stronger and false.

## OUT_OF_SCOPE

None. The open questions already correctly route forward-looking topics (link inheritance under fork, address-space exhaustion, concurrency, tombstoning reconciliation) out of this ASN.

VERDICT: REVISE
