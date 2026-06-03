# Review of ASN-0071

The mathematics is sound. I checked the prefix-confinement (PC) proof, the resolve-equivalence derivation, the four-composite worked scenario, the multi-block dedup, the cross-depth subtree capture, and the interior-action-point rejection — all verify. My findings are confined to meta-prose accretion, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Orthogonal axiom invocation in the finiteness proof
**ASN-0071, Finiteness, step (c)**: "SequentialTransitionAxiom (ASN-0047) supplies the orthogonal property that each transition is atomic, uninterruptible, and totally ordered, which makes individual elementary transitions countable within such a sequence."
**Problem**: The prose itself labels this "orthogonal." The finiteness count needs only: finitely many composites, each composite a finite atomic sequence, concatenation of finite sequences is finite. Atomicity/total-ordering is not load-bearing for the count. This is explanation of why an axiom is mentioned rather than a step that advances the argument.
**Required**: Delete the SequentialTransitionAxiom sentence. The count closes on finite ancestry + finite composites alone.

### Issue 2: K.μ~ enumeration clause addresses a case the framing already excludes
**ASN-0071, Finiteness, step (b)**: "The named composite K.μ~ is not atomic; it decomposes into K.μ⁻ + K.μ⁺ (ValidCompositeAmended), both of which appear in the elementary list and fix E, so the induction over elementary steps need not enumerate it separately."
**Problem**: The induction is explicitly "over elementary steps." K.μ~ is by definition not elementary, so it is already outside the induction's index set. Explaining that it "need not be enumerated separately" defends against an objection the elementary-only framing has already foreclosed — reviser drift imagining a case the precondition excludes.
**Required**: Drop the clause; the induction over the elementary list is self-contained.

### Issue 3: "no appeal to well-formedness" repeated across three slots
**ASN-0071, The query / PC table row / Resolution**: the same defensive note recurs — "recovered from `actionPoint(ℓ) = #u` and `#u ≥ 2` without any appeal to well-formedness"; "it holds with no appeal to well-formedness"; PC row "holds without ContentReference well-formedness, so it does not rest on ASN-0058's C0a"; Resolution "(proven directly from PC, with no appeal to S3★-aux)".
**Problem**: The point that PC does not depend on ContentReference well-formedness is established once where PC is proven. Restating it in the table row and again in Resolution is redundant defensive prose the precise reader must skip past.
**Required**: State it once at the PC proof; remove the duplicate assertions in the table row and Resolution.

### Issue 4: Unmodeled formation-state/evaluation-state distinction
**ASN-0071, The operation, well-definedness precondition**: "The vspec clause `d_s ∈ Σ.E_doc` is a constraint on well-formedness *at the source state at which the vspec was formed*; the precondition above binds that constraint to the *evaluation state* `Σ`. The two coincide whenever `Q` is formed at a state no later than `Σ`..."
**Problem**: The vspec definition is just the pair `(d_s, σ)` with `d_s ∈ Σ.E_doc`; there is no "formation state" as a modeled object. This paragraph introduces a temporal scenario the formal definitions do not carry, then reassures the reader via P1. The operative content is simply: `find` requires `d_s ∈ Σ.E_doc` at the evaluation state.
**Required**: Reduce to the precondition statement; drop the formation-state narrative or, if forward-preservation is worth keeping, compress to one clause citing P1.

## OUT_OF_SCOPE

The Open Questions section already captures the future topics (historical-`R` reconciliation, rejection policy, distributed completeness, visibility filtering, contraction invariants). No additional out-of-scope topics to surface.

VERDICT: REVISE
