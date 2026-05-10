# Review of ASN-0051

## REVISE

### Issue 1: SV2/SV3 proof asymmetry — each omits the explicit derivation for one half

**ASN-0051, "Extension Preserves and May Enlarge" / "Contraction May Reduce"**: SV2 provides an explicit proof chain for projection ("`coverage(e) ∩ ran(M'(d)) ⊇ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎`") but asserts the resolution case without derivation ("because every old V-position is preserved... and new V-positions may be added"). SV3 provides an explicit proof for resolution (with ∎) but asserts the projection case without showing the parallel chain — it states "Therefore ran(M'(d)) ⊆ ran(M(d)), and: SV3..." jumping from ran-monotonicity to the π-subset conclusion in a single "and."

**Problem**: The missing steps are elementary (intersection monotonicity from range monotonicity), but SV2 and SV3 are dual results with identical proof structure. Showing the chain explicitly in one and omitting it in the other creates an unmotivated asymmetry. The projection derivation for SV3 — `π_{Σ'}(e,d) = coverage(e) ∩ ran(M'(d)) ⊆ coverage(e) ∩ ran(M(d)) = π_Σ(e,d)`, citing SV1 for coverage invariance and K.μ⁻'s frame for ran-monotonicity — is one sentence, exactly parallel to SV2's. The resolution derivation for SV2 — `let v ∈ resolve_Σ(e,d); then v ∈ dom(M(d)) and M(d)(v) ∈ coverage(e); K.μ⁺ preserves v ∈ dom(M'(d)) with M'(d)(v) = M(d)(v), so v ∈ resolve_{Σ'}(e,d)` — is three steps, exactly parallel to SV3's.

**Required**: Add the explicit derivation chain for SV3 projection (parallel to SV2's) and for SV2 resolution (parallel to SV3's). Each is one to three sentences.

### Issue 2: SV5 resolve proof elides the domain-membership condition

**ASN-0051, "Reordering Preserves Projection, Changes Resolution"**: "v' ∈ resolve_{Σ'}(e, d) iff M'(d)(v') ∈ coverage(e)"

**Problem**: The resolve definition is `{v ∈ dom(M'(d)) : M'(d)(v) ∈ coverage(e)}` — the domain membership is part of the definition. The stated "iff" drops the `v' ∈ dom(M'(d))` conjunct. The next sentence recovers it through the bijection ("Since ψ is a bijection from dom(M(d)) to dom(M'(d)), v' = ψ(v) for a unique v"), so the proof is substantively correct. But the iff statement as written is incomplete — it characterises membership in resolve by a condition on `M'(d)(v')` alone, leaving `v' ∈ dom(M'(d))` implicit.

**Required**: State the iff with the domain condition: "v' ∈ resolve_{Σ'}(e, d) iff v' ∈ dom(M'(d)) and M'(d)(v') ∈ coverage(e)." Then note that the bijection guarantees v' ranges over exactly dom(M'(d)).

## OUT_OF_SCOPE

### Topic 1: Same-origin byte-level coverage stability formalization
**Why out of scope**: The ASN correctly proves cross-origin exclusion (SV6) and explicitly identifies the same-origin byte-level case as depending on allocation discipline assumptions "not formalised in this ASN." The counterexample (child-depth entry via `inc(a, 1)`) demonstrates that same-origin exclusion fails in general. Formalizing the sibling-only discipline for text I-address allocation — and proving that it closes spans to future allocations — is a separate result, likely belonging in a Streams or Allocation Discipline ASN.

### Topic 2: Link-subspace V-positions and non-text projection
**Why out of scope**: SV11 explicitly scopes to `π_text(e, d)` and defers the link-subspace contribution ("deferred to the Link Subspace ASN"). The parenthetical noting that `π_text = π` for all reachable states under the current foundation model is correct — no defined operation creates non-text V-positions. This will need revisiting when the Link Subspace ASN introduces such operations, but it is not an error here.

VERDICT: REVISE
