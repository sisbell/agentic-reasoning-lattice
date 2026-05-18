# Review of ASN-0093

## REVISE

### Issue 1: Missing ContentStoreFiniteness invariant
**ASN-0093, K.α precondition**: "Subsequent emission ... `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`"
**Problem**: The substrate declares `L-fin` for the link store but has no analogous `C-fin` for the content store. The subsequent-emission rule for K.α requires `max{a' ∈ dom(C) : origin(a') = d}` to be well-defined, which depends on the set being finite. Finiteness is implicit (each transition adds at most one element starting from `Σ₀.C = ∅`), but never asserted.
**Required**: Add `C-fin: |dom(C)| < ∞` to invariants list, with discharge "Discharged: `|dom(C')| = |dom(C)| + 1`; finiteness closed under +1." Update Properties Introduced table.

### Issue 2: Forward references to non-foundation ASNs
**ASN-0093, multiple sections**: References to "ASN-0047" appear in Introduction, Scope, L1c discussion, L3 narrowing note, Open Questions, and Properties table. Reference to "ASN-0086's `Nullify`" appears in Open Questions.
**Problem**: Per review standards, only foundation ASNs (0034, 0036, 0040, 0043) may be cited by number. ASN-0047 and ASN-0086 are not foundation ASNs. While the references are explanatory rather than load-bearing, they violate self-containment.
**Required**: Either remove explicit ASN-0047/0086 numbers (refer to "higher-layer transition models" or similar abstract language) or restructure the explanatory material into a separately-marked relationship section.

### Issue 3: C1c chain exhibition imprecise
**ASN-0093, discharge table for C1c**: "Discharged at new key via the structural inc-chain (parallel to L1c chain exhibition below; first-emit case substitutes `s_C` for `s_L` in the final step)"
**Problem**: The link first-emit chain is `(d, b_C(d), b_L(d), ℓ)` with three inc steps; the content first-emit chain is `(d, b_C(d), a)` with two inc steps. These are not parallel chains differing only in the final-step subspace value — they are different lengths. The "substitutes `s_C` for `s_L` in the final step" wording mischaracterizes the structural difference (the link chain has an extra `inc(b_C(d), 0)` traversal step that the content chain lacks).
**Required**: Exhibit the C1c chain explicitly for both first-emit (`(d, b_C(d), a)` with inc(d, 2) then inc(b_C(d), 1)) and subsequent-emit cases (one-step extension by `inc(prev, 0)`). Verify per-step T10a admissibility for each step.

### Issue 4: K.α / K.λ forward-allocation clause asymmetry
**ASN-0093, K.λ precondition**: Contains explicit clause `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)` annotated "(forward allocation — T9, ASN-0034)".
**ASN-0093, K.α precondition**: Contains no analogous clause for content.
**Problem**: Both stores share the property that subsequent emissions are produced by `inc(prev, 0)`, which is strictly increasing (TA5(a)). Either the clause is a derivable consequence (and should be omitted from both preconditions for symmetry) or it is a substantive precondition obligation (and should appear in both). The current asymmetry is unjustified.
**Required**: Resolve symmetrically — either remove the clause from K.λ (rely on the inc emission rule to imply T9) or add the analogous content clause to K.α.

### Issue 5: Missing concrete worked example
**ASN-0093, throughout**: No specific scenario verifying invariants against concrete tumbler values.
**Problem**: The standards require the ASN to "verify its key postconditions against at least one specific scenario." The ASN gives generic chain exhibitions over a placeholder `d` but never instantiates with concrete numbers.
**Required**: Add a worked example. E.g., start at `Σ₀`, apply `K.σ(d)` for some specific document tumbler (e.g., `d = [1, 0, 2, 0, 5]` with `zeros(d) = 2`), then `K.α(d, a, v)` producing `a = [1.0.2.0.5.0.1.1]` (first emission), then `K.λ(d, ℓ, F, G, Θ)` producing `ℓ = [1.0.2.0.5.0.2.1]`. Verify M0, M1, C0–C2, L0–L14, L-fin at each step. Verify the L1c chain `(d, b_C(d), b_L(d), ℓ)` step-by-step under TA5/TA5a.

