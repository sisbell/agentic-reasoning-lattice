# Review of ASN-0042

The mathematical core here is unusually solid: the longest-match definition of `ω` (O2), the refinement regime (O3), irrevocable delegation (O8), and the fork construction (O10) are each carried through with real case work, the inductions cite their base clauses correctly, and the worked example verifies the load-bearing postconditions against concrete addresses. The dependency graph (O4→O2, O18→PrefixBaptismCoupling→SelfOwnership) is acyclic. My findings are almost entirely accretion/meta-prose, which is what this note's `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: ω-conformance-gap paragraph defers downstream and inventories use-sites
**ASN-0042, "Ownership as a Structural Predicate"**: "Those guarantees are therefore abstract obligations that any faithful implementation must discharge, not properties the existing `tumbleraccounteq` already secures; the absence of any `ω`-realizing mechanism in udanax-green is a conformance gap, recorded in the Open Questions."
**Problem**: This paragraph (a) forward-defers to Open Questions, (b) inventories the downstream guarantees that rest on `ω` ("exclusivity (O2), refinement (O3), irrevocable delegation (O8)"), and (c) argues at length about what the implementation does *not* realize. It is justification-about-the-model, not reasoning that advances the definition of `owns`. The single load-bearing fact — `tumbleraccounteq` decides the two-place `owns`, not the selector `ω` — can be stated in one sentence.
**Required**: Collapse to the one-sentence scope fact ("the implementation realizes `owns`; `ω` is an abstract obligation"). Drop the use-site inventory and the Open-Questions pointer.

### Issue 2: the owns/ω distinction is stated twice
**ASN-0042, intro vs. "Ownership as a Structural Predicate"**: intro — "The two-place ownership predicate `owns(π, a)` … reduces to a prefix comparison … The one-place effective-owner function `ω(a)` … must additionally consult the principal registry"; then the structural-predicate section re-derives the same distinction over several sentences.
**Problem**: Two paragraphs in different sections say the same thing in different words — exactly the duplication pattern the anti-bloat classifier targets.
**Required**: State the distinction once (the intro is the right slot) and let the structural-predicate section proceed directly to O1.

### Issue 3: O7(c) duplicated between postcondition prose and Formal Contract, with the same hedge twice
**ASN-0042, O7 postcondition (c)**: "The recursive right is thus established for the entry state `Σ'`; we do not establish it at an arbitrary later delegation state, where an intervening delegation may interpose a more-specific cover of `p''` and falsify (ii)" — and Formal Contract (c): "The claim is restricted to the entry state `Σ'`; satisfiability at an arbitrary later delegation state is not asserted."
**Problem**: The postcondition body, the proof, and the Formal Contract each separately enumerate which of (i)–(v) are discharged and repeat the "entry-state-only" caveat. The Formal Contract is supposed to compress, not restate, the prose.
**Required**: Keep the discharge bookkeeping in the proof only; let postcondition (c) and the Formal Contract state the result (recursive delegation holds at `Σ'`, binding obligations (iii) and (v)) without re-litigating the hedge.

### Issue 4: trailing T3 non-sequiturs after proofs already concluded
**ASN-0042, Covering-chain lemma**: "Hence `pᵢ = qᵢ` for `1 ≤ i ≤ #p`, and `#p ≤ #q`, so `p ≼ q` by the Prefix definition. By T3 (CanonicalRepresentation), the component equalities are well-defined. ∎"
**Problem**: The conclusion `p ≼ q` is already reached on the prior clause; the appended "component equalities are well-defined" was never used in the derivation (the derivation manipulated the equalities directly). The same defensive tail appears in O2 Step 3 ("By T3 … each component `aᵢ` is a uniquely determined natural number"). This is filler that the reader must skip past to confirm the proof actually ended.
**Required**: Delete the trailing T3 sentences; if determinacy of component comparison is genuinely needed, fold it into the one place that consumes it (O1's decidability postcondition) rather than re-asserting it at every prefix proof.

## OUT_OF_SCOPE

### Topic 1: ownership transfer / provenance-vs-effective-owner divergence
**Why out of scope**: Nelson's "bought the document rights" is correctly noted as having no mechanism in the system as specified, and the invariants of transfer are already deferred to Open Questions. Not an error in this ASN.

### Topic 2: cross-node identity federation
**Why out of scope**: O9 establishes node-locality; what a federation layer must satisfy to remain consistent with O9 is genuinely new territory and is already listed as an Open Question.

VERDICT: REVISE
