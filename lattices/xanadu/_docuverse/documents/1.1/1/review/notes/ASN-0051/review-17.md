# Review of ASN-0051

## REVISE

### Issue 1: Worked example does not verify SV6 (CrossOriginExclusion)

**ASN-0051, Worked Example**: The worked example operates entirely within a single document origin. SV6 is the ASN's most involved non-trivial claim — a multi-step sandwich argument establishing that element-level tumblers inside a span interval inherit the span start's field-separator positions, forcing `origin(t) = origin(s)`. This argument turns on the interaction between TumblerAdd's position-copying behavior, the action-point precondition `k > p₃`, and the element-level zero-count constraint. None of this machinery is exercised by the example.

**Problem**: The proof is correct on paper, but without a concrete cross-origin scenario, the precondition `k > p₃` is never instantiated with specific tumbler values, and the field-separator alignment is never demonstrated against a concrete counterexample candidate.

**Required**: Add a cross-origin scenario to the worked example. For instance:
- Let `s = 1.0.1.0.1.0.1.2.3` (nine components; field separators at positions 2, 4, 6; so `p₃ = 6`).
- Let `ℓ = 0.0.0.0.0.0.0.0.5` (action point `k = 9 > 6 = p₃`).
- Verify `reach = s ⊕ ℓ = 1.0.1.0.1.0.1.2.8`.
- Show a same-origin address `t = 1.0.1.0.1.0.1.2.5` lies in the span and has `origin(t) = 1.0.1.0.1 = origin(s)`.
- Show a cross-origin address `b = 1.0.1.0.2.0.1.2.5` (`origin(b) = 1.0.1.0.2 ≠ origin(s)`) satisfies `b > reach` (since `b₅ = 2 > 1 = reach₅`), hence `b ∉ ⟦(s, ℓ)⟧`.

This makes the field-separator alignment visible and verifies the precondition in practice.

### Issue 2: SV7 formal content understates its claimed insight

**ASN-0051, SV7 (TransclusionCouplingAbsence)**: "Formally, the monotonicity result `discover_s({a}) in Σ ⊆ discover_s({a}) in Σ'` is a direct corollary of SV8 instantiated with `A = {a}`."

**Problem**: The label promises "coupling absence" — that K.μ⁺ alone suffices, requiring no link-store mutation. The formal content is `⊆` (monotonicity), which is consistent with new links appearing. But for a K.μ⁺ transition specifically, L is in the frame (`L' = L`), so `discover_s(A)` is *invariant* (`=`), not merely monotonically non-decreasing. The `⊆` formulation, while correct, is weaker than what the coupling-absence claim asserts. The prose at the end of SV7 correctly argues the equality through the frame condition, but the formal statement should match.

**Required**: State SV7's formal content as equality for K.μ⁺: `discover_s(A) in Σ' = discover_s(A) in Σ` for all `A`, when `Σ → Σ'` is a K.μ⁺ or K.μ⁺_L transition. This follows from K.μ⁺'s frame preserving L (`dom(L') = dom(L)` and `L'(a) = L(a)` for all `a`), so coverage is identical in both states, and dom(L) is unchanged. The stronger equality captures the coupling-absence: K.μ⁺ introduces no new discovery relationships and removes none.

### Issue 3: SV6 proof — first-divergence reasoning is implicit

**ASN-0051, SV6 proof, `#t ≥ k` sub-argument**: "or t diverges from s at some `j ≤ #t` with `tⱼ > sⱼ`. Since `j ≤ #t < k`, we have `(s ⊕ ℓ)ⱼ = sⱼ`..."

**Problem**: The inequality `tⱼ > sⱼ` follows from T1(i) only at the *first* position of divergence. The proof says "diverges from s at some j" without specifying j is the first such position, then invokes T1 "at the first point of disagreement" in a parenthetical. The same elision recurs in the main agreement claim ("For suppose t diverges from s at position `j < k`. Then `tⱼ ≠ sⱼ`. Since `t ≥ s`, we have `tⱼ > sⱼ`"). In both places, the T1 application requires j to be the first divergence, and the comparison of t with `s ⊕ ℓ` requires confirming that t and `s ⊕ ℓ` also agree on positions `1..j−1` (which they do, since both agree with s there).

**Required**: In both the `#t ≥ k` sub-proof and the main agreement claim, explicitly state "let j be the *first* position where `tⱼ ≠ sⱼ`" before invoking T1(i). In the comparison with `s ⊕ ℓ`, note explicitly: "since t agrees with s on positions `1..j−1` and `(s ⊕ ℓ)` agrees with s on positions `1..k−1` (with `j−1 < k−1`), the first divergence of t and `s ⊕ ℓ` is at j."

## OUT_OF_SCOPE

### Topic 1: Same-origin byte-level coverage closure
**Why out of scope**: The ASN correctly identifies that byte-level closure depends on allocation discipline ("sequential sibling allocation closes existing spans to future allocations") not formalized in this or any current ASN. This is an allocation-regime property, not a link-survivability property. A future ASN on allocation discipline could formalize this.

### Topic 2: Link-subspace contribution to endset projection
**Why out of scope**: The ASN explicitly defers `π(e, d) \ π_text(e, d)` — the link-subspace I-addresses reachable through link-subspace V-positions — to the Link Subspace ASN. SV11 restricts to text-subspace fragments. The distinction between π and π_text is clearly stated.

### Topic 3: Fragment ordering and normalization
**Why out of scope**: The open questions list "canonical ordering of fragments" as future work. The current ASN establishes existence and finite decomposition (SV11) without imposing ordering constraints. Ordering is a representation concern for a future ASN.

VERDICT: REVISE
