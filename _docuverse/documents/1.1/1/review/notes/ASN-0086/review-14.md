# Review of ASN-0086

## REVISE

### Issue 1: Worked Sketch's L1c verification misidentifies the allocator producing link addresses
**ASN-0086, Worked Sketch, "L-invariant verification at the concrete b₁"**: "L1c (LinkAllocatorConformance): `b₁ = inc(a₁, 0)` extends the same depth-1 allocator `A_d` (rooted at `1.0.1.0.1.0.1`) that produced `a₁`..."

**Problem**: A_d (rooted at d.0.1 = 1.0.1.0.1.0.1) is the depth-1 element-field allocator; its domain is {d.0.1, d.0.2, d.0.3, ...} — siblings of length 7 emitted via inc(·, 0). a₁ = 1.0.1.0.1.0.2.1 has length 8 and is NOT in A_d's domain. a₁ is in the depth-2 element-field allocator (call it A_{a₁}) rooted at a₁, which is spawned by inc(d.0.2, 1) — step (iii) of a₁'s chain construction. b₁ = inc(a₁, 0) is the next sibling of a₁ in A_{a₁}'s sibling stream, not in A_d's stream. The claim that A_d "produced a₁" is incorrect, and "extends the same depth-1 allocator A_d" is wrong about which allocator b₁'s inc(·, 0) step operates in.

**Required**: Correct the worked sketch to name the depth-2 allocator (e.g., A_{a₁} with base a₁ = d.0.s_L.1 = 1.0.1.0.1.0.2.1). Also review R0 Step 2 Case A's parallel description "the L1c chain from d to a describes a walk through the depth-1 element-field allocator A_d" — the chain walks through A_d's domain (steps i–ii) and then spawns into the depth-2 allocator via step (iii); the target a is in the *spawned* allocator, not in A_d. A naming convention based on the allocator's base address (A_{base}) would prevent this confusion across both passages. The sibling-stream invariant in R0a is correctly stated in terms of `home(a).0.s_L.1` as the base, but the prose elsewhere drifts to "A_d", muddling which allocator hosts the link addresses.

### Issue 2: Emit_K's signature is functional but its definition is non-deterministic in home-document choice
**ASN-0086, Definition of Emit_K**: "`Emit_K : Σ × Endset × Endset → Σ' × A_rel^{Σ'}`... `Emit_K(Σ, F, G)` deposits a fresh tuple at an address constructed by R0 Step 2's sibling-frontier construction: pick any `d ∈ dom(Σ.M)`..."

**Problem**: The signature describes Emit_K as a function from (Σ, F, G) to (Σ', A_rel^{Σ'}), but "pick any d ∈ dom(Σ.M)" makes Emit_K non-deterministic — different home-document choices yield different (Σ', a) outcomes for the same input. More substantively, callers cannot express "create a link in document d_1 specifically" through Emit_K alone; the home determines L1a binding (and through it, the link's sub-tree placement, retraction reachability, type-catalog membership in any document-scoped layering, etc.). The Worked Sketch implicitly fixes a single document, but the abstract spec leaves home selection inexpressible.

**Required**: Either (a) add a home-document parameter to Emit_K's signature: `Emit_K : Σ × DocAddr × Endset × Endset → Σ' × A_rel^{Σ'}` with precondition `d ∈ dom(Σ.M)`; or (b) explicitly state that Emit_K is a *relation* rather than a function and adjust the signature notation accordingly; or (c) introduce a substrate-level home-selection policy (caller-provided context, most-recently-allocated, etc.) and document the chosen rule. Whichever option is selected, the worked sketch's idiomatic usage (where home is fixed implicitly) should align with the formal interface.

### Issue 3: Nullify's single-tuple-scope is implicitly conditional on substrate-wide discipline adherence
**ASN-0086, "Substrate emission primitive" paragraph**: "The substrate admits, as its primitive emission for the link store, *emit-at-any-L1c-conforming-fresh-address*..."
**ASN-0086, Nullify "Remark on the role of P3"**: "without the emission discipline supplying the post-state antichain, P3 alone is insufficient to discharge single-tuple-scope."

**Problem**: Nullify's correctness conclusion (single-tuple-scope) depends on R0a's antichain, which is discipline-conditional. Emit_K's definition binds itself to the discipline by construction, but the substrate emission primitive described above Emit_K is broader — it admits emissions at strict prefix-extensions of existing link addresses (e.g., a' = a₁.1), which R0a's antichain would not cover. The substrate spec does not explicitly mandate that Emit_K is the *only* operation extending dom(L); a future operation using the broader primitive could break R0a, after which Nullify could over-retract (the coverage `{t : a ≼ t}` would include prefix-extensions in dom(L) beyond a itself). The Remark identifies the dependency but does not propagate it to Nullify's specification.

**Required**: Make Nullify's discipline-dependence explicit at the operational layer. Options: (a) state in Nullify's definition that its single-tuple-scope conclusion assumes all link-store extensions in the system's history have respected the discipline; (b) elevate the discipline to a substrate-level guarantee (per the Open Questions item) — e.g., by tightening the substrate primitive to forbid emissions at strict prefix-extensions of existing link addresses — which makes R0a unconditional and Nullify automatic; or (c) introduce a defensive variant that verifies the post-state antichain at the affected slice before committing the retraction. As stated, the safety of Nullify is contingent on a substrate property (no undisciplined emissions) that the spec does not commit to.

## OUT_OF_SCOPE

None. The Open Questions section properly defers further substrate-level questions, including higher-arity active subsets, concurrent semantics, slice-wise reformulation under L14's native form, and the discipline-elevation question that overlaps with Issue 3.

VERDICT: REVISE
