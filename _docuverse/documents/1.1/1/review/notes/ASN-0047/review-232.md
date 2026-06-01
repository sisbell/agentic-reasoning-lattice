# Review of ASN-0047

## REVISE

### Issue 1: S8★ under K.μ⁻ — the named discharge fails to establish condition (c) for the content subspace

**ASN-0047, *Amendments to existing transitions*, S8★ definition and verification matrix S8★/K.μ⁻ cell**: The S8★ definition fixes that "for the content subspace, the partition together with conditions (a) and (b) *and* condition (c) is exactly ASN-0036's S8 ... including the uniqueness of the maximal-run decomposition." But the discharge is stated as: "Under a K.μ⁻ contraction the same trivial length-1 decomposition discharges S8★ on the survivors ... the trivial length-1 fall-back ... is always available on each subspace after contraction. This is the discharge named in the S8★ K.μ⁻ verification-matrix cell." The matrix cell reads "trivial length-1 fall-back on survivors per subspace."

**Problem**: The trivial length-1 decomposition is a valid run-*cover* satisfying conditions (a) and (b), but it is **not** the maximal-run decomposition whenever a surviving content run has genuine lockstep length > 1. The ASN itself notes for the link subspace that the trivial decomposition is the route "for which uniqueness of a maximal-run decomposition is not asserted." Applying that same trivial route to the content subspace therefore establishes only existence of a run-cover, not condition (c) (uniqueness of the maximal decomposition), which S8★(s_C) explicitly requires. The discharge mechanism named is strictly weaker than the invariant it claims to preserve — proof by insufficient justification at exactly the conjunct the definition flagged as load-bearing.

**Required**: Discharge S8★(s_C) under K.μ⁻ by reapplying ASN-0036's S8 to the contracted content-subspace projection — its preconditions (S2, S3★, S8a, S8-depth, S8-fin) are preserved by restriction, as the rest of the matrix already shows — exactly as the K.μ⁺ and K.μ~ content-subspace cells do ("per-subspace projection via ASN-0036's S8"). Reserve the trivial length-1 fall-back for the link subspace, where (c) is intentionally omitted.

### Issue 2: L1b subsequent-link derivation restates the same `inc(·,0)`-modifies-only-terminal fact twice

**ASN-0047, *Extended reachable-state invariants*, L1b prose, subsequent-link case**: The paragraph first derives `zeros(ℓ) = zeros(prev) = 3` via "TA5(c) gives `#ℓ = #prev` (inc(·, 0) modifies only position sig(prev)), and TA5-SigValid gives `sig(prev) = #prev` — the modified position is the last component, which is nonzero and stays nonzero," then re-derives the element-field-length claim with "The element-field length is unchanged because `inc(·, 0)` preserves every separator position: by TA5(c) it modifies only the value at position `sig(prev)`, and by TA5-SigValid `sig(prev) = #prev` — the terminal, non-separator element-field component, which is nonzero and stays nonzero."

**Problem**: The single fact "`inc(·,0)` modifies only the terminal (= sig = length) nonzero position, so no separator is added/moved/removed" is stated and fully re-proved twice in adjacent sentences. The reader must recognize the second derivation as identical machinery to the first. This is the "two passages say the same thing in different words" pattern the anti-bloat classifier targets.

**Required**: Derive the structural fact once (`inc(·,0)` modifies only position `sig(prev) = #prev`, leaving every separator position fixed), then read off both `zeros(ℓ) = zeros(prev)` and `#E(ℓ) = #E(prev)` from it in one step.

## OUT_OF_SCOPE

None — the topics this ASN defers (link-inheritance under fork, empty-endset consumer semantics, concurrency/address-exhaustion) are already correctly routed to the Open Questions list rather than claimed here.

VERDICT: REVISE
