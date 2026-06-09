# Review of ASN-0120

## REVISE

### Issue 1: Exact coverage equality `coverage(eⱼ) = ρ(Rⱼ, Σ)` is false as stated
**ASN-0120, "What the endset arguments name" (ML1) and Claims table (ML8)**: "packaged as an endset — a finite set of spans whose coverage equals `ρ(R, Σ)`" and ML8 "`coverage(Σ'.L(a).eᵢ) = ρ(R_i, Σ)`".
**Problem**: `ρ(R, Σ)` is a finite set of element-level I-addresses; `coverage(e)` is a union of order-convex half-open intervals `[s, s⊕ℓ)`. An arbitrary finite set of tumblers is generally **not** the exact coverage of any finite span-set — coverage of a width-`n` ordinal span `(a, δ(n, #a))` is `{t : a ≤ t < shift(a, n)}`, which contains the descendants/zero-extensions lying between consecutive resolved addresses, not just the `n` content addresses. ASN-0053 S7 (CoveringExistence) is explicit that the guarantee is `⟦Σ⟧ ⊇ P` (covering), **not** exact. So the set equality is unsupported and, in general, untrue.
**Required**: Weaken to `coverage(eⱼ) ⊇ ρ(Rⱼ, Σ)` together with `coverage(eⱼ) ∩ dom(Σ.C) = ρ(Rⱼ, Σ)`, and supply the argument that the extra coverage points are non-content (so the discoverability intersection in ML9 is unaffected since `ran(M(d')) ⊆ dom(Σ.C)`).

### Issue 2: ML9 wp derivation skips two cases
**ASN-0120, "The invariants MAKELINK preserves" (ML9)**: "`wp(makelink(...), discoverable_from(a, d', ·)) ≡ (E i : ρ(R_i, Σ) ∩ ran(Σ.M(d')) ≠ ∅)`".
**Problem**: The substitution is presented as one step but rests on two unstated facts. (a) It replaces `coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d'))` with `ρ(R_i,Σ) ∩ ran(Σ.M(d'))` — valid only because `ran ⊆ dom(Σ.C)` collapses the coverage/`ρ` gap of Issue 1, which is never shown. (b) For the boundary case `d' = d` (the home document — exactly the annotation case ML4 highlights), `Σ'.M(d) ≠ Σ.M(d)`: K.μ⁺_L extends it, so `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {a}`. The derivation writes `ran(Σ.M(d'))` (pre-state) without justifying that `a ∉ coverage(eᵢ)` (true because `a ∈ s_L` while content coverage is `s_C`, but unshown).
**Required**: Split the wp derivation into the two facts; explicitly handle `d' = d` versus `d' ≠ d`.

### Issue 3: Missing operation precondition forcing a non-empty type resolution
**ASN-0120, "Three endsets" (ML6)**: "by L3 (ASN-0043) MAKELINK requires the type endset to be non-empty".
**Problem**: If the type endset is `ρ`-resolved like the others (ML3 UniformResolution) and the supplied type spec `R₃` resolves to `ρ(R₃, Σ) = ∅` (e.g., its V-positions are inactive), then `e₃ = ∅`, violating K.λ's L3 precondition `e₃ ≠ ∅` (ASN-0093) and leaving the operation undefined. ML6 asserts non-emptiness as a property but never surfaces it as a precondition on the type **argument**.
**Required**: State an operation precondition `ρ(R₃, Σ) ≠ ∅` (or equivalent), and address what happens when a supplied type spec resolves empty.

### Issue 4: ML2 fragmentation claim is non-observable (drift to representation)
**ASN-0120, Claims table (ML2)**: "recorded span-set cardinality is dictated by I-space fragmentation, not by the supplied V-span count".
**Problem**: Span-set cardinality is not abstractly observable: L5 (ASN-0043) exposes no span-positional accessor, and LP21 (ASN-0098, RepresentationInvariance) makes projection depend only on coverage, not decomposition. A claim about "recorded span-set cardinality" therefore has no observable abstract content — it describes the sporgl representation (correctly relegated to the implementation note), not a system guarantee.
**Required**: Restate ML2 as an observable guarantee (e.g., `ρ` recovers all referenced content regardless of contiguity or input structure), or drop it as implementation detail.

### Issue 5: `ρ` reinvents ASN-0058's `resolve`
**ASN-0120, "What the endset arguments name"**: definition of `ρ(R, Σ)`.
**Problem**: ASN-0058 already defines `resolve(d_s, σ)` as the I-address recovery from restricting `M(d_s)` to `⟦σ⟧`. `ρ` is essentially the set-union of `resolve` over a spec-set with widths/ordering discarded. Standard 7 forbids reinventing notation a foundation already defines.
**Required**: Define `ρ` in terms of `resolve` (e.g., `ρ(R,Σ) = ∪_j coverage(resolve(d_j, σ_j))`), or explicitly justify the divergence (`ρ` filters `v ∈ dom(M)` rather than requiring a well-formed content reference) and name it as a deliberate generalization.

### Issue 6: Non-foundation cross-ASN reference
**ASN-0120, "What the endset arguments name"**: "a well-formed V-span `σ_j` over it (ASN-0058, ASN-0118)".
**Problem**: ASN-0118 is not among the foundation ASNs supplied. Standard 7 forbids cross-ASN references except to verified foundations; the ASN must be self-contained with respect to non-foundation material.
**Required**: Remove the ASN-0118 dependency or inline the V-spec/V-span well-formedness conditions this ASN relies on.

### Issue 7: No concrete worked example
**ASN-0120, throughout**.
**Problem**: Standard 6 requires verifying key postconditions against at least one specific scenario. The ASN has implementation notes (Gregory's CREATELINK) but no abstract worked example checking ML0, ML1, and ML9 against a concrete state — e.g., "home `d` in document C; from-spec over A resolving to I-addresses `{a₁, a₂}`; to-spec over B resolving to `{b₁}`; verify freshness of `a`, `home(a)=d`, the recorded coverage, and discoverability from A, B, and C."
**Required**: Add one concrete scenario verifying ML0/ML1/ML9, including the discoverability-from-multiple-documents case.

## OUT_OF_SCOPE

### Topic 1: Endsets referencing the link subspace
The behavior when a from/to spec `σ_j` lies in the `s_L` subspace (so `Σ.M(d_j)(v) ∈ dom(L)`, breaking `ρ ⊆ dom(C)`) is raised as an open question and belongs to a future ASN, not a revision here — provided Issue 3's precondition work notes the content-subspace assumption.

### Topic 2: Empty from/to resolution semantics
What an empty (non-type) endset means for a link's connection is correctly deferred as an open question; it is new territory, not an error in this ASN.

VERDICT: REVISE