### Issue 6: Cross-document disjointness lemma name suggests unused derivation
**ASN-0093, Properties Introduced table**: "Cross-doc disjointness | T10a.{2,5} → T10 lemma | LEMMA"
**Problem**: The proof body cites Prefix (ASN-0034), M0, T4's zero-count argument, and T10 (PartitionIndependence) — but not T10a.2 (NonNestingSiblingPrefixes) or T10a.5 (CrossAllocatorIncomparability) directly. The lemma name advertises a derivation path through T10a.{2,5} that the proof doesn't actually traverse.
**Required**: Either rename to "Cross-doc disjointness | T10 + Prefix + M0 lemma" reflecting the actual cited foundations, or add the intermediate derivation showing how T10a.2/T10a.5 underwrite the document-level disjointness (note: the proof works directly because document-level anchors are not produced by the same T10a allocator pair the way sub-allocator outputs are).

### Issue 7: M0 source citation imprecise
**ASN-0093, Properties Introduced table**: "M0 | DocumentTumblerWellFormed | INV | Substrate, derived from K.σ precondition"
**Problem**: M0 is an invariant preserved across all transitions, not just established at K.σ. The source line addresses only the K.σ case; K.α and K.λ hold M in frame, so M0 is trivially preserved at those.
**Required**: Reword to "Substrate, established at K.σ; preserved at K.α/K.λ by frame on M." Apply the same precision to other "Source" entries that conflate "established at" with "discharged from".

### Issue 8: SubAllocatorAxiom.T10aConformance — bootstrap asymmetry
**ASN-0093, SubAllocatorAxiom.T10aConformance**: "From the second emission onward, `A_C(d)` and `A_L(d)` are T10a-conforming sub-allocators, each treating the first emission committed by SubAllocatorAxiom.FirstEmission as the base address"
**Problem**: T10a's allocator definition includes a spawning triple `(parent(A), spawnPt(A), spawnParam(A))` and a base address. The substrate's sub-allocator is "active from K.σ-time" (Exists) but only "T10a-conforming from emission 2 onward" (T10aConformance), with the first emission existing in an axiomatic bootstrap region. This split means the sub-allocator's first emission has no T10a spawning triple, leaving its relationship to T10a's allocator-tree structure unspecified. The current formulation also relies on the substrate's invocations of "T10a's GlobalUniqueness on the `A_C(d)` inc chain" without specifying whether A_C(d) is embedded in T10a's global allocator tree or stands as a free-floating T10a-conforming chain.
**Required**: Clarify the embedding. Either (a) pre-commit the first emission and treat the entire A_C(d) as T10a-conforming with `(parent(A_C(d)), spawnPt(A_C(d)), spawnParam(A_C(d)))` specified, or (b) state explicitly that A_C(d) is a "T10a-discipline-satisfying chain" (T10a.7 + T10a.1 + T10a.8) without claiming embedding in T10a's global allocator tree, and adjust the freshness arguments to cite T10a.7 (within-chain injectivity) plus the cross-document disjointness lemma rather than the global "T10a's GlobalUniqueness".

### Issue 9: K.α/K.λ parameter semantics
**ASN-0093, K.α and K.λ definitions**: Both ops list `a` (resp. `ℓ`) in their parameter signatures with preconditions that pin the value uniquely from the state.
**Problem**: Whether `a`/`ℓ` is an input the caller must compute and supply, or an output the operator derives from state, is not stated. The deterministic pinning means either reading is consistent, but a caller invoking K.α with a stale `a` (e.g., one valid in `Σ_{n-1}` but not `Σ_n`) would silently fail the precondition. Operational clarity matters for downstream ASNs and implementations.
**Required**: Add a clarifying note. Either declare `a`/`ℓ` as outputs derivable from `(d, Σ)` (then they should not appear in parameter signatures), or as inputs subject to the deterministic-pinning precondition (then state explicitly that callers are expected to compute them from current state).

## OUT_OF_SCOPE

None — the ASN's Scope section correctly bounds the substrate layer, and Open Questions appropriately defers arrangement mutation, entity stratification, provenance recording, coupling constraints, and link withdrawal to higher-layer ASNs.

VERDICT: REVISE
