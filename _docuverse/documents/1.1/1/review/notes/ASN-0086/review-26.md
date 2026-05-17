# Review of ASN-0086

## REVISE

### Issue 1: Subspace-distinctness axiom framing
**ASN-0086, Setup section, "Subspace-distinctness — named explicitly"**: "This is *not* an additional axiom adopted by this note — it is implicit in ASN-0043's machinery and is structurally required by it."

**Problem**: The argument for why s_C ≠ s_L is "not an axiom" rests on a meta-argument that ASN-0043's machinery would be vacuous (L14's scoped disjointness would collapse to unconditional disjointness; L0a's slice would collapse to all of dom(Σ.C)) if s_C = s_L. This is a non-vacuity argument, not a derivation. The foundation ASNs (per the provided foundation excerpts: L0, L0a, L14 in ASN-0043; subspace_I in ASN-0036) introduce s_C and s_L as named constants but do not formally state their distinctness. ASN-0086 then uses s_C ≠ s_L as a load-bearing fact at multiple sites: R0 Step 4's L14 and L14a preservation bullets, R4's reduction of L14's scoped form to substrate-wide disjointness, Nullify's "no content address lies under a" argument, and indirectly R5 (via R0). Calling something "not an axiom" while treating it as one is slippery framing.

**Required**: Either (a) acknowledge s_C ≠ s_L explicitly as a new axiom or hypothesis of ASN-0086 — perhaps stated parallel to the globally-`s_C`-resident-content hypothesis in the Setup section — or (b) provide a formal derivation showing the foundation ASNs entail s_C ≠ s_L. The current "named explicitly" framing should not equivocate between these two options.

## OUT_OF_SCOPE

### Topic 1: Higher-arity active subsets
**Why out of scope**: The note explicitly restricts L_K to standard-triple links (`|Σ.L(a)| = 3`) and acknowledges higher-arity links exist in dom(Σ.L) but lie outside the active-subset machinery. Open Question 2 raises whether to define `A_K^{(n)}` for higher arities. Genuine future work.

### Topic 2: Lifting the Setup hypothesis to slice-wise formulation
**Why out of scope**: Setup (globally s_C-resident content) is acknowledged as strong. Open Question 7 traces the slice-wise reformulation under L14's native scoped form (with implications for R0, R4, R5). Distinct refactoring effort.

### Topic 3: Elevating the sibling-frontier discipline to a substrate guarantee
**Why out of scope**: R0a is discipline-conditional; the conditionality is consistently tagged. Open Question 8 raises whether to tighten Emit_K's specification or the substrate emission primitive to make R0a unconditional, which would discharge Nullify's P3 automatically. Substrate-design decision.

### Topic 4: Relaxing the discipline to admit deeper-sited links
**Why out of scope**: R0a-Cor2 narrows L1b's `#E ≥ 2` admission to `#E = 2` strictly. Open Question 9 raises whether to relax this to admit Nelson's foundational depth-N sub-link design (requiring tree-of-allocators reformulation of R0a). Substantive design decision.

### Topic 5-10: Various Open Questions
**Why out of scope**: Cardinality bounds on nullified(Σ) (Open Question 6), ordering on Observe results (Open Question 4), atomicity for concurrent Emit/Observe (Open Question 5), invariants relating L_K to arrangements (Open Question 1), dynamic type catalog extension (Open Question 10), operational meaning of Nullify(b) for b ∈ L_R (Open Question 3). Each is a coherent future-ASN topic, properly flagged in the note's Open Questions section.

VERDICT: REVISE
