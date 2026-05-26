# Review of ASN-0091

## REVISE

### Issue 1: K.μ~-FIX misattributed to ASN-0084

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "ASN-0084's K.μ~-FIX (DomainFixity) discharges RA-dom" and later "For REARRANGE_K specifically, this equality is not axiomatic but lemma-derived — ASN-0084's K.μ~-FIX establishes it from D-SEQ★ together with π's bijectivity."

**Problem**: K.μ~-FIX (DomainFixity) is defined in ASN-0047, not ASN-0084. Looking at the foundation claim lists, K.μ~-FIX appears under "ASN-0047 Claim Statements"; ASN-0084's claim list contains R-PRE, R-PIV, R-SWP, R-PPERM, R-SPERM, R-NS, R-COMM, R-BLK, R-RI, R-SP, R-DISP, R-FRAME-P/S, but no K.μ~-FIX. D-SEQ★ is also in ASN-0047, not ASN-0084.

**Required**: Correct both citations to "ASN-0047's K.μ~-FIX." Citation accuracy is load-bearing for foundation traceability.

### Issue 2: RE-trans cites RE-ran for multiset preservation

**ASN-0091, "Cross-Document Transclusion Preserved"**: "By RE-ran, the multiset of foreign addresses `{a ∈ ran(Σ.M(d)) : origin(a) ≠ d}` is preserved."

**Problem**: RE-ran preserves `ran(Σ.M(d))` as a set, not as a multiset. Multiplicities — including multiplicities of transclusion entries — are preserved by RE-μ, not RE-ran. The same omission appears in the Claims table provenance for RE-trans: "abstract (from RE-ran + RE-other + RE-C + RE-origin)" — RE-μ is missing from the dependency list, yet the statement of RE-trans explicitly claims "with the same multiplicity."

**Required**: In both the prose and the table, add RE-μ to the dependencies for RE-trans's multiplicity claim.

### Issue 3: Multistep composition formula imprecise for mixed-target sequences

**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"**: "RE-proj★: `project(e, d, Σ_n) = (π_n ∘ ⋯ ∘ π_1)(project(e, d, Σ_0))`, with the composed bijection acting on the projection set."

**Problem**: The formula assumes every step in the sequence `Σ₀ →_R Σ₁ →_R ⋯ →_R Σ_n` targets the same document d. If some step targets d' ≠ d, then π_i for that step is a bijection on `dom(M(d'))`, not on `dom(M(d))`, and cannot be composed into a chain acting on `project(e, d, Σ_0)`. By RE-other applied to d at such a step, the projection at d is unchanged — so the correct formula should compose only the bijections from steps targeting d (treating the rest as identity).

**Required**: Either restrict RE-proj★ to single-target sequences, or define π_i explicitly as `π_step_i` when step i targets d and `id_{dom(M(d))}` otherwise. The current phrasing is ambiguous on this point.

### Issue 4: RE-proj reverse-inclusion proof is terse

**ASN-0091, "Projection Transports Along π"**: "The reverse inclusion holds by π⁻¹, which exists because π is a bijection on a finite set."

**Problem**: The forward direction is laid out in three steps; the reverse direction is a one-liner. The proof works but the reader has to reconstruct it: for `v' ∈ project(e, d, Σ')`, set `v = π⁻¹(v')`; then `v ∈ dom(Σ.M(d))` (RA-dom + bijectivity), `Σ'.M(d)(v') = Σ.M(d)(v) ∈ coverage(e)` (RA-π + RE-cov), so `v ∈ project(e, d, Σ)` and `v' = π(v) ∈ π(project(e, d, Σ))`. Finiteness is not what licenses π⁻¹ here — bijectivity does, on any set. The parenthetical is misleading.

**Required**: Spell out the reverse direction in two lines, and remove the "on a finite set" qualifier (finiteness is invoked later for the cardinality argument in RE-μ, where it belongs).

## OUT_OF_SCOPE

### Topic 1: Behavior of REARRANGE on the link subspace

**Why out of scope**: ASN-0084's CS3 hardcodes the cut subspace to s_C, so REARRANGE_K cannot act on the link subspace. The ASN correctly flags this as an Open Question for a future operation; it is not a gap in ASN-0091.

### Topic 2: Reachability — which arrangement permutations are realizable by finite compositions of REARRANGE_K invocations?

**Why out of scope**: This is the final Open Question. Characterising the orbit of REARRANGE_K under composition is a separate algebraic question that does not affect any RE-* claim in this ASN.

### Topic 3: Quantitative bounds on run-decomposition cardinality changes

**Why out of scope**: RE-frag establishes the existential — cardinality can increase. Bounding the increase per invocation is a separate metric question that ASN-0091 does not attempt and is correctly listed under Open Questions.

VERDICT: REVISE
