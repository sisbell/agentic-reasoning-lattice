# Review of ASN-0047

I've worked through ASN-0047 carefully — the elementary transitions, the cross-layer invariants, the verification matrix, the K.μ~ link-fixity proof, and the worked examples. The ASN is unusually rigorous: the matrix structure makes every (invariant, transition) preservation explicit, the K.μ~ link-fixity proof carefully distinguishes the per-state CL-UNIQ preservation (Steps 1–3) from the pointwise π = id conclusion (Step 4), and the worked examples actually compute concrete addresses against TA5(c)/TA5(d) and discharge couplings against ran differences rather than waving at them.

I found one substantive issue and several places where the structure is correct but the prose could be sharper.

## REVISE

### Issue 1: Misleading claim about restriction preserving D-CTG★ / D-MIN★

**ASN-0047, "K.μ⁻ admissible contraction shape," reverse direction**: "Otherwise D-SEQ★ applied at the post-state — fired from D-CTG★, D-MIN★, S8-depth, S8-fin, and S8a at Σ', all of which restriction preserves from Σ — gives V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S} for some n'_S ≥ 1 directly."

**Problem**: The phrase "all of which restriction preserves from Σ" is wrong for two of the five invariants listed. Restriction does NOT preserve D-CTG★ or D-MIN★ in general — removing an interior position from V_S(d) violates D-CTG★ at the result; removing the minimum violates D-MIN★. Only S8-depth, S8-fin, and S8a are preserved by arbitrary restriction. In the reverse direction of the equivalence proof, D-CTG★ and D-MIN★ at Σ' are part of the *hypothesis* (the "post-state characterization" the equivalence is establishing), not a derived consequence of restriction.

The proof is sound — the reverse direction correctly assumes the post-state invariants and derives the constructive form. But the prose conflates "preserved by restriction" with "available at the post-state by hypothesis," which obscures what's load-bearing and could confuse readers tracing the proof carefully.

**Required**: Split the two sources cleanly: "S8-depth, S8-fin, and S8a at Σ' are preserved from Σ by restriction (subset of finite set is finite; restriction does not alter components or depth). D-CTG★ and D-MIN★ at Σ' are part of the hypothesis being characterized. D-SEQ★ at Σ' is then derived from these five via the standard D-SEQ★ derivation, giving V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}."

## OUT_OF_SCOPE

None. The ASN is scrupulous about scope: it stops at elementary transitions and named composites without specifying user-level operations like INSERT or COPY, and explicitly lists those as out-of-scope.

VERDICT: REVISE
