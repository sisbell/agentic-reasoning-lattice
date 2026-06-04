# Review of ASN-0076

## REVISE

### Issue 1: Worked-example E0 check re-runs the abstract proof instead of checking concrete values

**ASN-0076, A Worked Example, "E0." paragraph**: "K.λ's preconditions were discharged for both steps in the trace above. Step 1 invoked the first-emission case … SubAllocatorBundle furnished `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)` … Step 2 invoked the subsequent-emission … SubAllocatorBundle's T10a-conformance + L11a gave `ℓ_sup ∉ dom(L_1)` …"

**Problem**: The worked example's stated purpose is to verify postconditions against concrete tumblers. But this E0 check restates the entire foundation-citation chain a third time — it is verbatim the abstract E0 proof, and the concrete `Σ → Σ_1 → Σ_2` trace immediately above it already discharged the same preconditions against the concrete values. Three copies of one argument (E0 proof, trace, E0 check) is accretion the reader must skip past.

**Required**: Reduce the E0 check to what the example uniquely contributes — confirming the concrete addresses `ℓ_new = [4.0.2.0.3.0.2.1]`, `ℓ_sup = [4.0.2.0.3.0.2.2]` satisfy the namespace/L3 clauses — and cite E0 for the general discharge rather than re-listing every lemma.

### Issue 2: E2 proof carries editorial meta-prose in a proof slot

**ASN-0076, E2 proof**: "The result is foundational." and "The conclusion does not depend on any property of EDITLINK beyond its consisting of two K.λ steps."

**Problem**: Neither sentence advances the derivation. The first is filler; the second is a use-site/scope remark of the kind the anti-bloat pass targets. The actual argument (three distinct K.λ events → L11a → pairwise distinct addresses) stands without them.

**Required**: Delete both sentences. If the scope observation is load-bearing for a downstream claim, move it to that claim rather than leaving it as commentary here.

### Issue 3: E4 re-derives the two-step adjacency that E0 already established

**ASN-0076, E0 ("We must observe the adjacency of the two steps…") and E4 ("EDITLINK's composite consists of exactly two K.λ steps with no further atomic transitions intervening: this is the composite definition together with ValidComposite★, which fixes a composite as the literal finite sequence … Instantiated at `n = 2` …")**

**Problem**: E0 already proves, via SequentialTransitionAxiom and ValidComposite★, that the composite is the contiguous sequence `Σ → Σ_1 → Σ'` with no transition intervening. E4 reconstructs the same fact from the same two sources in different words to obtain `Σ' = Σ_2`. Two paragraphs asserting the same thing.

**Required**: In E4, cite E0's adjacency conclusion (`Σ' = Σ_2`) directly and proceed to the L6 slot-accessor step, rather than re-deriving the sequence structure from ValidComposite★.

## OUT_OF_SCOPE

### Topic 1: Discoverability/wp of the supersession link
E7 notes `ℓ_sup` is orphaned absent independent arrangement (LP17/LP18, ASN-0098). A weakest-precondition analysis for "`ℓ_sup` discoverable from `d_new`" is genuinely non-trivial, but EDITLINK claims no discoverability-preservation postcondition, so no wp is *missing* here — it belongs with arrangement operations, not this allocation composite.

### Topic 2: Supersession-chain invariants, cycles, retraction, authorization of `d_new`
The Open Questions and E6's application-layer note correctly defer these to future ASNs; they are new territory, not gaps in this one.

VERDICT: REVISE
