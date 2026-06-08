# Review of ASN-0102

The correctness work here is genuinely strong: the X16 tiling argument is exhaustive across all three position classes and both boundary cases, the worked examples exercise the discriminating predicates of X8/X12 firing *and* failing, and the invariant discharge in X14 is comprehensive. My findings are confined to accreted meta-prose and one duplication, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: "A remark on what COPY is" is taxonomy essay that duplicates the Definition and pulls in out-of-scope operations
**ASN-0102, "A remark on what COPY is"**: "content creation grows both stores; deletion shrinks reach without touching the store; rearrangement permutes within fixed reach; and the two reference-importing acts — K.μ⁺ and COPY — both grow reach over existing content... What separates COPY from K.μ⁺ is the *displacement*: K.μ⁺ extends only where it leaves every incumbent mapping fixed (`M'(d)(v) = M(d)(v)`), whereas COPY relabels the content subspace at or after `v` by the forward shift `· + W`..."
**Problem**: The displacement-vs-K.μ⁺ distinction is already stated in the Definition ("It is deliberately *not* an instance of K.μ⁺... which requires `M'(d)(v) = M(d)(v)` on every pre-existing V-position; COPY *relabels*... by the forward shift `· + W`"). The remark restates it in different words — the "two paragraphs say the same thing" pattern. The surrounding taxonomy ("deletion shrinks reach," "rearrangement permutes") narrates the mechanics of operations declared out of scope. The one genuinely new observation (K.μ⁺ also grows reach without growing the store) is a single sentence buried in an essay.
**Required**: Delete the taxonomy of deletion/rearrangement. If the K.μ⁺-shares-reach-growth observation is worth keeping, fold it into the Definition's existing K.μ⁺ contrast as one sentence rather than a standalone section.

### Issue 2: Scope-deferral meta-prose and a duplicated `Σ.R`-vs-`Contains_C` explanation
**ASN-0102, Definition**: "we specify it here only as far as needed to state COPY's invariants; its position-management mechanics are not the subject of this note. What *is* the subject is the half of the definition that distinguishes COPY..."
**ASN-0102, Definition** ("This is a state component distinct from the *derived* containment relation `Contains_C`... the provenance relation `Σ.R` records the fact persistently") **and X14** ("As the Definition established, this derived containment is automatic while the provenance relation `Σ.R` is the separate persistent record...").
**Problem**: The first quote is scope-deferral prose that does not advance reasoning ("not the subject of this note"). The `Σ.R`-vs-`Contains_C` distinction is explained once in the Definition's Provenance clause and re-explained in X14's opening — the same content twice.
**Required**: Drop the "not the subject of this note" framing; the displacement effect is fully specified, so no apology is needed. State the `Σ.R`/`Contains_C` distinction once (in the Definition) and have X14 simply cite it.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content, further-reference containment, time-varying views, identity after allocator unreachability
**Why out of scope**: The four Open Questions correctly point to material for future ASNs (subsequent-operation interaction, transitive containment, temporal view divergence, garbage-collection/reachability). They are properly posed as questions, not claims, and belong downstream.

VERDICT: REVISE
