# Review of ASN-0105

## REVISE

### Issue 1: Subspace-confinement argument needs an action-point constraint the precondition does not impose

**ASN-0105, Preconditions §3 / "Confinement is load-bearing"**: "With `subspace(s) = s_C` and the span level-uniform at depth `m`, foundation **T5** (ContiguousSubtrees, prefix `[s_C]`) gives that every depth-`m` position `t` with `s ≤ t < reach(σ)` has `t₁ = s_C`: a position with `t₁ > s_C` would exceed `reach(σ)`…"

**Problem**: The step "a position with `t₁ > s_C` would exceed `reach(σ)`" silently assumes `reach(σ)₁ = s_C`, which holds only when the displacement acts below position 1 — i.e. `actionPoint(ℓ) ≥ 2`. But precondition 3 requires only level-uniformity (`#s = #ℓ = m`), and precondition 2's T12 requires only `actionPoint(ℓ) ≤ #s`. A level-uniform span with `actionPoint(ℓ) = 1` is admissible: take `s = [1,1]`, `ℓ = [2,1]` (so `#s = #ℓ = 2`, `actionPoint(ℓ) = 1 ≤ #s`). Then `reach(σ) = s ⊕ ℓ = [3,1]`, and `⟦σ⟧` contains `[2,1]`, a subspace-2 (link) position. The very confinement the precondition claims to guarantee fails, and `A = dom(M(d)) ∩ ⟦σ⟧` can include link positions — exactly the failure mode R6a/R6b call meaningless.

**Required**: Add `actionPoint(ℓ) = #ℓ = m` (ordinal-level displacement) to precondition 3, or otherwise constrain `reach(σ)₁ = s_C`, and rewrite the confinement derivation to invoke that fact explicitly. As written the prefix-`[s_C]` argument does not go through.

### Issue 2: R5 references an undefined symbol and is stated vaguely

**ASN-0105, "Positions that hold nothing" / Claims table (R5)**: "a span whose `reach(σ)` exceeds `max(A) ⊕ δ` for any displacement past the last active position simply contributes the active positions it does cover and stops."

**Problem**: `δ` is never bound — "for any displacement past the last active position" is not a definition, and `max(A)` is undefined when `A = ∅`. The clause reduces to R4 (result keyed on `A`, nothing past the last active position contributes) but dressed in an inequality that has no formal content. A claim in the Claims Introduced table must have a checkable statement.

**Required**: Either give R5 a precise statement (e.g. "if `reach(σ) > max(A)` then `#ρ = |A|` and the last record is `(max(A), M(d)(max(A)))`", guarded by `A ≠ ∅`) or fold it into R4 and drop it as a separate claim.

### Issue 3: No concrete worked example

**ASN-0105, throughout**: The note argues every claim qualitatively but never instantiates one scenario with actual tumbler values.

**Problem**: Per the depth standard, key postconditions must be checked against a specific scenario. The two structurally interesting cases this ASN introduces — self-transclusion (R7: one I-address at two V-positions yielding two records) and a cross-origin boundary (R8: `origin(iaddr(ρ.j)) ≠ origin(iaddr(ρ.{j+1}))`) — are exactly where a reader needs to see the record sequence produced. Without a worked instance (e.g. `d` with `M(d) = {[1,1]↦a, [1,2]↦b, [1,3]↦a}`, read span `([1,1],[0,3])`, show `ρ = ⟨([1,1],a),([1,2],b),([1,3],a)⟩` and verify R0, R3, R7) the claims R7/R8/R9 are asserted but never exhibited.

**Required**: Add one concrete read scenario with tumbler-valued positions/addresses and verify R0–R3, R7, and R8 against the produced sequence.

## OUT_OF_SCOPE

(none — the open questions appropriately defer mixed-subspace reads, historical-version reads, span composition, and out-of-range arithmetic to future ASNs.)

VERDICT: REVISE
