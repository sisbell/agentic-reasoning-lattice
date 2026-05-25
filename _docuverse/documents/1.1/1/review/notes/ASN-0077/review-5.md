# Review of ASN-0077

## REVISE

### Issue 1: Numerical error in length of first emission
**ASN-0077, "Edge cases" / Singleton I-span**: "By SubAllocatorAxiom (ASN-0047), clauses (b)–(d), d's content sub-allocator A_C(d) is T10a-conforming with first emission [d.0.s_C.1] of length #d + 2."

**Problem**: For a document tumbler `d`, the first emission `[d.0.s_C.1]` has length `#d + 3`, not `#d + 2`. If `d = [d_1, ..., d_m]` with `#d = m`, then `[d.0.s_C.1] = [d_1, ..., d_m, 0, s_C, 1]` has `m + 3 = #d + 3` components. The error propagates to "every output of A_C(d) the length #d + 2" and "#a = #d + 2 = #b" in the same paragraph. The structural conclusion (uniform sibling length, hence `#a = #b`) survives because both quantities are equally wrong, but the numerical claim is incorrect.

**Required**: Replace `#d + 2` with `#d + 3` at both occurrences inside the singleton I-span derivation.

### Issue 2: Worked example invokes SHOWORIGIN_V with violated precondition
**ASN-0077, "A worked example" / "Transition Σ₁ → Σ₂"**: "at Σ₂, the seven-position V-span overshoots dom(M(d₃)) — ⟦σ_{1..7}⟧ ∩ dom(M(d₃)) = {[1,1,1], ..., [1,1,5]} (the remaining five) — so origins_V(Σ₂, d₃, σ_{1..7}) = {d₁}."

**Problem**: The V-span operation's precondition (vi) — `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))` — is violated at Σ₂ for σ_{1..7}: positions `[1,1,6]` and `[1,1,7]` lie in the range but not in `dom(M(d₃))`. The operation is not admissible at this input, yet the example computes and reports `{d₁}` and then draws the anti-monotonicity moral from it. The example for the *smaller* V-span σ_{1..5} (one paragraph later) is well-formed and demonstrates the same point about restriction stability under O7 — but the σ_{1..7} step is internally inconsistent with the stated operation spec.

**Required**: Either (a) reformulate the σ_{1..7} discussion to compare admissible inputs only (e.g., contrast σ_{1..7} at Σ₁ with σ_{1..5} at Σ₂ as two distinct well-formed queries); or (b) relax precondition (vi) — the F1 definition handles partial coverage naturally via intersection with `dom(M(d))`, and C1a's required premises (functionality, finite domain, common depth m ≥ 2) survive without it — and add a "partial-coverage" lemma to discharge the V-span operation on overshooting spans explicitly.

### Issue 3: O0(b) for dom(L) does not cite that K.λ is the sole modifier of dom(L)
**ASN-0077, O0 derivation, sub-claim (b) for `x ∈ dom(L)`**: "the allocation discipline of K.λ (LinkAllocation, ASN-0047) supplies the analogous correspondence: K.λ's preconditions include zeros(ℓ) = 3 ... and origin(ℓ) = d, where d ∈ E_doc is the document performing the allocation event."

**Problem**: The argument requires that every `ℓ ∈ dom(L)` entered `dom(L)` via a K.λ event — only then does K.λ's precondition `origin(ℓ) = d` propagate to a per-link semantic correspondence. This holds because every other elementary transition in ASN-0047 has frame condition `L' = L` (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ). The derivation does not cite this. L1c is later invoked as a "corroboration," but L1c only fixes the structural form of `ℓ` (descent from a document-level seed); it does not say K.λ is the sole modifier.

**Required**: Add an explicit citation that `dom(L)` is modified only by K.λ — either by listing ASN-0047's frame conditions for the other transitions, or by adding a one-line lemma. Without this step, the semantic-correspondence half of O0(b) does not close.

## OUT_OF_SCOPE

The Open Questions raised by the ASN (mixed-subspace I-span semantics; transclusion-chain visibility; native-vs-transcluded discrimination; unreachable-source behavior; historical-containment counterpart; intra-document multi-position sharing under S5) are appropriately flagged as future work and are not gaps in this ASN.

VERDICT: REVISE
