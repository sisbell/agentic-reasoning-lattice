# Review of ASN-0074

## REVISE

### Issue 1: Worked example invokes M16 without establishing distinct origins

**ASN-0074, Worked Example**: "b ≠ (a+1)+2 since a and b are from distinct allocations — M16, ASN-0058"

**Problem**: M16 requires `origin(a₁) ≠ origin(a₂)` — distinct *document-level prefixes*, not merely distinct allocation events. "Separate allocations" is ambiguous: a single document can perform multiple allocations (successive INSERTs), all producing I-addresses with the same origin. Under that reading, M16 does not apply, and `b = a + 3` is not ruled out. The example's setup says "a, b, c are distinct I-addresses from separate allocations" without stating whether they originate from different documents.

**Required**: State explicitly that `origin(a) ≠ origin(b) ≠ origin(c)` (i.e., the three I-address runs come from three distinct source documents — the scenario where a single document's arrangement contains transcluded content from multiple origins). This is the condition M16 actually checks.

### Issue 2: Width preservation observed but not proved

**ASN-0074, Worked Example**: "Total width: 2 + 2 = 4, matching the span width ℓₘ = 4 of the original content reference."

**Problem**: This states a general property as an example observation without proving it holds universally. The property — that the total resolved width equals the span's ordinal component ℓₘ — is a key structural invariant connecting content references to their resolutions. The proof is short:

1. By C0, `ℓ = δ(ℓₘ, m)`, so `reach(σ) = [u₁, …, u_{m−1}, uₘ + ℓₘ]`.
2. Depth-m tumblers in `[u, reach(σ))` are exactly `{[u₁, …, u_{m−1}, j] : uₘ ≤ j < uₘ + ℓₘ}` — ℓₘ positions (by T1, any depth-m tumbler diverging from `u` before component `m` falls outside the range).
3. Well-formedness gives `|dom(f)| = ℓₘ`.
4. B1 (coverage) + B2 (disjointness) + M0 (width coupling) give `Σ nⱼ = |dom(f)| = ℓₘ`.

**Required**: State and prove as a lemma: for a well-formed content reference `(dₛ, σ)` with `σ = (u, δ(ℓₘ, m))`, `w(resolve(dₛ, σ)) = ℓₘ`.

### Issue 3: C1a reconstruction verifies B3 but omits B1/B2

**ASN-0074, Resolution**: "Each merge step preserves B3: if β₁ = (v₁, a₁, n₁) and β₂ = (v₂, a₂, n₂) each satisfy B3 and M7 holds…"

**Problem**: The reconstruction of M11 for `f` explicitly verifies that the merge step preserves B3 (consistency) but does not address B1 (coverage) or B2 (disjointness). The claim "Both proofs require no property of M(d) beyond S2, S8-fin, and S8-depth" applies equally to B1/B2, but the verification is asymmetric — only B3 is shown. The initial singleton decomposition trivially satisfies B1/B2, and M7f (ASN-0058) establishes that each merge step preserves the full decomposition property (B1, B2, B3 together). Cite M7f for the frame property, or verify: `V(β₁ ⊞ β₂) = V(β₁) ∪ V(β₂)` preserves coverage and disjointness since neither property uses any domain-specific axiom.

**Required**: Either cite M7f explicitly and note it requires no property beyond set-theoretic operations on V-extents, or add B1/B2 preservation as a one-line verification alongside the B3 case split.

## OUT_OF_SCOPE

### Topic 1: D-SEQ simplification of well-formedness

D-SEQ (ASN-0036) establishes that V-positions in a subspace are sequential: `V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}`. Combined with C0, the well-formedness subset condition reduces to a range check: `uₘ ≥ 1 ∧ uₘ + ℓₘ − 1 ≤ n`. This simplification is useful but the current well-formedness definition is correct without it.

**Why out of scope**: The ASN's definitions are correct in their current generality. D-SEQ would add a convenience result, not fix an error.

### Topic 2: Content reference splitting and composition

If a content reference's span is split at an interior point (S4, ASN-0053), do the two sub-references resolve to contiguous subsequences of the original resolution? This invertibility property (analogous to S4a/S3b for spans) would be structurally useful for operations that decompose references.

**Why out of scope**: This is new territory — properties of operations on content references, not an error in their definition.

VERDICT: REVISE
