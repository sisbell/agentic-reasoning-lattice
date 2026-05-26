# Review of ASN-0098

## REVISE

### Issue 1: LP19's hypothesis ambiguous about per-pair scope under K.μ⁺ multi-mapping

**ASN-0098, LP19 (TightEndsetBoundaryExclusion)**: "any K.μ⁺ (or K.μ⁺_L) transition Σ_n → Σ_{n+1} that extends Σ_n.M(d) by a mapping (v_new, a_new): v_new ∉ project(e, d, Σ_{n+1})"

**Problem**: K.μ⁺ in ASN-0047 may add multiple mappings simultaneously — its effect clause `dom(M'(d)) ⊃ dom(M(d))` admits any finite strict extension, with the precondition explicitly listing "newly added V-positions {v_1, …, v_k} := dom(M'(d)) ∖ dom(M(d))". When K.μ⁺ adds several mappings in one step, only the ones whose I-address was freshly K.α-allocated are governed by LP19; others (transcluded pre-existing addresses) follow LP9's general growth analysis. The current wording reads as if the K.μ⁺ adds exactly one mapping.

**Required**: Restate the hypothesis as "for each specific mapping (v_new, a_new) added by the K.μ⁺ step where a_new is the address freshly allocated by some K.α (or K.λ) step on the prefix sequence Σ_e →* Σ_n". Or add a sentence noting that the lemma applies per-pair when multiple mappings are added.

### Issue 2: Empty endset projection statement lacks domain qualification

**ASN-0098, "The Projection Operation" section**: "The projection of the empty endset is uniformly empty: `project(∅, d, Σ) = ∅` for every `d, Σ`, since `coverage(∅)` is the empty union over an empty index set."

**Problem**: The projection function is defined only when `d ∈ dom(Σ.M)` (per the convention stated immediately above). The universal "for every d, Σ" is imprecise — project is undefined for d ∉ dom(Σ.M). The same imprecision affects the next sentence's "for every d, Σ" qualifying the empty-arrangement projection.

**Required**: Qualify as "for every d ∈ dom(Σ.M), Σ" in both sentences, or add a parenthetical noting that the equality holds wherever project is defined.

### Issue 3: Achievability subsection redundant with LP-Fin Corollary

**ASN-0098, "Boundary and Width Behaviour" section, Achievability subsection**: The four cross-document interference sub-cases (same-document cross-subspace × 2, non-nesting documents, descendant documents, ancestor documents) re-derive the structural content of LP-Fin Corollary.

**Problem**: LP-Fin Corollary already establishes that `F ∩ [s, s ⊕ ℓ) = {[d_0, 0, X, k] : k_s ≤ k < k_s + n}` — every F-candidate has the span's subspace identifier and origin. The four sub-cases in Achievability are showing why chain elements from other (d', subspace) pairs don't fall in the interval — exactly what LP-Fin Corollary concludes. The redundancy is not flagged, and a reader following the corollary cannot tell whether the sub-cases carry additional load.

**Required**: Either (a) state explicitly at the head of the Achievability subsection that these cross-document arguments are consequences of LP-Fin Corollary, presented for motivational clarity; or (b) collapse the sub-cases into a single sentence citing the corollary plus the emission-frontier choice `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)`. Otherwise the relationship between LP-Fin Corollary and the Achievability arguments is unclear.

### Issue 4: LP12a second boundary case forward-references LP-Fin Corollary

**ASN-0098, "Discoverability and Survival" section, LP12a's second boundary case**: "When `n'_{s_C} = 0` but `n'_{s_L} > 0` ... The argument requires structural machinery ... developed in the 'Boundary and Width Behaviour' section below; we defer the derivation to the corollary application 'LP12a Boundary Case Application' that immediately follows LP-Fin Corollary's statement there."

**Problem**: The forward reference is flagged but creates non-locality — a reader checking LP12a's claims must scan forward past LP13, LP16, LP17, LP18, and the entire LP-Fin development before finding the discharge. The discharge itself appears mid-section under a labeled paragraph, not as a clearly delineated lemma.

**Required**: Either (a) move LP-Fin and LP-Fin Corollary earlier (e.g., into a preliminaries section before Discoverability) so LP12a's boundary case can be discharged in place; or (b) label the deferred discharge as a separate corollary (e.g., LP12b) so it appears in the master claims table and the forward reference points to a tracked label.

## OUT_OF_SCOPE

### Topic 1: Multi-step lifting of LP9–LP11

**Why out of scope**: The single-step lemmas suffice for LP18's resurrection argument (which composes Store Monotonicity★ and LP3★). A general multi-step LP9★/LP10★/LP11★ would be useful for higher-level reasoning but isn't load-bearing for the claims of this ASN.

### Topic 2: Reverse-discovery primitive, V-order/I-order invariants, cross-link discovery, document homology, fork composite invariants

**Why out of scope**: All listed in Open Questions; appropriate as future ASNs.

VERDICT: REVISE
