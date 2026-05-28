# Review of ASN-0077

## REVISE

### Issue 1: O0 step (b) closure relies on implicit closed-world reading rather than a discharged premise
**ASN-0077, O0(b) derivation**: "by inspection of ASN-0047's transition effects and frames, K.λ is the unique transition that modifies dom(L)... K.μ⁺ and K.μ⁻ on M(d), K.ρ on R, with L outside the effect's scope"
**Problem**: ASN-0047's frame clauses for K.μ⁺ and K.μ⁻ do not explicitly assert L' = L; the conclusion "L outside the effect's scope ⇒ L unchanged" requires a closed-world frame convention. This is the load-bearing closure step that bridges L1c (chain seed = origin tumbler) with K.λ's precondition (chain seed = allocating document); the entire semantic correspondence claim for dom(L) addresses in O0(b) rests on it. The argument enumerates each transition's behavior but appeals to convention rather than a discharged premise.
**Required**: Cite a labeled foundation invariant — e.g., L12 from ASN-0043, which ASN-0047's P3 invokes as a conjunct — that directly establishes link-store append-only behavior across the full transition vocabulary. The frame enumeration then becomes a verification, not the load-bearing inference.

### Issue 2: Singleton I-span argument for case #b < #a omits the trichotomy step that excludes b < a
**ASN-0077, edge case "Singleton I-span", case `#b < #a`**: "Suppose #b < #a. Equality a = b is impossible (T3 of ASN-0034 requires #a = #b), so by T1 trichotomy a < b."
**Problem**: T1 trichotomy after ruling out a = b gives `a < b ∨ b < a`, not `a < b` alone. The exclusion of `b < a` comes from the membership hypothesis `b ∈ ⟦σ_a⟧ ⇒ a ≤ b` (by T12's definition of denotation); combining this with trichotomy yields `a < b`. The derivation jumps directly to "a < b" without acknowledging the role of `a ≤ b`.
**Required**: Insert the intermediate step: "Since `b ∈ ⟦σ_a⟧`, by T12 we have `a ≤ b`, i.e., `a < b ∨ a = b`. Equality is ruled out by `#a ≠ #b` via T3, leaving `a < b`."

### Issue 3: O11 sub-case (a) cross-state depth identification assumes subspace preservation under K.μ⁺ implicitly
**ASN-0077, O11 (⊇) case (ii) sub-case (a), step (2)**: "K.μ⁺ extends dom(M(d)) ⊆ dom(M'(d)) while preserving prior mappings (and hence the subspace identifiers of prior V-positions; the extension adds, it does not relocate)"
**Problem**: The parenthetical "the extension adds, it does not relocate" carries the load-bearing claim that `subspace(v)` is unchanged across the transition for `v ∈ dom(M(d))`. This relies on `subspace(v) = v₁` being a state-independent projection — true, but left implicit. The same gap appears in O11' sub-case (b) when extending the argument across Σ → Σ'.
**Required**: Make the state-independence of `subspace(v)` explicit: "`subspace(v) = v₁` is a structural projection of the tumbler `v`'s first component; it is independent of state. Pre-state positions in `V_{s_C}(d)` therefore inhabit `V_{s_C}(d)` at Σ' as well, with their subspace identifiers preserved."

## OUT_OF_SCOPE

No items to flag — the ASN's Open Questions section appropriately defers scope extensions (cross-subspace I-span behavior, transclusion chain surfacing, distinguishing native vs transcluded content, unreachable home documents, historical containment via Σ.R, and intra-document I-address sharing).

VERDICT: REVISE
