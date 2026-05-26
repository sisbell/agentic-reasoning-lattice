# Review of ASN-0077

## REVISE

### Issue 1: Implicit cross-state depth identification in O11 sub-case (a)
**ASN-0077, O11 derivation, (⊇) direction, Sub-case (a)**: "By S8-depth (ASN-0036) on `d`'s content subspace, every position in `V_{s_C}(d) ⊆ dom(M'(d))` shares the common depth — equal to `m` by precondition (v)'s definition of `m` as `d`'s common depth in subspace `u₁ = s_C`."
**Problem**: `m` is defined at Σ via precondition (v), but the common depth invoked here is read at Σ' (note the `V_{s_C}(d) ⊆ dom(M'(d))`). The identification "common depth at Σ' = m" requires K.μ⁺'s extension to preserve a nonempty subspace's common depth. The step is sound (V_{s_C}(d) at Σ is nonempty by precondition (iii) with depth m; V_{s_C}(d) at Σ ⊆ V_{s_C}(d) at Σ'; S8-depth at Σ' must accommodate the pre-state positions), but elided. The same elision recurs in O11' sub-case (b) at `m = m_L = 2`.
**Required**: Spell out the cross-state depth identification — cite S8-depth at both Σ and Σ' and note that K.μ⁺'s post-state S8-depth obligation forces the post-state common depth to coincide with the pre-state value when the subspace was nonempty at Σ.

### Issue 2: Implicit zero-position argument in singleton I-span case `#b > #a`
**ASN-0077, Edge cases, "Singleton I-span", case `#b > #a`**: "Combined with `b` extending `a` structurally — `a` agrees with `b` on all positions `1, ..., #a` — the document-level prefix `N(b).0.U(b).0.D(b)` is computed from positions of `b` that already lie within `a`, so it coincides with `N(a).0.U(a).0.D(a)`."
**Problem**: The assertion that b's document-level prefix lies within positions 1..#a requires a zero-count balance argument that is omitted. The full chain: a has 3 zeros (S7b) all within positions 1..#a since #a is a's length; b has 3 zeros total (S7b); agreement on 1..#a forces b's three zeros to coincide positionally with a's; therefore b has no zero beyond position #a, and the document-element separator (third zero) of b is at the same position as a's. Without this step, the coincidence of document-level prefixes is asserted but not derived.
**Required**: Insert the zero-balance step: since `zeros(a) = zeros(b) = 3`, a's three zeros lie within positions 1..#a, b agrees with a on those positions so b's three zeros coincide with a's, and b has no zero in positions #a+1..#b — therefore b's third zero (the document-element separator) is at a's third-zero position, making the document-level prefixes identical.

## OUT_OF_SCOPE

The Open Questions section already enumerates the natural follow-ups (I-span lift for link addresses, intermediate-chain visibility operation, native-vs-transcluded distinction, source-unreachability handling, historical containment via Σ.R, intra-document sharing reporting). These are appropriately marked for future ASNs. No additional OUT_OF_SCOPE items to flag.

VERDICT: REVISE
