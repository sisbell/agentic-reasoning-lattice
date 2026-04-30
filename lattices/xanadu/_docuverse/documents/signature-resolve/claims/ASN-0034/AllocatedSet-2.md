# Signature Resolve — ASN-0034/AllocatedSet — run 2

*2026-04-30T20:13:09Z*
*Model: sonnet*

## Output

INTRODUCES:
- bullet: "- `𝒮` — state space of the allocation system; each s ∈ 𝒮 is a pair (Act(s), nₛ) of activated-allocator set and sibling-count function"
- bullet: "- `Σ` — transition vocabulary; the collection of admissible partial functions op : 𝒮 ⇀ 𝒮 whose application shapes are constrained by the admissibility axiom"
- bullet: "- `Act(·)` — activated-allocator set component of a state; Act(s) ⊆ 𝒯 is the set of allocators activated in s, computed as a projection of s alone"
- bullet: "- `nₛ(·)` — sibling-increment count component of a state; nₛ(A) ∈ ℕ is defined for each A ∈ Act(s) and undefined for A ∉ Act(s)"
- bullet: "- `activated(·,·)` — activation predicate; activated(A, s) ≡ A ∈ Act(s), total on 𝒯 × 𝒮, computed from s without induction over transitions"
- bullet: "- `domₛ(·)` — realized domain of allocator A at state s; the inc(·,0)-chain initial segment {t₀,…,t_{nₛ(A)}} when activated(A,s), else ∅; total on 𝒯 × 𝒮"
- bullet: "- `allocated(·)` — allocated set at state s; ⋃ { domₛ(A) : activated(A, s) }, the bridge between T10a's abstract dom(A) and the state-indexed realized domains"
- bullet: "- `s₀` — initial state constant; fixed by Act(s₀) = {root} and nₛ₀(root) = 0, giving allocated(s₀) = {t₀}"
- bullet: "- `→` — state transition relation on 𝒮; s → s' denotes the pair (s, op(s)) for some op ∈ Σ with s ∈ dom(op)"

REMOVES: []
