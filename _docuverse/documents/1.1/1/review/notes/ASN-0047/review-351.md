# Review of ASN-0047

The proof architecture is genuinely rigorous — the D-SEQ★ case split (m=2 / m≥3) is self-contained, the K.μ⁻ contraction-shape equivalence proves both directions, K.μ~ admissibility clause (v) is established as independent via a concrete counterexample, and seven worked examples verify the key postconditions against specific tumbler values (including the duplicate-I-address fork that separates φ-injectivity from range equality). I found no missing-case or unsound-step defects in the verification matrix or the coupling discharges. The findings below are forward-reference / meta-prose accretion, per the anti-bloat directive.

## REVISE

### Issue 1: Use-site inventory embedded in the SSGU proof
**ASN-0047, *NodeRootedForest / SSGU***: "Because this divergence falls at position `#N + 1 ≤ #a'`, a position present in both addresses, it yields not merely distinctness but prefix-incomparability whenever both operands carry an actual component there — **the form CrossNodeAccountBase instantiates below**."

**Problem**: The reasoning of the sentence completes at "prefix-incomparability." The trailing clause is a forward pointer naming a downstream consumer of the result — exactly the "definition/proof introduction enumerates downstream consumers" pattern. A reader following the SSGU argument must skip past it; it advances nothing in SSGU itself.

**Required**: Delete the trailing clause. If the linkage is needed, state it once at the CrossNodeAccountBase site ("this is the SSGU divergence instantiated at the account bases"), not as a back-pointer planted in SSGU.

### Issue 2: Downstream-application note in the ParentAllocatorDispatch statement slot
**ASN-0047, *ParentAllocatorDispatch (sub-lemma)***, Document-level case: "**Applied to the version sub-allocator `A_v(d)` for `d ∈ E_doc`, these two cases identify its parent allocator as `d`'s owning allocator.**"

**Problem**: This sentence sits in the lemma's *postcondition statement*, before the proof, and enumerates a use-site (the K.δ k=1 dispatch consumes (a')/(b') for `A_v(d)`) rather than stating what the lemma guarantees. The same application is then restated where it is actually used (J4's K.δ step, and *K.δ case (ii) discharge*). It is duplicated commentary in the wrong slot.

**Required**: Remove the application note from the lemma statement; the (a')/(b') case analysis is the lemma's content, and the `A_v(d)` instantiation belongs at the consuming dispatch site (where it already appears).

### Issue 3: Cross-lemma contrast commentary around near-identical freshness proofs
**ASN-0047, *ChildSpawnFreshness***: "Note `inc(t, k')` is non-node... **Unlike FrontierEquivalence, no `¬Node(t)` precondition on the operand is needed** — a `k' = 2` descent may be spawned off a node operand." The same contrast recurs in the worked example ("note the operand `1.2` is a node, which ChildSpawnFreshness admits — FrontierEquivalence does not").

**Problem**: ChildSpawnFreshness's proof is the same contrapositive-plus-SSGU structure as FrontierEquivalence's, and the prose repeatedly narrates the *relationship between the two lemmas* rather than the lemma's own content. The relationship commentary is meta-prose a reader must absorb to no deductive gain; the single load-bearing difference (node operands admitted) is already fixed by the precondition `k' ∈ {1,2}` and the non-node observation, which stand on their own.

**Required**: State the node-operand admission once, as a property of ChildSpawnFreshness's own preconditions, and drop the "Unlike FrontierEquivalence…" framing at both occurrences. Do not restate the contrast in the worked example.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
**Why out of scope**: Already correctly deferred to Open Questions — the present K.μ⁻ models only suffix-removal contraction; interior compact-and-renumber (`DELETEVSPAN`) is operation-level mechanics and a future-ASN concern, not a defect here.

VERDICT: REVISE
