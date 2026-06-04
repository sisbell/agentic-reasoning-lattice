# Review of ASN-0087

The technical content here is strong: the composite decomposition is justified, the precondition derivation for `ℓ ∉ ran(M(d))` is complete, the worked example checks out arithmetically, the D-CTG★ contiguity proof is done at arbitrary depth `m ≥ 2` (not assuming `m = 2`), and the invariant-preservation pass covers every conjunct of ASN-0047's `ExtendedReachableStateInvariants`, the composite-boundary properties, and the transition invariants. I found no correctness gap. The findings below are the meta-prose/forward-reference accretion this note is flagged to surface, plus one out-of-scope topic.

## REVISE

### Issue 1: "Scope" meta-paragraph explains proof strategy rather than advancing it
**ASN-0087, Invariant Preservation / Per-State Invariants**: "*Scope of the arrangement-indexed obligations.* The invariants S2, S8a, D-CTG★, D-MIN★, and D-SEQ★ are universally quantified over documents... Every conjunct at a document d' ≠ d is preserved by frame... Only the link-subspace conjunct at d... requires argument; the discharges below address exactly that conjunct."
**Problem**: This is a "Scope"-labeled sub-paragraph (one of the named accretion patterns) that narrates proof strategy. The load-bearing content is a single sentence: at `d`, only the link-subspace conjunct needs proof; everything else (other documents, the content subspace at `d`) is frame-preserved. The surrounding apparatus is meta-prose the reader works around to reach that reduction.
**Required**: Condense to the one load-bearing sentence; the per-conjunct frame argument can live inline where each conjunct is discharged.

### Issue 2: Atomicity section re-derives the wp discoverability delta
**ASN-0087, Atomicity**: "Because K.λ's frame fixes M, Σ_mid.M = Σ.M, so the discoverability difference between Σ_mid and Σ' is exactly the Σ → Σ' delta already computed: it agrees for every d_target ≠ d (M-WP, Case 1), and for d_target = d the two values agree unless some endset reflexively covers ℓ (M-Reflexive)."
**Problem**: This restates the M-WP Case 1 / Case 2 conclusions already derived in the *Weakest Precondition* section. The only non-redundant point is that the visibility change is localized to the K.μ⁺_L step (since K.λ leaves `M` fixed). The rest is duplication of a downstream-cited result.
**Required**: Reduce to the single new observation — the discoverability change occurs entirely at K.μ⁺_L, not K.λ — and drop the re-derivation of the Case 1/Case 2 split.

### Issue 3: Open question Q4 is substantially answered in the body
**ASN-0087, Open Questions**: "When MAKELINK's endsets reference content in documents not yet allocated, what discoverability properties become available once that content is later created?"
**Problem**: The body already answers the core of this. *Permanence of the Binding* cites LP17 (orphaned links remain in `dom(L)`) and LP18 ("it becomes discoverable again when any document later transcludes content covered by its endsets"), and the *Side Effects* section derives the resurrection pattern explicitly (`a* = ℓ`, LP18). Posing it as open re-opens derived material. Q1 ("well-formedness for endsets referencing unallocated addresses") and Q6 ("never-allocated type endset, discoverability in the limiting case") are two further facets of the same "endset → unallocated address" theme; the three should be consolidated to whatever genuinely remains open.
**Required**: Remove or sharpen Q4 to the part not already discharged by LP17/LP18 (e.g., the cross-document allocation→arrangement chain, if that is the intended residue); merge the overlapping Q1/Q6 framing.

## OUT_OF_SCOPE

### Topic 1: Type-slot participation in the discoverability disjunct
The discoverability mechanism `discoverable_from(ℓ, d, Σ') ⟺ (E i : 1 ≤ i ≤ |Σ.L(ℓ)| : coverage(eᵢ) ∩ ran(M(d)) ≠ ∅)` quantifies over **all** slots, including the type slot `e₃`. Since L3/L4 do not forbid a type endset from covering content addresses, a link can be surfaced by a "what links touch this content?" query through its type slot alone, even when no content endset reaches the queried content. The worked example sidesteps this by choosing `τ ⋠ x`, but the general tension between the "What Is Indexed?" framing and the unfiltered LP12 disjunct is a refinement question.
**Why out of scope**: LP12 is a foundation (ASN-0098) mechanism; whether discoverability should distinguish content slots from type slots is a future modeling decision, not an error in this ASN. ASN-0087 inherits and applies LP12 faithfully.

VERDICT: REVISE
